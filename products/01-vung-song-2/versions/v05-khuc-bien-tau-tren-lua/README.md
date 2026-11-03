# Vùng Sống 2 · V05 · Khúc biến tấu trên lụa (Atelier Editorial Showcase)

Phiên bản **V05** được thiết kế như một bản dựng **Atelier Editorial Showcase** 24 giây (1080 × 1920, 30 fps, 720 frame) trên Hyperframes 0.8.162, kết hợp lưới kiến trúc triển lãm (Swiss/Museum Grid), khung passepartout, chuyển cảnh cắt/wipe đồng bộ chính xác với các điểm nhấn âm nhạc (dưới nửa frame 30 fps) và chuyển động liên tục không nhảy crop.

## Điểm nhấn thiết kế (Design Showcase)

1. **Act I · Nguyên tác hội họa (`0,00s – 4,33s`, Frame 0–130)**:
   - Bố cục catalogue bảo tàng trên nền giấy lụa ngà `#F3EDE1` cùng khung viền mảnh `#163A3F` và chỉ dấu biên tập `01 · NGUYÊN TÁC HỘI HỌA`.
   - Khởi đầu bằng góc nhìn cận cảnh (macro diptych loupe) lướt qua chi tiết sắc chàm và hoa nước trắng của bức *Vùng Sống 2*, sau đó thu về toàn cảnh nguyên tác `100 × 200 cm` nằm trọn trong khung passepartout viền vàng mảnh đúng điểm nhấn nhạc tại **Frame 94 (`3,133s`)**.
2. **Act II · Không gian triển lãm & Xưởng chế tác (`4,33s – 8,57s`, Frame 130–257)**:
   - Thay vì phóng toàn màn hình các tư liệu máy in (vốn ở độ phân giải 720p), V05 đặt tư liệu triển lãm và cận cảnh in lụa trong bố cục **Song khung vòm bất đối xứng (Architectural Arch Diptych)** trên nền xanh cổ vịt đậm `#133337`, nối với nhau qua trục biên tập ở giữa: *"Sắc màu hội họa chuyển mình trên từng thước lụa"*.
   - Đúng nhịp nhạc tại **Frame 203 (`6,767s`)**, cả khung trên (tư liệu triển lãm) và khung dưới (chế tác in lụa) đồng loạt chuyển cảnh đối ứng.
3. **Act III · Dấu ấn chuyển thể & Đối chiếu nguyên tác (`8,57s – 12,83s`, Frame 257–385)**:
   - Khăn lụa mở rộng toàn khung hình (`la-scarf-01-unfold-front` chuyển sang `la-scarf-05-riverside-unfold` tại **Frame 348 / `11,600s`**) đi kèm thẻ **Origin Callout Card** nổi ở góc trên phải để người xem đối chiếu trực tiếp họa tiết trên lụa với nguyên tác *Vùng Sống 2 (2023)*.
4. **Act IV · Biến tấu phong cách — Triptych bất đối xứng (`12,83s – 17,37s`, Frame 385–521)**:
   - Ba cột dọc lệch nhịp với góc bo vòm điêu khắc lần lượt mở theo ba điểm nhấn nhạc (**Frame 385 / `12,833s`**, **Frame 421 / `14,033s`**, **Frame 448 / `14,933s`**): `01 TRÙM ĐẦU · 02 KHOÁC VAI · 03 PHỦ LƯNG`.
5. **Act V · Phóng toàn màn hình liền mạch (`17,37s – 20,40s`, Frame 521–612)**:
   - Cột thứ ba (`#f3` / `#look-back`) giữ nguyên một luồng video `1080 × 1920` duy nhất và mở `clip-path` + `transform` mượt mà ra toàn màn hình quanh tâm nhạc **Frame 521 (`17,367s`)**, không đổi thẻ `<video>` và không nhảy crop.
   - Thông số chất liệu xuất hiện tại **Frame 566 (`18,867s`)**: *100% lụa tơ tằm Bảo Lộc · Satin 16 momme · Viền khâu thủ công*.
6. **Act VI · Thẻ kết Golden-Hour Lookbook (`20,40s – 24,00s`, Frame 612–720)**:
   - Chuyển vào thẻ kết tại **Frame 612 (`20,400s`)** với 3 ảnh lookbook độ phân giải gốc trong bố cục collage vòm viền vàng, chuyển động thở nhẹ (micro-scale drift), logo thương hiệu tách nền rõ nét và thông tin tác phẩm.

## File bàn giao

| File | Quy cách |
| --- | --- |
| [Lumiere-Arts-V05-Showcase-24s-1080p.mp4](exports/Lumiere-Arts-V05-Showcase-24s-1080p.mp4) | 1080 × 1920, 30 fps, H.264/AAC |
| [Lumiere-Arts-V05-Showcase-24s-720p.mp4](exports/Lumiere-Arts-V05-Showcase-24s-720p.mp4) | 720 × 1280, 30 fps, H.264/AAC |
| [Lumiere-Arts-V05-Showcase-24s-540p.mp4](exports/Lumiere-Arts-V05-Showcase-24s-540p.mp4) | 540 × 960, 30 fps, H.264/AAC |
| [Lumiere-Arts-V05-Showcase-Contact-Sheet.jpg](exports/Lumiere-Arts-V05-Showcase-Contact-Sheet.jpg) | 15 khung hình trích từ MP4 xuất |

## Chạy và xuất lại

```sh
cd source
npm run preview
npm run check
npm run render
```
