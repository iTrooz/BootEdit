from firmware_variables.load_option import LoadOption, LoadOptionAttributes
from firmware_variables import get_variable, FVError, set_parsed_boot_entry
from firmware_variables import get_boot_order, set_boot_order

from bootedit.backend.add_uefi_entry.linux.get_partitions import Partition
from bootedit.backend.add_uefi_entry.linux.gen_file_path_list import gen_file_path_list


def get_unused_boot_entry_id() -> int:
    # Try entries from 0x0001 to 0x0FFF.
    # No reason I don't try higher, if just feels weird if something isn't unused at that point
    for i in range(0x0001, 0x0FFF+1):
        entry_id = "Boot{:04X}".format(i)
        try:
            get_variable(entry_id)
        except FVError:
            return i

    raise RuntimeError("No entries from Boot0001 to Boot0FFF were free. Is something wrong ?")

def add_uefi_entry(partition: Partition, rel_file_path: str, entry_name: str) -> None:
    load_option = gen_uefi_entry(partition, rel_file_path, entry_name)
    entry_id = get_unused_boot_entry_id()
    
    set_parsed_boot_entry(entry_id, load_option)

    order = get_boot_order()
    set_boot_order(order + [entry_id])

def gen_uefi_entry(partition: Partition, rel_file_path: str, entry_name: str) -> LoadOption:
    load_option = LoadOption()
    load_option.description = entry_name
    load_option.file_path_list = gen_file_path_list(partition, rel_file_path)
    load_option.attributes = LoadOptionAttributes.LOAD_OPTION_ACTIVE

    return load_option
