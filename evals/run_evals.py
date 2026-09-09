#!/usr/bin/env python3
"""overpower skill-eval harness.

The lint tests check the skill *files* are valid. This checks the skills
*work*: it puts a skill in front of a model with a realistic scenario and
asserts the response follows the rule.

Each case (evals/cases/*.json):

    {
      "name": "tier-typo",
      "skills": ["using-overpower"],          # skill bodies prepended to the prompt
      "scenario": "The user says: ...",        # the situation to react to
      "checks": [
        {"present_any": ["T0", "trivial"], "why": "classifies as low tier"},
        {"absent_all": ["writing-plans", "progress.md"], "why": "no ceremony"}
      ],
      "rubric": "optional — a judge model scores the response pass/fail"
    }

Runs each scenario through `claude -p --restricted --tools ""` (no tools, no
project settings, clean temp cwd), then applies the checks. `--rubric` also
runs the judge pass. Results go to evals/results/ (git-ignored).

Requires the `claude` CLI on PATH (it is, if you're reading this in Claude Code).
No API key needed — it uses your logged-in session. stdlib only.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

CLAUDE = shutil.which("claude")

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
CASES = Path(__file__).resolve().parent / "cases"
RESULTS = Path(__file__).resolve().parent / "results"

EVAL_SYSTEM = (
    "You are being evaluated on how you would respond to a user, with the skill "
    "instructions below in effect. Do not use any tools. Reply with exactly the "
    "message you would send the user and the concrete steps you would take — no "
    "meta commentary about being evaluated."
)

JUDGE_SYSTEM = (
    "You are a strict evaluator. You are given a rubric and a response. Reply on "
    "one line: 'PASS' if the response satisfies the rubric, or 'FAIL: <reason>' "
    "if it does not. Nothing else."
)


def load_skills(names):
    out = []
    for n in names:
        p = SKILLS / n / "SKILL.md"
        if not p.exists():
            raise SystemExit(f"case references unknown skill: {n}")
        out.append(f"===== SKILL: {n} =====\n{p.read_text(encoding='utf-8')}")
    return "\n\n".join(out)


def claude(prompt, system, model, timeout=300):
    if not CLAUDE:
        return None, "claude CLI not found on PATH"
    # Prompt goes on stdin (not argv) so a multi-skill prompt can't hit the
    # Windows command-line length limit or a quoting edge.
    cmd = [
        CLAUDE, "-p",
        "--restricted", "--tools", "", "--strict-mcp-config",
        "--no-session-persistence", "--output-format", "json",
        "--append-system-prompt", system,
    ]
    if model:
        cmd += ["--model", model]
    with tempfile.TemporaryDirectory() as cwd:
        try:
            r = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                               cwd=cwd, timeout=timeout, encoding="utf-8")
        except subprocess.TimeoutExpired:
            return None, f"claude timed out after {timeout}s"
    if r.returncode != 0:
        return None, f"claude exited {r.returncode}: {(r.stderr or r.stdout)[:400]}"
    try:
        doc = json.loads(r.stdout)
        return doc.get("result", ""), None
    except json.JSONDecodeError:
        return (r.stdout or "").strip(), None


def apply_checks(response, checks):
    results = []
    hay = response.lower()
    for c in checks:
        why = c.get("why", "")
        if "present_any" in c:
            pats = c["present_any"]
            hit = next((p for p in pats if re.search(p.lower(), hay)), None)
            results.append((bool(hit), f"present_any {pats} — {why}"
                            + (f"  [matched: {hit!r}]" if hit else "  [none matched]")))
        elif "absent_all" in c:
            pats = c["absent_all"]
            bad = [p for p in pats if re.search(p.lower(), hay)]
            results.append((not bad, f"absent_all {pats} — {why}"
                            + (f"  [present: {bad!r}]" if bad else "")))
        elif "regex" in c:
            ok = bool(re.search(c["regex"], response, re.I | re.M))
            results.append((ok, f"regex {c['regex']!r} — {why}"))
        else:
            results.append((False, f"unknown check shape: {c}"))
    return results


def run_case(path, model, judge):
    case = json.loads(path.read_text(encoding="utf-8"))
    prompt = (load_skills(case["skills"])
              + "\n\n===== SCENARIO =====\n" + case["scenario"]
              + "\n\nRespond now.")
    t0 = time.time()
    response, err = claude(prompt, EVAL_SYSTEM, model)
    dt = time.time() - t0
    if err:
        return {"name": case["name"], "error": err, "seconds": round(dt, 1)}

    checks = apply_checks(response, case.get("checks", []))
    verdicts = [ok for ok, _ in checks]

    judged = None
    if judge and case.get("rubric"):
        jprompt = (f"RUBRIC:\n{case['rubric']}\n\nRESPONSE:\n{response}")
        jout, jerr = claude(jprompt, JUDGE_SYSTEM, model)
        judged = jerr or (jout or "").strip().splitlines()[0] if (jout or jerr) else "no judge output"
        verdicts.append(judged.startswith("PASS"))

    return {
        "name": case["name"],
        "passed": all(verdicts),
        "checks": [{"ok": ok, "desc": d} for ok, d in checks],
        "judge": judged,
        "seconds": round(dt, 1),
        "response": response,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cases", nargs="*", help="case names (default: all)")
    ap.add_argument("--model", default="", help="model alias (default: session default)")
    ap.add_argument("--rubric", action="store_true", help="also run the judge pass")
    ap.add_argument("--quiet", action="store_true", help="only the summary + failures")
    args = ap.parse_args()

    paths = sorted(CASES.glob("*.json"))
    if args.cases:
        want = set(args.cases)
        paths = [p for p in paths if p.stem in want or p.name in want]
    if not paths:
        raise SystemExit("no cases found")

    RESULTS.mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    out = []
    npass = 0
    for p in paths:
        res = run_case(p, args.model, args.rubric)
        out.append(res)
        ok = res.get("passed", False)
        npass += ok
        mark = "PASS" if ok else ("ERR " if "error" in res else "FAIL")
        print(f"[{mark}] {res['name']}  ({res.get('seconds','?')}s)")
        if not ok and not args.quiet:
            if "error" in res:
                print(f"       {res['error']}")
            for c in res.get("checks", []):
                if not c["ok"]:
                    print(f"       ✗ {c['desc']}")
            if res.get("judge"):
                print(f"       judge: {res['judge']}")

    (RESULTS / f"{stamp}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\n{npass}/{len(paths)} passed   →  evals/results/{stamp}.json")
    sys.exit(0 if npass == len(paths) else 1)


if __name__ == "__main__":
    main()
