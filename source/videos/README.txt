将页面视频放在此目录，如 boxing-1.mp4, boxing-2.mp4 等。

优化加载速度建议：
- 在项目根目录运行 `python extract_video_thumbs.py` 可从各视频截取首帧，在同目录（source/videos）下生成同名 .jpg 作为封面；页面会从 videos 路径加载视频缩略图。
- 视频尽量压缩、控制分辨率和码率；可考虑提供 WebM 格式以减小体积（需在页面或 build 中支持多格式）。
