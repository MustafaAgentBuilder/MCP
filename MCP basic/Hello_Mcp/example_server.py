""" 
This Code out of order at that time we are not using it 

"""
from fastapi import FastAPI
from mcp import types
from mcp.server import Server
from mcp.server.fastapi import create_fastapi_app
from datetime import datetime
import json
import logging
from typing import Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# 1) CUSTOM EVENT STORE: append each event to a JSON lines file.
# ──────────────────────────────────────────────────────────────────────────────
class JSONFileEventStore:
    def __init__(self, file_path: str = "events.json"):
        self.file_path = file_path

    async def store_event(self, event: Any) -> None:
        """Store event to JSON file"""
        try:
            record = {
                "timestamp": datetime.utcnow().isoformat(),
                "event": event if isinstance(event, dict) else str(event)
            }
            with open(self.file_path, "a") as f:
                f.write(json.dumps(record) + "\n")
        except Exception as e:
            logger.error(f"Failed to store event: {e}")

# ──────────────────────────────────────────────────────────────────────────────
# 2) CREATE MCP SERVER
# ──────────────────────────────────────────────────────────────────────────────
server = Server("my-mcp-server")
event_store = JSONFileEventStore("mcp_events.log")

# ──────────────────────────────────────────────────────────────────────────────
# 3) DEFINE TOOLS
# ──────────────────────────────────────────────────────────────────────────────
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="say_hello",
            description="Returns a friendly greeting",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name to greet"
                    }
                },
                "required": ["name"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    # Log the tool call event
    await event_store.store_event({
        "tool_name": name,
        "arguments": arguments,
        "action": "tool_call"
    })
    
    if name == "say_hello":
        user_name = arguments.get("name", "Unknown")
        greeting = f"Hello, {user_name}! 👋 You've called say_hello."
        
        # Log the response
        await event_store.store_event({
            "tool_name": name,
            "response": greeting,
            "action": "tool_response"
        })
        
        return [types.TextContent(type="text", text=greeting)]
    else:
        error_msg = f"Unknown tool: {name}"
        await event_store.store_event({
            "tool_name": name,
            "error": error_msg,
            "action": "tool_error"
        })
        raise ValueError(error_msg)

# ──────────────────────────────────────────────────────────────────────────────
# 4) OPTIONAL: ADD RESOURCES SUPPORT
# ──────────────────────────────────────────────────────────────────────────────
@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available resources"""
    return [
        types.Resource(
            uri="file://events.log",
            name="Event Log",
            description="Log of all MCP events",
            mimeType="text/plain"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read resource content"""
    if uri == "file://events.log":
        try:
            with open("mcp_events.log", "r") as f:
                return f.read()
        except FileNotFoundError:
            return "No events logged yet."
    else:
        raise ValueError(f"Unknown resource: {uri}")

# ──────────────────────────────────────────────────────────────────────────────
# 5) CREATE FASTAPI APP
# ──────────────────────────────────────────────────────────────────────────────
# Create FastAPI app with MCP server
app = create_fastapi_app(server)

# Add custom routes if needed
@app.get("/")
async def root():
    return {"message": "MCP Server is running", "server_name": "my-mcp-server"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# ──────────────────────────────────────────────────────────────────────────────
# 6) RUN THE SERVER
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)