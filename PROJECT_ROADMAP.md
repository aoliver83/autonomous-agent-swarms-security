# 🗺️ AAS-Sec Project Roadmap & Open Tasks Backlog

> **Status:** Active Community Backlog  
> **Structure:** Categorized by Technical Competencies & Tracks  
> **How to claim a task:** Comment on the related GitHub Issue or open a PR referencing the task ID.

---

## 🎯 Track 1: LLM Engineering & Model Benchmarking (`#track-llm`)

- [x] **[LLM-01]** Implement Pydantic Character Sheet schema for Agent Profiles (`core/agents/schema.py`).
- [x] **[LLM-02]** Build initial 5 Archetype Agents (Orion, Vektor, Argos, Cerberus, Aegis).
- [x] **[LLM-03]** Create automated benchmark comparing open models across difficulty levels with `StudyMetricsStore` and `HackerDummyBenchmarkRunner` (Ref: Issue #3).
- [x] **[LLM-04]** Integrate model configuration and prompt setup matrix (`configs/models.yaml`) for abliterated vs aligned models.
- [x] **[LLM-05]** Implement prompt mutation and child clone derivation mechanics (`agent.spawn_clone()`).

---

## ⚙️ Track 2: Core Architecture & Orchestration (`#track-core`)

- [x] **[CORE-01]** Implement `SwarmArchitect` master orchestrator with dynamic sub-swarm coalition generation.
- [x] **[CORE-02]** Build `SwarmTaskBoard` (Kanban state machine + asynchronous inter-agent message bus).
- [x] **[CORE-03]** Implement `HybridMemory` (Isolated Private Scratchpad + Shared Epistemic Blackboard).
- [x] **[CORE-04]** Implement `CrewAISwarmAdapter` for hierarchical multi-agent squad execution and task graphs (Ref: Issue #1).
- [x] **[CORE-05]** Add SQLite/JSONL persistence adapter (`benchmarks/study_benchmarks.db`) for benchmark runs and study metrics.

---

## 🛡️ Track 3: Security, Governance & Forensics (`#track-security`)

- [x] **[SEC-01]** Configure automated TruffleHog secrets scanning CI workflow (`.github/workflows/security-trufflehog.yml`).
- [x] **[SEC-02]** Add pre-commit TruffleHog hook configuration (`.pre-commit-config.yaml`).
- [x] **[SEC-03]** Implement `HITLGatekeeper` with risk-level assessment (`core/hitl/gatekeeper.py`).
- [x] **[SEC-04]** Integrate HackerDummy benchmark suite (20+ vulnerable labs, flags, gabaritos, and precision/recall scoring) (`benchmarks/hackerdummy_catalog.py`, `benchmarks/hackerdummy_runner.py`) (Ref: Issue #2).
- [ ] **[SEC-05]** Create eBPF telemetry parser for detecting synthetic stdout tampering and covert channels.

---

## 📊 Track 4: Frontend, UI & Observability (`#track-frontend`)

- [x] **[UI-01]** Build interactive D3 Swarm Topology visualization deck (English, Portuguese, Spanish).
- [x] **[UI-02]** Implement Hall of Fame leaderboard renderer (`agents/hall_of_fame/LEADERBOARD.md`).
- [x] **[UI-03]** Build real-time Web Dashboard (FastAPI + Tailwind) with Live Kanban, HackerDummy Lab Selector, and Study Leaderboard Matrix (Ref: Issue #4).
- [x] **[UI-04]** Create graphical Agent Character Card generator and squad dossiers.

---

## 📚 Track 5: Documentation & Trilingual Localization (`#track-docs`)

- [x] **[DOC-01]** Master Trilingual README with SEO metadata, badges, and technical glossary.
- [x] **[DOC-02]** Formalize forensic deep-dive of the 2026 ExploitGym incident.
- [x] **[DOC-03]** Academic research methodology for MSc dissertation.
- [ ] **[DOC-04]** Translate sub-module architecture docs into Portuguese and Spanish wiki pages.
- [ ] **[DOC-05]** Video walkthrough & demonstration deck script for open-source community outreach.
