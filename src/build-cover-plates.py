#!/usr/bin/env python3
"""Plates for the object-led cover variants G, H, I (concepts of the luxury-catalogue art director, 04.10) → img/p3/cover-*.jpg.
Real photos and existing cut-outs only: the studio backdrop of a box photo is lifted to pure white and the photo is multiplied
onto the paper colour, so the thing keeps its own shadow and never sits in a white rectangle (src/ad-p3/lib.py).
The boxes are real «хустка 44 × 44 + твіллі» sets from obiimy.world, so what the cover shows is one of the four gifts
at its price (the art director's first choice, box-dots / box-red, shows SOLO scarves that are not sold as this set)."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "ad-p3"))
import lib
from lib import Canvas, norm_white, load, trim
from PIL import Image
lib.ROOT = str(ROOT) + "/"; lib.OUT = str(ROOT / "img" / "p3") + "/"
SH = dict(sh=(0.35, 0.7, 1.1, .30), amb=(0.2, 0.9, 4.2, .11))

# G · one box: the «Ніжність» set, the lid leaves through the top left corner
c = Canvas(297, 210, ppi=200)
print("G", c.multiply(norm_white(load("photo/site/set-tvilli-845-ta-khustky-4444-nizhnis-01.jpg"), feather=90, keep_edges="lt"), 0, 0, 152.0))
c.save("cover-1.jpg", q=90)

# H · four gifts on one line, growing to the box in the top right corner
c = Canvas(297, 210, ppi=200); BOX = 112.0; BASE = 108.0
print("H box", c.multiply(norm_white(load("photo/site/set-tvilli-845-ta-khustky-4444-hratsii-01.jpg"), feather=90, keep_edges="lt"), 297 - BOX, 0, BOX, rot=-90))
def stand(im, x, w):
    h = w * im.height / im.width; c.cutout(im, x, BASE - h, w, **SH); return round(h, 1)
print("twilly", stand(trim(load("img/cut/tysha-tw-1.webp")), 16.5, 39), "scarf", stand(trim(load("img/cut/zolote-44-1.webp")), 62.0, 53))
ring = trim(Image.open(ROOT / "src" / "ad-p3" / "ring-clean.png")); stand(ring, 62.0 + 53 - 2.5, 12.5)      # the ring stands on the line at the scarf's corner, with the same shadow as the other things
print("mask set", stand(trim(load("img/cut/maskscr-litnie-pole.webp")), 121.0, 53))
c.save("cover-2.jpg", q=90)

# I · the sunlit still life (170 × 210 mm, 181 ppi — not wider)
load("photo/site/set-ta-rezynka-litnie-pole-04.jpg").convert("RGB").crop((110, 0, 1324, 1500)).save(ROOT / "img" / "p3" / "cover-3.jpg", quality=92, subsampling=0)

# J, K, L · covers of the editorial art director (04.10)
import numpy as np
# J · one box on paper: the «Золоте світло» set (photo/box-gold.jpg), larger than G and bleeding off the top left corner
c = Canvas(297, 210, ppi=200)
print("J", c.multiply(norm_white(load("photo/box-gold.jpg"), feather=90, keep_edges="lt"), -3, -8.5, 160.0))
c.save("cover-4.jpg", q=90)
# K · the cover is the lid: brand yellow to the edge, the real box (re-cut by the art director, shadow baked) in the top right corner
c = Canvas(297, 210, color=(0xFD, 0xD3, 0x1A), ppi=200)
box = Image.open(ROOT / "src" / "ad-p3" / "box-gold-cw-recut.png").convert("RGBA"); w = round(177.5 * c.mm); box = box.resize((w, round(box.height * w / box.width)), Image.LANCZOS)
arr = np.asarray(box).astype(np.float32) / 255; c._blend(arr[..., :3], arr[..., 3], round((297 + 6 - 177.5) * c.mm), round(-3 * c.mm), mode="over")
c.save("cover-5.jpg", q=90)
# L · in the box and on the shoulders: the «Натхнення» set and a studio portrait with the same print (photo/dotyk-1.webp)
c = Canvas(297, 210, ppi=200)
ph = load("photo/dotyk-1.webp").convert("RGB").crop((98, 0, 941, 1500)).resize((round(118 * c.mm), c.h), Image.LANCZOS)
c.a[:, c.w - ph.width:] = np.asarray(ph).astype(np.float32) / 255
print("L", c.multiply(norm_white(load("photo/site/set-tvilli-845-ta-khustky-4444-natkhne-01.jpg"), feather=90, keep_edges="lt"), -4, -6, 122.0))
c.save("cover-6.jpg", q=90)
print("plates:", sorted(p.name for p in (ROOT / "img" / "p3").glob("cover-*.jpg")))
