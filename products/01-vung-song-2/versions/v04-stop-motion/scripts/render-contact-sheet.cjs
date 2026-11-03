const fs=require('fs'),path=require('path'),sharp=require('../source/node_modules/sharp');
const root=path.resolve(__dirname,'..'),times=JSON.parse(fs.readFileSync(path.join(root,'qa/verification.json'),'utf8')).sampled_times;
(async()=>{
 for(const [name,indices,w,cols,head] of [['exports/Lumiere-Arts-01-Vung-Song-2-V04-Contact-Sheet.jpg',[1,2,4,10,17,19,22,28],270,4,76],['qa/transition-sheet.jpg',times.map((_,i)=>i),180,6,0]]){
  const h=w*16/9,label=28,parts=[];
  for(const [n,i] of indices.entries()){
   const x=n%cols*w,y=head+Math.floor(n/cols)*(h+label),file=`${String(i).padStart(2,'0')}-${times[i].toFixed(3)}s.jpg`;
   parts.push({input:await sharp(path.join(root,'qa/rendered-frames',file)).resize(w,h).toBuffer(),left:x,top:y});
   parts.push({input:Buffer.from(`<svg width="${w}" height="28"><text x="10" y="20" fill="#ead8b6" font-family="Arial" font-size="14">${times[i].toFixed(2)} s</text></svg>`),left:x,top:y+h});
  }
  if(head)parts.push({input:Buffer.from('<svg width="1080" height="76"><text x="20" y="32" fill="#fff7e6" font-family="Georgia" font-size="26">LUMIERE ARTS · Vùng Sống 2 · Nhịp riêng</text><text x="20" y="57" fill="#dbc9a6" font-family="Arial" font-size="15">V04 / Photo stop-motion / 20 seconds / 1080 × 1920 / 30 fps</text></svg>'),left:0,top:0});
  await sharp({create:{width:w*cols,height:head+Math.ceil(indices.length/cols)*(h+label),channels:3,background:'#153b3e'}}).composite(parts).jpeg({quality:93}).toFile(path.join(root,name));
 }
})();
