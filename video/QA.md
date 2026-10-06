# 本轮视频检查

2026-10-06。WeiweimeiIntro：1080 × 1920，30 fps，1450 帧，48.3333 秒。

- 七场景配音采用本地 IndexTTS 2.5，B / 轻元气 / 0.94，完整句子之间额外 160 毫秒。句子原有留白保留，逗号不拆；开场短招呼一起生成。
- 模型 WAV、视频副本和审核混音有效、非静音、有限值。音轨副本只调整恒定增益，无后期变速、变调。
- 每条音轨帧数等于各句子音频与额外静音之和；每场景一条音轨。音轨、字幕位于场景范围，全片审核 WAV 长度与 1450 帧时间线一致。
- ESLint / TypeScript 通过；七场景代表静帧渲染通过，运行错误为空。实际查看 Hook 与 Showcase：Bang 字幕、九组动作可见，16 方向卖点已移除。
- Studio 本地预览检查通过：点击播放后新首句字幕出现、Hook.wav 返回 206、页面运行错误为空。HTML audio 状态列表为空，因此只证明素材加载和字幕出现，不证明实际听觉自然度。
- 实测句子边界用于字幕安排；句内多页字幕仍按文本长度估算，未做逐词识别。
- 同为 0.94 的动作展示连续版、Bang 普通英文版保留作对照。分句改变表达，不将其描述成只差静音的严格对照。
- 台词、吞字、英文发音、听感与字幕内部时序等待用户审核，新配置没有标成已认可。此前认可的 0.90 档和旧系统配音均保留。

报告：checks/report.json、checks/studio-report.json、checks/voice-replacement-report.json。当前结果是可审核预览与试听，未导出最终 MP4。

## 2026-10-06 本地 MP4 导出

按用户需要发给家人观看的要求，已导出当前 0.94 版本：[weiweimei-intro-094-review.mp4](exports/weiweimei-intro-094-review.mp4)。约 48.33 秒、1080 × 1920，H.264 + AAC，文件约 7.74 MiB。音视频流、1450 帧与全文件解码检查通过。此次为当前版本的本地分享文件，未向任何外部平台或联系人发送。报告见 checks/export-094-report.json。


## 新增结束语与封面

结尾加入“谢谢大家，我们下期再见！”，同步口播、字幕与结尾画面。0.94 参数沿用，只重生成 Outro，六个既有场景音轨复用。当前时长 1535 帧、51.17 秒。

新版分享文件：[weiweimei-intro-094-ending.mp4](exports/weiweimei-intro-094-ending.mp4)。旧 MP4 保留。

封面：[weiweimei-cover-v1.png](exports/weiweimei-cover-v1.png)，1672 × 941，横版 PNG。沿用 character-reference.png 的角色身份，标题为“把维维美装进 Codex！”，副标题为“虚拟桌面宠物 · 安装教程”。内置 image_gen 生成；[完整提示词](exports/weiweimei-cover-v1.prompt.txt) 与 exports/weiweimei-cover-v1.json 保存来源及生成记录。

源码 lint 通过，新 MP4 的 H.264/AAC 音视频流、1535 帧与全文件解码通过。报告：checks/export-094-ending-report.json。文件保存在本地，未外部提交或发送。
