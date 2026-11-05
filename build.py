"""Build the three Liberty Park option pages.

    python build.py            # writes option-1/, option-2/, option-3/ index.html
    python build.py --check    # builds in memory and verifies, writes nothing

Inputs: content.py (copy and colors), src/template.html, src/style.css,
src/app.js, and the web images made by tools/make_images.py. Each page is one
self-contained HTML file apart from its pictures and the two Google fonts.

The headline font (Clash Display Medium) is not on Google Fonts, so it is
embedded as base64 from the Playcraft website's font folder.
"""
import base64
import html
import json
import os
import re
import sys
from urllib.parse import quote

import content

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
CLASH_SOURCE = r"M:\2027 Website\playcraft-site\public\assets\fonts\ClashDisplayMedium.woff2"
CLASH_LOCAL = os.path.join(SRC, "ClashDisplayMedium.woff2")
WIDTHS = (1280, 1920, 2560)
BANNED_FONTS = ("Bricolage Grotesque", "IBM Plex", "Inter", "Space Grotesk")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def clash_b64():
    """The embedded headline font. A copy is kept in src/ so the build still
    runs when the M: drive is not mapped."""
    path = CLASH_LOCAL if os.path.exists(CLASH_LOCAL) else CLASH_SOURCE
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def nn(n):
    return f"{n:02d}"


def srcset(option, n):
    return ", ".join(f"../img/option-{option}/{nn(n)}-{w}.jpg {w}w" for w in WIDTHS)


def img(option, n, alt, sizes, default=1280, lazy=True, extra=""):
    return (
        f'<img src="../img/option-{option}/{nn(n)}-{default}.jpg" '
        f'srcset="{srcset(option, n)}" sizes="{sizes}" width="2560" height="1440" '
        f'alt="{html.escape(alt, quote=True)}"'
        f'{" loading=\"lazy\"" if lazy else ""} decoding="async"{extra}>'
    )


def alt_for(view):
    title, text = view
    return f"{title}. {text}"


def favicon(n, colors):
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
        f"<circle cx='32' cy='32' r='32' fill='{colors['a1']}'/>"
        f"<text x='32' y='45' font-family='Arial,sans-serif' font-size='38' font-weight='700' "
        f"text-anchor='middle' fill='{colors['on_a1']}'>{n}</text></svg>"
    )
    return quote(svg, safe="")


