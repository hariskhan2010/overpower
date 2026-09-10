"""The plugin's manifest, commands, agents, and hooks must be structurally
valid — a malformed one makes Claude Code drop the piece silently.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FM = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


class PluginManifestTest(unittest.TestCase):
    def test_plugin_json_is_valid(self):
        p = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        for k in ("name", "description", "version"):
            self.assertIn(k, p)
        self.assertEqual(p["name"], "overpower")

    def test_manifest_version_matches_changelog(self):
        """The manifest version must match the newest CHANGELOG heading —
        otherwise Claude Code installs a version the release notes don't describe.
        """
        p = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        latest = re.search(r"^##\s*\[([0-9]+\.[0-9]+\.[0-9]+)\]", changelog, re.M)
        self.assertIsNotNone(latest, "no versioned heading in CHANGELOG.md")
        self.assertEqual(p["version"], latest.group(1),
                         "plugin.json version drifted from the newest CHANGELOG entry")

    def test_marketplace_json_matches_plugin(self):
        m = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        p = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        names = [e["name"] for e in m["plugins"]]
        self.assertIn(p["name"], names)
        for e in m["plugins"]:
            if e["name"] == p["name"]:
                self.assertEqual(e["version"], p["version"],
                                 "marketplace.json version drifted from plugin.json")

    def test_hooks_json_is_valid_and_scripts_exist(self):
        h = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        for event, entries in h["hooks"].items():
            for entry in entries:
                for hook in entry["hooks"]:
                    self.assertEqual(hook["type"], "command")
                    m = re.search(r"run-hook\.cmd\"?\s+(\S+)", hook["command"])
                    self.assertIsNotNone(m, f"{event}: can't find the script name in {hook['command']!r}")
                    script = ROOT / "hooks" / m.group(1)
                    self.assertTrue(script.exists(), f"{event} references missing {script}")

    def test_commands_have_frontmatter(self):
        cmds = sorted((ROOT / "commands").glob("*.md"))
        self.assertGreaterEqual(len(cmds), 3)
        for c in cmds:
            m = FM.match(c.read_text(encoding="utf-8"))
            self.assertIsNotNone(m, f"{c.name}: no frontmatter")
            self.assertIn("description:", m.group(1), f"{c.name}: no description")
            self.assertTrue(m.group(2).strip(), f"{c.name}: empty body")

    def test_agents_have_frontmatter(self):
        agents = sorted((ROOT / "agents").glob("*.md"))
        self.assertGreaterEqual(len(agents), 2)
        for a in agents:
            m = FM.match(a.read_text(encoding="utf-8"))
            self.assertIsNotNone(m, f"{a.name}: no frontmatter")
            front = m.group(1)
            for k in ("name:", "description:"):
                self.assertIn(k, front, f"{a.name}: missing {k}")
            name = re.search(r"^name:\s*(\S+)", front, re.M).group(1)
            self.assertEqual(name, a.stem, f"{a.name}: frontmatter name must match filename")

    def test_autonomous_skill_references_real_agents(self):
        skill = (ROOT / "skills" / "autonomous-execution" / "SKILL.md").read_text(encoding="utf-8")
        agents = {a.stem for a in (ROOT / "agents").glob("*.md")}
        for ref in ("op-implementer", "op-reviewer"):
            self.assertIn(ref, skill)
            self.assertIn(ref, agents, f"autonomous-execution names `{ref}` but agents/{ref}.md is missing")


if __name__ == "__main__":
    unittest.main()
