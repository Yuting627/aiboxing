#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 Python 生成个人主页：读取 source/config.json 与 source/contents/*.json，
将数据嵌入并输出 pages/index.html。图片路径规则：paths + '/' + 文件名。
"""
import json
import os
import re

# 项目根目录（build.py 所在目录）
ROOT = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(ROOT, "source")
CONTENTS = os.path.join(SOURCE, "contents")
PAGES = os.path.join(ROOT, "pages")
PICS_DIR = os.path.join(SOURCE, "pics")
VIDEOS_DIR = os.path.join(SOURCE, "videos")

IMAGE_EXT = (".jpg", ".jpeg", ".png", ".gif", ".webp")
VIDEO_EXT = (".mp4", ".webm", ".mov")


def path_join(base: str, filename: str) -> str:
    """路径拼接：base + '/' + filename，避免双斜杠。"""
    if not base or not filename:
        return ""
    return base.rstrip("/") + "/" + filename


def load_json(path: str) -> dict | list | None:
    """加载 JSON 文件。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def scan_media() -> list:
    """扫描 source/pics 与 source/videos 下所有图片和视频，返回 AI BOXING 媒体列表（仅文件名）。"""
    media = []
    if os.path.isdir(PICS_DIR):
        for name in sorted(os.listdir(PICS_DIR)):
            if name.startswith(".") or os.path.isdir(os.path.join(PICS_DIR, name)):
                continue
            if any(name.lower().endswith(ext) for ext in IMAGE_EXT):
                media.append({"type": "image", "src": name, "thumb": name})
    if os.path.isdir(VIDEOS_DIR):
        for name in sorted(os.listdir(VIDEOS_DIR)):
            if name.startswith(".") or os.path.isdir(os.path.join(VIDEOS_DIR, name)):
                continue
            if any(name.lower().endswith(ext) for ext in VIDEO_EXT):
                base = os.path.splitext(name)[0]
                media.append({"type": "video", "src": name, "thumb": base + ".jpg"})
    return media


def build_page_data() -> dict:
    """读取 config 与 contents，组装页面数据（路径保持与 config 一致，由前端解析）。"""
    config = load_json(os.path.join(SOURCE, "config.json"))
    if not config or not config.get("paths"):
        raise SystemExit("缺少 source/config.json 或 config.paths")

    # AI BOXING 下方滚动展示 pics 与 videos 下所有图片和视频
    if "pages" not in config:
        config["pages"] = {}
    if "boxing" not in config["pages"]:
        config["pages"]["boxing"] = {}
    config["pages"]["boxing"]["media"] = scan_media()

    site = load_json(os.path.join(CONTENTS, "site.json"))
    home = load_json(os.path.join(CONTENTS, "home.json"))
    about = load_json(os.path.join(CONTENTS, "about.json"))
    skills = load_json(os.path.join(CONTENTS, "skills.json"))
    boxing = load_json(os.path.join(CONTENTS, "boxing.json"))

    # 读取后不把 \n 当作换行：将字符串中的真实换行符改回字面量 \n，由前端用 <br> 渲染
    def preserve_literal_backslash_n(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                obj[k] = preserve_literal_backslash_n(v)
        elif isinstance(obj, str):
            return obj.replace("\n", "\\n")
        elif isinstance(obj, list):
            return [preserve_literal_backslash_n(x) for x in obj]
        return obj

    for block in (about, boxing):
        if block and isinstance(block, dict):
            preserve_literal_backslash_n(block)

    return {
        "config": config,
        "site": site or {},
        "home": home or {},
        "about": about or {},
        "skills": skills or {},
        "boxing": boxing or {},
    }


def inject_embedded_data(html: str, data: dict) -> str:
    """在 <body> 后插入嵌入的 JSON 数据脚本；若已有 page-data 则替换其内容。"""
    json_content = json.dumps(data, ensure_ascii=False, indent=2)
    # 防止 JSON 内的 "</script>" 被解析为结束标签，导致后续脚本报错（如 unterminated string literal）
    json_content = json_content.replace("</", "<\\/")
    new_script = (
        '\n  <script type="application/json" id="page-data">\n'
        + json_content
        + "\n  </script>\n"
    )
    old_pattern = re.compile(
        r'<script type="application/json" id="page-data">.*?</script>',
        re.DOTALL,
    )
    if old_pattern.search(html):
        html = old_pattern.sub(new_script.rstrip(), html, count=1)
    else:
        html = html.replace("<body>", "<body>" + new_script, 1)
    return html


SYNC_INIT_JS = r"""    (function init() {
      var el = document.getElementById('page-data');
      if (!el) return;
      var data = JSON.parse(el.textContent);
      var config = data.config;
      if (!config || !config.paths) return;
      paths.pics = config.paths.pics || '';
      paths.icons = config.paths.icons || '';
      paths.videos = config.paths.videos || '';
      paths.contents = config.paths.contents || '';
      var site = data.site, home = data.home, about = data.about, skills = data.skills, boxing = data.boxing;
      if (site) setNav(site);
      setHome(home, config);
      setAbout(about, config);
      setSkills(skills);
      setBoxing(boxing, config);
      updateActiveNav();
    })();"""


def replace_init_with_sync(html: str) -> str:
    """将异步 init（fetch config/contents）替换为从嵌入数据初始化的同步 init。"""
    # 匹配 (async function init() { ... })(); 整块
    pattern = r"\(\s*async\s+function\s+init\s*\(\)\s*\{[\s\S]*?\}\s*\)\s*\(\s*\)\s*;"
    if re.search(pattern, html):
        return re.sub(pattern, SYNC_INIT_JS, html, count=1)
    return html


def _default_template_path() -> str:
    """返回默认模板所在路径（与 build.py 同目录的 template_index.html）。"""
    return os.path.join(ROOT, "template_index.html")


def main():
    data = build_page_data()
    os.makedirs(PAGES, exist_ok=True)
    template_path = os.path.join(PAGES, "index.html")
    out_path = os.path.join(PAGES, "index.html")

    default_tpl = _default_template_path()
    if os.path.isfile(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            html = f.read()
    elif os.path.isfile(default_tpl):
        with open(default_tpl, "r", encoding="utf-8") as f:
            html = f.read()
    else:
        raise SystemExit(
            "未找到模板：pages/index.html 或 项目根目录/template_index.html 不存在。"
            "请确保 template_index.html 在项目根目录后重新运行 python build.py"
        )

    html = inject_embedded_data(html, data)
    html = replace_init_with_sync(html)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("已生成:", out_path)


if __name__ == "__main__":
    main()
