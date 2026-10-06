#!/usr/bin/env python3
"""HR deck v2 (06.10.2026) — a second version from scratch, shorter and in the buyer's order: seven pages.
1 cover (the client's brief: four products on models, «подаруй» + the logo, the brand yellow) · 2 why silk, who we are ·
3 the four gifts with prices and budgets · 4 how it is worn · 5 packaging and your logo · 6 how to order, terms, a sample quote · 7 contacts.
Reuses the helpers, data and CSS of src/build-team-pdf.py (pages 5–7 are its pages 8, 14, 15 renumbered) and renders
obiimy-podarunky-dlia-komandy-v2.pdf; manual edits of the editor go to src/deck-edits-v2.json."""
import importlib.util, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent; OUT = ROOT.parent
sys.path.insert(0, str(ROOT))
_spec = importlib.util.spec_from_file_location("deck", ROOT / "build-team-pdf.py"); deck = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(deck)
pic, cut, money, GIFTS, typo, INTRO = deck.pic, deck.cut, deck.money, deck.GIFTS, deck.typo, deck.INTRO
PAGES = []; TERMS_P = 6
deck.USED.clear()   # frames of the v4 pages built at import do not count: only what v2 prints
def page(html, cls, folio=True, short=False):
    n = len(PAGES) + 1; tg = "@OBIIMY_sales" if short else "Telegram @OBIIMY_sales"
    f = (f'<p class="folio"><span><i class="fq">Запит: </i><a href="{deck.PHONE_HREF}">{deck.PHONE}</a> · <a href="{deck.TG}">{tg}</a></span><span>{n:02d}</span></p>' if folio else "")
    PAGES.append(f'<section class="pg {cls}">{html}{f}</section>')
def rh(section): return f'<p class="rh"><span>{section}</span><span>Obiimy · Подарунки для команди · 2026</span></p>'
def renumber(html, n):   # a page taken from the v4 deck keeps its markup, only the folio number and the «стор.» reference change
    html = re.sub(r'(<p class="folio">.*?<span>)(\d\d)(</span></p>)', lambda m: f"{m.group(1)}{n:02d}{m.group(3)}", html, flags=re.S)
    return re.sub(r"(стор\.[\s  ]*)(\d+)", lambda m: m.group(1) + str(TERMS_P), html)

# ── 1 · cover: the client's brief ────────────────────────────────────────────────────────────────────
FOUR = [("photo/site/tvilli-shovkovyi-probudzhennia-03.jpg", "50% 18%", "твіллі «Пробудження»"), ("photo/site/mask-nizhnist-03.jpg", "50% 50%", "маска для сну «Ніжність»"),
        ("photo/site/khustka-potsilunok-sontsia-44x44-02.jpg", "50% 50%", "хустка «Поцілунок сонця» 44 × 44"), ("photo/site/khustka-vidnovlennia-88x88-02.jpg", "50% 30%", "хустка «Відновлення» 88 × 88")]
page(f'''<div class="four">{"".join(pic(f, 72, 122, ps) for f, ps, _c in FOUR)}</div>
<div class="cvw-t"><h1 class="h54"><i>подаруй</i> <img src="brand/logo-ink.png" class="cvw-logo" alt="Obiimy"></h1>
<p class="h13 cvw-d">Українські преміальні шовкові аксесуари —<br>корпоративні подарунки для команди, партнерів і клієнтів.</p>
<div class="cvw-r"><p class="cap">Корпоративні подарунки · 2026</p><p class="h13">{deck.COVER_PRICE}</p><p class="t8">На фото — {", ".join(c for _f, _p, c in FOUR)}.</p></div></div>
{deck.COVER_LINE}''', "cv cvw", folio=False)

# ── 2 · why silk, who we are (split, photo left) ─────────────────────────────────────────────────────
WHY = [("Без розмірів і примірок", "Хустка, твіллі чи маска для сну підходять кожному — не треба збирати розміри, як для одягу."),
       ("Кожному — свій принт", "38 принтів твіллі, п’ять авторських колекцій. Один подарунок на всю команду — і кожному свій."),
       ("Шовк, який відчувають", "100% натуральний італійський шовк. Кутики кожної хустки кравчині обробляють вручну."),
       ("Український бренд з історією", "Заснований під час війни, виробництво повністю українське. Частина коштів від колекції «Співоча душа» — на гнізда для сиворакші з Червоної книги.")]
