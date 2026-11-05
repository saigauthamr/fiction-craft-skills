import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "story-edits" / "diff_chapter.py"
sys.path.insert(0, str(SCRIPT.parent))
import diff_chapter as dc  # noqa: E402

BASE = """<!-- status: awaiting check-in -->

The marker stood in the mud at low tide.

Tomas poled the ferry in silence. He did not look at her.

She wrote the date in her book and closed it.
"""


def run(delivered, current):
    with tempfile.TemporaryDirectory() as d:
        a, b = Path(d, "a.md"), Path(d, "b.md")
        a.write_text(delivered, encoding="utf-8")
        b.write_text(current, encoding="utf-8")
        r = subprocess.run([sys.executable, "-B", "-I", str(SCRIPT), str(a), str(b)], capture_output=True, text=True)
    return r.returncode, r.stdout


class DiffChapter(unittest.TestCase):
    def test_identical_is_unchanged(self):
        code, out = run(BASE, BASE)
        self.assertEqual(code, 0)
        self.assertIn("result: unchanged", out)
        self.assertIn("kept: 3", out)

    def test_status_line_removed_is_unchanged(self):
        code, out = run(BASE, BASE.split("\n", 2)[2])
        self.assertIn("result: unchanged", out)

    def test_rewrapped_text_is_unchanged(self):
        wrapped = BASE.replace("The marker stood in the mud at low tide.", "The marker stood in\nthe mud   at low tide.")
        self.assertIn("result: unchanged", run(BASE, wrapped)[1])

    def test_cut_paragraph(self):
        cur = BASE.replace("\nTomas poled the ferry in silence. He did not look at her.\n", "")
        out = run(BASE, cur)[1]
        self.assertIn("result: edited", out)
        self.assertIn("cut: 1", out)
        self.assertIn("cut: delivered line 5:", out)
        self.assertIn("kept: 2", out)

    def test_added_paragraph_with_location(self):
        cur = BASE + "\nThe water was already turning.\n"
        out = run(BASE, cur)[1]
        self.assertIn("added: 1", out)
        self.assertIn("added: current line 9:", out)

    def test_rewritten_paragraph_is_paired(self):
        cur = BASE.replace("Tomas poled the ferry in silence. He did not look at her.",
                           "Tomas poled the ferry in silence. He did not look at her once.")
        out = run(BASE, cur)[1]
        self.assertIn("rewritten: 1", out)
        self.assertIn("cut: 0", out)
        self.assertIn("added: 0", out)
        self.assertIn("delivered line 5 -> current line 5", out)

    def test_unrelated_replacement_is_cut_and_added(self):
        cur = BASE.replace("She wrote the date in her book and closed it.", "A gull cried over the empty flats and nobody answered.")
        out = run(BASE, cur)[1]
        self.assertIn("rewritten: 0", out)
        self.assertIn("cut: 1", out)
        self.assertIn("added: 1", out)

    def test_missing_file_is_an_error(self):
        r = subprocess.run([sys.executable, "-B", "-I", str(SCRIPT), "/nonexistent/a.md", "/nonexistent/b.md"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("error:", r.stdout)

    def test_long_paragraph_is_previewed_short(self):
        long = "word " * 100
        out = run("A\n\n" + long + "\n", "A\n")[1]
        cut_line = [line for line in out.splitlines() if line.startswith("cut: delivered")][0]
        self.assertLess(len(cut_line), 140)
        self.assertTrue(cut_line.endswith("..."))


if __name__ == "__main__":
    unittest.main(verbosity=0)
