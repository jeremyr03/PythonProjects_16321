# Modules to be imported
import sys
import time
from difflib import SequenceMatcher
from datetime import datetime


# Class to format printed text
class Format:
    end = '\033[0m'
    underline = '\033[4m'
    bold = '\033[1m'


class Statistics:

    def __init__(self):
        self.total_words = 0
        self.correct_sp = 0
        self.incorrect_sp = 0
        self.words_added = 0
        self.suggested = 0
        self.date_time = datetime(1999, 12, 31)
        self.time_elapsed = 0


# Main menu
def init():
    global stats
    # Creating the menu
    print("Spellchecker by Jeremy Roe".center(40, '-'))
    time.sleep(0.5)
    print("Setting up...", end='')
    for i in range(8):
        print(".", end="")
        time.sleep(0.4)

    while 1:
        user_input = input(f"\n\n{Format.underline}Menu page{Format.end}\n\n" +
                           "\t1:\tSpell check sentence\n" +
                           "\t2:\tSpell check file\n" +
                           "\t0:\tQuit program\n\n" +
                           "input:")

        # Runs subroutine appropriate to user choice
        # Numbered choices are turned into string in case user doesn't type an integer
        if user_input == str(1):
            start = datetime.now()
            # Run procedure to check sentence
            sentence_check()
            stats.date_time = datetime.now()
            # Time elapsed calculated using start and end
            stats.time_elapsed = stats.date_time - start
            # Print statistics
            print(f"Total number of words:\t{stats.total_words}\n" +
                  f"Number of words spelt correctly:\t{stats.correct_sp}\n" +
                  f"Number of words spelt incorrectly:\t{stats.incorrect_sp}\n" +
                  f"Words changed with suggested spelling:\t{stats.suggested}\n" +
                  f"Time and date spellchecked:\t{stats.date_time}\n" +
                  f"Time elapsed through spellcheck:\t{stats.time_elapsed}\n")
        elif user_input == str(2):
            file_check()
        elif user_input == str(0):
            print("Spellchecker closed")
            sys.exit()  # Stops execution of code
        else:
            print("invalid choice, try again")


def separate_words(line):

    # Splits words up into array
    words = line.split()
    print(words)

    # Removes anything that is not the alphabet
    for idx, val in enumerate(words):
        new_word = ""
        for j in val:
            if 97 <= ord(j.lower()) <= 122:
                new_word += j
        words[idx] = new_word
        yield new_word


def sentence_check():
    user_input = input("Enter your sentence:\n")
    user_sentence = [word for word in separate_words(user_input)]
    # Total word count
    stats.total_words = len(user_sentence)
    # Checks each word
    for idx, word in enumerate(user_sentence):
        if word.lower() not in dictionary:
            print(Format.bold + word + Format.end, end=" ")
            user_sentence[idx] = incorrect(word)
        else:
            stats.correct_sp += 1
            print(word)
        time.sleep(0.1)


def incorrect(word):
    while True:
        user_input = input("Spelling error found. Would you like to\n" +
                           "1:\tignore\n" +
                           "2:\tmark\n" +
                           "3:\tadd to dictionary\n" +
                           "4:\tsuggest spelling\n")

        if user_input == str(1):
            print(f"{word} is ignored")
            stats.incorrect_sp += 1
            return word
        elif user_input == str(2):
            print("The word is marked")
            stats.incorrect_sp += 1
            return f"??{word}??"
        elif user_input == str(3):
            dictionary.append(word)
            stats.correct_sp += 1
            return word
        elif user_input == str(4):
            return suggestion(word)
        else:
            input("Invalid choice. Press Enter to continue...")


def suggestion(word):
    suggested = ''
    highest_match = 0
    for suggested_word in dictionary:
        if SequenceMatcher(None, word, suggested_word).ratio() > 0.5 > highest_match:
            suggested = suggested_word
            highest_match = SequenceMatcher(None, word, suggested_word).ratio()
            print(suggested, highest_match)
    if highest_match > 0:
        user_input = input(f"Did you mean {suggested}? \nY/N...")
        if user_input.upper() == "Y":
            input("Word changed. Press anywhere to continue...")
            stats.correct_sp += 1
            stats.suggested += 1
            return suggested
        else:
            input("Word not changed. Press anywhere to continue...")
            stats.incorrect_sp += 1
            return word
    else:
        input("no suggestion found. Press anywhere to continue...")
        stats.incorrect_sp += 1
        return word


def file_check():
    pass


dictionary = []
# Upload all English Words to array
file = open("EnglishWords.txt", "r")
for lines in file:
    dictionary.append(lines.strip())
file.close()
stats = Statistics()

init()
