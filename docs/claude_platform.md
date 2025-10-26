# [Claude Platform](https://docs.claude.com/en/docs/intro)

## [Get started with Claude](https://docs.claude.com/en/docs/get-started)

### Prerequisites
- An Anthropic Console account
- An API key

### Call the API via cURL

- Set your API key: `export ANTHROPIC_API_KEY='your-api-key-here'`
- Make your first API call:

```bash
curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1000,
    "messages": [
      {
        "role": "user", 
        "content": "What should I search for to find the latest developments in renewable energy?"
      }
    ]
  }'
```

### Call the API via Python

- Set your API key: `export ANTHROPIC_API_KEY='your-api-key-here'`
- Install the Anthropic Python SDK: `pip install anthropic`
- Create `Quickstart.py`

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What should I search for to find the latest developments in renewable energy?"
        }
    ]
)
print(message.content)
```
- Run your code: `python quickstart.py`

### Call the API via Java

- Set your API key: `export ANTHROPIC_API_KEY='your-api-key-here'`
- Install [Anthropic Maven Package](https://central.sonatype.com/artifact/com.anthropic/anthropic-java)

```
<dependency>
    <groupId>com.anthropic</groupId>
    <artifactId>anthropic-java</artifactId>
    <version>2.9.0</version>
</dependency>
```
- Create `Quickstart.java`:

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;

public class QuickStart {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
                .model("claude-sonnet-4-5-20250929")
                .maxTokens(1000)
                .addUserMessage("What should I search for to find the latest developments in renewable energy?")
                .build();

        Message message = client.messages().create(params);
        System.out.println(message.content());
    }
}
```
- Run your code:

```bash
javac QuickStart.java
java QuickStart
```

## Capabilities

### [1. Context Windows](https://docs.claude.com/en/docs/build-with-claude/context-windows)

The “context window” refers to the entirety of the amount of text a language model can look back on and reference when generating new text plus the new text it generates. 

- Default mode: 200K tokens
- Beta mode (with special header + tier 4): 1M tokens

<table>
<tr>
<td width="50%">

**Python**
```python
from anthropic import Anthropic

client = Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Process this large document..."}
    ],
    betas=["context-1m-2025-08-07"]
)
```

</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: context-1m-2025-08-07" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Process this large document..."}
    ]
  }'
```

</td>
</tr>
</table>

### [2. Prompt Caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system=[
      {
        "type": "text",
        "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
      },
      {
        "type": "text",
        "text": "<the entire contents of 'Pride and Prejudice'>",
        "cache_control": {"type": "ephemeral"}
      }
    ],
    messages=[{"role": "user", "content": "Analyze the major themes in 'Pride and Prejudice'."}],
)
print(response.usage.model_dump_json())

# Call the model again with the same inputs up to the cache checkpoint
response = client.messages.create(.....)
print(response.usage.model_dump_json())
```

</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "system": [
      {
        "type": "text",
        "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
      },
      {
        "type": "text",
        "text": "<the entire contents of Pride and Prejudice>",
        "cache_control": {"type": "ephemeral"}
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "Analyze the major themes in Pride and Prejudice."
      }
    ]
  }'

# Call the model again with the same inputs up to the cache checkpoint
curl https://api.anthropic.com/v1/messages # rest of input
```

</td>
</tr>
</table>

### [3. Context Editing](https://docs.claude.com/en/docs/build-with-claude/context-editing)

Automatically manage conversation context as it grows with context editing. The simplest way to enable context editing is to specify only the strategy type, as all other configuration options will use their default values:

<table>
<tr>
<td width="50%">

**Python**
```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Search for recent developments in AI"
        }
    ],
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search"
        }
    ],
    betas=["context-management-2025-06-27"],
    context_management={
        "edits": [
            {"type": "clear_tool_uses_20250919"}
        ]
    }
)
```

</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-sonnet-4-5",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": "Search for recent developments in AI"
            }
        ],
        "tools": [
            {
                "type": "web_search_20250305",
                "name": "web_search"
            }
        ],
        "context_management": {
            "edits": [
                {"type": "clear_tool_uses_20250919"}
            ]
        }
    }'
```

</td>
</tr>
</table>

You can customize the context editing behavior with additional parameters:

<table>
<tr>
<td width="50%">

**Python**
```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Create a simple command line calculator app using Python"
        }
    ],
    tools=[
        {
            "type": "text_editor_20250728",
            "name": "str_replace_based_edit_tool",
            "max_characters": 10000
        },
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 3
        }
    ],
    betas=["context-management-2025-06-27"],
    context_management={
        "edits": [
            {
                "type": "clear_tool_uses_20250919",
                # Trigger clearing when threshold is exceeded
                "trigger": {
                    "type": "input_tokens",
                    "value": 30000
                },
                # Number of tool uses to keep after clearing
                "keep": {
                    "type": "tool_uses",
                    "value": 3
                },
                # Optional: Clear at least this many tokens
                "clear_at_least": {
                    "type": "input_tokens",
                    "value": 5000
                },
                # Exclude these tools from being cleared
                "exclude_tools": ["web_search"]
            }
        ]
    }
)
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-sonnet-4-5",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": "Create a simple command line calculator app using Python"
            }
        ],
        "tools": [
            {
                "type": "text_editor_20250728",
                "name": "str_replace_based_edit_tool",
                "max_characters": 10000
            },
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 3
            }
        ],
        "context_management": {
            "edits": [
                {
                    "type": "clear_tool_uses_20250919",
                    "trigger": {
                        "type": "input_tokens",
                        "value": 30000
                    },
                    "keep": {
                        "type": "tool_uses",
                        "value": 3
                    },
                    "clear_at_least": {
                        "type": "input_tokens",
                        "value": 5000
                    },
                    "exclude_tools": ["web_search"]
                }
            ]
        }
    }'
```
</td>
</tr>
</table>


### [4. Extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking)

Extended thinking gives Claude enhanced reasoning capabilities for complex tasks, while providing varying levels of transparency into its step-by-step thought process before it delivers its final answer.

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[{
        "role": "user",
        "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
    }]
)

