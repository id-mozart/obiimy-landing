# K1 «Натюрморт»: page-size still life (two real box photos multiplied onto paper + cutouts with soft shadows)
from lib import *
import sys
ver = sys.argv[1] if len(sys.argv) > 1 else 'v5'
c = Canvas(297, 210, ppi=250)
L = norm_white(load('photo/site/set-tvilli-845-ta-khustky-4444-smilyvy-01.jpg'), feather=70, keep_edges='lt')
R = norm_white(load('photo/site/set-ta-rezynka-litnie-pole-02.jpg'), feather=70, keep_edges='rt')
WL, WR = 110.0, 122.0
c.multiply(L, 0, 0, WL)
c.multiply(R, 297 - WR, 0, WR)
SH = dict(sh=(0.35, 0.7, 1.1, .30), amb=(0.2, 0.9, 4.2, .11))
sc = trim(load('img/cut/hratsiia-flat.webp'))
tw = trim(load('img/cut/tysha-tw-3.webp'))
ring = Image.open(OUT + 'ring-clean.png')
c.cutout(sc, 135.5, 46.5, 52, rot=5, **SH)
c.cutout(tw, 104, 44, 44, rot=-8, **SH)
c.cutout(ring, 179.5, 88.5, 12.5, rot=-6, sh=(0.3, 0.5, 0.7, .34), amb=(0.2, 0.6, 2.2, .14))
c.save('k1-tableau.png')
c.save('tmp/k1-tableau-preview.jpg', q=88)
