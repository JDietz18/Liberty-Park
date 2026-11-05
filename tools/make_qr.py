"""Make the QR codes for the three Liberty Park option pages.

    python tools/make_qr.py

For each option this writes, into qr/:

    option-N.svg        plain code, vector, for dropping into a layout
    option-N.png        plain code, 2000 px, for the same
    option-N-card.png   print-ready card: title band, code with the option
                        number in its center, and the address in words

and one sheet, liberty-park-qr-cards.pdf, with all three cards on a letter
page. Every file is decoded again after it is written and the script fails if
any of them does not read back as the right address.

The codes use the highest error-correction level (H, about 30 percent), which
is what lets the card carry a number badge over the middle of the code.

Needs: pip install segno zxing-cpp pillow
"""
import os
import sys

import segno
import zxingcpp
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import content  # noqa: E402

OUT = os.path.join(ROOT, "qr")
FONT_CANDIDATES = (
    os.path.join(ROOT, "src", "ClashDisplayMedium.ttf"),
    r"M:\2027 Website\playcraft-site\public\assets\fonts\ClashDisplayMedium.ttf",
)
QUIET = 4          # modules of white margin, the QR standard's minimum
CARD_W, CARD_H = 1200, 1650


def font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    sys.exit("Clash Display Medium not found; map M: or copy the .ttf into src/")


def url_for(n):
    return f"{content.SITE}/option-{n}/"


def qr_image(code, size, dark, badge=None, badge_fill=None, badge_ink=None):
    """Draw the code as a square image `size` px wide, quiet zone included."""
    matrix = [list(row) for row in code.matrix]
    count = len(matrix)
    module = size // (count + 2 * QUIET)
    side = module * (count + 2 * QUIET)
    im = Image.new("RGB", (side, side), "white")
    d = ImageDraw.Draw(im)
    for y, row in enumerate(matrix):
        for x, on in enumerate(row):
            if on:
                x0 = (x + QUIET) * module
                y0 = (y + QUIET) * module
                d.rectangle((x0, y0, x0 + module - 1, y0 + module - 1), fill=dark)
    if badge is not None:
        # A round badge over the middle: about 22 percent of the code's width,
        # which covers under 5 percent of its area. Level H tolerates 30.
        r = round(count * module * 0.11)
        c = side // 2
        d.ellipse((c - r - module, c - r - module, c + r + module, c + r + module), fill="white")
        d.ellipse((c - r, c - r, c + r, c + r), fill=badge_fill)
        f = font(round(r * 1.5))
        d.text((c, c), str(badge), font=f, fill=badge_ink, anchor="mm")
    if side != size:
        im = im.resize((size, size), Image.NEAREST)
    return im


def card(n, code, colors):
    im = Image.new("RGB", (CARD_W, CARD_H), "white")
    d = ImageDraw.Draw(im)
    band = 400
    d.rectangle((0, 0, CARD_W, band), fill=colors["a1"])
    d.text((80, 70), content.PARK, font=font(64), fill=colors["on_a1"])
    d.text((74, 140), f"Option {n}", font=font(210), fill=colors["on_a1"])
    dark = colors["bg"] if n != 2 else colors["ink"]
    qr = qr_image(code, 960, dark, badge=n, badge_fill=colors["a1"], badge_ink=colors["on_a1"])
    im.paste(qr, ((CARD_W - 960) // 2, band + 40))
    d.text((CARD_W // 2, band + 40 + 960 + 70), "Scan to walk through it",
           font=font(72), fill=dark, anchor="mm")
    d.text((CARD_W // 2, band + 40 + 960 + 160), url_for(n).replace("https://", ""),
           font=font(34), fill=dark, anchor="mm")
    return im


def decode(path_or_image):
    im = Image.open(path_or_image) if isinstance(path_or_image, str) else path_or_image
    return [r.text for r in zxingcpp.read_barcodes(im.convert("RGB"))]


def main():
    os.makedirs(OUT, exist_ok=True)
    cards = []
    failed = False
    for n in sorted(content.OPTIONS):
        colors = content.OPTIONS[n]["colors"]
        dark = colors["bg"] if n != 2 else colors["ink"]   # option 2's page is light; use its navy
        url = url_for(n)
        code = segno.make(url, error="h", micro=False)

        svg = os.path.join(OUT, f"option-{n}.svg")
        code.save(svg, scale=10, border=QUIET, dark=dark, light="#ffffff", xmldecl=False)

        png = os.path.join(OUT, f"option-{n}.png")
        qr_image(code, 2000, dark).save(png, optimize=True)

        card_path = os.path.join(OUT, f"option-{n}-card.png")
        c = card(n, code, colors)
        c.save(card_path, dpi=(300, 300), optimize=True)
        cards.append(c)

        # read every raster back, plus the card shrunk to a phone-camera size
        small = c.resize((CARD_W // 4, CARD_H // 4), Image.LANCZOS)
        for label, target in (("png", png), ("card", card_path), ("card at quarter size", small)):
            got = decode(target)
            ok = got == [url]
            failed = failed or not ok
            print(f"option {n} {label}: {'reads ' + url if ok else 'FAILED, got ' + repr(got)}")

    # all three on one landscape letter page at 300 dpi
    page = Image.new("RGB", (3300, 2550), "white")
    scale = 0.78
    w, h = round(CARD_W * scale), round(CARD_H * scale)
    gap = (3300 - 3 * w) // 4
    for i, c in enumerate(cards):
        page.paste(c.resize((w, h), Image.LANCZOS), (gap + i * (w + gap), (2550 - h) // 2))
    pdf = os.path.join(OUT, "liberty-park-qr-cards.pdf")
    page.save(pdf, "PDF", resolution=300.0)
    got = sorted(decode(page))
    ok = got == sorted(url_for(n) for n in content.OPTIONS)
    failed = failed or not ok
    print(f"sheet: {'all three read' if ok else 'FAILED, got ' + repr(got)}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
