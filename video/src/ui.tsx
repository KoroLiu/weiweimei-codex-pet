import {AbsoluteFill, CanvasImage, Easing, Interactive, interpolate, staticFile, useCurrentFrame} from 'remotion';
import type {CSSProperties, ReactNode} from 'react';
import timing from '../voiceover-timing.json';
import './style.css';

export const blue = '#2164df';
export const ink = '#202e44';
export const seconds = (f:number) => `${String(Math.floor(f/1800)).padStart(2,'0')}:${String(Math.floor(f/30)%60).padStart(2,'0')}`;
export const totalFrames = timing.reduce((sum, scene) => sum + scene.durationInFrames, 0);
const counts = [6,8,8,4,5,8,6,6,6];
export const Pet = ({row=0,scale=1,style={}}:{row?:number;scale?:number;style?:CSSProperties}) => {
  const frame = useCurrentFrame();
  const column = Math.floor(frame/4.1) % counts[row];
  return <div style={{width:192*scale,height:208*scale,overflow:'hidden',position:'relative',flexShrink:0,...style}}>
    <CanvasImage src={staticFile('pet/spritesheet.webp')} style={{position:'absolute',width:1536*scale,height:2288*scale,maxWidth:'none',left:-column*192*scale,top:-row*208*scale}} />
  </div>;
};
export const Card = ({children,style={}}:{children:ReactNode;style?:CSSProperties}) => <Interactive.Div name="Main visual" style={{background:'#fff',borderRadius:24,padding:44,boxShadow:'0 18px 45px #5675a019',border:'1px solid #e5edf6',...style}}>{children}</Interactive.Div>;
export const Label = ({children}:{children:ReactNode}) => <div style={{fontSize:32,fontWeight:500,letterSpacing:2,color:'#75869b'}}>{children}</div>;
export const SceneFrame = ({id,title,kicker,children,note}:{id:string;title:string;kicker:string;children:ReactNode;note?:string}) => {
  const frame = useCurrentFrame();
  const index = timing.findIndex(x=>x.id===id);
  const scene = timing[index];
  const elapsed = timing.slice(0,index).reduce((sum,x)=>sum+x.durationInFrames,0)+frame;
  return <AbsoluteFill style={{background:'linear-gradient(150deg,#fbfdff 0%,#f1f7ff 65%,#e9f2ff 100%)',color:ink,fontFamily:'"Microsoft YaHei", "PingFang SC", sans-serif',overflow:'hidden'}}>
    <div style={{position:'absolute',right:-320,top:250,width:790,height:790,border:'80px solid #dceafe66',borderRadius:'50%'}} />
    <div style={{position:'absolute',left:90,right:90,top:92,display:'flex',justifyContent:'space-between',fontSize:25,letterSpacing:2,color:'#8997aa'}}><span>2026-10-06 · PROJECT 01</span><span>{seconds(elapsed)} / {seconds(totalFrames)}</span></div>
    <div style={{position:'absolute',left:90,right:90,top:151,height:3,background:'#dbe4ef'}}><div style={{height:3,width:`${100*elapsed/totalFrames}%`,background:'#7c9bbb'}} /></div>
    <div style={{position:'absolute',top:199,left:90,display:'flex',alignItems:'center',gap:16,fontSize:28,fontWeight:600}}><span style={{background:blue,color:'#fff',borderRadius:9,fontSize:24,width:38,height:38,textAlign:'center',lineHeight:'38px'}}>W</span><span>Koro / CODEX PET</span></div>
    <div style={{position:'absolute',left:90,top:302,right:90,opacity:interpolate(frame,[0,10],[0,1],{extrapolateRight:'clamp',extrapolateLeft:'clamp'})}}>
      <div style={{color:blue,fontSize:29,fontWeight:700,letterSpacing:3,marginBottom:22}}>{kicker}</div>
      <Interactive.Div name="Scene title" style={{fontSize:68,fontWeight:700,letterSpacing:-1,lineHeight:1.35}}>{title}</Interactive.Div>
    </div>
    <div style={{position:'absolute',left:90,right:90,top:560,opacity:interpolate(frame,[2,15,scene.durationInFrames-8,scene.durationInFrames],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}),translate:interpolate(frame,[0,18],['0px 24px','0px 0px'],{easing:Easing.bezier(.16,1,.3,1),extrapolateRight:'clamp',extrapolateLeft:'clamp'})}}>{children}</div>
    {note ? <div style={{position:'absolute',left:110,right:110,top:1620,fontSize:28,lineHeight:1.6,color:'#7b8ca1'}}>{note}</div>:null}
    <div style={{position:'absolute',bottom:68,left:90,fontSize:22,color:'#8997aa'}}>维维美 · Codex 自定义宠物</div>
  </AbsoluteFill>;
};
export const Companion = ({text}:{text:string}) => <div style={{display:'flex',alignItems:'center',gap:34,marginTop:36}}><Pet row={3} scale={.7}/><div style={{borderLeft:'3px solid #cfdced',paddingLeft:28,fontSize:31,lineHeight:1.7,color:'#73849b',whiteSpace:'pre-line'}}>{text}</div></div>;
export const FileRow = ({name,selected=false}:{name:string;selected?:boolean}) => <div style={{display:'flex',alignItems:'center',gap:22,padding:'27px 24px',borderRadius:9,background:selected?'#e8f1ff':'transparent',fontSize:40,fontFamily:'"Microsoft YaHei",sans-serif',color:selected?blue:ink}}><span style={{fontSize:31,color:'#b0bed0'}}>▤</span>{name}</div>;
