from typing import Dict, Any, List
from guardrailai.core.models import (
    WorkflowDomain, GuardrailViolation, GuardrailSeverity
)
from guardrailai.guardrails.financial import FinancialGuardrails
from guardrailai.guardrails.healthcare import HealthcareGuardrails
from guardrailai.guardrails.legal import LegalGuardrails

class ComplianceAgent:
    """
    ComplianceAgent: Evaluates pre-execution inputs and post-execution results against
    strict statutory and institutional policies.
    """
    def __init__(self):
        self.name = "ComplianceAgent"
        self.version = "1.0.0"

    def evaluate_pre_flight(self, domain: WorkflowDomain, payload: Dict[str, Any]) -> List[GuardrailViolation]:
        if domain == WorkflowDomain.FINANCIAL:
            return FinancialGuardrails.evaluate_pre_flight(payload)
        elif domain == WorkflowDomain.HEALTHCARE:
            return HealthcareGuardrails.evaluate_pre_flight(payload)
        elif domain == WorkflowDomain.LEGAL:
            return LegalGuardrails.evaluate_pre_flight(payload)
        return []

    def evaluate_post_flight(self, domain: WorkflowDomain, result: Dict[str, Any]) -> List[GuardrailViolation]:
        if domain == WorkflowDomain.FINANCIAL:
            return FinancialGuardrails.evaluate_post_flight(result)
        elif domain == WorkflowDomain.HEALTHCARE:
            return HealthcareGuardrails.evaluate_post_flight(result)
        elif domain == WorkflowDomain.LEGAL:
            return LegalGuardrails.evaluate_post_flight(result)
        return []
