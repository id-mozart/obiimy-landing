#!/usr/bin/env python3
"""The HR deck with variant pages inside it, for the client to choose (04.10: «все добавляй в пдф, потом уберём лишнее»):
cover variants right after the cover and variants of page 3 («Що в коробці — і скільки це коштує») right after page 3.
Reuses the deck's helpers, data and CSS (src/build-team-pdf.py renders only when run as a script) and renders the public PDF itself.
When the choice is made: move the chosen layouts into build-team-pdf.py and build the deck with it again."""
import importlib.util, pathlib, subprocess, sys
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent; OUT = ROOT.parent
sys.path.insert(0, str(ROOT))
_spec = importlib.util.spec_from_file_location("deck", ROOT / "build-team-pdf.py"); deck = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(deck)
pic, cut, money, GIFTS, typo = deck.pic, deck.cut, deck.money, deck.GIFTS, deck.typo

PHOTO = [  # one model or lifestyle shot per gift (none of them is used elsewhere in the deck): file, crop for a tall tile, caption
    ("photo/solo/krok-tw-3.webp", "34% 50%", "твіллі «Сміливий крок»"),
    ("photo/solo/puls-44-5.webp", "40% 50%", "хустка «Пульс» 44 × 44, двосторонній друк"),
    ("photo/site/set-ta-rezynka-litnie-pole-04.jpg", "45% 50%", "набір «Літнє поле»"),
    ("photo/site/set-tvilli-845-ta-khustky-4444-vpevnen-02.jpg", "50% 30%", "набір «Впевненість»"),
]
NOTE = "Базові роздрібні ціни obiimy.world на людину, без акцій сайту, жовтень 2026. Пакування й наліпка з вашим логотипом — безкоштовно. Бюджети команди — у гривнях."
MIX = "Тим, хто не носить аксесуари, — маска для сну (2 700 грн), закладка (800 грн) чи сертифікат на 1 000–4 000 грн · до 1 000 грн на людину — резинка, закладка, сертифікат · приклад розрахунку — на стор. " + str(deck.TERMS_P) + "."
H2 = 'Що в коробці — <i>і скільки це коштує</i>'
FOLIO = f'<p class="folio"><span><i class="fq">Запит: </i><a href="{deck.PHONE_HREF}">{deck.PHONE}</a> · <a href="{deck.TG}">Telegram @OBIIMY_sales</a></span><span>03</span></p>'
def rh(tag): return f'<p class="rh"><span>Чотири подарунки</span><span>Сторінка 3 · {tag}</span></p>'
def price(p, hi, big="h28"):
    top = f'<span class="t8 hi">до {money(hi)} грн — двосторонній друк</span>' if hi else '<span class="t8 hi">&nbsp;</span>'
    return f'<p class="pr {big}">{"<small>від</small> " if hi else ""}{money(p)} <small>грн</small>{top}</p>'
def b3(p, hi, one=False):
    def val(n):
        if not hi: return f"<span>{money(p * n)}</span>"
        return f"<span>{money(p * n)}–{money(hi * n)}</span>" if one else f"<span>від {money(p * n)}</span><span>до {money(hi * n)}</span>"
    return '<div class="b3">' + "".join(f'<div><span class="t8">{n} людей</span>{val(n)}</div>' for n in (20, 50, 100)) + '</div>'
def photo_note(): return "На фото: " + "; ".join(f"{i + 1} — {c}" for i, (_f, _p, c) in enumerate(PHOTO)) + "."
PAGES = []; NAMES = ['v0-now', 'vA', 'vB', 'vC', 'vD', 'vE']

# 0 · the page as it is now (table) — for comparison
PAGES.append(deck.PAGES[2].replace("Obiimy · Подарунки для команди · 2026", "Сторінка 3 · зараз — таблиця"))

# A · four photographs in the margins, the offer under each
def col_a(i, G):
    lb, n, d, p, hi, c = G; f, ps, _c = PHOTO[i]
    return f'<figure class="g">{pic(f, 61.5, 84, ps, once=False)}<p class="cap">0{i + 1} · {lb}</p><h3 class="h13">{n}</h3>{price(p, hi)}{b3(p, hi)}</figure>'
PAGES.append(f'''<section class="pg paper v3a">{rh("варіант A — чотири кадри")}<div class="sheet">
<div class="hd"><h2 class="h28">{H2}</h2><p>{NOTE}</p></div>
<div class="g4">{"".join(col_a(i, G) for i, G in enumerate(GIFTS))}</div>
<p class="t8 end">{photo_note()} {MIX}</p></div>{FOLIO}</section>''')

# B · four posters to the edge: the photograph is the page, the offer sits on it
POSTER = [("photo/solo/krok-tw-3.webp", "47% 50%", 1.0), ("photo/solo/puls-44-5.webp", "32% 100%", 1.55), ("photo/site/mask-nizhnist-03.jpg", "50% 50%", 1.0), ("photo/site/set-tvilli-845-ta-khustky-4444-vpevnen-02.jpg", "50% 20%", 1.0)]   # file, crop, zoom: the thing itself stays in the clear middle of the poster
PCAP = ["твіллі «Сміливий крок»", "хустка «Пульс» 44 × 44", "маска для сну «Ніжність»", "набір «Впевненість»"]
def col_b(i, G):
    lb, n, d, p, hi, c = G; f, ps, z = POSTER[i]
    rng = f"{money(p)}–{money(hi)} грн" if hi else f"{money(p)} грн"
    team = f"{money(p * 50)}–{money(hi * 50)}" if hi else money(p * 50)
    short = n.replace(" в коробці", "").replace("Маска для сну й резинка", "Маска й резинка")
    return (f'<figure class="po">{pic(f, 72, 160.5, ps, once=False, hi=True, zoom=z)}<div class="po-top"><p class="cap">0{i + 1} · {lb}</p><b class="h28"><i>{short}</i></b></div>'
            f'<figcaption><div class="chip">{cut(c, 13)}<div><span>На людину</span><em>{rng}</em></div></div><span class="t8">50 людей — {team} грн</span><span class="t8 ph">На фото — {PCAP[i]}</span></figcaption></figure>')
PAGES.append(f'''<section class="pg v3b"><div class="sh"><div><p class="cap">Чотири подарунки · сторінка 3 · варіант B — чотири постери</p><h2 class="h28">{H2}</h2></div>
<p>{NOTE}</p></div>
<div class="posters">{"".join(col_b(i, G) for i, G in enumerate(GIFTS))}</div>{FOLIO}</section>''')

