# Graph-Based Notes System

A local-first notes application that uses an LLM to clean up rough notes, suggest relationships between notes, and build a user-approved graph of connected knowledge.

The LLM suggests formatted notes and relationships, but nothing is saved until the user reviews and approves it.

## Current Features

* Create a rough note and send it to a local LLM for Markdown formatting
* Review and edit the formatted note before approval
* Retrieve existing notes as relationship candidates
* Generate suggested links between related notes
* Review and approve suggested links before saving them
* Persist notes and links in SQLite
* View notes as an interactive graph
* Open saved notes from the graph and view their approved Markdown content
* Use a stub LLM service for development without running a local model

## Tech Stack

### Backend

* Python 3.11+
* FastAPI
* SQLite
* Pydantic
* Ollama-compatible local LLM integration
* pytest

### Frontend

* React
* TypeScript
* Vite
* Mantine
* react-force-graph-2d
* openapi-typescript / openapi-fetch

The frontend types are generated from FastAPI’s OpenAPI schema, which helps keep the TypeScript client in sync with backend changes.

## Architecture

The backend is split into a few small layers:

```text
FastAPI routes
    |
    v
workflows / vault services
    |              |
    v              v
LLM service     vault model
                   |
                   v
                 SQLite
```

Database queries return data in roughly the same shape as the SQLite tables. The service layer converts that data into the models used by the rest of the app.

LLM calls live in their own service module, which also makes it easy to swap in a stub while developing or testing.

## Core Workflow

```text
Write rough note
    |
    v
LLM formats note
    |
    v
Review / edit formatted note
    |
    v
Approve note
    |
    v
Generate relationship suggestions
    |
    v
Review suggested links
    |
    v
Save approved links
    |
    v
View note in graph
```

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/erenorexplorer/notes-app.git
cd notes-app
```

### 2. Set up the backend

Create and activate a Python virtual environment:

```bash
python -m venv .venv
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Create `backend/.env`:

```env
LLM_MODE=real
```

Use `LLM_MODE=stub` if you want to run the application without a local LLM.

For real LLM usage, install and configure [Ollama](https://ollama.com/download).

I’ve mainly tested the app with:

```text
qwen3:4b-instruct
```

but the model is not meant to be hard-coded long term.

Start the backend from the `backend` directory:

```bash
python -m uvicorn app.api:app --reload
```

The API will run at:

```text
http://localhost:8000
```

### 3. Set up the frontend

From `frontend/react-client`:

```bash
npm install
```

Create `frontend/react-client/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Start the development server:

```bash
npm run dev
```

Open the local URL shown by Vite in your browser.

## Tests

From the `backend` directory:

```bash
pytest
```

The current tests cover the main note creation and link approval workflow, along with graph data behavior.

## Project Status

**Active MVP.**

The core note creation, LLM-assisted review, relationship suggestion, persistence, graph visualization, and saved-note viewing workflows are functional.

Development is ongoing.
