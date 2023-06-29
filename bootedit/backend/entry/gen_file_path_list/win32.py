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

IOCTL_DISK_GET_PARTITION_INFO_EX = 458824

class GUID(ctypes.Structure):
    "WHY"
    _fields_ = [
            ("Data1", wintypes.LONG),
            ("Data2", wintypes.SHORT),
            ("Data3", wintypes.SHORT),
            ("Data4", wintypes.CHAR * 8),
            ]


class PARTITION_INFORMATION_GPT(ctypes.Structure):
    _fields_ = [
            ("PartitionType", GUID),
            ("PartitionId", GUID),
            ("Attributes", wintypes.ULARGE_INTEGER),
            ("Name", wintypes.WCHAR * 36),
            ]

class PARTITION_INFORMATION_EX(ctypes.Structure):
    _fields_ = [
            ("PartitionStyle", wintypes.DWORD),
            ("StartingOffset", wintypes.LARGE_INTEGER),
            ("PartitionLength", wintypes.LARGE_INTEGER),
            ("PartitionNumber", wintypes.ULONG),
            ("RewritePartition", wintypes.BOOLEAN),
            ("IsServicePartition", wintypes.BOOLEAN),
            ("Gpt", PARTITION_INFORMATION_GPT),
            ]


def get_partition_info(volume_id: str) -> Optional[int]:
    """
    Returns None if the volume path if invalid
    """

    handle = open_object(volume_id)
    if handle == None:
        return None

    output_buffer_size = 8192
    output_buffer = ctypes.create_unicode_buffer(output_buffer_size)

    written_bytes = ctypes.c_int32()
    ret = kernel32.DeviceIoControl(
        handle, # file handle
        IOCTL_DISK_GET_PARTITION_INFO_EX, # what to do
        None,
        0,
        ctypes.byref(output_buffer), # output buffer
        output_buffer_size, # output buffer size
        ctypes.byref(written_bytes), # OUT - bytes written to the output buffer,
        None,
    )
    
    if ret == 0:
        # No idea why it failed
        raise RuntimeError("Call to DeviceIoControl() failed")
    
    partition_information_ex = PARTITION_INFORMATION_EX.from_buffer(output_buffer)

    assert partition_information_ex.PartitionStyle == 1 # ensure GPT style
    
    return partition_information_ex


def gen_hard_drive_subtype(partition: Partition) -> DevicePath:
    "Untested"

    partition_info = get_partition_info(partition.device_name)
    
    p_number = partition.disk.id
    p_type = "vat"
    p_start = partition_info.StartingOffset
    p_size = partition_info.PartitionLength
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
