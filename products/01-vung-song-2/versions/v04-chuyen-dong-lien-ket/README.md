# Vùng Sống 2 · V04 · Chuyển động liên kết

Bản review **R3** theo phản hồi ngày **03/11/2026**. Video dọc 32 giây, 30 fps, 960 frame.

- **Chỉ sửa cảnh kết** `#closing` / `#closing-collage`. Mọi cảnh trước, mốc chuyển cảnh, thời lượng và nhạc giữ nguyên bản R2 đã duyệt.
- Thay bằng ba ảnh gốc mới của khách: áo dài ren trắng bên hồ làm ảnh chính **660 × 1300 px**; suit đen khoác khăn **348 × 610 px**; khăn trùm đầu cầm túi quà **420 × 672 px**. Mặt, khăn và toàn bộ túi quà nằm trong vùng hiển thị.
- Vùng collage tăng từ **1150 lên 1470 px** (+27,8% chiều cao), dải thương hiệu còn **450 px**. Các ô lệch cao độ, chồng nhẹ, góc bo bất đối xứng, viền vàng mảnh trên nền teal `#193e43`.
- Logo giữ **360 px**, độ sáng và opacity như R2; chữ kết thu gọn. Ba ô ảnh trượt nhẹ 18/24/30 px, bắt đầu cách nhau một frame trong chính wipe cũ **28,367–28,767 giây**, tâm nhạc vẫn **28,567 giây**.
- Giữ Rockot, offset **6,6 giây**, volume **0,8**, tốc độ gốc và đoạn nhạc liên tục. Không thay đoạn phóng video **23,133–24,333 giây** hay watermark đã duyệt.

Chi tiết vòng mới: [RECAP-2026-11-03-R3.md](RECAP-2026-11-03-R3.md). Lịch sử R2: [RECAP-2026-11-03-R2.md](RECAP-2026-11-03-R2.md).

Ảnh mới được sao chép nguyên byte vào `source/assets/images/` và `client-media/2026-11-02-vung-song/02-lookbook/` tại gốc dự án. Tên file, kích thước thực tế và SHA-256 ở [qa/r3-client-photos.json](qa/r3-client-photos.json). Ảnh áo dài thực tế 1710 × 2560; hai ảnh còn lại 1707 × 2560, không resize hay nén lại file gốc.

## File bàn giao

| File | Quy cách |
| --- | --- |
| [1080p](exports/Lumiere-Arts-V04-Review-32s-1080p.mp4) | 1080 × 1920, H.264/AAC |
| [720p](exports/Lumiere-Arts-V04-Review-32s-720p.mp4) | 720 × 1280, H.264/AAC |
| [540p](exports/Lumiere-Arts-V04-Review-32s-540p.mp4) | 540 × 960, H.264/AAC |
| [Contact sheet](exports/Lumiere-Arts-V04-Review-Contact-Sheet.jpg) | 15 khung hình từ bản MP4 R3 |

Bản 720p cũng được chép tới `~/Desktop/Lumiere-Arts-V04-Review-32s-720p.mp4`; SHA-256 trùng bản trong `exports/`.

## Chạy và xuất lại

Trong `source/`, chạy `npm ci` khi clone sang máy khác; máy hiện tại dùng symlink tới dependencies có sẵn. Hyperframes được khóa ở phiên bản **0.8.162**.

```sh
cd source
npm run preview
npm run check
npm run render
```

`npm run render` tạo thẳng `exports/Lumiere-Arts-V04-Review-32s-1080p.mp4`. Từ thư mục phiên bản này, tạo hai bản nhẹ và contact sheet:

```sh
ffmpeg -v error -y -i exports/Lumiere-Arts-V04-Review-32s-1080p.mp4 -vf scale=540:960 -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a copy -movflags +faststart exports/Lumiere-Arts-V04-Review-32s-540p.mp4
ffmpeg -v error -y -i exports/Lumiere-Arts-V04-Review-32s-1080p.mp4 -vf scale=720:1280 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a copy -movflags +faststart exports/Lumiere-Arts-V04-Review-32s-720p.mp4
python3 scripts/verify-render.py
cp exports/Lumiere-Arts-V04-Review-32s-720p.mp4 ~/Desktop/Lumiere-Arts-V04-Review-32s-720p.mp4
```

## Kiểm tra

- `scripts/verify-render.py`: độ dài, kích thước, fps, số frame, decode, khung đen, tương quan nhạc gốc, điểm nhấn đo lại từ audio source và MP4, frame lặp quanh đoạn phóng; tạo contact sheet và các dải frame chi tiết.
- `scripts/beat_analysis.py`: đo điểm nhấn từ dải âm 180–4000 Hz với cửa sổ 5 ms, độc lập với các mốc frame trong source. Không sử dụng danh sách beat cũ hoặc file tạm trong `/tmp`.
- `scripts/inspect-review.cjs`: kiểm tra bố cục, logo và tính liên tục của video qua Playwright tại cổng 4816. Dùng server có hỗ trợ HTTP Range để video seek đúng:

```sh
python3 scripts/serve-review.py
# Terminal khác, vẫn ở thư mục phiên bản:
playwright-cli -s=lumiere-r3 open http://127.0.0.1:4816/source/index.html
playwright-cli -s=lumiere-r3 --raw run-code --filename=scripts/inspect-review.cjs > qa/browser-layout.json
playwright-cli -s=lumiere-r3 close
```

Kết quả cuối ở `qa/hyperframes-check.json`, `qa/browser-layout.json`, `qa/verification.json`, `qa/beat-analysis.json`, `qa/delivery-manifest.json` và [qa/visual-review.md](qa/visual-review.md). Các ảnh `qa/rendered-hero-transition.jpg`, `qa/rendered-closing-transition.jpg` và sáu ảnh `qa/rendered-closing-full-{857,860,863,882,930,959}.png` được trích trực tiếp từ MP4 mới, không phải ảnh preview.

Bản source trước R3 giữ ở `qa/before-r3-closing.html`, MP4 trước R3 ở `qa/before-r3-1080p.mp4`; báo cáo R2 được lưu dưới tiền tố `qa/before-r3-*`. Đối chiếu phạm vi sửa ở `qa/r3-scope-check.json`.

Bản source trước R2 giữ ở `qa/before-r2-motion-music.html`; bản trước vòng review đầu ở `qa/before-logo-timing-review.html`. MP4 trước R2 được giữ cục bộ ở `qa/before-r2-1080p.mp4`. Các file `before-*` và `browser-layout-r2-initial.json` là tư liệu lịch sử; dùng báo cáo R3 hiện tại để kiểm chứng bản giao. Audio R3/R2 được so sánh toàn bộ PCM ở `qa/r3-audio-unchanged.json`. Không commit video xuất; phiên làm việc này không tạo commit.
