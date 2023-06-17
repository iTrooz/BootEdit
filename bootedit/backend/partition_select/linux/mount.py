import subprocess
import os
import tempfile

from .get_partitions import Partition

def mount(partition: Partition):
    tmpdir = tempfile.mkdtemp(prefix="tmp-bootedit-")
    
    subprocess.check_call(["mount", partition.device_name, tmpdir, "-t", partition.type, '-r'])
    
    print(f"Mounted partition {partition.device_name} on {tmpdir}")

    return tmpdir

def unmount(device_path: str):
    subprocess.check_call(["umount", device_path])
