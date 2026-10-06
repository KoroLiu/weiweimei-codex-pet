# 维维美介绍与安装教程 · 视频初稿

本片目标是让新观众认识维维美，并学会下载和安装。画幅 **1080 × 1920**，**30 fps**，**76.5 秒**；主合成 `WeiweimeiIntro`。采用示范视频的浅蓝色竖屏结构：顶部日期和进度、左对齐标题、中央主画面、宠物陪伴和底部字幕。

## 怎么看

当前预览：http://localhost:3007/WeiweimeiIntro

点击播放查看完整节奏，左侧 `Scenes` 可单独打开七个场景。重新启动时，在此目录运行 `npm run dev`，打开终端打印的本机地址。

## 已包含

- 项目现有透明图集驱动的动作；无需重新生成角色。
- 本机 Huihui 中文合成试配音，17 个音频段，没有调用云端配音服务。
- 依据音频实测长度同步的字幕、场景时长，以及 `captions.zh-CN.srt`。
- 实际 GitHub 仓库和本地预览截图；文件位置演示和标注为示意的 Codex 设置步骤。
- 当前原生客户端工作表情只短暂播放的说明。

这是可互动预览的初稿，尚未导出最终 MP4 或向平台提交。

## 文件怎么改

| 文件 | 用途 |
| --- | --- |
| `storyboard.json` | 口播稿；text 为字幕，say 为合成配音文本 |
| `src/scenes/` | 七个独立场景 |
| `src/ui.tsx`、`src/style.css` | 共用版式、颜色、图集动画 |
| `voiceover-timing.json`、`timeline.json` | 音频实测和时间线 |
| `PUBLISH_DRAFT.md` | 投稿标题和简介 |
| `REFERENCE_ANALYSIS.md` | 示范视频观察记录 |
| `QA.md` | 检查范围和限制 |

修改口播后，运行 `powershell -NoProfile -File .\scripts\make-voiceover.ps1`，然后运行 `npm run sync-voiceover`。同步脚本会重写 src/speech.tsx、src/Composition.tsx、src/Root.tsx 和字幕文件；在 Studio 修改这些生成文件后，重新同步前先保存手工改动。

换成自己的录音时，需要重新测量时长并同步字幕；直接覆盖 WAV 会保留旧时间。

## 验证与导出

`npm run lint` 检查源码，`npm run check-frames` 检查七个代表静帧。先在 Studio 中播放确认声音与节奏；定稿后可用 Studio 的 Render 界面导出 H.264 MP4，或运行 `npx remotion render WeiweimeiIntro out/weiweimei-intro.mp4`。导出后完整播放检查，再投稿。

字幕组件来源：[Remotion Basic Captions](https://www.remotion.dev/elements/captions/basic-captions)。官方源码保留，样式通过本项目 CSS 调整。

