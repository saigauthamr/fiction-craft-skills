#!/usr/bin/env python3
"""Adopt a writer's existing material into a Story project. Standard library only.

  adopt.py plan  <project> [--json plan.json]   read-only: show what would be imported
  adopt.py apply <project> <plan.json> --yes     do it (refuses without --yes)
  adopt.py review <project>                      list imported pages still marked needs review

Originals are never modified, moved, or deleted: everything is copied or converted
into new files. Each item is recorded in work/adopt/provenance.md with its source
hash, method, and status. Re-running skips what is imported, retries what failed,
and imports a changed source as a new version beside the old one. Each file is
written to a temporary name and moved into place, so a failure leaves nothing half
written. apply exits 5 if some items failed (the rest are imported).

Adopt does not write the project's settings; story-onboard does that afterward.
"""
import csv
import hashlib
import io
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path

SKIP_TOP = {"kb", "work", ".git", ".claude", ".agents", ".gemini", ".codex", ".hermes", ".venv", "node_modules", "__pycache__"}
DOC_EXT = {".docx", ".odt", ".txt", ".md", ".markdown"}
SHEET_EXT = {".xlsx", ".csv"}
UNSUPPORTED = {".doc": "old Word format", ".rtf": "rich text", ".pdf": "PDF", ".xls": "old Excel format",
               ".ods": "OpenDocument spreadsheet", ".pages": "Pages", ".numbers": "Numbers", ".scriv": "Scrivener project"}
INSTRUCTION_FILES = {"agents.md", "claude.md", "readme.md", "gemini.md"}
START = "<!-- story-project:start"
CHAPTER_RE = re.compile(r"(chapter|chap|\bch)[\s_\-]*\d+|\bscene\b|\bdraft\b", re.I)
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def sha1(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "untitled"


# ---------- readers (standard library only) ----------

def read_docx(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    out = []

    def para(p):
        style = p.find(f"{W}pPr/{W}pStyle")
        level = 0
        if style is not None:
            m = re.match(r"(?:Heading|Title)(\d?)", style.get(f"{W}val", ""))
            if m:
                level = int(m.group(1) or 1)
        parts = []
        for el in p.iter():
            if el.tag == f"{W}t":
                parts.append(el.text or "")
            elif el.tag == f"{W}tab":
                parts.append("\t")
            elif el.tag in (f"{W}br", f"{W}cr"):
                parts.append("\n")
        text = "".join(parts).rstrip()
        return ("#" * min(level, 3) + " " + text) if (level and text) else text

    body = root.find(f"{W}body")
    for el in (body if body is not None else []):
        if el.tag == f"{W}p":
            out.append(para(el))
        elif el.tag == f"{W}tbl":
            for tr in el.iter(f"{W}tr"):
                cells = [" ".join(para(p) for p in tc.iter(f"{W}p")).strip() for tc in tr.iter(f"{W}tc")]
                out.append("| " + " | ".join(cells) + " |")
    return re.sub(r"\n{3,}", "\n\n", "\n\n".join(x for x in out if x is not None)).strip() + "\n"


def read_odt(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("content.xml"))
    ns = "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}"
    paras = ["".join(p.itertext()).strip() for p in root.iter() if p.tag in (f"{ns}p", f"{ns}h")]
    return "\n\n".join(p for p in paras if p) + "\n"


def read_text(path):
    return Path(path).read_text(encoding="utf-8", errors="replace")


def _col_index(ref):
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def read_xlsx(path):
    """Return {sheet name: list of rows (lists of str/number/None)}."""
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        shared = []
        if "xl/sharedStrings.xml" in names:
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(f"{S}si"):
                shared.append("".join(t.text or "" for t in si.iter(f"{S}t")))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).iter(f"{PR}Relationship")}
        sheets = {}
        for sh in wb.iter(f"{S}sheet"):
            target = rels.get(sh.get(f"{R}id"), "")
            target = target.lstrip("/")
            target = target if target.startswith("xl/") else "xl/" + target
            if target not in names:
                continue
            rows = []
            for row in ET.fromstring(z.read(target)).iter(f"{S}row"):
                cells = {}
                for c in row.iter(f"{S}c"):
                    v = c.find(f"{S}v")
                    t = c.get("t")
                    if t == "inlineStr":
                        val = "".join(x.text or "" for x in c.iter(f"{S}t"))
                    elif v is None or v.text is None:
                        continue
                    elif t == "s":
                        val = shared[int(v.text)]
                    elif t in ("str", "e"):
                        val = v.text
                    elif t == "b":
                        val = "TRUE" if v.text == "1" else "FALSE"
                    else:
                        num = float(v.text)
                        val = int(num) if num == int(num) else num
                    cells[_col_index(c.get("r"))] = val
                if cells:
                    width = max(cells) + 1
                    rows.append([cells.get(i) for i in range(width)])
            sheets[sh.get("name")] = rows
    return sheets


