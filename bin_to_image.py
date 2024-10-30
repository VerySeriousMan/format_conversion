# -*- coding: utf-8 -*-

"""
Project Name: format_conversion
File Created: 2024.06.18
Author: ZhangYuetao
File Name: bin_to_image.py
Update: 2024.10.29
"""

from PIL import Image
import os
import toml
import numpy as np

from utils import is_bin


def bins_to_image(input_path, output_path, target_format, error_label=None):
    try:
        if not is_bin(input_path):
            return

        settings_path = "bin_setting.toml"

        with open(settings_path, 'r') as f:
            settings = toml.load(f)

        width = settings['width']
        height = settings['height']
        channels = settings['channels']
        dtype = getattr(np, settings['dtype'])

        with open(input_path, 'rb') as f:
            img_data = f.read()

        img_array = np.frombuffer(img_data, dtype=dtype)
        expected_size = width * height * channels
        if img_array.size != expected_size:
            raise ValueError(f"二进制文件大小与预期大小 {expected_size} 不匹配。")

        img_array = img_array.reshape((height, width, channels))

        if channels == 1:
            img_array = img_array[:, :, 0]
            img = Image.fromarray(img_array, 'L')
        else:
            img = Image.fromarray(img_array)

        if target_format.upper() == 'JPEG' and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        elif target_format.upper() == 'GIF' and img.mode not in ("P", "L"):
            img = img.convert("P")

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        filename = os.path.basename(input_path)
        output_file_path = os.path.join(output_path, os.path.splitext(filename)[0] + '.' + target_format.lower())
        img.save(output_file_path, target_format.upper())
    except Exception as e:
        if error_label:
            error_label.emit(f"错误: {str(e)}")


def bins_to_images(input_folder, output_folder, target_format, error_label=None):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            input_path = os.path.join(root, file)
            output_path = root.replace(input_folder, output_folder)
            bins_to_image(input_path, output_path, target_format, error_label)
