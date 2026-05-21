"""
Low-Level MCP Server Implementation (Stdio Transport)

This server demonstrates how to build MCP servers with full control
over tool definitions, input validation, and error handling.
"""

import asyncio
import logging
from typing import Any

from mcp.server import InitializationOptions
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('simple-math')


async def main():
    # ===========================================
    # Step 1: Create the Server Instance
    # ===========================================
    server = Server("simple-math")

    # ===========================================
    # Step 2: Define Available Tools
    # ===========================================
    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """
        Returns the name, description, and input schema of all available tools.

        Each tool requires:
        - name: Unique identifier for the tool
        - description: Human-readable description
        - inputSchema: JSON Schema defining expected arguments
        """
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
        """
        Handle tool execution requests.

        Args:
            name: The name of the tool to execute
            arguments: Dictionary of arguments passed to the tool

        Returns:
            List of content objects (TextContent, ImageContent, etc.)
        """
        try:
            # Validate arguments exist
            if not arguments:
                raise ValueError("No arguments provided")

            # Handle 'add' tool
            if name == "add":
                if "a" not in arguments or "b" not in arguments:
                    raise ValueError("Missing required arguments: a, b")
                result = arguments['a'] + arguments['b']
                return [types.TextContent(type="text", text=str(result))]

            # Handle 'subtract' tool
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
    # Step 4: Initialize and Run the Server
    # ===========================================
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="simple-math",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
