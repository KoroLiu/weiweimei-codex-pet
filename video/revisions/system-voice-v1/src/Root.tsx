import {Composition,Folder} from 'remotion';
import {MyComposition} from './Composition';
import {Hook} from './scenes/Hook';
import {Showcase} from './scenes/Showcase';
import {Download} from './scenes/Download';
import {Preview} from './scenes/Preview';
import {Install} from './scenes/Install';
import {Activate} from './scenes/Activate';
import {Outro} from './scenes/Outro';

export const RemotionRoot = () => <>
  <MyComposition/>
  <Folder name="Scenes">
    <Composition id="Hook" component={Hook} width={1080} height={1920} fps={30} durationInFrames={298} />
    <Composition id="Showcase" component={Showcase} width={1080} height={1920} fps={30} durationInFrames={283} />
    <Composition id="Download" component={Download} width={1080} height={1920} fps={30} durationInFrames={290} />
    <Composition id="Preview" component={Preview} width={1080} height={1920} fps={30} durationInFrames={297} />
    <Composition id="Install" component={Install} width={1080} height={1920} fps={30} durationInFrames={448} />
    <Composition id="Activate" component={Activate} width={1080} height={1920} fps={30} durationInFrames={294} />
    <Composition id="Outro" component={Outro} width={1080} height={1920} fps={30} durationInFrames={385} />
  </Folder>
</>;
