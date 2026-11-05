# Liberty Park: three option presentations

One animated page per playground option, each reached by its own QR code.

| Option | Page | QR card |
|---|---|---|
| 1 | https://jdietz18.github.io/Liberty-Park/option-1/ | `qr/option-1-card.png` |
| 2 | https://jdietz18.github.io/Liberty-Park/option-2/ | `qr/option-2-card.png` |
| 3 | https://jdietz18.github.io/Liberty-Park/option-3/ | `qr/option-3-card.png` |

All three cards on one letter page: `qr/liberty-park-qr-cards.pdf`.
Plain codes for dropping into a layout: `qr/option-N.svg` and `qr/option-N.png`.

The pages are served by GitHub Pages straight from the `main` branch, so a
push is a publish. The repository is public: anything committed here can be
seen by anyone with the link.

## Changing something

Words, captions, colors, which renders appear where: edit `content.py`, then

    python build.py

Never edit `option-N/index.html` by hand. `build.py` overwrites it.
`python build.py --check` builds in memory and verifies without writing.

New or replaced renders: put them in the `OPTION 1`, `OPTION 2`, `OPTION 3`
folders (named `... RENDER_<n> ...jpg`), then

    python tools/make_images.py
    python build.py

and add a caption for any new render number in `content.py`. The build fails
if a render on disk has no caption, or a caption has no render.

QR codes only need remaking if the address changes (`SITE` in `content.py`):

    python tools/make_qr.py

It decodes every file it writes and fails if one does not read back.
**Printed codes point at the address above. If the pages ever move, the
printed codes stop working**, so settle the address before printing.

## What is where

    content.py           everything the pages say, and each option's colors
    build.py             content + src/ -> option-N/index.html
    src/template.html    page structure
    src/style.css        layout and motion (inlined into each page)
    src/app.js           scroll-linked motion and the full-size viewer (inlined)
    tools/make_images.py source renders -> img/ (2560, 1920 and 1280 wide)
    tools/make_qr.py     the QR codes and print cards
    img/                 web-sized renders; the 6-7 MB originals are not here
    qr/                  QR codes, cards and the print sheet

## Notes

- Fonts follow the Playcraft website set: Clash Display Medium for headlines
  (embedded in each page; the font file itself is not in this repository),
  DM Sans for text and Raleway for labels (Google Fonts).
- Captions describe only what the renders show. They name no products and
  make no compliance or accessibility claims.
- The pages respect the "reduce motion" setting: with it on, every section
  falls back to a plain, still layout and the walk becomes a swipeable row.
- Needs Python 3.12+ with `pillow`, `segno` and `zxing-cpp`.
