# Module 2: Caching MCP Tool Lists with OpenAI Agents SDK

## Introduction

When an Agent interacts with an MCP server, it typically calls `list_tools()` to discover available tools. Frequent calls, especially to remote servers, can introduce latency. The OpenAI Agents SDK provides a way to cache this tool list to improve performance.

This module explains how to enable and verify tool list caching when using MCP server clients with the OpenAI Agents SDK, referencing the official SDK documentation.

As stated in the [OpenAI Agents SDK MCP Documentation](https://openai.github.io/openai-agents-python/mcp/):

> Every time an Agent runs, it calls `list_tools()` on the MCP server. This can be a latency hit, especially if the server is a remote server. To automatically cache the list of tools, you can pass `cache_tools_list=True`.


## Enabling Caching

To enable tool list caching, pass the boolean parameter `cache_tools_list=True` directly to the constructor of your MCP server client (e.g., `MCPServerStreamableHttp`, `MCPServerStdio`, or `MCPServerSse`).

```python
    async with MCPServerStreamableHttp(params=mcp_params_cached, name="CachedClient", cache_tools_list=True)
```

If you want to invalidate the cache, you can call invalidate_tools_cache() on the servers.


## Verifying Caching Behavior

**Server-Side Logs**: The most reliable way to verify caching is to check your MCP server's logs. When client-side caching is active, the server should receive significantly fewer `ListToolsRequest` messages for repeated `list_tools()` calls from the same client instance.