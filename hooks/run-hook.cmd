: << 'CMDBLOCK'
@echo off
REM Polyglot launcher for overpower hook scripts (Claude Code, Windows + Unix).
REM
REM On Windows cmd.exe runs this batch half and finds a Python interpreter.
REM On Unix the shell treats the leading ": << 'CMDBLOCK'" as a no-op heredoc
REM and runs the sh half below.
REM
REM Hook scripts are Python so JSON is built by json.dumps, not by hand — the
REM manual-escaping and bash-heredoc bugs that hit obra/superpowers
REM (issues #571, and the Windows path bug #2105) do not apply.
REM
REM Usage: run-hook.cmd <script-name.py> [args...]
setlocal
if "%~1"=="" ( echo run-hook.cmd: missing script name >&2 & exit /b 1 )
set "HOOK_DIR=%~dp0"
set "SCRIPT=%HOOK_DIR%%~1"
shift
for %%P in (python.exe python3.exe py.exe) do (
  where %%P >nul 2>nul && ( %%P "%SCRIPT%" %1 %2 %3 %4 %5 %6 %7 %8 %9 & exit /b %ERRORLEVEL% )
)
REM No Python found: skip the injection, plugin still works via the Skill tool.
exit /b 0
CMDBLOCK

# --- Unix ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_NAME="$1"; shift
for PY in python3 python; do
  if command -v "$PY" >/dev/null 2>&1; then
    exec "$PY" "${SCRIPT_DIR}/${SCRIPT_NAME}" "$@"
  fi
done
exit 0
