import {useCurrentFrame,useVideoConfig} from 'remotion';
import {Card,Companion,Pet,SceneFrame,blue} from '../ui';
import {ShowcaseAudio} from '../speech';
const rows=[0,3,4,1,2,5,6,7,8];
const labels=['轻眨眼','挥手','小跳','向右跑','向左跑','炸毛','等待','思考','开心'];
export const Showcase = () => {
  const frame=useCurrentFrame();
  const {durationInFrames}=useVideoConfig();
  const group=Math.min(2,Math.floor(frame/Math.max(1,durationInFrames/3)));
  return <><SceneFrame id="Showcase" title="小小一只，表情很丰富" kicker="动作素材展示" note="此处展示动作素材；原生客户端的触发和播放时长由客户端控制。">
    <Card style={{padding:'72px 20px 55px'}}>
      <div style={{display:'flex',justifyContent:'space-around'}}>{[0,1,2].map(i=><div key={i} style={{textAlign:'center'}}><Pet row={rows[group*3+i]} scale={1.35}/><div style={{fontSize:39,marginTop:32,fontWeight:600}}>{labels[group*3+i]}</div></div>)}</div>
      <div style={{borderTop:'1px solid #e8eef6',marginTop:65,paddingTop:43,display:'flex',justifyContent:'space-around'}}>
        <div><span style={{fontSize:94,fontWeight:700,color:blue}}>9</span><span style={{fontSize:36,marginLeft:20}}>组动作</span></div>
        <div style={{fontSize:36,lineHeight:1.7,color:blue}}>眨眼、挥手、小跳<br/>开心、等待、炸毛</div>
      </div>
    </Card>
    <Companion text={'透明背景，细描边\n先看看她，再决定要不要安装。'}/>
  </SceneFrame><ShowcaseAudio/></>;
};