def read_csv_sheet(path):
    text = read_text(path)
    rows = []
    for r in csv.reader(io.StringIO(text)):
        if any(x.strip() for x in r):
            rows.append([_num(x) for x in r])
    return {Path(path).stem: rows}


def _num(x):
    x = x.strip()
    if x == "":
        return None
    try:
        f = float(x)
        return int(f) if f == int(f) and "." not in x else f
    except ValueError:
        return x


# ---------- sheet classification and rendering ----------

def classify_sheet(rows):
    if not rows:
        return "empty"
    header = " ".join(str(c).lower() for c in rows[0] if c is not None)
    words = set(re.findall(r"[a-z]+", header))
    if words & {"words", "wordcount"} or "word count" in header:
        return "wordcount"
    if words & {"date", "year", "when", "era", "period"} and words & {"event", "events", "what", "happened", "description", "note", "notes"}:
        return "timeline"
    if "name" in words and words & {"role", "age", "born", "relationship", "trait", "traits", "faction", "description", "occupation"}:
        return "characters"
    body = [c for r in rows[1:] for c in r if c is not None]
    if body and sum(isinstance(c, (int, float)) for c in body) / len(body) >= 0.5:
        return "numbers"
    return "unknown"


def to_markdown_table(rows, date_cols=()):
    width = max(len(r) for r in rows)
    out = []
    for i, r in enumerate(rows):
        cells = []
        for j in range(width):
            v = r[j] if j < len(r) else None
            if v is None:
                v = ""
            elif j in date_cols and i > 0 and isinstance(v, (int, float)) and 20000 < v < 80000:
                v = (date(1899, 12, 30) + timedelta(days=int(v))).isoformat()
            cells.append(str(v).replace("|", "\\|").replace("\n", " "))
        out.append("| " + " | ".join(cells) + " |")
        if i == 0:
            out.append("|" + "---|" * width)
    return "\n".join(out) + "\n"


def to_csv_text(rows):
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows([["" if c is None else c for c in r] for r in rows])
    return buf.getvalue()


# ---------- project inspection ----------

def project_files(root):
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if p.is_file() and rel.parts[0] not in SKIP_TOP and not p.name.startswith("."):
            yield p


def describe_existing(root):
    kb = root / "kb"
    pages = [f for f in kb.rglob("*") if f.is_file() and f.name not in (".gitkeep", "vocab.md")] if kb.is_dir() else []
    instr = next((n for n in ("AGENTS.md", "CLAUDE.md") if (root / n).is_file()), None)
    has_section = bool(instr) and START in (root / instr).read_text(encoding="utf-8")
    register = None
    if kb.is_dir():
        for f in kb.rglob("open-questions*.md"):
            register = str(f.relative_to(root))
            break
    outline = [f for f in (root / "work" / "outline").rglob("*") if f.is_file() and f.name != ".gitkeep"] if (root / "work" / "outline").is_dir() else []
    tools = [d for d in (".claude", ".agents", ".gemini", ".codex", ".hermes", ".git") if (root / d).exists()]
    return {"instructions_file": instr, "section_present": has_section, "kb_pages": len(pages),
            "open_questions_register": register, "outline_files": len(outline), "tool_folders_left_alone": tools}


