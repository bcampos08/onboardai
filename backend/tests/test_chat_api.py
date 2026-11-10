"""POST /api/chat/ask must return exactly the fields in the interface contract."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

CONTRACT_FIELDS = {"conversation_id", "message_id", "answer", "citations", "fallback", "fallback_reason"}
CITATION_FIELDS = {"document_id", "section_id", "title", "section_heading", "source_page"}


def test_answer_matches_contract():
    response = client.post("/api/chat/ask", json={"question": "How do I request time off?", "conversation_id": None})
    assert response.status_code == 200
    body = response.json()
    assert set(body) == CONTRACT_FIELDS
    assert body["fallback"] is False
    assert set(body["citations"][0]) == CITATION_FIELDS


def test_fallback_matches_contract():
    response = client.post("/api/chat/ask", json={"question": "What is the parking policy?"})
    assert response.status_code == 200
    body = response.json()
    assert set(body) == CONTRACT_FIELDS
    assert (body["fallback"], body["fallback_reason"], body["citations"]) == (True, "no_match", [])


def test_empty_question_is_rejected():
    response = client.post("/api/chat/ask", json={"question": ""})
    assert response.status_code == 422


def test_demo_page_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "OnboardAI" in response.text
