#!/bin/bash
# opencode-session.sh - OpenCode Session 瀏覽器
# 安裝：chmod +x ~/.config/opencode/skills/opencode-session/opencode-session.sh
# 建議：ln -s ~/.config/opencode/skills/opencode-session/opencode-session.sh ~/bin/oc-session

SESSION_DIR="$HOME/.local/share/opencode/storage/session/global"

case "$1" in
  list|ls)
    # 列出最近 N 個 sessions（預設 10）
    COUNT="${2:-10}"
    echo "=== 最近的 Sessions ==="
    printf "%-35s | %-20s | %s\n" "Session ID" "Updated" "Title"
    echo "-----------------------------------+----------------------+------------------"
    for f in $(ls -t "$SESSION_DIR"/*.json 2>/dev/null | head -"$COUNT"); do
      id=$(basename "$f" .json)
      title=$(jq -r '.title // "無標題"' "$f" 2>/dev/null | head -c 40)
      updated=$(jq -r '.updatedAt // "?"' "$f" 2>/dev/null | cut -d'T' -f1,2 | tr 'T' ' ' | cut -c1-16)
      printf "%-35s | %-20s | %s\n" "$id" "$updated" "$title"
    done
    ;;
    
  find)
    # 根據 ID 片段查找
    if [ -z "$2" ]; then
      echo "Usage: $0 find <session_id_fragment>"
      echo "Example: $0 find ses_3fd4"
      exit 1
    fi
    echo "=== 搜尋 Session ID: *$2* ==="
    find "$HOME/.local/share/opencode/storage" -name "*$2*" -type f 2>/dev/null | while read f; do
      echo "$f"
    done
    ;;
    
  show)
    # 顯示 session 內容摘要
    if [ -z "$2" ]; then
      echo "Usage: $0 show <session_id>"
      exit 1
    fi
    
    # 嘗試找到 session 檔案
    if [ -f "$SESSION_DIR/$2.json" ]; then
      SESSION_FILE="$SESSION_DIR/$2.json"
    else
      SESSION_FILE=$(find "$SESSION_DIR" -name "*$2*" -type f 2>/dev/null | head -1)
    fi
    
    if [ -f "$SESSION_FILE" ]; then
      echo "=== Session 資訊 ==="
      jq -r '
        "Title: " + (.title // "無標題") + "\n" +
        "ID: " + .id + "\n" +
        "Created: " + .createdAt + "\n" +
        "Updated: " + .updatedAt + "\n" +
        "Messages: " + (.messages | length | tostring)
      ' "$SESSION_FILE"
      echo ""
      echo "=== 對話摘要 ==="
      jq -r '.messages[] | "[\(.role)] " + (.content[0:200] | gsub("\n"; " ")) + "..."' "$SESSION_FILE" | head -20
    else
      echo "找不到 session: $2"
      echo "提示：使用 '$0 find $2' 搜尋"
    fi
    ;;
    
  search)
    # 搜尋關鍵字
    if [ -z "$2" ]; then
      echo "Usage: $0 search <keyword>"
      exit 1
    fi
    echo "=== 搜尋關鍵字：$2 ==="
    grep -l "$2" "$SESSION_DIR"/*.json 2>/dev/null | while read f; do
      id=$(basename "$f" .json)
      title=$(jq -r '.title // "無標題"' "$f" 2>/dev/null | head -c 50)
      updated=$(jq -r '.updatedAt // "?"' "$f" 2>/dev/null | cut -d'T' -f1)
      echo "$id | $updated | $title"
    done
    ;;
    
  export)
    # 匯出為 Markdown
    if [ -z "$2" ]; then
      echo "Usage: $0 export <session_id> [output_file]"
      exit 1
    fi
    
    # 嘗試找到 session 檔案
    if [ -f "$SESSION_DIR/$2.json" ]; then
      SESSION_FILE="$SESSION_DIR/$2.json"
    else
      SESSION_FILE=$(find "$SESSION_DIR" -name "*$2*" -type f 2>/dev/null | head -1)
    fi
    
    OUTPUT="${3:-$HOME/session-$2.md}"
    
    if [ -f "$SESSION_FILE" ]; then
      jq -r '
        "# " + (.title // "無標題") + "\n\n" +
        "**Session ID:** " + .id + "\n" +
        "**Created:** " + .createdAt + "\n" +
        "**Updated:** " + .updatedAt + "\n\n---\n\n" +
        (.messages | to_entries | map(
          "## " + (if .value.role == "user" then "User" else "Assistant" end) + " (#" + (.key + 1 | tostring) + ")\n\n" + .value.content + "\n\n---\n"
        ) | join("\n"))
      ' "$SESSION_FILE" > "$OUTPUT"
      echo "已匯出到：$OUTPUT"
      echo "檔案大小：$(du -h "$OUTPUT" | cut -f1)"
    else
      echo "找不到 session: $2"
    fi
    ;;
    
  path)
    # 顯示 session 目錄路徑
    echo "$SESSION_DIR"
    ;;
    
  *)
    echo "OpenCode Session 瀏覽器"
    echo ""
    echo "Usage: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  list, ls [n]          列出最近的 n 個 sessions（預設 10）"
    echo "  find <id_fragment>    根據 ID 片段查找 session"
    echo "  show <session_id>     顯示 session 資訊和對話摘要"
    echo "  search <keyword>      搜尋包含關鍵字的 sessions"
    echo "  export <id> [file]    匯出 session 為 Markdown"
    echo "  path                  顯示 session 目錄路徑"
    echo ""
    echo "Examples:"
    echo "  $0 list 5             列出最近 5 個 sessions"
    echo "  $0 find ses_3fd4      查找 ID 包含 'ses_3fd4' 的 session"
    echo "  $0 show ses_3fd4      顯示 session 摘要"
    echo "  $0 export ses_3fd4    匯出為 ~/session-ses_3fd4.md"
    ;;
esac
