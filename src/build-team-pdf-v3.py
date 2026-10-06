#!/usr/bin/env python3
"""HR deck v3 (06.10.2026) — a third version: six pages, each answers one question of a cold buyer.
1 cover · 2 «Що подарувати команді, щоб носили?» (one photograph, three answers) · 3 «Скільки це коштує?» (four posters on models,
price per person, 50 people) · 4 «У чому це прийде — і де ваш логотип?» · 5 «Як замовити?» (steps, terms, a sample quote) · 6 contacts.
Reuses the helpers, data and CSS of src/build-team-pdf.py; renders obiimy-podarunky-dlia-komandy-v3.pdf."""
import importlib.util, pathlib, re, sys
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent; OUT = ROOT.parent
sys.path.insert(0, str(ROOT))
from imgs import wide
_spec = importlib.util.spec_from_file_location("deck", ROOT / "build-team-pdf.py"); deck = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(deck)
pic, cut, money, GIFTS, INTRO, ASK = deck.pic, deck.cut, deck.money, deck.GIFTS, deck.INTRO, deck.ASK
PAGES = []; TERMS_P = 5
deck.USED.clear()
def page(html, cls, folio=True, short=False):
    n = len(PAGES) + 1; tg = "@OBIIMY_sales" if short else "Telegram @OBIIMY_sales"
    f = (f'<p class="folio"><span><i class="fq">Запит: </i><a href="{deck.PHONE_HREF}">{deck.PHONE}</a> · <a href="{deck.TG}">{tg}</a></span><span>{n:02d}</span></p>' if folio else "")
    PAGES.append(f'<section class="pg {cls}">{html}{f}</section>')
def rh(section): return f'<p class="rh"><span>{section}</span><span>Obiimy · Подарунки для команди · 2026</span></p>'
def renumber(html, n):
    html = re.sub(r'(<p class="folio">.*?<span>)(\d\d)(</span></p>)', lambda m: f"{m.group(1)}{n:02d}{m.group(3)}", html, flags=re.S)
    return re.sub(r"(стор\.[\s  ]*)(\d+)", lambda m: m.group(1) + str(TERMS_P), html)

# ── 1 · cover (the client's brief) ───────────────────────────────────────────────────────────────────
FOUR = [("photo/site/tvilli-shovkovyi-probudzhennia-03.jpg", "50% 18%", "твіллі «Пробудження»"), ("photo/site/mask-nizhnist-03.jpg", "50% 50%", "маска для сну «Ніжність»"),
        ("photo/site/khustka-potsilunok-sontsia-44x44-02.jpg", "50% 50%", "хустка «Поцілунок сонця» 44 × 44"), ("photo/site/khustka-vidnovlennia-88x88-02.jpg", "50% 30%", "хустка «Відновлення» 88 × 88")]
page(f'''<div class="four">{"".join(pic(f, 72, 122, ps) for f, ps, _c in FOUR)}</div>
<div class="cvw-t"><h1 class="h54"><i>подаруй</i> <img src="brand/logo-ink.png" class="cvw-logo" alt="Obiimy"></h1>
<p class="h13 cvw-d">Українські преміальні шовкові аксесуари —<br>корпоративні подарунки для команди, партнерів і клієнтів.</p>
<div class="cvw-r"><p class="cap">Корпоративні подарунки · 2026</p><p class="h13">{deck.COVER_PRICE}</p><p class="t8">На фото — {", ".join(c for _f, _p, c in FOUR)}.</p></div></div>
{deck.COVER_LINE}''', "cv cvw", folio=False)

# ── 2 · the question: one photograph to the edge, three answers ──────────────────────────────────────
ANS = [("Одного розміру", "Хустка, твіллі чи маска для сну підходять кожному — без розмірів і примірок."),
       ("Кожному — свій принт", "38 принтів твіллі, п’ять авторських колекцій: один подарунок на всіх — і кожному свій."),
       ("Шовк, який відчувають", "100% натуральний італійський шовк, кутики обробляють вручну. Український бренд, заснований під час війни; частина коштів від колекції «Співоча душа» — на гнізда для сиворакші.")]
