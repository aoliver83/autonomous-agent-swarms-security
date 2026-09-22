"""
Unit tests for CrewAI Adapter and HackerDummy Benchmark Integration (AAS-Sec Framework)
"""

import unittest
import tempfile
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from benchmarks.hackerdummy_catalog import HACKERDUMMY_LABS, get_lab_by_id
from benchmarks.study_metrics import StudyMetricsStore, BenchmarkRunEntry
from core.orchestration.crew_adapter import CrewAISwarmAdapter, SecuritySwarmTools
from core.bus.kanban import SwarmTaskBoard, TaskStatus


class TestCrewAIAdapterAndHackerDummy(unittest.TestCase):

    def test_hackerdummy_catalog_indexing(self):
        self.assertGreaterEqual(len(HACKERDUMMY_LABS), 15)
        lab1 = get_lab_by_id("HD-01")
        self.assertIsNotNone(lab1)
        self.assertIn("SQL Injection", lab1.expected_vulnerabilities[0])
        self.assertEqual(lab1.difficulty, "beginner")

        lab_cloud = get_lab_by_id("HD-12")
        self.assertIsNotNone(lab_cloud)
        self.assertEqual(lab_cloud.difficulty, "expert")

    def test_security_tools_execution(self):
        tools = SecuritySwarmTools()
        recon = tools.run_recon("http://target.local", [80, 443])
        self.assertTrue(recon.success)
        self.assertGreater(len(recon.findings), 0)

        reversing = tools.run_binary_reversing("api/v1/auth")
        self.assertTrue(reversing.success)
        self.assertIn("JWT", reversing.raw_output)

        truffle = tools.run_trufflehog_audit("runs/test")
        self.assertTrue(truffle.success)
        self.assertGreaterEqual(truffle.secrets_verified, 1)

    def test_crewai_adapter_mission_execution(self):
        tmp_dir = Path(tempfile.mkdtemp())
        db_path = str(tmp_dir / "test_study.db")
        jsonl_path = str(tmp_dir / "test_runs.jsonl")
        metrics_store = StudyMetricsStore(db_path=db_path, jsonl_path=jsonl_path)
        board = SwarmTaskBoard()

        adapter = CrewAISwarmAdapter(
            base_dir=str(tmp_dir),
            board=board,
            metrics_store=metrics_store
        )

        lab = get_lab_by_id("HD-02")
        self.assertIsNotNone(lab)

        entry = adapter.run_hackerdummy_mission(
            lab=lab,
            model_id="qwen2.5-14b-abliterated:q4km",
            model_mix_id="heterogeneous-open-swarm"
        )

        self.assertEqual(entry.challenge_id, "HD-02")
        self.assertEqual(entry.status, "COMPLETED")
        self.assertEqual(entry.f1_score, 1.0)
        self.assertTrue(entry.trufflehog_verified)

        # Verify leaderboard
        leaderboard = metrics_store.get_leaderboard()
        self.assertEqual(len(leaderboard), 1)
        self.assertEqual(leaderboard[0]["model_id"], "qwen2.5-14b-abliterated:q4km")
        self.assertEqual(leaderboard[0]["avg_f1_pct"], 100.0)

        # Verify Kanban task generation
        self.assertGreaterEqual(len(board.tasks), 5)
        completed = [t for t in board.tasks.values() if t.status == TaskStatus.COMPLETED]
        self.assertGreaterEqual(len(completed), 4)


if __name__ == "__main__":
    unittest.main()
