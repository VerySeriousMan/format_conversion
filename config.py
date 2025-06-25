# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2025.06.24
Author: ZhangYuetao
File Name: config.py
Update: 2025.06.25
"""

import os
import toml

BIN_SETTING_FILE = r'settings/bin_setting.toml'
SECRET_FILE = r'settings/.secret.toml'
SOFTWARE_INFOS_FILE = r'settings/software_infos.toml'
QT_MATERIAL_THEME_FILE = r'settings/qt_material_theme.toml'

ICO_FILE = r'settings/xey.ico'

SOFTWARE_NAME = "格式转换软件"
SHARE_DIR = ""  # 你的服务器上的软件文件夹地址
PROBLEM_SHARE_DIR = ""  # 你的服务器上的问题反馈文件夹地址

# 定义默认参数值
BIN_SETTING_DEFAULT_CONFIG = {
    'width': 640,                  # int 类型，图像宽度
    'height': 480,                 # int 类型，图像高度
    'channels': 3,                 # int 类型，通道数（RGB）

    'dtype': 'uint8',              # str 类型，numpy 数据类型，如 'uint8', 'float32'

    'channel_order': 'RGB',        # str 类型，'RGB' 或 'BGR' 或 'GRAY'
    'layout': 'HWC',               # str 类型，常见为 'HWC' 或 'CHW'
    
    'endianness': 'little',        # str 类型，字节序，通常为 'little' 或 'big'
    'normalize': False,            # 是否将 float 图像归一化到 0~255 并转为 uint8

    'flip': False,                 # bool 类型，是否垂直翻转图像
    'rotate': 0                    # int 类型，旋转角度，支持 0/90/180/270
}

QT_MATERIAL_THEME_DEFAULT_CONFIG = {
    'theme': 'default',
}

def load_config(filepath, default):
    """
    加载配置文件，如果文件不存在或解析失败则使用默认配置

    :param filepath: TOML 文件路径
    :param default: 默认配置字典
    :return: 加载的配置字典
    """
    # 尝试读取现有的 TOML 文件
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                config = toml.load(f)
        else:
            config = default
    except (FileNotFoundError, toml.TomlDecodeError):
        config = default

    # 检查是否缺少必要的参数，如果缺少则更新为默认值
    for key, value in default.items():
        if key not in config:
            config[key] = value

    return config


def save_config(file_path, config_dict):
    """
    将配置字典保存到 TOML 文件中

    :param file_path: TOML 文件路径
    :param config_dict: 配置字典
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        toml.dump(config_dict, f)


def load_credentials(config_path=SECRET_FILE):
    """
    从配置文件中加载服务器连接凭证。

    :param config_path: 配置文件的路径。
    :return: 包含服务器IP、共享名称、用户名和密码的元组。
    """
    with open(config_path, 'r') as config_file:
        config_info = toml.load(config_file)
        credentials = config_info.get("credentials", {})
        return (
            credentials.get("server_ip"),
            credentials.get("share_name"),
            credentials.get("username"),
            credentials.get("password"),
        )
