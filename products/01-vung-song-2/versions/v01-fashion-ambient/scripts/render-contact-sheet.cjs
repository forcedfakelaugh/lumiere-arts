const fs=require('fs'),path=require('path');
const sharp=require('../source/node_modules/sharp');
const root=path.resolve(__dirname,'..');
const dir=path.join(root,'qa/rendered-frames');
const all=JSON.parse(fs.readFileSync(path.join(root,'qa/verification.json'),'utf8')).sampled_times.map((t,i)=>`${String(i).padStart(2,'0')}-${t.toFixed(3)}s.jpg`);
(async()=>{
 for(const [name,files,w,cols] of [
  ['Lumiere-Arts-Vung-Song-2-Fashion-Ambient-Contact-Sheet.jpg',[1,3,8,12,16,20,23,26].map(i=>all[i]),270,4],
  ['transition-sheet.jpg',all,180,6]
 ]){
  const h=Math.round(w*1920/1080),label=30,head=66,parts=[];
  for(const [i,f] of files.entries()){
   const x=i%cols*w,y=head+Math.floor(i/cols)*(h+label);
   parts.push({input:await sharp(path.join(dir,f)).resize(w,h).toBuffer(),left:x,top:y});
   parts.push({input:Buffer.from(`<svg width="${w}" height="30"><text x="10" y="21" fill="#e8d4b4" font-family="Arial" font-size="15">${f.slice(3,-4)}</text></svg>`),left:x,top:y+h});
  }
  parts.push({input:Buffer.from(`<svg width="${w*cols}" height="66"><text x="18" y="29" font-family="Georgia" font-size="25" fill="#f5ecdc">LUMIERE ARTS | Vùng Sống 2</text><text x="18" y="51" font-family="Arial" font-size="15" fill="#d0b282">20 seconds · 1080 × 1920 · 30 fps · Hyperframes</text></svg>`),left:0,top:0});
  await sharp({create:{width:w*cols,height:head+Math.ceil(files.length/cols)*(h+label),channels:3,background:'#15383d'}}).composite(parts).jpeg({quality:92}).toFile(path.join(root,name.startsWith('Lumiere')?'exports':'qa',name));
 }
})();
