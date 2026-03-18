class Validator:
    """Validates player input during the quiz."""

    def __init__(self, num_options: int = 4):
        self.num_options = num_options

    def validate_answer(self, raw_input: str) -> int:
        """
        Validate that the input is a number between 1 and num_options (inclusive).

        Returns the 0-based index on success.
        Raises ValueError with a descriptive message on failure.
        """
        if raw_input is None or raw_input.strip() == "":
            raise ValueError("Input cannot be empty. Please enter a number.")

        stripped = raw_input.strip()

        if not stripped.isdigit():
            raise ValueError(f"'{stripped}' is not a valid number. Please enter a number.")

        choice = int(stripped)

        if choice < 1 or choice > self.num_options:
            raise ValueError(
                f"Choice {choice} is out of range. Please enter a number between 1 and {self.num_options}."
            )

        return choice - 1  # convert to 0-based index

    def validate_player_name(self, name: str) -> str:
        """
        Validate that the player name is non-empty and not too long.

        Returns the stripped name on success.
        Raises ValueError on failure.
        """
        if name is None or name.strip() == "":
            raise ValueError("Player name cannot be empty.")

        stripped = name.strip()

        if len(stripped) > 30:
            raise ValueError("Player name must be 30 characters or fewer.")

        return stripped
