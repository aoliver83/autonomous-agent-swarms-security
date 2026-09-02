import unittest
from pathlib import Path
import sys
import tempfile

base_dir = Path(__file__).resolve().parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from core.agents.schema import (
    AgentProfileSheet, AgentCategory, SkillDomain, SkillProficiency,
    ModelBackendRecord, CompletedFeat
)
from core.agents.hall_of_fame import HallOfFameRegistry
from core.orchestration.architect import SwarmArchitect
from core.bus.kanban import TaskStatus, TaskPriority
from core.hitl.gatekeeper import HITLGatekeeper, RiskLevel


class TestSwarmCore(unittest.TestCase):

    def test_agent_schema_and_cloning(self):
        agent = AgentProfileSheet(
            agent_id="TEST-AGENT-01",
            name="Alpha Unit",
            nickname="Alpha",
            category=AgentCategory.SPECIALIST,
            skills=[
                SkillProficiency(domain=SkillDomain.PYTHON_AUTOMATION, level=8, primary_specialization=True)
            ],
            current_model=ModelBackendRecord(
                model_id="qwen2.5-coder:7b",
                provider="ollama",
                parameter_size="7B"
            )
        )
        
        self.assertEqual(agent.total_score, 0)
        agent.add_feat(CompletedFeat(id="f1", title="First Mission", description="Success", points=50, task_category="test"))
        self.assertEqual(agent.total_score, 50)
        
        # Test clone derivation
        clone = agent.spawn_clone("TEST-CLONE-01", subtask_id="subtask-xyz")
        self.assertTrue(clone.lineage.is_clone)
        self.assertEqual(clone.lineage.clone_generation, 1)
        self.assertEqual(clone.lineage.parent_agent_id, "TEST-AGENT-01")
        self.assertIn("TEST-CLONE-01", agent.lineage.derived_children_ids)

    def test_swarm_orchestration_and_task_board(self):
        tmp_dir = Path(tempfile.mkdtemp())
        hof = HallOfFameRegistry(tmp_dir / "hof")
        architect = SwarmArchitect(hof)
        
        agent = AgentProfileSheet(
            agent_id="LEAD-01",
            name="Lead Orchestrator",
            nickname="Lead",
            category=AgentCategory.SWARM_ARCHITECT,
            current_model=ModelBackendRecord(
                model_id="llama3.3:8b",
                provider="ollama",
                parameter_size="8B"
            )
        )
        architect.register_agent(agent)
        
        # Create Sub-Swarm
        subswarm = architect.create_subswarm(
            name="Reconnaissance Strike",
            goal="Discover exposed subdomains",
            lead_agent_id="LEAD-01",
            domain=SkillDomain.THREAT_INTELLIGENCE_OSINT
        )
        self.assertIn(subswarm.subswarm_id, architect.coalitions)
        self.assertIn("LEAD-01", subswarm.member_agent_ids)
        
        # Delegate Tasks
        tasks = architect.delegate_mission("Audit Scope", [
            {"title": "DNS Scan", "description": "Run subfinder", "category": "recon", "priority": TaskPriority.HIGH}
        ])
        self.assertEqual(len(tasks), 1)
        task_id = tasks[0].task_id
        
        # Assign and complete task
        architect.board.assign_task(task_id, agent_id="LEAD-01", subswarm_id=subswarm.subswarm_id)
        self.assertEqual(architect.board.tasks[task_id].status, TaskStatus.IN_PROGRESS)
        
        architect.board.update_status(task_id, TaskStatus.COMPLETED, audit_note="Verified clean output")
        self.assertEqual(architect.board.tasks[task_id].status, TaskStatus.COMPLETED)

    def test_hitl_gatekeeper(self):
        gatekeeper = HITLGatekeeper(auto_approve_moderate=False)
        
        # Safe action
        req_safe = gatekeeper.submit_request(
            agent_id="A1", action_type="read_file", target="/tmp/test.txt", justification="Inspecting", payload={}
        )
        self.assertTrue(req_safe.approved)
        
        # High risk action (egress)
        req_high = gatekeeper.submit_request(
            agent_id="A1", action_type="network_exploit", target="192.168.1.1", justification="Port probing", payload={"port": 80}
        )
        self.assertIsNone(req_high.approved)
        self.assertEqual(req_high.risk_level, RiskLevel.HIGH)
        
        # Human approves
        decided = gatekeeper.decide(req_high.request_id, approve=True, approver="SecurityOperator")
        self.assertIsNotNone(decided)
        if decided:
            self.assertTrue(decided.approved)
            self.assertEqual(decided.approver_identity, "SecurityOperator")


if __name__ == "__main__":
    unittest.main()

