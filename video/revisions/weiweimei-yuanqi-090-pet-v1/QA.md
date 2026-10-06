# 本轮视频检查

2026-10-06。WeiweimeiIntro：1080 × 1920，30 fps，1357 帧，45.2333 秒。

- 已换成七条本地 IndexTTS 2.5 整段音轨，使用用户认可的 B / 轻元气 / 0.90 配置。
- 七条模型 WAV 和视频音轨副本均已校验有效、非静音；副本仅做恒定音量增益，未变速或变调。
- 每场景仅一条音轨；字幕切换不切音频，不增加人为句内留白。
- 实测 WAV 长度与 audioTracks 时长一致；音轨与字幕均落在各自场景范围；全片时长等于七场景帧数之和。
- ESLint 与 TypeScript 通过；七个场景代表静帧渲染通过，浏览器错误为空。实际查看了 Showcase 和 Install 帧，角色、文字与安装路径可见。
- Studio 已启动在 http://localhost:3007/WeiweimeiIntro。自动检查点击播放后首条新字幕出现，新的 Hook.wav 返回有效分段响应 206，页面运行错误为空。
- Studio 检查中 HTML audio 元素的活跃状态列表为空；该检查证明新素材加载和字幕出现，不作为实际听觉自然度的证据。
- 已生成与视频时间线等长的 full-video-narration-review.wav，包含场景边缘留白供审核，不改变句内节奏。
- 稿件、发音、全片听感、字幕内部精确时间等待用户审核。字幕当前按文本长度估算，没有完成语音识别或逐词对齐。
- 原稿和系统音频已保留在 revisions/system-voice-v1；现有宠物安装素材和客户端未修改。此前检查记录在该备份里的 QA.md。

检查报告：checks/report.json、checks/studio-report.json、checks/voice-replacement-report.json。全片尚未导出最终 MP4；预览检查不能代替导出后的完整播放验收。
