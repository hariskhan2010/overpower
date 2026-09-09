"""designing-architecture makes specific promises the README relies on:
diagrams, an element spec with Where/Look/Does, and colour from the project's
tokens (not invented). Guard them so an edit can't quietly drop one.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "skills" / "designing-architecture" / "SKILL.md").read_text(encoding="utf-8")


class ArchitectureSkillTest(unittest.TestCase):
    def test_writes_the_artifact_to_overpower(self):
        self.assertIn(".overpower/architecture.md", SKILL)

    def test_requires_diagrams(self):
        self.assertIn("```mermaid", SKILL, "must show a mermaid diagram in the template")
        self.assertGreaterEqual(SKILL.count("```mermaid"), 2,
                                "component map + at least one more diagram")
        self.assertIn("wireframe", SKILL.lower(), "layout wireframe for UI features")

    def test_element_spec_has_where_look_does(self):
        for col in ("Where", "Look", "Does", "Data"):
            self.assertIn(col, SKILL, f"element spec table must have a {col!r} column")

    def test_colour_comes_from_the_project_tokens(self):
        low = SKILL.lower()
        self.assertIn("token", low)
        self.assertTrue(
            ("design system" in low) and ("proposed" in low),
            "must look for the project's design system and mark invented colours as proposed",
        )

    def test_has_interactive_states(self):
        low = SKILL.lower()
        for s in ("idle", "pending", "error"):
            self.assertIn(s, low, f"states table should cover {s!r}")

    def test_plan_and_implementer_reference_it(self):
        plan = (ROOT / "skills" / "writing-plans" / "SKILL.md").read_text(encoding="utf-8")
        impl = (ROOT / "agents" / "op-implementer.md").read_text(encoding="utf-8")
        self.assertIn("architecture.md", plan)
        self.assertIn("Design:", plan, "task template needs a Design line")
        self.assertIn("architecture.md", impl)


if __name__ == "__main__":
    unittest.main()
