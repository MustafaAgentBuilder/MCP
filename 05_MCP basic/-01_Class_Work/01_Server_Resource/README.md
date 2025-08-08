
## 📘 Class Lesson: Understanding MCP Resources


### 1. ✅ What is an MCP Resource?

* A **resource** is **read-only contextual data** provided by the server—like files, API responses, or documentation.
* Resources are identified by a **URI** (e.g., `file://config`, `note://meeting/agenda`, or dynamic `weather://{city}/today`).
* The client or agent can choose when to fetch them.
  ([modelcontextprotocol.io][1])

---

### 2. 🔍 Why Use Resources?

* Provide **structured context** to agents without side effects—no actions, just information.
* Reduce AI reasoning overhead by offering only needed data.
* Keep a clear separation: **resources = data**, **tools = actions**.
  ([Daily Dose of Data Science][2], [Medium][3])

---

### 3. 🗂 Types of Resources

#### A. Static Resources

* Fixed URIs that return consistent content.
* Example: `data://settings` provides server configuration or documentation.

#### B. Resource Templates

* URI patterns with placeholders like `{city}` or `{symbol}`.
* Example: `weather://{city}/today` → `weather://Karachi/today` returns live forecast.
  ([Daily Dose of Data Science][2], [DEV Community][4])

---

### 4. 📊 Resource Capabilities & Messages

* **`resources/list`**: returns available resources—with pagination via `cursor`.
* **`resources/read`**: fetches content for a specific URI.
* **`resources/templates/list`**: lists template definitions.
* Optional features:

  * `subscribe`: subscribe to updates on a resource.
  * `listChanged`: get notifications when available resources change.
    ([Medium][3], [Daily Dose of Data Science][2], [milvus.io][5], [modelcontextprotocol.io][1])

---

### 5. 🧠 Annotations: Resource Metadata

Resources can include optional metadata to guide usage:

| Annotation   | Description                        |
| ------------ | ---------------------------------- |
| audience     | `"user"` or `"assistant"`          |
| priority     | 0.0 (low) to 1.0 (high) importance |
| lastModified | ISO‑formatted timestamp            |

Agents or host applications can filter, prioritize, or sort resources based on these.
([huggingface.co][6], [modelcontextprotocol.io][1])

---

### 6. 🔄 Resources vs. Tools

* **Resources** are *application-controlled*, meaning the host selects when and which resource to use.
* **Tools** are *model‑controlled*—LLMs can discover and invoke them with permission.
* Use **resources** for read-only context; use **tools** when you need to perform actions.
  ([Reddit][7])

---

### 7. 📦 Example Flow

#### Mind Map:

```
MCP Resources
│
├─ Static Resource (fixed URI)
│
├─ Resource Template (dynamic with `{param}`)
│
├─ Methods:
│   ├─ resources/list
│   ├─ resources/read
│   ├─ resources/templates/list
│   ├─ notifications/resources/list_changed
│   └─ resources/subscribe
│
└─ Annotations: audience, priority, lastModified
```

---

### 8. 🧪 Sample Implementation (FastMCP Python)

```python
from fastmcp import FastMCP
import requests

mcp = FastMCP(name="DemoServer")

@mcp.resource("config://settings", description="App config")
def config():
    return {"mode": "demo", "version": "1.0"}

@mcp.resource("weather://{city}/today", description="Live weather data")
def weather(city: str):
    resp = requests.get(f"https://wttr.in/{city}?format=j1")
    return {"city": city, "temp_C": resp.json()["current_condition"][0]["temp_C"]}

@mcp.tool()
def show_weather(city: str, ctx):
    data = next(ctx.read_resource(f"weather://{city}/today"))
    return f"Weather in {city}: {data['temp_C']}°C"

mcp.run()
```

* `config://settings`: static resource.
* `weather://{city}/today`: template resource—fetches live weather.
* `show_weather`: tool logic reading a resource and returning a message.

---

### ✅ Summary Table

| Topic                   | Description                                           |
| ----------------------- | ----------------------------------------------------- |
| **Resource**            | Read-only context data provided to agents             |
| **Static Resource**     | Fixed URI mapping to data                             |
| **Resource Template**   | URI with `{param}` for dynamic resource requests      |
| **URI**                 | Unique identifier used to list/read resource          |
| **Annotations**         | Metadata guiding usage (audience, priority, etc.)     |
| **Difference vs Tools** | Tools perform actions; resources provide data context |



[1]: https://modelcontextprotocol.io/docs/concepts/resources?utm_source=chatgpt.com "Resources - Model Context Protocol"
[2]: https://www.dailydoseofds.com/model-context-protocol-crash-course-part-4/?utm_source=chatgpt.com "Building a Full-Fledged MCP Workflow using Tools, Resources, and ..."
[3]: https://ramwert.medium.com/mcp-demystifying-mcp-resources-vs-tools-a-practical-guide-for-agentic-automation-cb07fcb82241?utm_source=chatgpt.com "MCP : Demystifying MCP Resources vs. Tools: A Practical Guide for ..."
[4]: https://dev.to/debs_obrien/building-your-first-mcp-server-a-beginners-tutorial-5fag?utm_source=chatgpt.com "Building Your First MCP Server: A Beginners Tutorial"
[5]: https://milvus.io/ai-quick-reference/what-are-resources-in-model-context-protocol-mcp-and-how-do-i-expose-them?utm_source=chatgpt.com "What are “resources” in Model Context Protocol (MCP) and how do I ..."
[6]: https://huggingface.co/spaces/mcp-course/README/discussions/2?utm_source=chatgpt.com "mcp-course/README · Early Tool vs Resource Examples"
[7]: https://www.reddit.com/r/ClaudeAI/comments/1jso42a/mcp_resources_vs_tools/?utm_source=chatgpt.com "MCP Resources vs Tools : r/ClaudeAI - Reddit"
