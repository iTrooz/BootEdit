from typing import Optional

import ctypes
from ctypes import wintypes
kernel32 = ctypes.cdll.kernel32

from .open_object import open_object


"""
With the help of:
https://learn.microsoft.com/en-us/sysinternals/downloads/diskext
https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-ioctl_volume_get_volume_disk_extents (and others)
https://gist.github.com/Pagliacii/774ed5d3ea78a36cdb0754be6a25408d
https://mail.python.org/pipermail/python-win32/2021-February/014465.html

From what I've understood:
DiskDrive -> an actual hard drive
Volume -> a virtual partition. A disk might have multiple volumes, and a volume may be stored acros- multiple disks.
    And I have no idea why, but Microsoft chose to store the partition GUID in the Volume DeviceID (but not in DiskPartition).
"""


IOCTL_VOLUME_GET_VOLUME_DISK_EXTENTS = 5636096


class DISK_EXTENT(ctypes.Structure):
    _fields_ = [
                ("DiskNumber", wintypes.DWORD),
                ("StartingOffset", wintypes.LARGE_INTEGER),
                ("ExtentLength", wintypes.LARGE_INTEGER),
                ]

class VOLUME_DISK_EXTENTS(ctypes.Structure):
    _fields_ = [
                ("NumberOfDiskExtents", wintypes.DWORD),
                ("Extents", DISK_EXTENT*1), # Only account for one extent. If there's more, not my problem
                ]


def get_volume_disk_id(volume_id: str) -> Optional[int]:
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
        IOCTL_VOLUME_GET_VOLUME_DISK_EXTENTS, # what to do
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
    
    volume_disk_extents = VOLUME_DISK_EXTENTS.from_buffer(output_buffer)

    if volume_disk_extents.NumberOfDiskExtents != 1:
        # Since it's split across multiple disk, that thing probably isn't a partition ?
        # The UEFI probably wouldn't like it anyway
        return None
    
    return volume_disk_extents.Extents[0].DiskNumber
