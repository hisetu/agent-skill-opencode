---
name: opencode-failure-prompt-miner
description: >-
  Analyze OpenCode sessions in ~/.local/share/opencode/opencode.db, mine repeated
  failure patterns from tool errors and user correction signals, and turn them
  into reusable prompt guardrails. Use when the user wants to learn from past
  OpenCode mistakes, generate anti-failure prompts, or build prompt rules from
  session history. Triggers: failure prompt, learn from sessions, mine mistakes,
  session lessons, anti-failure prompt, 從 session 學習, 失敗經驗, 錯誤經驗,
  提示優化, prompt guardrails.
license: MIT
compatibility: opencode
metadata:
  author: lucas
  version: "1.0"
  language: zh-TW
---

# OpenCode Failure Prompt Miner

從 `~/.local/share/opencode/opencode.db` 抽取高訊號失敗經驗，整理成可重用提示。

這個 skill 的目標不是單純找錯，而是把「曾經怎麼失手」濃縮成之後可直接重用的 prompt guardrails。

## When to Use

- 使用者想把 OpenCode 歷史 session 的失敗經驗整理成提示
- 使用者想降低 AI 重犯同類錯誤
- 使用者想從 `opencode.db` 產出 prompt 規則或操作守則
- 使用者要建立一份可貼進 system prompt / skill / agent rule 的防呆提示

## What This Skill Mines

這個 skill 目前優先分析兩種高訊號資料：

- `tool error`: 工具實際執行失敗，例如 `File not found`、`oldString not found`
- `user correction`: 使用者明確糾正 agent，例如 `我只是問`、`先不要改`

這兩類訊號的價值最高，因為它們分別代表：

- 執行層失敗
- 意圖理解失敗

## Core Rule

先抽證據，再寫提示。

不要先憑印象寫「看起來很合理」的 prompt。一定要先從 session transcript 抽到具體錯誤訊號，再把它們提升為 guardrail。

## Workflow

### 1. 先跑 helper script 找候選失敗模式

```bash
python3 ~/.config/opencode/skills/opencode-failure-prompt-miner/scripts/mine_failures.py sessions --days 30 --limit 20
```

這一步會列出最近 session 的失敗分數，包含：

- tool error 數量
- user correction 數量
- 代表性證據

### 2. 產出可重用 prompt

```bash
python3 ~/.config/opencode/skills/opencode-failure-prompt-miner/scripts/mine_failures.py prompt --days 30 --limit 40
```

這一步會輸出：

- 觀察到的高頻失敗模式
- 每個模式的代表證據
- 對應的 prompt guardrail
- 一個可直接貼用的 prompt block

### 3. 必要時寫入目標檔案

如果使用者要把結果保存成文件或新的 skill reference，可以再把輸出整理後寫進：

- `SKILL.md`
- `references/*.md`
- 專案內的 AI 規則文件

若使用者沒有要求落地到檔案，先回傳整理後的 prompt 即可。

## Output Standard

回覆使用者時，優先用這個格式：

```text
觀察到的失敗模式:
1. ...
2. ...

代表證據:
- ses_xxx: ...
- ses_yyy: ...

建議加入的 prompt guardrails:
- ...
- ...

可直接使用的 prompt block:
<failure_guardrails>
- ...
</failure_guardrails>
```

## Guardrails

- 不要把單一次偶發錯誤過度泛化成硬規則
- 區分「工具失敗」與「使用者其實不想你動手」
- 引用證據時，優先用原始錯誤訊息或使用者糾正原文
- 若只是推論，不要寫成已驗證事實
- 若抽到的只是低訊號噪音，明說「目前沒有足夠穩定的失敗模式」

## Recommended Heuristics

這個 skill 目前最可靠的模式通常會落在：

- 路徑或檔案不存在，代表執行前驗證不夠
- `oldString not found`，代表 patch 前沒有 reread live file
- 使用者說 `我只是問` / `先不要改`，代表模式誤判成直接實作

## Helper Script

```bash
python3 ~/.config/opencode/skills/opencode-failure-prompt-miner/scripts/mine_failures.py --help
```

常用範例：

```bash
# 看最近 14 天有哪些高分失敗 session
python3 ~/.config/opencode/skills/opencode-failure-prompt-miner/scripts/mine_failures.py sessions --days 14 --limit 15

# 產出最近 30 天的防呆 prompt
python3 ~/.config/opencode/skills/opencode-failure-prompt-miner/scripts/mine_failures.py prompt --days 30 --limit 40

# 把結果存成 markdown
python3 ~/.config/opencode/skills/opencode-failure-prompt-miner/scripts/mine_failures.py prompt --days 30 --output /Users/lucas/failure-guardrails.md
```

## Notes

- 資料來源預設是 `~/.local/share/opencode/opencode.db`
- transcript 證據主要來自 `session`、`message`、`part`
- `part.data` 裡的 `tool` + `state.status=error` 是高價值訊號
- `message.role=user` 對應的 text part 很適合挖使用者糾正訊號
