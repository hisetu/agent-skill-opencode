export const console = config.console

OpenCode uses the [AI SDK](https://ai-sdk.dev/) and [Models.dev](https://models.dev) to support **75+ LLM providers** and it supports running local models.

To add a provider you need to:

1. Add the API keys for the provider using the `/connect` command.
2. Configure the provider in your OpenCode config.


### Config

You can customize the providers through the `provider` section in your OpenCode
config.


## OpenCode Zen

OpenCode Zen is a list of models provided by the OpenCode team that have been
tested and verified to work well with OpenCode. [Learn more](/docs/zen).

:::tip
If you are new, we recommend starting with OpenCode Zen.
:::

1. Run the `/connect` command in the TUI, select `OpenCode Zen`, and head to [opencode.ai/auth](https://opencode.ai/zen).

   ```txt
   /connect
   ```

2. Sign in, add your billing details, and copy your API key.

3. Paste your API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run `/models` in the TUI to see the list of models we recommend.

   ```txt
   /models
   ```

It works like any other provider in OpenCode and is completely optional to use.


## Directory

Let's look at some of the providers in detail. If you'd like to add a provider to the
list, feel free to open a PR.

:::note
Don't see a provider here? Submit a PR.
:::


### Amazon Bedrock

To use Amazon Bedrock with OpenCode:

1. Head over to the **Model catalog** in the Amazon Bedrock console and request
   access to the models you want.

   :::tip
   You need to have access to the model you want in Amazon Bedrock.
   :::

2. **Configure authentication** using one of the following methods:

   ***

   #### Environment Variables (Quick Start)

   Set one of these environment variables while running opencode:

   ```bash
   # Option 1: Using AWS access keys
   AWS_ACCESS_KEY_ID=XXX AWS_SECRET_ACCESS_KEY=YYY opencode

   # Option 2: Using named AWS profile
   AWS_PROFILE=my-profile opencode

   # Option 3: Using Bedrock bearer token
   AWS_BEARER_TOKEN_BEDROCK=XXX opencode
   ```

   Or add them to your bash profile:

   ```bash title="~/.bash_profile"
   export AWS_PROFILE=my-dev-profile
   export AWS_REGION=us-east-1
   ```

   ***

   #### Configuration File (Recommended)

   For project-specific or persistent configuration, use `opencode.json`:

   ```json title="opencode.json"
   {
     "$schema": "https://opencode.ai/config.json",
     "provider": {
       "amazon-bedrock": {
         "options": {
           "region": "us-east-1",
           "profile": "my-aws-profile"
         }
       }
     }
   }
   ```

   **Available options:**
   - `region` - AWS region (e.g., `us-east-1`, `eu-west-1`)
   - `profile` - AWS named profile from `~/.aws/credentials`
   - `endpoint` - Custom endpoint URL for VPC endpoints (alias for generic `baseURL` option)

   :::tip
   Configuration file options take precedence over environment variables.
   :::

   ***

   #### Advanced: VPC Endpoints

   If you're using VPC endpoints for Bedrock:

   ```json title="opencode.json"
   {
     "$schema": "https://opencode.ai/config.json",
     "provider": {
       "amazon-bedrock": {
         "options": {
           "region": "us-east-1",
           "profile": "production",
           "endpoint": "https://bedrock-runtime.us-east-1.vpce-xxxxx.amazonaws.com"
         }
       }
     }
   }
   ```

   :::note
   The `endpoint` option is an alias for the generic `baseURL` option, using AWS-specific terminology. If both `endpoint` and `baseURL` are specified, `endpoint` takes precedence.
   :::

   ***

   #### Authentication Methods
   - **`AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`**: Create an IAM user and generate access keys in the AWS Console
   - **`AWS_PROFILE`**: Use named profiles from `~/.aws/credentials`. First configure with `aws configure --profile my-profile` or `aws sso login`
   - **`AWS_BEARER_TOKEN_BEDROCK`**: Generate long-term API keys from the Amazon Bedrock console
   - **`AWS_WEB_IDENTITY_TOKEN_FILE` / `AWS_ROLE_ARN`**: For EKS IRSA (IAM Roles for Service Accounts) or other Kubernetes environments with OIDC federation. These environment variables are automatically injected by Kubernetes when using service account annotations.

   ***

   #### Authentication Precedence

   Amazon Bedrock uses the following authentication priority:
   1. **Bearer Token** - `AWS_BEARER_TOKEN_BEDROCK` environment variable or token from `/connect` command
   2. **AWS Credential Chain** - Profile, access keys, shared credentials, IAM roles, Web Identity Tokens (EKS IRSA), instance metadata

   :::note
   When a bearer token is set (via `/connect` or `AWS_BEARER_TOKEN_BEDROCK`), it takes precedence over all AWS credential methods including configured profiles.
   :::

3. Run the `/models` command to select the model you want.

   ```txt
   /models
   ```

:::note
For custom inference profiles, use the model and provider name in the key and set the `id` property to the arn. This ensures correct caching.
:::

```json title="opencode.json"
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "amazon-bedrock": {
      // ...
      "models": {
        "anthropic-claude-sonnet-4.5": {
          "id": "arn:aws:bedrock:us-east-1:xxx:application-inference-profile/yyy"
        }
      }
    }
  }
}
```


### Azure OpenAI

:::note
If you encounter "I'm sorry, but I cannot assist with that request" errors, try changing the content filter from **DefaultV2** to **Default** in your Azure resource.
:::

1. Head over to the [Azure portal](https://portal.azure.com/) and create an **Azure OpenAI** resource. You'll need:
   - **Resource name**: This becomes part of your API endpoint (`https://RESOURCE_NAME.openai.azure.com/`)
   - **API key**: Either `KEY 1` or `KEY 2` from your resource

2. Go to [Azure AI Foundry](https://ai.azure.com/) and deploy a model.

   :::note
   The deployment name must match the model name for opencode to work properly.
   :::

3. Run the `/connect` command and search for **Azure**.

   ```txt
   /connect
   ```

4. Enter your API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

5. Set your resource name as an environment variable:

   ```bash
   AZURE_RESOURCE_NAME=XXX opencode
   ```

   Or add it to your bash profile:

   ```bash title="~/.bash_profile"
   export AZURE_RESOURCE_NAME=XXX
   ```

6. Run the `/models` command to select your deployed model.

   ```txt
   /models
   ```


### Baseten

1. Head over to the [Baseten](https://app.baseten.co/), create an account, and generate an API key.

2. Run the `/connect` command and search for **Baseten**.

   ```txt
   /connect
   ```

3. Enter your Baseten API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select a model.

   ```txt
   /models
   ```


### Cloudflare AI Gateway

Cloudflare AI Gateway lets you access models from OpenAI, Anthropic, Workers AI, and more through a unified endpoint. With [Unified Billing](https://developers.cloudflare.com/ai-gateway/features/unified-billing/) you don't need separate API keys for each provider.

1. Head over to the [Cloudflare dashboard](https://dash.cloudflare.com/), navigate to **AI** > **AI Gateway**, and create a new gateway.

2. Set your Account ID and Gateway ID as environment variables.

   ```bash title="~/.bash_profile"
   export CLOUDFLARE_ACCOUNT_ID=your-32-character-account-id
   export CLOUDFLARE_GATEWAY_ID=your-gateway-id
   ```

3. Run the `/connect` command and search for **Cloudflare AI Gateway**.

   ```txt
   /connect
   ```

4. Enter your Cloudflare API token.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

   Or set it as an environment variable.

   ```bash title="~/.bash_profile"
   export CLOUDFLARE_API_TOKEN=your-api-token
   ```

5. Run the `/models` command to select a model.

   ```txt
   /models
   ```

   You can also add models through your opencode config.

   ```json title="opencode.json"
   {
     "$schema": "https://opencode.ai/config.json",
     "provider": {
       "cloudflare-ai-gateway": {
         "models": {
           "openai/gpt-4o": {},
           "anthropic/claude-sonnet-4": {}
         }
       }
     }
   }
   ```


### Cortecs

1. Head over to the [Cortecs console](https://cortecs.ai/), create an account, and generate an API key.

2. Run the `/connect` command and search for **Cortecs**.

   ```txt
   /connect
   ```

3. Enter your Cortecs API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select a model like _Kimi K2 Instruct_.

   ```txt
   /models
   ```


### Deep Infra

1. Head over to the [Deep Infra dashboard](https://deepinfra.com/dash), create an account, and generate an API key.

2. Run the `/connect` command and search for **Deep Infra**.

   ```txt
   /connect
   ```

3. Enter your Deep Infra API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select a model.

   ```txt
   /models
   ```


### Fireworks AI

1. Head over to the [Fireworks AI console](https://app.fireworks.ai/), create an account, and click **Create API Key**.

2. Run the `/connect` command and search for **Fireworks AI**.

   ```txt
   /connect
   ```

3. Enter your Fireworks AI API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select a model like _Kimi K2 Instruct_.

   ```txt
   /models
   ```


### GitHub Copilot

To use your GitHub Copilot subscription with opencode:

:::note
Some models might need a [Pro+
subscription](https://github.com/features/copilot/plans) to use.
:::

1. Run the `/connect` command and search for GitHub Copilot.

   ```txt
   /connect
   ```

2. Navigate to [github.com/login/device](https://github.com/login/device) and enter the code.

   ```txt
   ┌ Login with GitHub Copilot
   │
   │ https://github.com/login/device
   │
   │ Enter code: 8F43-6FCF
   │
   └ Waiting for authorization...
   ```

3. Now run the `/models` command to select the model you want.

   ```txt
   /models
   ```


### Groq

1. Head over to the [Groq console](https://console.groq.com/), click **Create API Key**, and copy the key.

2. Run the `/connect` command and search for Groq.

   ```txt
   /connect
   ```

3. Enter the API key for the provider.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select the one you want.

   ```txt
   /models
   ```


### Helicone

[Helicone](https://helicone.ai) is an LLM observability platform that provides logging, monitoring, and analytics for your AI applications. The Helicone AI Gateway routes your requests to the appropriate provider automatically based on the model.

1. Head over to [Helicone](https://helicone.ai), create an account, and generate an API key from your dashboard.

2. Run the `/connect` command and search for **Helicone**.

   ```txt
   /connect
   ```

3. Enter your Helicone API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select a model.

   ```txt
   /models
   ```

For more providers and advanced features like caching and rate limiting, check the [Helicone documentation](https://docs.helicone.ai).

#### Optional Configs

In the event you see a feature or model from Helicone that isn't configured automatically through opencode, you can always configure it yourself.

Here's [Helicone's Model Directory](https://helicone.ai/models), you'll need this to grab the IDs of the models you want to add.

```jsonc title="~/.config/opencode/opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "helicone": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Helicone",
      "options": {
        "baseURL": "https://ai-gateway.helicone.ai",
      },
      "models": {
        "gpt-4o": {
          // Model ID (from Helicone's model directory page)
          "name": "GPT-4o", // Your own custom name for the model
        },
        "claude-sonnet-4-20250514": {
          "name": "Claude Sonnet 4",
        },
      },
    },
  },
}
```

#### Custom Headers

Helicone supports custom headers for features like caching, user tracking, and session management. Add them to your provider config using `options.headers`:

```jsonc title="~/.config/opencode/opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "helicone": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Helicone",
      "options": {
        "baseURL": "https://ai-gateway.helicone.ai",
        "headers": {
          "Helicone-Cache-Enabled": "true",
          "Helicone-User-Id": "opencode",
        },
      },
    },
  },
}
```

##### Session tracking

Helicone's [Sessions](https://docs.helicone.ai/features/sessions) feature lets you group related LLM requests together. Use the [opencode-helicone-session](https://github.com/H2Shami/opencode-helicone-session) plugin to automatically log each OpenCode conversation as a session in Helicone.

```bash
npm install -g opencode-helicone-session
```

Add it to your config.

```json title="opencode.json"
{
  "plugin": ["opencode-helicone-session"]
}
```

The plugin injects `Helicone-Session-Id` and `Helicone-Session-Name` headers into your requests. In Helicone's Sessions page, you'll see each OpenCode conversation listed as a separate session.

##### Common Helicone headers

| Header                     | Description                                                   |
| -------------------------- | ------------------------------------------------------------- |
| `Helicone-Cache-Enabled`   | Enable response caching (`true`/`false`)                      |
| `Helicone-User-Id`         | Track metrics by user                                         |
| `Helicone-Property-[Name]` | Add custom properties (e.g., `Helicone-Property-Environment`) |
| `Helicone-Prompt-Id`       | Associate requests with prompt versions                       |

See the [Helicone Header Directory](https://docs.helicone.ai/helicone-headers/header-directory) for all available headers.


### IO.NET

IO.NET offers 17 models optimized for various use cases:

1. Head over to the [IO.NET console](https://ai.io.net/), create an account, and generate an API key.

2. Run the `/connect` command and search for **IO.NET**.

   ```txt
   /connect
   ```

3. Enter your IO.NET API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select a model.

   ```txt
   /models
   ```


### Moonshot AI

To use Kimi K2 from Moonshot AI:

1. Head over to the [Moonshot AI console](https://platform.moonshot.ai/console), create an account, and click **Create API key**.

2. Run the `/connect` command and search for **Moonshot AI**.

   ```txt
   /connect
   ```

3. Enter your Moonshot API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select _Kimi K2_.

   ```txt
   /models
   ```


### Nebius Token Factory

1. Head over to the [Nebius Token Factory console](https://tokenfactory.nebius.com/), create an account, and click **Add Key**.

2. Run the `/connect` command and search for **Nebius Token Factory**.

   ```txt
   /connect
   ```

3. Enter your Nebius Token Factory API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select a model like _Kimi K2 Instruct_.

   ```txt
   /models
   ```


### Ollama Cloud

To use Ollama Cloud with OpenCode:

1. Head over to [https://ollama.com/](https://ollama.com/) and sign in or create an account.

2. Navigate to **Settings** > **Keys** and click **Add API Key** to generate a new API key.

3. Copy the API key for use in OpenCode.

4. Run the `/connect` command and search for **Ollama Cloud**.

   ```txt
   /connect
   ```

5. Enter your Ollama Cloud API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

6. **Important**: Before using cloud models in OpenCode, you must pull the model information locally:

   ```bash
   ollama pull gpt-oss:20b-cloud
   ```

7. Run the `/models` command to select your Ollama Cloud model.

   ```txt
   /models
   ```


### OpenCode Zen

OpenCode Zen is a list of tested and verified models provided by the OpenCode team. [Learn more](/docs/zen).

1. Sign in to **<a href={console}>OpenCode Zen</a>** and click **Create API Key**.

2. Run the `/connect` command and search for **OpenCode Zen**.

   ```txt
   /connect
   ```

3. Enter your OpenCode API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select a model like _Qwen 3 Coder 480B_.

   ```txt
   /models
   ```


### SAP AI Core

SAP AI Core provides access to 40+ models from OpenAI, Anthropic, Google, Amazon, Meta, Mistral, and AI21 through a unified platform.

1. Go to your [SAP BTP Cockpit](https://account.hana.ondemand.com/), navigate to your SAP AI Core service instance, and create a service key.

   :::tip
   The service key is a JSON object containing `clientid`, `clientsecret`, `url`, and `serviceurls.AI_API_URL`. You can find your AI Core instance under **Services** > **Instances and Subscriptions** in the BTP Cockpit.
   :::

2. Run the `/connect` command and search for **SAP AI Core**.

   ```txt
   /connect
   ```

3. Enter your service key JSON.

   ```txt
   ┌ Service key
   │
   │
   └ enter
   ```

   Or set the `AICORE_SERVICE_KEY` environment variable:

   ```bash
   AICORE_SERVICE_KEY='{"clientid":"...","clientsecret":"...","url":"...","serviceurls":{"AI_API_URL":"..."}}' opencode
   ```

   Or add it to your bash profile:

   ```bash title="~/.bash_profile"
   export AICORE_SERVICE_KEY='{"clientid":"...","clientsecret":"...","url":"...","serviceurls":{"AI_API_URL":"..."}}'
   ```

4. Optionally set deployment ID and resource group:

   ```bash
   AICORE_DEPLOYMENT_ID=your-deployment-id AICORE_RESOURCE_GROUP=your-resource-group opencode
   ```

   :::note
   These settings are optional and should be configured according to your SAP AI Core setup.
   :::

5. Run the `/models` command to select from 40+ available models.

   ```txt
   /models
   ```


### OVHcloud AI Endpoints

1. Head over to the [OVHcloud panel](https://ovh.com/manager). Navigate to the `Public Cloud` section, `AI & Machine Learning` > `AI Endpoints` and in `API Keys` tab, click **Create a new API key**.

2. Run the `/connect` command and search for **OVHcloud AI Endpoints**.

   ```txt
   /connect
   ```

3. Enter your OVHcloud AI Endpoints API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select a model like _gpt-oss-120b_.

   ```txt
   /models
   ```


### Together AI

1. Head over to the [Together AI console](https://api.together.ai), create an account, and click **Add Key**.

2. Run the `/connect` command and search for **Together AI**.

   ```txt
   /connect
   ```

3. Enter your Together AI API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select a model like _Kimi K2 Instruct_.

   ```txt
   /models
   ```


### Vercel AI Gateway

Vercel AI Gateway lets you access models from OpenAI, Anthropic, Google, xAI, and more through a unified endpoint. Models are offered at list price with no markup.

1. Head over to the [Vercel dashboard](https://vercel.com/), navigate to the **AI Gateway** tab, and click **API keys** to create a new API key.

2. Run the `/connect` command and search for **Vercel AI Gateway**.

   ```txt
   /connect
   ```

3. Enter your Vercel AI Gateway API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select a model.

   ```txt
   /models
   ```

You can also customize models through your opencode config. Here's an example of specifying provider routing order.

```json title="opencode.json"
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "vercel": {
      "models": {
        "anthropic/claude-sonnet-4": {
          "options": {
            "order": ["anthropic", "vertex"]
          }
        }
      }
    }
  }
}
```

Some useful routing options:

| Option              | Description                                          |
| ------------------- | ---------------------------------------------------- |
| `order`             | Provider sequence to try                             |
| `only`              | Restrict to specific providers                       |
| `zeroDataRetention` | Only use providers with zero data retention policies |


### Z.AI

1. Head over to the [Z.AI API console](https://z.ai/manage-apikey/apikey-list), create an account, and click **Create a new API key**.

2. Run the `/connect` command and search for **Z.AI**.

   ```txt
   /connect
   ```

   If you are subscribed to the **GLM Coding Plan**, select **Z.AI Coding Plan**.

3. Enter your Z.AI API key.

   ```txt
   ┌ API key
   │
   │
   └ enter
   ```

4. Run the `/models` command to select a model like _GLM-4.7_.

   ```txt
   /models
   ```


## Custom provider

To add any **OpenAI-compatible** provider that's not listed in the `/connect` command:

:::tip
You can use any OpenAI-compatible provider with opencode. Most modern AI providers offer OpenAI-compatible APIs.
:::

1. Run the `/connect` command and scroll down to **Other**.

   ```bash
   $ /connect

   ┌  Add credential
   │
   ◆  Select provider
   │  ...
   │  ● Other
   └
   ```

2. Enter a unique ID for the provider.

   ```bash
   $ /connect

   ┌  Add credential
   │
   ◇  Enter provider id
   │  myprovider
   └
   ```

   :::note
   Choose a memorable ID, you'll use this in your config file.
   :::

3. Enter your API key for the provider.

   ```bash
   $ /connect

   ┌  Add credential
   │
   ▲  This only stores a credential for myprovider - you will need to configure it in opencode.json, check the docs for examples.
   │
   ◇  Enter your API key
   │  sk-...
   └
   ```

4. Create or update your `opencode.json` file in your project directory:

   ```json title="opencode.json" ""myprovider"" {5-15}
   {
     "$schema": "https://opencode.ai/config.json",
     "provider": {
       "myprovider": {
         "npm": "@ai-sdk/openai-compatible",
         "name": "My AI ProviderDisplay Name",
         "options": {
           "baseURL": "https://api.myprovider.com/v1"
         },
         "models": {
           "my-model-name": {
             "name": "My Model Display Name"
           }
         }
       }
     }
   }
   ```

   Here are the configuration options:
   - **npm**: AI SDK package to use, `@ai-sdk/openai-compatible` for OpenAI-compatible providers (for `/v1/chat/completions`). If your provider/model uses `/v1/responses`, use `@ai-sdk/openai`.
   - **name**: Display name in UI.
   - **models**: Available models.
   - **options.baseURL**: API endpoint URL.
   - **options.apiKey**: Optionally set the API key, if not using auth.
   - **options.headers**: Optionally set custom headers.

   More on the advanced options in the example below.

5. Run the `/models` command and your custom provider and models will appear in the selection list.


## Troubleshooting

If you are having trouble with configuring a provider, check the following:

1. **Check the auth setup**: Run `opencode auth list` to see if the credentials
   for the provider are added to your config.

   This doesn't apply to providers like Amazon Bedrock, that rely on environment variables for their auth.

2. For custom providers, check the opencode config and:
   - Make sure the provider ID used in the `/connect` command matches the ID in your opencode config.
   - The right npm package is used for the provider. For example, use `@ai-sdk/cerebras` for Cerebras. And for all other OpenAI-compatible providers, use `@ai-sdk/openai-compatible` (for `/v1/chat/completions`); if a model uses `/v1/responses`, use `@ai-sdk/openai`. For mixed setups under one provider, you can override per model via `provider.npm`.
   - Check correct API endpoint is used in the `options.baseURL` field.
