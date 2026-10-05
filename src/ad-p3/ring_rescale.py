# -*- coding: utf-8 -*-
"""The scarf ring at its true scale on the three flattened plates img/p3/lux-k1…3.jpg (05.10: «держатели гигантские»).
The plates were flattened in the art director's session, so the ring is replaced in place: the scarf and the small ring are
rendered again with the plate's own parameters and laid over a rebuilt ground wherever the old ring and its shadow were.
The ring is about 4 cm against a 44 cm scarf — 9 % of the scarf's width (was 24 %). Run once: python3 ring_rescale.py"""
import sys, pathlib
import lib
from lib import *
P3 = pathlib.Path(lib.ROOT) / 'img' / 'p3'
SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else P3      # the untouched plates, when a copy is kept
RING = Image.open(pathlib.Path(lib.ROOT) / 'src' / 'ad-p3' / 'ring-clean.png')
SH = dict(sh=(0.35, 0.7, 1.1, .30), amb=(0.2, 0.9, 4.2, .11))
RS = dict(sh=(0.15, 0.25, 0.4, .34), amb=(0.1, 0.3, 1.2, .14))

def layer(draw):
    l = Layer(297, 210, ppi=250); draw(l)
    rgb = l.c / np.maximum(l.al[..., None], 1e-4)
    im = Image.fromarray((np.dstack([np.clip(rgb, 0, 1), np.clip(l.al, 0, 1)]) * 255 + .5).astype(np.uint8)).resize((2339, 1654), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255
    return a[..., :3], a[..., 3]

def patch(name, scarf, old, new, ground):
    plate = np.asarray(Image.open(SRC / name).convert('RGB')).astype(np.float32) / 255; k = 2339 / 297
    _, a_old = layer(old); s_rgb, s_al = layer(scarf); n_rgb, n_al = layer(new)
    m = ndi.binary_dilation(a_old > 0.012, iterations=7) | (n_al > 0.012)
    ys, xs = np.nonzero(m); y0, y1, x0, x1 = ys.min() - 12, ys.max() + 13, xs.min() - 12, xs.max() + 13
    g = ground(plate, k, (y0, y1, x0, x1))
    out = g * (1 - s_al[y0:y1, x0:x1, None]) + s_rgb[y0:y1, x0:x1] * s_al[y0:y1, x0:x1, None]
    out = out * (1 - n_al[y0:y1, x0:x1, None]) + n_rgb[y0:y1, x0:x1] * n_al[y0:y1, x0:x1, None]
    w = np.clip(ndi.gaussian_filter(m[y0:y1, x0:x1].astype(np.float32), 2.5) * 1.6, 0, 1)[..., None]
    plate[y0:y1, x0:x1] = plate[y0:y1, x0:x1] * (1 - w) + out * w
    to_img(plate).save(P3 / name, quality=92, subsampling=0); print(name, 'patched', (x0 / k, y0 / k, x1 / k, y1 / k))

def flat(box):       # ground of one colour: the median of a clean patch of the plate (mm)
    def f(plate, k, r):
        bx = plate[int(box[1] * k):int(box[3] * k), int(box[0] * k):int(box[2] * k)]; col = np.median(bx.reshape(-1, 3), 0)
        return np.ones((r[1] - r[0], r[3] - r[2], 3), np.float32) * col
    return f
def column(x_mm):    # ground that changes only downwards (paper, then the yellow step): one clean column of the plate, stretched
    def f(plate, k, r):
        col = plate[r[0]:r[1], int(x_mm * k) - 2:int(x_mm * k) + 3].mean(1)
        return np.repeat(col[:, None, :], r[3] - r[2], 1)
    return f

hr = trim(load('img/cut/hratsiia-flat.webp')); pu = trim(load('img/cut/puls-44-1.webp'))
# I · table with two boxes: scarf 52 mm
patch('lux-k1.jpg', lambda l: l.cutout(hr, 135.5, 46.5, 52, rot=5, **SH),
      lambda l: l.cutout(RING, 179.5, 88.5, 12.5, rot=-6, sh=(0.3, 0.5, 0.7, .34), amb=(0.2, 0.6, 2.2, .14)),
      lambda l: l.cutout(RING, 184.3, 91.5, 4.7, rot=-6, **RS), flat((178, 105.5, 190, 108.5)))
# J · yellow tray: scarf 54 mm
S2 = dict(sh=(0.45, 0.9, 1.2, .34), amb=(0.3, 1.1, 4.6, .16), shadow_rgb=(128, 76, 0))
patch('lux-k2.jpg', lambda l: l.cutout(pu, 153.5, 52, 54, rot=5, **S2),
      lambda l: l.cutout(RING, 200, 93, 12.5, rot=-6, sh=(0.35, 0.6, 0.7, .46), amb=(0.2, 0.7, 2.4, .24), shadow_rgb=(120, 70, 0)),
      lambda l: l.cutout(RING, 201.8, 97.0, 4.9, rot=-6, sh=(0.18, 0.3, 0.4, .46), amb=(0.1, 0.35, 1.2, .24), shadow_rgb=(120, 70, 0)), flat((214, 94, 220, 100)))
# K · podium: scarf 46 mm standing on the second step (its top at 110 mm)
S3 = dict(sh=(0.3, 0.6, 1.0, .30), amb=(0.2, 0.9, 4.0, .12))
def scarf3(l):
    r = hr.rotate(4, resample=Image.BICUBIC, expand=True); h = 46 * r.height / r.width
    l.cutout(hr, 84 + (61.5 - 46) / 2 - 2, 110 - h + 1.0, 46, rot=4, **S3)
patch('lux-k3.jpg', scarf3,
      lambda l: l.cutout(RING, 84 + 43.5, 110 - 13.2, 12, rot=-6, sh=(0.3, 0.5, 0.7, .34), amb=(0.2, 0.6, 2.2, .14)),
      lambda l: l.cutout(RING, 134.8, 110.76 - 4.2 * RING.height / RING.width, 4.2, rot=-6, **RS), column(144.5))
