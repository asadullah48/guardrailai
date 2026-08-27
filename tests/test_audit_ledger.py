import pytest
from guardrailai.core.audit_ledger import AuditLedger

def test_audit_ledger_genesis_and_append():
    ledger = AuditLedger("wf-test-001")
    assert len(ledger.blocks) == 1
    assert ledger.blocks[0].step_name == "GENESIS"
    assert ledger.verify_integrity() is True

    # Append block 1
    b1 = ledger.append_entry("STEP_1", "ProcessAgent", {"input": "a"}, {"output": "b"})
    assert b1.block_index == 1
    assert b1.previous_block_hash == ledger.blocks[0].current_block_hash
    assert ledger.verify_integrity() is True

    # Append block 2
    b2 = ledger.append_entry("STEP_2", "ComplianceAgent", {"check": True}, {"passed": True})
    assert b2.block_index == 2
    assert ledger.verify_integrity() is True

def test_audit_ledger_tamper_detection():
    ledger = AuditLedger("wf-test-002")
    ledger.append_entry("STEP_1", "ProcessAgent", {"amount": 100}, {"status": "OK"})
    ledger.append_entry("STEP_2", "AuditAgent", {"verify": True}, {"certified": True})
    assert ledger.verify_integrity() is True

    # Tamper with block 1 output hash
    ledger.blocks[1].output_hash = "f" * 64
    assert ledger.verify_integrity() is False

def test_audit_certificate_generation():
    ledger = AuditLedger("wf-test-003")
    ledger.append_entry("EXEC", "ProcessAgent", {}, {})
    cert = ledger.generate_certificate()
    assert "AUDIT-SEAL" in cert
    assert "VERIFIED-True" in cert
