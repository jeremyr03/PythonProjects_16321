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
    red = '\033[1;31m'
    blue = '\033[1;34m'
    green = '\033[0;32m'
    cyan = '\033[1;36m'


# Class for details of spellchecker
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
    print(f"{Format.cyan}Spellchecker by Jeremy Roe{Format.end}".center(60, f'-'))
    time.sleep(0.5)
    print("Setting up...", end='')
    for i in range(8):
        print(".", end="")
        time.sleep(0.4)

    while 1:
        # Prints menu
        print("\n" + Format.blue + '-'.center(50, '-') + Format.end)
        user_input = input("\n" + f"{Format.underline}Welcome {os.getlogin()}{Format.end}".center(50) +
                           f"\n\n{Format.underline}Menu page{Format.end}\n\n" +
                           "\t1:\tSpell check sentence\n" +
                           "\t2:\tSpell check file\n" +
                           "\t0:\tQuit program\n\n" +
                           "input:")

        # Runs subroutine appropriate to user choice
        # Numbered choices are turned into string in case user doesn't type an integer
        selection_made = False
        while not selection_made:
            # Sentence Check
            if user_input == str(1):
                selection_made = True
                print(Format.blue + '-'.center(50, '-') + Format.end)
                # Create new instance of spellchecker statistics
                stats.append(Statistics())
                stats[len(stats) - 1].date_time = datetime.now()
                # Run procedure to check sentence
                sentence_check()
                # Time elapsed calculated
                stats[len(stats) - 1].time_elapsed = datetime.now() - stats[len(stats) - 1].date_time
                # Print statistics
                print("Total number of words:".ljust(37) + f"\t{stats[len(stats) - 1].total_words}\n" +
                      "Number of words spelt correctly:".ljust(37) + f"\t{stats[len(stats) - 1].correct_sp}\n" +
                      "Number of words spelt incorrectly:".ljust(37) + f"\t{stats[len(stats) - 1].incorrect_sp}\n" +
                      "Words changed with suggested spelling:".ljust(37) + f"\t{stats[len(stats) - 1].suggested}\n" +
                      "Time and date spellchecked:".ljust(37) + f"\t{stats[len(stats) - 1].date_time}\n" +
                      "Time elapsed through spellcheck:".ljust(
                          37) + f"\t{str(stats[len(stats) - 1].time_elapsed)[:11]}\n")
                input("Press enter to continue...")

            # File Check
            elif user_input == str(2):
                selection_made = True
                print(Format.blue + '-'.center(50, '-') + Format.end)
                stats.append(Statistics())
                stats[len(stats) - 1].date_time = datetime.now()
                # Run procedure to check sentence
                file_check()
                # Time elapsed calculated
                stats[len(stats) - 1].time_elapsed = datetime.now() - stats[len(stats) - 1].date_time
                # Print statistics
                print(f"Total number of words:\t{stats[len(stats) - 1].total_words}\n" +
                      f"Number of words spelt correctly:\t{stats[len(stats) - 1].correct_sp}\n" +
                      f"Number of words spelt incorrectly:\t{stats[len(stats) - 1].incorrect_sp}\n" +
                      f"Words changed with suggested spelling:\t{stats[len(stats) - 1].suggested}\n" +
                      f"Time and date spellchecked:\t{stats[len(stats) - 1].date_time}\n" +
                      f"Time elapsed through spellcheck:\t{str(stats[len(stats) - 1].time_elapsed)[:11]}\n")
                input("Press enter to continue...")

            # Terminate Program
            elif user_input == str(0):
                print(Format.blue + '-'.center(50, '-') + Format.end)
                print(f"Spellchecker closed\nGoodbye {os.getlogin()}")
                time.sleep(1)
                sys.exit()  # Stops execution of code

            # Validation
            else:
                print("invalid choice, try again")
                user_input = input("input:")


def read_file(filename):
    temp_array = []
    try:
        file = open(filename, "r")
        for idx, lines in enumerate(file):
            for i in separate_words(lines):
                temp_array.append(i)
        file.close()
        return temp_array
    # In the event a file that is not in the same repository/nonexistent file is tried to be opened
    except FileNotFoundError:
        print(f"error. {Format.bold}{filename}{Format.end} not found. Try again")
        return ''


def separate_words(line):
    # Splits words up into array
    words = line.split()

    # Removes anything that is not the alphabet
    for idx, val in enumerate(words):
        new_word = ""
        for j in val:
            if 97 <= ord(j.lower()) <= 122:
                new_word += j
        words[idx] = new_word
        yield new_word


