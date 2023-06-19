from typing import List, Optional
import os

from PyQt6.QtWidgets import QWidget, QLineEdit, QDialogButtonBox, QMessageBox, QFileDialog, QTreeWidgetItem

from bootedit.backend.add_uefi_entry import Disk, Partition
from bootedit.backend.add_uefi_entry import mount, unmount, add_uefi_entry
from bootedit.backend.add_uefi_entry.linux.mount import MountError
from bootedit.ui.qt.add_uefi_entry_ui import Ui_AddUEFIEntry

# https://stackoverflow.com/a/37095733
def path_is_parent(parent_path: str, child_path: str) -> bool:
    # Smooth out relative path names, note: if you are concerned about symbolic links, you should use os.path.realpath too
    parent_path = os.path.abspath(parent_path)
    child_path = os.path.abspath(child_path)

    # Compare the common path of the parent and child path with the common path of just the parent path. Using the commonpath method on just the parent path will regularise the path name in the same way as the comparison that deals with both paths, removing any trailing path separator
    return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, child_path])


def set_line_edit_color(line_edit: QLineEdit):
    line_edit.setStyleSheet("QLineEdit{border:1px solid red}")

def clear_line_edit_color(line_edit: QLineEdit):
    line_edit.setStyleSheet("")


# https://stackoverflow.com/a/1094933
def sizeof_fmt(num: int, suffix: str="B") -> str:
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


