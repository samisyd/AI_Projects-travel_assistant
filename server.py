#!/usr/bin/env python3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types

from agent import APP_NAME, root_agent

app = FastAPI(title="TravelWise AI Agent API")

"""
Why Session Memory Matters in ADK:
Without memory, agents are stateless - each message is independent.
The agent forgets everything after each response. Session memory
enables the agent to remember context across conversation turns.
"""

session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()
artifact_service = InMemoryArtifactService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service,
    artifact_service=artifact_service,
)


from fastapi import Response

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/")
async def get_chat_interface():
    """Serve the chat interface HTML page."""
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


class ChatRequest(BaseModel):
    user_id: str = "demo_user"
    session_id: str | None = None
    message: str


async def event_streamer(user_id: str, session_id: str, message: str):
    """Generates a text stream chunk-by-chunk from the ADK runner."""
    content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=message)],
    )

    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        yield part.text
    except Exception as e:
        yield f"\n[Error during generation: {str(e)}]"


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    session_id = request.session_id
    if not session_id:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=request.user_id,
        )
        session_id = session.id

    return StreamingResponse(
        event_streamer(request.user_id, session_id, request.message),
        media_type="text/plain",
    )


@app.post("/api/session/create")
async def create_new_session(user_id: str = "demo_user"):
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
    )
    return {"session_id": session.id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
