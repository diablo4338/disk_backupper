import os
import time

from src.dataclasses import Partition, Disk
from src.parsing import find_disks, find_partitions
from src.exceptions import ParsingError
from src.choosing import choose_disk, choose_partition
from src.printing import print_choose_action
from src.enums import ActionEnum


def select_disk() -> Disk:
    disks = find_disks()
    if not disks:
        raise ParsingError
    return choose_disk(disks)


def select_partition(disk: Disk) -> Partition:
    partitions = find_partitions(disk)
    if not partitions:
        raise ParsingError
    return choose_partition(partitions)


def select_action() -> ActionEnum:
    while 1:
        try:
            os.system('clear')
            print_choose_action()
            choose = input("\nChoose action:\n")
            choose = int(choose)
            return ActionEnum(choose)
        except ValueError:
            print("Wrong input, try again\n")
            time.sleep(2)
            continue
