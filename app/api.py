# imports
from fastapi import FastAPI
from pydantic import BaseModel
import workflows
import llm.service as llm_service
from typing import Optional
import uvicorn


# ================= tmp for testing/ =================

from vault.model import setup
setup()

# ================= \tmp for testing =================


app = FastAPI()

class FormatNoteRequest(BaseModel):
    content:str
    # command: Optional[str] = None

@app.get("/")
def root():
    return {'message': "API Available"}


# ====== Note Formatting ======

# 1. accept raw note
# 2. return formatted note for approval
@app.post("/format")
def format_raw(raw: FormatNoteRequest) -> dict:
    """Take in raw note, return formatted note for user approval"""
    response = llm_service.format_note(raw.content)
    return response

# 3. register 'approve' action
# Note: by REST standards, need to re-send both raw and approved notes from browser?
#       otherwise, may need to consider saving only raw first.

if __name__ == "__main__":
    uvicorn.run("api:app", reload=True) # need to clarify what this argument does