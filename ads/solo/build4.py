"""SOLO in the classic Obiimy ad style (series 1–2 look: full-bleed photo or ivory product frame,
Prata headline with a muted accent, Onest body, pill CTA), with copy written from the press release.
Rules kept from the audits: all text and logo inside the story safe zone (y 280…1540), price = product in frame,
no third-party brands, verbatim quotes, no price next to war-related lines. Output: solo4.html → out4/*.jpg"""
import pathlib, sys, os
YELLOW = os.environ.get("YELLOW") == "1"   # variant B: product named on a yellow brand plate
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit import P, PP, S, CUT, HI, spot_photo, nb, LOGO_W, LOGO_K, GRAIN

def S2(name): return f"src/{name}-2k.webp" if (HERE / f"src/{name}-2k.webp").exists() else f"src/{name}.webp"

CSS = """
:root { --ivory: #F4F2ED; --stone: #E8E2D8; --ink: #141216; --ink-2: #4A4750; --ink-3: #8A8592; --gold: #F2B705; --plum: #1B1430; --line: rgba(20,18,22,.16); }
* { box-sizing: border-box; }
body { margin: 0; background: #666; font-family: 'Onest', 'Helvetica Neue', Arial, sans-serif; color: var(--ink); -webkit-font-smoothing: antialiased; }
.ad { width: 1080px; height: 1920px; position: relative; overflow: hidden; background: var(--ivory); margin: 20px auto; }
.ad > * { position: absolute; margin: 0; }
.ad p, .ad h1 { margin: 0; }
.ad::after { content: ""; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: .12; mix-blend-mode: multiply; background-image: GRAIN; }
.dark::after { mix-blend-mode: soft-light; opacity: .35; }
.logo { left: 50%; transform: translateX(-50%); height: 54px; }
.logo img { display: block; height: 54px; width: auto; }
.eyebrow { font-size: 30px; letter-spacing: .16em; text-transform: uppercase; font-weight: 600; color: var(--ink-2); left: 80px; right: 80px; text-align: center; }
.h { font-family: 'Prata', serif; font-size: 100px; line-height: 1.04; text-align: center; left: 70px; right: 70px; letter-spacing: -0.01em; text-wrap: balance; }
.h em { font-style: normal; color: var(--ink-3); }
.body { font-size: 36px; line-height: 1.45; font-weight: 300; color: var(--ink-2); left: 120px; right: 120px; text-align: center; text-wrap: pretty; }
.price { font-family: 'Prata', serif; font-size: 46px; text-align: center; left: 80px; right: 80px; }
.price small { max-width: 840px; margin-left: auto; margin-right: auto; font-family: 'Onest'; font-size: 28px; letter-spacing: .1em; text-transform: uppercase; color: var(--ink-3); display: block; margin-top: 8px; font-weight: 500; }
.cta { left: 50%; transform: translateX(-50%); background: var(--ink); color: var(--ivory); font-size: 32px; font-weight: 600; letter-spacing: .03em; padding: 28px 60px; border-radius: 999px; white-space: nowrap; }
.full > .photo { position: absolute; left: 0; right: 0; top: 200px; height: 1720px; }
.photo { overflow: hidden; }
.photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
.dark { background: #141216; color: #F4F2ED; }
.dark .eyebrow { color: rgba(244,242,237,.75); }
.dark .body { color: rgba(244,242,237,.88); }
.dark .h em { color: rgba(244,242,237,.62); }
.dark .price small { color: rgba(244,242,237,.86); }
.dark .cta { background: var(--gold); color: var(--ink); }
.shade { left: 0; right: 0; bottom: 0; height: 1080px; background: linear-gradient(180deg, rgba(20,18,22,0) 0%, rgba(20,18,22,.55) 40%, rgba(20,18,22,.92) 100%); }
.shade-top { left: 0; right: 0; top: 0; height: 560px; background: linear-gradient(180deg, #141216 0%, #141216 36%, rgba(20,18,22,0) 100%); }
.frame { left: 90px; right: 90px; overflow: hidden; }
.frame img { width: 100%; height: 100%; object-fit: cover; display: block; }
.cut { display: block; filter: drop-shadow(0 28px 32px rgba(40,25,10,.28)); }
""".replace("GRAIN", GRAIN)

