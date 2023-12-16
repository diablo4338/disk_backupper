import subprocess

from src.dataclasses import Partition

TEMPLATE_BASH_WITH_COMPRESSED = 'dd if={partition} bs=4M | pv -s {partition_size} -N raw -c | pigz -c | pv -N compressed -s {partition_size} > {filename}'
TEMPLATE_BASH = 'dd if={partition} bs=4M | pv -s {partition_size} -N raw -c > {filename}'
TEMPLATE_PYTHON_WITH_COMPRESSED = 'dd if={partition} bs=4M | pigz -c > {filename}'
TEMPLATE_PYTHON = 'dd if={partition} bs=4M'


def call_fdisk():
    res = subprocess.Popen(('fdisk', '-l'), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    responce, error = res.communicate()
    return responce.decode()


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
