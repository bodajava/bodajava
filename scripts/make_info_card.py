#!/usr/bin/env python3
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "info-card.svg"
ROWS = [
    ("user", "bodajava"),
    ("role", "Frontend Engineer"),
    ("focus", "Motion design · clean UI/UX"),
    ("stack", "TypeScript · JavaScript · GSAP"),
    ("building", "full-stack products & experiences"),
    ("location", "Giza, Egypt"),
    ("portfolio", "rptpfolio.vercel.app"),
]


def main():
    width, height = 520, 430
    lines = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="bodajava neofetch profile card">
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}} .row{{opacity:0;animation:show .45s ease-out forwards}} @keyframes show{{from{{opacity:0;transform:translateX(10px)}}to{{opacity:1;transform:none}}}}</style>
<rect x=".5" y=".5" width="519" height="429" rx="12" fill="#080c12" stroke="#1f6feb" stroke-opacity=".55"/>
<circle cx="20" cy="17" r="5" fill="#ff5f56"/><circle cx="36" cy="17" r="5" fill="#ffbd2e"/><circle cx="52" cy="17" r="5" fill="#27c93f"/>
<text x="260" y="21" text-anchor="middle" fill="#7d8590" font-size="12">boda@github: ~ $ neofetch</text><line y1="34" y2="34" x2="520" stroke="#1f6feb" stroke-opacity=".35"/>
<text x="28" y="82" fill="#39d353" font-size="22" font-weight="700">bodajava<tspan fill="#7d8590">@github</tspan></text>
<line x1="28" y1="97" x2="488" y2="97" stroke="#30363d"/>''']
    for index, (key, value) in enumerate(ROWS):
        y = 133 + index * 39
        lines.append(f'<g class="row" style="animation-delay:{.22+index*.11:.2f}s"><text x="28" y="{y}" fill="#22d3ee" font-size="13" font-weight="700">{html.escape(key):10}</text><text x="145" y="{y}" fill="#c9d1d9" font-size="13">{html.escape(value)}</text></g>')
    lines.extend(['<rect x="28" y="394" width="22" height="12" rx="2" fill="#1f6feb"/><rect x="56" y="394" width="22" height="12" rx="2" fill="#22d3ee"/><rect x="84" y="394" width="22" height="12" rx="2" fill="#39d353"/><rect x="112" y="394" width="22" height="12" rx="2" fill="#f2cc60"/>', '</svg>'])
    OUTPUT.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()

