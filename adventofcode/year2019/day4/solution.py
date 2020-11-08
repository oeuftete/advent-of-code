class DepotPassword(object):
    def __init__(self, pw):
        self.pw = str(pw)

    @property
    def digits(self):
        return [int(d) for d in self.pw]

    def is_valid(self, part_b_rules=False):
        """Returns true if a password is valid."""
        #  Maybe also to consider: 6 characters, all digits
        return self.has_double(part_b_rules) and self.does_not_decrease()

    def has_double(self, part_b_rules=False):
        """Returns true if a password has a "double"."""
        pw = self.pw

        for i in range(len(pw) - 1):
            if pw[i] == pw[i + 1]:  # it's a double
                if part_b_rules:
                    if i > 0 and pw[i - 1] == pw[i]:
                        continue
                    if i < (len(pw) - 2) and pw[i + 2] == pw[i]:
                        continue
                return True

        return False

    def does_not_decrease(self):
        """Returns true if the password's digits do not decrease."""
        pw = self.pw
        for i in range(len(pw) - 1):
            if int(pw[i]) > int(pw[i + 1]):
                return False

        return True


def count_valid_passwords(low, high, part_b_rules=False):
    return len(
        list(
            filter(
                lambda p: DepotPassword(p).is_valid(part_b_rules), range(low, high + 1)
            )
        )
    )
