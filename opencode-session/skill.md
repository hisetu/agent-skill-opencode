---
name: opencode-session
description: 快速查找和讀取 OpenCode session 檔案。當需要繼續之前的工作、查看 session 歷史、或讀取特定 session 內容時使用此 skill。觸發詞：session、繼續工作、之前的對話、ses_xxx。
---

# OpenCode Session 工具

快速查找和讀取 OpenCode session 檔案。

## Session 檔案位置

OpenCode session 檔案儲存在以下位置：

```
~/.local/share/opencode/storage/
├── session/global/          # Session JSON 檔案
│   └── ses_xxxxx.json
├── session_diff/            # Session diff 檔案
│   └── ses_xxxxx.json
└── todo/                    # Todo 檔案
    └── ses_xxxxx.json
```

## 快速指令

### 1. 列出最近的 sessions（按修改時間排序）

```bash
ls -lt ~/.local/share/opencode/storage/session/global/*.json | head -10
```

### 2. 根據 session ID 片段查找

```bash
# 用 session ID 片段查找（例如 ses_3fd4）
find ~/.local/share/opencode/storage -name "*ses_3fd4*" -type f 2>/dev/null
```

### 3. 查看 session 基本資訊

```bash
# 取得 session 的標題和時間
SESSION_FILE="$HOME/.local/share/opencode/storage/session/global/ses_xxxxx.json"
jq '{title: .title, createdAt: .createdAt, updatedAt: .updatedAt}' "$SESSION_FILE"
```

### 4. 列出 session 的對話摘要

```bash
# 列出所有訊息的角色和前 100 字
SESSION_FILE="$HOME/.local/share/opencode/storage/session/global/ses_xxxxx.json"
jq -r '.messages[] | "\(.role): \(.content[0:100])..."' "$SESSION_FILE"
```

### 5. 匯出 session 為 Markdown

```bash
SESSION_FILE="$HOME/.local/share/opencode/storage/session/global/ses_xxxxx.json"
OUTPUT_FILE="/tmp/session_export.md"

jq -r '
  "# " + .title + "\n\n" +
  "**Session ID:** " + .id + "\n" +
  "**Created:** " + .createdAt + "\n" +
  "**Updated:** " + .updatedAt + "\n\n---\n\n" +
  (.messages | map(
    "## " + (if .role == "user" then "User" else "Assistant" end) + "\n\n" + .content + "\n\n---\n"
  ) | join("\n"))
' "$SESSION_FILE" > "$OUTPUT_FILE"

echo "已匯出到：$OUTPUT_FILE"
```

## 搜尋 Session 內容

### 根據關鍵字搜尋 sessions

```bash
# 搜尋包含特定關鍵字的 session
grep -l "關鍵字" ~/.local/share/opencode/storage/session/global/*.json
```

### 搜尋並顯示上下文

```bash
# 搜尋並顯示匹配行
grep -r "關鍵字" ~/.local/share/opencode/storage/session/global/ --include="*.json" | head -20
```

## 完整腳本：Session 瀏覽器

