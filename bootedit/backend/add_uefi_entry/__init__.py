import sys

match sys.platform:
    case "win32":
        from .win32 import Disk, Partition, get_partitions
    case "linux":
        from .linux import Disk, Partition, get_partitions, mount, unmount, add_uefi_entry
    case _:
        raise RuntimeError("Platform not supported: "+sys.platform)
