#!/usr/bin/env python3
"""Plates for the page-3 variants L, M, N «набори з каталогу» (06.10): the shop's gift sets, photographed for obiimy.world,
cut out whole (src/cutout.py: box-*) and laid on the paper with soft shadows — no photo frame, no white rectangle.
L · four boxes on one line, the text under each · M · a still life of the four boxes and a ledger · N · one box large, three small.
→ img/p3/sets-l.jpg, sets-m.jpg, sets-n.jpg (200 ppi). Positions are in mm, the deck grid: columns 61.5, gutters 6, margins 16.5."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "ad-p3"))
import lib
from lib import Canvas, load, trim
from PIL import Image
lib.ROOT = str(ROOT) + "/"; lib.OUT = str(ROOT / "img" / "p3") + "/"
SOFT = dict(sh=(0.35, 0.7, 1.1, .30), amb=(0.2, 0.9, 4.2, .11))
BOX = ["box-twscr-litnie-pole", "box-maskscr-litnie-pole", "box-sctw-spokusa", "box-maskbm-pidnesennia"]   # 01 … 04, as in SETS_L
def cut(name): return trim(load(f"img/cut/{name}.webp"))
def lay(c, name, cx, cy, w, rot=0):
    """A cut-out by its centre (mm), w mm wide before rotation."""
    im = cut(name); r = im.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else im
    bw = w * r.width / im.width; bh = bw * r.height / r.width
    c.cutout(im, cx - bw / 2, cy - bh / 2, bw, rot=rot, **SOFT); return bw, bh
def stand(c, name, cx, base, w, rot=0):
    """A cut-out by its horizontal centre and the line it stands on (mm)."""
    im = cut(name); r = im.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else im
    bw = w * r.width / im.width; bh = bw * r.height / r.width
    c.cutout(im, cx - bw / 2, base - bh, bw, rot=rot, **SOFT); return bw, bh

# L · four boxes on one line: each as wide as its column allows, bottoms on one line
c = Canvas(297, 210, ppi=200)
for i, (name, w) in enumerate(zip(BOX, (64, 62, 63, 56))):
    print("L", name, [round(v, 1) for v in stand(c, name, 16.5 + 30.75 + i * 67.5, 112.0, w)])
c.save("sets-l.jpg", q=86)

# M · flat lay two by two on the left two thirds (captions under each box in HTML), the ledger on the right
c = Canvas(297, 210, ppi=200)
for name, cx, cy, w, rot in ((BOX[0], 60, 58, 73, 3), (BOX[1], 156, 57, 66, -3), (BOX[2], 60, 142, 73, -3), (BOX[3], 156, 142, 60, 3)):
    print("M", name, [round(v, 1) for v in lay(c, name, cx, cy, w, rot)])
c.save("sets-m.jpg", q=86)

# N · one box large (the scarf and twilly set), the three others as a column beside the text
c = Canvas(297, 210, ppi=200)
print("N hero", [round(v, 1) for v in lay(c, BOX[2], 16.5 + 54, 94, 108, -4)])
for name, cy, w in ((BOX[0], 66, 52), (BOX[1], 116, 52), (BOX[3], 165, 46)):
    print("N", name, [round(v, 1) for v in lay(c, name, 186, cy, w)])
c.save("sets-n.jpg", q=86)
print("plates:", sorted(p.name for p in (ROOT / "img" / "p3").glob("sets-*.jpg")))
