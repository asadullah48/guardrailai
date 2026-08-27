import pytest
from guardrailai.agents.process_agent import ProcessAgent
from guardrailai.agents.compliance_agent import ComplianceAgent
from guardrailai.agents.audit_agent import AuditAgent
from guardrailai.core.models import WorkflowDomain
from guardrailai.core.audit_ledger import AuditLedger

def test_process_agent_deterministic_execution():
    agent = ProcessAgent()
    fin_res = agent.execute_step(WorkflowDomain.FINANCIAL, {"amount_usd": 7500})
    assert fin_res["execution_status"] == "PROCESSED"
    assert fin_res["amount_processed_usd"] == 7500

    med_res = agent.execute_step(WorkflowDomain.HEALTHCARE, {"medication_name": "Metformin", "dosage_mg": 500})
    assert med_res["execution_status"] == "CLINICALLY_VERIFIED"

def test_compliance_agent_evaluation():
    agent = ComplianceAgent()
    violations = agent.evaluate_pre_flight(WorkflowDomain.FINANCIAL, {"amount_usd": 25000, "destination_country": "IRAN"})
    assert len(violations) >= 2

def test_audit_agent_record_and_certify():
    agent = AuditAgent()
    ledger = AuditLedger("wf-agent-test")
    agent.record_step(ledger, "TEST_STEP", agent.name, {"key": "val"}, {"status": "DONE"})
    cert = agent.certify_workflow(ledger)
    assert "AUDIT-SEAL" in cert
