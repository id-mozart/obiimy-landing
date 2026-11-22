"""Black Friday, the series after the FINAL home banner bfh-51-four (22.11.2026, the client: «новую серию креативов на чёрную пятницу —
по мотивам этого нашего баннера на главной, и с этими картинками, и с 1 картинкой красиво во весь баннер, и с другими товарами
из чёрной пятницы вариантами»). The banner's language: the dark field, «Чорна п’ятниця» in the brand yellow (Montserrat), the sub-line
«Неймовірні знижки в OBIIMY» in the same face, lifestyle frames with a tight yellow «−20%» circle on the foot of each, no captions,
the outlined «Дивитися всі →» instead of a yellow pill. Photos: the products' own galleries on obiimy.world (photo/bf-draft/life/);
the discount of every frame is its article's value in the client's draft (ads/bf/draft-products.json).
Three templates: `four` (the banner's four frames in a row or a 2 × 2 grid), `hero` (one frame edge to edge, the words on the
bottom veil, one circle by the product), and the same two on other sets of discounted goods.
  python3 bf/build_final.py                       → bf/bff.html   (FORMAT=story|feed|square → bff-<format>.html)
  cd ads && ADS=bf/bff.html OUT=bf/out-final node render.mjs   (and FORMAT=… OUT=bf/out-final-<format>)"""
import json, pathlib
from common import *
HERE = pathlib.Path(__file__).parent
P = {p["article"]: p for p in json.load(open(HERE / "draft-products.json", encoding="utf-8"))}
LIVE = json.load(open(HERE / "live-discounts.json", encoding="utf-8"))   # 22.11: the discounts as /black-friday/ shows them (92 articles); the draft is the fallback
PL = "../../photo/bf-draft/life/"
NBSP = " "
def pct(a): return int(LIVE[a]["disc"] if a in LIVE else (P[a]["value"] or 0))

