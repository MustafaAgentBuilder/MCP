from mcp.server.fastmcp import FastMCP
import random
# Initialize FastMCP server with enhanced metadata for 2025-06-18 spec
mcp = FastMCP(
    name="hello-server",
    stateless_http=True
)

@mcp.tool(name="Get weather")
def get_weather(city: str)->str:
    # TODO Implement Search logic 
    return f"Weather is {city} Sunny"


mcp_app = mcp.streamable_http_app()
