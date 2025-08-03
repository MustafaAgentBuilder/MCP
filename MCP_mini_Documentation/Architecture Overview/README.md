
## 1. What is MCP—**really**?

* **MCP** stands for **Model Context Protocol**.
* It’s a **standard way** for an AI application (your “MCP host”) to talk to **one or more** little helper programs (“MCP servers”) that provide extra context or do work for the AI.

**Analogy:**

> Imagine ChatGPT is your main app. You also have a calculator program, a weather service, and a file-reader running. MCP is the “language” they all speak so ChatGPT can say, “Hey calculator, compute this,” or “Hey weather, fetch today’s forecast.”

---

## 2. Who’s Who? **Participants**

1. **MCP Host**

   * The AI app (e.g. an OpenAI-powered editor, or your own Python script).
   * It manages multiple MCP clients.

2. **MCP Client**

   * A little connector inside the host that keeps a one-to-one link to a server.
   * Example: `McpClient("http://weather-server")`.

3. **MCP Server**

   * The program that actually provides tools, data, or prompts.
   * Could run on your computer (stdio) or remotely over HTTP.

🎨 **Diagram in your mind**:

```
[MCP Host]
   ├─ MCP Client 1 ──> Weather Server  
   ├─ MCP Client 2 ──> Calculator Server  
   └─ MCP Client 3 ──> File-System Server  
```

---

## 3. Two Layers of MCP

### A) Data Layer (the **inner** protocol)

* Uses **JSON-RPC 2.0** messages (standard format).
* Defines **lifecycle** (initialize, close), **primitives** (tools, resources, prompts), and **notifications**.

### B) Transport Layer (the **outer** envelope)

* **StdIO**: talking over standard input/output (good for local servers).
* **Streamable HTTP**: talking over HTTP + Server-Sent Events (good for remote servers).
* Handles framing, auth, and streaming details so your code doesn’t have to.

---

## 4. Core Data-Layer Concepts

### 4.1 Lifecycle Management

* **Handshake** at the start:

  1. Client sends `initialize` (which protocol version, which features).
  2. Server replies with its version and supported features.
  3. Client sends back “notifications/initialized” → we’re ready!

#### Mini Example:

```jsonc
// Client → Server
{ "method": "initialize", "params": { "protocolVersion":"2025-06-18", "capabilities": {"tools":{}}, "clientInfo":{...} } }

// Server → Client
{ "id":1, "result": { "protocolVersion":"2025-06-18", "capabilities":{"tools":{"listChanged":true}}, "serverInfo":{...} } }
```

### 4.2 Primitives—what servers can offer

1. **Tools**

   * Functions you can **call** (e.g. `tools/list`, `tools/call`).
   * Example “Get weather”, “Compute 2+2”, “Read file contents”.

2. **Resources**

   * Data you can **read** (e.g. file contents, DB schema).
   * Methods like `resources/list`, `resources/read`.

3. **Prompts**

   * Templates or system messages (e.g. a standard “You are a helpful assistant” prompt).
   * Methods like `prompts/list`, `prompts/get`.

#### How discovery works:

* Client asks `tools/list` → server sends back a list of tool names, descriptions, and input schemas.
* Client now **knows** what it can call.

### 4.3 Client-Exposed Primitives

* Sometimes servers ask the **client** to do things:

  * **Sampling**: “Client, please ask your own LLM to complete this text for me.”
  * **Elicitation**: “Client, ask the user for more info (e.g. confirm ‘yes/no’).”
  * **Logging**: “Client, log this debug message.”

---

## 5. Notifications (Real-time Updates)

* If a server’s tools or resources **change**, it can send a **notification** (no response expected) like:

  ```json
  { "method":"notifications/tools/list_changed" }
  ```
* The client then re-calls `tools/list` to get the updated set.

---

## 6. Putting It All Together—**Example Flow**

1. **Initialize**

   * Client ↔ Server handshake.
2. **Discover Tools**

   * Client → `tools/list` → gets back tool names & schemas.
3. **Execute Tool**

   * Client → `tools/call` with `"name":"com.example.weather/current","arguments":{...}` → server replies with structured result.
4. **Notifications**

   * Later, server sends `notifications/tools/list_changed` → client re-asks `tools/list`.

---

## 7. How This Relates to OpenAI Agents SDK

* The **Agents SDK** often needs to call out to external services (tools) or fetch context (resources).
* MCP provides a **standard protocol** so your Agent doesn’t have to custom-wire every integration.
* You write a small server exposing tools via FastMCP or another SDK, and the Agent uses an MCP client to call them.

### Real-world mini example:

1. You build a **weather tool**:

   ```python
   @tool
   async def get_weather(city: str) -> str:
       # call a real weather API...
       return "Sunny, 28°C"
   ```
2. You spin up a **FastMCP server** on localhost:8000.
3. Your **OpenAI Agent** (running in Python) does:

   ```python
   from mcp.client import MCPClient
   async with MCPClient("http://localhost:8000/mcp") as client:
       tools = await client.list_tools()
       result = await client.call_tool("get_weather", city="Karachi")
   ```
4. The LLM inside your Agent now has **live weather data** whenever it needs it.

---

### 🎓 Key Takeaways for Your Exam

* **MCP = JSON-RPC + Transport** for context exchange.
* **Clients** maintain **one-to-one** connections to **servers**.
* Two layers: **data** (JSON-RPC primitives) and **transport** (HTTP or stdio).
* **Primitives**: tools, resources, prompts (server → client) and sampling, elicitation, logging (client → server).
* **Notifications** keep client & server in sync when things change.

By understanding these pieces, you can both **build** MCP servers (with FastMCP or another SDK) and **write** MCP clients (in Python, Node.js, etc.) to integrate real-time tools into your AI agents. 