class AddUEFIEntryWindow(QWidget):
    
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        
        self.selected_partition: Partition = None
        self.selected_file_relpath: Optional[str] = None
        self.selected_file_size: Optional[int] = None
        self.entry_name: str = ""
        self.mount_point: Optional[str] = None
        self.disks: Optional[List[Disk]] = None

        self.ui = Ui_AddUEFIEntry()
        self.ui.setupUi(self)

        # Reset UI values
        self.ui.edit_partition.setText("")
        self.ui.edit_file.setText("")
        self.ui.edit_file_size.setText("")
        self.ui.edit_entry_name.setText("")

        self.ui.tree_manual_partition.itemSelectionChanged.connect(self.partition_tree_selected_slot)
        self.ui.edit_partition.textChanged.connect(self.partition_line_edit_edited_slot)

        self.ui.but_manual_file.clicked.connect(self.select_file_with_file_selector_slot)
        self.ui.edit_file.textChanged.connect(self.file_line_edit_edited_slot)

        self.ui.edit_entry_name.textEdited.connect(self.entry_name_line_edit_edited_slot)

        self.ui.edit_entry_name.textEdited.connect(self.entry_name_line_edit_edited_slot)

        ok_button = self.ui.box_ok_cancel.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.clicked.connect(self.ok_button_clicked_slot)
        
        cancel_button = self.ui.box_ok_cancel.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.clicked.connect(lambda: self.close())

        self.update_widgets_errors()

    # ----- Partition stuff

    def find_partition(self, device_name) -> Optional[Partition]:
        for disk in self.disks:
            for partition in disk.partitions:
                if partition.device_name == device_name:
                    return partition
        return None

    def partition_line_edit_edited_slot(self):
        """
        Trigerred when we edit the partition line edit widget (one call per character)
        """

        partition = self.find_partition(self.ui.edit_partition.text()) # Find this device name in all the partitions we have
        self.set_selected_partition(partition) # sets self.selected_partition, mounts it, and clears file line edits

        self.update_widgets_errors()

    def partition_tree_selected_slot(self):
        """
        Trigerred when we select a partition through the tree widget
        """

        selected_list = self.ui.tree_manual_partition.selectedItems()
        partition: Optional[Partition] = None
        if len(selected_list) == 1:
            part_item = selected_list[0]
            if hasattr(part_item, "partition"):
                partition = part_item.partition
        
        if partition:
            self.ui.edit_partition.setText(partition.device_name)
            # the edit line text edit event will take care of updating the partition
            
            self.update_widgets_errors()
        else:
            self.ui.edit_partition.setText("")
            # the edit line text edit event will take care of updating the partition

            self.update_widgets_errors()
    
    def set_selected_partition(self, partition: Optional[Partition]) -> None:
        """
        Helper function to set the partition, mount it, and clear file data
        does NOT set the line edit
        """

        if self.selected_partition == partition:
            return

        # clear file data
        self.set_selected_file(None)
        self.update_file_line_edits()

        # remove from old mount point
        if self.mount_point:
            unmount(self.mount_point)
            self.mount_point = None

        # try to mount the new mount point
        error = None
        if partition:
            try:
                self.mount_point = mount(partition)
            except MountError as e:
                error = e

        if error:
            self.mount_point = None
            self.selected_partition = None
            self.selected_partition_valid = False

            self.update_widgets_errors()

            QMessageBox.critical(self, "", f"Failed to mount partition {partition.device_name}.\n"
                                    f"Error: {error}")
        elif partition == None:
            self.selected_partition = None
            self.selected_partition_valid = False

            self.update_widgets_errors()
        else:
            self.selected_partition = partition
            self.selected_partition_valid = True

            self.update_widgets_errors()

    # ----- END Partition stuff

    # ----- File and file size stuff

    def file_line_edit_edited_slot(self):
        """
        Trigerred when we edit the file line edit widget (one call per character)
        """

        full_file_path = os.path.join(self.mount_point, self.ui.edit_file.text())
        self.set_selected_file(full_file_path)

        self.update_widgets_errors()

    def select_file_with_file_selector_slot(self):
        """
        Called when we want to select the file with the system file selector
        """
        ret = QFileDialog.getOpenFileName(directory=self.mount_point)

        full_file_path = ret[0]
        if full_file_path:
            if path_is_parent(self.mount_point, full_file_path):
                self.set_selected_file(full_file_path)

                self.update_file_line_edits()

                self.update_widgets_errors()
            else:
                
                QMessageBox.critical(self, "", "File selected is not inside the mounted partition")

    def update_file_line_edits(self):
        """
        Override edit line values with the object fields
        This will NOT call events sets on the file edit line.
        """

        old_state = self.ui.edit_file.blockSignals(True)

        if self.selected_file_relpath == None:
            self.ui.edit_file.setText("")
            self.ui.edit_file_size.setText("")
        else:
            self.ui.edit_file.setText(self.selected_file_relpath)
            self.ui.edit_file_size.setText(sizeof_fmt(self.selected_file_size))
        
        self.ui.edit_file.blockSignals(old_state)

    def set_selected_file(self, full_file_path: Optional[str]) -> None:
        """
        Helper function to set the selected file field and its size.
        does NOT set the line edits
        """

        if full_file_path and os.path.isfile(full_file_path):
            self.selected_file_size = os.path.getsize(full_file_path)
            self.selected_file_relpath = os.path.relpath(full_file_path, self.mount_point)
        else:
            self.selected_file_size = None
            self.selected_file_relpath = None

    # ----- END File and file size stuff

    # ----- Entry name stuff

    def entry_name_line_edit_edited_slot(self):
        self.entry_name = self.ui.edit_entry_name.text()

        self.update_widgets_errors()

    # ----- EDN Entry name stuff

    def update_widgets_errors(self):
        """
        Update the red rectangle on line edits, button grayed, and the final error message.
        Does NOT modify the edit lines.
        """

        # Only enable the file selection button if we selected a partition
        self.ui.but_manual_file.setDisabled(self.selected_partition == None)

        error_msg = ""

        # Update "Partition" line in "Entry information"
        if self.selected_partition:
            clear_line_edit_color(self.ui.edit_partition)
            self.ui.edit_file.setEnabled(True)
        else:
            # If a partition is not selected, we shouldn't even be able to edit the field
            set_line_edit_color(self.ui.edit_partition)
            self.ui.edit_file.setEnabled(False)

            if self.ui.edit_partition.text():
                error_msg = error_msg or "Invalid partition selected"
            else:
                error_msg = error_msg or "Please select a partition"

        # Update "File" line in "Entry information"
        if self.selected_file_relpath:
            clear_line_edit_color(self.ui.edit_file)
        else:
            if self.selected_partition:
                set_line_edit_color(self.ui.edit_file)
                if self.ui.edit_file.text():
                    error_msg = error_msg or "Invalid file selected"
                else:
                    error_msg = error_msg or "Please select a file inside the partition"
        
        # Reset the red rectangle if we can't interact with the button
        if not self.ui.edit_file.isEnabled():
            clear_line_edit_color(self.ui.edit_file)

        # Set the error message is the entry name is not set
        if self.entry_name:
            clear_line_edit_color(self.ui.edit_entry_name)
        else:
            set_line_edit_color(self.ui.edit_entry_name)
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
        self.disks = disks

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

    def ok_button_clicked_slot(self):
        rel_file_path = self.selected_file_relpath

        # Ensure the format of the relative file path in the partition (should start with the character '\' )
        if rel_file_path[0] != "\\":
            rel_file_path = "\\" + rel_file_path
        
        add_uefi_entry(self.selected_partition, rel_file_path, self.entry_name)

        self.close()        
