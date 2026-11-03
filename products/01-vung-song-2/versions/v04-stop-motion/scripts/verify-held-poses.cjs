const fs=require('fs'),path=require('path'),{execFileSync}=require('child_process');
const sharp=require('../source/node_modules/sharp');
const root=path.resolve(__dirname,'..'),video=path.join(root,'exports/Lumiere-Arts-01-Vung-Song-2-V04-Stop-Motion-20s-1080p.mp4');
const dir=path.join(root,'qa/held-frames');fs.mkdirSync(dir,{recursive:true});
(async()=>{
 const result=[];
 for(const [shot,start] of [['opening',0],['signature',9]]){
  for(let i=0;i<4;i++){
   const id=`${shot}-${String(i+1).padStart(2,'0')}`,t=start+i;
   const pair=[];
   for(const [index,delta] of [.633333,.833333].entries()){
    const file=path.join(dir,`${id}-${index}.png`);
    execFileSync('ffmpeg',['-v','error','-y','-ss',String(t+delta),'-i',video,'-frames:v','1',file]);
    pair.push(await sharp(file).removeAlpha().raw().toBuffer());
   }
   const fg=await sharp(path.join(root,'source/assets/poses',id+'-foreground.webp')).ensureAlpha().raw().toBuffer();
   const clean=await sharp(path.join(root,'source/assets/poses',id+'.png')).removeAlpha().raw().toBuffer();
   let sum=0,count=0,sourceError=0,renderReferenceError=0;
   for(let y=400;y<1200;y++)for(let x=0;x<1080;x++){
    const p=y*1080+x;if(fg[p*4+3]<254)continue;
    for(let c=0;c<3;c++){
     sum+=Math.abs(pair[0][p*3+c]-pair[1][p*3+c]);
     sourceError+=Math.abs(fg[p*4+c]-clean[p*3+c]);count++;
     renderReferenceError+=Math.abs(pair[0][p*3+c]-clean[p*3+c]);
    }
   }
   const mean=sum/count;
   const item={pose:id,times:[t+.633333,t+.833333],sampled_channels:count,mean_absolute_render_difference:mean,foreground_rgb_source_difference:sourceError/count,mean_render_reference_difference:renderReferenceError/count};
   result.push(item);
   if(mean>1.5||sourceError!==0||renderReferenceError/count>8)throw new Error('Held pose failed: '+JSON.stringify(item));
  }
 }
 fs.writeFileSync(path.join(root,'qa/hold-stability.json'),JSON.stringify(result,null,2)+'\n');
 const file=path.join(root,'qa/verification.json'),record=JSON.parse(fs.readFileSync(file));
 record.hold_stability={checked_poses:result.length,max_mean_absolute_render_difference:Math.max(...result.map(x=>x.mean_absolute_render_difference)),foreground_rgb_matches_original:true,details:result};
 fs.writeFileSync(file,JSON.stringify(record,null,2)+'\n');
 console.log(JSON.stringify(result,null,2));
})();
