# Visión General de la Arquitectura — Seguridad de Enjambres de Agentes de IA (AAS-Sec)

> **Tesis Central:** Los modelos de IA abiertos y más pequeños (3B, 7B, 14B), cuando se organizan en un enjambre colaborativo con división del trabajo, memoria híbrida y tablero de tareas, logran resultados equivalentes a los grandes modelos propietarios de frontera.

---

## 🏛️ Pilares del Framework

1. **Orquestador Maestro y Sub-Enjambres Dinámicos (`SwarmArchitect`):**
   * Descompone misiones complejas en tareas atómicas y permite la formación espontánea de coaliciones especializadas.
   * Los agentes tienen la libertad de generar clones y sub-equipos para resolver objetivos concretos.

2. **Ficha de Calificación y Salón de la Fama (Hall of Fame):**
   * Hoja de personaje por agente: Nombre, Callsign, Categoría, Árbol de Habilidades (Assembly, Python, Pentest, OSINT), Puntuación de Logros, Karma de Colaboración y Registro de Modelos LLM utilizados.
   * **Linaje y Derivación:** Registro de agentes que instanciaron clones especializados.
   * **Salón de la Fama:** Clasificación pública de los agentes más efectivos.

3. **Memoria Híbrida y Tablero Kanban:**
   * **Scratchpad Privado:** Memoria aislada por agente para evitar la contaminación de contexto.
   * **Pizarra Epistémica Compartida:** Base de conocimiento global para descubrimientos, IoCs y artefactos verificados.
   * **Task Board:** Flujo de trabajo transparente (`Backlog` ➔ `En Progreso` ➔ `Auditoría` ➔ `Completado`).

4. **Gobernanza de Secretos con TruffleHog:**
   * Escaneo activo de secretos en pre-commit y CI para evitar fugas de claves, tokens o certificados.

5. **Human-in-the-Loop (HITL) y Observabilidad:**
   * Puerta de aprobación humana para acciones de alto impacto y telemetría continua de llamadas de herramientas.
