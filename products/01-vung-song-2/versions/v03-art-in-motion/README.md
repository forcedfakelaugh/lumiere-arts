# Vùng Sống 2 · V03 · Art in Motion

24-second vertical fashion film, 1080 × 1920, 30 fps. Oversized type travels behind the moving model in two sequences, with 300 separate foreground mattes.

## Deliverables

- `exports/Lumiere-Arts-01-Vung-Song-2-V03-24s-1080p.mp4`
- `exports/Lumiere-Arts-01-Vung-Song-2-V03-Preview-540p.mp4`
- `exports/Lumiere-Arts-01-Vung-Song-2-V03-Contact-Sheet.jpg`
- `exports/CAPTION-AND-MUSIC-CREDIT.txt`

Open the Full HD file for final review. All prior versions are preserved.

## Edit and render

In `source/`, run `npm ci` on another machine, then `npm run preview`, `npm run check`, or `npm run render`. The local checkout reuses the existing node_modules installation via symlink. The required composited clips, fonts, artwork and music are included with the source. Full renders remain outside Git.

`index.html` owns the timeline, captions, artwork reveal and closing card. `type-layers.html` owns the oversized typography. `shots.json` records exact source trims.

To rebuild the depth clips after editing type, recapture the transparent PNG plates with `scripts/capture-type.cjs` through Playwright CLI (update its local root/preview URL for another machine), then run `python3 scripts/composite-depth.py` from this version folder.

The saved grayscale matte videos can be reused without Vision. To regenerate them on macOS, compile `scripts/segment-person.swift` with Swift and run it on the clean clip, start time 0, duration 6 or 4 seconds, output matte path, and width 540. The script uses the Homebrew FFmpeg path. Local video-decoder and Vision access are required.

`BRIEF.md`, `STORYBOARD.md`, `CREDITS.md` and `qa/verification.json` document the direction, sources and finished-file verification.
