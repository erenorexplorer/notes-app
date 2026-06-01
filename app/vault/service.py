from datetime import datetime
import uuid
import model

# future: function to return large DTO of whole vault structure
# i.e. stitch together notes and links.
# using model's getallnotes and getalllinks

def create_raw_note(raw:str) -> str:
    """Create a new note with raw note and return uuid"""
    uid = str(uuid.uuid4())
    create_time = datetime.now()
    model.insert_note(uid, raw, create_time)
    return uid

def save_approved_note(uid:str, approved_note:str):
    """Update note with approved note and change status to 'approved'"""
    update_time = datetime.now()
    model.approve_note(uid, approved_note, update_time)