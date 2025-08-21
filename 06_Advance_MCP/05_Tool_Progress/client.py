import asyncio
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.shared.context import RequestContext
async def progress_handler(progress: float, total: float | None, message: str | None):
    """Handle progress updates from the server"""
    if total:
        percentage = (progress / total) * 100
        progress_bar = "█" * int(percentage // 5) + "░" * (20 - int(percentage // 5))
        print(f"    📊 [{progress_bar}] {percentage:.1f}% - {message or 'Working...'}")
    else:
        print(f"    📊 Progress: {progress} - {message or 'Working...'}")

async def main():
    """
    Simple MCP client that demonstrates progress tracking for count_numbers tool.
    """
    print("🚀 Starting MCP Progress Demo")
    print("=" * 50)

    # Connect using streamable HTTP client
    async with streamablehttp_client("http://localhost:8000/mcp/") as (read_stream, write_stream, get_session_id):
        async with ClientSession(read_stream, write_stream) as session:
            print("✅ Connected to MCP server!")

            # Initialize the session
            init_result = await session.initialize()
            print(f"🔧 Server capabilities: {init_result.capabilities}")

            # List available tools
            tools_result = await session.list_tools()
            print(f"🛠️ Available tools: {[tool.name for tool in tools_result.tools]}")

            # Call the count_numbers tool with n=10
            n = 10
            print(f"\n🔢 Counting up to {n}")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "count_numbers",
                    {"n": n},
                    progress_callback=progress_handler
                )
                print("-" * 40)
                if result.content:
                    for content in result.content:
                        print(f"✅ Result: {content}")
                else:
                    print("✅ Tool completed successfully (no output)")
            except Exception as e:
                print(f"❌ Error calling tool: {e}")
            print()  # Extra spacing

    print("🎉 Demo completed!")
    print("\n💡 Progress updates were sent in real-time via MCP protocol!")

if __name__ == "__main__":
    asyncio.run(main())