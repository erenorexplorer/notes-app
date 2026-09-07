import pytest
import app.api as api
from app.vault import model
import app.workflows as workflows
import app.vault.service as vault_service
from fastapi.testclient import TestClient
from uuid import UUID
from app.schemas import NoteOverview, LinkSuggestion
import sqlite3

client = TestClient(api.app)

@pytest.fixture
def test_db(tmp_path, monkeypatch):
    test_db_path = tmp_path / "test_vault.db"
    monkeypatch.setattr(model, "VAULT_PATH", test_db_path)
    model.setup()
    return test_db_path

@pytest.fixture
def fake_llm(monkeypatch):

    def fake_format_note(raw: str) -> str:
        return "Formatted Version of:" + raw
    
    def fake_suggest_links(approved_note: str, candidates: list[NoteOverview]) -> list[LinkSuggestion]:
        for candidate in candidates:
            if candidate.title == "SQLite Foreign Key Enforcement":
                return [
                    LinkSuggestion(
                        candidate_id=candidate.id,
                        relation_type="related",
                    )
                ]
            
        return []

    
    monkeypatch.setattr(workflows.llm_service, "format_note", fake_format_note)
    monkeypatch.setattr(workflows.llm_service, "suggest_links", fake_suggest_links)

def test_create_approve_link_workflow(test_db, fake_llm):
    
    # ========== FORMAT_RAW ENDPOINT/ ==========

    # Arrange:
    # - Seed a note to simulate an existing note in db
    # - Define input note
    candidate_note = {
        'raw': (
            "SQLite does not always enforce foreign key constraints automatically. "
            "Foreign key enforcement may need to be enabled for each database connection."
        ),
        'title': "SQLite Foreign Key Enforcement",
        "approved": (
            "# SQLite Foreign Key Enforcement\n\n"
            "SQLite foreign key constraints help preserve relationships between tables, "
            "but enforcement may need to be enabled per connection using PRAGMA settings."
        ),
    }

    candidate_id = vault_service.create_raw_note(candidate_note['raw'])
    vault_service.save_approved_note(candidate_id, candidate_note['title'], candidate_note['approved'])

    raw_note_input = {
            'title': "SQL Foreign Keys",
            'content': "An SQLite foreign key constraint is a database rule that enforces a relationship between "
            "two tables to maintain referential integrity. It links a column (or columns) in a \"child\" table to a "
            "primary key or unique column in a \"parent\" table"
    }

    # Act:
    # - Call API with input note
    format_note_response = client.post("/notes", json=raw_note_input)

    # Assert:
    # - Check status code
    # - Check return values
    assert format_note_response.status_code == 200
    formatted_note = format_note_response.json()
    assert set(formatted_note.keys()) == {'id', 'title', 'content'}
    assert formatted_note['title'] == raw_note_input['title']
    assert formatted_note['content'] == "Formatted Version of:" + raw_note_input['content']
    
    note_id = UUID(formatted_note["id"])
    assert str(note_id) == formatted_note["id"]

    # ========== /FORMAT_RAW ENDPOINT ==========

    # ========== APPROVE_NOTE ENDPOINT/ ==========

    approve_note_response = client.put(f"/notes/{formatted_note['id']}/approve", json=formatted_note)
    assert approve_note_response.status_code == 200
    suggested_links = approve_note_response.json()
    assert isinstance(suggested_links, list)
    assert len(suggested_links) == 1
    assert set(suggested_links[0].keys()) == {'candidate_id', 'candidate_title', 'relation_type'}
    assert suggested_links[0]['candidate_id'] == candidate_id
    assert suggested_links[0]['candidate_title'] == candidate_note['title']
    assert suggested_links[0]['relation_type'] == 'related'

    # ========== /APPROVE_NOTE ENDPOINT ==========

    # ========== APPROVE_LINKS ENDPOINT/ ==========

    approved_links_response = client.post(f"/notes/{formatted_note['id']}/links/approve", json=suggested_links)
    assert approved_links_response.status_code == 200

    conn = sqlite3.connect(test_db)
    conn.row_factory = sqlite3.Row

    try:
        with conn:
            row = conn.execute(
                "SELECT source_note, target_note, relation_type FROM Link WHERE source_note = ?",
                (formatted_note['id'],)
            ).fetchone()
    finally:
        conn.close()

    assert row is not None
    assert row['source_note'] == formatted_note['id']
    assert row['target_note'] == candidate_id
    assert row['relation_type'] == "related"

    # ========== \APPROVE_LINKS ENDPOINT ==========

    conn = sqlite3.connect(test_db)
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            row = conn.execute(
                "SELECT id, title, raw_note, approved_note, status FROM Note WHERE id = ?",
                (formatted_note['id'],)
            ).fetchone()

    finally:
        conn.close()

    assert row is not None
    assert row['id'] == formatted_note['id']
    assert row['title'] == formatted_note['title']
    assert row['raw_note'] == raw_note_input['content']
    assert row['approved_note'] == formatted_note['content']
    assert row['status'] == "approved"