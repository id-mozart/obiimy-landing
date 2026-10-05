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
c.save("cover-1.jpg", q=84)

# H · four gifts on one line, growing to the box in the top right corner
c = Canvas(297, 210, ppi=200); BOX = 112.0; BASE = 108.0
print("H box", c.multiply(norm_white(load("photo/site/set-tvilli-845-ta-khustky-4444-hratsii-01.jpg"), feather=90, keep_edges="lt"), 297 - BOX, 0, BOX, rot=-90))
def stand(im, x, w):
    h = w * im.height / im.width; c.cutout(im, x, BASE - h, w, **SH); return round(h, 1)
print("twilly", stand(trim(load("img/cut/tysha-tw-1.webp")), 16.5, 39), "scarf", stand(trim(load("img/cut/zolote-44-1.webp")), 62.0, 53))
ring = trim(Image.open(ROOT / "src" / "ad-p3" / "ring-clean.png")); stand(ring, 62.0 + 53 + 0.8, 4.8)      # the ring stands on the line by the scarf's corner at its true scale: 9 % of the scarf's width
print("mask set", stand(trim(load("img/cut/maskscr-litnie-pole.webp")), 121.0, 53))
c.save("cover-2.jpg", q=84)

# I · the sunlit still life (170 × 210 mm, 181 ppi — not wider)
load("photo/site/set-ta-rezynka-litnie-pole-04.jpg").convert("RGB").crop((110, 0, 1324, 1500)).save(ROOT / "img" / "p3" / "cover-3.jpg", quality=92, subsampling=0)

# J, K, L · covers of the editorial art director (04.10)
import numpy as np
# J · one box on paper: the «Золоте світло» set (photo/box-gold.jpg), larger than G and bleeding off the top left corner
c = Canvas(297, 210, ppi=200)
print("J", c.multiply(norm_white(load("photo/box-gold.jpg"), feather=90, keep_edges="lt"), -3, -8.5, 160.0))
c.save("cover-4.jpg", q=84)
# K · the cover is the lid: brand yellow to the edge, the real box (re-cut by the art director, shadow baked) in the top right corner
c = Canvas(297, 210, color=(0xFD, 0xD3, 0x1A), ppi=200)
box = Image.open(ROOT / "src" / "ad-p3" / "box-gold-cw-recut.png").convert("RGBA"); w = round(177.5 * c.mm); box = box.resize((w, round(box.height * w / box.width)), Image.LANCZOS)
arr = np.asarray(box).astype(np.float32) / 255; c._blend(arr[..., :3], arr[..., 3], round((297 + 6 - 177.5) * c.mm), round(-3 * c.mm), mode="over")
c.save("cover-5.jpg", q=84)
# L · in the box and on the shoulders: the «Натхнення» set and a studio portrait with the same print (photo/dotyk-1.webp)
c = Canvas(297, 210, ppi=200)
ph = load("photo/dotyk-1.webp").convert("RGB").crop((98, 0, 941, 1500)).resize((round(118 * c.mm), c.h), Image.LANCZOS)
c.a[:, c.w - ph.width:] = np.asarray(ph).astype(np.float32) / 255
print("L", c.multiply(norm_white(load("photo/site/set-tvilli-845-ta-khustky-4444-natkhne-01.jpg"), feather=90, keep_edges="lt"), -4, -6, 122.0))
c.save("cover-6.jpg", q=84)

# M, N, O · three more covers after a fresh look (04.10): the scarf itself as the hero, a fan of prints, a framed studio portrait
SOFT = dict(sh=(0.6, 1.4, 2.2, .26), amb=(0.4, 1.6, 7.0, .14))
def lay(c, name, cx, cy, w, rot, **kw):
    """A cut-out by its centre (mm), w mm wide before rotation, turned by rot degrees, with a soft shadow."""
    im = trim(load(f"img/cut/{name}.webp")); r = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    bw = w * r.width / im.width; bh = bw * r.height / r.width
    c.cutout(im, cx - bw / 2, cy - bh / 2, bw, rot=rot, **(kw or SOFT))
# M · carré: one 44 × 44 scarf, nearly life-size, slightly turned and leaving through the right edge
c = Canvas(297, 210, ppi=200); lay(c, "zolote-44-1", 226, 106, 196, -7); c.save("cover-7.jpg", q=84)
# N · a fan of four 44 × 44 scarves: a print for each one in the team
c = Canvas(297, 210, ppi=200)
for name, cx, cy, rot in (("krok-44-1", 62, 52, 15), ("hratsiia-flat", 122, 44, 5), ("zolote-44-1", 182, 44, -6), ("puls-44-1", 240, 54, -16)):
    lay(c, name, cx, cy, 104, rot)
c.save("cover-8.jpg", q=84)
# O · a framed studio portrait (the brand's lookbook) and the four gifts as a small shelf under it
c = Canvas(297, 210, ppi=200)
ph = load("photo/lookbook/lb05-06-L.webp").convert("RGB"); pw = 108.0; phh = pw * ph.height / ph.width
x0, y0 = round((297 - 16.5 - pw) * c.mm), round(16.5 * c.mm); ph = ph.resize((round(pw * c.mm), round(phh * c.mm)), Image.LANCZOS)
c.a[y0:y0 + ph.height, x0:x0 + ph.width] = np.asarray(ph).astype(np.float32) / 255
BASE = 190.0; x = 297 - 16.5 - pw
for name, w in (("krok-tw-1", 15.5), ("duo-hratsiia-ring", 25), ("maskscr-litnie-pole", 25), ("pair-zolote", 27)):
    im = trim(load(f"img/cut/{name}.webp")); h = w * im.height / im.width
    c.cutout(im, x, BASE - h, w, sh=(0.3, 0.6, 0.9, .28), amb=(0.2, 0.7, 3.0, .10)); x += w + 3.6
