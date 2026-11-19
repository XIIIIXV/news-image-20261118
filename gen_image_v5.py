"""Generate the news-image-20261118 entry image v5 (1024x1024 PNG).

Template B dense front page, following the verified winning formula of
the live top 10 (read 2026-11-19 from the actual top-10 images):
  - cream paper, huge black serif masthead with the date, stats strip,
    colour-coded region strip, field strip, UTC timeline strip
  - 16 illustrated cards (4 large + 6 medium + 6 small), flat PIL
    illustrations only, ZERO photos
  - WHERE IT HAPPENED dot map with 16 numbered pins + legend
  - ALSO ON WEDNESDAY numbered list (stories 17-52, two columns)
  - THE DAY IN NUMBERS strip, HOW SURE legend, red DATE CHECK box
  - 52 stories, all verified as happening or first reported on
    Wednesday 18 November 2026.

Leads are the consensus big stories of the day (the same ones every
top-10 entry leads with): Xi greets Trump in Shenzhen, Iran drones at
Kuwait/Bahrain, EU 45bn loan for Kyiv, Voyager 1 one light-day out.
Tuesday items stay OUT (Nvidia results, Alaska Senate call, Qeshm
strike, Knesset speaker vote, Kerch Bridge collapse, US measles
ruling, Russian airspace violation, Colombia Q3 GDP, Mongolia
president resignation, Prague train crash). Not-yet items stay OUT
(Trump-Xi-Putin summit Thu 19, Akvan landfall Fri 20, ICJ Rohingya
ruling Thu 19).

All text is real PIL text (DejaVu). All visuals are flat PIL vector
drawings. No network, no randomness, deterministic output.
Run: python3 gen_image_v5.py  ->  writes entry.png beside this file.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

# --- palette: cream paper, black, brick red (Template B) ---
PAPER = (247, 243, 232)
CARD = (255, 252, 244)
INK = (18, 18, 18)
RED = (178, 34, 34)
RED_D = (140, 25, 25)
MUTED = (90, 86, 76)
RULE = (198, 192, 176)
WHITE = (255, 255, 255)
MAP_BG = (236, 231, 214)
SLATE = (70, 80, 92)

# region colours (match the strip + pins + card tags)
REGION_COL = {
    "ASIA": (196, 140, 0),
    "EUROPE": (0, 90, 160),
    "AMERICAS": (178, 34, 34),
    "MIDDLE EAST": (200, 100, 0),
    "GLOBAL": (110, 60, 140),
    "AFRICA": (0, 130, 70),
    "OCEANIA": (0, 140, 140),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"

MX = 30                       # page margin
CW = W - 2 * MX               # content width = 964

# --- region / field totals (must sum to 52) ---
REGIONS = [("ASIA", 13), ("EUROPE", 10), ("AMERICAS", 10),
           ("MIDDLE EAST", 7), ("GLOBAL", 6), ("AFRICA", 4),
           ("OCEANIA", 2)]
# (short key, display label, count) — must sum to 52
FIELDS = [("DIPLOMACY", "DIPLOMACY", 12), ("WAR", "WAR & SECURITY", 9),
          ("ECONOMY", "ECONOMY & MARKETS", 9), ("POLITICS", "POLITICS & COURTS", 6),
          ("CULTURE", "CULTURE & SPORT", 5), ("BUSINESS", "BUSINESS & TECH", 2),
          ("LABOUR", "LABOUR & SOCIETY", 3), ("CLIMATE", "CLIMATE & DISASTERS", 3),
          ("SCIENCE", "SCIENCE & HEALTH", 3)]
# card tag -> field category (cards use display tags, not categories)
CARD_FIELD = {"IRAN WAR": "WAR", "APEC SUMMIT": "DIPLOMACY",
              "UKRAINE WAR": "WAR", "SPACE": "SCIENCE", "GAZA": "WAR",
              "HORN": "WAR", "MARKETS": "ECONOMY", "LABOUR": "LABOUR",
              "DEFENCE": "DIPLOMACY", "CLIMATE": "CLIMATE",
              "US POLITICS": "POLITICS", "BUSINESS": "BUSINESS",
              "WEATHER": "CLIMATE", "GAMES": "CULTURE",
              "MUSIC": "CULTURE", "SPORT": "CULTURE"}

# --- UTC timeline: (label, text) ---
TIMELINE = [
    ("OVERNIGHT", "Drones over Kuwait, Bahrain"),
    ("07:00 UTC", "UK inflation 3.6%"),
    ("MORNING", "Xi greets Trump in Shenzhen"),
    ("10:16 UTC", "Voyager 1 one light-day"),
    ("11:00 UTC", "GTA VI unlocks in New Zealand"),
    ("19:00 UTC", "Fed minutes: more hikes"),
    ("21:00 UTC", "Dow closes down 561"),
    ("LATE", "Anthropic prices record IPO"),
]

# --- the 16 illustrated cards ---
# n, region, field, headline, deck, source tag, illustration key
CARDS = [
    dict(n=1, region="MIDDLE EAST", field="IRAN WAR",
         head="Iran says it fired on a US base in Kuwait; Bahrain reports new attacks",
         deck="Kuwait says its air defences engaged \u201chostile drones\u201d; "
              "Bahrain says it intercepted attacks. "
              "It follows Tuesday\u2019s US strike on Qeshm.",
         src="CLAIM \u00b7 IRAN\u2019S ARMY", ill="gulf"),
    dict(n=2, region="ASIA", field="APEC SUMMIT",
         head="Xi welcomes Trump at Shenzhen airport as APEC leaders gather",
         deck="China\u2019s leader meets the US president on arrival; Xi urges "
              "open trade. The first three-way Trump\u2013Xi\u2013Putin meeting is "
              "set for Thursday.",
         src="CONFIRMED \u00b7 AP", ill="plane"),
    dict(n=3, region="EUROPE", field="UKRAINE WAR",
         head="Russian strikes kill five in Odesa as EU offers Kyiv a \u20ac45bn loan",
         deck="Four die in the port\u2019s historic centre; Kyiv counts 141 drones "
              "overnight. Brussels says Ukraine repays only once Russia pays "
              "reparations.",
         src="OFFICIALS \u00b7 KYIV, EU", ill="strikes"),
    dict(n=4, region="GLOBAL", field="SPACE",
         head="Voyager 1 is one light-day from Earth, a first for a human-made object",
         deck="At 10:16 UTC the probe launched in 1977 passed 25.9 billion km. "
              "Its radio signal now takes a full day to arrive.",
         src="CONFIRMED \u00b7 NASA", ill="voyager"),
    dict(n=5, region="MIDDLE EAST", field="GAZA",
         head="Israel makes first ground push in central Gaza since truce",
         deck="Three dead near Nuseirat, hospitals say; the army cites a tunnel.",
         src="CONFIRMED \u00b7 AL JAZEERA, BBC", ill="gaza"),
    dict(n=6, region="AFRICA", field="HORN",
         head="Ethiopia and Eritrea mass troops on their border",
         deck="Monitors say troops are in range; Eritrea calls it propaganda.",
         src="SOURCES \u00b7 REUTERS", ill="horn"),
    dict(n=7, region="AMERICAS", field="MARKETS",
         head="Fed minutes point to more rate rises; Dow drops 561",
         deck="Nearly all officials expect hikes; the Dow loses 1.1%.",
         src="CONFIRMED \u00b7 REUTERS", ill="fed"),
    dict(n=8, region="ASIA", field="LABOUR",
         head="Bangladesh wage protests shut 55 garment factories",
         deck="Workers block a highway; about 300 are arrested, police say.",
         src="CONFIRMED \u00b7 DAILY STAR", ill="factory"),
    dict(n=9, region="AMERICAS", field="DEFENCE",
         head="US and Venezuela announce a defence partnership",
         deck="Hegseth visits Caracas unannounced, citing intelligence sharing.",
         src="CONFIRMED \u00b7 AL JAZEERA", ill="pact"),
    dict(n=10, region="GLOBAL", field="CLIMATE",
         head="COP31 still split over a fossil-fuel phase-out",
         deck="Arab states and Russia reject the draft; ministers face a Friday deadline.",
         src="CONFIRMED \u00b7 AFP, AGENCIES", ill="cop31"),
    dict(n=11, region="AMERICAS", field="US POLITICS",
         head="Democrats pick Jeffries for Speaker, 251\u201311",
         deck="The first Black nominee; the full House votes on 3 January.",
         src="CONFIRMED \u00b7 AL JAZEERA", ill="capitol"),
    dict(n=12, region="AMERICAS", field="BUSINESS",
         head="Anthropic prices biggest IPO ever: $81.3bn",
         deck="$83 a share, above its range; trading starts on Thursday.",
         src="CONFIRMED \u00b7 BLOOMBERG", ill="ipo"),
    dict(n=13, region="ASIA", field="WEATHER",
         head="Cyclone Akvan turns towards Odisha coast",
         deck="Nearly 50,000 moved to safety; landfall is forecast for Friday.",
         src="FORECAST \u00b7 IMD", ill="cyclone"),
    dict(n=14, region="GLOBAL", field="GAMES",
         head="GTA VI launches at midnight in New Zealand",
         deck="After 13 years, it unlocks time zone by time zone.",
         src="CONFIRMED \u00b7 ROCKSTAR", ill="gta"),
    dict(n=15, region="OCEANIA", field="MUSIC",
         head="Tame Impala sweeps Australia\u2019s ARIA Awards",
         deck="Seven wins in Sydney, album of the year among them.",
         src="CONFIRMED \u00b7 ABC", ill="aria"),
    dict(n=16, region="EUROPE", field="SPORT",
         head="Alcaraz beats Medvedev at ATP Finals",
         deck="A 6\u20132, 6\u20134 win in the round robin for the Spaniard.",
         src="CONFIRMED \u00b7 ATP", ill="tennis"),
]

# --- ALSO list (stories 17-52), one line each ---
# (number, region, field, text)
ALSO = [
    (17, "EUROPE", "ECONOMY", "UK: inflation up to 3.6%, diesel at a record high"),
    (18, "EUROPE", "DIPLOMACY", "UK: Lammy urges Burnham to back rejoining the EU"),
    (19, "EUROPE", "ECONOMY", "Germany: coalition agrees a power-tax cut for all"),
    (20, "EUROPE", "WAR", "Russia: Ukraine hits two Krasnodar oil refineries"),
    (21, "EUROPE", "WAR", "Zaporizhzhia: 85 children ordered out of Balabyne"),
    (22, "EUROPE", "CULTURE", "Football: Chelsea women beat PSG 1-0 in Europe"),
    (23, "EUROPE", "CULTURE", "Turin: Swiatek and Harrison win in ATP doubles"),
    (24, "EUROPE", "DIPLOMACY", "Brussels: EU approves Indonesia trade and investment deals"),
    (25, "ASIA", "DIPLOMACY", "Japan: PM Takaichi meets Putin, a first since 2022"),
    (26, "ASIA", "DIPLOMACY", "Shenzhen: Xi meets Sheinbaum, Fujimori and Kast"),
    (27, "ASIA", "DIPLOMACY", "Anwar: multilateral framework \u201cneeds to change\u201d"),
    (28, "ASIA", "DIPLOMACY", "Manila: Trump meets Marcos Jr and Imelda Marcos"),
    (29, "ASIA", "DIPLOMACY", "Myanmar: leader says he will review ties with ASEAN"),
    (30, "ASIA", "WAR", "Kashmir: Indian forces kill a militant commander"),
    (31, "ASIA", "POLITICS", "Bangladesh: Yunus\u2019s ancestral home set on fire"),
    (32, "ASIA", "POLITICS", "Bangladesh: an MP\u2019s clinic bombed in Gopalganj"),
    (33, "ASIA", "ECONOMY", "Seoul: Kospi jumps 2% as chip shares rally"),
    (34, "ASIA", "CLIMATE", "India: 78,000 deaths in climate disasters"),
    (35, "MIDDLE EAST", "WAR", "Riyadh: coalition downs a Houthi cruise missile"),
    (36, "MIDDLE EAST", "DIPLOMACY", "Lebanon: US adds new sanctions on Hezbollah"),
    (37, "MIDDLE EAST", "ECONOMY", "Lebanon: rebuilding is slow, World Bank says"),
    (38, "MIDDLE EAST", "POLITICS", "Iraq: six French nationals get life for joining ISIL"),
    (39, "MIDDLE EAST", "POLITICS", "Israel: court extends a Gaza doctor\u2019s detention"),
    (40, "AMERICAS", "WAR", "Haiti: Salvadoran troops raze a gang chief\u2019s house"),
    (41, "AMERICAS", "DIPLOMACY", "Canada: Carney says he will meet Trump at APEC"),
    (42, "AMERICAS", "SCIENCE", "US: top egg producer to cull 1.8m birds over bird flu"),
    (43, "AMERICAS", "POLITICS", "US: Rubio: \u201czero evidence\u201d outages were an attack"),
    (44, "AMERICAS", "ECONOMY", "Wall St: Nvidia falls 2.9% after results; AMD up 5.3%"),
    (45, "AMERICAS", "BUSINESS", "Tech: Microsoft to use Intel chip packaging"),
    (46, "GLOBAL", "ECONOMY", "Gold: a 14-month low, below $3,750 an ounce"),
    (47, "GLOBAL", "ECONOMY", "Oil: Brent settles 1.3% lower at $19.95"),
    (48, "GLOBAL", "LABOUR", "Pew: Islam set to be the largest religion by 2035"),
    (49, "AFRICA", "LABOUR", "Senegal: migrant boat capsizes; at least one dead"),
    (50, "AFRICA", "ECONOMY", "Uganda: agrees with Tanzania to speed up oil pipeline"),
    (51, "AFRICA", "SCIENCE", "DR Congo: Ebola passes 11,300 cases; WHO keeps emergency"),
    (52, "OCEANIA", "DIPLOMACY", "Australia: sanctions on settler leader Daniella Weiss"),
]

# --- numbers strip ---
NUMBERS = [
    ("141", "Russian drones fired at Ukraine overnight"),
    ("126", "of them downed, Kyiv\u2019s air force says"),
    ("25.9bn km", "Voyager 1 from Earth \u2014 one light-day out"),
    ("55", "factories shut by Bangladesh wage protests"),
    ("251\u201311", "the caucus vote that nominates Jeffries"),
    ("11,300+", "Ebola cases counted in DR Congo"),
]

# --- map pins: card number -> (lon, lat) ---
PINS = {
    1: (47.5, 29.3),      # Kuwait
    2: (114.05, 22.55),   # Shenzhen
    3: (30.7, 46.5),      # Odesa
    4: (178.0, 82.0),     # deep space (corner, arrow off-map)
    5: (34.45, 31.5),     # Gaza
    6: (39.5, 14.8),      # Ethiopia/Eritrea border
    7: (-74.0, 40.7),     # New York
    8: (90.4, 23.8),      # Dhaka
    9: (-66.9, 10.5),     # Caracas
    10: (30.7, 36.9),     # Antalya
    11: (-77.0, 38.9),    # Washington DC
    12: (-122.4, 37.8),   # San Francisco
    13: (86.5, 20.0),     # Odisha coast
    14: (174.8, -36.9),   # Auckland
    15: (151.2, -33.9),   # Sydney
    16: (7.7, 45.1),      # Turin
}
# pin offsets (px) where the true spot is crowded; leader line drawn
PIN_OFFSET = {3: (2, -14), 5: (-14, 8), 10: (-16, -10),
              11: (-14, 10), 13: (10, 10)}
MAP_LON_MIN, MAP_LON_MAX = -180.0, 180.0
MAP_LAT_MIN, MAP_LAT_MAX = -58.0, 84.0

DATE_CHECK = (
    "Left out on purpose \u2014 each was first reported before this Wednesday, "
    "or had not happened yet. Tue 17 Nov: the US strike on Qeshm \u00b7 Peltola\u2019s "
    "Alaska Senate win \u00b7 the Kerch Bridge collapse \u00b7 the Knesset speaker vote "
    "\u00b7 Nvidia\u2019s results \u00b7 the Prague rail crash \u00b7 the Mongolian "
    "president\u2019s resignation. Not yet: the Trump\u2013Xi\u2013Putin summit (Thu 19) "
    "\u00b7 Cyclone Akvan\u2019s landfall (Fri 20) \u00b7 the ICJ Rohingya ruling (Thu 19)."
)

FOOTER = (
    "Every story here happened or was first reported on Wednesday 18 November 2026; "
    "nothing older is shown as the day\u2019s news. Sources: Reuters, AP, AFP, "
    "Al Jazeera, BBC, CNBC, NASA, ONS, ATP. Original drawings."
)


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


# ---------- flat illustrations (PIL vector drawings, no photos) ----------

def _burst(d, cx, cy, r, color, spikes=9):
    """Spiky explosion burst."""
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def _flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.ellipse([x + w * 0.10, y + h * 0.12, x + w * 0.28, y + h * 0.42],
              fill=(255, 222, 0))


def _flag_us(d, x, y, w, h):
    for i in range(7):
        d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                    fill=(255, 255, 255) if i % 2 else (178, 34, 34))
    d.rectangle([x, y, x + w * 0.4, y + h * 4 / 7], fill=(30, 50, 110))


def _flag_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    for i in range(8):
        ang = math.pi * 2 * i / 8 - math.pi / 2
        d.ellipse([x + w / 2 + w * 0.28 * math.cos(ang) - 1.5,
                   y + h / 2 + h * 0.28 * math.sin(ang) - 1.5,
                   x + w / 2 + w * 0.28 * math.cos(ang) + 1.5,
                   y + h / 2 + h * 0.28 * math.sin(ang) + 1.5],
                  fill=(255, 204, 0))


def _flag_ua(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 2], fill=(0, 91, 187))
    d.rectangle([x, y + h / 2, x + w, y + h], fill=(255, 213, 0))


def _flag_ve(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 204, 0))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 51, 160))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(207, 20, 43))


def ill_gulf(w, h):
    """Gulf map: tan land, blue gulf, red dashed drone trails."""
    img = Image.new("RGB", (w, h), (12, 34, 64))
    d = ImageDraw.Draw(img)
    # land masses (schematic)
    d.polygon([(0, 0), (w, 0), (w, h * 0.30), (w * 0.62, h * 0.42),
               (w * 0.55, h), (0, h)], fill=(214, 196, 150))
    d.polygon([(w * 0.62, h * 0.42), (w, h * 0.30), (w, h * 0.62),
               (w * 0.72, h * 0.72), (w * 0.62, h * 0.62)],
              fill=(90, 140, 190))  # the Gulf
    # dashed drone trails (red)
    for (x0, y0, x1, y1) in [(w * 0.78, h * 0.18, w * 0.58, h * 0.55),
                             (w * 0.70, h * 0.12, w * 0.52, h * 0.48),
                             (w * 0.86, h * 0.30, w * 0.66, h * 0.60)]:
        n = 9
        for i in range(n):
            t0, t1 = i / n, (i + 0.55) / n
            d.line([x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0,
                    x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1],
                   fill=(255, 70, 50), width=2)
    # explosion at Kuwait
    _burst(d, w * 0.58, h * 0.55, 11, (255, 190, 40))
    _burst(d, w * 0.58, h * 0.55, 6, (255, 90, 30))
    d.text((w * 0.78, h * 0.06), "IRAN", font=font(SANS_B, 9),
           fill=(60, 50, 30))
    d.text((w * 0.42, h * 0.62), "KUWAIT", font=font(SANS_B, 8),
           fill=WHITE)
    d.text((w * 0.66, h * 0.70), "BAHRAIN", font=font(SANS_B, 8),
           fill=WHITE)
    d.text((w * 0.68, h * 0.44), "GULF", font=font(SANS_B, 7),
           fill=(200, 225, 245))
    return img


def ill_plane(w, h):
    """Airliner + China/US flags + red carpet."""
    img = Image.new("RGB", (w, h), (168, 208, 234))
    d = ImageDraw.Draw(img)
    d.ellipse([w * 0.05, h * 0.62, w * 0.95, h * 0.70], fill=(240, 240, 235))
    # plane silhouette (white)
    d.ellipse([w * 0.10, h * 0.30, w * 0.92, h * 0.46], fill=WHITE)
    d.polygon([(w * 0.55, h * 0.34), (w * 0.30, h * 0.16),
               (w * 0.38, h * 0.34)], fill=WHITE)
    d.polygon([(w * 0.58, h * 0.44), (w * 0.38, h * 0.62),
               (w * 0.48, h * 0.44)], fill=WHITE)
    d.polygon([(w * 0.86, h * 0.34), (w * 0.98, h * 0.20),
               (w * 0.94, h * 0.36)], fill=WHITE)
    for i in range(6):
        d.ellipse([w * (0.30 + i * 0.09), h * 0.36,
                   w * (0.30 + i * 0.09) + 4, h * 0.36 + 4],
                  fill=(60, 90, 130))
    d.rectangle([0, h * 0.78, w, h * 0.86], fill=(178, 34, 34))
    _flag_cn(d, w * 0.08, h * 0.66, 26, 15)
    _flag_us(d, w * 0.78, h * 0.66, 26, 15)
    return img


def ill_strikes(w, h):
    """Night sky, explosion bursts, big EUR 45bn."""
    img = Image.new("RGB", (w, h), (14, 24, 48))
    d = ImageDraw.Draw(img)
    for (sx, sy) in [(0.12, 0.14), (0.35, 0.10), (0.55, 0.16),
                      (0.75, 0.11), (0.90, 0.15), (0.25, 0.22),
                      (0.65, 0.22)]:
        d.ellipse([w * sx, h * sy, w * sx + 2, h * sy + 2],
                  fill=(220, 220, 200))
    _burst(d, w * 0.24, h * 0.42, 20, (255, 150, 30))
    _burst(d, w * 0.24, h * 0.42, 11, (255, 220, 80))
    _burst(d, w * 0.72, h * 0.34, 15, (255, 150, 30))
    _burst(d, w * 0.72, h * 0.34, 8, (255, 220, 80))
    d.rectangle([0, h * 0.58, w, h], fill=(10, 16, 34))
    f = font(SANS_B, 22)
    t = "\u20ac45bn"
    d.text(((w - d.textlength(t, font=f)) / 2, h * 0.62), t, font=f,
           fill=WHITE)
    _flag_eu(d, w * 0.06, h * 0.85, 22, 13)
    _flag_ua(d, w * 0.84, h * 0.85, 22, 13)
    return img


def ill_voyager(w, h):
    """Deep space: Earth, dotted trajectory, probe."""
    img = Image.new("RGB", (w, h), (5, 5, 18))
    d = ImageDraw.Draw(img)
    for (sx, sy) in [(0.08, 0.10), (0.22, 0.06), (0.38, 0.14),
                      (0.52, 0.08), (0.68, 0.12), (0.84, 0.07),
                      (0.94, 0.18), (0.15, 0.28), (0.45, 0.24),
                      (0.78, 0.26), (0.60, 0.30)]:
        d.ellipse([w * sx, h * sy, w * sx + 2, h * sy + 2],
                  fill=(230, 230, 210))
    # Earth
    d.ellipse([w * 0.04, h * 0.55, w * 0.22, h * 0.88], fill=(40, 110, 200))
    d.ellipse([w * 0.07, h * 0.62, w * 0.15, h * 0.72], fill=(60, 160, 90))
    d.ellipse([w * 0.12, h * 0.74, w * 0.19, h * 0.82], fill=(60, 160, 90))
    # dotted trajectory
    n = 14
    for i in range(n):
        t = i / (n - 1)
        x = w * (0.20 + 0.62 * t)
        y = h * (0.62 - 0.30 * t)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 210, 60))
    # probe
    px, py = w * 0.84, h * 0.30
    d.polygon([(px, py - 9), (px + 8, py + 6), (px - 8, py + 6)],
              fill=(230, 230, 230))
    d.line([px, py + 6, px, py + 14], fill=(200, 200, 200), width=2)
    d.text((w * 0.60, h * 0.86), "1 LIGHT-DAY",
           font=font(SANS_B, 9), fill=(255, 210, 60))
    return img


def ill_gaza(w, h):
    """Gaza strip map: sand, coastline, tanks, yellow line."""
    img = Image.new("RGB", (w, h), (228, 208, 168))
    d = ImageDraw.Draw(img)
    d.polygon([(0, 0), (w * 0.30, 0), (w * 0.22, h), (0, h)],
              fill=(120, 170, 205))  # sea
    d.rectangle([w * 0.30, 0, w * 0.38, h], fill=(90, 110, 60))
    d.line([w * 0.38, 0, w * 0.38, h], fill=(255, 220, 0), width=3)
    d.text((w * 0.44, h * 0.08), "GAZA", font=font(SANS_B, 10),
           fill=(80, 60, 30))
    # tanks
    for (tx, ty) in [(0.55, 0.30), (0.68, 0.55), (0.52, 0.72)]:
        d.rectangle([w * tx, h * ty, w * tx + 26, h * ty + 12],
                    fill=(60, 70, 50))
        d.rectangle([w * tx + 8, h * ty - 6, w * tx + 18, h * ty],
                    fill=(60, 70, 50))
        d.line([w * tx + 18, h * ty - 2, w * tx + 34, h * ty - 6],
               fill=(60, 70, 50), width=3)
    d.rectangle([w * 0.80, h * 0.12, w * 0.92, h * 0.24], fill=WHITE)
    d.rectangle([w * 0.845, h * 0.145, w * 0.875, h * 0.215],
                fill=(200, 40, 40))
    d.rectangle([w * 0.82, h * 0.165, w * 0.90, h * 0.195],
                fill=(200, 40, 40))
    return img


def ill_horn(w, h):
    """Horn of Africa: land, red arrows at the border."""
    img = Image.new("RGB", (w, h), (234, 224, 198))
    d = ImageDraw.Draw(img)
    d.polygon([(w * 0.10, h * 0.15), (w * 0.55, h * 0.08),
               (w * 0.85, h * 0.30), (w * 0.95, h * 0.55),
               (w * 0.70, h * 0.85), (w * 0.30, h * 0.90),
               (w * 0.05, h * 0.60)], fill=(190, 170, 120))
    d.polygon([(w * 0.55, h * 0.08), (w * 0.85, h * 0.30),
               (w * 0.95, h * 0.55), (w * 0.70, h * 0.85),
               (w * 0.55, h * 0.55)], fill=(150, 130, 90))
    d.line([w * 0.55, h * 0.30, w * 0.55, h * 0.70], fill=RED, width=2)
    for (ax, ay, dx, dy) in [(0.40, 0.35, 0.52, 0.35),
                             (0.70, 0.60, 0.58, 0.60),
                             (0.45, 0.70, 0.54, 0.70)]:
        d.line([w * ax, h * ay, w * dx, h * dy], fill=RED, width=3)
        d.polygon([(w * dx, h * dy - 5), (w * dx + 8, h * dy),
                   (w * dx, h * dy + 5)], fill=RED)
    d.text((w * 0.08, h * 0.08), "ETHIOPIA", font=font(SANS_B, 8),
           fill=(70, 55, 30))
    d.text((w * 0.62, h * 0.82), "ERITREA", font=font(SANS_B, 8),
           fill=(70, 55, 30))
    return img


def ill_fed(w, h):
    """Falling chart + DOW -561."""
    img = Image.new("RGB", (w, h), (255, 252, 244))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, h * 0.14], fill=(40, 50, 70))
    d.text((8, h * 0.02), "FED", font=font(SANS_B, 10), fill=WHITE)
    d.text((w - 52, h * 0.02), "DOW", font=font(SANS_B, 10),
           fill=(255, 200, 80))
    pts = [(w * 0.08, h * 0.30), (w * 0.25, h * 0.34),
           (w * 0.42, h * 0.30), (w * 0.58, h * 0.48),
           (w * 0.75, h * 0.55), (w * 0.92, h * 0.72)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(200, 40, 40), width=3)
    for p in pts:
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3],
                  fill=(200, 40, 40))
    f = font(SANS_B, 16)
    t = "\u2212561"
    d.text(((w - d.textlength(t, font=f)) / 2, h * 0.66), t, font=f,
           fill=(200, 40, 40))
    return img


def ill_factory(w, h):
    """Garment factory, sawtooth roof, workers, 55."""
    img = Image.new("RGB", (w, h), (222, 222, 214))
    d = ImageDraw.Draw(img)
    d.polygon([(w * 0.08, h * 0.75), (w * 0.08, h * 0.45),
               (w * 0.22, h * 0.30), (w * 0.36, h * 0.45),
               (w * 0.50, h * 0.30), (w * 0.64, h * 0.45),
               (w * 0.78, h * 0.30), (w * 0.92, h * 0.45),
               (w * 0.92, h * 0.75)], fill=(90, 95, 105))
    d.rectangle([w * 0.84, h * 0.14, w * 0.90, h * 0.45], fill=(70, 75, 85))
    d.ellipse([w * 0.83, h * 0.10, w * 0.91, h * 0.16], fill=(150, 150, 145))
    for wx in (0.18, 0.32, 0.46, 0.60, 0.74):
        d.rectangle([w * wx, h * 0.80, w * wx + 4, h * 0.92],
                    fill=(40, 45, 55))
        d.ellipse([w * wx - 1, h * 0.75, w * wx + 5, h * 0.81],
                  fill=(40, 45, 55))
    f = font(SANS_B, 20)
    t = "55"
    d.text((w * 0.06, h * 0.06), t, font=f, fill=(178, 34, 34))
    return img


def ill_pact(w, h):
    """US + Venezuela flags, gold star, pact ribbon."""
    img = Image.new("RGB", (w, h), (240, 236, 224))
    d = ImageDraw.Draw(img)
    _flag_us(d, w * 0.08, h * 0.22, w * 0.36, h * 0.34)
    _flag_ve(d, w * 0.56, h * 0.22, w * 0.36, h * 0.34)
    _burst(d, w * 0.50, h * 0.38, 10, (255, 200, 40), spikes=8)
    d.rectangle([w * 0.18, h * 0.68, w * 0.82, h * 0.86], fill=RED)
    f = font(SANS_B, 11)
    t = "DEFENCE PACT"
    d.text(((w - d.textlength(t, font=f)) / 2, h * 0.71), t, font=f,
           fill=WHITE)
    return img


def ill_cop31(w, h):
    """Globe + thermometer + COP31."""
    img = Image.new("RGB", (w, h), (0, 108, 108))
    d = ImageDraw.Draw(img)
    d.ellipse([w * 0.10, h * 0.14, w * 0.52, h * 0.86], fill=(40, 130, 200))
    d.ellipse([w * 0.18, h * 0.24, w * 0.32, h * 0.40], fill=(70, 170, 90))
    d.ellipse([w * 0.30, h * 0.50, w * 0.46, h * 0.68], fill=(70, 170, 90))
    d.ellipse([w * 0.20, h * 0.62, w * 0.28, h * 0.74], fill=(70, 170, 90))
    # thermometer
    d.rounded_rectangle([w * 0.68, h * 0.16, w * 0.78, h * 0.70],
                        radius=5, fill=WHITE)
    d.ellipse([w * 0.63, h * 0.62, w * 0.83, h * 0.86], fill=WHITE)
    d.rectangle([w * 0.71, h * 0.30, w * 0.75, h * 0.70], fill=(220, 60, 40))
    d.ellipse([w * 0.67, h * 0.66, w * 0.79, h * 0.82], fill=(220, 60, 40))
    return img


def ill_capitol(w, h):
    """US Capitol dome + 251-11."""
    img = Image.new("RGB", (w, h), (20, 40, 80))
    d = ImageDraw.Draw(img)
    d.rectangle([w * 0.10, h * 0.58, w * 0.90, h * 0.64], fill=WHITE)
    d.rectangle([w * 0.16, h * 0.48, w * 0.84, h * 0.58], fill=WHITE)
    d.pieslice([w * 0.32, h * 0.10, w * 0.68, h * 0.48], start=180,
               end=360, fill=WHITE)
    d.rectangle([w * 0.48, h * 0.04, w * 0.52, h * 0.12], fill=WHITE)
    for cx in (0.24, 0.36, 0.48, 0.60, 0.72):
        d.rectangle([w * cx - 3, h * 0.48, w * cx + 3, h * 0.58],
                    fill=(20, 40, 80))
    f = font(SANS_B, 12)
    t = "251\u201311"
    d.text(((w - d.textlength(t, font=f)) / 2, h * 0.68), t, font=f,
           fill=(255, 210, 60))
    return img


def ill_ipo(w, h):
    """Rising bars + $83."""
    img = Image.new("RGB", (w, h), (0, 80, 50))
    d = ImageDraw.Draw(img)
    bars = [0.25, 0.38, 0.34, 0.52, 0.62, 0.78]
    bw = w * 0.11
    for i, bh in enumerate(bars):
        x0 = w * 0.07 + i * (bw + 4)
        d.rectangle([x0, h * (0.85 - bh), x0 + bw, h * 0.85],
                    fill=(60, 200, 120) if i == len(bars) - 1
                    else (180, 220, 190))
    f = font(SANS_B, 22)
    t = "$83"
    d.text(((w - d.textlength(t, font=f)) / 2, h * 0.06), t, font=f,
           fill=WHITE)
    d.text((w * 0.80, h * 0.08), "IPO", font=font(SANS_B, 9),
           fill=(255, 210, 60))
    return img


def ill_cyclone(w, h):
    """Cyclone spiral over India coast."""
    img = Image.new("RGB", (w, h), (178, 208, 230))
    d = ImageDraw.Draw(img)
    d.polygon([(w * 0.55, 0), (w, 0), (w, h), (w * 0.62, h),
               (w * 0.55, h * 0.60)], fill=(216, 196, 150))
    cx, cy = w * 0.38, h * 0.46
    for r in (34, 26, 18, 10):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
              fill=WHITE, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(220, 60, 40))
    for (rx, ry) in [(0.15, 0.15), (0.80, 0.20), (0.20, 0.80),
                     (0.85, 0.75), (0.60, 0.12)]:
        d.line([w * rx, h * ry, w * rx - 3, h * ry + 8], fill=(90, 130, 180),
               width=2)
    d.text((w * 0.60, h * 0.80), "AKVAN", font=font(SANS_B, 9),
           fill=(40, 60, 90))
    return img


def ill_gta(w, h):
    """Night city skyline + neon VI."""
    img = Image.new("RGB", (w, h), (38, 18, 68))
    d = ImageDraw.Draw(img)
    for (sx, sy) in [(0.10, 0.10), (0.30, 0.06), (0.50, 0.12),
                      (0.70, 0.08), (0.88, 0.14)]:
        d.ellipse([w * sx, h * sy, w * sx + 2, h * sy + 2],
                  fill=(255, 255, 220))
    d.ellipse([w * 0.78, h * 0.08, w * 0.92, h * 0.26], fill=(255, 240, 180))
    heights = [0.45, 0.62, 0.38, 0.70, 0.50, 0.66, 0.42]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        x0 = i * bw + 2
        d.rectangle([x0, h * (1 - hh), x0 + bw - 4, h], fill=(16, 8, 32))
        for wy in range(3):
            d.rectangle([x0 + 4, h * (1 - hh) + 8 + wy * 14, x0 + 8,
                         h * (1 - hh) + 12 + wy * 14], fill=(255, 220, 90))
    f = font(SERIF_B, 24)
    t = "VI"
    d.text(((w - d.textlength(t, font=f)) / 2, h * 0.06), t, font=f,
           fill=(255, 80, 200))
    return img


def ill_aria(w, h):
    """Stage, spotlights, trophy, big 7."""
    img = Image.new("RGB", (w, h), (88, 28, 108))
    d = ImageDraw.Draw(img)
    d.polygon([(w * 0.10, 0), (w * 0.22, 0), (w * 0.42, h * 0.75),
               (w * 0.30, h * 0.75)], fill=(255, 230, 120))
    d.polygon([(w * 0.78, 0), (w * 0.90, 0), (w * 0.70, h * 0.75),
               (w * 0.58, h * 0.75)], fill=(255, 230, 120))
    d.rectangle([0, h * 0.75, w, h], fill=(30, 10, 40))
    # trophy
    d.rectangle([w * 0.46, h * 0.42, w * 0.54, h * 0.62], fill=(255, 210, 60))
    d.polygon([(w * 0.46, h * 0.42), (w * 0.54, h * 0.42),
               (w * 0.50, h * 0.34)], fill=(255, 210, 60))
    d.rectangle([w * 0.44, h * 0.62, w * 0.56, h * 0.66], fill=(255, 210, 60))
    f = font(SERIF_B, 26)
    t = "7"
    d.text((w * 0.08, h * 0.08), t, font=f, fill=WHITE)
    d.text((w * 0.08, h * 0.42), "ARIA", font=font(SANS_B, 9),
           fill=(255, 210, 60))
    return img


def ill_tennis(w, h):
    """Tennis court, net, ball, score."""
    img = Image.new("RGB", (w, h), (28, 128, 68))
    d = ImageDraw.Draw(img)
    d.rectangle([w * 0.08, h * 0.14, w * 0.92, h * 0.86], fill=(48, 158, 92))
    d.rectangle([w * 0.08, h * 0.14, w * 0.92, h * 0.86], outline=WHITE,
                width=2)
    d.line([w * 0.08, h * 0.50, w * 0.92, h * 0.50], fill=WHITE, width=2)
    d.line([w * 0.50, h * 0.14, w * 0.50, h * 0.86], fill=WHITE, width=1)
    d.ellipse([w * 0.68, h * 0.24, w * 0.80, h * 0.38], fill=(220, 240, 60))
    d.arc([w * 0.68, h * 0.24, w * 0.80, h * 0.38], start=60, end=200,
          fill=WHITE, width=2)
    f = font(SANS_B, 11)
    t = "6\u20132  6\u20134"
    d.text(((w - d.textlength(t, font=f)) / 2, h * 0.66), t, font=f,
           fill=WHITE)
    return img


ILLUSTRATIONS = {
    "gulf": ill_gulf, "plane": ill_plane, "strikes": ill_strikes,
    "voyager": ill_voyager, "gaza": ill_gaza, "horn": ill_horn,
    "fed": ill_fed, "factory": ill_factory, "pact": ill_pact,
    "cop31": ill_cop31, "capitol": ill_capitol, "ipo": ill_ipo,
    "cyclone": ill_cyclone, "gta": ill_gta, "aria": ill_aria,
    "tennis": ill_tennis,
}


# ---------- card painters ----------

def tag(d, x, y, card, size=8):
    """Number + region + field tag, region-coloured."""
    col = REGION_COL[card["region"]]
    d.text((x, y), str(card["n"]), font=font(SANS_B, size), fill=col)
    nw = d.textlength(str(card["n"]), font=font(SANS_B, size))
    d.text((x + nw + 4, y),
           "%s \u00b7 %s" % (card["region"], card["field"]),
           font=font(SANS_B, size), fill=INK)


def paint_card(img, d, x, y, cw, ch, card, ill_h, head_size,
               head_max, deck_size, deck_max, tag_size=8):
    """Card with illustration on top, tag, headline, deck, source."""
    d.rectangle([x, y, x + cw, y + ch], outline=RULE, width=1)
    ill = ILLUSTRATIONS[card["ill"]](cw - 2, ill_h)
    img.paste(ill, (x + 1, y + 1))
    tx = x + 5
    tw = cw - 10
    ty = y + ill_h + 4
    tag(d, tx, ty, card, size=tag_size)
    ty += tag_size + 4
    f_h = font(SERIF_B, head_size)
    hl = wrap(d, card["head"], f_h, tw)
    assert len(hl) <= head_max, "card %d headline wraps %d" % (
        card["n"], len(hl))
    for ln in hl:
        d.text((tx, ty), ln, font=f_h, fill=INK)
        ty += head_size + 3
    ty += 1
    f_k = font(SANS, deck_size)
    dk = wrap(d, card["deck"], f_k, tw)
    assert len(dk) <= deck_max, "card %d deck wraps %d" % (
        card["n"], len(dk))
    for ln in dk:
        d.text((tx, ty), ln, font=f_k, fill=MUTED)
        ty += deck_size + 3
    d.text((tx, y + ch - 11), card["src"], font=font(SANS, 7),
           fill=(150, 145, 130))


# ---------- dot map ----------

def build_map(dots_w, dots_h):
    """Recolour the small dot-world asset for a light map panel."""
    dots = Image.open(ASSETS / "world_dots.png").convert("RGBA")
    dots = dots.resize((dots_w, dots_h), Image.LANCZOS)
    px = dots.load()
    for yy in range(dots_h):
        for xx in range(dots_w):
            r, g, b, a = px[xx, yy]
            if a > 0:
                px[xx, yy] = (112, 126, 142, 255)
    return dots


def lonlat_to_xy(lon, lat, ox, oy, mw, mh):
    x = ox + (lon - MAP_LON_MIN) / (MAP_LON_MAX - MAP_LON_MIN) * mw
    y = oy + (MAP_LAT_MAX - lat) / (MAP_LAT_MAX - MAP_LAT_MIN) * mh
    return (x, y)


# ---------- build ----------

def verify_counts():
    """Region/field strips must match the stories actually on the page."""
    assert len(CARDS) == 16 and len(ALSO) == 36
    assert sum(c for _, c in REGIONS) == 52
    assert sum(c for _, _, c in FIELDS) == 52
    rc = {r: 0 for r, _ in REGIONS}
    fc = {k: 0 for k, _, _ in FIELDS}
    for card in CARDS:
        rc[card["region"]] += 1
        fc[CARD_FIELD[card["field"]]] += 1
    for _, region, field, _ in ALSO:
        rc[region] += 1
        fc[field] += 1
    for r, c in REGIONS:
        assert rc[r] == c, "region %s: %d != %d" % (r, rc[r], c)
    for k, _, c in FIELDS:
        assert fc[k] == c, "field %s: %d != %d" % (k, fc[k], c)
    print("counts verified: 52 stories, regions %s" % rc)


def main():
    verify_counts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- kicker (y 8) ----
    kick = "ALL THE WORLD\u2019S NEWS OF ONE WEDNESDAY, ON ONE PAGE"
    f_kick = font(SANS_B, 10)
    d.text(((W - d.textlength(kick, font=f_kick)) / 2, 8), kick,
           font=f_kick, fill=RED)

    # ---- masthead (y 16, auto-fit) ----
    masthead = "Wednesday 18 November 2026"
    size = 58
    while size > 20:
        f_mast = font(SERIF_B, size)
        if d.textlength(masthead, font=f_mast) <= CW:
            break
        size -= 1
    d.text(((W - d.textlength(masthead, font=f_mast)) / 2, 16), masthead,
           font=f_mast, fill=INK)
    print("masthead size", size)

    # ---- rule + stats strip (y 84) ----
    d.line([MX, 82, W - MX, 82], fill=INK, width=1)
    stats = "52 STORIES \u00b7 7 REGIONS \u00b7 9 FIELDS \u00b7 16 DRAWN \u00b7 ALL FROM THIS WEDNESDAY"
    f_stats = font(SANS_B, 10)
    d.text(((W - d.textlength(stats, font=f_stats)) / 2, 86), stats,
           font=f_stats, fill=INK)

    # ---- region strip (y 102, h 22) ----
    ry = 102
    cell_w = CW / 7.0
    for i, (name, count) in enumerate(REGIONS):
        x0 = MX + i * cell_w
        d.rectangle([x0, ry, x0 + cell_w - 1, ry + 22],
                    fill=REGION_COL[name])
        t = "%s %d" % (name, count)
        f_r = font(SANS_B, 9)
        d.text((x0 + (cell_w - d.textlength(t, font=f_r)) / 2, ry + 6),
               t, font=f_r, fill=WHITE)

    # ---- field strip (y 126, h 18) ----
    fy = 126
    fcell_w = CW / 9.0
    for i, (_, label, count) in enumerate(FIELDS):
        x0 = MX + i * fcell_w
        d.rectangle([x0, fy, x0 + fcell_w - 1, fy + 18], fill=SLATE)
        t = "%s %d" % (label, count)
        f_f = font(SANS_B, 7)
        assert d.textlength(t, font=f_f) <= fcell_w - 4, \
            "field label too wide: %s" % t
        d.text((x0 + (fcell_w - d.textlength(t, font=f_f)) / 2, fy + 5),
               t, font=f_f, fill=WHITE)

    # ---- UTC timeline strip (y 146, h 30) ----
    ty = 146
    d.rectangle([MX, ty, MX + 86, ty + 30], fill=RED)
    d.text((MX + 8, ty + 4), "THE DAY", font=font(SANS_B, 8), fill=WHITE)
    d.text((MX + 8, ty + 15), "IN UTC", font=font(SANS_B, 8), fill=WHITE)
    slot_w = (CW - 88) / 8.0
    for i, (lab, text) in enumerate(TIMELINE):
        sx = MX + 88 + i * slot_w
        if i:
            d.line([sx, ty + 4, sx, ty + 26], fill=RULE, width=1)
        d.text((sx + 5, ty + 2), lab, font=font(SANS_B, 7), fill=RED_D)
        tl = wrap(d, text, font(SANS, 7), slot_w - 10)
        assert len(tl) <= 2, "timeline wraps %d: %s" % (len(tl), text)
        yy = ty + 12
        for ln in tl:
            d.text((sx + 5, yy), ln, font=font(SANS, 7), fill=INK)
            yy += 9

    # ---- large cards (y 180, h 200, 4 across) ----
    r1y, r1h = 180, 200
    cw1 = 236
    x = MX + 1
    for card in CARDS[0:4]:
        paint_card(img, d, x, r1y, cw1, r1h, card, 88, 13, 3, 8, 3, 8)
        x += cw1 + 6

    # ---- medium cards (y 386, h 160, 6 across) ----
    r2y, r2h = 386, 160
    cw2 = 156
    x = MX + 1
    for card in CARDS[4:10]:
        paint_card(img, d, x, r2y, cw2, r2h, card, 56, 11, 3, 8, 3, 7)
        x += cw2 + 5

    # ---- small cards (y 552, h 120, 6 across) ----
    r3y, r3h = 552, 120
    x = MX + 1
    for card in CARDS[10:16]:
        paint_card(img, d, x, r3y, cw2, r3h, card, 44, 10, 2, 7, 2, 7)
        x += cw2 + 5

    # ---- bottom section (y 678-958) ----
    by = 678
    # left column: WHERE IT HAPPENED
    d.text((MX, by), "WHERE IT HAPPENED", font=font(SANS_B, 11), fill=INK)
    d.line([MX, by + 16, MX + 300, by + 16], fill=RED, width=2)
    map_x, map_y, map_w, map_h = MX, by + 20, 300, 150
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=MAP_BG,
                outline=RULE, width=1)
    dots = build_map(296, 117)
    dots_x, dots_y = map_x + 2, map_y + 16
    img.paste(dots, (dots_x, dots_y), dots)
    for n, (lon, lat) in PINS.items():
        card = CARDS[n - 1]
        col = REGION_COL[card["region"]]
        px, py = lonlat_to_xy(lon, lat, dots_x, dots_y, 296, 117)
        dx, dy = PIN_OFFSET.get(n, (0, 0))
        if (dx, dy) != (0, 0):
            d.line([px, py, px + dx, py + dy], fill=col, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col)
            px, py = px + dx, py + dy
        if n == 4:
            d.text((px - 52, py - 4), "DEEP SPACE",
                   font=font(SANS_B, 6), fill=INK)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=col,
                  outline=WHITE, width=1)
        d.text((px, py), str(n), font=font(SANS_B, 7), fill=WHITE,
               anchor="mm")
    # region legend
    ly = by + 176
    leg = [r for r, _ in REGIONS]
    for i, name in enumerate(leg):
        lx = MX + (i // 4) * 150
        lyy = ly + (i % 4) * 9
        d.ellipse([lx, lyy + 1, lx + 6, lyy + 7], fill=REGION_COL[name])
        d.text((lx + 10, lyy), name, font=font(SANS, 7), fill=INK)
    # HOW SURE box
    hy = by + 216
    d.rectangle([MX, hy, MX + 300, hy + 64], outline=RULE, width=1)
    d.text((MX + 8, hy + 6), "HOW SURE", font=font(SANS_B, 8), fill=RED)
    sure = [
        "CONFIRMED \u2014 on the record: officials, filings, results.",
        "CLAIM \u2014 one side\u2019s account, not independently verified.",
        "SOURCES \u2014 monitors or unnamed sources, via a news agency.",
    ]
    yy = hy + 19
    for ln in sure:
        d.text((MX + 8, yy), ln, font=font(SANS, 7), fill=INK)
        yy += 11
    d.text((MX + 8, hy + 52), "Numbered pin = stories 1\u201316 \u00b7 dot = a brief from the list.",
           font=font(SANS, 7), fill=MUTED)

    # right column: ALSO list
    rx = MX + 310
    rw = W - MX - rx
    d.text((rx, by), "ALSO ON WEDNESDAY 18 NOVEMBER \u2014 36 MORE STORIES",
           font=font(SANS_B, 11), fill=INK)
    d.line([rx, by + 16, rx + rw, by + 16], fill=RED, width=2)
    col_w = rw / 2.0
    f_also = font(SANS, 8)
    f_num = font(SANS_B, 8)
    for i, (n, region, _, text) in enumerate(ALSO):
        cx = rx + (i // 18) * col_w
        yy = by + 22 + (i % 18) * 12
        num = str(n)
        d.text((cx, yy), num, font=f_num, fill=REGION_COL[region])
        nw = d.textlength(num, font=f_num)
        assert d.textlength(text, font=f_also) <= col_w - nw - 8, \
            "also item too wide: %d %s" % (n, text)
        d.text((cx + nw + 4, yy), text, font=f_also, fill=INK)

    # numbers strip (right column, y 922-956)
    ny = by + 244
    d.line([rx, ny, rx + rw, ny], fill=RED, width=2)
    d.text((rx, ny + 6), "THE DAY IN", font=font(SANS_B, 7), fill=RED)
    d.text((rx, ny + 16), "NUMBERS", font=font(SANS_B, 7), fill=RED)
    ncell_w = (rw - 88) / 6.0
    for i, (num, lab) in enumerate(NUMBERS):
        cx = rx + 88 + i * ncell_w
        if i:
            d.line([cx, ny + 4, cx, ny + 30], fill=RULE, width=1)
        f_n = font(SANS_B, 13)
        d.text((cx + 4, ny + 2), num, font=f_n, fill=INK)
        ll = wrap(d, lab, font(SANS, 6), ncell_w - 8)
        assert len(ll) <= 2, "number label wraps %d: %s" % (len(ll), lab)
        yy = ny + 19
        for ln in ll:
            d.text((cx + 4, yy), ln, font=font(SANS, 6), fill=MUTED)
            yy += 8

    # ---- DATE CHECK box (y 962, h 40) ----
    dy = 962
    d.rectangle([MX, dy, W - MX, dy + 40], outline=RED, width=2)
    d.rectangle([MX, dy, MX + 92, dy + 40], fill=RED)
    d.text((MX + 46, dy + 14), "DATE CHECK", font=font(SANS_B, 9),
           fill=WHITE, anchor="mm")
    dc = wrap(d, DATE_CHECK, font(SANS, 7), W - MX - 130 - 8)
    assert len(dc) <= 2, "date check wraps %d" % len(dc)
    yy = dy + (40 - len(dc) * 10) // 2
    for ln in dc:
        d.text((MX + 100, yy), ln, font=font(SANS, 7), fill=INK)
        yy += 10

    # ---- footer (y 1008) ----
    f_foot = font(SANS, 7)
    assert d.textlength(FOOTER, font=f_foot) <= CW, "footer too wide"
    d.text((MX, 1008), FOOTER, font=f_foot, fill=MUTED)

    img.save(HERE / "entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
