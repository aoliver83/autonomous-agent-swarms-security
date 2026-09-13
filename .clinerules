# Autonomous Agent Swarms Security (AAS-Sec) — Cline & Agent Directives

You are operating within the **AAS-Sec Red Team Multi-Agent Swarm Laboratory** on `vps` (192.168.1.40).

## 🏛️ Core Architecture & Squad Hierarchy
The lab implements a decentralized multi-agent swarm architecture where smaller and open-source models achieve frontier parity through specialization, memory isolation, and dynamic coalitions.

### 👥 Active Red Team Squad (`core/redteam/squad.py`):
1. **`RED-ORION-01` (Swarm Commander & Architect):** Macro campaign decomposition, task dispatching, rules of engagement.
2. **`RED-ARGOS-02` (Reconnaissance & OSINT Scout):** Passive reconnaissance, ShadohDorks, DNS/certificate mapping.
3. **`RED-VEKTOR-03` (Vulnerability & Binary Specialist):** ELF/PE reversing, assembly decompilation, CVE triage.
4. **`RED-AEGIS-04` (Payload & Tooling Engineer):** Python PoC synthesizer, automated reflection and test execution.
5. **`RED-CERBERUS-05` (Post-Exploit & Secrets Auditor):** Active token verification with TruffleHog, ISO 27037 forensic manifest generation.

## 🧠 LLM Backend & Routing
- **Primary Open Model:** `qwen2.5-14b-abliterated:q4km` (or `ollama-local/qwen2.5-14b-abliterated:latest`).
- **Endpoint:** `http://192.168.1.20:20128/v1` (OmniRoute Proxy on GPU Host) or `http://localhost:11434`.

## 📋 Kanban Task Board & Workflow
- **Task States:** `backlog` ➔ `in_progress` ➔ `needs_audit` ➔ `hitl_pending` ➔ `completed`.
- When picking up tasks:
  1. Inspect the active board at `GET http://localhost:8090/api/tasks`.
  2. Advance the task state as work progresses.
  3. Log all execution events to `lab/telemetry/swarm_telemetry.jsonl`.
  4. Ensure zero secrets are committed using TruffleHog pre-commit gates.

## 🚀 Running the Web Dashboard:
```bash
./start_dashboard.sh
# Access UI at: http://192.168.1.40:8090
```
