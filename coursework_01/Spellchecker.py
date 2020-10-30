# Modules to be imported
import sys
import time
from difflib import SequenceMatcher
from datetime import datetime
import os


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
    # Creating the menu
    print("Spellchecker by Jeremy Roe".center(40, '-'))
    time.sleep(0.5)
    print("Setting up...", end='')
    for i in range(8):
        print(".", end="")
        time.sleep(0.4)

    while 1:
        print("\n" + "-".center(40, '-'))
        user_input = input(f"Welcome {os.getlogin()}" +
                           f"\n\n{Format.underline}Menu page{Format.end}\n\n" +
                           "\t1:\tSpell check sentence\n" +
                           "\t2:\tSpell check file\n" +
                           "\t0:\tQuit program\n\n" +
                           "input:")

        # Runs subroutine appropriate to user choice
        # Numbered choices are turned into string in case user doesn't type an integer
        selection_made = False
        while not selection_made:
            if user_input == str(1):
                selection_made = True
                stats.append(Statistics())
                start = datetime.now()
                # Run procedure to check sentence
                sentence_check()
                stats[len(stats)-1].date_time = datetime.now()
                # Time elapsed calculated using stats and end
                stats[len(stats)-1].time_elapsed = stats[len(stats)-1].date_time - start
                # Print statistics
                print(f"Total number of words:\t{stats[len(stats)-1].total_words}\n" +
                      f"Number of words spelt correctly:\t{stats[len(stats)-1].correct_sp}\n" +
                      f"Number of words spelt incorrectly:\t{stats[len(stats)-1].incorrect_sp}\n" +
                      f"Words changed with suggested spelling:\t{stats[len(stats)-1].suggested}\n" +
                      f"Time and date spellchecked:\t{stats[len(stats)-1].date_time}\n" +
                      f"Time elapsed through spellcheck:\t{str(stats[len(stats)-1].time_elapsed)[:11]}\n")
                input("Press enter to continue...")

            elif user_input == str(2):
                selection_made = True
                stats.append(Statistics())
                start = datetime.now()
                # Run procedure to check sentence
                file_check()
                stats[len(stats)-1].date_time = datetime.now()
                # Time elapsed calculated using stats and end
                stats[len(stats)-1].time_elapsed = stats[len(stats)-1].date_time - start
                # Print statistics
                print(f"Total number of words:\t{stats[len(stats)-1].total_words}\n" +
                      f"Number of words spelt correctly:\t{stats[len(stats)-1].correct_sp}\n" +
                      f"Number of words spelt incorrectly:\t{stats[len(stats)-1].incorrect_sp}\n" +
                      f"Words changed with suggested spelling:\t{stats[len(stats)-1].suggested}\n" +
                      f"Time and date spellchecked:\t{stats[len(stats)-1].date_time}\n" +
                      f"Time elapsed through spellcheck:\t{str(stats[len(stats)-1].time_elapsed)[:11]}\n")
                input("Press enter to continue...")

            elif user_input == str(0):
                print("Spellchecker closed")
                sys.exit()  # Stops execution of code

            else:
                print("invalid choice, try again")
                user_input = input("input:")


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
    stats[len(stats)-1].total_words = len(user_sentence)
    # Checks each word
    for idx, word in enumerate(user_sentence):
        if word.lower() not in dictionary:
            print(Format.bold + word + Format.end, end=" ")
            user_sentence[idx] = incorrect(word)
        else:
            stats[len(stats)-1].correct_sp += 1
            print(word)
        time.sleep(0.1)


def incorrect(word):
    user_input = input("Spelling error found. Would you like to\n" +
                       "1:\tignore\n" +
                       "2:\tmark\n" +
                       "3:\tadd to dictionary\n" +
                       "4:\tsuggest spelling\n")

    while True:
        if user_input == str(1):
            print(f"{word} is ignored")
            stats[len(stats)-1].incorrect_sp += 1
            return word
        elif user_input == str(2):
            print("The word is marked")
            stats[len(stats)-1].incorrect_sp += 1
            return f"??{word}??"
        elif user_input == str(3):
            dictionary.append(word)
            stats[len(stats)-1].correct_sp += 1
            return word
        elif user_input == str(4):
            return suggestion(word)
        else:
            input("Invalid choice. Press Enter to continue...")


def suggestion(word):
    suggested = ''
    highest_match = 0
    for suggested_word in dictionary:
        match = SequenceMatcher(None, word, suggested_word).ratio()
        if match > highest_match and match > 0.5:
            suggested = suggested_word
            highest_match = match
            print(suggested, highest_match)
    if highest_match > 0:
        user_input = input(f"Did you mean {suggested}? \nY/N...")
        if user_input.upper() == "Y":
            input("Word changed. Press anywhere to continue...")
            stats[len(stats)-1].correct_sp += 1
            stats[len(stats)-1].suggested += 1
            return suggested
        else:
            input("Word not changed. Press anywhere to continue...")
            stats[len(stats)-1].incorrect_sp += 1
            return word
    else:
        input("no suggestion found. Press anywhere to continue...")
        stats[len(stats)-1].incorrect_sp += 1
        return word


def file_check():
    done = False
    while not done:
        filename = input("\nEnter the file name:")
        user_file = read_file(filename)
        done = True
        print(user_file)
        # Total word count
        stats[len(stats) - 1].total_words = len(user_file)
        # Checks each word
        for idx, word in enumerate(user_file):
            if word.lower() not in dictionary:
                print(Format.bold + word + Format.end, end=" ")
                user_file[idx] = incorrect(word)
            else:
                stats[len(stats) - 1].correct_sp += 1
                print(word)
            time.sleep(0.1)


def read_file(filename):
    temp_array = []
    try:
        file = open(filename, "r")
        for idx, lines in enumerate(file):
            for i in separate_words(lines):
                temp_array.append(i)
        file.close()
        print(temp_array)
        return temp_array
    except FileNotFoundError:
        input("error. File not found. Press to continue")


# Upload all English Words to array
dictionary = read_file("EnglishWords.txt")
stats = []
init()
