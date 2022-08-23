import os


def username_from_email(email):
    return email.split("@")[0]


def get_extension_file(filename):
    return os.path.splitext(filename)[-1]
