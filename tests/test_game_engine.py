import pytest
from unittest.mock import MagicMock, patch, call
from game_engine import GameEngine
from question_provider import QuestionProvider
from score_tracker import ScoreTracker
from validator import Validator


MOCK_QUESTIONS = [
    {"id": 1, "question": "What is 2+2?", "options": ["3", "4", "5", "6"], "correct_index": 1, "category": "Math"},
    {"id": 2, "question": "Sky color?", "options": ["Red", "Green", "Blue", "Yellow"], "correct_index": 2, "category": "Science"},
]


def make_engine():
    """Helper: create a GameEngine with fully mocked dependencies."""
    provider = MagicMock(spec=QuestionProvider)
    tracker = MagicMock(spec=ScoreTracker)
    validator = MagicMock(spec=Validator)
    engine = GameEngine(provider, tracker, validator)
    return engine, provider, tracker, validator


class TestGameEngine:

    def test_correct_answer_calls_add_correct(self):
        """When the player answers correctly, add_correct should be called."""
        engine, provider, tracker, validator = make_engine()

        provider.get_all_questions.return_value = [MOCK_QUESTIONS[0]]
        validator.validate_player_name.return_value = "Alice"
        validator.validate_answer.return_value = 1  # correct_index for Q1
        tracker.get_score.return_value = 1
        tracker.get_total.return_value = 1
        tracker.get_percentage.return_value = 100.0
        tracker.get_highscores.return_value = []

        with patch("builtins.input", side_effect=["Alice", "0", "2"]):  # "0" = alla kategorier
            engine.run()

        tracker.add_correct.assert_called_once()
        tracker.add_incorrect.assert_not_called()

    def test_wrong_answer_calls_add_incorrect(self):
        """When the player answers incorrectly, add_incorrect should be called."""
        engine, provider, tracker, validator = make_engine()

        provider.get_all_questions.return_value = [MOCK_QUESTIONS[0]]
        validator.validate_player_name.return_value = "Bob"
        validator.validate_answer.return_value = 0  # wrong answer
        tracker.get_score.return_value = 0
        tracker.get_total.return_value = 1
        tracker.get_percentage.return_value = 0.0
        tracker.get_highscores.return_value = []

        with patch("builtins.input", side_effect=["Bob", "0", "1"]):  # "0" = alla kategorier
            engine.run()

        tracker.add_incorrect.assert_called_once()
        tracker.add_correct.assert_not_called()
    def test_no_questions_exits_early(self):
        """If there are no questions, the engine should exit without calling add_correct/add_incorrect."""
        engine, provider, tracker, validator = make_engine()

        provider.get_all_questions.return_value = []
        validator.validate_player_name.return_value = "Alice"

        with patch("builtins.input", side_effect=["Alice", "0"]):
            engine.run()

        tracker.add_correct.assert_not_called()
        tracker.add_incorrect.assert_not_called()
    def test_invalid_input_retried_until_valid(self):
        """The engine should keep asking until the player gives valid input."""
        engine, provider, tracker, validator = make_engine()

        provider.get_all_questions.return_value = [MOCK_QUESTIONS[0]]
        validator.validate_player_name.return_value = "Alice"

        # First two calls raise ValueError, third returns valid index
        validator.validate_answer.side_effect = [
            ValueError("not a valid number"),
            ValueError("out of range"),
            1,  # correct
        ]
        tracker.get_score.return_value = 1
        tracker.get_total.return_value = 1
        tracker.get_percentage.return_value = 100.0
        tracker.get_highscores.return_value = []

        with patch("builtins.input", side_effect=["Alice", "0", "x", "9", "2"]):  # "0" = alla kategorier
            engine.run()

        assert validator.validate_answer.call_count == 3

    def test_score_saved_at_end(self):
        """save_highscore should be called once after all questions."""
        engine, provider, tracker, validator = make_engine()

        provider.get_all_questions.return_value = MOCK_QUESTIONS
        validator.validate_player_name.return_value = "Alice"
        validator.validate_answer.side_effect = [1, 2]  # correct answers

        tracker.get_score.return_value = 2
        tracker.get_total.return_value = 2
        tracker.get_percentage.return_value = 100.0
        tracker.get_highscores.return_value = []

        with patch("builtins.input", side_effect=["Alice", "2", "3"]):
            engine.run()

        tracker.save_highscore.assert_called_once_with("Alice")
