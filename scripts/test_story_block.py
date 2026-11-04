import hashlib
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCAFFOLD = REPO / "skills" / "story-onboard" / "scaffold.py"
INSPECT = REPO / "skills" / "story-next" / "inspect.py"
INSTALL = REPO / "scripts" / "install.sh"

spec = importlib.util.spec_from_file_location("storyblock", REPO / "skills" / "story-onboard" / "storyblock.py")
sb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sb)

V1_STANDARD = "<!-- story-project:start -->\n## Story project\n\nold layout\n<!-- story-project:end -->\n"
V1_DIRECTOR = "<!-- story-project:start -->\n## Story project (director mode)\n\nold rules\n<!-- story-project:end -->\n"


def run(script, *args):
    r = subprocess.run([sys.executable, "-I", str(script), *map(str, args)], capture_output=True, text=True)
    return r.returncode, r.stdout


def facts(root):
    return dict(line.split(": ", 1) for line in run(INSPECT, root)[1].splitlines() if ": " in line)


def tree_hash(folder):
    h = hashlib.sha1()
    for p in sorted(folder.rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(folder)).encode() + p.read_bytes())
    return h.hexdigest()


class SettingsTests(unittest.TestCase):
    def test_every_preset_renders_and_parses_back(self):
        for name in sb.PRESETS:
            s = sb.resolve(name)
            self.assertEqual(sb.validate(s), [], name)
            status, _, parsed, _ = sb.classify({"AGENTS.md": sb.render(s), "CLAUDE.md": None})
            self.assertEqual((status, parsed), ("valid", s), name)

    def test_adjusting_a_stage_gives_the_matching_preset_or_custom(self):
        self.assertEqual(sb.resolve("ai-drafts-you-revise", plan="writer")["preset"], "you-outline-ai-drafts")
        self.assertEqual(sb.resolve("ai-writes-you-direct", draft="alternate")["preset"], "custom")

    def test_rule_1_design_only_has_no_prose_at_both_stages(self):
        problems = sb.validate(sb.resolve("design-only", revise="writer"))
        self.assertTrue(any(p.startswith("rule 1") for p in problems))

    def test_rule_2_ai_revises_only_its_own_prose(self):
        problems = sb.validate(sb.resolve("you-write-ai-checks", revise="ai"))
        self.assertTrue(any(p.startswith("rule 2") for p in problems))
        self.assertEqual(sb.validate(sb.resolve("custom", plan="ai", draft="alternate", revise="ai")), [])

    def test_custom_needs_every_stage(self):
        with self.assertRaises(ValueError):
            sb.resolve("custom", plan="ai", draft="ai")

    def test_craft_language_default_follows_the_drafter(self):
        self.assertEqual(sb.resolve("ai-writes-you-direct")["craft-language"], "none")
        self.assertEqual(sb.resolve("you-write-ai-checks")["craft-language"], "full")
        self.assertEqual(sb.resolve("design-only")["craft-language"], "brief")


