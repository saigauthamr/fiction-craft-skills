"""The Story project block: settings, validation, rendering, and parsing.

This file is the contract between onboarding (which writes the block) and the
inspector (which reads it). An identical copy sits in each skill that needs it,
so every skill stands alone; the library lint fails if the copies differ.
"""
import re

START_V1 = "<!-- story-project:start -->"
START_V2 = "<!-- story-project:start v2 -->"
START_RE = re.compile(r"<!-- story-project:start(?: (v\d+))? -->")
END = "<!-- story-project:end -->"
SETTINGS_START = "<!-- story-settings:start -->"
SETTINGS_END = "<!-- story-settings:end -->"
DIRECTOR_MARK = "(director mode)"

PRESETS = {
    "ai-writes-you-direct": ("ai", "ai", "ai"),
    "ai-drafts-you-revise": ("ai", "ai", "writer"),
    "you-outline-ai-drafts": ("writer", "ai", "writer"),
    "ai-outlines-you-write": ("ai", "writer", "writer"),
    "you-write-ai-checks": ("writer", "writer", "writer"),
    "design-only": ("ai", "none", "none"),
}
PRESET_LABELS = {
    "ai-writes-you-direct": "AI writes, you direct",
    "ai-drafts-you-revise": "AI drafts, you revise",
    "you-outline-ai-drafts": "You outline, AI drafts",
    "ai-outlines-you-write": "AI outlines, you write",
    "you-write-ai-checks": "You write, AI checks",
    "design-only": "Design only",
    "custom": "Custom",
}
ALLOWED = {
    "plan": ("ai", "writer"),
    "draft": ("ai", "writer", "alternate", "none"),
    "revise": ("ai", "writer", "none"),
    "craft-language": ("none", "brief", "full"),
    "check-in": ("chapter", "three-chapters", "part"),
}
KEYS = ("preset", "plan", "draft", "revise", "craft-language", "check-in")
STAGES = ("plan", "draft", "revise")
# Only untrusted chapters carry a status line. A chapter with none is trusted. "accepted" is the first
# build's marker: still read, as trusted, but never written.
CHAPTER_STATUSES = ("draft", "awaiting check-in", "needs revision")

LAYOUT = """Facts the story has committed to live in `kb/`. Working documents live in `work/`. If this file names other places for any of these, those take priority.

- `kb/characters/`, `kb/world/`, `kb/timeline/`, `kb/canon/`: settled story facts, one topic per file
- `kb/styles/`: voice and style files; `kb/samples/`: prose samples
- `kb/issues/`: problems and open questions that span chapters
- `kb/vocab.md`: canonical story terms, aliases, and terms to avoid
- `work/spec/`, `work/beats/`: the approved spec and chapter beats, saved only after the writer approves them
- `work/drafts/`: chapters; `work/critique-reports/`: check reports; `work/brainstorm/`: undecided notes
- `work/cards/`: short derived summaries of chapters, rebuilt from the chapters, so safe to delete
- `work/drafts/_previous/`: earlier versions of a chapter the AI revised; `work/drafts/_delivered/`: the exact text the AI handed over, kept only until the writer's edits have been learned from

Trust is the default: anything unmarked is trusted, and only untrusted material carries a marker. When the writer approves something, its marker is removed, and nothing records who approved it or when.

- A chapter the AI drafted starts with `<!-- status: draft -->`, `<!-- status: awaiting check-in -->`, or `<!-- status: needs revision: <reason> -->`. The writer's approval removes the line. A chapter with no status line is trusted, including every chapter the writer wrote.
- A fact proposed but not yet approved is a list item starting `[pending major]` or `[pending minor]`. Approval moves it into `kb/`, unmarked, and removes it from the list. A fact the writer turned down starts `[rejected]` and is never proposed again. Nothing goes into `kb/` until the writer approves it.
- Each open finding in a check report starts `[open]`. A fixed finding is deleted. One kept on purpose becomes `[resolved] declined: <reason>`.
"""

