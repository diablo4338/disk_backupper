from enum import IntEnum


class ActionEnum(IntEnum):
    PARTITION = 1
    PT = 2
    WHOLE_DISK = 3


class InterfaceEnum(IntEnum):
    PYTHON = 1
    BASH = 2
