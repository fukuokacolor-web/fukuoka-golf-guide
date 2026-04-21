#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HEIC/JPG を WebP に一括変換。
- HEIC は pillow-heif で読み込み
- 元ファイル名をベースに .webp 生成
- 既に .webp が存在したらスキップ
"""
import sys, io, os
from pathlib import Path
from PIL import Image
import pillow_heif

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
pillow_heif.register_heif_opener()

BASE = Path(r'C:/Users/Owner/fukuoka-golf-guide/images')
TARGET_EXT = {'.heic', '.jpg', '.jpeg'}

def convert(src: Path):
    dst = src.with_suffix('.webp')
    # 除外：スペース入りファイル名
    if dst.exists():
        print(f'  SKIP  {src.name}  → {dst.name} (already exists)')
        return
    try:
        img = Image.open(src)
        # EXIF回転を適用
        try:
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass
        # 長辺が2400px超なら縮小（ファイルサイズ対策）
        max_side = 2400
        w, h = img.size
        if max(w, h) > max_side:
            scale = max_side / max(w, h)
            img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
        # RGBA→RGB（JPG起源対策）
        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')
        img.save(dst, 'WEBP', quality=85, method=6)
        print(f'  OK    {src.name}  → {dst.name}  ({dst.stat().st_size//1024}KB)')
    except Exception as e:
        print(f'  FAIL  {src.name}: {e}')

def main():
    files = sorted([p for p in BASE.iterdir() if p.suffix.lower() in TARGET_EXT])
    # スペース入りや (1) 系の重複ファイルは除外
    files = [p for p in files if '(' not in p.name and ')' not in p.name]
    print(f'=== 変換対象：{len(files)}ファイル ===')
    for f in files:
        convert(f)
    print('=== 完了 ===')

if __name__ == '__main__':
    main()
