---
name: opencode-extension-search
description: 搜尋 OpenCode 現成可用的 extensions（plugins、MCP servers、themes、commands 等）。當使用者需要尋找 OpenCode 擴展、plugin、MCP server 或想知道有什麼現成工具可用時使用此 skill。
---

# OpenCode Extension Search

搜尋和推薦 OpenCode 現成可用的 extensions，包含 plugins、MCP servers、themes、slash commands、hooks 等。

## 觸發時機

當使用者詢問：
- 「有沒有 XXX 的 plugin？」
- 「找一個可以做 XXX 的 extension」
- 「OpenCode 有什麼現成的 XXX 工具？」
- 「推薦 OpenCode plugin」
- 「搜尋 opencode extension」

## Extension 類型

opencode.cafe 支援以下 extension 類型：

| 類型 | 說明 |
|------|------|
| `plugin` | 通用 plugin，可攔截事件和工具執行 |
| `mcp-server` | Model Context Protocol server，AI 整合 |
| `slash-command` | 自訂 `/` 命令 |
| `hook` | 生命週期 hooks，用於自動化 |
| `theme` | 視覺主題和配色 |
| `tool` | 獨立工具和實用程式 |
| `web-view` | 自訂 Web UI 面板 |
| `fork` | OpenCode 的修改版本 |

## 資料來源（按信任度排序）

### Tier 1 - 官方來源（優先搜尋）

| 來源 | URL | 說明 |
|------|-----|------|
| OpenCode Ecosystem | https://opencode.ai/docs/ecosystem | 官方維護的 plugin/project 列表 |
| OpenCode Docs | https://opencode.ai/docs/plugins | 官方 plugin 文件和範例 |

### Tier 2 - 社群精選

| 來源 | URL | 說明 |
|------|-----|------|
| opencode.cafe | https://www.opencode.cafe/ | 社群 marketplace |
| awesome-opencode | https://github.com/awesome-opencode/awesome-opencode | 社群精選列表 |

### Tier 3 - npm / GitHub 搜尋

| 來源 | URL | 說明 |
|------|-----|------|
| npm search | https://www.npmjs.com/search?q=opencode | 搜尋 opencode 相關套件 |
| GitHub search | https://github.com/search?q=opencode+plugin | GitHub 搜尋 |

## 搜尋流程

### Step 1: 解析使用者需求

從使用者描述中提取：
- 核心功能關鍵字（如：notification、auth、format）
- 擴展類型（plugin、MCP server、theme、command）
- 特殊需求（如：支援特定服務、特定語言）

### Step 2: 搜尋官方 Ecosystem

**首先使用 WebFetch 抓取官方列表：**

```
WebFetch: https://opencode.ai/docs/ecosystem
```

從頁面中提取所有 plugins 和 projects，比對使用者需求。

### Step 3: 搜尋 opencode.cafe（GitHub 原始碼）

由於 opencode.cafe 使用 Convex 動態渲染，WebFetch 無法直接抓取。
可透過其 GitHub repo 了解資料結構：

```
GitHub: https://github.com/R44VC0RP/opencode.cafe
Schema: https://raw.githubusercontent.com/R44VC0RP/opencode.cafe/main/convex/schema.ts
```

**opencode.cafe 資料結構：**
```typescript
{
  productId: string,        // 唯一識別碼
  type: "plugin" | "mcp-server" | "slash-command" | "hook" | "theme" | "tool" | "web-view" | "fork",
  displayName: string,      // 顯示名稱
  description: string,      // 簡短描述
  repoUrl: string,          // GitHub URL
  tags: string[],           // 標籤
  installation: string,     // 安裝說明 (markdown)
  status: "pending" | "approved" | "rejected"
}
```

### Step 4: 搜尋 awesome-opencode

```
WebFetch: https://github.com/awesome-opencode/awesome-opencode
```

### Step 5: 搜尋 npm（如果需要更多結果）

```
WebFetch: https://www.npmjs.com/search?q=opencode-{keyword}
```

### Step 6: 整理結果

## 已知的熱門 Plugins 快速參考