# C · the shelf: large cut-outs of the things themselves, the price as the second hero
SHELF = [("krok-tw-1", 60), ("duo-hratsiia-ring", 54), ("maskscr-litnie-pole", 54), ("pair-zolote", 58)]
def col_c(i, G):
    lb, n, d, p, hi, c = G; name, mm = SHELF[i]
    return f'<figure class="g"><div class="obj">{cut(name, mm, fix=True)}</div><p class="cap">0{i + 1} · {lb}</p><h3 class="h13">{n.replace(" в коробці", "")}</h3>{price(p, hi, "h40")}{b3(p, hi)}</figure>'
PAGES.append(f'''<section class="pg paper v3c">{rh("варіант C — полиця")}<div class="sheet">
<div class="hd"><h2 class="h28">{H2}</h2><p>{NOTE}</p></div>
<div class="g4">{"".join(col_c(i, G) for i, G in enumerate(GIFTS))}</div>
<p class="t8 end">На вирізках: твіллі «Сміливий крок»; хустка «Грація» 44 × 44 і кільце «Н стиль»; набір «Літнє поле»; хустка й твіллі «Золоте світло» (двосторонній друк, 3 600 грн). {MIX}</p></div>{FOLIO}</section>''')

# D · one photograph for half the page — the open box — and the four gifts as a short list
def row_d(i, G):
    lb, n, d, p, hi, c = G
    pr = f'<p class="pr h28">{"<small>від</small> " if hi else ""}{money(p)} <small>грн</small></p>'
    return f'<div class="rw">{cut(c, 23, "th")}<p class="cap">0{i + 1} · {lb}</p><h3 class="h13">{n.replace(" в коробці", "").replace("Маска для сну й резинка", "Маска й резинка")}</h3>{pr}{b3(p, hi, one=True)}</div>'
PAGES.append(f'''<section class="pg split l v3d"><figure class="ph">{pic("photo/site/set-ta-rezynka-litnie-pole-04.jpg", 148.5, 210, "42% 50%", once=False)}</figure>
<div class="panel"><p class="cap">Чотири подарунки · варіант D — кадр і список</p><h2 class="h28">Що в коробці —<br><i>і скільки це коштує</i></h2>
<div class="rows">{"".join(row_d(i, G) for i, G in enumerate(GIFTS))}</div>
<p class="t8 phc">На фото — набір «Літнє поле». Базові роздрібні ціни obiimy.world, жовтень 2026; бюджети — у гривнях; пакування й наліпка з логотипом — безкоштовно.</p></div>{FOLIO}</section>''')

# E · one frame to the edge and four chips, as in the SOLO banners; budgets stay on page 13
def chip_e(i, G):
    lb, n, d, p, hi, c = G
    rng = f"{money(p)}–{money(hi)} грн" if hi else f"{money(p)} грн"
    team = f"від {money(p * 50)}" if hi else money(p * 50)
    short = n.replace(" в коробці", "").replace("Маска для сну й резинка", "Маска й резинка")
    return f'<div class="chip">{cut(c, 16)}<div><span>0{i + 1} · {short}</span><em>{rng}</em><span>50 людей — {team}</span></div></div>'
PAGES.append(f'''<section class="pg frame v3e">{pic("photo/solo/krok-tw-3.webp", 297, 210, "50% 35%", "bg", hi=True, once=False)}
<p class="vtag cap">Чотири подарунки · сторінка 3 · варіант E — кадр і чипи</p>
<div class="fr-t"><h1 class="h40">Що в коробці —<br><i>і скільки це коштує</i></h1>
<p class="fr-p">Ціна на людину — базова роздрібна, obiimy.world, жовтень 2026. Пакування й наліпка з вашим логотипом — безкоштовно. Бюджети на 20 і 100 людей, змішана команда й приклад розрахунку — на стор. {deck.TERMS_P}.</p>
<div class="chips4">{"".join(chip_e(i, G) for i, G in enumerate(GIFTS))}</div></div>{FOLIO}</section>''')

# F, G, H · concepts of the editorial art director (04.10), ported from working mock-ups ─────────────────
def ob(name, x, y, w, r, z, warm=False):
    """A cut-out placed by its top-left corner (mm), w mm wide, turned by r degrees; the shadow is baked into the picture."""
    f, pad, h = deck.cutsh(name, w, layers=((0.6, 0.5, 0.28), (3.6, 4.5, 0.26)), tint=(70, 45, 0)) if warm else deck.cutsh(name, w)
    return f'<div class="ob" style="left:{x - pad:.2f}mm;top:{y - pad:.2f}mm;width:{w + 2 * pad:.2f}mm;z-index:{z}"><img src="review/lb/{f}" alt="" style="transform:rotate({r}deg)"></div>'
def bt(p, hi): return '<dl class="bt">' + "".join(f"<div><dt>{n} людей</dt><dd>{money(p * n)}{'–' + money(hi * n) if hi else ''}</dd></div>" for n in (20, 50, 100)) + "</dl>"
def legend(i, G, style=""):
    lb, n, d, p, hi, c = G
    top = f"до {money(hi)} грн — двосторонній друк" if hi else "&nbsp;"
    return (f'<div class="lc"{style}><p class="cap">0{i + 1} · {lb}</p><h3 class="h13">{n}</h3><p class="pr h28">{"<small>від</small> " if hi else ""}{money(p)} <small>грн</small>'
            f'<span class="t8 hi">{top}</span></p>{bt(p, hi)}</div>')
NOTE2 = "Базові роздрібні ціни obiimy.world на людину, без акцій сайту, жовтень 2026. Пакування й наліпка з вашим логотипом — безкоштовно."
# F · still life: all four gifts as one composition on paper, the open box leaves through the top right corner
F_OBJ = [("set-natkhnennia-box-cw", 183, -6, 126, 0, 1), ("krok-tw-1", 18, 38, 63, -8, 3), ("duo-hratsiia-ring", 70, 43, 82, 4, 2), ("scrunchie-pole", 160, 50, 37, 10, 4), ("mask-litnie-pole", 138, 96, 92, -17, 5)]
PAGES.append(f"""<section class="pg paper k1"><p class="cap k1-cap">Чотири подарунки · сторінка 3 · варіант F — натюрморт</p>
<h2 class="h28 k1-h">{H2}</h2>{"".join(ob(*o) for o in F_OBJ)}
<div class="lg">{"".join(legend(i, G) for i, G in enumerate(GIFTS))}</div>
<p class="t8 foot">{NOTE2} На вирізках: твіллі «Сміливий крок»; хустка «Грація» 44 × 44 і кільце «Н стиль»; маска й резинка «Літнє поле»; хустка й твіллі «Натхнення» в коробці.</p>{FOLIO}</section>""")
# G · the yellow box: the page is the bottom of the brand's box, the gifts lie in it, prices as a menu
G_OBJ = [("tysha-tw-1", 4, -14, 74, -6, 2), ("duo-hratsiia-ring", 62, 13, 82, 5, 3), ("maskscr-litnie-pole", 152, 84, 83, -6, 4), ("pair-zolote", 196, 95, 97, 4, 3)]
G_TAG = [("01", 50, 89), ("02", 136, 89), ("03", 152, 152), ("04", 267, 81)]
def row_g(i, G):
    lb, n, d, p, hi, c = G
    bud = "".join(f"<span>{k} людей — {money(p * k)}{'–' + money(hi * k) if hi else ''}</span>" for k in (20, 50, 100))
    return f'<div class="mr"><p class="cap">0{i + 1} · {lb}</p><h3 class="h13">{n}</h3><p class="pr h28">{money(p)}{"–" + money(hi) if hi else ""} <small>грн</small></p><p class="t8 bud">{bud}</p></div>'
