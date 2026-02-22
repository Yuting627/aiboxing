# Yuting's Home Page

## 项目构架
- pages/          分页面代码（主站在 pages/index.html）
- source/         所有图片、icon、文字等配置文件，方便修改
  - config.json   source 路径配置：paths（pics/icons/videos/contents 目录路径）、pages（各页面不同位置引用的图片/媒体文件名）；页面通过读取此文件获取图片路径。顶部菜单来自 site.json 的 menu，名称为页面名称，点击跳转对应页面
  - pics/         页面图片（背景、照片、拳击图等）
  - icons/        页面 icon（联系方式、技能图标）
  - videos/       页面视频
  - contents/     页面文字与配置（JSON）

## 用 Python 生成页面
在项目根目录执行：
  python build.py
会读取 source/config.json 与 source/contents/*.json，将数据嵌入并生成 pages/index.html。图片路径规则：paths + '/' + 图片文件名。生成后的页面无需再请求 JSON，可直接用浏览器或静态服务器打开。

重要：修改 source/contents/*.json 或 source/config.json 后，必须重新执行 python build.py，否则页面上仍会显示旧内容（因为页面用的是生成时嵌入的数据，不会自动重新读取 JSON）。

## 本地运行
用浏览器直接打开 index.html 会跳转到 pages/index.html。生成后的页面（运行过 build.py）无需本地服务器即可查看；若使用未生成的版本且需加载 JSON，建议用本地服务器，例如：
  npx serve .
或
  python -m http.server 8000
然后访问 http://localhost:8000 或 http://localhost:8000/pages/

## 修改内容
修改以下文件后请执行 python build.py 使页面生效。
- 菜单与站点标题：source/contents/site.json
- HOME 标题、副标题、背景图、联系方式：source/contents/home.json
- ABOUT 标题、简介：source/contents/about.json；照片文件名：source/config.json → pages.about.photo
- SKILLS 标题、说明、软件图标列表：source/contents/skills.json
- AI BOXING 标题、简介：source/contents/boxing.json；头像与媒体文件名：source/config.json → pages.boxing

## 页面设计（已实现）
- 黑白绿主色调，极简专业
- HOME：背景大图，左侧艺术字 YUTING FENG + 副标题 + 3 种联系方式（icon+文字）
- ABOUT：左文右图，刷新后图片从右侧滑入
- SKILLS：MY SKILLS 标题，文字说明，底下一排软件 icons
- AI BOXING：大头像 + 右侧 ALL IN BOXING 与简介，下方横向滚动图片/视频，悬浮放大，点击打开/播放
