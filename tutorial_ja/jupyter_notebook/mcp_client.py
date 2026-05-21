"""
MCP Client that connects to and invokes tools from MCP servers.

Supports:
- Stdio transport (for local servers)
- HTTP transport (for remote/HTTP servers)

Usage:
    python mcp_client.py                           # Default: mcp_server.py (stdio)
    python mcp_client.py mcp_server.py             # High-level server (stdio)
    python mcp_client.py mcp_server_low_level.py   # Low-level server (stdio)
    python mcp_client.py --http                    # HTTP mode (localhost:${MCP_PORT:-8000})
    python mcp_client.py --http http://custom:8080/mcp  # Custom HTTP URL
"""

import asyncio
import argparse
import os
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client

DEFAULT_MCP_PORT = os.environ.get("MCP_PORT") or "8000"
DEFAULT_HTTP_URL = f"http://localhost:{DEFAULT_MCP_PORT}/mcp"


class MCPClient:
    """A client for connecting to MCP servers via Stdio or HTTP transport."""

    # ===========================================
    # Step 1: Initialize __init__()
    # Set up session placeholder and AsyncExitStack for resource management
    # ===========================================
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    # ===========================================
    # Step 2: Define connect_to_server()
    # Launch and connect to local server via Stdio transport
    # ===========================================
    async def connect_to_server(self, server_script_path: str):
        print(f"→ Connecting to server: {server_script_path}")
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path]
        )
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )
        await self.session.initialize()

    # ===========================================
    # Step 3: Define connect_to_server_http()
    # Connect to remote server via HTTP transport
    # ===========================================
    async def connect_to_server_http(self, url: str):
        print(f"→ Connecting to HTTP server: {url}")
        streamablehttp_transport = await self.exit_stack.enter_async_context(
            streamablehttp_client(url)
        )
        self.read, self.write, _ = streamablehttp_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.read, self.write)
        )
        await self.session.initialize()

    # ===========================================
    # Step 4: Define list_tools()
    # Discover available tools from the connected server
    # ===========================================
    async def list_tools(self):
        res_tools = await self.session.list_tools()
        return res_tools.tools

    # ===========================================
    # Step 5: Define call_tool()
    # Execute a specific tool with arguments
    # ===========================================
    async def call_tool(self, tool_name: str, arguments: dict):
        result = await self.session.call_tool(tool_name, arguments)
        return result.content[0].text

    # ===========================================
    # Step 6: Define cleanup()
    # Release all resources by closing the AsyncExitStack
    # ===========================================
    async def cleanup(self):
        await self.exit_stack.aclose()


async def test_tools(client: MCPClient):
    """Test the available tools on the connected server."""
    tools = await client.list_tools()
    print(f"\n✓ Connected to server with tools: {[tool.name for tool in tools]}")

    print("\n→ Calling add(2, 3)")
    result = await client.call_tool('add', {'a': 2, 'b': 3})
    print(f"  Result: {result}")

    print("\n→ Calling subtract(7, 4)")
    result = await client.call_tool('subtract', {'a': 7, 'b': 4})
    print(f"  Result: {result}")


async def main_stdio(server_path: str):
    """Run client with Stdio transport."""
    client = MCPClient()
    try:
        await client.connect_to_server(server_path)
        await test_tools(client)
    finally:
        await client.cleanup()


async def main_http(url: str):
    """Run client with HTTP transport."""
    client = MCPClient()
    try:
        await client.connect_to_server_http(url)
        await test_tools(client)
    finally:
        await client.cleanup()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="MCP Client - Connect to MCP servers and invoke tools"
    )
    parser.add_argument(
        'server',
        nargs='?',
        default='mcp_server.py',
        help='Path to server script (default: mcp_server.py)'
    )
    parser.add_argument(
        '--http',
        nargs='?',
        const=DEFAULT_HTTP_URL,
        help=f'Use HTTP transport (default URL: {DEFAULT_HTTP_URL})'
    )

    args = parser.parse_args()

    if args.http:
        url = args.http
        asyncio.run(main_http(url))
    else:
        asyncio.run(main_stdio(args.server))
