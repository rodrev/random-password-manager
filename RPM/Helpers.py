import sys
import os


class Helpers:
    def valid_number(self, mylist):
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
            return self.valid_number(mylist)

    @staticmethod
    def add_entry(mylist, key, oshelf):
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
    def display_list(mylist, key):
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
    def display_data(data, name, quiet=False):
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

    @staticmethod
    def column_print(mylist):
        n = max(map(len, mylist))  # length of longest word in mylist
        c = 80 // (n + 4)  # number of columns
        r = len(mylist) // c + 1  # number of rows
        for row in [mylist[i::r] for i in range(r)]:
            print("".join(f"{w:{n + 4}}" for w in row))
