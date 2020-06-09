import re


def validate_username(uname):
    return uname != None and len(uname) > 2


def validate_password(uname):
    return uname != None and len(uname) > 2


def validate_input(input):
    return input != None and len(input) > 0 and len(input) < 1000


def sanitize_json(string):
    string = re.sub(r"\"", "\\\"", string)
    string = re.sub(r"<", "&lt;", string)
    string = re.sub(r">", "&gt;", string)

    return string
