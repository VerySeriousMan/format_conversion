# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.06.18
Author: ZhangYuetao
File Name: bin_to_image.py
Update: 2025.06.25
"""

import os
import numpy as np

from PIL import Image
import zyt_validation_utils

import config


def bin_to_image(input_path, output_path, target_format, error_label=None):
    """
    bin文件转换为图像。

    :param input_path: bin文件地址。
    :param output_path: 转换后图像保存地址。
    :param target_format: 目标格式，如 "jpeg"、"png"等。
    :param error_label: 错误信息信号，用于在 GUI 中显示错误信息，默认为 None。
    """
    try:
        if not zyt_validation_utils.is_bin(input_path, speed="fast"):
            raise ValueError("输入文件不是bin文件")

        bin_config = config.load_config(config.BIN_SETTING_FILE, config.BIN_SETTING_DEFAULT_CONFIG)

        width = bin_config['width']
        height = bin_config['height']
        channels = bin_config['channels']
        dtype = np.dtype(getattr(np, bin_config['dtype']))
        endianness = bin_config['endianness']
        layout = bin_config['layout'].upper()
        normalize = bin_config['normalize']
        channel_order = bin_config['channel_order'].upper()
        flip = bin_config['flip']
        rotate = bin_config['rotate']
        
        if channels not in (1, 3, 4):
            raise ValueError("channels 只支持 1/3/4")
        if width <= 0 or height <= 0 or channels <= 0:
            raise ValueError("width/height/channels 必须为正整数")

        # 处理字节序（endianness）
        if endianness == 'little':
            dtype = dtype.newbyteorder('<')
        elif endianness == 'big':
            dtype = dtype.newbyteorder('>')
            
        with open(input_path, 'rb') as f:
            img_data = f.read()

        img_array = np.frombuffer(img_data, dtype=dtype)
        expected_size = width * height * channels
        if img_array.size != expected_size:
            raise ValueError(f"二进制文件大小与预期大小 {expected_size} 不匹配（实际 {img_array.size}）")

        img_array = img_array.reshape((height, width, channels))
        
        # reshape: 按 layout 参数处理
        dims = {'C': channels, 'H': height, 'W': width}

        if sorted(layout) != ['C', 'H', 'W']:
            raise ValueError(f"layout 格式无效（必须由 C, H, W 三个字母组成），当前: {layout}")

        # reshape 成对应 layout 顺序
        reshape_shape = tuple(dims[c] for c in layout)
        img_array = img_array.reshape(reshape_shape)

        # transpose 成 HWC 顺序
        transpose_order = [layout.index(c) for c in 'HWC']
        img_array = np.transpose(img_array, transpose_order)
        
        # normalize（仅针对 float 类型）
        if normalize and np.issubdtype(dtype, np.floating):
            img_array = np.clip(img_array, 0, 1) * 255
            img_array = img_array.astype(np.uint8)

        # 通道顺序调整（BGR -> RGB）
        if channels == 3 and channel_order == 'BGR':
            img_array = img_array[:, :, ::-1]  # BGR → RGB

        # flip
        if flip:
            img_array = np.flipud(img_array)

        # rotate
        if rotate in (90, 180, 270):
            img_array = np.rot90(img_array, k=rotate // 90)
        elif rotate != 0:
            raise ValueError("rotate 参数只支持 0 / 90 / 180 / 270")
        
        # 创建图像对象
        if channels == 1:
            img_array = img_array[:, :, 0]
            img = Image.fromarray(img_array, 'L')
        elif channels == 2:
            img = Image.fromarray(img_array, mode='LA')
        elif channels == 3:
            img = Image.fromarray(img_array, 'RGB')
        elif channels == 4:
            img = Image.fromarray(img_array, mode='RGBA')
        else:
            raise ValueError(f"不支持的通道数：{channels}")
        
        # PIL 兼容性处理
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
    """
    bin文件批量转换为图像。

    :param input_folder: 输入文件夹地址。
    :param output_folder: 转换后图像保存文件夹地址。
    :param target_format: 目标格式，如 "jpeg"、"png"等。
    :param error_label: 错误信息信号，用于在 GUI 中显示错误信息，默认为 None。
    """
    for root, _, files in os.walk(input_folder):
        for file in files:
            input_path = os.path.join(root, file)
            output_path = root.replace(input_folder, output_folder)
            bin_to_image(input_path, output_path, target_format, error_label)
