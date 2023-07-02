from typing import List, Optional
import string
import tempfile
import os
import subprocess

import ctypes
kernel32 = ctypes.cdll.kernel32
import wmi

from bootedit.backend.partition.type import Partition

wmi_inst = wmi.WMI()

def diskpart(commands: List) -> str:
    """
    Execute the given commands in diskpart, and returns the output
    """

    tfile = tempfile.NamedTemporaryFile(delete=False)

    for command in commands:
        tfile.write(command.encode())
        tfile.write(b"\n")

    tfile.flush()
    tfile.close()
    

    output = subprocess.check_output(["diskpart", "/s", tfile.name])

    os.remove(tfile.name)

    return output.decode()

def get_allocated_letters() -> List[str]:
    """
    Get letters that are not available to be alloated to a new partition/volume/whatever
    Warning: sometimes, letters are allocated, but users can't access them. (Like, the letter is not available in the explorer)
    """

    output_buffer_size = 255
    output_buffer = ctypes.create_string_buffer(output_buffer_size)

    ret = kernel32.GetLogicalDriveStringsA(output_buffer_size, ctypes.byref(output_buffer))
    if not ret:
        raise RuntimeError(f"GetLogicalDriveStrings() failed: {kernel32.GetLastError()}")
    
    # Return value is a repetition of the 4-bytes pattern `X:\<NULL BYTE>`, followed by a (second) <NULL BYTE> to end it.
    letters_1 = []
    offset = 0
    while output_buffer.raw[offset] != 0:
        letter_1 = chr(output_buffer.raw[offset])
        letters_1.append(letter_1)
        offset+=4

    return letters_1

def get_free_letter() -> str:
    """Returns a letter in the format `C:/`"""

    used_letters_1 = get_allocated_letters()
    for letter_1 in reversed(string.ascii_uppercase):
        if not letter_1 in used_letters_1:
            assert len(letter_1) == 1
            return f"{letter_1}:\\"
    
    raise RuntimeError("All letters are used ?")

def volume_name_to_device_path(volume_name: str) -> None:
    """
    Takes a device path in the format `\Device\HarddiskVolume1` and returns a volume path in the formt 
    """

    output_buffer_size = 255
    output_buffer = ctypes.create_unicode_buffer(output_buffer_size)

    volume_name_subtr = volume_name[4:-1]
    ret = kernel32.QueryDosDeviceW(volume_name_subtr, ctypes.byref(output_buffer), output_buffer_size)
    if not ret:
        raise RuntimeError(f"Call to QueryDosDeviceA() failed: {kernel32.GetLastError()}")

    return output_buffer.value

def drive_letter_to_device_path(letter_3: str) -> None:
    """
    Takes a letter in the format `C:\` and returns a device path in the format `\Device\HarddiskVolume1`
    """

    assert len(letter_3) == 3
    letter_2 = letter_3[0:2]
    
    output_buffer_size = 255
    output_buffer = ctypes.create_unicode_buffer(output_buffer_size)

    ret = kernel32.QueryDosDeviceW(letter_2, ctypes.byref(output_buffer), output_buffer_size)
    if not ret:
        raise RuntimeError(f"Call to QueryDosDeviceA() failed: {kernel32.GetLastError()}")

    return output_buffer.value

def actually_mount(partition: Partition, letter_3: str) -> None:
    assert len(letter_3) == 3
   
    commands = [
        f"sel disk {partition.disk.id}",
        f"sel part {partition.id}",
        f"assign letter={letter_3[0]}"
    ]

    diskpart(commands)

def get_partition_letter(partition: Partition) -> Optional[str]:
    """Get the letter associated with this partition, in the format `C:\`, if there is one"""
    partition_device_path = volume_name_to_device_path(partition.device_name)

    for letter_1 in get_allocated_letters():
        letter_device_path = drive_letter_to_device_path(f"{letter_1}:\\")
        if not letter_device_path:
            continue
        
        if letter_device_path == partition_device_path:
            return f"{letter_1}:\\"

def mount(partition: Partition) -> str:
    """
    Makes a partition available ("mounted") **if it not already**
    Returns the root path of the partition
    """

    # Check if we already have a letter associated with this partition
    letter_3 = get_partition_letter(partition)
    if letter_3:
        return letter_3

    letter_3 = get_free_letter()
    
    actually_mount(partition, letter_3)

    return letter_3

def unmount(partition: Partition, letter_3: str):
    """
    Removes the given letter in the format `C:\` from the given partition.
    Undefined behaviour if any information is incorrect
    """
    assert len(letter_3) == 3
   
    commands = [
        f"sel disk {partition.disk.id}",
        f"sel part {partition.id}",
        f"remove letter={letter_3[0]}"
    ]

    diskpart(commands)
    pass
