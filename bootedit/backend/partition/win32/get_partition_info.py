from typing import Optional

import ctypes
from ctypes import wintypes
kernel32 = ctypes.cdll.kernel32

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


def get_partition_info(handle) -> Optional[object]:

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
