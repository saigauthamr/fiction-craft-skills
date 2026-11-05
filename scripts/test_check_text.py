import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECK = Path(__file__).resolve().parent.parent / "skills" / "story-check" / "check_text.py"

CLEAN_CURLY = """<!-- status: awaiting check-in -->
# Chapter 4: The Marker

*Harbor of Vell, the dry season*

Ines set the marker by the book. “You're early,” the inspector said, and she didn't answer him.

“It's the tide,” she said at last. “It turns an hour sooner this month, and nobody wrote it down.

“And if anyone had asked me, I'd have said so. Nobody asks the surveyor.”

---

The ferry horn sounded twice. Tomas didn't look up from the rope. “You coming or not?”

* * *

She didn't say, “Here's the revised plan,” because there wasn't one.
"""

CLEAN_STRAIGHT = '''# Chapter 5

"It's the tide," she said. "It turns an hour sooner.

"And nobody wrote it down."

Tomas didn't look up. "You coming or not?"
'''


def run(text, name="chapter.md", strict=False, extra=()):
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / name
        p.write_text(text, encoding="utf-8")
        args = [sys.executable, "-B", "-I", str(CHECK), str(p)] + (["--strict"] if strict else []) + list(extra)
        r = subprocess.run(args, capture_output=True, text=True)
        rules = [line.split(": ")[2] for line in r.stdout.splitlines() if ": warn: " in line]
        return r.returncode, rules, r.stdout


class CleanTextTests(unittest.TestCase):
    def test_a_clean_curly_chapter_has_no_warnings(self):
        code, rules, out = run(CLEAN_CURLY)
        self.assertEqual((code, rules), (0, []), out)

    def test_a_clean_straight_chapter_has_no_warnings(self):
        self.assertEqual(run(CLEAN_STRAIGHT)[1], [])

    def test_continued_speech_across_paragraphs_is_balanced(self):
        self.assertNotIn("quotes.unbalanced", run(CLEAN_CURLY)[1])

    def test_html_comments_and_code_fences_are_ignored(self):
        text = "# Title\n\n<!-- TODO as an AI, here's the chapter\n**bold** -->\n\nProse.\n\n```\nTODO **x**\n```\n"
        self.assertEqual(run(text)[1], [])

    def test_a_first_line_chapter_title_is_not_a_markdown_leak(self):
        self.assertNotIn("markdown.heading", run("# Chapter 1: Title\n\nProse here.\n")[1])


class ProblemTests(unittest.TestCase):
    def rules(self, body):
        return run("# Chapter\n\n" + body + "\n")[1]

    def test_wrapper_and_closing_wrapper(self):
        self.assertIn("leak.wrapper", self.rules("Here's the revised chapter you asked for!\n\nProse."))
        self.assertIn("leak.wrapper", self.rules("Prose.\n\nI hope this captures what you were looking for!"))
        self.assertIn("leak.wrapper", self.rules("Prose.\n\nWould you like me to continue?"))

    def test_the_same_words_inside_dialogue_are_not_a_leak(self):
        self.assertNotIn("leak.wrapper", self.rules('"Here\'s the revised plan," she said, and "as an AI" meant nothing to him.'))

    def test_placeholders(self):
        self.assertIn("leak.placeholder", self.rules("The tide came in. TODO fix this scene."))
        self.assertIn("leak.placeholder", self.rules("She met [insert name] at the pier."))

    def test_markdown_leaks(self):
        r = self.rules("The **marker** held.\n\n- she nodded\n\n> a quote\n\n`code`\n\n## A heading")
        for rule in ("markdown.bold", "markdown.list", "markdown.quote", "markdown.code", "markdown.heading"):
            self.assertIn(rule, r)

    def test_scene_break_markers_are_not_markdown_leaks(self):
        self.assertEqual(self.rules("One.\n\n---\n\nTwo.\n\n* * *\n\nThree."), [])

    def test_unbalanced_quotes(self):
        self.assertIn("quotes.unbalanced", self.rules('She said "it is the tide.\n\nThen she left.'))
        self.assertIn("quotes.stray-close", self.rules("It is the tide,” she said."))

    def test_mixed_quote_styles(self):
        self.assertIn("quotes.mixed", self.rules('"One," he said. “Two,” she said.'))

    def test_duplicate_and_near_duplicate_paragraphs(self):
        para = "The ferry horn sounded twice and carried across the flat grey water toward the far harbor wall."
        self.assertIn("dup.paragraph", self.rules(para + "\n\nOther.\n\n" + para))
        near = para.replace("flat grey", "flat gray")
        self.assertIn("dup.near", self.rules(para + "\n\nOther.\n\n" + near))

    def test_encoding_damage(self):
        self.assertIn("encoding.mojibake", self.rules("The tide was â€œearly."))
        self.assertIn("encoding.replacement", self.rules("The tide was � early."))
        self.assertIn("encoding.invisible", self.rules("The tide​ was early."))

    def test_whitespace(self):
        r = self.rules("Two  spaces here.\n\nA\ttab.\n\n\n\n\nAfter a run.")
        for rule in ("space.double", "space.tab", "space.blank-run"):
            self.assertIn(rule, r)


