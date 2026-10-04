#!/usr/bin/env python3
"""Product cut-outs with a transparent background → img/cut/<name>.webp (RGBA).
Client rule (04.10): no «photo in a white rectangle» in the deck or on the corporate landing — the product sits on the page.
SOLO cut-outs already exist (ads/solo/src/*-cut.webp) and are copied; the rest are cut here: the light, unsaturated
background connected to the image border is removed, the edge is eroded by a pixel and feathered. Parameters per image."""
import pathlib, shutil
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "img" / "cut"

def cut(src, name=None, light=228, sat=16, erode=1, feather=0.8, crop=True, pad=0.03, close=0, inner=False):
    im = Image.open(ROOT / src).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    mx, mn = a.max(2), a.min(2)
    cand = (mn >= light) & ((mx - mn) <= sat)                 # light and unsaturated = background candidate
    if close: cand = ndimage.binary_opening(cand, iterations=close)
    lab, n = ndimage.label(cand)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])); edge = edge[edge != 0]
    bg = np.isin(lab, edge)                                   # only what touches the border: whites inside the product stay
    if inner:                                                 # …unless the product is a ring: large enclosed background goes too
        sizes = ndimage.sum(cand, lab, range(1, n + 1)); big = [i + 1 for i, sz in enumerate(sizes) if sz > cand.size * (inner if inner is not True else 0.03)]
        bg |= np.isin(lab, big)
    fg = ~bg
    fg = ndimage.binary_fill_holes(fg) if False else fg
    if erode: fg = ndimage.binary_erosion(fg, iterations=erode)
    # drop specks: keep components larger than 0.05% of the frame
    lab2, n2 = ndimage.label(fg)
    if n2 > 1:
        sizes = ndimage.sum(fg, lab2, range(1, n2 + 1)); keep = [i + 1 for i, s in enumerate(sizes) if s > fg.size * 0.0005]
        fg = np.isin(lab2, keep)
    alpha = Image.fromarray((fg * 255).astype(np.uint8))
    if feather: alpha = alpha.filter(ImageFilter.GaussianBlur(feather))
    out = im.convert("RGBA"); out.putalpha(alpha)
    if crop:
        box = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
        if box:
            w, h = out.size; p = int(max(w, h) * pad)
            out = out.crop((max(0, box[0] - p), max(0, box[1] - p), min(w, box[2] + p), min(h, box[3] + p)))
    out.thumbnail((1400, 1400))
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / ((name or pathlib.Path(src).stem) + ".webp")
    out.save(dst, "WEBP", quality=88, method=6)
    return dst

def cut_grab(src, name, strong=26, weak=9, dark=70, fill=True, drop_neutral=0, scale=900, pad=0.03):
    """For products on a neutral backdrop with a soft, tinted shadow (boxes, rings): the lightness test keeps the shadow as ragged
    patches. Seeds come from chroma (strongly coloured or dark = product, neutral area touching the frame = backdrop), GrabCut settles
    the rest. fill=True returns enclosed neutral parts (white stripes of a scarf inside the box); drop_neutral > 0 removes enclosed
    backdrop larger than that share of the frame (the inside of a ring) while keeping small highlights on the metal."""
    import cv2
    im0 = Image.open(ROOT / src).convert("RGB"); W0, H0 = im0.size; k = scale / max(W0, H0)
    im = im0.resize((round(W0 * k), round(H0 * k)), Image.LANCZOS); a = np.asarray(im).astype(np.int16)
    rg, gb = a[..., 0] - a[..., 1], a[..., 1] - a[..., 2]
    edge = np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3), a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)]); light = edge[edge.min(1) > 170]
    brg, bgb = np.median(light[:, 0] - light[:, 1]), np.median(light[:, 1] - light[:, 2])
    ch = np.maximum(np.abs(rg - brg), np.abs(gb - bgb))
    sure = (ch > strong) | (a.max(2) < dark); prob = (ch > weak) | (a.max(2) < dark)
    sure = ndimage.binary_erosion(ndimage.binary_opening(sure, iterations=2), iterations=3)
    neutral = (ch <= 6) & (a.min(2) > 150); lab, n = ndimage.label(neutral)
    ids = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])); ids = ids[ids != 0]
    back = ndimage.binary_erosion(np.isin(lab, ids), iterations=4)
    mask = np.full(a.shape[:2], cv2.GC_PR_BGD, np.uint8); mask[prob] = cv2.GC_PR_FGD; mask[sure] = cv2.GC_FGD; mask[back] = cv2.GC_BGD
    cv2.grabCut(cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR), mask, None, np.zeros((1, 65)), np.zeros((1, 65)), 6, cv2.GC_INIT_WITH_MASK)
    fg = ndimage.binary_opening((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), iterations=2)
    if drop_neutral:
        soft = (ch <= 9) & (a.min(2) > 110) & fg; lab, n = ndimage.label(soft)
        if n:
            sizes = ndimage.sum(soft, lab, range(1, n + 1)); fg &= ~np.isin(lab, [i + 1 for i, z in enumerate(sizes) if z > fg.size * drop_neutral])
        fg = ndimage.binary_opening(fg, iterations=1)
    elif fill: fg = ndimage.binary_fill_holes(fg)
    lab, n = ndimage.label(fg)
    if n > 1:
        sizes = ndimage.sum(fg, lab, range(1, n + 1)); fg = np.isin(lab, [i + 1 for i, z in enumerate(sizes) if z > sizes.max() * 0.02])
    alpha = Image.fromarray((fg * 255).astype(np.uint8)).resize(im0.size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.6))
    alpha = alpha.point(lambda v: 0 if v < 110 else (255 if v > 170 else int((v - 110) * 255 / 60)))     # pull the edge a pixel inside, keep it soft
    out = im0.convert("RGBA"); out.putalpha(alpha)
    box = alpha.getbbox(); w, h = out.size; q = int(max(w, h) * pad)
    out = out.crop((max(0, box[0] - q), max(0, box[1] - q), min(w, box[2] + q), min(h, box[3] + q)))
    out.thumbnail((1400, 1400))
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / (name + ".webp"); out.save(dst, "WEBP", quality=90, method=6)
    return dst

