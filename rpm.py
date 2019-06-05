#!/usr/bin/env python3
from random import randint, choice
import os
import shelve
import sys

# Relative path of directory containing this file
REL = os.path.dirname(sys.argv[0])
# Absolute path of directory containing this file
ABS = os.path.abspath(REL)

# File paths to create in this directory:
OPTIONS = ABS + "/opt"  # save options here (bytes)
DATA = ABS + "/dat"  # save data here (bytes)
SAVE = ABS + "/txt"  # save data here with 'Save all' feature (text)


class Options:
    # default options
    emails = [""]
    usernames = [""]
    length = 40
    lrange = 0
    punctuation = "limited"
    punctuation_choices = {
        "all": "!#$%&()*+,-./:;<=>?@[]^_{|}~",
        "some": "%+-./:=@_",
        "limited": "@._-",
        "none": ""
    }
    lowercase = True
    uppercase = True
    numbers = True

    def __init__(self, oshelf, interactive=True):
        if oshelf:  # get options from shelf
            self.emails = oshelf["emails"]
            self.usernames = oshelf["usernames"]
            self.length = oshelf["length"]
            self.lrange = oshelf["lrange"]
            self.punctuation = oshelf["punctuation"]
            self.lowercase = oshelf["lowercase"]
            self.uppercase = oshelf["uppercase"]
            self.numbers = oshelf["numbers"]
        else:  # empty shelf (first run)
            print(f"{OPTIONS} file created with default options\n"
                  "Select [options] to customize\n")
            # save default options to shelf
            oshelf["emails"] = self.emails
            oshelf["usernames"] = self.usernames
            oshelf["length"] = self.length
            oshelf["lrange"] = self.lrange
            oshelf["punctuation"] = self.punctuation
            oshelf["lowercase"] = self.lowercase
            oshelf["uppercase"] = self.uppercase
            oshelf["numbers"] = self.numbers

        if interactive:
            print("Current Options:")
            print("emails:")
            for email in self.emails:
                print(email)
            print("usernames:")
            for username in self.usernames:
                print(username)
            print("length", self.length)
            print("lrange", self.lrange)
            print("punctuation", self.punctuation,
                  self.punctuation_choices[self.punctuation])
            print("lowercase", self.lowercase)
            print("uppercase", self.uppercase)
            print("numbers", self.numbers)

    # ~~ Setters and getters ~~
    # todo: integrate setters and getters
    def get_emails(self):
        return self.emails

    def get_length(self):
        return self.length

    def get_punctuation(self):
        return self.punctuation

    def get_range(self):
        return self.lrange

    def get_usernames(self):
        return self.usernames

    def set_emails(self, e):
        self.emails = e

    def set_length(self, l):
        self.length = l

    def set_punctuation(self, p):
        self.punctuation = p

    def set_range(self, r):
        self.lrange = r

    def set_usernames(self, u):
        self.usernames = u


