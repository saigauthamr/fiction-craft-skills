#!/usr/bin/env python3
"""Count the prose habits a drafter cannot count by ear. English prose. Standard library only.

Usage: habits.py <chapter-file-or-folder>

For each chapter it lists, with line numbers, the places in the narration (outside quoted
speech) where it finds: comparisons (like, as if, as though, as X as, the way a), negated narration
(did not, was not, didn't), body reports (chest, breath, pulse, stomach, throat), hedges
(seemed, almost, somehow, a kind of, something like), and paragraphs of one short line. It also
gives the share of words in dialogue, any run of sentences that open with the same word, and
the chapter's first and last lines, so the openings and endings of several chapters can be
read side by side.

These are counts to look at, never verdicts, and there is no passing number. Every one of
these is ordinary in good prose. What matters is one habit carrying a page: look at each
instance and keep the ones doing work.

HTML comments and fenced code are ignored. Folders named _previous, _delivered, and cards
are skipped. Exit status is 0, or 2 when the target cannot be read.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {".md", ".markdown", ".txt", ".text"}
SKIP_DIRS = {"_previous", "_delivered", "cards", ".git", "__pycache__"}
WORD = re.compile(r"\w+(?:['’]\w+)*")
SHORT_PARAGRAPH_WORDS = 6
OPENER_RUN = 3

# "like" after these words is a verb ("I'd like a drink"), and before these it points, not compares ("like that").
NOT_COMPARISON = r"(?<!would )(?<!'d )(?<!’d )(?<!might )(?<!to )(?<!not )(?<!n't )(?<!n’t )(?<!I )(?<!you )(?<!we )(?<!they )"
HABITS = [
    ("comparisons", re.compile(
        r"\bas (?:if|though)\b|\bas \w+ as\b|"
        + NOT_COMPARISON + r"\blike\b(?! (?:to|that|this|it|him|her|them|you|me|us|so)\b)|"
        r"\bthe way (?:a|an|the|you|he|she|they|it|some|people|men|women|children)\b", re.I)),
    ("negated narration", re.compile(
        r"\b(?:did|does|do|was|were|is|are|had|has|would|could) not\b|"
        r"\b(?:did|does|do|was|were|is|are|had|has|would|could)n['’]t\b", re.I)),
    ("body reports", re.compile(
        r"\b(?:chest|breath|breaths|pulse|stomach|throat|heartbeat|lungs|ribs|spine|jaw|knuckles|gut)\b|"
        r"\bheart (?:was|pounded|hammered|raced|sank|lurched|stopped|thudded|skipped)\b|"
        r"\b(?:swallowed|exhaled|inhaled|shivered|trembled)\b", re.I)),
    ("hedges", re.compile(
        r"\b(?:seemed|seems|almost|somehow|vaguely)\b|\ba (?:kind|sort) of\b|\bsomething (?:like|in|about)\b|"
        r"\bnot (?:quite|exactly)\b", re.I)),
]


def blank_ignored(text):
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    return re.sub(r"^(```|~~~).*?^\1[^\n]*$", blank, text, flags=re.S | re.M)


def blank_speech(text):
    """Blank quoted speech, keeping length and newlines, so only narration is searched.

    A quotation that never closes is blanked to the end of its paragraph (continued speech)."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    out = []
    for para in re.split(r"(\n\s*\n)", text):
        para = re.sub(r"“[^”]*(?:”|$)", blank, para, flags=re.S)
        para = re.sub(r'"[^"]*(?:"|$)', blank, para, flags=re.S)
        out.append(para)
    return "".join(out)


def is_prose_line(line):
    s = line.strip()
    return bool(s) and not re.match(r"#{1,6}\s", s) and not re.fullmatch(r"[-*_\s]{3,}|\*\s\*\s\*", s)


def paragraphs(lines):
    """[(start_line, [lines])] for blocks of prose separated by blank lines, headings, or scene breaks."""
    out, buf, start = [], [], 0
    for n, line in enumerate(lines, 1):
        if is_prose_line(line):
            if not buf:
                start = n
            buf.append(line)
        elif buf:
            out.append((start, buf))
            buf = []
    if buf:
        out.append((start, buf))
    return out


def opener_runs(narration_lines, breaks):
    """Runs of OPENER_RUN or more sentences in a row that start with the same word. A scene break ends a run."""
    sentences = []
    for n, line in enumerate(narration_lines, 1):
        if n in breaks:
            sentences.append((None, n))
        for s in re.split(r"(?<=[.?!])\s+", line.strip()):
            m = WORD.match(s.lstrip("—–- "))
            if m and len(WORD.findall(s)) > 1:
                sentences.append((m.group(0).lower(), n))
    runs, i = [], 0
    while i < len(sentences):
        j = i
        while j + 1 < len(sentences) and sentences[j + 1][0] == sentences[i][0]:
            j += 1
        if sentences[i][0] is not None and j - i + 1 >= OPENER_RUN:
            runs.append((sentences[i][0], j - i + 1, sentences[i][1]))
        i = j + 1
    return runs


def clip(s, width=110):
    s = " ".join(s.split())
    return s if len(s) <= width else s[:width - 3].rstrip() + "..."


def report(path):
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = blank_ignored(raw)
    lines = text.split("\n")
    prose_lines = [l if is_prose_line(l) else "" for l in lines]
    narration = blank_speech("\n".join(prose_lines)).split("\n")
    total = len(WORD.findall("\n".join(prose_lines)))
    spoken = total - len(WORD.findall("\n".join(narration)))
    paras = paragraphs(lines)
    out = []
    if not total:
        return [f"{path}: no prose found"]
    short = [start for start, buf in paras
             if len(WORD.findall(" ".join(buf))) <= SHORT_PARAGRAPH_WORDS
             and not re.match(r'\s*["“]', buf[0])]
    out.append(f"{path}: {total:,} words, {round(100 * spoken / total)}% in dialogue, {len(paras)} paragraphs")
    for name, pattern in HABITS:
        hits = [n for n, line in enumerate(narration, 1) for _ in pattern.finditer(line)]
        rate = 1000 * len(hits) / total
        where = ", ".join(str(n) for n in hits[:30]) + (" ..." if len(hits) > 30 else "")
        out.append(f"  {name}: {len(hits)} ({rate:.1f} per 1,000 words)" + (f"; lines {where}" if hits else ""))
    out.append(f"  one-line paragraphs of narration: {len(short)} of {len(paras)}"
               + (f"; lines {', '.join(str(n) for n in short[:30])}" if short else ""))
    breaks = {n for n, l in enumerate(lines, 1) if l.strip() and not is_prose_line(l)}
    for word, count, line in opener_runs(narration, breaks):
        out.append(f"  {count} sentences in a row open with \"{word}\", from line {line}")
    out.append(f"  first line: {clip(paras[0][1][0])}")
    out.append(f"  last line: {clip(paras[-1][1][-1])}")
    return out


def targets(arg):
    p = Path(arg)
    if p.is_file():
        return [p]
    if p.is_dir():
        return sorted(f for f in p.rglob("*")
                      if f.is_file() and f.suffix.lower() in EXTENSIONS and not (SKIP_DIRS & set(f.relative_to(p).parts)))
    raise OSError(f"not found: {arg}")


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    try:
        files = targets(args[0])
    except OSError as e:
        print(f"error: {e}")
        return 2
    for f in files:
        print("\n".join(report(f)))
    print(f"{len(files)} file(s) read. Counts to look at, not verdicts.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
