import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner , set_tracing_disabled , enable_verbose_stdout_logging
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams , create_static_tool_filter


load_dotenv()
enable_verbose_stdout_logging()
SERVER_URL =  "http://localhost:8000/mcp"

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel( 
    model = "gemini-2.0-flash",
    openai_client= provider    
)

set_tracing_disabled(True)

static_tool = create_static_tool_filter(allowed_tool_names=[],blocked_tool_names=[])
async def main_code():

    #  These parameters tell the SDK how to reach the MCP server.
    mcp_parms = MCPServerStreamableHttpParams(url = SERVER_URL)
    print(f"MCP SERVER URL -> {mcp_parms}")

    async with MCPServerStreamableHttp(params = mcp_parms , name = "Agent Client", tool_filter=static_tool) as agent_client:
        print(f"MCPServerStreamableHttp Client Name {agent_client}")
        print("The SDK will use this client to interact with the MCP server.")



        try:
            assistant  =Agent(
                name = "User Assistant",
                instructions = "You are a Help Full assistant",
                mcp_servers=[agent_client],
                model = model
            )

            print(f"Agent '{assistant.name}' initialized with MCP server: '{agent_client.name}'.")
            print("Check the logs of your shared_mcp_server for a 'tools/list' request.")


            # tools = await agent_client.list_tools()
            # print(f"Tools -> {tools}")

            result = await Runner.run(assistant , "What is 2*2+34-21*2 and who ca i say hi in German")
            print("RESULT",result.final_output)


        except Exception as a:
            print(f"An error occurred during agent setup or tool listing: {a}")    


    print(f"MCPServerStreamableHttp client '{agent_client.name}' context exited.")
    print(f"--- Agent Connection Test End ---")


if __name__ == "__main__":
    asyncio.run(main_code())


