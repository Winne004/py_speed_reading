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

    def test_single_vowel_word(self):
        single_vowel_instance = BuildSpeedReadingString("apple")
        self.assertEqual(str(single_vowel_instance), "  apple")
        self.assertEqual(single_vowel_instance.prominent_vowel, 3)

    def test_empty_word(self):
        with self.assertRaises(ValueError) as context:
            empty_instance = BuildSpeedReadingString("")
        self.assertEqual(str(context.exception), "Input word cannot be empty")


if __name__ == '__main__':
    unittest.main()

