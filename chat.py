"""Simple CLI chat for SupportBot. Run: python chat.py"""

import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from supportbot.agent import app

load_dotenv()

APP = "supportbot"


async def main():
    sessions = InMemorySessionService()
    await sessions.create_session(
        app_name=APP, user_id="usr_882", session_id="s_882"
    )
    runner = Runner(app=app, session_service=sessions)

    print("SupportBot  |  type quit to exit")
    while True:
        query = input("You: ").strip()
        if query.lower() in {"quit", "exit", "q"}:
            break
        if not query:
            continue

        message = types.Content(role="user", parts=[types.Part(text=query)])
        async for event in runner.run_async(
            user_id="usr_882", session_id="s_882", new_message=message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print("Bot:", event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
