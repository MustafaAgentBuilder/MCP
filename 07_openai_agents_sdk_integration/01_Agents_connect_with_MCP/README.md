# Sub-module 01: Connecting to an MCP Server (Streamable HTTP)

**Objective:** To demonstrate the basic configuration and connection of an OpenAI Agent to an MCP server that uses the `streamable-http` transport, utilizing the `MCPServerStreamableHttp` client class from the OpenAI Agents SDK.

## Core Concept

The primary goal here is to show an `Agent` being initialized with an `MCPServerStreamableHttp` instance. This instance acts as a client that points to a running MCP server. We want to confirm that the agent, upon initialization or when it first needs to interact with MCP tools, attempts to connect to this server. A common first interaction is for the agent (or the SDK on its behalf) to call `list_tools()` on the MCP server.

## Key SDK Concepts:

- `MCPServerStreamableHttpParams`: For configuring connection details to a `streamable-http` MCP server.
- `MCPServerStreamableHttp`: The client class in the SDK for interacting with such servers.
- `Agent(mcp_servers=[...])`: How to make an agent aware of MCP servers.
- `mcp_server_client.list_tools()`: Directly invoking tool listing (also done implicitly by the Agent).
- Asynchronous Context Management (`async with`) for `MCPServerStreamableHttp`.
- Using `Runner.run()` to execute an agent with a query.


| Class                               | Purpose                                                            |
| ----------------------------------- | ------------------------------------------------------------------ |
| **`MCPServerStreamableHttp`**       | Client for connecting to a remote MCP server using Streamable HTTP |
| **`MCPServerStreamableHttpParams`** | Settings container for configuring the remote server connection    |



---

### See Code in main.py or server.py 