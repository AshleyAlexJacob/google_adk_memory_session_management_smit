"""Step 2 — Context Window Management.

As the conversation grows, keep only the last N turns (sliding window).
"""

from google.adk.agents import LlmAgent
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
    return None  # None = send the trimmed request


root_agent = LlmAgent(
    name="support_bot",
    model=MODEL,
    instruction=(
        "You are a support agent. Keep answers short. "
        "Use get_order_status for order questions."
    ),
    tools=[get_order_status],
    before_model_callback=trim_history,
)
