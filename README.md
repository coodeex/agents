# agents
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```
python anthropic.py
python deepseek.py
python parallel.py
python guardrail.py
.
.
.
```

**Parallel Agent**
This allows you to chat with multiple LLMs in parallel.
Configure `PARALLEL_AGENT_TELEGRAM_BOT_TOKEN`
```
cd parallel_agent

nohup bash -c 'while true; do python3 parallel_agent_bot.py; echo "Crashed. Restarting..."; sleep 5; done' > bot.log 2>&1 &

pkill -f parallel_agent_bot.py
```

**Git MCP Agent**
This allows you to chat with your git repo.
Configure `GIT_MCP_TELEGRAM_BOT_TOKEN` and `GIT_MCP_REPO_PATH`. Basically, you need to have the repo cloned in the `GIT_MCP_REPO_PATH` directory.
```

curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

cd git_mcp_agent

chmod +x git_pull.sh

nohup bash -c 'while true; do python3 git_mcp_agent_bot.py; echo "Crashed. Restarting..."; sleep 5; done' > bot.log 2>&1 &

pkill -f git_mcp_agent_bot.py
```

**Voice Agent**
This allows you to chat with the voice agent.

```
cd voice_agent

nohup bash -c 'while true; do python3 voice_agent_bot.py; echo "Crashed. Restarting..."; sleep 5; done' > bot.log 2>&1 &

pkill -f voice_agent_bot.py
```

**voice.py**
```
sudo apt-get install libportaudio2
python voice.py
```
