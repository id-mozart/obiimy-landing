# K2 «Жовта коробка»: transparent object layer (cutouts + warm shadows) for the yellow page
from lib import *
import sys
ver = sys.argv[1] if len(sys.argv) > 1 else 'v4'
YEL = (253, 211, 26)
S = dict(sh=(0.45, 0.9, 1.2, .34), amb=(0.3, 1.1, 4.6, .16), shadow_rgb=(128, 76, 0))
l = Layer(297, 210, ppi=250)
tw = trim(load('img/cut/flirt-tw-5.webp'))
sc = trim(load('img/cut/puls-44-1.webp'))
ring = Image.open(OUT + 'ring-clean.png')
mask = trim(defringe(load('img/cut/mask-litnie-pole.webp')))
scr = Image.open(OUT + 'scrunchie-litnie-pole-cut.png')
pair = trim(load('img/cut/pair-zolote.webp'))
l.cutout(tw, 21.5, 51.5, 51, rot=-4, **S)
l.cutout(sc, 153.5, 52, 54, rot=5, **S)
l.cutout(ring, 200, 93, 12.5, rot=-6, sh=(0.35, 0.6, 0.7, .46), amb=(0.2, 0.7, 2.4, .24), shadow_rgb=(120, 70, 0))
l.cutout(mask, 15, 118.5, 62, rot=14, **S)
l.cutout(scr, 55.5, 150, 22.5, **S)
l.cutout(pair, 153, 118.5, 57, **S)
l.save('k2-objects.png')
l.preview('tmp/k2-objects-preview.jpg', YEL)
