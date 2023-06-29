import sys

from .type import MountError

match sys.platform:
    case "linux":
        from .linux import mount, unmount
    case "win32":
        from .win32 import mount, unmount
    case _:
        raise RuntimeError("Platform not supported: "+sys.platform)
