"""Gift-set creatives (1080×1920 plain, plus story / feed / square via FORMAT): the ready-made sets of obiimy.world —
the yellow box, twilly + scarf, three twillies, the sleep set, «Співоча душа», the heart masks, zero-waste scrunchies,
a budget ladder and a «which set» grid. Photos are the shop's own set photographs (photo/site), cut-outs from img/cut;
prices and facts from review/SITE-FACTS.md (19.10.2026). Output: sets[-<format>].html → out-sets[-<format>]/*.jpg
(cd ads && ADS=solo/sets.html OUT=solo/out-sets node render.mjs)."""
import os, pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit import nb, LOGO_W, LOGO_K, GRAIN

def nbh(text):
    """Headlines: prepositions and dashes stick as in nb(), but the last word is left free — a three-word headline must still wrap."""
    import re
    text = re.sub(r"(?<![\w’'])(у|в|з|і|й|а|о|на|до|за|та|не|чи|із|зі|від|для|що|як|це)\s+(?=[^\s<])", lambda m: m.group(1) + "\u00a0", text, flags=re.I)
    return re.sub(r"\s+([—–])", lambda m: "\u00a0" + m.group(1), text)

FORMAT = os.environ.get("FORMAT", "plain")   # plain | story | feed | square
H = {"feed": 1350, "square": 1080}.get(FORMAT, 1920)
K = .72 if FORMAT == "square" else (.86 if FORMAT == "feed" else 1)     # type scale in the short frames
TOPL = 250 if FORMAT == "story" else 58       # the logo line
BOTB = 340 if FORMAT == "story" else 60       # the product row from the bottom
PH = "../../photo/site/"
CUT = "../../img/cut/"

CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #555; font-family: 'Onest', Arial, sans-serif; -webkit-font-smoothing: antialiased; }
.ad { width: 1080px; height: HPXpx; position: relative; overflow: hidden; background: #141110; margin: 20px auto; color: #F3EADB; }
.ad > * { position: absolute; margin: 0; }
.ad p { margin: 0; }
.ad::after { content: ""; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: .3; mix-blend-mode: soft-light; background-image: GRAIN; }
.ph { overflow: hidden; } .ph img { width: 100%; height: 100%; object-fit: cover; display: block; }
.big { font-family: 'Playfair Display', serif; font-weight: 900; font-style: italic; line-height: .95; letter-spacing: -.01em; text-wrap: balance; }
.small { font-family: 'EB Garamond', 'Cormorant Garamond', serif; font-weight: 500; line-height: 1.16; text-wrap: pretty; }
.kicker { font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: .14em; color: #E0B040; white-space: nowrap; }
.hdr { font-family: Montserrat, sans-serif; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; white-space: nowrap; }
.cta { font-family: 'Onest'; font-weight: 600; border-radius: 999px; background: #F2B705; color: #141216; white-space: nowrap; flex: none; }
.plate { display: flex; align-items: center; border-radius: 20px; flex: 0 1 auto; min-width: 0; }
.plate .nm { font-weight: 600; line-height: 1.1; text-wrap: balance; }
.plate .pr { font-family: 'Playfair Display', serif; font-weight: 700; line-height: 1; margin-top: 8px; }
.ink { color: #1B1613; } .ink .kicker { color: #8A6A12; }
""".replace("GRAIN", GRAIN).replace("HPX", str(H))

ads = []
def ad(id, body, note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad" id="{id}">{body}\n</section>')

def header(dark=True):
    col = "#F3EADB" if dark else "#1B1613"
    return (f'<img src="{LOGO_W if dark else LOGO_K}" alt="" style="left:64px;top:{TOPL}px;height:{int(58 * K)}px">'
            f'<p class="hdr" style="right:64px;top:{TOPL + int(18 * K)}px;font-size:{int(26 * K)}px;color:{col}">Авторські шовкові вироби</p>')

def plate(title, price, cut=None, dark=True, cta="Обрати набір"):
    """The product row at the bottom: a cut-out, the set's name, the retail price; the yellow button to the right."""
    th = int(120 * K)
    thumb = f'<img src="{CUT}{cut}.webp" alt="" style="height:{th}px;width:auto;max-width:{int(th * 1.3)}px;object-fit:contain;flex:none;filter:drop-shadow(0 8px 12px rgba(0,0,0,.4))">' if cut else ""
    bg, bd, fg = ("rgba(243,234,219,.1)", "1.5px solid rgba(243,234,219,.3)", "#F3EADB") if dark else ("rgba(27,22,19,.06)", "1.5px solid rgba(27,22,19,.18)", "#1B1613")
    return f'''
  <div style="left:64px;right:64px;bottom:{BOTB}px;display:flex;align-items:center;justify-content:space-between;gap:{int(24 * K)}px">
    <div class="plate" style="gap:{int(20 * K)}px;padding:{int(12 * K)}px {int(28 * K)}px {int(12 * K)}px {int(14 * K) if cut else int(28 * K)}px;background:{bg};border:{bd};color:{fg}">{thumb}
      <div style="min-width:0"><p class="nm" style="font-size:{int(27 * K)}px">{nb(title)}</p><p class="pr" style="font-size:{int(44 * K)}px">{price}</p></div></div>
    <div class="cta" style="font-size:{int(32 * K)}px;padding:{int(26 * K)}px {int(44 * K)}px">{cta}</div>
  </div>'''

def hero(id, photo, pos, kicker, big, small, product, note="", size=112, focus=None, dark_top=True):
    """One set photograph to the edges, the text over a dark veil above the product row."""
    row_h = int(170 * K)
    text_bottom = BOTB + row_h + int(40 * K)
    # the photo keeps its interesting part in the upper two thirds of the free frame in short formats
    style = f"object-position:{pos}"
    if focus is not None and FORMAT != "plain": style += f";object-position:{pos.split()[0]} {focus}"
    body = f'''
  <div class="ph" style="inset:0"><img src="{PH}{photo}.jpg" alt="" style="{style}"></div>
  <div style="inset:0;background:linear-gradient(180deg,rgba(12,9,8,{.72 if dark_top else .3}) 0%,rgba(12,9,8,0) {22 if FORMAT != 'square' else 30}%,rgba(12,9,8,0) 44%,rgba(12,9,8,.86) 72%,rgba(12,9,8,.96) 100%)"></div>
  {header()}
  <div style="left:64px;right:64px;bottom:{text_bottom}px">
    <p class="kicker" style="font-size:{int(26 * K)}px">{kicker}</p>
    <p class="big" style="font-size:{int(size * K)}px;margin-top:{int(18 * K)}px">{nbh(big)}</p>
    <p class="small" style="font-size:{int(40 * K)}px;margin-top:{int(24 * K)}px;max-width:900px">{nb(small)}</p>
  </div>
  {plate(*product)}'''
    ad(id, body, note)

def card(id, photo, pos, kicker, big, small, product, note="", size=104, ratio=1.0):
    """Paper page: the set photograph framed on top, the words below in ink, the product row dark."""
    top = TOPL + int(110 * K)
    row_h = int(170 * K); bottom_text = BOTB + row_h + int(40 * K)
    free = H - top - bottom_text
    ph_h = min(int((1080 - 128) * ratio), int(free * .56))
    body = f'''
  <div style="inset:0;background:#F1E8D8"></div>
  {header(dark=False)}
  <div class="ph" style="left:64px;right:64px;top:{top}px;height:{ph_h}px;border-radius:8px;box-shadow:0 30px 60px -30px rgba(40,25,10,.45)"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos}"></div>
  <div class="ink" style="left:64px;right:64px;top:{top + ph_h + int(44 * K)}px;bottom:{bottom_text}px;display:flex;flex-direction:column;justify-content:flex-start">
    <p class="kicker" style="font-size:{int(26 * K)}px">{kicker}</p>
    <p class="big" style="font-size:{int(size * K)}px;margin-top:{int(16 * K)}px">{nbh(big)}</p>
    <p class="small" style="font-size:{int(38 * K)}px;margin-top:{int(20 * K)}px;color:#4B423B">{nb(small)}</p>
  </div>
  <div style="left:0;right:0;bottom:0;height:{BOTB + row_h + int(24 * K)}px;background:#141110"></div>
  {plate(*product)}'''
    ad(id, body, note)

def grid(id, kicker, big, tiles, cta, note=""):
    """Four sets in a 2 × 2 grid: photograph, name, price — the catalogue of gifts on one screen."""
    top = TOPL + int(104 * K)
    head_h = int(190 * K)
    row_h = int(120 * K); bottom = BOTB + row_h + int(28 * K)
    gy = top + head_h; gh = H - gy - bottom; gap = int(18 * K)
    cell_w = (1080 - 128 - gap) // 2; cell_h = (gh - gap) // 2
    cap_h = int(96 * K)
    cells = ""
    for i, (photo, pos, name, price) in enumerate(tiles):
        x = 64 + (i % 2) * (cell_w + gap); y = gy + (i // 2) * (cell_h + gap)
        cells += f'''
  <div class="ph" style="left:{x}px;top:{y}px;width:{cell_w}px;height:{cell_h - cap_h}px;border-radius:6px"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos}"></div>
  <div style="left:{x}px;top:{y + cell_h - cap_h + int(12 * K)}px;width:{cell_w}px"><p style="font-size:{int(26 * K)}px;font-weight:600;line-height:1.15">{nb(name)}</p><p class="pr" style="font-family:'Playfair Display',serif;font-weight:700;font-size:{int(34 * K)}px;margin-top:{int(6 * K)}px;color:#F2B705">{price}</p></div>'''
    body = f'''
  {header()}
  <div style="left:64px;right:64px;top:{top}px"><p class="kicker" style="font-size:{int(26 * K)}px">{kicker}</p><p class="big" style="font-size:{int(92 * K)}px;margin-top:{int(14 * K)}px">{nbh(big)}</p></div>
  {cells}
  <div style="left:64px;right:64px;bottom:{BOTB}px;display:flex;align-items:center;justify-content:space-between;gap:24px">
    <p class="small" style="font-size:{int(34 * K)}px;color:#CFC4B2">{nb("Усі набори — у фірмовій коробці Obiimy.")}</p>
    <div class="cta" style="font-size:{int(32 * K)}px;padding:{int(26 * K)}px {int(44 * K)}px">{cta}</div></div>'''
    ad(id, body, note)

def ladder(id, kicker, big, bands, cta, note=""):
    """Three bands — three budgets: the photograph on the left, the shelf's price and its sets on the right."""
    top = TOPL + int(104 * K); head_h = int(262 * K)
    row_h = int(120 * K); bottom = BOTB + row_h + int(28 * K)
    y = top + head_h; gap = int(14 * K); bh = (H - y - bottom - 2 * gap) // 3
    out = ""
    for i, (photo, pos, shelf, lines) in enumerate(bands):
        by = y + i * (bh + gap)
        out += f'''
  <div class="ph" style="left:64px;top:{by}px;width:{int(430 * (K if K < 1 else 1))}px;height:{bh}px;border-radius:6px"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos}"></div>
  <div style="left:{64 + int(430 * (K if K < 1 else 1)) + int(34 * K)}px;right:64px;top:{by}px;height:{bh}px;display:flex;flex-direction:column;justify-content:center;border-bottom:1.5px solid rgba(243,234,219,.18)">
    <p class="kicker" style="font-size:{int(24 * K)}px">{shelf}</p>
    {"".join(f'<p style="font-size:{int(30 * K)}px;line-height:1.25;margin-top:{int(10 * K)}px;display:flex;justify-content:space-between;gap:16px"><span>{nb(n)}</span><b style="font-family:Playfair Display,serif;color:#F2B705;white-space:nowrap">{p}</b></p>' for n, p in lines)}
  </div>'''
    body = f'''
  {header()}
  <div style="left:64px;right:64px;top:{top}px"><p class="kicker" style="font-size:{int(26 * K)}px">{kicker}</p><p class="big" style="font-size:{int(92 * K)}px;margin-top:{int(14 * K)}px">{nbh(big)}</p></div>
  {out}
  <div style="left:64px;right:64px;bottom:{BOTB}px;display:flex;align-items:center;justify-content:space-between;gap:24px">
    <p class="small" style="font-size:{int(34 * K)}px;color:#CFC4B2">{nb("Роздрібні ціни obiimy.world.")}</p>
    <div class="cta" style="font-size:{int(32 * K)}px;padding:{int(26 * K)}px {int(44 * K)}px">{cta}</div></div>'''
    ad(id, body, note)

# ─── the twelve ────────────────────────────────────────────────────────────────────────────────────────────────────────────
hero("s01-box-natkhnennia", "set-tvilli-845-ta-khustky-4444-natkhne-01", "50% 42%", "Подарункові набори",
     "Подарунок, який уже запакований.", "Хустка 44 × 44 і твіллі одного принту — у фірмовій жовтій коробці.",
     ("Набір «Натхнення» · твіллі + хустка", "3 100 грн", "set-natkhnennia-box"), "the yellow box, the hero set", focus="38%")

hero("s02-three-twilly", "set-3-shovkovykh-tvilli-12", "50% 38%", "Подарункові набори",
     "Три твіллі — три настрої.", "Принти можна обрати різні: у волосся, на сумку, на шию.",
     ("Набір із трьох твіллі 84 × 5", "4 650 грн", "three-twilly-2"), "three twillies spilling from the box", focus="30%")

hero("s03-sleep", "maska-dlia-snu-ta-rezynka-svoboda-03", "50% 50%", "Подарункові набори",
     "Подарунок про відпочинок.", "Шовкова маска для сну й резинка в одному принті — набір для сну «Свобода».",
     ("Набір для сну · маска + резинка", "3 280 грн", "box-maskscr-litnie-pole"), "sunlit sleep set", focus="42%")

card("s04-twscr", "set-litnie-pole-01", "50% 50%", "Подарункові набори",
     "Два подарунки в одній коробці.", "Твіллі 84 × 5 і шовкова резинка — найпростіший подарунок, який носять.",
     ("Твіллі + резинка", "2 200 грн", "twscr-makiv"), "twilly and scrunchie, paper card")

hero("s05-no-size", "tvilli-ta-rezynka-prystrast-02", "50% 18%", "Подарункові набори",
     "Коли не знаєте розмір.", "Твіллі, резинка, маска для сну — подарунки без розміру. Один принт на дві речі.",
     ("Набори у коробці — від", "2 200 грн", "box-twscr-smilyvist", True, "Обрати подарунок"), "the twilly as a tie — no size needed", focus="16%")

card("s06-song", "set-maska-zakladka-rezynka-melodiia-01", "50% 50%", "Колекція «Співоча душа»",
     "Подарунок із сенсом.", "Маска для сну, закладка для книги й резинка в одному принті. Частина коштів із колекції — на порятунок сиворакші.",
     ("«Мелодія двох» · маска, закладка, резинка", "4 080 грн", "box-maskbm-melodiia"), "the Singing Soul accessory set", size=90)

hero("s07-hearts", "set-masok-dlia-snu-sertsebyttia-chervo-02", "50% 50%", "Подарункові набори",
     "Для двох.", "Пара шовкових масок для сну «Серцебиття» — червона та чорна.",
     ("Набір масок «Серцебиття»", "4 200 грн", None), "two heart masks", size=132, focus="44%")

ladder("s08-budget", "Подарунок за бюджетом", "Три полиці — три подарунки.", [
    ("set-litnie-pole-01", "50% 50%", "До 2 500 грн", [("Твіллі + резинка", "2 200"), ("Три резинки", "1 800")]),
    ("set-maska-rezynka-10-01", "50% 50%", "До 3 500 грн", [("Твіллі + хустка 44 × 44", "3 100"), ("Набір для сну", "3 280")]),
    ("set-3-shovkovykh-tvilli-10", "50% 40%", "До 5 000 грн", [("«Співоча душа»: маска, закладка, резинка", "4 080"), ("Три твіллі", "4 650")]),
], "Обрати набір", "the budget ladder")

grid("s09-which", "Подарункові набори", "Який набір обрати?", [
    ("set-litnie-pole-01", "50% 50%", "Твіллі + резинка", "2 200 грн"),
    ("set-maska-rezynka-10-01", "50% 50%", "Набір для сну", "3 280 грн"),
    ("set-tvilli-845-ta-khustky-4444-natkhne-01", "50% 45%", "Твіллі + хустка 44 × 44", "3 100 грн"),
    ("set-maska-zakladka-rezynka-melodiia-01", "50% 50%", "Маска, закладка й резинка", "4 080 грн"),
], "Усі набори", "four sets on one screen")

hero("s10-solo-2d", "set-tvilli-ta-khustky-zolote-svilo-01", "50% 50%", "Колекція SOLO",
     "Набір із двостороннім друком.", "Хустка 44 × 44 «Золоте світло» — два принти на одній хустці — і твіллі в тон.",
     ("Твіллі + хустка 2D «Золоте світло»", "4 080 грн", None), "the SOLO double-sided set", size=80, focus="44%")

card("s11-zero-waste", "set-iz-5-ty-shovkovykh-rezynok-zero-west-03", "50% 40%", "Подарункові набори",
     "Маленький знак уваги.", "П'ять шовкових резинок zero waste — подарунок, який точно підійде.",
     ("Набір резинок zero waste, 5 шт.", "2 420 грн", None), "five zero-waste scrunchies", ratio=.78)

hero("s12-one-print", "set-tvilli-845-ta-khustky-4444-natkhne-03", "50% 16%", "Подарункові набори",
     "Хустка й твіллі одного принту.", "Разом у коробці — або кожна річ окремо: на шию, у волосся, на сумку.",
     ("Набір «Натхнення» · твіллі + хустка", "3 100 грн", "set-natkhnennia-box"), "the twilly in the braid, the box below", focus="12%")

# ─── ten more (26.10) ──────────────────────────────────────────────────────────────────────────────────────────────────
hero("s13-ponytail", "set-smilyvist-02", "50% 22%", "Подарункові набори",
     "Твіллі у волоссі — і резинка в тон.", "Набір «Сміливість»: стрічка на хвіст чи косу, резинка — на щодень.",
     ("Твіллі + резинка «Сміливість»", "2 200 грн", "box-twscr-smilyvist"), "the twilly in the ponytail", focus="18%")

hero("s14-wrist", "set-makovyi-tsvit-02", "50% 40%", "Подарункові набори",
     "На зап’ясті — як браслет.", "Твіллі «Маків цвіт» і резинка в одному принті — два подарунки в коробці.",
     ("Твіллі + резинка «Маків цвіт»", "2 200 грн", "twscr-makiv"), "the twilly tied on the wrist, a tulip in hand", focus="36%")

hero("s15-packaging", "../box-gold", "50% 50%", "Пакування",
     "Подарунок починається з коробки.", "Кожен виріб Obiimy — в індивідуальному пакуванні: хустки, твіллі, маски для сну.",
     ("Хустки й твіллі — від", "1 600 грн", None, True, "Обрати подарунок"), "the signature box", size=92, focus="50%")

hero("s16-sleep-sun", "set-ta-rezynka-litnie-pole-04", "50% 50%", "Подарункові набори",
     "Сон у шовку.", "Маска для сну й резинка «Літнє поле» — набір для тієї, хто любить висипатися.",
     ("Набір для сну «Літнє поле»", "3 280 грн", "box-maskscr-litnie-pole"), "the sunlit sleep set", size=132, focus="46%")

card("s17-grey", "tvilli-ta-rezynka-zakhoplennia-02", "50% 50%", "Подарункові набори",
     "Для тієї, хто любить стримане.", "Сіра твіллі «Захоплення» й резинка в тон — у фірмовій коробці.",
     ("Твіллі + резинка «Захоплення»", "2 200 грн", "box-twscr-smilyvist"), "the grey set, paper card", size=92)

card("s18-bouquet", "set-prystrast-01", "50% 30%", "Подарункові набори",
     "Замість букета.", "Шовкова твіллі й резинка «Пристрасть» — подарунок, який не зів’яне.",
     ("Твіллі + резинка «Пристрасть»", "2 200 грн", "twscr-makiv"), "a flower in hand, the twilly on the wrist", ratio=.9)

hero("s19-three-looks", "set-3-shovkovykh-tvilli-11", "50% 45%", "Подарункові набори",
     "Один подарунок — три образи.", "Три твіллі 84 × 5 у святковому пакуванні: принти можна обрати різні.",
     ("Набір із трьох твіллі", "4 650 грн", "three-twilly-2"), "three twillies, another frame", focus="40%")

hero("s20-her-print", "set-tvilli-845-ta-khustky-4444-vpevnen-02", "50% 14%", "Подарункові набори",
     "Її принт — на двох речах.", "Хустка 44 × 44 і твіллі «Впевненість» в одному принті — разом або окремо.",
     ("Набір «Впевненість» · твіллі + хустка", "3 100 грн", "set-vpevnenist-box"), "the scarf on the back, the twilly in the braid", focus="10%")

grid("s21-how-worn", "Подарункові набори", "Як носять подарунок.", [
    ("set-tvilli-845-ta-khustky-4444-natkhne-03", "50% 10%", "Твіллі у косі · набір «Натхнення»", "3 100 грн"),
    ("set-tvilli-845-ta-khustky-4444-natkhne-02", "50% 12%", "Хустка на спині · набір «Натхнення»", "3 100 грн"),
    ("tvilli-ta-rezynka-prystrast-02", "50% 14%", "Твіллі краваткою · набір «Пристрасть»", "2 200 грн"),
    ("set-smilyvist-02", "50% 18%", "Твіллі у хвості · набір «Сміливість»", "2 200 грн"),
], "Обрати набір", "four ways to wear the sets")

hero("s22-today", "set-maska-rezynka-34-01", "50% 50%", "Подарункові набори",
     "Замовили до 16:00 — відправимо сьогодні.", "Набір для сну «Серцебиття»: маска й резинка в коробці, готові до вручення.",
     ("Набір для сну · маска + резинка", "3 280 грн", "box-maskscr-litnie-pole"), "same-day dispatch, the red sleep set", size=92, focus="46%")

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · gift sets</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=EB+Garamond:wght@500;600&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Oswald:wght@500&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("sets" + ("" if FORMAT == "plain" else "-" + FORMAT) + ".html")).write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "gift-set banners", FORMAT)
