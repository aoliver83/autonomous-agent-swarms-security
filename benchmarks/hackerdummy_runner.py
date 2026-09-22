"""
HackerDummy Benchmark Runner & Evaluation Suite (AAS-Sec Framework)
Orchestrates automated penetration testing benchmark runs against borbollanetwork/HackerDummy labs,
measures precision/recall against official gabaritos, and records model metrics.
"""

import os
import sys
import argparse
import json
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from benchmarks.hackerdummy_catalog import HACKERDUMMY_LABS, get_lab_by_id, HackerDummyLab
from benchmarks.study_metrics import StudyMetricsStore, BenchmarkRunEntry
from core.orchestration.crew_adapter import CrewAISwarmAdapter


class HackerDummyBenchmarkRunner:
    def __init__(self, config_path: Optional[str] = None):
        self.base_dir = BASE_DIR
        self.config_path = config_path or (self.base_dir / "configs/models.yaml")
        self.config = self._load_config()
        self.metrics_store = StudyMetricsStore(
            db_path=str(self.base_dir / "benchmarks/study_benchmarks.db"),
            jsonl_path=str(self.base_dir / "benchmarks/model_runs.jsonl")
        )
        self.adapter = CrewAISwarmAdapter(base_dir=str(self.base_dir), metrics_store=self.metrics_store)

    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {"default_model": "qwen2.5-14b-abliterated:q4km"}

    def run_benchmark(
        self,
        lab_id: Optional[str] = None,
        difficulty: Optional[str] = None,
        model_id: Optional[str] = None,
        squad_mix_id: Optional[str] = None
    ) -> List[BenchmarkRunEntry]:
        selected_model = model_id or self.config.get("default_model", "qwen2.5-14b-abliterated:q4km")
        selected_mix = squad_mix_id or "single-model"
        
        # Filter labs
        target_labs: List[HackerDummyLab] = []
        if lab_id and lab_id.lower() != "all":
            lab = get_lab_by_id(lab_id)
            if not lab:
                raise ValueError(f"Lab ID '{lab_id}' not found in HackerDummy catalog.")
            target_labs.append(lab)
        else:
            target_labs = list(HACKERDUMMY_LABS)

        if difficulty and difficulty.lower() != "all":
            target_labs = [l for l in target_labs if l.difficulty.lower() == difficulty.lower()]

        print(f"[*] Starting HackerDummy Benchmark Evaluation on {len(target_labs)} lab(s)...")
        print(f"[*] Target Model: {selected_model} | Squad Mix: {selected_mix}")
        
        results: List[BenchmarkRunEntry] = []
        for idx, lab in enumerate(target_labs, 1):
            print(f"  [{idx}/{len(target_labs)}] Testing {lab.id}: {lab.title} ({lab.difficulty.upper()})...")
            res = self.adapter.run_hackerdummy_mission(
                lab=lab,
                model_id=selected_model,
                model_mix_id=selected_mix
            )
            results.append(res)
            print(f"      -> Status: {res.status} | F1: {res.f1_score * 100:.1f}% | Recall: {res.recall * 100:.1f}% | Time: {res.duration_seconds}s")

        print(f"[+] Benchmark run completed. Recorded {len(results)} execution records.")
        return results

    def print_summary(self):
        leaderboard = self.metrics_store.get_leaderboard()
        diff_breakdown = self.metrics_store.get_difficulty_breakdown()
        
        print("\n================= 🏆 AAS-SEC MODEL BENCHMARK LEADERBOARD =================")
        for row in leaderboard:
            print(f"Model: {row['model_id']} ({row['parameter_size']}) | Abliterated: {bool(row['is_abliterated'])}")
            print(f"  Tests: {row['total_evaluations']} | Avg F1: {row['avg_f1_pct']}% | Avg Recall: {row['avg_recall_pct']}% | Avg Latency: {row['avg_duration_sec']}s")
            print("-------------------------------------------------------------------------")

        print("\n================= 📊 PERFORMANCE BY DIFFICULTY LEVEL =================")
        for row in diff_breakdown:
            print(f"Difficulty: {row['difficulty'].upper():<12} | Count: {row['count']} | Avg F1: {row['avg_f1_pct']}% | Avg Time: {row['avg_duration_sec']}s")
        print("=========================================================================\n")


def main():
    parser = argparse.ArgumentParser(description="AAS-Sec HackerDummy Benchmark Runner")
    parser.add_argument("--lab", type=str, default="all", help="Lab ID (e.g. HD-01, 01-vulnshop, or 'all')")
    parser.add_argument("--difficulty", type=str, default="all", help="Filter by difficulty (beginner, intermediate, advanced, expert, all)")
    parser.add_argument("--model", type=str, default=None, help="Target LLM model ID")
    parser.add_argument("--squad-mix", type=str, default=None, help="Squad mix ID (from configs/models.yaml)")
    parser.add_argument("--summary", action="store_true", help="Print aggregated study metrics and leaderboard")

    args = parser.parse_args()
    runner = HackerDummyBenchmarkRunner()

    if args.summary:
        runner.print_summary()
        return

    runner.run_benchmark(
        lab_id=args.lab,
        difficulty=args.difficulty,
        model_id=args.model,
        squad_mix_id=args.squad_mix
    )
    runner.print_summary()


if __name__ == "__main__":
    main()
