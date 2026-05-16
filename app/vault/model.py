import sqlite3
from pathlib import Path
from datetime import datetime

PATH = Path(__file__).resolve().parent
VAULT_PATH = PATH / "vaultdb.db"

def setup():
    """Create initial database tables if they don't already exist"""
    
    conn = sqlite3.connect(VAULT_PATH)
    note_table = """
    CREATE TABLE IF NOT EXISTS Note (
        id             TEXT PRIMARY KEY,
        title          TEXT NOT NULL,
        raw_note       TEXT NOT NULL,
        approved_note  TEXT NOT NULL,
        created_at     DATETIME,
        updated_at     DATETIME
    );
    """

    link_table = """
    CREATE TABLE IF NOT EXISTS Link (
    id               TEXT PRIMARY KEY,
    source_note      TEXT NOT NULL,
    target_note      TEXT NOT NULL,
    relation_type    TEXT,
    created_at       DATETIME,

    FOREIGN KEY (source_note) REFERENCES Note (id) ON DELETE CASCADE,
    FOREIGN KEY (target_note) REFERENCES Note (id) ON DELETE CASCADE,
    CHECK (source_note != target_note)
    );
    """    
    with conn:
        conn.execute("PRAGMA foreign_keys = ON;") # Enforce Foreign keys (default off for legacy)
        conn.execute(note_table)
        conn.execute(link_table)

    conn.close()

# assumes formatting before save
# datetime will be formed by service layer
# for a new note, assuming separate method later for updating
def insert_note(id:str, title:str, raw:str, form:str, time:datetime):
    """Create a new, complete, row in the Note table"""
    command = """
    INSERT INTO Note (id, title, raw_note, approved_note, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    conn = sqlite3.connect(VAULT_PATH)
    try:
        with conn:
            conn.execute(command, (id, title, raw, form, time))
    finally:
        conn.close()



def save_link():
    """Create a new, complete row in the Link table"""
    pass

# read that DTOs are typically only for inter-module or server to api. 
# however, getting all notes / links for graph or display will return a lot of data. consider DTO / other solution?

def select_note(uid:str) -> dict:
    """Get approved and raw note and metadata for one note"""
    command = """
    SELECT raw_note, approved_note, created_at, updated_at
    FROM Note
    WHERE id = ?
    """
    conn = sqlite3.connect(VAULT_PATH)
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            cur = conn.execute(command, (uid,))
            row = cur.fetchone()
        
        if row is None:
            return None
    finally:
        conn.close()

    return dict(row)

def select_all_notes() -> list[dict]:
    """Get title, id, later tags / summary, for all notes"""
    conn = sqlite3.connect(VAULT_PATH)
    conn.row_factory = sqlite3.Row

    try:
        with conn:
            cur = conn.execute("SELECT id, title, updated_at FROM Note")
            rows = cur.fetchall()
    finally:
        conn.close()

    return [dict(r) for r in rows]

def get_link(uuid:str):
    """Get all links for a specific note"""
    pass

def get_all_links():
    """Get source / target note, id, relation type, for all links, used to build visual view"""
    pass

# if __name__ == "__main__":
#     setup()