ROUTES = [
    ("asks what to do next, where to start, or says they are stuck", "story-next"),
    ("wants to set up the project, or change how we work (who writes, how much craft talk, check-ins)", "story-onboard"),
    ("has existing chapters, notes, or spreadsheets to bring in", "story-adopt"),
    ("wants the idea, premise, world, or a character questioned, sharpened, or decided (\"grill me\", \"help me design\")", "story-develop"),
    ("wants a spec, chapter beats, or a plot plan", "story-plan"),
    ("wants a chapter or scene written, or says \"go\"", "story-draft"),
    ("wants a chapter checked or reviewed, or asks whether it is any good", "story-check"),
    ("wants a chapter revised, or a check report's findings fixed", "story-revise"),
    ("has edited a chapter the AI drafted and wants the AI to learn from those edits", "story-edits"),
    ("wants to change the story in plain words (\"darker\", \"slower\", \"I don't like this character\")", "story-steer"),
    ("wants the next chapter of a serial written from what is already on the page", "story-continue"),
    ("wants to learn a craft technique, without writing anything", "story-learn"),
    ("wants magic, powers, or the rules of the world designed or stress-tested", "story-worldbuild"),
    ("wants characters, a villain, or relationships designed", "story-cast"),
    ("wants to choose how the story sounds", "story-voice"),
    ("asks about plot, pacing, a dragging middle, an opening, a payoff, events that do not cause each other, or when readers should learn a secret", "plot"),
    ("asks about a character: flat, passive, villain, motivation, arc, or writing someone they have not lived", "character"),
    ("asks about magic, worldbuilding, naming, or how much of the world to explain", "magic-worldbuilding"),
    ("asks about outlining versus discovery writing, feedback, revision, or early readers", "foundations"),
    ("asks how a scene is built or told: point of view, tense, showing versus telling, dialogue behavior, or what a character could plausibly know, see, or infer in a scene", "scene-craft"),
    ("asks to find or fix prose that sounds machine-written", "prose-ai-tells"),
]


def default_craft(draft):
    return {"ai": "none", "writer": "full"}.get(draft, "brief")


def preset_for(plan, draft, revise):
    for name, owners in PRESETS.items():
        if owners == (plan, draft, revise):
            return name
    return "custom"


def resolve(preset=None, **overrides):
    """Settings from a preset plus any per-key overrides. Validate the result separately."""
    s = {}
    if preset and preset != "custom":
        if preset not in PRESETS:
            raise ValueError(f"unknown preset '{preset}'; choose one of: {', '.join(PRESETS)}, custom")
        s.update(zip(STAGES, PRESETS[preset]))
    for k, v in overrides.items():
        if v is not None:
            s[k] = v
    if any(k not in s for k in STAGES):
        missing = [k for k in STAGES if k not in s]
        raise ValueError(f"a custom setup needs every stage owner; missing: {', '.join(missing)}")
    s.setdefault("craft-language", default_craft(s["draft"]))
    s.setdefault("check-in", "three-chapters")
    s["preset"] = preset_for(s["plan"], s["draft"], s["revise"])
    return {k: s[k] for k in KEYS}


def validate(s):
    """Return a list of problems; empty means the settings are valid."""
    errors = []
    for k, allowed in ALLOWED.items():
        if s.get(k) not in allowed:
            errors.append(f"{k} must be one of {', '.join(allowed)} (got '{s.get(k)}')")
    if errors:
        return errors
    if (s["draft"] == "none") != (s["revise"] == "none"):
        errors.append("rule 1: drafting and revising are 'none' together or not at all (design only has no prose)")
    if s["revise"] == "ai" and s["draft"] not in ("ai", "alternate"):
        errors.append("rule 2: the AI can revise only prose it drafted; with the writer drafting, revising stays with the writer (the AI can still check)")
    expected = preset_for(s["plan"], s["draft"], s["revise"])
    if s.get("preset") != expected:
        errors.append(f"preset says '{s.get('preset')}' but the stage owners match '{expected}'")
    return errors


def summary(s):
    who = {"ai": "the AI", "writer": "you"}
    parts = []
    if s["plan"] == "ai":
        parts.append("The AI plans and you approve the plan")
    else:
        parts.append("You plan")
    if s["draft"] == "none":
        parts.append("there is no prose: the result is the approved design")
    elif s["draft"] == "alternate":
        parts.append("you and the AI trade scenes")
    else:
        parts.append(f"{who[s['draft']]} draft{'s' if s['draft'] == 'ai' else ''}")
    if s["revise"] == "ai":
        parts.append("the AI revises its own drafts" + (" and you revise yours" if s["draft"] == "alternate" else ""))
    elif s["revise"] == "writer":
        parts.append("you revise")
    text = "; ".join(parts) + "."
    if s["draft"] in ("ai", "alternate"):
        text += f" The AI checks in every {'chapter' if s['check-in'] == 'chapter' else 'three chapters' if s['check-in'] == 'three-chapters' else 'part'}."
    text += " The AI checks any chapter on request. Only you make story facts canon."
    return text[0].upper() + text[1:]


def render(s):
    rows = "\n".join(f"| {k} | {s[k]} |" for k in KEYS)
    routes = "\n".join(f"| {when} | `{skill}` |" for when, skill in ROUTES)
    return (
        f"{START_V2}\n## Story project\n\n"
        f"### How we work ({PRESET_LABELS[s['preset']]})\n\n"
        f"{SETTINGS_START}\n| setting | value |\n| --- | --- |\n{rows}\n{SETTINGS_END}\n\n"
        f"{summary(s)}\n\n"
        f"### Where things go\n\n{LAYOUT}\n"
        f"### Skills for story work\n\n"
        f"For the requests below, load the named skill before answering. For this story they take priority over generic skills for the same job. Every skill reads the settings above.\n\n"
        f"| The writer... | Use |\n| --- | --- |\n{routes}\n"
        f"{END}\n"
    )


