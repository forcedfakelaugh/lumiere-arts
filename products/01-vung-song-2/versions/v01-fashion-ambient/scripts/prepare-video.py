from pathlib import Path
import subprocess,json
root=Path(__file__).resolve().parents[1]
media=root.parents[1]/'assets/originals/2026-11-02/04-video'
out=root/'source/assets/video'
out.mkdir(parents=True,exist_ok=True)
records=[]
for f in sorted(media.glob('*.mp4')):
 dest=out/f.name.replace('-4k','-1080p')
 log=root/'qa'/f'{f.stem}-transcode.log'
 cmd=['ffmpeg','-y','-v','warning','-i',str(f),'-map','0:v:0','-an','-vf','scale=1080:1920:flags=lanczos,setsar=1','-r','30','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart','-metadata:s:v:0','rotate=0',str(dest)]
 with log.open('w') as handle:r=subprocess.run(cmd,stdout=handle,stderr=handle)
 if r.returncode:raise RuntimeError(f'Failed transcode {f}')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]))
 records.append({'source':str(f),'proxy':str(dest),'metadata':probe})
 print(dest.name,probe['format']['duration'],flush=True)
(root/'qa/proxy-manifest.json').write_text(json.dumps(records,indent=2))
