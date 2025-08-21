# Purpose: Demonstrates all types of dynamic tool filtering for MCP agents (simple, context-aware, async)
import asyncio
import os
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
from agents.mcp import ToolFilterContext
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, set_tracing_export_api_key ,trace
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams

load_dotenv()
# enable_verbose_stdout_logging()
SERVER_URL =  "http://localhost:8000/mcp"


set_tracing_export_api_key("Add OPENAI_API_KEY")

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client=provider    
)

# --- DYNAMIC TOOL FILTERS ---
# 1. Simple filter: Only allow tools whose name starts with "tools name"
def custom_filter(context: ToolFilterContext, tool) -> bool:
    # Only allow specific tools: text_translator, unit_converter, calculator
    allowed_tools = ["text_translator", "unit_converter", "calculator"]
    return tool.name in allowed_tools


def custom_filter(context: ToolFilterContext, tool) -> bool:
    # Only allow tools that start with "mood"
    print(f"\n\nContext: {context}\n\n")
    print(f"Tool: {tool.name}, Is Allowed: {tool.name.startswith('ca')}")
    return tool.name.startswith("cal")

def context_aware_filter(context: ToolFilterContext, tool) -> bool:
    # Only allow tools for a specific agent
    return context.agent.name == "User Assistant" and tool.name == "text_translator"





async def main_code():
    # These parameters tell the SDK how to reach the MCP server.
    mcp_parms = MCPServerStreamableHttpParams(url=SERVER_URL)
    print(f"MCP SERVER URL -> {mcp_parms}")

    async with MCPServerStreamableHttp(params=mcp_parms, name="Agent Client", tool_filter=custom_filter) as agent_client:
        print(f"MCPServerStreamableHttp Client Name {agent_client}")
        print("The SDK will use this client to interact with the MCP server.")

        try:
            assistant = Agent(
                name="User Assistant",
                instructions="You are a Help Full assistant",
                mcp_servers=[agent_client],
                model=model
            )

            print(f"Agent '{assistant.name}' initialized with MCP server: '{agent_client.name}'.")
            print("Check the logs of your shared_mcp_server for a 'tools/list' request.")

            # tools = await agent_client.list_tools()
            # print(f"Tools -> {tools}")
            
            print("---------------------------------------------")    
            with trace("Dynamic Tool call"):
                result = await Runner.run(
                    assistant, 
                    "What is 2 * 3 ",
                    )
                print("RESULT", result.final_output)

        except Exception as a:
            print(f"An error occurred during agent setup or tool listing: {a}")    

    print(f"MCPServerStreamableHttp client '{agent_client.name}' context exited.")
    print(f"--- Agent Connection Test End ---")

if __name__ == "__main__":
    asyncio.run(main_code())


