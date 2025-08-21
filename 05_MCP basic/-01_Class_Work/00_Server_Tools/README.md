

## 1. 🛠️ What Are **Tools** in MCP?

* Tools are **actions** your AI assistant (like an LLM) can perform—like checking weather, sending emails, or querying a database.
* Unlike resources (which just give data), tools let the assistant **execute code or APIs**.
* 🧠 Tools are **called by the LLM**, not by your app. And you're in charge of approving or rejecting each call. ([modelcontextprotocol.io][1])


---

## 2. Key Properties of a Tool

Each tool has:

| Field                       | What it means in simple words                                                                                                                                   |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **name**                    | Unique ID (e.g. `"get_weather"`), how LLM calls it                                                                                                              |
| **title**                   | Human-readable name shown in UI                                                                                                                                 |
| **description**             | Short explanation of what the tool does                                                                                                                         |
| **inputSchema**             | Outlines what inputs the tool expects (JSON Schema)                                                                                                             |
| **outputSchema** (optional) | Describes structured output format if used ([modelcontextprotocol.io][1], [gofastmcp.com][2], [Firecrawl][3], [modelcontextprotocol.io][4], [DEV Community][5]) |
---
👉 These schemas are descriptors, not arguments.
When you write an MCP tool in FastMCP (or any MCP server), you declare your parameters and return values in Python or your language of choice. MCP automatically generates the inputSchema (and optionally the outputSchema) from your code or developer annotations (e.g. Pydantic models, decorators). You do not pass the schema during runtime—it's metadata registered in the MCP server’s tool listing (returned by tools/list) so clients (LLMs and applications) know how to call your tools correctly

**Example tool definition**:

```json
{
  "name": "get_weather",
  "title": "Weather Info",
  "description": "Fetch current weather for a city",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": { "type": "string", "description": "City name or zip code" }
    },
    "required": ["location"]
  }
}
```

---

## 3. How Tools Work: Protocol Flow

1. **Discovery**: Your bot asks the server

   ```json
   { "method": "tools/list", ... }
   ```

   — then gets information about all tools it can use. ([modelcontextprotocol.io][1])

2. **Execution**: When the model decides it needs a tool, it sends:

   ```json
   {
     "method": "tools/call",
     "params": {
       "name": "get_weather",
       "arguments": { "location": "Sialkot" }
     }
   }
   ```

