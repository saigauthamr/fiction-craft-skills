# Evals: prose-ai-tells

Two samples, both invented for this library. Run the detect pass (review mode) on each, with the skill and without, and compare.

## ai-tells-01 — Planted tells

**Passage:**

> Here's the scene you asked for!
>
> It wasn't the cold that woke Mara, but the silence. She sat up in the dark. She listened for the sea. She heard nothing. The cottage was quiet, cold, and empty. Her brother's bed was made, his boots gone from the hook.
>
> It seemed almost as though the house itself was somehow holding its breath. Mara pulled on her coat, her trembling hands speaking volumes about her fear. Hope, she knew, was a dangerous thing.
>
> Little did she know, the choice she made at that door would change her life forever.
>
> She stepped out into the grey morning. It was the end of one life and the beginning of another.
>
> I hope this captures what you were looking for! Would you like me to continue?

**Planted tells (nine):**
1. Chatbot wrapper (opening line and closing lines)
2. Not X but Y ("It wasn't the cold ... but the silence")
3. Repeated sentence openings ("She sat... She listened... She heard")
4. Forced triad ("quiet, cold, and empty")
5. Stacked hedges ("seemed almost as though... somehow")
6. Reaction rider ("trembling hands speaking volumes about her fear")
7. Aphorism in the narration ("Hope... a dangerous thing")
8. Narrated significance ("Little did she know...")
9. Interpretive closer ("the end of one life and the beginning of another")

**Must show:** finds at least seven of the nine, names the pattern, quotes the text, and gives a fix for each; does not invent tells that are not there; does not rewrite the passage in review mode.

## ai-tells-02 — Clean passage

**Passage:**

> The kettle had gone cold an hour ago. Tomas didn't move to reheat it.
>
> "You came back," Ines said.
>
> "I said I would." He turned the mug in his hands. "I said it twice, actually, once to you and once to the harbor, and only one of us was listening."
>
> She laughed, short and surprised. Outside, the ferry horn sounded twice and then a third time, the old signal for fog.
>
> "Tomas, I—"
>
> "Don't." He set the mug down. "Not before you've eaten."
>
> The bread was hard at the edges. She ate it anyway.
>
> The door was already open.

**Deliberate devices that must not be flagged:** a one-line closing paragraph that adds a fact; a dash for an interrupted line of dialogue; a parallel "once to you and once to the harbor"; a count ("twice and then a third time") that is a real count.

**Must show:** reports no tells, or at most one clearly marked weak note; does not call for rewrites; does not flag the four devices above.

---

## ai-tells-03 — Planted fiction habits

**Passage:**

> Dev's hands shook as he opened the letter. He was terrified.
>
> A flicker of hope crossed his face, mixed with a hint of fear. He felt a shiver run down his spine. The air was thick with tension, and somewhere, a clock ticked.
>
> "I feel betrayed," his sister said, "because you promised you'd stay and you didn't. And I'm sad that you left me alone."
>
> He let out a breath he didn't know he was holding.

**Planted tells:** named emotion after a shown one (pattern 13); "a flicker of... mixed with a hint of" (14); dialogue that states the subtext (15); stock body reactions, the shiver and the breath he didn't know he was holding (16); stock atmosphere, thick with tension and the clock (17).

**Must show:** finds patterns 13, 14, and 15 as strong; marks 16 and 17 as weak and mentions they need company (here they have it); gives a fix for each; does not rewrite the passage.

---

## ai-tells-04 — Fresh clean passage

(Written after the skill was tuned on ai-tells-02, so it checks for overfitting.)

**Passage:**

> The lamp room smelled of paraffin and cold brass. Wren trimmed the wick twice and checked it a third time, because her father would.
>
> "Gulls are low today," she said.
>
> "They're always low." He did not look up from the logbook. "That's what makes them gulls."
>
> She waited. Out past the rocks the water was the color of a slate roof, and then, between one breath and the next, it wasn't.
>
> "Da—"
>
> "I see it."
>
> He closed the book. He closed the shutters. He closed the door behind them, and the stairs began to ring under his boots.
>
> The lamp was still lit.

**Deliberate devices that must not be flagged:** a real count ("twice... a third time"); a dash for an interrupted line; a deliberate three-beat repetition ("He closed... He closed... He closed") that moves the action; a one-line closing paragraph that adds a fact.

**Must show:** reports no strong tells, at most one clearly marked weak note, no rewrite called for.
