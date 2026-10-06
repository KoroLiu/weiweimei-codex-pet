const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const scenes = JSON.parse(fs.readFileSync(path.join(root,'voiceover-timing.json'),'utf8').replace(/^\uFEFF/,''));
const official = fs.readFileSync(path.join(root,'basic-captions-source.md'),'utf8');
const source = official.match(/```tsx[^\n]*\n([\s\S]*?)\n```/)[1];
fs.writeFileSync(path.join(root,'src/basic-captions.tsx'), source+'\n');
const speech = [`import {Audio} from '@remotion/media';`,`import {staticFile} from 'remotion';`,`import {BasicCaptions} from './basic-captions';`];
for(const scene of scenes){
  speech.push(`export const ${scene.id}Audio = () => <>`);
  for(const cue of scene.audioTracks ?? scene.cues){
    speech.push(`  <Audio name=${JSON.stringify(cue.text)} src={staticFile(${JSON.stringify(cue.audio)})} from={${cue.frame}} durationInFrames={${Math.ceil(cue.duration*30)}} volume={0.9} />`);
  }
  speech.push(`  <div className="editorial-caption"><BasicCaptions width={900} combineTokensWithinMilliseconds={0} captions={${JSON.stringify(scene.cues.map(({text,startMs,endMs,timestampMs,confidence,pageBreakAfter})=>({text,startMs,endMs,timestampMs,confidence,pageBreakAfter})),null,2)}} /></div>`);
  speech.push('</>;');
}
fs.writeFileSync(path.join(root,'src/speech.tsx'),speech.join('\n')+'\n');
const imports = scenes.map(s=>`import {${s.id}} from './scenes/${s.id}';`).join('\n');
const total = scenes.reduce((sum,s)=>sum+s.durationInFrames,0);
const main = `import {Composition,Series} from 'remotion';\n${imports}\n\nexport const WeiweimeiVideo = () => <Series>\n${scenes.map(s=>`  <Series.Sequence name=${JSON.stringify(s.title)} durationInFrames={${s.durationInFrames}}><${s.id}/></Series.Sequence>`).join('\n')}\n</Series>;\n\nexport const MyComposition = () => <Composition id="WeiweimeiIntro" component={WeiweimeiVideo} width={1080} height={1920} fps={30} durationInFrames={${total}} />;\n`;
fs.writeFileSync(path.join(root,'src/Composition.tsx'),main);
const rootSource = `import {Composition,Folder} from 'remotion';\nimport {MyComposition} from './Composition';\n${imports}\n\nexport const RemotionRoot = () => <>\n  <MyComposition/>\n  <Folder name="Scenes">\n${scenes.map(s=>`    <Composition id="${s.id}" component={${s.id}} width={1080} height={1920} fps={30} durationInFrames={${s.durationInFrames}} />`).join('\n')}\n  </Folder>\n</>;\n`;
fs.writeFileSync(path.join(root,'src/Root.tsx'),rootSource);
let offset=0;
const manifest=scenes.map(s=>{const result={id:s.id,title:s.title,startFrame:offset,endFrame:offset+s.durationInFrames,durationInFrames:s.durationInFrames};offset+=s.durationInFrames;return result;});
fs.writeFileSync(path.join(root,'timeline.json'),JSON.stringify({fps:30,width:1080,height:1920,durationInFrames:total,scenes:manifest},null,2)+'\n');
let captionIndex=1;
const formatTime=(ms)=>{const n=Math.round(ms);return `${String(Math.floor(n/3600000)).padStart(2,'0')}:${String(Math.floor(n/60000)%60).padStart(2,'0')}:${String(Math.floor(n/1000)%60).padStart(2,'0')},${String(n%1000).padStart(3,'0')}`;};
offset=0;
const srt=[];
for(const scene of scenes){for(const c of scene.cues){srt.push(`${captionIndex++}\n${formatTime(offset/30*1000+c.startMs)} --> ${formatTime(offset/30*1000+c.endMs)}\n${c.text}\n`);}offset+=scene.durationInFrames;}
fs.writeFileSync(path.join(root,'captions.zh-CN.srt'),srt.join('\n'));
console.log(`Synced ${scenes.length} scenes; ${total} frames, ${total/30}s`);
