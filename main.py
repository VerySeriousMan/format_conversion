# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.06.14
Author: ZhangYuetao
File Name: main.py
Update: 2025.06.25
"""

import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
import qt_material

import config


if __name__ == "__main__":
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 自适应适配不同分辨率
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)

    from ui.main.main_window import MainWindow  # 延迟导入，解决opencv与pyqt线程冲突问题

    window_title = "格式转换软件V1.5"
    myWin = MainWindow(window_title)
    
    qt_material_theme = config.load_config(config.QT_MATERIAL_THEME_FILE, config.QT_MATERIAL_THEME_DEFAULT_CONFIG)['theme']
    if qt_material_theme != 'default' and not qt_material_theme.endswith('.xml'):
        qt_material_theme += '.xml'
    qt_material.apply_stylesheet(app, theme=qt_material_theme)
    
    myWin.show()
    sys.exit(app.exec_())
