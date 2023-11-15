import os
import time
import requests
import re
from colorama import Fore, Style

HTML_TAG_REGEX = re.compile("<.*?>")

class bcolors:
    Red = "\033[91m"
    Green = "\033[92m"
    Blue = "\033[94m"
    Cyan = "\033[96m"
    White = "\033[97m"
    Yellow = "\033[93m"
    Magenta = "\033[95m"
    Grey = "\033[90m"
    Black = "\033[90m"
    Default = "\033[99m"
    UNDERLINE = "\033[4m"
    ENDC = "\033[0m"


class BuildSpeedReadingString:
    VOWELS = {"a", "e", "i", "o", "u"}

    def __init__(self, word: str) -> None:
        self.word = word
        self.word_length = len(word)
        self.prominent_vowel = 0
        self.offset = 0

        if self.word_length <= 3:
            self.process_short_word()
        else:
            self.process_long_word()

        self.prominent_vowel += self.offset

    def __str__(self) -> str:
        try:
            columns = os.get_terminal_size().columns
        except OSError:
            columns = 80  # Default value if terminal size cannot be obtained

        formatted_word = (
            f"{self.word[:self.prominent_vowel]}{bcolors.Red}{bcolors.UNDERLINE}"
            f"{self.word[self.prominent_vowel]}{bcolors.ENDC}{self.word[self.prominent_vowel+1:]}"
        )

        return formatted_word.center(columns)

    def process_short_word(self) -> None:
        """Process a short word."""
        self.prominent_vowel = self.find_first_vowel()
        self.word, self.offset = self.pad_string()

    def process_long_word(self) -> None:
        """Process a long word."""
        self.prominent_vowel = self.find_first_vowel(1)
        self.word, self.offset = self.pad_string()

    def pad_string(self) -> tuple:
        """Pad a string with spaces based on the position of its first vowel."""
        offset = len(self.word[self.prominent_vowel + 1 :]) - len(
            self.word[: self.prominent_vowel]
        )
        return " " * offset + self.word, offset

    def find_first_vowel(self, start=0) -> int:
        """Find the position of the first vowel in a word, starting from the given index."""
        mid = len(self.word) // 2
        prominent_vowel = start
        while self.word[prominent_vowel] not in self.VOWELS and prominent_vowel < mid - 1:
            prominent_vowel += 1
        return prominent_vowel


def clean_html(raw_html: str) -> str:
    """Remove HTML tags from a string."""
    return re.sub(HTML_TAG_REGEX, "", raw_html)


def generate_word_list(text: str) -> list:
    """Generate a list of alphanumeric words from the given text."""
    return [char.lower() for char in text.split() if char.isalnum()]


if __name__ == "__main__":
    try:
        response = requests.get(
            "https://editorial.digitalcontent.sky/articles/12905218.json"
        )
        response.raise_for_status()
        body = response.json()["body"]
    except requests.RequestException as e:
        print(f"Error retrieving content: {e}")
        exit(1)

    os.system("cls" if os.name == "nt" else "clear")
    columns = os.get_terminal_size().columns
    print("hello world".center(columns))

    word_list = generate_word_list(clean_html(body))
    for word in word_list:
        print(BuildSpeedReadingString(word))
        time.sleep(0.1)
        os.system("cls" if os.name == "nt" else "clear")
