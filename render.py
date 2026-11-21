#!/usr/bin/env python3
"""The Friday Edition - V7. Draws entry.png (1024x1024) for make.fun
news-image-20261120: one day of world news, Friday 20 November 2026.

V7 angle - "One lead, drawn deep": a single dominant Kyiv lead story with a
layered night cityscape (sky, skyline, river, bridges, missile trails,
fires), two supporting heroes, and ten mids that are each a real mini-scene
with sky + ground + subject - no flat icon boxes. The bottom half is roomy:
a wide map with pins spread across every continent and the 22 briefs in two
balanced one-line columns. Region counts honestly sum to 35.

Same 35 verified facts as V6. No new stories invented. Mercury's orbit
capture (Saturday) and GTA VI's midnight launch (Thursday) stay in the
DATE CHECK only, never as Friday news.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

PAPER = (246, 241, 228)
INK = (25, 25, 25)
RED = (163, 30, 34)
DARKRED = (120, 20, 24)
NAVY = (16, 28, 52)
NAVY2 = (29, 53, 87)
CREAM2 = (232, 222, 198)
TAN = (217, 201, 163)
GREY = (90, 90, 88)
LIGHTGREY = (140, 135, 125)
WHITE = (250, 248, 242)
GOLD = (198, 152, 40)

NOTO = "/usr/share/fonts/truetype/noto"
DJV = "/usr/share/fonts/truetype/dejavu"
LIB = "/usr/share/fonts/truetype/liberation"


def F(path, size):
    return ImageFont.truetype(path, size)


BLACK = lambda s: F(f"{NOTO}/NotoSerifDisplay-Black.ttf", s)
BOLD = lambda s: F(f"{NOTO}/NotoSerifDisplay-Bold.ttf", s)
SERIF = lambda s: F(f"{NOTO}/NotoSerifDisplay-Regular.ttf", s)
ITAL = lambda s: F(f"{NOTO}/NotoSerifDisplay-Italic.ttf", s)
SANS = lambda s: F(f"{LIB}/LiberationSans-Regular.ttf", s)
SANSB = lambda s: F(f"{LIB}/LiberationSans-Bold.ttf", s)

random.seed(7)
WARN = []


def warn(msg):
    WARN.append(msg)
    print("WARN:", msg, file=sys.stderr)


def wrap(d, text, font, maxw):
    """Word-wrap text to lines fitting maxw. Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_line(d, text, font, maxw):
    """Single line; returns the text or warns if it cannot fit."""
    if d.textlength(text, font=font) <= maxw:
        return text
    warn(f"line too long ({d.textlength(text, font=font):.0f} > {maxw}): {text!r}")
    return text


def vgrad(d, box, c1, c2):
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        c = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def stars(d, box, n=40, bright=255):
    x0, y0, x1, y1 = box
    for _ in range(n):
        x = random.randint(x0 + 2, x1 - 2)
        y = random.randint(y0 + 2, y1 - 2)
        r = random.choice([1, 1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(bright, bright, 220))


def flame(d, x, y, r):
    d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=(230, 120, 30))
    d.ellipse([x - r * 0.6, y - r * 0.4, x + r * 0.6, y + r * 0.6],
              fill=(250, 190, 60))
    d.ellipse([x - r * 0.3, y - r * 0.1, x + r * 0.3, y + r * 0.4],
              fill=(255, 235, 150))


def missile_arc(d, x0, y0, x1, y1, lift):
    """Dotted arc from (x0,y0) to (x1,y1) bowing upward by lift px."""
    steps = 26
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t - lift * 4 * t * (1 - t)
        pts.append((x, y))
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=(255, 220, 130), width=2)
    hx, hy = pts[-1]
    d.ellipse([hx - 4, hy - 4, hx + 4, hy + 4], fill=(255, 200, 80))
    d.ellipse([hx - 2, hy - 2, hx + 2, hy + 2], fill=(255, 240, 180))


def skyline(d, x0, base, x1, hmin, hmax, color, lit=True):
    """Row of buildings with lit windows, tops below base."""
    x = x0
    while x < x1:
        bw = random.randint(14, 30)
        bh = random.randint(hmin, hmax)
        d.rectangle([x, base - bh, min(x + bw, x1), base], fill=color)
        if lit:
            for wy in range(base - bh + 4, base - 3, 7):
                for wx in range(x + 3, min(x + bw, x1) - 3, 7):
                    if random.random() < 0.45:
                        d.rectangle([wx, wy, wx + 2, wy + 3],
                                    fill=(255, 214, 120))
        x += bw + random.randint(1, 4)


def bridge(d, x0, y, w, deck_y, color=(240, 235, 220)):
    """Arch bridge: deck line, arc below, two pillars."""
    d.line([(x0, deck_y), (x0 + w, deck_y)], fill=color, width=3)
    d.arc([x0 + 4, deck_y - 14, x0 + w - 4, deck_y + 14], 180, 360,
          fill=color, width=3)
    d.line([(x0 + 6, deck_y), (x0 + 6, y)], fill=color, width=2)
    d.line([(x0 + w - 6, deck_y), (x0 + w - 6, y)], fill=color, width=2)


def cyclone_spiral(d, cx, cy, r, color=(255, 255, 255)):
    for k in range(5):
        rr = r * (0.25 + 0.19 * k)
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 200 + 55 * k,
              200 + 55 * k + 250, fill=color, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(200, 40, 40))


