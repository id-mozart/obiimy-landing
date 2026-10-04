# -*- coding: utf-8 -*-
"""Still-life compositing helpers for the page-3 concepts (PIL + numpy + scipy + cv2).
Everything is real photography / existing cutouts: only cropping, white-point normalisation,
rotation, scaling and soft shadows are applied."""
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as ndi

ROOT = '/Users/ivan/obiimy/'
OUT = '/private/tmp/claude-501/-Users-ivan-obiimy/9336a79c-fcae-4a0e-a194-062adfde257a/scratchpad/ad-luxury/'
PPI = 200.0
MM = PPI / 25.4          # px per mm
PAPER = (241, 239, 234)  # #F1EFEA


def load(path):
    return Image.open(path if path.startswith('/') else ROOT + path)


def norm_white(img, chroma_thr=14, lum_thr=205, dilate=55, sigma=110, gain=1/0.975, feather=0, keep_edges=''):
    """Photo on an off-white backdrop -> same photo with the backdrop lifted to pure white.
    Backdrop is estimated locally (normalised convolution over backdrop-only pixels) with a quadratic
    fit as fallback, so real contact shadows survive while the studio gradient disappears.
    Returns float array 0..1 (H,W,3)."""
    a = np.asarray(img.convert('RGB')).astype(np.float32)
    H, W = a.shape[:2]
    mx, mn = a.max(2), a.min(2)
    lum = a.mean(2)
    fg = ((mx - mn) > chroma_thr) | (lum < lum_thr)
    fg = ndi.binary_opening(fg, iterations=1)
    fg = ndi.binary_dilation(fg, iterations=dilate)
    bgm = (~fg).astype(np.float32)
    ys, xs = np.nonzero(~fg)
    sel = np.random.RandomState(1).choice(len(ys), size=min(40000, len(ys)), replace=False)
    y, x = ys[sel] / H, xs[sel] / W
    A = np.stack([np.ones_like(x), x, y, x * x, x * y, y * y], 1)
    yy, xx = np.mgrid[0:H, 0:W]
    yy, xx = yy / H, xx / W
    tf = [np.ones_like(xx), xx, yy, xx * xx, xx * yy, yy * yy]
    den = ndi.gaussian_filter(bgm, sigma)
    wloc = np.clip(den / 0.08, 0, 1)
    out = np.empty_like(a)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, a[ys[sel], xs[sel], c], rcond=None)
        poly = np.clip(sum(k * t for k, t in zip(coef, tf)), 150, 255)
        loc = ndi.gaussian_filter(a[..., c] * bgm, sigma) / np.maximum(den, 1e-4)
        bg = wloc * loc + (1 - wloc) * poly
        out[..., c] = a[..., c] / np.clip(bg, 150, 255)
    # hue-preserving: never clip a single channel (keeps the box yellow warm instead of lemon)
    out = out / np.maximum(out.max(2, keepdims=True), 1.0)
    # last 2.5 % lift only for near-white pixels, so the backdrop becomes exact white
    mnc = out.min(2, keepdims=True)
    w = np.clip((mnc - 0.86) / 0.09, 0, 1); w = w * w * (3 - 2 * w)
    out = np.clip(out * (1 + w * (gain - 1)), 0, 1)
    if feather:
        w = np.ones((H, W), np.float32)
        r = np.linspace(0, 1, feather, dtype=np.float32) ** 1.5
        if 'l' not in keep_edges: w[:, :feather] *= r[None, :]
        if 'r' not in keep_edges: w[:, -feather:] *= r[::-1][None, :]
        if 't' not in keep_edges: w[:feather, :] *= r[:, None]
        if 'b' not in keep_edges: w[-feather:, :] *= r[::-1][:, None]
        out = 1 - (1 - out) * w[..., None]
    return out


def to_img(f):
    return Image.fromarray((np.clip(f, 0, 1) * 255 + .5).astype(np.uint8))


