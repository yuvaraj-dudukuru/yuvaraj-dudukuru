"""Generate info-card.svg -- a neofetch-style panel of who I am.

Edit ROWS below and re-run. Nothing else needs to change.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "info-card.svg"

HEADER = "yuvaraj@fraylon"
HOSTLINE = "Co-Founder & COO · Fraylon Technologies LLP"

ROWS = [
    ("name",      "Dudukuru Yuvaraj"),
    ("role",      "Co-Founder & COO @ Fraylon Technologies"),
    ("education", "B.Tech AI & Data Science '27 · St. Mary's"),
    ("stack",     "React · TypeScript · Node.js · Python"),
    ("ai",        "Gemini API · GenAI apps · CS50P / CS50AI"),
    ("shipped",   "certificates · academy · lumora"),
    ("building",  "LMS platforms · hosting · automation"),
    ("location",  "Hyderabad, India"),
    ("motto",     "Learn as long as you live"),
]

BG = "#0b0f14"
PANEL = "#0f1620"
ACCENT = "#14b8a6"
ACCENT_DIM = "#0f766e"
KEY = "#5eead4"
VAL = "#c7d3d1"
MUTED = "#6b8280"

W = 520
PAD = 24
ROW_H = 26
HEAD_H = 78
FOOT_H = 46


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build():
    height = HEAD_H + len(ROWS) * ROW_H + FOOT_H
    key_w = max(len(k) for k, _ in ROWS)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" '
        f'width="{W}" height="{height}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
        f'<rect width="{W}" height="{height}" rx="10" fill="{BG}"/>',
        f'<rect x="1" y="1" width="{W-2}" height="{height-2}" rx="10" fill="{PANEL}" '
        f'stroke="{ACCENT_DIM}" stroke-width="1"/>',
        # title bar
        f'<rect x="1" y="1" width="{W-2}" height="30" rx="10" fill="#0c131b"/>',
        f'<rect x="1" y="21" width="{W-2}" height="10" fill="#0c131b"/>',
        f'<circle cx="20" cy="16" r="4.5" fill="#ef4444"/>',
        f'<circle cx="36" cy="16" r="4.5" fill="#eab308"/>',
        f'<circle cx="52" cy="16" r="4.5" fill="{ACCENT}"/>',
        f'<text x="{W//2}" y="20" fill="{MUTED}" font-size="11" text-anchor="middle">'
        f'~/whoami</text>',
    ]

    # prompt line
    out.append(
        f'<text x="{PAD}" y="{HEAD_H - 22}" font-size="13" fill="{ACCENT}" font-weight="600" opacity="0">'
        f'{esc(HEADER)}'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.1s" fill="freeze"/>'
        f'</text>'
    )
    out.append(
        f'<text x="{PAD}" y="{HEAD_H - 6}" font-size="10.5" fill="{MUTED}" opacity="0">'
        f'{esc(HOSTLINE)}'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.25s" fill="freeze"/>'
        f'</text>'
    )
    out.append(
        f'<line x1="{PAD}" y1="{HEAD_H + 2}" x2="{W - PAD}" y2="{HEAD_H + 2}" '
        f'stroke="{ACCENT_DIM}" stroke-width="1" opacity="0.5"/>'
    )

    for i, (k, v) in enumerate(ROWS):
        y = HEAD_H + 22 + i * ROW_H
        begin = round(0.4 + i * 0.12, 2)
        out.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.35s" '
            f'begin="{begin}s" fill="freeze"/>'
            f'<text x="{PAD}" y="{y}" font-size="12" fill="{KEY}">{esc(k.ljust(key_w))}</text>'
            f'<text x="{PAD + key_w * 7.4 + 6}" y="{y}" font-size="12" fill="{MUTED}">:</text>'
            f'<text x="{PAD + key_w * 7.4 + 18}" y="{y}" font-size="12" fill="{VAL}">{esc(v)}</text>'
            f'</g>'
        )

    # colour strip footer, like neofetch
    fy = height - 26
    strip = [ACCENT, "#5eead4", "#0f766e", "#134e4a", "#eab308", "#ef4444", "#3b82f6", "#a855f7"]
    for i, colour in enumerate(strip):
        out.append(
            f'<rect x="{PAD + i * 22}" y="{fy}" width="18" height="10" rx="2" fill="{colour}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" '
            f'begin="{round(0.4 + len(ROWS) * 0.12 + i * 0.05, 2)}s" fill="freeze"/>'
            f'</rect>'
        )

    # blinking cursor
    out.append(
        f'<rect x="{W - PAD - 10}" y="{fy}" width="8" height="12" fill="{ACCENT}">'
        f'<animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite" '
        f'begin="{round(0.4 + len(ROWS) * 0.12, 2)}s"/>'
        f'</rect>'
    )

    out.append("</svg>")
    OUT.write_text("\n".join(out))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
