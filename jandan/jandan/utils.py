import re


def retain_number(string):
    return re.sub('[^0-9]', '', string)