PAGES.append(f"""<section class="pg k2">{"".join(ob(*o, warm=True) for o in G_OBJ)}{"".join(f'<b class="tag" style="left:{x}mm;top:{y}mm">{t}</b>' for t, x, y in G_TAG)}
<div class="tt"><p class="cap">Чотири подарунки · сторінка 3 · варіант G — жовта коробка</p><h2 class="h40">Що в коробці —<br><i>і скільки це коштує</i></h2>
<p class="t8">{NOTE2} Ціна «від — до»: вища — з двостороннім друком; бюджети команди — у гривнях. На вирізках: твіллі «Тиша всередині»; хустка «Грація» й кільце «Н стиль»; набір «Літнє поле»; хустка й твіллі «Золоте світло» (двосторонній друк, 3 600 грн).</p></div>
<div class="menu">{"".join(row_g(i, G) for i, G in enumerate(GIFTS))}</div>{FOLIO}</section>""")
# H · steps: four studio frames stand on one line and rise with the price
H_X = [16.5, 84, 151.5, 219]; H_H = [67, 87, 107, 127]; H_B = 187
H_PH = [("photo/site/set-makovyi-tsvit-02.jpg", (0, 95, 1125, 1321), "На фото — твіллі з набору «Маків цвіт»"), ("photo/site/ring-n-styl-02.jpg", (500, 275, 1150, 1195), "На фото — кільце «Н стиль» на хустці"),
        ("photo/site/mask-nizhnist-03.jpg", (285, 0, 1147, 1500), "На фото — маска для сну «Ніжність»"), ("photo/site/set-tvilli-845-ta-khustky-4444-natkhne-02.jpg", (143, 0, 869, 1500), "На фото — набір «Натхнення»")]
def step(x, h, f, bx, c):
    im = pic(f, 61.5, h, once=False, box=bx).replace("<img ", "<img style='height:%smm' " % h)
    return f'<figure class="st" style="left:{x}mm;top:{H_B - h}mm">{im}<figcaption class="t8">{c}</figcaption></figure>'
steps = "".join(step(x, h, *ph) for x, h, ph in zip(H_X, H_H, H_PH))
legs = "".join(legend(i, G, f' style="left:{x}mm;bottom:{210 - (H_B - h) + 3}mm"') for i, (G, x, h) in enumerate(zip(GIFTS, H_X, H_H)))
PAGES.append(f"""<section class="pg paper k3"><p class="cap k3-cap">Чотири подарунки · сторінка 3 · варіант H — сходинки</p><h2 class="h28 k3-h">Що в коробці —<br><i>і скільки це коштує</i></h2>
<p class="t8 k3-n">{NOTE2}</p>{steps}{legs}{FOLIO}</section>""")
NAMES += ["vF", "vG", "vH"]

# I, J, K · concepts of the luxury-catalogue art director (04.10): plates assembled from real photos and cut-outs (img/p3, scripts in src/ad-p3)
def folio_tag(t): return FOLIO.replace("<span>03</span>", f'<span class="vt">Сторінка 3 · {t}</span><span>03</span>')
def budgets(p, hi): return [money(p * k) + (f"–{money(hi * k)}" if hi else "") for k in (20, 50, 100)]
def row_i(i, G):
    lb, n, d, p, hi, c = G
    note = (f"до {money(hi)} грн —<br>" + ("з двостороннім друком" if i == 1 else "двосторонній друк")) if hi else ""
    return (f'<div class="xlg"><b class="num">0{i + 1}</b><div><p class="cap">{lb}</p><h3 class="h13">{n}</h3></div>'
            f'<span class="pp h28"><small>{"від" if hi else ""}</small><span>{money(p)}</span><small>грн</small></span><span class="t8 nt">{note}</span>'
            + "".join(f'<span class="bd">{b}</span>' for b in budgets(p, hi)) + '</div>')
def cell_x(i, G, big):
    lb, n, d, p, hi, c = G
    note = (f"до {money(hi)} грн — " + ("з двостороннім друком" if i == 1 else "двосторонній друк")) if hi else "&nbsp;"
    bl = "".join(f"<div><dt>{k} людей</dt><dd>{b}</dd></div>" for k, b in zip((20, 50, 100), budgets(p, hi)))
    return (f'<article class="c c{i + 1}"><p class="cap">0{i + 1} · {lb}</p><h3 class="h13">{n}</h3><p class="pr {big}">{"<small>від</small> " if hi else ""}{money(p)} <small>грн</small></p>'
            f'<p class="t8 nt">{note}</p><dl class="bl">{bl}</dl></article>')
FINE = "Базові роздрібні ціни obiimy.world на людину, без акцій сайту, жовтень 2026. Пакування й наліпка з вашим логотипом — безкоштовно. Бюджети команди — у гривнях."
# I · a table seen from above: two real boxes come in from the top corners, the title between them, a fine ledger below
PAGES.append(f"""<section class="pg paper x1"><img class="bg" src="img/p3/lux-k1.jpg" alt="">
<div class="ttl"><h2 class="h28">Що в коробці —<br><i>і скільки це коштує</i></h2></div>
<p class="lab" style="left:16.5mm;top:105mm"><b>04</b><span>набір «Сміливий дотик»</span></p><p class="lab" style="left:102mm;top:105mm"><b>01</b><span>твіллі «Тиша всередині»</span></p>
<p class="lab" style="left:139mm;top:105mm"><b>02</b><span>хустка «Грація», кільце «Н стиль»</span></p><p class="lab r" style="right:16.5mm;top:105mm"><b>03</b><span>набір «Літнє поле»</span></p>
<div class="x1b"><div class="xlg head"><span></span><span class="cap">Подарунок</span><span class="cap" style="padding-left:8.5mm">На людину</span><span></span><span class="cap bd">20 людей</span><span class="cap bd">50 людей</span><span class="cap bd">100 людей</span></div>
{"".join(row_i(i, G) for i, G in enumerate(GIFTS))}<p class="t8 fine">{FINE}</p></div>{folio_tag("варіант I — стіл і дві коробки")}</section>""")
# J · the page is the box: brand yellow to the edge, four compartments
PAGES.append(f"""<section class="pg x2"><img class="bg" src="img/p3/lux-k2.jpg" alt=""><p class="rh"><span>Чотири подарунки</span><span>Сторінка 3 · варіант J — чотири відділення</span></p>
<h2 class="h40 x2t">Що в коробці — <i>і скільки це коштує</i></h2><div class="tray"></div>
{"".join(cell_x(i, G, "h40") for i, G in enumerate(GIFTS))}
<p class="t8 fine">На вирізках: твіллі «Флірт»; хустка «Пульс» 44 × 44 і кільце «Н стиль» — з двостороннім друком, 2 850 грн; набір «Літнє поле»; хустка й твіллі «Золоте світло» — 3 600 грн.<br>{FINE}</p>{FOLIO}</section>""")
# K · a yellow podium of four steps: the gifts stand on the steps, the real box on the top one
PAGES.append(f"""<section class="pg paper x3"><img class="bg" src="img/p3/lux-k3.jpg" alt="">
<div class="ttl"><p class="cap">Чотири подарунки · сторінка 3 · варіант K — подіум</p><h2 class="h40">Що в коробці —<br><i>і скільки це коштує</i></h2></div>
{"".join(cell_x(i, G, "h28") for i, G in enumerate(GIFTS))}
<p class="t8 fine">На вирізках: твіллі «Авантюра»; хустка «Грація» 44 × 44 і кільце «Н стиль»; набір «Літнє поле»; на фото — набір «Впевненість».<br>{FINE}</p>{FOLIO}</section>""")
NAMES += ["vI", "vJ", "vK"]

