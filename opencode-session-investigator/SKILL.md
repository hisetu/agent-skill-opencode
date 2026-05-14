---
name: opencode-session-investigator
description: Investigate why an OpenCode agent made a mistake by locating relevant sessions in ~/.local/share/opencode, querying opencode.db, reconstructing transcript/tool flow from session/message/part tables, and summarizing root cause. Use when the user asks to inspect OpenCode sessions, analyze agent mistakes, review a ses_xxx conversation, or find what went wrong yesterday.
license: MIT
compatibility: opencode
metadata:
  tech: sqlite3
  type: investigation
---

# OpenCode Session Investigator

Use this skill to diagnose why an OpenCode run went wrong.

This skill is for investigation, not implementation. The goal is to reconstruct what happened from OpenCode session data, identify the wrong turn, and explain the root cause with evidence.

## When to use

Use this skill when the user asks things like:
- `幫我調查 opencode session 為何昨天 ai agent 會做錯`
- `看看 ses_xxx 發生了什麼`
- `幫我找昨天哪個 session 出錯`
- `分析 AI agent 為什麼做錯`
- `review opencode session`

## Core findings to remember

- Start with the official OpenCode CLI when possible.
- Use SQLite only when CLI output/export is not enough for root-cause analysis.
- The real source of truth is usually `~/.local/share/opencode/opencode.db`.
- `~/.local/share/opencode/storage/session/global/*.json` is often only lightweight session metadata, not the full transcript.
- Full conversational evidence is typically reconstructed from SQLite tables:
  - `session`
  - `message`
  - `part`
- `part.data` is usually the most useful place to inspect text/tool flow.

## Investigation workflow

### 1. Find candidate sessions

Start with the official CLI:

```bash
opencode session list
opencode session list --max-count 30
opencode session list --max-count 50 --format json
```

If you already know the session id, jump straight to export:

```bash
opencode export ses_xxx
```

Prefer SQLite over filesystem mtimes.

Use the helper script:

```bash
python3 ~/.config/opencode/skills/opencode-session-investigator/scripts/session_probe.py sessions --date 2026-03-16 --limit 30
```

Or query SQLite directly:

```bash
sqlite3 "$HOME/.local/share/opencode/opencode.db" "
SELECT
  id,
  title,
  directory,
  datetime(time_created/1000,'unixepoch','localtime') AS created_at,
  datetime(time_updated/1000,'unixepoch','localtime') AS updated_at
FROM session
WHERE datetime(time_created/1000,'unixepoch','localtime') LIKE '2026-03-16%'
   OR datetime(time_updated/1000,'unixepoch','localtime') LIKE '2026-03-16%'
ORDER BY time_updated DESC
LIMIT 50;
"
```

Prioritize sessions by:
- title similarity to the reported problem
- matching repo directory
- timeframe proximity
- presence of related subagent sessions

### 2. Inspect session metadata

Try CLI export first:

```bash
opencode export ses_xxx
```

If the exported JSON already contains enough transcript context, use that first.

Then fall back to SQLite/session metadata when needed.

```bash
python3 ~/.config/opencode/skills/opencode-session-investigator/scripts/session_probe.py session ses_xxx
```

Or:

```bash
sqlite3 "$HOME/.local/share/opencode/opencode.db" "
SELECT
  id,
  title,
  directory,
  version,
  datetime(time_created/1000,'unixepoch','localtime') AS created_at,
  datetime(time_updated/1000,'unixepoch','localtime') AS updated_at
FROM session
WHERE id='ses_xxx';
"
```

### 3. Reconstruct message flow

Preferred order:
1. `opencode session list`
2. `opencode export`
3. SQLite `session` / `message` / `part`

Start with messages for timing and roles:

```bash
python3 ~/.config/opencode/skills/opencode-session-investigator/scripts/session_probe.py messages ses_xxx --limit 200
```

Then inspect parts for actual text/tool evidence:

```bash
python3 ~/.config/opencode/skills/opencode-session-investigator/scripts/session_probe.py parts ses_xxx --limit 400
```

Direct SQL fallback:

```bash
sqlite3 "$HOME/.local/share/opencode/opencode.db" "
SELECT
  message_id,
  json_extract(data,'$.type') AS type,
  substr(json_extract(data,'$.text'),1,300) AS text,
  json_extract(data,'$.tool') AS tool
FROM part
WHERE session_id='ses_xxx'
ORDER BY time_created;
"
```

### 4. Identify the actual wrong turn

Look for these patterns:

- **Mode confusion**
  - user asks `為什麼`, `合理嗎`, `幫我分析`
  - agent still edits, commits, pushes, or deploys
- **Evidence overreach**
  - agent claims runtime truth from code-path inspection only
  - no DB row, API response, or log verification
- **Requirement drift**
  - user asks for explanation or comparison
  - agent silently upgrades task into implementation
- **Premature irreversible actions**
  - commit/push/deploy before design is agreed
- **Ignored correction signals**
  - user says `我只是問`, `先不要改`, `只是確認`
  - agent continues execution anyway

### 5. Summarize with evidence

Your final summary should include:
- the most likely problematic `session id`
- why that session was selected
- the exact wrong turn
- 2-5 concrete evidence lines or actions
- whether the failure was:
  - misunderstanding
  - over-eager execution
  - insufficient verification
  - ignored user intent
- prevention suggestions

## Recommended reporting format

Use this structure:

```text
最可能的 session: ses_xxx

為什麼是它:
- ...

錯誤點:
- ...

證據:
- 使用者說了「...」
- agent 接著做了 ...
- 缺少了 ... 驗證

根因:
- ...

下次避免方式:
1. ...
2. ...
3. ...
```

## Important notes

- Official CLI is the first layer; SQLite is the forensic layer.
- `opencode export` is useful for quick review, but may still be less convenient than `part`-level SQLite queries when you need tool-flow evidence.
- Do not trust `storage/session/global/*.json` as the full transcript.
- If filesystem mtimes do not help, switch to SQLite immediately.
- Prefer `part` rows over `message` rows when you need the real conversational evidence.
- If the user says `昨天`, convert it relative to today's local date and query with `localtime`.
- Be explicit about evidence strength:
  - `code suggests`
  - `runtime verified`
  - `likely based on transcript`

## Helper script

This skill includes a deterministic helper script:

```bash
python3 ~/.config/opencode/skills/opencode-session-investigator/scripts/session_probe.py --help
```

Use it first before writing custom SQL.
