#!/usr/bin/env python3
"""Activity Curator - Complete this in Task 3"""

import os

from google.adk.agents import LlmAgent
# from google.adk.models.lite_llm import LiteLlm


from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# model = LiteLlm(
#     model="openai/gemini-2.5-flash",
#     api_key="sk-adk-lab-123",
#     api_base="http://localhost:4000"
# )

activity_curator = LlmAgent(
    name="activity_curator",                          # TODO 1: Use "activity_curator"
    model="gemini-2.5-flash",
    instruction="""You are an activity curator. You focus ONLY on things to do:
     attractions, restaurants, cultural experiences, and local tips.
     Do NOT provide flight or hotel recommendations."""                   
       
)
