import os
import time
import typing

from src.dataclasses import Partition, Disk
from src.parsing import find_disks, find_partitions

from src.printing import print_choosen_partition, print_disks, print_partitions


def chhose_compression(partition: Partition, filename: str) -> bool:
    while 1:
        os.system('clear')
        print_choosen_partition(partition)
        print(f"Filename\n{filename}\n")
        do_compress = input("Use compression? y/n\n")
        if do_compress == 'y':
            return True
        elif do_compress == 'n':
            return False
        else:
            print("Wrong input, try again\n")
            time.sleep(2)


def choose_interface(partition: Partition, filename: str) -> bool:
    while 1:
        os.system('clear')
        print_choosen_partition(partition)
        print(f"Filename\n{filename}\n")
        process_in_python = input("Use bash or python? b/p\n")
        if process_in_python == 'p':
            return True
        elif process_in_python == 'b':
            return False
        else:
            print("Wrong input, try again\n")
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


def choose_partition(partitions: list[Partition]) -> typing.Optional[Partition]:
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


def choose_source() -> typing.Optional[Partition]:
    disks = find_disks()
    if not disks:
        return
    disk = choose_disk(disks)
    partitions = find_partitions(disk)
    partition = choose_partition(partitions)
    if not partition:
        print("Not any disks find")
        return
    while 1:
        os.system('clear')
        print_choosen_partition(partition)
        choose = input("\nIt is correct? y/n\n")
        if choose == 'y':
            break
        elif choose == 'n':
            print("Not any disks find")
            return
        else:
            print("Wrong input, try again\n")
            time.sleep(2)
    return partition
