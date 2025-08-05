
## 🏗️ Overview: What is `FastMCP`?

`FastMCP` is a high‑level Python class (part of the MCP SDK) used to create an **MCP server** easily.
It helps you register tools, resources, prompts, and also add authentication and logging.
Think of it as a convenient **framework** or **wrapper** around low‑level MCP features. ([GitHub][1])

---

## 📦 `FastMCP(...)` parameters in detail:

```python
FastMCP(
    name: str | None = None,
    instructions: str | None = None,
    auth_server_provider: OAuthAuthorizationServerProvider[Any, Any, Any] | None = None,
    token_verifier: TokenVerifier | None = None,
    event_store: EventStore | None = None,
    *,
    tools: list[Tool] | None = None,
    **settings: Any
)
```

### 1. `name: str | None = None`

* Human-readable server name (e.g. `"MyAssistant"`).
* Used for logging or display in clients.

### 2. `instructions: str | None = None`

* A default instruction prompt for your server.
* Helps LLMs understand how to behave or what your server expects.

### 3. `auth_server_provider: OAuthAuthorizationServerProvider[...] | None = None`

* Enables OAuth 2.1 **authorization**.
* If your server is protected and requires login/permissions, you supply this provider.
* Manages redirect flows, discovering your auth server, user consent, and access tokens. ([GitHub][1], [gofastmcp.com][2])

### 4. `token_verifier: TokenVerifier | None = None`

* After a client connects and sends a token, MCP checks it with this verifier.
* Ensures tokens are valid and issued by a trusted auth server.

### 5. `event_store: EventStore | None = None`

* Optional: allows saving events, logs, requests, or tool calls for auditing.
* You can replay data or monitor usage.

### 6. `tools: list[Tool] | None = None`

* List of pre‑registered Tool objects.
* You can pass tools directly if you prefer not to use decorators.
* Otherwise, you decorate functions using `@mcp.tool()` after creating the `FastMCP` instance.

### 7. `**settings: Any`

* Arbitrary settings (like transport type, mount paths, debug flags).
* Flexibly configure behavior without changing code.

---

## 🧰 How and why you would use these

### ✅ Basic usage (no auth, simple tools):

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="DemoServer")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

