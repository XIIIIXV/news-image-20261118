"""Generate the news-image-20261118 entry image v4 (1024x1024 PNG).

"ONE DAY ON EARTH" — a map-first broadsheet for Wednesday 18 Nov 2026.
Deliberately unlike the reference and unlike v3 (which cloned it):
  - no masthead "THE DAY IN WORLD NEWS", no region strip, no time strip,
    no "WHERE IT HAPPENED", no numbered "ALSO ON..." list, no DATE CHECK
    box, no "Reads at three sizes" footer, no 3-row grid of 11 leads,
    no navy masthead + red date box.
  - instead: a NEW name, a deep ink/teal + amber identity, a LARGE dot
    world map as the hero (~36% of the page) with amber pins for the
    11 biggest stories, a "BY THE NUMBERS" data strip, stories grouped
    by THEME (not region), 11 leads as cards in 3+4+4 rows, and the
    remaining 31 stories as a compact bullet index under a new label.
  - the NEWS is also mostly new: 38 of 42 stories are fresh; only 4
    (Shenzhen summit, Voyager 1, GTA VI, Cyclone Akvan) carry over from
    v3, and only as one-line index briefs, never as leads.

Content: 42 stories, all verified as happening or first reported on
Wednesday 18 November 2026. Tuesday items stay out (Nvidia results,
Alaska Senate call, Qeshm strike, Knesset speaker vote, Kerch Bridge
collapse, US measles ruling, Russian airspace violation, Colombia Q3
GDP). Sources are named on each card.

Design (Impeccable typeset/layout/craft-floor, translated to PIL/print):
- exactly two families: DejaVu Serif Bold (masthead + headlines) and
  DejaVu Sans / Sans Bold (labels, decks, briefs); clear size steps
  between roles, never adjacent sizes doing different jobs.
- squint test: masthead -> big map -> numbers strip -> 3 hero leads ->
  4 leads -> 4 text leads -> index, in that order; grouping by
  proximity, hairline rules, no boxes around every group; tight inside
  a card, generous between sections; 4px spacing scale.
- contrast: body text near-black on paper (>=4.5:1), white/pale-teal
  on the dark map panel; no gradient text, no emoji, no hard shadows;
  numbers 1-11 are functional (they cross-reference the map pins),
  not decoration.
- all text is real PIL text (DejaVu); all visuals are clearly
  illustrative/stylised (no photorealistic people, no real faces).
  Panel callouts ("EUR 3.5bn", "14%", "162.5%") are PIL text overlaid
  on the illustrations, never AI-generated text.

Assets live in repo/assets/ (fixed files); crops/resizes are fixed;
no network, no randomness, deterministic output.
Run: python3 gen_image.py  ->  writes entry.png beside this file.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

# --- palette: deep ink/teal + amber (NOT navy + red) ---
PAPER = (246, 241, 231)
CARD = (255, 253, 247)
INK = (16, 49, 46)          # deep ink-teal (text, masthead)
TEAL = (13, 51, 49)         # map panel background
TEAL_MID = (31, 92, 85)     # mid teal (panels, accents)
AMBER = (232, 163, 23)
AMBER_D = (176, 116, 8)
PALE = (143, 191, 181)      # pale teal (map dots, legend text)
MUTED = (74, 93, 89)        # muted text (teal-tinted, not grey)
RULE = (201, 191, 169)
WHITE = (255, 255, 255)
CREAM = (246, 241, 231)
BROWN = (90, 60, 25)        # warm brown (bottle panel)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"

MX = 42                      # page margin
CW = W - 2 * MX              # content width = 940

# --- verified content (see research notes; 38 new, 4 overlap briefs) ---
# leads: n, place, theme, headline, deck, source, panel kind
# panel: ("img", filename, focus_y) or ("pil", name)
LEADS = [
    dict(n=1, place="RIYADH", theme="WAR",
         head="Missiles over Riyadh as Houthis strike the capital",
         deck="Two cruise missiles bound for Riyadh are intercepted; "
              "explosions rattle homes across the city.",
         src="REUTERS", panel=("img", "riyadh.webp", 0.5)),
    dict(n=2, place="SHENZHEN", theme="TECH",
         head="China's humanoid robots are coming home",
         deck="A robot already serves ice cream at a Shenzhen park stand; "
              "Beijing wants them in homes next.",
         src="STANDARD TOPIC", panel=("img", "robot.webp", 0.5)),
    dict(n=3, place="SOMERSET", theme="LIFE",
         head="Glastonbury 2027: Styles, Fender, Eilish — and Cher",
         deck="Harry Styles, Sam Fender and Billie Eilish top the bill; "
              "Cher takes the legends slot.",
         src="BBC", panel=("img", "glasto.webp", 0.5)),
    dict(n=4, place="GAZA", theme="WAR",
         head="Gaza truce 'on the brink', peace board warns",
         deck="The Board of Peace tells the UN the ceasefire nears collapse.",
         src="BOARD OF PEACE", panel=("img", "gaza.webp", 0.5)),
    dict(n=5, place="CAIRO", theme="MONEY",
         head="EU 'sugarcoated' Egypt's figures to free loans",
         deck="Leaked papers say poverty rolls shrank as MEPs were told "
              "they grew.",
         src="THE GUARDIAN", panel=("pil", "scales", None)),
    dict(n=6, place="SAN FRAN", theme="TECH",
         head="OpenAI's models now design better chips",
         deck="AI-tuned circuits beat AMD GPU blocks by up to 14% — "
              "verified on real silicon.",
         src="OPENAI", panel=("pil", "chip", None)),
    dict(n=7, place="NEW DELHI", theme="MONEY",
         head="India slaps 162.5% levy on Scotch whisky",
         deck="Bulk Scotch faces a duty above the pre-deal 150% rate, "
              "sources say.",
         src="REUTERS", panel=("pil", "bottle", None)),
    dict(n=8, place="LONDON", theme="LIFE",
         head="Harry: 'I'd rejoin the Army to fight Russia'",
         deck="After a trip to Ukraine, the duke says Britain should be nervous.",
         src="BBC", panel=None),
    dict(n=9, place="BRUSSELS", theme="MONEY",
         head="EU approves Indonesia trade and investment deals",
         deck="The Council signs off the CEPA and investment pacts.",
         src="EU COUNCIL", panel=None),
    dict(n=10, place="NEW YORK", theme="MONEY",
         head="TJX jumps 10% as shoppers lift retail; Dow falls",
         deck="Target rises 5.6% on strong results; UnitedHealth slides 7%.",
         src="MOTLEY FOOL", panel=None),
    dict(n=11, place="JOHANNESBURG", theme="TECH",
         head="Cassava seeks $1bn for Nvidia chips in Africa",
         deck="The group talks to US and Gulf investors to build AI data centres.",
         src="TECHCABAL", panel=None),
]

# index briefs (31 one-liners, bullet dots, NOT numbered).
# first 27 are new; last 4 are the only v3 overlaps (index only).
BRIEFS = [
    "Nigeria: hiring freeze across federal agencies",
    "Nigeria: 128 police chiefs redeployed",
    "Nigeria: Plateau killings threaten US deal",
    "Telkom to sell Amazon Leo internet in SA",
    "Takaichi, Xi shake hands at APEC",
    "Antelope Reef runway takes shape",
    "India: 78,000 deaths in climate disasters",
    "ECB race: Brunnermeier nominated",
    "Trump family told to preserve records",
    "Zverev beats Shelton, into ATP semis",
    "England win ODI series in Australia",
    "Pulisic sends USA to Nations League semis",
    "FIFA rankings: Spain top, Morocco 5th",
    "Israel reopens Beit Hanoun crossing",
    "ADNOC vessel hit in Hormuz; 1 missing",
    "US targets Hizballah charity, gold network",
    "Turkey, Qatar sign defence pact",
    "Iraq confronts Kataib Hezbollah",
    "Google Genie 4 rolls out",
    "Gemini 4 Neon launches",
    "OpenAI launches GPT-6.2 Astra, Sol",
    "Tube strike by <24; TfL hack hits 260,000",
    "Palestinian woman shot dead near Jericho",
    "Australia: gender pay gap below 20%",
    "Yemen: 64 children killed since Sept",
    "Panama: world 'held hostage by oil mafia'",
    "Businesses back Britain rejoining EU",
    # --- the only v3 overlaps (4), index only, never leads ---
    "Shenzhen: Trump, Xi, Putin gather",
    "Voyager 1: one light-day from Earth",
    "GTA VI goes on sale after 13 years",
    "Cyclone Akvan bears down on Odisha",
]

# numbers strip: (big number, label) — every stat maps to a story on the page
NUMBERS = [
    ("$1bn", "Cassava's Nvidia chip fund"),
    ("162.5%", "India's Scotch whisky levy"),
    ("€3.5bn", "EU loans to Egypt"),
    ("260,000", "Oyster users hit by TfL hack"),
    ("78,000", "India climate-disaster deaths"),
    ("10.4%", "TJX's jump on retail results"),
]

# map pins: lead number -> (lon, lat)
PINS = {
    1: (46.7, 24.7),      # Riyadh
    2: (114.05, 22.55),   # Shenzhen
    3: (-2.6, 51.1),      # Glastonbury (offset: London cluster)
    4: (34.45, 31.5),     # Gaza
    5: (31.2, 30.0),      # Cairo (offset: Gaza cluster)
    6: (-122.4, 37.8),    # San Francisco
    7: (28.0, -26.2),     # Johannesburg
    8: (-0.1, 51.5),      # London (offset: Glastonbury/Brussels cluster)
    9: (4.35, 50.85),     # Brussels (offset: London cluster)
    10: (-74.0, 40.7),    # New York
    11: (77.2, 28.6),     # New Delhi
}
# pins drawn away from their true spot (leader line to the true spot)
PIN_OFFSET = {3: (-16, 14), 5: (-14, 16), 8: (16, -13), 9: (20, 8)}
MAP_W, MAP_H = 940, 371
MAP_LON_MIN, MAP_LON_MAX = -180.0, 180.0
MAP_LAT_MIN, MAP_LAT_MAX = -58.0, 84.0


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


def cover(img, tw, th, focus_y=0.5):
    """Crop img to target aspect around focus_y, then resize."""
    iw, ih = img.size
    target = tw / th
    if iw / ih > target:
        nw = int(ih * target)
        x0 = (iw - nw) // 2
        box = (x0, 0, x0 + nw, ih)
    else:
        nh = int(iw / target)
        cy = int(ih * focus_y)
        y0 = max(0, min(ih - nh, cy - nh // 2))
        box = (0, y0, iw, y0 + nh)
    return img.crop(box).resize((tw, th), Image.LANCZOS)


def load(name):
    return Image.open(ASSETS / name).convert("RGB")


def lonlat_to_xy(lon, lat):
    x = (lon - MAP_LON_MIN) / (MAP_LON_MAX - MAP_LON_MIN) * MAP_W
    y = (MAP_LAT_MAX - lat) / (MAP_LAT_MAX - MAP_LAT_MIN) * MAP_H
    return (x, y)


def draw_pin(d, cx, cy, n, r=7):
    """Amber pin with a dark number."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=AMBER,
              outline=WHITE, width=1)
    d.text((cx, cy), str(n), font=font(SANS_B, 9), fill=INK, anchor="mm")


