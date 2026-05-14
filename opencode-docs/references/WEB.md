OpenCode can run as a web application in your browser, providing the same powerful AI coding experience without needing a terminal.

![OpenCode Web - New Session](../../assets/web/web-homepage-new-session.png)

## Getting Started

Start the web interface by running:

```bash
opencode web
```

This starts a local server on `127.0.0.1` with a random available port and automatically opens OpenCode in your default browser.

:::caution
If `OPENCODE_SERVER_PASSWORD` is not set, the server will be unsecured. This is fine for local use but should be set for network access.
:::

:::tip[Windows Users]
For the best experience, run `opencode web` from [WSL](/docs/windows-wsl) rather than PowerShell. This ensures proper file system access and terminal integration.
:::


## Using the Web Interface

Once started, the web interface provides access to your OpenCode sessions.

### Sessions

View and manage your sessions from the homepage. You can see active sessions and start new ones.

![OpenCode Web - Active Session](../../assets/web/web-homepage-active-session.png)

### Server Status

Click "See Servers" to view connected servers and their status.

![OpenCode Web - See Servers](../../assets/web/web-homepage-see-servers.png)


## Config File

You can also configure server settings in your `opencode.json` config file:

```json
{
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0",
    "mdns": true,
    "cors": ["https://example.com"]
  }
}
```

Command line flags take precedence over config file settings.
