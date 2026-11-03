import sys,subprocess,math
from pathlib import Path
sys.path.insert(0,'work/python')
import imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont,ImageOps
F=imageio_ffmpeg.get_ffmpeg_exe(); W,H=1080,1920
A=Path('/Users/linh/Desktop/lumiere-arts/products/01-vung-song-2/versions/v02-mot-chi-tiet-nhieu-dien-mao/source/assets'); V=A/'video'; I=A/'images'; OUT=Path('outputs'); T=Path('work')
cream='#f1ebdf'; teal='#193e43';gold='#ad9367'
font='/System/Library/Fonts/Supplemental/Times New Roman.ttf'
def txt(d,xy,s,size=46,fill=teal):d.text(xy,s,font=ImageFont.truetype(font,size),fill=fill)
def base():return Image.new('RGB',(W,H),cream)
def header(im,light=False):txt(ImageDraw.Draw(im),(72,150),'L U M I E R E   A R T S',30,'#fff9ec' if light else teal)
def overlay(n,lines):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 for y in range(1150,H):d.line((0,y,W,y),fill=(7,28,30,int(210*(y-1150)/(H-1150))))
 header(im,True)
 for y,s,sz in lines:txt(d,(72,y),s,sz,'#fff9ec')
 im.save(T/f'{n}.png');return T/f'{n}.png'
def run(args):
 r=subprocess.run([F,'-y','-loglevel','error',*map(str,args)],capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode())
def encode(n,src,start,dur,ov=None,still=False):
 inp=['-loop','1','-i',src] if still else ['-ss',start,'-i',src]
 filt='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30'
 if ov: inp+=['-i',ov];opts=['-filter_complex',f'[0:v]{filt}[v];[v][1:v]overlay=0:0[out]','-map','[out]']
 else:opts=['-vf',filt]
 run([*inp,*opts,'-t',dur,'-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',T/f'{n}.mp4'])
 print(n,flush=True)
# Continuous detail to complete artwork, with a held information card.
p=subprocess.Popen([F,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',str(T/'01.mp4')],stdin=subprocess.PIPE)
art=Image.open(I/'la-vung-song-2-artwork-landscape.jpg').convert('RGB')
for f in range(210):
 t=f/30;u=min(1,t/3.5);u=u*u*(3-2*u);im=base();width=int(3600+(936-3600)*u);ah=int(width*art.height/art.width);im.paste(art.resize((width,ah),Image.Resampling.LANCZOS),((W-width)//2,820-ah//2));header(im);d=ImageDraw.Draw(im)
 if t>=2.8:
  txt(d,(72,360),'Vùng Sống 2',104);txt(d,(76,490),'Nguyễn Văn Trinh',46)
  txt(d,(76,1220),'Màu nước trên lụa',46);txt(d,(76,1290),'100 × 200 cm  ·  2023',40)
  d.line((76,1410,200,1410),fill=gold,width=2);txt(d,(76,1470),'Từ một phần nguyên tác,',44);txt(d,(76,1530),'một hành trình mới trên lụa.',44)
 p.stdin.write(im.tobytes())
p.stdin.close();assert p.wait()==0;print('01',flush=True)
ov=overlay('gallery',[(1480,'Từ không gian nghệ thuật…',57),(1590,'Tư liệu triển lãm bộ Vùng Sống',32)])
encode('02',I/'la-gallery-interior-wide.jpg',0,3,ov,True)
ov=overlay('print1',[(1470,'…đến từng thước lụa.',65)])
encode('03','/Users/linh/Downloads/WhatsApp Video 2026-11-02 at 21.26.08.mp4',2,3,ov)
ov=overlay('print2',[(1450,'Họa tiết được in lên lụa,',56),(1525,'tiếp nối sắc màu của tranh.',52)])
encode('04','/Users/linh/Downloads/sen đỏ.mp4',8,3,ov)
ov=overlay('unfold',[(1400,'Một chi tiết.',86),(1530,'Chuyển thể từ một phần Vùng Sống 2',36)])
encode('05',V/'la-scarf-01-unfold-front-1080p.mp4',3.2,4,ov)
# Three simultaneous moving looks, with uncut portraits within each window.
b=base();header(b);d=ImageDraw.Draw(b);txt(d,(72,290),'VÙNG SỐNG 2',35);txt(d,(72,1530),'Nhiều diện mạo.',88);b.save(T/'triptych.png')
args=['-loop','1','-i',T/'triptych.png']
for n,s in [('04-head-wrap-closeup',1.3),('02-shoulder-drape',1.3),('06-riverside-portrait',.7)]:args+=['-ss',s,'-i',V/f'la-scarf-{n}-1080p.mp4']
filt=';'.join(f'[{i}:v]scale=300:980:force_original_aspect_ratio=increase,crop=300:980,setsar=1,fps=30[p{i}]' for i in range(1,4))+';[0:v][p1]overlay=72:470[a];[a][p2]overlay=390:470[b];[b][p3]overlay=708:470[out]'
run([*args,'-filter_complex',filt,'-map','[out]','-t',5,'-an','-c:v','libx264','-preset','fast','-crf',19,'-pix_fmt','yuv420p',T/'06.mp4']);print('06',flush=True)
ov=overlay('silk',[(1400,'100% lụa tơ tằm',68),(1485,'Bảo Lộc',84),(1610,'Satin 16 momme · Viền thủ công',36)])
encode('07',V/'la-scarf-06-riverside-portrait-1080p.mp4',6,4,ov)
im=Image.new('RGB',(W,H),teal);logo=Image.open(A/'lumiere-official-logo.jpg');logo.thumbnail((420,330));im.paste(logo,((W-logo.width)//2,480));d=ImageDraw.Draw(im);txt(d,(220,980),'The Art of Silk',94,'#fff9ec');txt(d,(315,1130),'Vùng Sống 2',62,'#e2c99a');txt(d,(242,1500),'lumierearts.com',52,'#fff9ec');im.save(T/'end.png');encode('08',T/'end.png',0,3,None,True)
(T/'concat.txt').write_text(''.join(f"file '{i:02}.mp4'\n" for i in range(1,9)))
run(['-f','concat','-safe',0,'-i',T/'concat.txt','-ss',6.6,'-i',A/'music/rockot-slow-motion-fashion-ambient.mp3','-map','0:v','-map','1:a','-c:v','copy','-af','afade=t=in:d=0.6,afade=t=out:st=30:d=2','-t',32,'-c:a','aac','-b:a','192k','-movflags','+faststart',OUT/'Lumiere-Vung-Song-2-V03.mp4'])
print('DONE',flush=True)
