import time

from src.dataclasses import Partition, Disk
from src.printing import print_disks, print_partitions
from src.enums import InterfaceEnum


def choose_compression() -> bool:
    while 1:
        do_compress = input("Use compression? y/n\n")
        if do_compress == 'y':
            return True
        elif do_compress == 'n':
            return False
        else:
            print("Wrong input, try again")
            time.sleep(2)


def choose_interface() -> InterfaceEnum:
    while 1:
        process_in_python = input("Use bash or python? b/p\n")
        if process_in_python == 'p':
            return InterfaceEnum.PYTHON
        elif process_in_python == 'b':
            return InterfaceEnum.BASH
        else:
            print("Wrong input, try again")
            time.sleep(2)


def choose_disk(disks: list[Disk]) -> Disk:
    while 1:
        print_disks(disks)
        try:
            disk = input("Choose disk:\n")
            disk = int(disk)
            if disk not in range(0, len(disks)):
                print("Wrong input, try again")
                time.sleep(2)
                continue
            return disks[disk]
        except ValueError:
            print("Wrong input, try again")
            time.sleep(2)


def choose_partition(partitions: list[Partition]) -> Partition | None:
    if not partitions:
        return
    print_partitions(partitions)
    while 1:
        print_partitions(partitions)
        partition = input("Choose partition:\n")
        partition = int(partition)
        if partition not in range(0, len(partitions)):
            print("Wrong input, try again")
            time.sleep(2)
            continue
        return partitions[partition]