```bash
#!/bin/bash
# opencode-session.sh - OpenCode Session 瀏覽器

SESSION_DIR="$HOME/.local/share/opencode/storage/session/global"

case "$1" in
  list|ls)
    # 列出最近 10 個 sessions
    echo "=== 最近的 Sessions ==="
    for f in $(ls -t "$SESSION_DIR"/*.json 2>/dev/null | head -10); do
      id=$(basename "$f" .json)
      title=$(jq -r '.title // "無標題"' "$f" 2>/dev/null | head -c 50)
      updated=$(jq -r '.updatedAt // "?"' "$f" 2>/dev/null)
      echo "$id | $updated | $title"
    done
    ;;
    
  find)
    # 根據 ID 片段查找
    if [ -z "$2" ]; then
      echo "Usage: $0 find <session_id_fragment>"
      exit 1
    fi
    find "$SESSION_DIR" -name "*$2*" -type f
    ;;
    
  show)
    # 顯示 session 內容
    if [ -z "$2" ]; then
      echo "Usage: $0 show <session_id>"
      exit 1
    fi
    SESSION_FILE="$SESSION_DIR/$2.json"
    if [ ! -f "$SESSION_FILE" ]; then
      # 嘗試模糊匹配
      SESSION_FILE=$(find "$SESSION_DIR" -name "*$2*" -type f | head -1)
    fi
    if [ -f "$SESSION_FILE" ]; then
      jq -r '
        "# " + (.title // "無標題") + "\n" +
        "Session: " + .id + "\n" +
        "Updated: " + .updatedAt + "\n\n" +
        "---\n\n" +
        (.messages | map(
          "### " + .role + "\n" + (.content[0:500]) + "\n"
        ) | join("\n---\n"))
      ' "$SESSION_FILE"
    else
      echo "找不到 session: $2"
    fi
    ;;
    
  search)
    # 搜尋關鍵字
    if [ -z "$2" ]; then
      echo "Usage: $0 search <keyword>"
      exit 1
    fi
    echo "=== 搜尋結果：$2 ==="
    grep -l "$2" "$SESSION_DIR"/*.json 2>/dev/null | while read f; do
      id=$(basename "$f" .json)
      title=$(jq -r '.title // "無標題"' "$f" 2>/dev/null | head -c 40)
      echo "$id | $title"
    done
    ;;
    
  export)
    # 匯出為 Markdown
    if [ -z "$2" ]; then
      echo "Usage: $0 export <session_id> [output_file]"
      exit 1
    fi
    SESSION_FILE="$SESSION_DIR/$2.json"
    if [ ! -f "$SESSION_FILE" ]; then
      SESSION_FILE=$(find "$SESSION_DIR" -name "*$2*" -type f | head -1)
    fi
    OUTPUT="${3:-/tmp/session_$2.md}"
    if [ -f "$SESSION_FILE" ]; then
      jq -r '
        "# " + (.title // "無標題") + "\n\n" +
        "**Session ID:** " + .id + "\n" +
        "**Created:** " + .createdAt + "\n" +
        "**Updated:** " + .updatedAt + "\n\n---\n\n" +
        (.messages | map(
          "## " + (if .role == "user" then "User" else "Assistant" end) + "\n\n" + .content + "\n\n---\n"
        ) | join("\n"))
      ' "$SESSION_FILE" > "$OUTPUT"
      echo "已匯出到：$OUTPUT"
    else
      echo "找不到 session: $2"
    fi
    ;;
    
  *)
    echo "OpenCode Session 瀏覽器"
    echo ""
    echo "Usage: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  list, ls              列出最近的 sessions"
    echo "  find <id_fragment>    根據 ID 片段查找 session"
    echo "  show <session_id>     顯示 session 內容摘要"
    echo "  search <keyword>      搜尋包含關鍵字的 sessions"
    echo "  export <id> [file]    匯出 session 為 Markdown"
    ;;
esac
```

## 常見用法

### 繼續之前的工作

1. 列出最近的 sessions：
   ```bash
   ls -lt ~/.local/share/opencode/storage/session/global/*.json | head -5
   ```

2. 查看 session 標題：
   ```bash
   jq -r '.title' ~/.local/share/opencode/storage/session/global/ses_xxxxx.json
   ```

3. 匯出為 Markdown 後讀取內容

### 用 session ID 片段查找

如果你只記得 session ID 的一部分（例如 `ses_3fd4`）：

```bash
# 查找檔案
find ~/.local/share/opencode/storage -name "*ses_3fd4*" -type f

# 或直接用 glob
ls ~/.local/share/opencode/storage/session/global/ses_3fd4*.json
```

## 注意事項

1. Session 檔案可能很大，直接讀取 JSON 可能不易閱讀
2. 建議先用 jq 擷取需要的部分
3. 匯出為 Markdown 後更容易閱讀和繼續工作
4. Session 檔案包含完整對話歷史，可能佔用大量空間
