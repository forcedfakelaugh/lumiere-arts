async page => {
  await page.setViewportSize({width:1080,height:1920});
  await page.goto('http://127.0.0.1:4814/source/index.html');
  await page.evaluate(()=>document.fonts.ready);
  await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
  const root='/Users/lucasnguyen/Developer/lumiere-arts/products/01-vung-song-2/versions/v04-stop-motion';
  const states=[];
  for(const time of [.8,1.4,2.4,3.4,6.8,9.4,10.4,11.4,12.4,14.5,16.8,19.5]){
    const state=await page.evaluate(t=>{
      window.__timelines['lumiere-vung-song-2-v04'].seek(t);
      const active=[...document.querySelectorAll('.scene')].filter(s=>getComputedStyle(s).opacity==='1');
      return {time:t,scene:active.map(s=>s.id),poses:active.flatMap(s=>[...s.querySelectorAll('.pose')].filter(p=>getComputedStyle(p).opacity==='1').map(p=>p.id))};
    },time);
    states.push(state);
    await page.screenshot({path:root+'/qa/layout-'+time+'.png'});
  }
  return {states,videoElements:await page.locator('video').count()};
}
