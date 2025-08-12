from mcp.server.fastmcp import FastMCP



mcp =FastMCP(

    name ="Lifecycle Testing",
    stateless_http = False,
)



app = mcp.streamable_http_app()