# K3 «Сходи»: transparent object layer — things standing on the yellow steps
from lib import *
import sys
ver = sys.argv[1] if len(sys.argv) > 1 else 'v4'
S = dict(sh=(0.3, 0.6, 1.0, .30), amb=(0.2, 0.9, 4.0, .12))
l = Layer(297, 210, ppi=250)
tw = trim(load('img/cut/avantiura-tw-2.webp'))
duo_s = trim(load('img/cut/hratsiia-flat.webp'))
ring = Image.open(OUT + 'ring-clean.png')
box3 = trim(load('img/cut/maskscr-litnie-pole.webp'))
pair = trim(load('img/cut/pair-zolote.webp'))
# step tops (mm): 132, 116, 100, 84 ; columns start 16.5, 84, 151.5, 219 (61.5 wide)
def stand(im, col_x, top, w, rot=0, dx=0, sink=1.0, **kw):
    r = im.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else im
    h = w * r.height / r.width
    l.cutout(im, col_x + (61.5 - w) / 2 + dx, top - h + sink, w, rot=rot, **(kw or S))
stand(tw, 16.5, 126, 40)
stand(duo_s, 84, 110, 46, rot=4, dx=-2)
l.cutout(ring, 84 + 43.5, 110 - 13.2, 12, rot=-6, sh=(0.3, 0.5, 0.7, .34), amb=(0.2, 0.6, 2.2, .14))
stand(box3, 151.5, 94, 58)
# 04 is a real photo (multiplied in CSS), see k3-box-vpevnenist-rot.jpg
l.save('k3-objects.png')
l.preview('tmp/k3-objects-preview.jpg', PAPER)
