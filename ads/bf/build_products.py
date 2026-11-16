"""Black Friday, the product series (16.11.2026, the client: «сделай серию креативов именно с этими товарами» — the goods he put
into the «Чорна п’ятниця» draft on /discounts). The draft decides the discount of every article (−10 / −20 / −30 %), so here, unlike
the earlier BF series, the number is pinned to the product: a yellow badge on every card and the price line «1 120 замість 1 600 грн»
(the retail price of obiimy.world, the new one computed from the draft). Photos: the products' own pictures from obiimy.world
(photo/bf-draft/<article>.jpg, copied as they are). Data: ads/bf/draft-products.json (written from GET /api/discounts/drafts +
/api/discounts). If the draft changes, re-export the json and re-render.
  python3 bf/build_products.py                → bf/bfp.html   (FORMAT=story|feed|square → bfp-<format>.html)
  cd ads && ADS=bf/bfp.html OUT=bf/out-products node render.mjs   (and FORMAT=… OUT=bf/out-products-<format>)"""
import json, pathlib, re
from common import *
HERE = pathlib.Path(__file__).parent
P = {p["article"]: p for p in json.load(open(HERE / "draft-products.json", encoding="utf-8"))}
PD = "../../photo/bf-draft/"
NBSP, THIN = " ", " "

def money(v): return f"{int(round(v)):,}".replace(",", NBSP) + NBSP + "грн"
def pct(a): return int(P[a]["value"] or 0)
def new(a): return P[a]["full"] * (1 - pct(a) / 100)
def line(a): return f"{money(new(a))} замість {money(P[a]['full'])}"
def count(prefix=None, cat=None, value=None):
    return sum(1 for p in P.values() if (prefix is None or p["article"].startswith(prefix)) and (cat is None or p["category"] == cat) and (value is None or p["value"] == value))
def words_n(n):
    return {2: "два", 3: "три", 4: "чотири", 5: "п’ять", 6: "шість", 7: "сім", 8: "вісім", 9: "дев’ять", 10: "десять", 11: "одинадцять", 12: "дванадцять", 13: "тринадцять"}.get(n, str(n))

TOTAL = sum(1 for p in P.values() if p["value"]); MAXP = max(pct(a) for a in P)   # the articles that actually carry a discount (11 of the 133 on the page have none)
CATS = f"{TOTAL} товари · до −{MAXP} %"
EXTRA = """
.pc { background: #fff; box-shadow: 0 30px 60px -24px rgba(0,0,0,.7), 0 4px 12px rgba(0,0,0,.25); overflow: hidden; }
.pc img { width: 100%; height: 100%; object-fit: cover; display: block; }
.pc.fit img { object-fit: contain; }
.bd { position: absolute; display: inline-block; background: #F2B705; color: #141110; box-shadow: 0 0 0 3px #141110; font-family: 'Montserrat', sans-serif; font-weight: 500; border-radius: 999px; line-height: 1; letter-spacing: -.01em; white-space: nowrap; font-variant-numeric: tabular-nums; z-index: 5; }
.pr { font-family: 'Montserrat', sans-serif; font-weight: 400; color: #F3EADB; white-space: nowrap; font-variant-numeric: tabular-nums; line-height: 1.1; }
.pr s { color: #A89E94; text-decoration-thickness: 1.5px; margin-right: .35em; font-weight: 300; }
.pr b { font-weight: 500; color: #fff; }
.nm { font-family: 'EB Garamond', serif; font-weight: 500; color: #D9CDB9; line-height: 1.15; }
"""

