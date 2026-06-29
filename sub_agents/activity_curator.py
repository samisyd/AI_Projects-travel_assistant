#!/usr/bin/env python3
"""Activity Curator - Complete this in Task 3"""

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
)

activity_curator = LlmAgent(
    name="activity_curator",                          
    model=model,
    instruction="""You are an activity curator. You focus ONLY on things to do:
     attractions, restaurants, cultural experiences, and local tips.
     Do NOT provide flight or hotel recommendations."""                   
       
)