# ── cover variants ──────────────────────────────────────────────────────────────────────────────────
LINE = deck.COVER_LINE
CAP = deck.COVER_CAP
H1 = deck.COVER_H1; H1W = "Подарунки для команди —<br><i>шовк, який носять</i>"; PRICE = deck.COVER_PRICE
def vtag(t): return f'<p class="vtag r cap">Обкладинка · {t}</p>'
COVERS = []
# B · another frame of the same shoot: a portrait with the scarf on the wrist
COVERS.append(f'''<section class="pg frame cv cvb">{pic("photo/solo/krok-44-3.webp", 297, 210, "50% 58%", "bg", hi=True, once=False)}<img src="brand/logo-white.png" class="logo" alt="Obiimy">{vtag("варіант B — портрет")}
<div class="fr-t"><p class="cap">{CAP}</p><h1 class="h54">{H1}</h1>
<div class="chip">{cut("krok-44-1", 13)}<div><span>Чотири варіанти подарунка · на людину</span><em>від 1 600 до 3 600 грн</em></div></div></div>{LINE}</section>''')
# C · paper and a photograph: the title on paper, the portrait takes the right half
COVERS.append(f'''<section class="pg cv cvc"><figure class="cph">{pic("photo/solo/puls-44-4.webp", 148.5, 210, "52% 50%", hi=True, once=False)}</figure>{vtag("варіант C — папір і портрет")}
<img src="brand/logo-ink.png" class="logo" alt="Obiimy">
<div class="cvt"><p class="cap">{CAP}</p><h1 class="h54">{H1}</h1>
<p class="h13">{PRICE}</p></div>{LINE}</section>''')
# D · three portraits — a team — and the title on a paper band
TRI = [("photo/solo/avantiura-88-5.webp", "62% 50%"), ("photo/solo/puls-44-4.webp", "50% 50%"), ("photo/solo/krok-44-3.webp", "50% 50%")]
COVERS.append(f'''<section class="pg cv cvd"><div class="tri">{"".join(pic(f, 97, 129, ps, hi=True, once=False) for f, ps in TRI)}</div>{vtag("варіант D — три портрети")}
<img src="brand/logo-ink.png" class="logo" alt="Obiimy">
<div class="cvt"><p class="cap">{CAP}</p><h1 class="h54">{H1W}</h1></div>
<p class="h13 cvp">Чотири варіанти подарунка<br>від 1 600 до 3 600 грн на людину</p>{LINE}</section>''')
def cve_ob(c, mm, x, y, r):
    iw, ih = Image.open(OUT / "img" / "cut" / f"{c}.webp").size; w = mm * min(1, iw / ih)          # mm is the long side
    f, pad, h = deck.cutsh(c, w, layers=((3.0, 4.0, 0.18),), tint=(0, 0, 0))
    return f'<div class="ob" style="left:{x - pad:.2f}mm;top:{y - pad:.2f}mm;width:{w + 2 * pad:.2f}mm"><img src="review/lb/{f}" alt="" style="width:100%;height:auto"></div>'
# E · the things themselves on paper, as in a gift guide
OBJ = [("krok-tw-1", 74, 163.5, 22.5, 0), ("duo-hratsiia-ring", 60, 219, 33, 0), ("maskscr-litnie-pole", 60, 157.5, 115.5, 0), ("pair-zolote", 64, 216, 112.5, 0)]   # cut-out, size mm, x, y, rotation
COVERS.append(f'''<section class="pg cv cve">{"".join(cve_ob(*o) for o in OBJ)}{vtag("варіант E — речі на папері")}
<img src="brand/logo-ink.png" class="logo" alt="Obiimy">
<div class="cvt"><p class="cap">{CAP}</p><h1 class="h54">{H1}</h1>
<p class="h13">{PRICE}</p></div>{LINE}</section>''')
# F · a wide scene by the sea, the scarf worn as a belt
COVERS.append(f'''<section class="pg frame cv cvf">{pic("photo/solo/avantiura-88-2.webp", 297, 210, "50% 30%", "bg", hi=True, once=False)}<img src="brand/logo-white.png" class="logo" alt="Obiimy">{vtag("варіант F — сцена")}
<div class="fr-t"><p class="cap">{CAP}</p><h1 class="h54">{H1}</h1>
<div class="chip">{cut("avantiura-88-1", 13)}<div><span>Чотири варіанти подарунка · на людину</span><em>від 1 600 до 3 600 грн</em></div></div></div>{LINE}</section>''')

