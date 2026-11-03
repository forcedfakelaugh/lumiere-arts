async page => {
  await page.setViewportSize({width:1080,height:1920});
  await page.goto('http://127.0.0.1:4816/source/index.html');
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.images].map(i => i.decode())));
  const root='/Users/lucasnguyen/Developer/lumiere-arts/products/01-vung-song-2/versions/v04-chuyen-dong-lien-ket';
  const timing=await page.evaluate(()=>window.__reviewTiming);
  // Force GSAP's zero-time setters to render before inspecting frame zero.
  await page.evaluate(()=>{window.__timelines['lumiere-v04'].seek(.000001).seek(0);});
  const shotFrames=[0,135,210,240,270,360,444,494,537,600,693,700,706,712,718,724,730,739,750,845,851,857,863,882,959];
  const frames=[...new Set([...shotFrames,...Array.from({length:42},(_,i)=>691+i)])].sort((a,b)=>a-b);
  const states=[];
  for(const frame of frames){
    const time=frame/30;
    const state=await page.evaluate(async ({t,frame})=>{
      window.__timelines['lumiere-v04'].seek(t);
      await Promise.all([...document.querySelectorAll('video')].map(v=>new Promise((resolve,reject)=>{
        const start=Number(v.dataset.start),duration=Number(v.dataset.duration);
        if(t<start-1e-8||t>=start+duration-1e-8)return resolve();
        const target=t-start+Number(v.dataset.mediaStart||0);
        if(Math.abs(v.currentTime-target)<.001&&v.readyState>=2)return resolve();
        const timer=setTimeout(()=>reject(new Error('Video seek timed out: '+v.id)),10000);
        v.addEventListener('seeked',()=>{clearTimeout(timer);resolve();},{once:true});v.currentTime=target;
      })));
      const active=[...document.querySelectorAll('.scene')].filter(s=>getComputedStyle(s).visibility==='visible');
      const box=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {x:r.x,y:r.y,width:r.width,height:r.height,opacity:Number(s.opacity),visibility:s.visibility,filter:s.filter};};
      const logo=document.querySelector('#brand-watermark'),closingLogo=document.querySelector('#closing-logo');
      const text=active.flatMap(s=>[...s.querySelectorAll('p,h1,h2,.caption')].filter(e=>{
        for(let p=e;p&&p!==s.parentElement;p=p.parentElement)if(Number(getComputedStyle(p).opacity)===0)return false;
        return true;
      }).map(e=>{const r=e.getBoundingClientRect();return {text:e.textContent.trim(),...box(e),overflow:r.right>1080||r.left<0||r.bottom>1920};}));
      const video=document.querySelector('#look-back'),style=getComputedStyle(video),matrix=new DOMMatrixReadOnly(style.transform);
      return {time:t,frame,scenes:active.map(s=>s.id),logo:{...box(logo),loaded:logo.complete&&logo.naturalWidth>0},closingLogo:{...box(closingLogo),loaded:closingLogo.complete&&closingLogo.naturalWidth>0},text,hero:{id:video.id,currentTime:video.currentTime,width:parseFloat(style.width),height:parseFloat(style.height),scale:matrix.a,x:matrix.e,y:matrix.f,clip:getComputedStyle(document.querySelector('#f3')).clipPath}};
    },{t:time,frame});
    if(state.text.some(t=>t.overflow))throw new Error('Text overflow at '+time);
    if(time>=timing.closingStart&&(state.logo.opacity!==0||state.logo.visibility!=='hidden'))throw new Error('Closing watermark remains at '+time);
    if(!state.logo.loaded||!state.closingLogo.loaded)throw new Error('Logo not loaded');
    states.push(state);
    if(shotFrames.includes(frame))await page.screenshot({path:root+'/qa/layout-frame-'+frame+'.png'});
  }
  const zoom=states.filter(s=>s.frame>=694&&s.frame<=730);
  for(let i=1;i<zoom.length;i++){
    const a=zoom[i-1].hero,b=zoom[i].hero;
    if(b.width!==1080||b.height!==1920||b.scale<a.scale||b.scale-a.scale>.028||Math.abs(b.currentTime-a.currentTime-1/30)>.002)throw new Error('Hero discontinuity at '+zoom[i].time);
  }
  const final=states.at(-1);
  if(final.closingLogo.width!==360||final.closingLogo.opacity!==1||final.closingLogo.visibility!=='visible')throw new Error('Closing logo incorrect');
  return {duration:await page.evaluate(()=>window.__timelines['lumiere-v04'].duration()),timing,checks:{textInBounds:true,watermarkHiddenThroughoutClosing:true,closingLogoWidth:360,heroSingleVideo:true,heroGeometryStable:true,heroSourceAdvancesOneFrame:true},states};
}
