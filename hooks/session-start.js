// SessionStart hook: load the using-overpower router into every session so the
// agent knows which overpower skill fits before it starts acting.
// Node only (cross-platform). Never fails the session.
//
// Output shape differs per harness:
//   Cursor (CURSOR_PLUGIN_ROOT)             → { additional_context }
//   Claude Code (CLAUDE_PLUGIN_ROOT, not Copilot/Muse) → { hookSpecificOutput: { hookEventName, additionalContext } }
//   Copilot CLI, Muse, anything else        → { additionalContext }   (SDK standard)
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const env = process.env;
const root = env.CURSOR_PLUGIN_ROOT || env.CLAUDE_PLUGIN_ROOT || env.MUSE_PLUGIN_ROOT
  || join(dirname(fileURLToPath(import.meta.url)), '..');

let body;
try {
  body = readFileSync(join(root, 'skills', 'using-overpower', 'SKILL.md'), 'utf8')
    .replace(/^---[\s\S]*?---\s*/, '');
} catch { process.exit(0); }

const context = '<overpower>\nYou have overpower. Its router skill is below; load the other overpower skills as its tool map says.\n\n'
  + body + '\n</overpower>';

let out;
if (env.CURSOR_PLUGIN_ROOT) out = { additional_context: context };
else if (env.CLAUDE_PLUGIN_ROOT && !env.COPILOT_CLI && !env.MUSE_PLUGIN_ROOT)
  out = { hookSpecificOutput: { hookEventName: 'SessionStart', additionalContext: context } };
else out = { additionalContext: context };

process.stdout.write(JSON.stringify(out));
