---
name: opencode-ecosystem
description: >-
  OpenCode 生態系統資源指南，包含社群 plugins、projects 和 agents。
  當使用者詢問 OpenCode 的擴展功能、推薦 plugin、找尋第三方整合、
  或想了解有哪些社群專案時使用此 skill。觸發詞：opencode plugin、
  ecosystem、extension、integration、community projects。
license: MIT
compatibility: opencode
metadata:
  audience: developers
---

# OpenCode Ecosystem

OpenCode 生態系統的社群資源總覽，包含 plugins、projects 和 agents。

## 資源連結

- [awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) - 精選資源列表
- [opencode.cafe](https://opencode.cafe) - 社群聚合網站

---

## Plugins

| 名稱 | 說明 |
|------|------|
| [opencode-helicone-session](https://github.com/H2Shami/opencode-helicone-session) | 自動注入 Helicone session headers |
| [opencode-type-inject](https://github.com/nick-vi/opencode-type-inject) | 自動注入 TypeScript/Svelte 類型到檔案讀取 |
| [opencode-openai-codex-auth](https://github.com/numman-ali/opencode-openai-codex-auth) | 使用 ChatGPT Plus/Pro 訂閱而非 API credits |
| [opencode-gemini-auth](https://github.com/jenslys/opencode-gemini-auth) | 使用現有 Gemini 方案而非 API 計費 |
| [opencode-antigravity-auth](https://github.com/NoeFabris/opencode-antigravity-auth) | 使用 Antigravity 免費模型 |
| [opencode-devcontainers](https://github.com/athal7/opencode-devcontainers) | 多分支 devcontainer 隔離 |
| [opencode-google-antigravity-auth](https://github.com/shekohex/opencode-google-antigravity-auth) | Google Antigravity OAuth 支援 |
| [opencode-dynamic-context-pruning](https://github.com/Tarquinen/opencode-dynamic-context-pruning) | 修剪過時 tool outputs 以優化 token 使用 |
| [opencode-websearch-cited](https://github.com/ghoulr/opencode-websearch-cited.git) | 支援 Google grounded 風格的原生網頁搜尋 |
| [opencode-pty](https://github.com/shekohex/opencode-pty.git) | 讓 AI agents 在 PTY 中執行背景程序 |
| [opencode-shell-strategy](https://github.com/JRedeker/opencode-shell-strategy) | 非互動式 shell 指令說明，防止 TTY 操作卡住 |
| [opencode-wakatime](https://github.com/angristan/opencode-wakatime) | 使用 Wakatime 追蹤 OpenCode 使用情況 |
| [opencode-md-table-formatter](https://github.com/franlol/opencode-md-table-formatter/tree/main) | 清理 LLM 產生的 markdown 表格 |
| [opencode-morph-fast-apply](https://github.com/JRedeker/opencode-morph-fast-apply) | 使用 Morph Fast Apply API 加速 10 倍程式碼編輯 |
| [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) | 背景 agents、預建 LSP/AST/MCP 工具、精選 agents |
| [opencode-notificator](https://github.com/panta82/opencode-notificator) | OpenCode 桌面通知與音效提示 |
| [opencode-notifier](https://github.com/mohak34/opencode-notifier) | 權限、完成、錯誤事件的桌面通知 |
| [opencode-zellij-namer](https://github.com/24601/opencode-zellij-namer) | AI 驅動的自動 Zellij session 命名 |
| [opencode-skillful](https://github.com/zenobi-us/opencode-skillful) | 讓 agents 按需載入 prompts |
| [opencode-supermemory](https://github.com/supermemoryai/opencode-supermemory) | 跨 session 持久記憶 |
| [@plannotator/opencode](https://github.com/backnotprop/plannotator/tree/main/apps/opencode-plugin) | 互動式計劃審閱與視覺化標註 |
| [@openspoon/subtask2](https://github.com/spoons-and-mirrors/subtask2) | 擴展 /commands 為強大的編排系統 |
| [opencode-scheduler](https://github.com/different-ai/opencode-scheduler) | 使用 cron 語法排程定期任務 |
| [micode](https://github.com/vtemian/micode) | 結構化 Brainstorm → Plan → Implement 工作流程 |
| [octto](https://github.com/vtemian/octto) | AI brainstorming 互動式瀏覽器 UI |
| [opencode-background-agents](https://github.com/kdcokenny/opencode-background-agents) | Claude Code 風格的背景 agents |
| [opencode-notify](https://github.com/kdcokenny/opencode-notify) | 原生 OS 通知 |
| [opencode-workspace](https://github.com/kdcokenny/opencode-workspace) | 打包的多 agent 編排工具 - 16 個組件一次安裝 |
| [opencode-worktree](https://github.com/kdcokenny/opencode-worktree) | 零摩擦的 git worktrees |

---

## Projects

| 名稱 | 說明 |
|------|------|
| [kimaki](https://github.com/remorses/kimaki) | Discord bot 控制 OpenCode sessions |
| [opencode.nvim](https://github.com/NickvanDyke/opencode.nvim) | Neovim plugin，基於 API 的編輯器感知提示 |
| [portal](https://github.com/hosenur/portal) | Mobile-first web UI via Tailscale/VPN |
| [opencode plugin template](https://github.com/zenobi-us/opencode-plugin-template/) | OpenCode plugins 開發模板 |
| [opencode.nvim (sudo-tee)](https://github.com/sudo-tee/opencode.nvim) | Neovim 前端 for opencode |
| [ai-sdk-provider-opencode-sdk](https://github.com/ben-vargas/ai-sdk-provider-opencode-sdk) | Vercel AI SDK provider for OpenCode |
| [OpenChamber](https://github.com/btriapitsyn/openchamber) | Web/Desktop App 和 VS Code Extension |
| [OpenCode-Obsidian](https://github.com/mtymek/opencode-obsidian) | 在 Obsidian UI 中嵌入 OpenCode |
| [OpenWork](https://github.com/different-ai/openwork) | Claude Cowork 開源替代方案 |
| [ocx](https://github.com/kdcokenny/ocx) | OpenCode extension manager |
| [CodeNomad](https://github.com/NeuralNomadsAI/CodeNomad) | Desktop、Web、Mobile 和 Remote Client App |

---

## Agents

| 名稱 | 說明 |
|------|------|
| [Agentic](https://github.com/Cluster444/agentic) | 模組化 AI agents 和結構化開發命令 |
| [opencode-agents](https://github.com/darrenhinde/opencode-agents) | Configs、prompts、agents 和 plugins 增強工作流程 |

---

## 使用情境

- 想找特定功能的 plugin（如通知、記憶、認證）
- 需要第三方工具整合（如 Neovim、Obsidian、Discord）
- 尋找多 agent 編排或背景執行解決方案
- 建立 OpenCode plugin 需要參考模板
- 探索社群專案獲取靈感

## 貢獻

如要將你的 OpenCode 相關專案加入列表，請到 [OpenCode GitHub](https://github.com/anomalyco/opencode) 提交 PR。
