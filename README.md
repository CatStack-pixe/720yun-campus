# 校园全景静态站

以 `index.html` 为主入口的静态网站。全景播放器、44 个场景、264 张立方体贴图和缩略图均随项目提供。

## 直接上传 Netlify

1. 解压 `netlify-deploy.zip`。
2. 在 Netlify 的手动部署区域上传解压后的整个文件夹，或直接拖入项目中的 `dist` 文件夹。
3. 确认上传文件夹的第一层包含 `index.html`、`images`、`thumbs` 和 `viewer`，上传完成后访问站点根地址。

访客通过浏览器访问即可，无需安装本地运行环境。手动上传的 `dist` 已经生成，可直接使用。

## 从 Git 仓库部署

仓库根目录的 `netlify.toml` 已配置：

- 构建命令：`python build/package_site.py`
- 发布目录：`dist`

构建命令只打包仓库内已有文件。`dist` 和 ZIP 均为生成产物，不纳入 Git。

旧地址 `/tour.html`、`/tour` 会跳转到首页；`#s=场景ID` 仍可用于场景分享。`_redirects` 和 `_headers` 随部署包一起提供。

## 本地预览

在项目根目录执行：

```sh
python -m http.server 8000 --bind 127.0.0.1
```

然后访问 `http://127.0.0.1:8000/`。Windows 也可双击 `启动.bat`，或运行 `node server.js`。

本地预览使用 HTTP 地址；直接双击 HTML 的 `file://` 打开方式会受浏览器的全景贴图读取限制。

## 更新页面与部署包

修改页面结构或交互时，编辑 `build/template.html`，再在项目根目录运行：

```sh
python build/build_tour.py
python build/package_site.py
```

只替换图片或直接修改 `index.html` 时，运行第二条命令即可更新部署包。之后重新上传 `dist`。

## 目录

```text
index.html           网站主入口
tour.html            旧入口兼容跳转
tour_data.json       场景与热点数据
cover.jpg            加载封面
images/              全景贴图
thumbs/              场景缩略图
viewer/              播放器及其许可证
_headers             静态资源缓存规则
_redirects           旧入口重定向规则
netlify.toml         仓库部署配置
build/               页面生成与打包工具
dist/                已生成的上传目录
netlify-deploy.zip   已生成的部署压缩包
```

素材来源、作者署名和使用说明保留于页面及 `使用说明.txt`；播放器许可证见 `viewer/LICENSE`。
原素材说明写有“请勿用于商业用途或公开传播”。在 Netlify 创建公开站点前，请先确认已获得相应发布许可。