LEDGER = "work/adopt/provenance.md"
LEDGER_HEAD = ("# Import provenance\n\nEvery file below was created from an original that was left untouched. "
               "Re-running Adopt skips rows marked imported and retries the rest.\n\n"
               "| Created file | Original | Original sha1 | Part | Method | Status | Imported |\n|---|---|---|---|---|---|---|\n")


def ledger_rows(root):
    """(origin, sha1, part, status) for every ledger row; first-build rows (no status column) count as imported."""
    led = root / LEDGER
    rows = []
    if led.is_file():
        for line in led.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 5 or not re.fullmatch(r"`[0-9a-f]{40}`", cells[2]):
                continue
            status = cells[5] if len(cells) >= 7 else "imported"
            rows.append((cells[1].strip("`"), cells[2].strip("`"), cells[3], status))
    return rows


def ledger_hashes(root):
    return {(o, h, part) for o, h, part, status in ledger_rows(root) if status == "imported"}


def imported_parts(root):
    """{(origin, part): sha1} for everything imported, to spot sources that changed since."""
    return {(o, part): h for o, h, part, status in ledger_rows(root) if status == "imported"}


# ---------- plan ----------

def build_plan(root):
    items, skipped, taken = [], [], set()
    done = ledger_hashes(root)

    def dest_for(base, ext=".md"):
        d = base + ext
        n = 2
        while (root / d).exists() or d in taken:
            d = f"{base}-{n}{ext}"
            n += 1
        taken.add(d)
        return d

    existing = describe_existing(root)
    earlier = imported_parts(root)
    bases = {}

    def note_changes(rel, part, digest, it):
        old = earlier.get((rel, part))
        if old and old != digest:
            it["note"] += "; changed since it was last imported, so this is a new version beside the old one"
            it["changed"] = True
        base = it["dest"].rsplit(".", 1)[0]
        base = re.sub(r"-\d+$", "", base)
        if base in bases:
            it["note"] += f"; same name as `{bases[base]}`, so it gets its own file"
        bases.setdefault(base, it["origin"] + (f" [{part}]" if part != "document" else ""))

    for p in project_files(root):
        rel = str(p.relative_to(root))
        ext = p.suffix.lower()
        if p.name.lower() in INSTRUCTION_FILES:
            continue
        if ext in UNSUPPORTED:
            skipped.append({"origin": rel, "reason": f"{UNSUPPORTED[ext]} is not supported; left in place. Export it to .docx, .txt, or .xlsx to import it."})
            continue
        digest = sha1(p)
        if ext in DOC_EXT:
            if (rel, digest, "document") in done:
                skipped.append({"origin": rel, "reason": "already imported"})
                continue
            is_chapter = bool(CHAPTER_RE.search(p.stem))
            base = ("work/drafts/" if is_chapter else "work/brainstorm/imported/") + slug(p.stem)
            it = {"kind": "document", "class": "chapter" if is_chapter else "planning or notes", "origin": rel, "sha1": digest,
                  "dest": dest_for(base), "action": "convert to markdown" if ext in (".docx", ".odt") else "copy as markdown",
                  "note": "your chapter text, unchanged" if is_chapter else "kept in brainstorm until you confirm facts for kb/"}
            note_changes(rel, "document", digest, it)
            items.append(it)
        elif ext in SHEET_EXT:
            try:
                sheets = read_xlsx(p) if ext == ".xlsx" else read_csv_sheet(p)
            except Exception as e:  # unreadable file: report, do not guess
                skipped.append({"origin": rel, "reason": f"could not read: {e}"})
                continue
            for name, rows in sheets.items():
                if (rel, digest, name) in done:
                    skipped.append({"origin": f"{rel} [{name}]", "reason": "already imported"})
                    continue
                kind = classify_sheet(rows)
                if kind == "empty":
                    skipped.append({"origin": f"{rel} [{name}]", "reason": "empty sheet"})
                    continue
                stem = slug(f"{Path(rel).stem}-{name}")
                dest, note = {
                    "timeline": (dest_for(f"kb/timeline/imported-{stem}"), "timeline events, marked needs review"),
                    "characters": (dest_for(f"kb/characters/imported-{stem}"), "character tracker, marked needs review"),
                    "numbers": (dest_for(f"kb/world/imported-{stem}"), "numbers table, marked needs review"),
                    "wordcount": (dest_for(f"work/data/{stem}"), "word-count log, kept as a working table"),
                    "unknown": (dest_for(f"work/data/{stem}", ".csv"), "could not classify; kept as raw CSV so nothing is lost"),
                }[kind]
                it = {"kind": "sheet", "class": kind, "origin": rel, "sheet": name, "sha1": digest, "dest": dest,
                      "action": "raw CSV" if kind == "unknown" else "convert to markdown table", "note": note}
                note_changes(rel, name, digest, it)
                items.append(it)
    return {"version": 2, "project": str(root), "existing": existing, "items": items, "left_in_place": skipped}


