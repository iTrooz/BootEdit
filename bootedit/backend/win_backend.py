from firmware_variables import *

from bootedit.backend.backend import Backend
from bootedit.backend.entry import UEFIEntry

class WinBackend(Backend):

    def get_uefi_entries(self) -> list[str]:
        my_entries = []

        with adjust_privileges():
            for entry_id in get_boot_order():
                load_option = get_parsed_boot_entry(entry_id)

                my_entry = UEFIEntry()
                my_entry.name = load_option.description
                my_entry.attributes = load_option.attributes
                my_entry.location = str(load_option.file_path_list)
                my_entries.append(my_entry)

        return my_entries
