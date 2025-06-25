# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.08.19
Author: ZhangYuetao
File Name: BinSetting.py
Update: 2025.06.25
"""

from ui.bin_settings import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui

import config


class SettingsDialog(QDialog, Ui_Dialog):
    """
    二进制文件参数设置对话框类，用于设置二进制文件的参数。
    
    Attributes:
        config (dict): 二进制文件的配置数据，包括宽度、高度、通道数和数据类型等数据。
    """

    def __init__(self, parent=None):
        """
        初始化二进制文件参数设置对话框。
        """
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("bin文件参数设置")
        self.setWindowIcon(QtGui.QIcon(config.ICO_FILE))
        
        self.config = config.load_config(config.BIN_SETTING_FILE, config.BIN_SETTING_DEFAULT_CONFIG)

        # 连接按钮的点击事件到 accept_settings 方法
        self.buttonBox.accepted.connect(self.accept_settings)
        
        # 初始化对话框中的输入框，显示传入的参数值
        self.setup_settings()
        
    def setup_settings(self):
        """
        初始化对话框中的输入框，显示传入的参数值。
        """
        self.width_lineEdit.setText(str(self.config['width']))
        self.heigth_lineEdit.setText(str(self.config['height']))
        self.channels_lineEdit.setText(str(self.config['channels']))
        self.dtype_lineEdit.setText(self.config['dtype'])
        self.channel_order_lineEdit.setText(self.config['channel_order'])
        self.layout_lineEdit.setText(self.config['layout'])
        self.endianness_lineEdit.setText(self.config['endianness'])
        self.normalize_checkBox.setChecked(self.config['normalize'])
        self.flip_checkBox.setChecked(self.config['flip'])
        self.rotate_lineEdit.setText(str(self.config['rotate']))
        
    def save_settings_to_toml(self):
        """
        将用户修改的配置保存到 TOML 文件中。

        从界面控件中获取用户修改的值，更新配置字典，并保存到 TOML 文件。
        """
        # 更新配置字典
        self.config['width'] = int(self.width_lineEdit.text())
        self.config['height'] = int(self.heigth_lineEdit.text())
        self.config['channels'] = int(self.channels_lineEdit.text())
        self.config['dtype'] = self.dtype_lineEdit.text()
        self.config['channel_order'] = self.channel_order_lineEdit.text()
        self.config['layout'] = self.layout_lineEdit.text()
        self.config['endianness'] = self.endianness_lineEdit.text()
        self.config['normalize'] = self.normalize_checkBox.isChecked()
        self.config['flip'] = self.flip_checkBox.isChecked()
        self.config['rotate'] = int(self.rotate_lineEdit.text())

        # 保存到 TOML 文件
        config.save_config(config.BIN_SETTING_FILE, self.config)

    def accept_settings(self):
        """
        保存用户修改的配置并关闭对话框。

        调用 `save_settings_to_toml` 方法保存配置，然后关闭对话框。
        """
        self.save_settings_to_toml()  # 保存配置
        self.accept()  # 关闭对话框
