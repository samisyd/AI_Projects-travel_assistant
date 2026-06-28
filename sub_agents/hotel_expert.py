#!/usr/bin/env python3
"""Hotel Expert - Pre-filled for coordinator tasks"""

import os

from google.adk.agents import LlmAgent
# from google.adk.models.lite_llm import LiteLlm

# model = LiteLlm(
#     model="openai/gemini-2.5-flash",
#     api_key="sk-adk-lab-123",
#     api_base="http://localhost:4000"
# )


from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

hotel_expert = LlmAgent(
    name="hotel_expert",
    model="gemini-2.5-flash",
    instruction="""You are a hotel expert for TravelWise.

You focus ONLY on accommodation:
- Hotels and resorts
- Locations and neighborhoods
- Amenities and room types
- Pricing and availability

Do NOT provide flight or activity recommendations.
Be concise and helpful about lodging options."""
)
