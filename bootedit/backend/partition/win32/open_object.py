from typing import Optional

from ctypes import wintypes, windll
import win32file

# Documentation in get_volume_disk_id.py

INVALID_HANDLE_VALUE = 0xFFFFFFFFFFFFFFFF

NULL = 0

def open_object(path: str) -> Optional[wintypes.HANDLE]:
    """
    ref: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew

    Return None if the path is invalid
    """

    CreateFileW = windll.kernel32.CreateFileW
    CreateFileW.argtypes = (
        wintypes.LPCWSTR,  # LPCWSTR               lpFileName
        wintypes.DWORD,    # DWORD                 dwDesiredAccess
        wintypes.DWORD,    # DWORD                 dwShareMode
        wintypes.LPVOID,   # LPSECURITY_ATTRIBUTES lpSecurityAttributes
        wintypes.DWORD,    # DWORD                 dwCreationDisposition
        wintypes.DWORD,    # DWORD                 dwFlagsAndAttributes
        wintypes.HANDLE,   # HANDLE                hTemplateFile
    )
    CreateFileW.restype = wintypes.HANDLE

    ret = CreateFileW(
        path,
        win32file.GENERIC_READ, # access
        win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, # share mode
        NULL, # security attributes
        win32file.OPEN_EXISTING, #creation
        0, # flag,
        NULL, # template file
    )

    if ret == INVALID_HANDLE_VALUE:
        return None
    else:
        return ret
