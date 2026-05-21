"""
Low-Level MCP Server Implementation (HTTP Transport)

Uses Starlette + Uvicorn for production-ready HTTP deployment.
Endpoint: http://localhost:${MCP_PORT:-8000}/mcp
"""

import asyncio
import logging
import os
import contextlib
from collections.abc import AsyncIterator
from typing import Any

from mcp.server import InitializationOptions
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send
import uvicorn
import mcp.types as types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('simple-math')
MCP_PORT = int(os.environ.get("MCP_PORT") or "8000")


def main():
    # ===========================================
    # Step 1: Create the Server Instance
    # ===========================================
    server = Server("simple-math")

    # ===========================================
    # Step 2: Define Available Tools
    # ===========================================
    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools with their schemas."""
        return [
            types.Tool(
                name="add",
                description="Add two numbers together",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["a", "b"],
                },
            ),
            types.Tool(
                name="subtract",
                description="Subtract second number from first",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["a", "b"]
                },
            ),
        ]

    # ===========================================
    # Step 3: Implement Tool Handlers
    # ===========================================
    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests."""
        try:
            if not arguments:
                raise ValueError("No arguments provided")

            if name == "add":
                if "a" not in arguments or "b" not in arguments:
                    raise ValueError("Missing required arguments: a, b")
                result = arguments['a'] + arguments['b']
                return [types.TextContent(type="text", text=str(result))]

            elif name == "subtract":
                if "a" not in arguments or "b" not in arguments:
                    raise ValueError("Missing required arguments: a, b")
                result = arguments['a'] - arguments['b']
                return [types.TextContent(type="text", text=str(result))]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            logger.error(f"Error executing tool '{name}': {e}")
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    # ===========================================
    # Step 4: Configure HTTP Session Manager
    # ===========================================
    session_manager = StreamableHTTPSessionManager(
        app=server,
        event_store=None,
        json_response=True,
        stateless=True,
    )

    # ===========================================
    # Step 5: Define Request Handler
    # ===========================================
    async def handle_streamable_http(
        scope: Scope, receive: Receive, send: Send
    ) -> None:
        """Handle incoming HTTP requests."""
        await session_manager.handle_request(scope, receive, send)

    # ===========================================
    # Step 6: Configure Application Lifecycle
    # ===========================================
    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        """Manage application startup and shutdown."""
        async with session_manager.run():
            logger.info(f"✓ MCP Server started at http://127.0.0.1:{MCP_PORT}/mcp")
            try:
                yield
            finally:
                logger.info("✓ MCP Server shutting down...")

    # ===========================================
    # Step 7: Create and Run ASGI Application
    # ===========================================
    starlette_app = Starlette(
        debug=True,
        routes=[
            Mount("/mcp", app=handle_streamable_http),
        ],
        lifespan=lifespan,
    )

    # Start the server
    uvicorn.run(starlette_app, host="0.0.0.0", port=MCP_PORT)


# Entry point
if __name__ == "__main__":
    main()