ads = []
def ad(id, cls, body, note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad {cls}" id="{id}">{body}\n</section>')

def price(main, small=""):
    return f'<p class="price" style="top:{{y}}px">{main}{f"<small>{small}</small>" if small else ""}</p>'

# ---------------------------------------------------------------- FULL-BLEED (dark)
from PIL import Image as _Im
def edge_tone(photo, spot):
    """Average colour of the photo's top edge — fills the story header zone so there is no seam or black bar."""
    im = _Im.open(HERE / f"src/{photo}.webp").convert("L" if spot else "RGB")
    row = im.crop((0, 0, im.width, 24)).resize((1, 1)).getpixel((0, 0))
    r, g, b = (row, row, row) if spot else row
    k = .8
    return f"rgb({int(r * k)},{int(g * k)},{int(b * k)})"


# what is sold in each full-frame banner: cutout, product type, print · size
PROD = {
    "c01-launch": (["tysha-88-1", "iskra-tw-4", "krok-44-1"], "Шовкові хустки й твіллі", "7 авторських принтів"),
    "c02-iskra": (["iskra-65-1"], "Шовкова хустка", "«Іскра» · 65 × 65 см"),
    "c03-flirt": (["flirt-65-1"], "Шовкова хустка", "«Флірт» · 65 × 65 см"),
    "c05-zolote": (["zolote-44-1"], "Шовкова хустка", "«Золоте світло» · 44 × 44 см"),
    "c06-avantiura": (["avantiura-88-1"], "Шовкова хустка", "«Авантюра»"),
    "c07-tysha": (["tysha-88-1"], "Шовкова хустка", "«Тиша всередині» · 88 × 88 см"),
    "c08-krok": (["krok-44-1"], "Шовкова хустка", "«Сміливий крок» · 44 × 44 см"),
    "c09-ya-ie": (["zolote-44-1"], "Шовкова хустка", "«Золоте світло» · 44 × 44 см"),
    "c10-grey": (["puls-44-1"], "Шовкова хустка", "«Пульс» · 44 × 44 см"),
    "c11-decades": (["flirt-tw-5"], "Шовкова твіллі", "«Флірт»"),
    "c12-hair": (["avantiura-tw-5"], "Шовкова твіллі", "«Авантюра»"),
    "c13-parts": (["avantiura-88-1"], "Шовкова хустка", "«Авантюра» · 88 × 88 см"),
    "u01-buy-ukrainian": (["flirt-tw-5"], "Шовкова твіллі", "«Флірт»"),
    "u02-london": (["zolote-44-1"], "", "«Золоте світло»"),
    "u03-made-in-ua": (["krok-44-1"], "Шовкова хустка", "«Сміливий крок» · 44 × 44 см"),
    "u04-not-mass": (["puls-tw-4"], "Шовкова твіллі", "«Пульс»"),
    "u05-luxury": (["tysha-88-1"], "Шовкова хустка", "«Тиша всередині»"),
    "u06-abroad": (["iskra-tw-4"], "Шовкова твіллі", "«Іскра»"),
}

MIN = {}   # id -> (cutouts, "Шовкова хустка «…»") for the minimal premium banners

LABEL = {"p12-wearable-art": "Шовкові вироби", "p01-quiet-luxury": "Шовкові вироби"}      # top-right label, where it differs from the default
INLINE = {"p05-character", "p12-wearable-art", "p01-quiet-luxury", "c06-avantiura"}
MIRROR_TOP = {"p12-wearable-art"}   # the source frame has no background above the head     # no button: «Обрати →» to the right of the price

def product_card(id, price_main, price_small):
    if id in MIN:
        cuts, title = MIN[id]
        img = "".join(f'<img src="{CUT(c)}" alt="" style="height:150px;width:auto;max-width:170px;object-fit:contain;filter:drop-shadow(0 10px 12px rgba(0,0,0,.4));transform:rotate(-6deg)">' for c in cuts)
        bg, c1 = ("#F2B705", "#141216") if YELLOW else ("rgba(244,242,237,.1)", "#fff")
        bd = "none" if YELLOW else "1.5px solid rgba(244,242,237,.3)"
        return f"""<div style="display:flex;align-items:center;gap:28px;margin-top:30px;padding:14px 38px 14px 16px;border-radius:{6 if YELLOW else 22}px;background:{bg};border:{bd};text-align:left">
      {img}<div><p style="font-size:36px;line-height:1.2;font-weight:600;color:{c1}">{title}</p>
      <div style="display:flex;align-items:baseline;justify-content:space-between;gap:40px;margin-top:10px"><p style="font-family:Prata,serif;font-size:50px;line-height:1;color:{c1}">{price_main}</p>{f'<p style="font-size:36px;font-weight:600;color:{"#141216" if YELLOW else "#F2B705"};white-space:nowrap">Обрати&nbsp;→</p>' if id in INLINE else ""}</div></div></div>"""
    cuts, kind, name = PROD[id]
    imgs = "".join(f'<img src="{CUT(c)}" alt="" style="height:200px;width:auto;max-width:{220 if len(cuts) == 1 else 140}px;object-fit:contain;margin-left:{0 if k == 0 else -40}px;filter:drop-shadow(0 12px 14px rgba(0,0,0,.4));transform:rotate({(-6, 5, -3)[k]}deg)">' for k, c in enumerate(cuts))
    if YELLOW:
        bg, bd, c1, c2, c3 = "#F2B705", "none", "#141216", "#141216", "#141216"
    else:
        bg, bd, c1, c2, c3 = "rgba(244,242,237,.1)", "1.5px solid rgba(244,242,237,.3)", "#E9D7A6", "#fff", "#fff"
    big = not kind      # only the name and the price: both a step larger
    price = f'<p style="font-family:Prata,serif;font-size:{70 if big else 58}px;line-height:1;color:{c3};margin-top:{14 if big else 10}px">{price_main}</p>' if price_main else ""
    return f"""<div style="display:flex;align-items:center;gap:32px;margin-top:28px;padding:18px 40px 18px 20px;border-radius:{6 if YELLOW else 22}px;background:{bg};border:{bd};text-align:left;box-shadow:{"0 20px 40px -20px rgba(0,0,0,.6)" if YELLOW else "none"}">
      <div style="display:flex;align-items:center;flex:none">{imgs}</div>
      <div>{f'<p style="font-size:30px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:{c1}">{kind}</p>' if kind else ""}
        <p style="font-size:{46 if big else 38}px;line-height:1.2;color:{c2};margin-top:{0 if big else 6}px;font-weight:{500 if (YELLOW or big) else 400}">{name}</p>
        <div style="display:flex;align-items:baseline;justify-content:space-between;gap:48px">{price}{f'<p style="font-size:38px;font-weight:600;color:{"#141216" if YELLOW else "#F2B705"};white-space:nowrap">Обрати&nbsp;→</p>' if id in INLINE else ""}</div></div></div>"""

LOCKUP = ('<span style="display:block;font-family:Montserrat,sans-serif;text-transform:uppercase;line-height:1;color:#fff">'
          '<span style="display:block;font-size:40px;font-weight:400">Колекція</span>'
          '<span style="display:block;font-size:170px;font-weight:300;margin-top:6px">Соло</span>'
          '<span style="display:block;font-size:40px;font-weight:400;margin-top:10px">Шлях до себе</span></span>')

def full(id, photo, pos, h, em, body, price_main, price_small, cta, spot=False, note="", hs=92, box=(0, 1920), top_text=False, shade_from=1040):
    """Plain banner: the photo fills the frame, logo at the top edge, text block at the bottom edge
    (or at the top for back-view frames). If the photo box does not start at 0, the gap takes the photo's edge tone."""
    t, hgt = box
    top_rgb = edge_tone(photo, spot)
    grad = ("linear-gradient(180deg,transparent 0,#000 140px,#000 calc(100% - 300px),transparent 100%)" if t + hgt < 1920
            else "linear-gradient(180deg,transparent 0,#000 140px)")      # the photo melts into the dark ground where it ends inside the frame
    feather = (f"-webkit-mask-image:{grad};mask-image:{grad}" if t > 0 else "")
    st = f"position:absolute;left:0;right:0;top:{t}px;height:{hgt}px;{feather}"
    ph = (spot_photo(photo, pos, style=st) if spot
          else f'<div class="photo" style="{st}"><img src="{S2(photo)}" alt="" style="object-position:{pos}"></div>')
    fill = f'<div style="left:0;right:0;top:0;height:{t + 160}px;background:{top_rgb}"></div>' if t > 0 else ""
    if id in MIRROR_TOP and t > 0:
        fill += (f'<div style="left:0;right:0;top:0;height:{t + 150}px;background:url(src/{photo}-top.webp) {pos.split()[0]} 0/1920px 100% no-repeat"></div>'
                 + f'<div style="left:0;right:0;top:0;height:{t + 150}px;background:linear-gradient(180deg,rgba(20,18,22,.86) 0%,rgba(20,18,22,.6) 45%,rgba(20,18,22,0) 100%)"></div>')
    pr = product_card(id, price_main, price_small)
    block = f"""<h1 class="h" style="position:static;color:#fff;font-size:{hs}px">{h}{f'<br><em style="color:#E9D7A6">{em}</em>' if em else ''}</h1>
    {f'<p class="body" style="position:static;margin-top:18px;max-width:900px">{nb(body)}</p>' if body else ""}
    {pr}
    {"" if id in INLINE else f'<div class="cta" style="position:static;transform:none;margin-top:26px">{cta}</div>'}"""
    if top_text:
        shade = '<div style="left:0;right:0;top:0;height:900px;background:linear-gradient(180deg,#141216 0%,rgba(20,18,22,.88) 42%,rgba(20,18,22,.5) 72%,rgba(20,18,22,0) 100%)"></div>'
        pos_block = "top:200px"
    else:
        shade = ('<div style="left:0;right:0;top:0;height:260px;background:linear-gradient(180deg,rgba(20,18,22,.55) 0%,rgba(20,18,22,0) 100%)"></div>'
                 f'<div style="left:0;right:0;top:{shade_from}px;bottom:0;background:linear-gradient(180deg,rgba(20,18,22,0) 0%,rgba(20,18,22,.78) 28%,rgba(20,18,22,.92) 58%,rgba(20,18,22,.95) 100%)"></div>')
        pos_block = "bottom:96px"
    ad(id, "full dark", f"""
  <div style="left:0;right:0;top:0;bottom:0;background:#141216"></div>
  {fill}
  {ph}
  {shade}
  <img src="{LOGO_W}" alt="" style="left:70px;top:64px;height:54px;display:block">
  <p style="right:70px;top:80px;font-family:Montserrat,sans-serif;font-size:26px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap;color:#fff;text-shadow:0 1px 10px rgba(0,0,0,.45)">{LABEL.get(id, "Авторські шовкові вироби")}</p>
  <div style="left:70px;right:70px;{pos_block};display:flex;flex-direction:column;align-items:center;text-align:center">
    {block}
  </div>""", note)

full("c01-launch", "tysha-88-2", "50% 0%", LOCKUP, "",
     "<span style=\"display:inline-block;font-family:Montserrat,sans-serif;font-size:30px;font-weight:500;padding:14px 28px;border-radius:999px;background:#F2B705;color:#141216\">Жіноча сила крізь десятиліття</span>",
     "від 1 600 грн", "твіллі · хустки 44, 65 і 88 см", "Дивитися всі 7 принтів", note="Launch")
full("c02-iskra", "iskra-65-2", "40% 0%", "Сміливість", "бути помітною.",
     "Внутрішня енергія та здатність запалювати зміни навколо себе.", "4 800 грн", "«Іскра» · хустка 65 × 65", "Обрати «Іскру»", spot=True, note="Iskra, colour spot", shade_from=980)
full("c03-flirt", "flirt-65-3", "38% 30%", "Флірт — це", "насамперед стан.",
     "Віра в перемогу, оптимізм і мистецтво невимушеної жіночності.", "4 800 грн", "«Флірт» · хустка 65 × 65", "Обрати «Флірт»", note="Flirt")
full("c05-zolote", "zolote-44-3", "50% 25%", "Коли все стає", "на свої місця.",
     "«Золоте світло» — хустка для моментів ясності.", "від 2 400 грн", "«Золоте світло» · хустка 44 × 44", "Обрати «Золоте світло»", note="Zolote")
full("c06-avantiura", "avantiura-88-5", "62% 30%", "За межі", "звичного.",
     "Готовність виходити за межі звичного та відкриватися новому досвіду.", "6 600 грн", "«Авантюра» · хустка 88 × 88", "Обрати «Авантюру»", spot=True, note="Avantiura, colour spot")
full("c07-tysha", "tysha-88-3", "50% 45%", "Тиша", "всередині.",
     "Стан, у якому більше не потрібно доводити, поспішати чи відповідати чужим очікуванням.", "6 600 грн", "«Тиша всередині» · хустка 88 × 88", "Обрати «Тишу всередині»", note="Tysha")
full("c08-krok", "krok-44-2", "50% 30%", "Сміливий", "крок.",
     "Не тому, що страх зникає, а тому, що з’являється щось важливіше — довіра до себе.", "2 400 грн", "«Сміливий крок» · хустка 44 × 44", "Обрати «Сміливий крок»", note="Krok")
full("c09-ya-ie", "zolote-44-2", "50% 20%", "Я є.<br>Я продовжую жити.", "Я обираю себе.",
     "Улюблена сукня, шовкова хустка, червона помада стають маленькими актами свободи.", "", "SOLO · шлях до себе", "Знайти свій стан", note="Manifesto, organic", hs=84)
full("c10-grey", "puls-44-2", "42% 40%", "Мода — це", "про гідність.",
     "Про право на жіночність навіть тоді, коли світ навколо стає темно-сірим.", "", "SOLO · шовкова свобода", "Знайти свій стан", spot=True, note="Dignity, organic")
full("c11-decades", "flirt-tw-4", "50% 40%", "Змінювалися епохи й силуети.", "Хустка залишалася поруч.",
     "Натхнення — обкладинки <span style=\"white-space:nowrap\">40–50-х</span>.", "1 600 грн", "твіллі «Флірт» · 84 × 5", "Обрати твіллі", note="Decades", hs=64, box=(0, 1920), top_text=True)
full("c12-hair", "avantiura-tw-3", "50% 40%", "У волоссі.", "Як у п’ятдесятих.",
     "Шовкова стрічка «Авантюра» — у волосся, на сумку чи на зап’ястя.", "1 600 грн", "твіллі «Авантюра» · 84 × 5", "Обрати твіллі", note="Twilly in hair", box=(300, 1620), top_text=True)
full("c13-parts", "avantiura-88-2", "40% 0%", "Найбільша хустка.", "Можна частинами.",
     "ПриватБанк — 4 платежі, monobank — 3 платежі.", "6 600 грн", "«Авантюра» · хустка 88 × 88", "Купити частинами", note="Pay in parts", box=(0, 1920), shade_from=1000)

# ---------------------------------------------------------------- IVORY (product)
def ivory(id, eyebrow, h, em, visual, body, price_main, price_small, cta, bg="var(--ivory)", note="", hs=100, quote="", dark=False):
    clean = bool(quote)     # image banner: no eyebrow, no price lines, one personal line above the button
    if dark: bg = "radial-gradient(90% 60% at 50% 45%,#2A2622,#141216 80%)"
    ad(id, "dark" if dark else "", f'''
  <div style="left:0;right:0;top:0;bottom:0;background:{bg}"></div>
  <img src="{LOGO_W if dark else LOGO_K}" alt="" style="left:70px;top:64px;height:54px;display:block">
  <p style="right:70px;top:80px;font-family:Montserrat,sans-serif;font-size:26px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;white-space:nowrap;font-size:24px;color:{"rgba(244,242,237,.85)" if dark else "var(--ink-2)"}">Авторські шовкові вироби</p>
  <div style="left:70px;right:70px;top:80px;bottom:{150 if clean else 96}px;display:flex;flex-direction:column;align-items:center;text-align:center">
    {'<div style="height:60px"></div>' if (YELLOW or clean) else f'<p class="eyebrow" style="position:static;margin-top:90px">{eyebrow}</p>'}
    <h1 class="h" style="position:static;margin-top:{60 if clean else 16}px;font-size:{hs}px">{h}<br><em{' style="color:#E9D7A6"' if dark else ""}>{em}</em></h1>
    <div style="flex:1;min-height:0;align-self:stretch;margin-top:{36 if clean else 44}px;position:relative">{visual}</div>
    {f"""<p style="position:static;margin-top:44px;max-width:860px;font-family:Prata,serif;font-size:50px;line-height:1.2;color:{"#F4F2ED" if dark else "var(--ink)"};text-wrap:balance">{nb(quote)}</p>""" if clean else f'<p class="body" style="position:static;margin-top:40px;max-width:880px">{nb(body)}</p>'}
    {"" if clean else yellow_plate(id) if YELLOW else f'<p class="price" style="position:static;margin-top:18px">{price_main}' + (f"<small>{price_small}</small>" if price_small else "") + '</p>'}
    <div class="cta" style="position:static;transform:none;margin-top:{40 if clean else 26}px">{cta}</div>
  </div>''', note)

PLATE = {
    "c14-twilly": ("Шовкова твіллі-стрічка", "84 × 5 см · 7 принтів", "1 600 грн"),
    "c15-box": ("Шовкова резинка «Флірт»", "у фірмовій коробочці", "700 грн"),
    "c16-gift": ("Шовкові хустки", "44, 65 і 88 см · 7 принтів", "від 2 400 грн"),
    "c17-double": ("Шовкова хустка «Іскра»", "65 × 65 см · двосторонній друк", "4 800 грн"),
    "c18-look": ("Хустка «Іскра» + твіллі", "доставка безкоштовна", "6 400 грн"),
    "c23-look-dark": ("Хустка «Іскра» + твіллі", "доставка безкоштовна", "6 400 грн"),
    "c19-certificate": ("Подарунковий сертифікат", "1 000 – 4 000 грн · діє 3 місяці", "від 1 000 грн"),
    "c20-showroom": ("Шовкові хустки SOLO", "шоурум: Сагайдачного, 12", "від 2 400 грн"),
    "c21-art": ("Шовкові хустки й твіллі", "7 авторських принтів", "від 1 600 грн"),
    "c22-delivery": ("Хустка «Пульс» + твіллі", "44 × 44 см · 84 × 5 см", "4 000 грн"),
    "u07-hand-edge": ("Шовкова хустка «Іскра»", "65 × 65 см · ручна обробка краю", "4 800 грн"),
    "u08-details": ("Шовкова хустка «Тиша всередині»", "88 × 88 см · двосторонній друк", "6 600 грн"),
    "u09-from-painting": ("Шовкові хустки SOLO", "7 авторських принтів", "від 2 400 грн"),
    "u10-trust": ("Шовкові хустки й твіллі", "український бренд Obiimy", "від 1 600 грн"),
    "u11-slow": ("Шовкова хустка «Золоте світло»", "44 × 44 см · 100% шовк", "2 400 грн"),
}

def yellow_plate(id):
    name, detail, price = PLATE[id]
    return f"""<div style="margin-top:26px;align-self:stretch;background:#F2B705;border-radius:6px;padding:24px 40px;box-shadow:0 20px 40px -24px rgba(90,60,0,.55);display:flex;align-items:center;justify-content:space-between;gap:30px;text-align:left">
      <div><p style="font-size:38px;line-height:1.15;font-weight:700">{name}</p><p style="font-size:30px;margin-top:6px;font-weight:500">{detail}</p></div>
      <p style="font-family:Prata,serif;font-size:60px;line-height:1;flex:none;white-space:nowrap">{price}</p></div>"""

V = lambda inner: f'<div style="position:absolute;inset:0;display:grid;place-items:center">{inner}</div>'
FRAME = lambda name, pos="50% 50%": f'<div class="frame" style="position:absolute;inset:0 20px"><img src="{S2(name)}" alt="" style="object-position:{pos}"></div>'

tw_img = lambda p: f'<img class="cut" src="{CUT(p["tw"])}" alt="" style="height:330px">'
tw = f'<div style="display:grid;gap:18px;justify-items:center"><div style="display:flex;gap:34px">{"".join(tw_img(p) for p in P[:4])}</div><div style="display:flex;gap:34px">{"".join(tw_img(p) for p in P[4:])}</div></div>'
ivory("c14-twilly", "Шовкові твіллі-стрічки 84 × 5 см", "Сім станів.", "Одна ціна.",
      V(tw),
      "Шовкова стрічка в кожному з семи принтів колекції SOLO.", "1 600 грн", "натуральний шовк", "Обрати свій принт", note="Seven twillies")
ivory("c15-box", "Шовкова резинка для волосся", "Жовта коробка,", "а в ній — «Флірт».",
      f'<div class="frame" style="position:absolute;inset:0 20px;mix-blend-mode:multiply;-webkit-mask-image:radial-gradient(75% 80% at 50% 50%,#000 70%,transparent 100%);mask-image:radial-gradient(75% 80% at 50% 50%,#000 70%,transparent 100%)"><img src="{S2("flirt-scr-1")}" alt="" style="object-position:50% 62%"></div>',
      "Шовкова резинка у фірмовій коробочці — перше знайомство з Obiimy.", "700 грн", "резинка для волосся «Флірт»", "Подарувати «Флірт»", bg="#F1F1F1", note="Yellow box")
trio = "".join(f'<img class="cut" src="{CUT(PP[i]["flat"])}" alt="" style="width:400px;transform:rotate({r}deg);margin:0 -56px">' for i, r in (("iskra", -10), ("tysha", 2), ("krok", 11)))
ivory("c16-gift", "Шовкові хустки у подарунок", "Подаруйте", "не річ, а стан.",
      V(f'<div style="display:flex;align-items:center">{trio}</div>'),
      "«Іскра» — для сміливої, «Тиша всередині» — для тієї, що вміє чути себе, «Сміливий крок» — для нових починань.",
      "від 2 400 грн", "хустки 44, 65 і 88 см", "Підібрати подарунок", note="Gift a state")
ivory("c17-double", "Шовкова хустка · двосторонній друк", "Жодного", "вивороту.",
      f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;overflow:hidden"><img class="cut" src="{CUT("iskra-65-5")}" alt="" style="height:96%;width:auto"></div>',
      "Авторський принт на обох боках натурального шовку — зав’язуйте як завгодно.", "4 800 грн", "«Іскра» · хустка 65 × 65", "Роздивитися «Іскру»", note="Double-sided")
look = f"""<div style="position:absolute;inset:0 20px;display:grid;grid-template-columns:1.2fr 1fr;gap:14px">
    <div class="photo"><img src="{S2('iskra-65-2')}" alt="" style="object-position:40% 35%"></div><div class="photo"><img src="{S2('iskra-tw-3')}" alt="" style="object-position:50% 60%"></div></div>"""
ivory("c18-look", "Шовкова хустка + твіллі", "Хустка й твіллі", "одного принту.", look,
      "Один принт — на плечах і на сумці.", "6 400 грн", "хустка + твіллі · доставка безкоштовна", "Зібрати образ", note="Complete look", quote="Ваш почерк — у кожній деталі.", hs=72)
look2 = f"""<div style="position:absolute;inset:0 20px;display:grid;grid-template-columns:1.2fr 1fr;gap:14px">
    <div class="photo"><img src="{S2('flirt-65-3')}" alt="" style="object-position:62% 30%"></div><div class="photo"><img src="{S2('flirt-tw-1')}" alt="" style="object-position:50% 40%"></div></div>"""
ivory("c23-look-dark", "Шовкова хустка + твіллі", "Хустка й твіллі", "одного принту.", look2,
      "Один принт — на плечах і на сумці.", "6 400 грн", "хустка + твіллі · доставка безкоштовна", "Зібрати образ", note="Complete look, dark", quote="Ваш почерк — у кожній деталі.", hs=72, dark=True)
cert = f"""<div style="position:absolute;inset:0 20px;background:url(src/{PP['zolote']['flat']}-hi.webp) center/170%"></div>
  <div style="position:absolute;left:150px;right:150px;top:110px;bottom:110px;background:#fff;box-shadow:0 30px 60px -24px rgba(0,0,0,.5);display:grid;place-items:center;text-align:center">
    <div><p style="font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)">Номінали, грн</p>
    <p style="font-family:Prata,serif;font-size:64px;line-height:1.12;margin-top:14px">1 000 · 1 500<br>2 000 · 2 500<br>4 000</p>
    <p style="margin-top:18px;font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)">на будь-який товар</p></div></div>"""
ivory("c19-certificate", "Подарунковий сертифікат Obiimy", "Нехай обере", "сама.", cert,
      "Електронний або фізичний. Діє 3 місяці.", "від 1 000 грн", "подарунковий сертифікат Obiimy", "Подарувати сертифікат", bg="var(--stone)", note="Certificate")
trio2 = "".join(f'<img class="cut" src="{CUT(PP[i]["flat"])}" alt="" style="width:400px;transform:rotate({r}deg);margin:0 -56px">' for i, r in (("puls", -9), ("avantiura", 3), ("zolote", 10)))
ivory("c20-showroom", "Шовкові хустки · шоурум у Києві", "Приміряйте", "наживо.", V(f'<div style="display:flex;align-items:center">{trio2}</div>'),
      "Вул. Петра Сагайдачного, 12. Пн–пт 10:00–18:00, сб 11:00–18:00.", "від 2 400 грн", "хустки SOLO", "Приміряти в шоурумі", note="Showroom")
sw = lambda p: f'<span style="width:216px;height:216px;background:url({HI(p)}) center/220%;box-shadow:0 14px 22px -12px rgba(0,0,0,.4)"></span>'
seven = f'<div style="display:grid;gap:18px;justify-items:center"><div style="display:flex;gap:18px">{"".join(sw(p) for p in P[:4])}</div><div style="display:flex;gap:18px">{"".join(sw(p) for p in P[4:])}</div></div>'
ivory("c21-art", "Шовкові хустки й твіллі SOLO", "Сім принтів.", "Сім станів.", V(seven),
      "«Іскра», «Флірт», «Пульс», «Золоте світло», «Авантюра», «Тиша всередині», «Сміливий крок».", "від 1 600 грн", "твіллі 1 600 · хустки від 2 400", "Дивитися всі 7 принтів", bg="var(--stone)", note="Seven prints")
ivory("c22-delivery", "Шовкова хустка й твіллі · доставка", "Замовте до 16:00 —", "відправимо сьогодні.",
      V(f'<div style="display:flex;align-items:center;gap:30px"><img class="cut" src="{CUT("puls-44-1")}" alt="" style="width:470px;transform:rotate(-6deg)"><img class="cut" src="{CUT("zolote-tw-3")}" alt="" style="height:500px;transform:rotate(8deg)"></div>'),
      "Новою поштою в день замовлення.", "4 000 грн", "«Пульс» 44 × 44 + твіллі «Золоте світло»", "Замовити до 16:00", note="Delivery", hs=84)


# =====================================================================================
# «Український преміум» — the same claim told in different ways (facts: review/pp/AUDIT-README.txt)
# =====================================================================================
full("u01-buy-ukrainian", "flirt-tw-1", "50% 30%", "Купуйте українське.", "Носіть красиве.",
     "Obiimy — український бренд шовкових аксесуарів з авторськими принтами.", "1 600 грн", "", "Обрати твіллі «Флірт»", note="Buy Ukrainian")
full("u02-london", "zolote-44-2", "50% 20%", "Українська хустка,", "яку продають у\u00a0Лондоні.",
     "Obiimy — в UFD London та Be\u00a0Brave Canada.", "від 2 400 грн", "", "Обрати «Золоте світло»", note="Sold abroad", hs=76)
full("u03-made-in-ua", "krok-44-4", "45% 20%", "Зроблено в Україні.", "Відчувається на дотик.",
     "100% італійський шовк, авторський принт, двосторонній друк.", "2 400 грн", "", "Обрати «Сміливий крок»", note="Made in Ukraine", hs=78)
full("u04-not-mass", "puls-tw-3", "50% 20%", "Авторський принт.", "Український бренд.",
     "Принти художниці й засновниці бренду Світлани Сніжко — на натуральному шовку.", "1 600 грн", "", "Обрати «Пульс»", note="Not mass market", hs=76)
full("u05-luxury", "tysha-88-2", "50% 50%", "Розкіш", "бути собою.",
     "Натуральний шовк преміальної якості.", "6 600 грн", "", "Обрати «Тишу всередині»", note="Luxury of being yourself", box=(-110, 1920))
full("u06-abroad", "iskra-tw-2", "50% 25%", "Подарунок з України,", "яким пишаються.",
     "Для рідних за кордоном. Міжнародна доставка — за тарифами перевізника.", "1 600 грн", "", "Надіслати подарунок", note="Gift abroad", hs=78)

ivory("u07-hand-edge", "Шовкова хустка «Іскра»", "Ручна робота там,", "де її не видно.",
      f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;overflow:hidden"><img class="cut" src="{CUT("iskra-65-5")}" alt="" style="height:96%;width:auto"></div>',
      "Край кожної хустки обробляють вручну.", "4 800 грн", "«Іскра» · 65 × 65", "Роздивитися хустку", note="Hand-finished edge")
tags = [("100% італійський шовк", "left:0;top:6%"), ("Авторський принт", "right:0;top:6%"), ("Двосторонній друк", "left:0;bottom:8%"), ("Ручна обробка краю", "right:0;bottom:8%")]
details = (f'<div style="position:absolute;inset:0;display:grid;place-items:center"><img class="cut" src="{CUT("tysha-88-1")}" alt="" style="max-height:74%;max-width:66%;width:auto;height:auto;transform:rotate(-4deg)"></div>'
           + "".join(f'<p style="position:absolute;{pos};background:#fff;padding:14px 24px;border-radius:999px;font-size:30px;font-weight:600;box-shadow:0 14px 26px -16px rgba(0,0,0,.4)">{t}</p>' for t, pos in tags))
ivory("u08-details", "Шовкова хустка «Тиша всередині»", "Преміум —", "це деталі.", details,
      "Усе, що робить шовк преміальним, — в одній хустці.", "6 600 грн", "«Тиша всередині» · 88 × 88", "Обрати хустку", note="Premium is details")
step = lambda img, label, extra="": f'<div style="display:grid;justify-items:center;gap:18px"><div style="width:290px;height:620px;{img};box-shadow:0 18px 28px -18px rgba(0,0,0,.45){extra}"></div><p style="font-size:30px;font-weight:600">{label}</p></div>'
process = (f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:space-between">'
           + step(f"background:url({HI(PP['avantiura'])}) center/330%", "Авторський принт")
           + '<p style="font-size:50px;color:var(--ink-3)">→</p>'
           + step(f"background:url({CUT('avantiura-88-1')}) center/92% no-repeat,linear-gradient(165deg,{PP['avantiura']['c']},{PP['avantiura']['deep']})", "Шовкова хустка")
           + '<p style="font-size:50px;color:var(--ink-3)">→</p>'
           + step(f"background:url({S2('avantiura-88-2')}) 42% 40%/cover", "Ваш образ")
           + '</div>')
ivory("u09-from-painting", "Шовкова хустка «Авантюра»", "Від принту художниці", "до вашого образу.", process,
      "Авторський принт, натуральний шовк, ручна обробка краю.", "6 600 грн", "хустка «Авантюра»", "Обрати хустку", bg="var(--stone)", note="From painting to scarf", hs=88)
logos = "".join(f'<p style="font-family:Prata,serif;font-size:50px;line-height:1.3">{n}</p>' for n in ["UFD London", "Be Brave · Канада", "INTERTOP", "Hram"])
trust = (f'<div style="position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:30px">'
         f'<div style="display:grid;place-items:center"><img class="cut" src="{CUT("krok-44-1")}" alt="" style="width:100%;max-width:440px;transform:rotate(-5deg)"></div>'
         f'<div style="text-align:left"><p style="font-size:28px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--ink-3)">Продається в</p>{logos}'
         f'<p style="font-size:28px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--ink-3);margin-top:30px">Про нас писали</p><p style="font-family:Prata,serif;font-size:44px;line-height:1.3">LIGA.net<br>INSIDER\u00a0UA</p></div></div>')
ivory("u10-trust", "Український бренд шовку", "Про нас пишуть.", "Нас носять.", trust,
      "Obiimy — український бренд шовкових хусток, твіллі й аксесуарів з авторськими принтами.", "2 400 грн", "хустка «Сміливий крок»", "Обрати хустку", note="Press and retail")
ivory("u11-slow", "Шовкова хустка «Золоте світло»", "Одна хустка з України", "замість десяти випадкових.",
      f'<div style="position:absolute;inset:0;display:grid;place-items:start center"><img class="cut" src="{CUT("zolote-44-1")}" alt="" style="width:700px;transform:rotate(-5deg);margin-top:30px"></div>',
      "У світі швидких трендів — речі зі змістом: натуральний шовк, що стає частиною вашої історії.", "2 400 грн", "«Золоте світло» · 44 × 44", "Обрати хустку", note="Slow fashion", hs=78)


# =====================================================================================
# «Тихий преміум» — short lines, one product line without sizes, delicate CTAs
# =====================================================================================
QUIET = [
    ("p01-quiet-luxury", "zolote-44-3", "50% 25%", False, "Бездоганна елегантність.", "Український бренд.", "Авторські принти на натуральному шовку.", ["zolote-44-1"], "Шовкова хустка «Золоте світло»", "від 2 400 грн", "Подивитися ближче"),
    ("p02-speaks", "avantiura-88-5", "62% 30%", False, "Шовк, який", "говорить за вас.", "", ["avantiura-88-1"], "Шовкова хустка «Авантюра»", "6 600 грн", "Знайти свій принт"),
    ("p05-character", "krok-44-2", "74% 30%", True, "Український шовк", "з характером.", "Принт «Сміливий крок» — довіра до себе.", ["krok-44-1"], "Шовкова хустка «Сміливий крок»", "від 2 400 грн", "Знайти свою"),
    ("p06-noticed", "avantiura-tw-3", "50% 40%", False, "Деталь,", "яку помічають.", "", ["avantiura-tw-5"], "Шовкова твіллі «Авантюра»", "1 600 грн", "Подарувати собі"),
    ("p07-whole-look", "iskra-tw-2", "50% 25%", False, "Один аксесуар —", "весь образ.", "", ["iskra-tw-4"], "Шовкова твіллі «Іскра»", "1 600 грн", "Подивитися образ"),
    ("p08-touch", "flirt-65-3", "38% 30%", False, "Шовк, до якого", "хочеться торкатися.", "«Флірт» — це насамперед стан.", ["flirt-65-1"], "Шовкова хустка «Флірт»", "4 800 грн", "Відкрити колекцію"),
    ("p09-for-her", "puls-44-4", "50% 20%", False, "Для неї.", "Або для себе.", "Індивідуальне пакування.<br>Підпишемо вашими словами.", ["puls-44-1"], "Шовкова хустка «Пульс»", "2 400 грн", "Обрати подарунок"),
    ("p11-italian-silk", "avantiura-88-4", "38% 50%", False, "Італійський шовк.", "Український характер.", "", ["avantiura-88-1"], "Шовкова хустка «Авантюра»", "6 600 грн", "Детальніше"),
    ("p12-wearable-art", "puls-44-2", "42% 40%", False, "Мистецтво,", "яке можна носити.", "Авторські принти українських художників.", ["puls-44-1"], "Шовкова хустка «Пульс»", "від 2 400 грн", "Переглянути SOLO"),
    ("p15-iskra", "iskra-65-2", "40% 0%", False, "Колір, який", "обирають сміливі.", "Принт «Іскра» — сміливість бути помітною.", ["iskra-65-1"], "Шовкова хустка «Іскра»", "4 800 грн", "Роздивитися «Іскру»"),
]
for id, ph, pos, spot, h, em, body, cuts, title, price, cta in QUIET:
    MIN[id] = (cuts, title)
    full(id, ph, pos, h, em, body, price, "", cta, spot=spot, note=f"Quiet premium: {h} {em}", hs=86,
         shade_from=1120 if id == "p06-noticed" else 980 if spot else 1040, **({"box": (110, 1320)} if id == "p06-noticed" else {"box": (210, 1920)} if id == "p12-wearable-art" else {"box": (50, 1920)} if id == "p01-quiet-luxury" else {"box": (190, 1730)} if id == "p09-for-her" else {}))

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · SOLO classic</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Prata&family=Onest:wght@300;400;500;600&family=Montserrat:wght@300;400;500&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("solo5.html" if YELLOW else "solo4.html")).write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "creatives (classic)")