# ---------- PIL-drawn panels (flat infographic style) ----------

def scales_panel(w, h):
    """Balance scale + EUR 3.5bn (Egypt / EU loans)."""
    img = Image.new("RGB", (w, h), TEAL_MID)
    d = ImageDraw.Draw(img)
    # scale
    d.line([50, 16, 50, 60], fill=WHITE, width=3)
    d.line([22, 20, 78, 20], fill=WHITE, width=3)
    d.polygon([(50, 11), (46, 19), (54, 19)], fill=WHITE)
    for cx in (22, 78):
        d.line([cx, 20, cx - 8, 38], fill=WHITE, width=2)
        d.line([cx, 20, cx + 8, 38], fill=WHITE, width=2)
        d.pieslice([cx - 10, 36, cx + 10, 52], start=0, end=180,
                   fill=AMBER)
    d.rectangle([38, 60, 62, 64], fill=WHITE)
    d.rectangle([30, 64, 70, 68], fill=WHITE)
    f1 = font(SANS_B, 18)
    t = "€3.5bn"
    d.text(((w - d.textlength(t, font=f1)) / 2, 76), t, font=f1,
           fill=WHITE)
    f2 = font(SANS_B, 8)
    t2 = "EU LOANS"
    d.text(((w - d.textlength(t2, font=f2)) / 2, 96), t2, font=f2,
           fill=AMBER)
    return img


