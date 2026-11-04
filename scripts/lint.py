#!/usr/bin/env python3
"""Structural lint for the skill library and its Extractions. No model, no dependencies.

Skills: frontmatter, description, hub children, quote length, and no references
to working material (skills ship without the transcripts or Extractions, so they
must not point at them).
Fixtures: each Story-project fixture is in the state its name promises.
Extractions (working folder only): required sections, a citation on every
framework, and every citation within the length of the lecture it cites.

Usage: lint.py [repo_root]   (defaults to the repo containing this script)
Exits 1 and prints one line per problem when any rule fails.
"""
import re
import sys
from pathlib import Path

MAX_DESCRIPTION = 1024
MAX_QUOTE_WORDS = 45
MAX_QUOTE_SENTENCES = 2
MIN_QUOTE_WORDS = 8  # shorter quoted spans are terms or scare quotes, not quotes
CITATION = re.compile(r"\[L(\d+(?:\.\d)?) @ (\d+(?::\d{2}){1,2})\]")
QUOTE = re.compile(r"[\"“]([^\"”\n]+)[\"”]")
WORKING_REFS = [r"extractions/", r"transcripts/", r"\.scratch", r"\.\./", r"\[L\d+(?:\.\d)? @"]
SKILL_PREFIXES = ("plot-", "character-", "magic-", "worldbuilding-", "foundations-", "scene-", "story-", "prose-")
# Skills removed when the process layer was rebuilt; nothing may still name them.
RETIRED = re.compile(r"\b(workflow-[a-z-]+|director-[a-z-]+|which-workflow|story-setup|magic-zeroeth-law)\b")
# File names the first build hard-coded; a skill must use the project's own conventions instead.
HARDCODED = ("director-preferences.md", "director-canon-queue.md", "grill-summary.md")
TYPES = {"hub", "framework", "workflow", "router", "setup", "other"}


def seconds(stamp):
    parts = [int(p) for p in stamp.split(":")]
    return parts[0] * 60 + parts[1] if len(parts) == 2 else parts[0] * 3600 + parts[1] * 60 + parts[2]


def parse_frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields, key = {}, None
    for line in m.group(1).splitlines():
        top = re.match(r"([A-Za-z_-]+):\s*(.*)$", line)
        if top and not line.startswith(" "):
            key = top.group(1)
            val = top.group(2)
            fields[key] = "" if val in (">", "|") else val
        elif key and key != "metadata" and line.strip():
            fields[key] = (fields[key] + " " + line.strip()).strip()
    # The one nested field we use: metadata -> type. Nothing else is nested.
    m2 = re.search(r"^metadata:\n((?:  .*\n?)+)", m.group(1) + "\n", re.M)
    if m2:
        t = re.search(r"^  type:\s*(\S+)", m2.group(1), re.M)
        if t:
            fields["type"] = t.group(1)
    return fields


def transcript_ends(root):
    ends = {}
    for f in (root / "transcripts").glob("*.md"):
        m = re.search(r"Lecture #(\d+(?:\.\d)?)", f.name)
        if not m:
            continue
        stamps = re.findall(r"^\[(\d+(?::\d{2}){1,2})\]", f.read_text(encoding="utf-8"), re.M)
        if stamps:
            ends[m.group(1)] = max(seconds(s) for s in stamps)
    return ends


def lint_skill(skill_dir, root, ends, errors):
    name = skill_dir.name
    md = skill_dir / "SKILL.md"
    if not md.exists():
        errors.append(f"{name}: missing SKILL.md")
        return
    text = md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append(f"{name}: missing frontmatter")
        return
    if fm.get("name") != name:
        errors.append(f"{name}: frontmatter name {fm.get('name')!r} does not match folder")
    desc = fm.get("description", "")
    if not desc.strip():
        errors.append(f"{name}: missing description")
    elif len(desc) > MAX_DESCRIPTION:
        errors.append(f"{name}: description is {len(desc)} chars (max {MAX_DESCRIPTION})")
    stype = fm.get("type", "")
    if stype not in TYPES:
        errors.append(f"{name}: type {stype!r} is not one of {sorted(TYPES)}")

    body = text.split("\n---\n", 1)[1] if "\n---\n" in text else text

    for q in QUOTE.findall(body):
        words = len(q.split())
        if words < MIN_QUOTE_WORDS:
            continue
        sentences = len(re.findall(r"[.?!](?:\s+[A-Z]|$)", q.strip()))
        if words > MAX_QUOTE_WORDS or sentences > MAX_QUOTE_SENTENCES:
            errors.append(f"{name}: quote too long ({words} words): {q[:50]}...")

    if stype in ("hub", "framework"):
        for tok in sorted(set(re.findall(r"`([a-z][a-z0-9-]+)`", body))):
            if tok.startswith(SKILL_PREFIXES) and not (root / "skills" / tok / "SKILL.md").exists():
                errors.append(f"{name}: references missing skill {tok!r}")

    if stype == "hub":
        section = re.search(r"## Children\n(.*?)(?=\n## |\Z)", body, re.S)
        if not section:
            errors.append(f"{name}: hub has no '## Children' section")
        else:
            kids = re.findall(r"^- `([a-z0-9-]+)`", section.group(1), re.M)
            if not kids:
                errors.append(f"{name}: hub lists no children")
            for kid in kids:
                if not (root / "skills" / kid / "SKILL.md").exists():
                    errors.append(f"{name}: hub lists missing child {kid!r}")

    for pattern in WORKING_REFS:
        if re.search(pattern, text):
            errors.append(f"{name}: references working material ({pattern.strip(chr(92))}); skills must be self-contained")


