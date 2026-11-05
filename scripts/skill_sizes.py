#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["tiktoken==0.14.0"]
# ///
# ─── How to run ───
# Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh
# Report (standard library only): python3 -B -I scripts/skill_sizes.py
# Record words and comparison tokens: uv run scripts/skill_sizes.py --write-baseline --tokens
# ──────────────────
"""Skill sizes: words and measured tokens, with hand-written text and generated check lists kept apart.

Usage:
  skill_sizes.py [repo_root]                              print a table against the baseline
  skill_sizes.py --write-baseline [--tokens] [repo_root]  record today's sizes as the baseline

A skill is loaded whole whenever a request reaches it, so size is a per-request cost. Hand-written text and
the check lists the compiler generates grow for different reasons, so they are measured separately: every
`<!-- generated:checks:start ... -->` block counts as generated, named or not.

Size never fails a build. Invalid commands or failed measurements do fail. Advisories printed by the lint:
  target    a skill's hand-written or generated text is above an optimization target
  growth    a skill grew well beyond its recorded baseline (more than GROWTH and more than MIN_GROWTH_WORDS)

The baseline (size-baseline.json, next to this script) holds words for every skill and, when measured, tokens.
Tokens use tiktoken's cl100k_base encoding, a reproducible comparison measure, NOT Claude billing or
context usage. Whole-file counts include frontmatter; hand/generated counts exclude it and are encoded
independently, so the parts need not sum to the whole. Refreshes never carry forward old token counts.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
import sys
from pathlib import Path
from typing import Protocol

HERE = Path(__file__).resolve().parent
BASELINE = HERE / "size-baseline.json"
GENERATED = re.compile(r"<!-- generated:checks:start(?: [a-z-]+)? -->.*?<!-- generated:checks:end(?: [a-z-]+)? -->\n?", re.S)
CHECK_LINE = re.compile(r"(?m)^- `[a-z]+\.[a-z]+\.\d+`")
# Optimization targets, in words. They are advisory: a skill above one is a candidate to look at, not a defect.
TARGETS = {"reference": 800, "stage hand-written": 1500, "stage generated": 1500}
GROWTH = 0.25
MIN_GROWTH_WORDS = 100


def split(text):
    """(hand-written body, generated blocks) of a skill file."""
    body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    blocks = GENERATED.findall(body)
    return GENERATED.sub("", body), "".join(blocks)


def kind(text):
    m = re.search(r"^\s*type:\s*(\S+)", text, re.M)
    return "reference" if (m and m.group(1) in ("framework", "hub")) else "stage"


def measure(md):
    text = md.read_text(encoding="utf-8")
    hand, gen = split(text)
    return {"kind": kind(text), "hand_words": len(hand.split()), "gen_words": len(gen.split()), "checks": len(CHECK_LINE.findall(gen))}


def measure_all(skills_dir):
    return {md.parent.name: measure(md) for md in sorted(Path(skills_dir).glob("*/SKILL.md"))}


def load_baseline(path=BASELINE):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def advisories(measures, baseline=None):
    """Advisory lines for a {skill: measure} mapping. Never errors."""
    out = []
    base = (baseline or {}).get("skills", {})
    for name, m in sorted(measures.items()):
        if m["kind"] == "reference":
            if m["hand_words"] + m["gen_words"] > TARGETS["reference"]:
                out.append(f"{name}: {m['hand_words'] + m['gen_words']} words, above the optimization target of {TARGETS['reference']}")
        else:
            if m["hand_words"] > TARGETS["stage hand-written"]:
                out.append(f"{name}: {m['hand_words']} words of hand-written text, above the optimization target of {TARGETS['stage hand-written']}")
            if m["gen_words"] > TARGETS["stage generated"]:
                out.append(f"{name}: {m['gen_words']} words of generated checks ({m['checks']} checks), above the optimization target of {TARGETS['stage generated']}")
        b = base.get(name)
        if not b:
            continue
        for label, key in (("hand-written text", "hand_words"), ("generated checks", "gen_words")):
            now, then = m[key], b.get(key, 0)
            if now - then > MIN_GROWTH_WORDS and now > then * (1 + GROWTH):
                out.append(f"{name}: {label} grew from {then} to {now} words since the baseline (+{round(100 * (now - then) / max(then, 1))}%)")
    return out


class Tokenizer(Protocol):
    def encode_ordinary(self, text: str) -> list[int]: ...


def write_baseline(root: Path, tokenizer: Tokenizer | None = None) -> int:
    measures = measure_all(root / "skills")
    skills = {}
    for name, m in measures.items():
        entry = {"hand_words": m["hand_words"], "gen_words": m["gen_words"], "checks": m["checks"]}
        md = root / "skills" / name / "SKILL.md"
        entry["sha256"] = hashlib.sha256(md.read_bytes()).hexdigest()
        if tokenizer is not None:
            text = md.read_text(encoding="utf-8")
            hand, gen = split(text)
            for part, content in (("whole", text), ("hand", hand), ("gen", gen)):
                entry[f"{part}_tokens"] = len(tokenizer.encode_ordinary(content))
        skills[name] = entry
    data = {
        "about": "Words exclude frontmatter. Whole-file tokens include it; hand/generated tokens are encoded separately. Comparison tokens are not Claude usage.",
        "tokens_measured_with": f"tiktoken {importlib.metadata.version('tiktoken')}, cl100k_base, encode_ordinary" if tokenizer is not None else None,
        "growth_warning": f"more than {int(GROWTH * 100)}% and more than {MIN_GROWTH_WORDS} words beyond the baseline",
        "skills": skills,
    }
    (root / "scripts" / "size-baseline.json").write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    return len(skills)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=HERE.parent)
    parser.add_argument("--write-baseline", action="store_true")
    parser.add_argument("--tokens", action="store_true", help="measure cl100k_base comparison tokens (requires tiktoken)")
    args = parser.parse_args(argv[1:])
    root = args.root.resolve()
    if not (root / "skills").is_dir() or not (root / "scripts").is_dir():
        parser.error("root must contain skills/ and scripts/")
    if args.tokens and not args.write_baseline:
        parser.error("--tokens requires --write-baseline")
    if args.write_baseline:
        tokenizer = None
        if args.tokens:
            import tiktoken
            tokenizer = tiktoken.get_encoding("cl100k_base")
        n = write_baseline(root, tokenizer)
        print(f"baseline written for {n} skills" + (" with cl100k_base comparison tokens" if tokenizer else " (words only)"))
        return 0
    measures = measure_all(root / "skills")
    baseline = load_baseline(root / "scripts" / "size-baseline.json")
    base = baseline.get("skills", {})
    print(f"baseline tokens: {baseline.get('tokens_measured_with') or 'not measured'}")
    print(f"{'skill':42} {'hand':>6} {'gen':>6} {'checks':>6} {'base tokens':>11}  vs baseline (words)")
    for name, m in measures.items():
        b = base.get(name, {})
        t = b.get("whole_tokens")
        change = ""
        if b:
            change = f"hand {m['hand_words'] - b['hand_words']:+d}, gen {m['gen_words'] - b['gen_words']:+d}"
        print(f"{name:42} {m['hand_words']:>6} {m['gen_words']:>6} {m['checks']:>6} {t if t is not None else '':>11}  {change}")
    for a in advisories(measures, baseline):
        print(f"advisory: {a}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
