# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.08.19
Author: ZhangYuetao
File Name: WorkerThread.py
Update: 2024.10.30
"""

import os

from PyQt5.QtCore import QThread, pyqtSignal

from image_convert import convert_image, convert_images
from bin_to_image import bins_to_image, bins_to_images
from video_to_image import video_to_images, videos_to_images
from image_to_bin import image_to_bin, images_to_bins


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
            elif self.process_type == "image_to_bin":
                if os.path.isdir(self.file_path):
                    images_to_bins(self.file_path, self.save_path, self.error_label)
                else:
                    image_to_bin(self.file_path, self.save_path, self.error_label)
            self.update_label.emit("格式转换完成")
        except Exception as e:
            self.update_label.emit("格式转换中断")
            self.error_label.emit(f"错误: {str(e)}")