class Canvas:
    def __init__(self, w_mm, h_mm, color=PAPER, ppi=PPI):
        self.ppi = ppi
        self.mm = ppi / 25.4
        self.w, self.h = int(round(w_mm * self.mm)), int(round(h_mm * self.mm))
        self.color = np.array(color, np.float32) / 255
        self.a = np.ones((self.h, self.w, 3), np.float32) * self.color

    # --- real photo with white backdrop: multiply onto the canvas (natural shadows stay) ---
    def multiply(self, f, x_mm, y_mm, w_mm, rot=0):
        im = to_img(f)
        if rot:
            im = im.rotate(rot, resample=Image.BICUBIC, expand=True, fillcolor=(255, 255, 255))
        w = int(round(w_mm * self.mm)); h = int(round(im.height * w / im.width))
        im = im.resize((w, h), Image.LANCZOS)
        self._blend(np.asarray(im).astype(np.float32) / 255, None, int(round(x_mm * self.mm)), int(round(y_mm * self.mm)), mode='mul')
        return w / self.mm, h / self.mm

    # --- cutout (RGBA) with a soft two-part shadow: contact + ambient ---
    def cutout(self, rgba, x_mm, y_mm, w_mm, rot=0, sh=(1.2, 1.6, 2.2, .26), amb=(0.4, 0.6, 5.0, .10), shadow_rgb=(40, 30, 20)):
        im = rgba.convert('RGBA')
        if rot:
            im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
        w = int(round(w_mm * self.mm)); h = int(round(im.height * w / im.width))
        im = im.resize((w, h), Image.LANCZOS)
        arr = np.asarray(im).astype(np.float32) / 255
        rgb, al = arr[..., :3], arr[..., 3]
        x0, y0 = int(round(x_mm * self.mm)), int(round(y_mm * self.mm))
        pad = int(14 * self.mm)
        alp = np.pad(al, pad)
        for (dx, dy, blur, op) in (amb, sh):
            if op <= 0: continue
            s = ndi.gaussian_filter(alp, blur * self.mm)
            s = ndi.shift(s, (dy * self.mm, dx * self.mm), order=1, mode='constant')
            col = np.ones(s.shape + (3,), np.float32) * (np.array(shadow_rgb, np.float32) / 255)
            self._blend(col, s * op, x0 - pad, y0 - pad, mode='over')
        self._blend(rgb, al, x0, y0, mode='over')
        return w / self.mm, h / self.mm

    def _blend(self, rgb, alpha, x0, y0, mode='over'):
        h, w = rgb.shape[:2]
        cx0, cy0 = max(x0, 0), max(y0, 0)
        cx1, cy1 = min(x0 + w, self.w), min(y0 + h, self.h)
        if cx1 <= cx0 or cy1 <= cy0: return
        sx0, sy0 = cx0 - x0, cy0 - y0
        src = rgb[sy0:sy0 + cy1 - cy0, sx0:sx0 + cx1 - cx0]
        dst = self.a[cy0:cy1, cx0:cx1]
        if mode == 'mul':
            dst *= src
        else:
            al = alpha[sy0:sy0 + cy1 - cy0, sx0:sx0 + cx1 - cx0][..., None]
            dst[:] = dst * (1 - al) + src * al

    def save(self, name, q=92):
        im = to_img(self.a)
        if name.endswith('.png'):
            im.save(OUT + name, optimize=True)
        else:
            im.save(OUT + name, quality=q, subsampling=0)
        return im