def chart_fall(d, box, vals, color=(230, 70, 60)):
    x0, y0, x1, y1 = box
    lo, hi = min(vals), max(vals)
    pts = []
    for i, v in enumerate(vals):
        x = x0 + (x1 - x0) * i / (len(vals) - 1)
        y = y1 - (y1 - y0) * (v - lo) / (hi - lo + 1e-9)
        pts.append((x, y))
    d.line(pts, fill=color, width=3, joint="curve")
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4,
               pts[-1][1] + 4], fill=color)


def tag(d, x, y, text, font, bg=RED, fg=WHITE):
    tw = d.textlength(text, font=font)
    d.rectangle([x, y, x + tw + 10, y + font.size + 6], fill=bg)
    d.text((x + 5, y + 3), text, font=font, fill=fg)
    return tw + 10


def pin(d, x, y, n, font):
    r = 8
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED,
              outline=WHITE, width=1)
    t = str(n)
    tw = d.textlength(t, font=font)
    d.text((x - tw / 2, y - font.size / 2 - 1), t, font=font, fill=WHITE)

# ---------------------------------------------------------------- scenes
def scene_kyiv(d, box):
    """Dominant lead: Kyiv at night - sky, skyline, river, three bridges,
    missile trails arcing in, fires burning. Layered, not abstract."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (12, 20, 44), (30, 52, 92))
    stars(d, (x0, y0, x1, y0 + 60), 46)
    # moon glow, top right
    d.ellipse([x1 - 62, y0 + 10, x1 - 34, y0 + 38], fill=(235, 230, 210))
    d.ellipse([x1 - 58, y0 + 14, x1 - 38, y0 + 34], fill=(250, 246, 225))
    # far skyline
    skyline(d, x0 + 6, y1 - 34, x1 - 6, 26, 52, (10, 16, 36), lit=True)
    # river band
    d.rectangle([x0, y1 - 34, x1, y1], fill=(18, 38, 74))
    for rx in range(x0 + 10, x1 - 10, 34):
        d.line([(rx, y1 - 22), (rx + 16, y1 - 22)], fill=(120, 150, 200),
               width=2)
        d.line([(rx + 8, y1 - 12), (rx + 22, y1 - 12)], fill=(90, 120, 175),
               width=2)
    # three bridges over the river
    bw = (x1 - x0 - 60) // 3
    for i in range(3):
        bx = x0 + 20 + i * (bw + 10)
        bridge(d, bx, y1, bw - 8, y1 - 34)
    # missile trails arcing down onto the city
    missile_arc(d, x0 + 120, y0 + 8, x0 + 260, y1 - 70, 26)
    missile_arc(d, x0 + 430, y0 + 4, x0 + 560, y1 - 62, 34)
    missile_arc(d, x0 + 700, y0 + 10, x0 + 820, y1 - 66, 22)
    # fires on the bridges and in the city
    flame(d, x0 + 150, y1 - 36, 9)
    flame(d, x0 + 480, y1 - 40, 7)
    flame(d, x0 + 830, y1 - 38, 8)
    # labels
    tag(d, x0 + 8, y0 + 8, "KYIV", SANSB(13))
    tag(d, x0 + 8, y1 - 26, "3 bridges hit", SANSB(12))


def scene_cyclone(d, box):
    """Cyclone Akvan: Odisha coast on the left, Bay of Bengal with a
    spiral storm and the landfall track on the right."""
    x0, y0, x1, y1 = box
    # land (left third)
    d.rectangle([x0, y0, x0 + (x1 - x0) // 3, y1], fill=(216, 196, 150))
    d.polygon([(x0, y0), (x0 + 120, y0), (x0 + 96, y1),
               (x0, y1)], fill=(206, 184, 138))
    d.text((x0 + 8, y0 + 8), "ODISHA", font=SANSB(11), fill=(90, 60, 20))
    d.text((x0 + 8, y0 + 22), "GOPALPUR", font=SANSB(10), fill=(90, 60, 20))
    d.ellipse([x0 + 96, y0 + 52, x0 + 104, y0 + 60], fill=RED)
    # sea (right two thirds)
    d.rectangle([x0 + (x1 - x0) // 3, y0, x1, y1], fill=(52, 110, 158))
    d.text((x0 + (x1 - x0) // 3 + 8, y0 + 6), "BAY OF BENGAL",
           font=SANSB(9), fill=(210, 225, 240))
    cx, cy = x0 + (x1 - x0) * 2 // 3, y0 + (y1 - y0) // 2 + 4
    # dashed track from the sea to landfall
    for i in range(0, 12):
        t0, t1 = i / 12, (i + 0.5) / 12
        d.line([(cx + 120 - 120 * t0, cy - 26 + 34 * t0),
                (cx + 120 - 120 * t1, cy - 26 + 34 * t1)],
               fill=(255, 255, 255), width=2)
    cyclone_spiral(d, cx, cy, 30)
    # rain slashes
    for rx in range(x0 + 130, x1 - 8, 22):
        d.line([(rx, y0 + 12), (rx - 5, y0 + 24)], fill=(200, 220, 240),
               width=2)
    tag(d, x1 - 118, y1 - 24, "Landfall  7:30 am", SANSB(11))


def scene_markets(d, box):
    """AI sell-off: dark chart panel, red falling line, index table."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(14, 22, 44))
    chart_fall(d, (x0 + 12, y0 + 12, x0 + 250, y1 - 14),
               [96, 88, 90, 74, 78, 62, 55, 40, 46, 30])
    rows = [("TAIEX", "-6.2%"), ("NIKKEI", "-5.1%"),
            ("KOSPI", "-5.2%"), ("HANG SENG", "-1.9%")]
    f1, f2 = SANSB(11), SANSB(11)
    ry = y0 + 8
    for name, val in rows:
        d.text((x0 + 268, ry), name, font=f1, fill=(220, 225, 235))
        vw = d.textlength(val, font=f2)
        d.text((x1 - 10 - vw, ry), val, font=f2, fill=(235, 90, 80))
        ry += 14
    tag(d, x0 + 8, y1 - 24, "Asia, Friday's close", SANSB(11))


