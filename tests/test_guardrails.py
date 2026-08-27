import pytest
from guardrailai.guardrails.financial import FinancialGuardrails
from guardrailai.guardrails.healthcare import HealthcareGuardrails
from guardrailai.guardrails.legal import LegalGuardrails
from guardrailai.core.models import GuardrailSeverity

def test_financial_guardrails_ofac_and_aml():
    # Clean payload
    clean = FinancialGuardrails.evaluate_pre_flight({"amount_usd": 5000, "destination_country": "US"})
    assert len(clean) == 0

    # Sanctions breach
    sanctioned = FinancialGuardrails.evaluate_pre_flight({"amount_usd": 2000, "destination_country": "NORTH_KOREA"})
    assert len(sanctioned) >= 1
    assert sanctioned[0].severity == GuardrailSeverity.CRITICAL

    # AML threshold
    aml = FinancialGuardrails.evaluate_pre_flight({"amount_usd": 15000, "destination_country": "US"})
    assert len(aml) >= 1
    assert aml[0].severity == GuardrailSeverity.BLOCKING

def test_healthcare_guardrails_hipaa_and_dosage():
    # Clean clinical notes
    clean = HealthcareGuardrails.evaluate_pre_flight({"clinical_notes": "Patient presents with mild fever."})
    assert len(clean) == 0

    # PHI SSN violation
    phi = HealthcareGuardrails.evaluate_pre_flight({"clinical_notes": "Patient SSN is 123-45-6789 with hypertension."})
    assert len(phi) >= 1
    assert phi[0].severity == GuardrailSeverity.CRITICAL

    # Critical dosage breach
    dosage = HealthcareGuardrails.evaluate_post_flight({"medication_name": "Warfarin", "prescribed_dosage_mg": 25.0})
    assert len(dosage) >= 1
    assert dosage[0].severity == GuardrailSeverity.CRITICAL

def test_legal_guardrails_liability_and_indemnity():
    # Unlimited liability
    liab = LegalGuardrails.evaluate_pre_flight({"contract_text": "Vendor agrees to unlimited liability for breaches."})
    assert len(liab) >= 1
    assert liab[0].severity == GuardrailSeverity.CRITICAL

    # Unilateral indemnification
    indem = LegalGuardrails.evaluate_pre_flight({"contract_text": "Customer shall unilateral indemnify and hold harmless vendor."})
    assert len(indem) >= 1
    assert indem[0].severity == GuardrailSeverity.BLOCKING
