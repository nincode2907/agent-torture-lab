# Agent Torture Lab

## LLM provider

`app/agent/llm.py` defaults to the local Codex server:

```python
LLM_PROVIDER = "local"  # Change to "groq" for the external Groq API.
```

You can also override it with the `LLM_PROVIDER` environment variable or
`CommerceLLM(provider="groq")`. Precedence: constructor, environment, then the
constant in `llm.py`. Groq requires `GROQ_API_KEY`; local mode does not.

Install dependencies and start the Codex server separately following its README:

```bash
python3 -m pip install -r requirements.txt
```

Local defaults and optional environment overrides:

| Variable | Default |
| --- | --- |
| `LOCAL_BASE_URL` | `http://127.0.0.1:4000/v1` |
| `LOCAL_MODEL` | `gpt-6.1-sol` |
| `LOCAL_REASONING_EFFORT` | `medium` |
| `LOCAL_API_KEY` | `local` (set to the gateway token if authentication is enabled) |
| `GROQ_MODEL` | `openai/gpt-oss-120b` |

Local requests use a 200-second timeout and no automatic retries. Both providers
return chat completions with function calls for the existing agent runner.

Run the Python app on the same host as the gateway to use its loopback address.
The existing Docker container has its own `127.0.0.1`; the gateway also rejects
non-localhost Host headers, so changing the URL to `host.docker.internal` alone
does not make this gateway accessible from Docker.
