The OpenCode CLI by default starts the [TUI](/docs/tui) when run without any arguments.

```bash
opencode
```

But it also accepts commands as documented on this page. This allows you to interact with OpenCode programmatically.

```bash
opencode run "Explain how closures work in JavaScript"
```


## Commands

The OpenCode CLI also has the following commands.


### attach

Attach a terminal to an already running OpenCode backend server started via `serve` or `web` commands.

```bash
opencode attach [url]
```

This allows using the TUI with a remote OpenCode backend. For example:

```bash
# Start the backend server for web/mobile access
opencode web --port 4096 --hostname 0.0.0.0

# In another terminal, attach the TUI to the running backend
opencode attach http://10.20.30.40:4096
```

#### Flags

| Flag        | Short | Description                       |
| ----------- | ----- | --------------------------------- |
| `--dir`     |       | Working directory to start TUI in |
| `--session` | `-s`  | Session ID to continue            |


#### list

List all available agents.

```bash
opencode agent list
```


#### login

OpenCode is powered by the provider list at [Models.dev](https://models.dev), so you can use `opencode auth login` to configure API keys for any provider you'd like to use. This is stored in `~/.local/share/opencode/auth.json`.

```bash
opencode auth login
```

When OpenCode starts up it loads the providers from the credentials file. And if there are any keys defined in your environments or a `.env` file in your project.


#### logout

Logs you out of a provider by clearing it from the credentials file.

```bash
opencode auth logout
```


#### install

Install the GitHub agent in your repository.

```bash
opencode github install
```

This sets up the necessary GitHub Actions workflow and guides you through the configuration process. [Learn more](/docs/github).


### mcp

Manage Model Context Protocol servers.

```bash
opencode mcp [command]
```


#### list

List all configured MCP servers and their connection status.

```bash
opencode mcp list
```

Or use the short version.

```bash
opencode mcp ls
```


#### logout

Remove OAuth credentials for an MCP server.

```bash
opencode mcp logout [name]
```


### models

List all available models from configured providers.

```bash
opencode models [provider]
```

This command displays all models available across your configured providers in the format `provider/model`.

This is useful for figuring out the exact model name to use in [your config](/docs/config/).

You can optionally pass a provider ID to filter models by that provider.

```bash
opencode models anthropic
```

#### Flags

| Flag        | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| `--refresh` | Refresh the models cache from models.dev                     |
| `--verbose` | Use more verbose model output (includes metadata like costs) |

Use the `--refresh` flag to update the cached model list. This is useful when new models have been added to a provider and you want to see them in OpenCode.

```bash
opencode models --refresh
```


### serve

Start a headless OpenCode server for API access. Check out the [server docs](/docs/server) for the full HTTP interface.

```bash
opencode serve
```

This starts an HTTP server that provides API access to opencode functionality without the TUI interface. Set `OPENCODE_SERVER_PASSWORD` to enable HTTP basic auth (username defaults to `opencode`).

#### Flags

| Flag         | Description                                |
| ------------ | ------------------------------------------ |
| `--port`     | Port to listen on                          |
| `--hostname` | Hostname to listen on                      |
| `--mdns`     | Enable mDNS discovery                      |
| `--cors`     | Additional browser origin(s) to allow CORS |


#### list

List all OpenCode sessions.

```bash
opencode session list
```

##### Flags

| Flag          | Short | Description                          |
| ------------- | ----- | ------------------------------------ |
| `--max-count` | `-n`  | Limit to N most recent sessions      |
| `--format`    |       | Output format: table or json (table) |


### export

Export session data as JSON.

```bash
opencode export [sessionID]
```

If you don't provide a session ID, you'll be prompted to select from available sessions.


### web

Start a headless OpenCode server with a web interface.

```bash
opencode web
```

This starts an HTTP server and opens a web browser to access OpenCode through a web interface. Set `OPENCODE_SERVER_PASSWORD` to enable HTTP basic auth (username defaults to `opencode`).

#### Flags

| Flag         | Description                                |
| ------------ | ------------------------------------------ |
| `--port`     | Port to listen on                          |
| `--hostname` | Hostname to listen on                      |
| `--mdns`     | Enable mDNS discovery                      |
| `--cors`     | Additional browser origin(s) to allow CORS |


### uninstall

Uninstall OpenCode and remove all related files.

```bash
opencode uninstall
```

#### Flags

| Flag            | Short | Description                                 |
| --------------- | ----- | ------------------------------------------- |
| `--keep-config` | `-c`  | Keep configuration files                    |
| `--keep-data`   | `-d`  | Keep session data and snapshots             |
| `--dry-run`     |       | Show what would be removed without removing |
| `--force`       | `-f`  | Skip confirmation prompts                   |


## Global Flags

The opencode CLI takes the following global flags.

| Flag           | Short | Description                          |
| -------------- | ----- | ------------------------------------ |
| `--help`       | `-h`  | Display help                         |
| `--version`    | `-v`  | Print version number                 |
| `--print-logs` |       | Print logs to stderr                 |
| `--log-level`  |       | Log level (DEBUG, INFO, WARN, ERROR) |


### Experimental

These environment variables enable experimental features that may change or be removed.

| Variable                                        | Type    | Description                             |
| ----------------------------------------------- | ------- | --------------------------------------- |
| `OPENCODE_EXPERIMENTAL`                         | boolean | Enable all experimental features        |
| `OPENCODE_EXPERIMENTAL_ICON_DISCOVERY`          | boolean | Enable icon discovery                   |
| `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT`  | boolean | Disable copy on select in TUI           |
| `OPENCODE_EXPERIMENTAL_BASH_DEFAULT_TIMEOUT_MS` | number  | Default timeout for bash commands in ms |
| `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX`        | number  | Max output tokens for LLM responses     |
| `OPENCODE_EXPERIMENTAL_FILEWATCHER`             | boolean | Enable file watcher for entire dir      |
| `OPENCODE_EXPERIMENTAL_OXFMT`                   | boolean | Enable oxfmt formatter                  |
| `OPENCODE_EXPERIMENTAL_LSP_TOOL`                | boolean | Enable experimental LSP tool            |
| `OPENCODE_EXPERIMENTAL_DISABLE_FILEWATCHER`     | boolean | Disable file watcher                    |
| `OPENCODE_EXPERIMENTAL_EXA`                     | boolean | Enable experimental Exa features        |
| `OPENCODE_EXPERIMENTAL_LSP_TY`                  | boolean | Enable TY LSP for python files          |
| `OPENCODE_EXPERIMENTAL_MARKDOWN`                | boolean | Enable experimental markdown features   |
| `OPENCODE_EXPERIMENTAL_PLAN_MODE`               | boolean | Enable plan mode                        |
