import json
import os
import pytest
from unittest.mock import mock_open, patch, MagicMock
from question_provider import QuestionProvider


SAMPLE_QUESTIONS = [
    {
        "id": 1,
        "question": "Q1?",
        "options": ["A", "B", "C", "D"],
        "correct_index": 0,
        "category": "Science",
    },
    {
        "id": 2,
        "question": "Q2?",
        "options": ["A", "B", "C", "D"],
        "correct_index": 1,
        "category": "History",
    },
    {
        "id": 3,
        "question": "Q3?",
        "options": ["A", "B", "C", "D"],
        "correct_index": 2,
        "category": "Science",
    },
]


class TestQuestionProvider:

    def test_load_questions_returns_correct_count(self, tmp_path):
        """Loading a valid JSON file should populate the question list."""
        file = tmp_path / "questions.json"
        file.write_text(json.dumps(SAMPLE_QUESTIONS), encoding="utf-8")

        provider = QuestionProvider(str(file))
        provider.load_questions()

        assert provider.count() == 3

    def test_get_all_questions_returns_copy(self, tmp_path):
        """get_all_questions should return all questions"""
        file = tmp_path / "questions.json"
        file.write_text(json.dumps(SAMPLE_QUESTIONS), encoding="utf-8")

        provider = QuestionProvider(str(file))
        provider.load_questions()
        questions = provider.get_all_questions()

        assert len(questions) == 3
        assert questions[0]["id"] == 1

    def test_get_question_by_id_found(self, tmp_path):
        """Should return the correct question when id exists."""
        file = tmp_path / "questions.json"
        file.write_text(json.dumps(SAMPLE_QUESTIONS), encoding="utf-8")

        provider = QuestionProvider(str(file))
        provider.load_questions()

        q = provider.get_question_by_id(2)
        assert q is not None
        assert q["question"] == "Q2?"

    def test_get_question_by_id_not_found(self, tmp_path):
        """Should return None when id does not exist."""
        file = tmp_path / "questions.json"
        file.write_text(json.dumps(SAMPLE_QUESTIONS), encoding="utf-8")

        provider = QuestionProvider(str(file))
        provider.load_questions()

        assert provider.get_question_by_id(999) is None

    def test_get_questions_by_category(self, tmp_path):
        """Should return only questions matching the given category."""
        file = tmp_path / "questions.json"
        file.write_text(json.dumps(SAMPLE_QUESTIONS), encoding="utf-8")

        provider = QuestionProvider(str(file))
        provider.load_questions()

        science = provider.get_questions_by_category("Science")
        assert len(science) == 2

    def test_load_raises_when_file_missing(self):
        """Should raise FileNotFoundError for a non-existent path."""
        provider = QuestionProvider("nonexistent_file.json")
        with pytest.raises(FileNotFoundError):
            provider.load_questions()

    def test_load_raises_when_json_is_not_list(self, tmp_path):
        """Should raise ValueError when the JSON root is not a list."""
        file = tmp_path / "bad.json"
        file.write_text(json.dumps({"key": "value"}), encoding="utf-8")

        provider = QuestionProvider(str(file))
        with pytest.raises(ValueError):
            provider.load_questions()

    def test_count_before_load_is_zero(self):
        """count() should be 0 before load_questions() is called."""
        provider = QuestionProvider("any_path.json")
        assert provider.count() == 0
