# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2025.06.24
Author: ZhangYuetao
File Name: feedback_main.py
Update: 2025.06.25
"""

from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui

import config
from ui.feedback import Ui_Form
from network.server_connect import submit_problem_feedback


class FeedbackWindow(QWidget, Ui_Form):
    """
    问题反馈窗口类，用于用户提交问题反馈。

    Attributes:
        problem_type (str): 问题类型，默认为 'bug'。
    """

    def __init__(self, parent=None):
        """
        初始化问题反馈窗口。

        :param parent: 父窗口对象，默认为 None。
        """
        super(FeedbackWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("问题反馈")
        self.setWindowIcon(QtGui.QIcon(config.ICO_FILE))

        self.problem_type = 'bug'

        # 连接信号与槽
        self.bug_checkBox.clicked.connect(self.process_bug_checkbox)
        self.suggestion_checkBox.clicked.connect(self.process_suggestion_checkbox)
        self.submit_pushButton.clicked.connect(self.submit)
        self.write_textEdit.textChanged.connect(self.info_label.clear)
        
        self.bug_checkBox.click()

    def process_bug_checkbox(self):
        """
        处理 'bug' 复选框的点击事件，更新问题类型。
        """
        if self.bug_checkBox.isChecked():
            self.problem_type = 'bug'
            self.suggestion_checkBox.setChecked(False)
        else:
            self.problem_type = 'suggestion'
            self.suggestion_checkBox.setChecked(True)

    def process_suggestion_checkbox(self):
        """
        处理 'suggestion' 复选框的点击事件，更新问题类型。
        """
        if self.suggestion_checkBox.isChecked():
            self.problem_type = 'suggestion'
            self.bug_checkBox.setChecked(False)
        else:
            self.problem_type = 'bug'
            self.bug_checkBox.setChecked(True)

    def submit(self):
        """
        处理提交按钮的点击事件，提交用户反馈。
        """
        submit_words = self.write_textEdit.toPlainText()
        if not submit_words:
            self.info_label.setText('提交内容不能为空')
            return
        try:
            submit_problem_feedback(submit_words, self.problem_type)
            self.info_label.setText('反馈成功！')
        except Exception as e:
            self.info_label.setText(str(e))

    def closeEvent(self, event):
        """
        在窗口关闭事件发生时执行的操作。

        :param event: 关闭事件对象。
        """
        event.accept()  # 接受关闭事件，允许窗口关闭
