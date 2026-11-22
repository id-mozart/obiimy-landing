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
    if mob: return BH.lock(big, None, kicker="Чорна п’ятниця", num=num, pill=pill, more=None, k=1.15, width=width or 760, xl=True, bigsize=bigsize or 100)
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


# ─── the fourth batch (16.11, «ещё варианты баннера на главную»): the receipt, budget shelves, three sizes, the pair, all scrunchies, the lookbook twilly ───
EXTRA3 = """
.rc { background: #F6F0E4; color: #141110; border-radius: 14px; box-shadow: 0 40px 80px -24px rgba(0,0,0,.7); font-family: 'Montserrat', sans-serif; }
.rc .ln { display: flex; align-items: center; gap: 14px; border-bottom: 1.5px dashed rgba(27,22,19,.25); padding: 10px 0; }
.rc .ln .th { flex: none; background: #fff; overflow: hidden; border-radius: 6px; width: 64px; height: 64px; } .rc .ln .th img { width: 100%; height: 100%; object-fit: cover; display: block; }
.rc .ln .nm { flex: 1; font-family: 'EB Garamond', serif; font-weight: 500; font-size: 26px; color: #1B1613; }
.rc .ln .old { color: #8A8378; text-decoration: line-through; font-weight: 300; font-size: 22px; } .rc .ln .nw { font-weight: 500; font-size: 26px; font-variant-numeric: tabular-nums; }
.rc .tot { display: flex; justify-content: space-between; align-items: center; border-top: 2px solid #141110; padding-top: 12px; margin-top: 4px; }
.tl { font-family: 'Onest', sans-serif; font-weight: 600; font-size: 18px; letter-spacing: .2em; text-transform: uppercase; color: #D9CDB9; white-space: nowrap; }
.plus { font-family: 'Montserrat', sans-serif; font-weight: 300; color: #F2B705; line-height: 1; text-align: center; }
.bb { background: #F2B705; color: #141110; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; font-family: 'Montserrat', sans-serif; box-shadow: 0 0 0 4px #141110, 0 24px 50px -16px rgba(0,0,0,.8); z-index: 9; }
.bb b { font-weight: 300; letter-spacing: -.04em; line-height: .9; } .bb i { font-style: normal; font-weight: 500; letter-spacing: .06em; text-transform: uppercase; margin-top: .4em; }
"""
HEAD = HEAD.replace("</style>", EXTRA3 + "</style>")
def money0(v): return money(v).replace(NBSP + "грн", "")
def short(a):
    m = re.search(r"[«\"]([^»\"]+)[»\"]", P[a]["name"]); return m.group(1) if m else P[a]["name"]
BASKET = ["44-21-D", "84-7", "R-4"]
tot_old = lambda arts: sum(P[a]["full"] for a in arts); tot_new = lambda arts: sum(new(a) for a in arts)

def v_receipt(H, mob):
    """A paper receipt with three products and the saving, the lock-up at the left."""
    w = 700 if not mob else 720; x = 1920 - w - 80; k = 1 if not mob else 1.1
    lines = "".join(f'<div class="ln"><div class="th"><img src="{PD}{a}.jpg" alt="" style="transform:scale({ZOOM.get(a, 1.0)});object-position:{POS.get(a, "50% 50%")}"></div><span class="nm">{short(a)} <span style="font-family:Montserrat,sans-serif;font-size:16px;color:#6B645C">−{pct(a)}{THIN}%</span></span><span class="old">{money0(P[a]["full"])}</span><span class="nw">{money(new(a))}</span></div>' for a in BASKET)
    rc = (f'<div class="rc" style="left:{x}px;top:50%;transform:translateY(-50%) scale({k});transform-origin:100% 50%;width:{w}px;padding:26px 30px">'
          f'<p class="bd" style="position:absolute;right:-14px;top:-22px;font-size:26px;padding:12px 18px">економія {money(tot_old(BASKET) - tot_new(BASKET))}</p>{lines}'
          f'<div class="tot"><span style="font-size:20px;color:#6B645C">Разом замість {money(tot_old(BASKET))}</span><span class="nw" style="font-size:34px;font-weight:500">{money(tot_new(BASKET))}</span></div></div>')
    return f'<div style="inset:0;background:{INK}"></div>' + rc + L("Кошик Чорної п’ятниці.", f"Хустка 44, твіллі 84 і резинка — {money(tot_new(BASKET))} замість {money(tot_old(BASKET))}.", f"Економія {money(tot_old(BASKET) - tot_new(BASKET))}", mob, width=780 if not mob else 640)
