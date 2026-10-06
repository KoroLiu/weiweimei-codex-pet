"""Record the requested 0.94 trial; retain the previously approved 0.90 profile."""
import importlib.util
import json
from datetime import datetime
from pathlib import Path

import numpy as np
import soundfile as sf

VIDEO = Path(__file__).resolve().parents[1]
PROJECT = VIDEO.parent
TTS = Path(r"C:\IndexTTS")
BATCH = TTS / "outputs/weiweimei/pet-intro/weiweimei-094-sentence-pet-v2"
PROFILE = TTS / "voices/weiweimei/profiles/weiweimei-yuanqi-094-sentence-v1"
OLD = TTS / "voices/weiweimei/profiles/weiweimei-yuanqi-090-v1"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


manifest = read(BATCH / "batch-manifest.json")
profile = read(PROFILE / "profile.json")
assert profile["durationFactor"] == 0.94 and profile["approvedBy"] is None
timeline = read(VIDEO / "timeline.json")
assert timeline["durationInFrames"] == 1450
now = datetime.now().astimezone().isoformat()

# Listening copies differ only by a constant gain, never tempo or pitch.
for name in ("Showcase", "Probe-Showcase-continuous", "Probe-Bang-plain"):
    source = BATCH / f"{name}.wav"
    destination = BATCH / f"{name}-listening.wav"
    if destination.exists():
        raise RuntimeError(f"Do not overwrite an existing listening copy: {destination}")
    wave, rate = sf.read(source, dtype="float32")
    assert rate == 22050 and np.isfinite(wave).all() and len(wave) > 0
    peak = float(np.max(np.abs(wave)))
    rms = float(np.sqrt(np.mean(wave.astype("float64") ** 2)))
    gain = min(0.08 / rms, 0.95 / peak)
    sf.write(destination, wave * gain, rate, subtype="PCM_16")
    sample = next(item for item in manifest["samples"] if item["id"] == name)
    sample["listeningCopy"] = {"path": str(destination), "constantGain": gain,
                                "durationSeconds": len(wave) / rate,
                                "tempoOrPitchChanged": False}
manifest["fullVideoReview"] = str(BATCH / "full-video-narration-review.wav")
write(BATCH / "batch-manifest.json", manifest)

trial = {"profile": str(PROFILE / "profile.json"), "durationFactor": 0.94,
         "generationMode": "complete_sentences", "sentencePauseMs": 160,
         "batchManifest": str(BATCH / "batch-manifest.json"),
         "status": "generated_awaiting_user_listening_review",
         "requestedBy": "user", "requestedAt": profile["requestedAt"],
         "previousApprovedProfile": str(OLD / "profile.json"),
         "latestUserFeedback": "0.90 仍太快，改 0.94；完整句子间需要正常停顿，听感仍奇怪。英文不顺；取消十六方向宣传。"}
catalog = read(TTS / "voices/catalog.json")
voice = next(item for item in catalog["voices"] if item["id"] == "weiweimei")
voice["currentProjectTrial"] = trial
voice["deliveryTuning"].update({"status": "retuning_awaiting_user_review",
                              "target": "参考 B，轻元气，0.94，完整句子间短留白，逗号保持连贯。",
                              "trialDurationFactor": 0.94, "finalDurationFactor": None,
                              "selectedProfile": trial["profile"], "pendingPlan": None,
                              "lastTrialBatch": trial["batchManifest"], "manualPauseInsertion": True,
                              "sentencePauseMs": 160, "latestUserFeedback": trial["latestUserFeedback"],
                              "selectedSampleId": None, "previousApprovedProfile": trial["previousApprovedProfile"]})
voice["latestProjectVoiceover"].update({"batchManifest": trial["batchManifest"],
                                       "profile": trial["profile"], "durationFactor": 0.94,
                                       "deliveryStatus": trial["status"],
                                       "fullReviewAudio": manifest["fullVideoReview"]})
catalog["updatedAt"] = now
write(TTS / "voices/catalog.json", catalog)
selection = read(TTS / "voices/weiweimei/reference-selection.json")
selection.update({"deliveryStatus": "retuning_awaiting_user_review", "finalDurationFactor": None,
                  "targetDelivery": voice["deliveryTuning"]["target"], "requestedDurationFactor": 0.94,
                  "currentProjectTrial": trial, "approvedDeliveryIsHistorical": True,
                  "lastTrialBatch": trial["batchManifest"], "latestUserFeedback": trial["latestUserFeedback"]})
