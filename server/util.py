"""
util.py

Contains utility functions used throughout the application.
"""


def is_int(string):
    """
    Returns true if the given string is an integer, otherwise the
    function returns false.

    :param string: the string that will be checked
    :return: whether the string represents an integer
    """
    try:
        int(string)
        return True

    except ValueError:
        return False
