"""Every skill must have valid, minimal frontmatter and a body. Guards the
class of bug that hit obra/superpowers #2233 (a stray `Triggers on:` line made
the frontmatter invalid YAML and the skill silently failed to register).
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
FM = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


class SkillsLintTest(unittest.TestCase):
    def skills(self):
        return sorted(SKILLS.glob("*/SKILL.md"))

    def test_there_are_skills(self):
        self.assertGreaterEqual(len(self.skills()), 10)

    def test_router_lists_every_skill(self):
        """using-overpower's skill table must stay in sync with skills/ ."""
        router = (SKILLS / "using-overpower" / "SKILL.md").read_text(encoding="utf-8")
        for name in (p.parent.name for p in self.skills()):
            self.assertIn(f"`{name}`", router,
                          f"using-overpower does not list the `{name}` skill")

    def test_frontmatter_is_valid_and_minimal(self):
        for skill in self.skills():
            text = skill.read_text(encoding="utf-8")
            m = FM.match(text)
            self.assertIsNotNone(m, f"{skill}: no `---` frontmatter block at the top")
            front, body = m.group(1), m.group(2)

            keys = {}
            for line in front.splitlines():
                self.assertRegex(
                    line, r"^[a-z_]+:\s.+$",
                    f"{skill}: frontmatter line is not `key: value` -> {line!r} "
                    f"(this is exactly superpowers #2233)",
                )
                k, v = line.split(":", 1)
                keys[k.strip()] = v.strip()

            self.assertEqual(set(keys), {"name", "description"},
                             f"{skill}: frontmatter keys must be exactly name + description")
            self.assertEqual(keys["name"], skill.parent.name,
                             f"{skill}: frontmatter name must match the directory name")
            self.assertGreaterEqual(len(keys["description"]), 30,
                                    f"{skill}: description too short to be a useful trigger")
            self.assertTrue(body.strip().startswith("#"),
                            f"{skill}: body should open with a heading")

    def test_referenced_skills_exist_or_are_listed_as_todo(self):
        """using-overpower names other skills; each must exist or be in the
        CHANGELOG 'Not yet' list so a reference is never a dead end silently."""
        have = {p.parent.name for p in self.skills()}
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        router = (SKILLS / "using-overpower" / "SKILL.md").read_text(encoding="utf-8")
        for name in re.findall(r"`([a-z][a-z-]+)`", router):
            if "-" not in name:
                continue
            if name in have:
                continue
            self.assertIn(name, changelog,
                          f"using-overpower references `{name}` but it neither "
                          f"exists nor is listed as planned in CHANGELOG.md")


if __name__ == "__main__":
    unittest.main()
