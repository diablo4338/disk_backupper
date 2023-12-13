import os

from src.dataclasses import Disk, Partition


def print_disks(disks: list[Disk]):
    os.system('clear')
    print("----Disks----")
    for k, i in enumerate(disks):
        print(f"{k}.   {i.name}  -  {i.description}")


def print_partitions(partitions: list[Partition]):
    os.system('clear')
    print("----Partitions----")
    for k, i in enumerate(partitions):
        print(f"{k}.   {i.name}  -  {i.human_size}  -  {i.filesystem}")


def print_choosen_partition(partition: Partition):
    print(
        f"Disk\n{partition.disk.name} -- {partition.disk.description}\nPartition\n{partition.name} -- {partition.filesystem} -- {partition.human_size}")