3. **Response**:

   ````json
   {
     "result": {
       "content": [ { "type": "text", "text": "Current weather is 32 °C, sunny" } ],
       "isError": false
     }
   }
   ``` :contentReference[oaicite:16]{index=16}
   ````

---

## 4. What Tool Results Look Like

* **`text`**: Simple plain-text output.

  ```json
  { "type": "text", "text": "Hello, world!" }
  ```
* **Images**, **audio**, or **resource links** (`resource_link` and `embedded resource`) may also be returned with metadata. ([modelcontextprotocol.io][1])
* Optionally, tools can return **structured content** in JSON format, which clients can parse easily (e.g. weather data JSON). This is typed to an `outputSchema`, so results are predictable and safe. ([GitHub][6])

---
## Example


## 🧠 Use Case:

Let's say you're making a tool named **"ShowLearningMaterial"**
This tool gives the student a **video**, **audio**, or **interactive content**.

---

## ✅ JSON Output Examples for Each Type

### 🔹 1. Text Response

```json
{
  "type": "text",
  "text": "Here is your requested study material on Python basics."
}
```

---

### 🔹 2. Video (resource link)

```json
{
  "type": "resource_link",
  "resource_link": {
    "url": "https://example.com/python-intro.mp4",
    "title": "Python Intro Video"
  }
}
```

---

### 🔹 3. Audio File

```json
{
  "type": "audio",
  "audio": {
    "url": "https://example.com/python-intro.mp3",
    "title": "Python Audio Lecture"
  }
}
```

---

### 🔹 4. Embedded Live Page (iframe)

```json
{
  "type": "resource",
  "resource": {
    "uri": "file:///project/src/main.rs",
    "title": "Main Rust File",
    "mimeType": "text/x-rust",
    "text": "fn main() {\n    println!(\"Hello world!\");\n}",
    "annotations": {
      "audience": ["assistant"],
      "priority": 0.8,
      "lastModified": "2025-05-03T14:30:00Z"
    }
  }
}
```


---

### 🔹 5. Image

```json
{
  "type": "image",
  "image": {
    "url": "https://example.com/python-cheatsheet.png",
    "title": "Python Cheatsheet"
  }
}
```

---

## 🔧 Python Tool Example (FastMCP-style)

Let’s say you want to return a **video + text**. Your Python function might look like this:


---

## ✅ Summary:

| You want to return...      | Use this type         |
| -------------------------- | --------------------- |
| Video file (hosted online) | `type: resource_link` |
| Audio lecture              | `type: audio`         |
| Live webpage or tool       | `type: iframe`        |
| Image                      | `type: image`         |
| Just a plain message       | `type: text`          |


---

## 5. Notifications: When Tool List Changes

If the server adds or removes tools, and it declared `"listChanged": true`, it sends:

```json
{ "method": "notifications/tools/list_changed" }
```

Then the client should call `tools/list` again to refresh possible actions. ([modelcontextprotocol.io][1], [DEV Community][5])

---

## 6. Error Handling

* If you call a tool that doesn't exist:

  ```json
  { "error": { "code": -32602, "message": "Unknown tool" } }
  ```
* If the tool runs but fails internally:

  ````json
  {
    "result": {
      "content": [ { "type": "text", "text": "API timeout" } ],
      "isError": true
    }
  }
  ``` :contentReference[oaicite:27]{index=27}
  ````

---

## 7. Real-Life Example: Weather Assistant with FastMCP

Here's how you'd code it in Python:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="WeatherAssistant")

@mcp.tool()
def get_weather(city: str) -> str:
    return f"Weather in {city}: 32 °C, clear skies"

# Run locally (stdio) or via HTTP
mcp.run(transport="streamable-http")
```

That tool:

* Is listed under `tools/list`
* Requires a `city` string (by input schema)
* Returns a simple string

---

## 8. 🧠 Why Tools Matter: The LLM Can Take Actions

Tools give AI the ability to **do things**, not just talk. Some examples:

* `send_email(to, subject, body)`
* `search_flights(origin, destination, date)`
* `summarize_document(path)`
* `add_numbers(a, b)`

**But always with your permission**—you control whether they run.

---

### ✅ Final Summary

> **Tools** in MCP are like small programs you expose to the LLM.
> The model **chooses** when and how to call them.
> They make your assistant **interact with external systems or APIs**.
> You remain in control for safety and reliability.

["For more detail go to Panaversity github"](https://github.com/panaversity/learn-agentic-ai/tree/main/03_ai_protocols/01_mcp/04_fundamental_%20primitives/03_defining_tools)

[1]: https://modelcontextprotocol.io/specification/2025-06-18/server/tools?utm_source=chatgpt.com "Tools - Model Context Protocol"
[2]: https://gofastmcp.com/python-sdk/fastmcp-server-server?utm_source=chatgpt.com "fastmcp.server"
[3]: https://www.firecrawl.dev/blog/fastmcp-tutorial-building-mcp-servers-python?utm_source=chatgpt.com "FastMCP Tutorial: Building MCP Servers in Python From Scratch"
[4]: https://modelcontextprotocol.io/docs/learn/architecture?utm_source=chatgpt.com "Architecture Overview - Model Context Protocol"
[5]: https://dev.to/alexmercedcoder/a-journey-from-ai-to-llms-and-mcp-9-tools-in-mcp-giving-llms-the-power-to-act-40cf?utm_source=chatgpt.com "9 - Tools in MCP — Giving LLMs the Power to Act - DEV Community"
[6]: https://github.com/modelcontextprotocol/python-sdk?utm_source=chatgpt.com "The official Python SDK for Model Context Protocol servers and clients"
