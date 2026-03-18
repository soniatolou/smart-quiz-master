from question_provider import QuestionProvider
from score_tracker import ScoreTracker
from validator import Validator
from game_engine import GameEngine


def main():
    # Dependency Injection: create each component and wire them together
    provider = QuestionProvider(filepath="questions.json")
    tracker = ScoreTracker(highscore_file="highscores.json")
    validator = Validator(num_options=4)

    engine = GameEngine(
        question_provider=provider,
        score_tracker=tracker,
        validator=validator,
    )

    engine.run()


if __name__ == "__main__":
    main()
