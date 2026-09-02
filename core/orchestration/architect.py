"""
Master Swarm Orchestrator & Dynamic Coalition Engine (AAS-Sec)
Coordinates high-level mission goals, sub-swarm formation, agent lineage/cloning, and task board synchronization.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
import uuid

from core.agents.schema import AgentProfileSheet, AgentCategory, SkillDomain, SkillProficiency, ModelBackendRecord, CompletedFeat
from core.agents.hall_of_fame import HallOfFameRegistry
from core.bus.kanban import SwarmTaskBoard, KanbanTask, TaskStatus, TaskPriority
from core.memory.hybrid_memory import SharedBlackboard, PrivateScratchpad


class SubSwarmCoalition(BaseModel):
    subswarm_id: str = Field(default_factory=lambda: f"subswarm-{uuid.uuid4().hex[:8]}")
    name: str
    goal: str
    lead_agent_id: str
    member_agent_ids: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    active: bool = True
    specialization_domain: SkillDomain


class SwarmArchitect:
    """
    Master Orchestrator / Swarm Architect.
    Enables smaller and open models to accomplish frontier-level goals via specialization and dynamic coalitions.
    """
    def __init__(self, hall_of_fame: HallOfFameRegistry):
        self.hof = hall_of_fame
        self.board = SwarmTaskBoard()
        self.blackboard = SharedBlackboard()
        self.scratchpads: Dict[str, PrivateScratchpad] = {}
        self.coalitions: Dict[str, SubSwarmCoalition] = {}

    def get_or_create_scratchpad(self, agent_id: str) -> PrivateScratchpad:
        if agent_id not in self.scratchpads:
            self.scratchpads[agent_id] = PrivateScratchpad(agent_id)
        return self.scratchpads[agent_id]

    def register_agent(self, agent: AgentProfileSheet) -> None:
        self.hof.register_or_update(agent)
        self.get_or_create_scratchpad(agent.agent_id)

    def create_subswarm(self, name: str, goal: str, lead_agent_id: str, domain: SkillDomain) -> SubSwarmCoalition:
        """Dynamically instantiates a specialized sub-swarm coalition."""
        coalition = SubSwarmCoalition(
            name=name,
            goal=goal,
            lead_agent_id=lead_agent_id,
            member_agent_ids=[lead_agent_id],
            specialization_domain=domain
        )
        self.coalitions[coalition.subswarm_id] = coalition
        
        # Update lead agent status
        agent = self.hof.get_agent(lead_agent_id)
        if agent:
            agent.status = "in_subswarm"
            agent.current_subswarm_id = coalition.subswarm_id
            self.hof.register_or_update(agent)
            
        return coalition

    def join_subswarm(self, subswarm_id: str, agent_id: str) -> bool:
        coalition = self.coalitions.get(subswarm_id)
        if coalition and agent_id not in coalition.member_agent_ids:
            coalition.member_agent_ids.append(agent_id)
            agent = self.hof.get_agent(agent_id)
            if agent:
                agent.status = "in_subswarm"
                agent.current_subswarm_id = subswarm_id
                self.hof.register_or_update(agent)
            return True
        return False

    def delegate_mission(self, mission_title: str, subtasks_specs: List[Dict[str, Any]]) -> List[KanbanTask]:
        """Decomposes a macro-mission into atomic board tasks matching agent skills."""
        created_tasks = []
        for spec in subtasks_specs:
            task = self.board.create_task(
                title=spec.get("title", "Untitled Subtask"),
                description=spec.get("description", ""),
                category=spec.get("category", "general"),
                priority=spec.get("priority", TaskPriority.MEDIUM),
                required_skills=spec.get("required_skills", [])
            )
            created_tasks.append(task)
        return created_tasks

    def record_achievement(self, agent_id: str, feat_title: str, description: str, points: int, category: str) -> None:
        agent = self.hof.get_agent(agent_id)
        if agent:
            feat = CompletedFeat(
                id=f"feat-{uuid.uuid4().hex[:6]}",
                title=feat_title,
                description=description,
                points=points,
                task_category=category
            )
            agent.add_feat(feat)
            self.hof.register_or_update(agent)
