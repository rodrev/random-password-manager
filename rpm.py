#!/usr/bin/env python3
from random import randint, choice
import os
import shelve
import sys

# relative path of directory containing this file
REL = os.path.dirname(sys.argv[0])
# absolute path of directory containing this file
ABS = os.path.abspath(REL)

# Filenames to create in this directory:
OPTIONS = ABS + "/opt"  # to store your options (bytes)
DATA = ABS + "/dat"  # to store your data (bytes)
# PRINT used by 'print all' feature, which allows you to override
# the default PRINT value by entering your own filename
PRINT = ABS + "/txt"  # to print data to text file (text)


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

    def main_menu(self):
        # COMMAND LINE ARGUMENTS (ARGV[0] IS FILEPATH)
        if len(sys.argv) > 1:
            if "--quiet" in sys.argv:
                sys.argv.remove("--quiet")
                Write().get_entry(" ".join(sys.argv[1:]), quiet=True)
            elif "-q" in sys.argv:
                sys.argv.remove("-q")
                Write().get_entry(" ".join(sys.argv[1:]), quiet=True)
            else:
                Write().get_entry(" ".join(sys.argv[1:]))
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
            "1": "Write().new_entry()",
            "2": "Write().new_entry(rand=False)",
            "3": "print(Write().generate_random())",
            "4": "Write().get_entry()",
            "5": "Write().edit_entry()",
            "6": "Write().delete_entry()",
            "7": "self.print_or_save_all()",
            "8": "Write().change_all()",
            "9": "Options().options_menu()",
            "0": "self.quit()"
        }
        i = input()
        if i in menu:
            eval(menu[i])
            input("[enter]...\n")  # pause before looping main menu
        self.main_menu()  # loop main menu until [quit] given

    def print_or_save_all(self):
        dshelf = shelve.open(DATA)  # read only data shelf
        alphabetical = sorted(dshelf)  # sorted list of names
        if len(dshelf) == 0:
            input("No data yet\n"
                  "[enter] main menu\n")
            dshelf.close()
            self.main_menu()  # no data. back to main menu
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for name in alphabetical:
            Helpers().__displayData__(dshelf, name)  # display 'name' data
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        i = input("\n[enter] main menu\n"
                  "[s] save all data to plain text file (not recommended!)")
        if i in ("s", "S"):  # save data to file
            here = input(f"[enter] save to {PRINT}\n"
                         f"[filepath] save here\n")
            if here == "":
                here = PRINT
            mode = "-"
            while mode not in ("", "w", "a"):
                mode = input(f"[enter] cancel\n"
                             f"[w] write {PRINT} (overwrite if it exists)\n"
                             f"[a] append {PRINT}\n").lower()
            if mode == "":
                dshelf.close()
                self.print_or_save_all()  # go back (try again)
            with open(here, mode) as f:  # save data to file f
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", file=f)
                for name in alphabetical:  # iterate (sorted) names
                    print(name, file=f)  # print 'name' to file
                    data = dshelf[name]
                    for key in range(len(data)):  # iterate fields (keys)
                        if data[key]:  # if data in field
                            print(data[key], file=f)  # print to file
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", file=f)
            print(f"{PRINT} {'written' if mode == 'w' else 'appended'}")
            input("[enter]...\n")
        dshelf.close()  # ==> main menu

    @staticmethod
    def quit():
        print("\nGoodbye\n")
        exit()

    # ~~ Setters and getters ~~
    def __setEmails__(self, e):
        self.emails = e

    def __getEmails__(self):
        return self.emails

    def __setUsernames__(self, u):
        self.usernames = u

    def __getUsernames__(self):
        return self.usernames

    def __setLength__(self, l):
        self.length = l

    def __getLength__(self):
        return self.length

    def __setRange__(self, r):
        self.lrange = r

    def __getRange__(self):
        return self.lrange

    def __setPunctuation__(self, p):
        self.punctuation = p

    def __getPunctuation__(self):
        return self.punctuation


