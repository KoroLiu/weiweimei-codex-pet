# 维维美介绍与安装教程 · 声音更新预览

2026-10-06。七个场景，1080 × 1920，30 fps，当前约 **45.23 秒**，主合成 `WeiweimeiIntro`。

声音已采用用户认可的 **参考 B、轻元气、时长系数 0.90、整段生成**。每场景一条连续音频，字幕页独立切换，不增加人工句内停顿。原来作者介绍角色的稿件已整理成维维美本人第一人称；**新台词仍是审核稿**。

[先看口播稿，逐段审核](SCRIPT_REVIEW.md)。[自己改稿、调标点、用 UI 试听的详细操作](VOICE_WORKSHOP.md)。[已认可的声音配置](C:/IndexTTS/voices/weiweimei/profiles/weiweimei-yuanqi-090-v1/README.md)。

## 怎么看

在此目录运行 `npm run dev`，打开终端打印的本机地址。默认为 `http://localhost:3007/WeiweimeiIntro`。点击播放，或在左侧 Scenes 选择单个场景。

预览已换成 IndexTTS 配音。尚未导出审核通过的最终 MP4，也没有向外部平台提交。

## 当前素材和配音

- 使用项目已有透明图集；七场景结构、安装步骤和实际客户端限制继续保留。
- 本地 IndexTTS 2.5、已有 Anaconda 命名环境 `index-tts`；没有云端语音收费接口。
- 用户已认可的参考音、四秒试听及完整参数在 C:\IndexTTS\voices\weiweimei\profiles\weiweimei-yuanqi-090-v1。
- 新的七条原始音频、参数在 C:\IndexTTS\outputs\weiweimei\pet-intro\weiweimei-yuanqi-090-pet-v1；视频音轨副本在 public/voiceover/weiweimei-yuanqi-090-pet-v1。
- 音轨副本仅用恒定增益统一音量，没有后期变速或变调。
- 音频与场景长度从 WAV 实测；字幕内部时间先按文本长度分配，仍需试听后细调。
- 动作切换和安装高亮已改成跟随场景时长，避免新配音缩短后看不到原来较晚的动画。

## 修改和重新生成

| 文件 | 你可以改什么 |
| --- | --- |
| `SCRIPT_REVIEW.md` | 阅读和提出逐段修改意见 |
| `storyboard.json` | say 为整段朗读，cues[].text 为字幕 |
| `voice-profile.json` | 本项目使用的中央声音配置和配音批次 |
| `src/scenes/` | 七个场景的画面和文案 |
| `voiceover-timing.json` | 整段音轨与字幕时间 |
| `timeline.json`、`captions.zh-CN.srt` | 自动同步后的全片时间线和字幕 |

用一个新批次名生成，保留旧版本：

```powershell
powershell -NoProfile -File .\scripts\make-index-voiceover.ps1 -BatchName my-edit-v2
npm run sync-voiceover
npm run dev
```

使用已认可配置的整段流程当前每场景不超过 40 字符；需要长稿时调整场景方案。具体 UI 调整和试听顺序见 VOICE_WORKSHOP.md。旧的 make-voiceover.ps1 是系统配音流程，本版改稿使用 make-index-voiceover.ps1。

同步会生成 src/speech.tsx、src/Composition.tsx、src/Root.tsx 和 SRT。Studio 中的字幕手动编辑需要先保留，或把修正写回 voiceover-timing.json；再次同步会重生成文件。

## 回退和定稿

旧稿、旧时序、生成源码和系统声音在 revisions/system-voice-v1；旧 public/voiceover 下的 WAV 也保留。新稿通过审核后再导出最终版本。新台词的听感、发音和字幕细节仍要整片试听。

检查命令：`npm run lint`、`npm run check-frames`、`node scripts/check-studio.cjs`。检查记录见 QA.md。
