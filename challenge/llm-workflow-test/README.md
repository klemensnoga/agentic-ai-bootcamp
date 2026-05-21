# LLM-WORKFLOW-TEST

## Commands

Launch the mcp web server

```bash
cd mcp-servers/invoice
uv run mcp-server-invoice
```

Run the test

```bash
cd llm-workflow-test
uv run main.py --mcp-server-url http://localhost:8000/mcp --inf-url http://localhost:9998/v1 --inf-url-qna-agent http://localhost:9999/v1 --nvidia-api-key dummy 
```

The `--mcp-server-url` default reads `MCP_PORT` from the environment (default
`8000`). For multi-user or shared-host setups, set `MCP_PORT` to a unique value
before launching the server and the test will pick it up automatically.