import {Composition,Series} from 'remotion';
import {Hook} from './scenes/Hook';
import {Showcase} from './scenes/Showcase';
import {Download} from './scenes/Download';
import {Preview} from './scenes/Preview';
import {Install} from './scenes/Install';
import {Activate} from './scenes/Activate';
import {Outro} from './scenes/Outro';

export const WeiweimeiVideo = () => <Series>
  <Series.Sequence name="给 Codex 添一位小伙伴" durationInFrames={298}><Hook/></Series.Sequence>
  <Series.Sequence name="九组动作，表情很丰富" durationInFrames={283}><Showcase/></Series.Sequence>
  <Series.Sequence name="01 · 下载项目" durationInFrames={290}><Download/></Series.Sequence>
  <Series.Sequence name="02 · 先看看她的样子" durationInFrames={297}><Preview/></Series.Sequence>
  <Series.Sequence name="03 · 把宠物放到这里" durationInFrames={448}><Install/></Series.Sequence>
  <Series.Sequence name="04 · 在 Codex 中选择她" durationInFrames={294}><Activate/></Series.Sequence>
  <Series.Sequence name="让维维美陪你工作" durationInFrames={385}><Outro/></Series.Sequence>
</Series>;

export const MyComposition = () => <Composition id="WeiweimeiIntro" component={WeiweimeiVideo} width={1080} height={1920} fps={30} durationInFrames={2295} />;
