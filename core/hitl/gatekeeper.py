"""
Human-in-the-Loop (HITL) Policy & Safety Gatekeeper
Implements approval boundaries for high-risk actions (network egress, privilege escalation, destructive ops).
"""

from typing import Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class RiskLevel(str, Enum):
    SAFE = "safe"              # Read-only, local parsing, syntax check
    MODERATE = "moderate"      # Non-destructive test script, build compile
    HIGH = "high"              # Network connection, packet injection, port scan
    CRITICAL = "critical"      # Code execution in container, privilege alteration, file deletion


class ApprovalRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: f"hitl-{uuid.uuid4().hex[:8]}")
    agent_id: str
    action_type: str
    target_resource: str
    risk_level: RiskLevel
    justification: str
    command_payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    approved: Optional[bool] = None
    approver_identity: Optional[str] = None
    decision_timestamp: Optional[datetime] = None


class HITLGatekeeper:
    """Enforces human-in-the-loop validation for agent actions exceeding safe risk levels."""
    def __init__(self, auto_approve_moderate: bool = False):
        self.auto_approve_moderate = auto_approve_moderate
        self.pending_requests: Dict[str, ApprovalRequest] = {}
        self.history: Dict[str, ApprovalRequest] = {}

    def assess_risk(self, action_type: str, payload: Dict[str, Any]) -> RiskLevel:
        action_lower = action_type.lower()
        if any(w in action_lower for w in ["delete", "rm", "drop", "purge", "format", "hostpath", "privilege"]):
            return RiskLevel.CRITICAL
        if any(w in action_lower for w in ["exploit", "egress", "network", "scan", "socket", "http_post"]):
            return RiskLevel.HIGH
        if any(w in action_lower for w in ["write_file", "compile", "exec_test"]):
            return RiskLevel.MODERATE
        return RiskLevel.SAFE

    def submit_request(self, agent_id: str, action_type: str, target: str, justification: str, payload: Dict[str, Any]) -> ApprovalRequest:
        risk = self.assess_risk(action_type, payload)
        req = ApprovalRequest(
            agent_id=agent_id,
            action_type=action_type,
            target_resource=target,
            risk_level=risk,
            justification=justification,
            command_payload=payload
        )
        
        if risk == RiskLevel.SAFE or (risk == RiskLevel.MODERATE and self.auto_approve_moderate):
            req.approved = True
            req.approver_identity = "system-policy-auto"
            req.decision_timestamp = datetime.utcnow()
            self.history[req.request_id] = req
        else:
            self.pending_requests[req.request_id] = req
            
        return req

    def decide(self, request_id: str, approve: bool, approver: str) -> Optional[ApprovalRequest]:
        req = self.pending_requests.pop(request_id, None)
        if req:
            req.approved = approve
            req.approver_identity = approver
            req.decision_timestamp = datetime.utcnow()
            self.history[req.request_id] = req
            return req
        return None
