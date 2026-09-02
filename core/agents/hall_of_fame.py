"""
Hall of Fame & Leaderboard Registry for Autonomous Agents
Ranks agents based on verified achievements, peer collaboration karma, and task execution efficiency.
"""

from typing import List, Dict, Optional
import json
from pathlib import Path
from core.agents.schema import AgentProfileSheet


class HallOfFameRegistry:
    def __init__(self, storage_path: Path):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.agents_file = self.storage_path / "agents_registry.json"
        self._agents: Dict[str, AgentProfileSheet] = {}
        self.load()

    def load(self) -> None:
        if self.agents_file.exists():
            try:
                data = json.loads(self.agents_file.read_text(encoding="utf-8"))
                for item in data:
                    sheet = AgentProfileSheet.model_validate(item)
                    self._agents[sheet.agent_id] = sheet
            except Exception as e:
                print(f"[!] Error loading Hall of Fame: {e}")

    def save(self) -> None:
        data = [agent.model_dump(mode="json") for agent in self._agents.values()]
        self.agents_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def register_or_update(self, agent: AgentProfileSheet) -> None:
        self._agents[agent.agent_id] = agent
        self.save()

    def get_agent(self, agent_id: str) -> Optional[AgentProfileSheet]:
        return self._agents.get(agent_id)

    def get_leaderboard(self, limit: int = 10) -> List[AgentProfileSheet]:
        """Ranks agents by total score * collaboration karma."""
        sorted_agents = sorted(
            self._agents.values(),
            key=lambda a: (a.total_score * (a.collaboration_karma / 10.0), len(a.completed_feats)),
            reverse=True
        )
        return sorted_agents[:limit]

    def render_markdown_leaderboard(self) -> str:
        leaders = self.get_leaderboard(20)
        lines = [
            "# 🏆 Autonomous Agents Hall of Fame",
            "",
            "> **Official Leaderboard of Verified Agent Contributions, Feats & Collaboration Karma**",
            "",
            "| Rank | Callsign | Category | Total Score | Karma | Best Model | Generation | Lineage |",
            "|:---:|---|---|:---:|:---:|---|:---:|:---:|"
        ]
        for idx, agent in enumerate(leaders, 1):
            parent = f"Child of {agent.lineage.parent_agent_id}" if agent.lineage.parent_agent_id else "Genesis (Root)"
            lines.append(
                f"| #{idx} | **{agent.nickname}** (`{agent.agent_id}`) | `{agent.category.value}` | "
                f"**{agent.total_score} pts** | ⭐ {agent.collaboration_karma:.1f}/10 | "
                f"`{agent.best_performing_model_id or agent.current_model.model_id}` | Gen {agent.lineage.clone_generation} | {parent} |"
            )
        return "\n".join(lines)
