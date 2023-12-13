import os
from src.exceptions import CopyingError


def handle_term(func):
    def wrapper():
        try:
            func()
        except KeyboardInterrupt:
            print("\nExit")
            return

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
