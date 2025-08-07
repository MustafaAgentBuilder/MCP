
## MCP Prompts – Easy Explanation

### What Are MCP Prompts?

* **Prompts** in MCP are like **templates or pre-written messages** that guide how the AI (LLM) should respond.
* Instead of writing prompts from scratch every time, you can predefine them on the server and the user can choose which one to use in the interface (like using slash commands) ([Model Context Protocol][1]).

---

### Why Do We Use Prompts?

1. **User-Controlled** – Users pick which prompt they want the AI to follow (e.g., "Generate email draft", "Analyze code") ([Model Context Protocol][1]).
2. **Consistent Experience** – The same prompt template ensures consistent behavior: tone, structure, or style.
3. **Customizable** – You can add arguments so each prompt fits different needs (like passing specific code to review).

---

### How Prompts Work (Step-by-Step)

#### 1. **Listing Prompts**

The client asks the server for available prompts using `prompts/list`.

Example response:

```json
{
  "prompts": [
    {
      "name": "code_review",
      "title": "Request Code Review",
      "description": "Ask the AI to analyze your code and suggest improvements",
      "arguments": [{ "name": "code", "required": true }]
    }
  ]
}
```

This returns what templates are available and what inputs they need ([Model Context Protocol][1]).

#### 2. **Using a Prompt**

To get a prompt filled out, clients send `prompts/get` with the prompt name and arguments.

Example request:

```json
{
  "method": "prompts/get",
  "args": { "name": "code_review", "arguments": { "code": "print('Hello world')" } }
}
```

Server response:

```json
{
  "messages": [
    {
      "role": "user",
      "content": { "type": "text", "text": "Please review this code:\nprint('Hello world')" }
    }
  ]
}
```

The prompt is customized and ready for AI use ([Model Context Protocol][1]).

#### 3. **Prompt Changes**

If the server updates prompts, it informs clients via a `prompts/list_changed` notification, so clients can refresh the list ([Model Context Protocol][1]).

---

### Bonus: Why Prompts Are Useful

As one Reddit user shared:

> "MCP prompts help steer AI actions, analysis, and outputs... I used prompts to provide a consistent way to call tools, analyze output, and generate commands." ([Reddit][2])

Prompts help create consistent and guided agent behavior!

---

## Summary Table

| Concept           | Description                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| **Prompt**        | A reusable message template guiding AI behavior                          |
| **List Prompts**  | Show available prompts to users                                          |
| **Get Prompt**    | Fill prompt with user input (arguments) to customize the message         |
| **Notifications** | Server informs clients when prompt list changes (`prompts/list_changed`) |

---

## Quick Example

Think of a travel app:

* You have a prompt “Plan a vacation”.
* User selects it, enters destination and dates.
* The prompt template fills in the details and sends it to the AI for itinerary suggestions.



[1]: https://modelcontextprotocol.io/specification/2025-06-18/server/prompts?utm_source=chatgpt.com "Prompts - Model Context Protocol"
[2]: https://www.reddit.com/r/mcp/comments/1jtfnlh/learning_mcp_what_is_the_use_of_prompts_coming/?utm_source=chatgpt.com "Learning MCP : What is the use of prompts coming from the server?"
