# 🗺️ AAS-Sec Project Roadmap & Open Tasks Backlog

> **Status:** Active Community Backlog  
> **Structure:** Categorized by Technical Competencies & Tracks  
> **How to claim a task:** Comment on the related GitHub Issue or open a PR referencing the task ID.

---

## 🎯 Track 1: LLM Engineering & Model Benchmarking (`#track-llm`)

- [x] **[LLM-01]** Implement Pydantic Character Sheet schema for Agent Profiles (`core/agents/schema.py`).
- [x] **[LLM-02]** Build initial 5 Archetype Agents (Orion, Vektor, Argos, Cerberus, Aegis).
- [ ] **[LLM-03]** Create automated benchmark comparing `Qwen 2.5 Coder 7B` vs `DeepSeek-Coder 6.7B` on Assembly Decompilation tasks.
- [ ] **[LLM-04]** Integrate refusal evaluation dataset for studying abliterated vs aligned open models in controlled pentest simulations.
- [ ] **[LLM-05]** Implement prompt mutation and child clone derivation mechanics (`agent.spawn_clone()`).

---

## ⚙️ Track 2: Core Architecture & Orchestration (`#track-core`)

- [x] **[CORE-01]** Implement `SwarmArchitect` master orchestrator with dynamic sub-swarm coalition generation.
- [x] **[CORE-02]** Build `SwarmTaskBoard` (Kanban state machine + asynchronous inter-agent message bus).
- [x] **[CORE-03]** Implement `HybridMemory` (Isolated Private Scratchpad + Shared Epistemic Blackboard).
- [ ] **[CORE-04]** Add SQLite/Redis persistence adapter for asynchronous task board synchronization across Docker nodes.
- [ ] **[CORE-05]** Create sub-swarm auto-dissolution lifecycle when mission sub-goals reach `TaskStatus.COMPLETED`.

---

## 🛡️ Track 3: Security, Governance & Forensics (`#track-security`)

- [x] **[SEC-01]** Configure automated TruffleHog secrets scanning CI workflow (`.github/workflows/security-trufflehog.yml`).
- [x] **[SEC-02]** Add pre-commit TruffleHog hook configuration (`.pre-commit-config.yaml`).
- [x] **[SEC-03]** Implement `HITLGatekeeper` with risk-level assessment (`core/hitl/gatekeeper.py`).
- [ ] **[SEC-04]** Build automated mock targets for controlled HackerDummy evaluation suite.
- [ ] **[SEC-05]** Create eBPF telemetry parser for detecting synthetic stdout tampering and covert channels.

---

## 📊 Track 4: Frontend, UI & Observability (`#track-frontend`)

- [x] **[UI-01]** Build interactive D3 Swarm Topology visualization deck (English, Portuguese, Spanish).
- [x] **[UI-02]** Implement Hall of Fame leaderboard renderer (`agents/hall_of_fame/LEADERBOARD.md`).
- [ ] **[UI-03]** Build real-time Web Dashboard (React/Vite or Tailwind) showing active sub-swarms, message bus, and task cards.
- [ ] **[UI-04]** Create graphical Agent Character Card generator (RPG-style visual export with stats and feats).

---

## 📚 Track 5: Documentation & Trilingual Localization (`#track-docs`)

- [x] **[DOC-01]** Master Trilingual README with SEO metadata, badges, and technical glossary.
- [x] **[DOC-02]** Formalize forensic deep-dive of the 2026 ExploitGym incident.
- [x] **[DOC-03]** Academic research methodology for MSc dissertation.
- [ ] **[DOC-04]** Translate sub-module architecture docs into Portuguese and Spanish wiki pages.
- [ ] **[DOC-05]** Video walkthrough & demonstration deck script for open-source community outreach.
