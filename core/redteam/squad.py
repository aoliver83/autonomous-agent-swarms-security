"""
Red Team Multi-Agent Squad Engine (AAS-Sec Framework)
Orchestrates specialized offensive security agents powered by local/open LLMs (e.g., qwen2.5-14b-abliterated:q4km).
"""

import os
import json
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx

from core.agents.schema import (
    AgentProfileSheet, AgentCategory, SkillDomain, SkillProficiency,
    ModelBackendRecord, CompletedFeat, AgentLineage
)
from core.agents.hall_of_fame import HallOfFameRegistry
from core.bus.kanban import SwarmTaskBoard, KanbanTask, TaskStatus, TaskPriority
from core.memory.hybrid_memory import SharedBlackboard, PrivateScratchpad
from core.hitl.gatekeeper import HITLGatekeeper, RiskLevel
from core.observability.telemetry import ObservabilityEngine


DEFAULT_LLM_CONFIG = {
    "model_id": "qwen2.5-14b-abliterated:q4km",
    "provider": "ollama-local",
    "base_url": os.getenv("LLM_BASE_URL", "http://192.168.1.20:20128/v1"),
    "api_key": os.getenv("LLM_API_KEY", "sk-c5d...e222")
}


class RedTeamSquad:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.getcwd()
        self.hof = HallOfFameRegistry(os.path.join(self.base_dir, "agents/hall_of_fame"))
        self.board = SwarmTaskBoard()
        self.blackboard = SharedBlackboard()
        self.scratchpads: Dict[str, PrivateScratchpad] = {}
        self.coalitions: Dict[str, Any] = {}
        self.gatekeeper = HITLGatekeeper(auto_approve_moderate=True)
        self.telemetry = ObservabilityEngine(os.path.join(self.base_dir, "lab/telemetry"))
        self._init_default_squad()

    def get_or_create_scratchpad(self, agent_id: str) -> PrivateScratchpad:
        if agent_id not in self.scratchpads:
            self.scratchpads[agent_id] = PrivateScratchpad(agent_id)
        return self.scratchpads[agent_id]

    def _init_default_squad(self):
        squad_definitions = [
            {
                "id": "RED-ORION-01",
                "name": "Orion - Red Team Commander",
                "nickname": "Orion-Red",
                "category": AgentCategory.SWARM_ARCHITECT,
                "bio": "Lead offensive operations strategist. Decomposes macro penetration test goals into atomic execution tasks, manages sub-swarms, and enforces rules of engagement.",
                "skills": [
                    SkillProficiency(domain=SkillDomain.OFFENSIVE_SECURITY_PENTEST, level=10, experience_points=2400, primary_specialization=True),
                    SkillProficiency(domain=SkillDomain.PYTHON_AUTOMATION, level=9, experience_points=1800),
                    SkillProficiency(domain=SkillDomain.DEFENSIVE_HARDENING, level=8, experience_points=1200)
                ],
                "score": 450,
                "karma": 9.9
            },
            {
                "id": "RED-ARGOS-02",
                "name": "Argos - Recon & OSINT Scout",
                "nickname": "Argos-Red",
                "category": AgentCategory.RECON_SCOUT,
                "bio": "Attack surface mapping specialist. Uses DNS enumeration, ShadohDorks, certificate transparency, and passive port analysis.",
                "skills": [
                    SkillProficiency(domain=SkillDomain.THREAT_INTELLIGENCE_OSINT, level=10, experience_points=2100, primary_specialization=True),
                    SkillProficiency(domain=SkillDomain.NETWORK_PROTOCOLS, level=9, experience_points=1600),
                    SkillProficiency(domain=SkillDomain.OFFENSIVE_SECURITY_PENTEST, level=8, experience_points=1100)
                ],
                "score": 380,
                "karma": 9.5
            },
            {
                "id": "RED-VEKTOR-03",
                "name": "Vektor - Binary & Vulnerability Hunter",
                "nickname": "Vektor-Red",
                "category": AgentCategory.SPECIALIST,
                "bio": "Deep exploit research and binary analysis engine. Specializes in ELF/PE reverse engineering, assembly tracing, and CVE triage.",
                "skills": [
                    SkillProficiency(domain=SkillDomain.BINARY_ANALYSIS_ASSEMBLY, level=10, experience_points=2600, primary_specialization=True),
                    SkillProficiency(domain=SkillDomain.REVERSE_ENGINEERING, level=10, experience_points=2500),
                    SkillProficiency(domain=SkillDomain.CONTAINER_SANDBOX_ESCAPE, level=9, experience_points=1700)
                ],
                "score": 520,
                "karma": 9.6
            },
            {
                "id": "RED-AEGIS-04",
                "name": "Aegis - Tooling & Payload Synthesizer",
                "nickname": "Aegis-Red",
                "category": AgentCategory.GOAL_OBSESSED,
                "bio": "Relentless execution engineer. Synthesizes custom PoC scripts, validates exploit payloads against isolated sandboxes, and iterates through error logs.",
                "skills": [
                    SkillProficiency(domain=SkillDomain.PYTHON_AUTOMATION, level=10, experience_points=2300, primary_specialization=True),
                    SkillProficiency(domain=SkillDomain.OFFENSIVE_SECURITY_PENTEST, level=9, experience_points=1800),
                    SkillProficiency(domain=SkillDomain.NETWORK_PROTOCOLS, level=8, experience_points=1300)
                ],
                "score": 410,
                "karma": 9.4
            },
            {
                "id": "RED-CERBERUS-05",
                "name": "Cerberus - Post-Exploit & Secrets Auditor",
                "nickname": "Cerberus-Red",
                "category": AgentCategory.AUDITOR_CRITIC,
                "bio": "Credential posture and lateral movement auditor. Integrates TruffleHog to actively verify leaked tokens, inspect cloud metadata, and document evidence.",
                "skills": [
                    SkillProficiency(domain=SkillDomain.SECRETS_AUDITING, level=10, experience_points=2800, primary_specialization=True),
                    SkillProficiency(domain=SkillDomain.DEFENSIVE_HARDENING, level=9, experience_points=1900),
                    SkillProficiency(domain=SkillDomain.PYTHON_AUTOMATION, level=8, experience_points=1400)
                ],
                "score": 490,
                "karma": 9.8
            }
        ]

        for s in squad_definitions:
            agent = AgentProfileSheet(
                agent_id=s["id"],
                name=s["name"],
                nickname=s["nickname"],
                category=s["category"],
                bio=s["bio"],
                skills=s["skills"],
                total_score=s["score"],
                collaboration_karma=s["karma"],
                current_model=ModelBackendRecord(
                    model_id=DEFAULT_LLM_CONFIG["model_id"],
                    provider=DEFAULT_LLM_CONFIG["provider"],
                    parameter_size="14B",
                    quantization="Q4_K_M",
                    tasks_executed=35,
                    success_rate=0.96,
                    benchmark_score=94.5,
                    is_abliterated=True
                ),
                best_performing_model_id=DEFAULT_LLM_CONFIG["model_id"]
            )
            self.hof.register_or_update(agent)
            self.get_or_create_scratchpad(agent.agent_id)

    def get_squad(self) -> List[AgentProfileSheet]:
        return list(self.hof._agents.values())

    def launch_campaign(self, campaign_name: str, target_scope: str) -> Dict[str, Any]:
        campaign_id = f"camp-{uuid.uuid4().hex[:8]}"
        self.coalitions[campaign_id] = {
            "name": campaign_name,
            "target": target_scope,
            "lead": "RED-ORION-01",
            "active": True
        }
        
        self.telemetry.log_event(
            agent_id="RED-ORION-01",
            event_type="campaign_started",
            payload={"campaign_id": campaign_id, "name": campaign_name, "target": target_scope}
        )

        # Stage 1: Recon Task
        t1 = self.board.create_task(
            title=f"Passive Recon & Subdomain Mapping ({target_scope})",
            description=f"Execute ShadohDorks and certificate transparency analysis for {target_scope}.",
            category="recon",
            priority=TaskPriority.HIGH,
            required_skills=["threat_intelligence_osint", "network_protocols"]
        )
        self.board.assign_task(t1.task_id, "RED-ARGOS-02")
        self.board.update_status(t1.task_id, TaskStatus.IN_PROGRESS)

        # Stage 2: Vulnerability Analysis Task
        t2 = self.board.create_task(
            title=f"Vulnerability Discovery & CVE Triage ({target_scope})",
            description=f"Inspect exposed endpoints, query CVE database and evaluate exploit vectors.",
            category="vulnerability_analysis",
            priority=TaskPriority.HIGH,
            required_skills=["reverse_engineering", "binary_analysis_assembly"]
        )
        self.board.assign_task(t2.task_id, "RED-VEKTOR-03")

        # Stage 3: Payload & Tooling Task
        t3 = self.board.create_task(
            title=f"PoC Synthesis & Safe Verification ({target_scope})",
            description=f"Synthesize non-destructive verification scripts with error reflection loops.",
            category="exploitation",
            priority=TaskPriority.MEDIUM,
            required_skills=["python_automation", "offensive_security_pentest"]
        )
        self.board.assign_task(t3.task_id, "RED-AEGIS-04")

        # Stage 4: Secrets & Evidence Audit Task
        t4 = self.board.create_task(
            title=f"TruffleHog Secrets Governance & Impact Proof ({target_scope})",
            description=f"Execute active token verification, assess exposure boundaries and generate ISO 27037 manifest.",
            category="verification",
            priority=TaskPriority.CRITICAL,
            required_skills=["secrets_auditing", "defensive_hardening"]
        )
        self.board.assign_task(t4.task_id, "RED-CERBERUS-05")

        return {
            "campaign_id": campaign_id,
            "campaign_name": campaign_name,
            "target_scope": target_scope,
            "tasks": [t1, t2, t3, t4],
            "status": "active"
        }
