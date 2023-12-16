import subprocess

from src.dataclasses import Partition
from src.decorators import remove_file_if_fail
from src.exceptions import CopyingError


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


def copying(partition: Partition, filename: str, use_compression: bool):
    if use_compression:
        copy_with_compression(partition, filename)
    else:
        copy_without_compression(partition, filename)
