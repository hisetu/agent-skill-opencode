OpenCode's share feature allows you to create public links to your OpenCode conversations, so you can collaborate with teammates or get help from others.

:::note
Shared conversations are publicly accessible to anyone with the link.
:::


## Sharing

OpenCode supports three sharing modes that control how conversations are shared:


### Auto-share

You can enable automatic sharing for all new conversations by setting the `share` option to `"auto"` in your [config file](/docs/config):

```json title="opencode.json"
{
  "$schema": "https://opencode.ai/config.json",
  "share": "auto"
}
```

With auto-share enabled, every new conversation will automatically be shared and a link will be generated.


## Un-sharing

To stop sharing a conversation and remove it from public access:

```
/unshare
```

This will remove the share link and delete the data related to the conversation.


### Data retention

Shared conversations remain accessible until you explicitly unshare them. This
includes:

- Full conversation history
- All messages and responses
- Session metadata


## For enterprises

For enterprise deployments, the share feature can be:

- **Disabled** entirely for security compliance
- **Restricted** to users authenticated through SSO only
- **Self-hosted** on your own infrastructure

[Learn more](/docs/enterprise) about using opencode in your organization.
