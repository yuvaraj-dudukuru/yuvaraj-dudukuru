"""Prepare source-photo.jpg -> data/prepped.png for the ASCII portrait.

Background removal via rembg is OPTIONAL. If rembg isn't installed the script
still works -- it just skips that step. Install it only if your photo has a busy
background:  pip install rembg
"""

import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "prepped.png"
CANDIDATES = ["source-photo.jpg", "source-photo.jpeg", "source-photo.png", "source-photo.webp"]


def find_source():
    for name in CANDIDATES:
        p = ROOT / name
        if p.exists():
            return p
    sys.exit(
        "No source photo found. Put your photo in the repo root as "
        "source-photo.jpg (or .png / .jpeg / .webp) and re-run."
    )


def strip_background(img):
    try:
        from rembg import remove
    except ImportError:
        print("rembg not installed -- skipping background removal (that's fine).")
        return img
    print("Removing background with rembg...")
    return remove(img)


def main():
    src = find_source()
    print(f"Source: {src.name}")

    img = Image.open(src)
    img = ImageOps.exif_transpose(img)  # honour phone rotation
    img = img.convert("RGBA")

    img = strip_background(img)

    # flatten onto black so transparent areas read as empty
    flat = Image.new("RGBA", img.size, (0, 0, 0, 255))
    flat.alpha_composite(img)
    img = flat.convert("L")

    # square centre crop
    w, h = img.size
    side = min(w, h)
    img = img.crop(((w - side) // 2, (h - side) // 2,
                    (w - side) // 2 + side, (h - side) // 2 + side))

    img = ImageOps.autocontrast(img, cutoff=2)
    img = ImageEnhance.Contrast(img).enhance(1.35)
    img = ImageEnhance.Brightness(img).enhance(1.05)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print(f"Wrote {OUT}  ({img.size[0]}x{img.size[1]})")
    print("Next: python scripts/make_ascii_svg.py")


if __name__ == "__main__":
    main()
