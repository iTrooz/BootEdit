import ctypes
import ctypes.util
import os
import tempfile

from .get_partitions import Partition

libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
libc.mount.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong, ctypes.c_char_p)

def mount_raw(source, target, fs, options=''):
    ret = libc.mount(source.encode(), target.encode(), fs.encode(), 0, options.encode())
    if ret < 0:
        errno = ctypes.get_errno()
        raise OSError(errno, f"Error mounting {source} ({fs}) on {target} with options '{options}': {os.strerror(errno)}")

def mount(partition: Partition):
    tmpdir = tempfile.mkdtemp()
    mount_raw(partition.device_name, tmpdir, partition.type, 'ro')

    print(f"Mounted partition {partition.device_name} on {tmpdir}")

    return tmpdir

def unmount(path: str):
    # TODO
    pass