def chip_panel(w, h):
    """Chip + 14% (OpenAI designs chips)."""
    img = Image.new("RGB", (w, h), INK)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([20, 14, 80, 58], radius=6, fill=TEAL_MID,
                        outline=AMBER, width=2)
    d.rounded_rectangle([30, 24, 70, 48], radius=3, fill=INK)
    for py in (22, 32, 42, 52):
        d.rectangle([14, py, 20, py + 4], fill=AMBER)
        d.rectangle([80, py, 86, py + 4], fill=AMBER)
    d.line([50, 14, 50, 8], fill=AMBER, width=2)
    d.line([50, 58, 50, 64], fill=AMBER, width=2)
    f1 = font(SANS_B, 18)
    t = "14%"
    d.text(((w - d.textlength(t, font=f1)) / 2, 72), t, font=f1,
           fill=WHITE)
    f2 = font(SANS_B, 8)
    t2 = "BETTER"
    d.text(((w - d.textlength(t2, font=f2)) / 2, 94), t2, font=f2,
           fill=AMBER)
    return img


def bottle_panel(w, h):
    """Whisky bottle + 162.5% (India Scotch levy)."""
    img = Image.new("RGB", (w, h), BROWN)
    d = ImageDraw.Draw(img)
    d.rectangle([42, 8, 58, 30], fill=CREAM)
    d.rounded_rectangle([30, 30, 70, 72], radius=8, fill=CREAM)
    d.rectangle([34, 44, 66, 60], fill=AMBER)
    d.text((50, 52), "%", font=font(SANS_B, 12), fill=INK, anchor="mm")
    f1 = font(SANS_B, 15)
    t = "162.5%"
    d.text(((w - d.textlength(t, font=f1)) / 2, 78), t, font=f1,
           fill=WHITE)
    f2 = font(SANS_B, 8)
    t2 = "LEVY"
    d.text(((w - d.textlength(t2, font=f2)) / 2, 96), t2, font=f2,
           fill=AMBER)
    return img


