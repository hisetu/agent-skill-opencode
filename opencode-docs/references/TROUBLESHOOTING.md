To debug issues with OpenCode, start by checking the logs and local data it stores on disk.


## Storage

opencode stores session data and other application data on disk at:

- **macOS/Linux**: `~/.local/share/opencode/`
- **Windows**: Press `WIN+R` and paste `%USERPROFILE%\.local\share\opencode`

This directory contains:

- `auth.json` - Authentication data like API keys, OAuth tokens
- `log/` - Application logs
- `project/` - Project-specific data like session and message data
  - If the project is within a Git repo, it is stored in `./<project-slug>/storage/`
  - If it is not a Git repo, it is stored in `./global/storage/`


### Disable plugins

If the desktop app is crashing on launch, hanging, or behaving strangely, start by disabling plugins.

#### Check the global config

Open your global config file and look for a `plugin` key.

- **macOS/Linux**: `~/.config/opencode/opencode.jsonc` (or `~/.config/opencode/opencode.json`)
- **macOS/Linux** (older installs): `~/.local/share/opencode/opencode.jsonc`
- **Windows**: Press `WIN+R` and paste `%USERPROFILE%\.config\opencode\opencode.jsonc`

If you have plugins configured, temporarily disable them by removing the key or setting it to an empty array:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [],
}
```

#### Check plugin directories

OpenCode can also load local plugins from disk. Temporarily move these out of the way (or rename the folder) and restart the desktop app:

- **Global plugins**
  - **macOS/Linux**: `~/.config/opencode/plugins/`
  - **Windows**: Press `WIN+R` and paste `%USERPROFILE%\.config\opencode\plugins`
- **Project plugins** (only if you use per-project config)
  - `<your-project>/.opencode/plugins/`

If the app starts working again, re-enable plugins one at a time to find which one is causing the issue.


### Fix server connection issues

OpenCode Desktop can either start its own local server (default) or connect to a server URL you configured.

If you see a **"Connection Failed"** dialog (or the app never gets past the splash screen), check for a custom server URL.

#### Clear the desktop default server URL

From the Home screen, click the server name (with the status dot) to open the Server picker. In the **Default server** section, click **Clear**.

#### Remove `server.port` / `server.hostname` from your config

If your `opencode.json(c)` contains a `server` section, temporarily remove it and restart the desktop app.

#### Check environment variables

If you have `OPENCODE_PORT` set in your environment, the desktop app will try to use that port for the local server.

- Unset `OPENCODE_PORT` (or pick a free port) and restart.


### Windows: WebView2 runtime

On Windows, OpenCode Desktop requires the Microsoft Edge **WebView2 Runtime**. If the app opens to a blank window or won't start, install/update WebView2 and try again.


### Notifications not showing

OpenCode Desktop only shows system notifications when:

- notifications are enabled for OpenCode in your OS settings, and
- the app window is not focused.


## Getting help

If you're experiencing issues with OpenCode:

1. **Report issues on GitHub**

   The best way to report bugs or request features is through our GitHub repository:

   [**github.com/anomalyco/opencode/issues**](https://github.com/anomalyco/opencode/issues)

   Before creating a new issue, search existing issues to see if your problem has already been reported.

2. **Join our Discord**

   For real-time help and community discussion, join our Discord server:

   [**opencode.ai/discord**](https://opencode.ai/discord)


### OpenCode won't start

1. Check the logs for error messages
2. Try running with `--print-logs` to see output in the terminal
3. Ensure you have the latest version with `opencode upgrade`


### Model not available

1. Check that you've authenticated with the provider
2. Verify the model name in your config is correct
3. Some models may require specific access or subscriptions

If you encounter `ProviderModelNotFoundError` you are most likely incorrectly
referencing a model somewhere.
Models should be referenced like so: `<providerId>/<modelId>`

Examples:

- `openai/gpt-4.1`
- `openrouter/google/gemini-2.5-flash`
- `opencode/kimi-k2`

To figure out what models you have access to, run `opencode models`


### AI_APICallError and provider package issues

If you encounter API call errors, this may be due to outdated provider packages. opencode dynamically installs provider packages (OpenAI, Anthropic, Google, etc.) as needed and caches them locally.

To resolve provider package issues:

1. Clear the provider package cache:

   ```bash
   rm -rf ~/.cache/opencode
   ```

   On Windows, press `WIN+R` and delete: `%USERPROFILE%\.cache\opencode`

2. Restart opencode to reinstall the latest provider packages

This will force opencode to download the most recent versions of provider packages, which often resolves compatibility issues with model parameters and API changes.
