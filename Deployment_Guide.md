# Agentic AI Bootcamp

This bootcamp is a hands-on path from inference to production-style agents. You will call **NVIDIA® NIM™** from cloud and local endpoints, expose and consume capabilities with the **Model Context Protocol (MCP)** (including a low-level server implementation), and orchestrate reasoning and tool use with **LangGraph**. You will then use **NeMo Agent Toolkit (NAT)** to connect MCP tools to NIM with **YAML** workflow configuration—plus observability and evaluation—before tying the stack together in a final **Challenge**.

## Deploying the Labs

### Tested environment

We tested and ran all labs on a DGX machine equipped with an A100 and H100 GPUs (80GB).

### Prerequisites

Basic experience with Python programming is required for this bootcamp. Familiarity with fundamental concepts of Large Language Models (LLMs) and generative AI is recommended but not mandatory. Experience working with APIs (such as REST APIs) will be helpful. No prior experience with agentic AI frameworks is required.

Ensure the following tools are installed on your system:
* [UV Package Manager](https://docs.astral.sh/uv/getting-started/installation/)
* [Python](https://docs.astral.sh/uv/guides/install-python/)
* [Git Version Control](https://github.com/git-guides/install-git)

#### 1. Setting up a Virtual Environment

First, clone this repository and navigate to the project directory:
```bash
https://github.com/openhackathons-org/agentic-ai-bootcamp
cd agentic-ai-bootcamp
```

Create and activate a new virtual environment using **Python 3.13 or newer**:

```bash
# Create virtual environment
python -m venv agentic-ai-env

# Activate virtual environment
source agentic-ai-env/bin/activate
```

#### 2. Installing Required Packages

With the virtual environment activated, install the required packages:
```bash
# Install requirements
uv pip install -r requirements.txt
```

#### 3. Installing VS Code Server (code-server)

```bash
curl -fsSL https://code-server.dev/install.sh | sh

code-server --auth none --port 8888
```

After running the command, you should see output similar to:

```
[2026-04-15T08:04:15.280Z] info  Wrote default config file to /Users/krkalyan/.config/code-server/config.yaml
[2026-04-15T08:04:15.461Z] info  code-server 4.112.0 d7599ae360900ad55b503e3c840b417a1eae4798
[2026-04-15T08:04:15.462Z] info  Using user-data-dir /Users/root/.local/share/code-server
[2026-04-15T08:04:15.468Z] info  Using config file /Users/root/.config/code-server/config.yaml
[2026-04-15T08:04:15.468Z] info  HTTP server listening on http://127.0.0.1:8888/
[2026-04-15T08:04:15.468Z] info    - Authentication is enabled
[2026-04-15T08:04:15.468Z] info      - Using password from /Users/root/.config/code-server/config.yaml
[2026-04-15T08:07:10.214Z] info    - Authentication is disabled
[2026-04-15T08:04:15.468Z] info    - Not serving HTTPS
```

Copy the URL from the output and paste it into your browser. If prompted for a token, you can find it in the terminal output.

#### 4. Opening the labs

With **code-server** running, open **http://localhost:8888** in your browser (or use the URL printed in the terminal if it differs). In the workspace, open the **tutorial** directory and start from **start_here.ipynb**.

When you are finished with the labs close your shell or pressing **Ctrl+D** in the terminal. Congratulations, you've successfully built and deployed an Agentic AI Bootcamp!

#### Troubleshooting

If you encounter any issues:

1. **Virtual Environment Issues**
   - Make sure you're in the correct directory when creating the virtual environment
   - Verify that the virtual environment is activated (you should see `(agentic-ai-env)` in your terminal prompt)

2. **Package Installation Issues**
   - Try updating pip before installing requirements: `pip install --upgrade pip`
   - If a package fails to install, try installing it separately

3. **GPU Access Issues**
   - Ensure NVIDIA drivers are properly installed
   - Check if CUDA toolkit is installed and matches your PyTorch version
   - Run `nvidia-smi` in terminal to verify GPU is recognized

4. **VSCode Access Issues**
   - Make sure port 8888 is not being used by another application
   - If accessing from another machine, ensure firewall settings allow the connection
   - Try a different port if 8888 is unavailable

For additional help, please open an issue in the GitHub repository.