# The response will contain summarized thinking blocks and text blocks
for block in response.content:
    if block.type == "thinking":
        print(f"\nThinking summary: {block.thinking}")
    elif block.type == "text":
        print(f"\nResponse: {block.text}")
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-5",
    "max_tokens": 16000,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 10000
    },
    "messages": [
        {
            "role": "user",
            "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
        }
    ]
}'
```
</td>
</tr>
</table>


You can stream extended thinking responses using server-sent events (SSE). When streaming is enabled for extended thinking, you receive thinking content via thinking_delta events.

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "What is 27 * 453?"}],
) as stream:
    thinking_started = False
    response_started = False

    for event in stream:
        if event.type == "content_block_start":
            print(f"\nStarting {event.content_block.type} block...")
            # Reset flags for each new block
            thinking_started = False
            response_started = False
        elif event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                if not thinking_started:
                    print("Thinking: ", end="", flush=True)
                    thinking_started = True
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                if not response_started:
                    print("Response: ", end="", flush=True)
                    response_started = True
                print(event.delta.text, end="", flush=True)
        elif event.type == "content_block_stop":
            print("\nBlock complete.")
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-5",
    "max_tokens": 16000,
    "stream": true,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 10000
    },
    "messages": [
        {
            "role": "user",
            "content": "What is 27 * 453?"
        }
    ]
}'
```
</td>
</tr>
</table>

### [5. Streaming Messages](https://docs.claude.com/en/docs/build-with-claude/streaming)

Anthropic's Python SDK offers multiple ways of streaming. The Python SDK allows both sync and async streams. See the documentation in each SDK for details.

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=256,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --data \
'{
  "model": "claude-sonnet-4-5",
  "messages": [{"role": "user", "content": "Hello"}],
  "max_tokens": 256,
  "stream": true
}'
```
</td>
</tr>
</table>

In this request, we ask Claude to use a tool to tell us the weather.

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    }
]

with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "any"},
    messages=[
        {
            "role": "user",
            "content": "What is the weather like in San Francisco?"
        }
    ],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-sonnet-4-5",
      "max_tokens": 1024,
      "tools": [
        {
          "name": "get_weather",
          "description": "Get the current weather in a given location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
              }
            },
            "required": ["location"]
          }
        }
      ],
      "tool_choice": {"type": "any"},
      "messages": [
        {
          "role": "user",
          "content": "What is the weather like in San Francisco?"
        }
      ],
      "stream": true
    }'
```
</td>
</tr>
</table>

### [6. Batch processing](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

Batch processing is a powerful approach for handling large volumes of requests efficiently. Instead of processing requests one at a time with immediate responses, batch processing allows you to submit multiple requests together for asynchronous processing. This pattern is particularly useful when:
- You need to process large volumes of data
- Immediate responses are not required
- You want to optimize for cost efficiency
- You’re running large-scale evaluations or analyses

Any request that you can make to the Messages API can be included in a batch. This includes:
- Vision
- Tool use
- System messages
- Multi-turn conversations
- Any beta features

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

client = anthropic.Anthropic()

message_batch = client.messages.batches.create(
    requests=[
        Request(
            custom_id="my-first-request",
            params=MessageCreateParamsNonStreaming(
                model="claude-sonnet-4-5",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": "Hello, world",
                }]
            )
        ),
        Request(
            custom_id="my-second-request",
            params=MessageCreateParamsNonStreaming(
                model="claude-sonnet-4-5",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": "Hi again, friend",
                }]
            )
        )
    ]
)

print(message_batch)
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages/batches \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "requests": [
        {
            "custom_id": "my-first-request",
            "params": {
                "model": "claude-sonnet-4-5",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": "Hello, world"}
                ]
            }
        },
        {
            "custom_id": "my-second-request",
            "params": {
                "model": "claude-sonnet-4-5",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": "Hi again, friend"}
                ]
            }
        }
    ]
}'
```
</td>
</tr>
</table>


Tracking your batch:


<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()

message_batch = client.messages.batches.retrieve(
    "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d",
)
print(f"Batch {message_batch.id} processing status is {message_batch.processing_status}")
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages/batches/msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d \
 --header "x-api-key: $ANTHROPIC_API_KEY" \
 --header "anthropic-version: 2023-06-01" \
 | sed -E 's/.*"id":"([^"]+)".*"processing_status":"([^"]+)".*/Batch \1 processing status is \2/'
```
</td>
</tr>
</table>

Retrieving batch results


<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()

# Stream results file in memory-efficient chunks, processing one at a time
for result in client.messages.batches.results(
    "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d",
):
    match result.result.type:
        case "succeeded":
            print(f"Success! {result.custom_id}")
        case "errored":
            if result.result.error.type == "invalid_request":
                # Request body must be fixed before re-sending request
                print(f"Validation error {result.custom_id}")
            else:
                # Request can be retried directly
                print(f"Server error {result.custom_id}")
        case "expired":
            print(f"Request expired {result.custom_id}")
```
</td>
<td width="50%">

**cURL**
```bash
#!/bin/sh
curl "https://api.anthropic.com/v1/messages/batches/msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  | grep -o '"results_url":[[:space:]]*"[^"]*"' \
  | cut -d'"' -f4 \
  | while read -r url; do
    curl -s "$url" \
      --header "anthropic-version: 2023-06-01" \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      | sed 's/}{/}\n{/g' \
      | while IFS= read -r line
    do
      result_type=$(echo "$line" | sed -n 's/.*"result":[[:space:]]*{[[:space:]]*"type":[[:space:]]*"\([^"]*\)".*/\1/p')
      custom_id=$(echo "$line" | sed -n 's/.*"custom_id":[[:space:]]*"\([^"]*\)".*/\1/p')
      error_type=$(echo "$line" | sed -n 's/.*"error":[[:space:]]*{[[:space:]]*"type":[[:space:]]*"\([^"]*\)".*/\1/p')

      case "$result_type" in
        "succeeded")
          echo "Success! $custom_id"
          ;;
        "errored")
          if [ "$error_type" = "invalid_request" ]; then
            # Request body must be fixed before re-sending request
            echo "Validation error: $custom_id"
          else
            # Request can be retried directly
            echo "Server error: $custom_id"
          fi
          ;;
        "expired")
          echo "Expired: $line"
          ;;
      esac
    done
  done
