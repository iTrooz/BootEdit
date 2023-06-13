import sys

from bootedit.backend.win_backend import WinBackend

def get_platform_backend():
    match sys.platform:
        case "win32":
            return WinBackend()
        case _:
            raise NotImplementedError(f"Platform {sys.platform} not supported")
