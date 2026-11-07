# Agent notes · LUMIERE ARTS video series

Read README.md for repo layout. This file is the fast path and the known gotchas.

## Fast path for a new product video
1. Assets: Drive folders shared "anyone with link" download directly, no MCP needed:
   `curl -sL -o NAME "https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t"` (list IDs with the Google Drive MCP `search_files` `parentId = '<folder>'`). Run 6 in parallel with xargs -P 6. Save to `products/<NN-slug>/assets/originals/<YYYY-MM-DD>/`.
2. Look before planning: contact sheets with ffmpeg (`tile=`); for mixed-size photos scale each to a fixed box first, then concat → tile. No ImageMagick/PIL on this Mac; ffmpeg has no `drawtext`.
3. Scaffold by copying the latest version's `source/` (index.html, package.json, meta.json, assets/gsap.min.js, assets/fonts/*.woff2, assets/lumiere-logo-transparent.png) and symlink node_modules →
   `/Users/lucasnguyen/Documents/Codex/2026-10-16/task-2/elosmash-hyperframes/node_modules`.
4. Build → `npm run check` → `npx hyperframes snapshot --at t1,t2,... -o ../qa/snapN --describe false` and LOOK → `npm run render` → 720p light copy with ffmpeg → update product README, root README table, catalog.json, BRIEF/STORYBOARD/CREDITS.

## Gotchas (each cost real time)
- Sony 4K clips (C00xx.MP4) are PORTRAIT via rotation metadata: ffprobe says 3840x2160, ffmpeg auto-rotates to 2160x3840. Cut with plain `scale=1080:1920`, never a landscape crop.
- Shell is zsh: `for p in "a b"` does not word-split; use `a:b` pairs with `${p%%:*}`. Don't name shell functions `g` (alias clash).
- Pixabay pages block curl (Cloudflare), but its CDN does not: find the track in Chrome (claude-in-chrome), `fetch()` the track page in-page, regex the `cdn.pixabay.com/download/audio/...mp3?filename=...` URL, then curl that URL with a browser User-Agent and `-e https://pixabay.com/`. incompetech MP3s download directly (CC BY 4.0 → credit required in post caption). HeyGen music needs `npx hyperframes auth login` (not signed in).
- Content ID: the user does NOT want Pixabay tracks marked "Content ID Registered" (allowed by licence but auto-flagged on YouTube/Facebook). Check the track page HTML for the text `Content ID Registered` and skip any that have it.
- Beat grid: `npx hyperframes audio <mp3> --only bpm,downbeats,sections --json`; start the `<audio>` at a downbeat via `data-media-start` so film t=0 is beat 1.
- Lint warnings `timeline_track_too_dense` / `nested_structure_needs_subcomposition` are expected with the repo's single-file index.html convention.
- Bright riverside/white-column footage kills text contrast: always put a gradient `.shade` clip under copy.
- Never commit renders (`exports/`, `renders/`) or `assets/originals/`.

## Music library (`shared/music/`, all free, no Content ID)
User shortlisted these for 03 Thủy tinh hóa 14 (artistic, not generic fashion-ad, not old classical piano). Copy the chosen file into the version's `source/assets/music/`.
- `rockot-slow-motion-fashion-ambient-173505.mp3` — ambient/spacious, 1:47 (user's top pick in the brief: painting first, then silk and model)
- `rockot-eona-emotional-ambient-pop-351436.mp3` — ambient pop, 123 BPM, 2:32
- `rockot-chillout-soul-174805.mp3` — downtempo, 90 BPM, 1:29
- `kulakovka-luxury-life-620531.mp3` — luxury house, 120 BPM, 2:44
- `kulakovka-ambient-house-624653.mp3` — ambient house, 118 BPM, 2:47
- `prettyjohn1-fashion-507165.mp3` — soft house/runway, 118 BPM, 2:19
- Rejected (Content ID registered, deleted): Coma-Media "Sculpted Light", Sonican "Elegant Chill", WaveMaster "Fashion", penguinmusic "Elegant Abstract".
BPM values are from `hyperframes audio --only bpm` (signal-based, verify downbeats before cutting).

## Music already used
- 01 Vùng Sống 2: Rockot "Slow Motion Fashion Ambient", penguinmusic "Lazy Day" (Pixabay)
- 02 Sen Đỏ: WhatsApp reference beat (120 BPM)
- 03 Thủy tinh hóa 14 V01: Kevin MacLeod "Werq" (125 BPM, CC BY 4.0), file offset 2.915 s

## Styles tried
- 02 Sen Đỏ: editorial arch cards + text panels on wine-red.
- 03 V01 Nhịp Lụa: beat-synced montage (1 shot/bar calm → 2-beat → 1-beat cuts at drop, flash only on drop, painting zoom-out end card). Template: `products/03-thuy-tinh-hoa-14/versions/v01-nhip-lua/source/index.html`.
