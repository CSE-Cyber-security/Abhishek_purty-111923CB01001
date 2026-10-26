"""Behavior checks for password criteria and the interactive checker."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from password_checker import analyze_password, main


ROOT = Path(__file__).resolve().parents[1]
CRITERIA = ["Length", "Uppercase", "Lowercase", "Numbers", "Symbols"]


class PasswordAnalysisTests(unittest.TestCase):
    def test_examples_report_each_criterion(self):
        for password, expected_checks, expected_strength in (
            ("Abc123", [False, True, True, True, False], "Moderate"),
            ("password", [True, False, True, False, False], "Weak"),
            ("Hello@123", [True, True, True, True, True], "Strong"),
        ):
            with self.subTest(password=password):
                checks, strength = analyze_password(password)
                self.assertEqual(list(checks), CRITERIA)
                self.assertEqual(list(checks.values()), expected_checks)
                self.assertTrue(all(type(value) is bool for value in checks.values()))
                self.assertEqual(strength, expected_strength)

    def test_length_requires_eight_characters(self):
        seven_checks, seven_strength = analyze_password("Abc123!")
        eight_checks, eight_strength = analyze_password("Abc123!x")
        self.assertFalse(seven_checks["Length"])
        self.assertTrue(eight_checks["Length"])
        self.assertEqual(seven_strength, "Moderate")
        self.assertEqual(eight_strength, "Strong")

    def test_strength_boundaries_from_zero_to_five_checks(self):
        for password, score, expected in (
            ("", 0, "Weak"), ("a", 1, "Weak"), ("aA", 2, "Weak"),
            ("aA1", 3, "Moderate"), ("aA1!", 4, "Moderate"),
            ("aA1!aaaa", 5, "Strong"),
        ):
            with self.subTest(score=score):
                checks, strength = analyze_password(password)
                self.assertEqual(sum(checks.values()), score)
                self.assertEqual(strength, expected)

    def test_non_ascii_characters_do_not_count_as_ascii_categories(self):
        for password in ("Éé١💡", "Ａａ１🦀"):
            with self.subTest(password=password):
                checks, strength = analyze_password(password)
                self.assertEqual(checks, dict.fromkeys(CRITERIA, False))
                self.assertEqual(strength, "Weak")
        checks, strength = analyze_password("é" * 8)
        self.assertEqual(list(checks.values()), [True, False, False, False, False])
        self.assertEqual(strength, "Weak")

    def test_whitespace_counts_toward_length_but_is_not_a_symbol(self):
        checks, strength = analyze_password(" Abc12  ")
        self.assertEqual(list(checks.values()), [True, True, True, True, False])
        self.assertEqual(strength, "Moderate")
        checks, strength = analyze_password(" " * 8)
        self.assertEqual(list(checks.values()), [True, False, False, False, False])
        self.assertEqual(strength, "Weak")

    def test_ascii_punctuation_counts_as_symbols(self):
        for symbol in ("!", "_", "\\", "`", "\"", "~"):
            with self.subTest(symbol=symbol):
                checks, strength = analyze_password(symbol)
                self.assertEqual(list(checks.values()), [False, False, False, False, True])
                self.assertEqual(strength, "Weak")


class PasswordCommandLineTests(unittest.TestCase):
    def run_checker(self, input_text):
        return subprocess.run(
            [sys.executable, str(ROOT / "password_checker.py")],
            input=input_text, text=True, capture_output=True, cwd=ROOT, timeout=10,
        )

    def test_initial_exit_is_case_insensitive(self):
        result = self.run_checker("ExIt\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("=== Password Strength Checker ===", result.stdout)
        self.assertIn("Enter your password (or type 'exit' to quit):", result.stdout)
        self.assertNotIn("Password Strength:", result.stdout)

    def test_repeating_displays_both_results_and_exact_status_labels(self):
        result = self.run_checker("Abc123\ny\npassword\nn\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("Password Strength:"), 2)
        first = result.stdout.index("Password Strength: Moderate")
        second = result.stdout.index("Password Strength: Weak")
        self.assertLess(first, second)
        for line in (
            "Length: Not satisfied", "Uppercase: Satisfied", "Lowercase: Satisfied",
            "Numbers: Satisfied", "Symbols: Not satisfied", "Length: Satisfied",
            "Uppercase: Not satisfied", "Numbers: Not satisfied",
        ):
            self.assertIn(line, result.stdout)

    def test_invalid_repeat_reply_is_reprompted_without_analysis(self):
        result = self.run_checker("Abc123\nmaybe\nnope\nn\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("Password Strength:"), 1)
        self.assertEqual(result.stdout.count("(y/n):"), 3)
        self.assertIn("Please enter y or n.", result.stdout)

    def test_empty_password_is_evaluated_as_weak(self):
        result = self.run_checker("\nn\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        for label in CRITERIA:
            self.assertIn(f"{label}: Not satisfied", result.stdout)
        self.assertIn("Password Strength: Weak", result.stdout)

    def test_password_input_preserves_surrounding_spaces(self):
        result = self.run_checker(" Abc12  \nn\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Length: Satisfied", result.stdout)
        self.assertIn("Symbols: Not satisfied", result.stdout)
        self.assertIn("Password Strength: Moderate", result.stdout)

    def test_surrounding_spaces_make_exit_an_ordinary_password(self):
        result = self.run_checker(" exit \nn\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Lowercase: Satisfied", result.stdout)
        self.assertIn("Password Strength: Weak", result.stdout)

    def test_exit_at_repeat_prompt_quits(self):
        result = self.run_checker("Abc123\nExIt\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("Password Strength:"), 1)
        self.assertNotIn("Please enter y or n.", result.stdout)

    def test_eof_is_clean_at_password_and_repeat_prompts(self):
        for input_text in ("", "Abc123\n", "Abc123\ny\n"):
            with self.subTest(input_text=input_text):
                result = self.run_checker(input_text)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_keyboard_interrupt_is_clean_at_each_prompt(self):
        for responses in ([KeyboardInterrupt], ["Abc123", KeyboardInterrupt]):
            with self.subTest(responses=responses):
                output = StringIO()
                with patch("builtins.input", side_effect=responses), redirect_stdout(output):
                    self.assertEqual(main(), 0)
                self.assertNotIn("Traceback", output.getvalue())


if __name__ == "__main__":
    unittest.main()
