# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.08.19
Author: ZhangYuetao
File Name: utils.py
Update: 2024.11.14
"""

import toml


def save_settings_to_toml(width, height, channels, dtype):
    settings_path = "settings/bin_setting.toml"
    settings = {
        'width': int(width),
        'height': int(height),
        'channels': int(channels),
        'dtype': dtype
    }
    with open(settings_path, 'w') as f:
        toml.dump(settings, f)


def is_bin(file_name):
    return file_name.lower().endswith('.bin')


def is_image(file_name):
    image_extensions = ['.jpg', '.jpeg', '.bmp', '.png', '.gif', '.tiff']
    return any(file_name.lower().endswith(ext) for ext in image_extensions)


def is_video(file_name):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    return any(file_name.lower().endswith(ext) for ext in video_extensions)
