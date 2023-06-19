from firmware_variables import *

from .entry import UEFIEntry
from .fv_ext import parse_file_path_list

def get_uefi_entries() -> list[str]:
    my_entries = []

    with adjust_privileges():
        for entry_id in get_boot_order():
            load_option = get_parsed_boot_entry(entry_id)

            my_entry = UEFIEntry()
            my_entry.name = load_option.description
            my_entry.attributes = load_option.attributes
            
            location = parse_file_path_list(load_option.file_path_list)
            if location.is_valid():
                my_entry.location = location
            
            my_entries.append(my_entry)

    return my_entries
