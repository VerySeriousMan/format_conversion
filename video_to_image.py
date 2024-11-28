# -*- coding: utf-8 -*-

"""
Project Name: format_conversion
File Created: 2024.06.14
Author: ZhangYuetao
File Name: video_to_image.py
Update: 2024.11.28
"""

import cv2
import os
from PIL import Image
from utils import is_video


def get_video_fps(video_path):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"Error: Could not open video {video_path}.")
        return None
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    return fps


def video_to_images(input_path, output_path, nums, target_format, error_label=None):
    try:
        if not is_video(input_path):
            return

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        video = cv2.VideoCapture(input_path)

        if not video.isOpened():
            raise ValueError("Error: Could not open video.")

        fps = video.get(cv2.CAP_PROP_FPS)  # 获取帧率
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # 获取总帧数

        old_filename = input_path.split('/')[-1]

        if target_format.lower() == "gif":
            nums = int(nums)
            segment_frames = total_frames // nums
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
                    gif_path = os.path.join(output_path, f"{old_filename}_{i + 1:02d}.gif")
                    frames[0].save(gif_path, save_all=True, append_images=frames[1:], loop=0, duration=int(1000 / fps))
                    extracted_count += 1

            video.release()
            print(f"Extracted {extracted_count} GIFs from the video {input_path}.")

        else:
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
                    filepath = os.path.join(output_path, f"{old_filename}_{extracted_count:04d}.{target_format.lower()}")
                    filepath = filepath.replace('\\', '/')
                    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    image.save(filepath)
                    extracted_count += 1

            video.release()
            print(f"Extracted {extracted_count} frames from the video {input_path}.")
    except Exception as e:
        if error_label:
            error_label.emit(f"错误: {str(e)}")
        else:
            print(f"Error: {str(e)}")


def videos_to_images(input_folder, output_folder, nums, target_format, error_label=None):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            input_path = os.path.join(root, file).replace('\\', '/')
            output_path = root.replace(input_folder, output_folder).replace('\\', '/')
            # 创建输出路径的目录
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            video_to_images(input_path, output_path, nums, target_format, error_label)


# videos_to_images("/home/zyt/桌面/video_test", "/home/zyt/桌面/tte", 5, "gif")
