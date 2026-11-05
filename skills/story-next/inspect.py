#!/usr/bin/env python3
"""Report the state of a Story project: its settings and where the story stands.

Usage: inspect.py [project_dir]

Prints one `key: value` line per fact. Read-only: it never creates, changes, or
deletes anything.
"""
import hashlib
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import storyblock as sb  # noqa: E402

PROJECT_DIRS = {"kb", "work", ".git", ".claude", ".agents", ".gemini", "node_modules", "docs"}
WRITING_EXT = {".docx", ".doc", ".odt", ".rtf", ".pdf", ".xlsx", ".xls", ".ods", ".csv", ".scriv", ".txt", ".md", ".markdown"}
INSTRUCTION_FILES = {"agents.md", "claude.md", "readme.md", "gemini.md"}
ESTABLISHED_KB_PAGES = 10
SKILLS = ["story-onboard", "story-next", "story-adopt", "story-develop", "story-plan", "story-draft",
          "story-check", "story-revise", "story-steer", "story-continue", "story-learn",
          "story-worldbuild", "story-cast", "story-voice", "story-edits"]
NUM_RE = re.compile(r"(\d+)")
STATUS_LINE_RE = re.compile(r"<!--\s*status:.*?-->", re.I)
PROMISE_RE = re.compile(r"^\s*[-*]\s*(P\d+)\s*\|\s*planted\s+(?:ch(?:apter)?\.?\s*)?(\d+)\s*\|\s*(open|advanced|paid|dropped)\b", re.I)
CARD_HEADER_RE = re.compile(r"^<!--\s*card:\s*(.*?);\s*hash:\s*([0-9a-f]{12})\s*-->\s*$")


def files_in(folder):
    if not folder.is_dir():
        return []
    return sorted(f for f in folder.rglob("*") if f.is_file() and f.name != ".gitkeep")


