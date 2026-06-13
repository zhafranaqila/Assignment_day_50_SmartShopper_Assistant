# main.py

import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from agent import root_agent

# ── Setup ──────────────────────────────────────────────────────────
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="smartshopper",
    session_service=session_service,
)

APP_NAME = "smartshopper"
USER_ID = "user_001"
SESSION_ID = "session_001"

# ── Fungsi Chat (async) ────────────────────────────────────────────
async def chat(user_input: str):
    message = Content(role="user", parts=[Part(text=user_input)])

    response_text = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    response_text += part.text

    return response_text

# ── Main ───────────────────────────────────────────────────────────
async def main():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    print("SmartShopper Assistant siap! Ketik 'exit' untuk keluar.\n")
    while True:
        user_input = input("Kamu: ")
        if user_input.lower() == "exit":
            break
        response = await chat(user_input)
        print(f"Assistant: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())