BODY = "She waited at the marker until the tide turned and the water began to leave the flats, and the ferry did not come, and the light went out of the sky one band at a time until only the white posts showed."


class EndingTests(unittest.TestCase):
    def test_a_chapter_cut_off_mid_sentence_is_flagged(self):
        code, rules, _ = run("# C\n\n" + BODY + "\n\nThen she took the book from her coat and began to")
        self.assertIn("truncated.ending", rules)
        self.assertEqual(code, 0)

    def test_a_last_line_ending_on_a_comma_or_hyphen_is_flagged(self):
        self.assertIn("truncated.ending", run("# C\n\n" + BODY + "\n\nThen she turned,")[1])
        self.assertIn("truncated.ending", run("# C\n\n" + BODY + "\n\nThen she turned to the half-")[1])

    def test_ordinary_endings_are_not_flagged(self):
        for end in ("Then she went home.", "Then she went home!", "Was that all?", "She went home\u2026", "She said, \u201cGo home.\u201d",
                    'She said, "Go home."', "She went home (alone).", "\u201cDa\u2014\u201d", "She said it again\u2014", "She went home.)"):
            self.assertNotIn("truncated.ending", run("# C\n\n" + BODY + "\n\n" + end + "\n")[1], end)

    def test_a_deliberate_dash_ending_outside_quotes_is_not_flagged(self):
        self.assertNotIn("truncated.ending", run("# C\n\n" + BODY + "\n\nShe opened her mouth to answer\u2014\n")[1])

    def test_a_scene_break_a_short_caps_line_and_a_tiny_file_are_not_judged(self):
        self.assertNotIn("truncated.ending", run("# C\n\n" + BODY + "\n\n* * *\n")[1])
        self.assertNotIn("truncated.ending", run("# C\n\n" + BODY + "\n\nTHE END\n")[1])
        self.assertNotIn("truncated.ending", run("# C\n\nShe went and then she")[1])

    def test_a_trailing_comment_or_status_line_does_not_hide_the_ending(self):
        self.assertIn("truncated.ending", run("# C\n\n" + BODY + "\n\nThen she took the book and\n\n<!-- end -->\n")[1])


class LoopTests(unittest.TestCase):
    SENT = "The lamp dipped twice and the water answered with a low note that nobody could place."

    def test_a_long_sentence_repeated_three_times_is_flagged_once(self):
        _, rules, out = run("# C\n\n" + "\n\n".join([self.SENT, "Ines listened.", self.SENT, "Tomas said nothing.", self.SENT]) + "\n")
        self.assertEqual(rules.count("repeat.loop"), 1)
        self.assertIn("occurs 3 times", out)

    def test_twice_is_not_a_loop(self):
        _, rules, _ = run("# C\n\n" + "\n\n".join([self.SENT, "Ines listened.", self.SENT]) + "\n")
        self.assertNotIn("repeat.loop", rules)

    def test_a_short_refrain_is_not_a_loop(self):
        text = "# C\n\nThree times she called her father's name. Three times the wind answered. Three times the lamp dipped. Three times nobody came.\n"
        self.assertNotIn("repeat.loop", run(text)[1])

    def test_a_repeated_phrase_inside_different_sentences_is_found(self):
        phrase = "the old keeper had never once told anyone where he went"
        text = "# C\n\n" + f"Everyone knew {phrase} at night. Mara asked why {phrase} in all those years. She wrote that {phrase} in her book.\n"
        self.assertIn("repeat.loop", run(text)[1])

    def test_a_loop_is_reported_where_it_starts(self):
        _, _, out = run("# C\n\nFine opening line here.\n\n" + "\n\n".join([self.SENT] * 3) + "\n")
        self.assertIn(":5: warn: repeat.loop", out)


