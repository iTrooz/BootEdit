from ..partition import Partition
from .platform import mount, get_mount_path, unmount

class MountError(RuntimeError):
    pass

class MountGuard:
    """
    Mounts a partition, and unmounts it when the object is deleted

    Apparently __del__ is not guarranted to be called, and I should use context managers,
    but AFAIK context managers would not work in this case. 
    (the object gets deleted in another function, when the user clicks on another entry)
    """

    def __init__(self, partition: Partition) -> None:
        self.partition = partition

        # Try to get existing mount path
        self.path = get_mount_path(self.partition)
        if self.path:
            self.mounted_by_me = False
        else:
            # If none exist, mount the partition
            self.path = mount(partition)
            self.mounted_by_me = True

    def unmount(self):
        if self.mounted_by_me:
            unmount(self.partition, self.path)
            
            # Reset object properties so we don't unmoutn it a second time (like when the object is deleted)
            self.partition = None
            self.mounted_by_me = None

    def __del__(self, *_):
        self.unmount()
