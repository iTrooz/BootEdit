# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'entry_addqtHFFb.ui'
##
## Created by: Qt User Interface Compiler version 5.15.9
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

# Modified manually for use in PyQt6

from PyQt6.QtCore import *  # type: ignore
from PyQt6.QtGui import *  # type: ignore
from PyQt6.QtWidgets import *  # type: ignore


class Ui_EntryAdd(object):
    def setupUi(self, EntryAdd):
        if not EntryAdd.objectName():
            EntryAdd.setObjectName(u"EntryAdd")
        EntryAdd.resize(446, 714)
        self.verticalLayout_4 = QVBoxLayout(EntryAdd)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget = QWidget(EntryAdd)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.label)

        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.but_auto_windows = QPushButton(self.widget)
        self.but_auto_windows.setObjectName(u"but_auto_windows")

        self.horizontalLayout.addWidget(self.but_auto_windows)

        self.but_auto_linux = QPushButton(self.widget)
        self.but_auto_linux.setObjectName(u"but_auto_linux")

        self.horizontalLayout.addWidget(self.but_auto_linux)

        self.but_auto_all = QPushButton(self.widget)
        self.but_auto_all.setObjectName(u"but_auto_all")

        self.horizontalLayout.addWidget(self.but_auto_all)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_4.addWidget(self.widget)

        self.widget_2 = QWidget(EntryAdd)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.label_2)

        self.line_2 = QFrame(self.widget_2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.tree_manual_partition = QTreeWidget(self.widget_2)
        __qtreewidgetitem = QTreeWidgetItem(self.tree_manual_partition)
        QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(self.tree_manual_partition)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem2 = QTreeWidgetItem(self.tree_manual_partition)
        QTreeWidgetItem(__qtreewidgetitem2)
        self.tree_manual_partition.setObjectName(u"tree_manual_partition")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tree_manual_partition.sizePolicy().hasHeightForWidth())
        self.tree_manual_partition.setSizePolicy(sizePolicy2)
        self.tree_manual_partition.setHeaderHidden(False)
        self.tree_manual_partition.header().setDefaultSectionSize(175)

        self.verticalLayout.addWidget(self.tree_manual_partition)

        self.but_manual_file = QPushButton(self.widget_2)
        self.but_manual_file.setObjectName(u"but_manual_file")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.but_manual_file.sizePolicy().hasHeightForWidth())
        self.but_manual_file.setSizePolicy(sizePolicy3)

        self.verticalLayout.addWidget(self.but_manual_file)


        self.verticalLayout_4.addWidget(self.widget_2)

        self.widget_3 = QWidget(EntryAdd)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.label_3)

        self.line_3 = QFrame(self.widget_3)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_6 = QLabel(self.widget_3)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.label_6)

        self.edit_partition = QLineEdit(self.widget_3)
        self.edit_partition.setObjectName(u"edit_file_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.edit_partition.sizePolicy().hasHeightForWidth())
        self.edit_partition.setSizePolicy(sizePolicy4)

        self.horizontalLayout_5.addWidget(self.edit_partition)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_4)

        self.edit_file = QLineEdit(self.widget_3)
        self.edit_file.setObjectName(u"edit_file")
        sizePolicy4.setHeightForWidth(self.edit_file.sizePolicy().hasHeightForWidth())
        self.edit_file.setSizePolicy(sizePolicy4)

        self.horizontalLayout_3.addWidget(self.edit_file)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(self.widget_3)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.edit_file_size = QLineEdit(self.widget_3)
        self.edit_file_size.setObjectName(u"edit_file_size")

        self.horizontalLayout_4.addWidget(self.edit_file_size)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_7 = QLabel(self.widget_3)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.label_7)

        self.edit_entry_name = QLineEdit(self.widget_3)
        self.edit_entry_name.setObjectName(u"edit_file_3")
        sizePolicy4.setHeightForWidth(self.edit_entry_name.sizePolicy().hasHeightForWidth())
        self.edit_entry_name.setSizePolicy(sizePolicy4)

        self.horizontalLayout_6.addWidget(self.edit_entry_name)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)


        self.verticalLayout_4.addWidget(self.widget_3)

        self.line_4 = QFrame(EntryAdd)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_error = QLabel(EntryAdd)
        self.label_error.setObjectName(u"label_error")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_error.sizePolicy().hasHeightForWidth())
        self.label_error.setSizePolicy(sizePolicy5)

        self.horizontalLayout_2.addWidget(self.label_error)

        self.box_ok_cancel = QDialogButtonBox(EntryAdd)
        self.box_ok_cancel.setObjectName(u"box_ok_cancel")
        sizePolicy3.setHeightForWidth(self.box_ok_cancel.sizePolicy().hasHeightForWidth())
        self.box_ok_cancel.setSizePolicy(sizePolicy3)
        self.box_ok_cancel.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout_2.addWidget(self.box_ok_cancel)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.retranslateUi(EntryAdd)

        QMetaObject.connectSlotsByName(EntryAdd)
    # setupUi

    def retranslateUi(self, EntryAdd):
        EntryAdd.setWindowTitle(QCoreApplication.translate("EntryAdd", u"Add UEFI Entry", None))
        self.label.setText(QCoreApplication.translate("EntryAdd", u"Automatic selection", None))
        self.but_auto_windows.setText(QCoreApplication.translate("EntryAdd", u"Find Windows boot file", None))
        self.but_auto_linux.setText(QCoreApplication.translate("EntryAdd", u"Find Linux boot file", None))
        self.but_auto_all.setText(QCoreApplication.translate("EntryAdd", u"Find all boot files", None))
        self.label_2.setText(QCoreApplication.translate("EntryAdd", u"Manual selection", None))
        ___qtreewidgetitem = self.tree_manual_partition.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("EntryAdd", u"size", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("EntryAdd", u"type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("EntryAdd", u"name", None));

        __sortingEnabled = self.tree_manual_partition.isSortingEnabled()
        self.tree_manual_partition.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.tree_manual_partition.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("EntryAdd", u"/dev/sda", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("EntryAdd", u"400MiB", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("EntryAdd", u"fat32", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("EntryAdd", u"/deb/sda1", None));
        ___qtreewidgetitem3 = self.tree_manual_partition.topLevelItem(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("EntryAdd", u"/dev/sdb", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem3.child(0)
        ___qtreewidgetitem4.setText(2, QCoreApplication.translate("EntryAdd", u"20MiB", None));
        ___qtreewidgetitem4.setText(1, QCoreApplication.translate("EntryAdd", u"fat32", None));
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("EntryAdd", u"/dev/sdb1", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem3.child(1)
        ___qtreewidgetitem5.setText(2, QCoreApplication.translate("EntryAdd", u"500GiB", None));
        ___qtreewidgetitem5.setText(1, QCoreApplication.translate("EntryAdd", u"zfs", None));
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("EntryAdd", u"/dev/sdb2", None));
        ___qtreewidgetitem6 = self.tree_manual_partition.topLevelItem(2)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("EntryAdd", u"/dev/nvme0n1", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem6.child(0)
        ___qtreewidgetitem7.setText(2, QCoreApplication.translate("EntryAdd", u"1.87TiB", None));
        ___qtreewidgetitem7.setText(1, QCoreApplication.translate("EntryAdd", u"fat32", None));
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("EntryAdd", u"/dev/nvme0n1p1", None));
        self.tree_manual_partition.setSortingEnabled(__sortingEnabled)

        self.but_manual_file.setText(QCoreApplication.translate("EntryAdd", u"Select file manually", None))
        self.label_3.setText(QCoreApplication.translate("EntryAdd", u"Entry information", None))
        self.label_6.setText(QCoreApplication.translate("EntryAdd", u"Partition", None))
        self.edit_partition.setText(QCoreApplication.translate("EntryAdd", u"/dev/sda1", None))
        self.label_4.setText(QCoreApplication.translate("EntryAdd", u"File path", None))
        self.edit_file.setText(QCoreApplication.translate("EntryAdd", u"/EFI/grub/boot64.efi", None))
        self.label_5.setText(QCoreApplication.translate("EntryAdd", u"File size", None))
        self.edit_file_size.setText(QCoreApplication.translate("EntryAdd", u"64KiB", None))
        self.label_7.setText(QCoreApplication.translate("EntryAdd", u"Entry name", None))
        self.edit_entry_name.setText(QCoreApplication.translate("EntryAdd", u"Ubuntu GRUB", None))
        self.label_error.setText(QCoreApplication.translate("EntryAdd", u"Please select a partition", None))
    # retranslateUi

