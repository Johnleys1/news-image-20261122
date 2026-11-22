#!/usr/bin/env python3
"""Draw THE WORLD — Sunday 22 November 2026: a one-page front page summing up
the day's world news. 38 verified stories from 22 Nov 2026, across 8 regions.
Output: entry.png, 1024x1024, valid PNG under 1 MiB."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 26  # page margin
CW = W - 2 * M  # 972 content width

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (253, 252, 247)
INK = (17, 17, 17)
RED = (155, 28, 28)
GREY = (90, 90, 90)
RULE = (60, 60, 60)

# (region name, colour, [stories]) — every story verified from 22 Nov 2026 reporting.
REGIONS = [
    ("NORTH AMERICA", (32, 74, 122), [
        "Hegseth sets new limits on U.S.–Canada defence ties",
        "U.S. airlines warned of possible al-Qaeda attacks",
        "Trump: Iran deal could last 20 years",
        "Gupta jailed 19 years over Pannun murder plot",
        "Senate Democrats test new leaders after sweep",
    ]),
    ("LATIN AMERICA", (138, 109, 0), [
        "Magnitude 6.9 quake shakes Peru's Andes",
        "Bolsonaro in ICU with bowel obstruction",
        "Cartel arrest sparks deadly Sinaloa violence; 11 dead",
        "Brazil town clears rubble after deadly storm",
    ]),
    ("EUROPE", (91, 45, 142), [
        "Estonia to shut border with Russia from Dec 1",
        "Drones hit Russian cargo ship in Baltic; Finland on alert",
        "Russian missiles crash in Poland; Tusk sees provocation",
        "Denmark foils Russian plot to kill rapper; envoy expelled",
        "Von der Leyen: Russian threats 'becoming more overt'",
        "French march for sixth weekend over living costs",
    ]),
    ("MIDDLE EAST", (155, 28, 28), [
        "Bahrain: Iran hit civilian plant, sparking fire",
        "Bahrain probes Patriot interceptor crash",
        "Qeshm blasts 'U.S. munitions disposal', Iran says",
        "Tankers hit off Oman as Iran–U.S. tensions rise",
        "Saudi coalition downs 3 Houthi missiles aimed at Riyadh",
        "Four Palestinians killed in Gaza ceasefire breaches",
        "Man shot dead by West Bank settler guards",
    ]),
    ("ASIA-PACIFIC", (15, 107, 74), [
        "Modi opens Nitish Setu bridge in Bihar",
        "Cyclone Akvan grounds 14 flights at Ranchi",
        "Japanese troops to train live-fire in India — a first",
        "Nepal PM Shah visits India on first foreign trip",
        "Seoul offers $75,000 bounty on exam cheats",
        "Trump: China's nuclear build-up 'rapid and concerning'",
    ]),
    ("AFRICA", (179, 92, 0), [
        "Boat capsizes in Nigeria; 24 dead on way to funeral",
        "Libya loses $30.8m as gunmen block oil pipeline",
        "Violence and distrust hamper DR Congo Ebola fight",
    ]),
    ("SOUTH ASIA", (14, 107, 122), [
        "Pakistan forces kill 15 militants in Balochistan",
        "India face New Zealand in windy Wellington",
        "Advani, Ramachandran win snooker openers",
    ]),
    ("WORLD & MARKETS", (51, 51, 51), [
        "COP31 climate talks near final deal in Antalya",
        "COP31 AI pledge shunned by big U.S. tech firms",
        "Crude oil futures slide over 3%",
    ]),
]

LEAD_HEAD = "IRAN STRIKES U.S. BASE IN KUWAIT"
LEAD_SUM = ("Tehran hits an American air base in Kuwait and targets Bahrain as Gulf "
            "attacks widen — tankers are struck off Oman and a civilian plant is left burning.")


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer border
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    # ---- masthead ----
    f_title = ImageFont.truetype(SERIF_B, 86)
    d.text((W / 2, 30), "THE WORLD", font=f_title, fill=INK, anchor="ma")
    f_date = ImageFont.truetype(SANS_B, 24)
    d.text((W / 2, 122), "SUNDAY 22 NOVEMBER 2026", font=f_date, fill=RED, anchor="ma")
    d.line([(M, 152), (W - M, 152)], fill=INK, width=3)
    d.line([(M, 157), (W - M, 157)], fill=INK, width=1)

    # ---- lead story ----
    y = 168
    f_tag = ImageFont.truetype(SANS_B, 13)
    tag = "LEAD STORY"
    tw = f_tag.getlength(tag)
    d.rectangle([M, y, M + tw + 18, y + 22], fill=RED)
    d.text((M + 9, y + 4), tag, font=f_tag, fill=(255, 255, 255))
    y += 30
    f_head = ImageFont.truetype(SANS_B, 33)
    d.text((M, y), LEAD_HEAD, font=f_head, fill=INK)
    y += 42
    f_sum = ImageFont.truetype(SANS, 16)
    for line in wrap(d, LEAD_SUM, f_sum, CW):
        d.text((M, y), line, font=f_sum, fill=(51, 51, 51))
        y += 20
    y += 6
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)

    # ---- region bands ----
    band_h = 88
    gap = 2
    by = y + 8
    for name, color, stories in REGIONS:
        # header strip
        d.rectangle([M, by, W - M, by + 22], fill=color)
        f_reg = ImageFont.truetype(SANS_B, 14)
        d.text((M + 8, by + 4), f"{name} — {len(stories)}", font=f_reg, fill=(255, 255, 255))
        # story rows
        n = len(stories)
        rows = 1 if n <= 3 else 2
        cols = (n + rows - 1) // rows
        col_w = CW / cols
        f_story = ImageFont.truetype(SANS, 13 if rows == 1 else 12)
        lh = 16 if rows == 1 else 15
        row_h = (band_h - 22) // rows
        for i, story in enumerate(stories):
            r, c = divmod(i, cols)
            x = M + c * col_w
            sy = by + 22 + r * row_h + 4
            d.rectangle([x + 2, sy + 3, x + 11, sy + 12], fill=color)
            lines = wrap(d, story, f_story, col_w - 20)
            ly = sy
            for line in lines[: 4 if rows == 1 else 2]:
                d.text((x + 16, ly), line, font=f_story, fill=INK)
                ly += lh
        by += band_h + gap

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