def trim(rgba, thr=8):
    a = np.asarray(rgba.convert('RGBA'))
    ys, xs = np.nonzero(a[..., 3] > thr)
    return rgba.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def defringe(rgba, band=7, sat_thr=0.16, lum_thr=0.62, erode=1):
    """Remove the light, colourless rim (baked white backdrop / shadow) from a cutout's edge band."""
    a = np.asarray(rgba.convert('RGBA')).astype(np.float32) / 255
    rgb, al = a[..., :3], a[..., 3].copy()
    solid = al > 0.5
    inner = ndi.binary_erosion(solid, iterations=band)
    edge = (al > 0.02) & ~inner
    mx, mn = rgb.max(2), rgb.min(2)
    sat = (mx - mn) / np.maximum(mx, 1e-3)
    bad = edge & (sat < sat_thr) & (rgb.mean(2) > lum_thr)
    # only rim pixels that are connected to the outside count as fringe
    out = ~solid
    grow = ndi.binary_dilation(out, iterations=1)
    for _ in range(band + 2):
        nxt = ndi.binary_dilation(grow, iterations=1) & (bad | out)
        if (nxt == grow).all(): break
        grow = nxt
    al[grow & bad] = 0
    if erode:
        al = ndi.minimum_filter(al, size=2 * erode + 1)
    al = ndi.gaussian_filter(al, 0.6)
    a[..., 3] = al
    return Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))


class Layer:
    """Transparent page-size layer (RGBA, straight alpha) for objects + shadows that must sit on a CSS colour."""
    def __init__(self, w_mm, h_mm, ppi=PPI):
        self.mm = ppi / 25.4
        self.w, self.h = int(round(w_mm * self.mm)), int(round(h_mm * self.mm))
        self.c = np.zeros((self.h, self.w, 3), np.float32)   # premultiplied colour
        self.al = np.zeros((self.h, self.w), np.float32)

    def _over(self, rgb, alpha, x0, y0):
        h, w = alpha.shape
        cx0, cy0 = max(x0, 0), max(y0, 0)
        cx1, cy1 = min(x0 + w, self.w), min(y0 + h, self.h)
        if cx1 <= cx0 or cy1 <= cy0: return
        sx0, sy0 = cx0 - x0, cy0 - y0
        s = rgb[sy0:sy0 + cy1 - cy0, sx0:sx0 + cx1 - cx0]
        a = alpha[sy0:sy0 + cy1 - cy0, sx0:sx0 + cx1 - cx0]
        self.c[cy0:cy1, cx0:cx1] = s * a[..., None] + self.c[cy0:cy1, cx0:cx1] * (1 - a[..., None])
        self.al[cy0:cy1, cx0:cx1] = a + self.al[cy0:cy1, cx0:cx1] * (1 - a)

    def cutout(self, rgba, x_mm, y_mm, w_mm, rot=0, sh=(0.35, 0.7, 1.1, .30), amb=(0.2, 0.9, 4.2, .11), shadow_rgb=(40, 30, 20)):
        im = rgba.convert('RGBA')
        if rot:
            im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
        w = int(round(w_mm * self.mm)); h = int(round(im.height * w / im.width))
        im = im.resize((w, h), Image.LANCZOS)
        arr = np.asarray(im).astype(np.float32) / 255
        rgb, al = arr[..., :3], arr[..., 3]
        x0, y0 = int(round(x_mm * self.mm)), int(round(y_mm * self.mm))
        pad = int(14 * self.mm)
        alp = np.pad(al, pad)
        for (dx, dy, blur, op) in (amb, sh):
            if op <= 0: continue
            s = ndi.gaussian_filter(alp, blur * self.mm)
            s = ndi.shift(s, (dy * self.mm, dx * self.mm), order=1, mode='constant')
            col = np.ones(s.shape + (3,), np.float32) * (np.array(shadow_rgb, np.float32) / 255)
            self._over(col, s * op, x0 - pad, y0 - pad)
        self._over(rgb, al, x0, y0)
        return w / self.mm, h / self.mm

    def save(self, name):
        rgb = self.c / np.maximum(self.al[..., None], 1e-4)
        out = np.dstack([np.clip(rgb, 0, 1), np.clip(self.al, 0, 1)])
        im = Image.fromarray((out * 255 + .5).astype(np.uint8))
        im.save(OUT + name, optimize=True)
        return im

    def preview(self, name, bg):
        rgb = self.c + (1 - self.al[..., None]) * (np.array(bg, np.float32) / 255)
        to_img(rgb).save(OUT + name, quality=88)
