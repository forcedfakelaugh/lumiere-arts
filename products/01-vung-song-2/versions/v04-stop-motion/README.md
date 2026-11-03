# Vùng Sống 2 · V04 · Nhịp riêng

20 giây, dọc 1080 × 1920, 30 fps. Bản thay thế theo yêu cầu chuyển sang stop-motion sau khi người dùng nhận thấy lỗi masking ở V03.

19 tư thế trích từ footage gốc; đổi ảnh mỗi 0,5–1 giây. Hai cảnh chữ phía sau người mẫu dùng 8 mask tĩnh đã chọn, giữ nguyên trong mỗi tư thế. Người và nền dùng cùng một ảnh, cùng màu; không còn matting theo từng frame hoặc nội suy giữa tư thế. Đây là stop-motion dựng từ ảnh trích, không phải footage stop-motion quay mới.

## File giao

- `exports/Lumiere-Arts-01-Vung-Song-2-V04-Stop-Motion-20s-1080p.mp4`
- `exports/Lumiere-Arts-01-Vung-Song-2-V04-Preview-540p.mp4`
- `exports/Lumiere-Arts-01-Vung-Song-2-V04-Contact-Sheet.jpg`
- `exports/CAPTION-AND-MUSIC-CREDIT.txt`

## Source

Trong `source/`: `npm ci` khi clone sang máy khác, sau đó `npm run preview`, `npm run check`, `npm run render`. Máy hiện tại dùng symlink tới dependencies đã có.

- `index.html`: bố cục, chữ, thời điểm đổi tư thế và easing theo nấc.
- `poses.json`: ảnh được trích từ clip nào và ở thời điểm nào.
- `assets/poses/`: ảnh nền PNG cùng cutout WebP lossless. Ảnh nền và foreground khớp pixel, không đổi màu riêng foreground.
- `assets/masks/`: 8 mask tĩnh ở 1080 × 1920, tái sử dụng từ những frame được chọn ở V03.
- `scripts/prepare-static-poses.cjs`: dựng lại cutout từ ảnh và mask đã lưu.
- `scripts/build-composition.py`: tái tạo bố cục V04 từ layout V03 được giữ bên cạnh; sửa trực tiếp `index.html` nếu chỉ chỉnh bản hiện tại.
- `qa/verification.json`: thông số xuất, kiểm tra decode và các mẫu giữ tư thế.

V01, V02 và V03 được giữ nguyên. Video xuất nằm ngoài Git.
