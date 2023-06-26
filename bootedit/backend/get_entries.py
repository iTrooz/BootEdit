from bootedit.backend.entry import UEFIEntry

from firmware_variables import *


def get_uefi_entries() -> list[UEFIEntry]:
    my_entries = []

    with adjust_privileges():
        for entry_id in get_boot_order():
            load_option = get_parsed_boot_entry(entry_id)

            my_entry = UEFIEntry.from_load_option(entry_id, load_option)

            my_entries.append(my_entry)

    return my_entries
