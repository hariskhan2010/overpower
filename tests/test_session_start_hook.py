"""The session-start hook must emit exactly one clean JSON object on stdout —
no BOM, pure ASCII — in whichever shape the running harness consumes, and must
degrade to empty output (never a crash) if the skill file is missing.
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "hooks" / "session_start.py"


class SessionStartHookTest(unittest.TestCase):
    def _run(self, env_extra=None):
        env = {k: v for k, v in os.environ.items()
               if not k.startswith(("CURSOR_", "CLAUDE_PLUGIN_ROOT", "COPILOT_CLI"))}
        env.update(env_extra or {})
        return subprocess.run([sys.executable, str(HOOK)], capture_output=True,
                              cwd=ROOT, env=env)

    def _ctx(self, doc):
        if "hookSpecificOutput" in doc:
            return doc["hookSpecificOutput"]["additionalContext"]
        return doc.get("additionalContext") or doc.get("additional_context")

    def test_default_shape_is_top_level_additionalContext(self):
        r = self._run()
        self.assertEqual(r.returncode, 0)
        self.assertFalse(r.stdout.startswith(b"\xef\xbb\xbf"), "no UTF-8 BOM")
        doc = json.loads(r.stdout.decode("utf-8"))
        self.assertIn("additionalContext", doc)
        ctx = self._ctx(doc)
        self.assertIn("Using overpower", ctx)
        self.assertIn("classify the task", ctx)
        self.assertIn(".overpower/progress.md", ctx)

    def test_claude_code_shape(self):
        doc = json.loads(self._run({"CLAUDE_PLUGIN_ROOT": str(ROOT)}).stdout.decode())
        self.assertEqual(doc["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("Using overpower", self._ctx(doc))

    def test_cursor_shape_is_snake_case(self):
        doc = json.loads(self._run({"CURSOR_TRACE_ID": "x"}).stdout.decode())
        self.assertIn("additional_context", doc)
        self.assertIn("Using overpower", doc["additional_context"])

    def test_copilot_does_not_get_the_claude_shape(self):
        doc = json.loads(self._run({"CLAUDE_PLUGIN_ROOT": str(ROOT), "COPILOT_CLI": "1"}).stdout.decode())
        self.assertNotIn("hookSpecificOutput", doc)
        self.assertIn("additionalContext", doc)

    def test_stdout_is_pure_ascii(self):
        self._run().stdout.decode("ascii")

    def test_missing_skill_file_degrades_to_nothing(self):
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as d:
            fake = Path(d) / "hooks"
            fake.mkdir()
            shutil.copy(HOOK, fake / "session_start.py")
            r = subprocess.run([sys.executable, str(fake / "session_start.py")], capture_output=True)
            self.assertEqual(r.returncode, 0)
            self.assertEqual(r.stdout.strip(), b"")


if __name__ == "__main__":
    unittest.main()
