#!/usr/bin/env python3
"""Compile craft checks from the framework skills into the skills that use them.

Usage: compile_checks.py [--check] [repo_root]

Framework skills are the single source of every check: a `## Checks` section of
list items, each starting with a stable ID such as `plot.ppp.01`. The mapping
file (check-map.txt, next to this script) says which checks each consuming skill
uses, per operation. This script writes a generated section into each consuming
skill between markers and never touches text outside them.

--check writes nothing and exits 1 if any generated section is out of date or the
checks or mapping have problems. The library lint runs the same check.
"""
import re
import sys
from pathlib import Path

# Hubs whose framework skills must carry a Checks section. Extended hub by hub.
CONTRACT_PREFIXES = ("plot-", "character-", "magic-", "worldbuilding-", "foundations-",
                     "scene-", "show-dont-tell", "viewpoint-and-tense", "prose-")
ID_RE = re.compile(r"^[a-z]+\.[a-z]+\.\d{2}$")
ITEM_RE = re.compile(r"^- `([^`]+)` (.+)$")
GEN_RE = re.compile(r"<!-- generated:checks:start(?: ([a-z-]+))? -->\n.*?<!-- generated:checks:end(?: \1)? -->\n?", re.S)
MAP_FILE = Path(__file__).resolve().parent / "check-map.txt"

PREAMBLE = ("Apply each check that fits this story. In the files you write (beats, reports, notes), record its ID with a "
            "short note of what it found in this story, or `n/a` with a reason. Never show IDs or skill names to the writer: "
            "in conversation, ask or say the substance in the craft language the settings name. A deliberate break of a framework is a valid answer, not a defect: say it is "
            "deliberate and do not push the story back toward the formula. Load the skill listed for a check's family "
            "(after the list) only when you need its full reasoning.")


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fields = dict(re.findall(r"^([a-z-]+):\s*(.*)$", m.group(1), re.M))
    t = re.search(r"^metadata:\n(?:  .*\n)*?  type:\s*(\S+)", m.group(1) + "\n", re.M)
    if t:
        fields["type"] = t.group(1)
    return fields