print("O portrait", round(phh, 1), "mm high, shelf ends at", round(x, 1))
c.save("cover-9.jpg", q=84)
print("plates:", sorted(p.name for p in (ROOT / "img" / "p3").glob("cover-*.jpg")))

# P–U · covers on the brand's own editorial photographs (05.10: the assortment looked through — obiimy.world product galleries)
import numpy as np
PAPER_F = np.array(lib.PAPER, np.float32) / 255
def photo(c, path, x, y, w, crop=None, match=None, fade_l=0):
    """A photograph laid straight on the page (mm). crop — window in the source (fractions). match — a patch of its studio backdrop
    (fractions): the picture is balanced so that the patch takes the paper's colour, whites stay white. fade_l (mm) — the inner
    left edge dissolves into the paper, so a studio frame never stands as a light rectangle."""
    im = load(path).convert("RGB"); W, H = im.size
    if crop: im = im.crop((round(crop[0] * W), round(crop[1] * H), round(crop[2] * W), round(crop[3] * H))); W, H = im.size
    a = np.asarray(im).astype(np.float32) / 255
    if match: a = np.clip(a * (PAPER_F / np.median(a[round(match[1] * H):round(match[3] * H), round(match[0] * W):round(match[2] * W)].reshape(-1, 3), 0)), 0, 1)
    pw = round(w * c.mm); ph = round(pw * H / W); a = np.asarray(lib.to_img(a).resize((pw, ph), Image.LANCZOS)).astype(np.float32) / 255
    al = np.ones((ph, pw), np.float32)
    if fade_l: n = round(fade_l * c.mm); t = np.linspace(0, 1, n); al[:, :n] *= (t * t * (3 - 2 * t))[None, :]
    c._blend(a, al, round(x * c.mm), round(y * c.mm), mode="over"); return round(ph / c.mm, 1)

# P · the tulip: a hand with a twilly on the wrist gives a flower — the gesture of a gift; the photograph lies on the paper
c = Canvas(297, 210, ppi=200)
print("P", c.multiply(norm_white(load("photo/site/tvilli-ta-rezynka-makovyi-tsvit-02.jpg"), feather=70, keep_edges="lb"), 0, 0, 157.5)); c.save("cover-10.jpg", q=84)
# Q · the white T-shirt: a 44 × 44 scarf at the neck, the way it is worn every day
c = Canvas(297, 210, ppi=200)
print("Q", photo(c, "photo/site/khustka-potsilunok-sontsia-44x44-02.jpg", 108, 0, 210, match=(0.02, 0.25, 0.14, 0.45), fade_l=46)); c.save("cover-11.jpg", q=84)
# R · the box whole in the frame: the «Спокуса» set, the lid beside it
c = Canvas(297, 210, ppi=200)
print("R", c.multiply(norm_white(load("photo/site/set-tvilli-845-ta-khustky-4444-spokusa-02.jpg"), feather=90, keep_edges="b"), 148, 6.2, 145)); c.save("cover-12.jpg", q=84)       # the lower edge is the page's: the ends of the twilly do not dissolve
# S · the sofa: an editorial frame to the edge, the twilly at the neck
c = Canvas(297, 210, ppi=200)
print("S", photo(c, "photo/site/tvilli-shovkovyi-melodiia-dvokh-02.jpg", 157, 0, 140)); c.save("cover-13.jpg", q=84)
# T · the suit: a twilly worn as a tie — the office look, a framed portrait
c = Canvas(297, 210, ppi=200)
print("T", photo(c, "photo/site/tvilli-shovkovyi-sokovyti-spohady-02.jpg", 297 - 16.5 - 112, 16.5, 112)); c.save("cover-14.jpg", q=84)
# U · the smile and the four gifts as a shelf under the headline
c = Canvas(297, 210, ppi=200)
print("U", photo(c, "photo/site/tvilli-shovkovyi-yednannia-04.jpg", 0, 0, 134.4, crop=(0, 0, 0.96, 1))); x = 151.0       # the tip of the twilly is cut clearly, not left touching the edge
for name, w in (("krok-tw-1", 19), ("duo-hratsiia-ring", 31), ("maskscr-litnie-pole", 31), ("pair-zolote", 33)):
    im = trim(load(f"img/cut/{name}.webp")); h = w * im.height / im.width
    c.cutout(im, x, 92.0 - h, w, sh=(0.3, 0.6, 0.9, .28), amb=(0.2, 0.7, 3.0, .10)); x += w + 5
c.save("cover-15.jpg", q=84)
print("plates:", sorted(p.name for p in (ROOT / "img" / "p3").glob("cover-*.jpg")))

# V · the hybrid of H and U after the third cold-buyer round: the four gifts large on one line, a two-line headline, a real portrait at the right
c = Canvas(297, 210, ppi=200)
print("V", photo(c, "photo/site/khustka-potsilunok-sontsia-44x44-02.jpg", 170, 0, 210, crop=(0.215, 0, 0.785, 1), match=(0.02, 0.25, 0.14, 0.45), fade_l=12)); x = 16.5   # the portrait at the scale of cover Q: the whole scarf, the head not blown up (jury, round 4)
for name, w in (("krok-tw-1", 26), ("duo-hratsiia-ring", 38), ("maskscr-litnie-pole", 38), ("set-natkhnennia-box", 40)):
    im = trim(load(f"img/cut/{name}.webp")); h = w * im.height / im.width
    c.cutout(im, x, 100.0 - h, w, sh=(0.3, 0.6, 0.9, .28), amb=(0.2, 0.7, 3.0, .10)); x += w + 6
c.save("cover-16.jpg", q=84)
