OpenCode supports standard proxy environment variables and custom certificates for enterprise network environments.


### Authenticate

If your proxy requires basic authentication, include credentials in the URL.

```bash
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

:::caution
Avoid hardcoding passwords. Use environment variables or secure credential storage.
:::

For proxies requiring advanced authentication like NTLM or Kerberos, consider using an LLM Gateway that supports your authentication method.