```
</td>
</tr>
</table>

### [7. Citations](https://docs.claude.com/en/docs/build-with-claude/citations)

Claude is capable of providing detailed citations when answering questions about documents, helping you track and verify information sources in responses.

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "text",
                        "media_type": "text/plain",
                        "data": "The grass is green. The sky is blue."
                    },
                    "title": "My Document",
                    "context": "This is a trustworthy document.",
                    "citations": {"enabled": True}
                },
                {
                    "type": "text",
                    "text": "What color is the grass and sky?"
                }
            ]
        }
    ]
)
print(response)
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "document",
            "source": {
              "type": "text",
              "media_type": "text/plain",
              "data": "The grass is green. The sky is blue."
            },
            "title": "My Document",
            "context": "This is a trustworthy document.",
            "citations": {"enabled": true}
          },
          {
            "type": "text",
            "text": "What color is the grass and sky?"
          }
        ]
      }
    ]
  }'
```
</td>
</tr>
</table>

Using Prompt Caching with Citations:

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()

# Long document content (e.g., technical documentation)
long_document = "This is a very long document with thousands of words..." + " ... " * 1000  # Minimum cacheable length

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "text",
                        "media_type": "text/plain",
                        "data": long_document
                    },
                    "citations": {"enabled": True},
                    "cache_control": {"type": "ephemeral"}  # Cache the document content
                },
                {
                    "type": "text",
                    "text": "What does this document say about API features?"
                }
            ]
        }
    ]
)
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "text",
                        "media_type": "text/plain",
                        "data": "This is a very long document with thousands of words..."
                    },
                    "citations": {"enabled": true},
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text",
                    "text": "What does this document say about API features?"
                }
            ]
        }
    ]
}'
```
</td>
</tr>
</table>

### [8. Multilingual support](https://docs.claude.com/en/docs/build-with-claude/multilingual-support)

Claude excels at tasks across multiple languages, maintaining strong cross-lingual performance relative to English.

### [9. Token counting](https://docs.claude.com/en/docs/build-with-claude/token-counting)

Token counting enables you to determine the number of tokens in a message before sending it to Claude, helping you make informed decisions about your prompts and usage. With token counting, you can:

- Proactively manage rate limits and costs
- Make smart model routing decisions
- Optimize prompts to be a specific length

### [10. Embeddings](https://docs.claude.com/en/docs/build-with-claude/embeddings)

Text embeddings are numerical representations of text that enable measuring semantic similarity. This guide introduces embeddings, their applications, and how to use embedding models for tasks like search, recommendations, and anomaly detection. Key factors for choosing an embeddings provider:

1. Dataset size & domain fit - Larger, domain-specific training data produces better embeddings for your use case

2. Speed - Important for production deployments at scale

3. Customization - Ability to fine-tune on your own data for specialized vocabularies


| Model | Context Length | Embedding Dimension | Description |
|-------|----------------|---------------------|-------------|
| `voyage-3-large` | 32,000 | 1024 (default), 256, 512, 2048 | Best general-purpose and multilingual retrieval |
| `voyage-3.5` | 32,000 | 1024 (default), 256, 512, 2048 | Optimized for general-purpose and multilingual retrieval |
| `voyage-3.5-lite` | 32,000 | 1024 (default), 256, 512, 2048 | Optimized for latency and cost |
| `voyage-code-3` | 32,000 | 1024 (default), 256, 512, 2048 | Optimized for code retrieval |
| `voyage-finance-2` | 32,000 | 1024 | Optimized for finance retrieval and RAG |
| `voyage-law-2` | 16,000 | 1024 | Optimized for legal and long-context retrieval |

```python
import voyageai

vo = voyageai.Client()
# This will automatically use the environment variable VOYAGE_API_KEY.
# Alternatively, you can use vo = voyageai.Client(api_key="<your secret key>")

texts = ["Sample text 1", "Sample text 2"]

result = vo.embed(texts, model="voyage-3.5", input_type="document")
print(result.embeddings[0])
print(result.embeddings[1])
```

### [11. Files API](https://docs.claude.com/en/docs/build-with-claude/files)

The Files API lets you upload and manage files to use with the Claude API without re-uploading content with each request.

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()
client.beta.files.upload(
  file=("document.pdf", open("/path/to/document.pdf", "rb"), "application/pdf"),
)
```
</td>
<td width="50%">

**cURL**
```bash
curl -X POST https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -F "file=@/path/to/document.pdf"
```
</td>
</tr>
</table>

Using a file in messages:

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Please summarize this document for me."
                },
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": "file_011CNha8iCJcU1wXNR6q4V8w"
                    }
                }
            ]
        }
    ],
    betas=["files-api-2025-04-14"],
)
print(response)
```
</td>
<td width="50%">

**cURL**
```bash
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Please summarize this document for me."          
          },
          {
            "type": "document",
            "source": {
              "type": "file",
              "file_id": "file_011CNha8iCJcU1wXNR6q4V8w"
            }
          }
        ]
      }
    ]
  }'
```
</td>
</tr>
</table>

The Files API supports different file types that correspond to different content block types:

| File Type | MIME Type | Content Block Type | Use Case |
| --- | --- | --- | --- |
| PDF | application/pdf | document | Text analysis, document processing |
| Plain text | text/plain | document | Text analysis, processing |
| Images | image/jpeg, image/png, image/gif, image/webp | image | Image analysis, visual tasks |
| Datasets, others | Varies | container_upload | Analyze data, create visualizations |
​
For file types that are not supported as document blocks (.csv, .txt, .md, .docx, .xlsx), convert the files to plain text, and include the content directly in your message:

<table>
<tr>
<td width="50%">

**Python**
```python
import pandas as pd
import anthropic

client = anthropic.Anthropic()

