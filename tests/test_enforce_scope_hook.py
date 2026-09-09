"""The PostToolUse scope hook must:
  - be a strict no-op when there's no active .overpower/progress.md
  - block an Edit/Write that lands outside the worktree during a live build
  - allow edits inside the worktree and inside .overpower/
  - never crash on malformed input
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "hooks" / "enforce_scope.py"


def run(event: dict):
    r = subprocess.run([sys.executable, str(HOOK)],
                       input=json.dumps(event), capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


class EnforceScopeHookTest(unittest.TestCase):
    def _project_with_build(self, tmp):
        """A project dir with a worktree sibling and an .overpower/progress.md."""
        project = Path(tmp) / "repo"
        worktree = Path(tmp) / "repo-feature"
        (project / ".overpower").mkdir(parents=True)
        worktree.mkdir()
        (project / ".overpower" / "progress.md").write_text(
            "# feature\n\n## Log\n- 2026-09-09 worktree ../repo-feature on feat/x; baseline: 0/0\n",
            encoding="utf-8")
        return project, worktree

    def test_noop_without_a_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "repo"
            project.mkdir()
            rc, out = run({"tool_name": "Edit", "cwd": str(project),
                           "tool_input": {"file_path": str(project / "src" / "a.py")}})
            self.assertEqual(rc, 0)
            self.assertEqual(out, "", "no .overpower/progress.md -> hook says nothing")

    def test_blocks_edit_outside_the_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            project, worktree = self._project_with_build(tmp)
            stray = project / "src" / "main.py"   # in the MAIN checkout, not the worktree
            rc, out = run({"tool_name": "Write", "cwd": str(project),
                           "tool_input": {"file_path": str(stray)}})
            self.assertEqual(rc, 0)
            doc = json.loads(out)
            self.assertEqual(doc["decision"], "block")
            self.assertIn("scope breach", doc["reason"])
            self.assertIn(str(worktree), doc["reason"])

    def test_allows_edit_inside_the_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            project, worktree = self._project_with_build(tmp)
            good = worktree / "src" / "main.py"
            rc, out = run({"tool_name": "Edit", "cwd": str(project),
                           "tool_input": {"file_path": str(good)}})
            self.assertEqual(out, "", "edit inside the worktree is allowed silently")

    def test_allows_overpower_state_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            project, _ = self._project_with_build(tmp)
            rc, out = run({"tool_name": "Edit", "cwd": str(project),
                           "tool_input": {"file_path": str(project / ".overpower" / "progress.md")}})
            self.assertEqual(out, "", "the orchestrator updating progress.md is fine")

    def test_ignores_non_edit_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            project, _ = self._project_with_build(tmp)
            rc, out = run({"tool_name": "Bash", "cwd": str(project),
                           "tool_input": {"command": "rm -rf /"}})
            self.assertEqual(out, "", "this hook only inspects Edit/Write/MultiEdit")

    def test_survives_garbage_input(self):
        r = subprocess.run([sys.executable, str(HOOK)], input="not json{",
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
