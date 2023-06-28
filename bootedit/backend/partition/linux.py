# This module retrieves partitions available on this computer and their name

import os
import subprocess
from typing import Tuple, List, Optional

from bootedit.backend.fv_ext import parse_file_path_list, get_parsed_current_boot_entry
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
    

def get_partitions() -> Tuple[List[Disk], Optional[Partition]]:
    """
    Linux-only implementation
    """
    curr_entry = get_parsed_current_boot_entry()
    curr_entry_loc = parse_file_path_list(curr_entry.file_path_list)

    disks = {}
    default_partition = None

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
            disk = Disk(name=disk_name)
            disks[disk_name] = disk

        partition = Partition(disk=disk, device_name=device_name, part_uuid=part_uuid, type=part_type)
        disk.partitions.append(partition)

        if part_uuid == curr_entry_loc.sig_id:
            default_partition = partition
        
    
    return disks.values(), default_partition