def checks_section(text):
    m = re.search(r"^## Checks\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else None


def collect(skills_dir, errors):
    """{check_id: (text, skill)} from every skill's Checks section."""
    found = {}
    for md in sorted(skills_dir.glob("*/SKILL.md")):
        skill, text = md.parent.name, md.read_text(encoding="utf-8")
        if not skill.startswith(CONTRACT_PREFIXES):
            continue  # skills outside the contract keep their own check lists until their hub joins
        section = checks_section(text)
        if section is None:
            if frontmatter(text).get("type") == "framework":
                errors.append(f"{skill}: framework has no '## Checks' section (list checks, or say 'None.' and why)")
            continue
        items = [l for l in section.splitlines() if l.startswith("- ")]
        if not items and not section.strip().startswith("None."):
            errors.append(f"{skill}: '## Checks' has no checks and does not say 'None.'")
        for line in items:
            m = ITEM_RE.match(line)
            if not m or not ID_RE.match(m.group(1)):
                errors.append(f"{skill}: check without a valid ID: {line[:60]}")
                continue
            cid = m.group(1)
            if cid in found:
                errors.append(f"{skill}: duplicate check ID {cid} (also in {found[cid][1]})")
                continue
            found[cid] = (m.group(2).strip(), skill)
    # Each generated list names one skill per check family, so a family may not be split across skills.
    owners = {}
    for cid, (_, skill) in found.items():
        owners.setdefault(family(cid), set()).add(skill)
    for fam, skills in sorted(owners.items()):
        if len(skills) > 1:
            errors.append(f"check family {fam} is split across skills {', '.join(sorted(skills))}; one skill per family")
    return found


def load_map(path, errors):
    """[(consumer, operation_or_None, [patterns])] in file order."""
    entries = []
    if not path.is_file():
        errors.append(f"mapping file missing: {path.name}")
        return entries
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        head, _, rest = line.partition(":")
        consumer, _, op = head.strip().partition("/")
        if not rest.strip() or not re.match(r"^[a-z0-9-]+$", consumer) or (op and not re.match(r"^[a-z-]+$", op)):
            errors.append(f"{path.name} line {n}: expected 'skill[/operation]: id id ...'")
            continue
        entries.append((consumer, op or None, rest.replace(",", " ").split()))
    return entries


def expand(patterns, checks, where, errors):
    ids = []
    for pat in patterns:
        if pat.endswith(".*"):
            hit = sorted(c for c in checks if c.startswith(pat[:-1]))
            if not hit:
                errors.append(f"{where}: '{pat}' matches no check")
        elif pat in checks:
            hit = [pat]
        else:
            errors.append(f"{where}: unknown check ID '{pat}'")
            hit = []
        ids += [c for c in hit if c not in ids]
    return ids


def family(check_id):
    return ".".join(check_id.split(".")[:2])


def render(op, ids, checks):
    tag = f" {op}" if op else ""
    title = f"## Craft checks{': ' + op if op else ''} (generated)"
    lines = "\n".join(f"- `{c}` {checks[c][0]}" for c in ids)
    seen = {}
    for c in ids:
        seen.setdefault(family(c), checks[c][1])
    skills = "; ".join(f"`{f}` {s}" for f, s in seen.items())
    return (f"<!-- generated:checks:start{tag} -->\n{title}\n\n{PREAMBLE}\n\n{lines}\n\n"
            f"Skill for each check family: {skills}.\n"
            f"<!-- generated:checks:end{tag} -->\n")


def apply(text, sections):
    """Replace or append generated sections; remove generated sections no longer mapped."""
    wanted = dict(sections)
    out, pos = [], 0
    for m in GEN_RE.finditer(text):
        out.append(text[pos:m.start()])
        op = m.group(1)
        if op in wanted:
            out.append(wanted.pop(op))
        pos = m.end()
    out.append(text[pos:])
    new = "".join(out)
    for op, block in sections:
        if op in wanted:
            new = new.rstrip("\n") + "\n\n" + block
    return new


def compile_all(root, write, errors, notices, require_all=False):
    """Return the list of skills whose generated sections differ from a fresh compile.

    With require_all, a check that no skill uses is an error."""
    skills_dir = root / "skills"
    checks = collect(skills_dir, errors)
    entries = load_map(root / "scripts" / MAP_FILE.name, errors)
    by_consumer, used = {}, set()
    for consumer, op, patterns in entries:
        ids = expand(patterns, checks, f"{consumer}{'/' + op if op else ''}", errors)
        used.update(ids)
        by_consumer.setdefault(consumer, []).append((op, render(op, ids, checks)))
    if require_all:
        errors += [f"{c} ({checks[c][1]}): no skill uses this check; add it to {MAP_FILE.name}" for c in sorted(set(checks) - used)]
    stale = []
    for md in sorted(skills_dir.glob("*/SKILL.md")):
        skill = md.parent.name
        text = md.read_text(encoding="utf-8")
        sections = by_consumer.pop(skill, [])
        if not sections and not GEN_RE.search(text):
            continue
        new = apply(text, sections)
        if new != text:
            stale.append(skill)
            if write:
                md.write_text(new, encoding="utf-8")
    for consumer in by_consumer:
        notices.append(f"mapping names '{consumer}', which is not in the library yet; skipped")
    return stale


def main(argv):
    check = "--check" in argv
    args = [a for a in argv[1:] if not a.startswith("--")]
    root = Path(args[0]).resolve() if args else Path(__file__).resolve().parent.parent
    errors, notices = [], []
    stale = compile_all(root, False, errors, notices, require_all=True)
    if not check and not errors and stale:
        compile_all(root, True, [], [])
    for n in notices:
        print(f"note: {n}")
    for e in errors:
        print(e)
    if check:
        for s in stale:
            print(f"{s}: generated checks are out of date; run scripts/compile_checks.py")
        return 1 if errors or stale else 0
    print(f"updated: {', '.join(stale) or 'nothing'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
