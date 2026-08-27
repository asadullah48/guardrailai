from typing import Dict, Any, List
from guardrailai.core.models import (
    WorkflowExecutionRequest, WorkflowExecutionResponse, WorkflowStatus,
    GuardrailSeverity, FallbackPolicy
)
from guardrailai.core.audit_ledger import AuditLedger
from guardrailai.agents.process_agent import ProcessAgent
from guardrailai.agents.compliance_agent import ComplianceAgent
from guardrailai.agents.audit_agent import AuditAgent

class DeterministicWorkflowEngine:
    """
    Orchestrates the compliance-critical deterministic pipeline:
    PLAN -> PRE_GUARDRAIL -> PROCESS -> POST_GUARDRAIL -> AUDIT -> CERTIFICATE
    With automated Circuit Breakers and Fallback routing.
    """
    def __init__(self):
        self.process_agent = ProcessAgent()
        self.compliance_agent = ComplianceAgent()
        self.audit_agent = AuditAgent()
        self.active_ledgers: Dict[str, AuditLedger] = {}

    def execute_workflow(self, req: WorkflowExecutionRequest) -> WorkflowExecutionResponse:
        ledger = AuditLedger(workflow_id=req.workflow_id)
        self.active_ledgers[req.workflow_id] = ledger

        all_violations = []
        circuit_breaker = False
        fallback_applied = False

        # Step 1: Pre-Flight Guardrail Check
        pre_violations = self.compliance_agent.evaluate_pre_flight(req.domain, req.payload)
        all_violations.extend(pre_violations)

        self.audit_agent.record_step(
            ledger, "PRE_FLIGHT_GUARDRAIL", self.compliance_agent.name,
            req.payload, [v.model_dump() for v in pre_violations],
            {"violations_count": len(pre_violations)}
        )

        has_critical_pre = any(v.severity in [GuardrailSeverity.CRITICAL, GuardrailSeverity.BLOCKING] for v in pre_violations)

        if has_critical_pre:
            circuit_breaker = True
            fallback_applied = True
            fallback_result = self._apply_fallback(req, pre_violations, "PRE_FLIGHT_VIOLATION")
            
            self.audit_agent.record_step(
                ledger, "FALLBACK_CIRCUIT_BREAKER", "SystemEngine",
                req.payload, fallback_result, {"reason": "Pre-flight policy violation"}
            )
            cert = self.audit_agent.certify_workflow(ledger)
            return WorkflowExecutionResponse(
                workflow_id=req.workflow_id,
                domain=req.domain,
                final_status=WorkflowStatus.CIRCUIT_BREAKER_TRIGGERED,
                violations_detected=all_violations,
                circuit_breaker_active=True,
                fallback_applied=True,
                result_data=fallback_result,
                audit_chain_length=len(ledger.blocks),
                tamper_evident_certificate=cert
            )

        # Step 2: Deterministic Processing
        process_out = self.process_agent.execute_step(req.domain, req.payload)
        self.audit_agent.record_step(
            ledger, "DETERMINISTIC_PROCESS", self.process_agent.name,
            req.payload, process_out, {"status": "SUCCESS"}
        )

        # Step 3: Post-Flight Guardrail Check
        post_violations = self.compliance_agent.evaluate_post_flight(req.domain, process_out)
        all_violations.extend(post_violations)

        self.audit_agent.record_step(
            ledger, "POST_FLIGHT_GUARDRAIL", self.compliance_agent.name,
            process_out, [v.model_dump() for v in post_violations],
            {"violations_count": len(post_violations)}
        )

        has_critical_post = any(v.severity == GuardrailSeverity.CRITICAL for v in post_violations)

        if has_critical_post:
            circuit_breaker = True
            fallback_applied = True
            fallback_result = self._apply_fallback(req, post_violations, "POST_FLIGHT_SAFETY_BREACH")
            self.audit_agent.record_step(
                ledger, "POST_FALLBACK_APPLIED", "SystemEngine",
                process_out, fallback_result, {"reason": "Post-flight safety breach"}
            )
            cert = self.audit_agent.certify_workflow(ledger)
            return WorkflowExecutionResponse(
                workflow_id=req.workflow_id,
                domain=req.domain,
                final_status=WorkflowStatus.FALLBACK_EXECUTED,
                violations_detected=all_violations,
                circuit_breaker_active=True,
                fallback_applied=True,
                result_data=fallback_result,
                audit_chain_length=len(ledger.blocks),
                tamper_evident_certificate=cert
            )

        # Step 4: Final Certification
        cert = self.audit_agent.certify_workflow(ledger)
        return WorkflowExecutionResponse(
            workflow_id=req.workflow_id,
            domain=req.domain,
            final_status=WorkflowStatus.COMPLETED,
            violations_detected=all_violations,
            circuit_breaker_active=False,
            fallback_applied=False,
            result_data=process_out,
            audit_chain_length=len(ledger.blocks),
            tamper_evident_certificate=cert
        )

    def _apply_fallback(self, req: WorkflowExecutionRequest, violations: List[Any], context: str) -> Dict[str, Any]:
        if req.fallback_policy == FallbackPolicy.SAFE_DEFAULT:
            return {
                "action": "SAFE_DEFAULT_APPLIED",
                "original_request": req.task_intent,
                "safety_override": "Operation clamped to verified regulatory limits.",
                "context": context,
                "remediations": [v.remediation_action for v in violations]
            }
        elif req.fallback_policy == FallbackPolicy.HUMAN_ESCALATION:
            return {
                "action": "ESCALATED_TO_HUMAN_SUPERVISOR",
                "escalation_ticket_id": f"ESC-{abs(hash(req.workflow_id)) % 100000}",
                "pending_approval": True,
                "violations": [v.description for v in violations]
            }
        else:
            return {
                "action": "REJECTED_NON_COMPLIANT",
                "reason": violations[0].description if violations else "Policy breach",
                "remediation": violations[0].remediation_action if violations else "Adjust parameters"
            }
