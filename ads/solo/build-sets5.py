"""Gift-set creatives, fifth series (05.11.2026, client: «вот такие варианты ещё» — the dark full-bleed hero of the 26.10 series —
«но не настолько близко: непонятно, что на картинке»). The moody frame stays: the photograph fills the banner to the edges, a dark
veil at the bottom, the big italic headline, the product row. But the set is shown whole: what fills the frame is a blurred, darkened
copy of the same photograph, and the sharp picture lies on it at full width with feathered edges — nothing is cropped, nothing reads as
a pasted rectangle. 1080×1920 plain plus story / feed / square via FORMAT. Photos: photo/site (obiimy.world); prices and names from
review/SITE-FACTS.md (19.10.2026). Output: sets5[-<format>].html → out-sets5[-<format>]/*.jpg
(cd ads && ADS=solo/sets5.html OUT=solo/out-sets5 node render.mjs)."""
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
.big { font-family: 'Montserrat', sans-serif; font-weight: 500; font-style: normal; line-height: 1.08; letter-spacing: 0; text-wrap: balance; }   /* 05.11: the brand's light grotesque instead of the heavy italic */
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


FEATHER = ("-webkit-mask-image:linear-gradient(to right,transparent,#000 7%,#000 93%,transparent),linear-gradient(to bottom,transparent,#000 7%,#000 93%,transparent);"
           "-webkit-mask-composite:source-in;mask-image:linear-gradient(to right,transparent,#000 7%,#000 93%,transparent),linear-gradient(to bottom,transparent,#000 7%,#000 93%,transparent);mask-composite:intersect;")

def hero_whole(id, photo, kicker, big, small, product, note="", size=104, pos="50% 50%", lift=0):
    """The dark hero, the set nearly whole. Tall frames: the photograph runs edge to edge across the top at almost its full width
    (a square photo loses a few percent at the sides, not half), the ink field with the veil, the headline and the row below it.
    Short frames: a blurred, darkened copy of the photo fills the frame, the sharp picture lies whole on the left, the words on the right."""
    w, h = dims(photo); ar = w / h
    if not SHORT:
        text_h = int(360 * K)
        yph = min(int(H * .6), Y1 - text_h - int(20 * K))
        body = f"""
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="left:0;right:0;top:0;height:{yph}px"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos}"></div>
  <div style="inset:0;background:linear-gradient(180deg,rgba(12,9,8,.5) 0,rgba(12,9,8,0) {int(230 * K)}px,rgba(12,9,8,0) {yph - int(300 * K)}px,rgba(12,9,8,.9) {yph}px,rgba(12,9,8,1) {yph + int(40 * K)}px);z-index:3"></div>
  {header()}
  <div style="left:64px;right:64px;bottom:{H - Y1 + int(10 * K)}px;z-index:5">
    <p class="kicker" style="font-size:{int(26 * K)}px">{kicker}</p>
    <p class="big" style="font-size:{int(size * K)}px;margin-top:{int(16 * K)}px">{nbh(big)}</p>
    <p class="small" style="font-size:{int(40 * K)}px;margin-top:{int(22 * K)}px;max-width:{int(900 * K)}px;color:#E6DBC8">{nb(small)}</p>
  </div>
  {plate(*product)}"""
    else:   # short frames: a light version — the blurred copy at its own brightness, the sharp picture whole on the left, ink words
        zh = Y1 - Y0 + int(20 * K); ph_h = zh; ph_w = min(int(1080 * .58), int(ph_h * ar)); ph_h = int(ph_w / ar)
        px = 40; py = Y0 - int(10 * K) + (zh - ph_h) // 2
        tx = px + ph_w + int(36 * K)
        body = f"""
  <div class="ph" style="inset:-60px"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos};filter:blur(50px) brightness(.97);transform:scale(1.15)"></div>
  <div style="inset:0;background:linear-gradient(90deg,rgba(243,234,219,0) 45%,rgba(243,234,219,.55) 75%,rgba(243,234,219,.7) 100%);z-index:1"></div>
  <div class="ph" style="left:{px}px;top:{py}px;width:{ph_w}px;height:{ph_h}px;{FEATHER}z-index:2"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos}"></div>
  <div style="inset:0;background:#F2EADC;mix-blend-mode:multiply;z-index:3"></div>
  {header(dark=False)}
  <div class="ink" style="left:{tx}px;right:56px;top:{Y0 + int(30 * K)}px;z-index:5">
    <p class="kicker" style="font-size:{int(24 * K)}px">{kicker}</p>
    <p class="big" style="font-size:{int(size * .78 * K)}px;margin-top:{int(14 * K)}px">{nbh(big)}</p>
    <p class="small" style="font-size:{int(36 * K)}px;margin-top:{int(18 * K)}px;color:#4B423B">{nb(small)}</p>
  </div>
  {plate(*product, dark=False)}"""
    ad(id, body, note)

TW_KH = ("Твіллі 84 × 5 + хустка 44 × 44", "3 100 грн")
TW_KH2 = ("Твіллі 84 × 5 + хустка 44 × 44, двосторонній друк", "4 080 грн")
TW_SCR = ("Твіллі + резинка, у коробці", "2 200 грн")
SLEEP = ("Маска для сну + резинка", "3 280 грн")
THREE = ("Три твіллі 84 × 5, принти на вибір", "4 650 грн")
MBS = ("Маска, закладка для книги, резинка", "4 080 грн")

