# Credits and provenance

## Client footage and art

Media supplied for Vùng Sống 2 on 2026-11-02. Source inventory: `../../assets/originals-manifest.json`.

- Painting: **Vùng Sống 2 / Living Realm 2**, Nguyễn Văn Trinh, 2023, as identified by the supplied title card.
- The scarf design is adapted from **a portion of the original artwork**. The film makes no additional material, manufacturing or certification claims.
- Working clips originate from V02’s upright 1080p proxies of supplied shots 02, 03 and 06. Exact trims: `source/shots.json`.
- The original painting, lookbook scarf photograph and official Lumiere Arts logo are reused as supplied. No generated imagery.

## Music

**Slow Motion Fashion Ambient — Rockot**

Track: https://pixabay.com/music/beats-slow-motion-fashion-ambient-173505/

License: https://pixabay.com/service/license-summary/

Reused from the local source previously downloaded through the official Pixabay download on 2026-11-02. Its existing source and license evidence is in `../v02-mot-chi-tiet-nhieu-dien-mao/qa/rockot-source-validation.json`; no new license verification was performed for this edit.

V03 uses source 6.6–30.6 s. Stereo 48 kHz WAV; loudness normalization target -17 LUFS / -1.5 dBTP; 0.12 s fade in and 2 s fade out. Final AAC export measures -15.5 LUFS integrated and -1.5 dBFS true peak. Courtesy credit is included with the deliverables.

## Typography and processing

Existing local EB Garamond and Cormorant Medium font files. GSAP and Hyperframes 0.8.162, as in the previous project.

Apple Vision accurate person segmentation generates a 540 × 960 matte for every video frame. FFmpeg scales and refines the mask, composites two moving transparent type plates between the teal-graded scenery and the original foreground, and writes the 1080p clips. These clips are deliberately precomposited to keep Hyperframes playback and export deterministic. The original subject pixels remain the foreground; the model and scarf are not synthesized.