def render_plan(plan):
    e = plan["existing"]
    lines = ["# Adopt plan", "", f"Project: {plan['project']}", "",
             "Nothing has been written. Your original files will not be modified, moved, or deleted.", ""]
    lines += ["## What is already here", f"- Instructions file: {e['instructions_file'] or 'none'} (story project section: {'yes' if e['section_present'] else 'no'})",
              f"- Knowledge base pages: {e['kb_pages']}"]
    if e["open_questions_register"]:
        lines.append(f"- Open-questions register: `{e['open_questions_register']}` (stays the one register; no second one is created)")
    if e["outline_files"]:
        lines.append(f"- `work/outline/` has {e['outline_files']} file(s); the Router counts it as your beats")
    if e["tool_folders_left_alone"]:
        lines.append("- Left alone: " + ", ".join(e["tool_folders_left_alone"]))
    lines += ["", f"## Will be created ({len(plan['items'])})"]
    if not plan["items"]:
        lines.append("- nothing")
    for it in plan["items"]:
        if True:
            src = it["origin"] + (f" [{it['sheet']}]" if it.get("sheet") else "")
            lines.append(f"- `{src}` -> `{it['dest']}` ({it['class']}; {it['action']}; {it['note']})")
    if plan["left_in_place"]:
        lines += ["", f"## Left in place ({len(plan['left_in_place'])})"]
        lines += [f"- `{s['origin']}`: {s['reason']}" for s in plan["left_in_place"]]
    lines += ["", "The settings for how you want to work are set up afterward, by story-onboard.",
              "Say yes to apply this plan, or tell me what to change."]
    return "\n".join(lines)


# ---------- apply ----------

def snapshot(root):
    return {str(p.relative_to(root)): sha1(p) for p in root.rglob("*")
            if p.is_file() and ".git" not in p.relative_to(root).parts}


