import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_assistant_chat_endpoint_fallback():
    # Calling assistant with general inquiry
    payload = {
        "message": "What is the fee for income certificate?",
        "language": "en",
        "context": {
            "service_slug": "income-certificate"
        }
    }
    res = client.post("/api/v1/assistant/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "answer" in data["data"]
    assert len(data["data"]["sources"]) > 0
    assert any("Aaple Sarkar" in s["title"] for s in data["data"]["sources"])
    assert data["data"]["session_id"] is not None

def test_assistant_chat_marathi():
    payload = {
        "message": "उत्पन्नाचा दाखला कसा काढायचा?",
        "language": "mr",
        "context": {
            "service_slug": "income-certificate"
        }
    }
    res = client.post("/api/v1/assistant/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["data"]["answer"]) > 10
