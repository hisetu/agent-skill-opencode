export const console = config.console

[**OpenCode**](/) is an open source AI coding agent. It's available as a terminal-based interface, desktop app, or IDE extension.

![OpenCode TUI with the opencode theme](../../assets/lander/screenshot.png)

Let's get started.


## Install

The easiest way to install OpenCode is through the install script.

```bash
curl -fsSL https://opencode.ai/install | bash
```

You can also install it with the following commands:

- **Using Node.js**

        

      
      ```bash
      npm install -g opencode-ai
      ```

          

        
        ```bash
        bun install -g opencode-ai
        ```

          

        
        ```bash
        pnpm install -g opencode-ai
        ```

          

        
        ```bash
        yarn global add opencode-ai
        ```

      

  

- **Using Homebrew on macOS and Linux**

  ```bash
  brew install anomalyco/tap/opencode
  ```

  > We recommend using the OpenCode tap for the most up to date releases. The official `brew install opencode` formula is maintained by the Homebrew team and is updated less frequently.

- **Installing on Arch Linux**

  ```bash
  sudo pacman -S opencode           # Arch Linux (Stable)
  paru -S opencode-bin              # Arch Linux (Latest from AUR)
  ```

#### Windows

:::tip[Recommended: Use WSL]
For the best experience on Windows, we recommend using [Windows Subsystem for Linux (WSL)](/docs/windows-wsl). It provides better performance and full compatibility with OpenCode's features.
:::

- **Using Chocolatey**

  ```bash
  choco install opencode
  ```

- **Using Scoop**

  ```bash
  scoop install opencode
  ```

- **Using NPM**

  ```bash
  npm install -g opencode-ai
  ```

- **Using Mise**

  ```bash
  mise use -g github:anomalyco/opencode
  ```

- **Using Docker**

  ```bash
  docker run -it --rm ghcr.io/anomalyco/opencode
  ```

Support for installing OpenCode on Windows using Bun is currently in progress.

You can also grab the binary from the [Releases](https://github.com/anomalyco/opencode/releases).


## Initialize

Now that you've configured a provider, you can navigate to a project that
you want to work on.

```bash
cd /path/to/project
```

And run OpenCode.

```bash
opencode
```

Next, initialize OpenCode for the project by running the following command.

```bash frame="none"
/init
```

This will get OpenCode to analyze your project and create an `AGENTS.md` file in
the project root.

:::tip
You should commit your project's `AGENTS.md` file to Git.
:::

This helps OpenCode understand the project structure and the coding patterns
used.


### Ask questions

You can ask OpenCode to explain the codebase to you.

:::tip
Use the `@` key to fuzzy search for files in the project.
:::

```txt frame="none" "@packages/functions/src/api/index.ts"
How is authentication handled in @packages/functions/src/api/index.ts
```

This is helpful if there's a part of the codebase that you didn't work on.


### Make changes

For more straightforward changes, you can ask OpenCode to directly build it
without having to review the plan first.

```txt frame="none" "@packages/functions/src/settings.ts" "@packages/functions/src/notes.ts"
We need to add authentication to the /settings route. Take a look at how this is
handled in the /notes route in @packages/functions/src/notes.ts and implement
the same logic in @packages/functions/src/settings.ts
```

You want to make sure you provide a good amount of detail so OpenCode makes the right
changes.


## Share

The conversations that you have with OpenCode can be [shared with your
team](/docs/share).

```bash frame="none"
/share
```

This will create a link to the current conversation and copy it to your clipboard.

:::note
Conversations are not shared by default.
:::

Here's an [example conversation](https://opencode.ai/s/4XP1fce5) with OpenCode.