def scene_ukeu(d, box):
    """UK and EU flags waving on poles against a pale sky."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (168, 196, 224), (220, 228, 238))
    d.rectangle([x0, y1 - 12, x1, y1], fill=(120, 140, 110))
    # Union Jack (simplified): blue field, white + red crosses
    fx, fy, fw, fh = x0 + 14, y0 + 8, 62, 28
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(18, 46, 120))
    d.line([(fx, fy), (fx + fw, fy + fh)], fill=WHITE, width=4)
    d.line([(fx + fw, fy), (fx, fy + fh)], fill=WHITE, width=4)
    d.line([(fx, fy), (fx + fw, fy + fh)], fill=(200, 30, 40), width=2)
    d.line([(fx + fw, fy), (fx, fy + fh)], fill=(200, 30, 40), width=2)
    d.rectangle([fx + fw // 2 - 4, fy, fx + fw // 2 + 4, fy + fh],
                fill=WHITE)
    d.rectangle([fx, fy + fh // 2 - 4, fx + fw, fy + fh // 2 + 4],
                fill=WHITE)
    d.rectangle([fx + fw // 2 - 2, fy, fx + fw // 2 + 2, fy + fh],
                fill=(200, 30, 40))
    d.rectangle([fx, fy + fh // 2 - 2, fx + fw, fy + fh // 2 + 2],
                fill=(200, 30, 40))
    d.line([(fx + 2, fy + fh), (fx + 2, y1 - 12)], fill=(60, 60, 60),
           width=2)
    # EU flag: blue field, ring of gold stars
    ex = x0 + 104
    d.rectangle([ex, fy, ex + 62, fy + fh], fill=(0, 51, 153))
    for k in range(8):
        a = math.pi * 2 * k / 8 - math.pi / 2
        sx = ex + 31 + 11 * math.cos(a)
        sy = fy + 17 + 11 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    d.line([(ex + 2, fy + fh), (ex + 2, y1 - 12)], fill=(60, 60, 60),
           width=2)
    tag(d, x0 + 6, y1 - 20, "Agreed", SANSB(10))


def scene_poland(d, box):
    """A Kh-101 cruise missile over a green Polish field, crater smoke."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (190, 210, 225), (225, 232, 238))
    d.rectangle([x0, y1 - 22, x1, y1], fill=(110, 150, 90))
    d.polygon([(x0, y1 - 22), (x0 + 60, y1 - 34), (x0 + 130, y1 - 22)],
              fill=(90, 130, 75))
    # missile body, angled down
    mx, my = x0 + 34, y0 + 26
    d.polygon([(mx, my), (mx + 96, my + 16), (mx + 104, my + 22),
               (mx + 96, my + 28), (mx, my + 12)], fill=(180, 185, 190))
    d.polygon([(mx + 96, my + 16), (mx + 112, my + 12), (mx + 112, my + 26),
               (mx + 96, my + 28)], fill=(200, 40, 40))
    d.polygon([(mx + 30, my + 12), (mx + 44, my + 26), (mx + 52, my + 24),
               (mx + 40, my + 10)], fill=(120, 125, 130))
    # exhaust + crater smoke
    d.ellipse([mx - 14, my - 2, mx + 2, my + 14], fill=(220, 220, 220))
    d.ellipse([x0 + 130, y1 - 44, x0 + 150, y1 - 24],
              fill=(200, 200, 200))
    d.ellipse([x0 + 138, y1 - 50, x0 + 154, y1 - 32],
              fill=(225, 225, 225))
    tag(d, x1 - 84, y0 + 6, "Kh-101 down", SANSB(10))


def scene_cop31(d, box):
    """COP31: globe, red thermometer, clock - the last day, no deal."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (200, 220, 235), (235, 240, 245))
    cx, cy, r = x0 + 46, y0 + 30, 22
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 120, 190))
    d.ellipse([cx - 13, cy - 16, cx + 1, cy - 2], fill=(90, 170, 110))
    d.ellipse([cx + 3, cy + 5, cx + 16, cy + 18], fill=(90, 170, 110))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 60, 110),
              width=2)
    # thermometer
    tx = x0 + 108
    d.rectangle([tx, y0 + 8, tx + 12, y0 + 40], fill=WHITE,
                outline=(120, 120, 120))
    d.rectangle([tx + 2, y0 + 24, tx + 10, y0 + 38], fill=(200, 40, 40))
    d.ellipse([tx - 3, y0 + 38, tx + 15, y0 + 54], fill=(200, 40, 40))
    # clock
    kx, ky, kr = x0 + 158, y0 + 26, 13
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=WHITE,
              outline=(60, 60, 60), width=2)
    d.line([(kx, ky), (kx, ky - 8)], fill=INK, width=2)
    d.line([(kx, ky), (kx + 6, ky + 3)], fill=INK, width=2)
    tag(d, x1 - 58, y1 - 20, "Last day", SANSB(10))


def scene_iraq(d, box):
    """Iraqi army: desert sky, sand, two tanks, a palm."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (240, 220, 170), (245, 232, 195))
    d.rectangle([x0, y1 - 24, x1, y1], fill=(214, 186, 130))
    # palm
    px = x0 + 168
    d.line([(px, y1 - 24), (px, y0 + 22)], fill=(110, 80, 40), width=4)
    for a in range(-50, 51, 25):
        d.line([(px, y0 + 22), (px + int(16 * math.sin(math.radians(a))),
                 y0 + 22 + int(12 * math.cos(math.radians(a))))],
               fill=(70, 130, 70), width=3)
    # tanks
    for tx in (x0 + 16, x0 + 76):
        d.rectangle([tx, y1 - 40, tx + 52, y1 - 26], fill=(70, 72, 60))
        d.rectangle([tx + 12, y1 - 50, tx + 36, y1 - 40],
                    fill=(80, 82, 68))
        d.line([(tx + 36, y1 - 46), (tx + 56, y1 - 48)], fill=(60, 62, 52),
               width=3)
        for wx in range(tx + 4, tx + 50, 10):
            d.ellipse([wx, y1 - 26, wx + 7, y1 - 19], fill=(40, 40, 34))
    tag(d, x0 + 6, y0 + 6, "Jurf al-Sakhar", SANSB(10))


