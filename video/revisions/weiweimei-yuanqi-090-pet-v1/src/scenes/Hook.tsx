import {interpolate,useCurrentFrame,useVideoConfig} from 'remotion';
import {Label,Pet,SceneFrame,blue} from '../ui';
import {HookAudio} from '../speech';
export const Hook = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  return <><SceneFrame id="Hook" title="给 Codex 添一位小伙伴" kicker="项目介绍">
    <div style={{height:720,display:'flex',alignItems:'center',justifyContent:'center',position:'relative'}}>
      <div style={{width:610,height:610,position:'absolute',borderRadius:'50%',border:'2px solid #d8e6f6'}} />
      <Pet row={frame<durationInFrames*.4?0:3} scale={2.8} style={{scale:interpolate(frame,[0,24],[.94,1],{extrapolateRight:'clamp'})}}/>
    </div>
    <div style={{textAlign:'center',marginTop:30,fontSize:112,fontWeight:700,color:blue,letterSpacing:12}}>维维美</div>
    <div style={{textAlign:'center',marginTop:34}}><Label>二维 Q 版 · 自定义宠物</Label></div>
  </SceneFrame><HookAudio/></>;
};
