const fs=require('fs'),path=require('path');
const sharp=require('../source/node_modules/sharp');
const root=path.resolve(__dirname,'..');
(async()=>{
  const poses=JSON.parse(fs.readFileSync(path.join(root,'source/poses.json'),'utf8'));
  for(const pose of poses.filter(p=>p.static_mask)){
    const input=path.join(root,'source/assets/poses',pose.id+'.png');
    const mask=await sharp(path.join(root,'source/assets/masks',pose.id+'-mask.png')).greyscale().threshold(112).blur(.5).raw().toBuffer();
    const rgb=await sharp(input).removeAlpha().raw().toBuffer();
    await sharp(rgb,{raw:{width:1080,height:1920,channels:3}}).joinChannel(mask,{raw:{width:1080,height:1920,channels:1}}).webp({lossless:true,effort:6}).toFile(path.join(root,'source/assets/poses',pose.id+'-foreground.webp'));
  }
  const selected=poses.filter(p=>p.static_mask),parts=[];
  for(const [i,pose] of selected.entries()){
    parts.push({input:await sharp(path.join(root,'source/assets/poses',pose.id+'-foreground.webp')).resize(270,480).toBuffer(),left:i%4*270,top:Math.floor(i/4)*520});
    parts.push({input:Buffer.from(`<svg width="270" height="40"><text x="12" y="25" fill="white" font-size="17" font-family="Arial">${pose.id}</text></svg>`),left:i%4*270,top:Math.floor(i/4)*520+480});
  }
  await sharp({create:{width:1080,height:1040,channels:3,background:'#673c56'}}).composite(parts).jpeg({quality:94}).toFile(path.join(root,'qa/static-cutout-sheet.jpg'));
})();
