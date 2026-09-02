"""
Telemetry & Audit Trail Logger (AAS-Sec Observability Engine)
Captures execution traces, tool calls, stdout fingerprints, and eBPF-style behavioral metrics.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import json
from pathlib import Path


class TraceEvent(BaseModel):
    event_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_id: str
    subswarm_id: Optional[str] = None
    event_type: str  # "tool_call" | "message_sent" | "state_change" | "hitl_request" | "security_alert"
    payload: Dict[str, Any] = Field(default_factory=dict)
    stdout_hash: Optional[str] = None
    execution_duration_ms: Optional[float] = None
    anomaly_flag: bool = False


class ObservabilityEngine:
    def __init__(self, log_dir: Path):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.trace_file = self.log_dir / "swarm_telemetry.jsonl"
        self._events: List[TraceEvent] = []

    def log_event(self, agent_id: str, event_type: str, payload: Dict[str, Any], subswarm_id: Optional[str] = None, duration_ms: Optional[float] = None, anomaly: bool = False) -> TraceEvent:
        event = TraceEvent(
            event_id=f"evt-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
            agent_id=agent_id,
            subswarm_id=subswarm_id,
            event_type=event_type,
            payload=payload,
            execution_duration_ms=duration_ms,
            anomaly_flag=anomaly
        )
        self._events.append(event)
        
        # Append to JSONL stream
        with open(self.trace_file, "a", encoding="utf-8") as f:
            f.write(event.model_dump_json() + "\n")
            
        return event

    def query_traces_by_agent(self, agent_id: str) -> List[TraceEvent]:
        return [e for e in self._events if e.agent_id == agent_id]

    def get_anomalies(self) -> List[TraceEvent]:
        return [e for e in self._events if e.anomaly_flag]
