# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.08.19
Author: ZhangYuetao
File Name: BinSetting.py
Update: 2024.08.19
"""

from bin_settings import Ui_Dialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui


class SettingsDialog(QDialog, Ui_Dialog):
    settings_accepted = pyqtSignal(str, str, str, str)

    def __init__(self, width, height, channels, dtype, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("bin文件参数设置")
        self.setWindowIcon(QtGui.QIcon("xey.ico"))

        self.width_lineEdit.setText(str(width))
        self.heigth_lineEdit.setText(str(height))
        self.channels_lineEdit.setText(str(channels))
        self.dtype_lineEdit.setText(dtype)

        self.buttonBox.accepted.connect(self.accept_settings)

    def accept_settings(self):
        width_value = self.width_lineEdit.text()
        height_value = self.heigth_lineEdit.text()
        channels_value = self.channels_lineEdit.text()
        dtype_value = self.dtype_lineEdit.text()
        self.settings_accepted.emit(width_value, height_value, channels_value, dtype_value)
        self.accept()
