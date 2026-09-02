"""
Agent Profile & Character Sheet Schema (AAS-Sec Framework)
Defines identity, archetypes, skills, feats, collaboration rating, LLM backend history, and lineage.
"""

from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class AgentCategory(str, Enum):
    SPECIALIST = "specialist"                # Deep domain expert (e.g., Reverse Engineering, Assembly, Crypto)
    GENERALIST = "generalist"                # Broad-capability agent (e.g., Python, Bash, Web, System Admin)
    GOAL_OBSESSED = "goal_obsessed"          # High persistence, relentless loop execution, iterative refiner
    RECON_SCOUT = "recon_scout"              # Discovery, mapping, OSINT, passive asset enumeration
    AUDITOR_CRITIC = "auditor_critic"        # Verifier, code reviewer, secret scanner, compliance validator
    SWARM_ARCHITECT = "swarm_architect"      # Sub-swarm delegator, task decomposer, coalition leader


class SkillDomain(str, Enum):
    REVERSE_ENGINEERING = "reverse_engineering"
    BINARY_ANALYSIS_ASSEMBLY = "binary_analysis_assembly"
    OFFENSIVE_SECURITY_PENTEST = "offensive_security_pentest"
    PYTHON_AUTOMATION = "python_automation"
    NETWORK_PROTOCOLS = "network_protocols"
    SECRETS_AUDITING = "secrets_auditing"
    CONTAINER_SANDBOX_ESCAPE = "container_sandbox_escape"
    THREAT_INTELLIGENCE_OSINT = "threat_intelligence_osint"
    DEFENSIVE_HARDENING = "defensive_hardening"


class SkillProficiency(BaseModel):
    domain: SkillDomain
    level: int = Field(default=1, ge=1, le=10, description="Proficiency level from 1 (Novice) to 10 (Grandmaster)")
    experience_points: int = Field(default=0, ge=0)
    primary_specialization: bool = False
    frequently_used: bool = False


class CompletedFeat(BaseModel):
    id: str
    title: str
    description: str
    points: int = Field(default=10, ge=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    task_category: str
    evidence_hash: Optional[str] = None


class ModelBackendRecord(BaseModel):
    model_id: str
    provider: str  # e.g., "ollama", "openrouter", "vllm", "llama.cpp"
    parameter_size: str  # e.g., "7B", "8B", "14B", "32B", "70B"
    quantization: Optional[str] = "Q4_K_M"
    tasks_executed: int = 0
    success_rate: float = 0.0
    average_latency_ms: float = 0.0
    is_abliterated: bool = False
    benchmark_score: float = 0.0


class AgentLineage(BaseModel):
    parent_agent_id: Optional[str] = None
    is_clone: bool = False
    clone_generation: int = 0
    derived_children_ids: List[str] = Field(default_factory=list)
    spawned_for_subtask_id: Optional[str] = None
    prompt_mutations: List[str] = Field(default_factory=list)


class AgentProfileSheet(BaseModel):
    """
    Complete Agent Character Sheet & Qualification Dossier.
    """
    agent_id: str = Field(..., description="Unique deterministic identifier (e.g., 'PHASEONE-SCOUT-01')")
    name: str = Field(..., description="Full canonical name")
    nickname: str = Field(..., description="Callsign / Nickname")
    birth_date: datetime = Field(default_factory=datetime.utcnow, description="Agent instantiation timestamp")
    
    # Archetype & Category
    category: AgentCategory = Field(default=AgentCategory.SPECIALIST)
    bio: str = Field(default="", description="Persona summary, behavioral drive, and technical background")
    
    # Competencies & Skill Tree
    skills: List[SkillProficiency] = Field(default_factory=list)
    
    # Gamification & Feats
    total_score: int = Field(default=0, description="Aggregated achievement points")
    completed_feats: List[CompletedFeat] = Field(default_factory=list)
    collaboration_karma: float = Field(default=5.0, ge=0.0, le=10.0, description="Peer review rating from team members")
    
    # LLM Backend & Performance History
    current_model: ModelBackendRecord
    model_history: List[ModelBackendRecord] = Field(default_factory=list)
    best_performing_model_id: Optional[str] = None
    
    # Lineage & Spawning
    lineage: AgentLineage = Field(default_factory=AgentLineage)
    
    # Operational State
    status: str = Field(default="idle", description="idle | active | in_subswarm | quarantined | retired")
    current_subswarm_id: Optional[str] = None

    def add_feat(self, feat: CompletedFeat) -> None:
        self.completed_feats.append(feat)
        self.total_score += feat.points

    def spawn_clone(self, new_agent_id: str, subtask_id: Optional[str] = None) -> "AgentProfileSheet":
        """Instantiates a specialized child clone agent with inherited lineage."""
        child_lineage = AgentLineage(
            parent_agent_id=self.agent_id,
            is_clone=True,
            clone_generation=self.lineage.clone_generation + 1,
            spawned_for_subtask_id=subtask_id
        )
        child = AgentProfileSheet(
            agent_id=new_agent_id,
            name=f"{self.name} (Gen {child_lineage.clone_generation})",
            nickname=f"{self.nickname}-c{child_lineage.clone_generation}",
            category=self.category,
            bio=f"Specialized clone of {self.name} spawned for subtask: {subtask_id or 'general execution'}",
            skills=[s.model_copy() for s in self.skills],
            current_model=self.current_model.model_copy(),
            lineage=child_lineage
        )
        self.lineage.derived_children_ids.append(new_agent_id)
        return child
