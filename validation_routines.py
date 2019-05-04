# Functions used in validating user input.
def strIsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def strLenValid(str, min, max):
    if min <= len(str.strip()) <= max:
        return True
    else:
        return False


def strIntValid(str, min, max):
    if min <= int(str.strip()) <= max:
        return True
    else:
        return False