EXTRACTION_SECTIONS = ["## Summary", "## Frameworks", "## Principles", "## Terms", "## Cross-references", "## Unclear"]


def lint_extractions(root, ends, errors):
    folder = root / "extractions"
    if not folder.is_dir():
        return 0
    files = [f for f in sorted(folder.glob("*.md")) if f.name not in ("FORMAT.md", "INVENTORY.md")]
    for f in files:
        text = f.read_text(encoding="utf-8")
        for sec in EXTRACTION_SECTIONS:
            if sec not in text:
                errors.append(f"{f.name}: missing section {sec!r}")
        fw = re.search(r"## Frameworks\n(.*?)(?=\n## )", text, re.S)
        if fw:
            for block in re.split(r"^### ", fw.group(1), flags=re.M)[1:]:
                if not CITATION.search(block):
                    errors.append(f"{f.name}: framework {block.splitlines()[0]!r} has no citation")
        for lec, stamp in CITATION.findall(text):
            if lec in ends and seconds(stamp) > ends[lec] + 60:
                errors.append(f"{f.name}: citation [L{lec} @ {stamp}] is past the end of the lecture")
    return len(files)


START_MARK = "<!-- story-project:start"
END_MARK = "<!-- story-project:end -->"
FIXTURE_DIRS = ["kb/characters", "kb/world", "kb/timeline", "kb/canon", "kb/styles", "kb/samples", "kb/issues",
                "work/spec", "work/beats", "work/drafts", "work/critique-reports", "work/brainstorm"]
# name -> (scaffolded, min/exact files in spec, beats, drafts); None means "at least one"
FIXTURES = {
    "empty-scaffolded": (True, {"spec": 0, "beats": 0, "drafts": 0}),
    "spec-only": (True, {"spec": None, "beats": 0, "drafts": 0}),
    "draft-only": (True, {"spec": 0, "beats": 0, "drafts": None}),
    "with-instructions": (False, None),
    "existing-material": (False, None),  # the writer's own files; no instructions file
    "grilled": (True, {"spec": 0, "beats": 0, "drafts": 0}),
    "beats-ready": (True, {"spec": None, "beats": None, "drafts": 0}),
    "drafted": (True, {"spec": None, "beats": None, "drafts": None}),
    "reviewed": (True, {"spec": None, "beats": None, "drafts": None, "critique-reports": None}),
    "serial": (True, {"spec": 0, "beats": 0, "drafts": None}),  # established story, chapters written, no plan
}
NEEDS_INSTRUCTIONS = {"empty-scaffolded", "spec-only", "draft-only", "with-instructions",
                      "grilled", "beats-ready", "drafted", "reviewed", "serial"}


def count_files(folder):
    return len([f for f in folder.rglob("*") if f.is_file() and f.name != ".gitkeep"]) if folder.is_dir() else 0


def lint_fixtures(root, errors):
    base = root / "fixtures"
    if not base.is_dir():
        return 0
    dirs = sorted(d for d in base.iterdir() if d.is_dir())
    for d in dirs:
        if d.name not in FIXTURES:
            errors.append(f"fixture {d.name}: unknown fixture, add its expectations to the lint")
            continue
        scaffolded, counts = FIXTURES[d.name]
        agents = d / "AGENTS.md"
        if not agents.is_file() and d.name in NEEDS_INSTRUCTIONS:
            errors.append(f"fixture {d.name}: missing AGENTS.md")
            continue
        has_markers = agents.is_file() and START_MARK in agents.read_text(encoding="utf-8")
        if scaffolded:
            if not has_markers:
                errors.append(f"fixture {d.name}: AGENTS.md has no story project section")
            for rel in FIXTURE_DIRS:
                if not (d / rel).is_dir():
                    errors.append(f"fixture {d.name}: missing folder {rel}")
            for key, want in counts.items():
                n = count_files(d / "work" / key)
                if want is None and n == 0:
                    errors.append(f"fixture {d.name}: work/{key} should have files but is empty")
                elif want == 0 and n != 0:
                    errors.append(f"fixture {d.name}: work/{key} should be empty but has {n} file(s)")
        else:
            if has_markers:
                errors.append(f"fixture {d.name}: should not already contain the story project section")
            if (d / "kb").exists() or (d / "work").exists():
                errors.append(f"fixture {d.name}: should not already have kb/ or work/")
    for name in FIXTURES:
        if not (base / name).is_dir():
            errors.append(f"fixture {name}: missing")
    return len(dirs)


