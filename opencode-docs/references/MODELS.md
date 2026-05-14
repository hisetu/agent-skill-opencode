OpenCode uses the [AI SDK](https://ai-sdk.dev/) and [Models.dev](https://models.dev) to support **75+ LLM providers** and it supports running local models.


## Select a model

Once you've configured your provider you can select the model you want by typing in:

```bash frame="none"
/models
```


## Set a default

To set one of these as the default model, you can set the `model` key in your
OpenCode config.

```json title="opencode.json" {3}
{
  "$schema": "https://opencode.ai/config.json",
  "model": "lmstudio/google/gemma-3n-e4b"
}
```

Here the full ID is `provider_id/model_id`. For example, if you're using [OpenCode Zen](/docs/zen), you would use `opencode/gpt-5.1-codex` for GPT 5.1 Codex.

If you've configured a [custom provider](/docs/providers#custom), the `provider_id` is key from the `provider` part of your config, and the `model_id` is the key from `provider.models`.


## Variants

Many models support multiple variants with different configurations. OpenCode ships with built-in default variants for popular providers.

### Built-in variants

OpenCode ships with default variants for many providers:

**Anthropic**:

- `high` - High thinking budget (default)
- `max` - Maximum thinking budget

**OpenAI**:

Varies by model but roughly:

- `none` - No reasoning
- `minimal` - Minimal reasoning effort
- `low` - Low reasoning effort
- `medium` - Medium reasoning effort
- `high` - High reasoning effort
- `xhigh` - Extra high reasoning effort

**Google**:

- `low` - Lower effort/token budget
- `high` - Higher effort/token budget

:::tip
This list is not comprehensive. Many other providers have built-in defaults too.
:::

### Custom variants

You can override existing variants or add your own:

```jsonc title="opencode.jsonc" {7-18}
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "openai": {
      "models": {
        "gpt-5": {
          "variants": {
            "thinking": {
              "reasoningEffort": "high",
              "textVerbosity": "low",
            },
            "fast": {
              "disabled": true,
            },
          },
        },
      },
    },
  },
}
```

### Cycle variants

Use the keybind `variant_cycle` to quickly switch between variants. [Learn more](/docs/keybinds).