def scene_bukele(d, box):
    """Bukele's third-term bid: a desk, a ballot box, a flag, the date."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (200, 214, 232), (232, 238, 244))
    # wall + desk
    d.rectangle([x0, y1 - 18, x1, y1], fill=(150, 110, 70))
    # small flag on the wall
    d.rectangle([x0 + 132, y0 + 10, x0 + 172, y0 + 34], fill=(0, 71, 171))
    d.rectangle([x0 + 132, y0 + 10, x0 + 172, y0 + 18], fill=WHITE)
    # ballot box on the desk
    bx, by = x0 + 48, y0 + 22
    d.rectangle([bx, by, bx + 72, by + 34], fill=(250, 248, 242),
                outline=(60, 60, 60), width=2)
    d.line([(bx + 22, by + 2), (bx + 50, by + 2)], fill=INK, width=3)
    d.line([(bx + 26, by + 10), (bx + 34, by + 20)], fill=(30, 140, 70),
           width=4)
    d.line([(bx + 34, by + 20), (bx + 52, by + 6)], fill=(30, 140, 70),
           width=4)
    d.text((bx + 6, by + 22), "VOTE", font=SANSB(10), fill=(60, 60, 60))
    tag(d, x0 + 6, y0 + 6, "Vote 28 Feb 2027", SANSB(10))


def scene_italy(d, box):
    """General strike in Rome: street, buildings, a marching crowd with
    banners under a SCIOPERO bar."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (210, 205, 190), (235, 228, 210))
    # buildings
    d.rectangle([x0 + 8, y0 + 14, x0 + 52, y1 - 26], fill=(180, 150, 110))
    d.rectangle([x0 + 140, y0 + 8, x0 + 188, y1 - 26], fill=(160, 130, 95))
    for wy in range(y0 + 20, y1 - 30, 12):
        d.rectangle([x0 + 16, wy, x0 + 24, wy + 7], fill=(90, 70, 50))
        d.rectangle([x0 + 148, wy, x0 + 156, wy + 7], fill=(80, 60, 42))
    # street
    d.rectangle([x0, y1 - 26, x1, y1], fill=(150, 140, 125))
    # crowd: heads + bodies + one banner
    for i, cx in enumerate(range(x0 + 22, x1 - 14, 26)):
        c = (40, 40, 44) if i % 2 == 0 else (120, 30, 34)
        d.ellipse([cx - 5, y1 - 46, cx + 5, y1 - 36], fill=(60, 45, 35))
        d.rectangle([cx - 6, y1 - 36, cx + 6, y1 - 24], fill=c)
    d.rectangle([x0 + 62, y0 + 44, x0 + 128, y0 + 56], fill=WHITE,
                outline=(60, 60, 60))
    d.text((x0 + 70, y0 + 46), "SCIOPERO", font=SANSB(9), fill=RED)
    tag(d, x0 + 6, y0 + 6, "26 bn budget", SANSB(10))


