import os
import re
import uuid

from firmware_variables.device_path import DevicePathList, DevicePath, DevicePathType, string_to_utf16_bytes
from firmware_variables.device_path import MediaDevicePathSubtype, EndOfHardwareDevicePathSubtype

from bootedit.backend.partition import Partition
from .platform import gen_hard_drive_subtype

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


def gen_file_path_list(partition: Partition, rel_file_path: str) -> DevicePathList:
    device_path_list = DevicePathList()

    device_path_list.paths.append(gen_hard_drive_subtype(partition))

    device_path_list.paths.append(gen_file_subtype(rel_file_path))
    device_path_list.paths.append(gen_hardware_end())

    return device_path_list
