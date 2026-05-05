# jigsaw-assets

Kho ảnh cho game Jigsaw trong package `tmk_games`. Phục vụ qua jsDelivr CDN, không bundle vào app — app tải về khi user chọn ảnh chơi (cache vĩnh viễn ở client).

## Cấu trúc

```
original/<category>/<id>.webp   ← ảnh gốc full chất lượng (chơi)
thumb/<category>/<id>.webp      ← ảnh resize ~300px (gallery)
```

`<category>` slug tiếng Anh: `travel`, `nature`, `animal`, `food`, `art`.

## URL CDN

```
https://cdn.jsdelivr.net/gh/tmkgroup/jigsaw-assets/original/<category>/<id>.webp
https://cdn.jsdelivr.net/gh/tmkgroup/jigsaw-assets/thumb/<category>/<id>.webp
```

> jsDelivr cache theo commit. Đổi ảnh: `git push` → đợi vài phút, hoặc dùng `@<tag>` để pin version.

## Quy ước thêm ảnh mới

1. Đặt file gốc vào `original/<category>/<id>.webp`.
2. Tạo bản resize 300px width (giữ tỉ lệ, quality ~70) đặt vào `thumb/<category>/<id>.webp`.
3. Mở `lib/src/xep_hinh/jigsaw/data/jigsaw_image_config.dart` trong package `tmk_games`, thêm 1 dòng `JigsawImageConfig(...)`.
4. Commit + push.

## Tên file

- Lowercase, không dấu, dùng `_` (vd: `cat_flower.webp`, không phải `Cat Flower.webp`).
- `<id>` trong code Dart phải khớp tên file (không gồm `.webp`).

## Repo

- **Phải là public** (jsDelivr không phục vụ private repo).
- Remote: `https://github.com/tmkgroup/jigsaw-assets`