# Example: Reading a CSV file
df = pd.read_csv('data.csv')
csv_content = df.to_string()

# Send as plain text in the message
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Here's the CSV data:\n\n{csv_content}\n\nPlease analyze this data."
                }
            ]
        }
    ]
)

print(response.content[0].text)
```
</td>
<td width="50%">

**cURL**
```bash
# Example: Reading a text file and sending it as plain text
# Note: For files with special characters, consider base64 encoding
TEXT_CONTENT=$(cat document.txt | jq -Rs .)

curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d @- <<EOF
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here's the document content:\n\n${TEXT_CONTENT}\n\nPlease summarize this document."
        }
      ]
    }
  ]
}
EOF
```
</td>
</tr>
</table>

Retrieve a list of your uploaded files:

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()
files = client.beta.files.list()
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```
</td>
</tr>
</table>

Get file metadata:

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()
file = client.beta.files.retrieve_metadata("file_011CNha8iCJcU1wXNR6q4V8w")
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/files/file_011CNha8iCJcU1wXNR6q4V8w \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```
</td>
</tr>
</table>

Delete a file:

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()
result = client.beta.files.delete("file_011CNha8iCJcU1wXNR6q4V8w")
```
</td>
<td width="50%">

**cURL**
```bash
curl -X DELETE https://api.anthropic.com/v1/files/file_011CNha8iCJcU1wXNR6q4V8w \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```
</td>
</tr>
</table>

Downloading a file:

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()
file_content = client.beta.files.download("file_011CNha8iCJcU1wXNR6q4V8w")

# Save to file
with open("downloaded_file.txt", "w") as f:
    f.write(file_content.decode('utf-8'))
```
</td>
<td width="50%">

**cURL**
```bash
curl -X GET "https://api.anthropic.com/v1/files/file_011CNha8iCJcU1wXNR6q4V8w/content" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  --output downloaded_file.txt
```
</td>
</tr>
</table>

### [12. Vision](https://docs.claude.com/en/docs/build-with-claude/vision)

The Claude 3 and 4 families of models comes with new vision capabilities that allow Claude to understand and analyze images, opening up exciting possibilities for multimodal interaction. You can include multiple images in a single request (up to 20 for claude.ai and 100 for API requests). If you submit an image larger than 8000x8000 px, it will be rejected. If you submit more than 20 images in one API request, this limit is 2000x2000 px. If your image does not need to be resized, you can estimate the number of tokens used through this algorithm: `tokens = (width px * height px)/750`.

Base64-encoded image example:

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image1_media_type,
                        "data": image1_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ],
        }
    ],
)
print(message)
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image",
            "source": {
              "type": "base64",
              "media_type": "image/jpeg",
              "data": "'"$BASE64_IMAGE_DATA"'"
            }
          },
          {
            "type": "text",
            "text": "Describe this image."
          }
        ]
      }
    ]
  }'
```
</td>
</tr>
</table>

URL-based image example:

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ],
        }
    ],
)
print(message)
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image",
            "source": {
              "type": "url",
              "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
            }
          },
          {
            "type": "text",
            "text": "Describe this image."
          }
        ]
      }
    ]
  }'
```
</td>
</tr>
</table>

Files API image example:

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()

# Upload the image file
with open("image.jpg", "rb") as f:
    file_upload = client.beta.files.upload(file=("image.jpg", f, "image/jpeg"))

# Use the uploaded file in a message
message = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    betas=["files-api-2025-04-14"],
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "file",
                        "file_id": file_upload.id
                    }
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ]
        }
    ],
)

print(message.content)
```
</td>
<td width="50%">

**cURL**
```bash
# First, upload your image to the Files API
curl -X POST https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -F "file=@image.jpg"

# Then use the returned file_id in your message
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image",
            "source": {
              "type": "file",
              "file_id": "file_abc123"
            }
          },
          {
            "type": "text",
            "text": "Describe this image."
          }
        ]
      }
    ]
  }'
```
</td>
</tr>
</table>


### [13. PDF support](https://docs.claude.com/en/docs/build-with-claude/pdf-support)

Process PDFs with Claude. Extract text, analyze charts, and understand visual content from your documents. You can now ask Claude about any text, pictures, charts, and tables in PDFs you provide. Some sample use cases:

- Analyzing financial reports and understanding charts/tables
- Extracting key information from legal documents
- Translation assistance for documents
- Converting document information into structured formats

Claude works with any standard PDF. However, you should ensure your request size meets these requirements when using PDF support:

| Requirement | Limit |
| --- | --- |
| Maximum request size | 32MB |
| Maximum pages per request | 100 |
| Format | Standard PDF (no passwords/encryption) |

URL-based PDF document:

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "url",
                        "url": "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
                    }
                },
                {
                    "type": "text",
                    "text": "What are the key findings in this document?"
                }
            ]
        }
    ],
)

print(message.content)
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
   -H "content-type: application/json" \
   -H "x-api-key: $ANTHROPIC_API_KEY" \
   -H "anthropic-version: 2023-06-01" \
   -d '{
     "model": "claude-sonnet-4-5",
     "max_tokens": 1024,
     "messages": [{
         "role": "user",
         "content": [{
             "type": "document",
             "source": {
                 "type": "url",
                 "url": "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
             }
         },
         {
             "type": "text",
             "text": "What are the key findings in this document?"
         }]
     }]
 }'
```
</td>
</tr>
</table>

Base64-encoded PDF document:

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic
import base64
import httpx

# First, load and encode the PDF 
pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
pdf_data = base64.standard_b64encode(httpx.get(pdf_url).content).decode("utf-8")

# Alternative: Load from a local file
# with open("document.pdf", "rb") as f:
#     pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

# Send to Claude using base64 encoding
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data
                    }
                },
                {
                    "type": "text",
                    "text": "What are the key findings in this document?"
                }
            ]
        }
    ],
)

print(message.content)
```
</td>
<td width="50%">

