"""Author V04 from the preserved editorial layout, using only frozen photographs."""
from pathlib import Path
import re,json

root=Path(__file__).resolve().parents[1]
old=root.parent/'v03-art-in-motion/source'
html=(old/'index.html').read_text()
html=html.replace('Art in Motion','Nhịp riêng').replace('lumiere-vung-song-2-v03','lumiere-vung-song-2-v04')
html=html.replace('data-duration="24"','data-duration="20"')
def stack(scene, count, start, duration, depth=False):
    parts=[]
    for i in range(1,count+1):
        name=f'{scene}-{i:02}'
        attrs=f'data-start="{start}" data-duration="{duration}"'
        parts.append(f'<div id="{name}" class="pose" data-layout-ignore>')
        parts.append(f'<img id="{name}-photo" class="footage pose-back" src="assets/poses/{name}.png" alt="Tư thế {i}, khăn Vùng Sống 2" {attrs}>')
        if depth:
            a,b=('VÙNG','SỐNG') if scene=='opening' else ('NÉT','RIÊNG')
            parts.append(f'<div class="depth-type" aria-hidden="true" data-layout-allow-occlusion><p class="type-a" data-layout-allow-occlusion>{a}</p><p class="type-b" data-layout-allow-occlusion>{b}</p></div>')
            parts.append(f'<img id="{name}-front" class="footage pose-front" src="assets/poses/{name}-foreground.webp" alt="" {attrs}>')
        parts.append('</div>')
    return '\n'.join(parts)
for scene,count,start,duration,depth in [('opening',4,0,5,True),('gesture',8,5,4,False),('signature',4,9,4,True),('closing',3,16,4,False)]:
    html=re.sub(fr'<video id="{scene}-video".*?</video>',stack(scene,count,start,duration,depth),html)
