# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.06.14
Author: ZhangYuetao
File Name: main.py
last renew 2024.06.18
"""

import os
import sys
from convent_ware import Ui_MainWindow
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtGui
import qt_material

from image_convert import convert_image, convert_images
from bin_to_image import bins_to_image, bins_to_images


class Worker(QThread):
    update_label = pyqtSignal(str)

    def __init__(self, file_path, save_path, process_type, target_format, nums=None):
        super().__init__()
        self.file_path = file_path
        self.save_path = save_path
        self.process_type = process_type
        self.target_format = target_format
        self.nums = nums

    def run(self):
        self.update_label.emit("格式转换进行中")
        if self.process_type == "图片格式转化":
            if os.path.isdir(self.file_path):
                convert_images(self.file_path, self.save_path, self.target_format)
            else:
                convert_image(self.file_path, self.save_path, self.target_format)
        elif self.process_type == "视频抽帧":
            if os.path.isdir(self.file_path):
                videos_to_images(self.file_path, self.save_path, self.nums, self.target_format)
            else:
                video_to_images(self.file_path, self.save_path, self.nums, self.target_format)
        elif self.process_type == "bin文件转图像":
            if os.path.isdir(self.file_path):
                bins_to_images(self.file_path, self.save_path, self.target_format)
            else:
                bins_to_image(self.file_path, self.save_path, self.target_format)
        self.update_label.emit("格式转换完成")


class MyClass(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyClass, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("格式转化软件V1.0")
        self.setWindowIcon(QtGui.QIcon("xey.ico"))

        self.file_path = None
        self.save_path = None

        self.process_type_box.addItems(["图片格式转化", "视频抽帧", "bin文件转图像"])
        self.target_format_box.addItems(['jpeg', 'bmp', 'png', 'gif', 'tiff'])

        self.input_file_button.clicked.connect(self.open_file)
        self.input_dir_button.clicked.connect(self.open_dir)
        self.save_path_button.clicked.connect(self.save_file)
        self.submit_button.clicked.connect(self.submit)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.animation_index = 0

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self)[0]
        self.file_path = file_path
        self.input_dir_label.clear()
        self.input_file_label.setText("已导入文件")

    def open_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self)
        self.file_path = dir_path
        self.input_file_label.clear()
        self.input_dir_label.setText("已导入文件夹")

    def save_file(self):
        save_path = QFileDialog.getExistingDirectory(self)
        self.save_path = save_path
        self.save_path_label.setText("已设置保存地址")

    def submit(self):
        target_format = self.target_format_box.currentText()
        nums = None
        if self.file_path is not None and self.save_path is not None:
            if self.process_type_box.currentText() == "视频抽帧":
                nums = float(self.nums_doubleSpinBox.text())
            self.worker = Worker(self.file_path, self.save_path, self.process_type_box.currentText(), target_format, nums)
            self.worker.update_label.connect(self.update_info_label)
            self.worker.finished.connect(self.stop_animation)
            self.worker.start()
            self.start_animation()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    from video_to_image import video_to_images, videos_to_images  # 延迟导入，解决pyqt5与opencv线程冲突问题

    myWin = MyClass()
    qt_material.apply_stylesheet(app, theme='default')
    myWin.show()
    sys.exit(app.exec_())