ans = "".join(f'<div class="an"><b class="num">0{i + 1}</b><div><h3 class="h13">{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(ANS))
page(f'''{pic(wide("photo/site/khustka-vpevnenist-44x44-04.jpg", ext=1120, bottom=1500, patch=(20, 40, 160, 300)), 297, 210, "100% 20%", "bg")}
<div class="q2"><p class="cap">Питання перше</p><h1 class="h40">Що подарувати<br>команді, щоб носили,<br><i>а не клали в шухляду?</i></h1>
<p class="fr-p">{INTRO}</p><div class="ans">{ans}</div><p class="t8 pc">На фото — хустка «Впевненість»</p></div>''', "frame dark q")

# ── 3 · the price: four posters on models (the page-3 variant B of the full deck, trimmed) ──────────
POSTER = [("photo/site/tvilli-shovkovyi-pidnesennia-02.jpg", (0.05, 0.0, 0.95, 0.80), 70, "Шовкова<br>твіллі", "Стрічка 84 × 5 см, 38 принтів", "твіллі «Піднесення»"),
          ("photo/site/khustka-potsilunok-sontsia-44x44-03.jpg", (0.103, 0.03, 0.897, 1.0), 60, "Хустка<br>й кільце", "Хустка 44 × 44 і кільце Gold", "«Поцілунок сонця» 44 × 44"),
          ("photo/site/set-ta-rezynka-litnie-pole-04.jpg", (0.135, 0.12, 0.855, 1.10), 73, "Маска<br>й резинка", "Маска для сну й резинка, 8 принтів", "набір «Літнє поле»"),
          ("photo/site/set-tvilli-845-ta-khustky-4444-natkhne-02.jpg", (-0.026, 0.08, 1.026, 0.938), 58, "Хустка<br>й твіллі", "Хустка 44 × 44 і твіллі в коробці", "набір «Натхнення»")]
ADD = {1: ("ring-in-use", 19.5, "rnd")}
def frame_b(f, win):
    q = pathlib.Path(f); srcp = OUT / f; W, H = Image.open(srcp).size
    L, R, B = [round(max(0, v) * n) + (2 if v > 0 else 0) for v, n in ((-win[0], W), (win[2] - 1, W), (win[3] - 1, H))]
    if L or R or B:
        from PIL import ImageFilter, ImageOps
        ext = deck.LB / f"{q.stem}-ext{L}-{R}-{B}.jpg"
        if not ext.exists() or ext.stat().st_mtime < srcp.stat().st_mtime:
            im = Image.open(srcp).convert("RGB"); out = Image.new("RGB", (W + L + R, H + B)); out.paste(im, (L, 0))
            if L: out.paste(im.crop((0, 0, 6, H)).resize((1, H), Image.BOX).resize((L, H)).filter(ImageFilter.GaussianBlur(4)), (0, 0))
            if R: out.paste(im.crop((W - 6, 0, W, H)).resize((1, H), Image.BOX).resize((R, H)).filter(ImageFilter.GaussianBlur(4)), (L + W, 0))
            if B: out.paste(ImageOps.flip(out.crop((0, H - B, W + L + R, H))).filter(ImageFilter.GaussianBlur(W / 150)), (0, H))
            out.save(ext, quality=92)
        f = str(ext.relative_to(OUT))
    box = (round(win[0] * W) + L, round(win[1] * H), round(win[2] * W) + L, round(win[3] * H)); hb = round(61.5 * (box[3] - box[1]) / (box[2] - box[0]), 1)
    return pic(f, 61.5, hb, box=box), hb
def col_b(i, G):
    lb, n, d, p, hi, c = G; f, win, fa, name, what, capt = POSTER[i]
    img, hb = frame_b(f, win); fc = hb - .5
    fade = "linear-gradient(180deg," + ",".join(f"rgba(20,17,14,{al}) {fa + (fc - fa) * t:.1f}mm" for t, al in ((0, 0), (.15, .06), (.35, .3), (.55, .62), (.75, .86), (.9, .96), (1, 1))) + ")"
    team = f"{money(p * 50)}–{money(hi * 50)}" if hi else money(p * 50); rng = f"{money(p)}–{money(hi)}" if hi else money(p)
    add = cut(ADD[i][0], ADD[i][1], cls="add " + ADD[i][2], fix=True) if i in ADD else ""
    lb = lb.replace("Тим, хто носить аксесуари", "Хто носить аксесуари")
    return (f'<figure class="po"><div class="ph" style="height:{hb}mm">{img}<i class="fd" style="background:{fade}"></i></div>{add}'
            f'<figcaption><p class="cap">0{i + 1} · {lb}</p><div class="po-t"><b class="h28"><i>{name}</i></b></div><span class="t8 wh">{what}</span>'
            f'<p class="pp h28">{rng}</p><span class="t8">грн на людину</span><span class="t8">50 людей — {team} грн</span><span class="t8 pf">На фото — {capt}</span></figcaption></figure>')
page(f'''<div class="sh"><div><p class="cap">Питання друге</p><h2 class="h28">Скільки це коштує — <i>на людину й команду?</i></h2></div>
<p>Базові роздрібні ціни obiimy.world, жовтень 2026; верхня ціна — принти з двостороннім друком. Пакування й наліпка з вашим логотипом — безкоштовно. Тим, хто не носить аксесуари, — маска для сну (2 700 грн) або сертифікат на 1 000–4 000 грн; до 1 000 грн — резинка (700) чи закладка (800). Приклад розрахунку — на стор. {TERMS_P}.</p></div>
<div class="posters">{"".join(col_b(i, G) for i, G in enumerate(GIFTS))}</div><div class="plinth"></div>''', "v3b")

# ── 4 · the box and the logo ─────────────────────────────────────────────────────────────────────────
ask = "".join(f'<div class="arg"><b class="num">0{i + 1}</b><div><h3 class="h13">{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(ASK))
_f, _pad, _h = deck.cutsh("box-book-makiv", 140.0, layers=((3.0, 4.0, 0.18),), tint=(0, 0, 0))
page(f'''{rh("Питання третє")}<figure class="boxcut" style="left:{6 - _pad:.1f}mm;top:{22 - _pad:.1f}mm;width:{140 + 2 * _pad:.1f}mm"><img src="review/lb/{_f}" alt=""></figure>
<div class="sheet logo2"><h2 class="h28">У чому це прийде —<br><i>і де ваш логотип?</i></h2>
<div class="free"><p class="cap">У кожному корпоративному замовленні</p><p class="h28">Безкоштовно</p><p>Подарункове пакування кожної речі й наліпка з логотипом вашої компанії всередині. Від вас — логотип. Пакування кожного подарунка покажемо в добірці.</p></div>
<p class="cap req">За запитом</p><div class="args">{ask}</div>
<p class="t8 end">Що встигаємо до вашої дати й скільки це коштує — пишемо в розрахунку. На фото — коробка-книжка набору «Маків цвіт»: твіллі й резинка, 2 200 грн.</p></div>''', "paper")

# ── 5–6 · how to order, contacts — the v4 pages ──────────────────────────────────────────────────────
PAGES.append(renumber(deck.PAGES[13].replace('<p class="rh"><span>Умови й замовлення</span>', '<p class="rh"><span>Питання четверте</span>'), 5))
PAGES.append(deck.PAGES[14].replace('</figure>', '<figcaption class="t8 pc">На фото — хустка «Піднесення» 44 × 44</figcaption></figure>', 1)
             .replace(f'<a href="{deck.LANDING}">Сторінка для команд із формою запиту</a>', f'<a href="{deck.LANDING}">Сторінка для команд: {deck.LANDING.replace("https://", "")}</a>'))

POSTER_CSS = pathlib.Path("/private/tmp/claude-501/-Users-ivan-obiimy/9336a79c-fcae-4a0e-a194-062adfde257a/scratchpad/poster.css").read_text(encoding="utf-8") if False else """
.v3b { background: #F1EFEA; } .v3b .sh { grid-template-columns: 1fr 106.5mm; } .v3b .sh > p { color: #4A4A47; padding-top: 7.5mm; } .v3b .sh .cap { color: #6E6A63; } .v3b .sh h2 { white-space: normal; }
.posters { position: absolute; left: 16.5mm; right: 16.5mm; top: 53mm; bottom: 17.5mm; display: grid; grid-template-columns: repeat(4, 61.5mm); column-gap: 6mm; }
.plinth { position: absolute; left: 0; right: 0; bottom: 0; height: 17.6mm; background: #14110E; }
.po figcaption { left: 4.5mm; right: 3mm; }
.po { position: relative; overflow: hidden; background: #14110E; }
.po .ph { position: absolute; left: 0; right: 0; top: 0; } .po .ph img { display: block; width: 100%; height: 100%; object-fit: cover; }
.po .fd { position: absolute; left: 0; right: 0; top: 0; bottom: -.5mm; }
.po figcaption { position: absolute; left: 6mm; right: 4.5mm; bottom: 3.5mm; z-index: 2; color: #fff; }
.po .cap { color: rgba(255,255,255,.82); letter-spacing: .13em; white-space: nowrap; margin-bottom: 1.5mm; }
.po-t { position: relative; margin-bottom: 1.5mm; } .po-t b { display: block; color: #fff; }
.po .add { position: absolute; right: 3mm; bottom: 63mm; z-index: 2; } .po .add.rnd { border-radius: 50%; box-shadow: 0 0 0 .5pt rgba(231,217,166,.5); }
.po .pp { color: #E7D9A6; white-space: nowrap; margin-bottom: 1.5mm; font-size: 26pt; line-height: 28pt; } .po .pp small { font: 400 9.5pt/30pt Tenor, sans-serif; letter-spacing: 0; color: rgba(231,217,166,.9); }
.po .t8 { display: block; color: rgba(255,255,255,.88); white-space: nowrap; } .po .t8.pf { overflow: hidden; text-overflow: clip; } .po .t8.wh { margin-bottom: 2.5mm; } .po .t8.pf { color: rgba(255,255,255,.62); }
.v3b .folio { color: rgba(255,255,255,.7); z-index: 3; }
"""
CSS = deck.CSS + """
/* v3 · cover on the brand yellow */
.pg.cvw { background: #FDD31A; color: #141414; } .cvw .four { position: absolute; left: 0; right: 0; top: 0; height: 122mm; display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; } .cvw .four img { width: 100%; height: 122mm; object-fit: cover; }
.cvw-t { position: absolute; left: 16.5mm; right: 16.5mm; top: 139mm; z-index: 2; } .cvw-t h1 { white-space: nowrap; margin-bottom: 7.5mm; font-size: 58pt; line-height: 58pt; } .cvw-t h1 i { font-style: italic; color: #141414; }
.cvw-logo { display: inline-block; height: 15.6mm; width: auto; vertical-align: baseline; margin-left: 0; position: relative; top: .6mm; }
.cvw-d { color: #141414; } .cvw-r { position: absolute; right: 0; top: 0; width: 106.5mm; text-align: right; } .cvw-r .cap { margin-bottom: 3mm; padding-top: 1.6mm; } .cvw-r .h13 { margin-bottom: 1.5mm; } .cvw-r .t8 { color: #141414; margin-top: 8mm; }
.cvw .folio, .cvw .cap { color: #141414; }
/* v3 · the question page: text on the extended studio backdrop */
.q::after { background: linear-gradient(90deg, rgba(0,0,0,.74) 0%, rgba(0,0,0,.56) 40%, rgba(0,0,0,0) 60%); }
.q2 { position: absolute; left: 16.5mm; top: 22.5mm; bottom: 19.5mm; width: 150mm; z-index: 2; color: #fff; display: flex; flex-direction: column; } .q2 .cap { margin-bottom: 3.75mm; } .q2 h1 { margin-bottom: 6mm; } .q2 h1 i { color: #E7D9A6; }
.q2 .fr-p { max-width: 118mm; margin: 0 0 4.5mm; } .ans { display: grid; } .an { display: grid; grid-template-columns: 10.5mm 1fr; padding: 3mm 0; border-top: .35pt solid rgba(255,255,255,.3); } .an h3 { margin-bottom: .75mm; } .an p { color: rgba(255,255,255,.86); max-width: 112mm; } .an .num { color: #E7D9A6; }
.q2 .pc { margin-top: auto; color: rgba(255,255,255,.62); }
.last .ph .pc { position: absolute; left: 16.5mm; bottom: 10.05mm; z-index: 2; color: #E7D9A6; } .last .ph::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 40mm; background: linear-gradient(0deg, rgba(0,0,0,.6), rgba(0,0,0,0)); }
""" + POSTER_CSS
PIDS = ["cover", "why", "price", "box", "terms", "contacts"]
if __name__ == "__main__":
    deck.render(PAGES, CSS, PIDS, builder="src/build-team-pdf-v3.py", out_html=OUT / "team-deck-v3.html", out_pdf=OUT / "obiimy-podarunky-dlia-komandy-v3.pdf",
                shots=OUT / "review" / "pp" / "team" / "deck-v3", edits_file=OUT / "src" / "deck-edits-v3.json", pages_file=OUT / "review" / "deck-editor-pages-v3.json")
