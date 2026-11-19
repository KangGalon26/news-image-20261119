#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page, 1024x1024, deterministic.

A fresh newspaper layout drawn with Pillow and DejaVu only. No network,
no random values, no timestamps inside the image except the fixed date.
Run: python3 draw.py  -> writes entry.png beside this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

INK = (18, 18, 18)
RED = (178, 24, 24)
BLUE = (24, 62, 140)
TEAL = (14, 92, 92)
GOLD = (176, 124, 18)
GREY = (92, 92, 92)
LIGHT = (240, 238, 232)
MIDLINE = (200, 198, 190)


def wrap(draw, text, fnt, width):
    """Wrap text to fit a pixel width, word by word."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, size, leading, colour=INK):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=colour)
        y += leading
    return y


def headline(draw, x, y, width, text, fnt, leading):
    return para(draw, x, y, width, text, fnt, leading, leading, INK)


def rule(draw, x, y, width, colour=INK, thickness=2):
    draw.rectangle([x, y, x + width, y + thickness - 1], fill=colour)


def kicker(draw, x, y, text, colour):
    f = font(SANS_B, 19)
    draw.text((x, y), text.upper(), font=f, fill=colour)
    return y + 26


def main():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=6)

    # ---- top date bar -------------------------------------------------
    d.rectangle([6, 6, W - 7, 52], fill=INK)
    d.text((24, 16), "THURSDAY 19 NOVEMBER 2026", font=font(SANS_B, 24),
           fill=(255, 255, 255))
    d.text((W - 24 - d.textlength("ONE DAY  •  ONE PAGE", font=font(SANS_B, 20)),
            19), "ONE DAY  •  ONE PAGE", font=font(SANS_B, 20),
           fill=(210, 210, 210))

    # ---- masthead ------------------------------------------------------
    d.text((512, 66), "THE WORLD TODAY", font=font(SERIF, 72),
           fill=INK, anchor="ma")
    d.text((512, 148), "The day's world news, summed up in one image",
           font=font(SANS, 22), fill=GREY, anchor="ma")
    rule(d, 24, 186, 976, INK, 3)
    rule(d, 24, 193, 976, INK, 1)

    # ---- lead story ----------------------------------------------------
    y = 210
    d.text((24, y), "SHENZHEN  •  APEC", font=font(SANS_B, 19), fill=RED)
    d.text((24, y + 26), "Three leaders, one room,",
           font=font(SERIF, 46), fill=INK)
    d.text((24, y + 76), "for the first time",
           font=font(SERIF, 46), fill=INK)

    # three leader discs on the right of the lead
    discs = [("TRUMP", "USA", BLUE), ("XI", "CHINA", RED),
             ("PUTIN", "RUSSIA", (70, 70, 70))]
    cx = 700
    for label, country, colour in discs:
        d.ellipse([cx, y + 6, cx + 92, y + 98], fill=colour,
                  outline=(255, 255, 255), width=3)
        d.text((cx + 46, y + 30), label, font=font(SANS_B, 17),
               fill=(255, 255, 255), anchor="ma")
        d.text((cx + 46, y + 108), country, font=font(SANS_B, 15),
               fill=GREY, anchor="ma")
        cx += 102

    lead = ("Donald Trump, Xi Jinping and Vladimir Putin meet at Kylin "
            "Villa in Shenzhen for the first trilateral summit of the "
            "three powers. Nuclear arms top the agenda — New START "
            "expired in February — with Ukraine, the war in Iran, trade "
            "and AI also on the table. No deal is expected.")
    y = para(d, 24, y + 132, 976, lead, font(SANS, 22), 22, 29)

    rule(d, 24, 470, 976, MIDLINE, 2)

    # ---- middle row: Gulf and Gaza / The Hague -------------------------
    my = 490
    # left column: Gulf
    d.text((24, my), "THE GULF", font=font(SANS_B, 19), fill=RED)
    y = headline(d, 24, my + 28, 470,
                 "Iran widens its Gulf attacks",
                 font(SERIF, 34), 40)
    y = para(d, 24, y + 6, 470,
             "Iranian drones target the US Ali Al Salem base in Kuwait "
             "and sites in Bahrain, after a US strike on Qeshm Island. "
             "Both states say they shot the attacks down.",
             font(SANS, 20), 20, 27)
    y = para(d, 24, y + 8, 470,
             "A tanker is hit near the Strait of Hormuz; the energy "
             "agency calls it the greatest threat ever to energy security.",
             font(SANS, 20), 20, 27)
    # right column: Gaza + Hague
    d.text((530, my), "GAZA  •  THE HAGUE", font=font(SANS_B, 19), fill=BLUE)
    y2 = headline(d, 530, my + 28, 470,
                  "Israeli forces cross the Gaza ceasefire line",
                  font(SERIF, 34), 40)
    y2 = para(d, 530, y2 + 6, 470,
              "Troops move into Hamas-held central Gaza, past the Yellow "
              "Line. A peace board warns both sides are failing to keep "
              "the ceasefire.",
              font(SANS, 20), 20, 27)
    y2 = para(d, 530, y2 + 8, 470,
              "In The Hague, the world court rules today on whether "
              "Myanmar committed genocide against the Rohingya — a first "
              "for a state.",
              font(SANS, 20), 20, 27)

    rule(d, 24, 796, 976, MIDLINE, 2)

    # ---- bottom row: Europe and culture --------------------------------
    by = 814
    d.text((24, by), "EUROPE", font=font(SANS_B, 19), fill=TEAL)
    y = headline(d, 24, by + 28, 470, "EU offers Ukraine a €45bn loan",
                 font(SERIF, 30), 36)
    y = para(d, 24, y + 4, 470,
             "The European Commission proposes the loan to cover Kyiv's "
             "funding shortfall next year.",
             font(SANS, 19), 19, 26)

    d.text((530, by), "CULTURE", font=font(SANS_B, 19), fill=GOLD)
    y = headline(d, 530, by + 28, 470,
                 "Van Gogh sells for a record $190.4m",
                 font(SERIF, 30), 36)
    y = para(d, 530, y + 4, 470,
             "\"Chestnut Trees in Blossom\" (1890) beats the old $117.2m "
             "record at Sotheby's, New York.",
             font(SANS, 19), 19, 26)

    # ---- footer strip ---------------------------------------------------
    d.rectangle([6, 968, W - 7, H - 7], fill=LIGHT)
    d.text((24, 978), "Also today: unrest in Bangladesh  •  COP31 talks in Antalya  •  "
                      "Ethiopia–Eritrea troops mass  •  IAEA warns on N. Korea",
           font=font(SANS, 16), fill=INK)
    d.text((24, 1000 - 6), "Sources: Yonhap, BBC, Reuters, Al Jazeera, Euronews, Sotheby's — 19 Nov 2026",
           font=font(SANS, 14), fill=GREY)

    img.save(OUT, "PNG", optimize=True)


if __name__ == "__main__":
    main()
