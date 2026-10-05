# 维维美 Codex 宠物

[English](README.md) | **简体中文**

为 Codex 桌面客户端制作的二维 Q 版自定义宠物，包含细描边角色、九组动作和十六个视线方向，可离线预览，并在支持自定义宠物的客户端中安装。

<p align="center">
  <img src="final/previews/idle.webp" width="144" alt="常态轻眨眼">
  <img src="final/previews/review.webp" width="144" alt="完成开心">
  <img src="final/previews/failed.webp" width="144" alt="失败炸毛">
</p>

## 内容

- 九组动作：常态、向右跑、向左跑、挥手、小跳、炸毛、等待回应、思考工作、完成开心。
- 十六个视线方向：零度朝上，顺时针每 22.5 度一帧。
- 透明无损 WebP 图集，支持深浅背景预览及 96 × 104 小尺寸检查。
- 离线互动预览、Windows 安装脚本和可重新打包的 ZIP 安装包。

## 快速开始

### 1. 下载并预览

点击仓库上方的 **Code → Download ZIP**，解压后在浏览器中打开 [`final/index.html`](final/index.html)。不需要启动服务，也不需要安装 Python。

预览页面可以切换动作、视线方向、背景和尺寸。网页上的鼠标跟随及持续播放是预览器提供的素材检查功能。

### 2. 安装到 Codex

需要 Windows 上支持自定义宠物的 Codex 桌面客户端。把 [`final/weiweimei/`](final/weiweimei/) 整个文件夹复制到：

```text
%USERPROFILE%\.codex\pets\weiweimei\
```

如果设置了 `CODEX_HOME`，则使用 `<CODEX_HOME>\pets\weiweimei\`。文件夹中应直接包含 `pet.json` 和 `spritesheet.webp`。

也可以在 PowerShell 中进入下载后的项目根目录，运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\final\Install-Pet.ps1
```

此命令仅对本次 PowerShell 进程指定执行策略。安装脚本检查素材哈希，遇到已有同名目录会停止。

### 3. 选择宠物

在 Codex 设置中的 **Pets / Mini / Mini 与虚拟宠物** 页面刷新，选择“维维美”，再打开宠物显示或唤醒 Mini。实际按钮名称取决于客户端版本。

更多步骤见 [中文使用说明](final/USAGE.zh-CN.md)。

## 当前验证与限制

- 已验证：v2 图集结构、透明边缘、无损解码、预览素材一致性；项目所有者已确认 Windows 原生客户端可以选择、显示，外观正常。
- 工作表情在已检查的客户端中默认播放三轮，约 2.46 秒后回到常态。**它不能持续表示任务是否仍在运行。**
- 十六方向素材已包含，但当前客户端不会持续跟随手动鼠标位置。浏览器预览中的效果不能视为原生客户端功能。
- 完成、等待回应、失败、拖动和重开后的保留行为仍需逐项实测。其他客户端版本和操作系统未验证。

详细检查见 [素材 QA](final/QA.md) 和 [兼容性说明](docs/COMPATIBILITY.md)。

## 项目结构

```text
README.md                   英文首页
README.zh-CN.md             中文首页
final/
  weiweimei/                可安装的 pet.json 和 spritesheet.webp
  previews/                 动画、方向和透明边缘预览
  index.html                离线互动预览
  Install-Pet.ps1           Windows 安装脚本
  USAGE.md                  英文使用说明
  USAGE.zh-CN.md             中文使用说明
  sources/                  补绘源图与提示词
  assemble_pet.py            图集组装与素材检查
  build_delivery.py          本地 ZIP 打包
samples/v3/                 已确认的三种表情源图与动画帧
scripts/validate_release.py  发布前素材与文件检查
docs/COMPATIBILITY.md       已验证行为和客户端限制
```

## 制作与重新打包

仅开发需要 Python 3.11+、Pillow 和 NumPy；当前组装脚本的中文 QA 标注使用 Windows 的微软雅黑字体。

```powershell
python -m pip install -r requirements.txt
python scripts/validate_release.py
python final/build_delivery.py
```

打包结果位于 `final/weiweimei-codex-pet-v1.zip`，同时生成 `SHA256SUMS.txt` 和 `ZIP-SHA256.txt`。打包不依赖本机已经安装宠物，也不会修改 Codex 设置。

需要重新组装图集时运行 `python final/assemble_pet.py`；需要重新提取已确认的三种表情帧时先运行 `python samples/render_samples_v3.py`，再组装、检查和打包。

## 来源

角色外观依据项目所有者提供的维维美视频与表情图片，缺少的动作和方向通过 ImageGen 补绘。处理脚本只做裁切、透明边缘清理、缩放、定位和编码。制作与安装组织参考了 [zili-codex-pet](https://github.com/2846182283/zili-codex-pet)，未使用其角色图集。

原始录屏、表情参考和本机排查记录保留在本地，未纳入仓库。此项目未指定开源许可证；角色及素材的原有权利仍属于相应权利人。
