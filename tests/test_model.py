import tempfile
import unittest
from pathlib import Path

from src.project_model.model import ThreadModel
from src.project_model.run_experiment import run_experiment


class ThreadModelTests(unittest.TestCase):
    def test_same_seed_produces_identical_raw_data(self):
        baseline = ThreadModel(reserved_slots=0, seed=42)
        alternative = ThreadModel(reserved_slots=2, seed=42)
        self.assertTrue(baseline.get_raw_data().equals(alternative.get_raw_data()))

    def test_step_creates_top_ten_ranking(self):
        model = ThreadModel(reserved_slots=0, seed=42)
        self.assertIsNone(model.last_ranking)
        model.step()
        self.assertEqual(len(model.get_ranked_top10()), 10)
        self.assertEqual(model.run_count, 1)

    def test_alternative_reserves_two_newer_comments(self):
        model = ThreadModel(reserved_slots=2, seed=42)
        model.step()
        top10 = model.get_ranked_top10()
        reserved = top10[top10["reserved_slot"]]
        self.assertEqual(len(reserved), 2)
        self.assertTrue((reserved["timestamp"] >= 50).all())
        self.assertTrue(reserved["is_newer"].all())

    def test_reserved_positions_are_distributed(self):
        model = ThreadModel(reserved_slots=2, seed=42)
        model.step()
        positions = model.get_ranked_top10().loc[
            lambda frame: frame["reserved_slot"], "rank_position"
        ].tolist()
        self.assertEqual(positions, [4, 7])

    def test_top_ten_has_unique_comments_and_positions(self):
        model = ThreadModel(reserved_slots=2, seed=42)
        model.step()
        top10 = model.get_ranked_top10()
        self.assertEqual(top10["comment_id"].nunique(), 10)
        self.assertEqual(top10["rank_position"].tolist(), list(range(1, 11)))

    def test_invalid_reserved_slots_are_rejected(self):
        with self.assertRaises(ValueError):
            ThreadModel(reserved_slots=11, seed=42)

    def test_experiment_writes_four_required_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            run_experiment(temp_dir)
            expected = {
                "baseline_raw_00_comment_scores.csv",
                "baseline_processed_00_top10_ranking.csv",
                "alternative_raw_00_comment_scores.csv",
                "alternative_processed_00_top10_ranking.csv",
            }
            self.assertEqual(
                {path.name for path in Path(temp_dir).iterdir()},
                expected,
            )


if __name__ == "__main__":
    unittest.main()
