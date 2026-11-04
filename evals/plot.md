# Evals: plot hub

Each entry is a realistic writer prompt, the skill expected to trigger, and what a good answer must show. Run each prompt with the skills installed and without, and compare. A pass means the behaviors appear with the skills and mostly do not appear without them.

Scoring per entry: list which "must show" items appear. Generic advice (such as "raise the stakes" or "add conflict") that names no framework does not count.

---

## plot-01 — The drag

**Prompt:** My fantasy novel is about a thief who must steal a crown to free her brother. The first hundred pages are great, but around chapter 12 to 20 the middle drags. The crew travels, argues, and gathers supplies. Readers stop caring. What's wrong?

**Should trigger:** `plot` (hub), `plot-promise-progress-payoff`, `plot-types-of-progress`

**Must show:**
- Frames the problem as promise versus progress: what is being promised in this stretch and what signals tell the reader the story is moving toward it
- Suggests a fix by adding or revising a promise so the diversion reads as progress, not only cutting scenes
- Asks or checks whether a promised thread (the brother, the crown) has been dropped for subplots
- Names the kind of progress this story measures and how to signpost it

**Must not rely on:** generic advice such as "raise the stakes" or "cut the boring parts" without a diagnosis

---

## plot-02 — The opening

**Prompt:** I'm rewriting chapter one of my cozy mystery. It opens with a long description of the village and then the detective wakes up. Beta readers say it's pleasant but forgettable. What should the first chapter be doing?

**Should trigger:** `plot-kinds-of-promises`

