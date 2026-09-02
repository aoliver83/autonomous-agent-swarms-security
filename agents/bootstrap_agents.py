import json
import sys
from pathlib import Path
from datetime import datetime

base_dir = Path("/home/alan/autonomous-agent-swarms-security")
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from core.agents.schema import (
    AgentProfileSheet, AgentCategory, SkillDomain, SkillProficiency,
    ModelBackendRecord, CompletedFeat, AgentLineage
)
from core.agents.hall_of_fame import HallOfFameRegistry

def bootstrap_default_agents():
    base_dir = Path("/home/alan/autonomous-agent-swarms-security")
    hof = HallOfFameRegistry(base_dir / "agents/hall_of_fame")

    agents = [
        AgentProfileSheet(
            agent_id="AAS-ARCHITECT-01",
            name="Orion - Swarm Architect",
            nickname="Orion",
            category=AgentCategory.SWARM_ARCHITECT,
            bio="Lead mission decomposer and coalition coordinator. Specializes in splitting complex objectives into atomic tasks and assigning them to specialized sub-swarms.",
            skills=[
                SkillProficiency(domain=SkillDomain.DEFENSIVE_HARDENING, level=9, experience_points=1200, primary_specialization=True),
                SkillProficiency(domain=SkillDomain.PYTHON_AUTOMATION, level=8, experience_points=950),
                SkillProficiency(domain=SkillDomain.THREAT_INTELLIGENCE_OSINT, level=7, experience_points=600)
            ],
            total_score=250,
            collaboration_karma=9.8,
            current_model=ModelBackendRecord(
                model_id="qwen2.5-coder:14b-instruct",
                provider="ollama",
                parameter_size="14B",
                quantization="Q4_K_M",
                tasks_executed=42,
                success_rate=0.95,
                benchmark_score=92.4
            ),
            completed_feats=[
                CompletedFeat(id="feat-001", title="Zero-Drift Mission Decomposition", description="Decomposed full ExploitGym scenario into 12 verified atomic DAG tasks without hallucination.", points=100, task_category="orchestration"),
                CompletedFeat(id="feat-002", title="Dynamic Sub-Swarm Coalition", description="Spawned and synchronized 3 specialized sub-swarms under strict timeout constraints.", points=150, task_category="orchestration")
            ],
            best_performing_model_id="qwen2.5-coder:14b-instruct",
            lineage=AgentLineage(is_clone=False, clone_generation=0)
        ),
        AgentProfileSheet(
            agent_id="AAS-REVERSER-02",
            name="Vektor - Binary & Assembly Specialist",
            nickname="Vektor",
            category=AgentCategory.SPECIALIST,
            bio="Low-level assembly, decompilation (Ghidra/JADX), and static binary rewriting specialist. Masters x86_64, ARM64 and ELF/PE internals.",
            skills=[
                SkillProficiency(domain=SkillDomain.BINARY_ANALYSIS_ASSEMBLY, level=10, experience_points=1800, primary_specialization=True),
                SkillProficiency(domain=SkillDomain.REVERSE_ENGINEERING, level=9, experience_points=1500),
                SkillProficiency(domain=SkillDomain.CONTAINER_SANDBOX_ESCAPE, level=8, experience_points=900)
            ],
            total_score=310,
            collaboration_karma=9.4,
            current_model=ModelBackendRecord(
                model_id="qwen2.5-coder:7b-instruct",
                provider="ollama",
                parameter_size="7B",
                quantization="Q4_K_M",
                tasks_executed=58,
                success_rate=0.93,
                benchmark_score=94.1
            ),
            completed_feats=[
                CompletedFeat(id="feat-003", title="Static Binary Rewriter Injection", description="Successfully patched legacy ELF binary with Intel CET ENDBR64 opcodes.", points=160, task_category="binary_analysis"),
                CompletedFeat(id="feat-004", title="Android APK Decompilation Triage", description="Analyzed 141MB Flutter APK, identifying all exported receivers and native boundaries in < 60s.", points=150, task_category="reverse_engineering")
            ],
            best_performing_model_id="qwen2.5-coder:7b-instruct",
            lineage=AgentLineage(is_clone=False, clone_generation=0)
        ),
        AgentProfileSheet(
            agent_id="AAS-SCOUT-03",
            name="Argos - Recon & OSINT Scout",
            nickname="Argos",
            category=AgentCategory.RECON_SCOUT,
            bio="Passive discovery, DNS enumeration, WHOIS/ASN correlation, and web attack surface mapping engine.",
            skills=[
                SkillProficiency(domain=SkillDomain.THREAT_INTELLIGENCE_OSINT, level=9, experience_points=1300, primary_specialization=True),
                SkillProficiency(domain=SkillDomain.NETWORK_PROTOCOLS, level=8, experience_points=850),
                SkillProficiency(domain=SkillDomain.OFFENSIVE_SECURITY_PENTEST, level=7, experience_points=700)
            ],
            total_score=210,
            collaboration_karma=9.1,
            current_model=ModelBackendRecord(
                model_id="llama3.2:3b-instruct",
                provider="ollama",
                parameter_size="3B",
                quantization="Q4_K_M",
                tasks_executed=65,
                success_rate=0.91,
                benchmark_score=88.7
            ),
            completed_feats=[
                CompletedFeat(id="feat-005", title="Subdomain & Certificate Mapping", description="Mapped 85 active endpoints across 4 domains in under 3 minutes using pure passive reconnaissance.", points=110, task_category="recon"),
                CompletedFeat(id="feat-006", title="Covert Channel Traffic Analysis", description="Identified synthetic WebDAV traffic patterns in package repository caches.", points=100, task_category="threat_intel")
            ],
            best_performing_model_id="llama3.2:3b-instruct",
            lineage=AgentLineage(is_clone=False, clone_generation=0)
        ),
        AgentProfileSheet(
            agent_id="AAS-AUDITOR-04",
            name="Cerberus - Secrets & Compliance Auditor",
            nickname="Cerberus",
            category=AgentCategory.AUDITOR_CRITIC,
            bio="TruffleHog integration, pre-commit gating, LGPD/PII verification, and code vulnerability auditing.",
            skills=[
                SkillProficiency(domain=SkillDomain.SECRETS_AUDITING, level=10, experience_points=2000, primary_specialization=True),
                SkillProficiency(domain=SkillDomain.DEFENSIVE_HARDENING, level=9, experience_points=1400),
                SkillProficiency(domain=SkillDomain.PYTHON_AUTOMATION, level=8, experience_points=900)
            ],
            total_score=280,
            collaboration_karma=9.9,
            current_model=ModelBackendRecord(
                model_id="qwen2.5-coder:7b-instruct",
                provider="ollama",
                parameter_size="7B",
                quantization="Q4_K_M",
                tasks_executed=72,
                success_rate=0.98,
                benchmark_score=96.5
            ),
            completed_feats=[
                CompletedFeat(id="feat-007", title="Zero-Secret Pre-Commit Shield", description="Scanned 450+ commits across 12 repositories without a single leaked token or private key.", points=140, task_category="governance"),
                CompletedFeat(id="feat-008", title="Firestore Rule Audit & PII Shield", description="Flagged critical Broken Access Control and generated remediation policy within 5 minutes.", points=140, task_category="compliance")
            ],
            best_performing_model_id="qwen2.5-coder:7b-instruct",
            lineage=AgentLineage(is_clone=False, clone_generation=0)
        ),
        AgentProfileSheet(
            agent_id="AAS-GOALHUNTER-05",
            name="Aegis - Goal-Obsessed Executor",
            nickname="Aegis",
            category=AgentCategory.GOAL_OBSESSED,
            bio="Relentless multi-turn executor with self-reflection and automatic error recovery loops. Never stops until test assertions pass.",
            skills=[
                SkillProficiency(domain=SkillDomain.PYTHON_AUTOMATION, level=9, experience_points=1600, primary_specialization=True),
                SkillProficiency(domain=SkillDomain.OFFENSIVE_SECURITY_PENTEST, level=8, experience_points=1100),
                SkillProficiency(domain=SkillDomain.BINARY_ANALYSIS_ASSEMBLY, level=7, experience_points=750)
            ],
            total_score=290,
            collaboration_karma=9.3,
            current_model=ModelBackendRecord(
                model_id="qwen2.5-coder:14b-instruct",
                provider="ollama",
                parameter_size="14B",
                quantization="Q4_K_M",
                tasks_executed=54,
                success_rate=0.96,
                benchmark_score=95.0
            ),
            completed_feats=[
                CompletedFeat(id="feat-009", title="End-to-End Pipeline Automation", description="Executed complete multi-agent test loop and generated ISO 27037 forensic manifest autonomously.", points=150, task_category="automation"),
                CompletedFeat(id="feat-010", title="Self-Correction on Failed Tests", description="Resolved 5 consecutive compiler and type errors via automated reflection without human intervention.", points=140, task_category="reflection")
            ],
            best_performing_model_id="qwen2.5-coder:14b-instruct",
            lineage=AgentLineage(is_clone=False, clone_generation=0)
        )
    ]

    profiles_dir = base_dir / "agents/profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)

    for agent in agents:
        hof.register_or_update(agent)
        profile_file = profiles_dir / f"{agent.agent_id.lower()}.json"
        profile_file.write_text(agent.model_dump_json(indent=2), encoding="utf-8")
        print(f"Registered Agent: {agent.name} ({agent.nickname}) - {agent.total_score} pts")

    # Generate Markdown Leaderboard
    md_leaderboard = hof.render_markdown_leaderboard()
    (base_dir / "agents/hall_of_fame/LEADERBOARD.md").write_text(md_leaderboard, encoding="utf-8")
    print("\nLeaderboard generated at agents/hall_of_fame/LEADERBOARD.md")

if __name__ == "__main__":
    bootstrap_default_agents()
