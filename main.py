#!/usr/bin/env python3

from src.decorators import handle_term, handle_parsing_error
from src.selecting import select_action

from src.copy_sources.base import BackupperBase
from src.copy_sources.partition import PartitionSource
from src.copy_sources.disk import DiskSource
from src.copy_sources.pt import PartitionTableSource
from src.enums import ActionEnum
from src.selecting import select_disk, select_partition
from src.exceptions import NotDefineSource


def get_source_class(action: ActionEnum) -> BackupperBase:
    if action.PARTITION == action:
        disk = select_disk()
        source = select_partition(disk)
        return PartitionSource(source)
    elif action.PT == action:
        source = select_disk()
        return PartitionTableSource(source)
    elif action.WHOLE_DISK == action:
        source = select_disk()
        return DiskSource(source)
    else:
        raise NotDefineSource


@handle_term
@handle_parsing_error
def main():
    action = select_action()
    source_class = get_source_class(action)
    source_class.do_it()
    print('Done')


if __name__ == '__main__':
    main()