# G, H, I · object-led covers of the luxury-catalogue art director (plates: src/build-cover-plates.py → img/p3/cover-*.jpg)
CONTACTS = f'<a href="https://obiimy.world/">obiimy.world</a> · <a href="{deck.PHONE_HREF}">{deck.PHONE}</a> · <a href="{deck.TG}">Telegram @OBIIMY_sales</a>'
WHO = "Український бренд шовкових хусток і аксесуарів"
PACK = "Пакування й наліпка з вашим логотипом — у ціні"
COVERS.append(f"""<section class="pg lx lx1"><img class="plate" src="img/p3/cover-1.jpg" alt=""><img src="brand/logo-ink.png" class="lxlogo" alt="Obiimy">
<p class="cap who">{WHO}</p>
<div class="lxt"><p class="cap">Корпоративні подарунки · 2026 · обкладинка, варіант G</p>
<h1 class="h54">Подарунки<br>для команди —<br><i>шовк,<br>який носять</i></h1>
<p class="price">Чотири варіанти подарунка —<br>від 1 600 до 3 600 грн на людину</p><p class="pack">{PACK}</p></div>
<p class="credit">На обкладинці — набір «Ніжність»: хустка й твіллі,<br>варіант за 3 600 грн.</p>
<p class="folio"><span>{CONTACTS}</span></p></section>""")
COVERS.append(f"""<section class="pg lx lx2"><img class="plate" src="img/p3/cover-2.jpg" alt=""><img src="brand/logo-ink.png" class="lxlogo" alt="Obiimy">
<p class="cap who">{WHO}</p><div class="rule"></div>
<p class="lxc" style="left:16.5mm"><b>01</b>Твіллі</p><p class="lxc" style="left:62mm"><b>02</b>Хустка й кільце</p>
<p class="lxc" style="left:121mm"><b>03</b>Маска для сну й резинка</p><p class="lxc" style="left:187mm"><b>04</b>Хустка й твіллі в коробці</p>
<div class="lxt"><h1 class="h54">Подарунки для команди —<br><i>шовк, який носять</i></h1>
<div class="row"><div><p class="price">{PRICE}</p><p class="pack">{PACK}</p></div>
<p class="t8 lxcr">На обкладинці — принти «Тиша всередині», «Золоте світло»,<br>«Літнє поле», «Грація» · варіант H</p></div></div>
<p class="folio"><span>Корпоративні подарунки · 2026</span><span>{CONTACTS}</span></p></section>""")
COVERS.append(f"""<section class="pg lx lx3"><img class="sun" src="img/p3/cover-3.jpg" alt=""><img src="brand/logo-ink.png" class="lxlogo" alt="Obiimy">
<p class="cap who">Український бренд<br>шовкових хусток і аксесуарів</p>
<div class="lxt"><p class="cap">Корпоративні подарунки · 2026 · варіант I</p>
<h1 class="h40">Подарунки<br>для команди —<br><i>шовк,<br>який носять</i></h1>
<p class="price">Чотири варіанти подарунка —<br>від 1 600 до 3 600 грн на людину</p><p class="pack">{PACK}</p></div>
<p class="credit">На обкладинці — набір «Літнє поле»: маска для сну й резинка.</p>
<p class="folio"><span><a href="https://obiimy.world/">obiimy.world</a></span><span><a href="{deck.PHONE_HREF}">{deck.PHONE}</a> · <a href="{deck.TG}">Telegram @OBIIMY_sales</a></span></p></section>""")

# J, K, L · covers of the editorial art director (plates img/p3/cover-4…6.jpg)
COVERS.append(f"""<section class="pg ed ed1"><img class="plate" src="img/p3/cover-4.jpg" alt="">
<div class="ed1-col"><img src="brand/logo-ink.png" class="ed-logo" alt="Obiimy"><p class="cap ed-who">Український бренд шовкових<br>хусток і аксесуарів</p>
<div class="ed1-b"><p class="cap">Корпоративні подарунки · 2026 · варіант J</p>
<h1 class="ed-h50">Подарунки<br>для команди —<br><i>шовк, який<br>носять</i></h1>
<p class="ed-price">Чотири варіанти подарунка —<br>від 1 600 до 3 600 грн на людину</p><p class="ed-pack">{PACK}</p></div></div>
<p class="folio"><span>У коробці — хустка й твіллі «Золоте світло», 3 600 грн</span><span>{CONTACTS}</span></p></section>""")
COVERS.append(f"""<section class="pg ed ed2"><img class="plate" src="img/p3/cover-5.jpg" alt="">
<img src="brand/logo-ink.png" class="ed-logo" alt="Obiimy"><p class="cap ed-who">Український бренд шовкових хусток<br>і аксесуарів</p>
<div class="ed2-t"><p class="cap">Корпоративні подарунки · 2026 · варіант K</p><h1>Шовкові подарунки<br><i>для команди</i></h1></div>
<div class="ed2-p"><p class="ed-price">Чотири варіанти подарунка —<br>від 1 600 до 3 600 грн на людину</p><p class="ed-pack">{PACK}</p></div>
<p class="folio"><span>У коробці — хустка й твіллі «Золоте світло»</span><span>{CONTACTS}</span></p></section>""")
COVERS.append(f"""<section class="pg ed ed3"><img class="plate" src="img/p3/cover-6.jpg" alt="">
<div class="ed3-m"><img src="brand/logo-ink.png" class="ed-logo" alt="Obiimy"><p class="cap ed-who">Український бренд<br>шовкових хусток<br>і аксесуарів</p>
<p class="t8">На фото — хустки<br>«Сміливий дотик» і «Натхнення».<br>У коробці — хустка й твіллі<br>«Натхнення», 3 200 грн.</p></div>
<div class="ed3-t"><p class="cap">Корпоративні подарунки · 2026 · варіант L</p>
<h1 class="ed-h50">Подарунки<br>для команди —<br><i>шовк, який носять</i></h1>
<p class="ed-price">{PRICE}</p><p class="ed-pack">{PACK}</p></div>
<p class="folio"><span>{CONTACTS}</span></p></section>""")

