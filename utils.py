# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.08.19
Author: ZhangYuetao
File Name: utils.py
last renew: 2024.08.19
"""

import toml


def save_settings_to_toml(width, height, channels, dtype):
    settings_path = "bin_setting.toml"
    settings = {
        'width': int(width),
        'height': int(height),
        'channels': int(channels),
        'dtype': dtype
    }
    with open(settings_path, 'w') as f:
        toml.dump(settings, f)
