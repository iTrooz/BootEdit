import sys

from .type import Disk, Partition

match sys.platform:
    case "linux":
        from .linux import get_partitions
    case "win32":
        from .win32 import get_partitions
    case _:
        raise RuntimeError("Platform not supported: "+sys.platform)
