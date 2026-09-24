"""Step 4 — Summarization Memory.

When a session grows long, ADK compresses older events into a summary.
"""

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.apps import App
from google.adk.apps.app import EventsCompactionConfig
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm(model="openai/gpt-4o")
MAX_TURNS = 20

ORDERS = {
    "48213": {"status": "shipped", "eta": "tomorrow"},
    "10001": {"status": "processing", "eta": "3 days"},
}


def get_order_status(order_id: str) -> dict:
    """Look up a fake order by id like 48213."""
    order = ORDERS.get(order_id)
    if not order:
        return {"order_id": order_id, "error": "not_found"}
    return {"order_id": order_id, **order}


def trim_history(callback_context, llm_request):
    """Keep only the last MAX_TURNS messages in the context window."""
    llm_request.contents = llm_request.contents[-MAX_TURNS:]
    return None


planner = LlmAgent(
    name="planner",
    model=MODEL,
    instruction="List the steps to solve the issue. Do not reply to the user.",
    output_key="scratchpad",
)

answerer = LlmAgent(
    name="answerer",
    model=MODEL,
    instruction="Follow this plan: {scratchpad}. Keep answers short. Use get_order_status for orders.",
    tools=[get_order_status],
    before_model_callback=trim_history,
)

support_bot = SequentialAgent(
    name="support_bot",
    sub_agents=[planner, answerer],
)

# Summarize every 5 turns; keep 1 turn of overlap for continuity
app = App(
    name="supportbot",
    root_agent=support_bot,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=5,
        overlap_size=1,
    ),
)

root_agent = support_bot  # kept for package export / ADK web UI
