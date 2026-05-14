OpenCode integrates with VS Code, Cursor, or any IDE that supports a terminal. Just run `opencode` in the terminal to get started.


## Installation

To install OpenCode on VS Code and popular forks like Cursor, Windsurf, VSCodium:

1. Open VS Code
2. Open the integrated terminal
3. Run `opencode` - the extension installs automatically

If on the other hand you want to use your own IDE when you run `/editor` or `/export` from the TUI, you'll need to set `export EDITOR="code --wait"`. [Learn more](/docs/tui/#editor-setup).


### Troubleshooting

If the extension fails to install automatically:

- Ensure you’re running `opencode` in the integrated terminal.
- Confirm the CLI for your IDE is installed:
  - For VS Code: `code` command
  - For Cursor: `cursor` command
  - For Windsurf: `windsurf` command
  - For VSCodium: `codium` command
  - If not, run `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux) and search for "Shell Command: Install 'code' command in PATH" (or the equivalent for your IDE)
- Ensure VS Code has permission to install extensions
