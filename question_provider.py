import json
import os
from typing import List, Dict, Optional


class QuestionProvider:
    """Loads and provides quiz questions from a JSON file."""

    def __init__(self, filepath: str = "questions.json"):
        self.filepath = filepath
        self._questions: List[Dict] = []

    def load_questions(self) -> None:
        """Load questions from the JSON file."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Question file not found: {self.filepath}")

        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("Question file must contain a JSON array.")

        self._questions = data

    def get_all_questions(self) -> List[Dict]:
        """Return all loaded questions."""
        return list(self._questions)

    def get_question_by_id(self, question_id: int) -> Optional[Dict]:
        """Return a single question by its id, or None if not found."""
        for q in self._questions:
            if q.get("id") == question_id:
                return q
        return None

    def get_questions_by_category(self, category: str) -> List[Dict]:
        """Return all questions belonging to a given category."""
        return [q for q in self._questions if q.get("category", "").lower() == category.lower()]

    def count(self) -> int:
        """Return the number of loaded questions."""
        return len(self._questions)