def incorrect(word):
    # Asks user what they would like to do with incorrectly spelt word
    user_input = input("\nSpelling error found. Would you like to\n" +
                       "1:\tignore\n" +
                       "2:\tmark\n" +
                       "3:\tadd to dictionary\n" +
                       "4:\tsuggest spelling\nchoice:")

    # User input is validated
    while True:
        if user_input == str(1):
            # Ignore word
            print(f"{Format.bold}{word}{Format.end} is ignored")
            print(Format.blue + "_".center(20, '_') + Format.end)
            stats[len(stats) - 1].incorrect_sp += 1
            return word
        elif user_input == str(2):
            # Mark word
            print(f"{Format.bold}{word}{Format.end} is marked")
            print(Format.blue + "_".center(20, '_') + Format.end)
            stats[len(stats) - 1].incorrect_sp += 1
            return f"??{word}??"
        elif user_input == str(3):
            # Add word to dictionary
            dictionary.append(word)
            print(f"{user_input} is added to the dictionary")
            print(Format.blue + "_".center(20, '_') + Format.end)
            stats[len(stats) - 1].correct_sp += 1
            return word
        elif user_input == str(4):
            # Suggest alternate spelling
            return suggestion(word)
        else:
            user_input = input("Invalid choice. Try again.\n\nWould you like to\n" +
                               "1:\tignore\n" +
                               "2:\tmark\n" +
                               "3:\tadd to dictionary\n" +
                               "4:\tsuggest spelling\nchoice:")


def suggestion(word):
    suggested = ''
    highest_match = 0
    # Use SequenceMatcher to give a ratio of how close a word is to one in the dictionary
    # The one with the highest ratio is the suggested word
    for suggested_word in dictionary:
        match = SequenceMatcher(None, word, suggested_word).ratio()
        # Assuming that if there is not at least a 0.5 ratio match then there is no suggested word in the library
        if match > highest_match and match > 0.5:
            suggested = suggested_word
            highest_match = match
    if highest_match > 0:
        # Ask user if this is the word they mean
        user_input = input(f"Did you mean {Format.red}{suggested}{Format.end}? \nY/N...")
        if y_or_n(user_input):
            input("Word changed. Press anywhere to continue...")
            print(Format.blue + "_".center(20, '_') + Format.end)
            stats[len(stats) - 1].correct_sp += 1
            stats[len(stats) - 1].suggested += 1
            return suggested
        else:
            input("Word not changed. Press anywhere to continue...")
            print(Format.blue + "_".center(20, '_') + Format.end)
            stats[len(stats) - 1].incorrect_sp += 1
            return word
    # In the event of no suggestion
    else:
        input("no suggestion found. Press anywhere to continue...")
        print(Format.blue + "_".center(20, '_') + Format.end)
        stats[len(stats) - 1].incorrect_sp += 1
        return word


def sentence_check():
    valid_sentence = False
    while not valid_sentence:
        user_input = input("Enter a sentence:\n")
        # Verification that a valid sentence is inputted
        for i in user_input:
            if 97 <= ord(i.lower()) <= 122:
                valid_sentence = True

    print(Format.blue + "_".center(20, '_') + Format.end)
    user_sentence = [word for word in separate_words(user_input)]
    # Total word count
    stats[len(stats) - 1].total_words = len(user_sentence)
    # Checks each word
    for idx, word in enumerate(user_sentence):
        # Incorrectly spelt word
        if word.lower() not in dictionary:
            print(Format.red + word + Format.end)
            user_sentence[idx] = incorrect(word)
        else:
            # Correctly spelt word
            stats[len(stats) - 1].correct_sp += 1
            print(word)
        time.sleep(0.1)
    print("Spellcheck complete".center(50, '-'))
    check_to_file(user_sentence)


def file_check():
    user_file = ''
    # Presence check for file name
    while user_file == '':
        filename = input("Enter the file name (including file extensions)\nFilename:")
        user_file = read_file(filename)

    print("_".center(20, '_'))
    # Total word count
    stats[len(stats) - 1].total_words = len(user_file)
    # Checks each word
    for idx, word in enumerate(user_file):
        if word.lower() not in dictionary:
            # Word incorrectly spelt
            print(f"{Format.red}{word}{Format.end}")
            user_file[idx] = incorrect(word)
        else:
            # Word correctly spelt
            stats[len(stats) - 1].correct_sp += 1
            print(word)
        time.sleep(0.1)

    check_to_file(user_file)


def check_to_file(inp):
    # Time elapsed calculated
    stats[len(stats) - 1].time_elapsed = datetime.now() - stats[len(stats) - 1].date_time
    new_filename = ''
    # Presence check filename
    while new_filename == '':
        new_filename = input("Enter a new file name (no file extension)\nFilename:").strip()
        new_filename += ".txt"
        if new_filename == ".txt":
            print("Nothing entered. Please try again")
            new_filename = ""

    print("Creating new file")
    # Writing to new file
    file = open(new_filename, "w")
    for i in inp:
        file.write(i + " ")
    file.close()
    time.sleep(1)
    input(f"New file created\t{new_filename}. Press enter to continue...")
    print(Format.blue + '-'.center(50, '-') + Format.end)


def y_or_n(inp):
    # Yes
    if inp.lower() in ['y', 'yes', 'yeah', 'yup', 'oui', 'da', 'yuh']:
        return True
    # No
    else:
        return False


# Upload all English Words to array
dictionary = read_file("EnglishWords.txt")
stats = []
init()
