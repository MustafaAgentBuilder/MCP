

# MCP Agent with Tavily Remote Server

This project shows how to connect a OpenAI agent to a **remote MCP (Model Context Protocol)** server using the OpenAI Agents SDK. It’s beginner-friendly and easy to follow.

---

##  What This Project Does

- Connects your agent to **Tavily’s remote MCP server** using HTTP
- Uses a powerful language model (Gemini)
- Guides the agent to search for the latest news using tools provided by the server
- Everything runs remotely—**no local MCP installation needed**

---

##  Folder Structure

```

.
├── main.py           # Your agent code
├── server\_config.json# Example config (for local setup)
└── README.md         # This file

````

---

##  main.py Explained (Line by Line)

```python
import asyncio
import os
from dotenv import load_dotenv

from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_export_api_key
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
````

* These import necessary tools and classes.
* `dotenv` loads your API keys from a `.env` file for safety.

```python
load_dotenv()
```

* Loads environment variables from a `.env` file in your project folder.

```python
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
```

* Configures the language model provider with your Gemini API key stored safely outside the code.

```python
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=provider
)
```

* Specifies which model to use (Gemini-2.5-flash) and links it to the provider.

```python
set_tracing_export_api_key("OPENAI_API_KEY")
```

* (Optional) Enables debugging/tracing for your OpenAI usage.

```python
SERVER_URL = "https://mcp.tavily.com/mcp/?tavilyApiKey=YOUR_KEY"
mcp_parms = MCPServerStreamableHttpParams(url=SERVER_URL)
```

* Defines the remote MCP server URL with your Tavily API key included.
* This gives your agent permission to use remote tools over HTTPS.

```python
async def main_code():
    async with MCPServerStreamableHttp(
        params=mcp_parms,
        name="Agent Client",
    ) as agent_client:
        print("Connected to MCP server:", agent_client.name)
```

* Opens a connection to the remote MCP server using streamable HTTP transport.
* `agent_client.name` gives a friendly name for your connection.

```python
assistant = Agent(
    name="User Assistant",
    instructions="You are a helpful assistant",
    mcp_servers=[agent_client],
    model=model
)
```

* Sets up the `Agent`, giving it instructions, the model, and access to your MCP server.

```python
result = await Runner.run(
    assistant,
    "Tell me latest News about Pakistan"
)
print("RESULT:", result.final_output)
```

* Runs your agent with a prompt. The agent can use tools from the MCP server to answer.
* The final answer is printed on the screen.

```python
if __name__ == "__main__":
    asyncio.run(main_code())
```

* Standard Python way to run your async `main_code()` function when you run `python main.py`.

---

## server\_config.json (Local Example)

```json
{
  "mcpServers": {
    "tavily-mcp": {
      "command": "npx",
      "args": ["-y", "tavily-mcp"],
      "env": {
        "TAVILY_API_KEY": "YOUR_KEY"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

* This example is for running a local MCP server.
* It installs and runs the Tavily MCP server using `npx`, passing your API key through an environment variable.

---

## Why Use URL-Based API Key for Remote?

* Allows your agent to **connect directly** to Tavily’s tools over the internet—no need to run anything locally.
* **Pros:** Simple and quick setup using HTTPS.
* **Cons:** Query parameters may get logged in access logs. Use HTTPS to keep your key encrypted in transit.

---

## Summary Table

| Feature           | Description                                       |
| ----------------- | ------------------------------------------------- |
| Remote MCP Server | Connects directly to Tavily using HTTP            |
| Streamable HTTP   | Fast and efficient transport for tools via SDK    |
| Secure API Setup  | Keys stored in `.env`, not hard-coded             |
| Beginner-Friendly | Clear structure, easy to follow even for new devs |

---

## How to Run

1. Clone the repo.
2. Create a `.env` file:

   ```env
   GEMINI_API_KEY=your_gemini_key
   ```
3. Replace `YOUR_KEY` in `main.py` with your Tavily API key.
4. Install packages:

   ```bash
   pip install openai-agents
   ```
5. Run the agent:

   ```bash
   python main.py
   ```
6. See the result print out “NEWS ABOUT PAKISTAN”.
