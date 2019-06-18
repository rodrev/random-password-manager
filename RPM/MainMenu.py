from RPM.Data import Data
from RPM.OptionsUI import OptionsUI


class MainMenu:
    def __init__(self, options):
        """ INTERACTIVE MODE """
        menu = {
            "1": Data().new_random_entry,
            "2": Data().new_entry,
            "3": Data().print_random,
            "4": Data().get_entry,
            "5": Data().edit_entry,
            "6": Data().delete_entry,
            "7": Data().print_or_save_all,
            "8": Data().change_all,
            "9": OptionsUI().options_menu,
            "0": self.quit
        }
        i = "dummy"
        while i != "0":  # loop until [quit]
            print(options)
            print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        RANDOM PASSWORD MANAGER
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    [1] New random password entry
    [2] New password entry
    [3] Generate random password
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    [4] Get entry
    [5] Edit entry
    [6] Delete entry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    [7] Print/Save all
    [8] Change all
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    [9] Options
    [0] Quit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""")
            if i not in menu:
                print(i, 'not in menu')
            else:
                print(i, 'in menu')
            while i not in menu:  # ensure valid choice
                i = input()
            menu[i]()
            input("[enter]...\n")  # pause

    @staticmethod
    def quit():
        print("\nGoodbye\n")
