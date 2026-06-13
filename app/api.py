# imports
from fastapi import FastAPI
from pydantic import BaseModel
import app.workflows as workflows
# from app.llm import service as llm_service
# from typing import Optional
import uvicorn
from app.schemas import FormatNoteRequest, NoteContent, LinkSuggestion


# ================= tmp for testing/ =================

from app.vault.model import setup
setup()

# ================= \tmp for testing =================


app = FastAPI()

@app.get("/")
def root():
    return {'message': "API Available"}


# ====== Note Formatting ======

# 1. accept raw note
# 2. return formatted note for approval
@app.post("/notes")
def format_raw(raw: FormatNoteRequest) -> NoteContent:
    """Take in raw note, return formatted note for user approval"""
    response = workflows.create_formatted_draft(raw.content)
    return NoteContent(id=response['id'], content=response['content'])

# 3. register 'approve' action
# pass to workflows and save for now, add return suggested links later
# note: uid known from url but currently unused
@app.put("/notes/{uid}/approve")
def approve_note(approved_note: NoteContent) -> list[LinkSuggestion]:
    response = workflows.create_link_suggestions(approved_note.id, approved_note.content)
    return response

# python -m uvicorn app.api:app --reload
if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)