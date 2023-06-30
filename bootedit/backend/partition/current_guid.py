from typing import Optional

from bootedit.backend.fv_ext import parse_file_path_list, get_parsed_current_boot_entry


def get_current_guid() -> Optional[str]:
    """
    get the GUID of the partition we used to boot
    """

    curr_entry = get_parsed_current_boot_entry()
    curr_entry_loc = parse_file_path_list(curr_entry.file_path_list)

    return curr_entry_loc.sig_id
