#!/usr/bin/env python3

import os

from src.dataclasses import Partition
from src.decorators import handle_term, handle_parsing_error
from src.copying import copying
from src.printing import print_choosen_partition
from src.choosing import choose_interface, choose_compression, choose_source
from src.utils import make_bash_script


def preparing_conditions() -> tuple[Partition, str, bool, bool]:
    partition = choose_source()
    os.system('clear')
    print_choosen_partition(partition)
    filename = input("\nInput filename for backup:\n")
    use_compression = choose_compression(partition, filename)
    if use_compression:
        filename = filename + '.gz'
    use_python = choose_interface(partition, filename)
    os.system('clear')
    print_choosen_partition(partition)
    print(f"Filename\n{filename}\n")
    print("Everything is ready. Press  Enter to start process...\n")
    input()
    return partition, filename, use_compression, use_python


@handle_term
@handle_parsing_error
def main():
    partition, filename, use_compression, use_python = preparing_conditions()
    if use_python:
        copying(partition, filename, use_compression)
        print('Done')
    else:
        make_bash_script(partition, filename, use_compression)


if __name__ == '__main__':
    main()