class ClassifyTests(unittest.TestCase):
    def block(self, **overrides):
        return sb.render(sb.resolve("ai-drafts-you-revise", **overrides))

    def test_none(self):
        self.assertEqual(sb.classify({"AGENTS.md": "# notes\n", "CLAUDE.md": None})[0], "none")

    def test_missing_end_marker_is_malformed(self):
        text = self.block().replace(sb.END, "")
        self.assertEqual(sb.classify({"AGENTS.md": text, "CLAUDE.md": None})[0], "malformed")

    def test_unknown_key_invalid_value_and_invalid_combination_are_malformed(self):
        good = self.block()
        for bad in (good.replace("| check-in |", "| mood |"),
                    good.replace("| draft | ai |", "| draft | robot |"),
                    good.replace("| revise | writer |", "| revise | ai |").replace("| draft | ai |", "| draft | writer |")):
            status, detail, settings, _ = sb.classify({"AGENTS.md": bad, "CLAUDE.md": None})
            self.assertEqual((status, settings), ("malformed", None), detail)

    def test_missing_settings_markers_is_malformed(self):
        text = self.block().replace(sb.SETTINGS_START, "")
        self.assertEqual(sb.classify({"AGENTS.md": text, "CLAUDE.md": None})[0], "malformed")

    def test_two_blocks_in_one_file_is_duplicate(self):
        self.assertEqual(sb.classify({"AGENTS.md": self.block() + "\n" + self.block(), "CLAUDE.md": None})[0], "duplicate")

    def test_blocks_in_both_files_conflict_and_agents_wins(self):
        status, _, settings, src = sb.classify({"AGENTS.md": self.block(), "CLAUDE.md": sb.render(sb.resolve("design-only"))})
        self.assertEqual((status, src, settings["preset"]), ("conflicting", "AGENTS.md", "ai-drafts-you-revise"))

    def test_first_build_blocks_are_read_as_their_preset(self):
        st, _, s, _ = sb.classify({"AGENTS.md": None, "CLAUDE.md": V1_DIRECTOR})
        self.assertEqual((st, s["preset"]), ("v1-director", "ai-writes-you-direct"))
        st, _, s, _ = sb.classify({"AGENTS.md": V1_STANDARD, "CLAUDE.md": None})
        self.assertEqual((st, s["preset"]), ("v1-standard", "you-write-ai-checks"))

    def test_chapter_status_marker(self):
        self.assertEqual(sb.chapter_status("<!-- status: needs revision: uses the rejected harbor name -->\n# Ch 3"),
                         ("needs revision", "uses the rejected harbor name"))
        self.assertIsNone(sb.chapter_status("# Chapter 1\n\nNo marker here."))


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_a_preset_is_required(self):
        self.assertEqual(run(SCAFFOLD, self.root)[0], 4)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_invalid_combination_is_rejected_with_its_rule(self):
        code, out = run(SCAFFOLD, self.root, "--preset", "you-write-ai-checks", "--revise", "ai")
        self.assertEqual(code, 4)
        self.assertIn("rule 2", out)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_fresh_project_gets_block_folders_and_pointer(self):
        self.assertEqual(run(SCAFFOLD, self.root, "--preset", "design-only")[0], 0)
        self.assertEqual(facts(self.root)["setup"], "valid")
        self.assertIn("@AGENTS.md", (self.root / "CLAUDE.md").read_text())
        self.assertTrue((self.root / "work" / "beats").is_dir())

    def test_changing_settings_touches_only_the_block(self):
        (self.root / "AGENTS.md").write_text("# Mine\n\nKeep this exactly.\n")
        run(SCAFFOLD, self.root, "--preset", "ai-writes-you-direct")
        (self.root / "kb" / "characters" / "ines.md").write_text("Ines\n")
        (self.root / "work" / "drafts" / "001-x.md").write_text("<!-- status: draft -->\ntext\n")
        kb, work = tree_hash(self.root / "kb"), tree_hash(self.root / "work")
        self.assertEqual(run(SCAFFOLD, self.root, "--preset", "you-write-ai-checks")[0], 0)
        text = (self.root / "AGENTS.md").read_text()
        self.assertTrue(text.startswith("# Mine\n\nKeep this exactly.\n"))
        self.assertEqual((tree_hash(self.root / "kb"), tree_hash(self.root / "work")), (kb, work))
        self.assertEqual(facts(self.root)["preset"], "you-write-ai-checks")

    def test_rerun_with_keep_changes_nothing(self):
        run(SCAFFOLD, self.root, "--preset", "ai-outlines-you-write")
        before = tree_hash(self.root)
        code, out = run(SCAFFOLD, self.root, "--keep")
        self.assertEqual((code, tree_hash(self.root)), (0, before))
        self.assertIn("no changes", out)

    def test_dry_run_writes_nothing_and_shows_a_diff(self):
        (self.root / "AGENTS.md").write_text(V1_DIRECTOR)
        before = tree_hash(self.root)
        code, out = run(SCAFFOLD, self.root, "--keep", "--dry-run")
        self.assertEqual((code, tree_hash(self.root)), (0, before))
        self.assertIn("+<!-- story-project:start v2 -->", out)

    def test_v1_blocks_migrate_with_keep(self):
        (self.root / "CLAUDE.md").write_text("# Project\n\n" + V1_DIRECTOR + "\nAfter.\n")
        self.assertEqual(run(SCAFFOLD, self.root, "--keep")[0], 0)
        text = (self.root / "CLAUDE.md").read_text()
        self.assertTrue(text.startswith("# Project\n\n") and text.endswith("\nAfter.\n"))
        self.assertNotIn("(director mode)", text)
        self.assertEqual(facts(self.root)["preset"], "ai-writes-you-direct")

    def test_established_project_without_block_is_refused(self):
        (self.root / "kb" / "world").mkdir(parents=True)
        for i in range(10):
            (self.root / "kb" / "world" / f"p{i}.md").write_text("x")
        before = tree_hash(self.root)
        self.assertEqual(run(SCAFFOLD, self.root, "--preset", "design-only")[0], 3)
        self.assertEqual(tree_hash(self.root), before)
        self.assertEqual(run(SCAFFOLD, self.root, "--preset", "design-only", "--force")[0], 0)

    def test_duplicate_blocks_need_repair(self):
        two = sb.render(sb.resolve("design-only")) + "\n" + sb.render(sb.resolve("ai-writes-you-direct"))
        (self.root / "AGENTS.md").write_text("Top.\n\n" + two)
        self.assertEqual(run(SCAFFOLD, self.root, "--preset", "design-only")[0], 6)
        self.assertEqual(run(SCAFFOLD, self.root, "--preset", "design-only", "--repair")[0], 0)
        text = (self.root / "AGENTS.md").read_text()
        self.assertEqual(text.count(sb.START_V2), 1)
        self.assertTrue(text.startswith("Top.\n"))

    def test_conflicting_files_repair_leaves_a_pointer(self):
        (self.root / "AGENTS.md").write_text(sb.render(sb.resolve("design-only")))
        (self.root / "CLAUDE.md").write_text("# Claude\n\nMy note.\n\n" + sb.render(sb.resolve("ai-writes-you-direct")))
        run(SCAFFOLD, self.root, "--keep")
        self.assertEqual(facts(self.root)["setup"], "conflicting")
        run(SCAFFOLD, self.root, "--keep", "--repair")
        claude = (self.root / "CLAUDE.md").read_text()
        self.assertNotIn("story-project:start", claude)
        self.assertIn("My note.", claude)
        self.assertIn("AGENTS.md", claude)
        self.assertEqual(facts(self.root)["setup"], "valid")

    def test_missing_end_marker_is_never_rewritten(self):
        broken = sb.render(sb.resolve("design-only")).replace(sb.END, "")
        (self.root / "AGENTS.md").write_text(broken)
        self.assertEqual(run(SCAFFOLD, self.root, "--preset", "design-only", "--repair")[0], 6)
        self.assertEqual((self.root / "AGENTS.md").read_text(), broken)


class InspectorTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        run(SCAFFOLD, self.root, "--preset", "ai-writes-you-direct")

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def test_reports_chapter_statuses(self):
        self.write("work/drafts/001-a.md", "<!-- status: accepted -->\nx")
        self.write("work/drafts/002-b.md", "<!-- status: awaiting check-in -->\nx")
        self.write("work/drafts/003-c.md", "<!-- status: needs revision: harbor name rejected -->\nx")
        self.write("work/drafts/_previous/003-c.md", "<!-- status: draft -->\nold")
        f = facts(self.root)
        self.assertEqual((f["chapters_trusted"], f["chapters_awaiting_check_in"], f["chapters_needs_revision"], f["draft_files"]),
                         ("1", "002-b.md", "003-c.md", "3"))

    def test_counts_pending_rejected_facts_and_open_findings(self):
        self.write("work/brainstorm/queue.md", "- [pending major] The guild owns the island\n- [pending minor] The ferry is green\n- [rejected] Tomas is her brother\n")
        self.write("kb/issues/open-questions.md", "- [pending major] When the channels started moving\n")
        self.write("work/critique-reports/001-check.md", "- [open] plot.promise.01 the hook is missing\n- [resolved] a typo\n")
        f = facts(self.root)
        self.assertEqual((f["pending_major_facts"], f["pending_minor_facts"], f["rejected_facts"], f["open_findings"]), ("2", "1", "1", "1"))

    def test_lists_beats_not_yet_drafted(self):
        self.write("work/beats/001-a.md", "beats")
        self.write("work/beats/002-b.md", "beats")
        self.write("work/drafts/001-a.md", "<!-- status: draft -->\nx")
        self.assertEqual(facts(self.root)["undrafted_beats"], "002-b.md")

    def test_inspection_changes_nothing(self):
        self.write("work/drafts/001-a.md", "<!-- status: draft -->\nx")
        before = tree_hash(self.root)
        run(INSPECT, self.root)
        self.assertEqual(tree_hash(self.root), before)


