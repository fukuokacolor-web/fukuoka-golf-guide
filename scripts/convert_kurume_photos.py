#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""convert_kurume_photos.py — 久留米CC 現地レポート用に 3 枚の HEIC を webp へ変換。

オーナー実体験コンテンツ (2026-05-17 久留米CCラウンド) 用。
3 枚: IMG_1424.HEIC / IMG_1432.HEIC / IMG_1433 (1).HEIC
変換後 1600px 長辺・WEBP quality 85。REPO + PREVIEW 両方に書き出し。
変換後にプレビューで内容確認 → 後段でディスクリプティブ名にリネーム。

Usage: python scripts/convert_kurume_photos.py
"""
import sys
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

register_heif_opener()

SRC_PREVIEW = Path("C:/Users/Owner/Documents/新しいPJ/images")
DST_PREVIEW = SRC_PREVIEW
DST_REPO = Path("C:/Users/Owner/fukuoka-golf-guide/images")

FILES = [
    ("IMG_1424.HEIC",     "IMG_1424.webp"),
    ("IMG_1432.HEIC",     "IMG_1432.webp"),
    ("IMG_1433 (1).HEIC", "IMG_1433_1.webp"),
]

MAX_SIDE = 1600
QUALITY = 85

for src_name, dst_name in FILES:
    src = SRC_PREVIEW / src_name
    if not src.exists():
        print(f"  NOT FOUND: {src}")
        continue
    img = Image.open(src)
    # 自動 EXIF 回転 (iPhone HEIC は回転メタデータあり)
    try:
        from PIL import ImageOps
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    # 長辺 MAX_SIDE にリサイズ (アスペクト比保持)
    img.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)
    # RGBA → RGB if needed
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    for dst_root in (DST_PREVIEW, DST_REPO):
        dst_root.mkdir(parents=True, exist_ok=True)
        out = dst_root / dst_name
        img.save(out, "WEBP", quality=QUALITY, method=6)
        sz = out.stat().st_size // 1024
        print(f"  {src_name} -> {dst_root.name}/{dst_name} ({sz} KB, {img.width}x{img.height})")
print("DONE")
