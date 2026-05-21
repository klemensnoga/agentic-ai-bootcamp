# MCP-SERVER-INVOICE-TEST

## Commands

Launch the mcp web server
```bash
cd mcp-servers/invoice
uv run mcp-server-invoice
```

Run the test
```bash
cd mcp-server-invoice-test
uv run main.py --mcp-server-url http://localhost:8000/mcp
```

The server reads the port from the `MCP_PORT` environment variable, falling back
to `8000` if unset. In multi-user or shared-host workshop setups, set `MCP_PORT`
to a unique value per user before launching the server, and either pass the same
port to `--mcp-server-url` or rely on the default which respects `MCP_PORT`:

```bash
export MCP_PORT=8123
cd mcp-servers/invoice && uv run mcp-server-invoice &
cd mcp-server-invoice-test && uv run main.py   # picks up MCP_PORT automatically
```