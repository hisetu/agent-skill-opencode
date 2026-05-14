export const console = config.console
export const email = `mailto:${config.email}`

OpenCode Zen is a list of tested and verified models provided by the OpenCode team.

:::note
OpenCode Zen is currently in beta.
:::

Zen works like any other provider in OpenCode. You login to OpenCode Zen and get
your API key. It's **completely optional** and you don't need to use it to use
OpenCode.


## How it works

OpenCode Zen works like any other provider in OpenCode.

1. You sign in to **<a href={console}>OpenCode Zen</a>**, add your billing
   details, and copy your API key.
2. You run the `/connect` command in the TUI, select OpenCode Zen, and paste your API key.
3. Run `/models` in the TUI to see the list of models we recommend.

You are charged per request and you can add credits to your account.


### Models

You can fetch the full list of available models and their metadata from:

```
https://opencode.ai/zen/v1/models
```


### Auto-reload

If your balance goes below $5, Zen will automatically reload $20.

You can change the auto-reload amount. You can also disable auto-reload entirely.


### Deprecated models

| Model            | Deprecation date |
| ---------------- | ---------------- |
| MiniMax M2.1     | March 15, 2026   |
| GLM 4.7          | March 15, 2026   |
| GLM 4.6          | March 15, 2026   |
| Gemini 3 Pro     | March 9, 2026    |
| Kimi K2 Thinking | March 6, 2026    |
| Kimi K2          | March 6, 2026    |
| Qwen3 Coder 480B | Feb 6, 2026      |


## For Teams

Zen also works great for teams. You can invite teammates, assign roles, curate
the models your team uses, and more.

:::note
Workspaces are currently free for teams as a part of the beta.
:::

Managing your workspace is currently free for teams as a part of the beta. We'll be
sharing more details on the pricing soon.


### Model access

Admins can enable or disable specific models for the workspace. Requests made to a disabled model will return an error.

This is useful for cases where you want to disable the use of a model that
collects data.


## Goals

We created OpenCode Zen to:

1. **Benchmark** the best models/providers for coding agents.
2. Have access to the **highest quality** options and not downgrade performance or route to cheaper providers.
3. Pass along any **price drops** by selling at cost; so the only markup is to cover our processing fees.
4. Have **no lock-in** by allowing you to use it with any other coding agent. And always let you use any other provider with OpenCode as well.
