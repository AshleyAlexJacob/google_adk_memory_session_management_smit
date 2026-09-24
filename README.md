# SupportBot — Complete

All 7 pieces from the slides, assembled:

1. ADK sessions + Runner
2. Context window trim (`before_model_callback`)
3. Scratchpad (planner `output_key`)
4. Summarization (`EventsCompactionConfig`)
5. JSON session state (`sessions/*.json`)
6. Concurrent sessions (`demo` command)
7. State persistence (`DatabaseSessionService` + `user:` prefix)

```bash
cp .env.example .env   # set OPENAI_API_KEY
pip install -r requirements.txt
python chat.py
```

## Try it

- `Where is order #48213?`
- `What was my last order?` (after a restart — state persists)
- type `demo` for two users at once

## Your turn (practical project)

Build your own agent with the same building blocks:

- Runner + SessionService, one session per `user_id` + `session_id`
- Multi-turn history in session events
- Context window handling with `before_model_callback`
- Scratchpad: planner writing to state via `output_key`
- Summarization with `EventsCompactionConfig`
- At least one tool that saves results with `tool_context.state`
- State in JSON first, then `DatabaseSessionService`
- TTL: ignore sessions past a saved timestamp
