"""Py Speed Reader

"""
import argparse
import os
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
import re
import requests


class bcolors:
    Red = "\033[91m"
    UNDERLINE = "\033[4m"
    ENDC = "\033[0m"


class BuildSpeedReadingString:
    """
    A class for generating speed reading strings by adding spaces based on the position of the first
    vowel.

    Attributes:
    - original_word (str): The original word provided during initialization.
    - word (str): The processed word with added spaces for speed reading.
    - word_length (int): The length of the original word.
    - prominent_vowel (int): The index of the first prominent vowel in the word.
    - offset (int): The number of spaces added to the word.

    Methods:
    - __init__(self, word: str): Initializes the speed reading string with the given word.
    - __str__(self) -> str: Returns the processed speed reading string.
    - process_short_word(self) -> None: Processes a short word by finding the first vowel and
      adding spaces.
    - process_long_word(self) -> None: Processes a long word by finding the first vowel after [0]
      and adding spaces.
    - pad_string(self) -> tuple: Pads the string with spaces based on the position of its
      first vowel.
    - find_first_vowel(self, start=0) -> int: Finds the position of the first vowel in a word,
      starting from the given index.
    """

    VOWELS = {"a", "e", "i", "o", "u"}

    def __init__(self, word: str) -> None:
        if not word:
            raise ValueError("Input word cannot be empty")

        self.original_word = word
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
        return self.word

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
        while (
            self.word[prominent_vowel] not in self.VOWELS and prominent_vowel < mid - 1
        ):
            prominent_vowel += 1
        return prominent_vowel


class SpeedRead(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.grid(row=4, column=2)
        self.var = StringVar()

        Label(self, text="", font="Courier 17 bold", anchor="center").grid(
            row=0, column=0, padx=50
        )
        Label(self, text="", font="Courier 17 bold", anchor="center").grid(
            row=0, column=2, padx=50
        )
        Label(
            self, textvariable=self.var, font="Courier 17 bold", anchor="s", width=50
        ).grid(row=1, column=1)
        Label(
            self,
            text="|",
            font="Courier 17 bold",
            foreground="red",
            anchor="n",
            width=50,
            fg="red",
        ).grid(row=0, column=1)
        Label(
            self,
            text="|",
            font="Courier 17 bold",
            foreground="red",
            anchor="n",
            width=50,
            fg="red",
        ).grid(row=2, column=1)
        ttk.Button(self, text="Quit", command=self.master.destroy).grid(row=3, column=1)


class PrintToTerminal:
    @staticmethod
    def print_to_terminal(word):
        columns = os.get_terminal_size().columns
        print(PrintToTerminal.format_string_for_printing(word).center(columns))
        time.sleep(0.1)
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def format_string_for_printing(word):
        formatted_word = (
            f"{word.word[:word.prominent_vowel]}{bcolors.Red}{bcolors.UNDERLINE}"
            f"{word.word[word.prominent_vowel]}{bcolors.ENDC}{word.word[word.prominent_vowel+1:]}"
        )

        return formatted_word


class ArticleGetter:
    ARTICLE_URL = "https://editorial.digitalcontent.sky/articles/12905218.json"
    HTML_TAG_REGEX = re.compile(r"<.*?>")  # Compile the regex for better performance

    @staticmethod
    def get_article_body():
        try:
            response = requests.get(ArticleGetter.ARTICLE_URL, timeout=10)
            response.raise_for_status()
            body = response.json().get("body", "")

        except requests.RequestException as e:
            print(f"Error retrieving content: {e}")
            return None

        return ArticleGetter.generate_word_list(ArticleGetter.clean_html(body))

    @staticmethod
    def clean_html(raw_html: str) -> str:
        """Remove HTML tags from a string."""
        return re.sub(ArticleGetter.HTML_TAG_REGEX, "", raw_html)

    @staticmethod
    def generate_word_list(text: str) -> list:
        """Generate a list of alphanumeric words from the given text."""
        return [char.lower() for char in text.split() if char.isalnum()]


class OutputHelper:
    @staticmethod
    def print_to_UI_helper(word_list):
        def display_word(root, var, word):
            result = BuildSpeedReadingString(word)
            var.set(str(result))
            root.update()
            time.sleep(0.1)

        root = tk.Tk()
        app = SpeedRead(master=root)

        for word in word_list:
            display_word(root, app.var, word)

        root.mainloop()

    @staticmethod
    def print_to_terminal_helper(word_list):
        os.system("cls" if os.name == "nt" else "clear")
        for word in word_list:
            word = BuildSpeedReadingString(word)
            PrintToTerminal.print_to_terminal(word)


def main():
    parser = argparse.ArgumentParser(description="Print or display output.")
    # parser.add_argument("text", help="Text to be displayed or printed.")
    parser.add_argument(
        "--output-type",
        choices=["terminal", "ui"],
        default="ui",
        help="Choose output type: terminal or ui (default: terminal).",
    )

    args = parser.parse_args()
    word_list = ArticleGetter.get_article_body()

    if args.output_type == "terminal":
        OutputHelper.print_to_terminal_helper(word_list)

    elif args.output_type == "ui":
        OutputHelper.print_to_UI_helper(word_list)


if __name__ == "__main__":
    main()
