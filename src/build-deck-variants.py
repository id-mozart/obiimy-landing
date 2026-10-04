#!/usr/bin/env python3
"""The HR deck with variant pages inside it, for the client to choose (04.10: «все добавляй в пдф, потом уберём лишнее»):
cover variants right after the cover and variants of page 3 («Що в коробці — і скільки це коштує») right after page 3.
Reuses the deck's helpers, data and CSS (src/build-team-pdf.py renders only when run as a script) and renders the public PDF itself.
When the choice is made: move the chosen layouts into build-team-pdf.py and build the deck with it again."""
import importlib.util, pathlib, subprocess, sys
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

# ── cover variants ──────────────────────────────────────────────────────────────────────────────────
LINE = f'<p class="folio"><span>Пакування й наліпка з вашим логотипом — безкоштовно</span><span><a href="{deck.PHONE_HREF}">{deck.PHONE}</a> · <a href="{deck.TG}">Telegram @OBIIMY_sales</a></span></p>'
CAP = deck.COVER_CAP
H1 = "Подарунки<br>для команди,<br><i>які носять</i>"
def vtag(t): return f'<p class="vtag r cap">Обкладинка · {t}</p>'
COVERS = []
# B · another frame of the same shoot: a portrait with the scarf on the wrist
COVERS.append(f'''<section class="pg frame cv cvb">{pic("photo/solo/krok-44-3.webp", 297, 210, "50% 58%", "bg", hi=True, once=False)}<img src="brand/logo-white.png" class="logo" alt="Obiimy">{vtag("варіант B — портрет")}
<div class="fr-t"><p class="cap">{CAP}</p><h1 class="h54">{H1}</h1>
<div class="chip">{cut("krok-44-1", 13)}<div><span>Чотири подарунки · на людину</span><em>від 1 600 до 3 600 грн</em></div></div></div>{LINE}</section>''')
# C · paper and a photograph: the title on paper, the portrait takes the right half
COVERS.append(f'''<section class="pg cv cvc"><figure class="cph">{pic("photo/solo/puls-44-4.webp", 148.5, 210, "52% 50%", hi=True, once=False)}</figure>{vtag("варіант C — папір і портрет")}
<img src="brand/logo-ink.png" class="logo" alt="Obiimy">
<div class="cvt"><p class="cap">{CAP}</p><h1 class="h54">{H1}</h1>
<p class="h13">Чотири подарунки — від 1 600 до 3 600 грн на людину</p></div>{LINE}</section>''')
# D · three portraits — a team — and the title on a paper band
TRI = [("photo/solo/avantiura-88-5.webp", "62% 50%"), ("photo/solo/puls-44-4.webp", "50% 50%"), ("photo/solo/krok-44-3.webp", "50% 50%")]
COVERS.append(f'''<section class="pg cv cvd"><div class="tri">{"".join(pic(f, 97, 129, ps, hi=True, once=False) for f, ps in TRI)}</div>{vtag("варіант D — три портрети")}
<img src="brand/logo-ink.png" class="logo" alt="Obiimy">
<div class="cvt"><p class="cap">{CAP}</p><h1 class="h54">Подарунки для команди,<br><i>які носять</i></h1></div>
<p class="h13 cvp">Чотири подарунки<br>від 1 600 до 3 600 грн на людину</p>{LINE}</section>''')
# E · the things themselves on paper, as in a gift guide
OBJ = [("krok-tw-1", 74, 163.5, 22.5, 0), ("duo-hratsiia-ring", 60, 219, 33, 0), ("maskscr-litnie-pole", 60, 157.5, 115.5, 0), ("pair-zolote", 64, 216, 112.5, 0)]   # cut-out, size mm, x, y, rotation
COVERS.append(f'''<section class="pg cv cve">{"".join(f'<div class="ob" style="left:{x}mm;top:{y}mm;transform:rotate({r}deg)">{cut(c, mm, fix=True)}</div>' for c, mm, x, y, r in OBJ)}{vtag("варіант E — речі на папері")}
<img src="brand/logo-ink.png" class="logo" alt="Obiimy">
<div class="cvt"><p class="cap">{CAP}</p><h1 class="h54">{H1}</h1>
<p class="h13">Чотири подарунки — від 1 600 до 3 600 грн на людину</p></div>{LINE}</section>''')
# F · a wide scene by the sea, the scarf worn as a belt
COVERS.append(f'''<section class="pg frame cv cvf">{pic("photo/solo/avantiura-88-2.webp", 297, 210, "50% 30%", "bg", hi=True, once=False)}<img src="brand/logo-white.png" class="logo" alt="Obiimy">{vtag("варіант F — сцена")}
<div class="fr-t"><p class="cap">{CAP}</p><h1 class="h54">{H1}</h1>
<div class="chip">{cut("avantiura-88-1", 13)}<div><span>Чотири подарунки · на людину</span><em>від 1 600 до 3 600 грн</em></div></div></div>{LINE}</section>''')

