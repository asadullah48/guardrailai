from typing import Dict, Any, List, Tuple
from guardrailai.core.models import (
    WorkflowDomain, GuardrailViolation, GuardrailSeverity
)

AML_MAX_TRANSACTION_USD = 10000.0  # Bank Secrecy Act / FinCEN CTR Threshold
SANCTIONED_COUNTRIES = ["NORTH_KOREA", "IRAN", "SYRIA", "CRIMEA_REGION"]

class FinancialGuardrails:
    """
    Enforces AML limits, OFAC Sanctions, SOX financial thresholds, and Shari'ah leverage caps.
    """

    @staticmethod
    def evaluate_pre_flight(payload: Dict[str, Any]) -> List[GuardrailViolation]:
        violations = []
        amount = float(payload.get("amount_usd", 0.0))
        dest_country = str(payload.get("destination_country", "US")).upper()

        # 1. Sanctions Check
        if dest_country in SANCTIONED_COUNTRIES:
            violations.append(GuardrailViolation(
                rule_id="FIN-OFAC-001",
                domain=WorkflowDomain.FINANCIAL,
                severity=GuardrailSeverity.CRITICAL,
                description=f"Destination country '{dest_country}' is subject to OFAC comprehensive sanctions.",
                remediation_action="Block transaction immediately and report to BSA/AML compliance officer."
            ))

        # 2. AML Threshold Check
        if amount >= AML_MAX_TRANSACTION_USD:
            violations.append(GuardrailViolation(
                rule_id="FIN-AML-002",
                domain=WorkflowDomain.FINANCIAL,
                severity=GuardrailSeverity.BLOCKING,
                description=f"Transaction amount ${amount:,.2f} exceeds CTR mandatory reporting threshold ($10,000).",
                remediation_action="Trigger FinCEN Currency Transaction Report (CTR) workflow or split verification."
            ))

        return violations

    @staticmethod
    def evaluate_post_flight(result: Dict[str, Any]) -> List[GuardrailViolation]:
        violations = []
        debt_to_equity = float(result.get("debt_to_equity_ratio", 0.0))
        if debt_to_equity > 0.33:
            violations.append(GuardrailViolation(
                rule_id="FIN-SHARIAH-003",
                domain=WorkflowDomain.FINANCIAL,
                severity=GuardrailSeverity.WARNING,
                description=f"Debt-to-Market-Cap ratio {debt_to_equity:.2%} exceeds AAOIFI 33% Islamic compliance threshold.",
                remediation_action="Filter out non-compliant security from halal investment mandate."
            ))
        return violations
