from RPM.Main import OPTIONS


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
        "none": "",
    }
    lowercase = True
    uppercase = True
    numbers = True

    def __init__(self, oshelf):
        if oshelf:  # get options from shelf
            Options.emails = oshelf["emails"]
            Options.usernames = oshelf["usernames"]
            Options.length = oshelf["length"]
            Options.lrange = oshelf["lrange"]
            Options.punctuation = oshelf["punctuation"]
            Options.lowercase = oshelf["lowercase"]
            Options.uppercase = oshelf["uppercase"]
            Options.numbers = oshelf["numbers"]
            self.first_run = ""
        else:  # first run, save default options to empty shelf
            oshelf["emails"] = Options.emails
            oshelf["usernames"] = Options.usernames
            oshelf["length"] = Options.length
            oshelf["lrange"] = Options.lrange
            oshelf["punctuation"] = Options.punctuation
            oshelf["lowercase"] = Options.lowercase
            oshelf["uppercase"] = Options.uppercase
            oshelf["numbers"] = Options.numbers
            self.first_run = f"Default options saved to file:\n{OPTIONS}\n"

    def __str__(self):
        lr = f"length varies +/- {Options.lrange}" if Options.lrange else "0"
        return f"password options:\n" \
            f"{self.first_run}" \
            f"length: {Options.length} characters\n" \
            f"lrange: {lr}\n" \
            f"random characters:\n" \
            f"{' lowercase,' if Options.lowercase else ''}" \
            f"{' uppercase,' if Options.uppercase else ''}" \
            f"{' numbers,' if Options.numbers else ''}" \
            f"\n {Options.punctuation} punctuation " \
            f"{Options.punctuation_choices[Options.punctuation]}"

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
