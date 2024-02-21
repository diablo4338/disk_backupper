from src.copy_sources.partition import PartitionSource
from src.utils import is_debug


class DiskSource(PartitionSource):
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
