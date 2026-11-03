async page => {
  await page.setViewportSize({width:1080,height:1920});
  const root='/Users/lucasnguyen/Developer/lumiere-arts/products/01-vung-song-2/versions/v03-art-in-motion';
  for(const plate of ['opening-a','opening-b','signature-a','signature-b']){
    await page.goto('http://127.0.0.1:4813/source/type-layers.html?plate='+plate);
    await page.evaluate(()=>document.fonts.ready);
    await page.screenshot({path:root+'/source/assets/images/'+plate+'.png',omitBackground:true});
  }
  return 'Four transparent typography plates saved.';
}
