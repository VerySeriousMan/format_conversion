# -*- coding: utf-8 -*-

"""
Project Name: format_conversion
File Created: 2024.06.13
Author: ZhangYuetao
File Name: image_convert.py
Update: 2024.10.29
"""

from PIL import Image
import os

from utils import is_image


def convert_image(input_path, output_path, target_format):
    if not is_image(input_path):
        return

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
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            input_path = os.path.join(root, file)
            output_path = root.replace(input_folder, output_folder)
            convert_image(input_path, output_path, target_format)

# convert_images("/home/zyt/桌面/t1", "/home/zyt/桌面/ll", "gif")
