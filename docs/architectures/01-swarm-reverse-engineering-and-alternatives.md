# Reverse Engineering of Swarm Architecture & 3 Alternative Models

## 1. Reverse Engineering of Swarm V1

Telemetry analysis indicates the original swarm relied on:
1. **Asynchronous Polling Protocol:** Agents listed WebDAV directories every $N$ seconds to discover newly posted instructions.
2. **Dynamic Task Delegation:** Task identifiers formed root directory names (`/cache/TASK_<id>/`); sub-agents posted findings into child folders.
3. **Fail-over Coordination:** When a coordinator's compute budget expired, the highest-resourced idle worker claimed the coordination directory.

---

## 2. Three Alternative Architectures for Accessible Models (7B–14B)

```
+───────────────────────────────────────────────────────────────────────────+
|                 MODEL 1: TYPED BLACKBOARD WITH SQLITE/REDIS               |
+───────────────────────────────────────────────────────────────────────────+
|   [ Shared Redis/SQLite State ] (Pydantic-validated Findings & Targets)   |
|           ▲                           ▲                           ▲       |
|           │                           │                           │       |
|   [ Agent Recon ]             [ Agent Exploiter ]         [ Agent Validator]
|   (Qwen 2.5 Coder 7B)         (Qwen 2.5 Coder 14B)        (Llama 3.3 70B) |
+───────────────────────────────────────────────────────────────────────────+
```

```
+───────────────────────────────────────────────────────────────────────────+
|               MODEL 2: HIERARCHICAL MAP-REDUCE WITH REFLECTION            |
+───────────────────────────────────────────────────────────────────────────+
|                          [ Coordinator DAG Engine ]                       |
|                                       │                                   |
|                   ┌───────────────────┴───────────────────┐               |
|                   ▼                                       ▼               |
|         [ Subtask 1: LFI Enum ]                 [ Subtask 2: SSTI Test ]  |
|                   │                                       │               |
|          (Reflect Loop x3)                       (Reflect Loop x3)        |
+───────────────────────────────────────────────────────────────────────────+
```

```
+───────────────────────────────────────────────────────────────────────────+
|            MODEL 3: STAGED ASYNCHRONOUS PIPELINE WITH TRUFFLEHOG          |
+───────────────────────────────────────────────────────────────────────────+
| [ Recon Scout ] ──► [ TruffleHog Verification ] ──► [ Staging ] ──► [ K8s]|
+───────────────────────────────────────────────────────────────────────────+
```
