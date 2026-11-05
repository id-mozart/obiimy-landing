"""Gift-set creatives, third series (05.11.2026, client: «менее артовые — больше акцента просто на фото наборов»): one photograph
of the set as large as the frame allows, no veils, no labels, no decoration — the logo line, one short headline, the product row.
White packshots sit on a white field (the field is the photo); every other photograph bleeds to the edges down to an ink band
that carries the headline and the row. 1080×1920 plain plus story / feed / square via FORMAT. Photos: photo/site (obiimy.world);
prices and names from review/SITE-FACTS.md (19.10.2026). Output: sets3[-<format>].html → out-sets3[-<format>]/*.jpg
(cd ads && ADS=solo/sets3.html OUT=solo/out-sets3 node render.mjs)."""
import os, pathlib, re, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit import nb, LOGO_W, LOGO_K, GRAIN

def nbh(text):
    text = re.sub(r"(?<![\w’'])(у|в|з|і|й|а|о|на|до|за|та|не|чи|із|зі|від|для|що|як|це)\s+(?=[^\s<])", lambda m: m.group(1) + " ", text, flags=re.I)
    return re.sub(r"\s+([—–])", lambda m: " " + m.group(1), text)

FORMAT = os.environ.get("FORMAT", "plain")   # plain | story | feed | square
H = {"feed": 1350, "square": 1080}.get(FORMAT, 1920)
K = .72 if FORMAT == "square" else (.86 if FORMAT == "feed" else 1)
SHORT = FORMAT in ("feed", "square")          # the short frames; a story is as tall as the banner, only its safe zones differ
TOPL = 250 if FORMAT == "story" else 58
BOTB = 340 if FORMAT == "story" else 60
ROW = int(170 * K)                            # the product row
Y0 = TOPL + int(100 * K)                      # content starts under the logo line
Y1 = H - BOTB - ROW - int(36 * K)             # and ends above the product row
PH = "../../photo/site/"
YEL, INK, PAPER, CREAM, WHITE = "#F2B705", "#141110", "#F1E8D8", "#F3EADB", "#FFFFFF"

CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #555; font-family: 'Onest', Arial, sans-serif; -webkit-font-smoothing: antialiased; }
.ad { width: 1080px; height: HPXpx; position: relative; overflow: hidden; background: #141110; margin: 20px auto; color: #F3EADB; }
.ad > * { position: absolute; margin: 0; }
.ad p { margin: 0; }
.ad::after { content: ""; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: .22; mix-blend-mode: soft-light; background-image: GRAIN; }
.ph { overflow: hidden; } .ph img { width: 100%; height: 100%; object-fit: cover; display: block; }
.fit img { object-fit: contain; }
.mult img { mix-blend-mode: multiply; }   /* a white packshot on the white field: its edges vanish */
.big { font-family: 'Montserrat', sans-serif; font-weight: 400; font-style: normal; line-height: 1.08; letter-spacing: 0; text-wrap: balance; }   /* 05.11: the brand's light grotesque instead of the heavy italic */
.small { font-family: 'EB Garamond', 'Cormorant Garamond', serif; font-weight: 500; line-height: 1.16; text-wrap: pretty; }
.kicker { font-family: 'Montserrat', sans-serif; font-weight: 500; text-transform: uppercase; letter-spacing: .18em; color: #E0B040; white-space: nowrap; }
.hdr { font-family: Montserrat, sans-serif; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; white-space: nowrap; }
.cta { font-family: 'Onest'; font-weight: 600; border-radius: 999px; background: #F2B705; color: #141216; white-space: nowrap; flex: none; }
.plate { display: flex; align-items: center; border-radius: 20px; flex: 0 1 auto; min-width: 0; }
.plate .nm { font-weight: 600; line-height: 1.1; text-wrap: balance; }
.plate .pr { font-family: 'Montserrat', sans-serif; font-weight: 400; line-height: 1; margin-top: 8px; }
.ink { color: #1B1613; } .ink .kicker { color: #8A6A12; }
.card { background: #fff; box-shadow: 0 30px 60px -20px rgba(20,12,6,.5), 0 4px 10px rgba(20,12,6,.16); }
.card img { width: 100%; height: 100%; object-fit: cover; display: block; }
.cap { font-size: CAPpx; line-height: 1.2; }
.cap b { font-family: 'Montserrat', sans-serif; font-weight: 500; color: #F2B705; white-space: nowrap; }
""".replace("GRAIN", GRAIN).replace("HPX", str(H)).replace("CAP", str(int(24 * K)))

ads = []
def ad(id, body, note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad" id="{id}">{body}\n</section>')

def header(dark=True):
    col = CREAM if dark else "#1B1613"
    return (f'<img src="{LOGO_W if dark else LOGO_K}" alt="" style="left:64px;top:{TOPL}px;height:{int(58 * K)}px;z-index:5">'
            f'<p class="hdr" style="right:64px;top:{TOPL + int(18 * K)}px;font-size:{int(26 * K)}px;color:{col};z-index:5">Авторські шовкові вироби</p>')

def plate(title, price, cta="Обрати набір", dark=True, ink_cta=False):
    """The product row at the bottom: the set's name, the retail price; the yellow button to the right. No thumbnails — no cut-outs."""
    bg, bd, fg = ("rgba(243,234,219,.1)", "1.5px solid rgba(243,234,219,.3)", CREAM) if dark else ("rgba(27,22,19,.06)", "1.5px solid rgba(27,22,19,.18)", "#1B1613")
    return f'''
  <div style="left:64px;right:64px;bottom:{BOTB}px;display:flex;align-items:center;justify-content:space-between;gap:{int(24 * K)}px;z-index:6">
    <div class="plate" style="padding:{int(14 * K)}px {int(28 * K)}px;background:{bg};border:{bd};color:{fg}">
      <div style="min-width:0"><p class="nm" style="font-size:{int(27 * K)}px">{nb(title)}</p><p class="pr" style="font-size:{int(44 * K)}px">{price}</p></div></div>
    <div class="cta" style="font-size:{int(40 * K)}px;padding:{int(32 * K)}px {int(58 * K)}px;{"background:#141110;color:#F3EADB" if ink_cta else ""}">{cta}</div>
  </div>'''

def words(kicker, big, small, size, ink=False, width=None):
    sc = "#4B423B" if ink else "#D9CDB9"
    w = f"max-width:{width}px;" if width else ""
    return (f'<p class="kicker" style="font-size:{int(26 * K)}px">{kicker}</p>'
            f'<p class="big" style="font-size:{int(size * K)}px;margin-top:{int(16 * K)}px;{w}">{nbh(big)}</p>'
            + (f'<p class="small" style="font-size:{int(38 * K)}px;margin-top:{int(20 * K)}px;color:{sc};{w}">{nb(small)}</p>' if small else ""))

def ink_band():
    return f'<div style="left:0;right:0;bottom:0;height:{BOTB + ROW + int(24 * K)}px;background:{INK}"></div>'


# ─── the one template ──────────────────────────────────────────────────────────────────────────────────────────────────

def border_color(photo):
    """The median colour of a photograph's border — the frame is painted with it, so a photo shown whole seems to continue."""
    from PIL import Image
    im = Image.open(HERE.parent.parent / "photo/site" / f"{photo}.jpg").convert("RGB"); w, h = im.size; b = max(3, w // 40)
    px = []
    for box in [(0, 0, w, b), (0, h - b, w, h), (0, 0, b, h), (w - b, 0, w, h)]: px += list(im.crop(box).getdata())
    px.sort(key=sum); r, g, bl = px[len(px) // 2]
    return f"#{r:02x}{g:02x}{bl:02x}"

def simple(id, photo, pos, big, product, note="", white=False, zoom=1.0, ar=1.0, kicker="Подарунковий набір", fit=False):
    """The set and nothing else. White packshot: a white frame, the headline under the logo, the photo fills the rest, the row is light.
    fit: the photograph shown whole at full width on a field of its own border colour. Otherwise it bleeds to the edges.
    An ink band at the bottom holds the headline and the row."""
    size = int((52 if SHORT else 60) * K)
    if white:
        top = Y0 + int(110 * K)
        ph_h = Y1 - top; ph_w = min(1080, int(ph_h * ar))
        if ph_w < int(ph_h * ar): ph_h = int(ph_w / ar)
        px = (1080 - ph_w) // 2
        body = f"""
  <div style="inset:0;background:{WHITE}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0}px;z-index:5"><p class="kicker" style="font-size:{int(24 * K)}px">{kicker}</p><p class="big" style="font-size:{size}px;margin-top:{int(10 * K)}px">{nbh(big)}</p></div>
  <div class="ph mult" style="left:{px}px;top:{top}px;width:{ph_w}px;height:{ph_h}px"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  <div style="inset:0;background:#F2EADC;mix-blend-mode:multiply;z-index:2"></div>
  {plate(*product, dark=False)}"""
    else:
        band = BOTB + ROW + int(150 * K)
        if fit:
            fill = border_color(photo); top = TOPL + int(80 * K)
            pic = f'<div style="inset:0;background:{fill}"></div><div class="ph fit" style="left:0;right:0;top:{top}px;height:{H - band - top}px"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos};transform:scale({zoom})"></div>'
            top_fade = ""
            hdr = header(dark=False)
        else:
            pic = f'<div class="ph" style="left:0;right:0;top:0;height:{H - band + int(2 * K)}px"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos};transform:scale({zoom})"></div>'
            top_fade = f'<div style="left:0;right:0;top:0;height:{int(200 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,.38),rgba(12,9,8,0))"></div>'
            hdr = header()
        body = f"""
  <div style="inset:0;background:{INK}"></div>
  {pic}
  {top_fade}
  {hdr}
  <div style="left:0;right:0;bottom:0;height:{band}px;background:{INK}"></div>
  <div style="left:64px;right:64px;top:{H - band + int(30 * K)}px"><p class="kicker" style="font-size:{int(24 * K)}px">{kicker}</p><p class="big" style="font-size:{size}px;margin-top:{int(8 * K)}px">{nbh(big)}</p></div>
  {plate(*product)}"""
    ad(id, body, note)

# ─── sixteen ───────────────────────────────────────────────────────────────────────────────────────────────────────────

simple("p01-natkhnennia", "set-tvilli-845-ta-khustky-4444-natkhne-01", "50% 50%", "Твіллі + хустка «Натхнення»", ("Твіллі 84 × 5 + хустка 44 × 44", "3 100 грн"), "the Natkhnennia box, whole", fit=True, zoom=1.15)
simple("p02-smilyvist", "set-smilyvist-01", "50% 50%", "Твіллі + резинка «Сміливість»", ("Твіллі + резинка, у коробці", "2 200 грн"), "white packshot", white=True, zoom=1.08)
simple("p03-sleep-28", "set-maska-rezynka-28-01", "50% 50%", "Набір для сну «Літнє поле»", ("Маска для сну + резинка", "3 280 грн"), "white packshot", white=True, zoom=1.1)
simple("p04-vpevnenist", "set-tvilli-845-ta-khustky-4444-vpevnen-01", "50% 50%", "Твіллі + хустка «Впевненість»", ("Твіллі 84 × 5 + хустка 44 × 44", "3 100 грн"), "the red box, whole", fit=True, zoom=1.15)
simple("p05-three-twilly-13", "set-3-shovkovykh-tvilli-13", "50% 50%", "Набір із трьох твіллі", ("Три твіллі 84 × 5, принти на вибір", "4 650 грн"), "white packshot, portrait", white=True, ar=1060 / 1500)
simple("p06-melodiia", "set-maska-zakladka-rezynka-melodiia-01", "50% 50%", "Набір «Мелодія двох»", ("Маска, закладка для книги, резинка", "4 080 грн"), "white packshot", white=True, zoom=1.1)
simple("p07-hearts", "set-masok-dlia-snu-sertsebyttia-chervo-01", "50% 50%", "Набір масок «Серцебиття»", ("Дві маски для сну: червона та чорна", "4 200 грн"), "white packshot, portrait", white=True, ar=1250 / 1500)
simple("p08-sun-sleep", "set-ta-rezynka-litnie-pole-04", "50% 50%", "Набір для сну «Літнє поле»", ("Маска для сну + резинка", "3 280 грн"), "sunlit flat-lay, bleed")
simple("p09-nizhnist", "set-tvilli-845-ta-khustky-4444-nizhnis-01", "50% 50%", "Твіллі + хустка «Ніжність»", ("Твіллі + хустка 44 × 44, двосторонній друк", "4 080 грн"), "the blue box, whole", fit=True, zoom=1.15)
simple("p10-three-twilly-03", "set-3-shovkovykh-tvilli-03", "50% 50%", "Набір із трьох твіллі", ("Три твіллі 84 × 5, принти на вибір", "4 650 грн"), "three twillies in the box, whole", fit=True, zoom=1.15)
simple("p11-makiv", "tvilli-ta-rezynka-makovyi-tsvit-01", "50% 50%", "Твіллі + резинка «Маків цвіт»", ("Твіллі + резинка, у коробці", "2 200 грн"), "white packshot", white=True, zoom=1.08)
simple("p12-sun-svoboda", "maska-dlia-snu-ta-rezynka-svoboda-03", "50% 50%", "Набір для сну «Свобода»", ("Маска для сну + резинка", "3 280 грн"), "sunlit, bleed")
simple("p13-zero-waste", "set-iz-5-ty-shovkovykh-rezynok-zero-west-03", "50% 45%", "П’ять резинок zero waste", ("Набір резинок zero waste, 5 шт.", "2 420 грн"), "five scrunchies, whole", fit=True)
simple("p14-sleep-10", "set-maska-rezynka-10-01", "50% 50%", "Набір для сну «Літнє поле»", ("Маска для сну + резинка", "3 280 грн"), "white packshot, the box open", white=True, zoom=1.1)
simple("p15-svoboda-box", "set-tvilli-845-ta-khustky-4444-svoboda-02", "50% 50%", "Твіллі + хустка «Свобода»", ("Твіллі 84 × 5 + хустка 44 × 44", "3 100 грн"), "the yellow box, whole", fit=True, zoom=1.15)
simple("p16-pidnesennia", "set-maska-zakladka-rezynka-pidnesennia-01", "50% 50%", "Набір «Піднесення»", ("Маска, закладка для книги, резинка", "4 080 грн"), "white packshot", white=True, zoom=1.1)


def _lighter(html, k=0.95):
    """Montserrat Light runs wider than the italic serif it replaced: every headline keeps its layout at a smaller size."""
    import re
    return re.sub(r'(class="big"[^>]*?font-size:)(\d+)px', lambda m: m.group(1) + str(int(int(m.group(2)) * k)) + "px", html)

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · gift sets, series 3</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=EB+Garamond:wght@500;600&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Oswald:wght@500&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("sets3" + ("" if FORMAT == "plain" else "-" + FORMAT) + ".html")).write_text(HEAD + _lighter("".join(ads)) + "\n</body></html>")
print(len(ads), "gift-set banners (series 3)", FORMAT)
