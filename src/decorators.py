import os
from src.exceptions import CopyingError, ParsingError


def handle_term(func):
    def wrapper():
        try:
            return func()
        except KeyboardInterrupt:
            print("\nExit")

    return wrapper


def remove_file_if_fail(func):
    def wrapper(partition, filename):
        try:
            func(partition, filename)
        except (CopyingError, KeyboardInterrupt) as error:
            os.remove(filename)
            if isinstance(error, KeyboardInterrupt):
                raise error

    return wrapper


def handle_parsing_error(func):
    def wrapper():
        try:
            return func()
        except ParsingError as error:
            print("Make sure what you using sudo or you are root. Error when parsing fdisk, exit...")

    return wrapper
