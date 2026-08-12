#!/usr/bin/env python3
import datetime as dt
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def level(count, maximum):
    if not count:
        return 0
    return min(4, max(1, round(count / max(maximum, 1) * 4)))


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    days = data["days"]
    first = dt.date.fromisoformat(days[0]["date"])
    padding = (first.weekday() + 1) % 7
    maximum = max(day["count"] for day in days)
    cells = []
    month_labels = []
    seen = set()
    for index, day in enumerate(days):
        date = dt.date.fromisoformat(day["date"])
        position = index + padding
        column, row = divmod(position, 7)
        if date.month not in seen and date.day <= 7:
            seen.add(date.month)
            month_labels.append((column, date.strftime("%b")))
        cells.append((column, row, day, level(day["count"], maximum)))
    columns = max(item[0] for item in cells) + 1
    width, height = 70 + columns * 15, 252
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="bodajava GitHub contribution graph">
<style>
  text {{ font-family: ui-monospace,SFMono-Regular,Menlo,monospace; }}
  .cell {{ opacity:0; animation:reveal .45s cubic-bezier(.2,.8,.2,1) forwards; }}
  @keyframes reveal {{ from {{ opacity:0; transform:translateY(-7px) }} to {{ opacity:1; transform:none }} }}
</style>
<defs><linearGradient id="bg" x2="0" y2="1"><stop stop-color="#0d1420"/><stop offset="1" stop-color="#080c12"/></linearGradient></defs>
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="12" fill="url(#bg)" stroke="#1f6feb" stroke-opacity=".65"/>
<circle cx="20" cy="17" r="5" fill="#ff5f56"/><circle cx="36" cy="17" r="5" fill="#ffbd2e"/><circle cx="52" cy="17" r="5" fill="#27c93f"/>
<text x="{width/2}" y="21" text-anchor="middle" fill="#7d8590" font-size="12">boda@github: ~/contributions --graph</text>
<line y1="34" y2="34" x2="{width}" stroke="#1f6feb" stroke-opacity=".35"/>''']
    for column, label in month_labels:
        parts.append(f'<text x="{48 + column*15}" y="52" fill="#7d8590" font-size="10">{label}</text>')
    for row, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        parts.append(f'<text x="12" y="{72 + row*15}" fill="#7d8590" font-size="9">{label}</text>')
    for column, row, day, color_level in cells:
        delay = column * .018 + row * .04
        title = html.escape(f"{day['date']}: {day['count']} contributions")
        parts.append(f'<rect class="cell" x="{48+column*15}" y="{62+row*15}" width="12" height="12" rx="2.5" fill="{PALETTE[color_level]}" style="animation-delay:{delay:.3f}s"><title>{title}</title></rect>')
    parts.extend([
        '<line x1="0" y1="181" x2="100%" y2="181" stroke="#1f6feb" stroke-opacity=".25"/>',
        f'<text x="20" y="207" fill="#39d353" font-size="13" font-weight="700">{data["total_contributions"]:,}<tspan fill="#7d8590" font-weight="400"> contributions in the last year</tspan></text>',
        f'<text x="20" y="231" fill="#7d8590" font-size="12">current streak <tspan fill="#22d3ee" font-weight="700">{data["current_streak"]} days</tspan>  ·  longest <tspan fill="#22d3ee" font-weight="700">{data["longest_streak"]} days</tspan></text>',
        f'<text x="{width-20}" y="231" text-anchor="end" fill="#7d8590" font-size="12">best day <tspan fill="#f2cc60" font-weight="700">{data["best_day"]["count"]}</tspan></text>',
        '</svg>'
    ])
    OUTPUT.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()