**cURL**
```bash
# Method 1: Fetch and encode a remote PDF
curl -s "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt

# Method 2: Encode a local PDF file
# base64 document.pdf | tr -d '\n' > pdf_base64.txt

# Create a JSON request file using the pdf_base64.txt content
jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [{
        "role": "user",
        "content": [{
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": "application/pdf",
                "data": $PDF_BASE64
            }
        },
        {
            "type": "text",
            "text": "What are the key findings in this document?"
        }]
    }]
}' > request.json

# Send the API request using the JSON file
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d @request.json
```
</td>
</tr>
</table>

For PDFs you’ll use repeatedly, or when you want to avoid encoding overhead, use the Files API:

<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic
import base64
import httpx

# First, load and encode the PDF 
pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
pdf_data = base64.standard_b64encode(httpx.get(pdf_url).content).decode("utf-8")

# Alternative: Load from a local file
# with open("document.pdf", "rb") as f:
#     pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

# Send to Claude using base64 encoding
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data
                    }
                },
                {
                    "type": "text",
                    "text": "What are the key findings in this document?"
                }
            ]
        }
    ],
)

print(message.content)
```
</td>
<td width="50%">

**cURL**
```bash
# First, upload your PDF to the Files API
curl -X POST https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -F "file=@document.pdf"

# Then use the returned file_id in your message
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -d '{
    "model": "claude-sonnet-4-5", 
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": [{
        "type": "document",
        "source": {
          "type": "file",
          "file_id": "file_abc123"
        }
      },
      {
        "type": "text",
        "text": "What are the key findings in this document?"
      }]
    }]
  }'
```
</td>
</tr>
</table>

### [14. Search Results](https://docs.claude.com/en/docs/build-with-claude/search-results)

Enable natural citations for RAG applications by providing search results with source attribution.

```python
from anthropic import Anthropic
from anthropic.types import (
    MessageParam,
    TextBlockParam,
    SearchResultBlockParam,
    ToolResultBlockParam
)

client = Anthropic()

# Define a knowledge base search tool
knowledge_base_tool = {
    "name": "search_knowledge_base",
    "description": "Search the company knowledge base for information",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query"
            }
        },
        "required": ["query"]
    }
}

# Function to handle the tool call
def search_knowledge_base(query):
    # Your search logic here
    # Returns search results in the correct format
    return [
        SearchResultBlockParam(
            type="search_result",
            source="https://docs.company.com/product-guide",
            title="Product Configuration Guide",
            content=[
                TextBlockParam(
                    type="text",
                    text="To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs."
                )
            ],
            citations={"enabled": True}
        ),
        SearchResultBlockParam(
            type="search_result",
            source="https://docs.company.com/troubleshooting",
            title="Troubleshooting Guide",
            content=[
                TextBlockParam(
                    type="text",
                    text="If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values."
                )
            ],
            citations={"enabled": True}
        )
    ]

# Create a message with the tool
response = client.messages.create(
    model="claude-sonnet-4-5",  # Works with all supported models
    max_tokens=1024,
    tools=[knowledge_base_tool],
    messages=[
        MessageParam(
            role="user",
            content="How do I configure the timeout settings?"
        )
    ]
)

# When Claude calls the tool, provide the search results
if response.content[0].type == "tool_use":
    tool_result = search_knowledge_base(response.content[0].input["query"])
    
    # Send the tool result back
    final_response = client.messages.create(
        model="claude-sonnet-4-5",  # Works with all supported models
        max_tokens=1024,
        messages=[
            MessageParam(role="user", content="How do I configure the timeout settings?"),
            MessageParam(role="assistant", content=response.content),
            MessageParam(
                role="user",
                content=[
                    ToolResultBlockParam(
                        type="tool_result",
                        tool_use_id=response.content[0].id,
                        content=tool_result  # Search results go here
                    )
                ]
            )
        ]
    )
```

Search results as top-level content:

<table>
<tr>
<td width="50%">

**Python**
```python
from anthropic import Anthropic
from anthropic.types import (
    MessageParam,
    TextBlockParam,
    SearchResultBlockParam
)

client = Anthropic()

# Provide search results directly in the user message
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        MessageParam(
            role="user",
            content=[
                SearchResultBlockParam(
                    type="search_result",
                    source="https://docs.company.com/api-reference",
                    title="API Reference - Authentication",
                    content=[
                        TextBlockParam(
                            type="text",
                            text="All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
                        )
                    ],
                    citations={"enabled": True}
                ),
                SearchResultBlockParam(
                    type="search_result",
                    source="https://docs.company.com/quickstart",
                    title="Getting Started Guide",
                    content=[
                        TextBlockParam(
                            type="text",
                            text="To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
                        )
                    ],
                    citations={"enabled": True}
                ),
                TextBlockParam(
                    type="text",
                    text="Based on these search results, how do I authenticate API requests and what are the rate limits?"
                )
            ]
        )
    ]
)

print(response.model_dump_json(indent=2))
```
</td>
<td width="50%">

**cURL**
```bash
#!/bin/sh
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "search_result",
                    "source": "https://docs.company.com/api-reference",
                    "title": "API Reference - Authentication",
                    "content": [
                        {
                            "type": "text",
                            "text": "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
                        }
                    ],
                    "citations": {
                        "enabled": true
                    }
                },
                {
                    "type": "search_result",
                    "source": "https://docs.company.com/quickstart",
                    "title": "Getting Started Guide",
                    "content": [
                        {
                            "type": "text",
                            "text": "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
                        }
                    ],
                    "citations": {
                        "enabled": true
                    }
                },
                {
                    "type": "text",
                    "text": "Based on these search results, how do I authenticate API requests and what are the rate limits?"
                }
            ]
        }
    ]
}'
```
</td>
</tr>
</table>

### [15. Claude for Sheets](https://docs.claude.com/en/docs/agents-and-tools/claude-for-sheets)

### [16. Tools use](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview#sequential-tools)

Claude is capable of interacting with tools and functions, allowing you to extend Claude’s capabilities to perform a wider variety of tasks.


<table>
<tr>
<td width="50%">

**Python**
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"],
            },
        }
    ],
    messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
)
print(response)
```
</td>
<td width="50%">

