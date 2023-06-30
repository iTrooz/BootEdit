import os
import re
import uuid

from firmware_variables.device_path import DevicePathList, DevicePath, DevicePathType, string_to_utf16_bytes
from firmware_variables.device_path import MediaDevicePathSubtype, EndOfHardwareDevicePathSubtype

from bootedit.backend.fv_ext.load_option_path import EFI_HARD_DRIVE
from bootedit.backend.partition import Partition

def gen_file_subtype(rel_file_path: str) -> DevicePath:
    if rel_file_path[0] != '\\':
        raise ValueError("UEFI entry file path should start with '\\'")

    return DevicePath(
        path_type=DevicePathType.MEDIA_DEVICE_PATH,
        subtype=MediaDevicePathSubtype.FILE_PATH,
        data=string_to_utf16_bytes(rel_file_path)
    )

def gen_hardware_end() -> DevicePath:
    return DevicePath(
        path_type=DevicePathType.END_OF_HARDWARE_DEVICE_PATH,
        subtype=EndOfHardwareDevicePathSubtype.END_ENTIRE_DEVICE_PATH,
        data=b''
    )

def gen_hard_drive_subtype(partition: Partition) -> DevicePath:
    p_number = partition.id
    p_type = "vat"
    p_start = partition.block_start_offset
    p_size = partition.block_size
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

def gen_file_path_list(partition: Partition, rel_file_path: str) -> DevicePathList:
    device_path_list = DevicePathList()

    device_path_list.paths.append(gen_hard_drive_subtype(partition))

    device_path_list.paths.append(gen_file_subtype(rel_file_path))
    device_path_list.paths.append(gen_hardware_end())

    return device_path_list
