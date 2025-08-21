from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession, types
import asyncio
from contextlib import AsyncExitStack
from typing import Any
from pydantic import AnyUrl
import json

class MCPClient:
    def __init__(self, url):
        self.url = url                # attribute: server URL
        self.stack = AsyncExitStack() # attribute: manages async contexts
        self._sess = None            # attribute: will hold ClientSession (None until opened)
        
    async def __aenter__(self):
        print("[MCPClient] Opening session...")  # log: session opening
        receive , send   = await self.stack.enter_async_context(
            streamablehttp_client(self.url)
        )
        self._sess = await self.stack.enter_async_context(
            ClientSession(receive , send)
        )
        await self._sess.initialize()
        print("[MCPClient] Session opened.")     # log: session ready
        return self
        
    async def __aexit__(self, *args):
        print("[MCPClient] Closing session...")  # log: closing
        await self.stack.aclose()
        print("[MCPClient] Session closed.")     # log: closed
    
    async def list_tools(self) -> list[types.Tool]:
        assert self._sess, "Session not available."
        return (await self._sess.list_tools()).tools
    
    # async def tool_call(self , ool_name, *args, **kwargs):
    #     return await self._sess.call_tool()
    
    async def tool_call(self, tool_name: str, arguments: dict | None = None):
        # """
        # Call a server tool by name.
        # - tool_name: e.g. "calculator"
        # - arguments: dict of the tool's parameters, e.g. {"expression": "2+3"}
        # Returns whatever the session returns (CallToolResult or raw result).
        # """
        assert self._sess, "Session not available."
        # Call the tool via the active ClientSession
        result = await self._sess.call_tool(tool_name, arguments or {})
        return result

    
    # ✅ Typo fixed here: method name is now list_resources
    async def list_resources(self) -> list[types.Resource]:
        assert self._sess, "Session not available."
        result: types.ListResourcesResult = await self._sess.list_resources()
        return result.resources

    async def list_resource_templates(self) -> list[types.ResourceTemplate]:
        assert self._sess, "Session not available."
        result: types.ListResourceTemplatesResult = await self._sess.list_resource_templates()
        # print("LIST RESOURCE TEMPLATES", result.__dict__)
        return result.resourceTemplates

    # async def read_resources(self, uri: str) -> types.ReadResourceResult:
    #     assert self._sess, "Session not available."
    #     result = await self._sess.read_resource(AnyUrl(uri))
    #     # print("READ RESOURCES DICT", result.__dict__)
    #     resource = result.contents[0]
    #     if isinstance(resource, types.TextResourceContents):
    #         if resource.mimeType == "application/json":
    #             try:
    #                 return json.loads(resource.text)
    #             except json.JSONDecodeError as e:
    #                 print(f"Error decoding JSON: {e}")
    #     return resource.text
        
async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        # tools = await client.list_tools()
        # print(tools, " tools")
        
        # resources = await client.list_resources()
        # print(resources[0].uri, " resources")

        # data = await client.read_resources(resources[0].uri)
        # print(data, " data")

        # for r in resources:
        #     data = await client.read_resources(r.uri)
        #     print(f"Resource URI: {r.uri}")
        #     print(f"Data: {data}")
       result = await client.tool_call("calculator", {"expression": "2+3"})
       print(result)



asyncio.run(main())
