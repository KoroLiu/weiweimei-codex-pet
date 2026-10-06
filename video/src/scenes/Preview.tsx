import {CanvasImage,staticFile} from 'remotion';
import {Card,Companion,SceneFrame,blue} from '../ui';
import {PreviewAudio} from '../speech';
export const Preview = () => <><SceneFrame id="Preview" title="安装前，先看看她" kicker="02 / 离线预览" note="网页中的循环播放和方向控制用于素材预览。">
  <Card style={{padding:0,overflow:'hidden'}}>
    <div style={{padding:'28px 30px',fontSize:32,color:blue,borderBottom:'1px solid #e4edf7'}}>final / index.html</div>
    <CanvasImage src={staticFile('preview-real.png')} style={{width:900,height:761,objectFit:'cover',display:'block'}}/>
  </Card>
  <Companion text={'双击打开，就能看\n不需要启动服务，也不用装 Python。'}/>
</SceneFrame><PreviewAudio/></>;
