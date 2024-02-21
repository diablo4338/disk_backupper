import subprocess

from src.copy_sources.base import BackupperBase
from src.copying import copying_disk_or_partition
from src.utils import is_debug


class PartitionSource(BackupperBase):
    TEMPLATE_BASH_WITH_COMPRESSED = 'dd if={partition} bs=4M | pv -s {partition_size} -N raw -c | pigz -c | pv -N compressed -s {partition_size} > {filename}'
    TEMPLATE_BASH = 'dd if={partition} bs=4M | pv -s {partition_size} -N raw -c > {filename}'
    TEMPLATE_PYTHON_WITH_COMPRESSED = 'dd if={partition} bs=4M | pigz -c > {filename}'
    TEMPLATE_PYTHON = 'dd if={partition} bs=4M'

    @property
    def get_top_message(self) -> str:
        result = []
        debug_message_template = '!!!!!!!!!! DEBUG MODE !!!!!!!!!!'
        main_template = f"""Disk
{self.source.disk.name} -- {self.source.disk.description}
Partition
{self.source.name} -- {self.source.filesystem} -- {self.source.human_size}"""
        filename_template = f"""Filename
{self.filename}"""

        if is_debug():
            result.append(debug_message_template)
        result.append(main_template)

        if self.filename:
            result.append(filename_template)
        return '\n'.join(result)

    def make_code_for_bash(self):
        if self.compression:
            command = self.TEMPLATE_BASH_WITH_COMPRESSED.format(partition_size=self.source.size, filename=self.filename,
                                                                partition=self.source.name)
        else:
            command = self.TEMPLATE_BASH.format(partition_size=self.source.size, filename=self.filename,
                                                partition=self.source.name)
        with open('backup.sh', 'w') as script:
            script.write("#!/bin/bash\n")
            script.write(f'{command}\n')
        subprocess.run(['chmod', '+x', 'backup.sh'])
        print('Done. Run ./backup.sh manually')

    def copy_by_python(self):
        copying_disk_or_partition(self.source, self.filename, self.compression)
