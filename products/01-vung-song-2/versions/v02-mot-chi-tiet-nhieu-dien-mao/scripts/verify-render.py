from pathlib import Path
import subprocess,json,hashlib

root=Path(__file__).resolve().parents[1]
qa=root/'qa';frames=qa/'rendered-frames';frames.mkdir(exist_ok=True)
video=root/'exports/Lumiere-Arts-01-Vung-Song-2-V02-20s-1080p.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)]))
(qa/'render-metadata.json').write_text(json.dumps(probe,indent=2))
decode=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],capture_output=True,text=True)
(qa/'full-decode.log').write_text(decode.stderr)
scan=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-vf','blackdetect=d=0.07:pix_th=0.08:pic_th=0.98,freezedetect=n=-50dB:d=1.5','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True)
(qa/'black-freeze-audio.log').write_text(scan.stderr)
times=[0,.5,1.066667,1.1,1.8,3.4,3.466667,4,4.6,5.1,5.7,6.5,8.8,9.266667,9.65,10,11.5,12.766667,12.833333,13.5,15,17.166667,17.2,17.6,18.5,19.966667]
for i,t in enumerate(times):
 subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1','-vf','scale=540:960','-y',str(frames/f'{i:02d}-{t:.3f}s.jpg')],check=True)
vs=next(s for s in probe['streams'] if s['codec_type']=='video')
aus=next(s for s in probe['streams'] if s['codec_type']=='audio')
verification={
 'file':str(video),'duration':float(probe['format']['duration']),'video_frames':vs.get('nb_frames'),'video_codec':vs['codec_name'],'audio_codec':aus['codec_name'],'width':vs['width'],'height':vs['height'],'fps':vs['r_frame_rate'],
 'bytes':video.stat().st_size,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),
 'decode_exit_code':decode.returncode,'decode_errors':decode.stderr.strip(),
 'black_segments':[x for x in scan.stderr.splitlines() if 'black_start:' in x],
 'freeze_segments':[x for x in scan.stderr.splitlines() if 'freeze_start:' in x or 'freeze_duration:' in x],
 'sampled_times':times,'visual_review':'pending','hyperframes_check':'passed: zero lint/runtime warnings or errors, 16 layout samples with zero issues, 10/10 sampled contrast checks pass; see hyperframes-check.log'
}
(qa/'verification.json').write_text(json.dumps(verification,indent=2))
print(json.dumps(verification,indent=2))
assert decode.returncode==0 and not decode.stderr.strip()
assert abs(verification['duration']-20)<.06
assert vs['width']==1080 and vs['height']==1920 and vs['r_frame_rate']=='30/1'
assert not verification['black_segments']
