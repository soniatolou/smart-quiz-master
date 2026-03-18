import json
import pytest
from score_tracker import ScoreTracker


class TestScoreTracker:

    def setup_method(self):
        self.tracker = ScoreTracker(highscore_file="test_highscores_tmp.json")

    def teardown_method(self):
        import os
        if os.path.exists("test_highscores_tmp.json"):
            os.remove("test_highscores_tmp.json")

    def test_initial_score_is_zero(self):
        assert self.tracker.get_score() == 0

    def test_add_correct_increments_score(self):
        self.tracker.add_correct()
        assert self.tracker.get_score() == 1

    def test_add_incorrect_does_not_increment_score(self):
        self.tracker.add_incorrect()
        assert self.tracker.get_score() == 0

    def test_total_increments_on_correct_and_incorrect(self):
        self.tracker.add_correct()
        self.tracker.add_incorrect()
        assert self.tracker.get_total() == 2

    def test_percentage_calculation(self):
        self.tracker.add_correct()
        self.tracker.add_correct()
        self.tracker.add_incorrect()
        assert self.tracker.get_percentage() == pytest.approx(66.666, rel=1e-2)

    def test_percentage_when_no_questions(self):
        """Percentage should be 0.0 when no questions have been answered."""
        assert self.tracker.get_percentage() == 0.0

    def test_reset_clears_score_and_total(self):
        self.tracker.add_correct()
        self.tracker.add_correct()
        self.tracker.reset()
        assert self.tracker.get_score() == 0
        assert self.tracker.get_total() == 0

    def test_save_highscore_creates_file(self):
        import os
        self.tracker.add_correct()
        self.tracker.save_highscore("TestPlayer")
        assert os.path.exists("test_highscores_tmp.json")

    def test_save_highscore_content(self):
        self.tracker.add_correct()
        self.tracker.add_incorrect()
        self.tracker.save_highscore("Alice")

        scores = self.tracker.get_highscores()
        assert len(scores) == 1
        assert scores[0]["player"] == "Alice"
        assert scores[0]["score"] == 1
        assert scores[0]["total"] == 2

    def test_highscores_sorted_by_score_descending(self):
        self.tracker.add_correct()
        self.tracker.save_highscore("Low")

        self.tracker.reset()
        self.tracker.add_correct()
        self.tracker.add_correct()
        self.tracker.save_highscore("High")

        scores = self.tracker.get_highscores()
        assert scores[0]["player"] == "High"
        assert scores[1]["player"] == "Low"

    def test_get_highscores_returns_empty_list_when_no_file(self):
        scores = self.tracker.get_highscores()
        assert scores == []
