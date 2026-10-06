import {Audio} from '@remotion/media';
import {staticFile} from 'remotion';
import {BasicCaptions} from './basic-captions';
export const HookAudio = () => <>
  <Audio name="嘿，我是维维美！想让我陪你用扣代克斯？这就带你把我装进电脑里！" src={staticFile("voiceover/weiweimei-yuanqi-090-pet-v1/Hook.wav")} from={8} durationInFrames={157} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "嘿，我是维维美！",
    "startMs": 266.6666666666667,
    "endMs": 1381.2244897959183,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "想让我陪你用 Codex？",
    "startMs": 1381.2244897959183,
    "endMs": 3424.580498866213,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "这就带你把我装进电脑里！",
    "startMs": 3424.580498866213,
    "endMs": 5467.936507936508,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
export const ShowcaseAudio = () => <>
  <Audio name="眨眼、挥手、小跳，还有炸毛！九组动作和十六个视线方向，表情管够！" src={staticFile("voiceover/weiweimei-yuanqi-090-pet-v1/Showcase.wav")} from={8} durationInFrames={171} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "眨眼、挥手、小跳，还有炸毛！",
    "startMs": 266.6666666666667,
    "endMs": 2537.578231292517,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "九组动作、十六个视线方向",
    "startMs": 2537.578231292517,
    "endMs": 5035.580952380952,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "表情管够！",
    "startMs": 5035.580952380952,
    "endMs": 5943.945578231292,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
export const DownloadAudio = () => <>
  <Audio name="先打开简介里的项目链接，点开绿色的下载菜单，下载压缩包，再解压。" src={staticFile("voiceover/weiweimei-yuanqi-090-pet-v1/Download.wav")} from={8} durationInFrames={176} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "打开简介里的项目链接",
    "startMs": 266.6666666666667,
    "endMs": 2039.8268398268397,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "Code → Download ZIP",
    "startMs": 2039.8268398268397,
    "endMs": 4699.5670995671,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "下载压缩包，再解压",
    "startMs": 4699.5670995671,
    "endMs": 6118.095238095238,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
export const PreviewAudio = () => <>
  <Audio name="先打开画面上这个预览文件，切换动作，看看是不是你喜欢的样子！" src={staticFile("voiceover/weiweimei-yuanqi-090-pet-v1/Preview.wav")} from={8} durationInFrames={146} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "打开 final 里的 index.html",
    "startMs": 266.6666666666667,
    "endMs": 2907.4087816944957,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "切换动作",
    "startMs": 2907.4087816944957,
    "endMs": 3494.240362811791,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "看看是不是你喜欢的样子！",
    "startMs": 3494.240362811791,
    "endMs": 5108.027210884354,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
export const InstallAudio = () => <>
  <Audio name="喜欢的话，就把维维美文件夹放进画面上的宠物目录，里面直接放这两个文件。" src={staticFile("voiceover/weiweimei-yuanqi-090-pet-v1/Install.wav")} from={8} durationInFrames={175} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "复制 final 里的 weiweimei 文件夹",
    "startMs": 266.6666666666667,
    "endMs": 2089.7796730632554,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "放到用户目录下的 .codex\\pets",
    "startMs": 2089.7796730632554,
    "endMs": 3652.447964260331,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "里面直接有 pet.json 和 spritesheet.webp",
    "startMs": 3652.447964260331,
    "endMs": 6083.265306122449,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
export const ActivateAudio = () => <>
  <Audio name="回到扣代克斯设置，找到迷你与虚拟宠物。刷新列表，选我，再打开显示！" src={staticFile("voiceover/weiweimei-yuanqi-090-pet-v1/Activate.wav")} from={8} durationInFrames={196} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "设置 → Mini 与虚拟宠物",
    "startMs": 266.6666666666667,
    "endMs": 3017.3382173382174,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "刷新列表 → 选择维维美",
    "startMs": 3017.3382173382174,
    "endMs": 5267.887667887668,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "打开宠物显示",
    "startMs": 5267.887667887668,
    "endMs": 6768.253968253968,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
export const OutroAudio = () => <>
  <Audio name="装好啦，我来陪你工作！提醒一下，工作表情目前只会短暂播放。项目链接在简介里！" src={staticFile("voiceover/weiweimei-yuanqi-090-pet-v1/Outro.wav")} from={8} durationInFrames={196} volume={0.9} />
  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={[
  {
    "text": "装好啦，我来陪你工作！",
    "startMs": 266.6666666666667,
    "endMs": 2284.4006568144496,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "工作表情目前只会短暂播放",
    "startMs": 2284.4006568144496,
    "endMs": 4974.712643678161,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "项目链接在简介里！",
    "startMs": 4974.712643678161,
    "endMs": 6768.253968253968,
    "timestampMs": null,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</>;
