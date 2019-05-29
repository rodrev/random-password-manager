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


class Run:
    def __init__(self):
        emails, usernames = [""], [""]  # defaults
        length, lrange, punctuation = 40, 0, "all"  # defaults
        if os.path.isfile(OPTIONS):  # OPTIONS file found
            oshelf = shelve.open(OPTIONS, writeback=True)  # options shelf
            try:  # get settings from OPTIONS file
                emails = oshelf["emails"]
                usernames = oshelf["usernames"]
                length = oshelf["length"]
                lrange = oshelf["lrange"]
                punctuation = oshelf["punctuation"]
                oshelf.close()
            except KeyError:
                print(f"Options file {OPTIONS} corrupted\n"
                      f"Delete it and run again to make a new one")
                oshelf.close()
                exit(1)
        else:  # OPTIONS not found, set defaults
            print("~~~~~ Welcome to Random P a s s w o r d  Manager ~~~~~\n"
                  f"{OPTIONS} file created with default options\n"
                  "Select [options] from menu to customize\n")
            # Create OPTIONS file to shelve defaults
            # oshelf {Strings (keys) : Any object (values)}
            oshelf = shelve.open(OPTIONS, writeback=True)
            oshelf["emails"] = emails
            oshelf["usernames"] = usernames
            oshelf["length"] = length
            oshelf["lrange"] = lrange
            oshelf["punctuation"] = punctuation
            oshelf.close()
        # Initialize defaults if OPTIONS file not found
        # Otherwise, initialize from OPTIONS file
        self.emails = emails
        self.usernames = usernames
        self.length = length
        self.lrange = lrange
        self.punctuation = punctuation

    @staticmethod
    def goodbye():
        print("\nGoodbye\n")
        exit()

    def main_menu(self):
        """ INTERACTIVE MODE """
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
        menu = {
            "1": Write().new_random_entry,
            "2": Write().new_entry,
            "3": Write().print_random,
            "4": Write().get_entry,
            "5": Write().edit_entry,
            "6": Write().delete_entry,
            "7": Write().print_or_save_all,
            "8": Write().change_all,
            "9": Options().options_menu,
            "0": self.goodbye
        }
        i = 'dummy'
        while i not in menu:
            i = input()
        menu[i]()
        input("[enter]...\n")  # pause
        self.main_menu()  # loop Main Menu until [Quit]

    @staticmethod
    def no_ui(name):
        """ NON-INTERACTIVE MODE """
        if name[0] in ("-q", "--quiet"):
            Write().get_entry_no_ui(name=" ".join(name[1:]), quiet=True)
        else:
            Write().get_entry_no_ui(name=" ".join(name), quiet=False)

    # ~~ Setters and getters ~~
    # todo: integrate setters and getters
    def __get_emails__(self):
        return self.emails

    def __get_length__(self):
        return self.length

    def __get_punctuation__(self):
        return self.punctuation

    def __get_range__(self):
        return self.lrange

    def __get_usernames__(self):
        return self.usernames

    def __set_emails__(self, e):
        self.emails = e

    def __set_length__(self, l):
        self.length = l

    def __set_punctuation__(self, p):
        self.punctuation = p

    def __set_range__(self, r):
        self.lrange = r

    def __set_usernames__(self, u):
        self.usernames = u