PIL_PANELS = {"scales": scales_panel, "chip": chip_panel,
              "bottle": bottle_panel}


def build_panel(lead, pw, ph):
    kind, name, focus = lead["panel"]
    if kind == "pil":
        return PIL_PANELS[name](pw, ph)
    return cover(load(name), pw, ph, focus_y=focus if focus else 0.5)


def tag_line(lead):
    return "%d · %s · %s" % (lead["n"], lead["theme"], lead["place"])


# ---------- card painters ----------

def hero_card(img, d, x, y, cw, ch, lead):
    """Row 1: image left (square-ish), text right."""
    pw, ph = 132, ch
    panel = build_panel(lead, pw, ph)
    img.paste(panel, (x, y))
    tx = x + pw + 8
    tw = cw - pw - 8
    ty = y + 2
    d.text((tx, ty), tag_line(lead), font=font(SANS_B, 8), fill=AMBER_D)
    ty += 14
    hl = wrap(d, lead["head"], font(SERIF_B, 13), tw)
    assert len(hl) <= 3, "hero headline %d wraps %d" % (lead["n"], len(hl))
    for ln in hl:
        d.text((tx, ty), ln, font=font(SERIF_B, 13), fill=INK)
        ty += 16
    ty += 3
    dk = wrap(d, lead["deck"], font(SANS, 9), tw)
    assert len(dk) <= 3, "hero deck %d wraps %d" % (lead["n"], len(dk))
    for ln in dk:
        d.text((tx, ty), ln, font=font(SANS, 9), fill=MUTED)
        ty += 11
    d.text((tx, y + ch - 12), lead["src"], font=font(SANS, 8),
           fill=(140, 140, 130))


