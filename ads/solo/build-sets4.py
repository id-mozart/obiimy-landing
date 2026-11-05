"""Gift-set creatives, fourth series (05.11.2026, client: «акцент на красиву картинку набору; набір видно цілком або майже цілком;
фон фото зливається з фоном банера — без прямокутника з тінню»). One photograph of the set, shown whole, on a field painted with the
photograph's own border colour; the photo's edges are feathered into the field, so nothing reads as a pasted rectangle. The words are
small: the logo line, a kicker, one headline, the price row — above or below the picture (plain), beside it (short frames).
1080×1920 plain plus story / feed / square via FORMAT. Photos: photo/site (obiimy.world); prices and names from review/SITE-FACTS.md
(19.10.2026). Output: sets4[-<format>].html → out-sets4[-<format>]/*.jpg  (cd ads && ADS=solo/sets4.html OUT=solo/out-sets4 node render.mjs)."""
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



def dims(photo):
    from PIL import Image
    with Image.open(HERE.parent.parent / "photo/site" / f"{photo}.jpg") as im: return im.size

def border_color(photo):
    """The median colour of the photograph's border — the whole frame is painted with it, so the picture continues into the field."""
    from PIL import Image
    im = Image.open(HERE.parent.parent / "photo/site" / f"{photo}.jpg").convert("RGB"); w, h = im.size; b = max(3, w // 40)
    px = []
    for box in [(0, 0, w, b), (0, h - b, w, h), (0, 0, b, h), (w - b, 0, w, h)]: px += list(im.crop(box).getdata())
    px.sort(key=sum); r, g, bl = px[len(px) // 2]
    return f"#{r:02x}{g:02x}{bl:02x}"

TONE = "#F2EADC"      # warm paper laid over picture and field alike (multiply): no bright white, and the seam stays invisible

def row_light(title, price, cta="Обрати набір"):
    """The editorial product row: a hairline across, the set's name in small capitals, the price in the serif, the button."""
    return f'''
  <div style="left:64px;right:64px;bottom:{BOTB}px;display:flex;align-items:center;justify-content:space-between;gap:{int(24 * K)}px;padding-top:{int(26 * K)}px;border-top:1.5px solid rgba(27,22,19,.22);z-index:6;color:#1B1613">
    <div style="min-width:0"><p class="hdr" style="font-size:{int(20 * K)}px;letter-spacing:.16em;white-space:normal;line-height:1.3">{nb(title)}</p><p style="font-family:'Montserrat',sans-serif;font-weight:400;font-size:{int(50 * K)}px;line-height:1;margin-top:{int(10 * K)}px">{price}</p></div>
    <div class="cta" style="font-size:{int(40 * K)}px;padding:{int(32 * K)}px {int(58 * K)}px">{cta}</div>
  </div>'''

FEATHER = ("-webkit-mask-image:linear-gradient(to right,transparent,#000 8%,#000 92%,transparent),linear-gradient(to bottom,transparent,#000 8%,#000 92%,transparent);"
           "-webkit-mask-composite:source-in;mask-image:linear-gradient(to right,transparent,#000 8%,#000 92%,transparent),linear-gradient(to bottom,transparent,#000 8%,#000 92%,transparent);mask-composite:intersect;")

def whole(id, photo, big, product, note="", layout="top", kicker="Подарунковий набір", zoom=1.0, pos="50% 50%"):
    """The set whole. The frame is the photo's border colour; the photo sits at its largest size with feathered edges; the words take
    the strip above (layout «top») or below (layout «bottom») the picture; in short frames they move to the left of it."""
    fill = border_color(photo); w, h = dims(photo); ar = w / h
    size = int((52 if SHORT else 64) * K)
    txt_h = int(150 * K)
    if SHORT:
        col = int(380 * K)
        zx, zy, zw, zh = 64 + col, Y0 - int(30 * K), 1080 - 64 - col, Y1 - Y0 + int(30 * K)
        text = f'<div class="ink" style="left:64px;width:{col - int(24 * K)}px;top:{Y0 + int(20 * K)}px;z-index:5"><p class="kicker" style="font-size:{int(22 * K)}px">{kicker}</p><p class="big" style="font-size:{size}px;margin-top:{int(10 * K)}px">{nbh(big)}</p></div>'
    elif layout == "top":
        zx, zy, zw, zh = 0, Y0 + txt_h, 1080, Y1 - Y0 - txt_h
        text = f'<div class="ink" style="left:64px;right:64px;top:{Y0}px;z-index:5"><p class="kicker" style="font-size:{int(24 * K)}px">{kicker}</p><p class="big" style="font-size:{size}px;margin-top:{int(10 * K)}px">{nbh(big)}</p></div>'
    else:
        zx, zy, zw, zh = 0, Y0 - int(30 * K), 1080, Y1 - Y0 - txt_h + int(10 * K)
        text = f'<div class="ink" style="left:64px;right:64px;top:{Y1 - txt_h + int(20 * K)}px;z-index:5"><p class="kicker" style="font-size:{int(24 * K)}px">{kicker}</p><p class="big" style="font-size:{size}px;margin-top:{int(10 * K)}px">{nbh(big)}</p></div>'
    ph_w = min(zw, int(zh * ar)); ph_h = int(ph_w / ar)
    px = zx + (zw - ph_w) // 2; py = zy + (zh - ph_h) // 2
    body = f"""
  <div style="inset:0;background:{fill}"></div>
  {header(dark=False)}
  <div class="ph" style="left:{px}px;top:{py}px;width:{ph_w}px;height:{ph_h}px;{FEATHER}"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  <div style="inset:0;background:{TONE};mix-blend-mode:multiply;z-index:2"></div>
  {text}
  {row_light(*product)}"""
    ad(id, body, note)

TW_KH = ("Твіллі 84 × 5 + хустка 44 × 44", "3 100 грн")
TW_KH2 = ("Твіллі 84 × 5 + хустка 44 × 44, двосторонній друк", "4 080 грн")
TW_SCR = ("Твіллі + резинка, у коробці", "2 200 грн")
SLEEP = ("Маска для сну + резинка", "3 280 грн")
THREE = ("Три твіллі 84 × 5, принти на вибір", "4 650 грн")
MBS = ("Маска, закладка для книги, резинка", "4 080 грн")

whole("w01-natkhnennia", "set-tvilli-845-ta-khustky-4444-natkhne-01", "Твіллі + хустка «Натхнення»", TW_KH, "the box whole on its own grey")
whole("w02-smilyvist", "set-smilyvist-01", "Твіллі + резинка «Сміливість»", TW_SCR, "white packshot", layout="bottom", zoom=1.06)
whole("w03-vpevnenist", "set-tvilli-845-ta-khustky-4444-vpevnen-01", "Твіллі + хустка «Впевненість»", TW_KH, "the red box")
whole("w04-sleep-28", "set-maska-rezynka-28-01", "Набір для сну «Літнє поле»", SLEEP, "sleep set laid out", layout="bottom", zoom=1.06)
whole("w05-nizhnist", "set-tvilli-845-ta-khustky-4444-nizhnis-01", "Твіллі + хустка «Ніжність»", TW_KH2, "the blue box, double-sided print")
whole("w06-three-03", "set-3-shovkovykh-tvilli-03", "Набір із трьох твіллі", THREE, "three twillies in the box", layout="bottom")
whole("w07-smilyvy-dotyk", "set-tvilli-845-ta-khustky-4444-smilyvy-01", "Твіллі + хустка «Сміливий дотик»", TW_KH, "the beige leopard box")
whole("w08-melodiia", "set-maska-zakladka-rezynka-melodiia-01", "Набір «Мелодія двох»", MBS, "mask, bookmark, scrunchie", layout="bottom", zoom=1.06)
whole("w09-hratsiia", "set-tvilli-845-ta-khustky-4444-hratsii-01", "Твіллі + хустка «Грація»", TW_KH, "the orange leopard box")
whole("w10-hearts", "set-masok-dlia-snu-sertsebyttia-chervo-01", "Набір масок «Серцебиття»", ("Дві маски для сну: червона та чорна", "4 200 грн"), "two heart masks with the box", layout="bottom")
whole("w11-svoboda", "set-tvilli-845-ta-khustky-4444-svoboda-02", "Твіллі + хустка «Свобода»", TW_KH, "the yellow box, twilly out")
whole("w12-three-13", "set-3-shovkovykh-tvilli-13", "Набір із трьох твіллі", THREE, "three twillies, portrait white", layout="bottom")
whole("w13-spokusa", "set-tvilli-845-ta-khustky-4444-spokusa-02", "Твіллі + хустка «Спокуса»", TW_KH, "the pink box")
whole("w14-sleep-10", "set-maska-rezynka-10-01", "Набір для сну «Літнє поле»", SLEEP, "the sleep box open", layout="bottom", zoom=1.06)
whole("w15-makiv", "tvilli-ta-rezynka-makovyi-tsvit-01", "Твіллі + резинка «Маків цвіт»", TW_SCR, "white packshot")
whole("w16-pidnesennia", "set-maska-zakladka-rezynka-pidnesennia-01", "Набір «Піднесення»", MBS, "mask, bookmark, scrunchie", layout="bottom", zoom=1.06)
whole("w17-zero-waste", "set-iz-5-ty-shovkovykh-rezynok-zero-west-03", "П’ять резинок zero waste", ("Набір резинок zero waste, 5 шт.", "2 420 грн"), "five scrunchies with the bag")
whole("w18-litnie-pole", "tvilli-ta-rezynka-litnie-pole-01", "Твіллі + резинка «Літнє поле»", TW_SCR, "white packshot", layout="bottom", zoom=1.06)
whole("w19-sun-sleep", "set-ta-rezynka-litnie-pole-04", "Набір для сну «Літнє поле»", SLEEP, "sunlit flat-lay, whole")
whole("w20-two-sleep", "set-ta-rezynka-litnie-pole-03", "Набори для сну «Літнє поле» і «Свобода»", ("Маска для сну + резинка — кожен набір", "3 280 грн"), "two sleep sets with dried flowers", layout="bottom")
whole("w21-black-heart", "set-maska-dlia-snu-ta-rezynka-sertseby-01", "Набір для сну «Серцебиття»", SLEEP, "black heart mask on the box")
whole("w22-zakhoplennia", "tvilli-ta-rezynka-zakhoplennia-02", "Твіллі + резинка «Захоплення»", TW_SCR, "the grey set", layout="bottom")
whole("w23-sun-svoboda", "maska-dlia-snu-ta-rezynka-svoboda-03", "Набір для сну «Свобода»", SLEEP, "sunlit, whole")
whole("w24-sun-vpevnenist", "maska-dlia-snu-ta-rezynka-vpevnenist-03", "Набір для сну «Впевненість»", SLEEP, "sunlit, whole", layout="bottom")
whole("w25-prystrast", "set-prystrast-01", "Твіллі + резинка «Пристрасть»", TW_SCR, "the set with the flower")
whole("w26-makiv-03", "set-makovyi-tsvit-03", "Твіллі + резинка «Маків цвіт»", TW_SCR, "the poppy set with a stem", layout="bottom")
whole("w27-three-07", "set-3-shovkovykh-tvilli-07", "Набір із трьох твіллі", THREE, "three twillies unfolded")
whole("w28-sleep-26", "set-maska-rezynka-26-02", "Набір для сну «Свобода»", SLEEP, "the sleep box", layout="bottom")


def _lighter(html, k=0.95):
    """Montserrat Light runs wider than the italic serif it replaced: every headline keeps its layout at a smaller size."""
    import re
    return re.sub(r'(class="big"[^>]*?font-size:)(\d+)px', lambda m: m.group(1) + str(int(int(m.group(2)) * k)) + "px", html)

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · gift sets, series 4</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=EB+Garamond:wght@500;600&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Oswald:wght@500&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("sets4" + ("" if FORMAT == "plain" else "-" + FORMAT) + ".html")).write_text(HEAD + _lighter("".join(ads)) + "\n</body></html>")
print(len(ads), "gift-set banners (series 4)", FORMAT)
