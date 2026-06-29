#!/usr/bin/env python3
"""Hotel Expert - Pre-filled for coordinator tasks"""

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


hotel_expert = LlmAgent(
    name="hotel_expert",
    model=model,
    instruction="""You are a hotel expert for TravelWise.

You focus ONLY on accommodation:
- Hotels and resorts
- Locations and neighborhoods
- Amenities and room types
- Pricing and availability

Do NOT provide flight or activity recommendations.
Be concise and helpful about lodging options."""
)
