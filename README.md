# agent-skill-opencode

A curated collection of OpenCode-focused skills extracted from `~/.agents/skills`.

## Included skills

| Skill | Purpose |
|---|---|
| `opencode-docs` | Retrieve and explain OpenCode documentation, including features, configuration, commands, providers, agents, skills, MCP servers, rules, and TUI usage. |
| `opencode-ecosystem` | Explore the OpenCode ecosystem, including community plugins, projects, agents, and third-party integrations. |
| `opencode-extension-search` | Search for existing OpenCode extensions such as plugins, MCP servers, themes, and commands. |
| `opencode-failure-prompt-miner` | Analyze OpenCode session history to mine repeated failure patterns and turn them into reusable prompt guardrails. |
| `opencode-plugin` | Guide for building and understanding OpenCode plugins, including event listeners and tool interception. |
| `opencode-session` | Quickly find and inspect OpenCode session files to continue previous work or review session history. |
| `opencode-session-cleaner` | Remove compaction messages from OpenCode sessions to restore fuller conversation history. |
| `opencode-session-investigator` | Investigate why an OpenCode agent made a mistake by reconstructing relevant session and tool flow history. |
| `opencode-session-sqlite` | Use SQLite-based workflows to trace which OpenCode session introduced or reintroduced a change. |

## Repository structure

```text
agent-skill-opencode/
├── README.md
├── opencode-docs/
├── opencode-ecosystem/
├── opencode-extension-search/
├── opencode-failure-prompt-miner/
├── opencode-plugin/
├── opencode-session/
├── opencode-session-cleaner/
├── opencode-session-investigator/
└── opencode-session-sqlite/
```

## Notes

- Source: extracted from local skills under `~/.agents/skills`.
- The original file naming is preserved, including directories that use `skill.md` instead of `SKILL.md`.
- Any bundled `references/` or `scripts/` directories are included as-is.

## Usage

Clone or copy this repository into your OpenCode skills directory, for example:

```bash
git clone git@github.com:hisetu/agent-skill-opencode.git ~/.config/opencode/skills/agent-skill-opencode
```

Or copy individual skill folders into your own skills path as needed.
