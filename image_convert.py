# -*- coding: utf-8 -*-

"""
Project Name: format_conversion
File Created: 2024.06.13
Author: ZhangYuetao
File Name: image_convert.py
last renew 2024.06.18
"""

from PIL import Image
import os


def convert_image(input_path, output_path, target_format):
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


def is_image(file_name):
    image_extensions = ['.jpg', '.jpeg', '.bmp', '.png', '.gif', '.tiff']
    return any(file_name.lower().endswith(ext) for ext in image_extensions)


def convert_images(input_folder, output_folder, target_format):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if is_image(file):
                input_path = os.path.join(root, file)
                output_path = root.replace(input_folder, output_folder)
                convert_image(input_path, output_path, target_format)

# convert_images("/home/zyt/桌面/t1", "/home/zyt/桌面/ll", "gif")
