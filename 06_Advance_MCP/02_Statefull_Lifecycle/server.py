#StateFull MCP Server

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "Hi",
    stateless_http = True
)



@mcp.tool(name="calculator", description="Perform mathematical calculations")
async def calculate(expression: str) -> str:
    try:
        result = eval(expression)  # Be careful with eval in production
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"
    

app = mcp.streamable_http_app()