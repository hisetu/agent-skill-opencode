---
name: opencode-session-cleaner
description: >-
  清理 OpenCode session 中的 compaction（壓縮）訊息，恢復完整對話歷史。
  Compaction 會讓 AI agent 失憶，此工具可移除壓縮摘要並保留原始對話。
  當使用者提到「清理 session」、「刪除 compaction」、「session 壓縮」、
  「agent 失憶」、「清理壓縮訊息」、「clean compaction」、
  「remove compaction」、「session cleaner」時使用此 skill。
license: MIT
compatibility: opencode
---

# OpenCode Session Compaction Cleaner

清理 OpenCode session 中的 compaction（壓縮）訊息，避免 AI agent 因壓縮摘要而失憶。

## 問題背景

OpenCode 會自動對過長的對話進行 compaction（壓縮），將原始對話替換為摘要。
這會導致 AI agent 失去原始上下文的細節，產生「失憶」現象。

## 使用方式

### 方式一：使用腳本（推薦）

```bash
# 1. 先預覽會刪除什麼（安全）
python3 scripts/clean_compaction.py <session_id> --dry-run

# 2. 備份後清理（推薦）
python3 scripts/clean_compaction.py <session_id> --backup

# 3. 只刪除 compaction 訊息本身（保留之後的對話）
python3 scripts/clean_compaction.py <session_id> --mode compaction-only --backup
```

### 方式二：手動 SQL

```bash
DB=~/.local/share/opencode/opencode.db
SESSION_ID="ses_xxxxxxxx"

# 1. 備份
cp "$DB" "$DB.bak-$(date +%Y%m%d-%H%M%S)"

# 2. 查看 compaction 訊息
sqlite3 "$DB" "
SELECT m.id, m.time_created, json_extract(m.data, '$.mode')
FROM message m
WHERE m.session_id = '$SESSION_ID'
  AND json_extract(m.data, '$.mode') = 'compaction'
ORDER BY m.time_created;"

# 3. 找出第一條 compaction 的 time_created
FIRST_COMPACTION_TIME=$(sqlite3 "$DB" "
SELECT MIN(m.time_created) FROM message m
WHERE m.session_id = '$SESSION_ID'
  AND json_extract(m.data, '$.mode') = 'compaction';")

# 4. 刪除 parts（先刪，因為 FK）
sqlite3 "$DB" "
DELETE FROM part
WHERE session_id = '$SESSION_ID'
  AND message_id IN (
    SELECT id FROM message
    WHERE session_id = '$SESSION_ID'
      AND time_created >= $FIRST_COMPACTION_TIME
  );"

# 5. 刪除 messages
sqlite3 "$DB" "
DELETE FROM message
WHERE session_id = '$SESSION_ID'
  AND time_created >= $FIRST_COMPACTION_TIME;"

# 6. 也刪除 compaction 觸發的 user 訊息（part type = 'compaction'）
sqlite3 "$DB" "
DELETE FROM part WHERE session_id = '$SESSION_ID'
  AND message_id IN (
    SELECT DISTINCT m.id FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE m.session_id = '$SESSION_ID'
      AND json_extract(p.data, '$.type') = 'compaction'
  );
DELETE FROM message WHERE session_id = '$SESSION_ID'
  AND id IN (
    SELECT DISTINCT m.id FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE m.session_id = '$SESSION_ID'
      AND json_extract(p.data, '$.type') = 'compaction'
  );"
```

## 清理模式

| 模式 | 說明 |
|------|------|
| `compaction-and-after` | 刪除第一條 compaction 及之後所有訊息（預設，最乾淨） |
| `compaction-only` | 只刪除 compaction 訊息本身，保留之後的對話 |

## 如何找到 Session ID

```bash
# 列出最近的 sessions
sqlite3 ~/.local/share/opencode/opencode.db "
SELECT id, title, slug, datetime(time_created/1000, 'unixepoch', 'localtime') as created
FROM session ORDER BY time_created DESC LIMIT 10;"

# 用標題搜尋
sqlite3 ~/.local/share/opencode/opencode.db "
SELECT id, title FROM session WHERE title LIKE '%關鍵字%';"
```

## DB 結構速查

| Table | Key Columns | Notes |
|-------|-------------|-------|
| `session` | id, title, slug, directory | Session 本體 |
| `message` | id, session_id, time_created, data (JSON) | data 含 role, mode, text |
| `part` | id, message_id, session_id, data (JSON) | data 含 type (text/tool/compaction) |

- `part` 有 FK 到 `message`，刪除順序：**先 parts → 再 messages**
- Compaction 識別：`json_extract(data, '$.mode') = 'compaction'` 或 `json_extract(data, '$.type') = 'compaction'`

## 注意事項

- **務必先備份**：`cp ~/.local/share/opencode/opencode.db ~/.local/share/opencode/opencode.db.bak`
- 刪除後無法復原（除非有備份）
- 建議先用 `--dry-run` 預覽
- 清理後重新打開 session，AI 就能看到完整原始對話
