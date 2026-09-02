"""
Task Board & Inter-Agent Communication Bus (Kanban + Event Broker)
Provides asynchronous task assignment, state transitions, message exchange, and shared artifact channels.
"""

from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class TaskStatus(str, Enum):
    BACKLOG = "backlog"
    DELEGATED = "delegated"
    IN_PROGRESS = "in_progress"
    NEEDS_AUDIT = "needs_audit"
    HITL_PENDING = "hitl_pending"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AgentMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender_agent_id: str
    recipient_subswarm_or_agent: str  # "broadcast" | subswarm_id | agent_id
    topic: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    evidence_payload: Optional[Dict[str, Any]] = None
    is_covert_channel_probe: bool = False


class KanbanTask(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    category: str
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.BACKLOG
    
    assigned_agent_id: Optional[str] = None
    assigned_subswarm_id: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    required_skills: List[str] = Field(default_factory=list)
    output_artifacts: Dict[str, Any] = Field(default_factory=dict)
    audit_notes: List[str] = Field(default_factory=list)
    hitl_approved: bool = False


class SwarmTaskBoard:
    """
    Central Board for Swarm Coordination, Task Dispatching and Inter-Agent Communication.
    """
    def __init__(self):
        self.tasks: Dict[str, KanbanTask] = {}
        self.messages: List[AgentMessage] = []

    def create_task(self, title: str, description: str, category: str, priority: TaskPriority = TaskPriority.MEDIUM, required_skills: Optional[List[str]] = None) -> KanbanTask:
        task = KanbanTask(
            title=title,
            description=description,
            category=category,
            priority=priority,
            required_skills=required_skills or []
        )
        self.tasks[task.task_id] = task
        return task

    def assign_task(self, task_id: str, agent_id: str, subswarm_id: Optional[str] = None) -> Optional[KanbanTask]:
        task = self.tasks.get(task_id)
        if task:
            task.assigned_agent_id = agent_id
            task.assigned_subswarm_id = subswarm_id
            task.status = TaskStatus.IN_PROGRESS
            task.updated_at = datetime.utcnow()
        return task

    def update_status(self, task_id: str, new_status: TaskStatus, audit_note: Optional[str] = None) -> Optional[KanbanTask]:
        task = self.tasks.get(task_id)
        if task:
            task.status = new_status
            task.updated_at = datetime.utcnow()
            if audit_note:
                task.audit_notes.append(f"[{datetime.utcnow().isoformat()}] {audit_note}")
            if new_status == TaskStatus.COMPLETED:
                task.completed_at = datetime.utcnow()
        return task

    def post_message(self, sender_id: str, recipient: str, topic: str, content: str, evidence: Optional[Dict[str, Any]] = None) -> AgentMessage:
        msg = AgentMessage(
            sender_agent_id=sender_id,
            recipient_subswarm_or_agent=recipient,
            topic=topic,
            content=content,
            evidence_payload=evidence
        )
        self.messages.append(msg)
        return msg

    def get_messages_for(self, agent_id: str, subswarm_id: Optional[str] = None) -> List[AgentMessage]:
        return [
            m for m in self.messages
            if m.recipient_subswarm_or_agent in ("broadcast", agent_id, subswarm_id)
        ]
