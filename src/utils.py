import os
import subprocess

example = '''
   Disk /dev/nvme0n1: 465,76 GiB, 500107862016 bytes, 976773168 sectors
Disk model: Samsung SSD 970 EVO Plus 500GB
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 111111-111-1111-1111-1111

Device             Start       End   Sectors   Size Type
/dev/nvme0n1p1      2048    616447    614400   300M EFI System
/dev/nvme0n1p2    616448    649215     32768    16M Microsoft reserved
/dev/nvme0n1p3    649216 191603172 190953957  91,1G Microsoft basic data
/dev/nvme0n1p4 191604736 579486496 387881761   185G Microsoft basic data
/dev/nvme0n1p5 579487744 581044223   1556480   760M Windows recovery environment
/dev/nvme0n1p6 581044224 582113279   1069056   522M Windows recovery environment
/dev/nvme0n1p7 582113280 879273983 297160704 141,7G Microsoft basic data
/dev/nvme0n1p8 879276032 974505983  95229952  45,4G Linux filesystem
/dev/nvme0n1p9 974508032 976732159   2224128   1,1G Windows recovery environment
'''


def is_debug() -> bool:
    try:
        debug = bool(os.getenv('BACKUPPER_DEBUG', False))
    except ValueError:
        debug = False
    return debug


def call_fdisk() -> str:
    if is_debug():
        return example
    res = subprocess.Popen(('fdisk', '-l'), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    response, error = res.communicate()
    return response.decode()
