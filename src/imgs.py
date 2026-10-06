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
        if not vp.exists() or vp.stat().st_mtime < p.stat().st_mtime:
            v = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB"); v.thumbnail((tw, tw * 4)); v.save(vp, "WEBP", quality=82, method=6)   # cut-outs keep their transparency
        out.append((str(vp.relative_to(ROOT)), tw))
    out.append((src, w))
    _cache[src] = (out, (w, h)); return _cache[src]

def wide(src, ext=1000, bottom=None, patch=(10, 200, 120, 700), seed=1):
    """A studio portrait continued to the left by its own backdrop (ext px of the median colour of `patch`, a faint top-to-bottom
    light fall-off, a soft 160 px join, a touch of grain) → <stem>-wide.jpg beside the source. For full-bleed landscape slots
    where the text stands on the left: nothing is invented but plain backdrop. bottom — crop the source to this height first."""
    import numpy as np
    srcp = ROOT / src; dst = srcp.with_name(srcp.stem + "-wide.jpg")
    if dst.exists() and dst.stat().st_mtime >= srcp.stat().st_mtime: return str(dst.relative_to(ROOT))
    im = Image.open(srcp).convert("RGB"); W, H = im.size
    if bottom: im = im.crop((0, 0, W, bottom)); H = bottom
    a = np.asarray(im).astype(np.float32); bg = np.median(a[patch[1]:patch[3], patch[0]:patch[2]].reshape(-1, 3), 0)
    g = np.linspace(1.015, 0.985, H)[:, None, None]
    out = np.ones((H, ext + W, 3), np.float32) * bg; out[:, :ext] *= g; out[:, ext:] = a
    n = 160; t = np.linspace(0, 1, n); w = (t * t * (3 - 2 * t))[None, :, None]
    out[:, ext:ext + n] = out[:, ext:ext + n] * w + (np.ones((H, n, 3)) * bg * g) * (1 - w)
    out[:, :ext] += np.random.default_rng(seed).normal(0, 1.2, (H, ext, 3))
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(dst, quality=90, subsampling=0)
    return str(dst.relative_to(ROOT))

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
    """Non-breaking spaces in prices, sizes, units, phone numbers, after short prepositions and before a dash — text only, never inside <style>/<script>."""
    parts = re.split(r'(<style[\s\S]*?</style>|<script[\s\S]*?</script>)', html)
    return "".join(p if p.startswith("<style") or p.startswith("<script") else _typo_text(p) for p in parts)

def _typo_text(html):
    html = html.replace("+38 067 010 85 25", "+38" + NBSP + "067" + NBSP + "010" + NBSP + "85" + NBSP + "25")
    html = html.replace("+38 073 925 99 49", "+38" + NBSP + "073" + NBSP + "925" + NBSP + "99" + NBSP + "49")
    html = re.sub(r'(?<=\d) (?=\d{3}(?!\d))', THIN, html)
    html = re.sub(r'(\d) × (\d)', lambda m: m.group(1) + NBSP + "×" + NBSP + m.group(2), html)
    html = re.sub(r'(\d) (грн|см|шт\.|°C)', lambda m: m.group(1) + NBSP + m.group(2), html)
    html = re.sub(r'(до|від|з) (\d)', lambda m: m.group(1) + NBSP + m.group(2), html)
    # short words stay with the next one, a dash stays with the previous one: no hanging prepositions, no line starting with «—»
    html = re.sub(r"(?<![\w’'-])([ВвУуІіЙйЗзАаОо]|[Нн]а|[Дд]о|[Зз]а|[Нн]е|[Щщ]о|[Чч]и|[Тт]а|[Пп]о|[Іі]з|[Зз]і|[Яя]к|[Вв]ід|[Дд]ля|[Бб]ез|[Пп]ід|[Пп]ро|[Пп]ри) (?=[^\s<])", lambda m: m.group(1) + NBSP, html)
    html = re.sub(r'(?<=[^\s>]) — ', NBSP + '— ', html)
    # names do not break: «Літній віночок», UFD London, вул. Петра Сагайдачного, 12; opening hours stay with their days
    html = re.sub(r'«([^»<>]{3,26})»', lambda m: '«' + m.group(1).replace(' ', NBSP) + '»', html)
    for name in ("UFD London", "Be Brave", "INSIDER UA", "вул. Петра Сагайдачного, 12", "Світлани Сніжко", "Нова пошта", "Новою поштою", "Нового року", "святого Миколая"):
        html = html.replace(name, name.replace(' ', NBSP))
    html = re.sub(r'(пн–пт|сб|нд) (\d)', lambda m: m.group(1) + NBSP + m.group(2), html)
    html = re.sub(r'(?<=\d) ([+=]) (?=\d)', lambda m: NBSP + m.group(1) + NBSP, html)      # 2 400 + 450 = 2 850
    html = html.replace("айстер-клас", "айстер-\u2060клас")                                # no break after the hyphen
    html = re.sub(r'(?<=[\dа-яіїє])–(?=[\dа-яіїє])', '–\u2060', html)          # 1 000–4 000, пн–пт, 10:00–18:00 stay on one line
    return html