def card(a, x, y, w, h, rot=0, badge=True, pos="50% 50%", zoom=1.0, fit=False, bsize=30, z=3, price=False, name=False):
    """A white product card with the yellow discount badge in its top-left corner; optional price line and name under it."""
    r = f"transform:rotate({rot}deg);" if rot else ""
    zoom = zoom if zoom != 1.0 else ZOOM.get(a, 1.0); pos = POS.get(a, pos) if pos == "50% 50%" else pos; flt = f"filter:{FILTER[a]};" if a in FILTER else ""
    out = f'<div class="pc{" fit" if fit else ""}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{r}z-index:{z}"><img src="{PD}{a}.jpg" alt="" style="object-position:{pos};transform:scale({zoom});{flt}"></div>'
    if badge: out += f'<p class="bd" style="left:{x + int(18 * K)}px;top:{y + int(18 * K)}px;font-size:{int(bsize * K)}px;padding:{int(bsize * .42 * K)}px {int(bsize * .62 * K)}px;{r}transform-origin:{-18 * K}px {-18 * K}px;z-index:{z + 1}">−{pct(a)}{THIN}%</p>'
    if price: out += f'<p class="pr" style="left:{x}px;top:{y + h + int(14 * K)}px;width:{w}px;text-align:center;font-size:{int(42 * K)}px"><s>{money(P[a]["full"])}</s><b>{money(new(a))}</b></p>'
    if name: out += f'<p class="nm" style="left:{x}px;top:{y + h + int(16 * K) + (int(34 * K) if price else 0)}px;width:{w}px;text-align:center;font-size:{int(22 * K)}px">{nb(short(a))}</p>'
    return out

ZOOM = {"222-1": 2.1, "333-1": 2.1, "444-1": 2.0, "555-1": 2.1, "111-2": 2.1, "Book-027": 1.5}   # the site shot small things with a wide white margin
POS = {}
for _a in P:
    if _a.startswith("R-"): ZOOM.setdefault(_a, 1.5); POS.setdefault(_a, "50% 85%")   # the scrunchie large, the top of the yellow box with the logo leaving the frame
FILTER = {"140-1": "brightness(1.12) contrast(1.05)"}   # a grey studio background that should read white on the card

def short(a):
    """«Хустка твіллі шовкова «Спокуса» 84x5» → «Спокуса»; a ring → «Безкінечність»."""
    m = re.search(r"[«\"]([^»\"]+)[»\"]", P[a]["name"]); return m.group(1) if m else P[a]["name"]

import math
def wh_est(big, small, size=76):
    """How tall the words block will be: lines × line height (Montserrat ≈ .55 em a character, Garamond ≈ .43 em)."""
    cpl_b = max(8, int(952 / (0.55 * size * K))); cpl_s = max(20, int(952 / (0.43 * 36 * K)))
    h = math.ceil(len(re.sub(r"<[^>]+>", "", big)) / cpl_b) * size * K * 1.06
    if small: h += 22 * K + math.ceil(len(re.sub(r"<[^>]+>", "", small)) / cpl_s) * 36 * K * 1.22
    return int(h)

def frame(id, block, bh, big, small, note, label=None, dark=True, size=76):
    """`block(top)` draws the product block of height `bh` from `top`; the words sit right under it, the pair floats a little above
    the centre of the free space between the logo line and the bottom row."""
    hd = hdr_text(big); cls = "light" if dark else "ink"
    wh = wh_est(big, small, size); gap = int(40 * K)
    free = (Y1 - Y0) - (bh + gap + wh)
    top = Y0 + max(int(10 * K), int(free * 0.42))
    body = f'''
  <div style="inset:0;background:{INK if dark else WHITE}"></div>
  {block(top)}
  {header(dark, hd)}
  <div class="{cls}" style="left:64px;right:64px;top:{top + bh + gap}px;z-index:4">{words(big, small, size, dark)}</div>
  {bar(dark, label or CATS)}'''
    ad(id, body, note)

# ─── templates ─────────────────────────────────────────────────────────────────────────────────────────────────────────────

def trio(id, arts, big, small, note, label=None):
    """Three cards fanned, the words under them."""
    if SQ:
        cs = 400; cy = Y0 - 10; xs = [30, 340, 650]; rots = [-6, 2, 7]; dys = [34, 0, 30]
        inner = "".join(card(a, x, cy + dy, cs, cs, r, z=3 + i) for i, (a, x, r, dy) in enumerate(zip(arts, xs, rots, dys)))
        words_h = f'<div class="light" style="left:64px;right:64px;bottom:{H - Y1}px;z-index:4">{words(big, small, 54)}</div>'
        ad(id, f'<div style="inset:0;background:{INK}"></div>{inner}{header(True, hdr_text(big))}{words_h}{bar(True, label or CATS)}', note); return
    cs = int(600 * K); xs = [int(v * K) for v in (24, 240, 456)]; rots = [-7, 2, 8]; dys = [int(v * K) for v in (46, 0, 40)]
    bh = cs + int(100 * K)
    block = lambda top: "".join(card(a, x, top + dy, cs, cs, r, z=3 + i) for i, (a, x, r, dy) in enumerate(zip(arts, xs, rots, dys)))
    frame(id, block, bh, big, small, note, label)

