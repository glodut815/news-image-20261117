#!/usr/bin/env python3
"""news-image-20261117 — sum up 17 November 2026 world news in one image.

A newspaper front page, 1024x1024: a masthead, one big hero panel (the
Kerch bridge collapse) and six smaller panels. Every panel has a drawn
scene, a bold headline and a one-line caption in large, high-contrast
type — the image must be understandable with no news feed at all.

PIL only. Fully deterministic: no random, no time, fixed palette and
fonts shipped in fonts/. Run twice and the PNG bytes are identical.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(BASE, "fonts")

PAPER = (247, 243, 230)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 90, 90)
RULE = (30, 30, 30)
SKY = (184, 199, 214)
SEA = (47, 109, 179)
DECK = (52, 52, 58)


def bold(size):
    return ImageFont.truetype(os.path.join(FONTS, "DejaVuSans-Bold.ttf"), size)


def regular(size):
    return ImageFont.truetype(os.path.join(FONTS, "DejaVuSans.ttf"), size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, font, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def panel_border(draw, x, y, w, h, width=2):
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=width)


# ---------------------------------------------------------------- scenes
def draw_hero_bridge(draw, x, y, w, h):
    """Kerch bridge: road deck with a collapsed arch gap, sea, smoke."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun haze
    draw.ellipse([x + w - 130, y + 14, x + w - 70, y + 74], fill=(238, 226, 180))
    # sea
    sea_y = y + int(h * 0.62)
    draw.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    for wy in (sea_y + 14, sea_y + 34, sea_y + 54):
        draw.line([x + 20, wy, x + w - 20, wy], fill=(120, 165, 215), width=2)
    draw.text((x + 16, y + h - 28), "KERCH STRAIT", font=regular(17),
              fill=(225, 235, 245))
    deck_y = y + int(h * 0.52)
    # support pillars
    for px in (x + 120, x + 200, x + w - 260, x + w - 140):
        draw.rectangle([px, deck_y + 8, px + 14, sea_y + 40], fill=(70, 70, 78))
    # intact arch (left half) above the deck
    draw.arc([x + 60, deck_y - 92, x + 470, deck_y + 30], 180, 360,
             fill=DECK, width=8)
    draw.arc([x + 560, deck_y - 92, x + w - 60, deck_y + 30], 180, 360,
             fill=DECK, width=8)
    # deck: left and right of the gap, ends tilted down into the water
    gap_l, gap_r = x + 430, x + 560
    draw.rectangle([x, deck_y, gap_l, deck_y + 12], fill=DECK)
    draw.rectangle([gap_r, deck_y, x + w, deck_y + 12], fill=DECK)
    draw.polygon([(gap_l - 6, deck_y), (gap_l + 46, deck_y + 58),
                  (gap_l + 30, deck_y + 66), (gap_l - 16, deck_y + 12)],
                 fill=DECK)
    draw.polygon([(gap_r + 6, deck_y), (gap_r - 46, deck_y + 58),
                  (gap_r - 30, deck_y + 66), (gap_r + 16, deck_y + 12)],
                 fill=DECK)
    # fallen arch piece in the water
    draw.arc([gap_l - 10, sea_y - 6, gap_r + 30, sea_y + 46], 0, 180,
             fill=(90, 90, 100), width=7)
    # explosion + smoke over the gap
    cx, cy = (gap_l + gap_r) // 2, deck_y - 6
    for r, col in ((34, (255, 140, 40)), (22, (255, 200, 60)),
                   (12, (255, 240, 160))):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for sx, sy, r in ((cx - 70, cy - 52, 26), (cx - 30, cy - 74, 32),
                      (cx + 18, cy - 66, 28), (cx + 62, cy - 44, 22)):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 125))
        draw.ellipse([sx - r + 6, sy - r + 6, sx + r - 4, sy + r - 4],
                     fill=(150, 150, 155))


