# herk-edit-kit tools (vendored)

Copied unchanged on 2026-11-10 from https://github.com/nateherkai/herk-edit-kit
(`.agents/skills/motion-showreel/scripts/` and `.agents/skills/hyperframes/scripts/`).
The showreel scripts are MIT (Nate Herk, see LICENSE-MIT). `contrast-report.mjs` comes from
the HyperFrames skill, Apache-2.0 (HeyGen, https://github.com/heygen-com/hyperframes).
All of them need Node 22+ and ffmpeg/ffprobe. Run them from the repo root.

| Script | Use it for |
|---|---|
| `music-grid.mjs <mp3> --bpm 120 [--beats]` | Beat period plus the **kick-band phase** (use this one, because the full-band phase can lock onto hi-hats and put cuts half a beat late). Prints energy per bar and per beat so you can find the build, drop and break. Cross-check it against `hyperframes audio`. |
| `splice-music.mjs <mp3> --period P --phase PH --segments "a-b,c-d" --length 30 [--gap N] [--fade 0.9] --out bed.wav` | Cuts a library track to the film's exact length, beat-accurate. `--gap N` ducks the half beat before output beat N (the pre-drop gap). Re-run `music-grid` on the result: the kick phase should be about 0. |
| `beatgrid.mjs --period P --length 30 --chapters "Calm:16, Drop:8, End:rest"` | Prints a section → seconds → frames sheet (60 fps) to paste into STORYBOARD.md. |
| `mix.mjs --bed bed.wav --events events.json --out master.wav --length 30` | Mixes the bed with optional beat-placed SFX and normalises to -14 LUFS / -1.2 dBTP. |
| `analyze-reference.mjs <video> <out-dir> --fps 6 --bpm 120 --phase 0` | Contact sheets plus `report.txt` (hard cuts, luminance rhythm, RMS, how far each cut is from the beat). Use it on client reference clips and on **our own render** (cuts should be within about 35 ms of a beat or half beat). |
| `contrast-report.mjs <source-dir> --samples 10 --out ../qa/contrast` | WCAG contrast audit of every text element over the actual pixels. Exits 1 if anything fails AA. **Needs `@hyperframes/producer`**, which is not in the shared node_modules yet (`sharp` is), so install it first. |

Skipped on purpose: `kie.mjs` (paid music/image/video generation) and `sfx.mjs` (paid SFX generation).
