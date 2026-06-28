# TravelWise AI Agent — Travel_Task1

This folder contains the TravelWise travel assistant demo built with Google ADK, FastAPI, and a simple browser chat interface.

## Overview

`Travel_Task1` is a multi-agent travel planning project that uses a root coordinator agent and three specialist sub-agents:

- `flight_specialist` — handles flight-related questions
- `hotel_expert` — handles hotel and accommodation questions
- `activity_curator` — handles activities and attractions

The coordinator agent in `agent.py` delegates user queries to all specialists and returns combined travel recommendations.

## Project Structure

```
Travel_Task1/
├── README.md
├── agent.py
├── index.html
├── server.py
├── safety.py
├── tools.py
├── Travel_Cordinator.jpg
├── __init__.py
├── logs/
└── sub_agents/
    ├── __init__.py
    ├── activity_curator.py
    ├── flight_specialist.py
    └── hotel_expert.py
```

## Key Files

- `server.py` — FastAPI application exposing a web interface and streaming chat API
- `agent.py` — root agent configuration and CLI demo runner
- `index.html` — browser-based chat UI for the FastAPI server
- `safety.py` — safety and content filtering helper logic
- `tools.py` — utility helpers used by the agent workflow
- `Travel_Cordinator.jpg` — visual asset for project branding or documentation
- `sub_agents/flight_specialist.py` — flight specialist logic
- `sub_agents/hotel_expert.py` — hotel specialist logic
- `sub_agents/activity_curator.py` — activity specialist logic

## Requirements

This project depends on the packages in the repository root. Install them from the project root:

```bash
python -m pip install -r ../requirements.txt
```

If you prefer `pyproject.toml`, install with:

```bash
python -m pip install .
```

## Environment

Create a `.env` file in the project root or `Travel_Task1` folder containing your Google API key:

```env
GOOGLE_API_KEY=<your_api_key>
```

## Running the web server

From the `Travel_Task1` folder, start the FastAPI server:

```bash
cd Travel_Task1
python server.py
```

Then open your browser to:

```txt
http://127.0.0.1:8000/
```

## API Endpoints

- `GET /` — serves the chat UI
- `POST /api/chat/stream` — streams assistant responses for chat messages
- `POST /api/session/create` — creates a new chat session

## CLI demo

`agent.py` can be run directly for a terminal-based interactive demo:

```bash
cd Travel_Task1
python agent.py
```

## Notes

- The coordinator agent enforces delegation to all three specialists.
- The web UI uses a streaming response to display assistant output incrementally.
- Sessions and memory are stored in-memory via `InMemorySessionService` and `InMemoryMemoryService`.
