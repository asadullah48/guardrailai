from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time

class WorkflowDomain(str, Enum):
    FINANCIAL = "FINANCIAL"
    HEALTHCARE = "HEALTHCARE"
    LEGAL = "LEGAL"
    GENERAL = "GENERAL"

class WorkflowStatus(str, Enum):
    INITIALIZED = "INITIALIZED"
    PRE_GUARDRAIL_EVALUATING = "PRE_GUARDRAIL_EVALUATING"
    PROCESSING = "PROCESSING"
    POST_GUARDRAIL_EVALUATING = "POST_GUARDRAIL_EVALUATING"
    AUDITING = "AUDITING"
    COMPLETED = "COMPLETED"
    CIRCUIT_BREAKER_TRIGGERED = "CIRCUIT_BREAKER_TRIGGERED"
    FALLBACK_EXECUTED = "FALLBACK_EXECUTED"

class GuardrailSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    BLOCKING = "BLOCKING"
    CRITICAL = "CRITICAL"

class GuardrailViolation(BaseModel):
    rule_id: str
    domain: WorkflowDomain
    severity: GuardrailSeverity
    description: str
    remediation_action: str
    timestamp: float = Field(default_factory=time.time)

class FallbackPolicy(str, Enum):
    SAFE_DEFAULT = "SAFE_DEFAULT"
    HUMAN_ESCALATION = "HUMAN_ESCALATION"
    REDACTION = "REDACTION"
    REJECT_WITH_REASON = "REJECT_WITH_REASON"

class AuditBlock(BaseModel):
    block_index: int
    workflow_id: str
    step_name: str
    agent_name: str
    input_hash: str
    output_hash: str
    previous_block_hash: str
    current_block_hash: str
    timestamp: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class WorkflowExecutionRequest(BaseModel):
    workflow_id: str = "wf-tx-001"
    domain: WorkflowDomain = WorkflowDomain.FINANCIAL
    task_intent: str = "TRANSFER_FUNDS"
    payload: Dict[str, Any] = Field(default_factory=dict)
    fallback_policy: FallbackPolicy = FallbackPolicy.SAFE_DEFAULT

class WorkflowExecutionResponse(BaseModel):
    workflow_id: str
    domain: WorkflowDomain
    final_status: WorkflowStatus
    violations_detected: List[GuardrailViolation]
    circuit_breaker_active: bool
    fallback_applied: bool
    result_data: Dict[str, Any]
    audit_chain_length: int
    tamper_evident_certificate: str
