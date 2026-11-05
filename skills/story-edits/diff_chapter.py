#!/usr/bin/env python3
"""Compare the chapter the AI delivered with the writer's edited version, paragraph by paragraph.

Usage: diff_chapter.py <delivered.md> <current.md>

Prints a summary and one line per change, with line numbers in each file. Read-only. Status lines
and whitespace differences are ignored, so a chapter that only had its status line removed, or was
re-wrapped, reports as unchanged.
"""
import difflib
import re
import sys
from pathlib import Path

STATUS_RE = re.compile(r"<!--\s*status:.*?-->", re.I)
PAIR_RATIO = 0.5  # a cut paragraph and an added one this similar count as one rewritten paragraph
PREVIEW = 70


def paragraphs(text):
    """[(first_line, last_line, normalized_text, original_text)] for each non-blank paragraph."""
    lines = text.splitlines()
    for i, line in enumerate(lines[:5]):
        if STATUS_RE.search(line):
            lines[i] = ""
    out, start, buf = [], None, []
    for n, line in enumerate(lines + [""], 1):
        if line.strip():
            if start is None:
                start = n
            buf.append(line)
        elif buf:
            raw = " ".join(s.strip() for s in buf)
            out.append((start, n - 1, " ".join(raw.split()), raw))
            start, buf = None, []
    return out


def loc(p):
    return f"line {p[0]}" if p[0] == p[1] else f"lines {p[0]}-{p[1]}"


def preview(p):
    s = p[3]
    return s if len(s) <= PREVIEW else s[:PREVIEW].rstrip() + "..."


def compare(delivered, current):
    a, b = paragraphs(delivered), paragraphs(current)
    sm = difflib.SequenceMatcher(None, [p[2] for p in a], [p[2] for p in b], autojunk=False)
    kept, cut, added, rewritten = 0, [], [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            kept += i2 - i1
        elif tag == "delete":
            cut += a[i1:i2]
        elif tag == "insert":
            added += b[j1:j2]
        else:
            old, new = list(a[i1:i2]), list(b[j1:j2])
            for o in old:
                best, best_r = None, PAIR_RATIO
                for n in new:
                    r = difflib.SequenceMatcher(None, o[2], n[2], autojunk=False).ratio()
                    if r >= best_r:
                        best, best_r = n, r
                if best is not None:
                    new.remove(best)
                    rewritten.append((o, best, best_r))
                else:
                    cut.append(o)
            added += new
    return kept, cut, added, rewritten


def main(argv):
    if len(argv) != 3:
        print("usage: diff_chapter.py <delivered.md> <current.md>")
        return 2
    try:
        delivered = Path(argv[1]).read_text(encoding="utf-8")
        current = Path(argv[2]).read_text(encoding="utf-8")
    except OSError as e:
        print(f"error: {e}")
        return 2
    kept, cut, added, rewritten = compare(delivered, current)
    changed = bool(cut or added or rewritten)
    print(f"result: {'edited' if changed else 'unchanged'}")
    print(f"kept: {kept}")
    print(f"rewritten: {len(rewritten)}")
    print(f"cut: {len(cut)}")
    print(f"added: {len(added)}")
    for o, n, r in rewritten:
        print(f"rewritten: delivered {loc(o)} -> current {loc(n)} (similarity {r:.2f})")
        print(f"  was: {preview(o)}")
        print(f"  now: {preview(n)}")
    for p in cut:
        print(f"cut: delivered {loc(p)}: {preview(p)}")
    for p in added:
        print(f"added: current {loc(p)}: {preview(p)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