mcp.run()
```

Add instructions if you need the LLM to follow a pattern:

```python
mcp = FastMCP(name="Demo", instructions="You are helpful assistant.")
```

---

### ✅ With authentication (OAuth flow):

If you want clients to authenticate via OAuth:

```python
auth = OAuthAuthorizationServerProvider(...)
verifier = TokenVerifier(...)
mcp = FastMCP(
    name="SecureServer",
    auth_server_provider=auth,
    token_verifier=verifier
)
```

Now only authorized clients can call your tools. ([PyPI][3], [GitHub][4], [GitHub][1])

---

### ✅ With event logging:

You provide an `EventStore` implementation to capture each tool invocation:

```python
mcp = FastMCP(
    name="LoggedServer",
    event_store=my_event_store_impl
)
```

Useful in production to track how your server is used.

---

## 📌 When to use each parameter

| Parameter              | When to include it                                    | Purpose                                |
| ---------------------- | ----------------------------------------------------- | -------------------------------------- |
| `instructions`         | When you want consistent system instructions for LLMs | Helps guide behavior                   |
| `auth_server_provider` | When you need **client authentication**               | Secure your MCP endpoints via OAuth    |
| `token_verifier`       | When verifying tokens from clients                    | Ensures only valid tokens are accepted |
| `event_store`          | When you want logging or event tracking               | Track tool calls, usage, and audit     |
| `tools`                | If you already built tool objects                     | Register tools programmatically        |
| `**settings`           | For transport or server configuration                 | Custom behavior without boilerplate    |

---

## 🧠 Why use `FastMCP`?

* It’s **easier** than the low-level `Server()` class — less code, simpler decorators.
* You get automatic schema generation, context injection, and structured output.
  You don’t write JSON schemas by hand — FastMCP reads your function type hints. ([Medium][5], [Medium][6], [GitHub][1], [Reddit][7])
* If you need advanced control (dynamic tools, runtime registration), you may fallback to `Server()` — but most use cases don’t need it. ([Reddit][7])

---

## ✅ Final Summary

* `FastMCP` is the user-friendly class to build MCP servers quickly.
* The parameters let you customize:

  * server name & instructions,
  * authentication (OAuth),
  * event logging,
  * initial tools,
  * and server behavior.
* Use it because it's **fast**, **Pythonic**, and handles boilerplate for you — while still flexible for production.

---
Great question, Mustafa! Let's break it down in **simple beginner-level words**:

---

## ✅ What does `stateless_http=True` mean?

### 🔹 `stateless_http=True`

This tells your MCP server:

> “Hey, don’t remember any old chat or session. Treat every new request as a **brand new** one.”

### ✅ Why use it?

* **Simple Testing**: Good when testing tools one by one.
* **Independent Calls**: No memory of previous questions or answers.
* **Fast & Clean**: Each call is quick and doesn’t store chat history.

### ❌ Without `stateless_http=True`

* The server will try to remember old messages.
* You’ll need to handle **session state**, history, and conversation memory.
* It's useful if you're building a **smart assistant that remembers things** (like ChatGPT does).


---

## 🧠 What is this doing?

This line creates a **web server app** that supports **streaming** responses — powered by **FastAPI** + **MCP SDK**.

It’s like saying:

> "Turn my MCP server into a real web server so people (like a client or browser or Postman) can connect to it on HTTP."

---

## 🧪 What does `streamable_http_app()` mean?

* `mcp` is your `FastMCP` instance.
* `.streamable_http_app()` is a **method** that prepares the app to:

  * Accept **HTTP requests**
  * Return **streaming responses**
  * Run on something like `localhost:8000`

---

## 🧩 So what is `mcp_app`?

* It becomes your **FastAPI app** (just like in a normal FastAPI project).
* Later, you **run** this app with:

```python
import uvicorn

uvicorn.run(mcp_app, host="localhost", port=8000)
```

---

## ✅ Summary:

| Line                                  | Meaning                                   |
| ------------------------------------- | ----------------------------------------- |
| `mcp = FastMCP(...)`                  | Create the MCP AI server                  |
| `mcp_app = mcp.streamable_http_app()` | Make that server accessible via HTTP API  |
| `uvicorn.run(...)`                    | Start the actual server to run and listen |

---


[1]: https://github.com/jlowin/fastmcp?utm_source=chatgpt.com "jlowin/fastmcp: The fast, Pythonic way to build MCP servers and clients"
[2]: https://gofastmcp.com/clients/auth/oauth?utm_source=chatgpt.com "OAuth Authentication - FastMCP"
[3]: https://pypi.org/project/fastmcp/1.0/?utm_source=chatgpt.com "fastmcp - PyPI"
[4]: https://github.com/modelcontextprotocol/python-sdk?utm_source=chatgpt.com "The official Python SDK for Model Context Protocol servers and clients"
[5]: https://medium.com/%40frulouis/4-obvious-libraries-for-building-mcp-servers-in-python-2025-19f3b5661590?utm_source=chatgpt.com "4 Obvious Libraries for Building MCP Servers in Python (2025) | by Fru"
[6]: https://medium.com/keycloak/securing-fastmcp-server-client-with-keycloak-using-ollama-llama-stack-in-python-5217efb40b43?utm_source=chatgpt.com "Securing FastMCP Server-Client with Keycloak Using Ollama ..."
[7]: https://www.reddit.com/r/mcp/comments/1i282ii/fastmcp_vs_server_with_python_sdk/?utm_source=chatgpt.com "FastMCP() vs. Server() with Python SDK? : r/mcp - Reddit"
