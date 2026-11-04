#!/usr/bin/env python3
"""Report the state of a Story project: its settings and where the story stands.

Usage: inspect.py [project_dir]

Prints one `key: value` line per fact. Read-only: it never creates, changes, or
deletes anything.
"""
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
          "story-worldbuild", "story-cast", "story-voice"]
NUM_RE = re.compile(r"(\d+)")


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
    drafts = [f for f in files_in(root / "work" / "drafts") if f.suffix == ".md" and "_previous" not in f.parts]
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
                                           open_findings, undrafted_beats, spec, beats, drafts, developed)
    if skill and skill not in have:
        reason += f"; {skill} is not installed"
    out += [("next_step", step), ("next_skill", skill or "none"), ("next_owner", owner), ("next_reason", reason)]
    return out


def next_step(status, settings, material, statuses, facts, unchecked, open_findings, undrafted_beats,
              spec, beats, drafts, developed):
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
