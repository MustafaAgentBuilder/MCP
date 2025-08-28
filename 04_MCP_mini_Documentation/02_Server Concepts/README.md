
## 1. What is an MCP Server?

* An **MCP server** is like a **specialized helper** your AI can talk to.
* Each server does one job well: e.g. file management, weather lookup, travel booking, or calendar/email handling.

---

## 2. The Three Building Blocks

Every server offers three kinds of things:

| Block        | What it does                        | Who decides when and how it’s used    |
| ------------ | ----------------------------------- | ------------------------------------- |
| **Tool**     | Performs an action (does something) | The AI model decides to call it       |
| **Resource** | Provides data (reads something)     | Your app (you) decide what to fetch   |
| **Prompt**   | Gives a template (asks something)   | The user picks from a menu or command |

---

### A. Tools (AI Actions)

* **What they are**: Functions your AI can invoke—like “searchFlights”, “sendEmail”, or “createCalendarEvent.”
* **How you use them**:

  1. AI lists available tools (`tools/list`).
  2. AI asks you (the user) for permission to run one.
  3. You approve, and the AI runs it (`tools/call`).
* **Example**:

  1. AI wants to book a flight.
  2. It calls `searchFlights(origin, destination, date)`.
  3. You see options and approve the best one.
  4. AI calls `createCalendarEvent(...)` to save your trip dates.

**Protocol operations:**

| Method       | Purpose                  | Returns                                |
| ------------ | ------------------------ | -------------------------------------- |
| tools/list | Discover available tools | Array of tool definitions with schemas |
| tools/call | Execute a specific tool  | Tool execution result                  |



---

### B. Resources (Context Data)

* **What they are**: Pieces of information—documents, calendar entries, email inboxes, weather data—that your app fetches for the AI.
* **How they work**:

  1. Your app calls `resources/list` to see what’s available (e.g. “Here are your calendars, files, and weather services.”).
  2. Your app picks specific resources by URI or fills in a template (like `weather://forecast/Sialkot/2025-08-03`).
  3. The app calls `resources/read` to retrieve the content (e.g. calendar events for June, the PDF of a document, or JSON weather data).
* **Why it matters**: AI needs up-to-date context—your day’s schedule, the latest flight prices, your project document—to give accurate answers.

**Protocol operations:**

| Method                     | Purpose                         | Returns                                |
| -------------------------- | ------------------------------- | -------------------------------------- |
| resources/list           | List available direct resources | Array of resource descriptors          |
| resources/templates/list | Discover resource templates     | Array of resource template definitions |
| resources/read           | Retrieve resource contents      | Resource data with metadata            |
| resources/subscribe      | Monitor resource changes        | Subscription confirmation              |


---

### C. Prompts (Interaction Templates)

* **What they are**: Pre-written “forms” or templates that guide a multi-step task.
* **How you use them**:

  1. User picks a prompt from a menu or types a slash command (e.g. `/plan-vacation`).
  2. The UI shows you fields to fill in (destination, dates, budget).
  3. The app calls `prompts/list` and `prompts/get` to load the template.
  4. After you fill it, the AI follows that structured flow—no guesswork needed.
* **Example**:

  * **Prompt**: “plan-vacation”
  * **Fields**: destination, duration, budget, interests
  * **Result**: AI knows exactly how to ask for flights, hotels, weather—and in what order.

**Protocol operations:**

| Method         | Purpose                    | Returns                               |
| -------------- | -------------------------- | ------------------------------------- |
| prompts/list | Discover available prompts | Array of prompt descriptors           |
| prompts/get  | Retrieve prompt details    | Full prompt definition with arguments |

---
# Example 1
## 3. Imagine a Travel-Planning **Scenario**

1. **User** clicks “Plan a Vacation” (`prompts/list` → `prompts/get` for “plan-vacation”).
2. A form appears:

   * Destination: **Barcelona**
   * Dates: **2024-06-15** to **2024-06-22**
   * Budget: **\$3,000**
   * Interests: **\[“architecture”, “food”]**
3. The AI reads your **calendar** (`resources/list` → `resources/read` on `calendar://events/June-2024`) to check free days.
4. The AI fetches the **weather** (`resources/read` on `weather://forecast/Barcelona/2024-06-15`).
5. The AI asks **you**: “Shall I search for flights now?” You say **Yes**.
6. It calls `searchFlights(origin: "NYC", destination: "Barcelona", date: "2024-06-15")` (**Tool**).
7. You pick a flight → AI calls `createCalendarEvent(...)` and `sendEmail(...)` to confirm.

All three building blocks work together:

* **Prompt** gave the structured workflow.
* **Resources** supplied calendar and weather context.
* **Tools** performed actions (flight search, calendar event, email).


# Example 2




## 5. 📎 Real-World Scenario

Let’s walk through a scenario to make it concrete ⭐:

### Travel Planning Assistant Example

1. **Server capabilities** include:

   * A **static resource**: `file:///Documents/Passport.pdf`
   * A **template resource**: `weather://forecast/{city}/{date}`
   * **Tools**: `searchFlights`, `createCalendarEvent`, etc.
   * **Prompts**: `plan-vacation`, `summary-meeting`

2. **User visits travel app** and selects *“Plan a Vacation”* prompt. The app shows a form and fills in:

   * Destination: `Barcelona`
   * Dates: `2025-09-01` to `2025-09-08`
   * Budget: `2000`
   * Interests: `[“architecture”, “food”]`

3. The app lists and fetches resources:

   * `resources/list` → finds `calendar://my-calendar/Sep-2025`
   * `resources/read` → gets your calendar entries
   * `resources/read` → fetches `weather://forecast/Barcelona/2025-09-01`
   * *(Optionally, subscribe to weather if planning interface updates in real-time)*

4. AI uses these as context to suggest flight options and hotel choices.

5. After AI asks for permission, tools are called:

   * `tools/call` → `searchFlights(origin: "NYC", destination: "Barcelona", date: "2025-09-01")`
   * Once you choose, `createCalendarEvent(...)`, `sendEmail(...)`, etc.

6. If the weather resource updates (say new forecast), the server triggers a:

   * `notifications/resources/updated`
   * The client may automatically `resources/read` again and update suggestions.

This flow ties together **Resources**, **Prompts**, and **Tools** beautifully to make a smart, context-aware system.

**Resources** = 📂 Data your AI needs (read-only).


---

## 4. Why This Matters for Your Exam

* **Tools** = “doers” (take action when AI asks).
* **Resources** = “readers” (bring in data your AI needs).
* **Prompts** = “guides” (give structured templates so users and AI don’t get lost).

### 🎯 Think like this:
**✅ Resource = notes you give to the LLM to read**

**✅ Tool = calculator or action the LLM can use itself**

