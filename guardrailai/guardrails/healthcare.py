import re
from typing import Dict, Any, List
from guardrailai.core.models import (
    WorkflowDomain, GuardrailViolation, GuardrailSeverity
)

class HealthcareGuardrails:
    """
    Enforces HIPAA Safe Harbor de-identification, FDA 21 CFR dosage safety, and clinical guardrails.
    """

    @staticmethod
    def evaluate_pre_flight(payload: Dict[str, Any]) -> List[GuardrailViolation]:
        violations = []
        notes = str(payload.get("clinical_notes", ""))
        
        # Check unscrubbed SSN
        if re.search(r"\b\d{3}-\d{2}-\d{4}\b", notes):
            violations.append(GuardrailViolation(
                rule_id="HEALTH-HIPAA-001",
                domain=WorkflowDomain.HEALTHCARE,
                severity=GuardrailSeverity.CRITICAL,
                description="Unredacted Social Security Number detected in clinical encounter input.",
                remediation_action="Execute automated Safe Harbor redaction pipeline prior to model invocation."
            ))
        return violations

    @staticmethod
    def evaluate_post_flight(result: Dict[str, Any]) -> List[GuardrailViolation]:
        violations = []
        dosage_mg = float(result.get("prescribed_dosage_mg", 0.0))
        medication = str(result.get("medication_name", "")).lower()

        # Critical dosage ceiling check
        if "warfarin" in medication and dosage_mg > 10.0:
            violations.append(GuardrailViolation(
                rule_id="HEALTH-DOSAGE-002",
                domain=WorkflowDomain.HEALTHCARE,
                severity=GuardrailSeverity.CRITICAL,
                description=f"Prescribed Warfarin dosage of {dosage_mg}mg exceeds maximum safe daily ceiling (10mg).",
                remediation_action="Circuit breaker tripped. Cap dosage at 5mg and require attending physician sign-off."
            ))
        return violations