def draw_summit(draw, x, y, w, h):
    """Three flags: US, China, Russia — the Shenzhen trilateral."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 240))
    fw, fh = 74, 46
    tops = [x + 18, x + 122, x + 226]
    pole_y = y + 8
    for i, fx in enumerate(tops):
        draw.rectangle([fx + fw // 2 - 2, pole_y, fx + fw // 2 + 2,
                        y + h - 14], fill=(80, 80, 80))
        fy = pole_y + 2
        if i == 0:  # United States
            for s in range(7):
                col = (178, 34, 52) if s % 2 == 0 else (245, 245, 245)
                draw.rectangle([fx, fy + s * 7, fx + fw, fy + s * 7 + 7],
                               fill=col)
            draw.rectangle([fx, fy, fx + 30, fy + 24], fill=(40, 60, 140))
            for dx in (6, 16, 26):
                for dy in (6, 16):
                    draw.ellipse([fx + dx - 2, fy + dy - 2, fx + dx + 2,
                                  fy + dy + 2], fill=(255, 255, 255))
        elif i == 1:  # China
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
            draw.ellipse([fx + 8, fy + 8, fx + 20, fy + 20],
                         fill=(255, 222, 0))
            for sx, sy in ((30, 8), (42, 14), (44, 26), (34, 32)):
                draw.ellipse([fx + sx - 3, fy + sy - 3, fx + sx + 3,
                              fy + sy + 3], fill=(255, 222, 0))
        else:  # Russia
            for s, col in enumerate(((245, 245, 245), (0, 90, 170),
                                     (210, 30, 30))):
                draw.rectangle([fx, fy + s * 16, fx + fw, fy + s * 16 + 16],
                               fill=col)
    # skyline below the flags
    base = y + h - 14
    for bx, bh in ((0, 12), (52, 20), (110, 14), (168, 24), (226, 16),
                   (272, 22)):
        draw.rectangle([x + bx, base - bh, x + bx + 46, base], fill=(60, 70, 90))


def draw_kyiv(draw, x, y, w, h):
    """City skyline, two bridges, explosions."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 200, 160))
    base = y + h
    for bx, bh, bw in ((0, 46, 40), (44, 66, 34), (82, 52, 44),
                       (130, 74, 36), (170, 56, 42), (216, 68, 34),
                       (254, 48, 40), (292, 60, 26)):
        draw.rectangle([x + bx, base - bh, x + bx + bw, base],
                       fill=(48, 48, 60))
        for wy in range(base - bh + 8, base - 6, 14):
            draw.rectangle([x + bx + 6, wy, x + bx + 12, wy + 7],
                           fill=(240, 210, 120))
    # two bridge arcs
    draw.arc([x + 10, y + 26, x + 150, y + 86], 180, 360, fill=(40, 40, 50),
             width=5)
    draw.arc([x + 170, y + 34, x + w - 10, y + 92], 180, 360,
             fill=(40, 40, 50), width=5)
    # explosions
    for ex, ey in ((x + 84, y + 30), (x + 238, y + 38)):
        for r, col in ((20, (255, 120, 30)), (12, (255, 190, 60)),
                       (6, (255, 240, 150))):
            draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)
        draw.ellipse([ex - 26, ey - 26, ex - 6, ey - 6], fill=(110, 110, 115))
        draw.ellipse([ex + 8, ey - 30, ex + 28, ey - 10], fill=(130, 130, 135))


def draw_measles(draw, x, y, w, h):
    """A virus particle with spikes."""
    draw.rectangle([x, y, x + w, y + h], fill=(245, 235, 220))
    cx, cy = x + w // 2, y + h // 2 + 2
    for k in range(12):
        ang = math.pi * 2 * k / 12
        x1 = cx + int(26 * math.cos(ang))
        y1 = cy + int(26 * math.sin(ang))
        x2 = cx + int(38 * math.cos(ang))
        y2 = cy + int(38 * math.sin(ang))
        draw.line([x1, y1, x2, y2], fill=(128, 60, 140), width=4)
        draw.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=(160, 80, 170))
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(150, 70, 160))
    for dx, dy in ((-10, -8), (10, -10), (0, 8), (-12, 10), (12, 10)):
        draw.ellipse([cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4],
                     fill=(110, 40, 125))
    for dx, dy in ((-58, -22), (56, -26), (-52, 28), (60, 24)):
        draw.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3],
                     fill=(190, 120, 200))


