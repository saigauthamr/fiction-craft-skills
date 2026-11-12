# Fiction Craft Skills

Agent skills for writing fiction. They give an AI writing assistant a set of craft frameworks (plot, character, magic and worldbuilding, scene craft, and process), a guided process from first idea to revised chapter, and a safe way to bring an existing project in. You decide how much of the work the AI does: all of it, none of it, or anything between.

They are plain `SKILL.md` folders, so any agent that reads that format can use them.

Want to read the skills? `READING-ORDER.md` lists every skill in a sensible order with a link to each.

## What is inside

| Part | Skills |
| --- | --- |
| Setting up and moving through a story | `story-onboard`, `story-next`, `story-adopt`, `story-develop`, `story-plan`, `story-draft`, `story-check`, `story-revise`, `story-edits`, `story-steer`, `story-continue`, `story-learn` |
| Design tools | `story-worldbuild` (a rules lab with an exploit hunt), `story-cast` (character build sheets), `story-voice` (pick a voice from demo passages) |
| Craft hubs and frameworks | `plot` (21 frameworks), `character` (14), `magic-worldbuilding` (15), `scene-craft` (6), `foundations` (6) |
| Prose | `prose-craft` (what makes narration alive: the character's mind on the page, the detail that belongs to the scene, exact sentences, proportion, range) and `prose-ai-tells` (spots and avoids machine-sounding fiction habits, including stilted dialogue) |

A story moves through develop (sharpen the idea), plan (a spec and chapter beats), draft, then check and revise in a loop until you say a chapter is done. When you edit a chapter the AI drafted, `story-edits` learns from your changes.

## Install

Pick **one** route per tool. Installing the same skills two ways lists every skill twice. All of them install the same 83 skills, which are plain `SKILL.md` folders in the open Agent Skills format.

| Tool | Route | Status |
| --- | --- | --- |
| Claude Code | Plugin (below) | Tested at 0.2.0 from a local copy: `plugin validate` passes and `marketplace add` and `install` work. On the first release, 6 plain requests loaded the right skills |
| Codex | Plugin marketplace (below) | Tested at 0.2.0 from a git copy of this repo: `marketplace add` and `plugin add` install all 82 skills. On the first release, a plain request also loaded the right skill |
| Cursor, OpenCode, and others | `npx skills add` (below) | At 0.2.0, `--list` finds all 82 skills. On the first release the Claude Code target was tested end to end (it copies the skills with their scripts). Other targets untested |
| Any tool | Clone and run `scripts/install.sh` (below) | Script and folders tested. On the first release, 22 plain requests loaded the right skills in Claude Code; other tools untested |
| GitHub Copilot | Plugin marketplace (below) | Not tested |
| Gemini CLI | `gemini skills install` (below) | Not tested; Gemini CLI was not available to test with |

### Claude Code: as a plugin

```
/plugin marketplace add saigauthamr/fiction-craft-skills
/plugin install fiction-craft-skills@fiction-craft-skills --scope project
```

`--scope project` installs it for the project you are in; leave it off to install for every project. Plugin skills are namespaced (`fiction-craft-skills:story-next`), and the routing table that setup writes still finds them.

### Codex: plugin marketplace

```
codex plugin marketplace add saigauthamr/fiction-craft-skills
codex plugin add fiction-craft-skills@fiction-craft-skills
```

Codex installs plugins for your user account and has no per-project install option, so the story skills are available in every project. To keep them out of other projects, use the clone-and-install route below instead. You can also install from the Codex app's plugin list.

### GitHub Copilot: plugin marketplace

```
copilot plugin marketplace add saigauthamr/fiction-craft-skills
copilot plugin install fiction-craft-skills@fiction-craft-skills
```

### Gemini CLI

```
gemini skills install https://github.com/saigauthamr/fiction-craft-skills.git --path skills --scope workspace
```

Re-run it to update.

### Cursor, OpenCode, and other tools

```
npx skills@latest add saigauthamr/fiction-craft-skills -a <agent>
```

### Any tool: clone and run the installer

From your story project's folder:

```
git clone https://github.com/saigauthamr/fiction-craft-skills.git ~/fiction-craft-skills
~/fiction-craft-skills/scripts/install.sh            # Claude Code: links into ./.claude/skills
~/fiction-craft-skills/scripts/install.sh --agents   # Codex, Gemini CLI, OpenCode, Cursor, Copilot: links into ./.agents/skills
```

Options: `--global` installs for every project (into `~/.claude/skills`, or `~/.agents/skills` with `--agents`); `--copy` copies the skills instead of linking them, for a tool that does not follow links; a folder path installs somewhere else. The installer never overwrites a folder or file that is not its own, refreshes its earlier links and copies, and removes dead links into this library. Install all of the skills together, since some read their sibling skills' folders.

Install per project where you can. A global install puts 83 story skills into every session, where they compete with your other skills.

### Where each tool looks

These are the folders and files each tool's documentation named when this was written (November 2026). Tools change them, so check yours if the skills do not appear.

| Tool | Skills folder (project) | Notes |
| --- | --- | --- |
| Claude Code | `.claude/skills` | Reads it from the folder you start in up to the repository root. Follows links. Ignores frontmatter fields it does not know. |
| Codex (CLI, IDE, app) | `.agents/skills` | Scans from the current folder up to the repository root, and `~/.agents/skills` for you. Follows links. |
| Gemini CLI | `.agents/skills` or `.gemini/skills` | `.agents/skills` wins within a level. Asks you to confirm when it activates a skill. Its docs say Antigravity CLI replaced it for some account types in June 2026. |
| OpenCode | `.agents/skills`, `.claude/skills`, or `.opencode/skills` | Reads all three. |
| Cursor | `.agents/skills`, `.claude/skills`, or `.cursor/skills` | Reads all three. |
| GitHub Copilot | `.agents/skills`, `.claude/skills`, or `.github/skills` | In VS Code you may need the `chat.useAgentSkills` setting on. |

### Project instructions

Setup writes your settings and the routing table into `AGENTS.md`, the file most of these tools read for project instructions. Two need a bridge:

- **Claude Code** reads `AGENTS.md` only when there is no `CLAUDE.md`. When setup creates `AGENTS.md` it also creates a `CLAUDE.md` containing `@AGENTS.md`, Claude Code's documented import. If you already have a `CLAUDE.md`, add that line to it.
- **Gemini CLI** reads `GEMINI.md`. Either add `"context": {"fileName": ["AGENTS.md", "GEMINI.md"]}` to its `settings.json`, or create a `GEMINI.md` containing `@AGENTS.md`.

If your tool reads a different file, point it at `AGENTS.md`.

### Too many skills for the tool's list

Tools put every skill's name and description into the model's context, within a budget, and drop or shorten descriptions when there are too many. The 83 descriptions here total about 20,000 characters. Codex's docs give the list about 2% of the context window (8,000 characters when the window size is unknown) and say it shortens descriptions first; `skills.max_context_tokens` raises that, up to 10,000 tokens. Claude Code's docs describe dropping the descriptions of rarely used skills first when it runs short, with a setting to raise the budget (`skillListingBudgetFraction`). If a skill does not trigger from a plain request, raise the budget. The routing table that setup writes into your instructions file is a second path: it names the right skill for each kind of request, and it is what made loading reliable in testing.

**Loading was tested in Claude Code (22 plain requests from project-local links, 6 from the plugin) and Codex (1 plain request).** The format follows the open standard and the paths above come from each tool's documentation. Other tools are untested; if a skill does not appear in yours, please open an issue.

## Start here

Ask your assistant to set up the story ("set up my story", or "I'm not a writer, I want you to write it"). `story-onboard` looks at the folder, asks a few questions with a recommended answer for each, shows exactly what it will write, and writes only after you agree. If the folder already holds chapters, notes, spreadsheets, or a knowledge base, it brings them in first with `story-adopt`, which shows a plan, never changes your files, and asks you to confirm every fact it extracts.

Setup adds a short "Story project" section to your project's instructions file: your settings, where things go, and a table of which skill handles which request.

## Who writes what

Onboarding asks who owns each stage: planning, drafting, and revising. Pick a preset or adjust any stage:

| Preset | Plan | Draft | Revise |
| --- | --- | --- | --- |
| AI writes, you direct | AI | AI | AI |
| AI drafts, you revise | AI | AI | you |
| You outline, AI drafts | you | AI | you |
| AI outlines, you write | AI | you | you |
| You write, AI checks | you | you | you |
| Design only | AI | (no prose) | (no prose) |

Every skill reads these settings. When a stage is yours, the assistant coaches and checks instead of writing; when it is the AI's, it does the work and shows it to you. Checking is always available and never edits your prose. Only you make story facts settled. You also choose how much craft language you want (none, one-line explanations, or full terms) and, when the AI drafts, how often it checks in with you. Run onboarding again any time to change any of it; your story files are never touched by a change of settings.

When the AI writes everything, it drafts chapter by chapter, checks and revises its own work, and stops at the check-ins you chose with a short card per chapter: what happened, what changed, and any new facts that need your yes or no. Plain-language notes such as "darker" or "slower" become a short list of changes, with their cost, for you to approve.

What to expect: this produces working drafts that follow your design and stay consistent with it. It is not a substitute for a human editor if you plan to publish professionally, and if you do publish, disclosing that AI wrote the text is your decision to make and often a platform requirement.

## How the prose is written

Clean prose is not the goal; prose that reads as written by someone is. When the AI drafts, it:

- **Decides how each scene is lived before writing it:** what the viewpoint character wants and dreads, what they have wrong, what only they would notice, and where the scene should spend its words.
- **Writes from inside the character.** The narration carries their judgments, thoughts, and mistakes, instead of filming them from outside. Feeling comes through what they notice and do, not through labels or a tight chest.
- **Matches a sample passage you approved.** `story-voice` ends with a voice sheet and a passage of about three hundred words in the chosen voice. Drafts follow its sound and never reuse its sentences.
- **Reads the chapter back before handing it over:** rewrites the passage a reader would skim, tests the lines that sound best for whether they state anything, and runs a small script that counts the habits a drafter cannot hear in its own text (comparisons, "did not" narration, body reports, hedges), with line numbers.

`story-check` then looks for flat prose as well as faults, and `story-revise` rewrites a flat passage whole instead of swapping words in it. The reasoning and worked examples are in `prose-craft`.

## How the craft knowledge is used

Each framework skill lists its checks with stable IDs. A build step copies the relevant ones into each stage skill, making the guidance available whenever that skill loads. Plans and check reports record which checks were applied and what each found. A framework the story breaks on purpose is recorded as deliberate, not treated as a defect. The compiled guidance does not guarantee that the model applies it correctly; behavioral evaluations check that separately.

## Long stories and your own edits

- **Learning from your edits.** The AI keeps an exact copy of each chapter it hands over. When you edit the chapter, `story-edits` compares the two, sorts your changes by what they did, asks only about changes it cannot explain, and saves the lessons you confirm to your voice file as one line each. A lesson needs several changes pointing the same way, or your say-so. A lesson you decline is recorded so it is not proposed again. The handed-over copy is deleted afterward, and nothing records who approved what.
- **Chapter cards.** For long stories, short derived summaries in `work/cards/` let the assistant read the chapter in hand and its neighbors in full and the rest as cards, with the prose always winning over a card. The inspector reports missing and stale cards by content hash. This is new and lightly tested: card upkeep works in tests and runs, but a saving on a long serial has not been measured.
- **Promise ledger (optional).** `story-plan` can keep one line per promise in `work/spec/promise-ledger.md`, in the shape `- P03 | planted ch2 | open | the promise in a few words`, with statuses open, advanced, paid, and dropped. The assistant updates it as chapters move or pay off promises, and the inspector counts them and names the oldest one still unpaid. If your project already tracks promises its own way, that is followed instead and this format is ignored.
- **Trust is the default.** Anything unmarked is trusted. Only untrusted material carries a marker (a chapter the AI drafted that you have not approved, a pending fact, an open finding), and approving something removes its marker.

## Principles the skills follow

- Your originals are never modified, moved, or deleted.
- Settings, specs, and beats are shown for approval before saving. The AI can save working drafts when it owns drafting; only your approval accepts a chapter or settles a story fact.
- Nothing is settled until you confirm it. Suggestions are marked as suggestions.
- Your project's own conventions (voice files, chapter naming, where open questions live) come before the library's defaults.
- Skills are self-contained and make no reference to files that are not installed.

## Testing and limits

- `scripts/lint.py` checks the skills' structure, cross-references, routing, generated check lists, and test fixtures. `scripts/test_*.py` test the settings block, the scaffold, the inspector and its next-step order, the importer, the check compiler, the chapter diff, the chapter cards, the text checker, and the habit counter. Run each with `python3 -I scripts/test_story_block.py`, and so on.
- `evals/` holds realistic prompts and sample pairs for checking skill behavior. These are smoke-test scenarios, not benchmarks or a guarantee of writing quality.
- The importer reads Word and Excel files with the standard library only. Files with unusual structure (tracked changes, comments, merged cells, formulas) may import imperfectly, and it tells you what it left in place.

## Examples and contributing

`examples/` has short before-and-after cases, each a single illustrative sample and not a benchmark. `CONTRIBUTING.md` says how to run the checks and what a skill must be. If a skill did not load, or produced something unhelpful, the issue templates ask for what is needed to reproduce it.

## Where the ideas come from

The craft frameworks restate, in original words, ideas taught in Brandon Sanderson's 2025 lecture series on writing science fiction and fantasy. No lecture text is included, and this project is not affiliated with or endorsed by him. Quotation is limited to short defining phrases. `prose-ai-tells` adapts [Humanizer](https://github.com/blader/humanizer) (MIT). Several ideas about dialogue, revision, chapter cards, and planning were adapted as ideas from [novel-writing](https://github.com/wgwtest/novel-writing) (MIT); wording, examples, and code are new. Ideas about varied options, draft checks, and promise tracking came from [Creative-writing-skill](https://github.com/xbraindance/Creative-writing-skill), [oh-story-claudecode](https://github.com/zenstory-ai/oh-story-claudecode), and [story-skills](https://github.com/danjdewhurst/story-skills) (all MIT), again as ideas only. See `NOTICE`.

## License

Apache License 2.0. See `LICENSE` and `NOTICE`.
