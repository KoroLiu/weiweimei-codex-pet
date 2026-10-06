# 维维美介绍与安装教程 · 新配音审核预览

2026-10-06。七个场景，1080 × 1920，30 fps，1535 帧，**51.17 秒**，主合成 WeiweimeiIntro。

最新试听使用参考 B、轻元气、**时长系数 0.94**。完整句子分别生成，句间额外加 160 毫秒，逗号保持连贯；每场景合并成一条音轨。Bang! 我是维维美！为开场。新稿、发音、全片听感等待用户审核；此前认可的 0.90 连续版保留作备选。

十六方向视线跟随已取消，从画面和口播卖点删除；图集方向格只为格式兼容保留。九组动作仍展示，工作表情短暂播放的限制保留。

[口播审核稿](SCRIPT_REVIEW.md)。[自己改稿、UI 调音、停顿与英文处理](VOICE_WORKSHOP.md)。[本轮配置](C:/IndexTTS/voices/weiweimei/profiles/weiweimei-yuanqi-094-sentence-v1/README.md)。

## 查看与审听

在此目录运行 npm run dev，打开 http://localhost:3007/WeiweimeiIntro。可播放全片或在 Scenes 选场景。

[全片配音试听](C:/IndexTTS/outputs/weiweimei/pet-intro/weiweimei-094-sentence-pet-v2/full-video-narration-review.wav)。动作展示另有相同 0.94 的连续版作为对照。分句也会改变表达，对照并非只相差静音。

## 修改和复用

- storyboard.json：say 是实际合成文本，displaySay 是普通审核稿，cues[].text 是字幕，voiceSentence 指向从 0 开始的句子。
- voice-profile.json：本项目采用的中央配置与最新批次。当前未标记为新听感已认可。
- scripts/make-index-voiceover.ps1：使用 D:\Anaconda\envs\index-tts；代码、权重、配置和原始结果集中管理于 C:\IndexTTS。无需安装新环境。
- 每个生成单元最多 40 字符是本工作流的低显存约束；完整场景可有多句，不是模型字数上限。
- 音频副本位于 public/voiceover/weiweimei-094-sentence-pet-v2，仅统一音量，没有后期变速变调。
- 字幕采用实测句子边界，同一句内的字幕页仍按文字长度估算，未完成逐词识别。

```powershell
powershell -NoProfile -File .\scripts\make-index-voiceover.ps1 -BatchName my-edit-v3
npm run sync-voiceover
npm run dev
```

只重做开场可加 -Scene Hook；全局语速或情感改变时重做全片。每次采用新批次名，不覆盖旧音频。脚本会生成整片审核 WAV；sync 会重生成 speech.tsx、Composition.tsx、Root.tsx、timeline.json、SRT，Studio 手工改字幕需先保留或写回 voiceover-timing.json。

## 回退和检查

0.90 配音与系统配音均保留，旧文稿、源码和时序在 revisions；旧文档只作历史记录。原生宠物安装素材与客户端未修改。本轮检查见 QA.md。声音和稿件审核通过后再导出最终视频。

## 2026-10-06 本地 MP4 导出

按用户需要发给家人观看的要求，已导出当前 0.94 版本：[weiweimei-intro-094-review.mp4](exports/weiweimei-intro-094-review.mp4)。约 48.33 秒、1080 × 1920，H.264 + AAC，文件约 7.74 MiB。音视频流、1450 帧与全文件解码检查通过。此次为当前版本的本地分享文件，未向任何外部平台或联系人发送。报告见 checks/export-094-report.json。


## 新增结束语与封面

结尾加入“谢谢大家，我们下期再见！”，同步口播、字幕与结尾画面。0.94 参数沿用，只重生成 Outro，六个既有场景音轨复用。当前时长 1535 帧、51.17 秒。

新版分享文件：[weiweimei-intro-094-ending.mp4](exports/weiweimei-intro-094-ending.mp4)。旧 MP4 保留。

封面：[weiweimei-cover-v1.png](exports/weiweimei-cover-v1.png)，1672 × 941，横版 PNG。沿用 character-reference.png 的角色身份，标题为“把维维美装进 Codex！”，副标题为“虚拟桌面宠物 · 安装教程”。内置 image_gen 生成；[完整提示词](exports/weiweimei-cover-v1.prompt.txt) 与 exports/weiweimei-cover-v1.json 保存来源及生成记录。

源码 lint 通过，新 MP4 的 H.264/AAC 音视频流、1535 帧与全文件解码通过。报告：checks/export-094-ending-report.json。文件保存在本地，未外部提交或发送。
