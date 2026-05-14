OpenCode automatically formats files after they are written or edited using language-specific formatters. This ensures that the code that is generated follows the code styles of your project.


## How it works

When OpenCode writes or edits a file, it:

1. Checks the file extension against all enabled formatters.
2. Runs the appropriate formatter command on the file.
3. Applies the formatting changes automatically.

This process happens in the background, ensuring your code styles are maintained without any manual steps.


### Disabling formatters

To disable **all** formatters globally, set `formatter` to `false`:

```json title="opencode.json" {3}
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": false
}
```

To disable a **specific** formatter, set `disabled` to `true`:

```json title="opencode.json" {5}
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": {
    "prettier": {
      "disabled": true
    }
  }
}
```
