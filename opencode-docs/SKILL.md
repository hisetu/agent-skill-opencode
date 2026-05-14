---
name: opencode-docs
description: Retrieve and explain OpenCode documentation. Use when the user asks about OpenCode features, configuration, commands, providers, agents, skills, MCP servers, rules, TUI usage, or any OpenCode-related questions.
license: MIT
metadata:
  author: opencode-community
  version: "2.0"
  source: https://github.com/anomalyco/opencode/tree/dev/packages/web/src/content/docs
---

# OpenCode Docs (Execution-Focused)

Use this skill to answer OpenCode questions quickly with correct commands, file paths, and minimal working config examples.

If the user writes in Chinese, respond in Traditional Chinese.

## When to Use

Activate when the user asks about:

- Installing/running OpenCode (TUI, CLI, web, IDE)
- `opencode.json` configuration, precedence, permissions
- Providers and authentication (`/connect`, env vars, OAuth)
- Agents and subagents (modes, tools, permissions)
- Custom commands (`.opencode/commands`, placeholders)
- Skills (`SKILL.md` format, discovery, permissions)
- MCP servers (local/remote, OAuth)
- Rules files (`AGENTS.md`, precedence, `instructions`)
- Tools and custom tools
- Plugins system
- Models and modes
- Keybinds and TUI shortcuts
- LSP integration, themes, formatters
- GitHub/GitLab integration
- Network, enterprise, troubleshooting
- Sharing sessions, ACP, SDK

## How to Use This Skill

1. Identify the user's intent (setup, troubleshoot, how-to, best practice).
2. Pick the smallest relevant reference file (do not read everything).
3. Produce an answer with:
   - exact command(s) to run
   - exact file path(s) to edit/create
   - a minimal, correct example snippet
   - 1-2 verification steps

## References Index

### Core Configuration

| File | Topics | Key Content |
|------|--------|-------------|
| `references/CONFIG.md` | 設定檔、優先順序、schema | 設定檔位置、優先順序、完整 JSON schema、theme/model/provider/tui/server 設定 |
| `references/PROVIDERS.md` | Provider、認證、API Key | OpenCode Zen、Anthropic、OpenAI、AWS Bedrock、Google、Azure、xAI、Ollama、OAuth |
| `references/PERMISSIONS.md` | 權限系統、allow/ask/deny | 權限操作(read/edit/bash等)、細粒度規則、glob 模式、per-agent 權限覆蓋 |
| `references/MODELS.md` | 模型選擇、切換 | 可用模型列表、`/models` 命令、opencode.json 中的 model 設定 |
| `references/RULES.md` | AGENTS.md、規則檔 | 規則檔位置、優先順序、`/init` 自動生成、手動建立格式 |

### Agents & Intelligence

| File | Topics | Key Content |
|------|--------|-------------|
| `references/AGENTS.md` | Agent 類型、自訂 Agent | Primary agents (Build/Plan)、Subagents (General/Explore)、自訂 agent 格式 |
| `references/MODES.md` | 操作模式 | Auto/Ask/Manual 模式、模式切換、權限控制 |
| `references/SKILLS.md` | Skills 格式、發現機制 | Skill 位置、目錄結構、frontmatter 格式、權限設定 |

### Tools & Extensions

| File | Topics | Key Content |
|------|--------|-------------|
| `references/TOOLS.md` | 內建工具清單 | Read/Edit/Write/Bash/Glob/Grep/Task 等所有內建工具說明 |
| `references/CUSTOM-TOOLS.md` | 自訂工具 | 使用 opencode.json 定義自訂工具、JSON Schema、範例 |
| `references/MCP-SERVERS.md` | MCP 伺服器、工具擴充 | Local/Remote MCP 設定、command/environment/timeout、OAuth MCP |
| `references/PLUGINS.md` | 外掛系統 | Plugin 架構、生命週期、event hooks、工具攔截 |
| `references/COMMANDS.md` | 內建命令、自訂命令 | 內建命令表、快捷鍵、自訂命令格式 |

### Interfaces

| File | Topics | Key Content |
|------|--------|-------------|
| `references/TUI.md` | TUI 操作、快捷鍵 | 啟動指令、輸入語法(`@` 檔案、`!` shell、`/` 命令)、session 管理 |
| `references/CLI.md` | CLI 模式 | `opencode run` 非互動模式、pipe 輸入、CLI 參數 |
| `references/WEB.md` | Web 界面 | `opencode web` 啟動、瀏覽器訪問 |
| `references/IDE.md` | IDE 整合 | VS Code 等 IDE 的整合方式 |
| `references/KEYBINDS.md` | 快捷鍵 | 全局快捷鍵、輸入框快捷鍵、自訂快捷鍵 |
| `references/THEMES.md` | 主題 | 內建主題、自訂主題、色彩設定 |
| `references/FORMATTERS.md` | 格式化 | Markdown 輸出格式化、glamour 設定 |

### Integrations & Platform

