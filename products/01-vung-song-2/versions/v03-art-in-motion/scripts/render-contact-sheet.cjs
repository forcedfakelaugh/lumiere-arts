const fs=require('fs'),path=require('path');
const sharp=require('../source/node_modules/sharp');
const root=path.resolve(__dirname,'..');
const times=JSON.parse(fs.readFileSync(path.join(root,'qa/verification.json'),'utf8')).sampled_times;
(async()=>{
  const selected=[2,3,7,11,15,18,20,22],w=270,h=480,label=30,head=76,parts=[];
  for(const [n,i] of selected.entries()){
    const t=times[i],filename=`${String(i).padStart(2,'0')}-${t.toFixed(3)}s.jpg`;
    const x=n%4*w,y=head+Math.floor(n/4)*(h+label);
    parts.push({input:await sharp(path.join(root,'qa/rendered-frames',filename)).resize(w,h).toBuffer(),left:x,top:y});
    parts.push({input:Buffer.from(`<svg width="270" height="30"><text x="12" y="21" fill="#dbc9a6" font-family="Arial" font-size="14">${t.toFixed(2)} s</text></svg>`),left:x,top:y+h});
  }
  parts.push({input:Buffer.from('<svg width="1080" height="76"><text x="20" y="32" fill="#fff7e6" font-family="Georgia" font-size="26">LUMIERE ARTS · Vùng Sống 2 · Art in Motion</text><text x="20" y="57" fill="#dbc9a6" font-family="Arial" font-size="15">V03 / 24 seconds / 1080 × 1920 / 30 fps / Moving foreground masks</text></svg>'),left:0,top:0});
  await sharp({create:{width:1080,height:1096,channels:3,background:'#153b3e'}}).composite(parts).jpeg({quality:94}).toFile(path.join(root,'exports/Lumiere-Arts-01-Vung-Song-2-V03-Contact-Sheet.jpg'));
})();
