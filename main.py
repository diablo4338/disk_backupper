#!/usr/bin/env python3

import subprocess
import re
from dataclasses import dataclass
import os
import time
import typing


class CopyingError(Exception):
    pass


@dataclass()
class Disk:
    description: str
    name: str


@dataclass()
class Partition:
    name: str
    human_size: str
    size: int
    filesystem: str
    disk: Disk


TEMPLATE_BASH_WITH_COMPRESSED = 'dd if={partition} bs=4M | pv -s {partition_size} -N raw -c | pigz -c | pv -N compressed -s {partition_size} > {filename}.tgz'
TEMPLATE_BASH = 'dd if={partition} bs=4M | pv -s {partition_size} -N raw -c > {filename}'
TEMPLATE_PYTHON_WITH_COMPRESSED = 'dd if={partition} bs=4M | pigz -c > {filename}.tgz'
TEMPLATE_PYTHON = 'dd if={partition} bs=4M'


def call_fdisk():
    res = subprocess.Popen(('fdisk', '-l'), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    responce, error = res.communicate()
    return responce.decode()


def find_disks():
    pattern = re.compile(r'Disk (\/dev\/(?!loop\d+)\w+): \d+,\d+ \w+, \d+ bytes, \d+ sectors\nDisk model: (.+)\n')
    result = re.findall(pattern, call_fdisk())
    return [Disk(name=i[0], description=i[1]) for i in result]


def print_disks(disks: list[Disk]):
    os.system('clear')
    print("----Disks----")
    for k, i in enumerate(disks):
        print(f"{k}.   {i.name}  -  {i.description}")


def find_partitions(disk: Disk) -> list[Partition]:
    pattern = re.compile(rf'({disk.name}\w+)\s+\d+\s+\d+\s+(\d+)\s+([\d\,GM]+)\s+(.+)\n')
    result = re.findall(pattern, call_fdisk())
    return [Partition(name=i[0],
                      human_size=i[2],
                      size=int(i[1]) * 512,
                      filesystem=i[3],
                      disk=disk) for i in result]


def print_partitions(partitions: list[Partition]):
    os.system('clear')
    print("----Partitions----")
    for k, i in enumerate(partitions):
        print(f"{k}.   {i.name}  -  {i.human_size}  -  {i.filesystem}")


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


def print_choosen_partition(partition: Partition):
    print(
        f"Disk\n{partition.disk.name} -- {partition.disk.description}\nPartition\n{partition.name} -- {partition.filesystem} -- {partition.human_size}")


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


def preparing_conditions() -> tuple[Partition, str, bool, bool]:
    partition = choose_source()
    os.system('clear')
    print_choosen_partition(partition)
    filename = input("\nInput filename for backup:\n")
    use_compression = chhose_compression(partition, filename)
    if use_compression:
        filename = filename + '.gz'
    use_python = choose_interface(partition, filename)
    os.system('clear')
    print_choosen_partition(partition)
    print(f"Filename\n{filename}\n")
    print("Everything is ready. Press  Enter to start process...\n")
    input()
    return partition, filename, use_compression, use_python


@remove_file_if_fail
def copy_with_compression(partition: Partition, filename: str):
    with open(filename, 'wb') as backup:
        ps1 = subprocess.Popen(('dd', f'if={partition.name}', 'bs=4M'), stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL)
        ps2 = subprocess.Popen(('pigz',), stdin=ps1.stdout, stdout=backup)
        output, errors = ps2.communicate()
        if ps2.returncode != 0:
            print(errors.decode())
            raise CopyingError


@remove_file_if_fail
def copy_without_compression(partition: Partition, filename: str):
    with open(filename, 'wb') as backup:
        result = subprocess.run(['dd', f'if={partition.name}', 'bs=4M'], stdout=backup, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(result.stderr.decode())
            raise CopyingError
        print('Done')


def copying(partition: Partition, filename: str, use_compression: bool):
    if use_compression:
        copy_with_compression(partition, filename)
    else:
        copy_without_compression(partition, filename)


def make_bash_script(partition: Partition, filename: str, use_compression: bool):
    if use_compression:
        command = TEMPLATE_BASH_WITH_COMPRESSED.format(partition_size=partition.size, filename=filename,
                                                       partition=partition.name)
    else:
        command = TEMPLATE_BASH.format(partition_size=partition.size, filename=filename, partition=partition.name)
    with open('backup.sh', 'w') as script:
        script.write("#!/bin/bash\n")
        script.write(f'{command}\n')
    subprocess.run(['chmod', '+x', 'backup.sh'])
    print('Done. Run ./backup.sh manually')


@handle_term
def main():
    partition, filename, use_compression, use_python = preparing_conditions()
    if use_python:
        copying(partition, filename, use_compression)
    else:
        make_bash_script(partition, filename, use_compression)


if __name__ == '__main__':
    main()