both("bfh-41-chek", v_receipt, "The receipt with three products and the saving")

def v_tiers(H, mob):
    """Three budget shelves side by side: a label, one card, the price."""
    groups = [("До 500 грн", "R-4"), ("До 1 500 грн", "84-7"), ("До 3 000 грн", "M-6")]
    cs = min(H - 190, 300 if not mob else 290); gap = 34; x0 = 1920 - 3 * cs - 2 * gap - 80; y = (H - cs - 100) // 2 + 36
    out = ""
    for i, (lb, a) in enumerate(groups):
        xx = x0 + i * (cs + gap)
        out += f'<p class="tl" style="left:{xx}px;top:{y - 34}px">{lb}</p>' + card(a, xx, y, cs, cs, bsize=28) + f'<p class="pr" style="left:{xx}px;top:{y + cs + 10}px;width:{cs}px;font-size:28px"><s>{money0(P[a]["full"])}</s>{money(new(a))}</p>'
    return f'<div style="inset:0;background:{INK}"></div>' + out + L("Подарунок за бюджетом.", "Три полиці — до 500, до 1 500 і до 3 000 грн; кожна річ уже зі знижкою.", f"Знижки до −{MAXP} %", mob, width=700 if not mob else 640)
both("bfh-42-biudzhet", v_tiers, "Three budget shelves")

def v_sizes(H, mob):
    """«Грація» in three sizes: three cards growing to the right, bottom-aligned."""
    arts = ["44-25-D", "65-25-D", "88-25-D"]; labels = [f"44{THIN}×{THIN}44 · −20{THIN}%", f"65{THIN}×{THIN}65 · −10{THIN}%", f"88{THIN}×{THIN}88 · −10{THIN}%"]
    big = min(H - 150, 470 if not mob else 460); ws = [int(big * .6), int(big * .8), big]; gap = -int(big * .18); pl = 60
    x = 1920 - sum(ws) - 2 * gap - 80; base = (H + big) // 2 - 16; out = ""; xx = x
    for i, (a, wi) in enumerate(zip(arts, ws)):
        out += card(a, xx, base - wi, wi, wi, bsize=24, z=3 + i); xx += wi + gap
    cw = (sum(ws) + 2 * gap) // 3
    out += "".join(f'<p class="pr" style="left:{x + i * cw}px;top:{base + 10}px;width:{cw}px;font-size:22px">{lb}<br><b>{money(new(a))}</b></p>' for i, (a, lb) in enumerate(zip(arts, labels)))
    return f'<div style="inset:0;background:{INK}"></div>' + out + L("«Грація» у трьох розмірах.", f"44{THIN}×{THIN}44 — {money(new('44-25-D'))}, 65{THIN}×{THIN}65 — {money(new('65-25-D'))}, 88{THIN}×{THIN}88 — {money(new('88-25-D'))}.", "«Грація» · від 1 920 грн", mob, width=780 if not mob else 640)
both("bfh-43-rozmiry", v_sizes, "One print in three sizes")

