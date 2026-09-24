"""Step 7 — State Persistence Across Turns.

DatabaseSessionService keeps sessions after restart.
State key prefixes control how long values live:
  no prefix = this session only
  user:     = every session of this user
  app:      = every user of the app
  temp:     = this turn only
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.apps import App
from google.adk.apps.app import EventsCompactionConfig
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext

MODEL = LiteLlm(model="openai/gpt-4o")
MAX_TURNS = 20
TTL_HOURS = 24
SESSIONS_DIR = Path("sessions")

ORDERS = {
    "48213": {"status": "shipped", "eta": "tomorrow"},
    "10001": {"status": "processing", "eta": "3 days"},
}


def get_order_status(order_id: str, tool_context: ToolContext) -> dict:
    """Look up a fake order and save the result in session + user state."""
    order = ORDERS.get(order_id)
    if not order:
        result = {"order_id": order_id, "error": "not_found"}
    else:
        result = {"order_id": order_id, **order}

    tool_context.state["last_tool_result"] = result  # this session only
    tool_context.state["user:last_order"] = order_id  # all of this user's sessions
    return result


def trim_history(callback_context, llm_request):
    """Keep only the last MAX_TURNS messages in the context window."""
    llm_request.contents = llm_request.contents[-MAX_TURNS:]
    return None


def save_json(session):
    """Write session.state to sessions/{id}.json."""
    SESSIONS_DIR.mkdir(exist_ok=True)
    path = SESSIONS_DIR / f"{session.id}.json"
    data = dict(session.state)
    data["saved_at"] = datetime.now().isoformat(timespec="seconds")
    path.write_text(json.dumps(data, indent=2))


def load_json(session_id):
    """Read session state from JSON. Empty if missing or past TTL."""
    path = SESSIONS_DIR / f"{session_id}.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    saved_at = data.pop("saved_at", None)
    if saved_at:
        age = datetime.now() - datetime.fromisoformat(saved_at)
        if age > timedelta(hours=TTL_HOURS):
            return {}
    return data


planner = LlmAgent(
    name="planner",
    model=MODEL,
    instruction="List the steps to solve the issue. Do not reply to the user.",
    output_key="scratchpad",
)

answerer = LlmAgent(
    name="answerer",
    model=MODEL,
    instruction=(
        "Follow this plan: {scratchpad}. Keep answers short. "
        "Use get_order_status for orders. "
        "If asked about the last order, use user:last_order from state."
    ),
    tools=[get_order_status],
    before_model_callback=trim_history,
)

support_bot = SequentialAgent(
    name="support_bot",
    sub_agents=[planner, answerer],
)

app = App(
    name="supportbot",
    root_agent=support_bot,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=5,
        overlap_size=1,
    ),
)

root_agent = support_bot

# Survives restart (needs aiosqlite async driver)
DB_URL = "sqlite+aiosqlite:///supportbot.db"
