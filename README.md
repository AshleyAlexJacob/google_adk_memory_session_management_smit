# Step 4 — Summarization Memory

`EventsCompactionConfig` summarizes older events every 5 turns so long chats stay cheap.

```bash
python chat.py
```

Send 5+ messages about order `#48213`. Older turns get compacted into a summary.
