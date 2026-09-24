# Step 2 — Context Window Management

Keep only the last 20 turns with `before_model_callback`. Older messages fall out of the window.

```bash
python chat.py
```

Try a few order questions. Long chats still stay short in the model context.
