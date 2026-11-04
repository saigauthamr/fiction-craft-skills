# Results: story-onboard

One run per scenario, Sonnet agents given the skill file, scripted writer replies, every result checked on disk against checksums taken before the run.

| Scenario | Expected | Result |
| --- | --- | --- |
| A. Empty folder, "I'm not a writer, I want you to write it" | Look first; recommend "AI writes, you direct"; one section per message; dry run shown; nothing written before "yes"; valid block after | Pass. Four turns (preset, craft language, check-ins, confirmation), each with a recommended default. Folder empty until "yes"; afterward `setup: valid`, `ai-writes-you-direct`, `craft-language: none`, `check-in: three-chapters` |
| B. First-build director block, "update my project's setup" | Read as "AI writes, you direct"; dry run; write on yes; own text, `kb/`, `work/` untouched | Pass. Writer's own line kept, v1 marker gone, both story files byte-identical |
| C. Folder of `.docx` chapters, notes, and a spreadsheet | Hand off to `story-adopt`; write nothing | Pass. Folder unchanged; noted the writer's preferred preset for afterward |
| D. Established knowledge base (12 pages) with no setup | Hand off to `story-adopt`; write nothing | Pass. Folder unchanged |

Not run: changing settings on a valid v2 project through the conversation (covered by the scaffold script tests), duplicate and conflicting repair through the conversation, and the standard-v1 case where the drafts look AI-drafted.
