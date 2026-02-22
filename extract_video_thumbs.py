#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 source/videos 下每个视频截取首帧，在同目录（source/videos）下生成同名 .jpg 缩略图。
依赖：需安装 ffmpeg 并加入 PATH（https://ffmpeg.org/download.html）。
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(ROOT, "source")
VIDEOS_DIR = os.path.join(SOURCE, "videos")
VIDEO_EXT = (".mp4", ".webm", ".mov")


def main() -> None:
    if not os.path.isdir(VIDEOS_DIR):
        print("目录不存在:", VIDEOS_DIR)
        return

    videos = [
        name
        for name in sorted(os.listdir(VIDEOS_DIR))
        if not name.startswith(".")
        and not os.path.isdir(os.path.join(VIDEOS_DIR, name))
        and any(name.lower().endswith(ext) for ext in VIDEO_EXT)
    ]
    if not videos:
        print("未在", VIDEOS_DIR, "中发现视频文件（支持 .mp4 / .webm / .mov）")
        return

    for name in videos:
        base, _ = os.path.splitext(name)
        video_path = os.path.join(VIDEOS_DIR, name)
        out_path = os.path.join(VIDEOS_DIR, base + ".jpg")
        # -y 覆盖已有文件，-vframes 1 只取一帧，-q:v 2 较高质量
        cmd = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            out_path,
        ]
        try:
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            )
            print("已生成:", base + ".jpg")
        except FileNotFoundError:
            print("错误: 未找到 ffmpeg。请安装 ffmpeg 并加入系统 PATH。")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print("处理失败:", name, e.stderr.decode(errors="replace") if e.stderr else e)
            sys.exit(1)

    print("完成，共", len(videos), "个视频已截取首帧到", VIDEOS_DIR)


if __name__ == "__main__":
    main()
