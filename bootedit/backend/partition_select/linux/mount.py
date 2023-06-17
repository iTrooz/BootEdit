import subprocess
import os
import tempfile

from .get_partitions import Partition

def mount(partition: Partition):
    tmpdir = tempfile.mkdtemp(prefix="tmp-bootedit-")
    
    mounted = False
    try:
        subprocess.check_call(["mount", partition.device_name, tmpdir, "-t", partition.type, '-r'])
        mounted = True
    except subprocess.CalledProcessError:
        pass
    
    # mount in read-only can fail if the partition was already mounted in read-write elsewhere
    # If so, try to mount again in read-write mode
    # Do not do this in the 'except' block to avoid 'During handling of the above exception, another exception occurred'
    if not mounted:
        subprocess.check_call(["mount", partition.device_name, tmpdir, "-t", partition.type])
    
    print(f"Mounted partition {partition.device_name} on {tmpdir}")

    return tmpdir

def unmount(device_path: str):
    subprocess.check_call(["umount", device_path])
