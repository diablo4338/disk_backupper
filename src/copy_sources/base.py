import time
import os

from src.dataclasses import Disk, Partition
from src.exceptions import UserTerminate
from src.choosing import choose_interface, choose_compression
from src.enums import InterfaceEnum


class BackupperBase:
    source: Disk | Partition = None
    _filename: str = None
    compression: bool = False
    quick: bool = False  # Generate filename from device name, use compression, use python
    simple: bool = False  # Generate filename from device name, not use compression, use python
    interface: InterfaceEnum = InterfaceEnum.PYTHON
    top_message: str = ''

    def __init__(self, source: Disk | Partition):
        self.source = source

    def check_user_choice(self):
        while 1:
            os.system('clear')
            print(self.get_top_message)
            choose = input(
                """
Is it correct?
y - continue
q - use quick mode
s - use quick mode without compression
n - exit
""")
            if choose == 'y':
                break
            elif choose == 'n':
                print("Okay, exit...")
                raise UserTerminate
            elif choose == 'q':
                self.quick = True
                break
            elif choose == 's':
                self.quick = True
                self.simple = True
                break
            else:
                print("Wrong input, try again\n")
                time.sleep(2)

    @property
    def get_top_message(self) -> str:
        raise NotImplemented

    @property
    def filename(self) -> str:
        if not self._filename:
            return ''
        if self.compression:
            return self._filename + '.gz'
        else:
            return self._filename

    @staticmethod
    def make_code_for_bash():
        raise NotImplemented

    @staticmethod
    def copy_by_python():
        raise NotImplemented

    def _autogenerate_filename(self):
        # TODO move this split code to dataclass attribute
        return self.source.name.split('/')[-1]

    def select_filename(self, silent: bool):
        if silent:
            self._filename = self._autogenerate_filename()
            return
        while 1:
            os.system('clear')
            print(self.get_top_message)
            filename = input("\nInput filename for backup:\n")
            if not filename:
                print("Filename can't be empty? try again")
                time.sleep(2)
                continue
            self._filename = filename
            break

    def select_compression(self):
        os.system('clear')
        print(self.get_top_message)
        self.compression = choose_compression()

    def select_worker(self):
        os.system('clear')
        print(self.get_top_message)
        self.interface = choose_interface()

    def do_it(self):
        try:
            self.check_user_choice()
        except UserTerminate:
            return
        self.select_filename(self.quick)
        if self.quick:
            if self.simple:
                self.compression = False
            else:
                self.compression = True
            self.interface = InterfaceEnum.PYTHON
            self.copy_by_python()
            return
        self.select_compression()
        self.select_worker()
        if self.interface == InterfaceEnum.PYTHON:
            self.copy_by_python()
        if self.interface == InterfaceEnum.BASH:
            self.make_code_for_bash()
