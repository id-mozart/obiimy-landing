"""Horoshop formats of the chosen home banner (06.11.2026). The client picked «Сім портретів · папір» (home-t3) and asked for
the left part — the field under the lock-up — to be dark; the seven portraits stay on paper. Sizes from the client's spec
(Google Doc «Розміри банерів для інтернет-магазину Хорошоп»): Desktop LINE 1 3840 × 1152 (10:3), Desktop/Mobile LINE 2–3
1440 × 864 (5:3), Mobile LINE 1 3840 × 1536 (5:2), inner pages top 2880 × 864 (10:3, the desktop art scaled).
Wide frames are drawn at 1920 px and rendered at DPR 2; the 5:3 frame is drawn at its own size.
  python3 solo/build_horoshop.py                      → solo/horoshop.html
  DPR=2 VW=2000 ADS=solo/horoshop.html OUT=solo/out-horoshop ONLY=hs-desktop,hs-mobile node render.mjs
  DPR=1 VW=2000 ADS=solo/horoshop.html OUT=solo/out-horoshop ONLY=hs-line2 node render.mjs
  python3 solo/build_horoshop.py finish               → solo/out-horoshop/final/*.jpg|webp (named by placement and size)"""
import pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import build_home as HB
from build_home import HEAD, lock, tiles7

INK, PAPER = "#141110", "#F0EBE1"
ads = []
def ad(id, w, h, body, note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad" id="{id}" style="width:{w}px;height:{h}px">{body}\n</section>')

# Desktop LINE 1 (and the inner-page top, scaled): the t3 strip, the lock-up's field dark, the portraits on paper
ad("hs-desktop-line1", 1920, 576, f"""
  <div style="inset:0;background:{PAPER}"></div>
  <div style="left:0;top:0;bottom:0;width:630px;background:{INK}"></div>
  {tiles7(690, 1840, 44, 532, names=True, states=True, dark=False)}
  {lock()}""", note="Desktop LINE 1 · 3840 × 1152 at DPR 2")

def band(h, kick=40, solo=150, pill=34, pad=80):
    """A horizontal lock-up for the stacked frames: «Колекція · Шлях до себе» over «Соло», the yellow pill at the right."""
    return (f'<div style="position:absolute;left:{pad}px;top:0;height:{h}px;display:flex;flex-direction:column;justify-content:center;text-transform:uppercase;line-height:1">'
            f'<p style="font-size:{kick}px;font-weight:400;letter-spacing:.06em">Колекція · Шлях до себе</p>'
            f'<p style="font-size:{solo}px;font-weight:300;letter-spacing:0;margin:{int(solo*.08)}px 0 0 -{int(solo*.05)}px">Соло</p></div>'
            f'<p class="pill" style="position:absolute;right:{pad}px;top:50%;margin:0;transform:translateY(-50%);font-size:{pill}px;padding:{int(pill*.75)}px {int(pill*1.3)}px">Жіноча сила крізь десятиліття</p>')

def band_wrap(h, inner): return f'<div style="left:0;right:0;top:0;height:{h}px;background:{INK}">{inner}</div>'

# Mobile LINE 1 · 5:2: the dark band with the lock-up on top, the seven portraits with names on paper under it
ad("hs-mobile-line1", 1920, 768, f"""
  <div style="inset:0;background:{PAPER}"></div>
  {band_wrap(330, band(330, kick=40, solo=160, pill=34))}
  {tiles7(80, 1840, 362, 742, gap=12, names=True, dark=False, name_size=26)}""", note="Mobile LINE 1 · 3840 × 1536 at DPR 2")

# LINE 2 / LINE 3 (desktop and mobile) · 5:3 at its own size
ad("hs-line2", 1440, 864, f"""
  <div style="inset:0;background:{PAPER}"></div>
  {band_wrap(330, band(330, kick=32, solo=130, pill=26, pad=64))}
  {tiles7(64, 1376, 366, 830, gap=12, names=True, dark=False, name_size=24)}""", note="LINE 2 / LINE 3 · 1440 × 864")

if "finish" in sys.argv:
    from PIL import Image
    src = HERE / "out-horoshop"; out = src / "final"; out.mkdir(exist_ok=True)
    plan = [("hs-desktop-line1", "solo-desktop-line1-3840x1152", (3840, 1152)), ("hs-desktop-line1", "solo-inner-top-2880x864", (2880, 864)),
            ("hs-mobile-line1", "solo-mobile-line1-3840x1536", (3840, 1536)), ("hs-line2", "solo-line2-line3-1440x864", (1440, 864))]
    for id, name, size in plan:
        im = Image.open(src / f"{id}.jpg").convert("RGB")
        if im.size != size: im = im.resize(size, Image.LANCZOS)
        im.save(out / f"{name}.jpg", "JPEG", quality=90, optimize=True, progressive=True)
        im.save(out / f"{name}.webp", "WEBP", quality=86, method=6)
        print(name, im.size, (out / f"{name}.jpg").stat().st_size // 1024, "KB jpg", (out / f"{name}.webp").stat().st_size // 1024, "KB webp")
else:
    (HERE / "horoshop.html").write_text(HEAD.replace("SOLO home banners", "SOLO · Horoshop formats") + "".join(ads) + "\n</body></html>")
    print(len(ads), "horoshop frames")