class Write:
    def __init__(self):
        run = Run()
        self.emails = run.__getEmails__()
        self.usernames = run.__getUsernames__()
        self.length = run.__getLength__()
        self.lrange = run.__getRange__()
        self.punctuation = run.__getPunctuation__()

    def new_entry(self, rand=True):
        """ open or create DATA shelf and write data to it """
        dshelf = shelve.open(DATA, writeback=True)
        name = ""
        while name == "":
            name = input("Entry [name]: ")
        try:
            data = dshelf[name]  # key error (new 'name') ==> except
            if data:  # no error ('name' exists in DATA)
                print("\n", name, "Entry already exists:")
                print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                Helpers().__displayData__(dshelf, name)  # print 'name' data
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                while True:  # confirm replace
                    i = input(f"[enter] main menu\n"
                              f"[t] try again\n"
                              f"[e] edit\n"
                              f"[type 'replace'] replace {name}'\n")
                    if i == "":
                        dshelf.close()
                        Run().main_menu()
                    elif i in ("t", "T"):  # try again
                        dshelf.close()
                        self.new_entry()
                    elif i in ("e", "E"):
                        dshelf.close()
                        self.edit_entry(name)
                    elif i == "replace":  # YES ==> replace with new
                        new = self.__inputData__(dshelf, rand)  # data tuple
                        dshelf[name][0] = new[0]  # shelf email
                        dshelf[name][1] = new[1]  # shelf username
                        dshelf[name][2] = new[2]  # shelf p
                        dshelf[name][3] = new[3]  # shelf notes
                        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        Helpers().__displayData__(dshelf, name)
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                        input("Saved\n"
                              "[enter]...\n")
                        break
            else:
                raise KeyError  # 'name' in DATA but no data ==> except
        except KeyError:
            # new 'name' or no data. get new data & write to DATA
            new = self.__inputData__(dshelf, rand)  # input/make data tuple
            dshelf[name] = {0: new[0],  # shelf email
                            1: new[1],  # shelf username
                            2: new[2],  # shelf p
                            3: new[3]}  # shelf notes
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            Helpers().__displayData__(dshelf, name)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            input("Saved\n"
                  "[enter]...\n")
        except IOError:  # problem writing!
            print(f"Could not write to {DATA}\n"
                  f"Make sure {DATA} is a valid filename\n"
                  f"Edit/add filenames via [options] submenu")
            input("[enter] main menu\n")
            dshelf.close()
            Run().main_menu()  # can't write. back to main menu
        finally:
            dshelf.close()

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

    def get_entry(self, name="", quiet=False):
        dshelf = shelve.open(DATA)  # read only
        if len(dshelf) > 0:
            try:
                if name:
                    try:
                        Helpers.__displayData__(dshelf, name=name, quiet=quiet)
                    except KeyError:
                        print('not found')
                        pass
                    finally:
                        dshelf.close()
                        exit()
                print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("Names:")
                for key in sorted(dshelf):
                    print(key)  # display names
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                name = input("[enter] main menu\n"
                             "[name] get entry\n")
                if name:
                    Helpers.__displayData__(dshelf, name)  # display data
                    input("[enter]...\n")
                else:
                    dshelf.close()
                    Run().main_menu()  # escape to main menu
            except KeyError:
                print('name not found')
                pass
        else:
            input("Database is empty\n"
                  "Make a new entry first\n"
                  "[enter]...\n")
            dshelf.close()
            Run().main_menu()  # escape to main menu
        dshelf.close()
        self.get_entry()  # get another until [enter] for main menu

    def edit_entry(self, name=None):
        dshelf = shelve.open(DATA, writeback=True)
        if len(dshelf) == 0:
            input("No data yet\n"
                  "[enter] main menu\n")
            dshelf.close()
            Run().main_menu()  # no data. back to main menu
        if name is None:  # also accept name as argument
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Names:")  # user chooses name
            for key in sorted(dshelf):
                print(key)  # display names alphabetically
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            name = input("[enter] main menu\n"
                         "[name] entry to edit\n")
            if name == "":
                dshelf.close()
                Run().main_menu()  # escape to main menu
        try:
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            Helpers.__displayData__(dshelf, name)  # display data for 'name'
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            i = input("EDIT\n"
                      "[e] email\n"
                      "[u] username\n"
                      "[p] p a s s w o r d\n"
                      "[n] note\n"
                      "[enter] done\n")
            if i in ("e", "E"):
                dshelf[name][0] = self.__chooseEmail__()  # edit email
                input("Saved\n"
                      "[enter]...\n")
            elif i in ("u", "U"):  # edit username
                dshelf[name][1] = self.__chooseUsername__()
                input("Saved\n"
                      "[enter]...\n")
            elif i in ("p", "P"):
                i, p = "", ""
                i = input("[enter] none\n"
                          "[r] random\n"
                          "[m] manual\n")
                if i in ("r", "R"):
                    p = self.generate_random()  # random p.w.
                elif i in ("m", "M"):
                    p = self.__enter_p_w__()  # manual p.w.
                if i and p:
                    dshelf[name][2] = p
                    input("Saved\n"
                          "[enter]...\n")
                else:
                    if input("\nblank p.w.? [y]es, [n]o: ") in ("y", "Y"):
                        dshelf[name][2] = ""
                        input("Saved\n"
                              "[enter]...\n")
                    else:
                        input("Unchanged\n"
                              "[enter]...\n")
            elif i in ("n", "N"):
                def add_note():
                    """ add note on new line until [enter] is pressed """
                    add = input("[enter] done\n"
                                "[note]\n")
                    return add + "\n" + add_note() if add else ""

                notes = dshelf[name][3].split("\n")  # split lines into list
                ln = len(notes)
                for n in range(ln):
                    print(n + 1, notes[n])
                if ln > 1:
                    while True:
                        i = input("[enter] go back\n"
                                  "[a] add note\n"
                                  "[number] edit note\n")
                        if i == "":
                            dshelf.close()
                            self.edit_entry()
                        elif i in ("a", "A"):
                            n = add_note().split("\n")
                            notes += n  # append new line(s) to list
                            dshelf[name][3] = "\n".join(notes)
                            input("Saved\n"
                                  "[enter]...\n")
                            break
                        try:  # try to edit note by line number
                            i = int(i)
                            assert i > 0
                            notes[i - 1] = input("New line: ")
                            dshelf[name][3] = "\n".join(notes)
                            input("Saved\n"
                                  "[enter]...\n")
                            break
                        except (IndexError, ValueError, AssertionError):
                            pass
                else:  # note is empty or one line
                    i = "-"
                    while i not in "aAeE":  # excludes [enter] ""
                        i = input("[a] add note\n"
                                  "[e] edit note\n")
                        if i in ("a", "A"):
                            dshelf[name][3] += add_note()
                            input("Saved\n"
                                  "[enter]...\n")
                        elif i in ("e", "E"):
                            n = add_note()
                            dshelf[name][3] = n
                            input("Saved\n"
                                  "[enter]...\n")
            else:
                dshelf.close()
                Run().main_menu()  # escape to main menu
            dshelf.close()  # save and close shelf
            self.edit_entry(name)  # edit same name (until escaped)
        except KeyError:
            i = input(f"No data for '{name}'\n"
                      f"[enter] main menu\n"
                      f"[t] try again\n")
            dshelf.close()  # try new name
            self.edit_entry() if i in ("t", "T") else Run().main_menu()

    def delete_entry(self):
        """ Delete entry by name from DATA.  Returns (None) to Main Menu """
        dshelf = shelve.open(DATA, writeback=True)
        if len(dshelf) == 0:
            input("No data yet\n"
                  "[enter] main menu\n")
            dshelf.close()
            Run().main_menu()  # no data. back to main menu
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Names:")
        for e in sorted(dshelf):
            print(e)  # display names
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        i = input("[enter] main menu\n"
                  "[name] entry to delete\n")
        if i == "":
            dshelf.close()
            Run().main_menu()
        elif i not in dshelf:
            dshelf.close()
            print("No entry for that name")
            if input("[enter] main menu\n"
                     "[t] try again\n") in ("t", "T"):
                self.delete_entry()  # try again
        else:
            deleted = False
            if input(f"Confirm delete '{i}'\n"
                     f"[y] yes\n"
                     f"[n] no\n").lower() in ("y", "yes"):
                del dshelf[i]  # delete entry 'i' from dshelf
                deleted = True
            i = input("Deleted\n"
                      "[enter] main menu\n"
                      "[d] delete another\n") \
                if deleted else \
                input("Nothing deleted\n"
                      "[enter] main menu\n"
                      "[t] try again\n")
            dshelf.close()
            if i.lower() in ("d", "t"):
                self.delete_entry()  # try again

    def change_all(self):
        dshelf = shelve.open(DATA, writeback=True)
        if len(dshelf) == 0:
            input("No data yet\n"
                  "[enter] main menu\n")
            dshelf.close()
            Run().main_menu()  # no data. back to main menu
        i = input("Change all p a s s w o r d s  (make all new random)\n"
                  "[enter] main menu\n"
                  "Confirm by typing 'change all'\n")
        if i.lower() == "change all":
            for entry in dshelf:
                print("\n" + entry)
                new = self.generate_random()
                print(new)
                dshelf[entry][2] = new
            dshelf.close()
            input("Success\n"
                  "[enter]...\n")  # main menu
        elif i == "":  # escape to main menu
            dshelf.close()
            Run().main_menu()
        else:  # bad input. try again
            dshelf.close()
            self.change_all()

    def __chooseEmail__(self):
        Helpers().__displayList__(self.emails, "emails")
        print("[enter] default\n"
              "[*] other\n"
              "[number] select\n"),
        i = Helpers().__valid_number__(self.emails)
        if i == "":  # default email (if exists)
            return self.emails[1] if len(self.emails) > 1 else ""
        elif i == "*":  # other
            # First input email and save it to OPTIONS
            oshelf = shelve.open(OPTIONS, writeback=True)
            ok, email = Helpers().__addEntry__(self.emails, oshelf, "emails")
            oshelf.close()
            print(email, "Saved to your email list") if ok else \
                print(f"Already have {email} saved")
            return email  # return email either way
        else:
            return self.emails[i]  # select email

    def __chooseUsername__(self):
        Helpers().__displayList__(self.usernames, "usernames")
        print("[enter] default\n"
              "[*] other\n"
              "[number] select\n")
        i = Helpers().__valid_number__(self.usernames)
        if i == "":  # default username (if exists)
            return self.usernames[1] if len(self.usernames) > 1 else ""
        elif i == "*":  # other
            # First add the username and save it to OPTIONS
            oshelf = shelve.open(OPTIONS, writeback=True)
            ok, username = Helpers().__addEntry__(self.usernames, oshelf,
                                                  "usernames")
            oshelf.close()
            print(username, "Saved to your usernames list") if ok else \
                print(f"Already have {username} saved")
            return username  # return username either way
        else:
            return self.usernames[i]  # select username

    def __writeP__(self, dshelf, rand=True):
        if rand:
            return self.generate_random()  # random
        else:
            m = self.__enter_p_w__()  # manual
            if m:
                return m
            else:
                dshelf.close()
                Run().main_menu()  # cancelled. back to main menu

    def __writeNotes__(self, result):
        """ add note on new line until [enter] is pressed """
        add = input("[enter] done\n"
                    "[note]\n")
        if add:
            result.append(add)
            self.__writeNotes__(result)
        return "\n".join(result)

    def __inputData__(self, dshelf, rand=True):
        return self.__chooseEmail__(), self.__chooseUsername__(), \
               self.__writeP__(dshelf, rand), self.__writeNotes__([])

    def __enter_p_w__(self):
        p, p1 = "", ""
        while p == "":
            p = input("Input p a s s w o r d\n")
        while p1 == "":
            p1 = input("Input again to confirm\n")
        if p == p1:
            return p  # match confirmed
        else:
            if input("P a s s w o r d s did not match\n"
                     "[enter] cancel\n"
                     "[t] try again\n") in ("t", "T"):
                return self.__enter_p_w__()  # try again
            return None  # cancel


