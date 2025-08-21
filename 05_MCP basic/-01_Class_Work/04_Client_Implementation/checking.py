
# Simple Testing code 

# asyncio.run(main())
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client
from typing import List, Dict, Any, Optional


class McpClient:
    def __init__(self, url: str):
        self.url = url
        self.stack = AsyncExitStack()
        self._session: Optional[ClientSession] = None

    async def __aenter__(self):
        try:
            # streamablehttp_client is actually an async context manager itself
            # that yields the session directly when entered
            self._session = await self.stack.enter_async_context(
                streamablehttp_client(self.url)
            )
            
            # Initialize the session
            await self._session.initialize()
            return self
            
        except Exception as e:
            print(f"Error during client initialization: {e}")
            await self.stack.aclose()
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._session:
                # Properly close the session first
                pass
        except Exception as e:
            print(f"Error during session cleanup: {e}")
        finally:
            await self.stack.aclose()

    # Tools functionality
    async def list_tools(self) -> List[types.Tool]:
        """List all available tools from the MCP server"""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        result = await self._session.list_tools()
        return result.tools

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> types.CallToolResult:
        """Call a specific tool with given arguments"""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        if arguments is None:
            arguments = {}
            
        return await self._session.call_tool(tool_name, arguments)

    # Resources functionality
    async def list_resources(self) -> List[types.Resource]:
        """List all available resources from the MCP server"""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        result = await self._session.list_resources()
        return result.resources

    async def read_resource(self, uri: str) -> types.ReadResourceResult:
        """Read a specific resource by URI"""
        if not self._session:
            raise RuntimeError("Session not initialized")
            
        return await self._session.read_resource(uri)

    async def subscribe_to_resource(self, uri: str) -> None:
        """Subscribe to resource updates"""
        if not self._session:
            raise RuntimeError("Session not initialized")
            
        await self._session.subscribe_to_resource(uri)

    async def unsubscribe_from_resource(self, uri: str) -> None:
        """Unsubscribe from resource updates"""
        if not self._session:
            raise RuntimeError("Session not initialized")
            
        await self._session.unsubscribe_from_resource(uri)

    # Prompts functionality
    async def list_prompts(self) -> List[types.Prompt]:
        """List all available prompts from the MCP server"""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        result = await self._session.list_prompts()
        return result.prompts

    async def get_prompt(self, name: str, arguments: Dict[str, str] = None) -> types.GetPromptResult:
        """Get a specific prompt with given arguments"""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        if arguments is None:
            arguments = {}
            
        return await self._session.get_prompt(name, arguments)

    # Additional utility methods
    async def get_server_info(self) -> Dict[str, Any]:
        """Get information about the MCP server"""
        if not self._session:
            raise RuntimeError("Session not initialized")
            
        return {
            "server_name": getattr(self._session, 'server_name', 'Unknown'),
            "server_version": getattr(self._session, 'server_version', 'Unknown'),
            "protocol_version": getattr(self._session, 'protocol_version', 'Unknown')
        }

    async def ping(self) -> bool:
        """Ping the server to check connectivity"""
        try:
            if not self._session:
                return False
            # Try to list tools as a connectivity test
            await self.list_tools()
            return True
        except Exception:
            return False


