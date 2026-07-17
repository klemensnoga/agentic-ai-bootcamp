
### Modification:

#### Installation
Add step after installation of `./agentic-ai-bootcamp/requirements.txt`
`uv pip install --no-cache -r ./agentic-ai-bootcamp/requirements-athena.txt`

#### Adding VSCode extensions

`export VSCODE_EXTENSIONS=$BASEDIR/vscode-server/extensions/`
`code-server --extensions-dir=$VSCODE_EXTENSIONS --install-extension ms-python.python --install-extension ms-toolsai.jupyter`



## 07_local_inference_endpoint

`apptainer registry login --username \$oauthtoken docker://nvcr.io`

`apptainer pull docker://nvcr.io/nim/meta/llama-3.2-3b-instruct:latest`

## 03_local_inference_endpoint

Add `"MCP_PORT"` to the notebook to 


## 05_

Set `"MCP_PORT"` to the notebook to 

```
and set os.environ["PHOENIX_PORT"]

phoenix_process = subprocess.Popen(
    ["phoenix", "serve"],
    stdout=log,
    stderr=subprocess.STDOUT,
)
```

Add message to the bot about TA/mentor " your TA/mentor is <> please join breakout room with mentor name during hands-on"
