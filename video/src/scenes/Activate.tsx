import {useCurrentFrame,useVideoConfig} from 'remotion';
import {Card,Companion,Pet,SceneFrame,blue} from '../ui';
import {ActivateAudio} from '../speech';
export const Activate = () => {
  const frame=useCurrentFrame();
  const {durationInFrames}=useVideoConfig();
  return <><SceneFrame id="Activate" title="在设置里，选择维维美" kicker="04 / 打开宠物" note="设置操作示意；页面名称和按钮位置可能随客户端版本变化。">
    <Card>
      <div style={{fontSize:48,fontWeight:600,marginBottom:30}}>Mini 与虚拟宠物</div>
      <div style={{height:1,background:'#e1eaf5',marginBottom:34}}/>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',fontSize:37}}><span>虚拟宠物</span><span style={{border:'1px solid #cbd9ec',padding:'15px 27px',borderRadius:12,color:blue}}>刷新列表 ↻</span></div>
      <div style={{border:'2px solid #88b3f9',background:'#eff5ff',borderRadius:19,marginTop:42,padding:'42px 25px',display:'flex',alignItems:'center',gap:38}}>
        <Pet row={3} scale={1.4}/><div><div style={{fontSize:48,fontWeight:700}}>维维美</div><div style={{fontSize:29,color:'#73869e',marginTop:17}}>自定义宠物</div></div><span style={{fontSize:45,color:blue,marginLeft:'auto'}}>✓</span>
      </div>
      <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',fontSize:38,marginTop:45}}><span>显示宠物 / 唤醒 Mini</span><div style={{height:44,width:85,borderRadius:30,background:frame>durationInFrames*.72?blue:'#c4d0df',padding:5}}><div style={{width:34,height:34,borderRadius:'50%',background:'#fff',marginLeft:frame>durationInFrames*.72?41:0}}/></div></div>
    </Card>
    <Companion text={'刷新 → 选择 → 打开显示\n她就可以陪你一起工作了。'}/>
  </SceneFrame><ActivateAudio/></>;
};