write(TTS / "voices/weiweimei/reference-selection.json", selection)

spec = importlib.util.spec_from_file_location("voice_workflow", VIDEO / "scripts/make-index-voiceover.py")
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)
timing = read(VIDEO / "voiceover-timing.json")
for scene in timing:
    scene["voiceSettings"] = workflow.voice_settings(profile)
write(VIDEO / "voiceover-timing.json", timing)

(PROFILE / "README.md").write_text("""# 维维美 · 0.94 · 完整句子留白试听

2026-10-06 用户要求：改为 0.94，完整句子间有停顿，逗号保持连贯。这份配置是待审核新试听，尚未得到新听感认可。此前 0.90 整段方案保留供回退。

参考仍为 B（日语原音 27.60–33.20 秒）；开心 0.30、惊喜 0.05、权重 0.65，随机关闭、脚本种子 42。每个完整句子生成后合并，句间额外加 160 毫秒；模型已有留白保留，实际衔接可能更长。短开场 Bang 与自我介绍一起生成。无后期变速或变调。

同样的 0.94，分句生成会改变句内表达。动作展示保留整段生成对照，因此两版不只是相差 160 毫秒静音。听感由用户判断。

[全部参数](profile.json)。[逐项调音操作](C:/codex project/codex pet/video/VOICE_WORKSHOP.md)。[口播审核稿](C:/codex project/codex pet/video/SCRIPT_REVIEW.md)。[全片试听](C:/IndexTTS/outputs/weiweimei/pet-intro/weiweimei-094-sentence-pet-v2/full-video-narration-review.wav)。

官方 UI 可加载旧预设“维维美_轻元气_090”载入参考与情感，再手动设 ZH、0.94。本轮没有创建新的 094 官方预设；固定句间空白需要脚本。英文先尝试原词和官方音素语法，不代表训练了英文模型。
""", encoding="utf-8")

notice = "> 最新调试（2026-10-06）：用户要求 **0.94、完整句子间短停顿**；新试听待认可。此前 0.90 连续版保留为回退，旧的‘不额外插停顿’不再是本项目最新要求。见 [本轮配置](profiles/weiweimei-yuanqi-094-sentence-v1/README.md) 与 [操作清单](C:/codex project/codex pet/video/VOICE_WORKSHOP.md)。\n\n"
rhythm = TTS / "voices/weiweimei/RHYTHM_GUIDE.md"
rhythm.write_text(notice + rhythm.read_text(encoding="utf-8-sig"), encoding="utf-8")
for path in (TTS / "README.md", TTS / "TUNING_GUIDE.md", TTS / "voices/weiweimei/character-direction-draft.md"):
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n\n## 2026-10-06 最新项目调试要求\n\n用户改为 0.94，完整句子间短留白；本轮额外静音先试 160 毫秒，逗号不拆。参考 B 与轻元气情感保留，新听感待审核。此前认可的 0.90 连续版仍可回退。本项目当前配置为 voices/weiweimei/profiles/weiweimei-yuanqi-094-sentence-v1/profile.json，详细操作在 C:/codex project/codex pet/video/VOICE_WORKSHOP.md。英文先校正拼写与音素，不需要先收集训练集。\n")

