# Results: story-develop

One run per scenario, Sonnet given the skill file, scripted writer, checked on disk.

| Scenario | Expected | Result |
| --- | --- | --- |
| Writer owns planning, full craft language, one-line premise, "grill me" | Numbered questions with a recommended answer each; framework ideas named in plain terms; nothing recorded before it is settled | First run: right shape, but showed internal check IDs (`magic.hardsoft.01`) to the writer. Fixed in the shared generated preamble ("never show IDs or skill names to the writer"), recompiled. Re-run: pass; plain names only, settled a loose term ("the light"), nothing recorded |
| AI owns planning, no craft language, "help me design, I like heists and magic" | Choices with defaults, at most four per round, plain words; "go" defaults recorded as the AI's, awaiting a yes | Pass. Three premises plus three default choices; after "3, and go for the rest", the premise is recorded as the writer's choice and the three defaults under "Defaults I picked, awaiting the writer's yes", with open questions listed and the new term in `kb/vocab.md` |
