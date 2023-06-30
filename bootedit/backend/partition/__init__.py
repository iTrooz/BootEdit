import sys

from .type import Disk, Partition
from .current_guid import get_current_guid

match sys.platform:
    case "linux":
        from .linux import get_partitions
    case "win32":
        from .win32 import get_partitions
    case _:
        raise RuntimeError("Platform not supported: "+sys.platform)
