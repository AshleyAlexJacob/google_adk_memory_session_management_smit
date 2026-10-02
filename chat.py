"""Simple CLI chat for SupportBot. Run: python chat.py

Type `demo` to run two users at once (concurrent sessions).
"""

import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from uuid import uuid4
from supportbot.agent import app, load_json, save_json

load_dotenv()

APP = "supportbot"


async def chat(runner, sessions, user_id, session_id, text):
    """One turn for one user/session. Isolated from other users."""
    msg = types.Content(role="user", parts=[types.Part(text=text)])
    reply = ""
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=msg
    ):
        if event.is_final_response() and event.content and event.content.parts:
            reply = event.content.parts[0].text
    session = await sessions.get_session(
        app_name=APP, user_id=user_id, session_id=session_id
    )
    if session:
        save_json(session)
    return reply


async def ensure_session(sessions, user_id, session_id):
    existing = await sessions.get_session(
        app_name=APP, user_id=user_id, session_id=session_id
    )
    if existing:
        return
    await sessions.create_session(
        app_name=APP,
        user_id=user_id,
        session_id=session_id,
        state=load_json(session_id),
    )


async def run_demo(runner, sessions):
    """Two users at once — one Runner, two isolated sessions."""
    user_id_1 = str(uuid4())
    user_id_2 = str(uuid4())
    session_id_1 = f"s_{user_id_1}"
    session_id_2 = f"s_{user_id_2}"
    await ensure_session(sessions, user_id_1, session_id_1)
    await ensure_session(sessions, user_id_2, session_id_2)
    a, b = await asyncio.gather(
        chat(runner, sessions, user_id_1, session_id_1, "Where is order #48213?"),
        chat(runner, sessions, user_id_2, session_id_2, "Why was I charged twice?"),
    )
    print("User A (usr_882):", a)
    print("User B (usr_910):", b)   


async def main():
    sessions = InMemorySessionService()
    await ensure_session(sessions, "usr_882", "s_882")
    runner = Runner(app=app, session_service=sessions)

    print("SupportBot  |  type demo for 2 users  |  quit to exit")
    while True:
        query = input("You: ").strip()
        if query.lower() in {"quit", "exit", "q"}:
            break
        if not query:
            continue
        if query.lower() == "demo":
            await run_demo(runner, sessions)
            continue

        reply = await chat(runner, sessions, "usr_882", "s_882", query)
        print("Bot:", reply)


if __name__ == "__main__":
    asyncio.run(main())
