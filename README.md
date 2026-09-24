# SMIT Peshawar · Memory & Session Management with Google ADK

Workshop code for `Agentic AI — Memory & Session Management with Google ADK.pdf`.

We build **SupportBot** one piece at a time. Checkout a branch, run the chat, then move on.

```bash
cp .env.example .env   # put your OPENAI_API_KEY in .env
pip install -r requirements.txt
git checkout step-01-sessions
python chat.py
```

| Branch | Slide topic |
| --- | --- |
| `step-01-sessions` | ADK session management |
| `step-02-context-window` | Context window (sliding window) |
| `step-03-scratchpad` | Scratchpad via planner `output_key` |
| `step-04-summarization` | Events compaction / summarization |
| `step-05-json-memory` | JSON file session memory |
| `step-06-concurrent-sessions` | Concurrent sessions |
| `step-07-state-persistence` | State prefixes + DatabaseSessionService |
| `complete` | All 7 pieces assembled |

Model on every step: `LiteLlm(model="openai/gpt-4o")`.
