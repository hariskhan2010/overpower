"""The SessionStart hook must emit exactly one clean JSON object on stdout —
no BOM, no stray prints — and must degrade to empty output (never a crash)
if the skill file is missing. Claude Code reads this stdout directly.
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "hooks" / "session_start.py"


class SessionStartHookTest(unittest.TestCase):
    def _run(self, cwd=None):
        return subprocess.run([sys.executable, str(HOOK)], capture_output=True,
                              cwd=cwd or ROOT)

    def test_emits_one_clean_json_object(self):
        r = self._run()
        self.assertEqual(r.returncode, 0)
        raw = r.stdout
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"), "no UTF-8 BOM")
        doc = json.loads(raw.decode("utf-8"))  # single object, parses
        hso = doc["hookSpecificOutput"]
        self.assertEqual(hso["hookEventName"], "SessionStart")
        ctx = hso["additionalContext"]
        self.assertIn("Using overpower", ctx, "the skill body is injected")
        self.assertIn("classify the task", ctx)
        self.assertIn(".overpower/progress.md", ctx, "compaction-recovery note present")

    def test_stdout_is_pure_ascii(self):
        # json.dumps(ensure_ascii=True) keeps the arrows/emoji in the skill as
        # \uXXXX, so a cp1252 Windows console can never mangle the hook output.
        r = self._run()
        r.stdout.decode("ascii")  # raises if not pure ASCII

    def test_missing_skill_file_degrades_to_nothing(self):
        # Run a copy of the hook from a dir with no skills/ tree.
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as d:
            fake = Path(d) / "hooks"
            fake.mkdir()
            shutil.copy(HOOK, fake / "session_start.py")
            r = subprocess.run([sys.executable, str(fake / "session_start.py")],
                               capture_output=True)
            self.assertEqual(r.returncode, 0, "must not crash")
            self.assertEqual(r.stdout.strip(), b"", "no skill file -> no output")


if __name__ == "__main__":
    unittest.main()
