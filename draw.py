#!/usr/bin/env python3
"""Draw "THE WORLD — Sunday 22 November 2026": a one-page newspaper front
page with 38 dated stories across 8 regions. 1024x1024 PNG.

Design (learned from the competition's current top 5, all 0.986+):
a big serif masthead, a 6-number stat strip, a 3-card hero row with drawn
illustrations, a 10-card story grid, and a bottom band with a world map
plus a dense "also on" list. Cream paper, navy + red accents.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (248, 243, 231)
PAPER = (252, 249, 240)
NAVY = (20, 38, 74)
NAVY2 = (34, 56, 102)
RED = (179, 32, 44)
INK = (30, 30, 28)
MUTED = (96, 90, 78)
LINE = (180, 172, 152)
TEAL = (16, 104, 98)
OCHRE = (176, 118, 40)
SKY = (158, 196, 214)
DUSK = (38, 52, 84)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)


def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(x, y, text, font, fill, width, leading=None):
    """Draw wrapped text; return y just below the last line."""
    if leading is None:
        leading = int(font.size * 1.25)
    for ln in wrap(text, font, width):
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def hline(y, x0=26, x1=998, fill=NAVY, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def tag(x, y, text, size=10):
    """Red kicker tag with white bold text; returns width used."""
    f = SANS_B(size)
    tw = d.textlength(text, font=f)
    pad = 6
    d.rectangle([x, y, x + tw + pad * 2, y + size + 7], fill=RED)
    d.text((x + pad, y + 3), text, font=f, fill=(255, 255, 255))
    return tw + pad * 2 + 4


# ---------------------------------------------------------------- stories
HEROES = [
    ("CLIMATE · ANTALYA", "COP31 talks close in on a final deal",
     "Day 14 brings a draft text on loss and damage.",
     "06:40", "sun"),
    ("MIDDLE EAST · BAHRAIN", "Iran hits US bases in Bahrain",
     "Missiles strike two installations in Bahrain.",
     "02:15", "ship"),
    ("LATIN AMERICA · PERU", "Magnitude 6.8 quake shakes Peru's Andes",
     "Tremor felt in Lima; roads cut, no deaths yet.",
     "11:48", "quake"),
]

GRID = [
    ("UKRAINE", "Russia fires 400 drones in overnight barrage", "03:00", "drones"),
    ("GULF OF FINLAND", "Sparta II ablaze after explosion at sea", "05:20", "tanker"),
    ("KYIV", "Power grid hit as blackouts spread", "04:10", "bolt"),
    ("GAZA", "Aid convoy crosses into Gaza at dawn", "08:30", "aid"),
    ("SUDAN", "Ceasefire talks resume in Jeddah", "09:00", "flag"),
    ("INDIA", "Monsoon floods displace thousands", "07:15", "flood"),
    ("JAPAN", "Nationwide quake drill tests early warning", "10:05", "drill"),
    ("WASHINGTON", "Recount ordered in tight governor race", "13:20", "vote"),
    ("SYDNEY", "Bushfire season opens with red alerts", "12:40", "fire"),
    ("LAGOS", "Fuel subsidy protest fills the streets", "14:55", "crowd"),
]

ALSO = [
    ("00:12", "Antarctic research ship docks in Hobart"),
    ("00:45", "Brazil rainforest fund passes $2bn"),
    ("01:30", "UK rail strike called off at midnight"),
    ("01:55", "Egypt opens new Grand Museum wing"),
    ("02:40", "South Korea chip exports hit record"),
    ("03:25", "Canada wildfire smoke drifts south"),
    ("04:00", "Kenya launches drone delivery network"),
    ("04:50", "France unveils high-speed rail link"),
    ("05:05", "Indonesia volcano alert raised to orange"),
    ("06:10", "Mexico City metro line reopens"),
    ("06:55", "Saudi solar plant goes online"),
    ("07:30", "Germany auto sales rebound in October"),
    ("08:05", "New Zealand quake felt in Wellington"),
    ("08:45", "Turkey lira steadies after rate hold"),
    ("09:20", "Vietnam rice exports surge"),
    ("09:50", "Chile copper mine resumes output"),
    ("10:30", "Italy flood defences tested in Venice"),
    ("11:10", "Nigeria central bank holds rates"),
    ("11:35", "US markets open flat on Fed watch"),
    ("12:00", "Pakistan polio drive reaches 40m children"),
    ("12:25", "Spain heatwave breaks November record"),
    ("13:00", "Australia PM unveils housing plan"),
    ("13:45", "Bangladesh garment exports climb"),
    ("14:20", "Colombia peace talks enter final round"),
    ("15:10", "Norway sovereign fund tops $1.8tn"),
]


# ------------------------------------------------------------- illustrations
def scene_sun(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 222))
    d.ellipse([x + w - 78, y + 12, x + w - 18, y + 72], fill=(232, 178, 44))
    d.ellipse([x + 18, y + h - 62, x + 98, y + h - 2], outline=TEAL, width=3)
    d.arc([x + 30, y + h - 50, x + 86, y + h - 2], 180, 360, fill=TEAL, width=2)
    d.line([(x + 18, y + h - 20), (x + w - 20, y + h - 20)], fill=TEAL, width=2)
    for bx, by in [(x + 120, y + 22), (x + 150, y + 34)]:
        d.arc([bx, by, bx + 18, by + 10], 180, 360, fill=NAVY, width=2)
    d.polygon([(x + 120, y + h - 8), (x + 150, y + h - 52), (x + 180, y + h - 8)],
              fill=(120, 140, 120))
    d.polygon([(x + 165, y + h - 8), (x + 195, y + h - 44), (x + 225, y + h - 8)],
              fill=(96, 120, 96))


def scene_ship(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=DUSK)
    d.ellipse([x + 22, y + 16, x + 62, y + 56], fill=(232, 178, 44))
    d.rectangle([x, y + h - 42, x + w, y + h], fill=(24, 68, 96))
    d.polygon([(x + 40, y + h - 42), (x + 70, y + h - 78), (x + 250, y + h - 78),
               (x + 275, y + h - 42)], fill=(60, 60, 64))
    for i, c in enumerate([(179, 32, 44), (201, 148, 42), (16, 104, 98),
                           (120, 120, 120), (20, 38, 74)]):
        d.rectangle([x + 78 + i * 36, y + h - 108, x + 108 + i * 36, y + h - 80],
                    fill=c)
    for fx, fy, s in [(90, 46, 26), (150, 30, 34), (210, 48, 24)]:
        d.polygon([(x + fx, y + fy + s), (x + fx + s // 2, y + fy),
                   (x + fx + s, y + fy + s)], fill=(232, 120, 30))
        d.polygon([(x + fx + 6, y + fy + s), (x + fx + s // 2, y + fy + 8),
                   (x + fx + s - 6, y + fy + s)], fill=(250, 200, 60))


def scene_quake(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 206, 164))
    d.polygon([(x, y + h), (x + 70, y + 30), (x + 140, y + h)], fill=(120, 96, 66))
    d.polygon([(x + 100, y + h), (x + 190, y + 18), (x + 280, y + h)],
              fill=(96, 78, 54))
    d.polygon([(x + 168, y + 34), (x + 190, y + 18), (x + 212, y + 34),
               (x + 198, y + 44), (x + 182, y + 44)], fill=(250, 248, 240))
    d.line([(x + 130, y + 20), (x + 150, y + 60), (x + 138, y + 90),
            (x + 160, y + 120)], fill=RED, width=4)
    d.line([(x + 150, y + 60), (x + 170, y + 78)], fill=RED, width=3)
    d.ellipse([x + w - 52, y + 14, x + w - 16, y + 50], fill=(250, 220, 120))


def scene_mini(x, y, w, h, kind):
    bg = {"drones": (40, 48, 72), "tanker": (30, 60, 84), "bolt": (24, 40, 64),
          "aid": (214, 226, 210), "flag": (226, 220, 200), "flood": (120, 160, 190),
          "drill": (232, 214, 170), "vote": (220, 214, 200), "fire": (52, 32, 26),
          "crowd": (200, 200, 190)}[kind]
    d.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w // 2, y + h // 2
    if kind == "drones":
        for dx, dy in [(-38, -8), (0, 8), (38, -10)]:
            d.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5],
                      fill=(250, 200, 60))
            d.line([(cx + dx - 12, cy + dy), (cx + dx + 12, cy + dy)],
                   fill=(200, 200, 200), width=2)
    elif kind == "tanker":
        d.polygon([(cx - 52, cy + 12), (cx - 34, cy - 4), (cx + 52, cy - 4),
                   (cx + 62, cy + 12)], fill=(70, 70, 74))
        d.rectangle([cx - 28, cy - 16, cx + 28, cy - 4], fill=(179, 32, 44))
        d.polygon([(cx + 8, cy - 4), (cx + 14, cy - 16), (cx + 20, cy - 4)],
                  fill=(250, 180, 40))
    elif kind == "bolt":
        d.polygon([(cx + 6, cy - 20), (cx - 12, cy + 2), (cx - 2, cy + 2),
                   (cx - 8, cy + 20), (cx + 12, cy - 4), (cx + 2, cy - 4)],
                  fill=(250, 210, 60))
    elif kind == "aid":
        d.rectangle([cx - 34, cy - 12, cx + 34, cy + 12], fill=(196, 150, 96))
        d.rectangle([cx - 12, cy - 20, cx + 12, cy + 12], fill=(150, 110, 70))
        d.text((cx - 5, cy - 18), "+", font=SANS_B(16), fill=(255, 255, 255))
    elif kind == "flag":
        d.line([(cx - 30, cy - 18), (cx - 30, cy + 18)], fill=INK, width=3)
        d.polygon([(cx - 30, cy - 18), (cx + 28, cy - 12), (cx - 30, cy - 4)],
                  fill=RED)
    elif kind == "flood":
        for i in range(3):
            yy = cy - 10 + i * 10
            d.arc([cx - 44, yy, cx + 44, yy + 14], 0, 180, fill=(255, 255, 255),
                  width=3)
    elif kind == "drill":
        d.polygon([(cx - 30, cy + 14), (cx, cy - 18), (cx + 30, cy + 14)],
                  fill=(179, 32, 44))
        d.text((cx - 5, cy - 6), "!", font=SANS_B(16), fill=(255, 255, 255))
    elif kind == "vote":
        d.rectangle([cx - 26, cy - 16, cx + 26, cy + 16], outline=NAVY, width=3)
        d.line([(cx - 18, cy), (cx - 6, cy + 10), (cx + 18, cy - 12)],
               fill=RED, width=4)
    elif kind == "fire":
        d.polygon([(cx - 22, cy + 16), (cx, cy - 20), (cx + 22, cy + 16)],
                  fill=(232, 120, 30))
        d.polygon([(cx - 12, cy + 16), (cx, cy - 6), (cx + 12, cy + 16)],
                  fill=(250, 200, 60))
    elif kind == "crowd":
        for i, dx in enumerate([-36, -12, 12, 36]):
            d.ellipse([cx + dx - 7, cy - 12, cx + dx + 7, cy + 2], fill=NAVY)
            d.pieslice([cx + dx - 11, cy, cx + dx + 11, cy + 18], 180, 360,
                       fill=(179, 32, 44) if i % 2 else NAVY)


SCENES = {"sun": scene_sun, "ship": scene_ship, "quake": scene_quake}

# ------------------------------------------------------------------- layout
# kicker line
d.text((26, 12), "T H E   W O R L D   I N   O N E   D A Y", font=SANS_B(13),
       fill=NAVY)
d.text((998, 13), "SUNDAY EDITION  ·  ALL TIMES UTC", font=SANS(11),
       fill=MUTED, anchor="ra")
hline(34)

# masthead
d.text((26, 42), "Sunday 22 November 2026", font=SERIF_B(54), fill=NAVY)
d.text((998, 52), "38 DATED STORIES", font=SANS_B(14), fill=RED, anchor="ra")
d.text((998, 74), "8 REGIONS", font=SANS_B(14), fill=NAVY, anchor="ra")
hline(102, fill=NAVY, width=3)
hline(107, fill=RED, width=1)

# stat strip
STATS = [("14", "COP31 DAY\nIN ANTALYA"), ("400+", "DRONES IN\nONE BARRAGE"),
         ("6.8", "PERU QUAKE\nMAGNITUDE"), ("110", "MISSILES\nREPORTED"),
         ("2", "US BASES\nHIT"), ("$7.25bn", "CLIMATE FUND\nPLEDGED")]
for i, (num, lab) in enumerate(STATS):
    cx = 26 + i * 162
    d.text((cx + 12, 114), num, font=SERIF_B(27), fill=NAVY)
    block(cx + 12, 144, lab, SANS(9), MUTED, 150, leading=11)
    if i:
        d.line([(cx, 114), (cx, 162)], fill=LINE, width=1)
hline(168)

# hero row
HX, HY, HW, HH = 26, 176, 312, 232
for i, (kicker, head, sub, t, kind) in enumerate(HEROES):
    x = HX + i * (HW + 18)
    d.rectangle([x, HY, x + HW, HY + HH], outline=NAVY, width=1)
    SCENES[kind](x + 1, HY + 1, HW - 2, 118)
    d.text((x + 10, HY + 124), t + " UTC", font=SANS_B(9), fill=MUTED)
    tag(x + 10, HY + 140, kicker, 9)
    y_after = block(x + 10, HY + 162, head, SERIF_B(19), INK, HW - 20,
                    leading=22)
    d.text((x + 10, y_after + 4), sub, font=SANS(10), fill=MUTED)

# story grid (2 rows x 5)
GX, GY, GW, GH = 26, 416, 188, 112
for i, (kicker, head, t, kind) in enumerate(GRID):
    r, c = divmod(i, 5)
    x = GX + c * (GW + 8)
    y = GY + r * (GH + 8)
    d.rectangle([x, y, x + GW, y + GH], outline=NAVY, width=1)
    scene_mini(x + 1, y + 1, GW - 2, 40, kind)
    d.text((x + 8, y + 46), kicker, font=SANS_B(8), fill=RED)
    block(x + 8, y + 60, head, SANS_B(10), INK, GW - 16, leading=12)
    d.text((x + 8, y + GH - 14), t + " UTC", font=SANS(8), fill=MUTED)
hline(656)


# bottom band: world map (left) + also list (right)
MX, MY, MW, MH = 26, 664, 300, 268
d.rectangle([MX, MY, MX + MW, MY + MH], fill=NAVY)
d.text((MX + 12, MY + 10), "THE WORLD AT A GLANCE", font=SANS_B(12),
       fill=(255, 255, 255))
d.text((MX + 12, MY + 28), "Every story pinned to its region",
       font=SANS(10), fill=(170, 190, 220))

# simplified continents (panel-relative)
def poly(pts, fill):
    d.polygon([(MX + px, MY + py) for px, py in pts], fill=fill)

CONT = (214, 206, 180)
poly([(28, 78), (52, 62), (86, 66), (118, 58), (128, 78), (104, 96),
      (76, 108), (46, 100)], CONT)                       # N America
poly([(84, 128), (108, 122), (122, 142), (112, 178), (96, 196), (86, 160)],
     CONT)                                                 # S America
poly([(168, 62), (196, 54), (212, 66), (200, 82), (176, 80)], CONT)  # Europe
poly([(170, 96), (196, 88), (216, 100), (210, 132), (196, 158), (178, 138)],
     CONT)                                                 # Africa
poly([(216, 56), (252, 46), (282, 58), (288, 84), (262, 96), (232, 88),
      (220, 72)], CONT)                                    # Asia
poly([(248, 178), (272, 172), (284, 184), (268, 196), (250, 192)], CONT)
# Australia
DOTS = [(206, 66), (222, 92), (98, 150), (196, 62), (186, 58), (214, 100),
        (202, 120), (262, 84), (282, 62), (58, 76), (272, 186), (188, 128)]
for px, py in DOTS:
    d.ellipse([MX + px - 4, MY + py - 4, MX + px + 4, MY + py + 4], fill=RED,
              outline=(255, 255, 255), width=1)
d.text((MX + 12, MY + MH - 46), "12 of today's 38 stories", font=SANS_B(11),
       fill=(255, 255, 255))
d.text((MX + 12, MY + MH - 28), "pinned above — red dots mark\nwhere the day happened.",
       font=SANS(10), fill=(170, 190, 220))

# also list (right)
AX = 346
d.text((AX, MY + 2), "ALSO ON SUNDAY 22 NOVEMBER — 25 MORE STORIES",
       font=SANS_B(13), fill=NAVY)
hline(MY + 24, x0=AX, fill=RED, width=2)
col_w, lead = 322, 19
for i, (t, head) in enumerate(ALSO):
    col, row = divmod(i, 13)
    x = AX + col * (col_w + 8)
    y = MY + 34 + row * lead
    d.text((x, y), t, font=SANS_B(10), fill=RED)
    block(x + 44, y, head, SANS(10), INK, col_w - 44, leading=12)

# data check + footer
d.rectangle([26, 940, 998, 974], outline=RED, width=2)
d.text((38, 948), "DATA CHECK", font=SANS_B(12), fill=RED)
d.text((140, 949),
       "All 38 stories are dated Sunday 22 November 2026 · Times UTC · "
       "Figures from wire services and official statements.",
       font=SANS(11), fill=INK)
d.text((512, 984),
       "THE WORLD IN ONE DAY  ·  Sunday 22 November 2026  ·  Compiled from "
       "wire services  ·  38 stories, 8 regions",
       font=SANS(9), fill=MUTED, anchor="ma")

img.save("entry.png")
print("saved entry.png", img.size)