html=html.replace('data-start="14" data-duration="4"','data-start="13" data-duration="3"')
html=html.replace('assets/music/art-in-motion-24s.wav','assets/music/stop-motion-20s.wav')
html=html.replace('Nghệ thuật<br>trên lụa.','Nghệ thuật<br>có nhịp riêng.')
html=html.replace('Theo từng<br>chuyển động.','Một chiếc khăn.<br>Nhiều nét riêng.')
html=html.replace('MỘT CHUYỂN ĐỘNG. MỘT NÉT RIÊNG.','VÙNG SỐNG 2 · NGUYỄN VĂN TRINH')
css='''
.pose{position:absolute;inset:0;opacity:0;isolation:isolate;z-index:0}
#opening-01{opacity:1}
.scene > :not(.pose){z-index:3}
.pose-back{z-index:0}.pose-front{z-index:2}
.depth-type{position:absolute;inset:0;z-index:1;color:#153e43;pointer-events:none}
.depth-type p{position:absolute;width:1080px;text-align:center;line-height:1;letter-spacing:-8px}
.type-a{top:338px;font-size:304px}.type-b{top:754px;font-size:314px}
#signature .type-a{top:320px;font-size:350px}
#signature .type-b{top:1232px;font-size:273px;letter-spacing:-6px}
#opening-copy{top:1480px;font-size:77px}
#gesture-title{font-size:89px}
#signature-note{top:1588px;font-size:72px}
#origin-heading{top:339px}
#opening .shade,#signature .shade{background:linear-gradient(180deg,rgba(8,34,37,.62),transparent 19%,transparent 68%,rgba(8,34,37,.8))}
#gesture .shade{background:linear-gradient(180deg,rgba(8,34,37,.6),transparent 22%,transparent 54%,rgba(8,34,37,.8))}
'''
html=html.replace('</style>',css+'\n</style>')
script='''
window.__timelines=window.__timelines||{};
const tl=gsap.timeline({paused:true});
const cut=(a,b,t)=>tl.set(a,{opacity:0},t).set(b,{opacity:1},t);
function poses(scene,sequence,start,hold){
  sequence.forEach((number,i)=>{
    const at=start+i*hold;
    if(scene==='opening' && i===0)return;
    tl.set('#'+scene+' .pose',{opacity:0},at)
      .set('#'+scene+'-'+String(number).padStart(2,'0'),{opacity:1},at);
  });
}
poses('opening',[1,2,3,4,2],0,1);
poses('gesture',[1,2,3,4,5,6,7,8],5,.5);
poses('signature',[1,2,3,4],9,1);
poses('closing',[1,2,3],16,1);
// The lettering advances on held steps; photo and mask never move independently.
tl.fromTo('#opening .type-a',{x:24},{x:-24,duration:5,ease:'steps(10)'},0)
  .fromTo('#opening .type-b',{x:-24},{x:24,duration:5,ease:'steps(10)'},0)
  .from('#opening-copy,#opening-no',{opacity:0,y:20,duration:.4,ease:'steps(2)'},.2)
  .from('#opening-rule,#opening-bottom',{opacity:0,duration:.4,ease:'steps(2)'},.6);
cut('#opening','#gesture',5);
tl.from('#gesture-title',{opacity:0,y:22,duration:.4,ease:'steps(2)'},5.1)
  .from('#gesture-index',{opacity:0,duration:.2,ease:'steps(1)'},5.4);
cut('#gesture','#signature',9);
tl.fromTo('#signature .type-a',{x:-26},{x:26,duration:4,ease:'steps(8)'},9)
  .fromTo('#signature .type-b',{x:26},{x:-26,duration:4,ease:'steps(8)'},9)
  .from('#signature-note,#signature-label',{opacity:0,y:16,duration:.4,ease:'steps(2)'},9.2);
cut('#signature','#origin',13);
tl.from('#origin-kicker,#origin-heading',{opacity:0,y:16,duration:.3,ease:'steps(2)'},13)
  .from('#art-frame',{opacity:0,y:20,duration:.3,ease:'steps(2)'},13.1)
  .from('#origin-title,#origin-artist,#origin-explanation,#origin-rule',{opacity:0,duration:.3,ease:'steps(2)'},13.2)
  .from('#silk-frame,#silk-label',{opacity:0,duration:.3,ease:'steps(2)'},13.35);
cut('#origin','#closing',16);
tl.from('#closing-line,#closing-small',{opacity:0,y:20,duration:.4,ease:'steps(2)'},16.1)
  .set('#closing-line,#closing-small',{opacity:0},18)
  .from('#endcard',{y:700,duration:.4,ease:'steps(3)'},18)
  .from('#end-logo,#end-title,#end-product,#end-rule,#end-url,#end-caption',{opacity:0,y:16,duration:.4,ease:'steps(2)'},18.25)
  .set({}, {},20);
window.__timelines['lumiere-vung-song-2-v04']=tl;
'''
html=re.sub(r'<script>\s*window.__timelines.*?</script>','<script>'+script+'</script>',html,flags=re.S)
(root/'source/index.html').write_text(html)
package={'name':'lumiere-arts-vung-song-2-v04','private':True,'scripts':{
    'check':'HYPERFRAMES_NO_TELEMETRY=1 hyperframes check --at 0,0.7,1.4,2.4,3.4,4.4,5,6.3,7.8,8.9,9.4,10.4,11.4,12.4,13,14.5,15.9,16.5,18.3,19.8 --snapshots',
    'preview':'HYPERFRAMES_NO_TELEMETRY=1 hyperframes preview --background',
    'render':'HYPERFRAMES_NO_TELEMETRY=1 hyperframes render --fps 30 --quality delivery --workers 2 --output ../exports/Lumiere-Arts-01-Vung-Song-2-V04-Stop-Motion-20s-1080p.mp4'},
    'dependencies':{'hyperframes':'0.8.162'}}
(root/'source/package.json').write_text(json.dumps(package,indent=2)+'\n')
p=root/'source/package-lock.json';d=json.loads(p.read_text());d['name']=package['name'];d['packages']['']['name']=package['name'];p.write_text(json.dumps(d,indent=2)+'\n')
(root/'source/meta.json').write_text(json.dumps({'id':'lumiere-vung-song-2-v04','name':'Lumiere Arts | Vùng Sống 2 | V04 | Nhịp riêng'},ensure_ascii=False)+'\n')
print('Authored 20-second photo-stop-motion composition; no video elements.')
