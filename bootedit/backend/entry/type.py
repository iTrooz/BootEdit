from firmware_variables.load_option import LoadOption, LoadOptionAttributes
from bootedit.backend.partition import get_partitions
from bootedit.backend.fv_ext.load_option_path import LoadOptionPath, parse_file_path_list


class UEFIEntry:
    """
    elements of an UEFI entry that an user will interact with

    :attr id: ID of this entry (the 4 hex digit of the Boot### variable in decimal form)
    :attr name: Name of this entry
    :attr enabled: if this boot entry is enabled or not
    :attr location: path of the executable to run
    """
    def __init__(self):
        self.id = 0
        self.name = ""
        self.enabled = False
        self.partition = ""
        self.file_path = ""

    @staticmethod
    def from_load_option(entry_id: int, load_option: LoadOption):
        entry = UEFIEntry()
        entry.id = entry_id
        entry.name = load_option.description
        entry.enabled = bool(load_option.attributes & LoadOptionAttributes.LOAD_OPTION_ACTIVE)

        load_option_path = parse_file_path_list(load_option.file_path_list)
        entry.file_path = load_option_path.file_path

        disks = get_partitions()
        for disk in disks:
            for partition in disk.partitions:
                if partition.part_uuid == load_option_path.guid:
                    entry.partition = partition.internal_name

        return entry
