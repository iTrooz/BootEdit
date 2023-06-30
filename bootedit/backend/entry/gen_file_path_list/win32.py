import os
import uuid
from typing import Optional

import ctypes
from ctypes import wintypes
kernel32 = ctypes.cdll.kernel32

from firmware_variables.device_path import MediaDevicePathSubtype, DevicePathType, DevicePath


from bootedit.backend.partition.type import Partition
from bootedit.backend.partition.win32.open_object import open_object
from bootedit.backend.fv_ext.load_option_path import EFI_HARD_DRIVE

def gen_hard_drive_subtype(partition: Partition) -> DevicePath:
    "Untested"
    
    p_number = partition.id
    p_type = "vat"
    p_start = partition.blockStartOffset
    p_size = partition.blockSize
    p_sig = uuid.UUID(hex=partition.part_uuid)
    p_sig_1 = int.from_bytes(p_sig.bytes_le[0:8], 'little')
    p_sig_2 = int.from_bytes(p_sig.bytes_le[8:], 'little')
    p_format = 0x02 # No idea
    p_type = 0x02 # No idea

    data = EFI_HARD_DRIVE.pack(p_number, p_start, p_size, p_sig_1, p_sig_2, p_format, p_type)
    
    return DevicePath(
        path_type=DevicePathType.MEDIA_DEVICE_PATH,
        subtype=MediaDevicePathSubtype.HARD_DRIVE,
        data=data
    )