def grid(id, arts, big, small, note, label=None, price=True, cols=None, zoom=1.0, fit=False):
    """A grid of square cards with badges; the number of columns is whichever gives the largest cards that still fit."""
    n = len(arts); gap = int(22 * K); pl = int(40 * K) if price else 0
    wh = wh_est(big, small); avail = (Y1 - Y0) - int(40 * K) - wh - int(20 * K)
    best = None
    for c in ([cols] if cols else (1, 2, 3)):
        r = (n + c - 1) // c; cw = (1080 - 128 - gap * (c - 1)) // c
        ch = min(cw, (avail - (r - 1) * gap - r * pl) // r)
        if ch <= 0: continue
        if best is None or ch > best[2]: best = (c, r, ch, cw)
    c, r, ch, cw = best
    bh = r * ch + (r - 1) * gap + r * pl
    def block(top):
        out = ""
        for i, a in enumerate(arts):
            rr, cc = divmod(i, c); x = 64 + cc * (cw + gap); y = top + rr * (ch + gap + pl)
            out += card(a, x, y, cw, ch, badge=True, bsize=26 if c >= 3 else 32, price=price, fit=fit, zoom=zoom)
        return out
    if SQ:
        # the square: the grid at the left two thirds, the words at the right
        pw = 640; gap2 = 14; avail2 = H - Y0 - BOTB - BAR - 50
        best2 = None
        for c2 in (1, 2, 3):
            r2 = (n + c2 - 1) // c2; cw2 = (pw - 48 - gap2 * (c2 - 1)) // c2; ch2 = min(cw2, (avail2 - gap2 * (r2 - 1)) // r2)
            if best2 is None or ch2 > best2[2]: best2 = (c2, r2, ch2, cw2)
        c2, r2, ch2, cw2 = best2; y02 = Y0 + (avail2 - r2 * ch2 - (r2 - 1) * gap2) // 2
        inner = "".join(card(a, 48 + (i % c2) * (cw2 + gap2), y02 + (i // c2) * (ch2 + gap2), cw2, ch2, badge=True, bsize=30, zoom=zoom, fit=fit) for i, a in enumerate(arts))
        ad(id, f'<div style="inset:0;background:{INK}"></div>{inner}{header(True, hdr_text(big))}<div class="light" style="left:{pw + 24}px;right:64px;top:{Y0 + 10}px;z-index:4">{words(big, small, 50)}</div>{bar(True, label or CATS)}', note); return
    frame(id, block, bh, big, small, note, label)

def hero(id, a, big, small, note, label=None, pos="50% 50%", zoom=1.0, fit=False):
    """One product large on a white card, the price under it, the words below."""
    if SQ:
        pw = 520; chh = H - Y0 - BOTB - BAR - 40
        inner = card(a, 48, Y0, pw - 48, chh, badge=True, bsize=36, pos=pos, zoom=zoom, fit=fit) + f'<p class="pr" style="left:{pw + 40}px;right:64px;top:{Y0 + 10}px;font-size:30px"><s>{money(P[a]["full"])}</s><b>{money(new(a))}</b></p>'
        body = f'<div style="inset:0;background:{INK}"></div>{inner}{header(True, hdr_text(big))}<div class="light" style="left:{pw + 40}px;right:64px;top:{Y0 + 76}px;z-index:4">{words(big, small, 50)}</div>{bar(True, label or CATS)}'
        ad(id, body, note); return
    cw = 1080 - 128; wh = wh_est(big, small)
    ch = min(int(cw * 1.0), (Y1 - Y0) - int(40 * K) - wh - int(70 * K))
    bh = ch + int(56 * K)
    block = lambda top: card(a, 64, top, cw, ch, badge=True, bsize=40, pos=pos, zoom=zoom, fit=fit, price=True)
    frame(id, block, bh, big, small, note, label)

def wall(id, arts, big, small, note, label=None):
    """A 3 × 3 wall of products with badges — the whole selection at a glance."""
    c = 3; gap = int(16 * K); cw = (1080 - 128 - gap * 2) // c; r = (len(arts) + c - 1) // c
    wh = wh_est(big, small); ch = min(cw, ((Y1 - Y0) - int(40 * K) - wh - int(20 * K) - (r - 1) * gap) // r)
    bh = r * ch + (r - 1) * gap
    block = lambda top: "".join(card(a, 64 + (i % c) * (cw + gap), top + (i // c) * (ch + gap), cw, ch, badge=True, bsize=24) for i, a in enumerate(arts))
    if SQ:
        pw = 640; cw2 = (pw - 48 - 20) // 3; ch2 = min(cw2, (H - Y0 - BOTB - BAR - 50 - 20) // 3); y02 = Y0 + ((H - Y0 - BOTB - BAR - 50) - 3 * ch2 - 20) // 2
        inner = "".join(card(a, 48 + (i % 3) * (cw2 + 10), y02 + (i // 3) * (ch2 + 10), cw2, ch2, badge=True, bsize=28) for i, a in enumerate(arts))
        ad(id, f'<div style="inset:0;background:{INK}"></div>{inner}{header(True, hdr_text(big))}<div class="light" style="left:{pw + 24}px;right:64px;top:{Y0 + 10}px;z-index:4">{words(big, small, 50)}</div>{bar(True, label or CATS)}', note); return
    frame(id, block, bh, big, small, note, label)

# ─── the set ──────────────────────────────────────────────────────────────────────────────────────────────────────────────

n44 = len({re.search(r"[«\"]([^»\"]+)[»\"]", p["name"]).group(1) if re.search(r"[«\"]([^»\"]+)[»\"]", p["name"]) else p["name"] for p in P.values() if "44-" in p["article"] and p["article"].endswith("-D") and p["value"] == 20})   # distinct prints: 44-xx-D and P-44-xx-D are the same scarf listed twice
n84 = count("84-", value=30); nR = sum(1 for p in P.values() if p["article"].startswith("R-") and p["article"] != "R-as" and p["value"] == 30)   # R-as is «в асортименті», not a print
nM = count(cat="Маски для сну", value=20); nRing = count(cat="Прикраси", value=30); n140_20 = count("140-", value=20); nSets = count(cat="Подарунки"); nM = count(cat="Маски для сну", value=20); nRing = count(cat="Прикраси", value=30)
n140_20 = count("140-", value=20); nSets = count(cat="Подарунки")

trio("bfp-01-khustky44", ["44-21-D", "44-22-D", "44-25-D"], f"Двосторонні хустки 44{NBSP}см. −20{THIN}%.",
     f"«Натхнення», «Сміливий дотик», «Грація» та ще {words_n(n44 - 3)} принтів 44{THIN}×{THIN}44 — {line('44-21-D')}.",
     "Three 44 cm scarves as fanned cards, −20 %", label=f"Хустки 44 см · {money(new('44-21-D'))}")

grid("bfp-02-rezynky", ["R-16", "R-18", "R-4", "R-7", "R-11", "R-6"], f"Резинки. −30{THIN}%.",
     f"Шовкова резинка — {line('R-16')}; у добірці {nR} принти.", "Six scrunchies on their yellow boxes, −30 %", label=f"Резинки · {money(new('R-16'))}", price=False)

grid("bfp-03-tvilli84", ["84-7", "84-27", "84-24", "84-30", "84-19", "84-2"], f"Твіллі 84 см. −30{THIN}%.",
     f"{line('84-7')} — {words_n(n84)} принтів: «Спокуса», «Мелодія двох», «Відновлення», «Коло сонця», «Ранкова кава», «Літнє поле»…",
     "Six twillies 84 × 5, −30 %", label=f"Твіллі 84 см · {money(new('84-7'))}", price=False)

grid("bfp-04-kiltsia", ["222-1", "333-1", "444-1", "555-1"], f"Кільця для хустки. −30{THIN}%.",
     f"«Безкінечність», «Х стиль», «Циліндр», «Н стиль» кольору Gold — {line('222-1')}.", "Four scarf rings, −30 %", label=f"Кільця · {money(new('222-1'))}", price=False, zoom=2.2)

hero("bfp-05-maska", "M-6", f"Маска для сну «Енергія». −20{THIN}%.", f"Маска з натурального шовку з принтом «Енергія». Усі маски в добірці — −20{THIN}%.",
     "The lavender sleep mask, −20 %", label=f"Маски для сну · {money(new('M-6'))}", pos="50% 50%", zoom=1.0)

hero("bfp-06-nabir-snu", "NM-6", f"Набір для сну «Енергія». −20{THIN}%.", f"Маска й резинка в жовтій коробці — подарунок, який не треба пакувати.",
     "The sleep set in the yellow box, −20 %", label=f"Подарункові набори · −20 %", pos="50% 50%")

hero("bfp-07-tvilli140", "140-1", f"Твіллі 140 см «Літній віночок». −30{THIN}%.", f"Довга твіллі — на шию, у волосся, на сумку.",
     "The long twilly, −30 %", label=f"«Літній віночок» · {money(new('140-1'))}", pos="50% 50%", zoom=1.0)

hero("bfp-08-try-rezynky", "NR-300", f"Три резинки в коробці. −30{THIN}%.", f"Три шовкові резинки в коробці — готовий подарунок.",
     "The three-scrunchie set, −30 %", label=f"Набір резинок · {money(new('NR-300'))}", pos="50% 50%")

hero("bfp-09-zakladka", "Book-027", f"Закладка «Мелодія двох». −30{THIN}%.", f"Шовкова закладка з китицею — маленький подарунок до книжки.",
     "The silk bookmark, −30 %", label=f"Закладка · {money(new('Book-027'))}", pos="50% 50%", fit=True)

hero("bfp-10-sertsebyttia", "M-96", f"Маска «Серцебиття». −20{THIN}%.", f"Червоні серця з шовку; є й чорна в чохлі.",
     "The red hearts mask, −20 %", label=f"Маски для сну · {money(new('M-96'))}", pos="50% 50%", fit=True)

grid("bfp-11-velyki", ["65-25-D", "88-33-D"], f"Великі хустки. −10{THIN}%.",
     f"«Грація» 65{THIN}×{THIN}65 — {line('65-25-D')}; «Флірт» 88{THIN}×{THIN}88 — {line('88-33-D')}.", "Two large scarves, −10 %", label="«Грація» і «Флірт» · −10 %", price=True)

hero("bfp-12-boksy", "NT-84-2", f"Бокс твіллі + резинка. −20{THIN}%.",
     f"Твіллі й резинка «Літнє поле» в коробці — подарунок, готовий до вручення; є також «Сміливість».", "The gift box, −20 %", label="Подарункові бокси · −20 %")

wall("bfp-13-dobirka", ["44-22-D", "84-7", "R-7", "M-6", "222-1", "NM-6", "140-1", "88-33-D", "84-27"], f"{TOTAL} товари зі знижкою.",
     f"Хустки, твіллі, маски, резинки, кільця й набори — вся добірка Чорної п’ятниці на obiimy.world, від −10 до −{MAXP}{THIN}%.",
     "The wall: nine products of the selection with their badges")

hero("bfp-14-kiltse", "444-1", f"Кільце «Циліндр». −30{THIN}%.", f"Кільце Gold — до хустки чи твіллі зі знижкою, в один кошик.",
     "One gold ring, −30 %", label=f"Кільця · {money(new('444-1'))}", pos="50% 50%", zoom=1.9)

HEAD = f"""<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · Black Friday · the draft's products</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;600&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>{CSS}{EXTRA}</style></head><body>"""
name = "bfp" + ("" if FORMAT == "plain" else f"-{FORMAT}") + ".html"
(HERE / name).write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "product banners →", name, "| counts: 44 см −20 %:", n44, "твіллі 84 −30 %:", n84, "резинки −30 %:", nR, "маски −20 %:", nM, "кільця −30 %:", nRing, "твіллі 140 −20 %:", n140_20, "подарунки:", nSets)