def build_page(n, template, css, js, clash):
    opt = content.OPTIONS[n]
    views = opt["views"]
    order = sorted(views)
    index = {num: i for i, num in enumerate(order)}
    e = html.escape

    hero_slides = "\n".join(
        f'    <div class="hero__slide{" on" if i == 0 else ""}">'
        + img(n, num, alt_for(views[num]), "(max-width: 700px) 640px, 120vw",
              default=1920, lazy=i > 0)
        + "</div>"
        for i, num in enumerate(opt["hero"])
    )
    hero_ticks = "".join("<i></i>" for _ in opt["hero"])

    zones = "\n".join(
        f'        <li{" class=\"on\"" if i == 0 else ""}><h3>{e(t)}</h3><p>{e(d)}</p></li>'
        for i, (t, d) in enumerate(opt["zones"])
    )

    words = opt["words"]
    one_set = "".join(f"<span>{e(w)}</span><i></i>" for w in words)
    band = one_set * 6  # an even number of sets: the loop jumps back by half the row

    scenes = "\n".join(
        '      <figure class="scene">'
        f'<button class="scene__frame" type="button" data-open="{index[num]}" '
        f'aria-label="Open full size: {e(views[num][0], quote=True)}">'
        + img(n, num, alt_for(views[num]), "(max-width: 700px) 600px, 72vw", lazy=i > 1)
        + f"</button><figcaption><h3>{e(views[num][0])}</h3><p>{e(views[num][1])}</p></figcaption></figure>"
        for i, num in enumerate(opt["walk"])
    )

    above = "\n\n".join(
        '<section class="above">\n  <div class="above__pin">\n    <div class="above__frame">'
        + img(n, num, alt_for(views[num]), "(max-width: 700px) 640px, 100vw")
        + f'</div>\n    <div class="above__cap"><h2>{e(title)}</h2><p>{e(text)}</p></div>\n  </div>\n</section>'
        for num, title, text in opt["above"]
    )

    grid = "\n".join(
        f'    <button class="view" type="button" data-open="{index[num]}" '
        f'aria-label="Open full size: {e(views[num][0], quote=True)}">'
        + img(n, num, alt_for(views[num]), "(max-width: 900px) 100vw, 60vw")
        + f"<span>{e(views[num][0])}</span></button>"
        for num in order
    )

    cross = ""
    if content.CROSS_LINKS:
        links = "".join(
            f'<a href="../option-{k}/">Option {k}</a>' for k in sorted(content.OPTIONS) if k != n
        )
        cross = f'  <p class="foot__others">{links}</p>'

    ring_text = (f"{content.PARK}  \u2022  Option {n}  \u2022  " * 4).strip()
    # Circle crop: the image is 16:9 and fills the disc's height.
    plan_left = 50 - content.PLAN_CENTER_X * (16 / 9) * 100
    plan_top = (0.5 - content.PLAN_CENTER_Y) * 100

    colors = opt["colors"]
    values = {
        "PARK": e(content.PARK),
        "N": str(n),
        "SITE": content.SITE,
        "HEADLINE": e(opt["headline"]),
        "LEDE": e(opt["lede"]),
        "DISCLAIMER": e(content.DISCLAIMER),
        "BG": colors["bg"],
        "PANEL": colors["panel"],
        "INK": colors["ink"],
        "MUTED": colors["muted"],
        "A1": colors["a1"],
        "A2": colors["a2"],
        "A3": colors["a3"],
        "ON_A1": colors["on_a1"],
        "SCRIM": colors["scrim"],
        "FAVICON": favicon(n, colors),
        "HERO0": nn(opt["hero"][0]),
        "HERO0_SRCSET": srcset(n, opt["hero"][0]),
        "HERO_SLIDES": hero_slides,
        "HERO_TICKS": hero_ticks,
        "PLAN": nn(opt["plan"]),
        "PLAN_SRCSET": srcset(n, opt["plan"]),
        "PLAN_LEFT": f"{plan_left:.2f}",
        "PLAN_TOP": f"{plan_top:.2f}",
        "RING_TEXT": e(ring_text),
        "ZONES": zones,
        "BAND": band,
        "WALK_N": str(len(opt["walk"])),
        "SCENES": scenes,
        "ABOVE": above,
        "VIEWS": grid,
        "CROSS": cross,
        "VIEWS_JSON": json.dumps(
            [{"n": nn(num), "t": views[num][0], "d": views[num][1]} for num in order],
            ensure_ascii=False,
        ).replace("</", "<\\/"),
        "CLASH_B64": clash,
        "CSS": css,
        "JS": js,
    }
    page = re.sub(r"\{\{([A-Z0-9_]+)\}\}", lambda m: values[m.group(1)], template)
    return page


def check(n, page):
    """Fail loudly on the mistakes this build can actually make."""
    problems = []
    opt = content.OPTIONS[n]
    if "{{" in page:
        problems.append("unfilled template token")
    for font in BANNED_FONTS:
        # matches a quoted CSS family ("Inter") or a Google Fonts URL (family=Inter)
        name = "[+ ]".join(re.escape(word) for word in font.split())
        if re.search("['\"=]" + name + r"\b", page):
            problems.append(f"banned font: {font}")
    if "colour" in page.lower():
        problems.append("'colour' spelling")
    for ref in set(re.findall(r"\.\./img/option-\d/[\w-]+\.jpg", page)):
        if not os.path.exists(os.path.normpath(os.path.join(ROOT, "option-x", ref))):
            problems.append(f"missing image {ref}")
    used = set(opt["hero"]) | {opt["plan"]} | set(opt["walk"]) | {a[0] for a in opt["above"]}
    for num in sorted(used - set(opt["views"])):
        problems.append(f"render {num} is used but has no caption in views")
    folder = os.path.join(ROOT, "img", f"option-{n}")
    on_disk = {int(f[:2]) for f in os.listdir(folder) if f.endswith("-1280.jpg")}
    if on_disk != set(opt["views"]):
        problems.append(f"views {sorted(opt['views'])} do not match renders on disk {sorted(on_disk)}")
    if len(opt["zones"]) != 3:
        problems.append("the wheel expects exactly three zones")
    return problems


def main():
    check_only = "--check" in sys.argv
    template = read(os.path.join(SRC, "template.html"))
    css = read(os.path.join(SRC, "style.css"))
    js = read(os.path.join(SRC, "app.js"))
    clash = clash_b64()
    failed = False
    for n in sorted(content.OPTIONS):
        page = build_page(n, template, css, js, clash)
        problems = check(n, page)
        if problems:
            failed = True
            for p in problems:
                print(f"option {n}: {p}")
            continue
        if not check_only:
            out_dir = os.path.join(ROOT, f"option-{n}")
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8", newline="\n") as f:
                f.write(page)
        print(f"option {n}: ok, {len(page) / 1024:.0f} KB" + (" (not written)" if check_only else ""))
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
