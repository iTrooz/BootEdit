from firmware_variables.load_option import LoadOption
from bootedit.backend.add_uefi_entry import get_partitions
from bootedit.backend.fv_ext.load_option_path import LoadOptionPath, parse_file_path_list


class UEFIEntry:
    """
    elements of an UEFI entry that an user will interact with

    :attr id: ID of this entry (the 4 hex digit of the Boot### variable in decimal form)
    :attr name: Name of this entry
    :attr attributes: bitfield with flags of this entry
    :attr location: path of the executable to run
    """
    def __init__(self):
        self.id = 0
        self.name = ""
        self.attributes = 0
        self.partition = ""
        self.file_path = ""

    @staticmethod
    def from_load_option(entry_id: int, load_option: LoadOption):
        entry = UEFIEntry()
        entry.id = entry_id
        entry.name = load_option.description
        entry.attributes = load_option.attributes

        load_option_path = parse_file_path_list(load_option.file_path_list)
        entry.file_path = load_option_path.file_path

        disks, _ = get_partitions()
        for disk in disks:
            for partition in disk.partitions:
                if partition.part_uuid == load_option_path.sig_id:
                    entry.partition = partition.device_name

        return entry