**cURL**
```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "tools": [
      {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"]
        }
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "What is the weather like in San Francisco?"
      }
    ]
  }'
```
</td>
</tr>
</table>

Claude supports two types of tools:

- **Client tools**: Tools that execute on your systems, which include:
    - User-defined custom tools that you create and implement
    - Anthropic-defined tools like computer use and text editor that require client implementation

- **Server tools**: Tools that execute on Anthropic’s servers, like the web search and web fetch tools. These tools must be specified in the API request but don’t require implementation on your part.

Client tools (both Anthropic-defined and user-defined) are specified in the tools top-level parameter of the API request. Each tool definition includes:

- **name**: The name of the tool. Must match the regex ^[a-zA-Z0-9_-]{1,64}$.
- **description**: A detailed plaintext description of what the tool does, when it should be used, and how it behaves.
- **input_schema**: A JSON Schema object defining the expected parameters for the tool.

```json
{
  "name": "get_weather",
  "description": "Get the current weather in a given location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
      }
    },
    "required": ["location"]
  }
}
```

Use the @beta_tool decorator to define tools and `client.beta.messages.tool_runner()` to execute them.

```python
import anthropic
import json
from anthropic import beta_tool

# Initialize client
client = anthropic.Anthropic()

# Define tools using the decorator
@beta_tool
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a given location.

    Args:
        location: The city and state, e.g. San Francisco, CA
        unit: Temperature unit, either 'celsius' or 'fahrenheit'
    """
    # In a full implementation, you'd call a weather API here
    return json.dumps({"temperature": "20°C", "condition": "Sunny"})

@beta_tool
def calculate_sum(a: int, b: int) -> str:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number
    """
    return str(a + b)

# Use the tool runner
with client.beta.messages.tool_runner(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[get_weather, calculate_sum],
    messages=[
        {"role": "user", "content": "What's the weather like in Paris? Also, what's 15 + 27?"}
    ]
) as runner:
    for message in runner:
        print(message.content[0].text)
```

In some cases, you may want Claude to use a specific tool to answer the user’s question, even if Claude thinks it can provide an answer without using a tool. You can do this by specifying the tool in the tool_choice field like so: `tool_choice = {"type": "tool", "name": "get_weather"}`

When working with the tool_choice parameter, we have four possible options:

- `auto`: allows Claude to decide whether to call any provided tools or not. This is the default value when tools are provided.
- `any`: tells Claude that it must use one of the provided tools, but doesn’t force a particular tool.
- `tool`: allows us to force Claude to always use a particular tool.
- `none`: prevents Claude from using any tools. This is the default value when no tools are provided.

By default, Claude may use multiple tools to answer a user query. You can disable this behavior by. Setting `disable_parallel_tool_use=true` when `tool_choice` type is `auto`, which ensures that Claude uses at most one tool

Claude Tool Use Reference:

| Tool | Usage | Example Code | Key Features |
|------|-------|--------------|--------------|
| **Bash Tool** (`bash_20250124`) | Execute shell commands in a persistent bash session. Maintains state between commands (environment variables, working directory). | `client.messages.create(model="claude-sonnet-4-5", tools=[{"type": "bash_20250124", "name": "bash"}], messages=[{"role": "user", "content": "List all Python files"}])` | - Persistent session state<br>- Command chaining<br>- Environment variable access<br>- Parameters: `command`, `restart` |
| **Code Execution Tool** (`code_execution_20250825`) | Execute bash commands and perform file operations in a secure sandbox. Automatically handles calculations, data analysis, and code execution. | ```curl https://api.anthropic.com/v1/messages --header "anthropic-beta: code-execution-2025-08-25" --data '{"model": "claude-sonnet-4-5", "tools": [{"type": "code_execution_20250825"}]}'``` | - Automatic bash & file operations<br>- Secure sandbox environment<br>- Container reuse for efficiency<br>- Pre-installed Python libraries |
| **Computer Use Tool** (`computer_20250124`) | Control desktop environment via screenshots, mouse, and keyboard. Enables Claude to interact with any application or interface. | ```client.beta.messages.create(model="claude-sonnet-4-5", tools=[{"type": "computer_20250124", "display_width_px": 1024, "display_height_px": 768}], betas=["computer-use-2025-01-24"])``` | - Screenshot capture<br>- Mouse control (click, drag, scroll)<br>- Keyboard input & shortcuts<br>- Actions: `screenshot`, `left_click`, `type`, `key`, `mouse_move`, `scroll` |
| **Text Editor Tool** (`text_editor_20250728`) | View, create, and edit files with precise string replacement. Ideal for code debugging, refactoring, and documentation. | ```curl https://api.anthropic.com/v1/messages --data '{"model": "claude-sonnet-4-5", "tools": [{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool", "max_characters": 10000}]}'``` | - Commands: `view`, `str_replace`, `create`, `insert`, `undo_edit`<br>- Precise text matching<br>- Line-based operations<br>- Directory listing support |
| **Web Fetch Tool** (`web_fetch_20250910`) | Retrieve and analyze content from URLs. Supports HTML pages and automatic PDF text extraction. | ```curl https://api.anthropic.com/v1/messages --header "anthropic-beta: web-fetch-2025-09-10" --data '{"model": "claude-sonnet-4-5", "tools": [{"type": "web_fetch_20250910", "max_uses": 5, "citations": {"enabled": true}}]}'``` | - Full text content retrieval<br>- PDF text extraction<br>- Domain filtering (allowed/blocked)<br>- Optional citations<br>- Content length limits |
| **Web Search Tool** (`web_search_20250305`) | Search the web and get results with cited sources. Claude decides when to search based on the prompt. | ```curl https://api.anthropic.com/v1/messages --data '{"model": "claude-sonnet-4-5", "tools": [{"type": "web_search_20250305", "max_uses": 5, "user_location": {"type": "approximate", "city": "San Francisco"}}]}'``` | - Automatic search execution<br>- Cited sources in responses<br>- Domain filtering<br>- Location-based results<br>- Max uses limit |
| **Memory Tool** (`memory_20250818`) | Persistent file storage in `/memories` directory. Maintains context across agent executions and builds knowledge over time. | ```curl https://api.anthropic.com/v1/messages --header "anthropic-beta: context-management-2025-06-27" --data '{"model": "claude-sonnet-4-5", "tools": [{"type": "memory_20250818", "name": "memory"}]}'``` | - Commands: `view`, `create`, `str_replace`, `insert`, `delete`, `rename`<br>- Cross-conversation learning<br>- Project context persistence<br>- Knowledge base building |

