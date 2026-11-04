#!/usr/bin/env python3
"""Scaffold a Story project and write its settings block.

Usage:
  scaffold.py <dir> --preset <name> [--plan X] [--draft X] [--revise X]
              [--craft-language X] [--check-in X] [--dry-run] [--force] [--repair]
  scaffold.py <dir> --keep [--dry-run] [--repair]

--preset picks a starting point (ai-writes-you-direct, ai-drafts-you-revise,
you-outline-ai-drafts, ai-outlines-you-write, you-write-ai-checks, design-only,
or custom with every stage owner given). The stage options adjust it.
--keep rewrites the block with the project's current settings (or the meaning
of a first-build block) and changes nothing else.
--dry-run writes nothing and prints a diff of the instructions file.

Never overwrites an existing file or folder, and never changes text outside the
block markers. Exit codes: 0 done; 2 bad folder; 3 established project with no
block (use Adopt; --force overrides); 4 settings missing or invalid; 6 broken
blocks that need --repair or a hand fix.
"""
import difflib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import storyblock as sb  # noqa: E402

FACT_DIRS = ["characters", "world", "timeline", "canon", "styles", "samples", "issues"]
WORK_DIRS = ["spec", "beats", "drafts", "critique-reports", "brainstorm"]
ESTABLISHED_KB_PAGES = 10
VOCAB_STUB = "# Vocabulary\n\nCanonical story terms. For each: the canonical name, a short definition, and aliases in use.\n"
# Claude Code reads AGENTS.md only when there is no CLAUDE.md; its documented bridge is an @-import.
POINTER = "# CLAUDE.md\n\n@AGENTS.md\n"
OPTIONS = ("--preset", "--plan", "--draft", "--revise", "--craft-language", "--check-in")


def parse_args(argv):
    opts, flags, pos = {}, set(), []
    it = iter(argv[1:])
    for a in it:
        if a in OPTIONS:
            opts[a[2:]] = next(it, None)
        elif a.startswith("--"):
            flags.add(a)
        else:
            pos.append(a)
    return opts, flags, pos


def read(path):
    return path.read_text(encoding="utf-8") if path.is_file() else None


def without_blocks(text):
    """Text with every Story project block removed (used by --repair on the losing file)."""
    out, last = [], 0
    for start, end, _ in sb.find_blocks(text):
        out.append(text[last:start].rstrip("\n"))
        last = end
    out.append(text[last:].lstrip("\n"))
    return "\n\n".join(p for p in out if p) + "\n"


def with_block(text, block, repair):
    """Replace the file's block with the new one, or append it. Raises ValueError on broken blocks."""
    if text is None:
        return f"# Project instructions\n\n{block}"
    blocks = sb.find_blocks(text)
    if any(end is None for _, end, _ in blocks):
        raise ValueError("a Story project block has no end marker; fix it by hand, then re-run")
    if len(blocks) > 1 and not repair:
        raise ValueError(f"{len(blocks)} Story project blocks in one file; re-run with --repair to keep one")
    if not blocks:
        sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
        return text + sep + block
    start, end, _ = blocks[0]
    new = text[:start] + block.rstrip("\n") + text[end:]
    for s2, e2, _ in reversed(sb.find_blocks(new)[1:]):
        new = new[:s2].rstrip("\n") + "\n" + new[e2:].lstrip("\n")
    return new


def main(argv):
    opts, flags, pos = parse_args(argv)
    dry, force, repair, keep = "--dry-run" in flags, "--force" in flags, "--repair" in flags, "--keep" in flags
    target = Path(pos[0] if pos else ".").resolve()
    if not target.is_dir():
        print(f"error: {target} is not a directory")
        return 2

    agents, claude = target / "AGENTS.md", target / "CLAUDE.md"
    files = {"AGENTS.md": read(agents), "CLAUDE.md": read(claude)}
    status, detail, current, src = sb.classify(files)

    if keep:
        if current is None:
            print(f"error: --keep needs existing settings, but the project's setup is '{status}' ({detail})")
            return 4
        settings = current
    else:
        if "preset" not in opts:
            print("error: choose --preset (" + ", ".join(list(sb.PRESETS) + ["custom"]) + ")")
            return 4
        try:
            settings = sb.resolve(opts["preset"], **{k: opts.get(k) for k in ("plan", "draft", "revise", "craft-language", "check-in")})
        except ValueError as e:
            print(f"error: {e}")
            return 4
    problems = sb.validate(settings)
    if problems:
        print("error: these settings can't be used:\n- " + "\n- ".join(problems))
        return 4

    kb = target / "kb"
    pages = len([f for f in kb.rglob("*") if f.is_file() and f.name not in (".gitkeep", "vocab.md")]) if kb.is_dir() else 0
    adopted = (target / "work" / "adopt" / "provenance.md").is_file()
    if pages >= ESTABLISHED_KB_PAGES and status == "none" and not adopted and not force:
        msg = (f"NOTE: kb/ already holds {pages} pages and there is no Story project block. "
               "This is an existing project: bring it in with story-adopt first.")
        if not dry:
            print(msg + "\nNothing was written. (Use --force only if you are sure.)")
            return 3
        print(msg)

    log = []

    def make_dir(path):
        if path.is_dir():
            return
        log.append(f"create   {path.relative_to(target)}/")
        if not dry:
            path.mkdir(parents=True)
            (path / ".gitkeep").write_text("")

    for d in FACT_DIRS:
        make_dir(kb / d)
    for d in WORK_DIRS:
        make_dir(target / "work" / d)
    if not (kb / "vocab.md").exists():
        log.append("create   kb/vocab.md")
        if not dry:
            (kb / "vocab.md").write_text(VOCAB_STUB)

    # The block goes into AGENTS.md if it exists, else CLAUDE.md if it exists, else a new AGENTS.md.
    instr = agents if files["AGENTS.md"] is not None else (claude if files["CLAUDE.md"] is not None else agents)
    old = files[instr.name]
    try:
        new = with_block(old, sb.render(settings), repair)
    except ValueError as e:
        print(f"error: {instr.name}: {e}")
        return 6

    writes = []
    if new != old:
        writes.append((instr, old, new))
    if status == "conflicting":
        other = claude if instr == agents else agents
        if repair:
            other_old = files[other.name]
            other_new = without_blocks(other_old)
            if "AGENTS.md" not in other_new:
                other_new = other_new.rstrip("\n") + ("\n\n@AGENTS.md\n" if other.name == "CLAUDE.md" else "\n\nSee [AGENTS.md](./AGENTS.md) for the Story project settings.\n")
            writes.append((other, other_old, other_new))
        else:
            log.append(f"note     {other.name} also has a block; AGENTS.md wins. Re-run with --repair to replace it with a pointer.")
    if old is None and instr == agents and files["CLAUDE.md"] is None:
        writes.append((claude, None, POINTER))

    for path, before, after in writes:
        verb = "create" if before is None else "update"
        log.append(f"{verb}   {path.name}" + (" (Story project block only)" if before is not None and path == instr else ""))
        if dry:
            log.extend(difflib.unified_diff((before or "").splitlines(), after.splitlines(),
                                            f"{path.name} (now)", f"{path.name} (after)", lineterm=""))
        else:
            path.write_text(after, encoding="utf-8")

    head = "DRY RUN: nothing written\n" if dry else ""
    print(head + f"settings: {sb.PRESET_LABELS[settings['preset']]} " +
          " ".join(f"{k}={settings[k]}" for k in sb.KEYS[1:]) + ("\n" + "\n".join(log) if log else "\nno changes"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
