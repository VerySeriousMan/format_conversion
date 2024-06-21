# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.06.14
Author: ZhangYuetao
File Name: main.py
last renew 2024.06.20
"""

import os
import sys
import toml

from convent_ware import Ui_MainWindow
from bin_settings import Ui_Dialog
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from PyQt5 import QtGui
import qt_material

from image_convert import convert_image, convert_images
from bin_to_image import bins_to_image, bins_to_images


class Worker(QThread):
    update_label = pyqtSignal(str)
    error_label = pyqtSignal(str)

    def __init__(self, file_path, save_path, process_type, target_format, nums=None):
        super().__init__()
        self.file_path = file_path
        self.save_path = save_path
        self.process_type = process_type
        self.target_format = target_format
        self.nums = nums

    def run(self):
        self.update_label.emit("格式转换进行中")
        try:
            if self.process_type == "convent_image":
                if os.path.isdir(self.file_path):
                    convert_images(self.file_path, self.save_path, self.target_format)
                else:
                    convert_image(self.file_path, self.save_path, self.target_format)
            elif self.process_type == "video_to_image":
                if os.path.isdir(self.file_path):
                    videos_to_images(self.file_path, self.save_path, self.nums, self.target_format, self.error_label)
                else:
                    video_to_images(self.file_path, self.save_path, self.nums, self.target_format, self.error_label)
            elif self.process_type == "bin_to_image":
                if os.path.isdir(self.file_path):
                    bins_to_images(self.file_path, self.save_path, self.target_format, self.error_label)
                else:
                    bins_to_image(self.file_path, self.save_path, self.target_format, self.error_label)
            self.update_label.emit("格式转换完成")
        except Exception as e:
            self.error_label.emit(f"错误: {str(e)}")


def save_settings_to_toml(width, height, channels, dtype):
    settings_path = "bin_setting.toml"
    settings = {
        'width': int(width),
        'height': int(height),
        'channels': int(channels),
        'dtype': dtype
    }
    with open(settings_path, 'w') as f:
        toml.dump(settings, f)


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


class MyClass(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyClass, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("格式转化软件V1.1")
        self.setWindowIcon(QtGui.QIcon("xey.ico"))

        self.file_path = None
        self.save_path = None
        self.process_type = None

        self.target_format_box.addItems(['jpeg', 'bmp', 'png', 'gif', 'tiff'])

        self.input_file_button.clicked.connect(self.open_file)
        self.input_dir_button.clicked.connect(self.open_dir)
        self.save_path_button.clicked.connect(self.save_file)
        self.bin_settings_button.clicked.connect(self.open_settings_dialog)
        self.submit_button.clicked.connect(self.submit)
        self.convent_image_checkBox.clicked.connect(self.click_convent_image)
        self.video_to_image_checkBox.clicked.connect(self.click_video_to_image)
        self.bin_to_image_checkBox.clicked.connect(self.click_bin_to_image)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.animation_index = 0

    def open_settings_dialog(self):
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
        self.file_path = file_path
        self.input_dir_label.clear()
        self.info_label.clear()
        self.error_label.clear()
        self.input_file_label.setText("已导入文件")

    def open_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self)
        self.file_path = dir_path
        self.input_file_label.clear()
        self.info_label.clear()
        self.error_label.clear()
        self.input_dir_label.setText("已导入文件夹")

    def save_file(self):
        save_path = QFileDialog.getExistingDirectory(self)
        self.save_path = save_path
        self.info_label.clear()
        self.error_label.clear()
        self.save_path_label.setText("已设置保存地址")

    def click_convent_image(self):
        self.info_label.clear()
        if self.convent_image_checkBox.isChecked():
            self.process_type = 'convent_image'
            self.video_to_image_checkBox.setChecked(False)
            self.bin_to_image_checkBox.setChecked(False)
        else:
            self.process_type = None

    def click_video_to_image(self):
        self.info_label.clear()
        if self.video_to_image_checkBox.isChecked():
            self.process_type = 'video_to_image'
            self.convent_image_checkBox.setChecked(False)
            self.bin_to_image_checkBox.setChecked(False)
        else:
            self.process_type = None

    def click_bin_to_image(self):
        self.info_label.clear()
        if self.bin_to_image_checkBox.isChecked():
            self.process_type = 'bin_to_image'
            self.convent_image_checkBox.setChecked(False)
            self.video_to_image_checkBox.setChecked(False)
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
    app = QApplication(sys.argv)

    from video_to_image import video_to_images, videos_to_images  # 延迟导入，解决pyqt5与opencv线程冲突问题

    myWin = MyClass()
    qt_material.apply_stylesheet(app, theme='default')
    myWin.show()
    sys.exit(app.exec_())
