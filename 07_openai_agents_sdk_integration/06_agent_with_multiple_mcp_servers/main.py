import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams

# Load env
load_dotenv(find_dotenv())

# MCP servers you want to connect
MCP_SERVER_URLS = [
    "http://localhost:8001/mcp",
    "http://localhost:8002/mcp",
]

# Gemini client
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

async def main():
    # Create MCP clients
    mcp_servers = [
        await MCPServerStreamableHttp.create(
            MCPServerStreamableHttpParams(url=url), 
            name=f"MCP_{i+1}"
        )
        for i, url in enumerate(MCP_SERVER_URLS)
    ]

    # Create agent
    assistant = Agent(
        name="MultiMCPAgent",
        instructions="You are a helpful assistant connected to multiple MCP servers.",
        mcp_servers=mcp_servers,
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    )

    # Run one test query
    result = await Runner.run(assistant, "Check weather in London and Junaid's mood.")
    print("\n[Agent Response]:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
