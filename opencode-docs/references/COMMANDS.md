Custom commands let you specify a prompt you want to run when that command is executed in the TUI.

```bash frame="none"
/my-command
```

Custom commands are in addition to the built-in commands like `/init`, `/undo`, `/redo`, `/share`, `/help`. [Learn more](/docs/tui#commands).

description: Run tests with coverage
agent: build
model: anthropic/claude-3-5-sonnet-20241022

## Configure

You can add custom commands through the OpenCode config or by creating markdown files in the `commands/` directory.


### Markdown

You can also define commands using markdown files. Place them in:

- Global: `~/.config/opencode/commands/`
- Per-project: `.opencode/commands/`

```markdown title="~/.config/opencode/commands/test.md"

Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

The markdown file name becomes the command name. For example, `test.md` lets
you run:

```bash frame="none"
/test
```


### Arguments

Pass arguments to commands using the `$ARGUMENTS` placeholder.

```md title=".opencode/commands/component.md"

Create a new React component named $ARGUMENTS with TypeScript support.
Include proper typing and basic structure.
```

Run the command with arguments:

```bash frame="none"
/component Button
```

And `$ARGUMENTS` will be replaced with `Button`.

You can also access individual arguments using positional parameters:

- `$1` - First argument
- `$2` - Second argument
- `$3` - Third argument
- And so on...

For example:

```md title=".opencode/commands/create-file.md"

Create a file named $1 in the directory $2
with the following content: $3
```

Run the command:

```bash frame="none"
/create-file config.json src "{ \"key\": \"value\" }"
```

This replaces:

- `$1` with `config.json`
- `$2` with `src`
- `$3` with `{ "key": "value" }`

description: Analyze test coverage
description: Review recent changes

### File references

Include files in your command using `@` followed by the filename.

```md title=".opencode/commands/review-component.md"

Review the component in @src/components/Button.tsx.
Check for performance issues and suggest improvements.
```

The file content gets included in the prompt automatically.


### Template

The `template` option defines the prompt that will be sent to the LLM when the command is executed.

```json title="opencode.json"
{
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report and show any failures.\nFocus on the failing tests and suggest fixes."
    }
  }
}
```

This is a **required** config option.


### Agent

Use the `agent` config to optionally specify which [agent](/docs/agents) should execute this command.
If this is a [subagent](/docs/agents/#subagents) the command will trigger a subagent invocation by default.
To disable this behavior, set `subtask` to `false`.

```json title="opencode.json"
{
  "command": {
    "review": {
      "agent": "plan"
    }
  }
}
```

This is an **optional** config option. If not specified, defaults to your current agent.


### Model

Use the `model` config to override the default model for this command.

```json title="opencode.json"
{
  "command": {
    "analyze": {
      "model": "anthropic/claude-3-5-sonnet-20241022"
    }
  }
}
```

This is an **optional** config option.
