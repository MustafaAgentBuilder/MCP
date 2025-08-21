from mcp import ClientSession, types                   # MCP client session and type definitions
from mcp.client.streamable_http import streamablehttp_client  # HTTP transport for MCP
from contextlib import AsyncExitStack                  # Helper to clean up multiple async contexts
import asyncio                                         # Python’s async I/O library

class McpClient:
    def __init__(self, url):
        # Save the server URL and prepare a stack for cleanup
        self.url = url
        self.stack = AsyncExitStack()
        self._sess = None  # Will hold our MCP session after entering context

    async def __aenter__(self):
        """
        Called when we enter 'async with McpClient(...) as client:'.
        Sets up the HTTP connection and initializes the MCP session.
        """
        # Open a streaming HTTP connection to the MCP server
        read, write, _ = await self.stack.enter_async_context(
            streamablehttp_client(self.url)
        )

        # Create and enter the MCP protocol session over that HTTP stream
        self._sess = await self.stack.enter_async_context(
            ClientSession(read, write)
        )

        # Perform any handshake or initialization steps
        await self._sess.initialize()

        # Return this object so the caller can use its methods
        return self

    async def __aexit__(self, *args):
        """
        Called when exiting the 'async with' block.
        Closes all resources in our exit stack (HTTP + session).
        """
        await self.stack.aclose()

    async def list_tool(self) -> list[types.Tool]:
        """
        Fetches and returns the list of tools available on the server.
        """
        result = await self._sess.list_tools()  # Ask the server for its tools
        return result.tools                     # Extract the list of Tool objects

    async def call_tool(self, tool_name, *args, **kwargs):
        """
        Calls a named tool with any arguments, and returns its response.
        """
        return await self._sess.call_tool(tool_name, *args, **kwargs)

    async def resources(self):
        """
        Retrieves resource usage info (like memory, open streams, etc.).
        """
        return await self._sess.resources()

async def main():
    # Use our client in an 'async with' so it sets up and tears down cleanly
    async with McpClient("http://localhost:8000/mcp") as client:
        # List the tools and print them
        tools = await client.list_tool()
        print("Tools:", tools)

# Start the asyncio event loop and run our main() function
asyncio.run(main())
