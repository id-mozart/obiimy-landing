"""Responsive image helper: generates WebP variants next to the source and emits <img> with srcset."""
import pathlib, re
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent.parent
WIDTHS = (480, 800, 1200)
_cache = {}

def variants(src):
    """Return (list of (path, width), (w, h) of original)."""
    if src in _cache: return _cache[src]
    p = ROOT / src
    im = Image.open(p); w, h = im.size
    stem = p.with_suffix("")
    out = []
    for tw in WIDTHS:
        if tw >= w: continue
        vp = pathlib.Path(f"{stem}-{tw}.webp")
        if not vp.exists():
            v = im.convert("RGB"); v.thumbnail((tw, tw * 4)); v.save(vp, "WEBP", quality=80, method=6)
        out.append((str(vp.relative_to(ROOT)), tw))
    out.append((src, w))
    _cache[src] = (out, (w, h)); return _cache[src]

def img(src, alt, sizes="100vw", lazy=True, cls="", extra="", eager_priority=False, style=""):
    vs, (w, h) = variants(src)
    srcset = ", ".join(f"{p} {tw}w" for p, tw in vs)
    mid = next((p for p, tw in vs if tw >= 800), vs[-1][0])
    attrs = [f'src="{mid}"', f'srcset="{srcset}"', f'sizes="{sizes}"', f'width="{w}"', f'height="{h}"', f'alt="{alt}"']
    if lazy: attrs.append('loading="lazy" decoding="async"')
    if eager_priority: attrs.append('fetchpriority="high"')
    if cls: attrs.append(f'class="{cls}"')
    if style: attrs.append(f'style="{style}"')
    if extra: attrs.append(extra)
    return "<img " + " ".join(attrs) + ">"

NBSP, THIN = "\u00a0", "\u202f"
def typo(html):
    """Non-breaking spaces in prices, sizes, units and phone numbers — text only, never inside <style>/<script>."""
    parts = re.split(r'(<style[\s\S]*?</style>|<script[\s\S]*?</script>)', html)
    return "".join(p if p.startswith("<style") or p.startswith("<script") else _typo_text(p) for p in parts)

def _typo_text(html):
    html = html.replace("+38 067 010 85 25", "+38" + NBSP + "067" + NBSP + "010" + NBSP + "85" + NBSP + "25")
    html = re.sub(r'(?<=\d) (?=\d{3}(?!\d))', THIN, html)
    html = re.sub(r'(\d) × (\d)', lambda m: m.group(1) + NBSP + "×" + NBSP + m.group(2), html)
    html = re.sub(r'(\d) (грн|см|шт\.|°C)', lambda m: m.group(1) + NBSP + m.group(2), html)
    html = re.sub(r'(до|від|з) (\d)', lambda m: m.group(1) + NBSP + m.group(2), html)
    return html