def text(path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def existing_material(root):
    """Writing the writer already has, outside the Story project layout."""
    found = []
    for f in root.rglob("*"):
        rel = f.relative_to(root)
        if not f.is_file() or rel.parts[0] in PROJECT_DIRS or any(p.startswith(".") for p in rel.parts):
            continue
        if f.suffix.lower() in WRITING_EXT and f.name.lower() not in INSTRUCTION_FILES:
            found.append(str(rel))
    return sorted(found)


def chapter_number(path):
    m = NUM_RE.search(path.stem)
    return int(m.group(1)) if m else None


def body(text):
    """A chapter's paragraphs, ignoring its status line and whitespace differences."""
    lines = text.splitlines()
    for i, line in enumerate(lines[:5]):
        if STATUS_LINE_RE.search(line):
            lines[i] = ""
    return [" ".join(p.split()) for p in re.split(r"\n\s*\n", "\n".join(lines)) if p.strip()]


def card_hash(text):
    return hashlib.sha1("\n".join(body(text)).encode("utf-8")).hexdigest()[:12]


def card_state(root, drafts):
    """Chapters whose card is missing or stale, and cards whose chapter is gone (see story-continue/cards.py)."""
    missing, stale = [], []
    for d in drafts:
        card = root / "work" / "cards" / d.name
        if not card.is_file():
            missing.append(d.name)
            continue
        first = (text(card).splitlines() or [""])[0]
        m = CARD_HEADER_RE.match(first)
        if not m or m.group(2) != card_hash(text(d)):
            stale.append(d.name)
    names = {d.name for d in drafts}
    orphan = sorted(f.name for f in files_in(root / "work" / "cards") if f.suffix == ".md" and f.name not in names)
    return missing, stale, orphan


def promise_state(root, drafts):
    """Promises written as `- P03 | planted ch2 | open | text`. Lines in any other shape are the project's own and are ignored.

    Returns (counts, oldest unpaid description). A promise is unpaid while it is open or advanced."""
    found = {}
    folders = [f for f in files_in(root / "work") if f.suffix == ".md" and f.relative_to(root / "work").parts[0] not in ("drafts", "cards")]
    for f in folders + [g for g in files_in(root / "kb" / "issues") if g.suffix == ".md"]:
        for line in text(f).splitlines():
            m = PROMISE_RE.match(line)
            if m:
                found[m.group(1).upper()] = (int(m.group(2)), m.group(3).lower())
    counts = {k: 0 for k in ("open", "advanced", "paid", "dropped")}
    for _, status in found.values():
        counts[status] += 1
    unpaid = [(planted, pid) for pid, (planted, status) in found.items() if status in ("open", "advanced")]
    if not unpaid:
        return counts, "none"
    planted, pid = min(unpaid)
    latest = max((n for n in (chapter_number(d) for d in drafts) if n is not None), default=None)
    age = f", {max(latest - planted, 0)} chapters ago" if latest is not None else ""
    return counts, f"{pid} (planted ch{planted}{age})"


def installed_skills():
    """Story skills installed beside this one (links are not resolved)."""
    skills_dir = Path(os.path.abspath(__file__)).parent.parent
    have = [s for s in SKILLS if (skills_dir / s / "SKILL.md").is_file()]
    return have, [s for s in SKILLS if s not in have]


def inspect(root):
    files = {n: (text(root / n) if (root / n).is_file() else None) for n in ("AGENTS.md", "CLAUDE.md")}
    status, detail, settings, src = sb.classify(files)

    spec = files_in(root / "work" / "spec")
    beats = [f for f in files_in(root / "work" / "beats") if f.suffix == ".md"]
    drafts = [f for f in files_in(root / "work" / "drafts") if f.suffix == ".md" and "_previous" not in f.parts and "_delivered" not in f.parts]
    reports = [f for f in files_in(root / "work" / "critique-reports") if f.suffix == ".md"]
    kb_pages = [f for f in files_in(root / "kb") if f.name != "vocab.md"]

    # Trust is the default: only chapters with a status line are untrusted. A chapter with none, or with the
    # first build's "accepted" line, is trusted and is never recommended for checking or revising on its own.
    statuses = {s: [] for s in sb.CHAPTER_STATUSES}
    trusted = []
    for d in drafts:
        st = sb.chapter_status(text(d))
        if st and st[0] in statuses:
            statuses[st[0]].append(d.name)
        else:
            trusted.append(d.name)

    facts = {"pending major": 0, "pending minor": 0, "rejected": 0}
    for f in files_in(root / "work") + files_in(root / "kb" / "issues"):
        if f.suffix == ".md":
            for line in text(f).splitlines():
                m = sb.FACT_RE.match(line)
                if m:
                    facts[m.group(1).lower()] += 1

    open_findings = 0
    for r in reports:
        open_findings += sum(1 for line in text(r).splitlines()
                             if (m := sb.FINDING_RE.match(line)) and m.group(1).lower() == "open")

    # A chapter the writer approved (no status line) that still has the AI's delivered copy, and differs from it,
    # has edits worth learning from. A chapter still marked is in progress, so its edits wait for approval.
    edited = []
    for d in drafts:
        if d.name in trusted:
            delivered = root / "work" / "drafts" / "_delivered" / d.name
            if delivered.is_file() and body(text(delivered)) != body(text(d)):
                edited.append(d.name)

    cards_missing, cards_stale, cards_orphan = card_state(root, drafts)
    promises, oldest_unpaid = promise_state(root, drafts)

    drafted_nums = {chapter_number(d) for d in drafts} - {None}
    undrafted_beats = [b.name for b in beats if chapter_number(b) is not None and chapter_number(b) not in drafted_nums]
    # Only drafts still marked as drafts need a check; trusted chapters are checked when the writer asks.
    unchecked = [n for n in statuses["draft"] if not any(str(chapter_number(Path(n)) or "x").zfill(3) in r.name or Path(n).stem in r.name for r in reports)]
    developed = len(kb_pages) > 0 or bool(files_in(root / "work" / "brainstorm"))
    have, missing = installed_skills()
    material = existing_material(root)

    out = [
        ("setup", status),
        ("setup_detail", detail),
        ("settings_file", src or "none"),
    ]
    if settings:
        out += [("preset", settings["preset"])] + [(k, settings[k]) for k in sb.KEYS[1:]]
    out += [
        ("scaffolded", (root / "kb").is_dir() and (root / "work").is_dir()),
        ("existing_material", len(material)),
        ("existing_material_files", "; ".join(material[:10]) or "none"),
        ("kb_pages", len(kb_pages)),
        ("established_kb", len(kb_pages) >= ESTABLISHED_KB_PAGES),
        ("developed", developed),
        ("spec_files", len(spec)),
        ("beats_files", len(beats)),
        ("draft_files", len(drafts)),
        ("undrafted_beats", ", ".join(undrafted_beats) or "none"),
        ("chapters_needs_revision", ", ".join(statuses["needs revision"]) or "none"),
        ("chapters_awaiting_check_in", ", ".join(statuses["awaiting check-in"]) or "none"),
        ("chapters_trusted", len(trusted)),
        ("chapters_draft", len(statuses["draft"])),
        ("chapters_edited_since_delivery", ", ".join(edited) or "none"),
        ("promises", " ".join(f"{k}={v}" for k, v in promises.items())),
        ("promises_oldest_unpaid", oldest_unpaid),
        ("cards_missing", ", ".join(cards_missing) or "none"),
        ("cards_stale", ", ".join(cards_stale) or "none"),
        ("cards_orphan", ", ".join(cards_orphan) or "none"),
        ("unchecked_drafts", ", ".join(unchecked) or "none"),
        ("critique_reports", len(reports)),
        ("open_findings", open_findings),
        ("pending_major_facts", facts["pending major"]),
        ("pending_minor_facts", facts["pending minor"]),
        ("rejected_facts", facts["rejected"]),
        ("installed_skills", ", ".join(have) or "none"),
        ("missing_skills", ", ".join(missing) or "none"),
    ]
    step, skill, owner, reason = next_step(status, settings, material, statuses, facts, unchecked,
                                           open_findings, undrafted_beats, spec, beats, drafts, developed, edited)
    if skill and skill not in have:
        reason += f"; {skill} is not installed"
    out += [("next_step", step), ("next_skill", skill or "none"), ("next_owner", owner), ("next_reason", reason)]
    return out


def next_step(status, settings, material, statuses, facts, unchecked, open_findings, undrafted_beats,
              spec, beats, drafts, developed, edited=()):
    """The first step in precedence order that applies: (step, skill, owner, reason).

    Owner is who acts: `ai`, `writer`, or `writer-decides` (a decision only the writer can make)."""
    if status in ("none", "malformed", "duplicate") or status.startswith("v1"):
        return "set up how we work", "story-onboard", "writer-decides", f"setup is '{status}'"
    if material:
        return "bring in existing material", "story-adopt", "writer-decides", f"{len(material)} files outside the project layout"
    s = settings
    design_only = s["draft"] == "none"
    if not design_only and statuses["needs revision"]:
        return "revise chapters that used a rejected fact", "story-revise", s["revise"] if s["revise"] != "none" else "writer", \
            "needs revision: " + ", ".join(statuses["needs revision"])
    if facts["pending major"]:
        return "decide pending story facts", None, "writer-decides", f"{facts['pending major']} major facts await a decision"
    if not design_only and statuses["awaiting check-in"]:
        return "check-in on drafted chapters", None, "writer-decides", "awaiting check-in: " + ", ".join(statuses["awaiting check-in"])
    if not design_only and edited:
        return "learn from your edits", "story-edits", "ai", "edited since delivery: " + ", ".join(edited)
    if not design_only and unchecked:
        return "check the latest draft", "story-check", "ai", "not yet checked: " + ", ".join(unchecked)
    if not design_only and open_findings:
        return "revise from the check report", "story-revise", s["revise"], f"{open_findings} open findings"
    if not design_only and undrafted_beats:
        return "draft the next chapter", "story-draft", s["draft"], "beats with no draft: " + ", ".join(undrafted_beats)
    if spec and beats and design_only:
        return "design complete", None, "writer-decides", "spec and beats are approved; the tools can refine the design"
    if spec:
        return "plan the next chapters", "story-plan", s["plan"], "a spec exists and every planned chapter is drafted" if beats else "a spec exists but no beats"
    if developed:
        return "write the spec", "story-plan", s["plan"], "decisions are recorded but there is no spec"
    return "develop the idea", "story-develop", s["plan"], "nothing is planned yet"


def main(argv):
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory")
        return 2
    for k, v in inspect(root):
        print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
