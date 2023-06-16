from typing import List
import os

from PyQt6.QtWidgets import *

from bootedit.backend.partition_select import Disk, Partition
from bootedit.backend.partition_select import mount, unmount
from bootedit.ui.qt.entry_add_ui import Ui_EntryAdd

# https://stackoverflow.com/a/37095733
def path_is_parent(parent_path: str, child_path: str) -> bool:
    # Smooth out relative path names, note: if you are concerned about symbolic links, you should use os.path.realpath too
    parent_path = os.path.abspath(parent_path)
    child_path = os.path.abspath(child_path)

    # Compare the common path of the parent and child path with the common path of just the parent path. Using the commonpath method on just the parent path will regularise the path name in the same way as the comparison that deals with both paths, removing any trailing path separator
    return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, child_path])

class EntryAddWindow(QWidget):
    
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        self.ui = Ui_EntryAdd()
        self.ui.setupUi(self)

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
        selected_list = self.tree.selectedItems()
        if len(selected_list) != 1:
            print("Should not happen: partition_selected() called not 1 selected item: {}", selected_list)
            return
        
        part_item = selected_list[0]
        if not hasattr(part_item, "partition"):
            return
        
        self.selected_partition = part_item.partition

        QMessageBox.information(self, "", "The selected partition will be mounted. "
                                "Please select the bootable file to add inside this partition")
        
        root_folder = mount(self.selected_partition)
        ret = QFileDialog.getOpenFileName(directory=root_folder)
        unmount(root_folder)

        selected_file = ret[0]
        if not selected_file:
            return
        if not path_is_parent(root_folder, selected_file):
            QMessageBox.critical(self, "", "File selected is not inside the mounted partition")
            return
            
        relpath = os.path.relpath(selected_file, root_folder)
        
        self.add_entry(self.selected_partition, relpath)
