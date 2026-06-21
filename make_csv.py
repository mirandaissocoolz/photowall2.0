#!/usr/bin/env python3
"""
Reads every photo in a folder and writes 'photos.csv' with the file name,
the date the photo was taken, and its width/height.

This does NOT touch Supabase and does NOT go on the internet. It only makes
a spreadsheet file on your computer that you can open and check. Once it
looks right, you import that file into Supabase yourself with a few clicks.
"""

import csv
from pathlib import Path
from PIL import Image, ExifTags

# Optional: lets it read iPhone .HEIC files too. Harmless to leave in.
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

# ---- The ONLY thing to change: the folder your photos are in ----
PHOTO_FOLDER = "./photos"
# -----------------------------------------------------------------


def date_taken(exif):
    raw = None
    try:
        raw = exif.get_ifd(ExifTags.IFD.Exif).get(36867)  # DateTimeOriginal
    except Exception:
        pass
    if not raw:
        raw = exif.get(306)  # plain DateTime, as a fallback
    if raw:
        # "2025:03:20 14:01:55" -> "2025-03-20"
        return str(raw).split(" ")[0].replace(":", "-")
    return ""


folder = Path(PHOTO_FOLDER)
exts = {".jpg", ".jpeg", ".png", ".heic", ".heif"}

rows = []
for p in sorted(folder.iterdir()):
    if p.suffix.lower() not in exts:
        continue
    img = Image.open(p)
    width, height = img.size
    rows.append([p.name, date_taken(img.getexif()), width, height])

with open("photos.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["file_name", "taken_at", "width", "height"])
    writer.writerows(rows)

print(f"Done. Wrote {len(rows)} rows to photos.csv")
