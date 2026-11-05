#!/usr/bin/env python3
"""Mechanical hygiene checks for fiction written or revised by an AI. Standard library only.

Usage: check_text.py <file-or-folder> [--strict] [--words MIN-MAX]

Reports, with file and line: assistant or instruction text that leaked into the prose,
stray Markdown, unbalanced double quotes, duplicated paragraphs, mixed quote styles,
encoding damage, whitespace problems, a last line that stops mid-sentence (a truncated
chapter), a long phrase repeated three or more times (a repetition loop), and, when
--words is given, a chapter outside that range (either bound may be left out: 1800-2500,
1800-, -2500). Word counts are for languages written with spaces. These are warnings to
look at, never verdicts about the writing. Exit status is 0 unless --strict is given and there are warnings
(1), or the target cannot be read (2).

HTML comments (status lines, origin comments) and fenced code blocks are ignored.
Folders named _previous, _delivered, and cards are skipped.
"""
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

EXTENSIONS = {".md", ".markdown", ".txt", ".text"}
SKIP_DIRS = {"_previous", "_delivered", "cards", ".git", "__pycache__"}

WRAPPER = [
    re.compile(r"^\s*(sure|certainly|of course|absolutely)\b[!,.]", re.I),
    re.compile(r"\bhere(?:'s| is| are)\s+(?:the|your|a|an)\s+(?:revised |updated |next |new |final |rewritten |full )?"
               r"(?:chapter|scene|draft|version|rewrite|continuation|passage|opening)\b", re.I),
    re.compile(r"\bI hope (?:this|that) (?:captures|helps|works|is what|meets)", re.I),
    re.compile(r"\b(?:would|shall) you like me to\b", re.I),
    re.compile(r"\blet me know if you(?:'d| would)? (?:like|want|need)\b", re.I),
    re.compile(r"\bas an (?:AI|artificial intelligence|language model)\b", re.I),
    re.compile(r"^\s*(?:note|word count|author's note|editor's note)\s*:", re.I),
    re.compile(r"^\s*(?:chapter|scene)\s+\w+\s+(?:continues|continued)\b", re.I),
]
PLACEHOLDER = re.compile(r"\b(?:TODO|TK|TBD|FIXME|XXX)\b|\[(?:insert|placeholder|add|fill)[^\]\n]*\]", re.I)
PLACEHOLDER_CASE = re.compile(r"\b(?:TODO|TK|TBD|FIXME|XXX)\b")
MOJIBAKE = re.compile("â€[™œ\u009d”“˜¦]|Ã[©¨¢ª®´¼¶§±]|Â[  ]|ï»¿")
ZERO_WIDTH = re.compile("[​‌‍⁠﻿]")
CONTROL = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
OPEN_CURLY, CLOSE_CURLY = "“", "”"
WORD = re.compile(r"\w+(?:['’]\w+)*")
LOOP_WORDS = 8  # a phrase this long, repeated three times, is not a refrain
MIN_WORDS_TO_JUDGE_ENDING = 30


