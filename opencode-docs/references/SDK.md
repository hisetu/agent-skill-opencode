export const typesUrl = `${config.github}/blob/dev/packages/sdk/js/src/gen/types.gen.ts`

The opencode JS/TS SDK provides a type-safe client for interacting with the server.
Use it to build integrations and control opencode programmatically.

[Learn more](/docs/server) about how the server works. For examples, check out the [projects](/docs/ecosystem#projects) built by the community.


## Create client

Create an instance of opencode:

```javascript

const { client } = await createOpencode()
```

This starts both a server and a client

#### Options

| Option     | Type          | Description                    | Default     |
| ---------- | ------------- | ------------------------------ | ----------- |
| `hostname` | `string`      | Server hostname                | `127.0.0.1` |
| `port`     | `number`      | Server port                    | `4096`      |
| `signal`   | `AbortSignal` | Abort signal for cancellation  | `undefined` |
| `timeout`  | `number`      | Timeout in ms for server start | `5000`      |
| `config`   | `Config`      | Configuration object           | `{}`        |


## Types

The SDK includes TypeScript definitions for all API types. Import them directly:

```typescript
```

All types are generated from the server's OpenAPI specification and available in the <a href={typesUrl}>types file</a>.


## Structured Output

You can request structured JSON output from the model by specifying an `format` with a JSON schema. The model will use a `StructuredOutput` tool to return validated JSON matching your schema.

### Basic Usage

```typescript
const result = await client.session.prompt({
  path: { id: sessionId },
  body: {
    parts: [{ type: "text", text: "Research Anthropic and provide company info" }],
    format: {
      type: "json_schema",
      schema: {
        type: "object",
        properties: {
          company: { type: "string", description: "Company name" },
          founded: { type: "number", description: "Year founded" },
          products: {
            type: "array",
            items: { type: "string" },
            description: "Main products",
          },
        },
        required: ["company", "founded"],
      },
    },
  },
})

// Access the structured output
console.log(result.data.info.structured_output)
// { company: "Anthropic", founded: 2021, products: ["Claude", "Claude API"] }
```

### Output Format Types

| Type          | Description                                            |
| ------------- | ------------------------------------------------------ |
| `text`        | Default. Standard text response (no structured output) |
| `json_schema` | Returns validated JSON matching the provided schema    |

### JSON Schema Format

When using `type: 'json_schema'`, provide:

| Field        | Type            | Description                                                |
| ------------ | --------------- | ---------------------------------------------------------- |
| `type`       | `'json_schema'` | Required. Specifies JSON schema mode                       |
| `schema`     | `object`        | Required. JSON Schema object defining the output structure |
| `retryCount` | `number`        | Optional. Number of validation retries (default: 2)        |

### Error Handling

If the model fails to produce valid structured output after all retries, the response will include a `StructuredOutputError`:

```typescript
if (result.data.info.error?.name === "StructuredOutputError") {
  console.error("Failed to produce structured output:", result.data.info.error.message)
  console.error("Attempts:", result.data.info.error.retries)
}
```

### Best Practices

1. **Provide clear descriptions** in your schema properties to help the model understand what data to extract
2. **Use `required`** to specify which fields must be present
3. **Keep schemas focused** - complex nested schemas may be harder for the model to fill correctly
4. **Set appropriate `retryCount`** - increase for complex schemas, decrease for simple ones


### Global

| Method            | Description                     | Response                             |
| ----------------- | ------------------------------- | ------------------------------------ |
| `global.health()` | Check server health and version | `{ healthy: true, version: string }` |


### App

| Method         | Description               | Response                                    |
| -------------- | ------------------------- | ------------------------------------------- |
| `app.log()`    | Write a log entry         | `boolean`                                   |
| `app.agents()` | List all available agents | <a href={typesUrl}><code>Agent[]</code></a> |


### Project

| Method              | Description         | Response                                      |
| ------------------- | ------------------- | --------------------------------------------- |
| `project.list()`    | List all projects   | <a href={typesUrl}><code>Project[]</code></a> |
| `project.current()` | Get current project | <a href={typesUrl}><code>Project</code></a>   |


### Path

| Method       | Description      | Response                                 |
| ------------ | ---------------- | ---------------------------------------- |
| `path.get()` | Get current path | <a href={typesUrl}><code>Path</code></a> |


### Config

| Method               | Description                       | Response                                                                                              |
| -------------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `config.get()`       | Get config info                   | <a href={typesUrl}><code>Config</code></a>                                                            |
| `config.providers()` | List providers and default models | `{ providers: `<a href={typesUrl}><code>Provider[]</code></a>`, default: { [key: string]: string } }` |


### Sessions

| Method                                                     | Description                        | Notes                                                                                                                                                                                                                    |
| ---------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `session.list()`                                           | List sessions                      | Returns <a href={typesUrl}><code>Session[]</code></a>                                                                                                                                                                    |
| `session.get({ path })`                                    | Get session                        | Returns <a href={typesUrl}><code>Session</code></a>                                                                                                                                                                      |
| `session.children({ path })`                               | List child sessions                | Returns <a href={typesUrl}><code>Session[]</code></a>                                                                                                                                                                    |
| `session.create({ body })`                                 | Create session                     | Returns <a href={typesUrl}><code>Session</code></a>                                                                                                                                                                      |
| `session.delete({ path })`                                 | Delete session                     | Returns `boolean`                                                                                                                                                                                                        |
| `session.update({ path, body })`                           | Update session properties          | Returns <a href={typesUrl}><code>Session</code></a>                                                                                                                                                                      |
| `session.init({ path, body })`                             | Analyze app and create `AGENTS.md` | Returns `boolean`                                                                                                                                                                                                        |
| `session.abort({ path })`                                  | Abort a running session            | Returns `boolean`                                                                                                                                                                                                        |
| `session.share({ path })`                                  | Share session                      | Returns <a href={typesUrl}><code>Session</code></a>                                                                                                                                                                      |
| `session.unshare({ path })`                                | Unshare session                    | Returns <a href={typesUrl}><code>Session</code></a>                                                                                                                                                                      |
| `session.summarize({ path, body })`                        | Summarize session                  | Returns `boolean`                                                                                                                                                                                                        |
| `session.messages({ path })`                               | List messages in a session         | Returns `{ info: `<a href={typesUrl}><code>Message</code></a>`, parts: `<a href={typesUrl}><code>Part[]</code></a>`}[]`                                                                                                  |
| `session.message({ path })`                                | Get message details                | Returns `{ info: `<a href={typesUrl}><code>Message</code></a>`, parts: `<a href={typesUrl}><code>Part[]</code></a>`}`                                                                                                    |
| `session.prompt({ path, body })`                           | Send prompt message                | `body.noReply: true` returns UserMessage (context only). Default returns <a href={typesUrl}><code>AssistantMessage</code></a> with AI response. Supports `body.outputFormat` for [structured output](#structured-output) |
| `session.command({ path, body })`                          | Send command to session            | Returns `{ info: `<a href={typesUrl}><code>AssistantMessage</code></a>`, parts: `<a href={typesUrl}><code>Part[]</code></a>`}`                                                                                           |
| `session.shell({ path, body })`                            | Run a shell command                | Returns <a href={typesUrl}><code>AssistantMessage</code></a>                                                                                                                                                             |
| `session.revert({ path, body })`                           | Revert a message                   | Returns <a href={typesUrl}><code>Session</code></a>                                                                                                                                                                      |
| `session.unrevert({ path })`                               | Restore reverted messages          | Returns <a href={typesUrl}><code>Session</code></a>                                                                                                                                                                      |
| `postSessionByIdPermissionsByPermissionId({ path, body })` | Respond to a permission request    | Returns `boolean`                                                                                                                                                                                                        |


### Files

| Method                    | Description                        | Response                                                                                    |
| ------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------- |
| `find.text({ query })`    | Search for text in files           | Array of match objects with `path`, `lines`, `line_number`, `absolute_offset`, `submatches` |
| `find.files({ query })`   | Find files and directories by name | `string[]` (paths)                                                                          |
| `find.symbols({ query })` | Find workspace symbols             | <a href={typesUrl}><code>Symbol[]</code></a>                                                |
| `file.read({ query })`    | Read a file                        | `{ type: "raw" \| "patch", content: string }`                                               |
| `file.status({ query? })` | Get status for tracked files       | <a href={typesUrl}><code>File[]</code></a>                                                  |

`find.files` supports a few optional query fields:

- `type`: `"file"` or `"directory"`
- `directory`: override the project root for the search
- `limit`: max results (1–200)


### TUI

| Method                         | Description               | Response  |
| ------------------------------ | ------------------------- | --------- |
| `tui.appendPrompt({ body })`   | Append text to the prompt | `boolean` |
| `tui.openHelp()`               | Open the help dialog      | `boolean` |
| `tui.openSessions()`           | Open the session selector | `boolean` |
| `tui.openThemes()`             | Open the theme selector   | `boolean` |
| `tui.openModels()`             | Open the model selector   | `boolean` |
| `tui.submitPrompt()`           | Submit the current prompt | `boolean` |
| `tui.clearPrompt()`            | Clear the prompt          | `boolean` |
| `tui.executeCommand({ body })` | Execute a command         | `boolean` |
| `tui.showToast({ body })`      | Show toast notification   | `boolean` |


### Auth

| Method              | Description                    | Response  |
| ------------------- | ------------------------------ | --------- |
| `auth.set({ ... })` | Set authentication credentials | `boolean` |


### Events

| Method              | Description               | Response                  |
| ------------------- | ------------------------- | ------------------------- |
| `event.subscribe()` | Server-sent events stream | Server-sent events stream |
