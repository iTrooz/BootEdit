from typing import List
import os

from PyQt6.QtWidgets import *

from bootedit.backend.partition_select import Disk, Partition
from bootedit.backend.partition_select import mount, unmount

# https://stackoverflow.com/a/37095733
def path_is_parent(parent_path: str, child_path: str) -> bool:
    # Smooth out relative path names, note: if you are concerned about symbolic links, you should use os.path.realpath too
    parent_path = os.path.abspath(parent_path)
    child_path = os.path.abspath(child_path)

    # Compare the common path of the parent and child path with the common path of just the parent path. Using the commonpath method on just the parent path will regularise the path name in the same way as the comparison that deals with both paths, removing any trailing path separator
    return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, child_path])

class PartitionSelector(QWidget):
    
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        self.setWindowTitle("Partition selector")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Select the partition on which the bootable file is")
        layout.addWidget(self.label)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.doubleClicked.connect(self.partition_selected)
        layout.addWidget(self.tree)

        bottom_widget = QWidget()
        layout.addWidget(bottom_widget)
        
        bottom_layout = QHBoxLayout()
        bottom_widget.setLayout(bottom_layout)
        bottom_layout.addStretch()

        self.open_button = QPushButton("Open")
        self.open_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.open_button.clicked.connect(self.partition_selected)
        bottom_layout.addWidget(self.open_button)


    def set_data(self, disks: List[Disk], default_partition: Partition):
        self.tree.clear()

        for disk in disks:
            disk_item = QTreeWidgetItem()
            disk_item.setText(0, disk.name)
            self.tree.addTopLevelItem(disk_item)
            disk_item.setExpanded(True)


            for partition in disk.partitions:
                part_item = QTreeWidgetItem()
                part_item.partition = partition
                part_item.setText(0, partition.name)
                disk_item.addChild(part_item)

                if partition == default_partition:
                    part_item.setSelected(True)
    
    def partition_selected(self):
        selected_list = self.tree.selectedItems()
        if len(selected_list) != 1:
            print("Should not happen: partition_selected() called not 1 selected item: {}", selected_list)
            return
        
        part_item = selected_list[0]
        self.selected_partition = part_item.partition

        QMessageBox.information(self, "", "The selected partition has been mounted. "
                                "Please select the bootable file to add inside this partition")
        
        root_folder = mount(self.selected_partition)
        ret = QFileDialog.getOpenFileName(directory=root_folder)
        unmount(root_folder)

        selected_file = ret[0]
        if selected_file:
            if not path_is_parent(root_folder, selected_file):
                QMessageBox.critical(self, "", "File selected is not inside the mounted partition")
                return
            
        relpath = os.path.relpath(selected_file, root_folder)
        

        print("Selected: file")