class Options:
    def __init__(self):
        run = Run()
        self.emails = run.__getEmails__()
        self.usernames = run.__getUsernames__()
        self.length = run.__getLength__()
        self.lrange = run.__getRange__()
        self.punctuation = run.__getPunctuation__()

    def options_menu(self):
        oshelf = shelve.open(OPTIONS, writeback=True)  # edit OPTIONS shelf
        print("\n~~~~~~~~~~~~~~~\n"
              "  options\n"
              "~~~~~~~~~~~~~~~\n"
              "[1] emails\n"
              "[2] usernames\n"
              "[3] length\n"
              "[4] range\n"
              "[5] punctuation\n"
              "~~~~~~~~~~~~~~~\n"
              "[6] main menu\n"
              "[7] quit\n"
              "~~~~~~~~~~~~~~~\n")
        option = input()
        if option == "1":
            self.email_options(oshelf)  # emails
        elif option == "2":
            self.username_options(oshelf)  # usernames
        elif option == "3":
            self.length_options(oshelf)  # length
        elif option == "4":
            self.range_options(oshelf)  # range
        elif option == "5":
            self.punctuation_options(oshelf)  # punctuation
        elif option == "6":
            oshelf.close()
            Run().main_menu()  # main menu
        elif option == "7":
            oshelf.close()
            print("Goodbye!\n")
            exit()  # quit
        oshelf.close()  # always close OPTIONS shelf
        self.options_menu()  # always runOptions until [main menu] or [exit]

    def email_options(self, oshelf):
        Helpers().__displayList__(self.emails, "emails")
        option = input("[enter] back to options\n"
                       "[a] add\n"
                       "[d] delete\n"
                       "[e] edit\n"
                       "[s] set default\n")
        if option == "":
            oshelf.close()  # escape to option menu
            self.options_menu()
        elif option in ("a", "A"):  # add email
            self.__addEmail__(oshelf)
        elif option in ("d", "D"):  # delete email
            self.__delEmail__(oshelf)
        elif option in ("e", "E"):  # edit email
            self.__editEmail__(oshelf)
        elif option in ("s", "S"):
            self.__defaultEmail__(oshelf)  # set default email
        self.email_options(oshelf)  # loop email options until escaped

    def username_options(self, oshelf):
        Helpers().__displayList__(self.usernames, "usernames")
        option = input("[enter] options menu\n"
                       "[a] add\n"
                       "[d] delete\n"
                       "[e] edit\n"
                       "[s] set default\n")
        if option == "":
            oshelf.close()  # escape to option menu
            self.options_menu()
        elif option in ("a", "A"):  # add username
            self.__addUsername__(oshelf)
        elif option in ("d", "D"):  # delete username
            self.__delUsername__(oshelf)
        elif option in ("e", "E"):  # edit username
            self.__editUsername__(oshelf)
        elif option in ("s", "S"):
            self.__defaultUsername__(oshelf)  # set default username
        self.username_options(oshelf)  # loop username options until escaped

    def length_options(self, oshelf):
        print("\ncurrent length is", str(self.length) + " characters")
        ln = input("[enter] options menu\n"
                   "[length]\n")
        if ln != "":  # not [enter] ("")
            try:
                ln = int(ln)
                assert ln > 0
                self.length = ln
                oshelf["length"] = ln
                print(f"Length set to {ln} characters")
            except (ValueError, AssertionError):  # bad input try again
                print("Length must be a positive integer")
                self.length_options(oshelf)

    def range_options(self, oshelf):
        print(f"\nRange to randomize p.w. length\n"
              f"\tE.g. range 2 and length 15\n"
              f"\trandomizes p.w. length between 13 to 17 characters\n"
              f"Current range is {self.lrange}")
        try:
            r = input("[enter] options menu\n"
                      "Set range\n")
            if r != "":  # not [enter] ("")
                r = int(r)
                assert r >= 0
                self.lrange = r
                oshelf["lrange"] = r
                print(f"Range set to +/- {r} characters")
        except (ValueError, AssertionError):  # bad input try again
            print("Range must be a non-negative integer")
            self.range_options(oshelf)

    def punctuation_options(self, oshelf):
        print("\ncurrent punctuation", self.punctuation)
        print("""
        [enter] options menu
        [a] all !#$%&()*+,-./:;<=>?@[]^_{|}~
        [s] some %+-./:=@_
        [l] limited @._-
        [n] none
        """)
        pn = {"a": "all", "s": "some", "l": "limited", "n": "none"}
        i = "input string"
        while (len(i) > 0) and (i not in pn):
            i = input().lower()  # loop if bad input
            if i in pn:
                self.punctuation = pn[i]
                oshelf["punctuation"] = self.punctuation
                print(f"Punctuation set to {self.punctuation}")

    def __addEmail__(self, oshelf):
        ok, e = Helpers().__addEntry__(self.emails, oshelf, "emails")
        Helpers().__displayList__(self.emails, "emails")
        i = input("Saved\n"
                  "[enter] email options\n"
                  "[a] add another\n") \
            if ok else input(f"Already have '{e}' saved\n"
                             f"[enter] email options\n"
                             f"[t] try again\n")
        if i.lower() in ("a", "t"):
            self.__addEmail__(oshelf)  # add another/try again

    def __addUsername__(self, oshelf):
        ok, u = Helpers().__addEntry__(self.usernames, oshelf, "usernames")
        Helpers().__displayList__(self.usernames, "usernames")
        i = input("Saved\n"
                  "[enter] username options\n"
                  "[a] add another\n") \
            if ok else input(f"Already have '{u}' saved\n"
                             f"[enter] username options\n"
                             f"[t] try again\n")
        if i.lower() in ("a", "t"):
            self.__addUsername__(oshelf)  # add another/try again

    def __delEmail__(self, oshelf):
        if len(self.emails) == 1:
            input("No emails to delete\n"
                  "[enter]...\n")
            self.email_options(oshelf)  # back to email options
        print("[enter] email options\n"
              "[number] remove email"),
        number = Helpers().__valid_number__(self.emails)
        if number == 0:
            if input("Cannot delete 'no email'\n"
                     "[enter] email options\n"
                     "[t] try again\n") in ("t", "T"):
                self.__delEmail__(oshelf)  # try again
        elif number not in ("", "*"):
            email = self.emails[number]  # number is valid
            if input(f"Remove {email} ?\n"
                     f"[y] yes\n"
                     f"[n] no\n").lower() in ("y", "yes"):
                temp = self.emails[:]
                temp.pop(number)
                self.emails = temp
                oshelf["emails"] = temp
                input(f"'{email}' deleted\n"
                      f"[enter]...\n")
            else:  # abort remove
                input("Nothing deleted\n"
                      "[enter]...\n")

    def __delUsername__(self, oshelf):
        if len(self.emails) == 1:
            input("No usernames to delete\n"
                  "[enter]...\n")
            self.username_options(oshelf)  # back to username options
        print("[enter] username options\n"
              "[number] remove username"),
        number = Helpers().__valid_number__(self.usernames)
        if number == 0:
            if input("Cannot delete 'no username'\n"
                     "[enter] username options\n"
                     "[t] try again\n") \
                    in ("t", "T"):
                self.__delUsername__(oshelf)  # try again
        elif number not in ("", "*"):
            username = self.usernames[number]  # number is valid
            if input(f"Remove {username} ?\n"
                     f"[y] yes\n"
                     f"[n] no\n").lower() in ("y", "yes"):
                temp = self.usernames[:]
                temp.pop(number)
                self.usernames = temp
                oshelf["usernames"] = temp
                input(f"'{username}' deleted\n"
                      f"[enter]...\n")
            else:  # abort remove
                input("Nothing deleted\n"
                      "[enter]...\n")

    def __editEmail__(self, oshelf):
        if len(self.emails) == 1:
            input("No emails to edit\n"
                  "[enter] email options\n")
            self.email_options(oshelf)  # options
        print("[enter] email options\n"
              "[number] edit email\n")
        if self.__editList__(self.emails, oshelf, "emails"):
            Helpers().__displayList__(self.emails, "emails")
            i = input("[enter] email options\n"
                      "[e] edit another\n")
        else:
            i = input("[enter] email options\n"
                      "[t] try again\n")
        if i.lower() in ("e", "t"):  # edit another/try again
            self.__editEmail__(oshelf)

    def __editUsername__(self, oshelf):
        if len(self.emails) == 1:
            input("No usernames to edit\n"
                  "[enter]...\n")
            return  # options
        print("[enter] options menu\n"
              "[number] edit username\n")
        if self.__editList__(self.usernames, oshelf, "usernames"):
            Helpers().__displayList__(self.usernames, "usernames")
            i = input("[enter] username options\n"
                      "[e] edit another\n")
        else:
            i = input("[enter] username options\n"
                      "[t] try again\n")
        if i.lower() in ("e", "t"):  # edit another/try again
            self.__editUsername__(oshelf)

    def __defaultEmail__(self, oshelf):
        if len(self.emails) == 1:
            input("Add an email first\n"
                  "[enter] go back\n")
            self.email_options(oshelf)  # back to email options
        print("[enter] email options\n"
              "[number] set default email")
        number = Helpers().__valid_number__(self.emails)
        if number == 0:
            if input("Cannot set 'no email' as default\n"
                     "[enter] email options\n"
                     "[t] try again\n") \
                    in ("t", "T"):
                self.__defaultEmail__(oshelf)  # try again
        elif number in ("", "*"):
            self.email_options(oshelf)  # back to email options
        else:
            d = self.emails.pop(number)  # remove from list, assign to 'd'
            temp = [self.emails[0], d] + self.emails[1:]  # put back as [1]
            self.emails = temp
            oshelf["emails"] = temp
            input(f"'{d}' Saved as default\n"
                  f"[enter]...\n")
        self.email_options(oshelf)

    def __defaultUsername__(self, oshelf):
        if len(self.usernames) == 1:
            input("Add a username first\n"
                  "[enter] go back...\n")
            self.username_options(oshelf)  # back to username options
        print("[enter] username options\n"
              "[number] set default username\n")
        number = Helpers().__valid_number__(self.usernames)
        if number == 0:
            if input("Cannot set 'no username' as default\n"
                     "[enter] username options\n"
                     "[t] try again\n") \
                    in ("t", "T"):
                self.__defaultUsername__(oshelf)  # try again
        elif number in ("", "*"):
            self.username_options(oshelf)  # back to username options
        else:
            d = self.usernames.pop(number)  # remove from list, assign to 'd'
            temp = [self.usernames[0], d] + self.usernames[1:]  # user[1]
            self.usernames = temp
            oshelf["usernames"] = temp
            input(f"'{d}' Saved as default\n"
                  f"[enter]...\n")

    def __editList__(self, mylist, oshelf, key):
        ind = Helpers().__valid_number__(mylist)
        if ind == "":
            if key == "emails":
                self.email_options(oshelf)
            elif key == "usernames":
                self.username_options(oshelf)
        elif ind == 0:
            print("0 is no username")
            return False
        entry = input("Email:\n") if key == "emails" else input("Username:\n")
        if entry in mylist:
            print(f"Already have {entry} saved")
            return False
        mylist[ind] = entry
        oshelf[key][ind] = entry
        Helpers().__displayList__(mylist, key)
        return True


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
    def __addEntry__(mylist, oshelf, key):
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
    def __displayList__(mylist, title):
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(title + ":")
        for n in range(len(mylist)):
            if n == 0:
                print(n, "none")
            elif n == 1:
                print(n, mylist[n], "default")
            else:
                print(n, mylist[n])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    @staticmethod
    def __displayData__(dshelf, name, quiet=False):
        data = dshelf[name]  # data is itself a dictionary object
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
            for key in range(len(data)):  # keys were defined as 0, 1, 2, 3
                if data[key]:
                    print(data[key])  # display contents of field if any
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


if __name__ == "__main__":
    Run().main_menu()
