import sys

match sys.platform:
    case "linux":
        from .linux import mount, unmount, get_mount_path
    case "win32":
        from .win32 import mount, unmount, get_mount_path
    case _:
        raise RuntimeError("Platform not supported: "+sys.platform)
