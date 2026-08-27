import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional

from guardrailai.core.models import (
    WorkflowExecutionRequest, WorkflowExecutionResponse, WorkflowDomain
)
from guardrailai.orchestration.workflow import DeterministicWorkflowEngine

app = FastAPI(
    title="GuardrailAI Platform Gateway",
    version="1.0.0",
    description="Compliance-Critical Deterministic Workflow Layer with Circuit Breakers and Cryptographic Audit Ledger"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = DeterministicWorkflowEngine()

# Mount Static UI Files
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_dashboard():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"service": "GuardrailAI", "status": "active", "docs": "/docs"}

@app.get("/healthz")
def healthz():
    return {"status": "healthy", "service": "GuardrailAI", "version": "1.0.0"}

@app.get("/readyz")
def readyz():
    return {"status": "ready", "guardrail_domains_active": 3}

@app.post("/api/v1/workflow/execute", response_model=WorkflowExecutionResponse)
def execute_workflow_endpoint(req: WorkflowExecutionRequest):
    return engine.execute_workflow(req)

@app.get("/api/v1/audit/ledger/{workflow_id}")
def get_audit_ledger(workflow_id: str):
    ledger = engine.active_ledgers.get(workflow_id)
    if not ledger:
        raise HTTPException(status_code=404, detail=f"Ledger for workflow '{workflow_id}' not found.")
    return {
        "workflow_id": workflow_id,
        "is_tamper_free": ledger.verify_integrity(),
        "total_blocks": len(ledger.blocks),
        "blocks": [b.model_dump() for b in ledger.blocks],
        "certificate": ledger.generate_certificate()
    }

@app.get("/api/v1/audit/verify/{workflow_id}")
def verify_audit_chain(workflow_id: str):
    ledger = engine.active_ledgers.get(workflow_id)
    if not ledger:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found.")
    is_valid = ledger.verify_integrity()
    return {
        "workflow_id": workflow_id,
        "valid": is_valid,
        "certificate": ledger.generate_certificate()
    }