BIG, SMALL, CTA = "Чорна п’ятниця", f"Неймовірні знижки в{NBSP}OBIIMY", "Дивитися всі"
EXTRA = """
.big.yel { color: #F2B705; }
.sub { font-family: 'Montserrat', sans-serif; font-weight: 400; color: #D9CDB9; line-height: 1.2; letter-spacing: -.01em; }
.ci { display: flex; align-items: center; justify-content: center; border-radius: 50%; background: #F2B705; color: #141110; box-shadow: 0 16px 30px -12px rgba(0,0,0,.7); font-family: 'Onest', 'Montserrat', sans-serif; font-weight: 700; letter-spacing: -.07em; line-height: 1; white-space: nowrap; font-variant-numeric: tabular-nums; z-index: 6; }
.more { display: inline-flex; align-items: center; gap: .45em; font-family: 'Onest', sans-serif; font-weight: 600; letter-spacing: .02em; border: 2.5px solid #F3EADB; border-radius: 999px; color: #F3EADB; white-space: nowrap; background: rgba(20,17,16,.35); }
.more::after { content: "→"; font-weight: 400; }
.tile { overflow: hidden; background: #2A2522; } .tile img { width: 100%; height: 100%; object-fit: cover; display: block; }
"""
# frame = (file in photo/bf-draft/life, article for the discount, focus for a tall slice, focus for the hero)
F = {
 "columns": ("88-11-01",   "88-11",   "52% 22%", "50% 30%"),    # «Впевненість» 88, the columns, the red floral blazer
 "chystyi": ("65-20-D-02", "65-20-D", "50% 14%", "50% 20%"),    # «З чистого листа» 65 knotted over the black top, the field
 "coffee":  ("88-33-D",    "88-33-D", "56% 40%", "50% 40%"),    # «Флірт» on the trench, the coffee and Vogue
 "sofa":    ("84-27-02",   "84-27",   "50% 20%", "50% 30%"),    # twilly «Мелодія двох», the cream suit on the leather sofa
 "fur":     ("84-24-02",   "84-24",   "50% 32%", "50% 35%"),    # twilly «Відновлення» in the teal fur, the field
 "camel":   ("65-24-01",   "65-24-D", "50% 30%", "50% 25%"),    # «Відновлення» 65 on the camel coat, profile (the 2D article is the one on /black-friday/)
 "trench":  ("88-22-D-02", "88-22-D", "50% 25%", "50% 25%"),    # «Сміливий дотик» 88 on the beige trench, the field
 "pashe":   ("P-44-12-02", "P-44-12", "50% 60%", "50% 55%"),    # the knotted pashe «Поцілунок Сонця», the dark close-up
 "blue":    ("88-25-D-02", "88-25-D", "50% 20%", "50% 30%"),    # «Грація» 88 as a belt on the blue blazer, the sky
 "leopard": ("65-21-D-04", "65-21-D", "50% 25%", "50% 25%"),    # «Натхнення» 65 on the trench, face to camera
 "suit":    ("140-16-01",  "140-16",  "50% 15%", "50% 25%"),    # twilly 140 «Соковиті спогади» as a tie on the black suit
 "leather": ("140-31-01",  "140-31",  "64% 20%", "60% 25%"),    # twilly 140 «Піднесення» on the black leather
 "mustard": ("P-44-98-00", "P-44-98", "60% 35%", "55% 30%"),    # pashe «Синій» on the mustard trench
 "scrunch": ("R-23",       "R-23",    "50% 40%", "50% 40%"),    # scrunchie «Баланс» on the ponytail
 "wine":    ("44-24-D-00", "44-24-D", "50% 45%", "50% 45%"),    # pashe «Відновлення» 44 knotted on the white shirt, the dark red
 "camel2":  ("88-24-03",   "88-24",   "50% 16%", "50% 22%"),    # «Відновлення» 88 on the camel coat, face to camera, the field
 "beige":   ("140-30-01",  "140-30",  "50% 18%", "50% 25%"),    # twilly 140 «Коло сонця» on the beige coat, the studio
 # 22.11, the client: «ещё вариантов с разными товарами из /black-friday/» — frames from the galleries of the other discounted goods
 "tee":     ("t-shirt-21L-03", "t-shirt-21L", "50% 30%", "50% 35%"),   # the T-shirt «Натхнення» with the scarf at the waist, −40
 "shirt":   ("C-10S-03",   "C-10S",   "50% 25%", "50% 30%"),    # the shirt «Маків цвіт» with the bow, the columns, −20
 "man":     ("P-44-12-D-02", "P-44-12-D", "50% 30%", "50% 35%"),  # the man in the white suit, the pocket square «Поцілунок сонця», −20
 "redpashe":("44-38-D-02", "44-38-D", "50% 25%", "50% 30%"),    # «Сміливий крок» 44 on the brown satin top, the terrace, −10
 "fieldtr": ("65-22-D-03", "65-22-D", "50% 25%", "50% 25%"),    # «Сміливий дотик» 65 on the trench, the field, −10
 "leath2":  ("65-31-D-03", "65-31-D", "55% 25%", "55% 30%"),    # «Піднесення» 65 on the black leather, −10
 "tiedark": ("84-11-03",   "84-11",   "50% 25%", "50% 30%"),    # twilly «Впевненість» on the black blazer, the dark field, −30
 "yelblue": ("84-8-02",    "84-8",    "50% 30%", "50% 35%"),    # twilly «Сміливість» on the neck, the black top, −30
 "leathtw": ("84-31-02",   "84-31",   "50% 30%", "50% 35%"),    # twilly «Піднесення» as a tie on the leather jacket, −30
 "hair":    ("84-16-05",   "84-16",   "50% 40%", "50% 45%"),    # the mint twilly in the hair, close, −30
 "neck":    ("84-23-02",   "84-23",   "50% 45%", "50% 50%"),    # twilly «Баланс» knotted on the neck, close, −30
 "ring":    ("111-1-03",   "111-1",   "50% 30%", "50% 35%"),    # the triple ring on the blue scarf, the black tee, −30
 "chpashe": ("P-44-20-D-03", "P-44-20-D", "50% 30%", "50% 35%"),  # pashe «З чистого листа» on the black top, the field, −20
}
FINAL = ["columns", "chystyi", "coffee", "sofa"]                          # the home banner's four, in the client's order

def circle(x, y, d, a):
    return f'<p class="ci" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;font-size:{int(d * .34)}px">−{pct(a)}%</p>'