class NextStepTests(unittest.TestCase):
    """One fixture per step of the precedence order."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def project(self, preset="ai-drafts-you-revise", **files):
        run(SCAFFOLD, self.root, "--preset", preset)
        for rel, text in files.items():
            p = self.root / rel.replace("__", "/")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        f = facts(self.root)
        return f["next_step"], f["next_skill"], f["next_owner"]

    def test_01_no_setup(self):
        self.assertEqual(facts(self.root)["next_skill"], "story-onboard")

    def test_02_existing_material(self):
        self.assertEqual(self.project(**{"chapter-1.docx": "x"})[1], "story-adopt")

    def test_03_needs_revision_comes_before_everything_else(self):
        step = self.project(**{"work__drafts__003-c.md": "<!-- status: needs revision: rejected fact -->\nx",
                               "work__brainstorm__q.md": "- [pending major] something\n"})
        self.assertEqual(step[1:], ("story-revise", "writer"))

    def test_04_pending_major_facts(self):
        self.assertEqual(self.project(**{"work__brainstorm__q.md": "- [pending major] The guild owns the island\n"})[:3],
                         ("decide pending story facts", "none", "writer-decides"))

    def test_05_awaiting_check_in(self):
        self.assertEqual(self.project(**{"work__drafts__001-a.md": "<!-- status: awaiting check-in -->\nx"})[0], "check-in on drafted chapters")

    def test_06_unchecked_draft(self):
        self.assertEqual(self.project(**{"work__drafts__001-a.md": "<!-- status: draft -->\nx"})[1:], ("story-check", "ai"))

    def test_07_open_findings_go_to_the_revise_owner(self):
        step = self.project(**{"work__drafts__001-a.md": "<!-- status: draft -->\nx",
                               "work__critique-reports__001-a-check.md": "- [open] plot.ppp.02 no signpost\n"})
        self.assertEqual(step[1:], ("story-revise", "writer"))

    def test_unmarked_chapters_are_trusted_and_never_recommended_for_a_check(self):
        step = self.project(**{"work__spec__spec.md": "s",
                               "work__drafts__001-the-writers-own.md": "# Chapter 1\n\nWritten by hand.\n"})
        f = facts(self.root)
        self.assertEqual((f["chapters_trusted"], f["unchecked_drafts"]), ("1", "none"))
        self.assertNotEqual(step[1], "story-check")

    def test_a_chapter_marked_draft_is_still_recommended_for_a_check(self):
        self.assertEqual(self.project(**{"work__drafts__001-a.md": "<!-- status: draft -->\nx"})[1], "story-check")

    def test_a_first_build_accepted_line_is_read_as_trusted(self):
        step = self.project(**{"work__drafts__001-a.md": "<!-- status: accepted -->\nx"})
        self.assertNotIn(step[1], ("story-check", "story-revise"))
        self.assertEqual(facts(self.root)["chapters_trusted"], "1")

    def test_07_a_finding_kept_on_purpose_is_settled(self):
        step = self.project(**{"work__drafts__001-a.md": "# Chapter 1\n\nWritten by hand.\n",
                               "work__critique-reports__001-a-check.md": "- [resolved] declined: kept on purpose\n"})
        self.assertNotEqual(step[1], "story-revise")

    def test_08_undrafted_beats_go_to_the_draft_owner(self):
        step = self.project("ai-outlines-you-write", **{"work__spec__spec.md": "s", "work__beats__002-b.md": "b"})
        self.assertEqual(step[1:], ("story-draft", "writer"))

    def test_09_spec_without_beats(self):
        self.assertEqual(self.project(**{"work__spec__spec.md": "s"})[1:], ("story-plan", "ai"))

    def test_10_developed_without_spec(self):
        self.assertEqual(self.project(**{"kb__characters__ines.md": "Ines"})[:2], ("write the spec", "story-plan"))

    def test_11_nothing_yet(self):
        self.assertEqual(self.project("you-write-ai-checks")[1:], ("story-develop", "writer"))

    def test_design_only_ends_at_an_approved_design(self):
        step = self.project("design-only", **{"work__spec__spec.md": "s", "work__beats__001-a.md": "b"})
        self.assertEqual(step[:2], ("design complete", "none"))

    def test_design_only_never_drafts(self):
        step = self.project("design-only", **{"work__spec__spec.md": "s", "work__beats__001-a.md": "b",
                                              "work__drafts__001-a.md": "<!-- status: draft -->\nx"})
        self.assertNotIn(step[1], ("story-draft", "story-check", "story-revise"))


class InstallTests(unittest.TestCase):
    def test_default_target_is_the_current_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run(["sh", str(INSTALL)], cwd=tmp, capture_output=True, text=True, env={**os.environ, "HOME": tmp + "/home"})
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((Path(tmp) / ".claude" / "skills" / "plot").is_symlink())
            self.assertFalse((Path(tmp) / "home" / ".claude").exists())

    def test_refuses_to_install_into_the_library_itself(self):
        r = subprocess.run(["sh", str(INSTALL)], cwd=REPO, capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((REPO / ".claude" / "skills").exists())

    def test_global_install_when_asked(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run(["sh", str(INSTALL), "--global"], cwd=tmp, capture_output=True, text=True, env={**os.environ, "HOME": tmp})
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((Path(tmp) / ".claude" / "skills" / "plot").is_symlink())


if __name__ == "__main__":
    unittest.main()
