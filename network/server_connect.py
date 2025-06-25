# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.11.14
Author: ZhangYuetao
File Name: server_connect.py
Update: 2025.06.24
"""

import os
import subprocess
import sys
import time
import shutil

import smbclient
import toml

from utils import is_file_complete
import config


def get_current_software_version(current_software_path):
    """
    获取当前软件的版本信息。

    :param current_software_path: 当前软件的可执行文件路径。
    :return: 当前软件的版本号，如果无法获取则返回 '未知'。
     """
    file_dir = os.path.dirname(current_software_path)
    file_path = os.path.join(file_dir, config.SOFTWARE_INFOS_FILE)

    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            file_content = f.read()  # 读取文件内容

        # 解析 TOML 文件
        toml_data = toml.loads(file_content)

        # 提取 version 信息
        version = toml_data.get("version", "未知")
        return version
    except:
        return '未知'


def get_update_log(software_name):
    """
    从服务器获取指定软件的更新日志。

    :param software_name: 软件的名称。
    :return: 更新日志的内容。
    :raises ValueError: 如果读取文件出错。
    """
    # 从 .secret.toml 中加载配置信息
    server_ip, share_name, username, password = config.load_credentials()

    # 注册会话
    smbclient.register_session(server_ip, username=username, password=password)

    # 构建共享路径
    share_path = f"\\\\{server_ip}\\{share_name}"

    file_dir = os.path.join(share_path, config.SHARE_DIR)

    # 读取文件内容
    try:
        txt_path = None
        files = smbclient.listdir(file_dir)
        for dir_name in files:
            if software_name in dir_name and 'linux' not in dir_name:
                software_dir = os.path.join(file_dir, dir_name)
                txt_path = os.path.join(software_dir, 'update_log.txt')
                break

        if not txt_path:
            raise FileNotFoundError("未找到txt对应文件")

        with smbclient.open_file(txt_path, mode='r', encoding='utf-8') as file:
            txt_content = file.read()

        return txt_content

    except Exception as e:
        raise ValueError(f"读取文件出错: {e}")


def get_new_software_version(software_name):
    """
    从服务器获取指定软件的最新版本号。

    :param software_name: 软件的名称。
    :return: 最新版本号。
    :raises ValueError: 如果读取文件出错。
    """
    # 从 .secret.toml 中加载配置信息
    server_ip, share_name, username, password = config.load_credentials()

    # 注册会话
    smbclient.register_session(server_ip, username=username, password=password)

    # 构建共享路径
    share_path = f"\\\\{server_ip}\\{share_name}"

    file_dir = os.path.join(share_path, config.SHARE_DIR)

    # 读取文件内容
    try:
        toml_path = None
        files = smbclient.listdir(file_dir)
        for dir_name in files:
            if software_name in dir_name and 'linux' not in dir_name:
                software_dir = os.path.join(file_dir, dir_name)
                toml_path = os.path.join(software_dir, config.SOFTWARE_INFOS_FILE)
                break

        if not toml_path:
            raise FileNotFoundError("未找到对应文件")

        with smbclient.open_file(toml_path, mode='r', encoding='utf-8') as file:
            toml_content = file.read()

        # 解析 TOML 文件
        toml_data = toml.loads(toml_content)

        # 提取 version 信息
        version = toml_data.get("version", "未找到 version 信息")
        return version
    except Exception as e:
        raise ValueError(f"读取文件出错: {e}")


def update_software(software_dir, software_name):
    """
    从服务器更新指定软件。

    :param software_dir: 当前软件的目录。
    :param software_name: 软件的名称。
    :raises ValueError: 如果更新过程中出错。
    """
    server_ip, share_name, username, password = config.load_credentials()

    # 注册会话
    smbclient.register_session(server_ip, username=username, password=password)

    # 构建共享路径
    share_path = f"\\\\{server_ip}\\{share_name}"

    file_dir = os.path.join(share_path, config.SHARE_DIR)

    # 读取文件内容
    try:
        files = smbclient.listdir(file_dir)
        update_software_dir = None
        for dir_name in files:
            if software_name in dir_name and 'linux' not in dir_name:
                update_software_dir = os.path.join(file_dir, dir_name)
                break

        if not update_software_dir:
            raise FileNotFoundError("未找到对应软件")

        new_software_path = None

        for root, _, files in smbclient.walk(update_software_dir):
            files = [f for f in files if not f.startswith('.')]  # 排除隐藏文件
            for file in files:
                if file.endswith('.exe'):
                    new_software_path = os.path.join(root, file)
                    temp_dir = os.path.join(software_dir, 'temp')
                    os.makedirs(temp_dir, exist_ok=True)
                    shutil.copy2(new_software_path, temp_dir)
                    new_software_path = os.path.join(temp_dir, file)
                else:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(software_dir, os.path.relpath(src_file, update_software_dir))
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copy2(src_file, dst_file)

        if new_software_path and is_file_complete(new_software_path):
            subprocess.Popen(new_software_path)
            time.sleep(1)
            sys.exit("程序已退出")

    except Exception as e:
        raise ValueError(f"读取文件出错: {e}")


def check_version(current_version):
    """
    检查当前版本是否与服务器上的最新版本一致。

    :param current_version: 当前软件的版本号。
    :return: 1 表示有新版本，0 表示版本一致，-1 表示无法获取最新版本。
    """
    try:
        new_version = get_new_software_version(config.SOFTWARE_NAME)
    except:
        new_version = '未知'

    if new_version != '未知':
        if current_version != new_version:
            return 1
        else:
            return 0
    else:
        return -1


def submit_problem_feedback(feedback_words, problem_type):
    """
    提交问题反馈到服务器。

    :param feedback_words: 反馈内容。
    :param problem_type: 问题类型。
    :raises ValueError: 如果写入文件出错。
    """
    # 从 .secret.toml 中加载配置信息
    server_ip, share_name, username, password = config.load_credentials()

    # 注册会话
    smbclient.register_session(server_ip, username=username, password=password)

    # 构建共享路径
    share_path = f"\\\\{server_ip}\\{share_name}"

    problem_share_dir = config.PROBLEM_SHARE_DIR
    file_dir = os.path.join(share_path, problem_share_dir)

    # 确保目录存在
    os.makedirs(file_dir, exist_ok=True)

    # 读取文件内容
    try:
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S")

        file_path = os.path.join(file_dir, f"{problem_type}_{current_time}.txt")

        with smbclient.open_file(file_path, mode='w') as file:
            file.write(feedback_words)

    except Exception as e:
        raise ValueError(f"写入文件出错: {e}")
