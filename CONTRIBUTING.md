# Contributing to Autonomous Agent Swarms Security Research (AAS-Sec)

Welcome to the **AAS-Sec Open Source Community**! We are building the open, reproducible framework for studying **Multi-Agent Swarm Intelligence, Dynamic Coalitions, Covert Channels, and Defensive Sandboxing**.

---

## 🌟 Our Core Thesis

> **Frontier scale is not the only path to complex intelligence.**  
> Smaller, older, and open-weight models (3B, 7B, 14B) possessing solid foundational knowledge in Python, assembly, reverse engineering, and networking can—when organized into specialized, collaborative swarms with memory and task boards—achieve outcomes on par with proprietary mega-models.

---

## 🛠️ Contribution Domains & Competencies

You can contribute across any of our five primary competency tracks:

1. **🤖 LLM Engineering & Agent Personas:**
   - Propose new agent character sheets (`core/agents/schema.py`).
   - Benchmark open/abliterated models against specialized challenges.
   - Tune prompt architectures and self-reflection loops.

2. **⚙️ Core Framework & Orchestration:**
   - Improve the `SwarmArchitect` dynamic coalition engine.
   - Enhance the `SwarmTaskBoard` / Kanban message broker.
   - Extend `HybridMemory` (Epistemic Blackboard + Private Scratchpad).

3. **🛡️ Security, DFIR & Sandbox Hardening:**
   - Integrate and test **TruffleHog** secrets verification gates.
   - Develop eBPF/Falco behavioral anomaly detection rules.
   - Harden gVisor / container sandbox boundaries against escape vectors.

4. **📊 Frontend, D3 Visualizations & UX:**
   - Expand interactive D3 swarm topology visualizers.
   - Build agent Hall of Fame UI cards and real-time kanban views.

5. **📚 Documentation & Trilingual Localization:**
   - Maintain and expand documentation across **English (primary)**, **Português (Brasil)**, and **Español**.

---

## 🔒 Security Policy: Zero Secrets Leak

Before submitting any Pull Request:
1. Run local secrets verification:
   ```bash
   trufflehog git file://. --only-verified
   ```
2. Ensure no API keys, private certificates, or internal tokens are committed.
3. Automated CI with TruffleHog runs on all PRs.

---

## 🚀 How to Get Started

1. Check our active [Project Roadmap & Issue Backlog](PROJECT_ROADMAP.md).
2. Choose an issue or submit a new proposal using our [GitHub Issue Templates](.github/ISSUE_TEMPLATE/).
3. Fork the repository, create a branch (`feature/your-agent-name`), commit your changes, and submit a PR.
