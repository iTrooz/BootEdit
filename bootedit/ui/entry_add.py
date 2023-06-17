from typing import List
import os

from PyQt6.QtWidgets import *

from bootedit.backend.partition_select import Disk, Partition
from bootedit.backend.partition_select import mount, unmount
from bootedit.backend.partition_select.linux.mount import MountError
from bootedit.ui.qt.entry_add_ui import Ui_AddUEFIEntry

# https://stackoverflow.com/a/37095733
def path_is_parent(parent_path: str, child_path: str) -> bool:
    # Smooth out relative path names, note: if you are concerned about symbolic links, you should use os.path.realpath too
    parent_path = os.path.abspath(parent_path)
    child_path = os.path.abspath(child_path)

    # Compare the common path of the parent and child path with the common path of just the parent path. Using the commonpath method on just the parent path will regularise the path name in the same way as the comparison that deals with both paths, removing any trailing path separator
    return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, child_path])



# https://stackoverflow.com/a/1094933
def sizeof_fmt(num: int, suffix: str="B") -> str:
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


class EntryAddWindow(QWidget):
    
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        
        self.selected_partition: Partition = None
        self.selected_file_relpath: str = None
        self.selected_file_size: int = None
        self.entry_name: str = None
        self.mount_point: str = ""

        self.ui = Ui_AddUEFIEntry()
        self.ui.setupUi(self)

        self.update_widgets_status()

        self.ui.tree_manual_partition.itemSelectionChanged.connect(self.partition_selected)
        self.ui.but_manual_file.clicked.connect(self.select_file)

        self.ui.edit_entry_name.setText("")
        self.ui.edit_entry_name.textEdited.connect(lambda: self.entry_name_edited())

    def info_entry_name_edited(self):
        self.entry_name = self.ui.edit_entry_name.text()
        self.update_widgets_status()

    def set_partition_and_update(self, partition: Partition) -> None:
        if self.selected_partition == partition:
            return
        
        self.selected_partition = partition

        # update mount point
        if self.mount_point:
            unmount(self.mount_point)

        try:
            self.mount_point = mount(self.selected_partition)
        except MountError as e:
            errmsg = (f"Failed to mount partition {self.selected_partition.device_name}. "
                                    f"Error: {e}")
            self.mount_point = None
            self.selected_partition = None
            self.set_file_and_update(None, None, update=False)

            self.update_widgets_status()

            QMessageBox.critical(self, "", errmsg)
            
            return

        self.set_file_and_update(None, None, update=False)

        self.update_widgets_status()

    def set_file_and_update(self, file_full_path: str, file_rel_path: str, update: bool = True) -> None:
        if self.selected_file_relpath == file_rel_path:
            return
        
        if file_full_path and file_rel_path:
            self.selected_file_size = os.path.getsize(file_full_path)
            self.selected_file_relpath = file_rel_path
        else:
            self.selected_file_size = 0
            self.selected_file_relpath = ""

        if update:
            self.update_widgets_status()

    def update_widgets_status(self):
        # Only enable the file selection button if we selected a partition
        self.ui.but_manual_file.setDisabled(self.selected_partition == None)

        error_msg = ""

        # Update "Partition" line in "Entry information"
        if self.selected_partition:
            self.ui.edit_partition.setText(self.selected_partition.device_name)
        else:
            error_msg = error_msg or "Please select a partition"
            self.ui.edit_partition.setText("")

        # Update "Partition" line in "Entry information"
        if self.selected_file_relpath:
            self.ui.edit_file.setText(self.selected_file_relpath)
        else:
            self.ui.edit_file.setText("")
            error_msg = error_msg or "Please select a file inside the partition"

        # Update "File size" line in "Entry information"
        if self.selected_file_size:
            self.ui.edit_file_size.setText(sizeof_fmt(self.selected_file_size))
        else:
            self.ui.edit_file_size.setText("")

        # Set the error message is the entry name is not set
        if not self.entry_name:
            error_msg = error_msg or "Please select a name for this entry"

        # Update "Ok" button if everything is entered right
        ok_button = self.ui.box_ok_cancel.button(QDialogButtonBox.StandardButton.Ok)
        if error_msg:
            self.ui.label_error.setText(error_msg)
            ok_button.setEnabled(False)
        else:
            self.ui.label_error.setText("")
            ok_button.setEnabled(True)
    

    def set_partitions_data(self, disks: List[Disk], default_partition: Partition):
        self.ui.tree_manual_partition.clear()

        for disk in disks:
            disk_item = QTreeWidgetItem()
            disk_item.setText(0, disk.name)
            self.ui.tree_manual_partition.addTopLevelItem(disk_item)
            disk_item.setExpanded(True)


            for partition in disk.partitions:
                part_item = QTreeWidgetItem()
                part_item.partition = partition
                part_item.setText(0, partition.device_name)
                part_item.setText(1, partition.type)
                disk_item.addChild(part_item)

                if partition == default_partition:
                    part_item.setSelected(True)
    
    def partition_selected(self):
        selected_list = self.ui.tree_manual_partition.selectedItems()
        if len(selected_list) == 1:
            part_item = selected_list[0]
            if hasattr(part_item, "partition"):
                self.set_partition_and_update(part_item.partition)
                return
            

        self.set_partition_and_update(None)

        
    def select_file(self):
        ret = QFileDialog.getOpenFileName(directory=self.mount_point)

        selected_file = ret[0]
        if selected_file:
            if path_is_parent(self.mount_point, selected_file):
                self.set_file_and_update(selected_file, os.path.relpath(selected_file, self.mount_point))
            else:
                QMessageBox.critical(self, "", "File selected is not inside the mounted partition")

