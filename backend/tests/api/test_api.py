import pytest
import app.api as api
from app.vault import model
from fastapi.testclient import TestClient
import sqlite3

client = TestClient(api.app)

@pytest.fixture
def test_db(tmp_path, monkeypatch):
    test_db_path = tmp_path / "test_vault.db"
    monkeypatch.setattr(model, "VAULT_PATH", test_db_path)
    model.setup()
    return test_db_path

def test_root():
    response = client.get("/")
    assert response.status_code == 200

# def test_format_endpoint(monkeypatch):

#     def fake_format_note(raw:str) -> str:
#         return "fake formatted note"
    
#     monkeypatch.setattr(api.llm_service, "format_note", fake_format_note)

#     response = client.post(
#         "/format",
#         json={"content": "note to format"}
#     )

#     assert response.status_code == 200
#     assert response.json() == "fake formatted note"

def test_get_graph_returns_correct_data_shape(test_db):
    seed_notes = [
    {
        "id": "note-python-functions",
        "title": "Python Functions as Objects",
        "raw_note": "functions can be assigned to variables and passed around",
        "approved_note": (
            "Python functions are first-class objects, so they can be "
            "assigned to variables and passed to other functions."
        ),
        "status": "approved",
        "created_at": "2026-09-01 10:00:00",
        "updated_at": "2026-09-01 10:05:00",
    },
    {
        "id": "note-callbacks",
        "title": "Callback Functions",
        "raw_note": "callbacks are functions another part of the program runs later",
        "approved_note": (
            "A callback is a function passed to another component so that "
            "component can invoke it later."
        ),
        "status": "approved",
        "created_at": "2026-09-02 11:00:00",
        "updated_at": "2026-09-02 11:05:00",
    },
    {
        "id": "note-dependency-injection",
        "title": "Dependency Injection",
        "raw_note": "give code dependencies instead of hard coding them",
        "approved_note": (
            "Dependency injection supplies a component with its dependencies "
            "instead of having the component construct them itself."
        ),
        "status": "approved",
        "created_at": "2026-09-03 12:00:00",
        "updated_at": "2026-09-03 12:05:00",
    },
]

    seed_links = [
        {
            "id": "link-functions-callbacks",
            "source_note": "note-python-functions",
            "target_note": "note-callbacks",
            "relation_type": "related",
            "created_at": "2026-09-04 09:00:00",
        },
        {
            "id": "link-callbacks-di",
            "source_note": "note-callbacks",
            "target_note": "note-dependency-injection",
            "relation_type": "related",
            "created_at": "2026-09-04 09:05:00",
        },
    ]

    conn = sqlite3.connect(test_db)

    try:
        with conn:
            conn.execute("PRAGMA foreign_keys = ON;")

            conn.executemany(
                """
                INSERT INTO Note (
                    id,
                    title,
                    raw_note,
                    approved_note,
                    status,
                    created_at,
                    updated_at
                )
                VALUES (
                    :id,
                    :title,
                    :raw_note,
                    :approved_note,
                    :status,
                    :created_at,
                    :updated_at
                )
                """,
                seed_notes,
            )

            conn.executemany(
                """
                INSERT INTO Link (
                    id,
                    source_note,
                    target_note,
                    relation_type,
                    created_at
                )
                VALUES (
                    :id,
                    :source_note,
                    :target_note,
                    :relation_type,
                    :created_at
                )
                """,
                seed_links,
            )
    finally:
        conn.close()

    response = client.get("/graph")
    assert response.status_code == 200

    graph_data = response.json()
    assert set(graph_data.keys()) == {"nodes", "links"}

    # Assert Nodes
    actual_nodes = sorted(graph_data["nodes"], key=lambda node: node["id"])
    expected_nodes = sorted(
        [
            {
                "id": note["id"],
                "title": note["title"],
                "preview": note["approved_note"],
            }
            for note in seed_notes
        ],
        key=lambda node: node["id"],
    )

    assert actual_nodes == expected_nodes

    # Assert Links
    actual_links = sorted(graph_data["links"], key=lambda link: link["id"])
    expected_links = sorted(
        [
            {
                "id": link["id"],
                "source_id": link["source_note"],
                "target_id": link["target_note"],
                "relation_type": link["relation_type"],
            }
            for link in seed_links
        ],
        key=lambda link: link["id"],
    )

    assert actual_links == expected_links

def test_get_graph_filters_links_to_invalid_nodes(test_db):
    seed_notes = [
        {
            "id": "note-a",
            "title": "Approved Note A",
            "raw_note": "raw a",
            "approved_note": "approved a",
            "status": "approved",
            "created_at": "2026-09-01 10:00:00",
            "updated_at": "2026-09-01 10:05:00",
        },
        {
            "id": "note-b",
            "title": "Approved Note B",
            "raw_note": "raw b",
            "approved_note": "approved b",
            "status": "approved",
            "created_at": "2026-09-02 10:00:00",
            "updated_at": "2026-09-02 10:05:00",
        },
        {
            "id": "note-unapproved",
            "title": "Unapproved Note",
            "raw_note": "raw only",
            "approved_note": None,
            "status": "raw_saved",
            "created_at": "2026-09-03 10:00:00",
            "updated_at": "2026-09-03 10:05:00",
        },
    ]

    seed_links = [
        {
            "id": "link-valid",
            "source_note": "note-a",
            "target_note": "note-b",
            "relation_type": "related",
            "created_at": "2026-09-04 09:00:00",
        },
        {
            "id": "link-invalid-for-graph",
            "source_note": "note-a",
            "target_note": "note-unapproved",
            "relation_type": "related",
            "created_at": "2026-09-04 09:05:00",
        },
    ]

    conn = sqlite3.connect(test_db)

    try:
        with conn:
            conn.execute("PRAGMA foreign_keys = ON;")

            conn.executemany(
                """
                INSERT INTO Note (
                    id,
                    title,
                    raw_note,
                    approved_note,
                    status,
                    created_at,
                    updated_at
                )
                VALUES (
                    :id,
                    :title,
                    :raw_note,
                    :approved_note,
                    :status,
                    :created_at,
                    :updated_at
                )
                """,
                seed_notes,
            )

            conn.executemany(
                """
                INSERT INTO Link (
                    id,
                    source_note,
                    target_note,
                    relation_type,
                    created_at
                )
                VALUES (
                    :id,
                    :source_note,
                    :target_note,
                    :relation_type,
                    :created_at
                )
                """,
                seed_links,
            )
    finally:
        conn.close()

    response = client.get("/graph")

    assert response.status_code == 200

    graph_data = response.json()

    node_ids = {node["id"] for node in graph_data["nodes"]}
    link_ids = {link["id"] for link in graph_data["links"]}

    assert node_ids == {"note-a", "note-b"}
    assert link_ids == {"link-valid"}