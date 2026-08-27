from fastapi.testclient import TestClient
from guardrailai.server import app

client = TestClient(app)

def test_server_dashboard_root():
    res = client.get("/")
    assert res.status_code == 200
    assert "GuardrailAI" in res.text

def test_server_healthz():
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_server_readyz():
    res = client.get("/readyz")
    assert res.status_code == 200
    assert res.json()["guardrail_domains_active"] == 3

def test_server_workflow_execute_api():
    payload = {
        "workflow_id": "wf-api-test-01",
        "domain": "FINANCIAL",
        "task_intent": "FUNDS_TRANSFER",
        "payload": {"amount_usd": 3000, "destination_country": "GB"},
        "fallback_policy": "SAFE_DEFAULT"
    }
    res = client.post("/api/v1/workflow/execute", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["final_status"] == "COMPLETED"
    assert data["audit_chain_length"] >= 4

def test_server_audit_ledger_api():
    # First execute
    payload = {
        "workflow_id": "wf-audit-api-01",
        "domain": "LEGAL",
        "task_intent": "CONTRACT_REVIEW",
        "payload": {"contract_text": "Mutual liability cap of $1M."},
        "fallback_policy": "SAFE_DEFAULT"
    }
    client.post("/api/v1/workflow/execute", json=payload)

    # Get ledger
    res = client.get("/api/v1/audit/ledger/wf-audit-api-01")
    assert res.status_code == 200
    assert res.json()["is_tamper_free"] is True
    assert len(res.json()["blocks"]) >= 4

    # Verify
    v_res = client.get("/api/v1/audit/verify/wf-audit-api-01")
    assert v_res.status_code == 200
    assert v_res.json()["valid"] is True
