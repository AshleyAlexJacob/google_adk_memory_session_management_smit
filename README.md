# Step 6 — Concurrent Sessions

One Runner serves many users. Each `user_id` + `session_id` is isolated.

```bash
python chat.py
```

Type `demo` to run User A and User B at the same time with `asyncio.gather`.
