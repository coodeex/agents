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

```
cd parallel_agent

nohup bash -c 'while true; do python3 bot.py; echo "Crashed. Restarting..."; sleep 5; done' > bot.log 2>&1 &

pkill -f bot.py
```