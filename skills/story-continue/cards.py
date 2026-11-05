#!/usr/bin/env python3
"""Chapter cards: short derived summaries that let a long story be read in tiers.

Usage:
  cards.py report [project_dir]             list chapters whose card is missing or stale, and orphan cards
  cards.py stamp <project_dir> <chapter>    put the chapter's current content hash on its card
  cards.py hash <chapter.md>                print a chapter's content hash

A card lives in work/cards/ under the chapter's file name. Its first line is
`<!-- card: <chapter file>; hash: <12 hex> -->`. The hash covers the chapter's paragraphs, ignoring the
status line and whitespace, so approving a chapter (which removes its status line) does not make its card
stale, and any change to the prose does. `report` only reads; `stamp` only rewrites the card's first line.
"""
import hashlib
import re
import sys
from pathlib import Path

STATUS_RE = re.compile(r"<!--\s*status:.*?-->", re.I)
HEADER_RE = re.compile(r"^<!--\s*card:\s*(.*?);\s*hash:\s*([0-9a-f]{12})\s*-->\s*$")
SKIP_DIRS = {"_previous", "_delivered"}


def body(text):
    """A chapter's paragraphs, ignoring its status line and whitespace differences."""
    lines = text.splitlines()
    for i, line in enumerate(lines[:5]):
        if STATUS_RE.search(line):
            lines[i] = ""
    return [" ".join(p.split()) for p in re.split(r"\n\s*\n", "\n".join(lines)) if p.strip()]


def body_hash(text):
    return hashlib.sha1("\n".join(body(text)).encode("utf-8")).hexdigest()[:12]


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def chapters(root):
    d = root / "work" / "drafts"
    if not d.is_dir():
        return []
    return sorted(f for f in d.rglob("*.md") if f.is_file() and not SKIP_DIRS & set(f.relative_to(d).parts))


def card_path(root, chapter):
    return root / "work" / "cards" / chapter.name


def card_hash(card_text):
    """The hash on a card's first line, or None when it has no header."""
    first = card_text.splitlines()[0] if card_text.strip() else ""
    m = HEADER_RE.match(first)
    return m.group(2) if m else None


def report(root):
    ok, missing, stale = [], [], []
    names = set()
    for ch in chapters(root):
        names.add(ch.name)
        cp = card_path(root, ch)
        if not cp.is_file():
            missing.append(ch.name)
        elif card_hash(read(cp)) == body_hash(read(ch)):
            ok.append(ch.name)
        else:
            stale.append(ch.name)
    cards = root / "work" / "cards"
    orphan = sorted(f.name for f in cards.glob("*.md")) if cards.is_dir() else []
    orphan = [n for n in orphan if n not in names]
    return {"chapters": len(names), "ok": ok, "missing": missing, "stale": stale, "orphan": orphan}


def main(argv):
    if len(argv) >= 2 and argv[1] == "hash" and len(argv) == 3:
        p = Path(argv[2])
        if not p.is_file():
            print(f"error: {p} is not a file")
            return 2
        print(body_hash(read(p)))
        return 0
    if len(argv) >= 2 and argv[1] == "report" and len(argv) <= 3:
        root = Path(argv[2] if len(argv) == 3 else ".").resolve()
        if not root.is_dir():
            print(f"error: {root} is not a directory")
            return 2
        r = report(root)
        print(f"chapters: {r['chapters']}")
        print(f"cards_ok: {len(r['ok'])}")
        for key in ("missing", "stale", "orphan"):
            print(f"cards_{key}: {', '.join(r[key]) or 'none'}")
        return 0
    if len(argv) == 4 and argv[1] == "stamp":
        root = Path(argv[2]).resolve()
        ch = root / "work" / "drafts" / argv[3]
        if not ch.is_file():
            print(f"error: no chapter {ch}")
            return 2
        cp = card_path(root, ch)
        if not cp.is_file():
            print(f"error: write the card at {cp} first, then stamp it")
            return 2
        lines = read(cp).splitlines()
        if lines and HEADER_RE.match(lines[0]):
            lines = lines[1:]
        if not any(line.strip() for line in lines):
            print(f"error: the card at {cp} has no content")
            return 2
        h = body_hash(read(ch))
        cp.write_text(f"<!-- card: {ch.name}; hash: {h} -->\n" + "\n".join(lines).strip("\n") + "\n", encoding="utf-8")
        print(f"stamped {cp.name} {h}")
        return 0
    print(__doc__.strip().split("\n\n")[1])
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