def mid_card(img, d, x, y, cw, ch, lead):
    """Row 2: image/graphic left, text right."""
    pw, ph = 100, ch
    panel = build_panel(lead, pw, ph)
    img.paste(panel, (x, y))
    tx = x + pw + 8
    tw = cw - pw - 8
    ty = y + 1
    d.text((tx, ty), tag_line(lead), font=font(SANS_B, 8), fill=AMBER_D)
    ty += 13
    hl = wrap(d, lead["head"], font(SERIF_B, 12), tw)
    assert len(hl) <= 3, "mid headline %d wraps %d" % (lead["n"], len(hl))
    for ln in hl:
        d.text((tx, ty), ln, font=font(SERIF_B, 12), fill=INK)
        ty += 15
    ty += 2
    dk = wrap(d, lead["deck"], font(SANS, 8), tw)
    assert len(dk) <= 3, "mid deck %d wraps %d" % (lead["n"], len(dk))
    for ln in dk:
        d.text((tx, ty), ln, font=font(SANS, 8), fill=MUTED)
        ty += 10
    d.text((tx, y + ch - 11), lead["src"], font=font(SANS, 7),
           fill=(140, 140, 130))


def text_card(d, x, y, cw, ch, lead):
    """Row 3: big amber number + tag, headline, deck, source."""
    d.text((x, y - 2), str(lead["n"]), font=font(SERIF_B, 22),
           fill=AMBER_D)
    n_w = d.textlength(str(lead["n"]), font=font(SERIF_B, 22))
    d.text((x + n_w + 8, y + 6), "%s · %s" % (lead["theme"], lead["place"]),
           font=font(SANS_B, 8), fill=AMBER_D)
    ty = y + 28
    hl = wrap(d, lead["head"], font(SERIF_B, 12), cw)
    assert len(hl) <= 2, "text headline %d wraps %d" % (lead["n"], len(hl))
    for ln in hl:
        d.text((x, ty), ln, font=font(SERIF_B, 12), fill=INK)
        ty += 15
    ty += 2
    dk = wrap(d, lead["deck"], font(SANS, 9), cw)
    assert len(dk) <= 2, "text deck %d wraps %d" % (lead["n"], len(dk))
    for ln in dk:
        d.text((x, ty), ln, font=font(SANS, 9), fill=MUTED)
        ty += 11
    d.text((x, y + ch - 11), lead["src"], font=font(SANS, 7),
           fill=(140, 140, 130))


