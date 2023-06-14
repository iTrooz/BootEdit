from typing import List

from PyQt6.QtWidgets import *

from bootedit.backend.partition_select import Disk, Partition

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
        layout.addWidget(self.tree)

        bottom_widget = QWidget()
        layout.addWidget(bottom_widget)
        
        bottom_layout = QHBoxLayout()
        bottom_widget.setLayout(bottom_layout)
        bottom_layout.addStretch()

        self.open_button = QPushButton("Open")
        self.open_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
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
                part_item.setText(0, partition.name)
                disk_item.addChild(part_item)

                if partition == default_partition:
                    part_item.setSelected(True)

