async page => {
  const root='/Users/lucasnguyen/Developer/lumiere-arts/products/01-vung-song-2/versions/v03-art-in-motion';
  await page.goto('http://127.0.0.1:4813/source/index.html');
  await page.setViewportSize({width:1080,height:1920});
  await page.evaluate(()=>document.fonts.ready);
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  for(const time of [0,2,5,7.5,11.5,15.7,19.5,23.5]){
    await page.evaluate(async t=>{
      window.__timelines['lumiere-vung-song-2-v03'].seek(t);
      await Promise.all([...document.querySelectorAll('video')].map(async v=>{
        const start=Number(v.dataset.start),end=start+Number(v.dataset.duration);
        if(t<start||t>=end)return;
        if(v.readyState<2)await new Promise(r=>v.addEventListener('loadeddata',r,{once:true}));
        const desired=t-start;
        if(Math.abs(v.currentTime-desired)<.001)return;
        await new Promise(r=>{v.addEventListener('seeked',r,{once:true});v.currentTime=desired;});
      }));
    },time);
    await page.screenshot({path:root+'/qa/layout-'+String(time)+'.png'});
  }
  return {errors,duration:await page.evaluate(()=>window.__timelines['lumiere-vung-song-2-v03'].duration())};
}