def find_blocks(text):
    """All Story project blocks in a file: (start, end_or_None, version)."""
    blocks = []
    for m in START_RE.finditer(text):
        version = m.group(1) or "v1"
        end = text.find(END, m.end())
        nxt = START_RE.search(text, m.end())
        if end == -1 or (nxt and nxt.start() < end):
            blocks.append((m.start(), None, version))
        else:
            blocks.append((m.start(), end + len(END), version))
    return blocks


def parse_settings(block_text):
    """Settings dict from a v2 block, or raise ValueError naming the problem."""
    i, j = block_text.find(SETTINGS_START), block_text.find(SETTINGS_END)
    if i == -1 or j == -1 or j < i:
        raise ValueError("the settings table markers are missing")
    s = {}
    for line in block_text[i + len(SETTINGS_START):j].splitlines():
        cells = [c.strip().lower() for c in line.strip().strip("|").split("|")]
        if len(cells) != 2 or cells[0] in ("setting", "") or set(cells[0]) <= set("-: "):
            continue
        key, value = cells
        if key not in KEYS:
            raise ValueError(f"unknown setting '{key}'")
        if key in s:
            raise ValueError(f"setting '{key}' appears twice")
        s[key] = value
    preset = s.get("preset")
    if preset is None:
        raise ValueError("the preset setting is missing")
    if preset != "custom" and preset not in PRESETS:
        raise ValueError(f"unknown preset '{preset}'")
    if preset == "custom" and any(k not in s for k in STAGES):
        raise ValueError("a custom setup is missing a stage owner")
    if preset != "custom":
        for k, v in zip(STAGES, PRESETS[preset]):
            s.setdefault(k, v)
    s.setdefault("craft-language", default_craft(s["draft"]))
    s.setdefault("check-in", "three-chapters")
    problems = validate(s)
    if problems:
        raise ValueError("; ".join(problems))
    return {k: s[k] for k in KEYS}


def v1_meaning(block_text):
    """The settings a first-build block corresponds to."""
    return "ai-writes-you-direct" if DIRECTOR_MARK in block_text else "you-write-ai-checks"


def classify(files):
    """Classify a project's setup from {filename: text} of AGENTS.md and CLAUDE.md.

    Returns (status, detail, settings_or_None, source_file). Status is one of:
    none, valid, malformed, duplicate, conflicting, v1-standard, v1-director.
    """
    found = {name: find_blocks(text) for name, text in files.items() if text is not None}
    with_blocks = [n for n in ("AGENTS.md", "CLAUDE.md") if found.get(n)]
    if not with_blocks:
        return "none", "no Story project block", None, None
    src = with_blocks[0]
    blocks = found[src]
    if any(end is None for _, end, _ in blocks):
        return "malformed", f"{src}: a block has no end marker", None, src
    if len(blocks) > 1:
        return "duplicate", f"{src}: {len(blocks)} Story project blocks", None, src
    start, end, version = blocks[0]
    text = files[src][start:end]
    if version == "v1":
        kind = "v1-director" if DIRECTOR_MARK in text else "v1-standard"
        preset = v1_meaning(text)
        return kind, f"{src}: first-build block, read as '{preset}'", resolve(preset), src
    if version != "v2":
        return "malformed", f"{src}: unknown block version '{version}'", None, src
    try:
        settings = parse_settings(text)
    except ValueError as e:
        return "malformed", f"{src}: {e}", None, src
    if len(with_blocks) > 1:
        return "conflicting", "AGENTS.md and CLAUDE.md both have a block; AGENTS.md wins", settings, src
    return "valid", f"{src}: {PRESET_LABELS[settings['preset']]}", settings, src


STATUS_RE = re.compile(r"<!--\s*status:\s*(draft|awaiting check-in|accepted|needs revision)\s*(?::\s*(.*?))?\s*-->", re.I)
FACT_RE = re.compile(r"^\s*[-*]\s*\[(pending major|pending minor|rejected)\]", re.I)
FINDING_RE = re.compile(r"^\s*[-*]\s*\[(open|resolved)\]", re.I)


def chapter_status(text):
    """Status from the first few lines of a draft. None means no marker, which means trusted."""
    for line in text.splitlines()[:5]:
        m = STATUS_RE.search(line)
        if m:
            return m.group(1).lower(), (m.group(2) or "").strip()
    return None
