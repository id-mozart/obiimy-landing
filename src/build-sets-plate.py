#!/usr/bin/env python3
"""Plate for page-3 variant L «набори з каталогу» (06.10): four real photographs of the shop's gift sets (obiimy.world,
category «Подарункові набори») laid on the paper by multiplication — the box keeps its own shadow, no white rectangle.
Four columns of the deck grid (61.5 mm, gutters 6 mm), photographs cropped to one height → img/p3/sets-l.jpg (200 ppi)."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "ad-p3"))
import lib
from lib import Canvas, norm_white, load
lib.ROOT = str(ROOT) + "/"; lib.OUT = str(ROOT / "img" / "p3") + "/"
TOP, W, H = 36.0, 61.5, 72.0        # mm: the top of the photographs, the column, the height of the window
SETS = [  # file, window (fractions of the source) — the box whole, a little air around it
    ("photo/site/tvilli-ta-rezynka-litnie-pole-01.jpg", (0.0, 0.16, 1.0, 0.84)),     # the hinged box with its flaps is wide: shown whole, a little smaller
    ("photo/site/set-maska-rezynka-10-01.jpg", (0.05, 0.14, 0.95, 0.86)),
    ("photo/site/set-tvilli-845-ta-khustky-4444-svoboda-01.jpg", (0.0, 0.14, 1.0, 0.86)),   # the box with air around it: the backdrop can be lifted
    ("photo/site/set-maska-zakladka-rezynka-pidnesennia-01.jpg", (0.05, 0.04, 0.95, 0.96)),
]
c = Canvas(297, 210, ppi=200)
for i, (f, (x0, y0, x1, y1)) in enumerate(SETS):
    im = load(f).convert("RGB"); w, h = im.size
    win = im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)))
    tw, th = win.size
    if tw / th > W / H: pw = W; ph = W * th / tw           # contain: the whole window inside the column's slot, centred vertically
    else: ph = H; pw = H * tw / th
    print(f.split("/")[-1], c.multiply(norm_white(win, feather=50), 16.5 + i * (W + 6) + (W - pw) / 2, TOP + (H - ph) / 2, pw))
c.save("sets-l.jpg", q=86)
print("plate: img/p3/sets-l.jpg")
