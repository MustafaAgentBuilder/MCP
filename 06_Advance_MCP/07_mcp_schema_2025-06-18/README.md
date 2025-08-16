## MCP Scheme Message Classes — What They Do & Their Parameters

I looked at the **Model Context Protocol (MCP)** specification and Python SDK, and here’s a simple summary of each class you mentioned:

---

### 1. **PingRequest**

* **What it does:**
  Sends a “ping” to check if the other side (client or server) is alive and responsive.
* **Parameters:**
  No parameters. It’s just a simple request.
* **Response:**
  The other side returns an empty response (`result: {}`) to say “I’m alive.” ([modelcontextprotocol.io][1])

---

### 2. **InitializeRequest**

* **What it does:**
  Used by the client when connecting to the server. It sends its protocol version and capabilities to the server. The server responds with its own capabilities. ([Medium][2], [modelcontextprotocol.io][3])
* **Parameters:**

  * `protocolVersion`: which version of MCP the client speaks
  * `capabilities`: what features the client supports (like tools, prompts, logging, etc.)
* **Response:**
  `InitializeResult`, which includes the server’s protocol version and capabilities.

---

### 3. **CompleteRequest**

* **What it does:**
  Used to request completion suggestions (e.g., auto-complete or argument suggestions for prompts).
* **Parameters:**
  Usually includes a reference (like a prompt) and an argument name for which completion is requested.
* **Response:**
  `CompleteResult` with suggested values, typically inside a `values: list[str]` field. ([Medium][2])

---

### 4. **SetLevelRequest**

* **What it does:**
  Lets the client change the server’s logging level (like `"info"` or `"debug"`). Useful for debugging or controlling verbosity. ([Medium][2])
* **Parameters:**

  * `level`: The logging level to set (e.g. `"debug"`, `"info"`, `"error"`).

---

### 5. **GetPromptRequest**

* **What it does:**
  Retrieves a specific prompt template (like a message guide) from the server. ([Medium][2], [modelcontextprotocol.io][3])
* **Parameters:**

  * `name`: The name of the prompt to get
  * `arguments`: An object with values for any arguments the prompt expects

---

### 6. **ListPromptsRequest**

* **What it does:**
  Asks the server for the list of available prompt templates so the client can choose one. ([Medium][2], [modelcontextprotocol.io][3])
* **Parameters:**

  * `cursor` (optional): For pagination, if there are many prompts

---

### 7. **ListResourcesRequest**

* **What it does:**
  Asks the server to list available resources (like files, data templates). ([Medium][2])
* **Parameters:**
  Possibly includes pagination options like a `cursor`.

---

### 8. **ListResourceTemplatesRequest**

* **What it does:**
  Gets a list of resource templates (like patterns or metadata structures). ([Medium][2])
* **Parameters:**
  Also likely includes pagination options like `cursor`.

---

### 9. **ReadResourceRequest**

* **What it does:**
  Reads or fetches the content of a specific resource identified by a URI. ([Medium][2])
* **Parameters:**

  * `uri`: The specific resource identifier the client wants to read

---

### 10. **SubscribeRequest** & **UnsubscribeRequest**

* **What they do:**

  * `SubscribeRequest`: Client asks to get updates when a resource changes.
  * `UnsubscribeRequest`: Cancels that subscription.
    Useful for watching changes in resources. ([Medium][2])
* **Parameters:**

  * Usually include the `uri` of the resource to subscribe or unsubscribe.

---

### 11. **CallToolRequest**

* **What it does:**
  Lets the client call a server-provided "tool" (like a function or API). ([Medium][2])
* **Parameters:**

  * `name`: Name of the tool
  * `arguments`: A dictionary/object with named arguments for the tool

---

### 12. **ListToolsRequest**

* **What it does:**
  Asks the server for a list of available tools that the client can use. ([Medium][2])
* **Parameters:**

  * Might include pagination, e.g., a `cursor`.

---

### 13. **ClientNotification** & **ServerNotification**

* **What they do:**
  These are messages the server or client sends to notify the other side about important events (like progress, initialization done, or resource updates). ([Medium][2])
* **Parameters:**
  Vary by type:

  * `ProgressNotification` may include a `progressToken` and `progress` number.
  * `ResourceUpdatedNotification` includes info about which resource changed.
  * `InitializedNotification` indicates handshake is done.

---

### 14. **ClientResult** & **ServerResult**

* **What they do:**
  These are responses to requests:

  * `ClientResult`: Client’s output types (like `CompleteResult`, `EmptyResult`)
  * `ServerResult`: Server’s response types (like `InitializeResult`, `CallToolResult`, etc.) ([Medium][2])
* **Parameters:**
  Depends on specific request/response type.

---

## Summary Table

| Message Class                | Role / What it Does                                  | Key Parameters                           |
| ---------------------------- | ---------------------------------------------------- | ---------------------------------------- |
| PingRequest                  | Check connection alive                               | None                                     |
| InitializeRequest            | Client handshake                                     | `protocolVersion`, `capabilities`        |
| CompleteRequest              | Request auto-completion                              | Reference & argument field               |
| SetLevelRequest              | Change logging level                                 | `level`                                  |
| GetPromptRequest             | Get a prompt template                                | `name`, `arguments`                      |
| ListPromptsRequest           | List all prompts                                     | `cursor` (optional)                      |
| ListResourcesRequest         | List available resources                             | pagination parameters                    |
| ListResourceTemplatesRequest | List resource templates                              | pagination parameters                    |
| ReadResourceRequest          | Read specific resource content                       | `uri`                                    |
| SubscribeRequest             | Receive updates on resource changes                  | `uri`                                    |
| UnsubscribeRequest           | Stop receiving updates                               | `uri`                                    |
| CallToolRequest              | Invoke a tool/function                               | `name`, `arguments`                      |
| ListToolsRequest             | List available tools                                 | pagination parameters                    |
| Client/ServerNotification    | Notify events (progress, init done, resource update) | Varies by type (e.g. progressToken, URI) |
| ClientResult / ServerResult  | Return responses                                     | Varies by request–response type          |

---

[MCP Schema Reference]("https://modelcontextprotocol.io/specification/2025-06-18/schema")

[1]: https://modelcontextprotocol.io/specification/2025-03-26/basic/utilities/ping?utm_source=chatgpt.com "Ping - Model Context Protocol"
[2]: https://medium.com/%40danushidk507/ai-agents-xvi-mcp-python-sdk-73c02a06f7f0?utm_source=chatgpt.com "AI Agents XVI : MCP — Python SDK - Medium"
[3]: https://modelcontextprotocol.io/docs/concepts/prompts?utm_source=chatgpt.com "Prompts - Model Context Protocol"
