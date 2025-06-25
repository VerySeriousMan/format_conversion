# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2025.06.24
Author: ZhangYuetao
File Name: main_window.py
Update: 2025.06.25
"""

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5 import QtGui

import config
import utils
from ui.convent_ware import Ui_MainWindow
from ui.main.bin_setting_main import SettingsDialog
from ui.main.feedback_main import FeedbackWindow
from threads.work_thread import WorkingThread
from network.software_update import Updater
from network import server_connect

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    格式转换软件的主窗口类，用于处理图像、视频和二进制文件的格式转换。

    Attributes:
        file_path (str): 待处理文件的路径。
        save_path (str): 保存处理结果的路径。
        process_type (str): 当前选择的处理类型。
        feedback_window (FeedbackWindow): 问题反馈窗口对象。
        current_software_path (str): 当前软件的路径。
        current_software_version (str): 当前软件的版本号。
        updater(Updater): 自动更新类。
        timer (QTimer): 用于动画效果的定时器。
        animation_index (int): 动画索引，用于显示动态效果。
        working_thread (WorkingThread): 工作线程对象。
    """

    def __init__(self, window_title, parent=None):
        """
        初始化主窗口。

        :param window_title: 窗口标题，由外部传入。
        :param parent: 父窗口对象，默认为 None。
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(window_title)  # 使用传入的标题
        self.setWindowIcon(QtGui.QIcon(config.ICO_FILE))
        
        self.file_path = None
        self.save_path = None
        self.process_type = None
        self.feedback_window = None
        self.current_software_path = utils.get_current_software_path()
        self.current_software_version = server_connect.get_current_software_version(self.current_software_path)
        
        self.updater = Updater(self.current_software_path, self.current_software_version)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.animation_index = 0
        self.working_thread = None

        self.input_file_button.clicked.connect(self.open_file)
        self.input_dir_button.clicked.connect(self.open_dir)
        self.save_path_button.clicked.connect(self.save_file)
        self.bin_settings_button.clicked.connect(self.open_settings_dialog)
        self.submit_button.clicked.connect(self.submit)
        self.convent_image_checkBox.clicked.connect(self.click_convent_image)
        self.video_to_image_checkBox.clicked.connect(self.click_video_to_image)
        self.bin_to_image_checkBox.clicked.connect(self.click_bin_to_image)
        self.image_to_bin_checkBox.clicked.connect(self.click_image_to_bin)
        self.software_update_action.triggered.connect(self.updater.update_software)
        self.problem_feedback_action.triggered.connect(self.feedback_problem)
        
        self.updater.auto_update()
        self.updater.init_update()

        self.target_format_box.addItems(['jpeg', 'bmp', 'png', 'tiff'])
        
        self.init_input()

    def init_input(self):
        """
        初始化输入控件，禁用部分控件并设置初始文本。
        """
        self.control_enabled(False)
        self.target_format_box.setEnabled(False)
        self.target_format_label.setEnabled(False)
        self.nums_doubleSpinBox.setEnabled(False)
        self.nums_label.setEnabled(False)
        self.bin_settings_button.setEnabled(False)
        self.input_file_label.setText('请先导入待处理文件(夹)')

    def init_save_path(self):
        """
        初始化保存路径控件，清空输入文件标签并启用保存路径按钮。
        """
        self.input_file_label.clear()
        self.save_path_button.setEnabled(True)
        self.save_path_label.setText('请设置保存地址')

    def control_enabled(self, enable):
        """
        控制部分控件的启用状态。

        :param enable: 是否启用控件，True 为启用，False 为禁用。
        """
        self.save_path_button.setEnabled(enable)
        self.convent_image_checkBox.setEnabled(enable)
        self.video_to_image_checkBox.setEnabled(enable)
        self.bin_to_image_checkBox.setEnabled(enable)
        self.image_to_bin_checkBox.setEnabled(enable)
        self.submit_button.setEnabled(enable)
    
    def feedback_problem(self):
        """
        处理问题反馈操作，检查网络连接并打开反馈窗口。
        """
        if server_connect.check_version(self.current_software_version) == -1:
            QMessageBox.warning(self, '网络未连接', '网络未连接，请连接内网后再试')
        else:
            self.open_feedback_window()

    def open_settings_dialog(self):
        """
        打开二进制文件设置对话框。
        """
        self.info_label.clear()

        dialog = SettingsDialog(self)
        dialog.exec_()

    def open_file(self):
        """
        打开文件选择对话框，选择待处理的文件。
        """
        file_path = QFileDialog.getOpenFileName(self)[0]
        if file_path:
            self.file_path = file_path
            self.input_dir_label.clear()
            self.info_label.clear()
            self.error_label.clear()
            self.init_save_path()
            self.input_file_label.setText("已导入文件")

    def open_dir(self):
        """
        打开文件夹选择对话框，选择待处理的文件夹。
        """
        dir_path = QFileDialog.getExistingDirectory(self)
        if dir_path:
            self.file_path = dir_path
            self.input_file_label.clear()
            self.info_label.clear()
            self.error_label.clear()
            self.init_save_path()
            self.input_dir_label.setText("已导入文件夹")

    def save_file(self):
        """
        打开文件夹选择对话框，选择保存结果的路径。
        """
        save_path = QFileDialog.getExistingDirectory(self)
        if save_path:
            self.save_path = save_path
            self.info_label.clear()
            self.error_label.clear()
            self.control_enabled(True)
            self.save_path_label.setText("已设置保存地址")

    def click_convent_image(self):
        """
        处理图像格式转换复选框的点击事件。
        """
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
        """
        处理视频转图像复选框的点击事件。
        """
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
        """
        处理二进制文件转图像复选框的点击事件。
        """
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
        """
        处理图像转二进制文件复选框的点击事件。
        """
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
        """
        提交处理任务与工作线程，根据选择的处理类型执行相应的操作。
        """
        self.info_label.clear()
        self.error_label.clear()
        target_format = self.target_format_box.currentText()
        nums = None
        if self.file_path is not None and self.save_path is not None and self.process_type is not None:
            self.control_enabled(False)
            if self.process_type == "video_to_image":
                nums = float(self.nums_doubleSpinBox.text())
            self.worker = WorkingThread(self.file_path, self.save_path, self.process_type, target_format, nums)
            self.worker.update_signal.connect(self.update_info_label)
            self.worker.error_signal.connect(self.update_error_label)
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
        """
        启动处理动画。
        """
        self.animation_index = 0
        self.timer.start(500)

    def stop_animation(self):
        """
        停止处理动画。
        """
        self.timer.stop()
        self.control_enabled(True)

    def update_animation(self):
        """
        更新处理动画的文本。
        """
        animation_texts = ["格式转换进行中", "格式转换进行中.", "格式转换进行中..", "格式转换进行中..."]
        self.info_label.setText(animation_texts[self.animation_index])
        self.animation_index = (self.animation_index + 1) % len(animation_texts)

    def update_info_label(self, text):
        """
        更新信息标签的文本。

        :param text: 要显示的文本。
        """
        self.info_label.setText(text)

    def update_error_label(self, text):
        """
        更新错误标签的文本。

        :param text: 要显示的文本。
        """
        self.error_label.setText(text)
        
    def open_feedback_window(self):
        """
        打开问题反馈窗口。
        """
        self.feedback_window = FeedbackWindow()
        self.feedback_window.show()
        
    def closeEvent(self, event):
        """
        处理窗口关闭事件，确保所有资源被释放。

        :param event: 关闭事件对象。
        """
        if self.working_thread and self.working_thread.isRunning():
            self.working_thread.terminate()  # 终止线程
            self.working_thread.wait()  # 等待线程完全结束
        self.working_thread = None  # 置为 None

        if self.feedback_window:
            self.feedback_window.close()
        event.accept()
