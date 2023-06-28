from typing import List


class Disk:
    def __init__(self, name: str) -> None:
        self.name = name
        self.partitions: List[Partition] = []

    def __repr__(self) -> str:
        return "Disk(name={}, partitions={})".format(self.name, self.partitions)

class Partition:
    def __init__(self, disk: Disk, device_name: str, part_uuid: str, type: str) -> None:
        self.disk = disk
        self.device_name = device_name
        self.part_uuid = part_uuid
        self.type = type

    def __repr__(self) -> str:
        return "Partition(disk=Disk(device_name={}, ...), device_name={}, part_uuid={}, type={})".format(self.disk.name, self.device_name, self.part_uuid, self.type)
