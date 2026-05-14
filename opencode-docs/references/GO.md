export const console = config.console
export const email = `mailto:${config.email}`

OpenCode Go is a low cost subscription — **$5 for your first month**, then **$10/month** — that gives you reliable access to popular open coding models.

:::note
OpenCode Go is currently in beta.
:::

Go works like any other provider in OpenCode. You subscribe to OpenCode Go and
get your API key. It's **completely optional** and you don't need to use it to
use OpenCode.

It is designed primarily for international users, with models hosted in the US, EU, and Singapore for stable global access.


## How it works

OpenCode Go works like any other provider in OpenCode.

1. You sign in to **<a href={console}>OpenCode Zen</a>**, subscribe to Go, and
   copy your API key.
2. You run the `/connect` command in the TUI, select `OpenCode Go`, and paste
   your API key.
3. Run `/models` in the TUI to see the list of models available through Go.

:::note
Only one member per workspace can subscribe to OpenCode Go.
:::

The current list of models includes:

- **GLM-5**
- **Kimi K2.5**
- **MiniMax M2.5**
- **MiniMax M2.7**

The list of models may change as we test and add new ones.


### Usage beyond limits

If you also have credits on your Zen balance, you can enable the **Use balance**
option in the console. When enabled, Go will fall back to your Zen balance
after you've reached your usage limits instead of blocking requests.


## Privacy

The plan is designed primarily for international users, with models hosted in the US, EU, and Singapore for stable global access.

<a href={email}>Contact us</a> if you have any questions.
