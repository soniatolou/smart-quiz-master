from question_provider import QuestionProvider
from score_tracker import ScoreTracker
from validator import Validator


class GameEngine:
    """
    Orchestrates a quiz session.

    Dependencies are injected via the constructor (Dependency Injection),
    which makes each class easy to mock in unit tests.
    """

    def __init__(
        self,
        question_provider: QuestionProvider,
        score_tracker: ScoreTracker,
        validator: Validator,
    ):
        self.question_provider = question_provider
        self.score_tracker = score_tracker
        self.validator = validator

    def run(self) -> None:
        """Run a full quiz session in the console."""
        print("=" * 50)
        print("       Welcome to Smart Quiz Master!")
        print("=" * 50)

        raw_name = input("Enter your name: ")
        player_name = self.validator.validate_player_name(raw_name)

        self.question_provider.load_questions()
        questions = self.question_provider.get_all_questions()

        if not questions:
            print("No questions available. Exiting.")
            return

        self.score_tracker.reset()

        for i, question in enumerate(questions, start=1):
            print(f"\nQuestion {i}/{len(questions)}: {question['question']}")
            for idx, option in enumerate(question["options"], start=1):
                print(f"  {idx}. {option}")

            answer_index = self._get_valid_answer(len(question["options"]))

            if answer_index == question["correct_index"]:
                print("Correct!")
                self.score_tracker.add_correct()
            else:
                correct_text = question["options"][question["correct_index"]]
                print(f"Wrong. The correct answer was: {correct_text}")
                self.score_tracker.add_incorrect()

        self._show_results(player_name)

    def _get_valid_answer(self, num_options: int) -> int:
        """Prompt the player until a valid answer is given."""
        self.validator.num_options = num_options
        while True:
            raw = input("Your answer (enter number): ")
            try:
                return self.validator.validate_answer(raw)
            except ValueError as e:
                print(f"Invalid input: {e}")

    def _show_results(self, player_name: str) -> None:
        """Display the final results and save the high score."""
        score = self.score_tracker.get_score()
        total = self.score_tracker.get_total()
        pct = self.score_tracker.get_percentage()

        print("\n" + "=" * 50)
        print(f"Game over, {player_name}!")
        print(f"Score: {score}/{total}  ({pct:.1f}%)")
        print("=" * 50)

        self.score_tracker.save_highscore(player_name)
        print("Your score has been saved.")

        print("\nHigh Scores:")
        for rank, entry in enumerate(self.score_tracker.get_highscores(), start=1):
            print(f"  {rank}. {entry['player']} – {entry['score']}/{entry['total']} ({entry['percentage']}%)")
