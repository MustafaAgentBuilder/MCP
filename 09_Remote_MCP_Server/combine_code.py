# combined_mcp.py
import os
from mcp.server.fastmcp import FastMCP
# import functions from your tool files (make sure these files do NOT create their own FastMCP)
from mcp_calculator import calculate, advanced_calculate, convert_base
from live_search import web_search, news_search

# Create one MCP server
mcp = FastMCP("Combined MCP Server")

# --------- Calculator tools ---------
@mcp.tool()
def calc_eval(expression: str):
    """Evaluate a math expression like '2+2'."""
    return calculate(expression)

@mcp.tool()
def calc_advanced(operation: str, operands: list, **kwargs):
    """Perform advanced calculations like add, subtract, multiply, etc."""
    return advanced_calculate(operation, operands, **kwargs)

@mcp.tool()
def calc_convert(number: str, from_base: int, to_base: int):
    """Convert a number between bases (e.g. binary to decimal)."""
    return convert_base(number, from_base, to_base)

# --------- Tavily search tools ---------
@mcp.tool()
def tavily_web_search(query: str, api_key: str = None, max_results: int = 5, search_depth: str = "basic", include_answer: bool = True):
    """Search the web with Tavily."""
    return web_search(query, api_key=api_key, max_results=max_results, search_depth=search_depth, include_answer=include_answer)

@mcp.tool()
def tavily_news_search(query: str, api_key: str = None, days: int = 7, max_results: int = 5, include_answer: bool = True):
    """Search for news articles with Tavily."""
    return news_search(query, api_key=api_key, days=days, max_results=max_results, include_answer=include_answer)


    
app = mcp.streamable_http_app()