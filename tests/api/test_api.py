import pytest
import app.api as api
from fastapi.testclient import TestClient

client = TestClient(api.app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_format_endpoint(monkeypatch):

    def fake_format_note(raw:str) -> str:
        return "fake formatted note"
    
    monkeypatch.setattr(api.llm_service, "format_note", fake_format_note)

    response = client.post(
        "/format",
        json={"content": "note to format"}
    )

    assert response.status_code == 200
    assert response.json() == "fake formatted note"