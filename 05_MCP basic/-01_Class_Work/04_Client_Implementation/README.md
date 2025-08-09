
## Corrected, short flow (easy words)

1. **Open a transport (streamable HTTP) → get channels**

   * `streamablehttp_client(self.url)` opens a long-lived HTTP stream connection and returns channels you can use to send and receive messages. ([Claude MCP Community][1], [GitHub][2])

2. **Wrap the channels with `ClientSession` → session object**

   * `ClientSession(read, write)` uses those channels to create a **session** that knows how to speak the MCP protocol (it gives you methods like `initialize()`, `list_tools()`, `call_tool()`, `list_resources()`, `read_resource()`). ([Medium][3], [LlamaIndex][4])

3. **Call `initialize()` → handshake / ready**

   * `await session.initialize()` finishes any handshake/setup so the session is ready to use.

4. **Use session methods → ask the server to run tools or return resources**

   * When you call `await session.call_tool(...)` or `await session.read_resource(...)`, the session **sends a request** to the server, the server runs the tool or reads the resource, and sends back a response that the client returns to you. ([GitHub][5], [Microsoft GitHub][6])

5. **Close everything with `AsyncExitStack` / `__aexit__` → cleanup**

   * `AsyncExitStack` remembers the stream and session and closes them in the correct order when you exit the `async with` block. This avoids leaking connections. ([Claude MCP Community][1])