# Simple working example
async def simple_test():
    """Simple test that should work"""
    server_url = "http://127.0.0.1:8000/mcp"
    
    print(f"🔌 Connecting to MCP server at {server_url}...")
    
    try:
        async with McpClient(server_url) as client:
            print("✅ Connected successfully!")
            
            # Test tools
            print("\n📦 Testing tools...")
            tools = await client.list_tools()
            print(f"Found {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Test calculator if available
            if tools:
                calc_tool = next((t for t in tools if t.name == "calculator"), None)
                if calc_tool:
                    print("\n🧮 Testing calculator:")
                    result = await client.call_tool("calculator", {"expression": "10 + 5"})
                    print(f"  10 + 5 = {result.content[0].text}")
            
            # Test prompts
            print("\n📝 Testing prompts...")
            prompts = await client.list_prompts()
            print(f"Found {len(prompts)} prompts:")
            for prompt in prompts:
                print(f"  - {prompt.name}: {prompt.description}")
            
            # Test lesson plan prompt if available
            if prompts:
                lesson_prompt = next((p for p in prompts if "lesson" in p.name.lower()), None)
                if lesson_prompt:
                    print("\n📚 Testing lesson plan:")
                    result = await client.get_prompt(lesson_prompt.name, {
                        "subject": "Science",
                        "grade_level": "Grade 3",
                        "duration": "30 minutes"
                    })
                    print(f"  Generated plan: {result.messages[0].content.text[:100]}...")
            
            # Test resources
            print("\n📁 Testing resources...")
            resources = await client.list_resources()
            print(f"Found {len(resources)} resources:")
            for resource in resources:
                print(f"  - {resource.uri}: {resource.name}")
            
            # Test user resource if available
            if resources:
                user_resource = next((r for r in resources if "user" in r.uri), None)
                if user_resource:
                    print("\n👤 Testing user resource:")
                    # Replace template with actual user ID
                    user_uri = user_resource.uri.replace("{user_id}", "user_1")
                    result = await client.read_resource(user_uri)
                    print(f"  User data: {result.contents[0].text}")
            
            print("\n🎉 All tests completed successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nDebugging tips:")
        print("1. Make sure your server is running with: uv run server.py")
        print("2. Check if server is accessible: curl http://127.0.0.1:8000/mcp")
        print("3. Verify server logs for any errors")


# Alternative approach using direct session creation
async def alternative_approach():
    """Alternative approach that might work better"""
    server_url = "http://127.0.0.1:8000/mcp"
    
    print(f"🔌 Trying alternative connection to {server_url}...")
    
    try:
        # Direct approach without our wrapper class
        async with streamablehttp_client(server_url) as session:
            await session.initialize()
            print("✅ Connected with direct approach!")
            
            # Test basic functionality
            tools_result = await session.list_tools()
            print(f"Found {len(tools_result.tools)} tools")
            
            prompts_result = await session.list_prompts()
            print(f"Found {len(prompts_result.prompts)} prompts")
            
            resources_result = await session.list_resources()
            print(f"Found {len(resources_result.resources)} resources")
            
    except Exception as e:
        print(f"❌ Direct approach failed: {e}")


if __name__ == "__main__":
    print("🧪 Running MCP Client Tests...\n")
    
    # Try the simple test first
    asyncio.run(simple_test())
    
    print("\n" + "="*50)
    
    # If that fails, try the alternative
    asyncio.run(alternative_approach())



###############################
# Advance Code of Client 







import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client
from typing import List, Dict, Any, Optional


class McpClient:
    def __init__(self, url: str):
        self.url = url
        self.stack = AsyncExitStack()
        self._session: Optional[ClientSession] = None

    async def __aenter__(self):
        try:
            # The streamablehttp_client returns a session context manager
            # that yields read_stream, write_stream
            session_context = streamablehttp_client(self.url)
            read_stream, write_stream = await self.stack.enter_async_context(session_context)
            
            # Create MCP session with both streams
            self._session = await self.stack.enter_async_context(
                ClientSession(read_stream, write_stream)
            )
            
            # Initialize the session
            await self._session.initialize()
            return self
            
        except Exception as e:
            print(f"Error during client initialization: {e}")
            await self.stack.aclose()
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._session:
                # Properly close the session first
                pass
        except Exception as e:
            print(f"Error during session cleanup: {e}")
        finally:
            await self.stack.aclose()

    # Tools functionality
    async def list_tools(self) -> List[types.Tool]:
        """List all available tools from the MCP server"""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        result = await self._session.list_tools()
        return result.tools

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> types.CallToolResult:
        """Call a specific tool with given arguments"""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        if arguments is None:
            arguments = {}
            
        return await self._session.call_tool(tool_name, arguments)

    # Resources functionality
    async def list_resources(self) -> List[types.Resource]:
        """List all available resources from the MCP server"""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        result = await self._session.list_resources()
        return result.resources

    async def read_resource(self, uri: str) -> types.ReadResourceResult:
        """Read a specific resource by URI"""
        if not self._session:
            raise RuntimeError("Session not initialized")
            
        return await self._session.read_resource(uri)

    async def subscribe_to_resource(self, uri: str) -> None:
        """Subscribe to resource updates"""
        if not self._session:
            raise RuntimeError("Session not initialized")
            
        await self._session.subscribe_to_resource(uri)

    async def unsubscribe_from_resource(self, uri: str) -> None:
        """Unsubscribe from resource updates"""
        if not self._session:
            raise RuntimeError("Session not initialized")
            
        await self._session.unsubscribe_from_resource(uri)

    # Prompts functionality
    async def list_prompts(self) -> List[types.Prompt]:
        """List all available prompts from the MCP server"""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        result = await self._session.list_prompts()
        return result.prompts

    async def get_prompt(self, name: str, arguments: Dict[str, str] = None) -> types.GetPromptResult:
        """Get a specific prompt with given arguments"""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        if arguments is None:
            arguments = {}
            
        return await self._session.get_prompt(name, arguments)

    # Additional utility methods
    async def get_server_info(self) -> Dict[str, Any]:
        """Get information about the MCP server"""
        if not self._session:
            raise RuntimeError("Session not initialized")
            
        return {
            "server_name": getattr(self._session, 'server_name', 'Unknown'),
            "server_version": getattr(self._session, 'server_version', 'Unknown'),
            "protocol_version": getattr(self._session, 'protocol_version', 'Unknown')
        }

    async def ping(self) -> bool:
        """Ping the server to check connectivity"""
        try:
            if not self._session:
                return False
            # Try to list tools as a connectivity test
            await self.list_tools()
            return True
        except Exception:
            return False


async def demo_client():
    """Demonstration of how to use the MCP client"""
    # Based on your FastMCP server, the correct endpoint should be:
    urls_to_try = [
        "http://127.0.0.1:8000/mcp",  # Your server endpoint
        "http://localhost:8000/mcp",  # Alternative localhost
        "http://127.0.0.1:8000/sse",  # SSE endpoint (if supported)
        "http://localhost:8000/sse",  # Alternative SSE
    ]
    
    for url in urls_to_try:
        try:
            print(f"Trying to connect to: {url}")
            async with McpClient(url) as client:
                print("Connected to MCP server successfully!")
                
                # Test server connectivity
                is_connected = await client.ping()
                print(f"Server connectivity: {'OK' if is_connected else 'Failed'}")
                
                # Get server info
                try:
                    server_info = await client.get_server_info()
                    print(f"Server info: {server_info}")
                except Exception as e:
                    print(f"Could not get server info: {e}")
                
                # List and display tools
                try:
                    tools = await client.list_tools()
                    print(f"\nAvailable Tools ({len(tools)}):")
                    for tool in tools:
                        print(f"  - {tool.name}: {tool.description}")
                        
                    # Example tool call (replace with actual tool name and arguments)
                    if tools:
                        first_tool = tools[0]
                        print(f"\nCalling tool: {first_tool.name}")
                        try:
                            result = await client.call_tool(first_tool.name, {})
                            print(f"Tool result: {result}")
                        except Exception as e:
                            print(f"Tool call failed: {e}")
                            
                except Exception as e:
                    print(f"Error listing tools: {e}")

                # List and display resources
                try:
                    resources = await client.list_resources()
                    print(f"\nAvailable Resources ({len(resources)}):")
                    for resource in resources:
                        print(f"  - {resource.uri}: {resource.name} ({resource.mimeType})")
                        
                    # Example resource read (replace with actual resource URI)
                    if resources:
                        first_resource = resources[0]
                        print(f"\nReading resource: {first_resource.uri}")
                        try:
                            resource_content = await client.read_resource(first_resource.uri)
                            print(f"Resource content: {resource_content}")
                        except Exception as e:
                            print(f"Resource read failed: {e}")
                            
                except Exception as e:
                    print(f"Error listing resources: {e}")

                # List and display prompts
                try:
                    prompts = await client.list_prompts()
                    print(f"\nAvailable Prompts ({len(prompts)}):")
                    for prompt in prompts:
                        print(f"  - {prompt.name}: {prompt.description}")
                        
                    # Example prompt get (replace with actual prompt name and arguments)
                    if prompts:
                        first_prompt = prompts[0]
                        print(f"\nGetting prompt: {first_prompt.name}")
                        try:
                            prompt_result = await client.get_prompt(first_prompt.name, {})
                            print(f"Prompt result: {prompt_result}")
                        except Exception as e:
                            print(f"Prompt get failed: {e}")
                            
                except Exception as e:
                    print(f"Error listing prompts: {e}")
                
                # If we get here, connection was successful, so break out of the loop
                return
                
        except Exception as e:
            print(f"Connection to {url} failed: {e}")
            continue
    
    # If we get here, all URLs failed
    print("Failed to connect to any MCP server URL. Please check:")
    print("1. MCP server is running")
    print("2. Server URL and port are correct")
    print("3. Server supports HTTP transport")
    print("4. Firewall/network settings allow connection")


# Alternative simple usage example
async def simple_usage():
    """Simple usage example with error handling"""
    urls_to_try = [
        "http://localhost:8000/sse",
        "http://localhost:8000/mcp",
        "http://127.0.0.1:8000/sse",
        "http://127.0.0.1:8000/mcp",
    ]
    
    for url in urls_to_try:
        try:
            async with McpClient(url) as client:
                # List all available capabilities
                tools = await client.list_tools()
                resources = await client.list_resources()
                prompts = await client.list_prompts()
                
                print(f"Connected to {url}")
                print(f"Server has {len(tools)} tools, {len(resources)} resources, {len(prompts)} prompts")
                return
        except Exception as e:
            print(f"Failed to connect to {url}: {e}")
            continue
    
    print("Could not connect to any MCP server")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_client())
    
    # Or run simple usage
    # asyncio.run(simple_usage())




##########################
# Correct Code Normal



