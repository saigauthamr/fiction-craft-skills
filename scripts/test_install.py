import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class InstallTests(unittest.TestCase):
    def test_install_prunes_only_dead_links_owned_by_this_library(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            stale = target / "retired"
            stale.symlink_to(ROOT / "skills" / "retired")
            foreign = target / "foreign"
            foreign.symlink_to(target / "missing-foreign")
            custom = target / "custom"
            custom.mkdir()
            note = custom / "note.txt"
            note.write_text("writer-owned")

            result = subprocess.run(
                ["sh", str(ROOT / "scripts/install.sh"), str(target)],
                capture_output=True, text=True, check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(stale.is_symlink())
            self.assertEqual(foreign.readlink(), target / "missing-foreign")
            self.assertEqual(note.read_text(), "writer-owned")
            self.assertEqual((target / "story-draft").resolve(), ROOT / "skills/story-draft")


def install(*args, cwd, home=None):
    env = {**os.environ, "HOME": str(home or cwd)}
    return subprocess.run(["sh", str(ROOT / "scripts/install.sh"), *args], cwd=cwd, capture_output=True, text=True, env=env)


class TargetTests(unittest.TestCase):
    def test_agents_flag_installs_into_the_shared_folder_for_this_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = install("--agents", cwd=tmp)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((Path(tmp) / ".agents/skills/story-draft").is_symlink())
            self.assertFalse((Path(tmp) / ".claude").exists())

    def test_global_agents_goes_to_the_users_shared_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            home.mkdir()
            r = install("--agents", "--global", cwd=tmp, home=home)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((home / ".agents/skills/plot").is_symlink())
            self.assertFalse((Path(tmp) / ".agents").exists())

    def test_default_is_still_the_claude_folder_for_this_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(install(cwd=tmp).returncode, 0)
            self.assertTrue((Path(tmp) / ".claude/skills/plot").is_symlink())

    def test_unknown_option_is_refused_and_help_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = install("--bogus", cwd=tmp)
            self.assertEqual(r.returncode, 2)
            self.assertFalse((Path(tmp) / ".claude").exists())
            h = install("--help", cwd=tmp)
            self.assertEqual(h.returncode, 0)
            self.assertIn("--agents", h.stdout)


class CopyTests(unittest.TestCase):
    def test_copy_makes_real_folders_marked_as_ours_and_without_bytecode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = install("--agents", "--copy", cwd=tmp)
            self.assertEqual(r.returncode, 0, r.stderr)
            skill = Path(tmp) / ".agents/skills/story-onboard"
            self.assertTrue(skill.is_dir() and not skill.is_symlink())
            self.assertTrue((skill / ".installed-by-fiction-craft-skills").is_file())
            self.assertTrue((skill / "SKILL.md").is_file() and (skill / "scaffold.py").is_file())
            self.assertEqual(list(Path(tmp).rglob("__pycache__")), [])

    def test_rerunning_a_copy_refreshes_our_copy_but_never_a_writers_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            install("--agents", "--copy", cwd=tmp)
            target = Path(tmp) / ".agents/skills"
            (target / "plot/SKILL.md").write_text("stale")
            mine = target / "custom-skill"
            mine.mkdir()
            (mine / "SKILL.md").write_text("writer-owned")
            clash = target / "character"
            shutil_rm = __import__("shutil").rmtree
            shutil_rm(clash)
            clash.mkdir()
            (clash / "SKILL.md").write_text("writer's own character skill")
            r = install("--agents", "--copy", cwd=tmp)
            self.assertEqual(r.returncode, 1)
            self.assertIn("skip character", r.stderr)
            self.assertNotEqual((target / "plot/SKILL.md").read_text(), "stale")
            self.assertEqual((clash / "SKILL.md").read_text(), "writer's own character skill")
            self.assertEqual((mine / "SKILL.md").read_text(), "writer-owned")

    def test_copy_over_an_earlier_link_install_replaces_the_link_not_the_library(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            install("--agents", cwd=tmp)
            install("--agents", "--copy", cwd=tmp)
            plot = Path(tmp) / ".agents/skills/plot"
            self.assertFalse(plot.is_symlink())
            self.assertTrue((ROOT / "skills/plot/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
