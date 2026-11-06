"""Horoshop formats of the chosen home banner (06.11.2026): «Студійний кадр · темний» (home-h-reblum-dark) — the lock-up on
ink, the studio close-up of «Авантюра» to the right, and the ink melting into the picture without a hard edge. Sizes from the client's spec
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

RB = "src/reblum-avantiura-2k.webp"      # the studio close-up of «Авантюра» (home-h-reblum-dark)
def photo(left, feather, pos):
    """The frame from `left` to the right edge, feathered into the ink over `feather` px (mask) with a dark veil over the
    same zone on top — no hard edge between the field and the picture (the client, 06.11)."""
    return (f'<div class="ph" style="left:{left}px;right:0;top:0;bottom:0;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 {feather}px);mask-image:linear-gradient(90deg,transparent 0,#000 {feather}px)"><img src="{RB}" alt="" style="object-position:{pos}"></div>'
            f'<div style="left:{left}px;top:0;bottom:0;width:{int(feather * 1.5)}px;background:linear-gradient(90deg,{INK} 0,rgba(20,17,16,.6) 40%,rgba(20,17,16,0) 100%)"></div><div class="scrim-d"></div>')
def lock_scaled(k):
    inner = lock().replace('<div class="lock">', '<div class="lock" style="position:absolute">')
    return f'<div style="left:0;top:0;bottom:0;width:900px;transform:scale({k});transform-origin:0 50%">{inner}</div>'

# Desktop LINE 1 (and the inner-page top, scaled): the lock-up on ink, the close-up to the right edge, a soft blend between
ad("hs-desktop-line1", 1920, 576, f"""
  <div style="inset:0;background:{INK}"></div>
  {photo(680, 540, "40% 36%")}
  {lock()}""", note="Desktop LINE 1 · 3840 × 1152 at DPR 2")

# Mobile LINE 1 · 5:2: the same, the lock-up a fifth larger for the small screen
ad("hs-mobile-line1", 1920, 768, f"""
  <div style="inset:0;background:{INK}"></div>
  {photo(740, 560, "40% 38%")}
  {lock_scaled(1.2)}""", note="Mobile LINE 1 · 3840 × 1536 at DPR 2")

# LINE 2 / LINE 3 (desktop and mobile) · 5:3 at its own size
ad("hs-line2", 1440, 864, f"""
  <div style="inset:0;background:{INK}"></div>
  {photo(500, 500, "42% 40%")}
  {lock()}""", note="LINE 2 / LINE 3 · 1440 × 864")

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
