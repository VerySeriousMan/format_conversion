# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.08.19
Author: ZhangYuetao
File Name: work_thread.py
Update: 2025.06.25
"""

import os

from PyQt5.QtCore import QThread, pyqtSignal

import core


class WorkingThread(QThread):
    """
    工作线程类，用于在后台执行格式转换任务，避免阻塞主线程。

    Signals:
        update_signal(pyqtSignal): 用于更新主界面中的状态标签的信号。
        error_signal (pyqtSignal): 用于在发生错误时更新主界面中的错误标签的信号。
    """

    update_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, file_path, save_path, process_type, target_format, nums=None):
        """
        初始化工作线程。

        :param file_path: 待处理文件的路径。
        :param save_path: 保存处理结果的路径。
        :param process_type: 处理类型，如 "convent_image"、"video_to_image" 等。
        :param target_format: 目标格式，如 "jpeg"、"png" 等。
        :param nums: 视频转图像时的帧率参数，默认为 None。
        """
        super().__init__()
        self.file_path = file_path
        self.save_path = save_path
        self.process_type = process_type
        self.target_format = target_format
        self.nums = nums

    def run(self):
        """
        线程执行的核心方法，根据处理类型调用相应的转换函数。
        """
        self.update_signal.emit("格式转换进行中")
        try:
            if self.process_type == "convent_image":
                # 处理图像格式转换
                if os.path.isdir(self.file_path):
                    core.convert_images(self.file_path, self.save_path, self.target_format)
                else:
                    core.convert_image(self.file_path, self.save_path, self.target_format)
            elif self.process_type == "video_to_image":
                # 处理视频转图像
                if os.path.isdir(self.file_path):
                    core.videos_to_images(self.file_path, self.save_path, self.nums, self.target_format, self.error_signal)
                else:
                    core.video_to_images(self.file_path, self.save_path, self.nums, self.target_format, self.error_signal)
            elif self.process_type == "bin_to_image":
                # 处理二进制文件转图像
                if os.path.isdir(self.file_path):
                    core.bins_to_images(self.file_path, self.save_path, self.target_format, self.error_signal)
                else:
                    core.bin_to_image(self.file_path, self.save_path, self.target_format, self.error_signal)
            elif self.process_type == "image_to_bin":
                # 处理图像转二进制文件
                if os.path.isdir(self.file_path):
                    core.images_to_bins(self.file_path, self.save_path, self.error_signal)
                else:
                    core.image_to_bin(self.file_path, self.save_path, self.error_signal)
            self.update_signal.emit("格式转换完成")
        except Exception as e:
            # 捕获异常并发送错误信息
            self.update_signal.emit("格式转换中断")
            self.error_signal.emit(f"错误: {str(e)}")
