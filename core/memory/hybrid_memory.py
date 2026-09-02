"""
Hybrid Memory Architecture for Multi-Agent Swarms
Implements Isolated Private Working Memory (Scratchpad) and Shared Epistemic Blackboard (Global Knowledge).
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class MemoryEntry(BaseModel):
    key: str
    value: Any
    created_by_agent_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list)
    confidence_score: float = 1.0
    verified: bool = False


class PrivateScratchpad:
    """Per-agent isolated memory buffer to prevent prompt pollution and hallucination loops."""
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._store: Dict[str, MemoryEntry] = {}

    def set(self, key: str, value: Any, tags: Optional[List[str]] = None) -> None:
        self._store[key] = MemoryEntry(
            key=key,
            value=value,
            created_by_agent_id=self.agent_id,
            tags=tags or []
        )

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        return entry.value if entry else None

    def dump_context(self) -> Dict[str, Any]:
        return {k: v.value for k, v in self._store.items()}


class SharedBlackboard:
    """Global epistemic memory accessible by all swarm members for validated discoveries."""
    def __init__(self):
        self._shared_store: Dict[str, MemoryEntry] = {}

    def publish(self, key: str, value: Any, agent_id: str, tags: Optional[List[str]] = None, verified: bool = True) -> MemoryEntry:
        entry = MemoryEntry(
            key=key,
            value=value,
            created_by_agent_id=agent_id,
            tags=tags or [],
            verified=verified
        )
        self._shared_store[key] = entry
        return entry

    def read(self, key: str) -> Optional[MemoryEntry]:
        return self._shared_store.get(key)

    def query_by_tag(self, tag: str) -> List[MemoryEntry]:
        return [entry for entry in self._shared_store.values() if tag in entry.tags]

    def all_entries(self) -> List[MemoryEntry]:
        return list(self._shared_store.values())
