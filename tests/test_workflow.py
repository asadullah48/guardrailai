import pytest
from guardrailai.orchestration.workflow import DeterministicWorkflowEngine
from guardrailai.core.models import (
    WorkflowExecutionRequest, WorkflowDomain, WorkflowStatus, FallbackPolicy
)

def test_workflow_clean_execution():
    engine = DeterministicWorkflowEngine()
    req = WorkflowExecutionRequest(
        workflow_id="wf-clean-01",
        domain=WorkflowDomain.FINANCIAL,
        task_intent="PAYMENT_ROUTING",
        payload={"amount_usd": 4500, "destination_country": "US"}
    )
    res = engine.execute_workflow(req)
    assert res.final_status == WorkflowStatus.COMPLETED
    assert res.circuit_breaker_active is False
    assert res.fallback_applied is False
    assert len(res.violations_detected) == 0
    assert res.audit_chain_length >= 4

def test_workflow_circuit_breaker_pre_flight():
    engine = DeterministicWorkflowEngine()
    req = WorkflowExecutionRequest(
        workflow_id="wf-sanction-01",
        domain=WorkflowDomain.FINANCIAL,
        task_intent="CROSS_BORDER_WIRE",
        payload={"amount_usd": 50000, "destination_country": "IRAN"},
        fallback_policy=FallbackPolicy.SAFE_DEFAULT
    )
    res = engine.execute_workflow(req)
    assert res.final_status == WorkflowStatus.CIRCUIT_BREAKER_TRIGGERED
    assert res.circuit_breaker_active is True
    assert res.fallback_applied is True
    assert len(res.violations_detected) >= 1
    assert "SAFE_DEFAULT_APPLIED" in res.result_data["action"]

def test_workflow_human_escalation_policy():
    engine = DeterministicWorkflowEngine()
    req = WorkflowExecutionRequest(
        workflow_id="wf-escalate-01",
        domain=WorkflowDomain.HEALTHCARE,
        task_intent="CLINICAL_ORDER",
        payload={"clinical_notes": "Patient SSN is 000-11-2222"},
        fallback_policy=FallbackPolicy.HUMAN_ESCALATION
    )
    res = engine.execute_workflow(req)
    assert res.final_status == WorkflowStatus.CIRCUIT_BREAKER_TRIGGERED
    assert res.result_data["action"] == "ESCALATED_TO_HUMAN_SUPERVISOR"
