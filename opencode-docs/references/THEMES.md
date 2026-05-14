With OpenCode you can select from one of several built-in themes, use a theme that adapts to your terminal theme, or define your own custom theme.

By default, OpenCode uses our own `opencode` theme.


## Built-in themes

OpenCode comes with several built-in themes.

| Name                   | Description                                                                  |
| ---------------------- | ---------------------------------------------------------------------------- |
| `system`               | Adapts to your terminal’s background color                                   |
| `tokyonight`           | Based on the [Tokyonight](https://github.com/folke/tokyonight.nvim) theme    |
| `everforest`           | Based on the [Everforest](https://github.com/sainnhe/everforest) theme       |
| `ayu`                  | Based on the [Ayu](https://github.com/ayu-theme) dark theme                  |
| `catppuccin`           | Based on the [Catppuccin](https://github.com/catppuccin) theme               |
| `catppuccin-macchiato` | Based on the [Catppuccin](https://github.com/catppuccin) theme               |
| `gruvbox`              | Based on the [Gruvbox](https://github.com/morhetz/gruvbox) theme             |
| `kanagawa`             | Based on the [Kanagawa](https://github.com/rebelot/kanagawa.nvim) theme      |
| `nord`                 | Based on the [Nord](https://github.com/nordtheme/nord) theme                 |
| `matrix`               | Hacker-style green on black theme                                            |
| `one-dark`             | Based on the [Atom One](https://github.com/Th3Whit3Wolf/one-nvim) Dark theme |

And more, we are constantly adding new themes.


## Using a theme

You can select a theme by bringing up the theme select with the `/theme` command. Or you can specify it in `tui.json`.

```json title="tui.json" {3}
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "tokyonight"
}
```


### Hierarchy

Themes are loaded from multiple directories in the following order where later directories override earlier ones:

1. **Built-in themes** - These are embedded in the binary
2. **User config directory** - Defined in `~/.config/opencode/themes/*.json` or `$XDG_CONFIG_HOME/opencode/themes/*.json`
3. **Project root directory** - Defined in the `<project-root>/.opencode/themes/*.json`
4. **Current working directory** - Defined in `./.opencode/themes/*.json`

If multiple directories contain a theme with the same name, the theme from the directory with higher priority will be used.


### JSON format

Themes use a flexible JSON format with support for:

- **Hex colors**: `"#ffffff"`
- **ANSI colors**: `3` (0-255)
- **Color references**: `"primary"` or custom definitions
- **Dark/light variants**: `{"dark": "#000", "light": "#fff"}`
- **No color**: `"none"` - Uses the terminal's default color or transparent


### Terminal defaults

The special value `"none"` can be used for any color to inherit the terminal's default color. This is particularly useful for creating themes that blend seamlessly with your terminal's color scheme:

- `"text": "none"` - Uses terminal's default foreground color
- `"background": "none"` - Uses terminal's default background color
