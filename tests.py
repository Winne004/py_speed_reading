import unittest
import os
from main import BuildSpeedReadingString, bcolors


class TestBuildSpeedReadingString(unittest.TestCase):
    def test_short_word(self):
        word = "cat"
        speed_reader = BuildSpeedReadingString(word)
        expected_output = "  cat"
        self.assertEqual(str(speed_reader), expected_output)

    def test_long_word(self):
        word = "elephant"
        speed_reader = BuildSpeedReadingString(word)
        expected_output = "   elephant"
        self.assertEqual(str(speed_reader), expected_output)

    def test_word_with_no_vowels(self):
        word = "rhythm"
        speed_reader = BuildSpeedReadingString(word)
        expected_output = " rhythm"
        self.assertEqual(str(speed_reader), expected_output)


if __name__ == "__main__":
    unittest.main()
