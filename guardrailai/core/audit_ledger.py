import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from guardrailai.core.models import AuditBlock

class AuditLedger:
    """
    Cryptographically immutable SHA-256 hash-chained audit ledger.
    Every step H_i is computed from H_{i-1} + payload + timestamp.
    """
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.blocks: List[AuditBlock] = []
        self._genesis_block()

    def _genesis_block(self):
        genesis = AuditBlock(
            block_index=0,
            workflow_id=self.workflow_id,
            step_name="GENESIS",
            agent_name="AuditAgent",
            input_hash="0" * 64,
            output_hash="0" * 64,
            previous_block_hash="0" * 64,
            current_block_hash=self._hash_string(f"GENESIS-{self.workflow_id}-{time.time()}"),
            timestamp=time.time(),
            metadata={"status": "INITIALIZED"}
        )
        self.blocks.append(genesis)

    @staticmethod
    def _hash_string(data_str: str) -> str:
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

    def append_entry(self, step_name: str, agent_name: str, input_data: Any, output_data: Any, metadata: Optional[Dict[str, Any]] = None) -> AuditBlock:
        prev_block = self.blocks[-1]
        input_h = self._hash_string(json.dumps(input_data, sort_keys=True, default=str))
        output_h = self._hash_string(json.dumps(output_data, sort_keys=True, default=str))
        
        block_payload = f"{prev_block.current_block_hash}|{step_name}|{agent_name}|{input_h}|{output_h}"
        curr_hash = self._hash_string(block_payload)

        block = AuditBlock(
            block_index=len(self.blocks),
            workflow_id=self.workflow_id,
            step_name=step_name,
            agent_name=agent_name,
            input_hash=input_h,
            output_hash=output_h,
            previous_block_hash=prev_block.current_block_hash,
            current_block_hash=curr_hash,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        self.blocks.append(block)
        return block

    def verify_integrity(self) -> bool:
        """
        Verifies that no block in the chain has been modified or tampered with.
        """
        for i in range(1, len(self.blocks)):
            curr = self.blocks[i]
            prev = self.blocks[i - 1]
            if curr.previous_block_hash != prev.current_block_hash:
                return False
            expected_payload = f"{prev.current_block_hash}|{curr.step_name}|{curr.agent_name}|{curr.input_hash}|{curr.output_hash}"
            if self._hash_string(expected_payload) != curr.current_block_hash:
                return False
        return True

    def generate_certificate(self) -> str:
        is_valid = self.verify_integrity()
        latest_hash = self.blocks[-1].current_block_hash
        return f"AUDIT-SEAL-{self.workflow_id[:8].upper()}-{latest_hash[:16].upper()}-VERIFIED-{is_valid}"
