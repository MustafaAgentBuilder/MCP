from mcp.server.fastmcp import FastMCP



mcp =FastMCP(

    name ="Lifecycle Testing",
    stateless_http = False,
    # json_response = True
)



app = mcp.streamable_http_app()