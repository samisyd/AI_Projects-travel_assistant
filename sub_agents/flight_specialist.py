#!/usr/bin/env python3
"""Flight Specialist - Pre-filled for coordinator tasks"""

import os

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


from dotenv import load_dotenv
# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# 2. Configure LiteLlm to use OpenAI instead of the local proxy/Gemini setup
model = LiteLlm(
    model="openai/gpt-4o",  # You can use "openai/gpt-4o" or "openai/gpt-4o-mini"
    api_key=API_KEY
    # Notice we removed api_base since we want to hit OpenAI's official production servers directly
)

flight_specialist = LlmAgent(
    name="flight_specialist",
    model=model,
    instruction="""You are a flight specialist for TravelWise.

You focus ONLY on air travel:
- Flight routes and connections
- Airlines and pricing
- Flight times and duration
- Airport information

Do NOT provide hotel or activity recommendations.
Be concise and informative about flight options."""
)
