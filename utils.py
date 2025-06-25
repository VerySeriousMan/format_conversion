# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.08.19
Author: ZhangYuetao
File Name: utils.py
Update: 2025.06.25
"""

import os
import sys
import time


def is_file_complete(file_path, timeout=60):
    """
    检查文件是否完全复制完成。

    :param file_path: 文件路径。
    :param timeout: 最大等待时间（秒）。
    :return: 如果文件复制完成则返回 True，否则返回 False。
    """
    if not os.path.exists(file_path):
        return False

    initial_size = os.path.getsize(file_path)
    time.sleep(1)  # 等待1秒钟，给文件写入一些时间
    final_size = os.path.getsize(file_path)

    # 如果文件大小没有变化，认为文件已复制完成
    if initial_size == final_size:
        return True

    # 如果文件大小仍在变化，则继续等待
    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(1)
        new_size = os.path.getsize(file_path)
        if new_size == final_size:
            return True
        final_size = new_size

    # 超过最大等待时间后认为文件未复制完成
    return False


def get_current_software_path():
    """
    获取当前软件的可执行文件路径。

    :return: 当前软件的可执行文件路径。
    """
    # 检查是否是打包后的程序
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后的路径
        return os.path.abspath(sys.argv[0])
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
