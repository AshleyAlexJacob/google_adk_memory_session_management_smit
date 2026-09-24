# Step 7 — State Persistence Across Turns

`DatabaseSessionService` stores sessions in SQLite. Tool results write to state:

- `last_tool_result` — this session only
- `user:last_order` — every session for this user

```bash
python chat.py
```

Try: ask about `#48213`, quit, run again, then ask `What was my last order?`
