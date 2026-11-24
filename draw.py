#!/usr/bin/env python3
"""news-23 b17 front-page-dense: THE WORLD TODAY, Monday 23 November 2026 (31 stories).
Draws entry.png (1024x1024) with PIL. Run: python3 draw.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 14                      # side margin
CW = W - 2 * M              # content width = 996

PAPER = (246, 241, 227)
INK = (20, 20, 20)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
GOLD = (154, 122, 26)
NAVY = (31, 58, 95)
TEAL = (15, 95, 107)
GRAY = (90, 90, 90)
LIGHT = (210, 205, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS_O = os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, max_w, line_h, max_lines=None):
    """Draw wrapped text; returns y after last line."""
    lines = wrap(d, text, font, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += line_h
    return y


def chip(d, x_right, y, label, bg):
    """Right-aligned chip; returns left x."""
    f = F(SANS_B, 9)
    w = d.textlength(label, font=f) + 10
    x = x_right - w
    d.rounded_rectangle([x, y, x_right, y + 13], radius=2, fill=bg)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return x


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.text((M, 6), "THE WORLD TODAY", font=F(SERIF_B, 50), fill=INK)
    date_txt = "MONDAY 23 NOVEMBER 2026"
    df = F(SANS_B, 20)
    d.text((W - M - d.textlength(date_txt, font=df), 22), date_txt, font=df, fill=GOLD)
    d.line([(M, 62), (W - M, 62)], fill=INK, width=2)

    # ---------- kicker ----------
    d.text((M, 68), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
           font=F(SANS_B, 13), fill=DARKRED)

    # ---------- number strip ----------
    nums = [
        ("\u22123.3%", "KOSPI", (192, 32, 32)),
        ("5.3", "US-CHINA POWER GAP", NAVY),
        ("11,762", "EBOLA CASES, DRC", (122, 90, 20)),
        ("$450M", "SKUBAL DEAL", (34, 110, 60)),
        ("$107.3B", "ANTHROPIC IPO", (110, 40, 130)),
    ]
    col_w = CW / 5.0
    y0 = 82
    for i, (num, lab, col) in enumerate(nums):
        x = M + i * col_w
        d.text((x + 4, y0), num, font=F(SANS_B, 30), fill=col)
        d.text((x + 4, y0 + 32), lab, font=F(SANS_B, 10), fill=INK)
        if i:
            d.line([(x, y0 + 4), (x, y0 + 40)], fill=LIGHT, width=1)
    d.line([(M, 128), (W - M, 128)], fill=LIGHT, width=1)

    # ---------- region bar ----------
    regions = [
        ("ASIA-PACIFIC 6", 6, (46, 93, 58)),
        ("AMERICAS 9", 9, NAVY),
        ("MIDDLE EAST 6", 6, (122, 90, 30)),
        ("EUROPE 5", 5, (31, 107, 107)),
        ("AFRICA 3", 3, (107, 122, 30)),
        ("WORLD 2", 2, (85, 85, 85)),
    ]
    total = sum(c for _, c, _ in regions)
    rx = M
    ry = 132
    for name, cnt, col in regions:
        w = CW * cnt / total
        d.rectangle([rx, ry, rx + w - 1, ry + 18], fill=col)
        tf = F(SANS_B, 10)
        tw = d.textlength(name, font=tf)
        d.text((rx + (w - tw) / 2, ry + 4), name, font=tf, fill=(255, 255, 255))
        rx += w

    # ---------- the day in numbers ----------
    d.text((M, 156), "THE DAY IN NUMBERS", font=F(SANS_B, 11), fill=INK)
    d.text((M + 148, 156), "\u22125.8% INTRADAY LOW  \u00b7  165 MISSILES IN A WEEK  \u00b7  12,000 CLEARED  \u00b7  264 KG SEIZED  \u00b7  2% TAX BACKED",
           font=F(SANS, 11), fill=INK)

    # ---------- hero scenes ----------
    hx = [M, M + 332, M + 664]
    hw = 326
    hy, hh = 172, 164

    # --- hero 1: Kospi night chart ---
    x = hx[0]
    d.rectangle([x, hy, x + hw, hy + hh], fill=(14, 30, 58))
    for sx, sy in [(30, 20), (90, 12), (150, 26), (210, 14), (260, 30), (300, 18), (60, 40), (180, 8), (240, 42)]:
        d.ellipse([x + sx - 1, hy + sy - 1, x + sx + 1, hy + sy + 1], fill=(255, 255, 255))
    # skyline
    import random
    random.seed(7)
    bx = x + 6
    while bx < x + hw - 14:
        bw = random.randint(14, 26)
        bh = random.randint(22, 52)
        d.rectangle([bx, hy + hh - 34 - bh, bx + bw, hy + hh - 34], fill=(24, 48, 84))
        for wy in range(hy + hh - 30 - bh, hy + hh - 36, 8):
            for wx in range(bx + 3, bx + bw - 3, 7):
                if random.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    # chart line (kept below the big label)
    pts = [(x + 12, hy + 66), (x + 52, hy + 60), (x + 92, hy + 70), (x + 132, hy + 62),
           (x + 172, hy + 76), (x + 212, hy + 72), (x + 252, hy + 88), (x + 292, hy + 84),
           (x + 316, hy + 96)]
    d.line(pts, fill=(255, 90, 70), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 214, 90))
    d.text((x + 10, hy + 6), "\u22123.3%", font=F(SANS_B, 30), fill=(255, 80, 60))
    d.rectangle([x, hy + hh - 22, x + hw, hy + hh], fill=(0, 0, 0))
    d.text((x + 8, hy + hh - 18), "KOSPI  4,708.54  \u00b7  \u2212161 PTS", font=F(SANS_B, 11), fill=(255, 255, 255))

    # --- hero 2: Guterres globe ---
    x = hx[1]
    d.rectangle([x, hy, x + hw, hy + hh], fill=TEAL)
    d.text((x + 10, hy + 6), "150 DELEGATES", font=F(SANS_B, 24), fill=(255, 214, 60))
    d.text((x + 10, hy + 34), "BACK A RISK FRAMEWORK", font=F(SANS_B, 13), fill=(255, 255, 255))
    # globe, right side, clear of text
    cx, cy, r = x + 258, hy + 96, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 215, 235))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(255, 255, 255), width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=1)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(255, 255, 255), width=1)
    d.ellipse([cx - 12, cy - 18, cx - 2, cy - 8], fill=(90, 160, 90))
    d.ellipse([cx + 6, cy + 8, cx + 16, cy + 18], fill=(90, 160, 90))
    # flags bottom-left
    for i, fc in enumerate([(200, 40, 40), (60, 90, 200), (240, 200, 40)]):
        fx = x + 18 + i * 34
        fy = hy + hh - 52
        d.line([(fx, fy), (fx, fy - 30)], fill=(255, 255, 255), width=2)
        d.polygon([(fx, fy - 30), (fx + 22, fy - 24), (fx, fy - 18)], fill=fc)
    # podium
    d.polygon([(x + 150, hy + hh - 22), (x + 210, hy + hh - 22), (x + 196, hy + hh - 62), (x + 164, hy + hh - 62)], fill=(90, 60, 30))
    d.rectangle([x, hy + hh - 22, x + hw, hy + hh], fill=(0, 0, 0))
    lbl = "UN \u00b7 BRIDGETOWN"
    lf = F(SANS_B, 10)
    d.text((x + hw - 8 - d.textlength(lbl, font=lf), hy + hh - 18), lbl, font=lf, fill=(255, 255, 255))

    # --- hero 3: power bars ---
    x = hx[2]
    d.rectangle([x, hy, x + hw, hy + hh], fill=(250, 246, 235))
    d.rectangle([x, hy, x + hw, hy + hh], outline=(180, 175, 160), width=1)
    d.text((x + 10, hy + 6), "NARROWEST SINCE 2018", font=F(SANS_B, 10), fill=INK)
    gap_txt = "GAP 5.3"
    gf = F(SANS_B, 16)
    d.text((x + hw - 8 - d.textlength(gap_txt, font=gf), hy + 4), gap_txt, font=gf, fill=GOLD)
    base = hy + hh - 34
    bars = [("US", 78.9, NAVY, 92), ("CHINA", 73.6, (178, 34, 34), 86), ("INDIA", 40.5, (176, 140, 30), 48)]
    bw = 62
    gap = (hw - 3 * bw) // 4
    for i, (name, val, col, bhgt) in enumerate(bars):
        bx = x + gap + i * (bw + gap)
        d.rectangle([bx, base - bhgt, bx + bw, base], fill=col)
        vt = f"{val}"
        vf = F(SANS_B, 13)
        d.text((bx + (bw - d.textlength(vt, font=vf)) / 2, base - bhgt + 6), vt, font=vf, fill=(255, 255, 255))
        nf = F(SANS_B, 10)
        d.text((bx + (bw - d.textlength(name, font=nf)) / 2, base + 6), name, font=nf, fill=INK)
    d.text((x + 10, hy + 22), "ASIA POWER INDEX 2026", font=F(SANS, 9), fill=GRAY)

    # ---------- hero text blocks ----------
    heroes = [
        ("1", "AI ROUT HITS ASIA",
         "Kospi \u22123.3% to 4,708.54, sheds 161 pts; intraday \u22125.8%. Samsung \u22123.1%, SK Hynix \u22122.5%.",
         "KOREA EXCHANGE", "REPORTED", NAVY),
        ("2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
         "UNITED NATIONS", "REPORTED", NAVY),
        ("3", "US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
         "LOWY INSTITUTE", "REPORTED", NAVY),
    ]
    ty = 342
    for i, (num, head, body, src, chip_lbl, chip_bg) in enumerate(heroes):
        x = hx[i]
        d.ellipse([x, ty, x + 20, ty + 20], fill=RED)
        nf = F(SANS_B, 12)
        d.text((x + 10 - d.textlength(num, font=nf) / 2, ty + 4), num, font=nf, fill=(255, 255, 255))
        text_block(d, x + 26, ty, head, F(SANS_B, 15), INK, hw - 26, 18, max_lines=2)
        text_block(d, x, ty + 38, body, F(SANS, 11), INK, hw, 13, max_lines=2)
        d.text((x, ty + 66), src, font=F(SANS, 9), fill=GRAY)
        chip(d, x + hw, ty + 64, chip_lbl, chip_bg)

    # ---------- cards ----------
    d.text((M, 432), "MORE OF THE DAY \u2014 10 STORIES", font=F(SANS_B, 12), fill=INK)
    d.line([(M, 446), (W - M, 446)], fill=INK, width=1)
    cards = [
        ("AMERICAS", NAVY, "BESSENT: NVIDIA ANSWERS", "Treasury chief wants to know of violations over China sales.", "Reuters", "REPORTED", NAVY),
        ("FBI", (60, 60, 60), "FBI PROBES NCIC HACK", "Hackers hit the NCIC system used by police nationwide.", "AP", "REPORTED", NAVY),
        ("WHITE HOUSE", (122, 90, 30), "TRUMP: IRAN STRIKES MAY RESUME", "President says strikes could resume in the New Year.", "Reuters", "REPORTED", NAVY),
        ("MARKETS", (107, 122, 30), "US FUTURES JUMP 3%", "Holiday-week rally lifts Nasdaq futures as the AI rout cools.", "Bloomberg", "REPORTED", NAVY),
        ("SPORT", (34, 110, 60), "SKUBAL'S $450M METS DEAL", "Two-time Cy Young winner signs nine years, largest ever for a pitcher.", "ESPN", "REPORTED", NAVY),
        ("SPORT", (34, 110, 60), "TOM JACKSON DIES AT 75", "Broncos linebacker turned ESPN voice dies.", "ESPN", "REPORTED", NAVY),
        ("LEGAL", (110, 40, 130), "STATES SUE SPACEX", "Ten states challenge AI safety claims.", "AP", "REPORTED", NAVY),
        ("TECH", TEAL, "ANTHROPIC IPO: $107.3B", "Claude maker raises at $83 a share; debut closes $97.17.", "WSJ", "REPORTED", NAVY),
        ("EUROPE", (31, 107, 107), "POLAND: 3 RUSSIAN MISSILES CROSSED AIRSPACE", "Kyiv says three Kh-101s crossed Polish airspace Friday.", "AP", "CLAIM", RED),
        ("SPACE", (60, 60, 60), "RUSSIAN NUCLEAR SATELLITE", "Intel claims Moscow built a satellite to carry a nuclear warhead.", "Reuters", "CLAIM", RED),
    ]
    colw = 195
    gapx = 5
    rowh = 72
    for idx, (cat, ccol, head, body, src, chip_lbl, chip_bg) in enumerate(cards):
        row, col = divmod(idx, 5)
        cx = M + col * (colw + gapx)
        cy = 452 + row * (rowh + 6)
        d.rectangle([cx, cy, cx + colw, cy + 14], fill=ccol)
        cf = F(SANS_B, 9)
        d.text((cx + 4, cy + 3), cat, font=cf, fill=(255, 255, 255))
        nf = F(SANS_B, 9)
        d.text((cx + colw - 4 - d.textlength(str(idx + 4), font=nf), cy + 3), str(idx + 4), font=nf, fill=(255, 255, 255))
        text_block(d, cx + 2, cy + 17, head, F(SANS_B, 11), INK, colw - 4, 13, max_lines=2)
        text_block(d, cx + 2, cy + 46, body, F(SANS, 9), INK, colw - 4, 11, max_lines=1)
        d.text((cx + 2, cy + 60), src, font=F(SANS, 8), fill=GRAY)
        chip(d, cx + colw, cy + 59, chip_lbl, chip_bg)

    # ---------- map + ALSO ----------
    my = 608
    d.text((M, my), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=INK)
    d.text((530, my), "ALSO ON MONDAY", font=F(SANS_B, 12), fill=INK)
    map_x, map_y, map_w, map_h = M, my + 18, 500, 178
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(207, 224, 234))
    for gx in range(map_x, map_x + map_w + 1, 25):
        d.line([(gx, map_y), (gx, map_y + map_h)], fill=(235, 242, 246), width=1)
    for gy in range(map_y, map_y + map_h + 1, 25):
        d.line([(map_x, gy), (map_x + map_w, gy)], fill=(235, 242, 246), width=1)

    def proj(lon, lat):
        px = map_x + (lon + 180) / 360.0 * map_w
        py = map_y + (85 - lat) / 145.0 * map_h
        return (px, py)

    LAND = (143, 174, 107)
    continents = [
        [(-168, 66), (-140, 70), (-125, 71), (-120, 49), (-124, 42), (-117, 33), (-110, 29), (-105, 22), (-97, 16), (-94, 17), (-86, 12), (-83, 9), (-79, 9), (-81, 25), (-76, 35), (-74, 40), (-70, 42), (-66, 45), (-60, 47), (-55, 52), (-65, 60), (-78, 62), (-85, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)],
        [(-58, 64), (-52, 70), (-40, 76), (-25, 76), (-20, 70), (-30, 66), (-45, 60)],
        [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -50), (-66, -55), (-68, -52), (-62, -45), (-57, -38), (-52, -33), (-48, -28), (-41, -23), (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-77, 10)],
        [(-17, 15), (-16, 20), (-10, 31), (-5, 35), (10, 37), (20, 32), (30, 31), (32, 31), (35, 28), (37, 22), (39, 18), (43, 12), (48, 11), (51, 10), (44, 5), (41, 0), (40, -5), (38, -10), (35, -18), (32, -26), (28, -33), (20, -35), (17, -32), (14, -22), (12, -17), (13, -12), (9, -1), (9, 4), (-8, 5), (-13, 8), (-17, 12)],
        [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-2, 48), (-4, 49), (0, 51), (3, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70), (15, 70), (12, 66), (10, 62), (5, 60), (5, 58), (8, 55), (10, 54), (13, 54), (19, 54), (23, 54), (24, 52), (28, 48), (23, 45), (19, 42), (16, 40), (12, 42), (8, 39), (3, 38), (0, 38), (-2, 37), (-6, 36)],
        [(30, 62), (40, 68), (55, 69), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70), (160, 66), (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (156, 50), (142, 45), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38), (120, 32), (115, 25), (110, 20), (108, 12), (105, 9), (100, 8), (98, 12), (94, 17), (91, 22), (88, 22), (85, 19), (80, 15), (77, 8), (75, 12), (70, 20), (66, 25), (61, 25), (57, 26), (54, 26), (51, 28), (50, 30), (48, 30), (44, 29), (42, 27), (39, 21), (39, 18), (35, 28), (35, 31), (30, 36), (28, 41), (27, 45), (28, 48), (30, 52), (32, 58), (35, 62), (40, 65)],
        [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    ]
    for poly in continents:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND)

    # pins: (num, lon, lat, dx, dy) — nudges keep US/Europe pins from stacking
    pins = [
        (1, 127, 37.5, 6, 2), (2, -59.6, 13.1, 0, 0), (3, 116.4, 39.9, -6, -2),
        (4, -77, 38.9, 0, 8), (5, -74, 40.7, 0, -10), (6, 51.4, 35.7, 0, 0),
        (7, -87.6, 41.9, 0, -4), (8, -122.4, 37.8, 0, 0), (9, -105, 39.7, 0, 0),
        (10, -97.7, 30.3, 0, 2), (11, 21, 52.2, -5, -5), (12, 30.5, 50.4, 6, 5),
        (13, 37.6, 55.8, 6, -6),
    ]
    pf = F(SANS_B, 8)
    for num, lon, lat, dx, dy in pins:
        px, py = proj(lon, lat)
        px += dx
        py += dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
        tw = d.textlength(str(num), font=pf)
        d.text((px - tw / 2, py - 5), str(num), font=pf, fill=(255, 255, 255))
    legend = ("Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 4 Washington \u00b7 5 New York \u00b7 6 Tehran \u00b7 "
              "7 Chicago \u00b7 8 San Francisco \u00b7 9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 Kyiv \u00b7 13 Moscow")
    text_block(d, map_x, map_y + map_h + 4, legend, F(SANS, 9), GRAY, map_w, 11, max_lines=2)

    # ALSO list, two columns
    also = [
        "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
        "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
        "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
        "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
        "22. Iran war: no deal in sight", "23. Lebanon seizes 264 kg explosives",
        "24. Bahrain: strike hits plant, 2 hurt", "25. Sudan: defences down drones",
        "26. DRC: fighting traps Ebola teams", "27. Bangladesh: Hasina jailed if returns",
        "28. Seoul minister quits over exam chaos", "29. SK Telecom \u22127.3% as hype cools",
        "30. China eases margin rules", "31. Seoul readies 10T-won fund",
    ]
    af = F(SANS, 11)
    for i, item in enumerate(also):
        col = i // 9
        row = i % 9
        ax = 530 + col * 242
        ay = my + 20 + row * 22
        d.text((ax, ay), item, font=af, fill=INK)

    # ---------- DATE CHECK ----------
    dy = 836
    d.rectangle([M, dy, W - M, dy + 84], outline=RED, width=2)
    d.text((M + 8, dy + 6), "DATE CHECK", font=F(SANS_B, 13), fill=RED)
    d.text((M + 118, dy + 8), "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY",
           font=F(SANS_B, 10), fill=INK)
    left_out = ("LEFT OUT \u2014 NOT 23 NOV: Democrats reach 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 "
                "El Chapo Isidro captured (22 Nov) \u00b7 EU\u2013Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)")
    text_block(d, M + 8, dy + 26, left_out, F(SANS, 10), INK, CW - 16, 13, max_lines=2)
    d.text((M + 8, dy + 56), "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
           font=F(SANS, 10), fill=INK)

    # ---------- footer ----------
    d.text((M, 928), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
           font=F(SANS, 9), fill=GRAY)
    d.text((M, 942), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently confirmed \u00b7 ONGOING = still developing",
           font=F(SANS, 9), fill=GRAY)
    d.text((M, 956), "Scenes are drawn illustrations, not photographs.  \u00b7  THE WORLD TODAY \u2014 Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
           font=F(SANS_B, 10), fill=INK)
    d.rectangle([0, 972, W, H], fill=(0, 0, 0))
    band = "THE WORLD TODAY \u2014 MONDAY 23 NOVEMBER 2026 \u00b7 31 STORIES"
    bf = F(SANS_B, 13)
    d.text(((W - d.textlength(band, font=bf)) / 2, 992), band, font=bf, fill=(255, 214, 60))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