Tool Compatibility Notes:

- **Claude 4 models** (Opus 4.1, Opus 4, Sonnet 4.5, Sonnet 4, Haiku 4.5): Support all tools
- **Claude Sonnet 3.7**: Supports all tools except Memory
- **Claude Sonnet 3.5 v2** (deprecated): Limited support, check specific tool docs
- **Beta headers required**: Computer use, code execution, web fetch, web search, memory tools require specific beta headers

Security Best Practices:

1. **Computer Use**: Use dedicated VM/container with minimal privileges, avoid sensitive data access
2. **Bash Tool**: Validate commands, block dangerous patterns (e.g., `rm -rf /`)
3. **Web Tools**: Use domain filtering, validate URLs for homograph attacks
4. **Memory Tool**: Implement path traversal protection, manage file storage limits

### [17. Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

Agent Skills are modular capabilities that extend Claude’s functionality. Each Skill packages instructions, metadata, and optional resources (scripts, templates) that Claude uses automatically when relevant.

#### How It Works (3 Levels)

**Level 1 - The Label 🏷️**

- Claude sees a short description: "PDF Processing - extract text from PDFs"
- This is always loaded, so Claude knows the Skill exists
- Uses very few tokens (like ~100)

**Level 2 - The Instructions 📖**

- When you ask Claude to work with a PDF, it opens the instruction manual
- Reads step-by-step guidance on how to process PDFs
- Only loaded when needed

**Level 3 - The Tools & Resources 🛠️**

- Extra files, code scripts, templates, examples
- Claude only opens these if specifically needed
- Saves lots of space in Claude's "memory"

#### Where It Runs

**Claude API 🌐**

- Skills run in Anthropic's cloud (their servers, not your machine)
- You upload Skills to their servers via the API
- Claude executes them in a virtual machine they provide

**Claude.ai (Web/Mobile/Desktop app) 🌐**

- Skills also run in Anthropic's cloud
- When you upload a Skill as a zip file, it goes to their servers
- Claude uses it in their environment, not on your device

**Claude Code 💻**

- THIS is where it runs locally!
- Skills live in directories on your computer (`~/.claude/skills/` or `.claude/skills/`)
- Claude Code runs on your machine and accesses Skills from your filesystem
- This is the only case where Skills are truly "local"

Here’s how Claude loads and uses a PDF processing skill:

- **Startup**: System prompt includes: PDF Processing - Extract text and tables from PDF files, fill forms, merge documents
- **User request**: “Extract the text from this PDF and summarize it”
- **Claude invokes**: bash: read pdf-skill/SKILL.md → Instructions loaded into context
- **Claude determines**: Form filling is not needed, so FORMS.md is not read
- **Claude executes**: Uses instructions from SKILL.md to complete the task

#### Get Started

**Pre-requisites**

- Anthropic API key
- Python 3.7+ or curl installed
- Basic familiarity with making API requests

**Step 1: List available Skills**

```python
import anthropic

client = anthropic.Anthropic()

# List Anthropic-managed Skills
skills = client.beta.skills.list(
    source="anthropic",
    betas=["skills-2025-10-02"]
)

for skill in skills.data:
    print(f"{skill.id}: {skill.display_title}")
```

**Step 2: Create a presentation**

```python
import anthropic

client = anthropic.Anthropic()

# Create a message with the PowerPoint Skill
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {
                "type": "anthropic",
                "skill_id": "pptx",
                "version": "latest"
            }
        ]
    },
    messages=[{
        "role": "user",
        "content": "Create a presentation about renewable energy with 5 slides"
    }],
    tools=[{
        "type": "code_execution_20250825",
        "name": "code_execution"
    }]
)

print(response.content)
```

**Step 3: Download the created file**

```python
# Extract file ID from response
file_id = None
for block in response.content:
    if block.type == 'tool_use' and block.name == 'code_execution':
        # File ID is in the tool result
        for result_block in block.content:
            if hasattr(result_block, 'file_id'):
                file_id = result_block.file_id
                break

if file_id:
    # Download the file
    file_content = client.beta.files.download(
        file_id=file_id,
        betas=["files-api-2025-04-14"]
    )

    # Save to disk
    with open("renewable_energy.pptx", "wb") as f:
        file_content.write_to_file(f.name)

    print(f"Presentation saved to renewable_energy.pptx")
```

#### Try more examples:

**Create a spreadsheet**

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {
                "type": "anthropic",
                "skill_id": "xlsx",
                "version": "latest"
            }
        ]
    },
    messages=[{
        "role": "user",
        "content": "Create a quarterly sales tracking spreadsheet with sample data"
    }],
    tools=[{
        "type": "code_execution_20250825",
        "name": "code_execution"
    }]
)
```

**Create a Word document**

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {
                "type": "anthropic",
                "skill_id": "docx",
                "version": "latest"
            }
        ]
    },
    messages=[{
        "role": "user",
        "content": "Write a 2-page report on the benefits of renewable energy"
    }],
    tools=[{
        "type": "code_execution_20250825",
        "name": "code_execution"
    }]
)
```

