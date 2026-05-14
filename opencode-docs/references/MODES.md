:::caution
Modes are now configured through the `agent` option in the opencode config. The
`mode` option is now deprecated. [Learn more](/docs/agents).
:::

Modes in opencode allow you to customize the behavior, tools, and prompts for different use cases.

It comes with two built-in modes: **build** and **plan**. You can customize
these or configure your own through the opencode config.

You can switch between modes during a session or configure them in your config file.


### Build

Build is the **default** mode with all tools enabled. This is the standard mode for development work where you need full access to file operations and system commands.


## Switching

You can switch between modes during a session using the _Tab_ key. Or your configured `switch_mode` keybind.

See also: [Formatters](/docs/formatters) for information about code formatting configuration.

model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  write: false
  edit: false
  bash: false

### Model

Use the `model` config to override the default model for this mode. Useful for using different models optimized for different tasks. For example, a faster model for planning, a more capable model for implementation.

```json title="opencode.json"
{
  "mode": {
    "plan": {
      "model": "anthropic/claude-haiku-4-20250514"
    }
  }
}
```


### Prompt

Specify a custom system prompt file for this mode with the `prompt` config. The prompt file should contain instructions specific to the mode's purpose.

```json title="opencode.json"
{
  "mode": {
    "review": {
      "prompt": "{file:./prompts/code-review.txt}"
    }
  }
}
```

This path is relative to where the config file is located. So this works for
both the global opencode config and the project specific config.


#### Available tools

Here are all the tools can be controlled through the mode config.

| Tool        | Description             |
| ----------- | ----------------------- |
| `bash`      | Execute shell commands  |
| `edit`      | Modify existing files   |
| `write`     | Create new files        |
| `read`      | Read file contents      |
| `grep`      | Search file contents    |
| `glob`      | Find files by pattern   |
| `list`      | List directory contents |
| `patch`     | Apply patches to files  |
| `todowrite` | Manage todo lists       |
| `todoread`  | Read todo lists         |
| `webfetch`  | Fetch web content       |

temperature: 0.1
tools:
  bash: true
  read: true
  grep: true
  write: false
  edit: false
model: anthropic/claude-sonnet-4-20250514
temperature: 0.2
tools:
  edit: true
  read: true
  grep: true
  glob: true

### Use cases

Here are some common use cases for different modes.

- **Build mode**: Full development work with all tools enabled
- **Plan mode**: Analysis and planning without making changes
- **Review mode**: Code review with read-only access plus documentation tools
- **Debug mode**: Focused on investigation with bash and read tools enabled
- **Docs mode**: Documentation writing with file operations but no system commands

You might also find different models are good for different use cases.
