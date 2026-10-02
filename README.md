# Step 5 — JSON for Fast Session Memory

Session state and chat history are saved to `sessions/{id}.json`. Restart the chat — scratchpad, state, and prior turns come back. Files older than 24 hours are ignored (TTL).

```bash
python chat.py
```

Try an order question, quit, run again, then ask about the same order.