**Must show:**
- Lists the kinds of promise an opening makes (tone, plot, character) and checks which are missing
- Says what the opening should show about the character (want, need, why they can't have it)
- Notes the tone promise for a cozy mystery and how names, description, and prose carry it
- Does not demand that all promises be made

**Must not rely on:** "start with action" or "add a hook" without naming what is being promised

---

## plot-03 — What is it about

**Prompt:** My manuscript has a lot of good scenes but my critique partner says the chapters feel random. I can't even summarize what the book is about in a sentence. Help?

**Should trigger:** `plot-big-p-little-p`

**Must show:**
- Distinguishes the book-level Plot (a sentence or two) from the chapter-by-chapter plot
- Asks the writer to write the Big P Plot in one or two sentences and checks the chapters against it
- Suggests that each chapter's small plot advance or make a promise of the main one

**Must not rely on:** "outline the book" alone

---

## plot-04 — Bait and switch

**Prompt:** I've written a book that opens as a lighthearted road trip and turns into a thriller halfway. Early readers feel misled. How do I fix this without rewriting the whole middle?

**Should trigger:** `plot-promise-progress-payoff`, `plot-kinds-of-promises`

**Must show:**
- Names the tone promise made by the opening and the mismatch with what follows
- Recommends revising the promise (the opening and early chapters) as the cheaper fix, with the reason
- Notes that a story that switches tones can promise both at the start

**Must not rely on:** "rewrite the middle" or "pick one genre" without addressing the promise

---

## plot-05 — Two stories at once

**Prompt:** My sci-fi adventure follows a crew chasing an alien artifact to save Earth, but readers keep telling me the real heart is the friendship between the pilot and the engineer. The ending is a big artifact battle. It feels hollow. Why?

**Should trigger:** `plot-types-of-progress`, `plot-big-p-little-p`

**Must show:**
- Identifies the friendship as the story's soul, i.e. the progress thread that should drive the climax
- Notes the climax should resolve the thread the story actually measured (relationship progress), not only the headline plot
- Suggests paying the threads off together, with the relationship deciding the outcome
- Separates the headline plot from the little p plot

**Must not rely on:** "make the battle bigger" or generic stakes advice

---

## plot-06 — An opening scene that previews the book

**Prompt:** I want my heist novel to start with a short scene that gives readers the feel of the whole book. How should that work and when would it be a bad idea?

**Should trigger:** `plot-cold-open-microcosm`

**Must show:**
- Explains a short opening mini-story that shows the story's shape in small, which the book then repeats or breaks at length
- Gives the heist structure (a job that goes right, then one that goes wrong) as an application
- Says when it is a bad idea: it needs the main conflict to be previewable, and it is optional

**Must not rely on:** general "hook the reader" advice

---

## router-plot-01 — Hub routing (no framework named)

**Prompt:** Something's off with my plot but I can't tell what. Chapters 5 through 9 just don't land.

**Should trigger:** `plot` (hub) first, then `plot-promise-progress-payoff`

**Must show:**
- Starts from diagnosis questions (what is being promised, what signals progress) instead of jumping to a fix
- Asks at most two or three clarifying questions about the stretch in question

---

## struct-01 - Sagging middle with no question
**Prompt:** I'm writing a thriller about a night-shift nurse who discovers patients are being swapped. Chapters 1 to 5 set up her life, the hospital, and her sister. Then I have about twenty chapters of her investigating and I can't tell whether the book is actually going anywhere. Where should the big turns land?
**Should trigger:** `plot-three-act-structure`
**Must show:**
- Asks for or helps write the major dramatic question and checks whether it is posed by the end of Act I
- Identifies a point of no return that ends Act I, separate from the inciting incident
- Places a midpoint that reframes or personalizes the story, then an all is lost low point before a final realization
- Notes that the middle is really two halves, and that each attempt should make things worse
**Must not rely on:** generic advice such as "raise the stakes" or "add twists" with no beats named

## struct-02 - Hero's journey as checklist
**Prompt:** I outlined my fantasy novel using the hero's journey, twelve stages, and now every chapter feels like I'm ticking a box. The mentor death is forced and my heroine doesn't even need a mentor. Should I scrap the outline or push on?
**Should trigger:** `plot-story-circle`
**Must show:**
- Recommends dropping or reshaping steps that do not fit rather than forcing them, and warns against treating the model as a checklist
- Offers the simpler eight-step circle and checks the character's arc (rest, call, threshold, trials, transformation, return) instead of external beats
- Points out the model is so vague it fits nearly anything, so a missing step is a question, not an error
**Must not rely on:** "just write what feels right" or listing the twelve stages again

## struct-03 - Sequel and tragic arcs
**Prompt:** My trilogy's first book ends with my farm-boy hero finally leaving home and training with the order. Book two he fails badly, and book three he is meant to fall to the dark side and die. Is this structured sensibly, and how do I make each book feel complete?
**Should trigger:** `plot-story-circle`
**Must show:**
- Describes nested circles: book one as a full loop that is also only the first threshold of the larger arc
- Frames book two as a failure and retry and book three as a tragic bend where the hero refuses the elixir or return
- Distinguishes the external goal from the character arc the progress signposts should track
**Must not rely on:** generic trilogy advice about cliffhangers or raising stakes each book

## struct-04 - Writing in a pattern I love
**Prompt:** I love underdog team stories, and I want to put one inside my space opera as the story of a washed-out cadet squad. I don't want it to feel like a copy of the movies I love. How do I borrow the shape without cloning it?
**Should trigger:** `plot-structure-model`
**Must show:**
- Advises studying many examples of the narrow pattern and listing the plot points that make it work
- Says to keep the working points, drop the ones the writer dislikes, and adapt to a new medium or aesthetic with raised stakes
- Reassures that tropes cannot all be avoided and that the shape will stretch with the writer's own characters and worldbuilding
**Must not rely on:** "add a twist" or "make your characters unique" without a method

---

## cycle-01 - The too-easy heist
**Prompt:** In my fantasy novel a young cartographer has to retrieve a stolen map from a warlord's fortress. She plans it carefully, sneaks in on the first try, grabs the map, and escapes. My critique group says the sequence is competent but flat and the stakes never felt real. How do I fix it?
**Should trigger:** `plot-try-fail-cycle`
**Must show:**
- Says a goal like this should usually fail at least once, ideally two or three times, before it succeeds
- Has her first attempt be the smartest available approach, failing because of a flaw, a skill gap, or an opponent who anticipated the obvious move
- Ties each failure to a change such as new information, higher cost, or a larger problem
**Must not rely on:** generic advice such as "add obstacles" or "raise the stakes" with no failure structure

## cycle-02 - Stuck on what comes next
**Prompt:** I'm writing by the seat of my pants. My detective just found the victim's ledger, and I have no idea where to go. I want each scene to push into the next instead of just happening. Any method?
**Should trigger:** `plot-yes-but-no-and`
**Must show:**
- Poses the next problem as a question and answers it with "yes, but" or "no, and"
- Makes the complication the next problem and demonstrates two or three links in the chain
- Warns that the method is best over shorter stretches and can run out of gas in a very long book
**Must not rely on:** generic suggestions such as "brainstorm possible twists" or "ask what your character wants"

## cycle-03 - The sudden redemption
**Prompt:** My protagonist is a pilot who never trusts anyone and flies solo. In the final battle he finally trusts his wingmate and it lands flat. Readers say it came out of nowhere, and some found him annoying for most of the book. What do I do?
**Should trigger:** `plot-layering-conflict`
**Must show:**
- Calls for an early promise of what he must learn, and for a legitimate flaw with a serious early failure
- Suggests seeding inner-conflict beats at intervals through the middle, and having the narrative acknowledge the flaw
- Sets up the climax as a bigger version of the earlier problem, with a one-two punch where he overcomes it
- Addresses reader annoyance by making the flaw understandable and relatable
**Must not rely on:** generic advice to "show his growth more" or "give him a backstory"

## cycle-04 - How big should this be
**Prompt:** I have an idea about a kingdom collapsing and a whole generation of families caught in it, but I only want to write about 60,000 words. A friend says it will feel rushed. I also can't decide if my chapters should be long or short. How do I decide the size of the plot?
**Should trigger:** `plot-scale-of-plot`
**Must show:**
- Matches scope to word count, noting that 80,000 to 100,000 words suits tighter plots and that broad, escalating, or generational scope usually needs more length
- Offers options such as narrowing to a few lives, a novella-scale slice, or a longer book
- Links chapter length to how the book will be read, with short chapters pulling readers faster and break points for longer works
**Must not rely on:** generic advice to "focus the story" without word-count guidance

---

## payoff-01 - The twist that fell flat
**Prompt:** In my romance novel the heroine is engaged to a wealthy architect for the whole book, and in the last chapter I reveal she's actually in love with his quiet brother. Test readers say the reveal felt random and kind of cheap. How do I make the twist land?
**Should trigger:** `plot-twists-promise-and-wish`
**Must show:**
- Describes the method of promising one outcome, making the reader wish for a different one, then delivering the preferred one
- Asks where in the middle the brother becomes the option the reader would prefer
- Suggests signposting so the swap feels inevitable, and checks whether the story needs a twist at all
**Must not rely on:** generic advice to "add foreshadowing" or "make the reveal more surprising"

---

## payoff-02 - The predictable rescue
**Prompt:** My besieged army holds a fortress, and the queen's brother is supposed to arrive with reinforcements. Beta readers say they knew he'd show up and the arrival felt flat. How do I make it hit harder?
**Should trigger:** `plot-payoff-deniability-forgotten-promise`
**Must show:**
- Offers plausible deniability, stacking real obstacles so the reader doubts the arrival
- Offers the forgotten promise, burying the setup until the darkest moment, possibly with a reminder as it lands
- Warns that a rescuer with no earlier setup reads as a convenient arrival
**Must not rely on:** generic advice to "add tension" or "delay the arrival"

---

## payoff-03 - Too guessable
**Prompt:** My mystery has a traitor reveal at the end. Two of my five beta readers guessed it by chapter 3, and the other three never saw it coming and said it came out of nowhere. I'm confused. What do I fix?
**Should trigger:** `plot-foreshadowing-twists`
**Must show:**
- States a target such as most readers guessing only a page or paragraph before the reveal, and says some early guessers are unavoidable
- Distinguishes the two problems and how to fix each, including turning suspense instead of surprise as an option
- Offers concrete techniques for hiding clues, such as repetition, character attention, or a character remarking on an oddity
**Must not rely on:** generic advice to "balance foreshadowing" without a target or techniques

---

## payoff-04 - The best scene is in the middle
**Prompt:** My fantasy has two viewpoints. The big battle at about three-quarters through is the best thing I've written, and the actual ending feels weak next to it. Do I cut the battle, or what?
**Should trigger:** `plot-climax-placement-aftermath`, `plot-cheer-moment-sanderlanche`
**Must show:**
- Gives the options of moving the climax, raising the ending, or accepting it as a quirk, with raising the ending as the one to practice
- Suggests strengthening the weaker viewpoint or plotline to balance the two
- Asks whether the early climax is a plot payoff while the ending should be the emotional payoff
**Must not rely on:** generic advice to "build tension toward the ending" or "cut the weaker scenes"

---

## archetype-01 - Friend who betrays
**Prompt:** In my fantasy novel, Ren's closest friend Dax turns on her in the last third and sells her out to the empire. Beta readers said it felt random and they didn't buy it. How do I make it land without telegraphing it?
**Should trigger:** `plot-archetypes`
**Must show:**
- Treats the betrayal as a relationship arc built to go wrong, not an isolated twist
- Shows the two working well together early, then gradual divergence of motivations shown through actions
- Notes readers follow the viewpoint character's attention, so cracks can be planted while Ren still sees Dax as a friend
- Gives Dax a solid motivation so readers think "I should have seen that"
**Must not rely on:** generic advice such as "add foreshadowing" or "give the villain more motivation" without the arc structure

## archetype-02 - Generic heist
**Prompt:** I'm writing a heist story about a crew robbing a casino vault. It feels like every heist I've read. How can I make it stand out?
**Should trigger:** `plot-archetypes`
**Must show:**
- Distinguishes heist subtypes (plan thrown off and improvised versus plan executed smoothly with minor complications)
- Suggests layering other archetypes such as mentor and apprentice, mystery, or romance
- Suggests shifting archetype midway when things go wrong and scope grows, such as heist into revolution or whodunit into cat and mouse
- Says to foreshadow the shift
**Must not rely on:** "add a twist" or "make the characters more unique"

## archetype-03 - Outline for many threads
**Prompt:** My epic fantasy has three viewpoints, a slow romance, a magic-system puzzle, and a main war plot. I keep forgetting what I promised. How should I outline this?
**Should trigger:** `plot-outline-interwoven-cycles`
**Must show:**
- Identifies separate plot cycles (internal arcs, main plot, romance, information plot)
- Lists each cycle's beats starting from its ending, with signposts and backslides
- Merges lists into parts, marking each part's end with a big complication or achievement
- Warns about the added complexity of multiple viewpoints and suggests staggering payoffs
**Must not rely on:** a generic three-act or chapter-by-chapter outline template

## archetype-04 - Discovery writer outlining
**Prompt:** I'm a pantser and outlines kill my drive. But my 60,000-word draft has a romance and a mystery that both seem to have gone nowhere. Is there a way to use outlining without ruining my process?
**Should trigger:** `plot-outline-interwoven-cycles`
**Must show:**
- Suggests listing the cycles actually written after drafting, and checking each for missing progress or payoff
- Says setup and foreshadowing can be added afterward, which is easier than removing it
- Offers a light, time-limited option that fixes only the cycles and their endings
- Says a working method need not be replaced
**Must not rely on:** "just outline first" or "keep writing and fix it in revision" with no method
