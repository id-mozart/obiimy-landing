"""Black Friday home banners built from the «Чорна п’ятниця» draft of /discounts (16.11.2026, the client: «и ещё варианты для чёрной
пятницы баннера на главную»). Same frames as build_home.py (Horoshop Desktop LINE 1 1920 × 576 and Mobile LINE 1 1920 × 768, rendered
at DPR 2) and the same lock-up, but the picture side carries the draft's own products as white cards with the yellow «−30 %» badge and
the real prices — the discount is no longer a range, the draft fixed it per article. Data: draft-products.json; photos: photo/bf-draft.
  python3 bf/build_home_products.py                                                 → bf/home-products.html
  cd ads && DPR=2 VW=2000 ADS=bf/home-products.html OUT=bf/out-home node render.mjs  → out-home/bfh-2*.jpg
  python3 bf/build_home.py finish                                                   → out-home/final (all bfh-*)"""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import build_home as BH                                   # the frames, the CSS and the lock-up of the first fourteen
from common import nbh, YEL, INK, CREAM

P = {p["article"]: p for p in json.load(open(HERE / "draft-products.json", encoding="utf-8"))}
PD = "../../photo/bf-draft/"; NBSP, THIN = " ", " "
def money(v): return f"{int(round(v)):,}".replace(",", NBSP) + NBSP + "грн"
def pct(a): return int(P[a]["value"] or 0)
def new(a): return P[a]["full"] * (1 - pct(a) / 100)
def count(prefix=None, cat=None, value=None):
    return sum(1 for p in P.values() if (prefix is None or p["article"].startswith(prefix)) and (cat is None or p["category"] == cat) and (value is None or p["value"] == value))
TOTAL = sum(1 for p in P.values() if p["value"]); MAXP = max(pct(a) for a in P)
KICK = "Чорна п’ятниця · добірка зі знижками"

EXTRA = """
.pc { background: #fff; box-shadow: 0 40px 80px -24px rgba(0,0,0,.7), 0 6px 14px rgba(0,0,0,.3); overflow: hidden; }
.pc img { width: 100%; height: 100%; object-fit: cover; display: block; }
.bd { display: inline-block; background: #F2B705; color: #141110; box-shadow: 0 0 0 3px #141110; font-family: 'Montserrat', sans-serif; font-weight: 500; border-radius: 999px; line-height: 1; letter-spacing: -.01em; white-space: nowrap; font-variant-numeric: tabular-nums; z-index: 6; }
.pr { font-family: 'Montserrat', sans-serif; font-weight: 400; color: #F3EADB; white-space: nowrap; font-variant-numeric: tabular-nums; text-align: center; }
.pr s { color: #9A9088; margin-right: .3em; font-weight: 300; }
"""
ZOOM = {"222-1": 2.1, "333-1": 2.1, "444-1": 2.0, "555-1": 2.1}; POS = {}
for _a in P:
    if _a.startswith("R-"): ZOOM.setdefault(_a, 1.5); POS.setdefault(_a, "50% 85%")
ads = []
def ad(id, body, cls="", note=""): ads.append(f'\n<!-- {note} -->\n<section class="ad {cls}" id="{id}">{body}\n</section>')
def both(id, build, note=""):
    ad(id, build(576, False), note=note); ad(id + "-mobile", build(768, True), cls="mobile", note=note + " · mobile 5:2")

def card(a, x, y, w, h, rot=0, zoom=1.0, bsize=28, z=3, price=False, pos="50% 50%"):
    r = f"transform:rotate({rot}deg);" if rot else ""
    zoom = zoom if zoom != 1.0 else ZOOM.get(a, 1.0); pos = POS.get(a, pos) if pos == "50% 50%" else pos
    out = f'<div class="pc" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{r}z-index:{z}"><img src="{PD}{a}.jpg" alt="" style="object-position:{pos};transform:scale({zoom})"></div>'
    out += f'<p class="bd" style="left:{x + 16}px;top:{y + 16}px;font-size:{bsize}px;padding:{int(bsize * .42)}px {int(bsize * .62)}px;{r}transform-origin:-16px -16px;z-index:{z + 1}">−{pct(a)}{THIN}%</p>'
    if price: out += f'<p class="pr" style="left:{x}px;top:{y + h + 12}px;width:{w}px;font-size:{int(w * .085)}px"><s>{money(P[a]["full"])}</s>{money(new(a))}</p>'
    return out

