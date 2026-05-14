---
name: opencode-plugin
description: >-
  OpenCode Plugin 系統指南。當需要了解 OpenCode 的擴展機制、建立 plugin、
  設定 event listener、攔截工具執行時使用此 skill。觸發詞：opencode plugin、
  建立 plugin、plugin system、擴展 opencode、tool intercept。
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: extensibility
---

# OpenCode Plugin 系統指南

OpenCode 提供完整的 Plugin 系統，讓你可以擴展和自動化 AI 編程助手的行為。

## 六種擴展機制

| 機制 | 複雜度 | 彈性 | 最適用途 |
|------|--------|------|----------|
| **Plugin System** | 高 | 非常高 | 自訂邏輯、事件 hooks、驗證 |
| **SDK/API** | 中 | 非常高 | 完整程式化控制、整合 |
| **MCP Servers** | 中 | 高 | 外部工具、第三方協定 |
| **GitHub Integration** | 低 | 中 | PR/Issue 工作流程 |
| **Custom Commands** | 低 | 低 | 可重用提示詞、簡單自動化 |
| **Non-Interactive** | 低 | 中 | CI/CD、腳本、批次處理 |

---

## 1. Plugin System（最強大）

Plugin 是 JavaScript/TypeScript 檔案，可以攔截事件和工具執行。

### 目錄結構

```
.opencode/
├── plugins/
│   ├── my-plugin.ts      # 專案層級 plugin
│   └── another-plugin.ts
└── opencode.json         # 設定檔
```

或全域：
```
~/.config/opencode/
├── plugins/
│   └── global-plugin.ts  # 全域 plugin
└── opencode.json
```

### Plugin 基本結構

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({ app, client, $ }) => {
  // app: OpenCode 應用程式實例
  // client: API 客戶端
  // $: 執行 shell 命令的工具（類似 zx）

  return {
    // 工具執行 hooks
    tool: {
      execute: {
        before: async (input, output) => {
          // 在工具執行前觸發
          // 可以拋出錯誤來阻止執行
        },
        after: async (input, output) => {
          // 在工具執行後觸發
        }
      }
    },

    // 事件 hooks
    event: async ({ event }) => {
      // 監聽所有 OpenCode 事件
      console.log("Event:", event.type)
    }
  }
}
```

### 範例：保護敏感檔案

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export const EnvProtection: Plugin = async ({ client }) => {
  const sensitivePatterns = ['.env', 'secret', 'credentials', 'private-key']

  return {
    tool: {
      execute: {
        before: async (input, output) => {
          if (input.tool === "read") {
            const filePath = output.args.filePath.toLowerCase()
            
            if (sensitivePatterns.some(p => filePath.includes(p))) {
              throw new Error(`Cannot read sensitive file: ${output.args.filePath}`)
            }
          }
        }
      }
    }
  }
}
```

### 範例：編輯後自動格式化

```typescript
export const AutoFormat: Plugin = async ({ $ }) => {
  return {
    tool: {
      execute: {
        after: async (input, output) => {
          if (input.tool === "edit") {
            await $`prettier --write ${output.args.filePath}`
            console.log("Code formatted!")
          }
        }
      }
    }
  }
}
```

### 範例：Slack 通知

```typescript
export const SlackNotifier: Plugin = async () => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.idle") {
        await fetch(process.env.SLACK_WEBHOOK_URL!, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            text: `OpenCode session completed!`,
            blocks: [{
              type: "section",
              text: {
                type: "mrkdwn",
                text: `*Session ID:* ${event.properties.sessionId}`
              }
            }]
          })
        })
      }
    }
  }
}
```

### Plugin 設定（opencode.json）

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": {
    "my-plugin": {
      "enabled": true
    },
    "env-protection": {
      "enabled": true
    }
  }
}
```

### 安裝 Plugin 類型

```bash
npm install @opencode-ai/plugin
```

---

## 2. SDK with Event Streaming

SDK 讓你從外部應用程式控制 OpenCode，使用 SSE 即時串流事件。

### 啟動 OpenCode Server

```bash
opencode serve --port 4096
```

### 安裝 SDK

```bash
npm install @opencode-ai/sdk
```

### 基本使用

```typescript
import { createOpencodeClient } from "@opencode-ai/sdk"

const client = createOpencodeClient({
  baseUrl: "http://localhost:4096"
})

