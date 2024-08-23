# format_conversion

- **Version**: V1.2

## 作者

- **Author**: Zhang Yuetao
- **GitHub**: [VerySeriousMan](https://github.com/VerySeriousMan)


## 项目简介

format_conversion: **格式转换工具**，提供了图片转换、从视频中提取帧以及将二进制文件转换为图片的功能。它利用PyQt5构建了GUI，并集成了PIL（Pillow）和OpenCV库用于图片和视频处理。

## 版本更新日志

### V1.2（2024.08.19）
**1、优化界面显示**<br>
① 增加页面布局，使控件随窗口大小变化而变化<br>
② 增加界面整体自适应缩放，适配不同的分辨率，解决在高分辨率显示器下文字过小的问题<br>
**2、优化视频抽帧算法**<br>
①编写时间累积器，替换简单的间隔多少帧抽取，精确控制每秒提取的帧数
**3、优化代码已知问题**<br>
①增加文件名读取，修复多段视频格式转化覆盖问题<br>
②增加文件与文件夹导入检测<br>
③修复windows下多段视频抽帧保存问题
**4、优化代码架构**<br>

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
   - 采用多线程分离转换处理与界面操作。

## 环境依赖
- Python 3.x
- PyQt5、PIL（Pillow）、OpenCV库
