import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LINT = Path(__file__).resolve().parent / "lint.py"
NAME = "02 - T - Writing Lecture #2 (2025).md"
GOOD_FRAMEWORK = f"""---
name: demo
metadata:
  type: framework
description: >
  Demo framework.
---

# Demo

A point.
"""
GOOD_EXTRACTION = """# Extraction: Lecture 2 - T

## Summary
Short.

## Frameworks

### Demo
- **Statement**: x [L2 @ 01:00]
- **Citations**: [L2 @ 01:00]

## Principles
- a principle [L2 @ 02:00]

## Terms
- t

## Cross-references
- none

## Unclear
- none
"""


def run(files, extraction=GOOD_EXTRACTION, extra=None):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "transcripts").mkdir()
        (root / "extractions").mkdir()
        (root / "scripts").mkdir()
        (root / "scripts" / "check-map.txt").write_text("# no consumers\n", encoding="utf-8")
        (root / "transcripts" / NAME).write_text("# T\n\n[00:00] a\n\n[05:00] b\n", encoding="utf-8")
        if extraction is not None:
            (root / "extractions" / NAME).write_text(extraction, encoding="utf-8")
        for rel, text in files.items():
            p = root / "skills" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        for rel, text in (extra or {}).items():
            q = root / rel
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_text(text, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(LINT), str(root)], capture_output=True, text=True)
        return r.returncode, r.stdout


class SkillTests(unittest.TestCase):
    def test_good_framework_passes(self):
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK})
        self.assertEqual(code, 0, out)

    def test_reference_to_extraction_fails(self):
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK + "\nSee `../../extractions/x.md`.\n"})
        self.assertEqual(code, 1)
        self.assertIn("references working material", out)

    def test_inline_citation_fails(self):
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK.replace("A point.", "A point [L2 @ 01:00].")})
        self.assertEqual(code, 1)
        self.assertIn("references working material", out)

    def test_overlong_quote_fails(self):
        quote = " ".join(["word"] * 50)
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK.replace("A point", f'He said "{quote}".')})
        self.assertEqual(code, 1)
        self.assertIn("quote too long", out)

    def test_short_quote_passes(self):
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK.replace("A point", 'He said "one short defining line of ten words or so here".')})
        self.assertEqual(code, 0, out)

    def test_missing_description_fails(self):
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK.replace("  Demo framework.\n", "")})
        self.assertEqual(code, 1)
        self.assertIn("missing description", out)

    def test_long_description_fails(self):
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK.replace("Demo framework.", "x" * 1100)})
        self.assertEqual(code, 1)
        self.assertIn("description is", out)

    def test_name_mismatch_fails(self):
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK.replace("name: demo", "name: other")})
        self.assertEqual(code, 1)
        self.assertIn("does not match folder", out)

    def test_framework_referencing_a_missing_skill_fails(self):
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK.replace("A point.", "See `plot-ghost` for more.")})
        self.assertEqual(code, 1)
        self.assertIn("references missing skill 'plot-ghost'", out)

    def test_framework_referencing_an_existing_skill_passes(self):
        other = GOOD_FRAMEWORK.replace("name: demo", "name: plot-real") + "\n## Checks\n\nNone. A test fixture.\n"
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK.replace("A point.", "See `plot-real` for more."), "plot-real/SKILL.md": other})
        self.assertEqual(code, 0, out)

    def test_hub_with_missing_child_fails(self):
        hub = "---\nname: hubby\nmetadata:\n  type: hub\ndescription: >\n  A hub.\n---\n\n## Children\n\n- `ghost`: not real\n"
        code, out = run({"hubby/SKILL.md": hub})
        self.assertEqual(code, 1)
        self.assertIn("missing child 'ghost'", out)

    def test_hub_with_real_child_passes(self):
        hub = "---\nname: hubby\nmetadata:\n  type: hub\ndescription: >\n  A hub.\n---\n\n## Children\n\n- `demo`: real\n"
        code, out = run({"hubby/SKILL.md": hub, "demo/SKILL.md": GOOD_FRAMEWORK})
        self.assertEqual(code, 0, out)


class ExtractionTests(unittest.TestCase):
    def test_framework_without_citation_fails(self):
        bad = GOOD_EXTRACTION.replace("- **Statement**: x [L2 @ 01:00]\n- **Citations**: [L2 @ 01:00]", "- **Statement**: x")
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK}, extraction=bad)
        self.assertEqual(code, 1)
        self.assertIn("has no citation", out)

    def test_citation_past_end_fails(self):
        bad = GOOD_EXTRACTION.replace("[L2 @ 02:00]", "[L2 @ 59:00]")
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK}, extraction=bad)
        self.assertEqual(code, 1)
        self.assertIn("past the end", out)

    def test_missing_section_fails(self):
        bad = GOOD_EXTRACTION.replace("## Unclear\n- none\n", "")
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK}, extraction=bad)
        self.assertEqual(code, 1)
        self.assertIn("missing section '## Unclear'", out)