readme = """# 维维美介绍与安装教程 · 新配音审核预览

2026-10-06。七个场景，1080 × 1920，30 fps，1450 帧，**48.33 秒**，主合成 WeiweimeiIntro。

最新试听使用参考 B、轻元气、**时长系数 0.94**。完整句子分别生成，句间额外加 160 毫秒，逗号保持连贯；每场景合并成一条音轨。Bang! 我是维维美！为开场。新稿、发音、全片听感等待用户审核；此前认可的 0.90 连续版保留作备选。

十六方向视线跟随已取消，从画面和口播卖点删除；图集方向格只为格式兼容保留。九组动作仍展示，工作表情短暂播放的限制保留。

[口播审核稿](SCRIPT_REVIEW.md)。[自己改稿、UI 调音、停顿与英文处理](VOICE_WORKSHOP.md)。[本轮配置](C:/IndexTTS/voices/weiweimei/profiles/weiweimei-yuanqi-094-sentence-v1/README.md)。

## 查看与审听

在此目录运行 npm run dev，打开 http://localhost:3007/WeiweimeiIntro。可播放全片或在 Scenes 选场景。

[全片配音试听](C:/IndexTTS/outputs/weiweimei/pet-intro/weiweimei-094-sentence-pet-v2/full-video-narration-review.wav)。动作展示另有相同 0.94 的连续版作为对照。分句也会改变表达，对照并非只相差静音。

## 修改和复用

- storyboard.json：say 是实际合成文本，displaySay 是普通审核稿，cues[].text 是字幕，voiceSentence 指向从 0 开始的句子。
- voice-profile.json：本项目采用的中央配置与最新批次。当前未标记为新听感已认可。
- scripts/make-index-voiceover.ps1：使用 D:\\Anaconda\\envs\\index-tts；代码、权重、配置和原始结果集中管理于 C:\\IndexTTS。无需安装新环境。
- 每个生成单元最多 40 字符是本工作流的低显存约束；完整场景可有多句，不是模型字数上限。
- 音频副本位于 public/voiceover/weiweimei-094-sentence-pet-v2，仅统一音量，没有后期变速变调。
- 字幕采用实测句子边界，同一句内的字幕页仍按文字长度估算，未完成逐词识别。

```powershell
powershell -NoProfile -File .\\scripts\\make-index-voiceover.ps1 -BatchName my-edit-v3
npm run sync-voiceover
npm run dev
```

只重做开场可加 -Scene Hook；全局语速或情感改变时重做全片。每次采用新批次名，不覆盖旧音频。脚本会生成整片审核 WAV；sync 会重生成 speech.tsx、Composition.tsx、Root.tsx、timeline.json、SRT，Studio 手工改字幕需先保留或写回 voiceover-timing.json。

## 回退和检查

0.90 配音与系统配音均保留，旧文稿、源码和时序在 revisions；旧文档只作历史记录。原生宠物安装素材与客户端未修改。本轮检查见 QA.md。声音和稿件审核通过后再导出最终视频。
"""
(VIDEO / "README.md").write_text(readme, encoding="utf-8")
(VIDEO / "QA.md").write_text("""# 本轮视频检查

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
""", encoding="utf-8")
production = VIDEO / "PRODUCTION_PLAN.md"
text = production.read_text(encoding="utf-8-sig")
text = text.replace("45.23", "48.33").replace("## 已选声音", "## 当前试听声音")
start = text.index("参考 B、轻元气、时长系数")
end = text.index("\n\n## 画面与内容", start)
text = text[:start] + "参考 B、轻元气、时长系数 0.94，完整句子生成后合并。开心 0.30、惊喜 0.05、权重 0.65；句间额外 160 毫秒，模型已有留白保留，逗号不拆。配置在 C:/IndexTTS/voices/weiweimei/profiles/weiweimei-yuanqi-094-sentence-v1。新听感待认可；此前 0.90 连续版保留作回退。官方 UI 可加载旧 090 预设载入参考和情感，再手动设 ZH、0.94；固定句间留白用脚本。" + text[end:]
text = text.replace("维维美介绍自己、邀请安装", "Bang! 我是维维美！")
text = text.replace("配音每场景整段生成", "配音按完整句子生成并合成每场景一条音轨")
text = text.replace("基准 0.90 保留，实验另存", "当前试听 0.94，旧 0.90 回退版保留，实验另存")
text = text.replace("当前是文本长度估算，不是识别得到的逐词时间", "采用实测句子边界，句内字幕页按文本长度估算，未完成逐词识别")
production.write_text(text, encoding="utf-8")
brief = PROJECT / "PROJECT_BRIEF.md"
text = brief.read_text(encoding="utf-8-sig").replace("16 个视线方向已加入", "此前加入方向素材（相关功能现已取消，仅保留格式兼容格）")
brief.write_text(text, encoding="utf-8")
with (PROJECT / "STATUS.md").open("a", encoding="utf-8") as handle:
    handle.write("\n\n0.94 整句试听和 48.33 秒视频预览已生成，句间额外 160 毫秒。Bang 开场与取消十六方向文案已同步；新发音和听感待审核，0.90 认可版保留。七静帧、源码和预览加载检查通过。详见 video/QA.md 与 video/VOICE_WORKSHOP.md。\n")
print(json.dumps({"seconds": timeline["durationInFrames"] / 30, "currentTrial": trial,
                  "centralAndProjectDocsUpdated": True}, ensure_ascii=False))
