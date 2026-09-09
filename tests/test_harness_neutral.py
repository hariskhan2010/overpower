"""overpower must be usable on any agent, not just Claude Code. Guard that:
  - skill bodies don't lean on a Claude-only concept without the neutral framing
  - the multi-harness adapter files exist and point at the skills
  - AGENTS.md / SUPPORT.md name every skill directory
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = sorted((ROOT / "skills").glob("*/SKILL.md"))
SKILL_NAMES = [p.parent.name for p in SKILLS]

# terms that are fine in .claude-plugin/ and the vocabulary table, but in a
# skill BODY must appear alongside the neutral word so a non-Claude agent knows
# what to do. (using-overpower defines the mapping, so it's exempt.)
CLAUDE_ONLY = ["the Skill tool", "the Agent tool", "tool_result block",
               "PostToolUse", "SessionStart hook", "TodoWrite", "TaskCreate"]


class HarnessNeutralTest(unittest.TestCase):
    def test_skills_do_not_lean_on_claude_only_terms(self):
        for p in SKILLS:
            if p.parent.name == "using-overpower":
                continue  # defines the vocabulary
            text = p.read_text(encoding="utf-8")
            for term in CLAUDE_ONLY:
                self.assertNotIn(term, text,
                    f"{p.parent.name}: uses Claude-only '{term}' — use the neutral "
                    f"word (delegate / skills mechanism / guard hook) or annotate it")

    def test_agentid_only_appears_with_a_neutral_alternative(self):
        for p in SKILLS:
            text = p.read_text(encoding="utf-8")
            for m in re.finditer(r"agentId|run id|run=", text):
                window = text[max(0, m.start() - 140): m.end() + 140]
                self.assertTrue(
                    re.search(r"inline|delegat|run artifact|run=<id|concrete|otherwise", window, re.I),
                    f"{p.parent.name}: an 'agentId'/'run id' mention near "
                    f"{text[m.start()-30:m.start()+30]!r} has no inline fallback")

    def test_adapter_files_exist_and_reference_the_skills(self):
        adapters = {
            "AGENTS.md": ROOT / "AGENTS.md",
            "SUPPORT.md": ROOT / "SUPPORT.md",
            ".cursor/rules/overpower.mdc": ROOT / ".cursor" / "rules" / "overpower.mdc",
            ".github/copilot-instructions.md": ROOT / ".github" / "copilot-instructions.md",
        }
        for label, path in adapters.items():
            self.assertTrue(path.exists(), f"missing adapter {label}")
            body = path.read_text(encoding="utf-8")
            self.assertIn("using-overpower", body, f"{label} must route to using-overpower")
            self.assertIn("overpower", body.lower())

    def test_agents_md_and_support_md_list_every_skill(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for name in SKILL_NAMES:
            self.assertIn(name, agents, f"AGENTS.md omits the {name} skill")

    def test_support_matrix_covers_the_major_harnesses(self):
        support = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
        for h in ["Claude Code", "Codex", "Cursor", "Gemini", "Copilot", "Aider"]:
            self.assertIn(h, support, f"SUPPORT.md matrix omits {h}")

    def test_using_overpower_defines_the_vocabulary(self):
        text = (ROOT / "skills" / "using-overpower" / "SKILL.md").read_text(encoding="utf-8")
        for term in ("skills mechanism", "delegate", "guard hook"):
            self.assertIn(term, text, f"using-overpower must define '{term}'")


if __name__ == "__main__":
    unittest.main()