def apply_plan(root, plan, yes):
    if not yes:
        print("Not approved: nothing was written. Run again with --yes after the writer approves the plan.")
        return 4
    if Path(plan["project"]).resolve() != root:
        print("The plan was made for a different folder. Nothing was written.")
        return 2
    for it in plan["items"]:
        if sha1(root / it["origin"]) != it["sha1"]:
            print(f"{it['origin']} changed since the plan was made. Nothing was written; make a new plan.")
            return 2
    before = snapshot(root)
    today = date.today().isoformat()
    ledger = []

    failed = []
    for it in plan["items"]:
        origin = root / it["origin"]
        ext = origin.suffix.lower()
        dest = root / it["dest"]
        src = it["origin"] + (f" [{it['sheet']}]" if it.get("sheet") else "")
        part = "document" if it["kind"] == "document" else it["sheet"]
        if dest.exists():
            failed.append((it, f"{it['dest']} already exists; make a new plan"))
            ledger.append((it["dest"], it["origin"], it["sha1"], part, it["action"], "skipped"))
            continue
        tmp = dest.with_name(dest.name + ".adopt-tmp")
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            if it["kind"] == "document":
                text = read_docx(origin) if ext == ".docx" else read_odt(origin) if ext == ".odt" else read_text(origin)
                # The writer's own text is trusted, and notes sit in brainstorm, which is untrusted by location, so
                # neither needs a banner. One short comment names the origin; the ledger has the rest.
                body = f"<!-- adopt: from \"{src}\" -->\n\n" + text
            else:
                rows = (read_xlsx(origin) if ext == ".xlsx" else read_csv_sheet(origin))[it["sheet"]]
                if it["class"] == "unknown":
                    body = to_csv_text(rows)
                else:
                    date_cols = {i for i, c in enumerate(rows[0]) if c and "date" in str(c).lower()}
                    needs = it["class"] in ("timeline", "characters", "numbers")
                    # Only a table that still needs the writer's confirmation is marked; confirming removes the marker.
                    banner = f"<!-- adopt: from \"{src}\" -->\n" + ("> Status: needs review.\n" if needs else "") + "\n"
                    body = f"# {Path(it['dest']).stem.replace('-', ' ')}\n\n" + banner + to_markdown_table(rows, date_cols)
            tmp.write_text(body, encoding="utf-8")
            os.replace(tmp, dest)
            ledger.append((it["dest"], it["origin"], it["sha1"], part, it["action"], "imported"))
        except Exception as e:  # one bad file must not stop the rest
            if tmp.exists():
                tmp.unlink()
            failed.append((it, str(e) or type(e).__name__))
            ledger.append((it["dest"], it["origin"], it["sha1"], part, it["action"], "failed"))

    led = root / LEDGER
    led.parent.mkdir(parents=True, exist_ok=True)
    if not led.exists():
        led.write_text(LEDGER_HEAD, encoding="utf-8")
    with open(led, "a", encoding="utf-8") as f:
        for dest_, origin_, digest, part, method, status in ledger:
            f.write(f"| `{dest_}` | `{origin_}` | `{digest}` | {part} | {method} | {status} | {today} |\n")

    after = snapshot(root)
    problems = [k for k, v in before.items() if k != LEDGER and after.get(k) != v]
    if problems:
        print("PROBLEM: these existing files changed:", problems)
        return 3
    done = sum(1 for row in ledger if row[5] == "imported")
    print(f"Imported {done} item(s). All {len(before)} files that existed before are unchanged. Provenance: {LEDGER}")
    for it, why in failed:
        print(f"FAILED {it['origin']}" + (f" [{it['sheet']}]" if it.get("sheet") else "") + f": {why}")
    if failed:
        print(f"{len(failed)} item(s) failed and were not imported; re-run Adopt to retry them.")
        return 5
    return 0


def review(root):
    found = []
    for p in sorted((root / "kb").rglob("*.md")) if (root / "kb").is_dir() else []:
        if "Status: needs review" in p.read_text(encoding="utf-8", errors="replace"):
            found.append(str(p.relative_to(root)))
    print(f"{len(found)} page(s) still marked needs review")
    for f in found:
        print(" -", f)
    return 0


def main(argv):
    if len(argv) < 3 or argv[1] not in ("plan", "apply", "review"):
        print(__doc__)
        return 2
    root = Path(argv[2]).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory")
        return 2
    if argv[1] == "plan":
        plan = build_plan(root)
        if "--json" in argv:
            Path(argv[argv.index("--json") + 1]).write_text(json.dumps(plan, indent=2), encoding="utf-8")
        print(render_plan(plan))
        return 0
    if argv[1] == "review":
        return review(root)
    if len(argv) < 4:
        print("apply needs a plan file")
        return 2
    return apply_plan(root, json.loads(Path(argv[3]).read_text(encoding="utf-8")), "--yes" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