class FixtureTests(unittest.TestCase):
    def build(self, tmp, spec=0, beats=0, drafts=0, markers=True):
        root = Path(tmp)
        (root / "skills").mkdir()
        (root / "scripts").mkdir()
        (root / "scripts" / "check-map.txt").write_text("# no consumers\n")
        base = root / "fixtures"
        for name in ("empty-scaffolded", "spec-only", "draft-only", "with-instructions", "existing-material",
                     "grilled", "beats-ready", "drafted", "reviewed", "serial"):
            (base / name).mkdir(parents=True)
        for name in ("empty-scaffolded", "spec-only", "draft-only", "grilled", "beats-ready", "drafted", "reviewed", "serial"):
            d = base / name
            for rel in ("kb/characters", "kb/world", "kb/timeline", "kb/canon", "kb/styles", "kb/samples", "kb/issues",
                        "work/spec", "work/beats", "work/drafts", "work/critique-reports", "work/brainstorm"):
                (d / rel).mkdir(parents=True)
            (d / "AGENTS.md").write_text("<!-- story-project:start -->\nx\n<!-- story-project:end -->\n" if markers else "x\n")
        (base / "with-instructions" / "AGENTS.md").write_text("mine\n")
        (base / "spec-only" / "work" / "spec" / "spec.md").write_text("s")
        (base / "draft-only" / "work" / "drafts" / "c1.md").write_text("d")
        (base / "serial" / "work" / "drafts" / "c1.md").write_text("d")
        for name, kinds in (("beats-ready", ("spec", "beats")), ("drafted", ("spec", "beats", "drafts")),
                            ("reviewed", ("spec", "beats", "drafts", "critique-reports"))):
            for k in kinds:
                (base / name / "work" / k / "f.md").write_text("x")
        return root

    def lint(self, root):
        r = subprocess.run([sys.executable, "-I", str(LINT), str(root)], capture_output=True, text=True)
        return r.returncode, r.stdout

    def test_good_fixtures_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self.lint(self.build(tmp))
            self.assertEqual(code, 0, out)

    def test_spec_only_with_a_beats_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.build(tmp)
            (root / "fixtures" / "spec-only" / "work" / "beats" / "b.md").write_text("b")
            code, out = self.lint(root)
            self.assertEqual(code, 1)
            self.assertIn("work/beats should be empty", out)

    def test_draft_only_without_a_draft_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.build(tmp)
            (root / "fixtures" / "draft-only" / "work" / "drafts" / "c1.md").unlink()
            code, out = self.lint(root)
            self.assertEqual(code, 1)
            self.assertIn("work/drafts should have files", out)

    def test_scaffolded_fixture_missing_section_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self.lint(self.build(tmp, markers=False))
            self.assertEqual(code, 1)
            self.assertIn("no story project section", out)

    def test_instructions_fixture_must_be_unscaffolded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.build(tmp)
            (root / "fixtures" / "with-instructions" / "kb").mkdir()
            code, out = self.lint(root)
            self.assertEqual(code, 1)
            self.assertIn("should not already have kb/ or work/", out)


def manifests(version_claude="0.1.0", version_codex="0.1.0", codex_name="fiction-craft-skills"):
    import json
    plugin = lambda v, n="fiction-craft-skills": json.dumps({"name": n, "version": v, "skills": "./skills/"})
    market = lambda n: json.dumps({"name": "m", "plugins": [{"name": n}]})
    return {".claude-plugin/plugin.json": plugin(version_claude), ".claude-plugin/marketplace.json": market("fiction-craft-skills"),
            ".codex-plugin/plugin.json": plugin(version_codex, codex_name), ".agents/plugins/marketplace.json": market("fiction-craft-skills")}


class PluginManifestTests(unittest.TestCase):
    def test_agreeing_manifests_pass(self):
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK}, extra=manifests())
        self.assertEqual(code, 0, out)

    def test_disagreeing_versions_fail(self):
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK}, extra=manifests(version_codex="0.2.0"))
        self.assertEqual(code, 1)
        self.assertIn("versions disagree", out)

    def test_disagreeing_names_fail(self):
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK}, extra=manifests(codex_name="other-name"))
        self.assertEqual(code, 1)
        self.assertIn("names disagree", out)

    def test_a_missing_manifest_fails_when_any_exists(self):
        extra = manifests()
        del extra[".agents/plugins/marketplace.json"]
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK}, extra=extra)
        self.assertEqual(code, 1)
        self.assertIn("manifest missing", out)

    def test_invalid_json_fails(self):
        extra = manifests()
        extra[".claude-plugin/plugin.json"] = "{not json"
        code, out = run({"demo/SKILL.md": GOOD_FRAMEWORK}, extra=extra)
        self.assertEqual(code, 1)
        self.assertIn("not valid JSON", out)


if __name__ == "__main__":
    unittest.main()
