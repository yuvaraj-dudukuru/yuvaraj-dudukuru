"""Scrape the public GitHub contribution calendar into data/contributions.json.

No token required -- this reads the same public HTML that renders on a profile page.
"""

import json
import os
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER = os.environ.get("GH_PROFILE_USER", "yuvaraj-dudukuru")
URL = f"https://github.com/users/{USER}/contributions"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


def fetch():
    resp = requests.get(
        URL,
        headers={
            "Accept": "text/html",
            "User-Agent": "profile-art-bot",
            "X-Requested-With": "XMLHttpRequest",
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.text


def parse(html):
    soup = BeautifulSoup(html, "lxml")

    # Counts live in <tool-tip for="cell-id"> elements, not inside the cells.
    tips = {}
    for tip in soup.select("tool-tip"):
        target = tip.get("for")
        if not target:
            continue
        text = tip.get_text(" ", strip=True)
        count = 0
        for token in text.replace(",", "").split():
            if token.isdigit():
                count = int(token)
                break
        tips[target] = count

    days = []
    for cell in soup.select("td.ContributionCalendar-day"):
        date = cell.get("data-date")
        if not date:
            continue
        raw = cell.get("data-level")
        level = int(raw) if raw is not None else 0
        days.append({
            "date": date,
            "level": level,
            "count": tips.get(cell.get("id"), 0),
        })

    if not days:
        raise SystemExit("No contribution cells found -- GitHub markup may have changed.")

    days.sort(key=lambda d: d["date"])
    return days


def main():
    days = parse(fetch())
    total = sum(d["count"] for d in days)

    # longest run of consecutive days with any activity
    best = run = 0
    for d in days:
        run = run + 1 if d["level"] > 0 else 0
        best = max(best, run)

    # current streak, counting back from the most recent day
    current = 0
    for d in reversed(days):
        if d["level"] > 0:
            current += 1
        else:
            break

    payload = {
        "user": USER,
        "days": days,
        "total": total,
        "longest_streak": best,
        "current_streak": current,
        "start": days[0]["date"],
        "end": days[-1]["date"],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {len(days)} days for {USER} -> {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
