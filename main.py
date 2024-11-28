# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.06.14
Author: ZhangYuetao
File Name: main.py
Update: 2024.11.28
"""
import os.path
import shutil
import subprocess
import sys
import time
import toml

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import QtGui, QtCore
import qt_material

from convent_ware import Ui_MainWindow
from BinSetting import SettingsDialog
from utils import save_settings_to_toml
import server_connect


class MyClass(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyClass, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("格式转化软件V1.4.1")
        self.setWindowIcon(QtGui.QIcon("xey.ico"))

        self.file_path = None
        self.save_path = None
        self.process_type = None
        self.current_software_path = self.get_file_path()
        self.current_software_version = server_connect.get_current_software_version(self.current_software_path)

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
        self.software_update_action.triggered.connect(self.update_software)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.animation_index = 0
        self.init_input()

        # # 延迟调用 auto_update
        # QTimer.singleShot(0, self.auto_update)
        self.auto_update()
        self.init_update()

    def init_update(self):
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
                msg_box = QMessageBox(self)  # 创建一个新的 QMessageBox 对象
                reply = msg_box.question(self, '更新完成', '软件更新完成，需要立即重启吗？',
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
                    text = server_connect.get_update_log('格式转换软件')
                    QMessageBox.information(self, '更新成功', f'更新成功！\n{text}')
                except Exception as e:
                    QMessageBox.critical(self, '更新成功', f'日志加载失败: {str(e)}')

    def init_input(self):
        self.control_enabled(False)
        self.target_format_box.setEnabled(False)
        self.target_format_label.setEnabled(False)
        self.nums_doubleSpinBox.setEnabled(False)
        self.nums_label.setEnabled(False)
        self.bin_settings_button.setEnabled(False)
        self.input_file_label.setText('请先导入待处理文件(夹)')

    def init_save_path(self):
        self.input_file_label.clear()
        self.save_path_button.setEnabled(True)
        self.save_path_label.setText('请设置保存地址')

    def control_enabled(self, enable):
        self.save_path_button.setEnabled(enable)
        self.convent_image_checkBox.setEnabled(enable)
        self.video_to_image_checkBox.setEnabled(enable)
        self.bin_to_image_checkBox.setEnabled(enable)
        self.image_to_bin_checkBox.setEnabled(enable)
        self.submit_button.setEnabled(enable)

    @staticmethod
    def get_file_path():
        # 检查是否是打包后的程序
        if getattr(sys, 'frozen', False):
            # PyInstaller 打包后的路径
            current_path = os.path.abspath(sys.argv[0])
        else:
            # 非打包情况下的路径
            current_path = os.path.abspath(__file__)
        return current_path

    def auto_update(self):
        dir_path = os.path.dirname(self.current_software_path)
        dir_name = os.path.basename(dir_path)
        if dir_name != 'temp':
            if server_connect.check_version(self.current_software_version) == 1:
                self.update_software()

    def update_software(self):
        update_way = server_connect.check_version(self.current_software_version)
        if update_way == -1:
            # 网络未连接，弹出提示框
            QMessageBox.warning(self, '更新提示', '网络未连接，暂时无法更新')
        elif update_way == 0:
            # 当前已为最新版本，弹出提示框
            QMessageBox.information(self, '更新提示', '当前已为最新版本')
        else:
            # 弹出提示框，询问是否立即更新
            msg_box = QMessageBox(self)  # 创建一个新的 QMessageBox 对象
            reply = msg_box.question(self, '更新提示', '发现新版本，开始更新吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            msg_box.raise_()  # 确保弹窗显示在最上层

            if reply == QMessageBox.Yes:
                try:
                    server_connect.update_software(os.path.dirname(self.current_software_path), '格式转换软件')
                    text = server_connect.get_update_log('格式转换软件')
                    QMessageBox.information(self, '更新成功', f'更新成功！\n{text}')
                except Exception as e:
                    QMessageBox.critical(self, '更新失败', f'更新失败: {str(e)}')
            else:
                pass

    def open_settings_dialog(self):
        self.info_label.clear()
        settings_path = r"settings/bin_setting.toml"

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
            self.control_enabled(False)
            if self.process_type == "video_to_image":
                nums = float(self.nums_doubleSpinBox.text())
            self.worker = Worker(self.file_path, self.save_path, self.process_type, target_format, nums)
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
        self.control_enabled(True)

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
