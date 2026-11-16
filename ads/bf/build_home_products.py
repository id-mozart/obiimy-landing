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

def L(big, small, pill, mob, num=None, width=None, xl=True, bigsize=None):
    """Desktop: the full lock-up. Mobile (the frame is shown at a third of its size on a phone): the headline larger, the paragraph
    and the second button dropped — the yellow price pill is the only call (the art director, 16.11)."""
    if mob: return BH.lock(big, None, kicker=KICK, num=num, pill=pill, more=None, k=1.15, width=width or 760, xl=True, bigsize=bigsize or 100)
    return BH.lock(big, small, kicker=KICK, num=num, pill=pill, k=1, width=width or 860, xl=xl, bigsize=bigsize)

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
