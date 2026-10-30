#!/usr/bin/env python3
"""Generate an original, font-free Kazumi NX NRO JPEG icon."""
from pathlib import Path
from argparse import ArgumentParser
from PIL import Image, ImageDraw

def create_icon(path: Path) -> None:
    im = Image.new("RGB", (256, 256), (18, 27, 52))
    p = im.load()
    for y in range(256):
        for x in range(256):
            p[x, y] = (15 + 17*x//256, 29 + 38*y//256, 50 + 22*x//256)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 14, 242, 242), radius=53,
                        fill=(18, 38, 68), outline=(64, 184, 216), width=6)
    d.polygon([(104, 72), (104, 182), (190, 127)], fill=(54, 219, 184))
    d.rounded_rectangle((70, 73, 90, 182), radius=8, fill=(244, 247, 250))
    d.line([(82, 131), (145, 71)], fill=(244, 247, 250), width=19)
    d.line([(84, 123), (146, 183)], fill=(244, 247, 250), width=19)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "JPEG", quality=82, optimize=True)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    create_icon(parser.parse_args().output)
