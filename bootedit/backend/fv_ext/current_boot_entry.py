from firmware_variables import get_variable, get_parsed_boot_entry

def get_current_boot_entry_id():
    data, attributes = get_variable("BootCurrent")
    return int.from_bytes(data, 'little')

def get_parsed_current_boot_entry():
    entry_id = get_current_boot_entry_id()
    return get_parsed_boot_entry(entry_id)
