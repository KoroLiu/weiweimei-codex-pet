import {Audio} from '@remotion/media';
import {staticFile} from 'remotion';
import {BasicCaptions} from './basic-captions';
export const HookAudio = () => <>
  <Audio name="我给 Codex 做了一只小宠物" src={staticFile("voiceover/Hook-1.wav")} from={14} durationInFrames={87} volume={0.9} />
  <Audio name="她叫维维美" src={staticFile("voiceover/Hook-2.wav")} from={107} durationInFrames={49} volume={0.9} />
  <Audio name="带你认识她，再装到自己的电脑上" src={staticFile("voiceover/Hook-3.wav")} from={162} durationInFrames={114} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "我给 Codex 做了一只小宠物",
    "startMs": 466.6666666666667,
    "endMs": 3449.84126984127,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "她叫维维美",
    "startMs": 3566.666666666667,
    "endMs": 5273.197278911564,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "带你认识她，再装到自己的电脑上",
    "startMs": 5400,
    "endMs": 9275.691609977324,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
export const ShowcaseAudio = () => <>
  <Audio name="眨眼、挥手、小跳、炸毛……" src={staticFile("voiceover/Showcase-1.wav")} from={14} durationInFrames={118} volume={0.9} />
  <Audio name="一共九组动作、十六个视线方向" src={staticFile("voiceover/Showcase-2.wav")} from={138} durationInFrames={123} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "眨眼、挥手、小跳、炸毛……",
    "startMs": 466.6666666666667,
    "endMs": 4481.224489795918,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "一共九组动作、十六个视线方向",
    "startMs": 4600,
    "endMs": 8777.596371882086,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
export const DownloadAudio = () => <>
  <Audio name="打开简介里的 GitHub 项目链接" src={staticFile("voiceover/Download-1.wav")} from={14} durationInFrames={90} volume={0.9} />
  <Audio name="Code → Download ZIP，下载后解压" src={staticFile("voiceover/Download-2.wav")} from={110} durationInFrames={157} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "打开简介里的 GitHub 项目链接",
    "startMs": 466.6666666666667,
    "endMs": 3563.0839002267576,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "Code → Download ZIP，下载后解压",
    "startMs": 3666.6666666666665,
    "endMs": 8998.730158730157,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
export const PreviewAudio = () => <>
  <Audio name="打开 final 里的 index.html" src={staticFile("voiceover/Preview-1.wav")} from={14} durationInFrames={86} volume={0.9} />
  <Audio name="离线切换动作，看看喜不喜欢" src={staticFile("voiceover/Preview-2.wav")} from={106} durationInFrames={169} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "打开 final 里的 index.html",
    "startMs": 466.6666666666667,
    "endMs": 3414.6938775510207,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "离线切换动作，看看喜不喜欢",
    "startMs": 3533.333333333333,
    "endMs": 9246.938775510203,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
export const InstallAudio = () => <>
  <Audio name="复制 final 里的 weiweimei 文件夹" src={staticFile("voiceover/Install-1.wav")} from={14} durationInFrames={106} volume={0.9} />
  <Audio name="粘贴到用户目录下的 .codex\\pets" src={staticFile("voiceover/Install-2.wav")} from={126} durationInFrames={170} volume={0.9} />
  <Audio name="确认里面直接有这两个文件" src={staticFile("voiceover/Install-3.wav")} from={302} durationInFrames={124} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "复制 final 里的 weiweimei 文件夹",
    "startMs": 466.6666666666667,
    "endMs": 4093.786848072562,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "粘贴到用户目录下的 .codex\\pets",
    "startMs": 4200,
    "endMs": 9966.57596371882,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "确认里面直接有这两个文件",
    "startMs": 10066.666666666666,
    "endMs": 14279.410430839001,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
export const ActivateAudio = () => <>
  <Audio name="设置 → Mini 与虚拟宠物" src={staticFile("voiceover/Activate-1.wav")} from={14} durationInFrames={122} volume={0.9} />
  <Audio name="刷新列表 → 选择维维美 → 打开显示" src={staticFile("voiceover/Activate-2.wav")} from={142} durationInFrames={130} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "设置 → Mini 与虚拟宠物",
    "startMs": 466.6666666666667,
    "endMs": 4624.263038548753,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "刷新列表 → 选择维维美 → 打开显示",
    "startMs": 4733.333333333333,
    "endMs": 9145.12471655329,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
export const OutroAudio = () => <>
  <Audio name="装好以后，她就能陪你工作啦" src={staticFile("voiceover/Outro-1.wav")} from={14} durationInFrames={91} volume={0.9} />
  <Audio name="当前工作表情只会短暂播放" src={staticFile("voiceover/Outro-2.wav")} from={111} durationInFrames={116} volume={0.9} />
  <Audio name="项目链接在简介里，我们下期见" src={staticFile("voiceover/Outro-3.wav")} from={233} durationInFrames={129} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "装好以后，她就能陪你工作啦",
    "startMs": 466.6666666666667,
    "endMs": 3595.7369614512477,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "当前工作表情只会短暂播放",
    "startMs": 3700,
    "endMs": 7636.281179138322,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "项目链接在简介里，我们下期见",
    "startMs": 7766.666666666667,
    "endMs": 12153.061224489795,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
