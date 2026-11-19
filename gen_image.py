"""Generate the news-image-20261118 entry image (1024x1024 PNG).

Front page for Wednesday 18 November 2026. Six stories, chosen and
headline-checked with an external model against web sources (AP, Reuters,
AFP, USA Today, Al Jazeera, The Hindu). All drawing is PIL primitives with
DejaVu fonts; no network, no randomness, deterministic output.
Run: python3 gen_image.py  ->  writes entry.png beside this file.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)
NAVY = (20, 33, 61)
RED = (179, 39, 30)
GOLD = (201, 162, 39)
GRAY = (38, 44, 60)
TEAL = (14, 124, 123)
LIGHT = (233, 227, 211)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def icon_globe(d, cx, cy, r, ink):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ink, width=6)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=ink, width=4)
    d.line([cx - r, cy, cx + r, cy], fill=ink, width=4)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 200, 340, fill=ink, width=4)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 20, 160, fill=ink, width=4)
    for dx, dy in ((-0.45, -0.35), (0.5, 0.1), (-0.1, 0.55)):
        px, py = cx + dx * r, cy + dy * r
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255))


def icon_drone(d, cx, cy, s, ink):
    d.rounded_rectangle([cx - s * 0.42, cy - s * 0.16, cx + s * 0.42, cy + s * 0.16],
                        radius=10, fill=ink)
    for sx in (-1, 1):
        for sy in (-1, 1):
            ax, ay = cx + sx * s * 0.52, cy + sy * s * 0.30
            d.line([cx + sx * s * 0.30, cy + sy * s * 0.12, ax, ay], fill=ink, width=6)
            d.ellipse([ax - s * 0.16, ay - 5, ax + s * 0.16, ay + 5], fill=ink)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
    d.ellipse([cx - s * 0.24, cy + s * 0.36, cx + s * 0.24, cy + s * 0.84],
              outline=RED, width=5)


def icon_bridge(d, cx, cy, s, ink):
    d.line([cx - s * 0.62, cy + s * 0.28, cx - s * 0.62, cy - s * 0.30], fill=ink, width=8)
    d.line([cx + s * 0.62, cy + s * 0.28, cx + s * 0.62, cy - s * 0.30], fill=ink, width=8)
    d.line([cx - s * 0.62, cy + s * 0.28, cx - s * 0.12, cy + s * 0.28], fill=ink, width=10)
    d.line([cx + s * 0.12, cy + s * 0.28, cx + s * 0.62, cy + s * 0.28], fill=ink, width=10)
    d.arc([cx - s * 0.62, cy - s * 0.42, cx + s * 0.62, cy + s * 0.42],
          180, 360, fill=ink, width=6)
    # broken span: jagged crack in the middle of the deck
    d.line([cx - s * 0.12, cy + s * 0.28, cx - s * 0.04, cy + s * 0.04], fill=RED, width=8)
    d.line([cx - s * 0.04, cy + s * 0.04, cx + s * 0.06, cy + s * 0.28], fill=RED, width=8)
    d.line([cx + s * 0.06, cy + s * 0.28, cx + s * 0.12, cy + s * 0.28], fill=RED, width=8)


def icon_ballot(d, cx, cy, s, ink):
    d.rounded_rectangle([cx - s * 0.45, cy - s * 0.05, cx + s * 0.45, cy + s * 0.45],
                        radius=8, outline=ink, width=6)
    d.line([cx - s * 0.28, cy - s * 0.05, cx + s * 0.28, cy - s * 0.05], fill=ink, width=6)
    d.polygon([(cx - s * 0.16, cy - s * 0.42), (cx + s * 0.16, cy - s * 0.42),
               (cx + s * 0.10, cy - s * 0.08), (cx - s * 0.10, cy - s * 0.08)],
              fill=(255, 255, 255), outline=ink)
    d.line([cx - s * 0.30, cy + s * 0.12, cx - s * 0.08, cy + s * 0.32], fill=RED, width=8)
    d.line([cx - s * 0.08, cy + s * 0.32, cx + s * 0.34, cy - s * 0.18], fill=RED, width=8)


def icon_chip(d, cx, cy, s, ink):
    d.rounded_rectangle([cx - s * 0.34, cy - s * 0.34, cx + s * 0.34, cy + s * 0.34],
                        radius=10, fill=ink)
    d.rounded_rectangle([cx - s * 0.16, cy - s * 0.16, cx + s * 0.16, cy + s * 0.16],
                        radius=6, outline=GOLD, width=4)
    for i in (-1, 0, 1):
        off = i * s * 0.20
        d.line([cx + off, cy - s * 0.34, cx + off, cy - s * 0.52], fill=ink, width=6)
        d.line([cx + off, cy + s * 0.34, cx + off, cy + s * 0.52], fill=ink, width=6)
        d.line([cx - s * 0.34, cy + off, cx - s * 0.52, cy + off], fill=ink, width=6)
        d.line([cx + s * 0.34, cy + off, cx + s * 0.52, cy + off], fill=ink, width=6)


def icon_cyclone(d, cx, cy, s, ink):
    for k, r in enumerate((0.14, 0.28, 0.42, 0.55)):
        start = 40 + k * 95
        d.arc([cx - s * r, cy - s * r, cx + s * r, cy + s * r],
              start, start + 250, fill=TEAL if k % 2 else ink, width=7)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # side margin

    # ---- masthead banner ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((mx, 18), "WORLD NEWS", font=font(SERIF_B, 62), fill=(255, 255, 255))
    d.text((mx, 92), "Wednesday, 18 November 2026", font=font(SANS_B, 34),
           fill=(232, 180, 74))
    d.rectangle([0, 148, W, 154], fill=GOLD)

    # ---- lead story: summit ----
    y = 176
    d.text((mx, y), "SUMMIT IN SHENZHEN", font=font(SANS_B, 24), fill=RED)
    y += 34
    hl = wrap(d, "Trump Lands in Shenzhen; Xi Meets Putin", font(SANS_B, 48), 640)
    y = draw_lines(d, hl, mx, y, font(SANS_B, 48), NAVY, 56)
    y += 6
    dk = wrap(d, "First US\u2013China\u2013Russia summit set for Thursday at APEC",
              font(SANS_B, 29), 640)
    y = draw_lines(d, dk, mx, y, font(SANS_B, 29), NAVY, 36)
    icon_globe(d, 880, 272, 64, NAVY)
    _cap = "SHENZHEN \u2022 APEC"
    _cw = d.textlength(_cap, font=font(SANS_B, 20))
    d.text((880 - _cw / 2, 348), _cap, font=font(SANS_B, 20), fill=NAVY)
    d.line([mx, 468, W - mx, 468], fill=NAVY, width=3)

    # ---- secondary row: stories 2 and 3 ----
    col_w = (W - 2 * mx - 24) // 2
    y0 = 492
    second = [
        ("GULF CRISIS", "Iran Drones Target US Base in Kuwait",
         "Kuwait, Bahrain intercept drones; US hits missile site on Qeshm",
         icon_drone),
        ("WAR IN UKRAINE", "Ukraine Strikes Kerch Bridge Again",
         "Day two of strikes; Russia claims 1,400 drones downed",
         icon_bridge),
    ]
    for i, (tag, head, deck, icon) in enumerate(second):
        x = mx + i * (col_w + 24)
        d.text((x, y0), tag, font=font(SANS_B, 22), fill=RED)
        hh = wrap(d, head, font(SANS_B, 31), col_w - 108)
        yy = draw_lines(d, hh, x, y0 + 32, font(SANS_B, 31), NAVY, 37)
        dd = wrap(d, deck, font(SANS, 21), col_w - 108)
        draw_lines(d, dd, x, yy + 4, font(SANS, 21), GRAY, 27)
        icon(d, x + col_w - 52, y0 + 78, 80, NAVY)
    d.line([mx, 706, W - mx, 706], fill=NAVY, width=3)

    # ---- small row: stories 4, 5, 6 ----
    col3 = (W - 2 * mx - 48) // 3
    y1 = 724
    small = [
        ("US POLITICS", "Peltola Wins Alaska; Democrats Take 56\u201344",
         "Senate now 56\u201344; ninth flip, biggest since 2009",
         icon_ballot),
        ("TECH", "Nvidia Rejects Huang's Return",
         "Record $115.8B quarter amid transition", icon_chip),
        ("DISASTER", "Cyclone Akvan Bears Down on Odisha",
         "Odisha evacuates; schools shut", icon_cyclone),
    ]
    for i, (tag, head, deck, icon) in enumerate(small):
        x = mx + i * (col3 + 24)
        if i:
            d.line([x - 12, y1, x - 12, 962], fill=(210, 203, 185), width=2)
        d.text((x, y1), tag, font=font(SANS_B, 21), fill=RED)
        icon(d, x + 34, y1 + 62, 56, NAVY)
        hh = wrap(d, head, font(SANS_B, 24), col3)
        yy = draw_lines(d, hh, x, y1 + 108, font(SANS_B, 24), NAVY, 29)
        dd = wrap(d, deck, font(SANS, 19), col3)
        draw_lines(d, dd, x, yy + 4, font(SANS, 19), GRAY, 24)

    # ---- footer ----
    d.line([mx, 972, W - mx, 972], fill=GOLD, width=2)
    d.text((mx, 982), "Sources: AP, Reuters, AFP, USA Today, Al Jazeera, The Hindu",
           font=font(SANS, 16), fill=GRAY)
    d.text((W - mx - 220, 982), "All events of 18 Nov 2026", font=font(SANS_B, 16),
           fill=GRAY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
