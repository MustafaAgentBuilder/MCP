import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner ,set_tracing_export_api_key,trace
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams


load_dotenv()
# enable_verbose_stdout_logging()
SERVER_URL =  "http://localhost:8000/mcp"

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client= provider    
)

set_tracing_export_api_key("OPENAI_API_KEY")
# set_tracing_disabled(True)
# set_default_openai_api()

async def main_code():

    #  These parameters tell the SDK how to reach the MCP server.
    mcp_parms = MCPServerStreamableHttpParams(url = SERVER_URL)
    print(f"MCP SERVER URL -> {mcp_parms}")

    async with MCPServerStreamableHttp(params = mcp_parms , name = "Agent Client" , cache_tools_list=True ) as agent_client:
        print(f"MCPServerStreamableHttp Client Name {agent_client}")
        print("The SDK will use this client to interact with the MCP server.")
        print(f"Cache Tools List Enabled: {agent_client.cache_tools_list}")
        
        # ✅ First fetch the tools list
        tools_before = await agent_client.list_tools()
        print(f"Initial Tools List: {[t.name for t in tools_before]}")

        # ✅ Later check again if server tools changed
        tools_after = await agent_client.list_tools()
        print(f"Updated Tools List: {[t.name for t in tools_after]}")

        # ✅ Compare lists → if changed, refresh the cache
        if tools_before != tools_after:
            print("⚡ Tools have been updated on server → Invalidating cache...")
            agent_client.invalidate_tools_cache()
        else:
            print("✅ No changes in server tools. Cache is fine.")


        try:
            with trace("Tools Cache"):
                assistant  =Agent(
                    name = "User Assistant",
                    instructions = "You are a Help Full assistant",
                    mcp_servers=[agent_client],
                    model = model
                )

            print("-------------First Agent Run------------------")
            result = await Runner.run(assistant , "My Name is Mustafa convert my name is to German language")
            print("RESULT",result.final_output)
            print("-------------Second Agent Run-----------------")
            result = await Runner.run(assistant , "Wha is 2*2+34-22")
            print("RESULT",result.final_output)  
            
            print("-------------Third Agent Run------------------")
            result = await Runner.run(assistant , "22 celsius convert into fahrenheit")
            print("RESULT",result.final_output)    

            print("--------------Fourth Agent---------------------")
            result = await Runner.run(assistant , "Tell me about Pakistan Best Cricket Player ")
            print("RESULT",result.final_output)
        except Exception as a:
            print(f"An error occurred during agent setup or tool listing: {a}")


    print(f"MCPServerStreamableHttp client '{agent_client.name}' context exited.")
    print(f"--- Agent Connection Test End ---")


if __name__ == "__main__":
    asyncio.run(main_code())
