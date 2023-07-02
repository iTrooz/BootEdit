# This module retrieves partitions available on this computer and their name

import os
import subprocess
from typing import Tuple, List, Optional
import re

from bootedit.backend.partition.type import Disk, Partition

def trim_number(input_str: str):
    """
    Utility function to trim the number at the end of a string
    Used for trimming numbers in Linux partition names (e.g. /dev/sda1 -> /dev/sda)
    """
    for i in reversed(range(len(input_str))):
        if not input_str[i].isdigit():
            return input_str[:i+1]
    raise RuntimeError(f"string {input_str} has only numbers")

def lsblk() -> dict:
    parts_parents = {}

    output = subprocess.check_output(['lsblk', '-o', 'pkname,name,type', '--raw'])

    for line in output.split(b"\n"):
        line = line.decode()
        if not line:
            continue

        disk_name, part_name, type = line.split(" ")
        if type == "part":
            parts_parents[part_name] = disk_name
    
    return parts_parents

def blkid() -> List[dict]:
    parts_data = {}
    partitions = []

    output = subprocess.check_output(['blkid', '-o', 'export'])

    for line in output.split(b"\n"):
        line = line.decode()
        if not line:
            partitions.append(parts_data)
            parts_data = {}
            continue
        i = line.find("=")
        key, value = line[:i], line[i+1:]

        parts_data[key] = value
    
    return partitions

def get_end_number(s: str) -> int:
    "get number at the end of string"
    return int(re.match('.*?([0-9]+)$', s).group(1))

def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()

def get_partition_info(disk_path: str, partition_path: str) -> Tuple[int, int, int]:
    """
    Returns (id, start, size)
    """
    p_number = get_end_number(partition_path)
    sys_part_dir = "/sys/block/{}/{}".format(os.path.basename(disk_path), os.path.basename(partition_path))
    p_start = int(read_file(sys_part_dir + "/start"))
    p_size = int(read_file(sys_part_dir + "/size"))

    return (p_number, p_size, p_start)
    

def get_partitions() -> List[Disk]:
    """
    Linux-only implementation
    """
    
    disks = {}

    parts_parents = lsblk()

    for part_data in sorted(blkid(), key= lambda x: x["DEVNAME"]):
        device_name = part_data["DEVNAME"]
        part_uuid = part_data.get("PARTUUID")
        part_type = part_data.get("TYPE")
        if not part_uuid:
            # not a partition
            continue
        if not part_type:
            # we will not be able to read this partition
            continue

        # remove the '/dev/' part
        part_name = device_name[5:]
        disk_name = parts_parents[part_name]

        disk = disks.get(disk_name)
        if not disk:
            disk = Disk(friendly_name=disk_name)
            disks[disk_name] = disk

        partition_info = get_partition_info(disk_path=disk.friendly_name, partition_path=device_name)

        partition = Partition(disk=disk, id=partition_info[0], device_name=device_name, part_uuid=part_uuid,
                              type=part_type, block_start_offset=partition_info[1], block_size=partition_info[2])
        disk.partitions.append(partition)
    
    return list(disks.values())
