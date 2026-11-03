"""Rebuild moving typography behind the real subject. Requires saved matte/plates."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
assets = root / 'source/assets'
for shot, duration, motion_a, motion_b in [
    ('opening', 6, '28-10*t', '-28+10*t'),
    ('signature', 4, '-50+25*t', '44-22*t'),
]:
    # Restore the original subject over graded footage and two drifting titles.
    # Contract uncertain gray fringe slightly, fill internal pinholes, retain a
    # subpixel antialiased silhouette. All inputs share the exact 30 fps edit.
    graph = (
        '[0:v]split[background][person];'
        '[background]drawbox=x=0:y=0:w=iw:h=ih:color=0x082e34@0.42:t=fill[graded];'
        '[1:v]scale=1080:1920:flags=lanczos,format=gray,'
        "lut=y='clip((val-28)*255/160,0,255)',gblur=sigma=0.6[mask];"
        '[person][mask]alphamerge[foreground];'
        f'[2:v]format=rgba,fade=t=in:st=0:d=0.48:alpha=1,fade=t=out:st={duration-0.5}:d=0.5:alpha=1[a];'
        f'[3:v]format=rgba,fade=t=in:st=0.18:d=0.6:alpha=1,fade=t=out:st={duration-0.5}:d=0.5:alpha=1[b];'
        f"[graded][a]overlay=x='{motion_a}':y=0:shortest=1[first];"
        f"[first][b]overlay=x='{motion_b}':y=0:shortest=1[lettered];"
        '[lettered][foreground]overlay=shortest=1,format=yuv420p[out]'
    )
    cmd = ['ffmpeg','-y','-v','warning','-i',str(assets/f'video/{shot}-clean.mp4'),
           '-i',str(assets/f'masks/{shot}-mask.mp4'),
           '-loop','1','-framerate','30','-i',str(assets/f'images/{shot}-a.png'),
           '-loop','1','-framerate','30','-i',str(assets/f'images/{shot}-b.png'),
           '-filter_complex',graph,'-map','[out]','-an','-t',str(duration),
           '-r','30','-c:v','libx264','-preset','fast','-crf','16',
           '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
           '-movflags','+faststart',str(assets/f'video/{shot}-depth.mp4')]
    subprocess.run(cmd, check=True)
    print(f'{shot}: {duration * 30} composited frames', flush=True)