def v_pair(H, mob):
    cs = min(H - 110, 380 if not mob else 410); gap = 110 if not mob else 90; x0 = 1920 - 2 * cs - gap - 80; y = (H - cs - 50) // 2
    out = card("84-7", x0, y, cs, cs, bsize=30, price=True) + card("222-1", x0 + cs + gap, y, cs, cs, bsize=30, price=True) + f'<p class="plus" style="left:{x0 + cs}px;top:{y + cs // 2 - 50}px;width:{gap}px;font-size:110px">+</p>'
    tot = tot_new(["84-7", "222-1"]); was = tot_old(["84-7", "222-1"])
    return f'<div style="inset:0;background:{INK}"></div>' + out + L(f"Твіллі + кільце. {money(tot)}.", f"Разом замість {money(was)}: твіллі 84{NBSP}см і кільце Gold, обидва −30{THIN}%.", f"{money(tot)} замість {money(was)}", mob, width=720 if not mob else 700)
both("bfh-44-para", v_pair, "The pair: twilly and ring")

def v_allscr(H, mob):
    arts = ["R-16", "R-18", "R-4", "R-7", "R-11", "R-6", "R-1", "R-10"] if not mob else ["R-16", "R-18", "R-4", "R-7", "R-11", "R-6"]
    cols = 4 if not mob else 3; gap = 14; x0 = 1000 if not mob else 1060; rows_n = 2
    size = min((1920 - x0 - 28 - gap * (cols - 1)) // cols, (H - 56 - gap) // rows_n); y0 = (H - rows_n * size - gap) // 2
    out = "".join(card(a, x0 + (i % cols) * (size + gap), y0 + (i // cols) * (size + gap), size, size, bsize=22).split('<p class="bd"')[0] for i, a in enumerate(arts))
    d = 240 if not mob else 300
    out += f'<div class="bb" style="left:{1920 - d - 40}px;top:{H - d - 44}px;width:{d}px;height:{d}px"><b style="font-size:{int(d * .34)}px">−30 %</b><i style="font-size:{int(d * .075)}px">на всі {nR} принти</i></div>'
    return f'<div style="inset:0;background:{INK}"></div>' + out + L(f"Резинки. Усі −30{THIN}%.", f"{nR} принти по {money(new('R-4'))} замість {money(P['R-4']['full'])}.", f"{money(new('R-4'))} замість {money(P['R-4']['full'])}", mob)
both("bfh-45-vsi-rezynky", v_allscr, "All scrunchies, one round badge")

def v_lookbook(H, mob):
    """A lookbook frame with a twilly at the neck melting into the field, one twilly card over it."""
    cs = 320 if not mob else 360
    return f'<div style="inset:0;background:{INK}"></div>' + BH.feathered(LB + "lb07-08-L.webp", 980 if not mob else 960, 440, "50% 28%" if not mob else "35% 0%") + card("84-7", 1000 if not mob else 1040, H - cs - 50, cs, cs, rot=-4, z=5, bsize=30) + \
        L(f"Твіллі 84{NBSP}см. −30{THIN}%.", f"{n84} принтів по {money(new('84-7'))} замість {money(P['84-7']['full'])} — на шию, у волосся, на сумку.", f"{money(new('84-7'))} замість {money(P['84-7']['full'])}", mob, width=780 if not mob else 700)
both("bfh-46-lookbook", v_lookbook, "The lookbook twilly with one card")


# ── batch 5 (17.11): the client — «баннер на основе home-t1-seven-faces: фото товаров чёрной пятницы и снизу в кружочках скидки».
# The SOLO strip of seven portraits becomes seven tall slices of the draft's products (one per kind: 88, 44, twilly 84 and 140,
# sleep mask, scrunchie, ring), the print name in gold italic under each and the yellow discount circle sitting on the tile's foot.
EXTRA5 = """
.sv .nm { font-family: 'EB Garamond', serif; font-style: italic; font-weight: 500; color: #E7D9A6; line-height: 1.1; }
.sv .tp { font-family: 'Montserrat', sans-serif; font-weight: 400; color: #C9C6C0; line-height: 1.25; }
.sv .ci { display: flex; align-items: center; justify-content: center; border-radius: 50%; background: #F2B705; color: #141110; box-shadow: 0 16px 30px -12px rgba(0,0,0,.7); font-family: 'Onest', 'Montserrat', sans-serif; font-weight: 700; letter-spacing: -.03em; line-height: 1; white-space: nowrap; font-variant-numeric: tabular-nums; z-index: 6; }
"""
HEAD = HEAD.replace("</style>", EXTRA5 + "</style>").replace("EB+Garamond:wght@500;600", "EB+Garamond:ital,wght@0,500;0,600;1,500").replace("Onest:wght@400;600", "Onest:wght@400;600;700")
# 17.11, the client: «бери фото не просто товара, а где человек есть или где-то в жизни» — the galleries of the same products on
# obiimy.world (data/horoshop/products.json → gallery_common), copied to photo/bf-draft/life/<article>.jpg
# 17.11, the client again: «зроби менше товарів, щоб було краще видно їх» — five slices instead of seven, all with a person
# 17.11, the art director's pick («посимпатичніше, уважно з арт-директором»): one warm beige-caramel shoot, no sunglasses, faces calm,
# mid / close / mid / mid / close; captions are one word (the client: «не твіллі 95, а просто твіллі»)
SEVEN = [("88-22-D", "Хустка", "64% 20%", 1.0), ("44-21-D", "Паше", "44% 25%", 1.0), ("84-30", "Твіллі", "50% 25%", 1.0),
         ("65-23-D", "Хустка", "50% 15%", 1.0), ("R-23", "Резинка", "60% 20%", 1.0)]   # 65-23-D is the AD's alternate: the first pick (65-24-D) turned out to be a back view
PL = "../../photo/bf-draft/life/"
def seven_tiles(left, right, top, bottom, mob, gap=10, names=True, tiles=None, tight=False, d=None):
    tiles = tiles or [(a, a, tp, pos, z) for a, tp, pos, z in SEVEN]   # (file stem, article for the discount, caption, focus, zoom)
    n = len(tiles); w = (right - left - gap * (n - 1)) // n
    d = d or (72 if not mob else 104)                           # the discount circle on the foot of the tile (the reviewers: air around the digits, larger on mobile)
    sym = (lambda a: f'−{pct(a)}%') if tight else (lambda a: f'−{pct(a)}{THIN}%')   # tight (the client, 22.11): no space before %, the glyphs closer
    ls = "letter-spacing:-.07em;" if tight else ""
    cap_h = (int(26 * 1.3) + 12) if names else 0
    h = bottom - top - d // 2 - cap_h
    out = ""
    for i, t in enumerate(tiles):
        f, a, tp, pos, z = t[:5]
        if mob and len(t) > 5: pos = t[5]                      # the narrower mobile slice may need its own focus
        x = left + i * (w + gap)
        out += f'<div class="ph" style="left:{x}px;top:{top}px;width:{w}px;height:{h}px;background:#2A2522"><img src="{PL}{f}.jpg" alt="" style="object-position:{pos};transform:scale({z});transform-origin:{pos}"></div>'
        out += f'<p class="ci" style="left:{x + (w - d) // 2}px;top:{top + h - d // 2}px;width:{d}px;height:{d}px;font-size:{int(d * .34)}px;{ls}">{sym(a)}</p>'
        if names:
            out += f'<div class="sv" style="left:{x}px;width:{w}px;top:{top + h + d // 2 + 12}px;text-align:center"><p class="nm" style="font-size:26px;white-space:nowrap">{tp}</p></div>'
    return out
def v_seven(H, mob):
    # the copy (the client: «текст зліва осмислений»; the copywriter's option 1): a gift to yourself or to someone you love
    if mob: return f'<div style="inset:0;background:{INK}"></div>' + seven_tiles(960, 1892, 40, 728, True, gap=12, names=False) + \
        L("Подаруйте собі шовк", None, f"−10 · −20 · −30{THIN}%", True, width=720, bigsize=92)
    return f'<div style="inset:0;background:{INK}"></div>' + seven_tiles(790, 1856, 36, 540, False, gap=14) + \
        BH.lock("Подаруйте собі шовк — або тому, кого любите", f"{TOTAL} авторські шовкові вироби, створені в Україні, — зі знижками −10, −20 і −30{THIN}%.",
                kicker="Чорна п’ятниця в OBIIMY", pill=f"−10 · −20 · −30{THIN}%", more="Обрати подарунок", width=660, xl=False, bigsize=58)
both_cls("bfh-47-sim", v_seven, "Seven product slices with names and discount circles (after home-t1-seven-faces)", "sv")

# 17.11, the client: «давай несколько разных версий, и учти что осень-зима уже» — the same five-slice layout, but the frames are the
# autumn-winter shoots from the products' galleries (coats, trenches, the teal fur, the leather jacket, blazers); captions stay one word.
# After the reviews (AD 8.2 / 7.9 / 7.2, facts 7.5 / 7.5 / 6.5): a pashe caption only where a pashe is in the frame (the 44 galleries reuse the
# big-scarf shots, so the trench/camel frames are credited to the 88 articles), «і на зиму» instead of «і до зими» (read as a deadline),
# no «Чорна п’ятниця» twice, no sweater that isn't in the frames, non-breaking spaces inside the discount list, the camel frame not in every version.
# tile = (photo file in photo/bf-draft/life, article for the discount, caption, focus point, zoom)
SEASON = {
 # warm palette: camel coat, cream knit, beige trench, mustard trench, black suit — faces front / ¾ / profile / front / front, outdoor and studio alternate
 "bfh-48-coat": ([("88-24-03", "88-24", "Хустка", "50% 18%", 1.0), ("84-27-03", "84-27", "Твіллі", "22% 20%", 1.0, "30% 20%"), ("88-22-D-02", "88-22-D", "Хустка", "62% 18%", 1.0),
                  ("P-44-98-00", "P-44-98", "Паше", "50% 18%", 1.0), ("140-16-01", "140-16", "Твіллі", "50% 15%", 1.0)],
                 "Шовк до пальта{NBSP}— і на зиму", "Хустка, паше чи твіллі до пальта, тренча й жакета: {TOTAL}{NBSP}авторські шовкові вироби, створені в Україні,{NBSP}— зі{NBSP}знижками −10,{NBSP}−20{NBSP}і{NBSP}−30{THIN}%.",
                 "Шовк до пальта"),
 # colour against grey days: teal fur, black leather, black blazer with a red scarf, a knotted pashe close-up, beige trench with the leopard print
 "bfh-49-fur": ([("84-24-02", "84-24", "Твіллі", "40% 15%", 1.0), ("140-31-01", "140-31", "Твіллі", "72% 20%", 1.0), ("88-11-01", "88-11", "Хустка", "55% 18%", 1.0),
                 ("P-44-12-02", "P-44-12", "Паше", "50% 40%", 1.0), ("88-22-D-01", "88-22-D", "Хустка", "50% 100%", 1.18)],
                "Кольоровий шовк{NBSP}— проти сірих днів", "Яскравий акцент до хутра, шкіри й тренча: {TOTAL}{NBSP}авторські шовкові вироби, створені в Україні,{NBSP}— зі{NBSP}знижками −10,{NBSP}−20{NBSP}і{NBSP}−30{THIN}%.",
                "Кольоровий шовк"),
 # black + camel + one mint accent: black suit, camel coat, black blazer with the red scarf, teal fur (the profile frame hid the face in hair → the front one), black blazer with a pocket square
 "bfh-50-city": ([("140-16-01", "140-16", "Твіллі", "50% 15%", 1.0), ("88-24-01", "88-24", "Хустка", "50% 18%", 1.0), ("88-11-04", "88-11", "Хустка", "70% 20%", 1.0),
                  ("84-24-02", "84-24", "Твіллі", "40% 15%", 1.0), ("P-44-99-01", "P-44-99", "Паше", "50% 20%", 1.0)],
                 "Акцент холодного сезону{NBSP}— шовк", "До пальта, жакета й хутра: {TOTAL}{NBSP}авторські шовкові вироби, створені в Україні,{NBSP}— зі{NBSP}знижками −10,{NBSP}−20{NBSP}і{NBSP}−30{THIN}%.",
                 "Шовк холодного сезону"),
}
def v_season(key):
    tiles, big, small, mbig = SEASON[key]
    big = big.replace("{NBSP}", NBSP)
    small = small.replace("{TOTAL}", str(TOTAL)).replace("{THIN}", THIN).replace("{NBSP}", NBSP)
    def v(H, mob):
        if mob: return f'<div style="inset:0;background:{INK}"></div>' + seven_tiles(960, 1892, 40, 728, True, gap=12, names=False, tiles=tiles) + \
            L(mbig, None, f"−10 · −20 · −30{THIN}%", True, width=720, bigsize=92)
        return f'<div style="inset:0;background:{INK}"></div>' + seven_tiles(790, 1856, 36, 540, False, gap=14, tiles=tiles) + \
            BH.lock(big, small, kicker="Чорна п’ятниця в OBIIMY", pill=f"−10 · −20 · −30{THIN}%", more="Обрати подарунок", width=660, xl=False, bigsize=58)
    return v
for key in SEASON: both_cls(key, v_season(key), "Five autumn-winter slices with discount circles (after bfh-47)", "sv")

# 22.11, the client on bfh-50-city («вот этот доработаем»): the discount circles without the space before % and with the glyphs closer;
# other photos, fewer and smaller — four; less text on the left: the headline is «Чорна п’ятниця», the sub-line laconic.
# Frames not used in bfh-48…50: camel coat with the pink scarf (¾ face), black leather with the twilly, mustard trench with the blue
# pashe, teal fur front — camel / black / mustard / mint, outdoor and studio alternate; the pashe caption only where a pashe is in the frame.
# 22.11, the client again: no captions under the circles, and only frames without a white / light studio background — the outdoor
# shoots (camel coat, beige trench, teal fur in the field) and the dark close-up of the knotted pashe; the AD's round 1: calm faces, mobile focuses so no face is cut
# the AD, round 2 (8,5 / 8,2): the fur frame with air above the head (84-24), the pashe close-up below the earring, the first frame higher on mobile
# 22.11, the client: the second frame — the second gallery photo of /shovkova-khustka-flirt-65kh65-dvostoronnii-druk/ (coffee, Vogue, the «Флірт»
# scarf knotted on the trench); the pool already holds that shot at 1800 px as 88-33-D.jpg, and the 88 article carries the same −10 % the 65 page shows
FOUR = [("65-24-01", "65-24", "Хустка", "50% 18%", 1.0, "50% 30%"), ("88-33-D", "88-33-D", "Хустка", "54% 38%", 1.0, "56% 40%"),
        ("65-21-D-04", "65-21-D", "Хустка", "50% 22%", 1.0, "50% 25%"), ("84-24", "84-24", "Твіллі", "50% 18%", 1.0, "50% 12%")]
def v_four(H, mob):
    field = f'<div style="inset:0;background:{INK}"></div>'
    if mob: return field + seven_tiles(940, 1820, 44, 684, True, gap=14, names=False, tiles=FOUR, tight=True, d=124) + \
        BH.lock("Чорна п’ятниця", None, kicker="", pill=None, more="Дивитися всі", k=1.35, width=600, xl=True, bigsize=72)   # no kicker: it would repeat the headline; the client, 22.11: no yellow pill, the button on mobile too; k 1.35 — the AD: the circles 124 px, right margin ≈ 100 px
    return field + seven_tiles(1060, 1856, 78, 498, False, gap=14, names=False, tiles=FOUR, tight=True) + \
        BH.lock("Чорна п’ятниця", f"Неймовірні знижки в{NBSP}OBIIMY", kicker="", pill=None, more="Дивитися всі", width=760, xl=False, bigsize=92)   # the client's words, 22.11 («всі» after a vowel, euphony)
both_cls("bfh-51-four", v_four, "Four smaller autumn-winter slices, tight discount circles, the short lock-up (bfh-50 reworked)", "sv")

(HERE / "home-products.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "home frames incl. the fourth batch")