### 認證類
| Plugin | 說明 | GitHub |
|--------|------|--------|
| opencode-openai-codex-auth | 使用 ChatGPT Plus/Pro 訂閱 | [GitHub](https://github.com/numman-ali/opencode-openai-codex-auth) |
| opencode-gemini-auth | 使用現有 Gemini 方案 | [GitHub](https://github.com/jenslys/opencode-gemini-auth) |
| opencode-antigravity-auth | 使用 Antigravity 免費模型 | [GitHub](https://github.com/NoeFabris/opencode-antigravity-auth) |
| opencode-google-antigravity-auth | Google Antigravity OAuth | [GitHub](https://github.com/shekohex/opencode-google-antigravity-auth) |

### 通知類
| Plugin | 說明 | GitHub |
|--------|------|--------|
| opencode-notificator | 桌面通知和音效 | [GitHub](https://github.com/panta82/opencode-notificator) |
| opencode-notifier | 權限/完成/錯誤通知 | [GitHub](https://github.com/mohak34/opencode-notifier) |
| opencode-notify | 原生 OS 通知 | [GitHub](https://github.com/kdcokenny/opencode-notify) |

### 效能優化類
| Plugin | 說明 | GitHub |
|--------|------|--------|
| opencode-dynamic-context-pruning | 裁剪過時 tool output | [GitHub](https://github.com/Tarquinen/opencode-dynamic-context-pruning) |
| opencode-morph-fast-apply | 10x 更快的程式碼編輯 | [GitHub](https://github.com/JRedeker/opencode-morph-fast-apply) |

### 開發輔助類
| Plugin | 說明 | GitHub |
|--------|------|--------|
| opencode-type-inject | 自動注入 TypeScript 類型 | [GitHub](https://github.com/nick-vi/opencode-type-inject) |
| opencode-shell-strategy | 防止 TTY hang | [GitHub](https://github.com/JRedeker/opencode-shell-strategy) |
| opencode-pty | PTY 背景程序支援 | [GitHub](https://github.com/shekohex/opencode-pty.git) |
| opencode-md-table-formatter | 清理 markdown 表格 | [GitHub](https://github.com/franlol/opencode-md-table-formatter) |
| opencode-wakatime | Wakatime 時間追蹤 | [GitHub](https://github.com/angristan/opencode-wakatime) |
| opencode-helicone-session | Helicone session headers | [GitHub](https://github.com/H2Shami/opencode-helicone-session) |
| opencode-websearch-cited | 網頁搜尋（含引用） | [GitHub](https://github.com/ghoulr/opencode-websearch-cited.git) |

### 多 Agent / 進階工作流
| Plugin | 說明 | GitHub |
|--------|------|--------|
| opencode-background-agents | 背景 agents | [GitHub](https://github.com/kdcokenny/opencode-background-agents) |
| opencode-workspace | 多 agent 編排（16 元件） | [GitHub](https://github.com/kdcokenny/opencode-workspace) |
| oh-my-opencode | 背景 agents + LSP/AST/MCP | [GitHub](https://github.com/code-yeongyu/oh-my-opencode) |
| @openspoon/subtask2 | 強大的編排系統 | [GitHub](https://github.com/spoons-and-mirrors/subtask2) |
| micode | Brainstorm → Plan → Implement | [GitHub](https://github.com/vtemian/micode) |

### Git / 開發環境
| Plugin | 說明 | GitHub |
|--------|------|--------|
| opencode-devcontainers | 多分支 devcontainer 隔離 | [GitHub](https://github.com/athal7/opencode-devcontainers) |
| opencode-worktree | 零摩擦 git worktrees | [GitHub](https://github.com/kdcokenny/opencode-worktree) |
| opencode-zellij-namer | AI 自動命名 Zellij session | [GitHub](https://github.com/24601/opencode-zellij-namer) |

### 其他實用
| Plugin | 說明 | GitHub |
|--------|------|--------|
| opencode-scheduler | cron 排程任務 | [GitHub](https://github.com/different-ai/opencode-scheduler) |
| opencode-supermemory | 跨 session 持久記憶 | [GitHub](https://github.com/supermemoryai/opencode-supermemory) |
| opencode-skillful | 按需載入 prompts | [GitHub](https://github.com/zenobi-us/opencode-skillful) |
| @plannotator/opencode | 視覺化 plan review | [GitHub](https://github.com/backnotprop/plannotator) |

## 相關 Projects（非 Plugin）

| Project | 說明 | GitHub |
|---------|------|--------|
| kimaki | Discord bot 控制 OpenCode | [GitHub](https://github.com/remorses/kimaki) |
| opencode.nvim | Neovim 整合 | [GitHub](https://github.com/NickvanDyke/opencode.nvim) |
| portal | Mobile-first Web UI | [GitHub](https://github.com/hosenur/portal) |
| OpenChamber | Web/Desktop/VSCode Extension | [GitHub](https://github.com/btriapitsyn/openchamber) |
| OpenCode-Obsidian | Obsidian 整合 | [GitHub](https://github.com/mtymek/opencode-obsidian) |
| OpenWork | Claude Cowork 替代方案 | [GitHub](https://github.com/different-ai/openwork) |
| ocx | Extension manager | [GitHub](https://github.com/kdcokenny/ocx) |
| CodeNomad | 跨平台 Client App | [GitHub](https://github.com/NeuralNomadsAI/CodeNomad) |

## 輸出格式

```markdown
## 找到 X 個相關 Extensions

### 推薦（官方/高信任度）

1. **[plugin-name](github-url)**
   - 類型：plugin
   - 功能：xxx
   - 來源：OpenCode Ecosystem（官方）
   - 安裝：`"plugin": ["plugin-name"]`

### 值得考慮

2. **[plugin-name](github-url)**
   - 類型：mcp-server
   - 功能：xxx
   - 來源：opencode.cafe
   - Stars: xxx | 最後更新: xxx

### 安裝方式

在 `opencode.json` 中加入：
```json
{
  "plugin": ["plugin-name-1", "plugin-name-2"]
}
```
```

## 注意事項

1. **優先推薦官方 Ecosystem 列表中的 plugin** - 這些經過社群驗證
2. **opencode.cafe 使用 Convex 動態渲染** - WebFetch 無法直接抓取內容，但可參考 GitHub repo 了解結構
3. **檢查 GitHub stars 和最後更新時間** - 避免推薦已棄用的專案
4. **如果找不到合適的** - 誠實告知使用者，建議參考官方 plugin 範例自行建立
5. **安全提醒** - 提醒使用者檢查 plugin 原始碼，特別是涉及認證的 plugin

## 延伸資源

- 官方 Plugin 文件：https://opencode.ai/docs/plugins
- 官方 MCP Servers：https://opencode.ai/docs/mcp-servers
- 官方 Custom Tools：https://opencode.ai/docs/custom-tools
- opencode.cafe：https://www.opencode.cafe/
- opencode.cafe GitHub：https://github.com/R44VC0RP/opencode.cafe
- awesome-opencode：https://github.com/awesome-opencode/awesome-opencode
