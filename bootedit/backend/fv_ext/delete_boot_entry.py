from firmware_variables.variables import delete_variable
from firmware_variables.boot import get_boot_order, set_boot_order

def delete_boot_entry(entry_id: int) -> None:
    delete_variable("Boot{:04X}".format(entry_id))
    order = get_boot_order()
    try:
        order.remove(entry_id)
    except ValueError:
        entry_str = "{:04X}".format(entry_id)
        raise RuntimeError(f"Entry ID '{entry_str}' is not present in the boot order !")
    
    set_boot_order(order)