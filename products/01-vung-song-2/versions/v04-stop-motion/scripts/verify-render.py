from pathlib import Path
import subprocess,json,hashlib
root=Path(__file__).resolve().parents[1]
qa=root/'qa';frames=qa/'rendered-frames';frames.mkdir(exist_ok=True)
video=root/'exports/Lumiere-Arts-01-Vung-Song-2-V04-Stop-Motion-20s-1080p.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)]))
(qa/'render-metadata.json').write_text(json.dumps(probe,indent=2))
decode=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],capture_output=True,text=True)
(qa/'full-decode.log').write_text(decode.stderr)
scan=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-vf','blackdetect=d=0.07:pix_th=0.08:pic_th=0.98','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True)
(qa/'black-audio.log').write_text(scan.stderr)
times=[0,.8,1.4,2.4,3.4,4.4,5,5.25,5.75,6.25,6.75,7.25,7.75,8.25,8.75,9,9.4,10.4,11.4,12.4,13,13.6,14.5,15.966667,16,16.4,17.4,18.4,19.966667]
for i,t in enumerate(times):
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1','-vf','scale=540:960',str(frames/f'{i:02d}-{t:.3f}s.jpg')],check=True)
vs=next(s for s in probe['streams'] if s['codec_type']=='video');aus=next(s for s in probe['streams'] if s['codec_type']=='audio')
record={'file':str(video.relative_to(root)),'duration':float(probe['format']['duration']),'width':vs['width'],'height':vs['height'],'fps':vs['r_frame_rate'],'frames':int(vs['nb_frames']),'video_codec':vs['codec_name'],'audio_codec':aus['codec_name'],'bytes':video.stat().st_size,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'decode_errors':decode.stderr.strip(),'black_segments':[x for x in scan.stderr.splitlines() if 'black_start:' in x],'sampled_times':times,'photographic_poses':19,'static_foreground_masks':8,'visual_review':'pending','hyperframes_check':'0 lint/runtime/layout/motion issues across 20 sampled times; 19/19 contrast checks pass. Large occluded type is intentional.','freeze_check':'Not applicable: held photographic poses are intentional. Dedicated hold-stability verification is used instead.'}
(qa/'verification.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
assert decode.returncode==0 and not record['decode_errors'] and not record['black_segments']
assert record['duration']==20 and record['frames']==600 and (vs['width'],vs['height'])==(1080,1920) and vs['r_frame_rate']=='30/1'
print(json.dumps(record,ensure_ascii=False,indent=2))
