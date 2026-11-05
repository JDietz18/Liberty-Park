"""Make web-sized copies of the Liberty Park renders.

Source renders are 3840x2160 JPEGs of 6-7 MB each: too heavy for a phone that
just scanned a QR code. This writes three progressive JPEGs per render into
img/option-N/ (2560, 1920 and 1280 wide); the pages pick one with srcset.

    python tools/make_images.py                      # default source folders
    python tools/make_images.py "D:/renders"         # folder holding OPTION 1..3

Renders are numbered by the RENDER_<n> in the file name, so the order on the
page matches the order they were rendered in.
"""
import glob
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SRC = os.path.join(os.path.expanduser("~"), "OneDrive - PlayCore", "Desktop")
SIZES = ((2560, 80), (1920, 80), (1280, 78))  # (width, JPEG quality)


def render_number(path):
    return int(re.search(r"RENDER_(\d+)", os.path.basename(path)).group(1))


def main():
    src_root = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    total = 0
    for option in (1, 2, 3):
        files = sorted(
            glob.glob(os.path.join(src_root, f"OPTION {option}", "*.jpg")),
            key=render_number,
        )
        if not files:
            sys.exit(f"No renders found in {os.path.join(src_root, f'OPTION {option}')}")
        out_dir = os.path.join(ROOT, "img", f"option-{option}")
        os.makedirs(out_dir, exist_ok=True)
        for path in files:
            n = render_number(path)
            with Image.open(path) as im:
                im = im.convert("RGB")
                for width, quality in SIZES:
                    height = round(width * im.height / im.width)
                    out = os.path.join(out_dir, f"{n:02d}-{width}.jpg")
                    im.resize((width, height), Image.LANCZOS).save(
                        out, "JPEG", quality=quality, progressive=True, optimize=True
                    )
                    total += os.path.getsize(out)
        print(f"option {option}: {len(files)} renders")
    print(f"total {total / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