def lockup(top, size=118, sub=40, left=64, width=952, align="left"):
    """«Чорна п’ятниця» yellow, the sub-line in the same face under it."""
    return (f'<div style="left:{left}px;width:{width}px;top:{top}px;z-index:5;text-align:{align}">'
            f'<p class="big yel" style="font-size:{int(size * K)}px">{BIG}</p>'
            f'<p class="sub" style="font-size:{int(sub * K)}px;margin-top:{int(14 * K)}px">{SMALL}</p></div>')

def ctabar():
    """The bottom row of the series, in the banner's manner: the outlined «Дивитися всі →» and the address, no yellow pill."""
    return (f'<div style="left:64px;right:64px;bottom:{BOTB}px;height:{BAR}px;display:flex;align-items:center;justify-content:space-between;z-index:6">'
            f'<span class="more" style="font-size:{int(38 * K)}px;padding:{int(22 * K)}px {int(44 * K)}px">{CTA}</span>'   # the client, 22.11: «заметней и чуть крупнее»
            f'<span class="hdr" style="font-size:{int(26 * K)}px;color:{CREAM};letter-spacing:.1em;text-transform:none">obiimy.world</span></div>')

def tiles(keys, left, right, top, bottom, cols=None, gap=None):
    """The frames as equal tiles with the circle on the foot of each; one row, or a grid of `cols` columns."""
    n = len(keys); cols = cols or n; rows = (n + cols - 1) // cols; gap = gap or int(16 * K)
    d = int((210 if cols <= 2 else 168) * K)          # the client, 22.11: the discount circle larger, then «ещё чуть крупнее и выше»
    w = (right - left - gap * (cols - 1)) // cols
    h = (bottom - top - gap * (rows - 1)) // rows
    ins = int(14 * K); up = int(26 * K)                 # the client, 22.11: the circle in the bottom-right corner of the frame, lifted a little
    out = ""
    for i, k in enumerate(keys):
        f, a, pos, _ = F[k]; r, c = divmod(i, cols)
        x = left + c * (w + gap); y = top + r * (h + gap)
        out += f'<div class="tile" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><img src="{PL}{f}.jpg" alt="" style="object-position:{pos}"></div>'
        out += circle(x + w - d - ins, y + h - d - ins - up, d, a)
    return out

def four(id, keys, note, grid=False):
    """The banner's layout: the words above, the four frames in a row (or a 2 × 2 grid), the bar below."""
    field = f'<div style="inset:0;background:{INK}"></div>'
    if SQ:
        if grid:   # the words on the left, the grid on the right
            body = field + header(True, hdr_text(BIG)) + lockup(Y0 + int(30 * K), size=96, sub=30, width=430) + tiles(keys, 520, 1016, Y0, Y1 - int(10 * K), cols=2, gap=12) + ctabar()
        else:
            body = field + header(True, hdr_text(BIG)) + lockup(Y0, size=96, sub=30) + tiles(keys, 64, 1016, Y0 + int(200 * K), Y1 - int(10 * K)) + ctabar()
    else:
        wh = int(230 * K)
        body = field + header(True, hdr_text(BIG)) + lockup(Y0 + int(10 * K)) + tiles(keys, 64, 1016, Y0 + wh + int(40 * K), Y1 - int(16 * K), cols=2 if grid else 4) + ctabar()
    ad(id, body, note)

def hero(id, key, note, cx=.62, cy=.58, size=118):
    """One frame edge to edge; the words on the dark veil at the foot; one circle by the product (cx, cy — fractions of the frame)."""
    f, a, _, pos = F[key]
    d = int(260 * K)                                    # the client, 22.11: larger, then larger and higher again
    body = f'''
  <div class="tile" style="inset:0;background:{INK}"><img src="{PL}{f}.jpg" alt="" style="object-position:{pos}"></div>
  <div style="left:0;right:0;top:0;height:{int(360 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,.6),rgba(12,9,8,0))"></div>
  <div style="left:0;right:0;bottom:0;height:{int(H * .5)}px;background:linear-gradient(0deg,rgba(20,17,16,1) {int(BOTB + BAR * .6)}px,rgba(20,17,16,.92) {int(BOTB + BAR + 120 * K)}px,rgba(20,17,16,0))"></div>
  {header(True, hdr_text(BIG))}
  {circle(1080 - 64 - d, H - BOTB - BAR - int(70 * K) - d, d, a)}
  {lockup(Y1 - int((330 if not SQ else 190) * K), size=size if not SQ else 96, sub=40 if not SQ else 30, width=1080 - 128 - d - int(24 * K))}
  {ctabar()}'''
    ad(id, body, note)

