import json
import os
from typing import List, Dict


class ScoreTracker:
    """Tracks score during a game session and persists high scores to a file."""

    def __init__(self, highscore_file: str = "highscores.json"):
        self.highscore_file = highscore_file
        self._score: int = 0
        self._total_questions: int = 0

    def reset(self) -> None:
        """Reset the current session score."""
        self._score = 0
        self._total_questions = 0

    def add_correct(self) -> None:
        """Register a correct answer."""
        if self._score < 0:
            raise ValueError("Score is in an invalid negative state.")
        self._score += 1
        self._total_questions += 1

    def add_incorrect(self) -> None:
        """Register an incorrect answer."""
        self._total_questions += 1

    def get_score(self) -> int:
        """Return the current score."""
        return self._score

    def get_total(self) -> int:
        """Return the total number of questions answered."""
        return self._total_questions

    def get_percentage(self) -> float:
        """Return the score as a percentage (0.0 – 100.0)."""
        if self._total_questions == 0:
            return 0.0
        return (self._score / self._total_questions) * 100

    def save_highscore(self, player_name: str) -> None:
        """Append the current result to the high scores file."""
        if self._score < 0:
            raise ValueError("Cannot save a negative score.")

        entry: Dict = {
            "player": player_name,
            "score": self._score,
            "total": self._total_questions,
            "percentage": round(self.get_percentage(), 1),
        }

        scores = self._load_highscores()
        scores.append(entry)
        scores.sort(key=lambda x: x["score"], reverse=True)

        with open(self.highscore_file, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2, ensure_ascii=False)

    def get_highscores(self) -> List[Dict]:
        """Return the sorted list of high scores."""
        return self._load_highscores()

    def _load_highscores(self) -> List[Dict]:
        if not os.path.exists(self.highscore_file):
            return []
        with open(self.highscore_file, "r", encoding="utf-8") as f:
            return json.load(f)
