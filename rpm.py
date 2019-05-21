from random import randint, choice
import os
import shelve
import sys

# relative path of directory containing this file.
REL = os.path.dirname(sys.argv[0])
# absolute path of directory containing this file.
ABS = os.path.abspath(REL)

# Filenames to create in this directory:
OPTIONS = ABS + "/opt"  # to store your options (bytes).
DATA = ABS + "/dat"  # to store your data (bytes).
# PRINT used by 'print all' feature, which allows you to override
# the default PRINT value by entering your own filename.
PRINT = ABS + "/txt"  # to print data to text file (text).


class Run:
    def __init__(self):
        # Defaults: emails, usernames, length, lrange, punctuation.
        e, u, le, lr, p = [""], [""], 15, 0, "all"
        if os.path.isfile(OPTIONS):  # OPTIONS file found.
            oshelf = shelve.open(OPTIONS, writeback=True)  # options shelf.
            try:  # get settings from OPTIONS file.
                e = oshelf["emails"]
                u = oshelf["usernames"]
                le = oshelf["length"]
                lr = oshelf["lrange"]
                p = oshelf["punctuation"]
                oshelf.close()
            except KeyError:
                print(f"options file {OPTIONS} corrupted. delete it and run"
                      f"again to make a new one.")
                oshelf.close()
                exit(101)
        else:  # OPTIONS not found. Setting defaults.
            print("~~~~~ welcome to random p.a.s.s.w.o.r.d. manager ~~~~~")
            print(OPTIONS, "file created. default options saved.\n"
                           "select [options] from menu to customize.\n")
            # Create OPTIONS file to shelve defaults into like a dictionary..
            # Strings (keys) : Any object (values).
            oshelf = shelve.open(OPTIONS, writeback=True)
            oshelf["emails"] = e
            oshelf["usernames"] = u
            oshelf["length"] = le
            oshelf["lrange"] = lr
            oshelf["punctuation"] = p
            oshelf.close()
        # Initialize defaults if OPTIONS file not found.
        # Otherwise, initialize from OPTIONS file.
        self.emails = e
        self.usernames = u
        self.length = le
        self.lrange = lr
        self.punctuation = p

    def main_menu(self):
        # COMMAND LINE ARGUMENTS (ARGV[0] IS FILENAME).
        if len(sys.argv) > 1:
            if "--quiet" in sys.argv:
                sys.argv.remove("--quiet")
                Write().get(" ".join(sys.argv[1:]), quiet=True)
            elif "-q" in sys.argv:
                sys.argv.remove("-q")
                Write().get(" ".join(sys.argv[1:]), quiet=True)
            else:
                Write().get(" ".join(sys.argv[1:]))
        print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 random p.a.s.s.w.o.r.d. manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[1] make
