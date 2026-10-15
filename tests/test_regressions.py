import os
import subprocess
import sys

import pytest

from guardrailai.core.audit_ledger import AuditLedger
from guardrailai.core.models import (
    FallbackPolicy, GuardrailSeverity, GuardrailViolation,
    WorkflowDomain, WorkflowExecutionRequest, WorkflowStatus,
)
from guardrailai.orchestration.workflow import DeterministicWorkflowEngine


@pytest.mark.parametrize("index", [0, 1])
@pytest.mark.parametrize("field,value", [
    ("block_index", 99), ("workflow_id", "other-workflow"),
    ("step_name", "ALTERED"), ("agent_name", "OtherAgent"),
    ("input_hash", "a" * 64), ("output_hash", "b" * 64),
    ("previous_block_hash", "c" * 64), ("current_block_hash", "d" * 64),
    ("timestamp", 0.0), ("metadata", {"approved": True}),
])
def test_integrity_covers_every_block_field(index, field, value):
    ledger = AuditLedger("wf-integrity")
    ledger.append_entry("EXEC", "ProcessAgent", {}, {}, {"approved": False})
    assert ledger.verify_integrity()
    setattr(ledger.blocks[index], field, value)
    assert ledger.verify_integrity() is False


def test_empty_ledger_is_invalid():
    ledger = AuditLedger("wf-empty")
    ledger.blocks.clear()
    assert ledger.verify_integrity() is False
    assert "VERIFIED-False" in ledger.generate_certificate()


def test_metadata_is_snapshotted_when_appended():
    ledger = AuditLedger("wf-snapshot")
    metadata = {"policy": {"approved": False}}
    ledger.append_entry("EXEC", "ProcessAgent", {}, {}, metadata)
    metadata["policy"]["approved"] = True
    assert ledger.blocks[1].metadata == {"policy": {"approved": False}}
    assert ledger.verify_integrity()


@pytest.mark.parametrize("kind", ["transaction", "escalation"])
def test_identifiers_are_stable_across_processes(kind):
    script = '''
from guardrailai.agents.process_agent import ProcessAgent
from guardrailai.core.models import WorkflowDomain, WorkflowExecutionRequest, FallbackPolicy
from guardrailai.orchestration.workflow import DeterministicWorkflowEngine
'''
    if kind == "transaction":
        script += '''
a = ProcessAgent()
x = a.execute_step(WorkflowDomain.FINANCIAL, {"amount_usd": 3, "destination_country": "GB"})
y = a.execute_step(WorkflowDomain.FINANCIAL, {"destination_country": "GB", "amount_usd": 3})
assert x == y
print(x["transaction_reference"])
'''
    else:
        script += '''
r = WorkflowExecutionRequest(workflow_id="wf-stable", payload={"destination_country": "IRAN"}, fallback_policy=FallbackPolicy.HUMAN_ESCALATION)
print(DeterministicWorkflowEngine().execute_workflow(r).result_data["escalation_ticket_id"])
'''
    outputs = [subprocess.check_output(
        [sys.executable, "-c", script], text=True,
        env={**os.environ, "PYTHONHASHSEED": seed},
    ).strip() for seed in ("1", "2")]
    assert outputs[0] == outputs[1]


def test_post_flight_blocking_violation_routes_to_fallback(monkeypatch):
    engine = DeterministicWorkflowEngine()
    violation = GuardrailViolation(
        rule_id="TEST-BLOCK", domain=WorkflowDomain.GENERAL,
        severity=GuardrailSeverity.BLOCKING, description="Blocked result",
        remediation_action="Reject output",
    )
    monkeypatch.setattr(engine.compliance_agent, "evaluate_post_flight", lambda *_: [violation])
    response = engine.execute_workflow(WorkflowExecutionRequest(domain=WorkflowDomain.GENERAL))
    assert response.final_status == WorkflowStatus.FALLBACK_EXECUTED
    assert response.circuit_breaker_active
    assert response.fallback_applied
    assert "payload_echo" not in response.result_data
