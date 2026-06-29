#!/usr/bin/env python3
"""Task 6: Complete Multi-Agent Demo"""

import asyncio
import os
# from urllib import response
from dotenv import load_dotenv

# Load environment variables FIRST before importing ADK modules
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
from google.adk.models.lite_llm import LiteLlm

from google.adk.agents import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.tools import ToolContext
from tools import convert_currency, calculate_budget
from safety import input_filter, output_filter, log_event, check_rate_limit, MAX_REQUESTS, WINDOW_SECONDS

# Fix relative import error by using absolute import
from sub_agents import activity_curator, flight_specialist, hotel_expert


def set_preference(key: str, value: str, tool_context: ToolContext) -> str:
    """Store a travel preference for the user."""
    tool_context.state[key] = value
    return f"Saved: {key} = {value}"


def get_preferences(tool_context: ToolContext) -> str:
    """Retrieve all stored travel preferences."""
    # Get individual preferences (ADK State doesn't support dict() conversion)
    preferences = {}
    destination = tool_context.state.get("destination", None)
    budget = tool_context.state.get("budget", None)
    currency = tool_context.state.get("currency", None)
    
    if destination:
        preferences["destination"] = destination
    if budget:
        preferences["budget"] = budget
    if currency:
        preferences["currency"] = currency
    
    if not preferences:
        return "No preferences stored yet."
    summary = "Your preferences:\n"
    for key, value in preferences.items():
        summary += f"  - {key}: {value}\n"
    return summary

def safety_check(user_message: str, session_id: str = "default") -> str:
    """Complete safety check: rate limit + input filter."""
    rate_allowed, rate_msg = check_rate_limit(session_id)
    log_event("RATE_CHECK", {"session_id": session_id, "allowed": rate_allowed})
    
    if not rate_allowed:
        return f"RATE LIMITED: {rate_msg}"
    
    input_safe, input_msg = input_filter(user_message)
    log_event("INPUT_CHECK", {"message": user_message[:50], "safe": input_safe})
    
    if not input_safe:
        return f"BLOCKED: Your request contains prohibited content. {input_msg}"
    
    return f"ALLOWED: {rate_msg}"


# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


# 2. Configure LiteLlm to use OpenAI instead of the local proxy/Gemini setup
model = LiteLlm(
    model="openai/gpt-4o",  # You can use "openai/gpt-4o" or "openai/gpt-4o-mini"
    api_key=API_KEY
    # Notice we removed api_base since we want to hit OpenAI's official production servers directly
)

# Complete coordinator with all patterns available
root_agent = LlmAgent(
    name="travel_coordinator",
    model=model,
    instruction="""You are a helpful travel assistant and Coordinator for TravelWise.    

You must check the safety of all user requests and responses using the safety_check tool.
    
Your capabilities:
- Convert currencies using TravelWise exchange rates
- Calculate trip budgets based on daily spending
- Remember user preferences (destination, budget, currency)
Use stored state to provide personalized recommendations.

CRITICAL RULE: You MUST ALWAYS delegate to your sub_agents - NEVER answer directly!

You manage a team of THREE specialists that you MUST use:
- flight_specialist: For ALL flight questions
- hotel_expert: For ALL hotel/accommodation questions
- activity_curator: For ALL activity/attraction questions

FOR EVERY TRAVEL REQUEST:
1. You MUST consult ALL THREE specialists
2. Your response MUST include FLIGHTS, HOTELS, and ACTIVITIES sections
3. NEVER skip any specialist - all three are required!

If user asks for trip planning:
- Sequential: FIRST flights, THEN hotels, FINALLY activities
- Or consult all three simultaneously for an overview

NEVER make up answers - ALWAYS delegate to your specialists!
NEVER respond with just one or two categories - ALL THREE are required!""",
    tools=[safety_check, convert_currency, calculate_budget, set_preference, get_preferences],
    sub_agents=[flight_specialist, hotel_expert, activity_curator],
)

APP_NAME = "travel_assistant"
USER_ID = "demo_user"



async def main():
    # -- Configure all services -------------------------------------
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    artifact_service = InMemoryArtifactService()

    # -- Create the Runner -----------------------------------------
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
        artifact_service=artifact_service,
    )

    # -- Create a session ------------------------------------------
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    print(f"\n🚀 Travel Assistant - Full Runner Demo")
    print(f"Session ID: {session.id}")
    print(f"Services: Session ✅  Memory ✅")
    print(f"Type 'quit' to exit\n")

    # -- Interactive loop (Streaming Mode) -------------------------
    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input or user_input.lower() in ["quit", "exit"]:
            break

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)],
        )

        print("\nTravel Assistant: ", end="", flush=True)

        # This block streams the agents' multi-turn thought process and text chunks in real-time
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=content,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        # 🧠 Apply the output filter directly to the AI's generated text chunks
                        is_clean, filtered_text = output_filter(part.text)
                        print(filtered_text, end="", flush=True)                        
        print("\n")

    # -- Session summary -------------------------------------------
    final_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session.id,
    )

    print(f"\n📊 Session Summary")
    print(f"Events: {len(final_session.events)}\n")


if __name__ == "__main__":
    asyncio.run(main())