| File | Topics | Key Content |
|------|--------|-------------|
| `references/GITHUB.md` | GitHub 整合 | GitHub Copilot 認證、GitHub Actions、PR 工作流 |
| `references/GITLAB.md` | GitLab 整合 | GitLab CI/CD、GitLab 認證 |
| `references/LSP.md` | LSP 整合 | Language Server Protocol 設定、語言支援 |
| `references/NETWORK.md` | 網路設定 | Proxy 設定、SSL、網路除錯 |
| `references/ENTERPRISE.md` | 企業功能 | 企業部署、團隊管理 |
| `references/WINDOWS-WSL.md` | Windows/WSL | Windows 和 WSL 環境設定 |

### Advanced Features

| File | Topics | Key Content |
|------|--------|-------------|
| `references/SHARE.md` | 分享 Session | 分享對話、匯出功能 |
| `references/ZEN.md` | OpenCode Zen | Zen 訂閱服務、功能 |
| `references/ACP.md` | ACP 協議 | Agent Communication Protocol |
| `references/SDK.md` | SDK | 程式化使用 OpenCode |
| `references/SERVER.md` | Server 模式 | 伺服器模式運行 |
| `references/GO.md` | Go SDK | Go 語言 SDK 使用 |
| `references/ECOSYSTEM.md` | 生態系統 | 社群資源、第三方整合 |
| `references/INDEX.md` | 總覽 | OpenCode 功能總覽 |
| `references/TROUBLESHOOTING.md` | 疑難排解 | 常見問題、除錯方法 |

## Decision Guide (Which Reference to Load)

根據問題類型選擇對應參考檔：

- **設定問題** (config file, precedence, schema, theme, model) → `references/CONFIG.md`
- **Provider 問題** (authentication, API key, OAuth, 連線) → `references/PROVIDERS.md`
- **權限問題** (allow, ask, deny, permission, 權限) → `references/PERMISSIONS.md`
- **Agent 問題** (custom agent, mode, tools, permission) → `references/AGENTS.md`
- **模式問題** (auto mode, ask mode, manual mode) → `references/MODES.md`
- **模型問題** (model, 切換模型, /models) → `references/MODELS.md`
- **命令問題** (slash command, keybind, custom command) → `references/COMMANDS.md`
- **Skills 問題** (SKILL.md, skill discovery, skill format) → `references/SKILLS.md`
- **工具問題** (built-in tools, read, edit, bash, glob) → `references/TOOLS.md`
- **自訂工具** (custom tool, JSON schema, tool definition) → `references/CUSTOM-TOOLS.md`
- **MCP 問題** (MCP server, external tools, local/remote) → `references/MCP-SERVERS.md`
- **Plugin 問題** (plugin, hook, event, intercept) → `references/PLUGINS.md`
- **規則問題** (AGENTS.md, CLAUDE.md, instructions) → `references/RULES.md`
- **TUI 問題** (keybind, input prefix, session, UI) → `references/TUI.md`
- **CLI 問題** (opencode run, pipe, non-interactive) → `references/CLI.md`
- **Web 問題** (opencode web, browser) → `references/WEB.md`
- **IDE 問題** (VS Code, editor integration) → `references/IDE.md`
- **快捷鍵問題** (keybind, shortcut) → `references/KEYBINDS.md`
- **主題問題** (theme, color, 外觀) → `references/THEMES.md`
- **格式化問題** (formatter, markdown rendering) → `references/FORMATTERS.md`
- **GitHub 問題** (Copilot auth, GitHub Actions) → `references/GITHUB.md`
- **GitLab 問題** (GitLab CI/CD) → `references/GITLAB.md`
- **LSP 問題** (language server, completion) → `references/LSP.md`
- **網路問題** (proxy, SSL, network) → `references/NETWORK.md`
- **企業問題** (enterprise, team) → `references/ENTERPRISE.md`
- **Windows 問題** (Windows, WSL) → `references/WINDOWS-WSL.md`
- **分享問題** (share session, export) → `references/SHARE.md`
- **Zen 問題** (subscription, Zen) → `references/ZEN.md`
- **SDK/Server 問題** (programmatic, Go SDK, server) → `references/SDK.md`, `references/GO.md`, `references/SERVER.md`
- **疑難排解** (troubleshooting, error, debug) → `references/TROUBLESHOOTING.md`
- **生態系統** (ecosystem, community) → `references/ECOSYSTEM.md`

## Output Template

Prefer this structure:

- What to do: 1 sentence.
- Commands: fenced `bash` block (only what is necessary).
- Files: list exact paths.
- Example config: fenced `json` or `jsonc` (use `jsonc` if comments).
- Verify: 1-2 quick checks.

## Minimal Quick Pointers

```bash
# install
curl -fsSL https://opencode.ai/install | bash

# run TUI
opencode

# run CLI (non-interactive)
opencode run "your prompt"

# run Web UI
opencode web

# add provider credentials
/connect

# pick model
/models

# initialize rules
/init
```

For details, load the matching reference file listed above.

## Common Clarifying Questions (Ask Only If Blocked)

- Are you using project-local config (`./opencode.json`) or global (`~/.config/opencode/opencode.json`)?
- Which interface: TUI (`opencode`) vs CLI (`opencode run`) vs Web (`opencode web`)?
- Which provider/model are you trying to use?
- Do you want settings applied globally or only for this repo?
