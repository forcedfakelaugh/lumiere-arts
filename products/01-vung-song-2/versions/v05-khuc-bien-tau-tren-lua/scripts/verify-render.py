from pathlib import Path
import array
import hashlib
import json
import math
import subprocess
from beat_analysis import analyze, authored_hits, align

root = Path(__file__).resolve().parents[1]
video = root / 'exports/Lumiere-Arts-V05-Showcase-24s-1080p.mp4'
qa = root / 'qa'
frames = qa / 'rendered-frames'
frames.mkdir(exist_ok=True)
source = root / 'source/index.html'
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(video)]))
vs = next(s for s in probe['streams'] if s['codec_type'] == 'video')
aus = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
decode = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-f', 'null', '-'], capture_output=True, text=True)
scan = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(video), '-vf', 'blackdetect=d=0.03:pix_th=0.08:pic_th=0.98', '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True)
(qa / 'decode.log').write_text(decode.stderr)
(qa / 'black-audio.log').write_text(scan.stderr)


def pcm(args):
    result = subprocess.check_output(['ffmpeg', '-v', 'error', *args, '-t', '24', '-ac', '1', '-ar', '8000', '-f', 'f32le', '-'])
    samples = array.array('f')
    samples.frombytes(result)
    return samples


song = root / 'source/assets/music/rockot-slow-motion-fashion-ambient.mp3'
reference = pcm(['-ss', '6.6', '-i', str(song), '-af', 'volume=0.8'])
actual = pcm(['-i', str(video), '-vn'])
n = min(len(reference), len(actual))
correlation = sum(reference[i] * actual[i] for i in range(n)) / math.sqrt(sum(x*x for x in reference[:n]) * sum(x*x for x in actual[:n]))
hits = authored_hits(source.read_text())
source_peaks = analyze(song, offset=6.6, volume=.8, duration=24)
rendered_peaks = analyze(video, duration=24)
transitions = align(hits, source_peaks)
rendered_transitions = align(hits, rendered_peaks)
beat_record = {
    'method': 'Percussive band 180-4000 Hz; 5 ms RMS; positive novelty against previous 25 ms; local maxima and 200 ms non-maximum suppression. Markers read from source/index.html; detected attacks are computed independently over the entire audio.',
    'music_offset_seconds': 6.6, 'volume': .8, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'source_transitions': transitions, 'rendered_transitions': rendered_transitions,
    'all_source_attacks': source_peaks, 'all_rendered_attacks': rendered_peaks,
}
(qa / 'beat-analysis.json').write_text(json.dumps(beat_record, ensure_ascii=False, indent=2) + '\n')


def frame_at(frame, path, width=270):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{frame/30:.9f}', '-i', str(video), '-frames:v', '1', '-vf', f'scale={width}:-1', str(path)], check=True)


def sheet(frame_numbers, folder, output, columns=5):
    folder.mkdir(exist_ok=True)
    for i, frame in enumerate(frame_numbers):
        frame_at(frame, folder / f'{i:02d}.jpg')
    rows = math.ceil(len(frame_numbers) / columns)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '1', '-i', str(folder / '%02d.jpg'), '-vf', f'tile={columns}x{rows}:nb_frames={len(frame_numbers)}:padding=8:margin=8:color=0x0d2629', '-frames:v', '1', str(output)], check=True)


sampled_frames = [20, 60, 100, 135, 185, 250, 310, 365, 405, 435, 470, 520, 580, 645, 710]
sheet(sampled_frames, frames, root / 'exports/Lumiere-Arts-V05-Showcase-Contact-Sheet.jpg')
frame_at(98, qa / 'rendered-s1-poster-full.png', 1080)
frame_at(185, qa / 'rendered-s2-atelier-full.png', 1080)
frame_at(310, qa / 'rendered-s3-motion-full.png', 1080)
frame_at(470, qa / 'rendered-s4-bento-full.png', 1080)
frame_at(550, qa / 'rendered-s5-arch-full.png', 1080)
frame_at(660, qa / 'rendered-s6-finale-full.png', 1080)

record = {
    'file': str(video.relative_to(root)), 'duration': float(probe['format']['duration']),
    'width': vs['width'], 'height': vs['height'], 'fps': vs['r_frame_rate'], 'frames': int(vs['nb_frames']),
    'video_codec': vs['codec_name'], 'audio_codec': aus['codec_name'], 'bytes': video.stat().st_size,
    'sha256': hashlib.sha256(video.read_bytes()).hexdigest(), 'source_sha256': beat_record['source_sha256'],
    'decode_errors': decode.stderr.strip(), 'black_segments': [s for s in scan.stderr.splitlines() if 'black_start:' in s],
    'audio_reference_correlation': correlation,
    'music': 'Rockot Slow Motion Fashion Ambient, uninterrupted source excerpt starting at 6.6s, volume 0.8.',
    'transitions': transitions, 'rendered_transitions': rendered_transitions,
    'contact_sheet_frames': sampled_frames, 'sampled_times': [round(f/30, 3) for f in sampled_frames],
}
(qa / 'verification.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
assert decode.returncode == 0 and not record['decode_errors'] and not record['black_segments']
assert scan.returncode == 0
assert record['duration'] == 24 and record['frames'] == 720 and (vs['width'], vs['height']) == (1080, 1920) and vs['r_frame_rate'] == '30/1'
assert correlation > .98, correlation
assert max(abs(r['offset_ms']) for r in transitions) <= 1000 / 30
assert max(abs(r['offset_ms']) for r in rendered_transitions) <= 1000 / 30
print(json.dumps(record, ensure_ascii=False, indent=2))
