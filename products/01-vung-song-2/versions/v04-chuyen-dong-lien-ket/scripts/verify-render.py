from pathlib import Path
import array
import hashlib
import json
import math
import subprocess
from beat_analysis import analyze, authored_hits, align

root = Path(__file__).resolve().parents[1]
video = root / 'exports/Lumiere-Arts-V04-Review-32s-1080p.mp4'
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
    result = subprocess.check_output(['ffmpeg', '-v', 'error', *args, '-t', '32', '-ac', '1', '-ar', '8000', '-f', 'f32le', '-'])
    samples = array.array('f')
    samples.frombytes(result)
    return samples


song = root / 'source/assets/music/rockot-slow-motion-fashion-ambient.mp3'
reference = pcm(['-ss', '6.6', '-i', str(song), '-af', 'volume=0.8'])
actual = pcm(['-i', str(video), '-vn'])
n = min(len(reference), len(actual))
correlation = sum(reference[i] * actual[i] for i in range(n)) / math.sqrt(sum(x*x for x in reference[:n]) * sum(x*x for x in actual[:n]))
hits = authored_hits(source.read_text())
source_peaks = analyze(song, offset=6.6, volume=.8)
rendered_peaks = analyze(video)
transitions = align(hits, source_peaks)
rendered_transitions = align(hits, rendered_peaks)
beat_record = {
    'method': 'Percussive band 180-4000 Hz; 5 ms RMS; positive novelty against previous 25 ms; local maxima and 200 ms non-maximum suppression. Markers read from source/index.html; detected attacks are computed independently over the entire audio.',
    'music_offset_seconds': 6.6, 'volume': .8, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'source_transitions': transitions, 'rendered_transitions': rendered_transitions,
    'all_source_attacks': source_peaks, 'all_rendered_attacks': rendered_peaks,
}
(qa/'beat-analysis.json').write_text(json.dumps(beat_record, ensure_ascii=False, indent=2)+'\n')


def frame_at(frame, path, width=270):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{frame/30:.9f}', '-i', str(video), '-frames:v', '1', '-vf', f'scale={width}:-1', str(path)], check=True)


def sheet(frame_numbers, folder, output, columns=5):
    folder.mkdir(exist_ok=True)
    # Limit the image sequence explicitly, so stale files cannot enter the sheet.
    for i, frame in enumerate(frame_numbers):
        frame_at(frame, folder/f'{i:02d}.jpg')
    rows = math.ceil(len(frame_numbers)/columns)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '1', '-i', str(folder/'%02d.jpg'), '-vf', f'tile={columns}x{rows}:nb_frames={len(frame_numbers)}:padding=8:margin=8:color=0x193e43', '-frames:v', '1', str(output)], check=True)


sampled_frames = [0, 135, 210, 240, 270, 360, 444, 537, 600, 700, 712, 730, 750, 882, 959]
sheet(sampled_frames, frames, root/'exports/Lumiere-Arts-V04-Review-Contact-Sheet.jpg')
transition_frames = [690, 693, 694, 697, 700, 703, 706, 709, 712, 715, 718, 721, 724, 727, 730, 731, 733, 739, 748, 750]
sheet(transition_frames, qa/'transition-frames', qa/'rendered-hero-transition.jpg')
closing_frames = [844, 848, 850, 851, 853, 855, 857, 860, 863, 866, 875, 882, 900, 930, 959]
sheet(closing_frames, qa/'closing-frames', qa/'rendered-closing-transition.jpg')
frame_at(882, qa/'rendered-closing-full.png', 1080)
for frame in [857, 860, 863, 882, 930, 959]:
    frame_at(frame, qa/f'rendered-closing-full-{frame}.png', 1080)
frame_at(712, qa/'rendered-hero-midpoint.png', 1080)

# The moving hero window must not contain duplicated output frames.
raw = subprocess.check_output(['ffmpeg','-v','error','-ss',str(691/30),'-i',str(video),'-frames:v','42','-vf','scale=108:192,format=gray','-f','rawvideo','-'])
stride = 108*192
motion_frames = [raw[i:i+stride] for i in range(0, len(raw), stride)]
deltas = [sum(abs(x-y) for x,y in zip(a,b))/stride for a,b in zip(motion_frames, motion_frames[1:])]
record = {
    'file': str(video.relative_to(root)), 'duration': float(probe['format']['duration']),
    'width': vs['width'], 'height': vs['height'], 'fps': vs['r_frame_rate'], 'frames': int(vs['nb_frames']),
    'video_codec': vs['codec_name'], 'audio_codec': aus['codec_name'], 'bytes': video.stat().st_size,
    'sha256': hashlib.sha256(video.read_bytes()).hexdigest(), 'source_sha256': beat_record['source_sha256'],
    'decode_errors': decode.stderr.strip(), 'black_segments': [s for s in scan.stderr.splitlines() if 'black_start:' in s],
    'audio_reference_correlation': correlation,
    'music': 'Same original track, uninterrupted source excerpt starting at 6.6s, volume 0.8; no tempo change or splice.',
    'transitions': transitions, 'rendered_transitions': rendered_transitions,
    'hero_transition': {'start_frame':694,'midpoint_frame':712,'end_frame':730,'start_seconds':694/30,'midpoint_seconds':712/30,'end_seconds':730/30,'duplicate_frames':sum(d==0 for d in deltas),'adjacent_frame_mean_absolute_difference':deltas},
    'contact_sheet_frames': sampled_frames, 'sampled_times':[f/30 for f in sampled_frames],
    'hero_review_frames':transition_frames, 'closing_review_frames':closing_frames,
    'visual_review':'See qa/visual-review.md after manual inspection of the current export; this script does not perform subjective visual acceptance.',
}
(qa/'verification.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
assert decode.returncode == 0 and not record['decode_errors'] and not record['black_segments']
assert scan.returncode == 0
assert record['duration'] == 32 and record['frames'] == 960 and (vs['width'],vs['height']) == (1080,1920) and vs['r_frame_rate'] == '30/1'
assert correlation > .98, correlation
assert max(abs(r['offset_ms']) for r in transitions) <= 1000/30
assert max(abs(r['offset_ms']) for r in rendered_transitions) <= 1000/30
assert len(motion_frames) == 42 and all(d>0 for d in deltas)
print(json.dumps({k:v for k,v in record.items() if k not in ['hero_transition']}, ensure_ascii=False, indent=2))
