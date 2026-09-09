"""Eval case files must be valid and self-consistent, so a broken case can't
masquerade as a skill failure when `run_evals.py` runs.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "evals" / "cases"
SKILLS = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}


class EvalCasesLintTest(unittest.TestCase):
    def cases(self):
        return sorted(CASES.glob("*.json"))

    def test_there_are_cases(self):
        self.assertGreaterEqual(len(self.cases()), 8)

    def test_each_case_is_valid(self):
        for p in self.cases():
            with self.subTest(case=p.name):
                case = json.loads(p.read_text(encoding="utf-8"))
                self.assertEqual(case["name"], p.stem,
                                 "case name must match the filename")
                self.assertTrue(case["scenario"].strip(), "scenario is empty")
                self.assertTrue(case["skills"], "no skills listed")
                for s in case["skills"]:
                    self.assertIn(s, SKILLS, f"case references unknown skill {s!r}")
                self.assertTrue(case.get("checks") or case.get("rubric"),
                                "a case needs at least one check or a rubric")
                for c in case.get("checks", []):
                    self.assertTrue(
                        {"present_any", "absent_all", "regex"} & set(c),
                        f"check has no recognized shape: {c}")
                    self.assertTrue(c.get("why"), f"check missing 'why': {c}")

    def test_runner_covers_every_check_shape(self):
        runner = (ROOT / "evals" / "run_evals.py").read_text(encoding="utf-8")
        shapes = set()
        for p in self.cases():
            for c in json.loads(p.read_text(encoding="utf-8")).get("checks", []):
                shapes |= {"present_any", "absent_all", "regex"} & set(c)
        for shape in shapes:
            self.assertIn(f'"{shape}"', runner,
                          f"cases use check shape {shape!r} but run_evals.py doesn't handle it")

    def test_runner_forces_utf8_output(self):
        """Skill text / model responses carry arrows and em-dashes; the runner
        must not crash on a cp1252 console or a non-UTF-8 pipe."""
        runner = (ROOT / "evals" / "run_evals.py").read_text(encoding="utf-8")
        self.assertIn('reconfigure(encoding="utf-8"', runner)


if __name__ == "__main__":
    unittest.main()
