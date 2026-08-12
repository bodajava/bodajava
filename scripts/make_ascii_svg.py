#!/usr/bin/env python3
import html
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source-photo.jpg"
OUTPUT = ROOT / "boda-ascii.svg"
RAMP = "@%#*+=-:. "
COLS = 56


def main():
    image = Image.open(SOURCE).convert("RGB")
    image = ImageOps.fit(image, (COLS, 42), method=Image.Resampling.LANCZOS)
    gray = ImageEnhance.Contrast(ImageOps.grayscale(image)).enhance(1.55)
    lines = []
    for y in range(gray.height):
        line = "".join(RAMP[pixel * (len(RAMP)-1) // 255] for pixel in [gray.getpixel((x, y)) for x in range(gray.width)])
        lines.append(html.escape(line.rstrip()))
    width, height = 420, 430
    body = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Animated ASCII portrait of bodajava">
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;fill:#c9d1d9;font-size:8.2px}} .line{{opacity:0;animation:type .16s ease-out forwards}} @keyframes type{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}</style>
<rect x=".5" y=".5" width="419" height="429" rx="12" fill="#080c12" stroke="#1f6feb" stroke-opacity=".55"/>
<circle cx="20" cy="17" r="5" fill="#ff5f56"/><circle cx="36" cy="17" r="5" fill="#ffbd2e"/><circle cx="52" cy="17" r="5" fill="#27c93f"/>
<text x="210" y="21" text-anchor="middle" fill="#7d8590" font-size="12">boda@github: ~/portrait.txt</text><line y1="34" y2="34" x2="420" stroke="#1f6feb" stroke-opacity=".35"/>''']
    for index, line in enumerate(lines):
        body.append(f'<text class="line" x="18" y="{52 + index*8.7:.1f}" xml:space="preserve" style="animation-delay:{index*.035:.3f}s">{line or " "}</text>')
    body.append('</svg>')
    OUTPUT.write_text("".join(body), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()