class Write:
    def __init__(self):
        self.run = Run()
        self.emails = self.run.__get_emails__()
        self.usernames = self.run.__get_usernames__()
        self.length = self.run.__get_length__()
        self.lrange = self.run.__get_range__()
        self.punctuation = self.run.__get_punctuation__()
        self.random = False
        self.dshelf = shelve.open(DATA, writeback=True)

    def main_menu(self):
        self.dshelf.close()
        self.run.main_menu()

    def change_all(self):
        if not self.dshelf:
            input("No data yet\n"
                  "[enter] Main Menu\n")
            self.main_menu()
        i = input("Change all p a s s w o r d s  (make all new random)\n"
                  "[enter] Main Menu\n"
                  "Confirm by typing 'change all'\n")
        if i == "change all":
            for entry in self.dshelf:
                print("\n" + entry)
                new = self.generate_random()
                print(new)
                self.dshelf[entry][2] = new
            input("Success\n"
                  "[enter]...\n")
        self.dshelf.close()  # done

    def delete_entry(self):
        """ Delete entry by name from DATA """
        if not self.dshelf:
            input("No data yet\n"
                  "[enter] Main Menu\n")
            self.main_menu()
        self.__display_entries__()  # print names
        i = input("[enter] Main Menu\n"
                  "[name] Entry to delete\n")
        if not i:
            self.main_menu()
        elif i not in self.dshelf:
            print("No entry for that name")
            if input("[enter] Main Menu\n"
                     "[t] Try again\n") == "t":
                self.delete_entry()  # Try again
        else:
            if input(f"Confirm delete '{i}'\n"
                     f"[y] Yes\n"
                     f"[n] No\n") == "y":
                del self.dshelf[i]  # delete entry 'i' from dshelf
                i = input("Deleted\n"
                          "[enter] Main Menu\n"
                          "[d] Delete another\n")
            else:
                i = input("Nothing deleted\n"
                          "[enter] Main Menu\n"
                          "[t] Try again\n")
            if i in ("d", "t"):
                self.delete_entry()  # Try again
        self.dshelf.close()  # done

    def set_email(self, name):
        self.dshelf[name][0] = self.__choose_email__()

    def set_username(self, name):
        self.dshelf[name][1] = self.__choose_username__()

    def edit_entry(self, name=None):
        if not self.dshelf:
            input("No data yet\n"
                  "[enter] Main Menu\n")
            self.main_menu()
        if name is None:  # also accept name as argument
            self.__display_entries__()
            name = input("[enter] Main Menu\n"
                         "[name] Entry to edit\n")
            if not name:
                self.main_menu()
        try:
            data = self.dshelf[name]
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            Helpers.__display_data__(data, name)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            edits = {
                "e": self.set_email,
                "u": self.set_username,
                "p": self.__edit_pw__,
                "n": self.__edit_note__,
                "": self.main_menu,
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
            self.edit_entry() if i == "t" else self.main_menu()

    def generate_random(self):
        """ Randomly generate a string of alphanumeric characters
            and (if True) punctuation. Length of string is determined by
            self.length. If self.lrange is non-zero, then self.length is
            randomly adjusted +/- some value within self.lrange """
        punctuation_marks = {
            "all": "!#$%&()*+,-./:;<=>?@[]^_{|}~",
            "some": "%+-./:=@_",
            "limited": "@._-",
            "none": ""
        }
        characters = "abcdefghijklmnopqrstuvwxyz" \
                     "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                     "1234567890" + punctuation_marks[self.punctuation]
        nchars = self.length + randint(-self.lrange, self.lrange) \
            if self.lrange > 0 else self.length
        return "".join(choice(characters) for _ in range(nchars))

    def get_entry(self):
        if not self.dshelf:  # empty database
            input("Database is empty\n"
                  "Make a new entry first\n"
                  "[enter]...\n")
            self.main_menu()
        self.__display_entries__()  # print names
        name = input("[enter] Main Menu\n"
                     "[name] Get entry\n")
        if not name:
            self.main_menu()
        try:
            data = self.dshelf[name]
        except KeyError:
            print(f"{name} not found\n")
        else:
            Helpers.__display_data__(data, name)
        finally:
            input("[enter]...\n")
            self.get_entry()  # get another until [Main Menu]

    def get_entry_no_ui(self, name, quiet):
        try:
            data = self.dshelf[name]
        except KeyError:
            print(f"{name} not found")
        else:
            Helpers.__display_data__(data, name, quiet)
        finally:
            self.dshelf.close()  # done

    def new_entry(self):
        """ open or create DATA shelf and write data to it """
        name = input("[enter] Main Menu\n"
                     "[name] Entry\n")
        if not name:
            self.main_menu()
        if name in self.dshelf:  # entry with 'name' already exists
            data = self.dshelf[name]
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
                    self.main_menu()
                elif i == "t":
                    self.new_entry()  # Try again
                elif i == "e":
                    self.edit_entry(name)  # edit
        # Write new entry
        # (name does not exist, is blank entry, or [Replace] selected)
        data = dict(enumerate(self.__input_data__()))
        self.dshelf[name] = data
        Helpers().__display_data__(data, name)
        input("Saved\n"
              "[enter]...\n")
        self.dshelf.close()  # done

    def new_random_entry(self):
        self.random = True
        self.new_entry()

    def print_or_save_all(self):
        alphabetical = sorted(self.dshelf)  # sorted list of names
        if not self.dshelf:
            input("No data yet\n"
                  "[enter] Main Menu\n")
            self.main_menu()
        for name in alphabetical:
            data = self.dshelf[name]  # data is itself a dictionary object
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
                    data = self.dshelf[name]
                    for key in range(len(data)):  # iterate fields (keys)
                        if data[key]:  # if data in field
                            print(data[key], file=f)  # print to file
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", file=f)
            print(f"{SAVE} {'written' if mode == 'w' else 'appended'}")
            input("[enter]...\n")
        self.dshelf.close()  # done

    def print_random(self):
        print(self.generate_random())

    def add_note(self):
        """ add note on new line until [enter] is pressed """
        add_line = input("[enter] Done\n"
                         "[note]\n")
        return f"{add_line}\n{self.add_note()}" if add_line else ""

    def __choose_email__(self):
        Helpers().__display_list__(self.emails, "emails")
        print("[enter] Default\n"
              "[*] Other\n"
              "[number] Select\n"),
        i = Helpers().__valid_number__(self.emails)
        if not i:  # default email (if exists)
            return self.emails[1] if len(self.emails) > 1 else ""
        elif i == "*":  # other
            # First input email and save it to OPTIONS
            oshelf = shelve.open(OPTIONS, writeback=True)
            ok, email = Helpers().__add_entry__(self.emails, oshelf, "emails")
            oshelf.close()
            print(f"{email} saved to your email list") if ok else \
                print(f"Already have {email} saved")
            return email  # return email either way
        else:
            return self.emails[i]  # select email

    def __choose_username__(self):
        Helpers().__display_list__(self.usernames, "usernames")
        print("[enter] Default\n"
              "[*] Other\n"
              "[number] Select\n")
        i = Helpers().__valid_number__(self.usernames)
        if not i:  # default username (if exists)
            return self.usernames[1] if len(self.usernames) > 1 else ""
        elif i == "*":  # other
            # First add the username and save it to OPTIONS
            oshelf = shelve.open(OPTIONS, writeback=True)
            ok, username = Helpers().__add_entry__(self.usernames, oshelf,
                                                   "usernames")
            oshelf.close()
            print(f"{username} saved to your usernames list") if ok else \
                print(f"Already have {username} saved")
            return username  # return username either way
        else:
            return self.usernames[i]  # select username

    # todo print names in columns
    def __display_entries__(self):
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Names:")
        for key in sorted(self.dshelf):
            print(key)  # display names
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    def __edit_note__(self, name):
        note = self.dshelf[name][3].split("\n")  # split lines into list
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
                    self.dshelf[name][3] = "\n".join(self.__write_note__(note))
                    input("Saved\n"
                          "[enter]...\n")
                    break
                try:  # try to edit note by line number
                    i = int(i)
                    assert i > 0
                    note[i - 1] = input("New line: ")
                    self.dshelf[name][3] = "\n".join(note)
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
                    self.dshelf[name][3] += self.add_note()
                    input("Saved\n"
                          "[enter]...\n")
                elif i == "e":
                    n = self.add_note()
                    self.dshelf[name][3] = n
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
            self.dshelf[name][2] = p
            input("Saved\n"
                  "[enter]...\n")
        else:
            if input("\nblank p.w.? [y]es, [n]o: ") == "y":
                self.dshelf[name][2] = ""
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
                self.main_menu()


class Options:
    def __init__(self):
        run = Run()
        self.emails = run.__get_emails__()
        self.usernames = run.__get_usernames__()
        self.length = run.__get_length__()
        self.lrange = run.__get_range__()
        self.punctuation = run.__get_punctuation__()
        self.oshelf = shelve.open(OPTIONS, writeback=True)

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
              "[7] Quit\n"
              "~~~~~~~~~~~~~~~\n")
        options = {
            "1": self.email_options,
            "2": self.username_options,
            "3": self.length_options,
            "4": self.range_options,
            "5": self.punctuation_options,
            "6": self.main_menu,
            "7": self.quit
        }
        i = "dummy"
        while i not in options:
            i = input()
        options[i]()
        self.options_menu()  # always runOptions until [Main Menu] or [Quit]

    def email_options(self):
        Helpers().__display_list__(self.emails, "emails")
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
        Helpers().__display_list__(self.usernames, "usernames")
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
        print(f"\nCurrent length is {self.length} characters")
        ln = input("[enter] Options menu\n"
                   "[length]\n")
        if ln != "":  # not [enter] ("")
            try:
                ln = int(ln)
                assert ln > 0
                self.length = ln
                self.oshelf["length"] = ln
                print(f"Length set to {ln} characters")
            except (ValueError, AssertionError):  # bad input Try again
                print("Length must be a positive integer")
                self.length_options()

    def range_options(self):
        print(f"\nRange to randomize p.w. length\n"
              f"\tE.g. range 2 and length 15\n"
              f"\trandomizes p.w. length between 13 to 17 characters\n"
              f"Current range is {self.lrange}")
        try:
            r = input("[enter] Options menu\n"
                      "Set range\n")
            if r != "":  # not [enter] ("")
                r = int(r)
                assert r >= 0
                self.lrange = r
                self.oshelf["lrange"] = r
                print(f"Range set to +/- {r} characters")
        except (ValueError, AssertionError):  # bad input Try again
            print("Range must be a non-negative integer")
            self.range_options()

    def punctuation_options(self):
        print(f"\nCurrent punctuation is {self.punctuation}")
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
                self.punctuation = pn[i]
                self.oshelf["punctuation"] = self.punctuation
                print(f"Punctuation set to {self.punctuation}")

    def main_menu(self):
        self.oshelf.close()
        Run().main_menu()

    def quit(self):
        self.oshelf.close()
        Run().goodbye()

    def __add_email__(self):
        ok, e = Helpers().__add_entry__(self.emails, self.oshelf, "emails")
        Helpers().__display_list__(self.emails, "emails")
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
            self.usernames, self.oshelf, "usernames")
        Helpers().__display_list__(self.usernames, "usernames")
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
        if len(self.emails) == 1:
            input("Add an email first\n"
                  "[enter] Go back\n")
            self.email_options()  # back to email options
        print("[enter] Email options\n"
              "[number] Set default email")
        number = Helpers().__valid_number__(self.emails)
        if number == 0:
            if input("Cannot set 'no email' as default\n"
                     "[enter] Email options\n"
                     "[t] Try again\n") == "t":
                self.__default_email__()  # Try again
        elif number in ("", "*"):
            self.email_options()  # back to email options
        else:
            d = self.emails.pop(number)  # remove from list, assign to 'd'
            temp = [self.emails[0], d] + self.emails[1:]  # put back as [1]
            self.emails = temp
            self.oshelf["emails"] = temp
            input(f"'{d}' Saved as default\n"
                  f"[enter]...\n")
        self.email_options()

    def __default_username__(self):
        if len(self.usernames) == 1:
            input("Add a username first\n"
                  "[enter] Go back...\n")
            self.username_options()  # back to username options
        print("[enter] Username options\n"
              "[number] Set default username\n")
        number = Helpers().__valid_number__(self.usernames)
        if number == 0:
            if input("Cannot set 'no username' as default\n"
                     "[enter] Username options\n"
                     "[t] Try again\n") == "t":
                self.__default_username__()  # Try again
        elif number in ("", "*"):
            self.username_options()  # back to username options
        else:
            d = self.usernames.pop(number)  # remove from list, assign to 'd'
            temp = [self.usernames[0], d] + self.usernames[1:]  # user[1]
            self.usernames = temp
            self.oshelf["usernames"] = temp
            input(f"'{d}' Saved as default\n"
                  f"[enter]...\n")

    def __del_email__(self):
        if len(self.emails) == 1:
            input("No emails to delete\n"
                  "[enter]...\n")
            self.email_options()  # back to email options
        print("[enter] Email options\n"
              "[number] Remove email"),
        number = Helpers().__valid_number__(self.emails)
        if number == 0:
            if input("Cannot delete 'no email'\n"
                     "[enter] Email options\n"
                     "[t] Try again\n") == "t":
                self.__del_email__()  # Try again
        elif number not in ("", "*"):
            email = self.emails[number]  # number is valid
            if input(f"Remove {email} ?\n"
                     f"[y] Yes\n"
                     f"[n] No\n") == "y":
                temp = self.emails[:]
                temp.pop(number)
                self.emails = temp
                self.oshelf["emails"] = temp
                input(f"'{email}' deleted\n"
                      f"[enter]...\n")
            else:  # abort remove
                input("Nothing deleted\n"
                      "[enter]...\n")

    def __del_username__(self):
        if len(self.emails) == 1:
            input("No usernames to delete\n"
                  "[enter]...\n")
            self.username_options()  # back to username options
        print("[enter] Username options\n"
              "[number] Remove username"),
        number = Helpers().__valid_number__(self.usernames)
        if number == 0:
            if input("Cannot delete 'no username'\n"
                     "[enter] Username options\n"
                     "[t] Try again\n") \
                    == "t":
                self.__del_username__()  # Try again
        elif number not in ("", "*"):
            username = self.usernames[number]  # number is valid
            if input(f"Remove {username} ?\n"
                     f"[y] Yes\n"
                     f"[n] No\n") == "y":
                temp = self.usernames[:]
                temp.pop(number)
                self.usernames = temp
                self.oshelf["usernames"] = temp
                input(f"'{username}' deleted\n"
                      f"[enter]...\n")
            else:  # abort remove
                input("Nothing deleted\n"
                      "[enter]...\n")

    def __edit_email__(self):
        if len(self.emails) == 1:
            input("No emails to edit\n"
                  "[enter] Email options\n")
            self.email_options()  # options
        print("[enter] Email options\n"
              "[number] Edit email\n")
        if self.__edit_list__(self.emails, "emails"):
            Helpers().__display_list__(self.emails, "emails")
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
        self.oshelf[key][ind] = entry
        Helpers().__display_list__(mylist, key)
        return True

    def __edit_username__(self):
        if len(self.emails) == 1:
            input("No usernames to edit\n"
                  "[enter]...\n")
            return  # options
        print("[enter] Options menu\n"
              "[number] Edit username\n")
        if self.__edit_list__(self.usernames, "usernames"):
            Helpers().__display_list__(self.usernames, "usernames")
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


if __name__ == "__main__":
    NAME = sys.argv[1:]


    def rpm():
        print("args:", sys.argv)
        if NAME:  # Command line argument given ==> Non-Interactive Mode
            Run().no_ui(NAME)  # No user interface
        else:  # No command line argument ==> Interactive Mode
            Run().main_menu()  # User interface


    GRAPH = False  # create a call graph

    if GRAPH:
        from pycallgraph import PyCallGraph
        from pycallgraph.output import GraphvizOutput

        with PyCallGraph(output=GraphvizOutput()):
            rpm()
    else:
        rpm()
