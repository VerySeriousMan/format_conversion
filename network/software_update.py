# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2025.06.24
Author: ZhangYuetao
File Name: software_update.py
Update: 2025.06.24
"""

import os
import shutil
import subprocess
import sys
import time

from PyQt5.QtWidgets import QMessageBox

import config
from network import server_connect


class Updater:
    """
        软件更新类，处理软件自动与手动更新。

        Attributes:
            current_software_path (str): 当前软件的可执行文件路径。
            current_software_version (str): 当前软件的版本号。
        """
    def __init__(self, current_software_path, current_software_version):
        self.current_software_path = current_software_path
        self.current_software_version = current_software_version

    def init_update(self):
        """
        初始化更新操作，检查是否需要更新软件。
        """
        dir_path = os.path.dirname(self.current_software_path)
        dir_name = os.path.basename(dir_path)
        if dir_name == 'temp':
            old_dir_path = os.path.dirname(dir_path)
            for file in os.listdir(old_dir_path):
                if file.endswith('.exe'):
                    old_software = os.path.join(old_dir_path, file)
                    os.remove(old_software)
            shutil.copy2(self.current_software_path, old_dir_path)
            new_file_path = os.path.join(old_dir_path, os.path.basename(self.current_software_path))
            if os.path.exists(new_file_path) and server_connect.is_file_complete(new_file_path):
                msg_box = QMessageBox()  # 创建一个新的 QMessageBox 对象
                reply = msg_box.question(None, '更新完成', '软件更新完成，需要立即重启吗？',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                msg_box.raise_()  # 确保弹窗显示在最上层

                if reply == QMessageBox.Yes:
                    subprocess.Popen(new_file_path)
                    time.sleep(1)
                    sys.exit("程序已退出")
                else:
                    sys.exit("程序已退出")
        else:
            is_updated = 0
            for file in os.listdir(dir_path):
                if file == 'temp':
                    is_updated = 1
                    shutil.rmtree(file)
            if is_updated == 1:
                try:
                    text = server_connect.get_update_log(config.SOFTWARE_NAME)
                    QMessageBox.information(None, '更新成功', f'更新成功！\n{text}')
                except Exception as e:
                    QMessageBox.critical(None, '更新成功', f'日志加载失败: {str(e)}')

    def auto_update(self):
        """
        自动检查并更新软件。
        """
        dir_path = os.path.dirname(self.current_software_path)
        dir_name = os.path.basename(dir_path)
        if dir_name != 'temp':
            if server_connect.check_version(self.current_software_version) == 1:
                self.update_software()

    def update_software(self):
        """
        更新软件到最新版本。
        """
        update_way = server_connect.check_version(self.current_software_version)
        if update_way == -1:
            # 网络未连接，弹出提示框
            QMessageBox.warning(None, '更新提示', '网络未连接，暂时无法更新')
        elif update_way == 0:
            # 当前已为最新版本，弹出提示框
            QMessageBox.information(None, '更新提示', '当前已为最新版本')
        else:
            # 弹出提示框，询问是否立即更新
            msg_box = QMessageBox()  # 创建一个新的 QMessageBox 对象
            reply = msg_box.question(None, '更新提示', '发现新版本，开始更新吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            msg_box.raise_()  # 确保弹窗显示在最上层

            if reply == QMessageBox.Yes:
                try:
                    server_connect.update_software(os.path.dirname(self.current_software_path), config.SOFTWARE_NAME)
                    text = server_connect.get_update_log(config.SOFTWARE_NAME)
                    QMessageBox.information(None, '更新成功', f'更新成功！\n{text}')
                except Exception as e:
                    QMessageBox.critical(None, '更新失败', f'更新失败: {str(e)}')
            else:
                pass