def blank_ignored(text):
    """Blank HTML comments and fenced code, keeping every newline so line numbers hold."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    return re.sub(r"^(```|~~~).*?^\1[^\n]*$", blank, text, flags=re.S | re.M)


def paragraphs(text):
    """[(start_line, text)] for blocks separated by blank lines."""
    out, buf, start = [], [], 0
    for n, line in enumerate(text.split("\n"), 1):
        if line.strip():
            if not buf:
                start = n
            buf.append(line)
        elif buf:
            out.append((start, "\n".join(buf)))
            buf = []
    if buf:
        out.append((start, "\n".join(buf)))
    return out


def strip_quoted(line):
    line = re.sub(r"“[^”]*”", lambda m: " " * len(m.group(0)), line)
    return re.sub(r'"[^"]*"', lambda m: " " * len(m.group(0)), line)


def check_leaks(lines, add):
    for n, line in enumerate(lines, 1):
        bare = strip_quoted(line)
        if any(p.search(bare) for p in WRAPPER):
            add(n, "leak.wrapper", "looks like assistant or instruction text, not story prose")
        elif PLACEHOLDER_CASE.search(bare) or re.search(r"\[(?:insert|placeholder|add|fill)[^\]\n]*\]", bare, re.I):
            add(n, "leak.placeholder", "placeholder text left in the prose")


def check_markdown(paras, add):
    first = True
    for start, para in paras:
        for off, line in enumerate(para.split("\n")):
            n = start + off
            stripped = line.strip()
            if first and off == 0 and re.match(r"#\s+\S", stripped):
                continue  # a chapter title
            if re.match(r"#{1,6}\s+\S", stripped):
                add(n, "markdown.heading", "heading inside the prose (only a chapter title belongs here)")
            elif re.match(r"(?:[-*+]\s+\S|\d+[.)]\s+\S)", stripped) and not re.match(r"[-*+]\s*[-*+]\s*[-*+]?\s*$", stripped):
                add(n, "markdown.list", "list marker at the start of a line of prose")
            elif stripped.startswith(">"):
                add(n, "markdown.quote", "blockquote marker in the prose")
            elif re.match(r"\|.*\|", stripped):
                add(n, "markdown.table", "table row in the prose")
            if "**" in line or "__" in line:
                add(n, "markdown.bold", "bold markers in the prose")
            if "`" in line:
                add(n, "markdown.code", "backticks in the prose")
        first = False


def check_quotes(paras, text, add):
    has_straight = '"' in text
    has_curly = OPEN_CURLY in text or CLOSE_CURLY in text
    if has_straight and has_curly:
        add(1, "quotes.mixed", "both straight and curly double quotes are used")
    pending = False
    pending_line = 0
    for start, para in paras:
        depth = 1 if pending and para.lstrip().startswith((OPEN_CURLY, '"')) else 0
        continued = depth == 1
        if pending and not continued:
            add(pending_line, "quotes.unbalanced", "a quotation is opened and never closed")
        pending = False
        i = 0
        if continued:
            i = para.index(next(c for c in para if c in (OPEN_CURLY, '"'))) + 1
        for ch in para[i:]:
            if ch == OPEN_CURLY:
                if depth:
                    add(start, "quotes.nested-open", "a second opening quote inside an open quotation")
                depth = 1
            elif ch == CLOSE_CURLY:
                if not depth:
                    add(start, "quotes.stray-close", "a closing quote with nothing open")
                depth = 0
            elif ch == '"':
                depth = 0 if depth else 1
        if depth:
            pending, pending_line = True, start
    if pending:
        add(pending_line, "quotes.unbalanced", "a quotation is opened and never closed")


def norm(s):
    return re.sub(r"[\W_]+", " ", s.lower()).strip()


def check_duplicates(paras, add):
    seen = {}
    long_ones = []
    for start, para in paras[:400]:
        key = norm(para)
        if len(key) < 40:
            continue
        if key in seen:
            add(start, "dup.paragraph", f"repeats the paragraph at line {seen[key]}")
            continue
        seen[key] = start
        if len(key) >= 80:
            for other_start, other_key in long_ones:
                if abs(len(key) - len(other_key)) < 0.2 * len(key) and SequenceMatcher(None, key, other_key).ratio() >= 0.9:
                    add(start, "dup.near", f"nearly repeats the paragraph at line {other_start}")
                    break
            long_ones.append((start, key))


def check_ending(paras, add):
    """A chapter whose last line stops on a letter, digit, comma, or hyphen was probably cut off.

    Closing quotes, sentence punctuation, and em dashes are fine (a dash is a deliberate interruption). A
    scene-break marker, a short all-caps line such as THE END, and a very short file are not judged."""
    if not paras:
        return
    start, last = paras[-1]
    last = last.strip()
    if not any(c.isalpha() for c in last):
        return
    if len(WORD.findall(" ".join(p for _, p in paras))) < MIN_WORDS_TO_JUDGE_ENDING:
        return
    if len(last.split()) <= 3 and last.isupper():
        return
    end = last[-1]
    if end.isalnum() or end in ",;:-\u2013":
        add(start + last.count("\n"), "truncated.ending", "the last line stops mid-sentence (no closing punctuation); the chapter may be cut off")


def check_loops(text, add):
    """The same long phrase three or more times, without overlapping, is how a degenerating draft looks."""
    words = []
    for n, line in enumerate(text.split("\n"), 1):
        for m in WORD.finditer(line):
            words.append((m.group(0).lower().replace("’", "'"), n))
    spans = {}
    for i in range(len(words) - LOOP_WORDS + 1):
        key = tuple(w for w, _ in words[i:i + LOOP_WORDS])
        spans.setdefault(key, []).append(i)
    covered = set()
    for key, starts in sorted(spans.items(), key=lambda kv: kv[1][0]):
        picked, last_end = [], -1
        for i in starts:
            if i >= last_end:
                picked.append(i)
                last_end = i + LOOP_WORDS
        if len(picked) >= 3 and picked[0] not in covered:
            # Grow the match while every occurrence continues the same way, so one repeated sentence is one finding.
            length = LOOP_WORDS
            bounds = picked[1:] + [len(words)]
            while all(i + length < nxt for i, nxt in zip(picked, bounds)) and len({words[i + length][0] for i in picked}) == 1:
                length += 1
            shown = [w for w, _ in words[picked[0]:picked[0] + length]]
            phrase = " ".join(shown[:14]) + (" ..." if len(shown) > 14 else "")
            add(words[picked[0]][1], "repeat.loop", f"the phrase \"{phrase}\" occurs {len(picked)} times (ignore it if it is a deliberate refrain, song, or repeated document header)")
            for i in picked:
                covered.update(range(i, i + length))


def parse_range(spec):
    m = re.fullmatch(r"(\d*)-(\d*)", spec or "")
    if not m or not (m.group(1) or m.group(2)):
        raise ValueError(f"--words wants MIN-MAX, MIN-, or -MAX (got {spec!r})")
    lo = int(m.group(1)) if m.group(1) else None
    hi = int(m.group(2)) if m.group(2) else None
    if lo is not None and hi is not None and lo > hi:
        raise ValueError(f"--words minimum {lo} is above its maximum {hi}")
    return lo, hi


def check_length(text, bounds, add):
    lo, hi = bounds
    body = "\n".join(line for line in text.split("\n") if not re.match(r"\s*#{1,6}\s", line))
    n = len(WORD.findall(body))
    if lo is not None and n < lo:
        add(1, "length.short", f"{n} words, below the {lo} the plan or the project asks for")
    if hi is not None and n > hi:
        add(1, "length.long", f"{n} words, above the {hi} the plan or the project asks for")


def check_encoding_and_space(raw, lines, add):
    for n, line in enumerate(lines, 1):
        if "�" in line:
            add(n, "encoding.replacement", "contains a replacement character (damaged text)")
        elif MOJIBAKE.search(line):
            add(n, "encoding.mojibake", "looks like text decoded with the wrong encoding")
        if ZERO_WIDTH.search(line) and not (n == 1 and line.startswith("﻿") and not ZERO_WIDTH.search(line[1:])):
            add(n, "encoding.invisible", "contains an invisible zero-width character")
        if CONTROL.search(line):
            add(n, "encoding.control", "contains a control character")
        if "\t" in line:
            add(n, "space.tab", "tab character in the prose")
        if re.search(r"\S {2,}\S", line.strip()):
            add(n, "space.double", "double space inside a line")
    # Count blank lines in the original text, so a blanked-out comment or code block is not mistaken for blank lines.
    blanks = 0
    for n, line in enumerate(raw.split("\n"), 1):
        blanks = blanks + 1 if not line.strip() else 0
        if blanks == 3:
            add(n, "space.blank-run", "three or more blank lines in a row")


def check_file(path, bounds=None):
    raw = path.read_text(encoding="utf-8", errors="replace")
    findings = []

    def add(line, rule, message):
        findings.append((line, rule, message))

    text = blank_ignored(raw)
    lines = text.split("\n")
    paras = paragraphs(text)
    check_leaks(lines, add)
    check_markdown(paras, add)
    check_quotes(paras, text, add)
    check_duplicates(paras, add)
    check_encoding_and_space(raw, lines, add)
    check_ending(paras, add)
    check_loops(text, add)
    if bounds:
        check_length(text, bounds, add)
    return sorted(set(findings))


def targets(arg):
    p = Path(arg)
    if p.is_file():
        return [p]
    if p.is_dir():
        return sorted(f for f in p.rglob("*")
                      if f.is_file() and f.suffix.lower() in EXTENSIONS and not (SKIP_DIRS & set(f.relative_to(p).parts)))
    raise OSError(f"not found: {arg}")


def main(argv):
    rest, spec, i = [], None, 1
    while i < len(argv):
        a = argv[i]
        if a == "--words" and i + 1 < len(argv):
            spec, i = argv[i + 1], i + 1
        elif a.startswith("--words="):
            spec = a.split("=", 1)[1]
        else:
            rest.append(a)
        i += 1
    args = [a for a in rest if not a.startswith("--")]
    strict = "--strict" in rest
    bounds = None
    if "--words" in argv and spec is None:
        print("error: --words wants a range such as 1800-2500")
        return 2
    if spec is not None:
        try:
            bounds = parse_range(spec)
        except ValueError as e:
            print(f"error: {e}")
            return 2
    if len(args) != 1:
        print(__doc__)
        return 2
    try:
        files = targets(args[0])
    except OSError as e:
        print(f"error: {e}")
        return 2
    total = 0
    for f in files:
        for line, rule, message in check_file(f, bounds):
            print(f"{f}:{line}: warn: {rule}: {message}")
            total += 1
    print(f"{len(files)} file(s) checked, {total} warning(s)")
    return 1 if strict and total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
