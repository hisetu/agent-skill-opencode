OpenCode integrates with your Language Server Protocol (LSP) to help the LLM interact with your codebase. It uses diagnostics to provide feedback to the LLM.


## How It Works

When opencode opens a file, it:

1. Checks the file extension against all enabled LSP servers.
2. Starts the appropriate LSP server if not already running.


### Environment variables

Use the `env` property to set environment variables when starting the LSP server:

```json title="opencode.json" {5-7}
{
  "$schema": "https://opencode.ai/config.json",
  "lsp": {
    "rust": {
      "env": {
        "RUST_LOG": "debug"
      }
    }
  }
}
```


### Disabling LSP servers

To disable **all** LSP servers globally, set `lsp` to `false`:

```json title="opencode.json" {3}
{
  "$schema": "https://opencode.ai/config.json",
  "lsp": false
}
```

To disable a **specific** LSP server, set `disabled` to `true`:

```json title="opencode.json" {5}
{
  "$schema": "https://opencode.ai/config.json",
  "lsp": {
    "typescript": {
      "disabled": true
    }
  }
}
```


## Additional Information

### PHP Intelephense

PHP Intelephense offers premium features through a license key. You can provide a license key by placing (only) the key in a text file at:

- On macOS/Linux: `$HOME/intelephense/license.txt`
- On Windows: `%USERPROFILE%/intelephense/license.txt`

The file should contain only the license key with no additional content.
