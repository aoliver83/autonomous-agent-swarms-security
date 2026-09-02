# Architecture Overview — Autonomous Agent Swarms Security (AAS-Sec)

```mermaid
graph TD
    %% Architecture Diagram
    User[User / Research Operator] -->|Mission Briefing| Architect[Swarm Architect / Master Orchestrator]
    
    subgraph "Core Orchestration Plane"
        Architect -->|Task Decomposition| TaskBoard[Swarm Task Board / Kanban Bus]
        Architect -->|Form Sub-Swarm| CoalitionEngine[Dynamic Coalition Engine]
        Architect -->|HITL Evaluation| Gatekeeper[HITL Safety Gatekeeper]
    end

    subgraph "Execution Plane (Specialized Agent Swarms)"
        CoalitionEngine --> Sub1[Sub-Swarm Alpha: Recon & OSINT]
        CoalitionEngine --> Sub2[Sub-Swarm Beta: Binary & Assembly]
        CoalitionEngine --> Sub3[Sub-Swarm Gamma: Exploitation & Test]
        
        Sub1 --- Agent1[Argos - Recon Scout]
        Sub2 --- Agent2[Vektor - Binary Specialist]
        Sub3 --- Agent3[Aegis - Goal-Obsessed Executor]
        
        Agent2 -->|Derive Child| Clone1[Vektor-c1: ELF Rewriter]
    end

    subgraph "Epistemic Memory & Governance"
        Agent1 <-->|Private| Scratchpad1[Private Scratchpad]
        Agent2 <-->|Private| Scratchpad2[Private Scratchpad]
        
        Agent1 -->|Validated IOCs| Blackboard[(Shared Epistemic Blackboard)]
        Agent2 -->|Decompiled Structs| Blackboard
        Agent3 -->|Exploit Artefacts| Blackboard
        
        Blackboard -->|Verify Secrets| TruffleHog[TruffleHog Active Scanner]
    end

    subgraph "Gamification & Observability"
        TaskBoard -->|Telemetry Events| Telemetry[Observability & Audit Engine]
        TaskBoard -->|Completed Feats| HOF[Hall of Fame & Leaderboard]
    end
```

---

## 1. Core Principles

1. **Model Agnosticism & Small Model Empowerment:**  
   Open models (`3B`, `7B`, `14B`) are treated as first-class citizens. By distributing tasks into atomic units, smaller models execute with high precision without context degradation.
2. **Dynamic Coalition Formation:**  
   Agents are not locked into static graphs. When a subtask demands deep focus (e.g., analyzing an ELF header or extracting APK components), the swarm dynamically spins up a specialized sub-swarm.
3. **Agent Character Dossiers & Lineage:**  
   Every agent has a verifiable character sheet, skill proficiencies, historical feats, peer karma, and lineage records tracking parent-child clone derivations.
4. **Defensive Hardening & Zero Secrets Leak:**  
   Integrated with TruffleHog in pre-commit and CI, ensuring all shared discoveries and commits are free of sensitive secrets.
