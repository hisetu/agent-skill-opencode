OpenCode provides an interactive terminal interface or TUI for working on your projects with an LLM.

Running OpenCode starts the TUI for the current directory.

```bash
opencode
```

Or you can start it for a specific working directory.

```bash
opencode /path/to/project
```

Once you're in the TUI, you can prompt it with a message.

```text
Give me a quick summary of the codebase.
```


## Bash commands

Start a message with `!` to run a shell command.

```bash frame="none"
!ls -la
```

The output of the command is added to the conversation as a tool result.


### connect

Add a provider to OpenCode. Allows you to select from available providers and add their API keys.

```bash frame="none"
/connect
```


### details

Toggle tool execution details.

```bash frame="none"
/details
```

**Keybind:** `ctrl+x d`


### exit

Exit OpenCode. _Aliases_: `/quit`, `/q`

```bash frame="none"
/exit
```

**Keybind:** `ctrl+x q`


### help

Show the help dialog.

```bash frame="none"
/help
```

**Keybind:** `ctrl+x h`


### models

List available models.

```bash frame="none"
/models
```

**Keybind:** `ctrl+x m`


### redo

Redo a previously undone message. Only available after using `/undo`.

:::tip
Any file changes will also be restored.
:::

Internally, this uses Git to manage the file changes. So your project **needs to
be a Git repository**.

```bash frame="none"
/redo
```

**Keybind:** `ctrl+x r`


### share

Share current session. [Learn more](/docs/share).

```bash frame="none"
/share
```

**Keybind:** `ctrl+x s`


### thinking

Toggle the visibility of thinking/reasoning blocks in the conversation. When enabled, you can see the model's reasoning process for models that support extended thinking.

:::note
This command only controls whether thinking blocks are **displayed** - it does not enable or disable the model's reasoning capabilities. To toggle actual reasoning capabilities, use `ctrl+t` to cycle through model variants.
:::

```bash frame="none"
/thinking
```


### unshare

Unshare current session. [Learn more](/docs/share#un-sharing).

```bash frame="none"
/unshare
```


## Configure

You can customize TUI behavior through `tui.json` (or `tui.jsonc`).

```json title="tui.json"
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "opencode",
  "keybinds": {
    "leader": "ctrl+x"
  },
  "scroll_speed": 3,
  "scroll_acceleration": {
    "enabled": true
  },
  "diff_style": "auto"
}
```

This is separate from `opencode.json`, which configures server/runtime behavior.

### Options

- `theme` - Sets your UI theme. [Learn more](/docs/themes).
- `keybinds` - Customizes keyboard shortcuts. [Learn more](/docs/keybinds).
- `scroll_acceleration.enabled` - Enable macOS-style scroll acceleration for smooth, natural scrolling. When enabled, scroll speed increases with rapid scrolling gestures and stays precise for slower movements. **This setting takes precedence over `scroll_speed` and overrides it when enabled.**
- `scroll_speed` - Controls how fast the TUI scrolls when using scroll commands (minimum: `0.001`, supports decimal values). Defaults to `3`. **Note: This is ignored if `scroll_acceleration.enabled` is set to `true`.**
- `diff_style` - Controls diff rendering. `"auto"` adapts to terminal width, `"stacked"` always shows a single-column layout.

Use `OPENCODE_TUI_CONFIG` to load a custom TUI config path.


#### Username display

Toggle whether your username appears in chat messages. Access this through:

- Command palette: Search for "username" or "hide username"
- The setting persists automatically and will be remembered across TUI sessions
