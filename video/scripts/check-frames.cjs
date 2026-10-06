const fs = require('node:fs');
const path = require('node:path');
const {bundle} = require('@remotion/bundler');
const {selectComposition, renderStill, openBrowser} = require('@remotion/renderer');
const root=path.resolve(__dirname,'..');
(async()=>{
  fs.mkdirSync(path.join(root,'checks'),{recursive:true});
  const timeline=JSON.parse(fs.readFileSync(path.join(root,'timeline.json'),'utf8'));
  const serveUrl=await bundle({entryPoint:path.join(root,'src/index.ts'),publicDir:path.join(root,'public')});
  const browser=await openBrowser('chrome');
  const composition=await selectComposition({serveUrl,id:'WeiweimeiIntro',puppeteerInstance:browser});
  if(composition.durationInFrames!==timeline.durationInFrames)throw new Error('Duration mismatch');
  const errors=[];
  for(const scene of timeline.scenes){
    const frame=scene.startFrame+Math.floor(scene.durationInFrames*.6);
    await renderStill({serveUrl,composition,puppeteerInstance:browser,frame,scale:.6,output:path.join(root,`checks/${scene.id}.png`),onBrowserLog:log=>{if(log.type==='error')errors.push(log.text)}});
    console.log(`Checked ${scene.id} at frame ${frame}`);
  }
  await browser.close({silent:true});
  if(errors.length)throw new Error(errors.join('\n'));
  const report={checkedAt:new Date().toISOString(),composition:'WeiweimeiIntro',frames:timeline.scenes.length,durationInFrames:composition.durationInFrames,width:composition.width,height:composition.height,fps:composition.fps,browserErrors:errors,audioFiles:fs.readdirSync(path.join(root,'public/voiceover')).length};
  fs.writeFileSync(path.join(root,'checks/report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report));
})().catch(e=>{console.error(e);process.exitCode=1;});
