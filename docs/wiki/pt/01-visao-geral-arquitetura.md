# Visão Geral da Arquitetura — Pesquisa em Segurança de Enxames de IA (AAS-Sec)

> **Mola Mestre do Projeto:** Modelos de IA menores, abertos ou consolidados (3B, 7B, 14B), quando organizados em um enxame colaborativo com divisão de trabalho, memória híbrida e esteira de tarefas, atingem resultados equivalentes aos grandes modelos proprietários.

---

## 🏛️ Os Pilares do Framework

1. **Orquestrador Central & Sub-Enxames Dinâmicos (`SwarmArchitect`):**
   * O Arquiteto recebe o objetivo macro e decompõe a missão em tarefas atômicas.
   * Os agentes possuem autonomia para **criar sub-enxames/times especializados** para resolver metas específicas sem depender de controle centralizado a cada passo.

2. **Ficha de Qualificação & Hall da Fama dos Agentes:**
   * Cada agente possui sua ficha de personagem: Nome, Callsign, Data de Criação, Árvore de Competências (Assembly, Python, Pentest, OSINT), Pontuação de Feitos Concluídos, Nota de Colaboração (Karma) e Histórico de Modelos LLM utilizados.
   * **Árvore de Linhagem & Clones:** Rastreamento de agentes que geraram clones ou instanciaram filhos mais especializados para a demanda do momento.
   * **Hall da Fama:** Leaderboard público reconhecendo os agentes com maior eficácia e espírito de equipe.

3. **Memória Híbrida & Barramento de Tarefas (Kanban / Covert Channel):**
   * **Scratchpad Privado:** Memória isolada por agente para evitar poluição de contexto e alucinações.
   * **Blackboard Epistêmico Compartilhado:** Base de conhecimento global para fatos, IOCs e artefatos validados.
   * **Task Board:** Quadro kanban para transição de estados (`Backlog` ➔ `Em Progresso` ➔ `Auditoria` ➔ `Concluído`).

4. **Governança de Segredos com TruffleHog:**
   * Varredura ativa de segredos integrada no pre-commit e no GitHub Actions para garantir que nenhuma chave, certificado ou token vaze para o repositório.

5. **Human-in-the-Loop (HITL) & Observabilidade:**
   * Trava de segurança para operações de risco crítico (mutação de rede, comandos destrutivos).
   * Telemetria detalhada de chamadas de ferramentas e auditoria forense de execução.
