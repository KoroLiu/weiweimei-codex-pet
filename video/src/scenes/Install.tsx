import {useCurrentFrame,useVideoConfig} from 'remotion';
import {Card,FileRow,Label,SceneFrame,blue} from '../ui';
import {InstallAudio} from '../speech';
export const Install = () => {
  const frame=useCurrentFrame();
  const {durationInFrames}=useVideoConfig();
  return <><SceneFrame id="Install" title="复制文件夹，就能安装" kicker="03 / Windows 安装" note="若自行设置了 CODEX_HOME，请使用该目录下的 pets 文件夹。">
    <Card>
      <Label>从下载的项目复制</Label>
      <div style={{fontSize:44,fontWeight:600,marginTop:28}}>final / <span style={{color:blue}}>weiweimei</span></div>
      <div style={{fontSize:70,textAlign:'center',color:blue,margin:'35px 0'}}>↓</div>
      <Label>Win + R · 输入路径并打开</Label>
      <div style={{fontSize:37,fontFamily:'Consolas, "Microsoft YaHei", monospace',padding:'28px 20px',background:'#eef5ff',borderRadius:12,color:blue,marginTop:24}}>{'%USERPROFILE%\\.codex\\pets\\'}</div>
      <div style={{fontSize:32,marginTop:32,color:'#72849a'}}>没有 pets，就在 .codex 下新建一个</div>
    </Card>
    <Card style={{marginTop:34,padding:'30px 38px',borderColor:frame>durationInFrames*.6?'#9fc4ff':'#e5edf6'}}>
      <div style={{fontSize:31,color:'#7789a1',marginBottom:20}}>安装后 · weiweimei 文件夹内</div>
      <FileRow name="pet.json" selected={frame>durationInFrames*.65}/>
      <FileRow name="spritesheet.webp" selected={frame>durationInFrames*.65}/>
    </Card>
  </SceneFrame><InstallAudio/></>;
};
