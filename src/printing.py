import os

from src.dataclasses import Disk, Partition
from src.enums import ActionEnum
from src.utils import is_debug

debug_message_template = '!!!!!!!!!! DEBUG MODE !!!!!!!!!!'


def print_disks(disks: list[Disk]):
    os.system('clear')
    if is_debug():
        print(debug_message_template)
    print("----Disks----")
    for k, i in enumerate(disks):
        print(f"{k}.   {i.name}  -  {i.description}")


def print_partitions(partitions: list[Partition]):
    os.system('clear')
    if is_debug():
        print(debug_message_template)
    print("----Partitions----")
    for k, i in enumerate(partitions):
        print(f"{k}.   {i.name}  -  {i.human_size}  -  {i.filesystem}")


def print_choose_action():
    if is_debug():
        print(debug_message_template)
    print(f"{ActionEnum(1).value}. Copy partition")
    print(f"{ActionEnum(2).value}. Copy partition table")
    print(f"{ActionEnum(3).value}. Copy all disk")
