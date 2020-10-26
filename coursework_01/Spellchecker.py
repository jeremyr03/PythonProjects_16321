# Modules to be imported
import sys


# Class to format printed text
class Format:
    end = '\033[0m'
    underline = '\033[4m'


# Main menu
def menu():
    choice_made = False
    print("Spellchecker by Jeremy Roe")
    while not choice_made:
        user_input = input(Format.underline + "Menu page\n\n" + Format.end +
                           "\t1:\tSpell check sentence\n" +
                           "\t2:\tSpell check file\n" +
                           "\t0:\tQuit program\n")

        if int(user_input) == 1:
            pass
        elif int(user_input) == 2:
            pass
        elif int(user_input) == 0:
            print("Spellchecker closed")
            sys.exit()
        else:
            print("invalid choice, try again")


menu()
