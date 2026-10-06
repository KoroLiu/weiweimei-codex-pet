import {Card,Pet,SceneFrame,blue} from '../ui';
import {OutroAudio} from '../speech';
export const Outro = () => <><SceneFrame id="Outro" title="让维维美陪你工作" kicker="项目链接在简介">
  <div style={{height:450,display:'flex',justifyContent:'flex-end',paddingRight:60}}><Pet row={8} scale={2.05}/></div>
  <Card style={{background:blue,color:'#fff',marginTop:32,padding:'47px 44px'}}>
    <div style={{fontSize:27,opacity:.7,marginBottom:23}}>项目地址 · GitHub</div>
    <div style={{fontSize:34,fontWeight:600,lineHeight:1.6}}>KoroLiu /<br/>weiweimei-codex-pet</div>
  </Card>
  <div style={{marginTop:52,fontSize:35,lineHeight:1.8,color:'#71839b'}}>当前工作表情只会短暂播放<br/>安装说明和预览，都在项目里。</div>
  <div style={{marginTop:46,fontSize:44,fontWeight:600}}>谢谢大家，我们下期再见！</div>
</SceneFrame><OutroAudio/></>;
