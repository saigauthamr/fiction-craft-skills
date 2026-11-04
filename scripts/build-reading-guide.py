#!/usr/bin/env python3
"""Build READING-ORDER.md (an ordered, linked index) and reading-edition.md (every skill in one file).

Usage: build-reading-guide.py [repo_root]
Order within a hub follows the hub's own Children list. Standard library only.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
skills = root / "skills"


def read(name):
    t = (skills / name / "SKILL.md").read_text(encoding="utf-8")
    fm, body = t.split("\n---\n", 1)
    m = re.search(r"description: >\n((?:  .*\n?)+)", fm + "\n")
    desc = " ".join(l.strip() for l in m.group(1).splitlines()) if m else ""
    return desc, body.strip()


def children(hub):
    body = read(hub)[1]
    sec = body.split("## Children")[1].split("\n## ")[0]
    return re.findall(r"^- `([a-z0-9-]+)`", sec, re.M)


SKIP_STARTS = ("For fiction", "First stage", "Not for", "Can also", "It may", "Do not")


def first_sentence(desc):
    """One line on what the skill gives: the first sentence after the 'Use when' one that is not a side note."""
    sents = [x.strip() for x in re.split(r"(?<=[.?!])\s+", desc) if x.strip()]
    pick = next((x for x in sents[1:] if not x.startswith(SKIP_STARTS)), sents[0] if sents else "")
    return pick if len(pick) <= 230 else pick[:227].rsplit(" ", 1)[0] + "..."


PARTS = [
    ("Part 1. Setting up and moving through a story", "Read these first. Onboarding decides who plans, drafts, and revises; the rest are the stages every story moves through, in order. Each stage adapts to those settings.",
     ["story-onboard", "story-next", "story-adopt", "story-develop", "story-plan", "story-draft", "story-check", "story-revise", "story-steer", "story-continue", "story-learn"]),
    ("Part 2. Tools", "Design tools any writer can use, whoever writes the prose: a rules lab for magic and world rules, character build sheets, and voice demos.",
     ["story-worldbuild", "story-cast", "story-voice"]),
    ("Part 3. Process and mindset", "How a writer works, takes feedback, and revises.", ["foundations"] + children("foundations")),
    ("Part 4. Plot", "The core model first, then structure, scene momentum, payoff, and planning.", ["plot"] + children("plot")),
    ("Part 5. Character", "The three scales first, then weaknesses and villains, presentation, and change.", ["character"] + children("character")),
    ("Part 6. Magic and worldbuilding", "Magic rules, then building the world, then showing it on the page.", ["magic-worldbuilding"] + children("magic-worldbuilding")),
    ("Part 7. Scene craft and prose", "Scene structure, showing and telling, viewpoint, and machine-sounding habits.", ["scene-craft"] + children("scene-craft") + ["prose-ai-tells"]),
]
order = [n for _, _, ns in PARTS for n in ns]
assert len(order) == len(set(order)), "a skill appears twice"
missing = sorted(p.name for p in skills.iterdir() if p.is_dir() and p.name not in order)
assert not missing, f"not placed in the reading order: {missing}"

words = {n: len(read(n)[1].split()) for n in order}
extra = {"prose-ai-tells": [("patterns.md", "the full pattern list with fiction examples")]}
for n, fs in extra.items():
    for f, _ in fs:
        words[n] += len((skills / n / f).read_text(encoding="utf-8").split())


def minutes(w):
    return max(1, round(w / 230))


idx = ["# Reading order", "",
       f"Every skill in the order that builds understanding, with a link to each file. {len(order)} skills, about {sum(words.values()):,} words, roughly {minutes(sum(words.values())) // 60} hours {minutes(sum(words.values())) % 60} minutes at reading pace.", "",
       "**To read everything in one file**, open `reading-edition.md`. It has a linked table of contents and every skill in this order.", "",
       "**A hub** is a short index that routes to its children, so read the hub first and then its children in the listed order.", ""]
n = 0
for title, blurb, names in PARTS:
    pw = sum(words[x] for x in names)
    idx += [f"## {title}", "", f"{blurb} ({len(names)} skills, about {minutes(pw)} minutes)", ""]
    for name in names:
        n += 1
        desc = read(name)[0]
        kind = re.search(r"^  type: (\w+)", (skills / name / "SKILL.md").read_text(), re.M).group(1)
        tag = " (hub)" if kind == "hub" else ""
        idx.append(f"{n}. [`{name}`](skills/{name}/SKILL.md){tag}: {first_sentence(desc)} ({minutes(words[name])} min)")
        for f, what in extra.get(name, []):
            idx.append(f"    - also [`{f}`](skills/{name}/{f}): {what}")
    idx.append("")
(root / "READING-ORDER.md").write_text("\n".join(idx), encoding="utf-8")

# the combined edition
ed = ["# Reading edition", "", "Every skill, in reading order, in one file. Generated from `skills/`; do not edit by hand.", "", "## Contents", ""]
n = 0
for title, blurb, names in PARTS:
    ed.append(f"**{title}**")
    for name in names:
        n += 1
        ed.append(f"- [{n}. {name}](#{n}-{name})")
    ed.append("")
n = 0
for title, blurb, names in PARTS:
    ed += ["", "---", "", f"# {title}", "", blurb, ""]
    for name in names:
        n += 1
        desc, body = read(name)
        body = re.sub(r"^# .*\n+", "", body, count=1)
        body = re.sub(r"^(#{1,5}) ", lambda m: "#" * min(6, len(m.group(1)) + 2) + " ", body, flags=re.M)
        ed += [f"## {n}. {name}", "", f"*{desc}*", "", body.strip(), ""]
        for f, _ in extra.get(name, []):
            sub = (skills / name / f).read_text(encoding="utf-8").strip()
            sub = re.sub(r"^# .*\n+", "", sub, count=1)
            sub = re.sub(r"^(#{1,5}) ", lambda m: "#" * min(6, len(m.group(1)) + 2) + " ", sub, flags=re.M)
            ed += [f"### {name}: {f}", "", sub, ""]
(root / "reading-edition.md").write_text("\n".join(ed), encoding="utf-8")
print(f"{len(order)} skills; {sum(words.values()):,} words")
