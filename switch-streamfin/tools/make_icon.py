#!/usr/bin/env python3
"""Generate an original icon for the Kazumi NX experiment; no copyrighted art."""
from pathlib import Path
from argparse import ArgumentParser
from PIL import Image, ImageDraw

def make_icon(path: Path) -> None:
    image = Image.new("RGB", (256, 256), (14, 24, 45))
    d = ImageDraw.Draw(image)
    d.rounded_rectangle((14, 14, 242, 242), radius=50,
                        fill=(20, 42, 73), outline=(55, 195, 217), width=7)
    d.polygon([(103, 70), (103, 184), (188, 127)], fill=(51, 218, 179))
    d.line([(70, 78), (70, 177)], fill=(247, 247, 248), width=19)
    d.line([(79, 128), (139, 79)], fill=(247, 247, 248), width=17)
    d.line([(79, 128), (139, 177)], fill=(247, 247, 248), width=17)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "JPEG", quality=83, optimize=True)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    make_icon(parser.parse_args().output)
