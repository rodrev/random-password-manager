from random import randint, choice
from RPM.MainMenu import MainMenu
from RPM.Main import Main, SAVE
from RPM.Helpers import Helpers
from RPM.Options import Options


class Data:
    def __init__(self):
        self.random = False

    def change_all(self):
        if not Main.dshelf:
            input("No data yet\n"
                  "[enter] Main Menu\n")
            MainMenu(Main.options)
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
            MainMenu(Main.options)
        self.__display_entries__()  # print names
        i = input("[enter] Main Menu\n"
                  "[name] Entry to delete\n")
        if not i:
            MainMenu(Main.options)
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
            MainMenu(Main.options)
        if name is None:  # also accept name as argument
            self.__display_entries__()
            name = input("[enter] Main Menu\n"
                         "[name] Entry to edit\n")
            if not name:
                MainMenu(Main.options)
        try:
            data = Main.dshelf[name]
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            Helpers.display_data(data, name)
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
            self.edit_entry() if i == "t" else MainMenu(Main.options)

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
            MainMenu(Main.options)
        self.__display_entries__()  # print names
        name = input("[enter] Main Menu\n"
                     "[name] Get entry\n")
        if not name:
            MainMenu(Main.options)
        try:
            data = Main.dshelf[name]
        except KeyError:
            print(f"{name} not found\n")
        else:
            Helpers.display_data(data, name)
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
            Helpers.display_data(data, name, quiet)

    def new_entry(self):
        """ open or create DATA shelf and write data to it """
        name = input("[enter] Main Menu\n"
                     "[name] Entry\n")
        if not name:
            MainMenu(Main.options)
        if name in Main.dshelf:  # entry with 'name' already exists
            data = Main.dshelf[name]
            if data:
                print(f"\n {name} already exists")
                Helpers().display_data(data, name)
                i = "dummy"
                while i not in ("", "t", "e", "r"):
                    i = input(f"[enter] Main Menu\n"
                              f"[t] Try another name\n"
                              f"[e] Edit {name}\n"
                              f"[r] Replace {name}\n")
                if not i:
                    MainMenu(Main.options)
                elif i == "t":
                    self.new_entry()  # Try again
                elif i == "e":
                    self.edit_entry(name)  # edit
        # Write new entry
        # (name does not exist, is blank entry, or [Replace] selected)
        data = dict([(str(key), value) for key, value
                     in enumerate(self.__input_data__())])
        Main.dshelf[name] = data
        Helpers().display_data(data, name)
        print("Saved")

    def new_random_entry(self):
        self.random = True
        self.new_entry()

    def print_or_save_all(self):
        alphabetical = sorted(Main.dshelf)  # sorted list of names
        if not Main.dshelf:
            input("No data yet\n"
                  "[enter] Main Menu\n")
            MainMenu(Main.options)
        for name in alphabetical:
            data = Main.dshelf[name]  # data is itself a dictionary object
            Helpers().display_data(data, name)
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
        Helpers().display_list(Options.emails, "emails")
        print("[enter] Default\n"
              "[*] Other\n"
              "[number] Select\n"),
        i = Helpers().valid_number(Options.emails)
        if not i:  # default email (if exists)
            return Options.emails[1] if len(Options.emails) > 1 else ""
        elif i == "*":  # other
            # First input email and save it to OPTIONS
            ok, email = Helpers().add_entry(
                Options.emails, Main.oshelf, "emails")
            print(f"{email} saved to your email list") if ok else \
                print(f"Already have {email} saved")
            return email  # return email either way
        else:
            return Options.emails[i]  # select email

    @staticmethod
    def __choose_username__():
        Helpers().display_list(Options.usernames, "usernames")
        print("[enter] Default\n"
              "[*] Other\n"
              "[number] Select\n")
        i = Helpers().valid_number(Options.usernames)
        if not i:  # default username (if exists)
            return Options.usernames[1] if len(Options.usernames) > 1 else ""
        elif i == "*":  # other
            # First add the username and save it to OPTIONS
            ok, username = Helpers().add_entry(
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
        Helpers.column_print(sorted(Main.dshelf))
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
                MainMenu(Main.options)
