from dataclasses import dataclass


@dataclass()
class Disk:
    description: str
    name: str


@dataclass()
class Partition:
    name: str
    human_size: str
    size: int
    filesystem: str
    disk: Disk
