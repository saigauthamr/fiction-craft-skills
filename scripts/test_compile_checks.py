import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compile_checks  # noqa: E402

COMPILER = HERE / "compile_checks.py"


def skill(name, stype, body):
    return f"---\nname: {name}\nmetadata:\n  type: {stype}\ndescription: >\n  test\n---\n\n# {name}\n\n{body}"


PLOT_A = skill("plot-a", "framework", "Intro.\n\n## Checks\n\n- `plot.a.01` First check.\n- `plot.a.02` Second check.\n\n## Cautions\n\nSome.\n")
PLOT_B = skill("plot-b", "framework", "## Checks\n\n- `plot.b.01` Only check.\n")
PLOT_NONE = skill("plot-none", "framework", "## Checks\n\nNone. A study method.\n")
CONSUMER = skill("story-x", "workflow", "Hand-written steps.\n")


class CompilerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        for name, text in (("plot-a", PLOT_A), ("plot-b", PLOT_B), ("plot-none", PLOT_NONE), ("story-x", CONSUMER)):
            (self.root / "skills" / name).mkdir(parents=True)
            (self.root / "skills" / name / "SKILL.md").write_text(text)
        (self.root / "scripts").mkdir()
        self.map("story-x/plan: plot.a.* plot.b.01\nstory-x/check: plot.a.02\n")

    def tearDown(self):
        self._tmp.cleanup()

    def map(self, text):
        (self.root / "scripts" / "check-map.txt").write_text(text)

    def compile(self, write=True):
        errors, notices = [], []
        stale = compile_checks.compile_all(self.root, write, errors, notices)
        return stale, errors, notices

    def consumer(self):
        return (self.root / "skills" / "story-x" / "SKILL.md").read_text()

    def check_cli(self):
        return subprocess.run([sys.executable, "-I", str(COMPILER), "--check", str(self.root)], capture_output=True, text=True).returncode

    def test_writes_sections_per_operation_with_ids_and_sources(self):
        stale, errors, _ = self.compile()
        self.assertEqual((stale, errors), (["story-x"], []))
        text = self.consumer()
        self.assertIn("<!-- generated:checks:start plan -->", text)
        self.assertIn("- `plot.a.01` First check. (`plot-a`)", text)
        self.assertIn("- `plot.b.01` Only check. (`plot-b`)", text)
        self.assertIn("<!-- generated:checks:start check -->", text)
        self.assertTrue(text.startswith(CONSUMER.rstrip("\n")))

    def test_deterministic_and_check_passes_after_compile(self):
        self.compile()
        first = self.consumer()
        stale, _, _ = self.compile()
        self.assertEqual((stale, self.consumer()), ([], first))
        self.assertEqual(self.check_cli(), 0)

    def test_hand_edit_inside_markers_is_drift_and_gets_overwritten(self):
        self.compile()
        p = self.root / "skills" / "story-x" / "SKILL.md"
        p.write_text(p.read_text().replace("First check.", "Edited by hand."))
        self.assertEqual(self.check_cli(), 1)
        self.compile()
        self.assertIn("First check.", self.consumer())
        self.assertNotIn("Edited by hand.", self.consumer())

    def test_hand_edit_outside_markers_is_preserved(self):
        self.compile()
        p = self.root / "skills" / "story-x" / "SKILL.md"
        p.write_text(p.read_text().replace("Hand-written steps.", "Hand-written steps, revised."))
        self.compile()
        self.assertIn("Hand-written steps, revised.", self.consumer())
        self.assertEqual(self.check_cli(), 0)

    def test_source_change_is_drift(self):
        self.compile()
        p = self.root / "skills" / "plot-b" / "SKILL.md"
        p.write_text(p.read_text().replace("Only check.", "Only check, reworded."))
        self.assertEqual(self.check_cli(), 1)

    def test_unmapped_section_is_removed(self):
        self.compile()
        self.map("story-x/plan: plot.a.*\n")
        self.compile()
        self.assertNotIn("generated:checks:start check", self.consumer())

    def test_unknown_id_and_empty_wildcard_are_errors(self):
        self.map("story-x: plot.a.09 plot.zzz.*\n")
        _, errors, _ = self.compile(write=False)
        self.assertTrue(any("unknown check ID 'plot.a.09'" in e for e in errors))
        self.assertTrue(any("'plot.zzz.*' matches no check" in e for e in errors))

    def test_duplicate_ids_are_errors(self):
        (self.root / "skills" / "plot-b" / "SKILL.md").write_text(PLOT_B.replace("plot.b.01", "plot.a.01"))
        _, errors, _ = self.compile(write=False)
        self.assertTrue(any("duplicate check ID plot.a.01" in e for e in errors))

    def test_contract_framework_without_checks_or_with_unnumbered_item_is_an_error(self):
        (self.root / "skills" / "plot-b" / "SKILL.md").write_text(skill("plot-b", "framework", "No checks here.\n"))
        (self.root / "skills" / "plot-none" / "SKILL.md").write_text(PLOT_NONE.replace("None. A study method.", "- an unnumbered check"))
        self.map("story-x: plot.a.01\n")
        _, errors, _ = self.compile(write=False)
        self.assertTrue(any(e.startswith("plot-b: framework has no '## Checks'") for e in errors))
        self.assertTrue(any(e.startswith("plot-none: check without a valid ID") for e in errors))

    def test_missing_consumer_is_a_note_not_an_error(self):
        self.map("story-y: plot.a.01\n")
        _, errors, notices = self.compile(write=False)
        self.assertEqual(errors, [])
        self.assertTrue(any("story-y" in n for n in notices))

    def test_unused_check_is_an_error_only_when_every_check_must_have_a_consumer(self):
        self.map("story-x: plot.a.*\n")
        _, errors, _ = self.compile(write=False)
        self.assertEqual(errors, [])
        errors, notices = [], []
        compile_checks.compile_all(self.root, False, errors, notices, require_all=True)
        self.assertTrue(any(e.startswith("plot.b.01 (plot-b): no skill uses this check") for e in errors))
        self.assertEqual(self.check_cli(), 1)

    def test_errors_block_writing(self):
        self.map("story-x: plot.a.09\n")
        before = self.consumer()
        subprocess.run([sys.executable, "-I", str(COMPILER), str(self.root)], capture_output=True)
        self.assertEqual(self.consumer(), before)


if __name__ == "__main__":
    unittest.main()
