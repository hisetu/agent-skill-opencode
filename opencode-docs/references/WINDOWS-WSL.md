While OpenCode can run directly on Windows, we recommend using [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) for the best experience. WSL provides a Linux environment that works seamlessly with OpenCode's features.

:::tip[Why WSL?]
WSL offers better file system performance, full terminal support, and compatibility with development tools that OpenCode relies on.
:::


## Desktop App + WSL Server

If you prefer using the OpenCode Desktop app but want to run the server in WSL:

1. **Start the server in WSL** with `--hostname 0.0.0.0` to allow external connections:

   ```bash
   opencode serve --hostname 0.0.0.0 --port 4096
   ```

2. **Connect the Desktop app** to `http://localhost:4096`

:::note
If `localhost` does not work in your setup, connect using the WSL IP address instead (from WSL: `hostname -I`) and use `http://<wsl-ip>:4096`.
:::

:::caution
When using `--hostname 0.0.0.0`, set `OPENCODE_SERVER_PASSWORD` to secure the server.
:::

```bash
OPENCODE_SERVER_PASSWORD=your-password opencode serve --hostname 0.0.0.0
```


## Accessing Windows Files

WSL can access all your Windows files through the `/mnt/` directory:

- `C:` drive → `/mnt/c/`
- `D:` drive → `/mnt/d/`
- And so on...

Example:

```bash
cd /mnt/c/Users/YourName/Documents/project
opencode
```

:::tip
For the smoothest experience, consider cloning/copying your repo into the WSL filesystem (for example under `~/code/`) and running OpenCode there.
:::
