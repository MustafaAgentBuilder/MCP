"""
MCP Tool Progress Server
Counts up to n, reporting progress and printing each step to the console.
"""
import asyncio
from mcp.server.fastmcp import FastMCP, Context  # same as mcp.server.fastmcp

mcp = FastMCP("Count Progress Server", stateless_http=False)

@mcp.tool()
async def count_numbers(n: int, ctx: Context) -> str:
    """Count up to n, reporting progress."""
    await ctx.info(f"Let's start counting to {n}!")
    print(f"[Server] Starting to count to {n}...")

    for i in range(n + 1):
        # Show how far we are
        await ctx.report_progress(progress=i, total=n, message=f"Count: {i}/{n}")
        # print(f"[Server] Count: {i}/{n}")
        await asyncio.sleep(0.1)  # simulate time
    await ctx.info("Counting finished!")
    print(f"[Server] Counting finished! Counted up to {n}.")
    return f"Done counting up to {n}."

# Setup the HTTP app (or other transport if preferred)
mcp_app = mcp.streamable_http_app()
