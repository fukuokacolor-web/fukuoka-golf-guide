#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2ファイル → 本番に昇格。
- course-*-v2.html → course-*.html（上書き）
- index-v2.html → index.html（上書き）
- V2ファイルは削除（gitに過去版は残る）
- v2-review.html も削除
"""
import sys, io, shutil
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = Path(r'C:/Users/Owner/fukuoka-golf-guide')

def promote():
    v2_files = sorted(BASE.glob('course-*-v2.html'))
    print(f'=== V2 → 本番 昇格: {len(v2_files)}コース ===')

    for v2 in v2_files:
        # course-xxx-v2.html → course-xxx.html
        prod_name = v2.name.replace('-v2.html', '.html')
        prod = BASE / prod_name
        # Overwrite production file with v2 content
        shutil.copy2(str(v2), str(prod))
        print(f'  ✓  {v2.name}  →  {prod.name}')
        # Remove v2 file
        v2.unlink()

    # index-v2.html → index.html
    idx_v2 = BASE / 'index-v2.html'
    idx = BASE / 'index.html'
    if idx_v2.exists():
        shutil.copy2(str(idx_v2), str(idx))
        print(f'\n  ✓  index-v2.html  →  index.html')
        idx_v2.unlink()

    # Clean up review page
    rev = BASE / 'v2-review.html'
    if rev.exists():
        rev.unlink()
        print(f'  ✓  v2-review.html (削除)')

    print(f'\n=== 完了 ===')

if __name__ == '__main__':
    promote()
