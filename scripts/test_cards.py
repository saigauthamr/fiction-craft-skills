import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "skills" / "story-continue" / "cards.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cards = load(CARDS, "cards")
diff_chapter = load(ROOT / "skills" / "story-edits" / "diff_chapter.py", "diff_chapter")
inspect_mod = load(ROOT / "skills" / "story-next" / "inspect.py", "inspect_mod")

CH = "<!-- status: awaiting check-in -->\n\nThe marker stood in the mud.\n\nShe waited.\n"
CARD = "Where: the outer channel.\nHappens: Ines sets a marker and the channel bends away.\n"


def run(*args):
    r = subprocess.run([sys.executable, "-B", "-I", str(CARDS), *map(str, args)], capture_output=True, text=True)
    return r.returncode, r.stdout


def tree(root):
    return sorted((str(p.relative_to(root)), p.read_bytes()) for p in root.rglob("*") if p.is_file())


class CardTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def report(self):
        return dict(line.split(": ", 1) for line in run("report", self.root)[1].splitlines())

    def test_a_chapter_with_no_card_is_missing(self):
        self.write("work/drafts/001-a.md", CH)
        r = self.report()
        self.assertEqual((r["chapters"], r["cards_ok"], r["cards_missing"]), ("1", "0", "001-a.md"))

    def test_stamping_a_written_card_makes_it_ok(self):
        self.write("work/drafts/001-a.md", CH)
        self.write("work/cards/001-a.md", CARD)
        self.assertIn("stamped 001-a.md", run("stamp", self.root, "001-a.md")[1])
        self.assertEqual(self.report()["cards_ok"], "1")
        self.assertTrue((self.root / "work/cards/001-a.md").read_text().startswith("<!-- card: 001-a.md; hash: "))

    def test_a_changed_chapter_makes_its_card_stale(self):
        self.write("work/drafts/001-a.md", CH)
        self.write("work/cards/001-a.md", CARD)
        run("stamp", self.root, "001-a.md")
        self.write("work/drafts/001-a.md", CH.replace("She waited.", "She left."))
        r = self.report()
        self.assertEqual((r["cards_ok"], r["cards_stale"]), ("0", "001-a.md"))

    def test_approving_a_chapter_does_not_stale_its_card(self):
        self.write("work/drafts/001-a.md", CH)
        self.write("work/cards/001-a.md", CARD)
        run("stamp", self.root, "001-a.md")
        self.write("work/drafts/001-a.md", CH.split("\n", 2)[2])
        self.assertEqual(self.report()["cards_ok"], "1")

    def test_rewrapping_does_not_stale_a_card(self):
        self.write("work/drafts/001-a.md", CH)
        self.write("work/cards/001-a.md", CARD)
        run("stamp", self.root, "001-a.md")
        self.write("work/drafts/001-a.md", CH.replace("The marker stood in the mud.", "The marker stood\nin the   mud."))
        self.assertEqual(self.report()["cards_ok"], "1")

    def test_a_card_with_no_header_is_stale(self):
        self.write("work/drafts/001-a.md", CH)
        self.write("work/cards/001-a.md", CARD)
        self.assertEqual(self.report()["cards_stale"], "001-a.md")

    def test_a_card_for_a_removed_chapter_is_an_orphan(self):
        self.write("work/cards/009-gone.md", CARD)
        self.assertEqual(self.report()["cards_orphan"], "009-gone.md")

    def test_previous_and_delivered_copies_are_not_chapters(self):
        self.write("work/drafts/001-a.md", CH)
        self.write("work/drafts/_previous/001-a.md", "old")
        self.write("work/drafts/_delivered/001-a.md", "old")
        self.assertEqual(self.report()["chapters"], "1")

    def test_stamping_again_replaces_the_header_and_never_doubles_it(self):
        self.write("work/drafts/001-a.md", CH)
        self.write("work/cards/001-a.md", CARD)
        run("stamp", self.root, "001-a.md")
        self.write("work/drafts/001-a.md", CH.replace("She waited.", "She left."))
        run("stamp", self.root, "001-a.md")
        text = (self.root / "work/cards/001-a.md").read_text()
        self.assertEqual(text.count("<!-- card:"), 1)
        self.assertEqual(self.report()["cards_ok"], "1")

    def test_stamping_needs_the_chapter_and_a_card_with_content(self):
        self.write("work/drafts/001-a.md", CH)
        self.assertEqual(run("stamp", self.root, "001-a.md")[0], 2)
        self.assertEqual(run("stamp", self.root, "009-none.md")[0], 2)
        self.write("work/cards/001-a.md", "\n\n")
        self.assertEqual(run("stamp", self.root, "001-a.md")[0], 2)

    def test_report_changes_nothing(self):
        self.write("work/drafts/001-a.md", CH)
        self.write("work/cards/001-a.md", CARD)
        before = tree(self.root)
        run("report", self.root)
        self.assertEqual(tree(self.root), before)

    def test_all_three_scripts_normalize_a_chapter_the_same_way(self):
        text = CH.replace("The marker stood in the mud.", "The marker  stood\nin the mud.") + "\n\n\nA third  paragraph.\n"
        self.assertEqual(cards.body(text), inspect_mod.body(text))
        self.assertEqual(cards.body(text), [p[2] for p in diff_chapter.paragraphs(text)])
        self.assertEqual(cards.body_hash(text), inspect_mod.card_hash(text))


    def test_the_inspector_reports_missing_stale_and_orphan_cards_like_the_script(self):
        self.write("work/drafts/001-a.md", CH)
        self.write("work/drafts/002-b.md", CH.replace("She waited.", "She left."))
        self.write("work/drafts/003-c.md", CH.replace("She waited.", "She ran."))
        self.write("work/cards/001-a.md", CARD)
        self.write("work/cards/002-b.md", CARD)
        self.write("work/cards/009-gone.md", CARD)
        run("stamp", self.root, "001-a.md")
        run("stamp", self.root, "002-b.md")
        self.write("work/drafts/002-b.md", CH.replace("She waited.", "She hid."))
        drafts = cards.chapters(self.root)
        missing, stale, orphan = inspect_mod.card_state(self.root, drafts)
        r = cards.report(self.root)
        self.assertEqual((missing, stale, orphan), (r["missing"], r["stale"], r["orphan"]))
        self.assertEqual((missing, stale, orphan), (["003-c.md"], ["002-b.md"], ["009-gone.md"]))


if __name__ == "__main__":
    unittest.main(verbosity=0)
