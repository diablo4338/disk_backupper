import subprocess

from src.dataclasses import Partition, Disk
from src.decorators import remove_file_if_fail
from src.exceptions import CopyingError


@remove_file_if_fail
def copy_with_compression(device: Partition | Disk, filename: str):
    with open(filename, 'wb') as backup:
        ps1 = subprocess.Popen(('dd', f'if={device.name}', 'bs=4M'), stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        ps2 = subprocess.Popen(('pigz',), stdin=ps1.stdout, stdout=backup, stderr=subprocess.PIPE)
        output, errors = ps2.communicate()
        if ps2.returncode != 0:
            print("Errors in coping process. Details:")
            print(errors.decode())
            raise CopyingError


@remove_file_if_fail
def copy_without_compression(device: Partition | Disk, filename: str):
    with open(filename, 'wb') as backup:
        result = subprocess.run(['dd', f'if={device.name}', 'bs=4M'], stdout=backup, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("Errors in coping process. Details:")
            print(result.stderr.decode())
            raise CopyingError


def copying_disk_or_partition(device: Partition | Disk, filename: str, use_compression: bool):
    if use_compression:
        copy_with_compression(device, filename)
    else:
        copy_without_compression(device, filename)


@remove_file_if_fail
def copy_partition_table(disk: Disk, filename: str):
    with open(filename, 'wb') as backup:
        result = subprocess.run(['sfdisk', '-d', disk.name], stdout=backup, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(result.stderr.decode())
            raise CopyingError
