"""
MCP Server using FastMCP (High-Level SDK)
This server exposes simple math tools that can be invoked by MCP clients.
"""

from mcp.server.fastmcp import FastMCP

# Create an MCP server instance with a descriptive name
mcp = FastMCP("simple-math")

# Define the 'add' tool using the @mcp.tool() decorator
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: First integer
        b: Second integer

    Returns:
        Sum of a and b
    """
    return a + b

# Define the 'subtract' tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract second number from first.

    Args:
        a: First integer
        b: Second integer

    Returns:
        Difference (a - b)
    """
    return a - b

if __name__ == "__main__":
    # Run the MCP server with SSE transport over HTTP
    mcp.run(transport="stdio")
