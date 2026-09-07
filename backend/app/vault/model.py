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
        title          TEXT,
        raw_note       TEXT NOT NULL,
        approved_note  TEXT,
        status         TEXT CHECK(status IN ('raw_saved', 'approved', 'archived')) NOT NULL DEFAULT 'raw_saved',
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

# for a new note, only raw note is required
def insert_note(id:str, raw:str, time:datetime):
    """Create a new row in the Note table containing id, time, and raw note"""
    command = """
    INSERT INTO Note (id, raw_note, status, created_at, updated_at)
    VALUES (?, ?, 'raw_saved', ?, ?)
    """
    conn = sqlite3.connect(VAULT_PATH)
    try:
        with conn:
            conn.execute(command, (id, raw, time, time))
    finally:
        conn.close()

# update approved note and status
def update_approved_note(id: str, title: str, approved: str, time: datetime):
    """Update an existing note with the approved note, title, and status."""
    command = """
    UPDATE Note
    SET 
        title = :title,
        approved_note = :approved_note,
        status = 'approved',
        updated_at = :updated_at
    WHERE id = :id
    """

    params = {
        "id": id,
        "title": title,
        "approved_note": approved,
        "updated_at": time,
    }

    conn = sqlite3.connect(VAULT_PATH)
    try:
        with conn:
            conn.execute(command, params)
    finally:
        conn.close()

def insert_approved_links(links: list[dict]):
    """Take a list of dicts and save links to database
    Each dict should contain: link_id, source_note, target_note, relation_type, created_at"""
    
    command = """
    INSERT INTO Link (id, source_note, target_note, relation_type, created_at)
    VALUES (:link_id, :source_note, :target_note, :relation_type, :created_at)
    """

    conn = sqlite3.connect(VAULT_PATH)
    try:
        with conn:
            conn.executemany(command, links)
    finally:
        conn.close()


def select_note(uid:str) -> dict:
    """Get approved and raw note and metadata for one note"""
    command = """
    SELECT title, raw_note, approved_note, created_at, updated_at
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

def select_note_overviews() -> list[dict]:
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

def select_note_previews() -> list[dict]:
    """Return note data used to build graph previews.

    Returns:
        list[dict]: A list of note rows. Each dictionary contains:
            - id (str): Unique note ID.
            - title (str): Note title.
            - approved_note (str): Approved note content used for the preview.
    """

    conn = sqlite3.connect(VAULT_PATH)
    conn.row_factory = sqlite3.Row

    try:
        with conn:
            cur = conn.execute(
                """
                SELECT id, title, approved_note
                FROM Note
                WHERE status = 'approved'
                """
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    return [dict(r) for r in rows]


def select_all_links() -> list[dict]:
    """Return all links from the vault.

    Returns:
        list[dict]: A list of link rows. Each dictionary contains:
            - id (str): Unique link ID.
            - source_note (str): Source note ID.
            - target_note (str): Target note ID.
            - relation_type (str): Relationship type between the notes.
    """
    conn = sqlite3.connect(VAULT_PATH)
    conn.row_factory = sqlite3.Row

    try:
        with conn:
            cur = conn.execute("SELECT id, source_note, target_note, relation_type FROM Link")
            rows = cur.fetchall()
    finally:
        conn.close()

    return [dict(r) for r in rows]


# if __name__ == "__main__":
#     setup()