def row(arts, H, mob, x0=None, zoom=1.0, price=False, maxw=None, rows_n=1):
    """Square cards from `x0` to the right edge in one or two rows, as large as the frame allows (bleeding a little past the edges)."""
    gap = 22; n = len(arts); x0 = (x0 if not mob else max(x0 or 0, 1040)) or 1000; cols = (n + rows_n - 1) // rows_n
    pl = 48 if price else 0
    size = min((1920 - x0 - 28 - gap * (cols - 1)) // cols, (H - 56 - gap * (rows_n - 1)) // rows_n - pl, maxw or 9999)
    y0 = (H - rows_n * size - (rows_n - 1) * gap - rows_n * pl) // 2
    return "".join(card(a, x0 + (i % cols) * (size + gap), y0 + (i // cols) * (size + gap + pl), size, size, zoom=zoom, price=price, bsize=26 if size < 300 else 32) for i, a in enumerate(arts))

def fan(arts, H, mob, x0=None, size=None, rots=(-7, 2, 8), dys=(30, 0, 26), step=None):
    size = size or (min(H - 90, 470) if not mob else min(H - 110, 560)); x0 = x0 or (1030 if not mob else 1070); step = step or int(size * .62)
    y = (H - size) // 2
    return "".join(card(a, x0 + i * step, y + dy, size, size, rot=r, z=3 + i, bsize=30) for i, (a, r, dy) in enumerate(zip(arts, rots, dys)))

def mosaic(arts, H, mob, x0=None, cols=4):
    gap = 18; x0 = (x0 if not mob else max(x0 or 0, 1040)) or 980; rows_n = (len(arts) + cols - 1) // cols
    size = min((1920 - x0 - 28 - gap * (cols - 1)) // cols, (H - 56 - gap * (rows_n - 1)) // rows_n)
    y0 = (H - rows_n * size - (rows_n - 1) * gap) // 2
    return "".join(card(a, x0 + (i % cols) * (size + gap), y0 + (i // cols) * (size + gap), size, size, bsize=22) for i, a in enumerate(arts))

def L(big, small, pill, mob, num=None, width=None, xl=True, bigsize=None, kicker=None):
    """Desktop: the full lock-up. Mobile (the frame is shown at a third of its size on a phone): the headline larger, the paragraph
    and the second button dropped — the yellow price pill is the only call (the art director, 16.11)."""
    if mob: return BH.lock(big, None, kicker=kicker or KICK, num=num, pill=pill, more=None, k=1.15, width=width or 760, xl=True, bigsize=bigsize or 100)
    return BH.lock(big, small, kicker=kicker or KICK, num=num, pill=pill, k=1, width=width or 860, xl=xl, bigsize=bigsize)

n44 = len({re.search(r"[«\"]([^»\"]+)[»\"]", p["name"]).group(1) if re.search(r"[«\"]([^»\"]+)[»\"]", p["name"]) else p["name"] for p in P.values() if "44-" in p["article"] and p["article"].endswith("-D") and p["value"] == 20})   # distinct prints: 44-xx-D and P-44-xx-D are the same scarf listed twice
n84 = count("84-", value=30); nR = sum(1 for p in P.values() if p["article"].startswith("R-") and p["article"] != "R-as" and p["value"] == 30)

def v_khustky(H, mob):
    return f'<div style="inset:0;background:{INK}"></div>' + fan(["44-21-D", "44-22-D", "44-25-D"], H, mob) + \
        L(f"Двосторонні хустки 44{NBSP}см. −20{THIN}%.", f"«Натхнення», «Сміливий дотик», «Грація» і ще {n44 - 3} принтів 44{THIN}×{THIN}44.", f"{money(new('44-21-D'))} замість {money(P['44-21-D']['full'])}", mob)
both("bfh-21-khustky", v_khustky, "Three 44 cm scarves as cards with −20 % badges")

def v_tvilli(H, mob):
    arts = ["84-7", "84-27", "84-24", "84-30", "84-19", "84-2"]
    return f'<div style="inset:0;background:{INK}"></div>' + row(arts, H, mob, rows_n=2) + \
        L(f"Твіллі 84{NBSP}см. −30{THIN}%.", f"{n84} принтів: «Спокуса», «Мелодія двох», «Відновлення», «Коло сонця», «Ранкова кава»…", f"{money(new('84-7'))} замість {money(P['84-7']['full'])}", mob)
both("bfh-22-tvilli", v_tvilli, "A row of twillies 84 × 5, −30 %")

def v_rezynky(H, mob):
    arts = ["R-16", "R-18", "R-4", "R-7", "R-11", "R-6"]
    return f'<div style="inset:0;background:{INK}"></div>' + row(arts, H, mob, x0=1000 if not mob else 1040, rows_n=2) + \
        L(f"Резинки. −30{THIN}%.", f"Шовкова резинка на жовтій коробці — {nR} принти в добірці.", f"{money(new('R-16'))} замість {money(P['R-16']['full'])}", mob)
both("bfh-23-rezynky", v_rezynky, "A row of scrunchies on their yellow boxes, −30 %")

def v_kiltsia(H, mob):
    return f'<div style="inset:0;background:{INK}"></div>' + row(["222-1", "333-1", "444-1", "555-1"], H, mob, zoom=2.1, rows_n=2, x0=1080 if not mob else 1060) + \
        L(f"Кільця для хустки. −30{THIN}%.", "«Безкінечність», «Х стиль», «Циліндр», «Н стиль» кольору Gold — до хустки чи твіллі зі знижкою.", f"{money(new('222-1'))} замість {money(P['222-1']['full'])}", mob)
both("bfh-24-kiltsia", v_kiltsia, "Four gold scarf rings, −30 %")

def v_son(H, mob):
    return f'<div style="inset:0;background:{INK}"></div>' + row(["M-6", "NM-6", "M-96"] if not mob else ["M-6", "NM-6", "M-96", "M-27"], H, mob, x0=980 if not mob else 1060, maxw=H - 60, rows_n=1 if not mob else 2) + \
        L(f"Маски й набори для сну. −20{THIN}%.", f"Маска «Енергія» — {money(new('M-6'))}, набір для сну в коробці — {money(new('NM-6'))}, «Серцебиття» — {money(new('M-96'))}.", "Усі маски −20 %", mob, bigsize=76 if not mob else 92)
both("bfh-25-son", v_son, "Masks and the sleep set, −20 %")

def v_dobirka(H, mob):
    arts = ["44-22-D", "84-7", "R-7", "M-6", "222-1", "NM-6", "140-1", "88-33-D"] if not mob else ["44-22-D", "84-7", "R-7", "M-6", "222-1", "NM-6"]
    return f'<div style="inset:0;background:{INK}"></div>' + mosaic(arts, H, mob, cols=4 if not mob else 3, x0=960 if not mob else 900) + \
        L(f"{TOTAL} товари. До −{MAXP}{THIN}%.", "Хустки, твіллі, маски, резинки, кільця й набори — вся добірка Чорної п’ятниці на obiimy.world.", f"Знижки до −{MAXP} %", mob)
both("bfh-26-dobirka", v_dobirka, "The mosaic: eight products of the selection with their badges")

HEAD = BH.HEAD.replace("</style>", EXTRA + "</style>")
(HERE / "home-products.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "home frames from the draft →", "home-products.html")

# ─── the third batch (16.11, «и потом ещё варианты баннера для ЧП на главную»): other layouts around the same products ─────────
LB = "../../photo/lookbook/"
EXTRA2 = """
.yellow .bd { background: #141110; color: #F2B705; box-shadow: 0 0 0 3px #F2B705; }
.band { background: #fff; box-shadow: 0 40px 80px -24px rgba(0,0,0,.7); overflow: hidden; }
.band img { width: 100%; height: 100%; object-fit: cover; display: block; }
.bigp { font-family: 'Montserrat', sans-serif; font-weight: 300; letter-spacing: -.04em; line-height: .92; color: #F2B705; white-space: nowrap; font-variant-numeric: tabular-nums; }
.bigp s { color: #9A9088; font-weight: 300; font-size: .5em; letter-spacing: -.02em; margin-right: .25em; vertical-align: .55em; }
.bigp span { font-size: .4em; letter-spacing: 0; color: #F3EADB; margin-left: .1em; }
.yellow .bigp { color: #141110; } .yellow .bigp span { color: #4B423B; } .yellow .bigp s { color: #8A6A12; }
"""
HEAD = HEAD.replace("</style>", EXTRA2 + "</style>")

def v_model(H, mob):
    """A lookbook portrait melting into the field at the right, two product cards of the draft over it, the words at the left."""
    cs = 290 if not mob else 320
    cards = (card("44-22-D", 880, H - cs - 50, cs, cs, rot=-5, z=5, bsize=30) + card("84-27", 880 + int(cs * .8), H - cs - 100, cs, cs, rot=4, z=6, bsize=30)) if not mob else card("44-22-D", 1060, H - cs - 60, cs, cs, rot=-5, z=5, bsize=30)
    return f'<div style="inset:0;background:{INK}"></div>' + BH.feathered(LB + "lb47-49-L.webp", 1000 if not mob else 960, 440, "50% 8%" if not mob else "30% 8%") + cards + \
        L(f"Чорна п’ятниця на шовк.", f"{TOTAL} товари добірки зі знижкою −10 / −20 / −30 %: хустки, твіллі, маски, резинки, кільця й набори.", f"Знижки до −{MAXP} %", mob, width=760 if not mob else 700, kicker=f"Добірка зі знижками · {TOTAL} товари")
both("bfh-31-model", v_model, "The lookbook portrait with two product cards over it")

def v_yellow(H, mob):
    """The brand's yellow field, the mosaic with ink badges, the lock-up inverted."""
    arts = ["44-21-D", "84-7", "R-4", "M-6", "222-1", "NM-6"] if not mob else ["44-21-D", "84-7", "R-4", "M-6"]
    return f'<div style="inset:0;background:{YEL}"></div>' + mosaic(arts, H, mob, cols=3 if not mob else 2, x0=1020 if not mob else 1100) + \
        L(f"Жовта п’ятниця. До −{MAXP}{THIN}%.", f"{TOTAL} товари добірки: хустки, твіллі, маски, резинки, кільця й набори — кожен зі своєю знижкою на картці.", f"Знижки до −{MAXP} %", mob, kicker=f"Добірка зі знижками · {TOTAL} товари")
def both_cls(id, build, note, cls):
    ad(id, build(576, False), cls=cls, note=note); ad(id + "-mobile", build(768, True), cls=cls + " mobile", note=note + " · mobile 5:2")
both_cls("bfh-32-yellow", v_yellow, "The yellow field with the mosaic", "yellow")

def bigprice(a, mob, size=190):
    return f'<p class="bigp" style="font-size:{size}px;margin-top:14px"><s>{money(P[a]["full"]).replace(NBSP + "грн", "")}</s>{money(new(a)).replace(NBSP + "грн", "")}<span>грн</span></p>'

def v_price(H, mob):
    """The price as the hero: «700 → 490 грн» huge, one scrunchie card large at the right."""
    cs = min(H - 80, 520 if not mob else 620)
    k = 1.15 if mob else 1
    lock = BH.lock("", None, kicker=KICK, num=f'<s style="font-size:.5em;color:#9A9088;vertical-align:.55em;margin-right:.25em">{money(P["R-4"]["full"]).replace(NBSP + "грн", "")}</s>{money(new("R-4")).replace(NBSP + "грн", "")}<span> грн</span>', pill="Резинки −30 %", more=None if mob else BH.CTA, k=k, width=860 if not mob else 760, numsize=240 if not mob else 190)
    lock = lock.replace('<p class="big"></p>', "")
    return f'<div style="inset:0;background:{INK}"></div>' + card("R-4", 1120 if not mob else 1920 - cs - 60, (H - cs) // 2, cs, cs, bsize=34, zoom=1.5, pos="50% 85%") + lock
both("bfh-33-price", v_price, "The price pair huge, one scrunchie large")

def v_bandflat(H, mob):
    """Flat 44 cm scarves as one continuous white band from the lock-up to the right edge, each with its badge."""
    arts = ["44-21-D", "44-22-D", "44-25-D", "44-26-D", "44-18-D"] if not mob else ["44-21-D", "44-22-D", "44-25-D"]
    x0 = 1000 if not mob else 1040; n = len(arts); w = (1920 - x0) // n + 1; h = H - 80; y = 40
    tiles = "".join(f'<div class="band" style="left:{x0 + i * (w - 1)}px;top:{y}px;width:{w}px;height:{h}px;z-index:3"><img src="{PD}{a}.jpg" alt="" style="object-position:50% 50%;transform:scale(1.02)"></div>'
                    f'<p class="bd" style="left:{x0 + i * (w - 1) + 16}px;top:{y + 16}px;font-size:28px;padding:12px 17px;z-index:4">−{pct(a)}{THIN}%</p>' for i, a in enumerate(arts))
    return f'<div style="inset:0;background:{INK}"></div>' + tiles + L(f"Двосторонні хустки 44{NBSP}см. −20{THIN}%.", "Одинадцять принтів із двостороннім друком.", f"{money(new('44-21-D'))} замість {money(P['44-21-D']['full'])}", mob, width=840 if not mob else 720)
both("bfh-34-band", v_bandflat, "A continuous band of flat 44 cm scarves")

def v_coupon(H, mob):
    """The yellow coupon with the twilly price, the twilly card at the right."""
    k = 1.12 if mob else 1
    tk = (f'<div class="tk" style="position:absolute;left:84px;top:50%;transform:translateY(-50%) scale({k});transform-origin:0 50%;width:{780 if not mob else 720}px">'
          f'<p class="k">{KICK}</p><p class="num" style="font-size:{140 if not mob else 118}px"><span style="font-size:.5em;letter-spacing:0;color:#8A6A12;vertical-align:.55em;margin-right:.2em">−30 %</span>{money(new("84-7")).replace(NBSP + "грн", "")}<span> грн</span></p>'
          + ("" if mob else f'<p class="l">Твіллі 84 см замість {money(P["84-7"]["full"])} — {n84} принтів у добірці</p><p class="more">{BH.CTA}</p>') + '</div>')
    cs = min(H - 80, 520 if not mob else 620)
    return f'<div style="inset:0;background:{INK}"></div>' + tk + card("84-7", 1920 - cs - 80 if not mob else 1920 - cs - 60, (H - cs) // 2, cs, cs, bsize=34, rot=3) + card("84-27", 1920 - cs - 80 - int(cs * .55) if not mob else 1920 - cs - 60 - int(cs * .5), (H - cs) // 2 + 20, cs, cs, bsize=34, rot=-5, z=2)
both("bfh-35-coupon", v_coupon, "The coupon with the twilly price and two twilly cards")

def v_sleep(H, mob):
    """Two sleep products large with their prices under the cards."""
    cs = min(H - 170, 400 if not mob else 390); gap = 36; x0 = 1920 - 2 * cs - gap - 70
    cards = card("M-6", x0, (H - cs - 56) // 2, cs, cs, bsize=32, price=True) + card("NM-6", x0 + cs + gap, (H - cs - 56) // 2, cs, cs, bsize=32, price=True)
    return f'<div style="inset:0;background:{INK}"></div>' + cards + L(f"Сон зі знижкою −20{THIN}%.", "Шовкова маска «Енергія» і набір для сну в жовтій коробці — подарунок, який не треба пакувати.", "Маски й набори −20 %", mob, width=800 if not mob else 700)
both("bfh-37-sleep", v_sleep, "Mask and sleep set large with prices")

(HERE / "home-products.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "home frames incl. the third batch")