// 訂閱所有事件
const eventStream = await client.event.subscribe()

for await (const event of eventStream) {
  console.log("Event:", event.type)

  if (event.type === "session.idle") {
    await sendNotification("Session completed!")
  }
}
```

### 自動化 Code Review

```typescript
async function autoReview() {
  const client = createOpencodeClient({
    baseUrl: "http://localhost:4096"
  })

  // 建立新 session
  const session = await client.session.create({
    title: "Automated Code Review"
  })

  // 取得修改的檔案
  const files = await client.file.status()
  const modifiedFiles = files.filter(f => f.status === "modified")

  // Review 每個檔案
  for (const file of modifiedFiles) {
    const content = await client.file.read({ path: file.path })

    await client.session.chat({
      id: session.id,
      providerID: "anthropic",
      modelID: "claude-sonnet-4-20250514",
      parts: [{
        type: "text",
        text: `Review this file for code quality issues:\n\n${content}`
      }]
    })
  }

  // 分享 review
  const shared = await client.session.share({ id: session.id })
  console.log("Review URL:", shared.shareUrl)
}
```

---

## 3. MCP Servers

MCP (Model Context Protocol) servers 讓你添加外部工具和能力。

### 設定 MCP Server（opencode.json）

```json
{
  "mcp": {
    "database-query": {
      "type": "local",
      "command": ["node", "./mcp-servers/database.js"],
      "enabled": true
    },
    "company-docs": {
      "type": "remote",
      "url": "https://docs.mycompany.com/mcp",
      "enabled": true,
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### 熱門 MCP Servers

- **Context7** - 文件搜尋
- **Playwright** - 瀏覽器自動化
- **Bright Data** - 網頁爬蟲
- **Appwrite** - 後端服務

---

## 4. GitHub Integration

自動回應 GitHub Issues 和 PRs。

### 安裝

```bash
opencode github install
```

### 使用方式

在 GitHub Issue 或 PR 中留言：
- `/opencode explain this issue`
- `/opencode fix this bug`
- `/opencode review these changes`

### 手動 Workflow 設定

```yaml
name: opencode
on:
  issue_comment:
    types: [created]

jobs:
  opencode:
    if: contains(github.event.comment.body, '/opencode')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: sst/opencode/github@latest
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        with:
          model: anthropic/claude-sonnet-4-20250514
```

---

## 5. Custom Commands

自訂命令是儲存為 Markdown 檔案的可重用提示詞。

### 建立命令

`.opencode/command/test.md`:
```markdown
---
description: "Run tests with coverage"
---
Run the full test suite with coverage:
`!npm test -- --coverage`

Analyze the results and suggest improvements.
```

### 使用命令

在 OpenCode 中輸入 `/test`

### 帶參數的命令

```markdown
---
description: Test a specific component
---
Run tests for the $COMPONENT component:
`!npm test -- $COMPONENT.test.ts`
```

使用：`/test Button`

---

## 6. Non-Interactive Mode

腳本化 OpenCode 用於自動化。

```bash
# 執行命令並取得 JSON 輸出
opencode run "analyze code quality" -f json -q

# 繼續之前的 session
opencode run "implement the fixes" -c session-id

# 用於 pre-commit hook
opencode run "review my changes" -q
```

---

## 設定優先順序

OpenCode 按以下順序尋找設定：

1. `OPENCODE_CONFIG` 環境變數
2. `./opencode.json`（專案目錄）
3. `~/.config/opencode/opencode.json`（全域）

---

## 常見事件類型

| 事件 | 說明 |
|------|------|
| `session.created` | Session 建立 |
| `session.idle` | Session 完成/閒置 |
| `tool.execute.start` | 工具開始執行 |
| `tool.execute.end` | 工具執行完成 |
| `file.read` | 檔案被讀取 |
| `file.write` | 檔案被寫入 |

---

## 參考資源

- **Plugins 文件**: https://opencode.ai/docs/plugins/
- **SDK 文件**: https://opencode.ai/docs/sdk/
- **MCP Servers**: https://opencode.ai/docs/mcp-servers/
- **GitHub Integration**: https://opencode.ai/docs/github/
- **Commands**: https://opencode.ai/docs/commands/
- **Configuration**: https://opencode.ai/docs/config/
- **GitHub Repository**: https://github.com/sst/opencode