CSS = deck.CSS + """
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
.vtag { position: absolute; left: 16.5mm; top: 16.5mm; z-index: 2; } .vtag.r { left: auto; right: 16.5mm; top: 19.5mm; z-index: 3; }
/* cover variants */
.cv .logo { position: absolute; left: 16.5mm; top: 16.5mm; height: 9mm; width: 42.4mm; z-index: 2; } .cv .folio { z-index: 2; }
.cvc .cph, .cph { position: absolute; right: 0; top: 0; width: 148.5mm; height: 210mm; } .cph img { width: 100%; height: 100%; object-fit: cover; }
.cvt { position: absolute; left: 16.5mm; bottom: 22.5mm; width: 126mm; z-index: 2; } .cvt .cap { margin-bottom: 3mm; } .cvt h1 { margin-bottom: 6mm; }
.cvc .vtag, .cve .vtag { color: #6E6A63; } .cvc .vtag { color: rgba(255,255,255,.8); }
.cvc .folio span:last-child { color: rgba(255,255,255,.8); }
.tri { position: absolute; left: 0; right: 0; top: 0; height: 129mm; display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; } .tri img { width: 100%; height: 129mm; object-fit: cover; }
.cvd .cvt { width: 264mm; bottom: 21mm; } .cvd .cvt h1 { margin-bottom: 0; } .cvd .cvp { position: absolute; right: 16.5mm; bottom: 24mm; text-align: right; color: #4A4A47; }
.cvd .logo { left: auto; right: 16.5mm; top: 141mm; } .cvd .vtag { color: rgba(255,255,255,.85); }
.cvb .fr-t { left: auto; right: 16.5mm; width: 130mm; text-align: right; } .cvb .chip { text-align: left; }
.cvb::after { background: linear-gradient(270deg, rgba(0,0,0,.62) 0%, rgba(0,0,0,.3) 36%, rgba(0,0,0,0) 60%), linear-gradient(0deg, rgba(0,0,0,.7) 0%, rgba(0,0,0,0) 46%), linear-gradient(180deg, rgba(0,0,0,.42) 0%, rgba(0,0,0,0) 24%); }
.cvb .vtag { top: 28.5mm; }
.cve .ob { position: absolute; } .cve .ob img { filter: drop-shadow(0 3mm 4mm rgba(0,0,0,.18)); }
.cvf::after { background: linear-gradient(90deg, rgba(0,0,0,.66) 0%, rgba(0,0,0,.36) 34%, rgba(0,0,0,0) 56%), linear-gradient(0deg, rgba(0,0,0,.5) 0%, rgba(0,0,0,0) 40%), linear-gradient(180deg, rgba(0,0,0,.4) 0%, rgba(0,0,0,0) 24%); } .v3e .fr-t { width: 264mm; } .v3e .fr-p { max-width: 118mm; }
.chips4 { display: grid; grid-template-columns: repeat(4, 61.5mm); column-gap: 6mm; } .chips4 .chip { display: grid; grid-template-columns: 16mm 1fr; height: 22.5mm; padding: 2mm 3mm 2mm 2.5mm; } .chips4 .chip img { width: 16mm; height: 16mm; } .chips4 .chip span { white-space: nowrap; }
"""
def doc(pages, title): return typo(f'<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>')
(OUT / "p3-variants.html").write_text(doc(PAGES, "Obiimy — сторінка 3, варіанти"))     # page 3 alone: a base for mock-ups
FULL = deck.PAGES[:1] + COVERS + deck.PAGES[1:2] + PAGES + deck.PAGES[3:]
print("cover variants:", len(COVERS), "· page 3 variants:", len(PAGES) - 1)
deck.render(FULL, CSS)
