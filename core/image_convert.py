# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.06.13
Author: ZhangYuetao
File Name: image_convert.py
Update: 2025.06.24
"""

import os

from PIL import Image
import zyt_validation_utils


def convert_image(input_path, output_path, target_format):
    """
    图像格式转化。

    :param input_path: 输入图像地址。
    :param output_path: 转换后图像保存地址。
    :param target_format: 目标格式，如 "jpeg"、"png"等。
    """
    if not zyt_validation_utils.is_image(input_path, speed="fast"):
        raise ValueError("不支持的图像格式")

    with Image.open(input_path) as img:
        # 根据目标格式进行必要的模式转换
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        if target_format.upper() == 'JPEG' and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        elif target_format.upper() == 'GIF' and img.mode not in ("P", "L"):
            img = img.convert("P")

        filename = os.path.basename(input_path)
        output_file_path = os.path.join(output_path, os.path.splitext(filename)[0] + '.' + target_format.lower())
        img.save(output_file_path, target_format.upper())


def convert_images(input_folder, output_folder, target_format):
    """
    批量图像格式转化。

    :param input_folder: 输入图像文件夹地址。
    :param output_folder: 转换后图像保存文件夹地址。
    :param target_format: 目标格式，如 "jpeg"、"png"等。
    """
    for root, _, files in os.walk(input_folder):
        for file in files:
            input_path = os.path.join(root, file)
            output_path = root.replace(input_folder, output_folder)
            convert_image(input_path, output_path, target_format)
