"""Step 1 — ADK Session Management.

LLM APIs are stateless. In ADK, a Session stores the conversation as events,
and the Runner resends them on every turn.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm(model="openai/gpt-4o")

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


root_agent = LlmAgent(
    name="support_bot",
    model=MODEL,
    instruction=(
        "You are a support agent. Keep answers short. "
        "Use get_order_status for order questions."
    ),
    tools=[get_order_status],
)