def scene_japan(d, box):
    """Japan inflation: red sun over a Tokyo skyline, bar chart rising."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (238, 228, 210), (245, 240, 225))
    # red sun
    d.ellipse([x0 + 130, y0 + 8, x0 + 162, y0 + 40], fill=(200, 40, 40))
    # skyline silhouette
    base = y1 - 20
    for i, (bx, bh) in enumerate([(8, 26), (34, 38), (62, 30), (92, 44),
                                  (122, 34)]):
        d.rectangle([x0 + bx, base - bh, x0 + bx + 24, base],
                    fill=(70, 70, 78))
    d.rectangle([x0, base, x1, y1], fill=(200, 195, 180))
    # rising bars
    bars = [10, 16, 22, 30]
    for i, bh in enumerate(bars):
        bx = x0 + 14 + i * 16
        d.rectangle([bx, y1 - 8 - bh, bx + 11, y1 - 8], fill=(180, 40, 40))
    tag(d, x1 - 64, y1 - 20, "+2.3% Oct", SANSB(10))


def scene_phillips(d, box):
    """Phillips 118: green pitch, crease lines, batsman, ball, stumps."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (150, 190, 110), (120, 165, 90))
    d.rectangle([x0, y1 - 14, x1, y1], fill=(90, 130, 70))
    # pitch strip
    d.rectangle([x0 + 70, y0 + 8, x0 + 126, y1 - 14], fill=(210, 190, 140))
    d.line([(x0 + 70, y0 + 20), (x0 + 126, y0 + 20)], fill=WHITE, width=2)
    d.line([(x0 + 70, y1 - 26), (x0 + 126, y1 - 26)], fill=WHITE, width=2)
    # stumps
    for sx in (x0 + 118, x0 + 122, x0 + 126):
        d.line([(sx, y0 + 12), (sx, y0 + 22)], fill=(240, 210, 120),
               width=2)
    # batsman: head, body, bat
    bx = x0 + 96
    d.ellipse([bx - 5, y0 + 30, bx + 5, y0 + 40], fill=(60, 45, 35))
    d.line([(bx, y0 + 40), (bx, y0 + 58)], fill=(30, 30, 34), width=5)
    d.line([(bx, y0 + 58), (bx - 8, y1 - 18)], fill=(30, 30, 34), width=3)
    d.line([(bx, y0 + 58), (bx + 8, y1 - 18)], fill=(30, 30, 34), width=3)
    d.line([(bx + 2, y0 + 46), (bx + 16, y0 + 62)], fill=(200, 170, 110),
           width=4)
    # red ball
    d.ellipse([x0 + 150, y0 + 52, x0 + 158, y0 + 60], fill=(200, 40, 40))
    tag(d, x0 + 6, y1 - 20, "118 off 125", SANSB(10))


def scene_rohingya(d, box):
    """Rohingya camps: hills, rows of tents, a pale sky."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (205, 222, 235), (235, 240, 242))
    d.polygon([(x0, y1 - 30), (x0 + 70, y1 - 52), (x0 + 140, y1 - 30)],
              fill=(140, 170, 110))
    d.polygon([(x0 + 90, y1 - 30), (x0 + 160, y1 - 48),
               (x1, y1 - 30)], fill=(120, 150, 95))
    d.rectangle([x0, y1 - 30, x1, y1], fill=(190, 170, 130))
    # tents
    for i, tx in enumerate(range(x0 + 12, x1 - 20, 34)):
        c = (245, 240, 225) if i % 2 == 0 else (210, 195, 160)
        d.polygon([(tx, y1 - 14), (tx + 12, y1 - 34), (tx + 24, y1 - 14)],
                  fill=c, outline=(120, 100, 70))
    tag(d, x0 + 6, y0 + 6, "Cox's Bazar", SANSB(10))


def scene_malawi(d, box):
    """Malawi fuel crisis: a road, a queue of cars, a red pump, 20L."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (215, 225, 235), (238, 240, 242))
    d.rectangle([x0, y1 - 26, x1, y1], fill=(120, 118, 110))
    d.line([(x0, y1 - 13), (x1, y1 - 13)], fill=(250, 250, 240), width=2)
    # fuel pump
    px = x0 + 150
    d.rectangle([px, y0 + 18, px + 26, y0 + 52], fill=(200, 40, 40))
    d.rectangle([px + 5, y0 + 24, px + 21, y0 + 36], fill=WHITE)
    d.text((px + 7, y0 + 26), "20L", font=SANSB(9), fill=RED)
    d.line([(px + 26, y0 + 30), (px + 36, y0 + 44)], fill=INK, width=2)
    # queued cars
    for i, cx in enumerate((x0 + 12, x0 + 52, x0 + 92)):
        c = (40, 80, 140) if i % 2 == 0 else (140, 60, 50)
        d.rectangle([cx, y1 - 44, cx + 32, y1 - 32], fill=c)
        d.rectangle([cx + 6, y1 - 52, cx + 24, y1 - 44], fill=(30, 30, 34))
        d.ellipse([cx + 4, y1 - 32, cx + 11, y1 - 25], fill=(20, 20, 20))
        d.ellipse([cx + 21, y1 - 32, cx + 28, y1 - 25], fill=(20, 20, 20))
    tag(d, x0 + 6, y1 - 20, "20 litres a day", SANSB(10))

# ---------------------------------------------------------------- layout
REGIONS = [("EUROPE", 7, (31, 78, 121)), ("ASIA", 10, (163, 30, 34)),
           ("MIDDLE EAST", 4, (138, 109, 27)), ("AFRICA", 3, (46, 125, 50)),
           ("AMERICAS", 4, (106, 61, 154)), ("OCEANIA", 1, (0, 119, 182)),
           ("GLOBAL", 6, (85, 85, 85))]

STATS = [("3", "bridges hit\nin Kyiv"), ("300,000+", "evacuated\nbefore Akvan"),
         ("-6.2%", "Taiex, Friday's\nclose"), ("0", "deaths as Akvan\ncame ashore"),
         ("2.3%", "Japan consumer\ninflation, Oct"),
         ("118", "runs by Glenn Phillips\nagainst India")]

# (lat, lon) for the 13 drawn stories, in story order
PINS = [(50.45, 30.52), (19.26, 84.92), (25.03, 121.56), (50.85, 4.35),
        (52.0, 19.0), (36.90, 30.70), (33.31, 44.36), (13.69, -89.22),
        (41.90, 12.50), (35.68, 139.69), (-41.29, 174.78), (21.44, 92.00),
        (-15.79, 35.00)]

