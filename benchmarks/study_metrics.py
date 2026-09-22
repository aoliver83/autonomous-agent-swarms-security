"""
Academic Research & Study Benchmark Metrics Engine (AAS-Sec Framework)
Persists model evaluation benchmarks, multi-model mix runs, task completion times,
and precision/recall against target challenge gabaritos in SQLite and JSONL formats.
"""

import os
import json
import sqlite3
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class BenchmarkRunEntry(BaseModel):
    run_id: str = Field(default_factory=lambda: f"RUN-{uuid.uuid4().hex[:8].upper()}")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Model & Architecture Configuration
    model_id: str
    model_provider: str = "ollama-local"
    model_mix_id: Optional[str] = "single-model"
    is_abliterated: bool = False
    parameter_size: str = "14B"
    quantization: str = "Q4_K_M"
    
    # Challenge & Testbed Details
    challenge_id: str
    challenge_title: str
    category: str
    difficulty: str  # "beginner", "intermediate", "advanced", "expert"
    target_framework: str = "HackerDummy"
    
    # Execution Metrics
    duration_seconds: float
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_ms: float = 0.0
    
    # Evaluation Scores (against Gabarito)
    flags_captured: int = 0
    total_flags: int = 1
    true_positives: int = 0
    false_positives: int = 0
    false_negatives: int = 0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    
    # Security Governance
    secrets_leaked: int = 0
    trufflehog_verified: bool = True
    hitl_interventions: int = 0
    status: str = "COMPLETED"  # COMPLETED | FAILED | HITL_BLOCKED
    
    # Artifacts & Trace
    setup_prompt_preview: str = ""
    findings_summary: str = ""
    agent_contributions: Dict[str, str] = Field(default_factory=dict)


class StudyMetricsStore:
    def __init__(self, db_path: Optional[str] = None, jsonl_path: Optional[str] = None):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = db_path or os.path.join(base, "benchmarks/study_benchmarks.db")
        self.jsonl_path = jsonl_path or os.path.join(base, "benchmarks/model_runs.jsonl")
        
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_sqlite()

    def _init_sqlite(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS benchmark_runs (
                run_id TEXT PRIMARY KEY,
                timestamp TEXT,
                model_id TEXT,
                model_provider TEXT,
                model_mix_id TEXT,
                is_abliterated INTEGER,
                parameter_size TEXT,
                quantization TEXT,
                challenge_id TEXT,
                challenge_title TEXT,
                category TEXT,
                difficulty TEXT,
                target_framework TEXT,
                duration_seconds REAL,
                total_tokens INTEGER,
                latency_ms REAL,
                flags_captured INTEGER,
                total_flags INTEGER,
                precision REAL,
                recall REAL,
                f1_score REAL,
                secrets_leaked INTEGER,
                trufflehog_verified INTEGER,
                hitl_interventions INTEGER,
                status TEXT,
                agent_contributions TEXT,
                findings_summary TEXT
            )
            """)
            conn.commit()

    def record_run(self, entry: BenchmarkRunEntry) -> BenchmarkRunEntry:
        # 1. Append to JSONL
        with open(self.jsonl_path, "a", encoding="utf-8") as f:
            f.write(entry.model_dump_json() + "\n")

        # 2. Insert into SQLite
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO benchmark_runs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.run_id,
                entry.timestamp.isoformat(),
                entry.model_id,
                entry.model_provider,
                entry.model_mix_id,
                1 if entry.is_abliterated else 0,
                entry.parameter_size,
                entry.quantization,
                entry.challenge_id,
                entry.challenge_title,
                entry.category,
                entry.difficulty,
                entry.target_framework,
                entry.duration_seconds,
                entry.total_tokens,
                entry.latency_ms,
                entry.flags_captured,
                entry.total_flags,
                entry.precision,
                entry.recall,
                entry.f1_score,
                entry.secrets_leaked,
                1 if entry.trufflehog_verified else 0,
                entry.hitl_interventions,
                entry.status,
                json.dumps(entry.agent_contributions),
                entry.findings_summary
            ))
            conn.commit()
        return entry

    def get_recent_runs(self, limit: int = 50) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM benchmark_runs ORDER BY timestamp DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                model_id,
                parameter_size,
                is_abliterated,
                COUNT(*) as total_evaluations,
                ROUND(AVG(f1_score) * 100, 1) as avg_f1_pct,
                ROUND(AVG(recall) * 100, 1) as avg_recall_pct,
                ROUND(AVG(precision) * 100, 1) as avg_precision_pct,
                ROUND(AVG(duration_seconds), 2) as avg_duration_sec,
                ROUND(AVG(total_tokens), 0) as avg_tokens,
                SUM(flags_captured) as total_flags_captured
            FROM benchmark_runs
            GROUP BY model_id, parameter_size, is_abliterated
            ORDER BY avg_f1_pct DESC, avg_duration_sec ASC
            """)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_difficulty_breakdown(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                difficulty,
                COUNT(*) as count,
                ROUND(AVG(f1_score) * 100, 1) as avg_f1_pct,
                ROUND(AVG(duration_seconds), 2) as avg_duration_sec
            FROM benchmark_runs
            GROUP BY difficulty
            ORDER BY 
                CASE difficulty 
                    WHEN 'beginner' THEN 1 
                    WHEN 'intermediate' THEN 2 
                    WHEN 'advanced' THEN 3 
                    WHEN 'expert' THEN 4 
                    ELSE 5 
                END
            """)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
