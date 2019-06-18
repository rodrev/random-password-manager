from RPM.Helpers import Helpers
from RPM.MainMenu import MainMenu
from RPM.Options import Options
from RPM.Main import Main


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
        Helpers().display_list(Options.emails, "emails")
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
        Helpers().display_list(Options.usernames, "usernames")
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
        ok, e = Helpers().add_entry(Options.emails, Main.oshelf, "emails")
        Helpers().display_list(Options.emails, "emails")
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
        ok, u = Helpers().add_entry(
            Options.usernames, Main.oshelf, "usernames")
        Helpers().display_list(Options.usernames, "usernames")
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
        number = Helpers().valid_number(Options.emails)
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
        number = Helpers().valid_number(Options.usernames)
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
        number = Helpers().valid_number(Options.emails)
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
        number = Helpers().valid_number(Options.usernames)
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
            Helpers().display_list(Options.emails, "emails")
            i = input("[enter] Email options\n"
                      "[e] Edit another\n")
        else:
            i = input("[enter] Email options\n"
                      "[t] Try again\n")
        if i in ("e", "t"):  # edit another/Try again
            self.__edit_email__()

    def __edit_list__(self, mylist, key):
        ind = Helpers().valid_number(mylist)
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
        Helpers().display_list(mylist, key)
        return True

    def __edit_username__(self):
        if len(Options.emails) == 1:
            input("No usernames to edit\n"
                  "[enter]...\n")
            return  # options
        print("[enter] Options menu\n"
              "[number] Edit username\n")
        if self.__edit_list__(Options.usernames, "usernames"):
            Helpers().display_list(Options.usernames, "usernames")
            i = input("[enter] Username options\n"
                      "[e] Edit another\n")
        else:
            i = input("[enter] Username options\n"
                      "[t] Try again\n")
        if i in ("e", "t"):  # edit another/Try again
            self.__edit_username__()
