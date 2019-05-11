"""validation_routines.py: Functions used to validate user input."""


def strIsInt(s):
    """Return True if 's' is an integer, False otherwise."""
    try:
        int(s)
        return True
    except ValueError:
        return False


def strLenValid(str, min, max):
    """Validate that length of 'str' is between 'min' and 'max'.

    Args:
        str (str): The string whose length is to be tested.
        min (int): The minimum acceptable string length.
        max (int): The maximum acceptable string length.

    Returns:
        bool: True if length is between min and max (inclusive),
        False otherwise.
    """
    if min <= len(str.strip()) <= max:
        return True
    else:
        return False


def strIntValid(str, min, max):
    """Validate that integer value of 'str' is between 'min' and 'max'.

    Args:
        str (str): The integer string whose value is to be tested.
        min (int): The minimum acceptable integer value.
        max (int): The maximum acceptable integer value.

    Returns:
        bool: True if integer value of str is between min and max args
        (inclusive), False otherwise.
    """
    if min <= int(str.strip()) <= max:
        return True
    else:
        return False
