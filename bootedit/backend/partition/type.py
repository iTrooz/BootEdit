from typing import List


class Disk:
    def __init__(self, name: str) -> None:
        self.name = name
        self.partitions: List[Partition] = []

    def __repr__(self) -> str:
        return "Disk(name={}, partitions={})".format(self.name, self.partitions)

class Partition:
    def __init__(self, disk: Disk, id: int, device_name: str, part_uuid: str, type: str, blockStartOffset: int, blockSize: int) -> None:
        self.disk = disk
        self.id = id
        self.device_name = device_name
        self.part_uuid = part_uuid
        self.type = type

        self.blockStartOffset = blockStartOffset
        self.blockSize = blockSize

    def __repr__(self) -> str:
        return "Partition(disk=Disk(device_name={}, ...), id={}, device_name={}, part_uuid={}, type={}, blockStartOffset={}, blockSize={})".format(
            self.disk.name, self.id, self.device_name, self.part_uuid, self.type, self.blockStartOffset, self.blockSize)
