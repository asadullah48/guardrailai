from typing import Dict, Any, List
from guardrailai.core.models import (
    WorkflowDomain, GuardrailViolation, GuardrailSeverity
)

class LegalGuardrails:
    """
    Enforces liability limitations, unilateral indemnity blockers, and legal ethical guardrails.
    """

    @staticmethod
    def evaluate_pre_flight(payload: Dict[str, Any]) -> List[GuardrailViolation]:
        violations = []
        contract_text = str(payload.get("contract_text", "")).lower()

        if "unlimited liability" in contract_text or "neither party's liability shall be limited" in contract_text:
            violations.append(GuardrailViolation(
                rule_id="LEGAL-LIABILITY-001",
                domain=WorkflowDomain.LEGAL,
                severity=GuardrailSeverity.CRITICAL,
                description="Uncapped consequential and direct liability detected in clause proposal.",
                remediation_action="Inject mandatory 12-month aggregate fee liability ceiling."
            ))

        if "unilateral indemnify" in contract_text or ("customer shall indemnify" in contract_text and "mutual" not in contract_text):
            violations.append(GuardrailViolation(
                rule_id="LEGAL-INDEMNITY-002",
                domain=WorkflowDomain.LEGAL,
                severity=GuardrailSeverity.BLOCKING,
                description="One-sided unilateral indemnification clause violates enterprise risk policy.",
                remediation_action="Transform indemnification clause into bilateral mutual indemnity structure."
            ))

        return violations

    @staticmethod
    def evaluate_post_flight(result: Dict[str, Any]) -> List[GuardrailViolation]:
        violations = []
        if not result.get("includes_ai_legal_disclaimer", True):
            violations.append(GuardrailViolation(
                rule_id="LEGAL-ETHICS-003",
                domain=WorkflowDomain.LEGAL,
                severity=GuardrailSeverity.WARNING,
                description="AI-generated legal work product lacks statutory non-lawyer disclaimer.",
                remediation_action="Append standard ABA Model Rule 5.3 supervisory notice."
            ))
        return violations
