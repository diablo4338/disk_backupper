from src.copy_sources.base import BackupperBase
from src.copying import copy_partition_table
from src.exceptions import UserTerminate
from src.utils import is_debug


class PartitionTableSource(BackupperBase):

    @property
    def get_top_message(self) -> str:
        result = []
        debug_message_template = '!!!!!!!!!! DEBUG MODE !!!!!!!!!!'
        main_template = f"""Disk
{self.source.name} -- {self.source.description}"""
        filename_template = f"""Filename
{self.filename}"""

        if is_debug():
            result.append(debug_message_template)
        result.append(main_template)

        if self.filename:
            result.append(filename_template)
        return '\n'.join(result)

    def make_code_for_bash(self):
        pass

    def copy_by_python(self):
        copy_partition_table(self.source, self.filename)

    def do_it(self):
        try:
            self.check_user_choice()
        except UserTerminate:
            return
        self.select_filename(self.quick)
        self.copy_by_python()
