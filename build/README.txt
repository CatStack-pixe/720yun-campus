这里是抓取 / 生成脚本，正常浏览全景不需要用到。

state.json        从原 720 云页面保存下来的场景数据（名称、视角、热点）
download.py       下载 44 个场景的 6 面全景图和缩略图
build_tour.py     生成 index.html 和 tour_data.json
package_site.py   将静态站打包到 dist/ 和 netlify-deploy.zip
template.html     页面模板（CSS / JS / 布局）

如果需要重新生成页面：
    python build_tour.py

如果需要生成可直接上传的部署目录与压缩包：
    python package_site.py

以上两条命令也可从项目根目录运行，脚本路径相应加上 build/。
页面模板中的资源均使用相对路径；tour.html 仅作为旧地址跳转页保留。

如果需要重新下载图片（会覆盖 images/ 和 thumbs/）：
    python download.py

注意：图片版权归原作者及学校所有，仅供个人离线浏览。