def draw_chip(draw, x, y, w, h):
    """A computer chip on a circuit board."""
    draw.rectangle([x, y, x + w, y + h], fill=(220, 240, 220))
    for tx in range(x + 14, x + w - 10, 26):
        draw.line([tx, y + 6, tx, y + 22], fill=(120, 160, 120), width=2)
        draw.line([tx, y + h - 22, tx, y + h - 6], fill=(120, 160, 120),
                  width=2)
    cx, cy = x + w // 2, y + h // 2
    draw.rectangle([cx - 34, cy - 34, cx + 34, cy + 34], fill=(16, 90, 50))
    for dx in (-46, -34, 34, 46):
        draw.rectangle([cx + dx - 3, cy - 28, cx + dx + 3, cy + 28],
                       fill=(200, 170, 60))
    for dy in (-46, -34, 34, 46):
        draw.rectangle([cx - 28, cy + dy - 3, cx + 28, cy + dy + 3],
                       fill=(200, 170, 60))
    draw.rectangle([cx - 20, cy - 20, cx + 20, cy + 20], fill=(40, 140, 80))
    f = bold(19)
    tw = draw.textlength("NV", font=f)
    draw.text((cx - tw / 2, cy - 13), "NV", font=f, fill=(255, 255, 255))


def draw_plane(draw, x, y, w, h):
    """A plane going down over mountains, smoke trail behind it."""
    draw.rectangle([x, y, x + w, y + h], fill=(180, 205, 230))
    # mountains
    base = y + h
    draw.polygon([(x, base), (x + 70, base - 34), (x + 140, base)],
                 fill=(90, 95, 105))
    draw.polygon([(x + 110, base), (x + 200, base - 48), (x + 290, base)],
                 fill=(70, 75, 88))
    draw.polygon([(x + 230, base), (x + 280, base - 26), (x + w, base)],
                 fill=(95, 100, 110))
    # smoke trail
    for i, (sx, sy, r) in enumerate(((x + 40, y + 22, 10), (x + 78, y + 30, 13),
                                     (x + 118, y + 40, 16), (x + 156, y + 50, 18))):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(140, 140, 145))
    # plane, nose down to the right
    px, py = x + 205, y + 62
    draw.polygon([(px - 52, py - 14), (px + 46, py + 26), (px + 58, py + 30),
                  (px + 40, py + 8), (px - 44, py - 26)], fill=(40, 45, 55))
    draw.polygon([(px - 8, py - 4), (px + 6, py - 34), (px + 16, py - 30),
                  (px + 8, py + 2)], fill=(40, 45, 55))
    draw.polygon([(px - 30, py + 2), (px - 18, py + 28), (px - 8, py + 24),
                  (px - 16, py + 0)], fill=(40, 45, 55))
    # impact burst
    ex, ey = x + 252, y + h - 30
    for r, col in ((18, (255, 120, 30)), (10, (255, 190, 60)),
                   (5, (255, 240, 150))):
        draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)


