#!/usr/bin/env python3
"""Tests for the prose habit counter bundled with story-check. Standard library only."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HABITS = Path(__file__).resolve().parent.parent / "skills" / "story-check" / "habits.py"

CHAPTER = """<!-- status: draft -->
# Chapter 2: The quay

The water did not rush. It was not loud. She didn't move, and the tide slid past like a rope being paid out.

"I would not do that," Tomas said. "It looks like a bad idea, as if you wanted to be caught."

Her chest was tight. It seemed almost quiet.

She waited.

---

She counted the posts. She counted them again. She counted the gaps. Then the ferry came in.

"You'd like a ride back?"

He went out laughing.
"""


def run(text, name="chapter.md"):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        path.write_text(text, encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", "-I", str(HABITS), str(path)], capture_output=True, text=True)
        return result.returncode, result.stdout


def line_for(out, label):
    return next(l for l in out.splitlines() if l.strip().startswith(label))


class HabitsTest(unittest.TestCase):
    def setUp(self):
        self.code, self.out = run(CHAPTER)

    def test_exit_status_is_zero_whatever_it_finds(self):
        self.assertEqual(self.code, 0)

    def test_negations_are_counted_in_narration_only(self):
        # did not, was not, didn't; "would not" inside Tomas's speech is not narration
        self.assertIn("negated narration: 3 ", line_for(self.out, "negated narration"))

    def test_comparisons_are_counted_in_narration_only(self):
        # "like a rope"; the two comparisons in speech and "You'd like a ride" are not counted
        self.assertIn("comparisons: 1 ", line_for(self.out, "comparisons"))

    def test_body_reports_and_hedges(self):
        self.assertIn("body reports: 1 ", line_for(self.out, "body reports"))
        self.assertIn("hedges: 2 ", line_for(self.out, "hedges"))

    def test_line_numbers_point_at_the_source_file(self):
        self.assertIn("lines 4, 4, 4", line_for(self.out, "negated narration"))
        self.assertIn("lines 8", line_for(self.out, "body reports"))

    def test_one_line_paragraphs_skip_speech_and_scene_breaks(self):
        # "She waited." and "He went out laughing."; the scene break and the line of speech are not counted
        self.assertIn("one-line paragraphs of narration: 2 of", line_for(self.out, "one-line paragraphs"))

    def test_run_of_same_opening_word(self):
        self.assertIn('3 sentences in a row open with "she", from line 14', self.out)

    def test_first_and_last_lines_skip_title_and_status(self):
        self.assertIn("first line: The water did not rush.", self.out)
        self.assertIn("last line: He went out laughing.", self.out)

    def test_dialogue_share(self):
        self.assertRegex(self.out.splitlines()[0], r"\d+ words, \d+% in dialogue")
        share = int(self.out.splitlines()[0].split("%")[0].split()[-1])
        self.assertTrue(20 <= share <= 45, share)

    def test_no_verdict_words(self):
        for word in ("dense", "too many", "fail", "error"):
            self.assertNotIn(word, self.out.lower())

    def test_curly_quotes_and_continued_speech(self):
        text = "“It did not rain,” she said. “And it was not\n\n“cold either.”\n\nThe road was dry.\n"
        code, out = run(text)
        self.assertEqual(code, 0)
        self.assertIn("negated narration: 0 ", line_for(out, "negated narration"))

    def test_empty_file_and_missing_file(self):
        code, out = run("<!-- status: draft -->\n# Chapter 1\n")
        self.assertEqual(code, 0)
        self.assertIn("no prose found", out)
        result = subprocess.run([sys.executable, "-B", "-I", str(HABITS), "/nonexistent/chapter.md"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)

    def test_borrowed_lines_are_listed(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "voice.md").write_text("# Voice\n\n- Example: She counted them again, because counting was free.\n- Short lines only.\n", encoding="utf-8")
            (base / "ch.md").write_text("The road was dry.\n\nShe counted again, because counting was free. Then the lamp went out.\n\nShe counted them twice.\n", encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", "-I", str(HABITS), str(base / "ch.md"), "--borrowed-from", str(base / "voice.md")], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertIn("shared with voice.md: 1 run(s)", result.stdout)
            self.assertIn('line 3: "again because counting was free"', result.stdout)
            missing = subprocess.run([sys.executable, "-B", "-I", str(HABITS), str(base / "ch.md"), "--borrowed-from", str(base / "nope.md")], capture_output=True, text=True)
            self.assertEqual(missing.returncode, 2)

    def test_folder_skips_delivered_and_previous_copies(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "_delivered").mkdir()
            (base / "001.md").write_text(CHAPTER, encoding="utf-8")
            (base / "002.md").write_text("She went home.\n", encoding="utf-8")
            (base / "_delivered" / "001.md").write_text(CHAPTER, encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", "-I", str(HABITS), str(base)], capture_output=True, text=True)
            self.assertIn("2 file(s) read", result.stdout)
            self.assertNotIn("_delivered", result.stdout)


if __name__ == "__main__":
    unittest.main()
