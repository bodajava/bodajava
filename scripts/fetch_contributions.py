#!/usr/bin/env python3
import datetime as dt
import json
import os
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_PROFILE_USER", "bodajava")
OUTPUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


def fetch_days():
    url = f"https://github.com/users/{USERNAME}/contributions"
    response = requests.get(url, headers={"User-Agent": "bodajava-profile/1.0"}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    for cell in soup.select("td.ContributionCalendar-day"):
        date = cell.get("data-date")
        if not date:
            continue
        tooltip = soup.find("tool-tip", attrs={"for": cell.get("id")})
        label = tooltip.get_text(" ", strip=True) if tooltip else ""
        match = re.search(r"([\d,]+) contribution", label, re.I)
        days.append({"date": date, "count": int(match.group(1).replace(",", "")) if match else 0})
    if not days:
        raise RuntimeError("GitHub contribution cells were not found")
    return sorted(days, key=lambda item: item["date"])


def streaks(days):
    longest = current = run = 0
    for day in days:
        run = run + 1 if day["count"] else 0
        longest = max(longest, run)
    index = len(days) - 1
    if index >= 0 and days[index]["count"] == 0:
        index -= 1
    while index >= 0 and days[index]["count"]:
        current += 1
        index -= 1
    return current, longest


def main():
    days = fetch_days()
    current, longest = streaks(days)
    best = max(days, key=lambda item: item["count"])
    payload = {
        "username": USERNAME,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": sum(day["count"] for day in days),
        "active_days": sum(day["count"] > 0 for day in days),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best,
        "days": days,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Fetched {len(days)} days and {payload['total_contributions']} contributions")


if __name__ == "__main__":
    main()

