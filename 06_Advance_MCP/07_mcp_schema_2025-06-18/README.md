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

Think of it like: **Client = Student** 🧑‍🎓 and **Server = Teacher** 👨‍🏫.
They send requests, notifications, and results to talk to each other.

---

# 🔹 Client Side

### 1. **ClientRequest** (student asking questions)

Types of requests client can send:

* **PingRequest** → check if server is alive.
* **InitializeRequest** → start connection, share capabilities.
* **CompleteRequest** → ask server to auto-complete something (like code/text).
* **SetLevelRequest** → set log/debug level.
* **GetPromptRequest** → ask for one prompt.
* **ListPromptsRequest** → get all available prompts.
* **ListResourcesRequest** → ask what resources exist.
* **ListResourceTemplatesRequest** → ask about resource templates.
* **ReadResourceRequest** → read data from a resource.
* **SubscribeRequest** → subscribe for updates.
* **UnsubscribeRequest** → stop updates.
* **CallToolRequest** → call a tool (like “analyze\_project”).
* **ListToolsRequest** → ask for all tools.

---

### 2. **ClientNotification** (student informing without asking result)

* **CancelledNotification** → tell server a task was cancelled.
* **ProgressNotification** → send progress update.
* **InitializedNotification** → client finished initializing.
* **RootsListChangedNotification** → roots list has changed.

---

### 3. **ClientResult** (answers client gets back from teacher)

* **EmptyResult** → no data, just success.
* **CreateMessageResult** → result of creating a message.
* **ListRootsResult** → server returns roots list.
* **ElicitResult** → result from elicitation (server asked back something).

---

# 🔹 Server Side

### 4. **ServerRequest** (teacher asking questions)

* **PingRequest** → check if client alive.
* **CreateMessageRequest** → ask client to create a message.
* **ListRootsRequest** → request list of roots.
* **ElicitRequest** → server asks client for clarification/input.

---

### 5. **ServerNotification** (teacher telling updates)

* **CancelledNotification** → task cancelled.
* **ProgressNotification** → update progress.
* **LoggingMessageNotification** → log/debug info.
* **ResourceUpdatedNotification** → a resource was updated.
* **ResourceListChangedNotification** → resource list changed.
* **ToolListChangedNotification** → tool list changed.
* **PromptListChangedNotification** → prompt list changed.

---

### 6. **ServerResult** (teacher gives back results)

* **EmptyResult** → no data, just success.
* **InitializeResult** → result of initialization.
* **CompleteResult** → result of completion.
* **GetPromptResult** → returns one prompt.
* **ListPromptsResult** → returns all prompts.
* **ListResourceTemplatesResult** → returns resource templates.
* **ListResourcesResult** → returns list of resources.
* **ReadResourceResult** → returns resource content.
* **CallToolResult** → result of running a tool.
* **ListToolsResult** → returns all tools.

---

✅ **In summary:**

* **Requests** = asking for something.
* **Notifications** = just telling, no reply needed.
* **Results** = answers to requests.

---


[MCP Schema Reference]("https://modelcontextprotocol.io/specification/2025-06-18/schema")

[1]: https://modelcontextprotocol.io/specification/2025-03-26/basic/utilities/ping?utm_source=chatgpt.com "Ping - Model Context Protocol"
[2]: https://medium.com/%40danushidk507/ai-agents-xvi-mcp-python-sdk-73c02a06f7f0?utm_source=chatgpt.com "AI Agents XVI : MCP — Python SDK - Medium"
[3]: https://modelcontextprotocol.io/docs/concepts/prompts?utm_source=chatgpt.com "Prompts - Model Context Protocol"