def draw_sanctions(draw, x, y, w, h):
    """A document stamped SANCTIONED."""
    draw.rectangle([x, y, x + w, y + h], fill=(240, 238, 225))
    px, py, pw, ph = x + 66, y + 6, 120, 72
    draw.rectangle([px, py, px + pw, py + ph], fill=(255, 255, 255),
                   outline=(160, 160, 160), width=1)
    draw.polygon([(px + pw - 16, py), (px + pw, py + 16), (px + pw, py),
                  ], fill=(220, 220, 220))
    for ly in (py + 12, py + 26, py + 40, py + 54):
        draw.line([px + 10, ly, px + pw - 14, ly], fill=(150, 150, 150),
                  width=2)
    # rotated red stamp, kept inside the illustration area
    stamp = Image.new("RGBA", (120, 30), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([2, 2, 117, 27], outline=(178, 34, 34), width=3)
    sf = bold(15)
    sd.text((60 - sd.textlength("SANCTIONED", font=sf) / 2, 7),
            "SANCTIONED", font=sf, fill=(178, 34, 34))
    stamp = stamp.rotate(8, expand=True, resample=Image.BICUBIC)
    draw._image.paste(stamp, (x + 172, y + 44), stamp)


PANELS = [
    ("TRUMP, XI, PUTIN TO MEET",
     "Trilateral summit set for Shenzhen, 19 Nov, at APEC",
     draw_summit),
    ("KYIV BRIDGES HIT",
     "Russian strikes hit two bridges as the bridge war grows",
     draw_kyiv),
    ("US LOSES MEASLES STATUS",
     "Elimination gone after 26 years - 5,400+ cases, 10 dead",
     draw_measles),
    ("NVIDIA CHIEF OUT",
     "Jensen Huang departs; chip-spy scandal shadows US-China talks",
     draw_chip),
    ("PLANE CRASH KILLS 19",
     "Russian military plane down in Kemerovo - all aboard dead",
     draw_plane),
    ("SETTLER KILLS WOMAN, 72",
     "UK sanctions 8 Israeli settlement firms after West Bank shooting",
     draw_sanctions),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([24, 20, W - 24, 23], fill=RULE)
    f_date = bold(28)
    date = "TUESDAY 17 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 30), date,
           font=f_date, fill=RED)
    f_title = bold(56)
    title = "WORLD NEWS IN ONE IMAGE"
    d.text(((W - d.textlength(title, font=f_title)) / 2, 62), title,
           font=f_title, fill=INK)
    d.rectangle([24, 128, W - 24, 130], fill=RULE)
    d.rectangle([24, 134, W - 24, 135], fill=RULE)

    # ---- hero panel: Kerch bridge ----
    hx, hy, hw, hh = 24, 146, 976, 392
    panel_border(d, hx, hy, hw, hh, width=3)
    draw_hero_bridge(d, hx + 3, hy + 3, hw - 6, 222)
    f_kick = bold(21)
    d.text((hx + 16, hy + 236), "TOP STORY  —  CRIMEA", font=f_kick, fill=RED)
    f_head = bold(46)
    d.text((hx + 16, hy + 262), "KERCH BRIDGE COLLAPSES", font=f_head,
           fill=INK)
    f_cap = regular(24)
    cap = ("Ukraine strike drops the road arch into the strait; rail span "
           "still stands. Zelensky: \u201cunprecedented\u201d.")
    draw_lines(d, wrap(d, cap, f_cap, hw - 32), f_cap, hx + 16, hy + 322,
               INK, 30)

    # ---- six small panels, 3 x 2 ----
    pw, ph, gap = 317, 204, 12
    for i, (headline, caption, scene) in enumerate(PANELS):
        col, row = i % 3, i // 3
        px = 24 + col * (pw + gap)
        py = 552 + row * (ph + 10)
        panel_border(d, px, py, pw, ph, width=2)
        scene(d, px + 2, py + 2, pw - 4, 90)
        f_h = bold(26)
        lines = wrap(d, headline, f_h, pw - 20)
        y = py + 100
        y = draw_lines(d, lines[:2], f_h, px + 10, y, INK, 28)
        f_c = regular(16)
        draw_lines(d, wrap(d, caption, f_c, pw - 20)[:2], f_c, px + 10,
                   y + 2, GREY, 19)

    # ---- footer ----
    f_f = regular(16)
    foot = "7 STORIES FROM 17 NOVEMBER 2026  •  ONE IMAGE"
    d.text(((W - d.textlength(foot, font=f_f)) / 2, 978), foot, font=f_f,
           fill=GREY)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    build().save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()
