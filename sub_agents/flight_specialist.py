#!/usr/bin/env python3
"""Flight Specialist - Pre-filled for coordinator tasks"""

import os

from google.adk.agents import LlmAgent
# from google.adk.models.lite_llm import LiteLlm


from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

flight_specialist = LlmAgent(
    name="flight_specialist",
    model="gemini-2.5-flash",
    instruction="""You are a flight specialist for TravelWise.

You focus ONLY on air travel:
- Flight routes and connections
- Airlines and pricing
- Flight times and duration
- Airport information

Do NOT provide hotel or activity recommendations.
Be concise and informative about flight options."""
)
