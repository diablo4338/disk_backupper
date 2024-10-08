import re

from src.utils import call_fdisk
from src.dataclasses import Disk, Partition


def find_disks() -> list[Disk]:
    pattern = re.compile(r'Disk (/dev/(?!loop\d+)\w+): (.+), \d+ \w+, (\d+) sectors\nDisk model: (.+)\n')
    result = re.findall(pattern, call_fdisk())
    return [Disk(name=i[0], size=i[1], description=i[2]) for i in result]


def find_partitions(disk: Disk) -> list[Partition]:
    pattern = re.compile(rf'({disk.name}\w+)\s+\d+\s+\d+\s+(\d+)\s+([\d,.GM]+)\s+(.+)\n')
    result = re.findall(pattern, call_fdisk())
    return [Partition(name=i[0],
                      human_size=i[2],
                      size=str(int(i[1]) * 512),
                      filesystem=i[3],
                      disk=disk) for i in result]
