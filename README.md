# Step 1 — ADK Session Management

The Runner keeps conversation history in a Session. Each turn, past events are sent again.

```bash
python chat.py
```

Try:

- `My order hasn't arrived.`
- `#48213` — it should remember you are talking about an order
- `What was my order number again?` — it should recall `#48213`