BRIEFS = [
    (14, "Kenya", "Oil rig starts; first crude due 1 Dec", "Business Daily"),
    (15, "China", "Loan rates held for an 18th month", "Xinhua"),
    (16, "Senegal", "Migrant boat capsizes; 4 dead", "Al Jazeera"),
    (17, "Las Vegas", "Russell fastest in wet GP practice",
     "formula1.com"),
    (18, "Health", "Cancer pill: tumours shrank 60.7%", "Reuters"),
    (19, "Seoul", "Ruling party moves to impeach top judge", "Yonhap"),
    (20, "Brent", "Brent $92.60 as Hormuz fears rise", "Reuters"),
    (21, "Riyadh", "Coalition says Houthi missiles intercepted", "Reuters"),
    (22, "Hormuz", "Iran claims two tankers hit mines", "CLAIM"),
    (23, "Health", "Erasca drug: 44% of patients respond", "Reuters"),
    (24, "F1", "Antonelli confirmed youngest champion", "FIA"),
    (25, "Lviv", "A strike on a railway station kills two", "BBC"),
    (26, "World", "Youth protests spread to five countries", "Reuters"),
    (27, "US", "900,000 advanced chips approved for China", "WSJ"),
    (28, "Odisha", "423 rescue teams, 9,341 shelters ready", "NDTV"),
    (29, "Tokyo", "SoftBank shares fall more than 14.6%", "Reuters"),
    (30, "COP31", "COP31 keeps its \u201c35 by 35\u201d goal", "Carbon Brief"),
    (31, "EU", "EU calls the COP31 draft \u201cnot acceptable\u201d", "AFP"),
    (32, "California", "Nvidia subpoenaed over chips to China",
     "Reuters"),
    (33, "Seoul", "Suneung: 111 caught cheating in exams", "Yonhap"),
    (34, "Odisha", "Patrapur sees 209 mm of rain as Akvan crosses",
     "PTI"),
    (35, "Poland", "F-16s scrambled; Rzeszow shut", "Ukrainska Pravda"),
]


