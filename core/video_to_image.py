# -*- coding: utf-8 -*-
"""
Project Name: format_conversion
File Created: 2024.06.14
Author: ZhangYuetao
File Name: video_to_image.py
Update: 2025.06.24
"""

import os

import cv2
from PIL import Image
import zyt_validation_utils


def get_video_fps(video_path):
    """
    获取视频的帧率（FPS）。

    :param video_path: 视频文件的路径。
    :return: 视频的帧率，如果无法打开视频则返回 None。
    """
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"Error: Could not open video {video_path}.")
        return None
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    return fps


def video_to_images(input_path, output_path, nums, target_format, error_label=None):
    """
    将视频文件转换为图像或 GIF 文件。

    :param input_path: 输入视频文件的路径。
    :param output_path: 输出图像或 GIF 文件的保存路径。
    :param nums: 控制提取帧的间隔或 GIF 的分段数量。
    :param target_format: 目标格式，如 "jpeg"、"png" 或 "gif"。
    :param error_label: 错误信息信号，用于在 GUI 中显示错误信息，默认为 None。
    """
    try:
        # 检查输入文件是否为视频
        if not zyt_validation_utils.is_video(input_path, speed="fast"):
            raise ValueError("不支持的视频格式")

        # 如果输出路径不存在，则创建
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # 打开视频文件
        video = cv2.VideoCapture(input_path)

        if not video.isOpened():
            raise ValueError("Error: Could not open video.")

        fps = video.get(cv2.CAP_PROP_FPS)  # 获取帧率
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # 获取总帧数

        old_filename = input_path.split('/')[-1]  # 获取视频文件名

        if target_format.lower() == "gif":
            # 处理 GIF 格式
            nums = int(nums)
            segment_frames = total_frames // nums  # 每段 GIF 的帧数
            frame_count = 0
            extracted_count = 0

            for i in range(nums):
                frames = []
                for j in range(segment_frames):
                    ret, frame = video.read()
                    if not ret:
                        break
                    frames.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                    frame_count += 1

                if frames:
                    # 保存 GIF 文件
                    gif_path = os.path.join(output_path, f"{old_filename}_{i + 1:02d}.gif")
                    frames[0].save(gif_path, save_all=True, append_images=frames[1:], loop=0, duration=int(1000 / fps))
                    extracted_count += 1

            video.release()
            print(f"Extracted {extracted_count} GIFs from the video {input_path}.")

        else:
            # 处理图像格式
            time_interval = 1.0 / nums  # 每帧的时间间隔
            current_time = 0.0
            extracted_count = 0

            while True:
                ret, frame = video.read()
                if not ret:
                    break

                current_time += 1.0 / fps  # 当前时间累积

                if current_time >= time_interval:
                    current_time -= time_interval  # 重置当前时间
                    # 保存图像文件
                    filepath = os.path.join(output_path, f"{old_filename}_{extracted_count:04d}.{target_format.lower()}")
                    filepath = filepath.replace('\\', '/')
                    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    image.save(filepath)
                    extracted_count += 1

            video.release()
            print(f"Extracted {extracted_count} frames from the video {input_path}.")
    except Exception as e:
        # 捕获异常并处理错误信息
        if error_label:
            error_label.emit(f"错误: {str(e)}")
        else:
            print(f"Error: {str(e)}")


def videos_to_images(input_folder, output_folder, nums, target_format, error_label=None):
    """
    将文件夹中的所有视频文件转换为图像或 GIF 文件。

    :param input_folder: 输入视频文件夹的路径。
    :param output_folder: 输出图像或 GIF 文件的保存文件夹路径。
    :param nums: 控制提取帧的间隔或 GIF 的分段数量。
    :param target_format: 目标格式，如 "jpeg"、"png" 或 "gif"。
    :param error_label: 错误信息信号，用于在 GUI 中显示错误信息，默认为 None。
    """
    for root, _, files in os.walk(input_folder):
        for file in files:
            input_path = os.path.join(root, file).replace('\\', '/')
            output_path = root.replace(input_folder, output_folder).replace('\\', '/')
            # 创建输出路径的目录
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            video_to_images(input_path, output_path, nums, target_format, error_label)