[2] enter yourself
[3] quick
~~~~~~~~~~~~~~~~~~
[4] get
[5] edit
[6] delete
~~~~~~~~~~~~~~~~~~
[7] print all
[8] change all
~~~~~~~~~~~~~~~~~~
[9] options
[0] quit
~~~~~~~~~~~~~~~~~~
""")
        menu = {
            "1": "Write().make()",  # ==> make.
            "2": "Write().make(rand=False)",  # ==> enter yourself.
            "3": "print(Write().quick())",  # ==> quick.
            "4": "Write().get()",  # ==> get.
            "5": "Write().edit()",  # ==> edit.
            "6": "Write().delete()",  # ==> delete.
            "7": "self.print_all()",  # ==> print all to text file.
            "8": "Write().change_all()",  # ==> change all.
            "9": "Options().options_menu()",  # ==> options.
            "0": "self.quit()"  # ==> quit.
        }
        i = input()
        if i in menu:
            eval(menu[i])
            input("[enter]...\n")  # pause before looping main menu.
        self.main_menu()  # loop main menu until [quit] given.

    def print_all(self):
        dshelf = shelve.open(DATA)  # read only data shelf.
        alphabetical = sorted(dshelf)  # returns sorted list of names.
        if len(dshelf) == 0:
            input("no data yet.\n"
                  "[enter] main menu.\n")
            dshelf.close()
            self.main_menu()  # no data. back to main menu.
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for name in alphabetical:
            Helpers().__displayData__(dshelf, name)  # display 'name' data.
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        i = input("\n[enter] main menu.\n"
                  "[p] print all data to file: ")
        if i in ("p", "P"):  # print data to file.
            print("\ncaution!\n"
                  "this creates a text file with all your data.\n"
                  "strongly recommended to delete it once you are done with "
                  "it.\nyou can always get your data via this app, which "
                  "should be p.w. protected.\n")
            here = input(f"[enter] print to {PRINT}.\n"
                         f"[filename] print here.\n")
            if here == "":
                here = PRINT
            mode = "-"
            while mode not in "wa":  # also excludes [enter] "".
                mode = input("[enter] cancel.\n"
                             "[w] write (overwrite).\n"
                             "[a] append.\n").lower()
            if mode == "":
                dshelf.close()
                self.print_all()  # go back (try again).
            with open(here, mode) as f:  # print name data to file f.
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", file=f)
                for name in alphabetical:  # iterate (sorted) names.
                    print(name, file=f)  # print 'name' to file.
                    data = dshelf[name]
                    for key in range(len(data)):  # iterate fields (keys).
                        if data[key]:  # if data in field.
                            print(data[key], file=f)  # print to file.
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", file=f)
            m = "written" if mode == "w" else "appended"
            print("success. data", m, "to", PRINT + ".")
            input("[enter]...\n")
        dshelf.close()  # ==> main menu.

    @staticmethod
    def quit():
        print("\nGoodbye.\n")
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

    def make(self, rand=True):
        """ open or create DATA shelf and write data to it """
        dshelf = shelve.open(DATA, writeback=True)
        name = ""
        while name == "":
            name = input("entry [name]: ")
        try:
            data = dshelf[name]  # key error (new 'name') ==> except.
            if data:  # no error ('name' exists in DATA).
                print("\n", name, "entry already exists:")
                print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                Helpers().__displayData__(dshelf, name)  # print 'name' data.
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                while True:  # confirm replace.
                    i = input("[enter] main menu.\n"
                              "[t]ry again.\n"
                              "[e]dit.\n"
                              "confirm by typing 'replace':\n")
                    if i == "":
                        dshelf.close()
                        Run().main_menu()
                    elif i in ("t", "T"):  # try again.
                        dshelf.close()
                        self.make()
                    elif i in ("e", "E"):
                        dshelf.close()
                        self.edit(name)
                    elif i == "replace":  # YES ==> replace with new.
                        new = self.__inputData__(dshelf, rand)  # data tuple.
                        dshelf[name][0] = new[0]  # shelf email.
                        dshelf[name][1] = new[1]  # shelf username.
                        dshelf[name][2] = new[2]  # shelf p.
                        dshelf[name][3] = new[3]  # shelf notes.
                        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        Helpers().__displayData__(dshelf, name)
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                        input("saved.\n"
                              "[enter]...\n")
                        break
            else:
                raise KeyError  # 'name' in DATA but no data ==> except.
        except KeyError:
            # new 'name' or no data. get new data & write to DATA.
            new = self.__inputData__(dshelf, rand)  # input/make data tuple.
            dshelf[name] = {0: new[0],  # shelf email.
                            1: new[1],  # shelf username.
                            2: new[2],  # shelf p.
                            3: new[3]}  # shelf notes.
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            Helpers().__displayData__(dshelf, name)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            input("saved.\n"
                  "[enter]...\n")
        except IOError:  # problem writing!
            print(f"could not write to: {DATA}\n"
                  f"make sure {DATA} is a valid filename.\n"
                  f"you can edit/add filenames via [options]."
                  )
            input("[enter] main menu.\n")
            dshelf.close()
            Run().main_menu()  # can't write. back to main menu.
        finally:
            dshelf.close()

    def quick(self):
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

    def get(self, name="", quiet=False):
        dshelf = shelve.open(DATA)  # read only.
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
                        exit()  # quick exit.
                print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("names:")
                for key in sorted(dshelf):
                    print(key)  # display names.
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                name = input("[enter] main menu.\n"
                             "[name] get entry.\n")
                if name:
                    Helpers.__displayData__(dshelf, name)  # display data.
                    input("[enter]...\n")
                else:
                    dshelf.close()
                    Run().main_menu()  # escape to main menu.
            except KeyError:
                print('name not found')
                pass
        else:
            input("database is empty.\n"
                  "make an entry first [enter]...\n")
            dshelf.close()
            Run().main_menu()  # escape to main menu.
        dshelf.close()
        self.get()  # get another until [enter] for main menu.

    def edit(self, name=None):
        dshelf = shelve.open(DATA, writeback=True)
        if len(dshelf) == 0:
            input("no data yet.\n"
                  "[enter] main menu.\n")
            dshelf.close()
            Run().main_menu()  # no data. back to main menu.
        if name is None:  # also accept name as argument.
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("names:")  # user chooses name...
            for key in sorted(dshelf):
                print(key)  # display names alphabetically.
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            name = input("[enter] main menu.\n"
                         "[name] entry to edit.\n")
            if name == "":
                dshelf.close()
                Run().main_menu()  # escape to main menu.
        try:
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            Helpers.__displayData__(dshelf, name)  # display data for 'name'.
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            i = input("[enter] done.\n"
                      "EDIT:\n"
                      "[e] email.\n"
                      "[u] username.\n"
                      "[p] p.a.s.s.w.o.r.d..\n"
                      "[n] note(s).\n")
            if i in ("e", "E"):
                dshelf[name][0] = self.__chooseEmail__()  # edit email.
                input("saved.\n"
                      "[enter]...\n")
            elif i in ("u", "U"):  # edit username.
                dshelf[name][1] = self.__chooseUsername__()
                input("saved.\n"
                      "[enter]...\n")
            elif i in ("p", "P"):
                i, p = "", ""
                i = input("[enter] none.\n"
                          "[r] random.\n"
                          "[m] manual.\n")
                if i in ("r", "R"):
                    p = self.quick()  # random p.w.
                elif i in ("m", "M"):
                    p = self.__enter_p_w__()  # manual p.w.
                if i and p:
                    dshelf[name][2] = p
                    input("saved.\n"
                          "[enter]...\n")
                else:
                    if input("\nblank p.w.? [y]es, [n]o: ") in ("y", "Y"):
                        dshelf[name][2] = ""
                        input("saved.\n"
                              "[enter]...\n")
                    else:
                        input("unchanged.\n"
                              "[enter]...\n")
            elif i in ("n", "N"):
                def add_note():
                    """ add note on new line until [enter] is pressed """
                    add = input("[enter] done.\n"
                                "[note].\n")
                    return add + "\n" + add_note() if add else ""

                notes = dshelf[name][3].split("\n")  # split lines into list.
                ln = len(notes)
                for n in range(ln):
                    print(n + 1, notes[n])
                if ln > 1:
                    while True:
                        i = input("[enter] go back.\n"
                                  "[a] add note(s).\n"
                                  "[number] edit note.\n")
                        if i == "":
                            dshelf.close()
                            self.edit()
                        elif i in ("a", "A"):
                            n = add_note().split("\n")
                            notes += n  # append new line(s) to list.
                            dshelf[name][3] = "\n".join(notes)
                            input("saved.\n"
                                  "[enter]...\n")
                            break
                        try:  # try to edit note by line number.
                            i = int(i)
                            assert i > 0
                            notes[i - 1] = input("new line: ")
                            dshelf[name][3] = "\n".join(notes)
                            input("saved.\n"
                                  "[enter]...\n")
                            break
                        except (IndexError, ValueError, AssertionError):
                            pass
                else:  # note is empty or one line.
                    i = "-"
                    while i not in "aAeE":  # excludes [enter] "" also.
                        i = input("[a] add note(s).\n"
                                  "[e] edit note.\n")
                        if i in ("a", "A"):
                            dshelf[name][3] += add_note()
                            input("saved.\n"
                                  "[enter]...\n")
                        elif i in ("e", "E"):
                            n = add_note()
                            dshelf[name][3] = n
                            input("saved.\n"
                                  "[enter]...\n")
            else:
                dshelf.close()
                Run().main_menu()  # escape to main menu.
            dshelf.close()  # save and close shelf.
            self.edit(name)  # edit same name (until escaped).
        except KeyError:
            i = input(f"no data for '{name}'.\n"
                      f"[enter] main menu.\n"
                      f"[t] try again.\n")
            dshelf.close()  # [t]ry new name.
            self.edit() if i in ("t", "T") else Run().main_menu()

    def delete(self):
        """ Delete entry by name from DATA.  Returns (None) to Main Menu """
        dshelf = shelve.open(DATA, writeback=True)
        if len(dshelf) == 0:
            input("no data yet.\n"
                  "[enter] main menu.\n")
            dshelf.close()
            Run().main_menu()  # no data. back to main menu.
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("names:")
        for e in sorted(dshelf):
            print(e)  # display names.
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        i = input("[enter] main menu.\n"
                  "[name] of entry to delete.\n")
        if i == "":
            dshelf.close()
            Run().main_menu()
        elif i not in dshelf:
            dshelf.close()
            print("no entry for that name.")
            if input("[enter] main menu.\n"
                     "[t] try again:\n") in ("t", "T"):
                self.delete()  # try again.
        else:
            deleted = False
            if input(f"confirm delete entry '{i}'.\n"
                     f"[y] yes.\n"
                     f"[n] no.\n").lower() in ("y", "yes"):
                del dshelf[i]  # delete entry 'i' from dshelf.
                deleted = True
            i = input("deleted.\n"
                      "[enter] main menu.\n"
                      "[d] delete another.\n") \
                if deleted else \
                input("nothing deleted.\n"
                      "[enter] main menu.\n"
                      "[t] try again\n")
            dshelf.close()
            if i.lower() in ("d", "t"):
                self.delete()  # try again.

    def change_all(self):
        dshelf = shelve.open(DATA, writeback=True)
        if len(dshelf) == 0:
            input("no data yet.\n"
                  "[enter] main menu.\n")
            dshelf.close()
            Run().main_menu()  # no data. back to main menu.
        i = input("change all p.a.s.s.w.o.r.d.s. (make all new random).\n"
                  "[enter] main menu.\n"
                  "confirm by typing 'change all'.\n")
        if i.lower() == "change all":
            for entry in dshelf:
                print("\n" + entry)
                new = self.quick()
                print(new)
                dshelf[entry][2] = new
            dshelf.close()
            input("success.\n"
                  "[enter]...\n")  # main menu.
        elif i == "":  # escape to main menu.
            dshelf.close()
            Run().main_menu()
        else:  # bad input. try again.
            dshelf.close()
            self.change_all()

    def __chooseEmail__(self):
        Helpers().__displayList__(self.emails, "emails")
        print("[enter] default.\n"
              "[*] other.\n"
              "[number] select.\n"),
        i = Helpers().__valid_number__(self.emails)
        if i == "":  # default email (if exists).
            return self.emails[1] if len(self.emails) > 1 else ""
        elif i == "*":  # other.
            # First input email and save it to OPTIONS.
            oshelf = shelve.open(OPTIONS, writeback=True)
            ok, email = Helpers().__addEntry__(self.emails, oshelf, "emails")
            oshelf.close()
            print(email, "saved to your email list.") if ok else \
                print("already have", email, "saved.")
            return email  # return email either way.
        else:
            return self.emails[i]  # select email.

    def __chooseUsername__(self):
        Helpers().__displayList__(self.usernames, "usernames")
        print("[enter] default.\n"
              "[*] other.\n"
              "[number] select.\n")
        i = Helpers().__valid_number__(self.usernames)
        if i == "":  # default username (if exists).
            return self.usernames[1] if len(self.usernames) > 1 else ""
        elif i == "*":  # other.
            # First add the username and save it to OPTIONS.
            oshelf = shelve.open(OPTIONS, writeback=True)
            ok, username = Helpers().__addEntry__(self.usernames, oshelf,
                                                  "usernames")
            oshelf.close()
            print(username, "saved to your usernames list.") if ok else \
                print("already have", username, "saved.")
            return username  # return username either way.
        else:
            return self.usernames[i]  # select username.

    def __writeP__(self, dshelf, rand=True):
        if rand:
            return self.quick()  # random.
        else:
            m = self.__enter_p_w__()  # manual.
            if m:
                return m
            else:
                dshelf.close()
                Run().main_menu()  # cancelled. back to main menu.

    def __writeNotes__(self, result):
        """ add note on new line until [enter] is pressed """
        add = input("[enter] done.\n"
                    "[note].\n")
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
            p = input("input p.a.s.s.w.o.r.d..\n")
        while p1 == "":
            p1 = input("input again to confirm.\n")
        if p == p1:
            return p  # match confirmed.
        else:
            if input("p.a.s.s.w.o.r.d.s did not match.\n"
                     "[enter] cancel.\n"
                     "[t] try again.\n") in ("t", "T"):
                return self.__enter_p_w__()  # try again.
            return None  # cancel.


class Options:
    def __init__(self):
        run = Run()
        self.emails = run.__getEmails__()
        self.usernames = run.__getUsernames__()
        self.length = run.__getLength__()
        self.lrange = run.__getRange__()
        self.punctuation = run.__getPunctuation__()

    def options_menu(self):
        oshelf = shelve.open(OPTIONS, writeback=True)  # edit OPTIONS shelf.
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
            self.email_options(oshelf)  # emails.
        elif option == "2":
            self.username_options(oshelf)  # usernames.
        elif option == "3":
            self.length_options(oshelf)  # length.
        elif option == "4":
            self.range_options(oshelf)  # range.
        elif option == "5":
            self.punctuation_options(oshelf)  # punctuation.
        elif option == "6":
            oshelf.close()
            Run().main_menu()  # main menu.
        elif option == "7":
            oshelf.close()
            print("goodbye!\n")
            exit()  # quit.
        oshelf.close()  # always close OPTIONS shelf.
        self.options_menu()  # always runOptions until [main menu] or [exit].

    def email_options(self, oshelf):
        Helpers().__displayList__(self.emails, "emails")
        option = input("[enter] back to options.\n"
                       "[a] add.\n"
                       "[d] delete.\n"
                       "[e] edit.\n"
                       "[s] set default.\n")
        if option == "":
            oshelf.close()  # escape to option menu.
            self.options_menu()
        elif option in ("a", "A"):  # add email.
            self.__addEmail__(oshelf)
        elif option in ("d", "D"):  # delete email.
            self.__delEmail__(oshelf)
        elif option in ("e", "E"):  # edit email.
            self.__editEmail__(oshelf)
        elif option in ("s", "S"):
            self.__defaultEmail__(oshelf)  # set default email.
        self.email_options(oshelf)  # loop email options until escaped.

    def username_options(self, oshelf):
        Helpers().__displayList__(self.usernames, "usernames")
        option = input("[enter] options menu.\n"
                       "[a] add.\n"
                       "[d] delete.\n"
                       "[e] edit.\n"
                       "[s] set default.\n")
        if option == "":
            oshelf.close()  # escape to option menu.
            self.options_menu()
        elif option in ("a", "A"):  # add username.
            self.__addUsername__(oshelf)
        elif option in ("d", "D"):  # delete username.
            self.__delUsername__(oshelf)
        elif option in ("e", "E"):  # edit username.
            self.__editUsername__(oshelf)
        elif option in ("s", "S"):
            self.__defaultUsername__(oshelf)  # set default username.
        self.username_options(oshelf)  # loop username options until escaped.

    def length_options(self, oshelf):
        print("\ncurrent length is", str(self.length) + " characters.")
        ln = input("[enter] options menu.\n"
                   "[length]\n")
        if ln != "":  # not [enter] ("").
            try:
                ln = int(ln)
                assert ln > 0
                self.length = ln
                oshelf["length"] = ln
                print("length set to", ln, "characters.")
            except (ValueError, AssertionError):  # bad input try again.
                print("length must be a positive integer.")
                self.length_options(oshelf)

    def range_options(self, oshelf):
        print("\nrange to randomize length. eg. range +/-5 and length 15\n"
              "randomly varies p.w. length between 10 to 20 characters.\n"
              "current range is +/- ", str(self.lrange) + " characters.\n")
        try:
            r = input("[enter] options menu.\n"
                      "set range:\n")
            if r != "":  # not [enter] ("").
                r = int(r)
                assert r >= 0
                self.lrange = r
                oshelf["lrange"] = r
                print("range set to +/-", r, "characters.")
        except (ValueError, AssertionError):  # bad input try again.
            print("range must be a non-negative integer.")
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
            i = input().lower()  # loop if bad input.
            if i in pn:
                self.punctuation = pn[i]
                oshelf["punctuation"] = self.punctuation
                print(f"punctuation set to {self.punctuation}.")

    def __addEmail__(self, oshelf):
        ok, e = Helpers().__addEntry__(self.emails, oshelf, "emails")
        Helpers().__displayList__(self.emails, "emails")
        i = input("saved.\n"
                  "[enter] email options.\n"
                  "[a] add another.\n") \
            if ok else input(f"already have '{e}' saved.\n"
                             f"[enter] email options.\n"
                             f"[t] try again.\n")
        if i.lower() in ("a", "t"):
            self.__addEmail__(oshelf)  # add another/try again.

    def __addUsername__(self, oshelf):
        ok, u = Helpers().__addEntry__(self.usernames, oshelf, "usernames")
        Helpers().__displayList__(self.usernames, "usernames")
        i = input("saved.\n"
                  "[enter] username options.\n"
                  "[a] add another.\n") \
            if ok else input(f"already have '{u}' saved.\n"
                             f"[enter] username options.\n"
                             f"[t] try again.\n")
        if i.lower() in ("a", "t"):
            self.__addUsername__(oshelf)  # add another/try again.

    def __delEmail__(self, oshelf):
        if len(self.emails) == 1:
            input("no emails to delete.\n"
                  "[enter]...\n")
            self.email_options(oshelf)  # back to email options.
        print("[enter] email options.\n"
              "[number] remove email."),
        number = Helpers().__valid_number__(self.emails)
        if number == 0:
            if input("0 is no email. cannot delete.\n"
                     "[enter] email options.\n"
                     "[t] try again.\n") in ("t", "T"):
                self.__delEmail__(oshelf)  # try again.
        elif number not in ("", "*"):
            email = self.emails[number]  # number is valid.
            if input("remove " + email + "? [y]es [n]o:").lower() in \
                    ("y", "yes"):
                temp = self.emails[:]
                temp.pop(number)
                self.emails = temp
                oshelf["emails"] = temp
                input(f"'{email}' deleted.\n"
                      f"[enter]...\n")
            else:  # abort remove.
                input("nothing deleted.\n"
                      "[enter]...\n")

    def __delUsername__(self, oshelf):
        if len(self.emails) == 1:
            input("no usernames to delete.\n"
                  "[enter]...\n")
            self.username_options(oshelf)  # back to username options.
        print("[enter] username options.\n"
              "[number] remove username."),
        number = Helpers().__valid_number__(self.usernames)
        if number == 0:
            if input("0 is for no username. cannot delete.\n"
                     "[enter] username options.\n"
                     "[t] try again.\n") \
                    in ("t", "T"):
                self.__delUsername__(oshelf)  # try again.
        elif number not in ("", "*"):
            username = self.usernames[number]  # number is valid.
            if input("remove " + username + "? [y]es [n]o:").lower() in \
                    ("y", "yes"):
                temp = self.usernames[:]
                temp.pop(number)
                self.usernames = temp
                oshelf["usernames"] = temp
                input(f"'{username}' deleted.\n"
                      f"[enter]...\n")
            else:  # abort remove.
                input("nothing deleted.\n"
                      "[enter]...\n")

    def __editEmail__(self, oshelf):
        if len(self.emails) == 1:
            input("no emails to edit.\n"
                  "[enter] email options.\n")
            self.email_options(oshelf)  # options.
        print("[enter] email options.\n"
              "[number] edit email.\n")
        if self.__editList__(self.emails, oshelf, "emails"):
            Helpers().__displayList__(self.emails, "emails")
            i = input("[enter] email options.\n"
                      "[e] edit another.\n")
        else:
            i = input("[enter] email options.\n"
                      "[t] try again.\n")
        if i.lower() in ("e", "t"):  # edit another/try again.
            self.__editEmail__(oshelf)

    def __editUsername__(self, oshelf):
        if len(self.emails) == 1:
            input("no usernames to edit.\n"
                  "[enter]...\n")
            return  # options.
        print("[enter] options menu.\n"
              "[number] edit username.\n")
        if self.__editList__(self.usernames, oshelf, "usernames"):
            Helpers().__displayList__(self.usernames, "usernames")
            i = input("[enter] username options.\n"
                      "[e] edit another.\n")
        else:
            i = input("[enter] username options.\n"
                      "[t] try again.\n")
        if i.lower() in ("e", "t"):  # edit another/try again.
            self.__editUsername__(oshelf)

    def __defaultEmail__(self, oshelf):
        if len(self.emails) == 1:
            input("add an email first.\n"
                  "[enter] go back\n")
            self.email_options(oshelf)  # back to email options.
        print("[enter] email options.\n"
              "[number] set default email.")
        number = Helpers().__valid_number__(self.emails)
        if number == 0:
            if input("0 is for no email. cannot set as default.\n"
                     "[enter] email options.\n"
                     "[t] try again.\n") \
                    in ("t", "T"):
                self.__defaultEmail__(oshelf)  # try again.
        elif number in ("", "*"):
            self.email_options(oshelf)  # back to email options.
        else:
            d = self.emails.pop(number)  # remove from list, assign to 'd'.
            temp = [self.emails[0], d] + self.emails[1:]  # put back as [1].
            self.emails = temp
            oshelf["emails"] = temp
            input(f"'{d}' saved as default.\n"
                  f"[enter]...\n")
        self.email_options(oshelf)

    def __defaultUsername__(self, oshelf):
        if len(self.usernames) == 1:
            input("add a username first.\n"
                  "[enter] go back...\n")
            self.username_options(oshelf)  # back to username options.
        print("[enter] username options.\n"
              "[number] set default username\n")
        number = Helpers().__valid_number__(self.usernames)
        if number == 0:
            if input("0 is for no username. Cannot set as default.\n"
                     "[enter] username options.\n"
                     "[t] try again.\n") \
                    in ("t", "T"):
                self.__defaultUsername__(oshelf)  # try again.
        elif number in ("", "*"):
            self.username_options(oshelf)  # back to username options.
        else:
            d = self.usernames.pop(number)  # remove from list, assign to 'd'.
            temp = [self.usernames[0], d] + self.usernames[1:]  # user[1].
            self.usernames = temp
            oshelf["usernames"] = temp
            input(f"'{d}' saved as default.\n"
                  f"[enter]...\n")

    def __editList__(self, mylist, oshelf, key):
        ind = Helpers().__valid_number__(mylist)
        if ind == "":
            if key == "emails":
                self.email_options(oshelf)
            elif key == "usernames":
                self.username_options(oshelf)
        elif ind == 0:
            print("0 is no username.")
            return False
        entry = input("email: ") if key == "emails" else input("username: ")
        if entry in mylist:
            print("already have", entry, "saved.")
            return False
        mylist[ind] = entry
        oshelf[key][ind] = entry
        Helpers().__displayList__(mylist, key)
        return True


class Helpers:
    def __valid_number__(self, mylist):
        try:
            number = input()
            if number in ("", "*"):  # if input is [enter] or <*>...
                return number  # return string (special option).
            else:
                number = int(number)  # try converting input to integer.
                assert number in range(len(mylist))  # confirm is valid index.
                return number
        except (ValueError, AssertionError):
            print("try again: ")
            return self.__valid_number__(mylist)

    @staticmethod
    def __addEntry__(mylist, oshelf, key):
        entry = ""
        if key == "emails":
            entry = input("email: ")
        elif key == "usernames":
            entry = input("username: ")
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
        data = dshelf[name]  # data is itself a dictionary object.
        if quiet:
            try:
                # sys.stdout.write(data[2])                        # p.w. only.
                print(data[2])  # p.w. only.
                # flush output here to force SIGPIPE to be triggered
                # while inside this try block.
                sys.stdout.flush()
            except BrokenPipeError:
                # Python flushes standard streams on exit;
                # redirect remaining output to devnull to avoid
                # another BrokenPipeError at shutdown.
                devnull = os.open(os.devnull, os.O_WRONLY)
                os.dup2(devnull, sys.stdout.fileno())
                sys.exit(1)  # Python exits with error code 1 on EPIPE
        else:
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(name)
            for key in range(len(data)):  # keys were defined as 0, 1, 2, 3.
                if data[key]:
                    print(data[key])  # display contents of field if any.
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


if __name__ == "__main__":
    Run().main_menu()
# end of file.
