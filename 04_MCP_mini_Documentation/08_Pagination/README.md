## 🔹 What is Pagination in MCP?

Imagine you ask a library for a list of **10,000 books** 📚.
If the library sends **all books in one message**, your computer may **hang** or **slow down**.

👉 So instead of sending all at once, the server sends results in **small parts (pages)**.
That’s called **Pagination**.

---

## 🔹 How MCP Does It?

MCP doesn’t use "page 1, page 2, page 3" numbers.
Instead, it uses a **cursor** → like a bookmark 📖.

* `cursor` = tells the server **where to continue next time**.
* `page size` = decided by the server (client cannot force it).

---

## 🔹 How It Works Step by Step

1. **Client asks** → “Give me resources”

   ```json
   {
     "jsonrpc": "2.0",
     "method": "resources/list"
   }
   ```

2. **Server replies** → “Here’s the first part + a bookmark (cursor)”

   ```json
   {
     "jsonrpc": "2.0",
     "id": "123",
     "result": {
       "resources": [...],
       "nextCursor": "abc123"
     }
   }
   ```

   * `resources` = first batch
   * `nextCursor` = bookmark to get the next batch

3. **Client uses cursor** → “Continue from `abc123`”

   ```json
   {
     "jsonrpc": "2.0",
     "method": "resources/list",
     "params": {
       "cursor": "abc123"
     }
   }
   ```

4. **Loop continues** until server stops sending `nextCursor`.

---

## 🔹 Which MCP Operations Use Pagination?

Pagination is used for lists that can get **very big**:

* `resources/list` → list of all resources
* `resources/templates/list` → list of resource templates
* `prompts/list` → list of prompts
* `tools/list` → list of tools

---

## 🔹 Client & Server Rules

✅ **Server should:**

* Give a **stable cursor** (bookmark works correctly).
* Handle **invalid cursors** nicely.

✅ **Client should:**

* Stop when `nextCursor` is missing → means “no more data”.
* Never guess or edit the cursor (just use it as is).
* Don’t save cursors across different sessions.

❌ **Don’t** treat cursor like a number (`page=1,2,3`) → it’s just a token.

---

## 🔹 Error Handling

If the client sends a **bad cursor**, server replies with:
`-32602 (Invalid params)` error.

---

✅ In **super simple words**:

* Pagination = breaking big results into smaller chunks.
* Cursor = bookmark to continue from where you left off.
* Server decides chunk size.
* Client just keeps asking until no more cursor is given.

