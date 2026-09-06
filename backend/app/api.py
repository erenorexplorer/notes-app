# imports
from fastapi import FastAPI
from pydantic import BaseModel
import app.workflows as workflows
import app.vault.service as vault_service
import uvicorn
from app.schemas import FormatNoteRequest, NoteContent, LinkSuggestion, NoteOverview, FullNote


# ================= tmp for testing/ =================

from app.vault.model import setup
setup()

# ================= \tmp for testing =================


app = FastAPI()

@app.get("/")
def root():
    return {'message': "API Available"}


# ====== Note Formatting/ ======

# 1. accept raw note
# 2. return formatted note for approval
@app.post("/notes")
def format_raw(raw: FormatNoteRequest) -> NoteContent:
    """Take in raw note, return formatted note for user approval"""
    response = workflows.create_formatted_draft(raw.title, raw.content)
    return NoteContent(id=response['id'], title=response['title'] ,content=response['content'])

# 3. register 'approve' action
# pass to workflows and save for now, add return suggested links later
# note: uid known from url but currently unused
@app.put("/notes/{uid}/approve")
def approve_note(approved_note: NoteContent) -> list[LinkSuggestion]:
    response = workflows.create_link_suggestions(approved_note.id, approved_note.title, approved_note.content)
    return response

# return overview of all notes
@app.get("/notes")
def get_notes() -> list[NoteOverview]:
    return vault_service.get_note_overviews()

@app.get("/notes/{uid}")
def get_note(uid:str) -> FullNote:
    """Get full note data by id"""
    note_data = vault_service.get_full_note(uid)
    if note_data is None:
        return None
    return note_data

# ====== /Note Formatting ======

# ====== Link Creation/ ======

@app.post("/notes/{uid}/links/approve")
def approve_links(uid:str, approved_links: list[LinkSuggestion]):
    """Accept approved links for a note and save to vault"""
    # pass through workflows since it will later trigger other actions
    workflows.approve_links(uid, approved_links)

# ====== /Link Creation ======

# python -m uvicorn app.api:app --reload
if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)