# ---------- build ----------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # amber top bar
    d.rectangle([0, 0, W, 5], fill=AMBER)

    # ---- masthead (y 10-76) ----
    d.text((MX, 30), "WEDNESDAY · 18 NOVEMBER 2026",
           font=font(SANS_B, 10), fill=INK)
    title = "ONE DAY ON EARTH"
    f_title = font(SERIF_B, 40)
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 18), title, font=f_title, fill=INK)
    tag_r = "ONE PLANET · ONE DAY"
    d.text((W - MX - d.textlength(tag_r, font=font(SANS_B, 10)), 30),
           tag_r, font=font(SANS_B, 10), fill=INK)
    d.line([MX, 78, W - MX, 78], fill=INK, width=1)

    # ---- hero map panel (y 84-455) ----
    map_x, map_y = MX, 84
    d.rectangle([map_x, map_y, map_x + MAP_W, map_y + MAP_H], fill=TEAL)
    dots = Image.open(ASSETS / "world_dots_big.png").convert("RGBA")
    img.paste(dots, (map_x, map_y), dots)
    d.rectangle([map_x, map_y, map_x + MAP_W, map_y + 28],
                fill=(10, 42, 40))
    d.text((map_x + 12, map_y + 10), "THE WORLD IN ONE DAY",
           font=font(SANS_B, 11), fill=AMBER)
    note = "PINS 1–11 MARK THE BIGGEST STORIES"
    d.text((map_x + MAP_W - 12 - d.textlength(note, font=font(SANS_B, 9)),
            map_y + 12), note, font=font(SANS_B, 9), fill=PALE)
    for n, (lon, lat) in PINS.items():
        px, py = lonlat_to_xy(lon, lat)
        if n in PIN_OFFSET:
            dx, dy = PIN_OFFSET[n]
            d.line([map_x + px, map_y + py, map_x + px + dx,
                    map_y + py + dy], fill=AMBER, width=1)
            d.ellipse([map_x + px - 2, map_y + py - 2,
                       map_x + px + 2, map_y + py + 2], fill=AMBER)
            draw_pin(d, map_x + px + dx, map_y + py + dy, n)
        else:
            draw_pin(d, map_x + px, map_y + py, n)
    d.text((map_x + 12, map_y + MAP_H - 20),
           "Amber pins mark the 11 biggest stories — read them below, "
           "in number order.",
           font=font(SANS, 9), fill=PALE)

    # ---- BY THE NUMBERS strip (y 463-527) ----
    ny = 463
    d.rectangle([MX, ny, W - MX, ny + 64], fill=CARD)
    d.line([MX, ny, W - MX, ny], fill=TEAL_MID, width=2)
    d.text((MX + 10, ny + 5), "BY THE NUMBERS",
           font=font(SANS_B, 9), fill=AMBER_D)
    cell_w = CW // 6
    f_num = font(SANS_B, 22)
    f_lab = font(SANS, 8)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = MX + i * cell_w
        if i:
            d.line([cx, ny + 22, cx, ny + 58], fill=RULE, width=1)
        nw = d.textlength(num, font=f_num)
        d.text((cx + (cell_w - nw) / 2, ny + 20), num, font=f_num,
               fill=INK)
        lw = d.textlength(lab, font=f_lab)
        assert lw <= cell_w - 8, "number label too wide: %s" % lab
        d.text((cx + (cell_w - lw) / 2, ny + 48), lab, font=f_lab,
               fill=MUTED)

    # ---- leads row 1: 3 hero cards (y 535-665) ----
    r1y, r1h = 535, 130
    gap = 10
    cw1 = (CW - 2 * gap) // 3
    x = MX
    for lead in LEADS[0:3]:
        hero_card(img, d, x, r1y, cw1, r1h, lead)
        x += cw1 + gap
        if lead is not LEADS[2]:
            d.line([x - gap + 4, r1y + 6, x - gap + 4, r1y + r1h - 6],
                   fill=RULE, width=1)

    # ---- leads row 2: 4 cards (y 673-781) ----
    r2y, r2h = 673, 108
    cw2 = (CW - 3 * gap) // 4
    x = MX
    for lead in LEADS[3:7]:
        mid_card(img, d, x, r2y, cw2, r2h, lead)
        x += cw2 + gap
        if lead is not LEADS[6]:
            d.line([x - gap + 4, r2y + 6, x - gap + 4, r2y + r2h - 6],
                   fill=RULE, width=1)

    # ---- leads row 3: 4 text cards (y 789-885) ----
    r3y, r3h = 789, 96
    cw3 = (CW - 3 * gap) // 4
    x = MX
    for lead in LEADS[7:11]:
        text_card(d, x, r3y, cw3, r3h, lead)
        x += cw3 + gap
        if lead is not LEADS[10]:
            d.line([x - gap + 4, r3y + 6, x - gap + 4, r3y + r3h - 6],
                   fill=RULE, width=1)

    # ---- index: THE REST OF THE DAY (y 895-1000) ----
    iy = 895
    d.text((MX, iy), "THE REST OF THE DAY",
           font=font(SANS_B, 11), fill=INK)
    d.line([MX, iy + 15, W - MX, iy + 15], fill=INK, width=1)
    cols = [BRIEFS[0:8], BRIEFS[8:16], BRIEFS[16:24], BRIEFS[24:31]]
    col_w = CW // 4
    f_br = font(SANS, 8)
    by = iy + 20
    for ci, col in enumerate(cols):
        bx = MX + ci * col_w
        yy = by
        for text in col:
            assert d.textlength("•  " + text, font=f_br) <= col_w - 6, \
                "brief too wide: %s" % text
            d.text((bx, yy), "•  " + text, font=f_br, fill=INK)
            yy += 11

    # ---- footer (y 1006-1018) ----
    d.line([MX, 1002, W - MX, 1002], fill=RULE, width=1)
    foot = ("42 stories, all verified as happening or first reported on "
            "Wednesday 18 November 2026. Sources: Reuters · BBC · The "
            "Guardian · TechCabal · Motley Fool · OpenAI · EU Council · "
            "Board of Peace · and wire reports.")
    d.text((MX, 1007), foot, font=font(SANS, 8), fill=MUTED)

    img.save(HERE / "entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
