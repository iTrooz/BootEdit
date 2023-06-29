import sys

match sys.platform:
    case "linux":
        from .linux import gen_hard_drive_subtype
    case "win32":
        from .win32 import gen_hard_drive_subtype
    case _:
        raise RuntimeError("Platform not supported: "+sys.platform)