class LengthTests(unittest.TestCase):
    def chapter(self, n):
        return "# Chapter 1\n\n" + " ".join(["word"] * (n - 1)) + " end.\n"

    def test_below_the_minimum_warns(self):
        self.assertIn("length.short", run(self.chapter(500), extra=["--words", "1800-2500"])[1])

    def test_above_the_maximum_warns(self):
        self.assertIn("length.long", run(self.chapter(3000), extra=["--words", "1800-2500"])[1])

    def test_inside_the_range_is_quiet(self):
        r = run(self.chapter(2000), extra=["--words", "1800-2500"])[1]
        self.assertFalse([x for x in r if x.startswith("length.")])

    def test_open_ended_ranges(self):
        self.assertIn("length.short", run(self.chapter(500), extra=["--words", "1800-"])[1])
        self.assertNotIn("length.long", run(self.chapter(5000), extra=["--words", "1800-"])[1])
        self.assertIn("length.long", run(self.chapter(3000), extra=["--words=-2500"])[1])

    def test_no_range_means_no_length_warning(self):
        self.assertFalse([x for x in run(self.chapter(5))[1] if x.startswith("length.")])

    def test_the_title_line_is_not_counted(self):
        code, rules, out = run("# One Two Three Four Five Six\n\n" + " ".join(["word"] * 9) + " end.\n", extra=["--words", "10-"])
        self.assertNotIn("length.short", rules, out)

    def test_a_bad_range_is_an_error(self):
        for bad in ("abc", "2500-1800", "-", ""):
            r = subprocess.run([sys.executable, "-B", "-I", str(CHECK), "/tmp", "--words", bad], capture_output=True, text=True)
            self.assertEqual(r.returncode, 2, bad)
            self.assertIn("error:", r.stdout)

    def test_a_missing_range_value_is_an_error(self):
        r = subprocess.run([sys.executable, "-B", "-I", str(CHECK), "/tmp", "--words"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)

    def test_the_length_warning_is_advisory_unless_strict(self):
        self.assertEqual(run(self.chapter(500), extra=["--words", "1800-2500"])[0], 0)
        self.assertEqual(run(self.chapter(500), strict=True, extra=["--words", "1800-2500"])[0], 1)


class ExitCodeAndTargetTests(unittest.TestCase):
    def test_warnings_exit_zero_unless_strict(self):
        text = "# C\n\nTODO\n"
        self.assertEqual(run(text)[0], 0)
        self.assertEqual(run(text, strict=True)[0], 1)

    def test_missing_target_exits_two(self):
        r = subprocess.run([sys.executable, "-B", "-I", str(CHECK), "/no/such/file.md"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)

    def test_folders_skip_previous_and_delivered_copies(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "_previous").mkdir()
            (d / "_delivered").mkdir()
            (d / "_previous" / "old.md").write_text("# C\n\nTODO\n")
            (d / "_delivered" / "old.md").write_text("# C\n\nTODO\n")
            (d / "001.md").write_text("# C\n\nFine prose.\n")
            r = subprocess.run([sys.executable, "-B", "-I", str(CHECK), str(d)], capture_output=True, text=True)
            self.assertIn("1 file(s) checked, 0 warning(s)", r.stdout)

    def test_the_checker_never_changes_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "c.md"
            p.write_text("# C\n\nTODO  **x**\n")
            before = p.read_bytes()
            subprocess.run([sys.executable, "-B", "-I", str(CHECK), str(p)], capture_output=True)
            self.assertEqual(p.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