GRAB = [  # src, name, params — everything shot on a white backdrop with a shadow: boxes, rings, small things
    ("photo/box-gold.jpg", "box-gold", {}),
    ("photo/site/set-tvilli-845-ta-khustky-4444-natkhne-01.jpg", "set-natkhnennia-box", {}),
    ("photo/site/set-tvilli-845-ta-khustky-4444-vpevnen-01.jpg", "set-vpevnenist-box", {}),
    ("photo/site/ring-n-styl-01.jpg", "ring-n", dict(drop_neutral=0.002, fill=False)),
    ("img/scrunchie-pole.webp", "scrunchie-pole", dict(drop_neutral=0.003, fill=False)),
    ("img/sets/twscr-makiv.webp", "twscr-makiv", {}),
    ("img/sets/bookmark-melodiia.webp", "bookmark-melodiia", {}),
    ("img/sets/obruch.webp", "obruch", dict(drop_neutral=0.01, fill=False)),
    ("photo/site/mask-synii-01.jpg", "mask-synii", {}),
    ("img/prob88.webp", "prob88", {}),
    ("img/sets/maskscr-litnie-pole.webp", "maskscr-litnie-pole", dict(drop_neutral=0.004, fill=False)),
    ("photo/hratsiia-flat.webp", "hratsiia-flat", {}),
]

def duo(scarf, ring, name, k=0.4):
    """Scarf with the ring on its corner — one image for «Хустка й кільце» thumbs."""
    a = Image.open(OUT / f"{scarf}.webp").convert("RGBA"); r = Image.open(OUT / f"{ring}.webp").convert("RGBA")
    w = int(a.width * k); r = r.resize((w, int(r.height * w / r.width)), Image.LANCZOS)
    out = Image.new("RGBA", (a.width + w // 3, a.height + r.height // 4), (0, 0, 0, 0)); out.alpha_composite(a, (0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0)); pos = (out.width - w, out.height - r.height)
    sh.paste((0, 0, 0, 70), (pos[0] + 6, pos[1] + 14), r.split()[-1]); out = Image.alpha_composite(out, sh.filter(ImageFilter.GaussianBlur(14)))
    out.alpha_composite(r, pos); out.save(OUT / f"{name}.webp", "WEBP", quality=90, method=6)


# SOLO cut-outs made earlier for the banners
for f in sorted((ROOT / "ads" / "solo" / "src").glob("*-cut.webp")):
    dst = OUT / f.name.replace("-cut.webp", ".webp")
    if not dst.exists(): OUT.mkdir(parents=True, exist_ok=True); shutil.copy(f, dst)

JOBS = [  # src, name, params
    ("img/twilly-zolote.webp", "twilly-zolote", {}),
    ("img/kolo-sontsia.webp", "kolo-sontsia", {}),
    ("photo/scrunchie.jpg", "scrunchie", dict(light=205, sat=24)),
    ("img/sets/pillow-kapuchyno.webp", "pillow-kapuchyno", dict(light=236, sat=10)),
    ("img/sets/bookmark-pidnesennia.webp", "bookmark-pidnesennia", {}),
    ("img/sets/sleep-pidnesennia.webp", "sleep-pidnesennia", dict(light=222, sat=18)),
    ("img/sets/masks-sertsebyttia.webp", "masks-sertsebyttia", dict(light=222, sat=18)),
    ("img/mask-svoboda.webp", "mask-svoboda", {}),
    ("img/mask-vpevnenist.webp", "mask-vpevnenist", {}),
    ("img/sets/pillow-tuman.webp", "pillow-tuman", dict(light=236, sat=10, erode=3)),
    ("img/sets/turban-bilyi.webp", "turban-bilyi", dict(light=244, sat=8)),
    ("img/sets/tw44-natkhnennia.webp", "tw44-natkhnennia", dict(light=222, sat=18)),
    ("img/sets/tw44-vpevnenist.webp", "tw44-vpevnenist", dict(light=222, sat=18)),
    ("img/sets/tw44-zolote.webp", "tw44-zolote", dict(light=222, sat=18)),
    ("img/sets/three-twilly.webp", "three-twilly", dict(light=192, sat=24)),
    ("img/sets/scr3.webp", "scr3", dict(light=192, sat=24)),
    ("photo/site/mask-litnie-pole-01.jpg", "mask-litnie-pole", {}),
]
if __name__ == "__main__":
    for src, name, kw in JOBS:
        if not (ROOT / src).exists(): print("MISSING", src); continue
        d = cut(src, name, **kw); im = Image.open(d)
        al = np.asarray(im.split()[-1]); print(f"{name:24} {im.size} opaque {round((al > 128).mean() * 100)}%")
    for src, name, kw in GRAB:
        d = cut_grab(src, name, **kw); im = Image.open(d)
        al = np.asarray(im.split()[-1]); print(f"{name:24} {im.size} opaque {round((al > 128).mean() * 100)}% (grabcut)")
    duo("hratsiia-flat", "ring-n", "duo-hratsiia-ring")
