import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner , set_tracing_export_api_key , trace
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams

load_dotenv(find_dotenv())

SERVER_URL = "http://localhost:8000/mcp"  # Your MCP server URL
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)




async def main():
    params = MCPServerStreamableHttpParams(url=SERVER_URL)
    async with MCPServerStreamableHttp(params=params, name="MCP Prompt Server") as server:
        # List available prompts
        prompts = await server.list_prompts()
        print("Available prompts:")
        for p in prompts.prompts:
            print(f" - {p.name}: {p.description}")

        # Select a prompt (here hard-coded, but you can use input())
        chosen_prompt = "generate_code_review_instructions"
        prompt_args = {"focus": "logic errors", "language": "python"}

        # Fetch prompt instructions
        prompt_result = await server.get_prompt(chosen_prompt, prompt_args)
        instructions = prompt_result.messages[0].content
        if hasattr(instructions, "text"):
            instructions = instructions.text
        else:
            instructions = str(instructions)

        print("Using instructions:", instructions)

        with trace("Prompts"):
        # Build the agent with dynamic instructions
            agent = Agent(
                name="Dynamic Instruction Agent",
                instructions=instructions,
                mcp_servers=[server],  # Enables future tool usage
                model=OpenAIChatCompletionsModel(
                    model="gemini-2.0-flash", openai_client=client
                ),
            )

        result = await Runner.run(
            starting_agent=agent,
            input="Please review this function for security issues."
        )
        print("Agent says:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