# ─── the series ──────────────────────────────────────────────────────────────────────────────────────────────────────────
# after the AD's round (8,0 / 7,0 / 7,0 on the first render): the «autumn» and «studio» grids dropped as duplicates, the fur / the
# trench in profile / the scarf-as-a-belt heroes replaced (the product was tiny or in shadow), the scrunchie from behind out of the rows
four("bff-01-final-row", FINAL, "The home banner's four frames in a row")
four("bff-02-final-grid", FINAL, "The home banner's four frames as a 2 × 2 grid", grid=True)
hero("bff-03-hero-columns", "columns", "One frame: the columns, «Впевненість» −10")
hero("bff-04-hero-chystyi", "chystyi", "One frame: «З чистого листа» in the field −20")
hero("bff-05-hero-coffee", "coffee", "One frame: «Флірт» on the trench, the coffee −10")
hero("bff-06-hero-sofa", "sofa", "One frame: the twilly on the sofa −30")
four("bff-07-field-row", ["fur", "camel", "trench", "pashe"], "Other goods: the fur, the camel coat, the trench, the dark pashe — in a row")
four("bff-08-field-grid", ["fur", "camel", "trench", "pashe"], "The same four as a grid", grid=True)
four("bff-09-autumn-row", ["blue", "leopard", "wine", "mustard"], "Other goods: the blue blazer, the leopard trench, the wine pashe, the mustard trench")
four("bff-10-studio-row", ["suit", "leather", "beige", "scrunch"], "Other goods, the studio set: the twilly tie, the leather, the beige coat, the scrunchie")
hero("bff-11-hero-camel", "camel2", "One frame: the camel coat, the pink scarf to camera −10")
hero("bff-12-hero-leopard", "leopard", "One frame: the leopard trench, face to camera −10")
hero("bff-13-hero-profile", "camel", "One frame: the camel coat in profile −20")
hero("bff-14-hero-pashe", "pashe", "One frame: the knotted pashe close-up −30")
hero("bff-15-hero-wine", "wine", "One frame: the wine pashe on the white shirt −20")
hero("bff-16-hero-suit", "suit", "One frame: the twilly as a tie on the black suit −20")
# other goods of /black-friday/ (22.11): the T-shirt −40, the shirt, the man's pocket square, twillies on the dark field, the ring
four("bff-17-dark-row", ["tiedark", "yelblue", "leath2", "leathtw"], "Other goods on the dark field: twilly on the blazer, twilly on the black top, the leather with «Піднесення», the leather tie")
four("bff-18-dark-grid", ["tiedark", "yelblue", "leath2", "leathtw"], "The same four as a grid", grid=True)
four("bff-19-wardrobe-row", ["tee", "shirt", "man", "redpashe"], "Other goods: the T-shirt −40, the shirt, the man's pocket square, the red pashe")
four("bff-20-wardrobe-grid", ["tee", "shirt", "man", "redpashe"], "The same four as a grid", grid=True)
four("bff-21-details-row", ["hair", "neck", "ring", "chpashe"], "Other goods, the details: the twilly in the hair, the twilly on the neck, the ring, the pashe in the field")
hero("bff-22-hero-tee", "tee", "One frame: the T-shirt «Натхнення» −40")
hero("bff-23-hero-shirt", "shirt", "One frame: the shirt «Маків цвіт» −20")
hero("bff-24-hero-man", "man", "One frame: the man's pocket square −20")
hero("bff-25-hero-tiedark", "tiedark", "One frame: the twilly on the black blazer −30")
hero("bff-26-hero-yelblue", "yelblue", "One frame: the twilly on the black top −30")
hero("bff-27-hero-redpashe", "redpashe", "One frame: the red pashe on the terrace −10")
hero("bff-28-hero-fieldtr", "fieldtr", "One frame: «Сміливий дотик» on the trench −10")

HEAD = f"""<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · Black Friday · after the final home banner</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;600&family=Montserrat:wght@300;400;500&family=Onest:wght@400;500;600;700&display=swap">
<style>{CSS}{EXTRA}</style></head><body>"""
name = "bff" + ("" if FORMAT == "plain" else f"-{FORMAT}") + ".html"
(HERE / name).write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "banners after the final →", name)