CSS = deck.CSS + """
/* J, K, L — the editorial art director's covers (prefix ed) */
.ed .plate { position: absolute; left: 0; top: 0; width: 297mm; height: 210mm; } .ed .cap { color: #6E6A63; } .ed1 h1 i, .ed3 h1 i { color: #6E6A63; }
.ed-h50 { font: 400 50pt/52pt Playfair, serif; letter-spacing: -.012em; } .ed-price { font: 400 13pt/16.5pt Playfair, serif; font-variant-numeric: lining-nums; color: #141414; } .ed-pack { color: #4A4A47; margin-top: .75mm; }
.ed .folio { z-index: 2; } .ed .folio a { color: inherit; }
.ed1-col { position: absolute; left: 154.5mm; right: 16.5mm; top: 16.5mm; bottom: 22.5mm; display: flex; flex-direction: column; } .ed1-col .ed-logo { width: 62mm; height: auto; } .ed1-col .ed-who { margin-top: 4.5mm; }
.ed1-b { margin-top: auto; } .ed1-b .cap { margin-bottom: 3.75mm; } .ed1-b h1 { margin-bottom: 6mm; white-space: nowrap; } .ed1-b .ed-price { border-top: .5pt solid #141414; padding-top: 3mm; }
.pg.ed2 { background: #FDD31A; color: #141414; } .ed2 .cap { color: rgba(20,20,20,.72); } .ed2 .ed-logo { position: absolute; left: 16.5mm; top: 16.5mm; width: 70mm; height: auto; } .ed2 .ed-who { position: absolute; left: 16.5mm; top: 36mm; }
.ed2-t { position: absolute; left: 16.5mm; bottom: 22.5mm; } .ed2-t .cap { margin-bottom: 3.75mm; } .ed2-t h1 { font: 400 62pt/61pt Playfair, serif; letter-spacing: -.012em; white-space: nowrap; } .ed2-t h1 i { color: rgba(20,20,20,.6); }
.ed2-p { position: absolute; right: 16.5mm; bottom: 24mm; text-align: right; } .ed2 .ed-pack { color: rgba(20,20,20,.76); } .ed2 .folio { color: rgba(20,20,20,.68); }
.ed3-m { position: absolute; left: 118mm; top: 16.5mm; width: 52.5mm; } .ed3-m .ed-logo { width: 52.5mm; height: auto; } .ed3-m .ed-who { margin-top: 4.5mm; } .ed3-m .t8 { margin-top: 3mm; }
.ed3-t { position: absolute; left: 16.5mm; bottom: 22.5mm; width: 150mm; } .ed3-t .cap { margin-bottom: 3mm; } .ed3-t h1 { margin-bottom: 4.5mm; white-space: nowrap; } .ed3 .folio { right: 134.5mm; }
/* G, H, I — object-led covers (prefix lx) */
.lx .plate { position: absolute; left: 0; top: 0; width: 297mm; height: 210mm; }
.lx .lxlogo { position: absolute; left: 16.5mm; top: 16.5mm; width: 52mm; height: 11.05mm; z-index: 2; }
.lx .who { position: absolute; left: 16.5mm; top: 32.2mm; z-index: 2; }
.lx .lxt { position: absolute; z-index: 2; } .lx .lxt .cap { margin-bottom: 4.5mm; } .lx .lxt h1 { margin-bottom: 6.75mm; }
.lx .price { font: 400 13pt/16.5pt Playfair, serif; color: #141414; } .lx .pack { font-size: 9.5pt; line-height: 4.5mm; color: #4A4A47; margin-top: 2.25mm; }
.lx .folio { z-index: 2; color: #6E6A63; } .lx .credit { position: absolute; top: 196.4mm; font-size: 8pt; line-height: 3.75mm; color: #6E6A63; z-index: 2; }
.lx1 .lxlogo, .lx1 .who { left: 148.5mm; } .lx1 .lxt { left: 148.5mm; width: 132mm; bottom: 24mm; } .lx1 .credit { left: 16.5mm; top: 192.65mm; } .lx1 .folio { left: 148.5mm; justify-content: flex-start; }
.lx2 .rule { position: absolute; left: 16.5mm; right: 16.5mm; top: 115.5mm; border-top: .5pt solid #141414; z-index: 2; }
.lx2 .lxc { position: absolute; top: 119.5mm; font: 400 13pt/16.5pt Playfair, serif; color: #141414; z-index: 2; white-space: nowrap; }
.lx2 .lxc b { font-style: italic; font-weight: 400; color: #8E8A84; margin-right: 2mm; }
.lx2 .lxt { left: 16.5mm; right: 16.5mm; top: 133.5mm; } .lx2 .lxt h1 { margin-bottom: 5.25mm; } .lx2 .row { display: flex; justify-content: space-between; align-items: flex-end; } .lx2 .row .pack { margin-top: .75mm; } .lx2 .lxcr { text-align: right; color: #6E6A63; }
.pg.lx3 { background: #FDD31A; } .lx3 .sun { position: absolute; left: 127mm; top: 0; width: 170mm; height: 210mm; } .lx3 .lxt { left: 16.5mm; width: 104mm; bottom: 36mm; }
.lx3 h1 i { color: #86690F; } .lx3 .cap, .lx3 .folio { color: rgba(20,20,20,.72); } .lx3 .pack { color: rgba(20,20,20,.78); }
.lx3 .folio { right: auto; display: block; top: 192.65mm; } .lx3 .folio span { display: block; } .lx3 .credit { left: 133mm; color: rgba(20,20,20,.62); }

/* page 3 variants */
.pr { white-space: nowrap; } .pr small { color: #8E8A84; font-style: italic; } .pr .hi { display: block; font-family: Tenor, sans-serif; letter-spacing: 0; margin-top: .75mm; }
.b3 { display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 3mm; border-top: .35pt solid #C9C6C0; padding-top: 1.5mm; margin-top: 2.25mm; font-variant-numeric: lining-nums tabular-nums; font-size: 8pt; line-height: 3.75mm; } .b3 span { display: block; white-space: nowrap; }
.g4 { display: grid; grid-template-columns: repeat(4, 61.5mm); column-gap: 6mm; } .g4 .cap { margin: 3mm 0 .75mm; letter-spacing: .13em; white-space: nowrap; } .g4 h3 { margin-bottom: .75mm; white-space: nowrap; }
.v3a .g img { width: 61.5mm; height: 84mm; object-fit: cover; }
.v3b { background: #F1EFEA; } .v3b .sh { grid-template-columns: 1fr 96mm; } .v3b .sh > p { color: #4A4A47; } .v3b .sh .cap { color: #6E6A63; } .v3b .sh h2 { white-space: nowrap; }
.posters { position: absolute; left: 0; right: 0; top: 49.5mm; bottom: 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; }
.po { position: relative; overflow: hidden; } .po > img { width: 100%; height: 100%; object-fit: cover; }
.po::after { content: ""; position: absolute; inset: 0; background: linear-gradient(0deg, rgba(0,0,0,.88) 0%, rgba(0,0,0,.6) 22%, rgba(0,0,0,0) 40%), linear-gradient(180deg, rgba(0,0,0,.66) 0%, rgba(0,0,0,.4) 18%, rgba(0,0,0,0) 34%); }
.po-top { position: absolute; left: 6mm; right: 4.5mm; top: 6mm; z-index: 2; color: #fff; }
.po figcaption { position: absolute; left: 6mm; right: 4.5mm; bottom: 18mm; z-index: 2; color: #fff; } .po .cap { color: rgba(255,255,255,.82); margin-bottom: 1.5mm; letter-spacing: .13em; } .po b { display: block; color: #E7D9A6; margin-bottom: 3.75mm; }
.po .chip { margin-bottom: 2.25mm; padding-right: 3.5mm; } .po .t8 { display: block; color: rgba(255,255,255,.88); } .po .t8.ph { color: rgba(255,255,255,.66); } .po b { margin-bottom: 0; }
.v3b .folio { color: rgba(255,255,255,.7); z-index: 3; }
.v3c .obj { height: 63mm; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 2.25mm; border-bottom: .5pt solid #141414; } .v3c .obj img { filter: drop-shadow(0 2mm 2.5mm rgba(0,0,0,.16)); }
.v3c .pr { margin: 1.5mm 0 0; }
.rows { margin-top: -1.5mm; } .rw { display: grid; grid-template-columns: 21mm 1fr auto; column-gap: 4.5mm; align-items: baseline; padding: 1.5mm 0; border-top: .35pt solid #C9C6C0; } .rw:last-child { border-bottom: .35pt solid #C9C6C0; }
.rw .th { grid-row: 1 / 4; align-self: center; width: 21mm; height: 21mm; object-fit: contain; filter: drop-shadow(0 1mm 1.5mm rgba(0,0,0,.14)); } .rw .cap { grid-column: 2 / 4; letter-spacing: .13em; }
.rw .b3 { grid-column: 2 / 4; margin-top: 0; padding-top: .75mm; } .rw .pr { line-height: 26pt; } .v3d .panel h2 { margin-bottom: 4.5mm; }
.v3d .phc { margin-top: auto; }
/* I, J, K — the luxury-catalogue art director's concepts */
.x1 .bg, .x2 .bg, .x3 .bg { position: absolute; left: 0; top: 0; width: 297mm; height: 210mm; } .vt { color: inherit; }
.x1 .lab { position: absolute; display: flex; align-items: baseline; gap: 2.25mm; white-space: nowrap; z-index: 2; } .x1 .lab b { font: italic 400 13pt/16.5pt Playfair, serif; color: #141414; }
.x1 .lab span { font-size: 8pt; line-height: 3.75mm; color: #6E6A63; } .x1 .lab.r { flex-direction: row-reverse; }
.x1 .ttl { position: absolute; left: 98.5mm; width: 100mm; top: 13.5mm; text-align: center; z-index: 2; }
.x1b { position: absolute; left: 16.5mm; right: 16.5mm; top: 116mm; z-index: 2; } .x1b .fine { margin-top: 3mm; }
.xlg { display: grid; grid-template-columns: 10.5mm 1fr 46.5mm 33mm 24mm 30.5mm 30.5mm; column-gap: 4.5mm; align-items: center; height: 14.25mm; border-top: .35pt solid #C9C6C0; } .xlg:last-of-type { border-bottom: .35pt solid #C9C6C0; }
.xlg.head { height: auto; border-top: .5pt solid #141414; padding: 1.9mm 0 1.6mm; } .xlg h3 { margin-top: .4mm; white-space: nowrap; } .xlg .cap { white-space: nowrap; letter-spacing: .2em; }
.xlg .pp { white-space: nowrap; line-height: 26pt; display: grid; grid-template-columns: 8.5mm auto 1fr; align-items: baseline; } .xlg .pp small { color: #8E8A84; font-style: italic; } .xlg .pp small:last-child { padding-left: 2mm; }
.xlg .nt { color: #6E6A63; white-space: nowrap; } .xlg .bd { text-align: right; font-variant-numeric: lining-nums tabular-nums; white-space: nowrap; }
.pg.x2 { background: #FDD31A; color: #141414; } .x2 .rh { color: rgba(20,20,20,.66); border-bottom-color: #141414; z-index: 2; } .x2 .folio, .x3 .folio { color: rgba(20,20,20,.62); z-index: 2; }
.x2 .x2t { position: absolute; left: 16.5mm; top: 24mm; white-space: nowrap; z-index: 2; } .x2 .x2t i { color: rgba(20,20,20,.5); }
.x2 .tray { position: absolute; left: 16.5mm; right: 16.5mm; top: 47mm; height: 131mm; border-top: .5pt solid #141414; border-bottom: .5pt solid #141414; z-index: 1; }
.x2 .tray::before { content: ""; position: absolute; left: 132mm; top: 0; bottom: 0; border-left: .5pt solid #141414; } .x2 .tray::after { content: ""; position: absolute; left: 0; right: 0; top: 65.5mm; border-top: .5pt solid #141414; }
.x2 .c { position: absolute; width: 58.5mm; height: 65.5mm; display: flex; flex-direction: column; justify-content: center; z-index: 2; }
.x2 .c1, .x2 .c3 { left: 84mm; } .x2 .c2, .x2 .c4 { left: 222mm; } .x2 .c1, .x2 .c2 { top: 47mm; } .x2 .c3, .x2 .c4 { top: 112.5mm; }
.x2 .c .cap, .x3 .c .cap { color: rgba(20,20,20,.66); letter-spacing: .13em; white-space: nowrap; margin-bottom: 1.5mm; } .x2 .c h3, .x3 .c h3 { white-space: nowrap; }
.x2 .c .pr { margin-top: .75mm; white-space: nowrap; } .x2 .c .pr small, .x3 .c .pr small { color: rgba(20,20,20,.55); font-style: italic; }
.x2 .c .nt { color: rgba(20,20,20,.66); white-space: nowrap; min-height: 3.75mm; margin: .5mm 0 2.25mm; }
.bl > div { display: flex; justify-content: space-between; align-items: baseline; padding: .65mm 0; border-top: .35pt solid rgba(20,20,20,.3); font-variant-numeric: lining-nums tabular-nums; } .bl > div:last-child { border-bottom: .35pt solid rgba(20,20,20,.3); }
.bl dt { font-size: 8pt; line-height: 3.75mm; color: rgba(20,20,20,.66); } .bl dd { white-space: nowrap; }
.x2 .fine { position: absolute; left: 16.5mm; right: 16.5mm; top: 181.25mm; color: rgba(20,20,20,.7); z-index: 2; }
.x3 .ttl { position: absolute; left: 16.5mm; top: 16.5mm; z-index: 2; } .x3 .ttl .cap { margin-bottom: 3.75mm; }
.x3 .c { position: absolute; top: 133mm; width: 58.5mm; z-index: 2; } .x3 .c1 { left: 16.5mm; } .x3 .c2 { left: 84mm; } .x3 .c3 { left: 151.5mm; } .x3 .c4 { left: 219mm; width: 61.5mm; }
.x3 .c .cap { margin-bottom: .75mm; } .x3 .c .pr { white-space: nowrap; } .x3 .c .nt { color: rgba(20,20,20,.66); white-space: nowrap; min-height: 3.75mm; margin: 0 0 1.5mm; } .x3 .bl > div { padding: .4mm 0; }
.x3 .fine { position: absolute; left: 16.5mm; right: 16.5mm; top: 182.25mm; color: rgba(20,20,20,.7); z-index: 2; }
/* F, G, H — the editorial art director's concepts */
.k1 .k1-cap, .k3 .k3-cap { position: absolute; left: 16.5mm; top: 16.5mm; } .k1 .k1-h, .k3 .k3-h { position: absolute; left: 16.5mm; top: 22.5mm; white-space: nowrap; }
.k1 .ob { position: absolute; } .k1 .ob img, .k2 .ob img { width: 100%; height: auto; }
.k1 .lg { position: absolute; left: 16.5mm; top: 139.5mm; display: grid; grid-template-columns: repeat(4, 61.5mm); column-gap: 6mm; }
.k1 .lc { border-top: .5pt solid #141414; padding-top: 2.25mm; } .lc .cap { letter-spacing: .13em; white-space: nowrap; margin-bottom: .5mm; } .lc h3 { white-space: nowrap; } .lc .pr { margin-top: 0; }
.bt { margin-top: 1.1mm; border-top: .35pt solid #C9C6C0; padding-top: 1.1mm; font-size: 8pt; line-height: 3.75mm; font-variant-numeric: lining-nums tabular-nums; } .bt div { display: flex; justify-content: space-between; white-space: nowrap; } .bt dt { color: #6E6A63; }
.k1 .foot { position: absolute; left: 16.5mm; right: 16.5mm; top: 185mm; }
.pg.k2 { background: #FCD21C; color: #141414; } .k2 .cap, .k2 .t8 { color: rgba(20,20,20,.74); } .k2 h2 i { color: rgba(20,20,20,.5); } .k2 .folio { color: rgba(20,20,20,.66); }
.k2 .ob { position: absolute; }
.k2 .tag { position: absolute; font: italic 400 28pt/30pt Playfair, serif; color: #141414; z-index: 9; }
.k2 .tt { position: absolute; left: 151.5mm; top: 16.5mm; width: 129mm; } .k2 .tt .cap { margin-bottom: 3.75mm; } .k2 .tt h2 { white-space: nowrap; margin-bottom: 4.5mm; } .k2 .tt .t8 { width: 112mm; }
.k2 .menu { position: absolute; left: 16.5mm; top: 109.5mm; width: 129mm; }
.k2 .mr { display: grid; grid-template-columns: 1fr auto; align-items: end; border-top: .5pt solid #141414; padding: 1.2mm 0 1.6mm; } .k2 .mr:last-child { border-bottom: .5pt solid #141414; }
.k2 .mr .pr { line-height: 24pt; } .k2 .mr .pr small { line-height: 1; color: rgba(20,20,20,.6); } .k2 .mr h3 { line-height: 16.5pt; position: relative; top: 1.7pt; } .k2 .mr .cap { grid-column: 1 / 3; letter-spacing: .13em; }
.k2 .mr .bud { grid-column: 1 / 3; margin-top: 1mm; display: grid; grid-template-columns: repeat(3, 1fr); font-variant-numeric: lining-nums tabular-nums; white-space: nowrap; color: #141414; } .k2 .mr .bud span:nth-child(2) { text-align: center; } .k2 .mr .bud span:nth-child(3) { text-align: right; }
.k3 .k3-n { position: absolute; left: 16.5mm; top: 48.75mm; width: 61.5mm; color: #6E6A63; }
.k3 .st { position: absolute; width: 61.5mm; } .k3 .st img { width: 61.5mm; object-fit: cover; } .k3 .st figcaption { position: absolute; left: 0; top: calc(100% + 1.5mm); color: #8E8A84; white-space: nowrap; }
.k3 .lc { position: absolute; width: 61.5mm; }
.vtag { position: absolute; left: 16.5mm; top: 16.5mm; z-index: 2; } .vtag.r { left: auto; right: 16.5mm; top: 19.5mm; z-index: 3; }
/* cover variants */
.cv .logo { position: absolute; left: 16.5mm; top: 16.5mm; height: 9mm; width: 42.4mm; z-index: 2; } .cv .folio { z-index: 2; }
.cvc .cph, .cph { position: absolute; right: 0; top: 0; width: 148.5mm; height: 210mm; } .cph img { width: 100%; height: 100%; object-fit: cover; }
.cvt { position: absolute; left: 16.5mm; bottom: 22.5mm; width: 126mm; z-index: 2; } .cve .cvt { width: 138mm; } .cvc .cvt h1 { font-size: 50pt; line-height: 50pt; } .cvt .cap { max-width: 112mm; } .cvt .cap { margin-bottom: 3mm; } .cvt h1 { margin-bottom: 6mm; }
.cvc .vtag, .cve .vtag { color: #6E6A63; } .cvc .vtag { color: rgba(255,255,255,.8); }
.cvc .folio span:last-child { color: rgba(255,255,255,.8); }
.tri { position: absolute; left: 0; right: 0; top: 0; height: 129mm; display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; } .tri img { width: 100%; height: 129mm; object-fit: cover; }
.cvd .cvt { width: 264mm; bottom: 21mm; } .cvd .cvt h1 { margin-bottom: 0; } .cvd .cvp { position: absolute; right: 16.5mm; bottom: 24mm; text-align: right; color: #4A4A47; }
.cvd .logo { left: auto; right: 16.5mm; top: 141mm; } .cvd .vtag { color: rgba(255,255,255,.85); }
.cvb .fr-t { left: auto; right: 16.5mm; width: 130mm; text-align: right; } .cvb .chip { text-align: left; }
.cvb::after { background: linear-gradient(270deg, rgba(0,0,0,.62) 0%, rgba(0,0,0,.3) 36%, rgba(0,0,0,0) 60%), linear-gradient(0deg, rgba(0,0,0,.7) 0%, rgba(0,0,0,0) 46%), linear-gradient(180deg, rgba(0,0,0,.42) 0%, rgba(0,0,0,0) 24%); }
.cvb .vtag { top: 28.5mm; }
.cve .ob { position: absolute; }
.cvf::after { background: linear-gradient(90deg, rgba(0,0,0,.66) 0%, rgba(0,0,0,.36) 34%, rgba(0,0,0,0) 56%), linear-gradient(0deg, rgba(0,0,0,.5) 0%, rgba(0,0,0,0) 40%), linear-gradient(180deg, rgba(0,0,0,.4) 0%, rgba(0,0,0,0) 24%); } .v3e .fr-t { width: 264mm; } .v3e .fr-p { max-width: 118mm; }
.chips4 { display: grid; grid-template-columns: repeat(4, 61.5mm); column-gap: 6mm; } .chips4 .chip { display: grid; grid-template-columns: 16mm 1fr; height: 22.5mm; padding: 2mm 3mm 2mm 2.5mm; } .chips4 .chip img { width: 16mm; height: 16mm; } .chips4 .chip span { white-space: nowrap; }
"""
def doc(pages, title): return typo(f'<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>')
(OUT / "p3-variants.html").write_text(doc(PAGES, "Obiimy — сторінка 3, варіанти"))     # page 3 alone: a base for mock-ups
FULL = deck.PAGES[:1] + COVERS + deck.PAGES[1:2] + PAGES + deck.PAGES[3:]
print("cover variants:", len(COVERS), "· page 3 variants:", len(PAGES) - 1)
deck.render(FULL, CSS)