**Generate a PDF**

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {
                "type": "anthropic",
                "skill_id": "pdf",
                "version": "latest"
            }
        ]
    },
    messages=[{
        "role": "user",
        "content": "Generate a PDF invoice template"
    }],
    tools=[{
        "type": "code_execution_20250825",
        "name": "code_execution"
    }]
)
```

## [API Reference](https://docs.claude.com/en/api/overview)

The API is made available via our web Console. You can use the Workbench to try out the API in the browser and then generate API keys in Account Settings. Use workspaces to segment your API keys and control spend by use case.

Claude also provides client libraries in a number of popular languages that make it easier to work with the Claude API.

Beta headers allow you to access experimental features and new model capabilities before they become part of the standard API. These features are subject to change and may be modified or removed in future releases.

Our API follows a predictable HTTP error code format:

`400` - invalid_request_error: There was an issue with the format or content of your request. We may also use this error type for other 4XX status codes not listed below.
`401` - authentication_error: There’s an issue with your API key.
`403` - permission_error: Your API key does not have permission to use the specified resource.
`404` - not_found_error: The requested resource was not found.
`413` - request_too_large: Request exceeds the maximum allowed number of bytes. The maximum request size is 32 MB for standard API endpoints.
`429` - rate_limit_error: Your account has hit a rate limit.
`500` - api_error: An unexpected error has occurred internal to Anthropic’s systems.
`529` - overloaded_error: The API is temporarily overloaded.

### Message

#### [Message](https://docs.claude.com/en/api/messages)

```bash
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, world"}
    ]
}'
```

Success response (200):

```json
{
  "content": [
    {
      "citations": null,
      "text": "Hi! My name is Claude.",
      "type": "text"
    }
  ],
  "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
  "model": "claude-sonnet-4-5-20250929",
  "role": "assistant",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "type": "message",
  "usage": {
    "input_tokens": 2095,
    "output_tokens": 503
  }
}
```

Error response (400):

```json
{
  "error": {
    "message": "Invalid request",
    "type": "invalid_request_error"
  },
  "request_id": "<string>",
  "type": "error"
}
```

Or with Python SDK:

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.count_tokens(
    model="claude-sonnet-4-5",
    system="You are a scientist",
    messages=[{
        "role": "user",
        "content": "Hello, Claude"
    }],
)

print(response.json())
```

Multi-conversation messages

```bash
#!/bin/sh
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, Claude"},
        {"role": "assistant", "content": "Hello!"},
        {"role": "user", "content": "Can you describe LLMs to me?"}

    ]
}'
```

Putting words in Claude’s mouth:

```bash
#!/bin/sh
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1,
    "messages": [
        {"role": "user", "content": "What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae"},
        {"role": "assistant", "content": "The answer is ("}
    ]
}'
```

#### [Count Message tokens](https://docs.claude.com/en/api/messages-count-tokens)

Count the number of tokens in a Message. The Token Count API can be used to count the number of tokens in a Message, including tools, images, and documents, without creating it.

```bash
curl https://api.anthropic.com/v1/messages/count_tokens \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-3-7-sonnet-20250219",
    "messages": [
        {"role": "user", "content": "Hello, world"}
    ]
}'
```

Or with Python SDK:

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.count_tokens(
    model="claude-sonnet-4-5",
    system="You are a scientist",
    messages=[{
        "role": "user",
        "content": "Hello, Claude"
    }],
)

print(response.json())
```

### Models

#### [List Models](https://docs.claude.com/en/api/models-list)

List available models.

```bash
curl https://api.anthropic.com/v1/models \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01"
```

#### [Get a specific model](https://docs.claude.com/en/api/models)

```bash
curl https://api.anthropic.com/v1/models/claude-sonnet-4-20250514 \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01"
```

### Message Batches

#### [Create a Message Batch](https://docs.claude.com/en/api/creating-message-batches)

Send a batch of Message creation requests.

```bash
curl https://api.anthropic.com/v1/messages/batches \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "requests": [
        {
            "custom_id": "my-first-request",
            "params": {
                "model": "claude-3-7-sonnet-20250219",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": "Hello, world"}
                ]
            }
        },
        {
            "custom_id": "my-second-request",
            "params": {
                "model": "claude-3-7-sonnet-20250219",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": "Hi again, friend"}
                ]
            }
        }
    ]
}'
```

#### [Retrieve a Message Batch](https://docs.claude.com/en/api/retrieving-message-batches)

```bash
curl https://api.anthropic.com/v1/messages/batches/msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01"
```

#### [Retrieve Message Batch Results](https://docs.claude.com/en/api/retrieving-message-batch-results)

Streams the results of a Message Batch as a `.jsonl` file.

```bash
curl https://api.anthropic.com/v1/messages/batches/msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d/results \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01"
```

Success response:

```json
{"custom_id":"my-second-request","result":{"type":"succeeded","message":{"id":"msg_014VwiXbi91y3JMjcpyGBHX5","type":"message","role":"assistant","model":"claude-3-5-sonnet-20240620","content":[{"type":"text","text":"Hello again! It's nice to see you. How can I assist you today? Is there anything specific you'd like to chat about or any questions you have?"}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":11,"output_tokens":36}}}}
{"custom_id":"my-first-request","result":{"type":"succeeded","message":{"id":"msg_01FqfsLoHwgeFbguDgpz48m7","type":"message","role":"assistant","model":"claude-3-5-sonnet-20240620","content":[{"type":"text","text":"Hello! How can I assist you today? Feel free to ask me any questions or let me know if there's anything you'd like to chat about."}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":10,"output_tokens":34}}}}
```

#### [List Message Batches](https://docs.claude.com/en/api/listing-message-batches)

List all Message Batches within a Workspace. Most recently created batches are returned first.

```bash
curl https://api.anthropic.com/v1/messages/batches \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01"
```

#### [Cancel a Message Batch](https://docs.claude.com/en/api/canceling-message-batches)

Batches may be canceled any time before processing ends. Once cancellation is initiated, the batch enters a canceling state, at which time the system may complete any in-progress, non-interruptible requests before finalizing cancellation.

```bash
curl --request POST https://api.anthropic.com/v1/messages/batches/msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d/cancel \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01"
```

#### [Delete a Message Batch](https://docs.claude.com/en/api/deleting-message-batches)

```bash
```

### Files

#### []()

```bash
```

#### []()

```bash
```

#### []()

```bash
```

### Skills

### Admin

#### []()

```bash
```

#### []()

```bash
```

#### []()

```bash
```

#### []()

```bash
```

#### []()

```bash
```
