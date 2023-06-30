from typing import Tuple, List, Optional
import re

import wmi

from bootedit.backend.partition.type import Disk, Partition

from .get_volume_disk_id import get_volume_disk_id
from .open_object import open_object
from .get_partition_info import get_partition_info

# Documentation in get_volume_disk_id.py

wmi_inst = wmi.WMI ()


def get_partitions() -> Tuple[List[Disk], Optional[Partition]]:
    my_disks = {}

    found_disks = { disk.index : disk for disk in wmi_inst.Win32_DiskDrive() }
    
    for volume in wmi_inst.Win32_Volume():
        
        volume_device_id = volume.deviceID[:-1]
        
        handle = open_object(volume_device_id)
        if handle == None:
            continue
        
        disk_id = get_volume_disk_id(handle)
        if disk_id == None:
            print("No disk id for volume ?")
            continue


        disk = my_disks.get(disk_id)
        if disk == None:
            found_disk = found_disks.get(disk_id)
            if not found_disk:
                print("No disk found with that disk index ?")
                continue

            disk = Disk(found_disk.Caption)
            my_disks[disk_id] = disk

        part_info = get_partition_info(handle)

        part_uuid = re.search('.*Volume{(.*)}', volume.DeviceID).group(1)

        partition = Partition(disk, id=part_info.PartitionNumber, device_name=volume.Caption, part_uuid=part_uuid, type=None,
                              blockStartOffset=part_info.StartingOffset, blockSize=part_info.PartitionLength)

        disk.partitions.append(partition)

    return list(my_disks.values()), None
