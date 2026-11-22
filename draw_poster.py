#!/usr/bin/env python3
"""Draw the entry image: a one-page newspaper poster summing up the world
news of Saturday 21 November 2026. Output: entry.png, 1024x1024, < 1 MiB.

Stories (all reported on 21 Nov 2026, cross-checked against news sources):
  1. Russian missiles land in Poland during a huge barrage on Ukraine
  2. Tech-stock crash: Nasdaq -5.3%, S&P 500 into correction
  3. COP31 climate summit deadlocked, runs into overtime
  4. Trump, Xi and Putin meet at the APEC summit in Shenzhen
  5. Magnitude 6.9 earthquake in the Peruvian Andes
  6. Iran's Hormuz tanker attacks reach a wartime high
Ticker: FBI/USDA hacked, Bayer $7.25bn Roundup settlement, Nvidia halts
H200 exports to China, Basra power-plant fire kills 4, NASA pauses
Perseverance science.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (16, 30, 60)
GOLD = (232, 184, 75)
INK = (24, 24, 24)
GREY = (92, 92, 92)
CARD = (255, 255, 255)
BORDER = (221, 213, 194)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SERIF_B, 56)
F_DATE = font(SANS_B, 30)
F_SUB = font(SANS, 20)
F_TAG = font(SANS_B, 19)
F_HEAD = font(SANS_B, 27)
F_BODY = font(SANS, 20)
F_TICK = font(SANS_B, 19)
F_TICK_BODY = font(SANS, 19)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
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


def star(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def icon_missile(d, cx, cy, c):
    # incoming missile streaks, top-right to bottom-left, with impact burst
    for dx, dy, w in [(14, -18, 5), (26, -6, 4), (2, -28, 3)]:
        d.line([(cx + dx + 12, cy + dy - 12), (cx + dx - 12, cy + dy + 12)],
               fill=c, width=w)
    d.polygon([(cx - 2, cy - 2), (cx + 16, cy - 20), (cx + 8, cy - 2)],
              fill=c)
    star(d, cx - 20, cy + 18, 16, 7, 8, (230, 140, 40))


def icon_chart(d, cx, cy, c):
    d.line([(cx - 34, cy + 30), (cx + 34, cy + 30)], fill=(180, 180, 180),
           width=3)
    d.line([(cx - 34, cy + 30), (cx - 34, cy - 32)], fill=(180, 180, 180),
           width=3)
    pts = [(cx - 30, cy - 22), (cx - 12, cy - 8), (cx + 2, cy - 14),
           (cx + 18, cy + 8), (cx + 32, cy + 22)]
    d.line(pts, fill=c, width=6, joint="curve")
    d.polygon([(cx + 32, cy + 22), (cx + 18, cy + 20), (cx + 30, cy + 8)],
              fill=c)


def icon_globe(d, cx, cy, c):
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=c, width=5)
    d.ellipse([cx - 30, cy - 12, cx + 30, cy + 12], outline=c, width=3)
    d.ellipse([cx - 12, cy - 30, cx + 12, cy + 30], outline=c, width=3)
    d.line([(cx - 30, cy), (cx + 30, cy)], fill=c, width=3)


def icon_summit(d, cx, cy, c):
    for dx, col in [(-26, (180, 60, 50)), (0, c), (26, (200, 150, 40))]:
        d.ellipse([cx + dx - 9, cy - 26, cx + dx + 9, cy - 8], fill=col)
        d.arc([cx + dx - 13, cy - 6, cx + dx + 13, cy + 26], 180, 360,
              fill=col, width=6)
    d.line([(cx - 26, cy + 30), (cx + 26, cy + 30)], fill=(180, 180, 180),
           width=3)


def icon_quake(d, cx, cy, c):
    pts = [(cx - 34, cy), (cx - 22, cy - 4), (cx - 14, cy + 16),
           (cx - 6, cy - 26), (cx + 4, cy + 22), (cx + 12, cy - 10),
           (cx + 20, cy + 4), (cx + 34, cy - 2)]
    d.line(pts, fill=c, width=5, joint="curve")
    d.line([(cx - 34, cy + 32), (cx - 10, cy + 32)], fill=(180, 180, 180),
           width=3)
    d.line([(cx + 10, cy + 32), (cx + 34, cy + 32)], fill=(180, 180, 180),
           width=3)
    d.line([(cx - 10, cy + 32), (cx, cy + 24), (cx + 10, cy + 32)],
           fill=(180, 180, 180), width=3)


def icon_tanker(d, cx, cy, c):
    d.polygon([(cx - 34, cy + 6), (cx + 34, cy + 6), (cx + 26, cy + 26),
               (cx - 26, cy + 26)], fill=c)
    d.rectangle([cx - 28, cy - 8, cx - 8, cy + 6], fill=(200, 150, 40))
    d.rectangle([cx - 4, cy - 14, cx + 12, cy + 6], fill=(120, 160, 200))
    d.rectangle([cx + 16, cy - 20, cx + 30, cy + 6], fill=(150, 150, 150))
    d.polygon([(cx - 2, cy - 34), (cx + 8, cy - 16), (cx - 10, cy - 16)],
              fill=(230, 120, 30))
    d.line([(cx - 36, cy + 32), (cx + 36, cy + 32)], fill=(140, 180, 220),
           width=4)


PANELS = [
    ("WAR IN EUROPE", (192, 57, 43), icon_missile,
     "Russian missiles land in Poland",
     "Two missiles and a drone cross into NATO member Poland during "
     "Russia's heaviest barrage on Ukraine in weeks."),
    ("MARKETS", (27, 94, 70), icon_chart,
     "Tech crash erases Nasdaq's 2026 gains",
     "Nasdaq -5.3% and S&P 500 -3.7% into correction; Chinese AI stocks "
     "have shed $1.7 trillion since June."),
    ("CLIMATE", (46, 125, 50), icon_globe,
     "COP31 talks run into overtime",
     "The UN climate summit in Turkey is deadlocked over fossil fuels "
     "as delegates hunt for a final deal."),
    ("DIPLOMACY", (21, 101, 192), icon_summit,
     "Trump, Xi and Putin meet in Shenzhen",
     "A first trilateral summit on the APEC sidelines; Trump calls "
     "Putin \u201cmy friend\u201d, dismaying Europe."),
    ("DISASTER", (180, 83, 9), icon_quake,
     "6.9 quake shakes Peruvian Andes",
     "A strong earthquake strikes central Peru, shaking the Andes "
     "mountains."),
    ("GULF CRISIS", (106, 27, 154), icon_tanker,
     "Tanker attacks hit wartime high",
     "Iran's strikes on Gulf shipping reach their highest level of the "
     "war; oil flows through the strait fall 15%."),
]

TICKER = ("ALSO ON 21 NOVEMBER  \u00b7  FBI and US Agriculture Dept hacked  "
          "\u00b7  Bayer pays $7.25bn over Roundup  \u00b7  Nvidia halts H200 "
          "exports to China  \u00b7  Basra plant fire kills 4")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.rectangle([0, 150, W, 156], fill=GOLD)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 18), title, font=F_TITLE, fill=(255, 255, 255))
    date = "S A T U R D A Y   \u00b7   2 1   N O V E M B E R   2 0 2 6"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 88), date, font=F_DATE, fill=GOLD)
    sub = "Six stories that defined the day \u2014 and the rest in brief"
    sw = d.textlength(sub, font=F_SUB)
    d.text(((W - sw) / 2, 126), sub, font=F_SUB, fill=(170, 180, 200))

    # Panels: 2 cols x 3 rows
    mx, my, gap = 20, 172, 14
    pw = (W - 2 * mx - gap) // 2
    ph = 240
    for i, (tag, color, icon, head, body) in enumerate(PANELS):
        x = mx + (i % 2) * (pw + gap)
        y = my + (i // 2) * (ph + gap)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=10, fill=CARD,
                            outline=BORDER, width=2)
        d.rectangle([x, y + 10, x + 10, y + ph - 10], fill=color)
        tx = x + 26
        d.text((tx, y + 16), tag, font=F_TAG, fill=color)
        # icon medallion, top right
        icx, icy = x + pw - 62, y + 62
        d.ellipse([icx - 46, icy - 46, icx + 46, icy + 46],
                  fill=(245, 240, 228), outline=BORDER, width=2)
        icon(d, icx, icy, color)
        text_w = pw - 26 - 118
        lines = wrap(d, head, F_HEAD, text_w)
        hy = y + 46
        for ln in lines[:2]:
            d.text((tx, hy), ln, font=F_HEAD, fill=INK)
            hy += 34
        by = hy + 10
        for ln in wrap(d, body, F_BODY, pw - 52)[:4]:
            d.text((tx, by), ln, font=F_BODY, fill=(60, 60, 60))
            by += 27

    # Ticker
    ty = H - 78
    d.rectangle([0, ty, W, H], fill=NAVY)
    d.rectangle([0, ty, W, ty + 4], fill=GOLD)
    label = "ALSO ON 21 NOVEMBER"
    d.text((20, ty + 24), label, font=F_TICK, fill=GOLD)
    lw = d.textlength(label, font=F_TICK)
    rest = ("FBI and US Agriculture Dept hacked  \u00b7  Bayer pays $7.25bn "
            "over Roundup  \u00b7  Nvidia halts H200 exports to China  "
            "\u00b7  Basra plant fire kills 4")
    lines = wrap(d, rest, F_TICK_BODY, W - 40 - lw - 24)
    ry = ty + 10
    for ln in lines[:2]:
        d.text((20 + lw + 24, ry), ln, font=F_TICK_BODY,
               fill=(220, 225, 235))
        ry += 25

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
