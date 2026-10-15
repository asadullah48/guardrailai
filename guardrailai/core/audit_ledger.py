from copy import deepcopy
import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from guardrailai.core.models import AuditBlock

class AuditLedger:
    """
    Tamper-evident, in-memory SHA-256 hash chain.
    Every stored field except current_block_hash contributes to the digest.
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
            current_block_hash="",
            timestamp=time.time(),
            metadata={"status": "INITIALIZED"}
        )
        genesis.current_block_hash = self._hash_block(genesis)
        self.blocks.append(genesis)

    @staticmethod
    def _hash_string(data_str: str) -> str:
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

    def append_entry(self, step_name: str, agent_name: str, input_data: Any, output_data: Any, metadata: Optional[Dict[str, Any]] = None) -> AuditBlock:
        prev_block = self.blocks[-1]
        input_h = self._hash_string(json.dumps(input_data, sort_keys=True, default=str))
        output_h = self._hash_string(json.dumps(output_data, sort_keys=True, default=str))
        
        block = AuditBlock(
            block_index=len(self.blocks),
            workflow_id=self.workflow_id,
            step_name=step_name,
            agent_name=agent_name,
            input_hash=input_h,
            output_hash=output_h,
            previous_block_hash=prev_block.current_block_hash,
            current_block_hash="",
            timestamp=time.time(),
            metadata=deepcopy(metadata) if metadata is not None else {}
        )
        block.current_block_hash = self._hash_block(block)
        self.blocks.append(block)
        return block

    @classmethod
    def _hash_block(cls, block: AuditBlock) -> str:
        payload = block.model_dump(exclude={"current_block_hash"})
        return cls._hash_string(json.dumps(payload, sort_keys=True, default=str))

    def verify_integrity(self) -> bool:
        """Check every block, its workflow identity, position and previous link."""
        if not self.blocks:
            return False
        previous_hash = "0" * 64
        for index, block in enumerate(self.blocks):
            if block.block_index != index or block.workflow_id != self.workflow_id:
                return False
            if block.previous_block_hash != previous_hash:
                return False
            if self._hash_block(block) != block.current_block_hash:
                return False
            previous_hash = block.current_block_hash
        return True

    def generate_certificate(self) -> str:
        is_valid = self.verify_integrity()
        latest_hash = self.blocks[-1].current_block_hash if self.blocks else "0" * 64
        return f"AUDIT-SEAL-{self.workflow_id[:8].upper()}-{latest_hash[:16].upper()}-VERIFIED-{is_valid}"
