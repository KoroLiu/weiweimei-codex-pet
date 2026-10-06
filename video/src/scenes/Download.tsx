import {CanvasImage,staticFile} from 'remotion';
import {Card,Companion,SceneFrame,blue} from '../ui';
import {DownloadAudio} from '../speech';
export const Download = () => <><SceneFrame id="Download" title="先把项目下载下来" kicker="01 / 下载项目">
  <Card style={{padding:0,overflow:'hidden'}}>
    <div style={{padding:'28px 30px',fontSize:27,color:'#7a8ba0',borderBottom:'1px solid #e4edf7'}}>真实项目仓库 · GitHub</div>
    <CanvasImage src={staticFile('repository-real.png')} style={{width:900,height:761,objectFit:'cover',display:'block'}}/>
  </Card>
  <div style={{marginTop:38,fontSize:39,fontWeight:600,color:blue}}>Code → Download ZIP → 解压</div>
  <Companion text={'项目链接放在视频简介里\nKoroLiu / weiweimei-codex-pet'}/>
</SceneFrame><DownloadAudio/></>;
