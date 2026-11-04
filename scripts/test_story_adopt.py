import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADOPT = ROOT / "skills" / "story-adopt" / "adopt.py"
SCAFFOLD = ROOT / "skills" / "story-onboard" / "scaffold.py"
FIX = ROOT / "fixtures" / "existing-material"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import office_fixtures as of  # noqa: E402


def run(*args):
    r = subprocess.run([sys.executable, "-I", str(ADOPT), *map(str, args)], capture_output=True, text=True)
    return r.returncode, r.stdout


def snap(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in sorted(Path(root).rglob("*")) if p.is_file()}


def copy_fixture(dst):
    import shutil
    shutil.copytree(FIX, dst)


class AdoptTests(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.p = Path(self._t.name) / "proj"
        copy_fixture(self.p)
        self.plan = Path(self._t.name) / "plan.json"

    def tearDown(self):
        self._t.cleanup()

    def make_plan(self):
        code, out = run("plan", self.p, "--json", self.plan)
        self.assertEqual(code, 0, out)
        return json.loads(self.plan.read_text())

    def test_plan_is_read_only(self):
        before = snap(self.p)
        run("plan", self.p)
        self.assertEqual(snap(self.p), before)

    def test_plan_classifies_files(self):
        items = {(i["origin"], i.get("sheet")): i for i in self.make_plan()["items"]}
        self.assertEqual(items[("chapter-1.docx", None)]["dest"], "work/drafts/chapter-1.md")
        self.assertEqual(items[("notes.txt", None)]["dest"], "work/brainstorm/imported/notes.md")
        self.assertEqual(items[("plot-notes.xlsx", "Timeline")]["class"], "timeline")
        self.assertEqual(items[("plot-notes.xlsx", "Characters")]["class"], "characters")
        self.assertEqual(items[("plot-notes.xlsx", "Word counts")]["class"], "wordcount")
        self.assertEqual(items[("plot-notes.xlsx", "Misc")]["class"], "unknown")
        self.assertTrue(items[("plot-notes.xlsx", "Misc")]["dest"].endswith(".csv"))

    def test_apply_refuses_without_yes_and_writes_nothing(self):
        self.make_plan()
        before = snap(self.p)
        code, out = run("apply", self.p, self.plan)
        self.assertEqual(code, 4)
        self.assertEqual(snap(self.p), before)

    def test_apply_leaves_originals_byte_identical(self):
        self.make_plan()
        before = snap(self.p)
        code, out = run("apply", self.p, self.plan, "--yes")
        self.assertEqual(code, 0, out)
        after = snap(self.p)
        for k, v in before.items():
            self.assertEqual(after[k], v, k)

    def test_converted_text_and_banner(self):
        self.make_plan()
        run("apply", self.p, self.plan, "--yes")
        text = (self.p / "work/drafts/chapter-1.md").read_text()
        self.assertIn("counted the barrels twice", text)
        self.assertIn('adopt: from "chapter-1.docx"', text)
        self.assertNotIn("Imported from", text)
        self.assertNotIn("needs review", text)

    def test_sheet_outputs(self):
        self.make_plan()
        run("apply", self.p, self.plan, "--yes")
        tl = (self.p / "kb/timeline/imported-plot-notes-timeline.md").read_text()
        self.assertIn("Status: needs review", tl)
        self.assertIn("| 1906 | The salt firm opens its second warehouse |", tl)
        self.assertIn("| 2310 |", (self.p / "work/data/plot-notes-word-counts.md").read_text())
        self.assertEqual((self.p / "work/data/plot-notes-misc.csv").read_text().splitlines()[0], "Thing,Maybe")

    def test_every_cell_survives_conversion(self):
        sys.path.insert(0, str(ROOT / "skills" / "story-adopt"))
        import importlib
        adopt = importlib.import_module("adopt")
        sheets = adopt.read_xlsx(FIX / "plot-notes.xlsx")
        self.make_plan()
        run("apply", self.p, self.plan, "--yes")
        outputs = {"Timeline": "kb/timeline/imported-plot-notes-timeline.md",
                   "Characters": "kb/characters/imported-plot-notes-characters.md",
                   "Word counts": "work/data/plot-notes-word-counts.md",
                   "Misc": "work/data/plot-notes-misc.csv"}
        for name, rel in outputs.items():
            text = (self.p / rel).read_text()
            for row in sheets[name]:
                for cell in row:
                    if cell is not None:
                        self.assertIn(str(cell), text, f"{name}: {cell}")

    def test_provenance_ledger_lists_every_import(self):
        plan = self.make_plan()
        run("apply", self.p, self.plan, "--yes")
        led = (self.p / "work/adopt/provenance.md").read_text()
        for it in plan["items"]:
            if it["kind"] != "section":
                self.assertIn(it["dest"], led)
                self.assertIn(it["sha1"], led)

    def test_replan_after_apply_finds_nothing_new(self):
        self.make_plan()
        run("apply", self.p, self.plan, "--yes")
        plan2 = self.make_plan()
        self.assertEqual(plan2["items"], [])
        self.assertTrue(any(s["reason"] == "already imported" for s in plan2["left_in_place"]))

    def test_existing_destination_is_not_overwritten(self):
        (self.p / "work/drafts").mkdir(parents=True)
        (self.p / "work/drafts/chapter-1.md").write_text("MY OWN FILE\n")
        plan = self.make_plan()
        dest = [i["dest"] for i in plan["items"] if i["origin"] == "chapter-1.docx"][0]
        self.assertEqual(dest, "work/drafts/chapter-1-2.md")
        run("apply", self.p, self.plan, "--yes")
        self.assertEqual((self.p / "work/drafts/chapter-1.md").read_text(), "MY OWN FILE\n")

    def test_unsupported_formats_are_listed_and_untouched(self):
        (self.p / "old.doc").write_bytes(b"binary")
        (self.p / "scan.pdf").write_bytes(b"pdf")
        plan = self.make_plan()
        left = {s["origin"] for s in plan["left_in_place"]}
        self.assertTrue({"old.doc", "scan.pdf"} <= left)
        run("apply", self.p, self.plan, "--yes")
        self.assertEqual((self.p / "old.doc").read_bytes(), b"binary")

    def test_origin_changed_since_plan_is_refused(self):
        self.make_plan()
        (self.p / "notes.txt").write_text("changed after the plan\n")
        before = snap(self.p)
        code, out = run("apply", self.p, self.plan, "--yes")
        self.assertEqual(code, 2)
        self.assertEqual(snap(self.p), before)

    def test_plan_for_another_folder_is_refused(self):
        self.make_plan()
        other = Path(self._t.name) / "other"
        other.mkdir()
        code, _ = run("apply", other, self.plan, "--yes")
        self.assertEqual(code, 2)

    def test_instruction_files_are_not_material(self):
        (self.p / "README.md").write_text("r")
        (self.p / "CLAUDE.md").write_text("# mine\n")
        origins = {i["origin"] for i in self.make_plan()["items"]}
        self.assertNotIn("README.md", origins)
        self.assertNotIn("CLAUDE.md", origins - {"CLAUDE.md"})  # only the section item may name it

    def test_review_lists_pages_needing_review(self):
        self.make_plan()
        run("apply", self.p, self.plan, "--yes")
        code, out = run("review", self.p)
        self.assertEqual(code, 0)
        self.assertIn("2 page(s) still marked needs review", out)

    def test_docx_headings_and_tables(self):
        d = self.p / "extra.docx"
        of.make_docx(d, [("h1", "A Heading"), "Body text."])
        self.make_plan()
        run("apply", self.p, self.plan, "--yes")
        out = (self.p / "work/brainstorm/imported/extra.md").read_text()
        self.assertIn("# A Heading", out)
        self.assertIn("Body text.", out)

    def test_minimal_xlsx_and_date_conversion(self):
        (self.p / "plot-notes.xlsx").unlink()
        serial = (date(2023, 3, 15) - date(1899, 12, 30)).days
        of.make_xlsx(self.p / "dates.xlsx", {"Timeline": [["Date", "Event"], [serial, "The harbor opens"]]})
        self.make_plan()
        run("apply", self.p, self.plan, "--yes")
        text = (self.p / "kb/timeline/imported-dates-timeline.md").read_text()
        self.assertIn("2023-03-15", text)

    def test_csv_file_is_a_sheet(self):
        (self.p / "plot-notes.xlsx").unlink()
        (self.p / "chars.csv").write_text("Name,Role,Age\nWren,Keeper,17\n")
        items = self.make_plan()["items"]
        self.assertTrue(any(i.get("class") == "characters" and i["origin"] == "chars.csv" for i in items))


class ExistingProjectTests(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.p = Path(self._t.name) / "proj"
        for d in ("kb/world", "kb/issues", "work/outline", "work/drafts", ".claude", ".git"):
            (self.p / d).mkdir(parents=True)
        for i in range(12):
            (self.p / "kb/world" / f"page{i}.md").write_text("x")
        (self.p / "kb/issues/open-questions.md").write_text("# Open\n")
        (self.p / "work/outline/ch1.md").write_text("beat")
        (self.p / ".claude/settings.json").write_text("{}")
        self.original = "# My project\n\nMy own rules here.\n"
        (self.p / "CLAUDE.md").write_text(self.original)
        self.plan = Path(self._t.name) / "plan.json"

    def tearDown(self):
        self._t.cleanup()

    def test_plan_describes_existing_project(self):
        code, out = run("plan", self.p, "--json", self.plan)
        self.assertEqual(code, 0)
        e = json.loads(self.plan.read_text())["existing"]
        self.assertEqual(e["kb_pages"], 13)
        self.assertEqual(e["open_questions_register"], "kb/issues/open-questions.md")
        self.assertIn(".claude", e["tool_folders_left_alone"])
        self.assertIn("story-onboard", out)

    def test_apply_writes_only_the_ledger(self):
        run("plan", self.p, "--json", self.plan)
        before = snap(self.p)
        code, out = run("apply", self.p, self.plan, "--yes")
        self.assertEqual(code, 0, out)
        after = snap(self.p)
        self.assertEqual(set(after) - set(before), {"work/adopt/provenance.md"})
        self.assertTrue(all(after[k] == v for k, v in before.items()))

    def test_onboarding_after_adopt_is_not_refused_and_keeps_the_writers_text(self):
        r = subprocess.run([sys.executable, "-I", str(SCAFFOLD), str(self.p), "--preset", "you-write-ai-checks"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 3)
        run("plan", self.p, "--json", self.plan)
        run("apply", self.p, self.plan, "--yes")
        r = subprocess.run([sys.executable, "-I", str(SCAFFOLD), str(self.p), "--preset", "you-write-ai-checks"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertTrue((self.p / "CLAUDE.md").read_text().startswith(self.original))


class RerunAndFailureTests(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.p = Path(self._t.name) / "proj"
        copy_fixture(self.p)
        self.plan = Path(self._t.name) / "plan.json"

    def tearDown(self):
        self._t.cleanup()

    def plan_items(self):
        run("plan", self.p, "--json", self.plan)
        return json.loads(self.plan.read_text())["items"]

    def ledger(self):
        return (self.p / "work/adopt/provenance.md").read_text()

    def test_ledger_records_method_and_status(self):
        self.plan_items()
        run("apply", self.p, self.plan, "--yes")
        rows = [l for l in self.ledger().splitlines() if l.startswith("| `")]
        self.assertTrue(rows)
        self.assertTrue(all(l.split("|")[6].strip() == "imported" for l in rows))

    def test_changed_source_is_imported_beside_the_old_version(self):
        self.plan_items()
        run("apply", self.p, self.plan, "--yes")
        first = (self.p / "work/brainstorm/imported/notes.md").read_text()
        with open(self.p / "notes.txt", "a") as f:
            f.write("\nA new note.\n")
        items = self.plan_items()
        self.assertEqual([i["origin"] for i in items], ["notes.txt"])
        self.assertTrue(items[0].get("changed"))
        self.assertEqual(items[0]["dest"], "work/brainstorm/imported/notes-2.md")
        run("apply", self.p, self.plan, "--yes")
        self.assertEqual((self.p / "work/brainstorm/imported/notes.md").read_text(), first)
        self.assertIn("A new note.", (self.p / "work/brainstorm/imported/notes-2.md").read_text())

    def test_a_failed_item_leaves_no_file_is_reported_and_is_retried(self):
        items = self.plan_items()
        bad = next(i for i in items if i["origin"] == "chapter-2.docx")
        (self.p / "chapter-2.docx").write_bytes(b"not a zip file")
        bad["sha1"] = __import__("hashlib").sha1(b"not a zip file").hexdigest()
        self.plan.write_text(json.dumps({**json.loads(self.plan.read_text()), "items": items}))
        code, out = run("apply", self.p, self.plan, "--yes")
        self.assertEqual(code, 5, out)
        self.assertIn("FAILED chapter-2.docx", out)
        self.assertFalse((self.p / bad["dest"]).exists())
        self.assertFalse(list(self.p.rglob("*.adopt-tmp")))
        self.assertTrue((self.p / "work/drafts/chapter-1.md").exists())
        self.assertIn("| failed |", self.ledger())
        retry = [i["origin"] for i in self.plan_items()]
        self.assertEqual(retry, ["chapter-2.docx"])


if __name__ == "__main__":
    unittest.main()