args = "".join(f'<div class="arg"><b class="num">0{i + 1}</b><div><h3 class="h13">{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(WHY))
page(f'''<figure class="ph">{pic("photo/site/khustka-z-chystoho-lysta-65x65-02.jpg", 148.5, 210, "50% 20%")}<figcaption class="t8">На фото — хустка «З чистого листа» 65 × 65</figcaption></figure>
<div class="panel"><p class="cap">Хто ми — і чому шовк</p><h2 class="h28">Подарунок, що носять,<br><i>а не кладуть у шухляду</i></h2>
<p class="proof">{INTRO}</p>
<div class="args">{args}</div></div>''', "split l shade")

# ── 3 · the four gifts: a row on paper, price and budgets under each ─────────────────────────────────
OBJ = ["krok-tw-1", "duo-hratsiia-ring", "box-maskscr-litnie-pole", "box-sctw-spokusa"]; OBJ_MM = [58, 54, 58, 56]
CAPT = ["твіллі «Сміливий крок»", "хустка «Грація» 44 × 44 і кільце «Н стиль»", "набір «Літнє поле»", "набір «Спокуса»"]
def b3(p, hi):
    def val(k): return f"<span>від {money(p * k)}</span><span>до {money(hi * k)}</span>" if hi else f"<span>{money(p * k)}</span>"
    return '<div class="ob3">' + "".join(f'<div><span class="t8">{k} людей</span>{val(k)}</div>' for k in (20, 50, 100)) + "</div>"
def col(i, G):
    lb, n, d, p, hi, c = G
    note = f"до {money(hi)} грн — двосторонній друк" if hi else "&nbsp;"
    ring = cut("ring-in-use", 14, cls="rd", fix=True) if i == 1 else ""
    return (f'<article class="oc"><div class="ob">{cut(OBJ[i], OBJ_MM[i], fix=True)}{ring}</div><p class="cap">0{i + 1} · {lb}</p><h3 class="h13">{n}</h3><p class="d">{d}</p>'
            f'<p class="pr h28">{"<small>від</small> " if hi else ""}{money(p)} <small>грн</small></p><p class="t8 nt">{note}</p>{b3(p, hi)}</article>')
page(f'''{rh("Чотири подарунки")}<div class="sheet offer">
<div class="hd"><h2 class="h28">Що даруємо — <i>і скільки це коштує</i></h2><p>Базові роздрібні ціни obiimy.world на людину, без акцій сайту, жовтень 2026; бюджети команди — у гривнях. Пакування й наліпка з вашим логотипом — безкоштовно.</p></div>
<div class="ocols">{"".join(col(i, G) for i, G in enumerate(GIFTS))}</div>
<p class="t8 end">На вирізках — {"; ".join(CAPT)}. Тим, хто не носить аксесуари, — маска для сну (2 700 грн), закладка для книги (800 грн) або сертифікат Obiimy на 1 000–4 000 грн; до 1 000 грн на людину — резинка, закладка, сертифікат. Усе — в одному розрахунку; приклад — на стор. {TERMS_P}.</p></div>''', "paper")

# ── 4 · how it is worn: six real frames, the formats and prices on a paper panel ─────────────────────
W6 = [("Твіллі у волоссі", "photo/site/tvilli-shovkovyi-sokovyti-spohady-06.jpg", "50% 0%"), ("Твіллі краваткою", "photo/site/tvilli-shovkovyi-pidnesennia-02.jpg", "50% 8%"), ("Хустка на шиї", "photo/site/khustka-potsilunok-sontsia-44x44-03.jpg", "50% 50%"),
      ("Поясом", "photo/site/khustka-hratsiia-65x65-02.jpg", "50% 42%"), ("Пов’язкою", "photo/site/khustka-shchyri-pochuttia-44x44-02.jpg", "50% 20%"), ("На плечах", "photo/site/khustka-vidnovlennia-88x88-04.jpg", "50% 25%")]
tiles = "".join(f'<figure class="w6">{pic(f, 61.5, 103.5, ps)}<figcaption class="h28"><i>{n}</i></figcaption></figure>' for n, f, ps in W6)
SZ3 = [("flat-smilyvist-44x44", 22, "44 × 44", "подарунки 02 і 04"), ("flat-rankova-kava-65x65", 32, "65 × 65", "від 3 200 грн"), ("flat-kolo-sontsia-88x88", 44, "88 × 88", "від 4 400 грн")]
sizes3 = "".join(f'<figure>{cut(c, mm, fix=True)}<figcaption><b class="h13">{n}</b><span class="t8">{pz}</span></figcaption></figure>' for c, mm, n, pz in SZ3)
page(f'''<div class="panel"><p class="cap">Як це носять</p><h2 class="h28">Одна річ —<br><i>щодня інакше</i></h2>
<p class="lead">Твіллі носять у волоссі, на шиї, краваткою й на сумці; хустку — на шиї, поясом, пов’язкою чи на плечах. Один подарунок — і кожному свій спосіб.</p>
<div class="sz3">{sizes3}</div>
<p class="t8 end">Три формати хусток: 44 × 44 — у подарунках 02 і 04; більші — за запитом, ціни роздрібні obiimy.world. На фото — «Соковиті спогади», «Піднесення», «Поцілунок сонця», «Грація», «Щирі почуття», «Відновлення».</p></div>
<div class="w6g">{tiles}</div>''', "ways6", short=True)

# ── 5–7 · packaging and the logo, how to order, contacts — the v4 pages, renumbered ──────────────────
for src_i in (7, 13):
    PAGES.append(renumber(deck.PAGES[src_i], len(PAGES) + 1))
PAGES.append(deck.PAGES[14].replace('</figure>', '<figcaption class="t8 pc">На фото — хустка «Піднесення» 44 × 44</figcaption></figure>', 1)
                                  .replace(f'<a href="{deck.LANDING}">Сторінка для команд із формою запиту</a>', f'<a href="{deck.LANDING}">Сторінка для команд: {deck.LANDING.replace("https://", "")}</a>'))

CSS = deck.CSS + """
/* v2 · cover on the brand yellow */
.pg.cvw { background: #FDD31A; color: #141414; } .cvw .four { position: absolute; left: 0; right: 0; top: 0; height: 122mm; display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; } .cvw .four img { width: 100%; height: 122mm; object-fit: cover; }
.cvw-t { position: absolute; left: 16.5mm; right: 16.5mm; top: 139mm; z-index: 2; } .cvw-t h1 { white-space: nowrap; margin-bottom: 7.5mm; font-size: 58pt; line-height: 58pt; } .cvw-t h1 i { font-style: italic; color: #141414; }
.cvw-logo { display: inline-block; height: 15.6mm; width: auto; vertical-align: baseline; margin-left: 0; position: relative; top: .6mm; }
.cvw-d { color: #141414; } .cvw-r { position: absolute; right: 0; top: 0; width: 106.5mm; text-align: right; } .cvw-r .cap { margin-bottom: 3mm; padding-top: 1.6mm; } .cvw-r .h13 { margin-bottom: 1.5mm; } .cvw-r .t8 { color: #141414; margin-top: 8mm; }
.cvw .folio, .cvw .cap { color: #141414; }
.last .ph .pc { position: absolute; left: 16.5mm; bottom: 10.05mm; z-index: 2; color: #E7D9A6; } .last .ph::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 40mm; background: linear-gradient(0deg, rgba(0,0,0,.6), rgba(0,0,0,0)); }
.ways6 .sz3 { margin-top: 12mm; } .ways6 .w6::after { inset: 46% 0 0; background: linear-gradient(0deg, rgba(0,0,0,.86) 0%, rgba(0,0,0,.5) 42%, rgba(0,0,0,0) 100%); }
/* v2 · the offer as four columns */
.offer .hd { margin-bottom: 4.5mm; } .ocols { display: grid; grid-template-columns: repeat(4, 61.5mm); column-gap: 6mm; }
.ob { position: relative; height: 60mm; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 3mm; margin-bottom: 3mm; border-bottom: .5pt solid #141414; } .ob img { filter: drop-shadow(0 2mm 2.5mm rgba(0,0,0,.16)); }
.ob .rd { position: absolute; right: 0; bottom: 3mm; border-radius: 50%; box-shadow: 0 0 0 .5pt #C9C6C0; filter: none; }
.oc .cap { white-space: nowrap; letter-spacing: .13em; margin-bottom: .75mm; } .oc h3 { white-space: nowrap; margin-bottom: 1.5mm; } .oc .d { color: #4A4A47; min-height: 13.5mm; margin-bottom: 1.5mm; }
.oc .pr { white-space: nowrap; } .oc .pr small { color: #8E8A84; font-style: italic; } .oc .nt { color: #6E6A63; margin: .75mm 0 2.25mm; }
.ob3 { display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 3mm; border-top: .35pt solid #C9C6C0; padding-top: 1.5mm; font-variant-numeric: lining-nums tabular-nums; font-size: 8pt; line-height: 3.75mm; } .ob3 span { display: block; white-space: nowrap; }
.offer .end { margin-top: auto; }
"""
PIDS = ["cover", "why", "offer", "ways", "logo", "terms", "contacts"]
if __name__ == "__main__":
    deck.render(PAGES, CSS, PIDS, builder="src/build-team-pdf-v2.py", out_html=OUT / "team-deck-v2.html", out_pdf=OUT / "obiimy-podarunky-dlia-komandy-v2.pdf",
                shots=OUT / "review" / "pp" / "team" / "deck-v2", edits_file=OUT / "src" / "deck-edits-v2.json", pages_file=OUT / "review" / "deck-editor-pages-v2.json")
