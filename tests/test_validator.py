import pytest
from validator import Validator


class TestValidator:

    def setup_method(self):
        self.validator = Validator(num_options=4)

    # --- validate_answer ---

    def test_valid_answer_lower_bound(self):
        """Input '1' should return index 0."""
        assert self.validator.validate_answer("1") == 0

    def test_valid_answer_upper_bound(self):
        """Input '4' should return index 3."""
        assert self.validator.validate_answer("4") == 3

    def test_valid_answer_with_whitespace(self):
        """Input with surrounding spaces should still be accepted."""
        assert self.validator.validate_answer("  2  ") == 1

    def test_empty_string_raises(self):
        """Empty input should raise ValueError."""
        with pytest.raises(ValueError, match="empty"):
            self.validator.validate_answer("")

    def test_whitespace_only_raises(self):
        """Whitespace-only input should raise ValueError."""
        with pytest.raises(ValueError, match="empty"):
            self.validator.validate_answer("   ")

    def test_none_input_raises(self):
        """None input should raise ValueError."""
        with pytest.raises(ValueError):
            self.validator.validate_answer(None)

    def test_letter_input_raises(self):
        """Non-numeric input should raise ValueError."""
        with pytest.raises(ValueError, match="not a valid number"):
            self.validator.validate_answer("a")

    def test_out_of_range_high_raises(self):
        """Input above num_options should raise ValueError."""
        with pytest.raises(ValueError, match="out of range"):
            self.validator.validate_answer("5")

    def test_out_of_range_zero_raises(self):
        """Input '0' should raise ValueError (below 1)."""
        with pytest.raises(ValueError, match="out of range"):
            self.validator.validate_answer("0")

    def test_negative_number_raises(self):
        """Negative numbers should raise ValueError."""
        with pytest.raises(ValueError):
            self.validator.validate_answer("-1")

    # --- validate_player_name ---

    def test_valid_name(self):
        """A normal name should be returned stripped."""
        assert self.validator.validate_player_name("  Alice  ") == "Alice"

    def test_empty_name_raises(self):
        """Empty name should raise ValueError."""
        with pytest.raises(ValueError, match="empty"):
            self.validator.validate_player_name("")

    def test_none_name_raises(self):
        """None name should raise ValueError."""
        with pytest.raises(ValueError):
            self.validator.validate_player_name(None)

    def test_name_too_long_raises(self):
        """Name longer than 30 characters should raise ValueError."""
        with pytest.raises(ValueError, match="30 characters"):
            self.validator.validate_player_name("A" * 31)

    def test_name_exactly_30_chars_is_valid(self):
        """Name of exactly 30 characters should be accepted."""
        name = "A" * 30
        assert self.validator.validate_player_name(name) == name
