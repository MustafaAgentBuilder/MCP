
## 🟢 What is Elicitation?

👉 **Elicitation** = A way for the **server** to ask the **user (through the client)** for extra information **while something is already happening**.

Think of it like this:

* Server is doing some work.
* It realizes it needs more info from the user (like an email, username, or choice).
* Instead of stopping, it **pauses** and **asks the client to show the user a question**.
* The user answers → client sends it back → server continues.

So, **Elicitation = Server asks → Client shows → User answers → Back to Server**.

---

## 🟢 Why do we need it?

Because sometimes the server **can’t finish a task without more info**.

💡 Example:

* You ask the server: *“Generate a GitHub repo report.”*
* Server: *“Wait, I need your GitHub username first.”* → (Elicitation happens).
* User types: *octocat* → Server now continues the task.

---

## 🟢 How does it work? (Easy steps)

1. **Server asks** → sends `elicitation/create` request with:

   * A **message** (“Please provide your GitHub username”).
   * A **schema** (rules for what kind of data is needed, e.g., must be a string).

2. **Client shows UI** → maybe a form or input box.

3. **User responds** → three options:

   * ✅ **Accept** → give the info.
   * ❌ **Decline** → say "No, I won’t give this info."
   * 🚪 **Cancel** → close/ignore the request.

4. **Client sends back to Server** → with user’s decision.

5. **Server continues** → using the new info (or handles decline/cancel).

---

## 🟢 Types of Responses

* **Accept** → Server gets the data and continues.
* **Decline** → Server knows the user refused.
* **Cancel** → Server knows the user just closed/dismissed.

---

## 🟢 Example in Real Life

* Imagine you’re filling out a form online.
* The server suddenly needs your **email**.
* A small box pops up → *“Please enter your email”*.
* You can:

  * Enter email → **Accept**
  * Say *“No thanks”* → **Decline**
  * Close the box → **Cancel**

---

## 🟢 Important Rules

* 🚫 Server must **not** ask for sensitive info (like passwords, credit cards).
* ✅ Client should let the user **see, edit, or reject** what is being sent.
* ⚡ Only **simple data** is allowed (strings, numbers, booleans, enums).

---

💡 **Simple Definition:**
Elicitation = The server’s way of politely saying:
*"Hey user, I need a bit more info before I continue. Can you give me this?"*

---

### Example of code:

```json

{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "elicitation/create",
  "params": {
    "message": "Please provide your contact information",
    "requestedSchema": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Your full name"
        },
        "email": {
          "type": "string",
          "format": "email",
          "description": "Your email address"
        },
        "age": {
          "type": "number",
          "minimum": 18,
          "description": "Your age"
        }
      },
      "required": ["name", "email"]
    }
  }
}

```