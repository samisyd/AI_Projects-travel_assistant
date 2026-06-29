#!/usr/bin/env python3
"""
Complete Safety Filters, Logging, and Rate Limiting
"""

import os
import json
from datetime import datetime, timedelta

LOG_FILE = "/root/logs/audit.log"

# ==================== INPUT FILTER ====================
BLOCKED_PHRASES = [
    "ignore previous instructions",
    "bypass safety",
    "pretend you are",
    "act as if you are",
    "forget your instructions",
    "disregard all previous",
    "you are now",
    "new persona",
]


def input_filter(user_input: str) -> tuple:
    """Check input for safety violations."""
    lower_input = user_input.lower()
    
    for phrase in BLOCKED_PHRASES:
        if phrase in lower_input:
            return False, f"Blocked: {phrase}"
    
    return True, "OK"


# ==================== OUTPUT FILTER ====================
FORBIDDEN_OUTPUT = [
    "as an ai",
    "i cannot help",
    "i don't have real-time",
    "i cannot provide",
    "as a language model",
]


def output_filter(response: str) -> tuple:
    """Check output for policy violations."""
    lower_response = response.lower()
    
    for phrase in FORBIDDEN_OUTPUT:
        if phrase in lower_response:
            response = response.replace(phrase, "[TravelWise Response]")
    
    return True, response


# ==================== RATE LIMITING ====================
# Global in-memory storage - persists for the lifetime of the server
_REQUEST_COUNTS = {}
MAX_REQUESTS = 5
WINDOW_SECONDS = 60


def check_rate_limit(session_id: str) -> tuple:
    """Check if session has exceeded rate limit."""
    global _REQUEST_COUNTS
    current_time = datetime.now()
    
    # Initialize session if new
    if session_id not in _REQUEST_COUNTS:
        _REQUEST_COUNTS[session_id] = {
            "count": 0,
            "window_start": current_time
        }
    
    session = _REQUEST_COUNTS[session_id]
    window_end = session["window_start"] + timedelta(seconds=WINDOW_SECONDS)
    
    # Reset window if expired
    if current_time > window_end:
        session["count"] = 0
        session["window_start"] = current_time
        window_end = current_time + timedelta(seconds=WINDOW_SECONDS)
    
    # Check if over limit
    if session["count"] >= MAX_REQUESTS:
        wait_seconds = int((window_end - current_time).total_seconds())
        if wait_seconds < 0:
            wait_seconds = WINDOW_SECONDS
        return False, f"Rate limit exceeded. Wait {wait_seconds}s."
    
    # Increment counter
    session["count"] += 1
    remaining = MAX_REQUESTS - session["count"]
    
    return True, f"{remaining} requests remaining"


# ==================== AUDIT LOGGING ====================
def log_event(event_type: str, data: dict) -> None:
    """Log an event to the audit file."""
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().isoformat()
    
    log_entry = {
        "timestamp": timestamp,
        "event_type": event_type,
        "data": data
    }
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
