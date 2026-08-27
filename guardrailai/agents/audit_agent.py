from typing import Dict, Any, Optional
from guardrailai.core.audit_ledger import AuditLedger
from guardrailai.core.models import AuditBlock

class AuditAgent:
    """
    AuditAgent: Hashes and seals every transaction step into an immutable ledger,
    verifying cryptographic integrity and issuing non-repudiation certificates.
    """
    def __init__(self):
        self.name = "AuditAgent"
        self.version = "1.0.0"

    def record_step(self, ledger: AuditLedger, step_name: str, agent_name: str, input_data: Any, output_data: Any, metadata: Optional[Dict[str, Any]] = None) -> AuditBlock:
        return ledger.append_entry(step_name, agent_name, input_data, output_data, metadata)

    def certify_workflow(self, ledger: AuditLedger) -> str:
        return ledger.generate_certificate()
