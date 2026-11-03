# LUMIERE ARTS · Series 6 video sản phẩm

Mỗi sản phẩm có asset, ý tưởng và các phiên bản video riêng. Hiện đã xác định sản phẩm 01: **Vùng Sống 2**. Năm sản phẩm còn lại chờ tên, brief và asset; không tự gán chung nguyên tác hoặc thông số chất liệu.

| Mã | Sản phẩm | Tình trạng |
|---|---|---|
| 01 | [Vùng Sống 2](products/01-vung-song-2/) | V04 Chuyển động liên kết, bản chỉnh 32 giây |
| 02 | [Chờ tên](products/02-chua-dat-ten/) | Chờ brief và asset |
| 03 | [Chờ tên](products/03-chua-dat-ten/) | Chờ brief và asset |
| 04 | [Chờ tên](products/04-chua-dat-ten/) | Chờ brief và asset |
| 05 | [Chờ tên](products/05-chua-dat-ten/) | Chờ brief và asset |
| 06 | [Chờ tên](products/06-chua-dat-ten/) | Chờ brief và asset |

## Cấu trúc mỗi sản phẩm

- `assets/originals/<ngày-nhận>/`: ảnh, video gốc và bảng đối chiếu tên/SHA-256.
- `concepts/`: ý tưởng, storyboard và quyết định sáng tạo.
- `versions/vNN-<concept>/`: một project Hyperframes riêng cho mỗi phiên bản.
- Trong mỗi phiên bản: `source/`, `exports/`, `qa/`, `scripts/`, brief, storyboard và credit.

`shared/brand/` giữ logo/font dùng chung; mỗi project vẫn có bản sao asset để render độc lập.
`archive/` giữ demo và media từ đợt trước, chưa gán vào sáu sản phẩm.
`catalog.json` là danh mục sản phẩm và phiên bản đang review.

## Review hiện tại

- V01 được giữ nguyên tại `products/01-vung-song-2/versions/v01-fashion-ambient/`.
- V02 được giữ tại `products/01-vung-song-2/versions/v02-mot-chi-tiet-nhieu-dien-mao/`.
- V03 được giữ tại `products/01-vung-song-2/versions/v03-art-in-motion/`; người dùng phản hồi lỗi masking khi chạy.
- V04 stop-motion được giữ tại `products/01-vung-song-2/versions/v04-stop-motion/`.
- V04 Chuyển động liên kết: `products/01-vung-song-2/versions/v04-chuyen-dong-lien-ket/`, chỉnh còn 32 giây; logo trong suốt xuyên suốt clip, chữ lớn hơn và chuyển cảnh căn nhạc.
- V05 Khúc Biến Tấu Trên Lụa (showcase thiết kế 24 giây): `products/01-vung-song-2/versions/v05-khuc-bien-tau-tren-lua/`.
- Mỗi phiên bản có Full HD, bản nhẹ và credit trong `exports/`.

Trong `source/`, dùng `npm run preview`, `npm run check`, `npm run render`.
Hyperframes 0.8.162; node_modules trên máy được dùng qua symlink. Khi clone sang máy khác, chạy `npm ci` trong source.

Các đường dẫn cũ `projects/2026-11-02`, `client-media/2026-11-02-vung-song` và `video-demo` được giữ bằng symlink để link đã gửi vẫn hoạt động. Làm việc mới từ `products/`. Xem `organization-2026-11-02.json` và `file-moves.json` để tra lịch sử di chuyển. QA cũ có thể ghi đường dẫn lịch sử.

## GitHub và dựng lại từ source

Repo lưu source các bản dựng cùng ảnh, clip làm việc 1080p, nhạc, font và dependencies đã khóa phiên bản. V03/V04 mới được tạo tại máy, chưa commit/push. **Không đưa video đã render lên GitHub.** Các thư mục `exports/`, `renders/`, cache và raw 4K được giữ ngoài Git. Xem [GIT-CONTENTS.md](GIT-CONTENTS.md) để biết phạm vi và cách chạy từ bản clone.
