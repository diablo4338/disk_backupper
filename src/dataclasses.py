from dataclasses import dataclass


@dataclass()
class Disk:
    description: str
    name: str
    size: str
    human_size: str


@dataclass()
class Partition:
    name: str
    human_size: str
    size: str
    filesystem: str
    disk: Disk