class MainMenu:
    def __init__(self):
        """ INTERACTIVE MODE """
        menu = {
            "1": Write().new_random_entry,
            "2": Write().new_entry,
            "3": Write().print_random,
            "4": Write().get_entry,
            "5": Write().edit_entry,
            "6": Write().delete_entry,
            "7": Write().print_or_save_all,
            "8": Write().change_all,
            "9": OptionsUI().options_menu,
            "0": self.quit
        }
        i = 'dummy'
        while i != "0":  # loop until [quit]
            print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    RANDOM  P A S S W O R D  MANAGER
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    [1] New random p.w. entry
    [2] New entry
    [3] Generate random p.w.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    [4] Get entry
    [5] Edit entry
    [6] Delete entry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    [7] Print/Save all
    [8] Change all
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    [9] Options
    [0] Quit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""")
            while i not in menu:  # ensure valid choice
                i = input()
            menu[i]()
            input("[enter]...\n")  # pause

    @staticmethod
    def quit():
        print("\nGoodbye\n")


class NoUI:
    def __init__(self, name):
        """ NON-INTERACTIVE MODE """
        if name[0] in ("-q", "--quiet"):
            Write().get_entry_no_ui(name=" ".join(name[1:]), quiet=True)
        else:
            Write().get_entry_no_ui(name=" ".join(name), quiet=False)


class Write:
    def __init__(self):
        self.random = False

    def change_all(self):
        if not Main.dshelf:
            input("No data yet\n"
                  "[enter] Main Menu\n")
            MainMenu()
        i = input("Change all p a s s w o r d s  (make all new random)\n"
                  "[enter] Main Menu\n"
                  "Confirm by typing 'change all'\n")
        if i == "change all":
            for entry in Main.dshelf:
                print("\n" + entry)
                new = self.generate_random()
                print(new)
                Main.dshelf[entry][2] = new
            input("Success\n"
                  "[enter]...\n")

    def delete_entry(self):
        """ Delete entry by name from DATA """
        if not Main.dshelf:
            input("No data yet\n"
                  "[enter] Main Menu\n")
            MainMenu()
        self.__display_entries__()  # print names
        i = input("[enter] Main Menu\n"
                  "[name] Entry to delete\n")
        if not i:
            MainMenu()
        elif i not in Main.dshelf:
            print("No entry for that name")
            if input("[enter] Main Menu\n"
                     "[t] Try again\n") == "t":
                self.delete_entry()  # Try again
        else:
            if input(f"Confirm delete '{i}'\n"
                     f"[y] Yes\n"
                     f"[n] No\n") == "y":
                del Main.dshelf[i]  # delete entry 'i' from dshelf
                i = input("Deleted\n"
                          "[enter] Main Menu\n"
                          "[d] Delete another\n")
            else:
                i = input("Nothing deleted\n"
                          "[enter] Main Menu\n"
                          "[t] Try again\n")
            if i in ("d", "t"):
                self.delete_entry()  # Try again

    def set_email(self, name):
        Main.dshelf[name][0] = self.__choose_email__()

    def set_username(self, name):
        Main.dshelf[name][1] = self.__choose_username__()

    def edit_entry(self, name=None):
        if not Main.dshelf:
            input("No data yet\n"
                  "[enter] Main Menu\n")
            MainMenu()
        if name is None:  # also accept name as argument
            self.__display_entries__()
            name = input("[enter] Main Menu\n"
                         "[name] Entry to edit\n")
            if not name:
                MainMenu()
        try:
            data = Main.dshelf[name]
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            Helpers.__display_data__(data, name)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            edits = {
                "e": self.set_email,
                "u": self.set_username,
                "p": self.__edit_pw__,
                "n": self.__edit_note__,
                "": MainMenu,
            }
            i = "dummy"
            while i not in edits:
                i = input("EDIT\n"
                          "[e] Email\n"
                          "[u] Username\n"
                          "[p] P a s s w o r d\n"
                          "[n] Note\n"
                          "[enter] Done\n")
            edits[i]()
            input("Saved\n"
                  "[enter]...\n")
            self.edit_entry(name)  # edit name until [enter]
        except KeyError:
            i = input(f"No data for '{name}'\n"
                      f"[enter] Main Menu\n"
                      f"[t] Try again\n")
            self.edit_entry() if i == "t" else MainMenu()

    @staticmethod
    def generate_random():
        """ Randomly generate a string of alphanumeric characters
            and (if True) punctuation. Length of string is determined by
            self.length. If self.lrange is non-zero, then self.length is
            randomly adjusted +/- some value within self.lrange """
        lowercase = "abcdefghijklmnopqrstuvwxyz" if Options.lowercase else ""
        uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if Options.uppercase else ""
        numbers = "0123456789" if Options.numbers else ""
        punctuation = Options.punctuation
        characters = lowercase + uppercase + numbers + punctuation
        nchars = Options.length + randint(-Options.lrange, Options.lrange)
        return "".join(choice(characters) for _ in range(nchars))

    def get_entry(self):
        if not Main.dshelf:  # empty database
            input("Database is empty\n"
                  "Make a new entry first\n"
                  "[enter]...\n")
            MainMenu()
        self.__display_entries__()  # print names
        name = input("[enter] Main Menu\n"
                     "[name] Get entry\n")
        if not name:
            MainMenu()
        try:
            data = Main.dshelf[name]
        except KeyError:
            print(f"{name} not found\n")
        else:
            Helpers.__display_data__(data, name)
        finally:
            input("[enter]...\n")
            self.get_entry()  # get another until [Main Menu]

    @staticmethod
    def get_entry_no_ui(name, quiet):
        try:
            data = Main.dshelf[name]
        except KeyError:
            print(f"{name} not found")
        else:
            Helpers.__display_data__(data, name, quiet)

    def new_entry(self):
        """ open or create DATA shelf and write data to it """
        name = input("[enter] Main Menu\n"
                     "[name] Entry\n")
        if not name:
            MainMenu()
        if name in Main.dshelf:  # entry with 'name' already exists
            data = Main.dshelf[name]
            if data:
                print(f"\n {name} already exists")
                Helpers().__display_data__(data, name)
                i = 'dummy'
                while i not in ("", "t", "e", "r"):
                    i = input(f"[enter] Main Menu\n"
                              f"[t] Try another name\n"
                              f"[e] Edit {name}\n"
                              f"[r] Replace {name}'\n")
                if not i:
                    MainMenu()
                elif i == "t":
                    self.new_entry()  # Try again
                elif i == "e":
                    self.edit_entry(name)  # edit
        # Write new entry
        # (name does not exist, is blank entry, or [Replace] selected)
        data = dict([(str(key), value) for key, value
                     in enumerate(self.__input_data__())])
        Main.dshelf[name] = data
        Helpers().__display_data__(data, name)
        input("Saved\n"
              "[enter]...\n")

    def new_random_entry(self):
        self.random = True
        self.new_entry()

    def print_or_save_all(self):
        alphabetical = sorted(Main.dshelf)  # sorted list of names
        if not Main.dshelf:
            input("No data yet\n"
                  "[enter] Main Menu\n")
            MainMenu()
        for name in alphabetical:
            data = Main.dshelf[name]  # data is itself a dictionary object
            Helpers().__display_data__(data, name)
        i = "dummy"
        while i not in ("", "s"):
            i = input("\n[enter] Main Menu\n"
                      "[s] Save all data to plain text file (not recommended!)")
        if i == "s":  # save data to file
            newpath = input(f"[enter] Save to {SAVE}\n"
                            f"[filepath] Save here\n")
            filepath = newpath if newpath else SAVE  # use default filepath
            # unless one is given by user
            mode = "dummy"
            while mode not in ("", "w", "a"):
                mode = input(f"[enter] Cancel\n"
                             f"[w] Write {SAVE} (overwrite if it exists)\n"
                             f"[a] Append {SAVE}\n")
            if not mode:
                self.print_or_save_all()  # go back (Try again)
            with open(filepath, mode) as f:  # save data to file f
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", file=f)
                for name in alphabetical:  # iterate (sorted) names
                    print(name, file=f)  # print 'name' to file
                    data = Main.dshelf[name]
                    for key in range(len(data)):  # iterate fields (keys)
                        if data[key]:  # if data in field
                            print(data[key], file=f)  # print to file
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", file=f)
            print(f"{SAVE} {'written' if mode == 'w' else 'appended'}")
            input("[enter]...\n")

    def print_random(self):
        print(self.generate_random())

    def add_note(self):
        """ add note on new line until [enter] is pressed """
        add_line = input("[enter] Done\n"
                         "[note]\n")
        return f"{add_line}\n{self.add_note()}" if add_line else ""

    @staticmethod
    def __choose_email__():
        Helpers().__display_list__(Options.emails, "emails")
        print("[enter] Default\n"
              "[*] Other\n"
              "[number] Select\n"),
        i = Helpers().__valid_number__(Options.emails)
        if not i:  # default email (if exists)
            return Options.emails[1] if len(Options.emails) > 1 else ""
        elif i == "*":  # other
            # First input email and save it to OPTIONS
            ok, email = Helpers().__add_entry__(
                Options.emails, Main.oshelf, "emails")
            print(f"{email} saved to your email list") if ok else \
                print(f"Already have {email} saved")
            return email  # return email either way
        else:
            return Options.emails[i]  # select email

    @staticmethod
    def __choose_username__():
        Helpers().__display_list__(Options.usernames, "usernames")
        print("[enter] Default\n"
              "[*] Other\n"
              "[number] Select\n")
        i = Helpers().__valid_number__(Options.usernames)
        if not i:  # default username (if exists)
            return Options.usernames[1] if len(Options.usernames) > 1 else ""
        elif i == "*":  # other
            # First add the username and save it to OPTIONS
            ok, username = Helpers().__add_entry__(
                Options.usernames, Main.oshelf, "usernames")
            print(f"{username} saved to your usernames list") if ok else \
                print(f"Already have {username} saved")
            return username  # return username either way
        else:
            return Options.usernames[i]  # select username

    # todo print names in columns
    @staticmethod
    def __display_entries__():
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Names:")
        for key in sorted(Main.dshelf):
            print(key)  # display names
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    def __edit_note__(self, name):
        note = Main.dshelf[name][3].split("\n")  # split lines into list
        for line in enumerate(note):
            print(line)
        if note:
            while True:
                i = input("[enter] Go back\n"
                          "[a] Add note\n"
                          "[number] Edit note\n")
                if not i:
                    self.edit_entry()
                elif i == "a":
                    Main.dshelf[name][3] = "\n".join(self.__write_note__(note))
                    input("Saved\n"
                          "[enter]...\n")
                    break
                try:  # try to edit note by line number
                    i = int(i)
                    assert i > 0
                    note[i - 1] = input("New line: ")
                    Main.dshelf[name][3] = "\n".join(note)
                    input("Saved\n"
                          "[enter]...\n")
                    break
                except (IndexError, ValueError, AssertionError):
                    pass
        else:  # note is empty or one line
            i = "-"
            while i not in ("a", "e"):
                i = input("[a] Add note\n"
                          "[e] Edit note\n")
                if i == "a":
                    Main.dshelf[name][3] += self.add_note()
                    input("Saved\n"
                          "[enter]...\n")
                elif i == "e":
                    n = self.add_note()
                    Main.dshelf[name][3] = n
                    input("Saved\n"
                          "[enter]...\n")

    def __edit_pw__(self, name):
        i, p = "", ""
        i = input("[enter] None\n"
                  "[r] Random\n"
                  "[m] Manual\n")
        if i == "r":
            p = self.generate_random()  # random p.w.
        elif i == "m":
            p = self.__enter_pw__()  # manual p.w.
        if i and p:
            Main.dshelf[name][2] = p
            input("Saved\n"
                  "[enter]...\n")
        else:
            if input("\nblank p.w.? [y]es, [n]o: ") == "y":
                Main.dshelf[name][2] = ""
                input("Saved\n"
                      "[enter]...\n")
            else:
                input("Unchanged\n"
                      "[enter]...\n")

    def __enter_pw__(self):
        p, p1 = "", ""
        while not p:
            p = input("Input p a s s w o r d\n")
        while not p1:
            p1 = input("Input again to confirm\n")
        if p == p1:
            return p  # match confirmed
        else:
            if input("P a s s w o r d s did not match\n"
                     "[enter] Cancel\n"
                     "[t] Try again\n") == "t":
                return self.__enter_pw__()  # Try again
            return None  # cancel

    def __input_data__(self):
        return self.__choose_email__(), self.__choose_username__(), \
               self.__write_pw__(), self.__write_note__([])

    def __write_note__(self, note):
        """ add note on new line until [enter] is pressed """
        line = input("[enter] Done\n"
                     "[note]\n")
        if line:
            note.append(line)
            self.__write_note__(note)
        return "\n".join(note)

    def __write_pw__(self):
        if self.random:
            return self.generate_random()  # random
        else:
            m = self.__enter_pw__()  # manual
            if m:
                return m
            else:
                MainMenu()


class OptionsUI:
    def options_menu(self):
        print("\n~~~~~~~~~~~~~~~\n"
              "    OPTIONS\n"
              "~~~~~~~~~~~~~~~\n"
              "[1] Emails\n"
              "[2] Usernames\n"
              "[3] Length\n"
              "[4] Range\n"
              "[5] Punctuation\n"
              "~~~~~~~~~~~~~~~\n"
              "[6] Main Menu\n"
              "~~~~~~~~~~~~~~~\n")
        options = {
            "1": self.email_options,
            "2": self.username_options,
            "3": self.length_options,
            "4": self.range_options,
            "5": self.punctuation_options,
            "6": MainMenu,
        }
        i = "dummy"
        while i not in options:
            i = input()
        options[i]()
        self.options_menu()  # loop until [Main Menu]

    def email_options(self):
        Helpers().__display_list__(Options.emails, "emails")
        options = {
            "": self.options_menu,
            "a": self.__add_email__,
            "d": self.__del_email__,
            "e": self.__edit_email__,
            "s": self.__default_email__,
        }
        i = "dummy"
        while i not in options:
            i = input("[enter] Options menu\n"
                      "[a] Add\n"
                      "[d] Delete\n"
                      "[e] Edit\n"
                      "[s] Set default\n")
        options[i]()
        self.email_options()  # loop email options until [enter]

    def username_options(self):
        Helpers().__display_list__(Options.usernames, "usernames")
        options = {
            "": self.options_menu,
            "a": self.__add_username__,
            "d": self.__del_username__,
            "e": self.__edit_username__,
            "s": self.__default_username__,
        }
        i = "dummy"
        while i not in options:
            i = input("[enter] Options menu\n"
                      "[a] Add\n"
                      "[d] Delete\n"
                      "[e] Edit\n"
                      "[s] Set default\n")
        options[i]()
        self.username_options()  # loop username options until [enter]

    def length_options(self):
        print(f"\nCurrent length is {Options.length} characters")
        ln = input("[enter] Options menu\n"
                   "[length]\n")
        if ln != "":  # not [enter] ("")
            try:
                ln = int(ln)
                assert ln > 0
                Options.length = ln
                Main.oshelf["length"] = ln
                print(f"Length set to {ln} characters")
            except (ValueError, AssertionError):  # bad input Try again
                print("Length must be a positive integer")
                self.length_options()

    def range_options(self):
        print(f"\nRange to randomize p.w. length\n"
              f"\tE.g. range 2 and length 15\n"
              f"\trandomizes p.w. length between 13 to 17 characters\n"
              f"Current range is {Options.lrange}")
        try:
            r = input("[enter] Options menu\n"
                      "Set range\n")
            if r != "":  # not [enter] ("")
                r = int(r)
                assert r >= 0
                Options.lrange = r
                Main.oshelf["lrange"] = r
                print(f"Range set to +/- {r} characters")
        except (ValueError, AssertionError):  # bad input Try again
            print("Range must be a non-negative integer")
            self.range_options()

    @staticmethod
    def punctuation_options():
        print(f"\nCurrent punctuation is {Options.punctuation}")
        print("""
        [enter] Options menu
        [a] All !#$%&()*+,-./:;<=>?@[]^_{|}~
        [s] Some %+-./:=@_
        [l] Limited @._-
        [n] None
        """)
        pn = {"a": "all", "s": "some", "l": "limited", "n": "none"}
        i = "input string"
        while i and (i not in pn):
            i = input()  # loop if bad input
            if i in pn:
                Options.punctuation = pn[i]
                Main.oshelf["punctuation"] = Options.punctuation
                print(f"Punctuation set to {Options.punctuation}")

    def __add_email__(self):
        ok, e = Helpers().__add_entry__(Options.emails, Main.oshelf, "emails")
        Helpers().__display_list__(Options.emails, "emails")
        if ok:
            i = input("Saved\n"
                      "[enter] Email options\n"
                      "[a] Add another\n")
        else:
            i = input(f"Already have '{e}' saved\n"
                      f"[enter] Email options\n"
                      f"[t] Try again\n")
        if i in ("a", "t"):
            self.__add_email__()  # Add another/Try again

    def __add_username__(self):
        ok, u = Helpers().__add_entry__(
            Options.usernames, Main.oshelf, "usernames")
        Helpers().__display_list__(Options.usernames, "usernames")
        if ok:
            i = input("Saved\n"
                      "[enter] Username options\n"
                      "[a] Add another\n")
        else:
            i = input(f"Already have '{u}' saved\n"
                      f"[enter] Username options\n"
                      f"[t] Try again\n")
        if i in ("a", "t"):
            self.__add_username__()  # add another/Try again

    def __default_email__(self):
        if len(Options.emails) == 1:
            input("Add an email first\n"
                  "[enter] Go back\n")
            self.email_options()  # back to email options
        print("[enter] Email options\n"
              "[number] Set default email")
        number = Helpers().__valid_number__(Options.emails)
        if number == 0:
            if input("Cannot set 'no email' as default\n"
                     "[enter] Email options\n"
                     "[t] Try again\n") == "t":
                self.__default_email__()  # Try again
        elif number in ("", "*"):
            self.email_options()  # back to email options
        else:
            d = Options.emails.pop(number)  # remove from list, assign to 'd'
            # put back as [1]
            temp = [Options.emails[0], d] + Options.emails[1:]
            Options.emails = temp
            Main.oshelf["emails"] = temp
            input(f"'{d}' Saved as default\n"
                  f"[enter]...\n")
        self.email_options()

    def __default_username__(self):
        if len(Options.usernames) == 1:
            input("Add a username first\n"
                  "[enter] Go back...\n")
            self.username_options()  # back to username options
        print("[enter] Username options\n"
              "[number] Set default username\n")
        number = Helpers().__valid_number__(Options.usernames)
        if number == 0:
            if input("Cannot set 'no username' as default\n"
                     "[enter] Username options\n"
                     "[t] Try again\n") == "t":
                self.__default_username__()  # Try again
        elif number in ("", "*"):
            self.username_options()  # back to username options
        else:
            d = Options.usernames.pop(number)  # remove from list, assign to 'd'
            temp = [Options.usernames[0], d] + Options.usernames[1:]  # user[1]
            Options.usernames = temp
            Main.oshelf["usernames"] = temp
            input(f"'{d}' Saved as default\n"
                  f"[enter]...\n")

    def __del_email__(self):
        if len(Options.emails) == 1:
            input("No emails to delete\n"
                  "[enter]...\n")
            self.email_options()  # back to email options
        print("[enter] Email options\n"
              "[number] Remove email"),
        number = Helpers().__valid_number__(Options.emails)
        if number == 0:
            if input("Cannot delete 'no email'\n"
                     "[enter] Email options\n"
                     "[t] Try again\n") == "t":
                self.__del_email__()  # Try again
        elif number not in ("", "*"):
            email = Options.emails[number]  # number is valid
            if input(f"Remove {email} ?\n"
                     f"[y] Yes\n"
                     f"[n] No\n") == "y":
                temp = Options.emails[:]
                temp.pop(number)
                Options.emails = temp
                Main.oshelf["emails"] = temp
                input(f"'{email}' deleted\n"
                      f"[enter]...\n")
            else:  # abort remove
                input("Nothing deleted\n"
                      "[enter]...\n")

    def __del_username__(self):
        if len(Options.emails) == 1:
            input("No usernames to delete\n"
                  "[enter]...\n")
            self.username_options()  # back to username options
        print("[enter] Username options\n"
              "[number] Remove username"),
        number = Helpers().__valid_number__(Options.usernames)
        if number == 0:
            if input("Cannot delete 'no username'\n"
                     "[enter] Username options\n"
                     "[t] Try again\n") \
                    == "t":
                self.__del_username__()  # Try again
        elif number not in ("", "*"):
            username = Options.usernames[number]  # number is valid
            if input(f"Remove {username} ?\n"
                     f"[y] Yes\n"
                     f"[n] No\n") == "y":
                temp = Options.usernames[:]
                temp.pop(number)
                Options.usernames = temp
                Main.oshelf["usernames"] = temp
                input(f"'{username}' deleted\n"
                      f"[enter]...\n")
            else:  # abort remove
                input("Nothing deleted\n"
                      "[enter]...\n")

    def __edit_email__(self):
        if len(Options.emails) == 1:
            input("No emails to edit\n"
                  "[enter] Email options\n")
            self.email_options()  # options
        print("[enter] Email options\n"
              "[number] Edit email\n")
        if self.__edit_list__(Options.emails, "emails"):
            Helpers().__display_list__(Options.emails, "emails")
            i = input("[enter] Email options\n"
                      "[e] Edit another\n")
        else:
            i = input("[enter] Email options\n"
                      "[t] Try again\n")
        if i in ("e", "t"):  # edit another/Try again
            self.__edit_email__()

    def __edit_list__(self, mylist, key):
        ind = Helpers().__valid_number__(mylist)
        if not ind:
            if key == "emails":
                self.email_options()
            elif key == "usernames":
                self.username_options()
        elif ind == 0:
            print(f"0 is no {key}")
            return False
        entry = input("Email:\n") if key == "emails" else input("Username:\n")
        if entry in mylist:
            print(f"Already have {entry} saved")
            return False
        mylist[ind] = entry
        Main.oshelf[key][ind] = entry
        Helpers().__display_list__(mylist, key)
        return True

    def __edit_username__(self):
        if len(Options.emails) == 1:
            input("No usernames to edit\n"
                  "[enter]...\n")
            return  # options
        print("[enter] Options menu\n"
              "[number] Edit username\n")
        if self.__edit_list__(Options.usernames, "usernames"):
            Helpers().__display_list__(Options.usernames, "usernames")
            i = input("[enter] Username options\n"
                      "[e] Edit another\n")
        else:
            i = input("[enter] Username options\n"
                      "[t] Try again\n")
        if i in ("e", "t"):  # edit another/Try again
            self.__edit_username__()


class Helpers:
    def __valid_number__(self, mylist):
        try:
            number = input()
            if number in ("", "*"):  # if input is [enter] or [*]
                return number  # return string (special option)
            else:
                number = int(number)  # try converting input to integer
                assert number in range(len(mylist))  # confirm is valid index
                return number
        except (ValueError, AssertionError):
            print("Try again: ")
            return self.__valid_number__(mylist)

    @staticmethod
    def __add_entry__(mylist, key, oshelf):
        entry = ""
        if key == "emails":
            entry = input("Email:\n")
        elif key == "usernames":
            entry = input("Username:\n")
        if entry not in mylist:
            mylist.append(entry)
            oshelf[key] = mylist
            return True, entry
        return False, entry

    @staticmethod
    def __display_list__(mylist, key):
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(key + ":")
        for n in range(len(mylist)):
            if n == 0:
                print(n, "none")
            elif n == 1:
                print(n, mylist[n], "default")
            else:
                print(n, mylist[n])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    @staticmethod
    def __display_data__(data, name, quiet=False):
        if quiet:
            try:
                # sys.stdout.write(data[2])
                print(data[2])  # p.w. only
                # flush output here to force SIGPIPE to be triggered
                # while inside this try block
                sys.stdout.flush()
            except BrokenPipeError:
                # Python flushes standard streams on exit;
                # redirect remaining output to devnull to avoid
                # another BrokenPipeError at shutdown
                devnull = os.open(os.devnull, os.O_WRONLY)
                os.dup2(devnull, sys.stdout.fileno())
                sys.exit(1)  # Python exits with error code 1 on EPIPE
        else:
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(name)
            for key in sorted(data):
                if data[key]:
                    print(data[key])
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


class Main:
    oshelf = shelve.open(OPTIONS, writeback=True)  # options shelf
    dshelf = shelve.open(DATA, writeback=True)
    Options(oshelf)

    def __init__(self):
        arguments = sys.argv[1:]
        print("arguments:", arguments)
        if arguments:  # Command line argument given ==> Non-Interactive Mode
            NoUI(arguments)  # No user interface
        else:  # No command line argument ==> Interactive Mode
            print("\n~~~~~ Welcome to Random P a s s w o r d  Manager ~~~~~\n")
            MainMenu()  # User interface
        self.oshelf.close()
        self.dshelf.close()


if __name__ == "__main__":
    GRAPH = False  # call graph

    if GRAPH:
        from pycallgraph import PyCallGraph
        from pycallgraph.output import GraphvizOutput
        with PyCallGraph(output=GraphvizOutput()):
            Main()
    else:
        Main()
