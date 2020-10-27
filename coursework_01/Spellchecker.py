# Modules to be imported
import sys
import time


# Class to format printed text
class Format:
    end = '\033[0m'
    underline = '\033[4m'
    bold = '\033[1m'


# Main menu
def init():
    # Creating the menu
    print("Spellchecker by Jeremy Roe")
    time.sleep(0.5)
    print("Setting up...")
    time.sleep(2)

    while 1:
        user_input = input(Format.underline + "Menu page\n\n" + Format.end +
                           "\t1:\tSpell check sentence\n" +
                           "\t2:\tSpell check file\n" +
                           "\t0:\tQuit program\n\n" +
                           "input:")

        # Runs subroutine appropriate to user choice
        # Numbered choices are turned into string in case user doesn't type an integer
        if user_input == str(1):
            sentence_check()
        elif user_input == str(2):
            file_check()
        elif user_input == str(0):
            print("Spellchecker closed")
            sys.exit()  # Stops execution of code
        else:
            print("invalid choice, try again")


def separate_words(line):
    words = []
    word_start = 0
    word_end = 0
    while word_end != -1:
        # Find where the space is and everything between a space is a word
        word_end = line.find(" ", word_start)
        if word_end == -1:
            # If the end of the sentence doesn't end with a space
            words.append(line[word_start:])
        else:
            words.append(line[word_start:word_end])
        word_start = word_end + 1

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
    print(user_sentence)

    print(user_sentence)
    for word in user_sentence:
        if word not in dictionary:
            print(Format.bold + word + Format.end, end=" ")
            incorrect()
        else:
            print(word, end=" ")
    input("Press Enter to continue...")


def incorrect():
    input("Error found. Press Enter to continue...")


def file_check():
    pass


dictionary = []
# Upload all English Words to array
print("Setting up...")
file = open("EnglishWords.txt", "r")
for line in file:
    dictionary.append(line.strip())
file.close()

init()