hero_whole("h01-three-looks", "set-3-shovkovykh-tvilli-11", "Подарункові набори", "Один подарунок — три образи.", "Три твіллі 84 × 5 у святковому пакуванні: принти можна обрати різні.", THREE, "the three twillies, whole this time")
hero_whole("h02-packed", "set-tvilli-845-ta-khustky-4444-natkhne-01", "Подарункові набори", "Подарунок, який уже запакований.", "Хустка 44 × 44 і твіллі одного принту — у фірмовій жовтій коробці.", ("Набір «Натхнення» · твіллі + хустка", "3 100 грн"), "the yellow box whole")
hero_whole("h03-three-moods", "set-3-shovkovykh-tvilli-13", "Подарункові набори", "Три твіллі — три настрої.", "Принти можна обрати різні: у волосся, на сумку, на шию.", THREE, "three twillies, the third one out")
hero_whole("h04-rest", "set-maska-rezynka-28-01", "Подарункові набори", "Подарунок про відпочинок.", "Шовкова маска для сну й резинка в одному принті — набір «Літнє поле».", SLEEP, "the sleep set laid out")
hero_whole("h05-two-gifts", "set-smilyvist-01", "Подарункові набори", "Два подарунки в одній коробці.", "Твіллі 84 × 5 і шовкова резинка — найпростіший подарунок, який носять.", ("Твіллі + резинка «Сміливість»", "2 200 грн"), "twilly and scrunchie, whole")
hero_whole("h06-sense", "set-maska-zakladka-rezynka-melodiia-01", "Колекція «Співоча душа»", "Подарунок із сенсом.", "Маска для сну, закладка для книги й резинка в одному принті. Частина коштів із колекції — на порятунок сиворакші.", ("«Мелодія двох» · маска, закладка, резинка", "4 080 грн"), "the Singing Soul set", size=96)
hero_whole("h07-for-two", "set-masok-dlia-snu-sertsebyttia-chervo-01", "Подарункові набори", "Для двох.", "Пара шовкових масок для сну «Серцебиття» — червона та чорна.", ("Набір масок «Серцебиття»", "4 200 грн"), "two heart masks", size=124)
hero_whole("h08-her-print", "set-tvilli-845-ta-khustky-4444-vpevnen-01", "Подарункові набори", "Її принт — на двох речах.", "Хустка 44 × 44 і твіллі «Впевненість» в одному принті — разом або окремо.", ("Набір «Впевненість» · твіллі + хустка", "3 100 грн"), "the red box whole")
hero_whole("h09-sleep-sun", "set-ta-rezynka-litnie-pole-04", "Подарункові набори", "Сон у шовку.", "Маска для сну й резинка «Літнє поле» — набір для тієї, хто любить висипатися.", ("Набір для сну «Літнє поле»", "3 280 грн"), "the sunlit sleep set", size=124)
hero_whole("h10-no-wilt", "set-makovyi-tsvit-03", "Подарункові набори", "Замість букета.", "Шовкова твіллі й резинка «Маків цвіт» — подарунок, який не зів’яне.", ("Твіллі + резинка «Маків цвіт»", "2 200 грн"), "the poppy set with a stem", size=124)
hero_whole("h11-small-sign", "set-iz-5-ty-shovkovykh-rezynok-zero-west-03", "Подарункові набори", "Маленький знак уваги.", "П’ять шовкових резинок zero waste — подарунок, який точно підійде.", ("Набір резинок zero waste, 5 шт.", "2 420 грн"), "five scrunchies with the bag")
hero_whole("h12-quiet", "tvilli-ta-rezynka-zakhoplennia-02", "Подарункові набори", "Для тієї, хто любить стримане.", "Сіра твіллі «Захоплення» й резинка в тон — у фірмовій коробці.", ("Твіллі + резинка «Захоплення»", "2 200 грн"), "the grey set", size=92)
hero_whole("h13-one-print", "set-tvilli-845-ta-khustky-4444-svoboda-02", "Подарункові набори", "Хустка й твіллі одного принту.", "Разом у коробці — або кожна річ окремо: на шию, у волосся, на сумку.", ("Набір «Свобода» · твіллі + хустка", "3 100 грн"), "the yellow box, twilly out", size=92)
hero_whole("h14-today", "set-maska-rezynka-34-01", "Подарункові набори", "Замовили до 16:00 — відправимо сьогодні.", "Набір для сну «Серцебиття»: маска й резинка в коробці, готові до вручення.", ("Набір для сну «Серцебиття»", "3 280 грн"), "same-day dispatch, the red sleep set", size=84)
hero_whole("h15-double", "set-tvilli-845-ta-khustky-4444-nizhnis-01", "Подарункові набори", "Набір із двостороннім друком.", "Хустка 44 × 44 «Ніжність» — два принти на одній хустці — і твіллі в тон.", ("Твіллі + хустка 2D «Ніжність»", "4 080 грн"), "the double-sided set", size=92)
hero_whole("h16-blue-sun", "maska-dlia-snu-ta-rezynka-svoboda-03", "Подарункові набори", "Подарунок, який уже запакований.", "Маска для сну й резинка «Свобода» в одному принті — у фірмовій жовтій коробці.", ("Набір для сну «Свобода»", "3 280 грн"), "the blue sleep set in sunlight", size=96)


def _lighter(html, k=1.0):
    """Montserrat Light runs wider than the italic serif it replaced: every headline keeps its layout at a smaller size."""
    import re
    return re.sub(r'(class="big"[^>]*?font-size:)(\d+)px', lambda m: m.group(1) + str(int(int(m.group(2)) * k)) + "px", html)

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · gift sets, series 5</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=EB+Garamond:wght@500;600&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Oswald:wght@500&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("sets5" + ("" if FORMAT == "plain" else "-" + FORMAT) + ".html")).write_text(HEAD + _lighter("".join(ads)) + "\n</body></html>")
print(len(ads), "gift-set banners (series 5)", FORMAT)
