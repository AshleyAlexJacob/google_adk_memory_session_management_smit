"""Simple CLI chat for SupportBot. Run: python chat.py"""

import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from supportbot.agent import root_agent

load_dotenv()

APP = "supportbot"
USER_ID = "usr_882"
SESSION_ID = "s_882"


async def show_scratchpad(sessions: InMemorySessionService) -> None:
    """Print the planner's latest plan from session state."""
    session = await sessions.get_session(
        app_name=APP, user_id=USER_ID, session_id=SESSION_ID
    )
    scratchpad = session.state.get("scratchpad") if session else None
    if not scratchpad:
        print("Scratchpad: (no plan yet)")
        return
    print("Scratchpad:")
    print(scratchpad)


async def main():
    sessions = InMemorySessionService()
    await sessions.create_session(
        app_name=APP, user_id=USER_ID, session_id=SESSION_ID
    )
    runner = Runner(agent=root_agent, app_name=APP, session_service=sessions)

    print("SupportBot  |  /scratchpad to see the plan  |  quit to exit")
    while True:
        query = input("You: ").strip()
        if query.lower() in {"quit", "exit", "q"}:
            break
        if not query:
            continue
        if query.lower() == "/scratchpad":
            await show_scratchpad(sessions)
            continue

        message = types.Content(role="user", parts=[types.Part(text=query)])
        async for event in runner.run_async(
            user_id=USER_ID, session_id=SESSION_ID, new_message=message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print("Bot:", event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