def draw_map(d, box):
    """Simplified world map in tan on cream, with numbered pins."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(238, 232, 214))
    # rough continent blobs (equirectangular-ish, stylised)
    land = (217, 201, 163)
    # North America
    d.polygon([(x0 + 18, y0 + 22), (x0 + 78, y0 + 12), (x0 + 96, y0 + 34),
               (x0 + 66, y0 + 52), (x0 + 40, y0 + 58), (x0 + 14, y0 + 40)],
              fill=land)
    # South America
    d.polygon([(x0 + 62, y0 + 78), (x0 + 92, y0 + 74), (x0 + 96, y0 + 104),
               (x0 + 80, y0 + 138), (x0 + 66, y0 + 108)], fill=land)
    # Europe
    d.polygon([(x0 + 150, y0 + 18), (x0 + 182, y0 + 12), (x0 + 192, y0 + 30),
               (x0 + 176, y0 + 44), (x0 + 152, y0 + 38)], fill=land)
    # Africa
    d.polygon([(x0 + 152, y0 + 58), (x0 + 192, y0 + 54), (x0 + 198, y0 + 86),
               (x0 + 182, y0 + 118), (x0 + 162, y0 + 100),
               (x0 + 150, y0 + 76)], fill=land)
    # Asia
    d.polygon([(x0 + 196, y0 + 10), (x0 + 300, y0 + 8), (x0 + 316, y0 + 34),
               (x0 + 296, y0 + 62), (x0 + 250, y0 + 66), (x0 + 214, y0 + 52),
               (x0 + 196, y0 + 30)], fill=land)
    # SE Asia islands + Australia
    d.polygon([(x0 + 268, y0 + 74), (x0 + 292, y0 + 70), (x0 + 296, y0 + 84),
               (x0 + 274, y0 + 88)], fill=land)
    d.polygon([(x0 + 278, y0 + 118), (x0 + 312, y0 + 114),
               (x0 + 316, y0 + 134), (x0 + 288, y0 + 140),
               (x0 + 274, y0 + 128)], fill=land)
    # pins from lat/lon
    pf = SANSB(9)
    for i, (lat, lon) in enumerate(PINS, start=1):
        px = x0 + (lon + 180) / 360 * (x1 - x0)
        py = y0 + (90 - lat) / 180 * (y1 - y0)
        # nudge the two Europe pins that would collide (Kyiv/Poland)
        if i == 5:
            px, py = px + 7, py - 7
        if i == 1:
            px, py = px - 6, py + 6
        pin(d, int(px), int(py), i, pf)


def story_caption(d, x, y, w, num, place, field, headline, body,
                  hl_size=20, body_size=12, max_hl=2, max_body=2):
    """Numbered dateline + headline + body. Returns bottom y."""
    fnum = SANSB(11)
    d.text((x, y), f"{num}", font=fnum, fill=RED)
    nw = d.textlength(f"{num}  ", font=fnum)
    d.text((x + nw, y), f"{place}  \u00b7  {field}", font=SANSB(10),
           fill=RED)
    y += 15
    hl = wrap(d, headline, BOLD(hl_size), w)
    if len(hl) > max_hl:
        warn(f"headline wraps to {len(hl)} lines: {headline!r}")
        hl = hl[:max_hl]
    for line in hl:
        d.text((x, y), line, font=BOLD(hl_size), fill=INK)
        y += hl_size + 3
    bl = wrap(d, body, SERIF(body_size), w)
    if len(bl) > max_body:
        warn(f"body wraps to {len(bl)} lines: {body!r}")
        bl = bl[:max_body]
    for line in bl:
        d.text((x, y), line, font=SERIF(body_size), fill=INK)
        y += body_size + 3
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 8                      # outer margin
    X1 = W - M
    y = 6
    # ---- kicker
    d.text((M, y), "THE WORLD IN ONE DAY", font=SANSB(11), fill=RED)
    rt = "35 STORIES  \u00b7  7 REGIONS  \u00b7  EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    d.text((X1 - d.textlength(rt, font=SANSB(11)), y), rt, font=SANSB(11),
           fill=INK)
    y += 17
    d.line([(M, y), (X1, y)], fill=INK, width=2)
    y += 4
    # ---- masthead
    mast = "Friday 20 November 2026"
    mf = BLACK(58)
    d.text(((W - d.textlength(mast, font=mf)) / 2, y), mast, font=mf,
           fill=INK)
    y += 62
    # ---- deck
    deck = ("Russian missiles hit Kyiv's bridges  \u00b7  Cyclone Akvan strikes "
            "India  \u00b7  An AI sell-off sinks Asia's markets  \u00b7  "
            "UK and EU seal a deal")
    df = ITAL(15)
    d.text(((W - d.textlength(deck, font=df)) / 2, y), deck, font=df,
           fill=RED)
    y += 20
    d.line([(M, y), (X1, y)], fill=INK, width=2)
    y += 5
    # ---- stat strip: six numbers, red left bars
    colw = (X1 - M) // 6
    for i, (num, lab) in enumerate(STATS):
        cx = M + i * colw
        d.line([(cx, y + 2), (cx, y + 34)], fill=RED, width=3)
        nf = BLACK(24)
        d.text((cx + 8, y), num, font=nf, fill=INK)
        ly = y + 26
        for part in lab.split("\n"):
            d.text((cx + 8, ly), part, font=SANS(10), fill=GREY)
            ly += 11
    y += 48
    # ---- region bar: honest counts, summing to 35.
    # Rects first, labels second, so a narrow segment's label is never
    # covered by the next segment's rectangle.
    total = sum(c for _, c, _ in REGIONS)
    assert total == 35, total
    rx = M
    spans = []
    for name, count, color in REGIONS:
        segw = int((X1 - M) * count / 35)
        d.rectangle([rx, y, rx + segw - 1, y + 16], fill=color)
        spans.append((rx, segw, f"{name} {count}"))
        rx += segw
    lf = SANSB(9)
    for sx, segw, label in spans:
        tw = d.textlength(label, font=lf)
        d.text((sx + (segw - tw) / 2, y + 3), label, font=lf, fill=WHITE)
    y += 18
    # ---- LEAD: Kyiv, full width, one dominant story
    lead_top = y
    scene_kyiv(d, (M, y, X1, y + 114))
    y += 120
    y = story_caption(
        d, M, y, X1 - M, 1, "KYIV, UKRAINE", "WAR",
        "Russian missiles hit three Kyiv bridges",
        "An overnight barrage of 80+ missiles and 400 drones killed 8 and "
        "cut power and water in the capital. Three Dnipro crossings hit. "
        "(Reuters, Kyiv Post)",
        hl_size=25, body_size=12, max_hl=1, max_body=2)
    y += 4
    d.line([(M, y), (X1, y)], fill=GREY, width=1)
    y += 6
    # ---- supporting heroes: cyclone + markets
    hw = (X1 - M - 12) // 2
    hx2 = M + hw + 12
    scene_cyclone(d, (M, y, M + hw, y + 64))
    scene_markets(d, (hx2, y, hx2 + hw, y + 64))
    y += 70
    y1 = story_caption(
        d, M, y, hw, 2, "ODISHA, INDIA", "CYCLONE",
        "Cyclone Akvan comes ashore in eastern India",
        "The storm crossed near Gopalpur; 300,000+ moved to shelters. "
        "No deaths reported. (IMD, NDTV)",
        hl_size=19, body_size=12, max_hl=2, max_body=2)
    y2 = story_caption(
        d, hx2, y, hw, 3, "TAIPEI \u00b7 SEOUL \u00b7 TOKYO", "MARKETS",
        "AI sell-off sinks Asia's stock markets",
        "Taiex fell 6.2% in its worst week since 1991 as chipmakers led "
        "the slide. (Al Jazeera, Reuters)",
        hl_size=19, body_size=12, max_hl=2, max_body=2)
    y = max(y1, y2) + 4
    d.line([(M, y), (X1, y)], fill=GREY, width=1)
    y += 6
    # ---- mids: 10 scenes, two rows of five
    mids = [
        (scene_ukeu, 4, "BRUSSELS", "DIPLOMACY",
         "UK and EU seal a \u201creset\u201d deal",
         "Food trade, youth visas. (Reuters)",
         "Agreed \u00b7 Reuters"),
        (scene_poland, 5, "EASTERN POLAND", "WAR",
         "Russian missile lands in Poland",
         "Jets scrambled. (Ukrainska Pravda)",
         "Minister says \u00b7 Reuters"),
        (scene_cop31, 6, "ANTALYA", "CLIMATE",
         "COP31 reaches its last day with no deal",
         "Draft leaves out fossil fuels. (AFP)",
         "Ongoing \u00b7 UN News"),
        (scene_iraq, 7, "CENTRAL IRAQ", "SECURITY",
         "Iraqi army enters a militia stronghold",
         "Army enters Jurf al-Sakhar. (Reuters)",
         "Witnessed \u00b7 Reuters"),
        (scene_bukele, 8, "SAN SALVADOR", "POLITICS",
         "Bukele files to run for a third term",
         "The vote is on 28 February 2027. (AP)",
         "Filed \u00b7 AP"),
        (scene_italy, 9, "ROME", "LABOUR",
         "General strike over Italy's budget",
         "Workers, students march. (Reuters)",
         "Reported \u00b7 Reuters"),
        (scene_japan, 10, "TOKYO", "ECONOMY",
         "Japan's inflation picks up to 2.3%",
         "Rate rise in view. (Japan Times)",
         "Official data"),
        (scene_phillips, 11, "WELLINGTON", "CRICKET",
         "Phillips hits 118 against India",
         "Hundreds in all three formats. (ICC)",
         "Scorecard \u00b7 ICC"),
        (scene_rohingya, 12, "COX'S BAZAR", "JUSTICE",
         "Rohingya weep and pray after ICJ ruling",
         "Camps react to verdict. (Al Jazeera)",
         "Reported \u00b7 Reuters"),
        (scene_malawi, 13, "BLANTYRE, MALAWI", "FUEL",
         "Malawi fuel crisis: night queues",
         "20 litres a day, queues grow. (AFP)",
         "Reported \u00b7 AFP"),
    ]
    mw = (X1 - M - 4 * 8) // 5
    row_tops = []
    for row in range(2):
        row_tops.append(y)
        for col in range(5):
            fn, num, place, field, hl, body, src = mids[row * 5 + col]
            mx = M + col * (mw + 8)
            fn(d, (mx, y, mx + mw, y + 60))
            d.text((mx, y + 64), f"{num}  {place}  \u00b7  {field}",
                   font=SANSB(9), fill=RED)
            hy = y + 76
            hl_lines = wrap(d, hl, BOLD(13), mw)
            if len(hl_lines) > 2:
                warn(f"mid headline wraps to {len(hl_lines)}: {hl!r}")
                hl_lines = hl_lines[:2]
            for line in hl_lines:
                d.text((mx, hy), line, font=BOLD(13), fill=INK)
                hy += 14
            bl = wrap(d, body, SERIF(11), mw)
            if len(bl) > 1:
                warn(f"mid body wraps to {len(bl)}: {body!r}")
                bl = bl[:1]
            for line in bl:
                d.text((mx, hy), line, font=SERIF(11), fill=INK)
                hy += 12
            d.text((mx, hy), src, font=SANS(9), fill=GREY)
        y += 128
    # ---- map + briefs
    d.text((M, y), "WHERE IT HAPPENED  \u00b7  PINS 1-13", font=SANSB(11),
           fill=RED)
    bt = "ALSO ON FRIDAY 20 NOVEMBER  \u2014  22 MORE STORIES"
    d.text((M + 348, y), bt, font=SANSB(11), fill=RED)
    y += 15
    map_top = y
    draw_map(d, (M, y, M + 330, y + 160))
    # briefs: two balanced columns, one clean line each
    bf = SANS(11)
    col_x = [M + 348, M + 348 + 336]
    col_w = 330
    for i, (num, place, text, src) in enumerate(BRIEFS):
        cx = col_x[i // 11]
        cy = map_top + (i % 11) * 15
        rest = f"{text}  ({src})"
        full_w = (d.textlength(f"{num}  ", font=SANSB(11))
                  + d.textlength(f"{place}  ", font=SANSB(11))
                  + d.textlength(rest, font=bf))
        if full_w > col_w:
            warn(f"brief too long ({full_w:.0f} > {col_w}): {num} {place} {text}")
        d.text((cx, cy), f"{num}", font=SANSB(11), fill=RED)
        nw = d.textlength(f"{num}  ", font=SANSB(11))
        d.text((cx + nw, cy), f"{place}  ", font=SANSB(11), fill=RED)
        pw = d.textlength(f"{place}  ", font=SANSB(11))
        rest = f"{text}  ({src})"
        d.text((cx + nw + pw, cy), rest, font=bf, fill=INK)
    y = map_top + 170
    # ---- DATE CHECK
    d.rectangle([M, y, X1, y + 34], outline=RED, width=2)
    d.text((M + 8, y + 4), "DATE CHECK", font=SANSB(11), fill=RED)
    dc1 = ("LEFT OUT \u2014 first reported Thursday 19 Nov: Anthropic's "
           "$83 IPO & Nasdaq debut \u00b7 Wall Street -2% \u00b7 the ICJ "
           "ruling itself \u00b7 Riyadh tower attack \u00b7 GTA VI midnight "
           "launch.")
    dc2 = ("NOT YET \u2014 BepiColombo Mercury orbit capture (Sat) "
           "\u00b7 COP31 final text \u00b7 ATP Finals final (Sun) "
           "\u00b7 Estonia border closure (1 Dec).")
    for k, line in enumerate((dc1, dc2)):
        lines = wrap(d, line, SANS(10), X1 - M - 96)
        d.text((M + 92, y + 3 + k * 17), lines[0] if lines else "",
               font=SANS(10), fill=INK)
        if len(lines) > 1:
            warn(f"date check line {k} wraps: {line[:40]!r}")
    y += 38
    # ---- footer
    d.text((M, y), "Every story here happened, or was first reported, on "
           "Friday 20 November 2026. Claims are attributed, not stated "
           "as fact.  Sources named beside each story  \u00b7  Original "
           "drawings", font=SANS(10), fill=GREY)
    y += 11
    print(f"final y: {y} / {H}")
    if y > H:
        warn(f"layout overflow: final y {y} > {H}")
    img.save(OUT, "PNG")
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
