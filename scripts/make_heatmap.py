"""Render data/contributions.json into an animated contribution heatmap SVG."""

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"

CELL = 12
GAP = 3
PITCH = CELL + GAP
PAD_L = 34
PAD_T = 44
PAD_B = 46

# teal ramp -- level 0 is the empty cell
PALETTE = ["#12201f", "#134e4a", "#0f766e", "#14b8a6", "#5eead4"]
BG = "#0b0f14"
FG = "#8ba3a0"
ACCENT = "#14b8a6"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    d = json.loads(DATA.read_text())
    days = d["days"]

    # bucket into week columns; column advances on each Sunday
    weeks, col = [], []
    for day in days:
        y, m, dd = (int(x) for x in day["date"].split("-"))
        dow = (date(y, m, dd).weekday() + 1) % 7  # 0 = Sunday
        if dow == 0 and col:
            weeks.append(col)
            col = []
        day["dow"] = dow
        col.append(day)
    if col:
        weeks.append(col)

    width = PAD_L + len(weeks) * PITCH + 16
    height = PAD_T + 7 * PITCH + PAD_B

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">',
        f'<rect width="{width}" height="{height}" rx="10" fill="{BG}"/>',
        f'<text x="{PAD_L}" y="24" fill="{ACCENT}" font-size="13" font-weight="600">'
        f'{d["total"]} contributions in the last year</text>',
        f'<text x="{width - 16}" y="24" fill="{FG}" font-size="11" text-anchor="end">'
        f'@{esc(d["user"])}</text>',
    ]

    # month labels
    seen = set()
    for wi, week in enumerate(weeks):
        first = week[0]["date"]
        mo = int(first.split("-")[1])
        if mo not in seen and int(first.split("-")[2]) <= 7:
            seen.add(mo)
            out.append(
                f'<text x="{PAD_L + wi * PITCH}" y="{PAD_T - 8}" fill="{FG}" '
                f'font-size="10">{MONTHS[mo - 1]}</text>'
            )

    # weekday labels
    for idx, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(
            f'<text x="0" y="{PAD_T + idx * PITCH + CELL - 2}" fill="{FG}" '
            f'font-size="9">{label}</text>'
        )

    # cells -- staggered fade+scale wave, left to right
    total_cols = len(weeks)
    for wi, week in enumerate(weeks):
        for day in week:
            x = PAD_L + wi * PITCH
            y = PAD_T + day["dow"] * PITCH
            fill = PALETTE[min(day["level"], 4)]
            delay = round(wi / total_cols * 2.2, 3)
            label = f'{day["count"]} contribution{"" if day["count"] == 1 else "s"} on {day["date"]}'
            out.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{fill}" opacity="0">'
                f'<title>{esc(label)}</title>'
                f'<animate attributeName="opacity" from="0" to="1" dur="0.45s" '
                f'begin="{delay}s" fill="freeze"/>'
                f'</rect>'
            )

    # legend
    ly = PAD_T + 7 * PITCH + 22
    out.append(f'<text x="{PAD_L}" y="{ly + 10}" fill="{FG}" font-size="10">Less</text>')
    for i, colour in enumerate(PALETTE):
        out.append(
            f'<rect x="{PAD_L + 32 + i * PITCH}" y="{ly}" width="{CELL}" height="{CELL}" '
            f'rx="2.5" fill="{colour}"/>'
        )
    out.append(
        f'<text x="{PAD_L + 32 + len(PALETTE) * PITCH + 6}" y="{ly + 10}" fill="{FG}" '
        f'font-size="10">More</text>'
    )

    stats = f'longest streak {d["longest_streak"]}d  ·  current {d["current_streak"]}d'
    out.append(
        f'<text x="{width - 16}" y="{ly + 10}" fill="{ACCENT}" font-size="10" '
        f'text-anchor="end">{stats}</text>'
    )

    out.append("</svg>")
    OUT.write_text("\n".join(out))
    print(f"Wrote {OUT} ({len(weeks)} weeks)")


if __name__ == "__main__":
    build()
