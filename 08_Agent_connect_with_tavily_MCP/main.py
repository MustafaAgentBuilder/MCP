import asyncio
import os
from dotenv import load_dotenv

from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner,set_tracing_export_api_key
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams

load_dotenv()

# 1. Set up the LLM provider and model
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=provider
)

# Add you own OpenAI API key here for tracing
set_tracing_export_api_key("OPENAI_API_KEY")
# 2. Define the remote MCP server URL (replace with your actual key)
SERVER_URL = (

    "https://mcp.tavily.com/mcp/?tavilyApiKey=ADD_YOUR_OWN_TAVILY_API_KEY_HERE"
)
mcp_parms = MCPServerStreamableHttpParams(url=SERVER_URL)

async def main_code():
    async with MCPServerStreamableHttp(
        params=mcp_parms,
        name="Agent Client",
    ) as agent_client:
        print("Connected to MCP server:", agent_client.name)

        assistant = Agent(
            name="User Assistant",
            instructions="You are a helpful assistant",
            mcp_servers=[agent_client],
            model=model
        )

        # Run a sequence of tasks
        result = await Runner.run(
            assistant,
            "Tell me latest News about Pakistan"
        )
        print("RESULT:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main_code())
