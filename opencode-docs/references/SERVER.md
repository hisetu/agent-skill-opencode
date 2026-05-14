export const typesUrl = `${config.github}/blob/dev/packages/sdk/js/src/gen/types.gen.ts`

The `opencode serve` command runs a headless HTTP server that exposes an OpenAPI endpoint that an opencode client can use.


### Authentication

Set `OPENCODE_SERVER_PASSWORD` to protect the server with HTTP basic auth. The username defaults to `opencode`, or set `OPENCODE_SERVER_USERNAME` to override it. This applies to both `opencode serve` and `opencode web`.

```bash
OPENCODE_SERVER_PASSWORD=your-password opencode serve
```


#### Connect to an existing server

When you start the TUI it randomly assigns a port and hostname. You can instead pass in the `--hostname` and `--port` [flags](/docs/cli). Then use this to connect to its server.

The [`/tui`](#tui) endpoint can be used to drive the TUI through the server. For example, you can prefill or run a prompt. This setup is used by the OpenCode [IDE](/docs/ide) plugins.


## APIs

The opencode server exposes the following APIs.


### Project

| Method | Path               | Description             | Response                                      |
| ------ | ------------------ | ----------------------- | --------------------------------------------- |
| `GET`  | `/project`         | List all projects       | <a href={typesUrl}><code>Project[]</code></a> |
| `GET`  | `/project/current` | Get the current project | <a href={typesUrl}><code>Project</code></a>   |


### Instance

| Method | Path                | Description                  | Response  |
| ------ | ------------------- | ---------------------------- | --------- |
| `POST` | `/instance/dispose` | Dispose the current instance | `boolean` |


### Provider

| Method | Path                             | Description                          | Response                                                                            |
| ------ | -------------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------- |
| `GET`  | `/provider`                      | List all providers                   | `{ all: `<a href={typesUrl}>Provider[]</a>`, default: {...}, connected: string[] }` |
| `GET`  | `/provider/auth`                 | Get provider authentication methods  | `{ [providerID: string]: `<a href={typesUrl}>ProviderAuthMethod[]</a>` }`           |
| `POST` | `/provider/{id}/oauth/authorize` | Authorize a provider using OAuth     | <a href={typesUrl}><code>ProviderAuthAuthorization</code></a>                       |
| `POST` | `/provider/{id}/oauth/callback`  | Handle OAuth callback for a provider | `boolean`                                                                           |


### Messages

| Method | Path                              | Description                             | Notes                                                                                                                                                                 |
| ------ | --------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GET`  | `/session/:id/message`            | List messages in a session              | query: `limit?`, returns `{ info: `<a href={typesUrl}>Message</a>`, parts: `<a href={typesUrl}>Part[]</a>`}[]`                                                        |
| `POST` | `/session/:id/message`            | Send a message and wait for response    | body: `{ messageID?, model?, agent?, noReply?, system?, tools?, parts }`, returns `{ info: `<a href={typesUrl}>Message</a>`, parts: `<a href={typesUrl}>Part[]</a>`}` |
| `GET`  | `/session/:id/message/:messageID` | Get message details                     | Returns `{ info: `<a href={typesUrl}>Message</a>`, parts: `<a href={typesUrl}>Part[]</a>`}`                                                                           |
| `POST` | `/session/:id/prompt_async`       | Send a message asynchronously (no wait) | body: same as `/session/:id/message`, returns `204 No Content`                                                                                                        |
| `POST` | `/session/:id/command`            | Execute a slash command                 | body: `{ messageID?, agent?, model?, command, arguments }`, returns `{ info: `<a href={typesUrl}>Message</a>`, parts: `<a href={typesUrl}>Part[]</a>`}`               |
| `POST` | `/session/:id/shell`              | Run a shell command                     | body: `{ agent, model?, command }`, returns `{ info: `<a href={typesUrl}>Message</a>`, parts: `<a href={typesUrl}>Part[]</a>`}`                                       |


### Files

| Method | Path                     | Description                        | Response                                                                                    |
| ------ | ------------------------ | ---------------------------------- | ------------------------------------------------------------------------------------------- |
| `GET`  | `/find?pattern=<pat>`    | Search for text in files           | Array of match objects with `path`, `lines`, `line_number`, `absolute_offset`, `submatches` |
| `GET`  | `/find/file?query=<q>`   | Find files and directories by name | `string[]` (paths)                                                                          |
| `GET`  | `/find/symbol?query=<q>` | Find workspace symbols             | <a href={typesUrl}><code>Symbol[]</code></a>                                                |
| `GET`  | `/file?path=<path>`      | List files and directories         | <a href={typesUrl}><code>FileNode[]</code></a>                                              |
| `GET`  | `/file/content?path=<p>` | Read a file                        | <a href={typesUrl}><code>FileContent</code></a>                                             |
| `GET`  | `/file/status`           | Get status for tracked files       | <a href={typesUrl}><code>File[]</code></a>                                                  |

#### `/find/file` query parameters

- `query` (required) — search string (fuzzy match)
- `type` (optional) — limit results to `"file"` or `"directory"`
- `directory` (optional) — override the project root for the search
- `limit` (optional) — max results (1–200)
- `dirs` (optional) — legacy flag (`"false"` returns only files)


### LSP, Formatters & MCP

| Method | Path         | Description                | Response                                                 |
| ------ | ------------ | -------------------------- | -------------------------------------------------------- |
| `GET`  | `/lsp`       | Get LSP server status      | <a href={typesUrl}><code>LSPStatus[]</code></a>          |
| `GET`  | `/formatter` | Get formatter status       | <a href={typesUrl}><code>FormatterStatus[]</code></a>    |
| `GET`  | `/mcp`       | Get MCP server status      | `{ [name: string]: `<a href={typesUrl}>MCPStatus</a>` }` |
| `POST` | `/mcp`       | Add MCP server dynamically | body: `{ name, config }`, returns MCP status object      |


### Logging

| Method | Path   | Description                                                  | Response  |
| ------ | ------ | ------------------------------------------------------------ | --------- |
| `POST` | `/log` | Write log entry. Body: `{ service, level, message, extra? }` | `boolean` |


### Auth

| Method | Path        | Description                                                     | Response  |
| ------ | ----------- | --------------------------------------------------------------- | --------- |
| `PUT`  | `/auth/:id` | Set authentication credentials. Body must match provider schema | `boolean` |


### Docs

| Method | Path   | Description               | Response                    |
| ------ | ------ | ------------------------- | --------------------------- |
| `GET`  | `/doc` | OpenAPI 3.1 specification | HTML page with OpenAPI spec |
