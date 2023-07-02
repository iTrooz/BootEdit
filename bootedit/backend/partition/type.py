from typing import List


class Disk:
    def __init__(self, id: int, friendly_name: str) -> None:
        self.id = id
        self.friendly_name = friendly_name
        self.partitions: List[Partition] = []

    def __repr__(self) -> str:
        return "Disk(id={}, friendly_name={}, partitions={})".format(self.id, self.friendly_name, self.partitions)

class Partition:
    def __init__(self, disk: Disk, id: int, device_name: str, part_uuid: str, type: str, block_start_offset: int, block_size: int) -> None:
        self.disk = disk
        self.id = id
        self.device_name = device_name
        self.part_uuid = part_uuid
        self.type = type

        self.block_start_offset = block_start_offset
        self.block_size = block_size

    def __repr__(self) -> str:
        return "Partition(disk=Disk(friendly_name={}, ...), id={}, device_name={}, part_uuid={}, type={}, block_start_offset={}, block_size={})".format(
            self.disk.friendly_name, self.id, self.device_name, self.part_uuid, self.type, self.block_start_offset, self.block_size)
