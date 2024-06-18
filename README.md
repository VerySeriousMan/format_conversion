# formart_conversion

- **Version**: V1.0

## 作者

- **Author**: Zhang Yuetao
- **GitHub**: [VerySeriousMan](https://github.com/VerySeriousMan)


## 项目简介

formart_conversion: **格式转换工具**，提供了图片转换、从视频中提取帧以及将二进制文件转换为图片的功能。它利用PyQt5构建了GUI，并集成了PIL（Pillow）和OpenCV库用于图片和视频处理。

## 功能特点
1. **支持的操作:**
   - **图片格式转换:** 可以将单个或多个图片文件夹中的图片转换为JPEG、BMP、PNG、GIF和TIFF格式。
   - **视频帧提取:** 从MP4、AVI、MOV、MKV、FLV、WMV等视频格式中提取帧，并输出为图片（JPEG、BMP、PNG、GIF和TIFF）。
   - **二进制文件转图片:** 根据预定义的尺寸和数据类型设置，将二进制文件转换为图片。

2. **GUI界面:**
   - 使用PyQt5实现用户友好的界面。
   - 提供选择输入文件或文件夹、设置输出目录、选择目标格式以及调整视频帧提取速率等参数的选项。

3. **进度反馈:**
   - 在转换操作过程中通过状态标签和动画反馈实时更新。

4.**多线程操作:**
   - 采用多线程进行格式转化处理，有效提升转化速率。

## 环境依赖
- Python 3.x
- PyQt5、PIL（Pillow）、OpenCV库
