import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data"]["status"] == "ok"
    assert data["data"]["app"] == "SAARTHI"

def test_list_services():
    res = client.get("/api/v1/services")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data"]["total"] >= 3
    slugs = [s["slug"] for s in data["data"]["items"]]
    assert "income-certificate" in slugs
    assert "domicile-certificate" in slugs

def test_service_detail():
    res = client.get("/api/v1/services/income-certificate")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data"]["slug"] == "income-certificate"
    assert data["data"]["statutory_fee_inr"] == 33.60
    assert data["data"]["processing_days"] == 15
    assert len(data["data"]["sources"]) > 0

def test_service_detail_not_found():
    res = client.get("/api/v1/services/non-existent-service")
    assert res.status_code == 404
    data = res.json()
    assert data["success"] is False
    assert data["error"]["code"] == "HTTP_404"

def test_search_services_exact_and_natural():
    # Natural query in English
    res = client.post("/api/v1/search", json={"query": "income certificate Pune", "language": "en"})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["data"]["items"]) > 0
    assert data["data"]["items"][0]["slug"] == "income-certificate"

    # Query in Marathi
    res_mr = client.post("/api/v1/search", json={"query": "उत्पन्नाचा दाखला", "language": "mr"})
    assert res_mr.status_code == 200
    assert res_mr.json()["data"]["items"][0]["slug"] == "income-certificate"

def test_service_documents():
    res = client.get("/api/v1/services/income-certificate/documents")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    docs = data["data"]["documents"]
    assert len(docs) >= 3
    # Check mandatory document exists
    assert any(d["is_mandatory"] is True for d in docs)

def test_service_steps():
    res = client.get("/api/v1/services/income-certificate/steps")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    steps = data["data"]["steps"]
    assert len(steps) >= 3
    assert steps[0]["step_number"] == 1

def test_eligibility_questions():
    res = client.get("/api/v1/services/income-certificate/eligibility/questions")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    questions = data["data"]["questions"]
    assert len(questions) >= 2
    keys = [q["field_key"] for q in questions]
    assert "is_maharashtra_resident" in keys
    assert "annual_family_income" in keys

def test_eligibility_evaluation_eligible():
    # Passing answers
    payload = {
        "answers": {
            "is_maharashtra_resident": True,
            "annual_family_income": 85000
        },
        "language": "en"
    }
    res = client.post("/api/v1/services/income-certificate/eligibility/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data"]["status"] == "potentially_eligible"
    assert len(data["data"]["rule_results"]) >= 2
    assert all(r["passed"] is True for r in data["data"]["rule_results"])

def test_eligibility_evaluation_disqualified():
    # Failing answers (not resident)
    payload = {
        "answers": {
            "is_maharashtra_resident": False,
            "annual_family_income": 85000
        },
        "language": "en"
    }
    res = client.post("/api/v1/services/income-certificate/eligibility/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data"]["status"] == "potentially_not_eligible"
    # Verify rule result failure
    res_failed = [r for r in data["data"]["rule_results"] if not r["passed"]]
    assert len(res_failed) > 0

def test_eligibility_evaluation_missing_info():
    # Missing required field
    payload = {
        "answers": {
            "is_maharashtra_resident": True
        },
        "language": "en"
    }
    res = client.post("/api/v1/services/income-certificate/eligibility/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data"]["status"] == "more_information_required"
    assert len(data["data"]["missing_information"]) > 0

def test_feedback_submission():
    payload = {
        "category": "clarity",
        "comments": "The document checklist was very clear and helpful.",
        "rating": 5,
        "language": "en"
    }
    res = client.post("/api/v1/feedback", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["success"] is True
    assert data["data"]["rating"] == 5

def test_admin_auth_and_protected_routes():
    # Attempt access without token
    res_unauth = client.get("/api/v1/admin/services")
    assert res_unauth.status_code == 401

    # Login with bootstrap credentials
    login_payload = {
        "email": "admin@saarthi.local",
        "password": "AdminSecurePassword123!"
    }
    res_login = client.post("/api/v1/admin/auth/login", json=login_payload)
    assert res_login.status_code == 200
    token = res_login.json()["data"]["access_token"]

    # Access protected route with Bearer token
    headers = {"Authorization": f"Bearer {token}"}
    res_admin_services = client.get("/api/v1/admin/services", headers=headers)
    assert res_admin_services.status_code == 200
    assert len(res_admin_services.json()["data"]) >= 3
