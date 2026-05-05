#!/usr/bin/env python3
"""
Jigsaw Asset Builder
--------------------
- Scans original/<cat>/*.jpg  → collects IDs
- Generates missing thumb/<cat>/<id>.webp (300px, q70) via ffmpeg
- Writes manifest.json at repo root

Usage:
  python tools/build.py [--dry-run]
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO_ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG_DIR     = os.path.join(REPO_ROOT, "original")
THUMB_DIR    = os.path.join(REPO_ROOT, "thumb")
CAT_FILE     = os.path.join(REPO_ROOT, "categories.json")
MANIFEST_OUT = os.path.join(REPO_ROOT, "manifest.json")

THUMB_WIDTH  = 300
THUMB_QUALITY = 70

DRY_RUN = "--dry-run" in sys.argv


def get_ids(cat_path: str) -> list[int]:
    ids = []
    if not os.path.isdir(cat_path):
        return ids
    for fname in os.listdir(cat_path):
        m = re.fullmatch(r"(\d+)\.jpg", fname, re.IGNORECASE)
        if m:
            ids.append(int(m.group(1)))
    return sorted(ids)


def make_thumb(src: str, dst: str):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", src,
        "-vf", f"scale={THUMB_WIDTH}:-1",
        "-c:v", "libwebp", "-quality", str(THUMB_QUALITY),
        dst,
    ]
    print(f"  thumb: {os.path.relpath(dst, REPO_ROOT)}", flush=True)
    if not DRY_RUN:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr.strip()}")


def main():
    with open(CAT_FILE, encoding="utf-8") as f:
        cat_meta = json.load(f)

    categories = []
    total_orig = 0
    total_thumb_gen = 0

    for slug, meta in cat_meta.items():
        orig_cat  = os.path.join(ORIG_DIR,  slug)
        thumb_cat = os.path.join(THUMB_DIR, slug)

        ids = get_ids(orig_cat)
        total_orig += len(ids)

        gen_count = 0
        for n in ids:
            src = os.path.join(orig_cat,  f"{n}.jpg")
            dst = os.path.join(thumb_cat, f"{n}.webp")
            if not os.path.exists(dst):
                make_thumb(src, dst)
                gen_count += 1

        total_thumb_gen += gen_count
        if gen_count:
            print(f"{slug}: {gen_count} thumb(s) generated")
        else:
            print(f"{slug}: {len(ids)} image(s) - thumbs up to date")

        categories.append({
            "slug":     slug,
            "title_vi": meta["title_vi"],
            "title_en": meta["title_en"],
            "ids":      ids,
        })

    manifest = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "categories":   categories,
    }

    print()
    if not DRY_RUN:
        with open(MANIFEST_OUT, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f"manifest.json written - {total_orig} image(s) across {len(categories)} categories")
    else:
        print("[dry-run] manifest not written:")
        print(json.dumps(manifest, ensure_ascii=False, indent=2))

    if total_thumb_gen > 0:
        print(f"\nDone. Run: git add . && git commit -m 'assets: add images' && git push")


if __name__ == "__main__":
    main()
