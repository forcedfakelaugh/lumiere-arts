"""Measure percussive attacks independently from the authored frame markers."""
import array
import math
import re
import subprocess


def analyze(audio, offset=0, volume=1, duration=24):
    seek = ['-ss', str(offset)] if offset else []
    raw = subprocess.check_output([
        'ffmpeg', '-v', 'error', *seek, '-i', str(audio), '-t', str(duration),
        '-af', f'volume={volume},highpass=f=180,lowpass=f=4000',
        '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'])
    samples = array.array('f')
    samples.frombytes(raw)
    hop = 80
    env = [math.sqrt(sum(x*x for x in samples[i:i+hop])/hop)
           for i in range(0, len(samples)-hop, hop)]
    novelty = [0]*5 + [max(0, env[i]-sum(env[i-5:i])/5) for i in range(5, len(env))]
    candidates = [i for i in range(5, len(novelty)-5)
                  if novelty[i] == max(novelty[i-4:i+5]) and novelty[i] > .08]
    selected = []
    for i in sorted(candidates, key=lambda i: novelty[i], reverse=True):
        if all(abs(i-j) > 40 for j in selected):
            selected.append(i)
    return [{'seconds': round((i+.5)*.005, 4), 'strength': round(novelty[i], 6)}
            for i in sorted(selected)]


def authored_hits(html):
    match = re.search(r'const hits\s*=\s*\{([^}]+)\}', html)
    assert match, 'Authored hit map missing'
    hits = [(name, int(frame)) for name, frame in re.findall(r'(\w+)\s*:\s*(\d+)\s*/\s*fps', match.group(1))]
    assert len(hits) == 11, f'Expected 11 hits, got {len(hits)}'
    return hits


def align(hits, peaks):
    result = []
    for name, frame in hits:
        peak = min(peaks, key=lambda p: abs(p['seconds']-frame/30))
        result.append({'scene': name, 'frame': frame, 'seconds': round(frame/30, 6),
                       'measured_attack_seconds': peak['seconds'],
                       'offset_ms': round((frame/30-peak['seconds'])*1000, 3),
                       'attack_strength': peak['strength']})
    return result