def lint_process_layer(root, errors):
    """Retired names, routing, and project conventions."""
    skills = root / "skills"
    for f in sorted(skills.rglob("*")):
        if f.is_file() and f.suffix in (".md", ".py") and "__pycache__" not in f.parts:
            for m in sorted(set(RETIRED.findall(f.read_text(encoding="utf-8")))):
                errors.append(f"{f.relative_to(skills)}: names retired skill {m!r}")
    block = skills / "story-onboard" / "storyblock.py"
    if block.is_file():
        ns = {}
        exec(compile(block.read_text(encoding="utf-8"), str(block), "exec"), ns)
        for _, skill in ns["ROUTES"]:
            if not (skills / skill / "SKILL.md").is_file():
                errors.append(f"routing table names missing skill {skill!r}")
    for md in sorted(skills.glob("story-*/SKILL.md")):
        text = md.read_text(encoding="utf-8")
        for name in HARDCODED:
            if name in text:
                errors.append(f"{md.parent.name}: hard-codes {name}; use the project's own conventions")
        if "status: accepted" in text:
            errors.append(f"{md.parent.name}: writes the retired 'accepted' marker; trust is the default, so approval removes a marker")
        for fallback in ("pending-facts.md", "adopt-facts.md"):
            if fallback in text and "names none" not in text and "second register" not in text:
                errors.append(f"{md.parent.name}: names {fallback} without saying to use the project's single register first")
        if md.parent.name not in ("story-next", "story-learn") and "project's own" not in text:
            errors.append(f"{md.parent.name}: does not say it follows the project's own conventions")


def lint_plugin_manifests(root, errors):
    """The Claude Code and Codex plugin manifests, and the marketplaces that list them, must agree."""
    import json
    files = [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
             ".codex-plugin/plugin.json", ".agents/plugins/marketplace.json"]
    if not any((root / f).exists() for f in files):
        return
    docs = {}
    for f in files:
        path = root / f
        if not path.is_file():
            errors.append(f"plugin manifest missing: {f}")
            continue
        try:
            docs[f] = json.loads(path.read_text(encoding="utf-8"))
        except ValueError as e:
            errors.append(f"{f}: not valid JSON ({e})")
    names = {f: d.get("name") if "plugin.json" in f else (d.get("plugins") or [{}])[0].get("name") for f, d in docs.items()}
    if len(set(names.values())) > 1:
        errors.append(f"plugin names disagree across manifests: {names}")
    versions = {f: d.get("version") for f, d in docs.items() if f.endswith("plugin.json")}
    if len(set(versions.values())) > 1:
        errors.append(f"plugin versions disagree: {versions}")
    codex = docs.get(".codex-plugin/plugin.json", {})
    if codex and codex.get("skills") != "./skills/":
        errors.append(".codex-plugin/plugin.json: skills must be './skills/'")


def lint_shared_copies(skills, errors):
    """Modules copied into several skills (so each stands alone) must stay identical."""
    copies = {}
    for f in sorted(skills.glob("*/storyblock.py")):
        copies.setdefault(f.read_bytes(), []).append(f.parent.name)
    if len(copies) > 1:
        errors.append("storyblock.py copies differ between skills: " + " / ".join(", ".join(v) for v in copies.values()))


def lint_checks(root, errors):
    """The knowledge contract: valid unique check IDs, a valid mapping, and no drift in generated sections."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import compile_checks
    found, notices = [], []
    stale = compile_checks.compile_all(root, False, found, notices, require_all=True)
    errors += [f"checks: {e}" for e in found]
    errors += [f"{s}: generated checks are out of date; run scripts/compile_checks.py" for s in stale]
    errors += [f"checks: {n}" for n in notices]


def main(argv):
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parent.parent
    skills = root / "skills"
    errors = []
    if not skills.is_dir():
        print("no skills directory")
        return 1
    ends = transcript_ends(root)
    dirs = sorted(d for d in skills.iterdir() if d.is_dir())
    for d in dirs:
        lint_skill(d, root, ends, errors)
    lint_shared_copies(skills, errors)
    lint_plugin_manifests(root, errors)
    lint_process_layer(root, errors)
    lint_checks(root, errors)
    n_ext = lint_extractions(root, ends, errors)
    n_fix = lint_fixtures(root, errors)
    for e in errors:
        print(e)
    print(f"{len(dirs)} skills, {n_ext} extractions, {n_fix} fixtures checked, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
