
## 🧠 What is JSON-RPC 2.0?

* It's a way for programs to **call functions remotely**, like saying:
  *“Hey server, run this function and give me the result.”*
* It uses **JSON** format (just text data) to send and receive messages.
* Works over **any network**: HTTP, WebSockets, etc.
* It's **stateless**: each request carries all needed info.

---

## 📦 1. Basic Request Format (What you send)

```json
{
  "jsonrpc": "2.0",
  "method": "functionName",
  "params": [or {"named": "params"}],
  "id": 1
}
```

| Field     | Description                                        |
| --------- | -------------------------------------------------- |
| `jsonrpc` | Always `"2.0"`                                     |
| `method`  | Function name to call on the server                |
| `params`  | Parameters (optional, can be a list or object)     |
| `id`      | Unique ID (optional, but needed to get a response) |

---

## 📬 2. Notification (No response needed)

* If you **don’t include `id`**, it’s a **notification**.
* Server won’t reply.
* Used when client doesn’t care about response (like logging or event).

```json
{
  "jsonrpc": "2.0",
  "method": "logSomething",
  "params": ["Hello"]
}
```

---

## 📥 3. Response from Server

If the request has `id`, the server sends this back:

✅ **Success**

```json
{
  "jsonrpc": "2.0",
  "result": 42,
  "id": 1
}
```

❌ **Error**

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32601,
    "message": "Method not found"
  },
  "id": 1
}
```

---

## ⚠️ 4. Common Error Codes

| Code    | Message            | Reason                  |
| ------- | ------------------ | ----------------------- |
| -32700  | Parse error        | Bad JSON sent           |
| -32600  | Invalid Request    | Request format is wrong |
| -32601  | Method not found   | Function doesn’t exist  |
| -32602  | Invalid params     | Wrong function inputs   |
| -32603  | Internal error     | Server-side bug         |
| -32000+ | Server error range | Custom server errors    |

---

## 📚 5. Param Types (2 Ways)

* **By position** (like a list):

  ```json
  "params": [5, 3]
  ```
* **By name** (like a dictionary):

  ```json
  "params": {"a": 5, "b": 3}
  ```

---

## 📦 6. Batch Requests (Multiple at once)

* Send an **array** of request objects
* Server replies with an array of responses

```json
[
  { "jsonrpc": "2.0", "method": "a", "id": 1 },
  { "jsonrpc": "2.0", "method": "b", "id": 2 }
]
```

---

## 📊 Example Summary

| Task             | Request                                     | Response                  |
| ---------------- | ------------------------------------------- | ------------------------- |
| Subtract 42 - 23 | `params: [42, 23]`                          | `result: 19`              |
| Named params     | `params: {"minuend": 42, "subtrahend": 23}` | `result: 19`              |
| Notification     | No `id`                                     | No response               |
| Wrong method     | `method: "foobar"`                          | `error: Method not found` |

---

## 🤖 Why JSON-RPC is Used in AI Agent Protocols (MCP)

### 🔄 REST is not enough:

* REST is for CRUD (Create, Read, Update, Delete) → good for simple web APIs
* But AI agents need **commands**, **sessions**, **streams**, not just CRUD

### ✅ JSON-RPC is better because:

| Feature             | REST                    | JSON-RPC ✅                   |
| ------------------- | ----------------------- | ---------------------------- |
| Call any method     | ❌ Limited to HTTP verbs | ✅ Yes                        |
| Streaming data      | ❌ Hard                  | ✅ Easy with WebSocket        |
| Notifications       | ❌ Not natural           | ✅ Built-in                   |
| Batch requests      | ❌ Hard                  | ✅ Built-in                   |
| Structured errors   | ❌ Not standard          | ✅ Standard format            |
| Multiplexing        | ❌ One request at a time | ✅ Many in one connection     |
| Stateful workflows  | ❌ Stateless only        | ✅ Track with session ID      |
| Agent Tools support | ❌ No                    | ✅ Works with LSP/Debug tools |

---

## 🧠 Final Thoughts

JSON-RPC is great for:

* Building **smart systems** like chatbots, LLM agents, IDE tools
* Handling **procedures, sessions, tools**, not just data
* Providing clear, **structured errors and results**
* Sending **commands**, not just accessing data

---
