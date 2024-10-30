# -*- coding: utf-8 -*-

"""
Project Name: format_conversion
File Created: 2024.10.29
Author: ZhangYuetao
File Name: image_to_bin.py
Update: 2024.10.30
"""

from PIL import Image
import os
import numpy as np
from utils import is_image


def image_to_bin(input_path, output_path, error_label=None):
    try:
        if not is_image(input_path):
            return

        # 打开图片并转换为指定通道数
        with Image.open(input_path) as img:
            # 根据模式和位深度确定数据类型
            if img.mode == 'L':
                max_val = img.getextrema()[1]  # 灰度图的最大值
                dtype = np.uint8 if max_val < 256 else np.uint16
            elif img.mode == 'RGB':
                max_val = max(img.getextrema()[0][1], img.getextrema()[1][1], img.getextrema()[2][1])  # RGB的最大值
                dtype = np.uint8 if max_val < 256 else np.uint16
            elif img.mode == 'RGBA':
                max_val = max(img.getextrema()[0][1], img.getextrema()[1][1], img.getextrema()[2][1], img.getextrema()[3][1])  # RGBA的最大值
                dtype = np.uint8 if max_val < 256 else np.uint16
            else:
                raise ValueError(f"不支持的图像模式: {img.mode}")

            # 转换图片为数组，并转换为指定数据类型
            img_array = np.array(img, dtype=dtype)

            if not os.path.exists(output_path):
                os.makedirs(output_path)

            filename = os.path.basename(input_path)
            output_file_path = os.path.join(output_path, os.path.splitext(filename)[0] + '.bin')

            img_array.tofile(output_file_path)

    except Exception as e:
        if error_label:
            error_label.emit(f"错误: {str(e)}")


def images_to_bins(input_folder, output_folder, error_label=None):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            input_path = os.path.join(root, file)
            output_path = root.replace(input_folder, output_folder)
            image_to_bin(input_path, output_path, error_label)
