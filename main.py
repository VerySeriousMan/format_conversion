# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.06.14
Author: ZhangYuetao
File Name: main.py
Update: 2024.10.30
"""

import sys
import toml

from convent_ware import Ui_MainWindow
from BinSetting import SettingsDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtGui, QtCore
from utils import save_settings_to_toml
import qt_material


class MyClass(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyClass, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("格式转化软件V1.3")
        self.setWindowIcon(QtGui.QIcon("xey.ico"))

        self.file_path = None
        self.save_path = None
        self.process_type = None

        self.target_format_box.addItems(['jpeg', 'bmp', 'png', 'tiff'])

        self.input_file_button.clicked.connect(self.open_file)
        self.input_dir_button.clicked.connect(self.open_dir)
        self.save_path_button.clicked.connect(self.save_file)
        self.bin_settings_button.clicked.connect(self.open_settings_dialog)
        self.submit_button.clicked.connect(self.submit)
        self.convent_image_checkBox.clicked.connect(self.click_convent_image)
        self.video_to_image_checkBox.clicked.connect(self.click_video_to_image)
        self.bin_to_image_checkBox.clicked.connect(self.click_bin_to_image)
        self.image_to_bin_checkBox.clicked.connect(self.click_image_to_bin)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.animation_index = 0
        self.init_input()

    def init_input(self):
        self.control_enabled(False)
        self.input_file_label.setText('请先导入待处理文件(夹)')

    def init_save_path(self):
        self.input_file_label.clear()
        self.save_path_button.setEnabled(True)
        self.save_path_label.setText('请设置保存地址')

    def control_enabled(self, enable):
        self.save_path_button.setEnabled(enable)
        self.target_format_box.setEnabled(enable)
        self.target_format_label.setEnabled(enable)
        self.nums_doubleSpinBox.setEnabled(enable)
        self.nums_label.setEnabled(enable)
        self.bin_settings_button.setEnabled(enable)
        self.convent_image_checkBox.setEnabled(enable)
        self.video_to_image_checkBox.setEnabled(enable)
        self.bin_to_image_checkBox.setEnabled(enable)
        self.image_to_bin_checkBox.setEnabled(enable)
        self.submit_button.setEnabled(enable)

    def open_settings_dialog(self):
        self.info_label.clear()
        settings_path = "bin_setting.toml"

        with open(settings_path, 'r') as f:
            settings = toml.load(f)

        width = settings['width']
        height = settings['height']
        channels = settings['channels']
        dtype = settings['dtype']

        dialog = SettingsDialog(width, height, channels, dtype, self)
        dialog.settings_accepted.connect(self.update_settings)
        dialog.exec_()

    def update_settings(self, width, height, channels, dtype):
        save_settings_to_toml(width, height, channels, dtype)
        self.info_label.setText("设置已更新")

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self)[0]
        if file_path:
            self.file_path = file_path
            self.input_dir_label.clear()
            self.info_label.clear()
            self.error_label.clear()
            self.init_save_path()
            self.input_file_label.setText("已导入文件")

    def open_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self)
        if dir_path:
            self.file_path = dir_path
            self.input_file_label.clear()
            self.info_label.clear()
            self.error_label.clear()
            self.init_save_path()
            self.input_dir_label.setText("已导入文件夹")

    def save_file(self):
        save_path = QFileDialog.getExistingDirectory(self)
        if save_path:
            self.save_path = save_path
            self.info_label.clear()
            self.error_label.clear()
            self.control_enabled(True)
            self.save_path_label.setText("已设置保存地址")

    def click_convent_image(self):
        self.info_label.clear()
        if self.convent_image_checkBox.isChecked():
            self.process_type = 'convent_image'
            self.video_to_image_checkBox.setChecked(False)
            self.bin_to_image_checkBox.setChecked(False)
            self.image_to_bin_checkBox.setChecked(False)
            self.bin_settings_button.setEnabled(False)
            self.nums_label.setEnabled(False)
            self.nums_doubleSpinBox.setEnabled(False)
            self.target_format_label.setEnabled(True)
            self.target_format_box.setEnabled(True)
        else:
            self.process_type = None

    def click_video_to_image(self):
        self.info_label.clear()
        if self.video_to_image_checkBox.isChecked():
            self.process_type = 'video_to_image'
            self.convent_image_checkBox.setChecked(False)
            self.bin_to_image_checkBox.setChecked(False)
            self.image_to_bin_checkBox.setChecked(False)
            self.bin_settings_button.setEnabled(False)
            self.nums_label.setEnabled(True)
            self.nums_doubleSpinBox.setEnabled(True)
            self.target_format_label.setEnabled(True)
            self.target_format_box.setEnabled(True)
        else:
            self.process_type = None

    def click_bin_to_image(self):
        self.info_label.clear()
        if self.bin_to_image_checkBox.isChecked():
            self.process_type = 'bin_to_image'
            self.convent_image_checkBox.setChecked(False)
            self.video_to_image_checkBox.setChecked(False)
            self.image_to_bin_checkBox.setChecked(False)
            self.bin_settings_button.setEnabled(True)
            self.nums_label.setEnabled(False)
            self.nums_doubleSpinBox.setEnabled(False)
            self.target_format_label.setEnabled(True)
            self.target_format_box.setEnabled(True)
        else:
            self.process_type = None

    def click_image_to_bin(self):
        self.info_label.clear()
        if self.image_to_bin_checkBox.isChecked():
            self.process_type = 'image_to_bin'
            self.convent_image_checkBox.setChecked(False)
            self.video_to_image_checkBox.setChecked(False)
            self.bin_to_image_checkBox.setChecked(False)
            self.bin_settings_button.setEnabled(False)
            self.nums_label.setEnabled(False)
            self.nums_doubleSpinBox.setEnabled(False)
            self.target_format_label.setEnabled(False)
            self.target_format_box.setEnabled(False)
        else:
            self.process_type = None

    def submit(self):
        self.info_label.clear()
        self.error_label.clear()
        target_format = self.target_format_box.currentText()
        nums = None
        if self.file_path is not None and self.save_path is not None and self.process_type is not None:
            if self.process_type == "video_to_image":
                nums = float(self.nums_doubleSpinBox.text())
            self.worker = Worker(self.file_path, self.save_path, self.process_type,  target_format, nums)
            self.worker.update_label.connect(self.update_info_label)
            self.worker.error_label.connect(self.update_error_label)
            self.worker.finished.connect(self.stop_animation)
            self.worker.start()
            self.start_animation()
        elif self.file_path is None:
            self.info_label.setText("未导入文件")
        elif self.save_path is None:
            self.info_label.setText("未设置保存地址")
        elif self.process_type is None:
            self.info_label.setText("未选择转换选项")

    def start_animation(self):
        self.animation_index = 0
        self.timer.start(500)

    def stop_animation(self):
        self.timer.stop()

    def update_animation(self):
        animation_texts = ["格式转换进行中", "格式转换进行中.", "格式转换进行中..", "格式转换进行中..."]
        self.info_label.setText(animation_texts[self.animation_index])
        self.animation_index = (self.animation_index + 1) % len(animation_texts)

    def update_info_label(self, text):
        self.info_label.setText(text)

    def update_error_label(self, text):
        self.error_label.setText(text)


if __name__ == "__main__":
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 自适应适配不同分辨率
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)

    from WorkerThread import Worker  # 延迟导入，解决pyqt5与opencv线程冲突问题

    myWin = MyClass()
    qt_material.apply_stylesheet(app, theme='default')
    myWin.show()
    sys.exit(app.exec_())
