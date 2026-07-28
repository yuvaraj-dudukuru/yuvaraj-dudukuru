"""Convert data/prepped.png into portrait.svg -- an ASCII portrait that types in.

Run prep_photo.py first. If no prepped photo exists, this writes a placeholder
portrait instead of failing, so the README never shows a broken image.
"""

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "prepped.png"
OUT = ROOT / "portrait.svg"

# dark -> light. Tweak this to change the texture of the portrait.
CHARS = " .:-=+*#%@"

COLS = 74            # character columns
CHAR_ASPECT = 0.52   # monospace glyphs are ~2x taller than wide
FONT_SIZE = 9
LINE_H = 9.2
CHAR_W = 5.42

BG = "#0b0f14"
ACCENT = "#14b8a6"
DIM = "#0f766e"
BRIGHT = "#5eead4"
MUTED = "#6b8280"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def to_ascii():
    img = Image.open(SRC).convert("L")
    rows = int(COLS * CHAR_ASPECT * img.size[1] / img.size[0])
    img = img.resize((COLS, rows), Image.LANCZOS)

    a = np.asarray(img, dtype=np.float32) / 255.0
    idx = np.clip((a * (len(CHARS) - 1)).round().astype(int), 0, len(CHARS) - 1)

    lines = ["".join(CHARS[i] for i in row) for row in idx]
    levels = [[int(i) for i in row] for row in idx]
    return lines, levels


def placeholder():
    art = [
        "",
        "        +--------------------------------------+",
        "        |                                      |",
        "        |        no source photo found         |",
        "        |                                      |",
        "        |   drop your photo in the repo root   |",
        "        |        as  source-photo.jpg          |",
        "        |                                      |",
        "        |   then run:                          |",
        "        |     python scripts/prep_photo.py     |",
        "        |     python scripts/make_ascii_svg.py |",
        "        |                                      |",
        "        +--------------------------------------+",
        "",
    ]
    return art, [[5] * len(line) for line in art]


def build():
    if SRC.exists():
        lines, levels = to_ascii()
    else:
        print("No data/prepped.png -- writing placeholder portrait.")
        lines, levels = placeholder()

    width = int(COLS * CHAR_W) + 36
    height = int(len(lines) * LINE_H) + 40

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
        f'<rect width="{width}" height="{height}" rx="10" fill="{BG}"/>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="10" fill="none" '
        f'stroke="{DIM}" stroke-width="1"/>',
    ]

    per_line = 1.8 / max(len(lines), 1)

    for r, line in enumerate(lines):
        y = 26 + r * LINE_H
        begin = round(0.15 + r * per_line, 3)
        # colour each line by its mean brightness so the face has depth
        mean = sum(levels[r]) / max(len(levels[r]), 1) if levels[r] else 0
        colour = BRIGHT if mean > 6 else (ACCENT if mean > 3 else DIM)
        out.append(
            f'<text x="18" y="{y}" font-size="{FONT_SIZE}" fill="{colour}" '
            f'xml:space="preserve" opacity="0">{esc(line)}'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.18s" '
            f'begin="{begin}s" fill="freeze"/></text>'
        )

    out.append(
        f'<text x="{width - 18}" y="{height - 12}" font-size="9" fill="{MUTED}" '
        f'text-anchor="end">./portrait --ascii</text>'
    )
    out.append("</svg>")

    OUT.write_text("\n".join(out))
    print(f"Wrote {OUT}  ({COLS} cols x {len(lines)} rows)")


if __name__ == "__main__":
    build()
