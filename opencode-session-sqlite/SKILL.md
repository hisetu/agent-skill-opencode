---
name: opencode-session-sqlite
description: >-
  Use SQLite to investigate OpenCode session provenance, find which session most
  likely introduced or reintroduced a file or endpoint change, and speed up
  repeated opencode.db queries with TEMP VIEW / TEMP TABLE patterns. Use when
  the user asks which session made a change, wants faster session forensics, or
  wants reusable SQLite shortcuts for OpenCode history analysis.
license: MIT
compatibility: opencode
metadata:
  tech: sqlite
  type: investigation
---

# OpenCode Session SQLite Investigator

## Purpose

This skill turns the ad hoc SQLite workflow we used during session provenance
investigation into a reusable playbook.

Use it to answer questions like:
- which OpenCode session most likely introduced this file change?
- which session mentioned this endpoint, use case, or path?
- why is this change sitting in the repo now?
- would `TEMP VIEW` or `TEMP TABLE` make this investigation faster?

## When to Use

- user asks `這個變更是哪個 opencode session 改的`
- user asks to trace a file, endpoint, route, or keyword back to a session
- user wants to search `opencode.db` directly with SQLite
- repeated session forensics make raw SQL too repetitive
- user asks whether `view` would speed up the investigation workflow

## Key Rule

Prefer `TEMP VIEW` and `TEMP TABLE`.

- `TEMP VIEW`: best for readability and repeated query authoring
- `TEMP TABLE`: best when you will run many searches in one SQLite session and
  want temporary indexes
- avoid modifying the persistent `opencode.db` schema unless the user explicitly
  wants a maintained long-term forensic setup

## Data Sources

Primary database:

```bash
sqlite3 "$HOME/.local/share/opencode/opencode.db"
```

Main tables used in this workflow:
- `session`
- `message`
- `part`

Most investigation value comes from `part.data` plus session metadata.

## Fast Workflow

### 1. Narrow candidates first

Always reduce the search space before doing broad text scans:
- repo directory
- date range
- likely title keywords
- likely endpoint / file / class / use case names

### 2. Start with TEMP VIEW

Create a flattened temporary view that keeps both extracted fields and raw JSON.
Do not rely only on `$.text`; many useful `tool`, `patch`, and `file` parts keep
the evidence in other JSON fields.

Use the ready-made setup in `references/sql-recipes.md`.

### 3. Use targeted searches

Search in this order:
- exact symbol / filename / endpoint
- related use case or route names
- raw JSON fallback when text extraction misses evidence
- then inspect candidate sessions chronologically

Use the copy-paste queries in `references/sql-recipes.md` for:
- repo session listing
- file / endpoint provenance search
- candidate-session evidence inspection
- whole-session timeline reconstruction
- temporary cached table setup for repeated searches

## When TEMP VIEW Is Enough

Use only `TEMP VIEW` when:
- you are doing one investigation
- candidate sessions are already narrow
- you mainly want shorter, less error-prone SQL

This was the main pain point in the previous investigation: repeated
`json_extract(...)`, repeated timestamp conversion, repeatedly flattening
`part.data`, and forgetting that relevant evidence may live outside `$.text`.

## When to Upgrade to TEMP TABLE

If you will run many text searches in one SQLite session, materialize once and
index it temporarily:

See `references/sql-recipes.md` for the materialized temp-table variant.

Notes:
- this helps repeated filtering by `session_id`, `directory`, and `part_type`
- it does **not** magically optimize `LIKE '%keyword%'` very much
- for true repeated text search acceleration, consider FTS or a dedicated search
  cache only if the user explicitly wants a heavier long-term solution

## Investigation Patterns

### Pattern A: file provenance

Goal: find which session most likely introduced a file change.

Search with:
- exact filename
- route function name
- endpoint path
- related use case names
- DTO/readmodel names
- raw JSON fallback for `patch`, `tool`, or `file` parts

Then separate:
- original design / implementation session
- later stash / restore / rebase session that merely reintroduced the changes

### Pattern B: endpoint provenance

Search with:
- literal endpoint path
- route class name
- use case names
- summary phrases like `remove download endpoint`, `align contract`, `try/catch`
- raw JSON fallback when endpoint evidence is stored outside `$.text`

### Pattern C: why is it in the repo now?

After finding the likely origin session, search for later sessions that mention:
- `git stash`
- `git checkout stash@{...}`
- `restore`
- `rebase`
- `sync develop`

This distinguishes original intent from mechanical restoration.

## Reporting Format

When you answer the user, separate confidence levels clearly:

```text
最可能的原始需求 session: ses_xxx
目前變更重新出現在 worktree 的 session: ses_yyy

為什麼:
- ...

直接證據:
- ...

信心:
- 高 / 中 / 低
```

## Practical Guidance

- prefer exact symbols before fuzzy natural-language phrases
- search file path + endpoint + use case together when possible
- treat matching mtimes as supporting evidence, not primary proof
- transcript snippets beat assumptions
- if SQL becomes repetitive, upgrade from raw query to `TEMP VIEW`
- if the same investigation repeats often in one sitting, upgrade to
  `TEMP TABLE` with temporary indexes
- phrase conclusions as `most likely` unless transcript evidence is explicit

## Reference

For copy-paste query templates, see:
- `references/sql-recipes.md`
