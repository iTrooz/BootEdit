# firmware-variables extension

import struct
from uuid import UUID

from firmware_variables.utils import utf16_string_from_bytes
from firmware_variables.device_path import DevicePathList, MediaDevicePathSubtype
from firmware_variables.platform import get_variable
from firmware_variables.boot import get_parsed_boot_entry

# Hard drive media device path (UEFI spec release 2.10 subsection 10.3.5.1)
EFI_HARD_DRIVE = struct.Struct("<IQQQQBB")

class EntryLocation:
    """
    :attr table_id: ID of this partition on the partition table of the device
    :attr sig_id: Unique ID of this partition, usually represented witht he UUID format
    """
    def __init__(self) -> None:
        self.table_id = None
        self.sig_id = None
        self.file_path = None

    def is_valid(self) -> bool:
        return (self.table_id != None and
            self.sig_id != None and
            self.file_path != None)

    def __repr__(self) -> str:
        return "EntryLocation(table_id={}, sig_id={}, file_path={})".format(self.table_id, self.sig_id, self.file_path)


def parse_file_path_list(file_path_list: DevicePathList) -> EntryLocation:
    entry_location = EntryLocation()
    for path in file_path_list.paths:

        if path.subtype == MediaDevicePathSubtype.HARD_DRIVE:
            p_number, p_start, p_size, p_sig_1, p_sig_2, p_format, p_type = EFI_HARD_DRIVE.unpack(path.data)
            entry_location.table_id = p_number

            p_sig = p_sig_1.to_bytes(8, 'little') + p_sig_2.to_bytes(8, 'little')

            entry_location.sig_id = str(UUID(bytes_le=p_sig))
        if path.subtype == MediaDevicePathSubtype.FILE_PATH:
            entry_location.file_path = utf16_string_from_bytes(path.data)
    
    return entry_location

def get_parsed_current_boot_entry():
    data, attributes = get_variable("BootCurrent")
    entry_id = int.from_bytes(data, 'little')
    return get_parsed_boot_entry(entry_id)
