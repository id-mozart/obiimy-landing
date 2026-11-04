#!/usr/bin/env python3
"""Two more, deliberately different, versions of the KRAЇNA EDEM × OBIIMY landing (client, 04.11.2026: «ещё пару версий — совсем других»).
Same copy, facts, pictures and registration API as src/build-edem.py:
  edem-shop — a product page, the way a shop shows one item: a gallery with thumbnails on the left, a sticky «buy box» on the right
              (name, the price line — honest: the price is not confirmed, so «повідомимо зареєстрованим»), specification, accordions
              (project, symbols, partners), the registration form as the checkout; white, ink and the print's deep blue;
  edem-book — a leporello book: seven spreads side by side, turned by ordinary vertical scrolling (a tall track with a sticky stage
              that slides the rail horizontally), page numbers and a progress rule; on phones the spreads simply stack.
Output: edem-shop.html, edem-book.html (HIDDEN in build-site: deployed, in the variants bar, not in the hub)."""
import importlib.util, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from imgs import img
_spec = importlib.util.spec_from_file_location("edemv", ROOT / "src" / "build-edem-variants.py"); V = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(V)
MANIFESTO, STORY, SYMBOLS, SPEC, EDEM_P, EDEM_L, OB_P, OB_L, STEPS = V.MANIFESTO, V.STORY, V.SYMBOLS, V.SPEC, V.EDEM_P, V.EDEM_L, V.OB_P, V.OB_L, V.STEPS
PHONE, PHONE_HREF, MAIL, TG = V.PHONE, V.PHONE_HREF, V.MAIL, V.TG
form_html, FORM_CSS, write, spec_rows = V.form_html, V.FORM_CSS, V.write, V.spec_rows

LEAD = "Мистецтво бути ближче. Шовкова хустка за трипільськими мотивами — спільна робота KRAЇNA EDEM та OBIIMY."
SCARF_LEAD = "Хустка тут — більше, ніж аксесуар: мистецьке полотно, що поєднує сучасний дизайн із пам’яттю про давні культури."
GALLERY = [("art-1600", "Принт хустки «Trypillia — The Art of Origins» повністю", "Принт повністю"), ("scarf", "Хустка KRAЇNA EDEM × OBIIMY — шовк, 88 × 88", "Хустка"),
           ("art-center", "Центральний медальйон крупно", "Медальйон"), ("art-pendants", "Гроно підвісок на плетених шнурах", "Підвіски"),
           ("art-corner", "Кут хустки: фігурка, плетені шнури, рамка", "Кут хустки"), ("art-sign", "Підпис OBIIMY × Edem на полотні", "Підпис")]

# ═══ A · SHOP — a product page ════════════════════════════════════════════════════════════════════════════════════════════
SHOP_CSS = """
:root { --ink: #1E1A17; --ink2: #6A625A; --blue: #2E4A6B; --blue2: #E9EEF4; --line: #E6E1D8; --paper: #FFFFFF; --paper2: #F7F4EE; --gold: #B48A3A; --acc: #2E4A6B; --fb: #D9D3C8; --fbg: #FFFFFF; --fink: #1E1A17; }
* { box-sizing: border-box; } html { scroll-behavior: smooth; }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: Montserrat, Arial, sans-serif; font-size: 15px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
img { max-width: 100%; height: auto; display: block; } p { margin: 0; } a { color: inherit; } figure { margin: 0; }
h1, h2, h3 { margin: 0; font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 500; line-height: 1.1; text-wrap: balance; }
.wrap { max-width: 1280px; margin: 0 auto; padding: 0 24px; }
.bar { position: sticky; top: 0; z-index: 20; background: rgba(255,255,255,.92); backdrop-filter: blur(10px); border-bottom: 1px solid var(--line); }
.bar .wrap { display: flex; align-items: center; justify-content: space-between; height: 60px; gap: 20px; }
.bar .brand { font-family: 'Cormorant Garamond', serif; font-size: 20px; letter-spacing: .06em; text-decoration: none; } .bar .brand small { font-family: Montserrat, sans-serif; font-size: 10px; letter-spacing: .22em; text-transform: uppercase; color: var(--ink2); margin-left: 12px; }
.bar nav { display: flex; gap: 22px; font-size: 12px; letter-spacing: .06em; } .bar nav a { text-decoration: none; color: var(--ink2); } .bar nav a:hover { color: var(--ink); } .bar nav a.cta { color: var(--blue); font-weight: 600; }
.crumbs { font-size: 12px; color: var(--ink2); padding: 18px 0 6px; } .crumbs a { text-decoration: none; } .crumbs span { margin: 0 8px; }
.pdp { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, .85fr); gap: clamp(28px, 4vw, 64px); align-items: start; padding: 14px 0 60px; }
.gal .main { position: relative; background: var(--paper2); aspect-ratio: 1; overflow: hidden; } .gal .main img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; opacity: 0; transition: opacity .35s; } .gal .main img.on { opacity: 1; }
.gal .main .tag { position: absolute; left: 14px; top: 14px; padding: 6px 10px; background: #fff; border: 1px solid var(--line); font-size: 10px; letter-spacing: .2em; text-transform: uppercase; color: var(--blue); z-index: 2; }
.gal .thumbs { display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; margin-top: 10px; } .gal .thumbs button { padding: 0; border: 1px solid var(--line); background: var(--paper2); cursor: pointer; aspect-ratio: 1; overflow: hidden; } .gal .thumbs button img { width: 100%; height: 100%; object-fit: cover; } .gal .thumbs button.on { border-color: var(--ink); } .gal .thumbs button:focus-visible { outline: 2px solid var(--blue); }
.gal .cap { margin-top: 10px; font-size: 12px; color: var(--ink2); }
.buy { position: sticky; top: 80px; }
.buy .eyebrow { font-size: 11px; letter-spacing: .22em; text-transform: uppercase; color: var(--blue); font-weight: 600; }
.buy h1 { font-size: clamp(30px, 3vw, 42px); margin-top: 10px; } .buy h1 i { font-style: italic; font-weight: 400; }
.buy .price { margin-top: 18px; padding: 16px 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); display: flex; justify-content: space-between; align-items: baseline; gap: 14px; flex-wrap: wrap; }
.buy .price b { font-family: 'Cormorant Garamond', serif; font-size: 26px; font-weight: 500; } .buy .price span { font-size: 12px; color: var(--ink2); }
.buy .lead { margin-top: 16px; font-size: 15px; color: var(--ink2); }
.buy .btn { width: 100%; justify-content: center; margin-top: 18px; } .btn-main { background: var(--ink); color: #fff; } .btn-main:hover { background: var(--blue); } .btn-line { border-color: var(--ink); color: var(--ink); }
.buy .sub { margin-top: 10px; font-size: 12px; color: var(--ink2); text-align: center; }
.trust { margin-top: 22px; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; } .trust div { padding: 12px; background: var(--paper2); font-size: 11px; line-height: 1.4; letter-spacing: .04em; } .trust b { display: block; font-family: 'Cormorant Garamond', serif; font-size: 20px; font-weight: 500; color: var(--ink); margin-bottom: 2px; }
.spec { margin-top: 24px; } .spec div { display: flex; justify-content: space-between; gap: 20px; padding: 10px 0; border-bottom: 1px solid var(--line); font-size: 13px; } .spec span { color: var(--ink2); } .spec b { font-weight: 600; text-align: right; }
details { border-top: 1px solid var(--line); } details:last-of-type { border-bottom: 1px solid var(--line); } summary { cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; padding: 16px 0; font-size: 13px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; } summary::-webkit-details-marker { display: none; } summary::after { content: "+"; font-family: 'Cormorant Garamond', serif; font-size: 26px; font-weight: 300; color: var(--ink2); } details[open] summary::after { content: "−"; }
details .body { padding: 0 0 22px; color: var(--ink2); font-size: 14px; } details .body p + p { margin-top: 1em; } details .body blockquote { margin: 0 0 14px; font-family: 'Cormorant Garamond', serif; font-size: 22px; line-height: 1.3; color: var(--ink); } details .body b { color: var(--blue); font-weight: 500; }
.syms { display: grid; gap: 12px; } .syms div { display: grid; grid-template-columns: 64px 1fr; gap: 14px; align-items: center; } .syms .pic { width: 64px; height: 64px; background: var(--paper2); display: flex; align-items: center; justify-content: center; } .syms .pic img { max-height: 54px; width: auto; } .syms h3 { font-size: 18px; } .syms p { font-size: 13px; margin-top: 2px; }
.brs { display: grid; gap: 14px; } .brs h3 { font-size: 18px; letter-spacing: .04em; color: var(--ink); } .brs ul { margin: 6px 0 0; padding-left: 16px; }
.strip { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; padding: 0 0 60px; } .strip figure img { width: 100%; height: auto; aspect-ratio: 1; object-fit: cover; background: var(--paper2); } .strip figcaption { margin-top: 8px; font-size: 12px; color: var(--ink2); }
.story { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(28px, 4vw, 64px); align-items: center; padding: 60px 0; border-top: 1px solid var(--line); }
.story h2 { font-size: clamp(30px, 3.4vw, 46px); margin-top: 10px; } .story .text { margin-top: 18px; color: var(--ink2); } .story .text p + p { margin-top: 1em; } .story img { width: 100%; height: auto; }
.reg { background: var(--paper2); padding: clamp(50px, 6vw, 90px) 0; border-top: 1px solid var(--line); }
.reg .wrap { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: clamp(28px, 5vw, 80px); align-items: start; }
.reg h2 { font-size: clamp(30px, 3.6vw, 48px); margin-top: 10px; } .reg .lead { margin-top: 14px; color: var(--ink2); }
.steps { margin-top: 22px; } .steps > div { display: grid; grid-template-columns: 32px 1fr; gap: 10px; padding: 12px 0; border-top: 1px solid var(--line); } .steps h3 { font-size: 18px; } .steps p { font-size: 13px; color: var(--ink2); } .steps i { font-style: normal; font-weight: 600; color: var(--blue); font-size: 12px; padding-top: 4px; }
.contacts { margin-top: 20px; font-size: 13px; color: var(--ink2); } .contacts a { text-decoration: none; border-bottom: 1px solid var(--line); }
.panel { background: #fff; border: 1px solid var(--line); padding: clamp(20px, 3vw, 36px); }
footer { padding: 28px 24px; font-size: 11px; letter-spacing: .06em; text-transform: uppercase; color: var(--ink2); display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; border-top: 1px solid var(--line); } footer a { text-decoration: none; }
.rv { opacity: 1 !important; transform: none !important; }
@media (max-width: 980px) { .pdp, .story, .reg .wrap { grid-template-columns: 1fr; } .buy { position: static; } .bar nav { display: none; } .strip { grid-template-columns: repeat(2, 1fr); } .gal .thumbs { grid-template-columns: repeat(6, 1fr); } }
@media (max-width: 600px) { .trust { grid-template-columns: 1fr 1fr; } }
"""

SHOP_JS = """
  var gal = document.getElementById('gal'); if (gal) { var mains = gal.querySelectorAll('.main img'), tb = gal.querySelectorAll('.thumbs button'), cap = gal.querySelector('.cap');
    tb.forEach(function (b, i) { b.addEventListener('click', function () { mains.forEach(function (m, j) { m.classList.toggle('on', i === j); }); tb.forEach(function (x, j) { x.classList.toggle('on', i === j); x.setAttribute('aria-pressed', i === j ? 'true' : 'false'); }); cap.textContent = b.getAttribute('data-cap'); }); }); }
"""

def shop():
    mains = "".join(img(f"photo/edem/{k}.webp", a, sizes="(max-width: 980px) 92vw, 56vw", lazy=i > 0, eager_priority=i == 0, cls="on" if i == 0 else "") for i, (k, a, c) in enumerate(GALLERY))
    thumbs = "".join(f'<button type="button" class="{"on" if i == 0 else ""}" aria-pressed="{"true" if i == 0 else "false"}" data-cap="{c}" aria-label="{c}">{img(f"photo/edem/{k}.webp", "", sizes="100px")}</button>' for i, (k, a, c) in enumerate(GALLERY))
    syms = "".join(f'<div><div class="pic">{img(f"photo/edem/{k}.webp", a, sizes="64px")}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for k, t, d, a in SYMBOLS)
    body = f'''
<main id="top">
<div class="bar"><div class="wrap"><a class="brand" href="#top">Obiimy<small>× Kraїna Edem</small></a><nav><a href="#about">Про проєкт</a><a href="#symbols">Символи</a><a href="#details">Деталі</a><a href="#story">Історія</a><a class="cta" href="#register">Ранній доступ</a></nav></div></div>
<div class="wrap">
  <p class="crumbs"><a href="#top">Хустки</a><span>/</span><a href="#top">Колаборації</a><span>/</span>Trypillia — The Art of Origins</p>
  <section class="pdp">
    <div class="gal" id="gal">
      <div class="main"><span class="tag">Лімітований випуск · 2026</span>{mains}</div>
      <div class="thumbs">{thumbs}</div>
      <p class="cap">{GALLERY[0][2]}</p>
    </div>
    <aside class="buy">
      <p class="eyebrow">KRAЇNA EDEM × OBIIMY · спільний мистецький проєкт</p>
      <h1>Шовкова хустка <i>«Trypillia — The Art of Origins»</i>, 88 × 88 см</h1>
      <div class="price"><b>Ціна — уточнюємо з партнером</b><span>повідомимо зареєстрованим першими</span></div>
      <p class="lead">{LEAD}</p>
      <a class="btn btn-main" href="#register">Отримати ранній доступ</a>
      <p class="sub">Без передоплати: лише повідомлення про ціну й відкриття продажів.</p>
      <div class="trust"><div><b>100%</b>натуральний шовк</div><div><b>88 × 88</b>см, авторський принт</div><div><b>UA</b>виготовлено в Україні</div></div>
      <div class="spec" id="details">{spec_rows()}</div>
      <div style="margin-top:22px">
        <details id="about" open><summary>Про проєкт</summary><div class="body"><blockquote>{MANIFESTO}</blockquote><p>{SCARF_LEAD}</p></div></details>
        <details id="symbols"><summary>Символи хустки</summary><div class="body"><div class="syms">{syms}</div></div></details>
        <details><summary>Партнери</summary><div class="body brs"><div><h3>KRAЇNA EDEM</h3><p>{EDEM_P}</p><ul>{"".join(f"<li>{x}</li>" for x in EDEM_L)}</ul></div><div><h3>OBIIMY</h3><p>{OB_P}</p><ul>{"".join(f"<li>{x}</li>" for x in OB_L)}</ul></div></div></details>
        <details><summary>Як придбати</summary><div class="body"><div class="steps">{"".join(f"<div><i>0{i + 1}</i><div><h3>{t}</h3><p>{d}</p></div></div>" for i, (t, d) in enumerate(STEPS))}</div></div></details>
      </div>
    </aside>
  </section>
  <div class="strip">{"".join(f'<figure>{img(f"photo/edem/{k}.webp", a, sizes="(max-width: 980px) 46vw, 24vw")}<figcaption>{c}</figcaption></figure>' for k, a, c in GALLERY[2:])}</div>
  <section class="story" id="story">
    <div><p class="eyebrow" style="font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--blue);font-weight:600">Історія, що живе в нас</p><h2>Наше коріння сягає глибини тисячоліть</h2><div class="text">{"".join(f"<p>{t}</p>" for t in STORY)}</div></div>
    <div>{img("photo/edem/figure.webp", "Трипільська фігурка — елемент принту", sizes="(max-width: 980px) 60vw, 30vw", style="max-width:360px;margin:0 auto")}</div>
  </section>
</div>
<section class="reg" id="register"><div class="wrap">
  <div><p class="eyebrow" style="font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--blue);font-weight:600">Ранній доступ</p><h2>Дізнайтеся про ціну й старт продажів першими</h2><p class="lead">Ціну й дату старту підтверджуємо з партнером. Щойно вони відомі — зареєстровані отримують персональне посилання на оплату.</p>
    <div class="steps">{"".join(f"<div><i>0{i + 1}</i><div><h3>{t}</h3><p>{d}</p></div></div>" for i, (t, d) in enumerate(STEPS))}</div>
    <div class="contacts">Питання: <a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="{TG}" target="_blank" rel="noopener">Telegram</a></div></div>
  <div class="panel">{form_html()}</div>
</div></section>
<footer><span>Kraїna Edem × Obiimy · Trypillia — The Art of Origins · 2026</span><span><a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a></span></footer>
</main>'''
    write("edem-shop", SHOP_CSS + FORM_CSS, body, SHOP_JS)

# ═══ B · BOOK — a leporello turned by scrolling ═══════════════════════════════════════════════════════════════════════════
BOOK_CSS = """
:root { --paper: #EFE9DF; --paper2: #F8F4EC; --ink: #2A2017; --ink2: #6B5A48; --blue: #2E4A6B; --gold: #B48A3A; --line: rgba(42,32,23,.16); --acc: #2E4A6B; --fb: rgba(42,32,23,.25); --fbg: #FFFFFF; --fink: #2A2017; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: Montserrat, Arial, sans-serif; font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
img { max-width: 100%; height: auto; display: block; } p { margin: 0; } a { color: inherit; } figure { margin: 0; }
h1, h2, h3 { margin: 0; font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 400; line-height: 1.05; text-wrap: balance; }
.eyebrow { font-size: 11px; font-weight: 600; letter-spacing: .26em; text-transform: uppercase; color: var(--blue); }
.lead { font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(20px, 1.8vw, 26px); font-weight: 300; line-height: 1.4; color: var(--ink2); }
.btn-main { background: var(--ink); color: var(--paper2); } .btn-main:hover { background: var(--blue); } .btn-line { border-color: var(--ink); color: var(--ink); }
.cta { display: flex; flex-wrap: wrap; gap: 12px; }
.track { height: 760vh; position: relative; }
.stage { position: sticky; top: 0; height: 100vh; overflow: hidden; }
.rail { display: flex; height: 100%; will-change: transform; }
.page { flex: 0 0 100vw; height: 100%; position: relative; padding: clamp(60px, 8vh, 90px) clamp(24px, 5vw, 80px) clamp(70px, 9vh, 100px); display: grid; align-items: center; border-right: 1px solid var(--line); overflow: hidden; }
.page .no { position: absolute; left: clamp(24px, 5vw, 80px); bottom: 28px; font-family: 'Cormorant Garamond', serif; font-size: 15px; letter-spacing: .3em; color: var(--ink2); }
.page .run { position: absolute; right: clamp(24px, 5vw, 80px); bottom: 30px; font-size: 10px; letter-spacing: .26em; text-transform: uppercase; color: var(--ink2); }
.page.alt { background: var(--paper2); }
.two { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(28px, 5vw, 90px); align-items: center; max-width: 1240px; margin: 0 auto; width: 100%; }
.cover h1 { font-size: clamp(50px, 6.5vw, 104px); margin-top: 16px; } .cover h1 i { font-style: italic; color: var(--gold); }
.cover .lead { margin-top: 22px; max-width: 24em; } .cover .cta { margin-top: 30px; }
.cover .facts { margin-top: 32px; font-size: 12px; letter-spacing: .12em; text-transform: uppercase; color: var(--ink2); display: flex; flex-wrap: wrap; gap: 8px 22px; } .cover .facts b { color: var(--ink); }
.cover .mock img { width: 100%; max-width: 560px; height: auto; margin: 0 auto; filter: drop-shadow(0 40px 60px rgba(58,42,28,.3)); transform: rotate(-4deg); }
.mani { text-align: center; } .mani blockquote { margin: 0 auto; max-width: 22em; font-family: 'Cormorant Garamond', serif; font-size: clamp(28px, 3.6vw, 56px); line-height: 1.2; font-weight: 300; } .mani b { font-weight: 400; color: var(--blue); } .mani .orn { width: 120px; margin: 0 auto 28px; }
.ph2 { font-size: clamp(34px, 4vw, 62px); margin-top: 12px; } .text { color: var(--ink2); margin-top: 20px; max-height: 52vh; overflow: auto; } .text p + p { margin-top: 1em; }
.fig img { width: 100%; max-height: 72vh; object-fit: contain; }
.sym4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: clamp(20px, 3vw, 48px); max-width: 1240px; margin: 0 auto; width: 100%; } .sym4 .pic { height: 30vh; display: flex; align-items: center; justify-content: center; } .sym4 .pic img { max-height: 100%; width: auto; filter: drop-shadow(0 18px 24px rgba(58,42,28,.2)); } .sym4 .pic.lg img { transform: scale(1.3); }
.sym4 h3 { font-size: 26px; margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--ink); } .sym4 p { margin-top: 8px; font-size: 13px; color: var(--ink2); }
.sym4wrap { width: 100%; } .sym4wrap .eyebrow { display: block; text-align: center; margin-bottom: 6px; } .sym4wrap h2 { text-align: center; font-size: clamp(30px, 3.6vw, 54px); margin-bottom: clamp(20px, 4vh, 44px); }
.print { flex-basis: 130vw; } .print .two { grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); max-width: none; } .print .big img { width: 100%; max-height: 80vh; object-fit: contain; }
.spec div { display: flex; justify-content: space-between; gap: 20px; padding: 10px 0; border-bottom: 1px solid var(--line); font-size: 14px; } .spec span { color: var(--ink2); } .spec b { font-weight: 600; text-align: right; }
.note { margin-top: 14px; font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 19px; color: var(--ink2); }
.brands { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(28px, 4vw, 64px); max-width: 1240px; margin: 0 auto; width: 100%; } .brands article { border-top: 1px solid var(--ink); padding-top: 20px; } .brands h3 { font-size: 30px; letter-spacing: .04em; margin-top: 8px; } .brands p { margin-top: 10px; color: var(--ink2); font-size: 14px; }
.brands ul { margin: 12px 0 0; padding: 0; list-style: none; } .brands li { padding: 8px 0; border-top: 1px solid var(--line); font-size: 13px; color: var(--ink2); }
.reg h2 { font-size: clamp(32px, 3.6vw, 54px); margin-top: 12px; } .reg .lead { margin-top: 14px; }
.steps { margin-top: 20px; } .steps > div { display: grid; grid-template-columns: 40px 1fr; gap: 12px; padding: 10px 0; border-top: 1px solid var(--line); } .steps h3 { font-size: 20px; } .steps p { font-size: 13px; color: var(--ink2); } .steps i { font-family: 'Cormorant Garamond', serif; font-style: normal; font-size: 20px; color: var(--gold); }
.contacts { margin-top: 18px; font-size: 13px; color: var(--ink2); } .contacts a { text-decoration: none; border-bottom: 1px solid var(--line); }
.panel { background: #fff; border: 1px solid var(--line); padding: clamp(18px, 2.4vw, 32px); max-height: 84vh; overflow: auto; }
.prog { position: fixed; left: 0; right: 0; bottom: 0; height: 2px; background: var(--line); z-index: 30; } .prog i { display: block; height: 100%; width: 0; background: var(--blue); }
.pages { position: fixed; left: 50%; transform: translateX(-50%); bottom: 12px; z-index: 30; font-family: 'Cormorant Garamond', serif; font-size: 14px; letter-spacing: .3em; color: var(--ink2); display: flex; gap: 10px; } .pages i { font-style: normal; } .pages i.on { color: var(--ink); }
.hint { position: fixed; right: 20px; top: 50%; transform: translateY(-50%); writing-mode: vertical-rl; font-size: 10px; letter-spacing: .3em; text-transform: uppercase; color: var(--ink2); z-index: 30; transition: opacity .4s; } .hint.off { opacity: 0; }
.vbar { bottom: 22px !important; }
@media (max-width: 980px) { .track { height: auto; } .stage { position: static; height: auto; overflow: visible; } .rail { display: block; transform: none !important; } .page { flex-basis: auto; height: auto; min-height: 0; padding: 60px 24px 70px; border-right: 0; border-bottom: 1px solid var(--line); display: block; } .two, .print .two, .brands { grid-template-columns: 1fr; } .sym4 { grid-template-columns: repeat(2, 1fr); } .sym4 .pic { height: 160px; } .text { max-height: none; overflow: visible; } .panel { max-height: none; overflow: visible; } .fig img, .print .big img { max-height: none; } .prog, .pages, .hint { display: none; } .cover .mock { margin-bottom: 28px; } .vbar { bottom: 10px !important; } }
@media (max-width: 600px) { .sym4 { grid-template-columns: 1fr; } .cta .btn { flex: 1 1 100%; justify-content: center; } }
@media (prefers-reduced-motion: reduce) { .rail { transition: none; } }
"""

BOOK_JS = """
  var track = document.getElementById('track'), rail = document.getElementById('rail'), prog = document.getElementById('prog'), hint = document.getElementById('hint'), pg = [].slice.call(document.querySelectorAll('#pages i'));
  var wide = function () { return window.innerWidth > 980; }, cur = -1;
  function tick() {
    if (!wide()) return;
    var max = track.offsetHeight - window.innerHeight, p = Math.max(0, Math.min(1, (window.scrollY - track.offsetTop) / max));
    var span = rail.scrollWidth - window.innerWidth; rail.style.transform = 'translate3d(' + (-p * span).toFixed(1) + 'px,0,0)';
    prog.style.width = (p * 100).toFixed(2) + '%'; if (hint) hint.classList.toggle('off', p > .04);
    var n = Math.min(pg.length - 1, Math.round(p * (pg.length - 1))); if (n !== cur) { cur = n; pg.forEach(function (e, i) { e.classList.toggle('on', i === n); }); }
  }
  window.addEventListener('scroll', tick, { passive: true }); window.addEventListener('resize', tick); tick();
  document.addEventListener('keydown', function (e) { if (!wide()) return; if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); window.scrollBy({ top: window.innerHeight * 1.1, behavior: 'smooth' }); } if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); window.scrollBy({ top: -window.innerHeight * 1.1, behavior: 'smooth' }); } });
  // anchors inside the rail: scroll the track to the page's share
  [].slice.call(document.querySelectorAll('a[href^="#p"]')).forEach(function (a) { a.addEventListener('click', function (e) { var t = document.getElementById(a.getAttribute('href').slice(1)); if (!t || !wide()) return; e.preventDefault(); var pages = [].slice.call(rail.children), i = pages.indexOf(t); var share = pages.slice(0, i).reduce(function (s, x) { return s + x.offsetWidth; }, 0) / (rail.scrollWidth - window.innerWidth); window.scrollTo({ top: track.offsetTop + share * (track.offsetHeight - window.innerHeight), behavior: 'smooth' }); }); });
"""

def book():
    pages = [("I", "Обкладинка"), ("II", "Маніфест"), ("III", "Історія"), ("IV", "Символи"), ("V", "Хустка"), ("VI", "Партнери"), ("VII", "Як придбати")]
    def foot(i): return f'<span class="no">{pages[i][0]}</span><span class="run">Kraїna Edem × Obiimy · {pages[i][1]}</span>'
    body = f'''
<main id="top">
<div class="prog" aria-hidden="true"><i id="prog"></i></div>
<div class="pages" id="pages" aria-hidden="true">{"".join(f'<i class="{"on" if i == 0 else ""}">{n}</i>' for i, (n, t) in enumerate(pages))}</div>
<p class="hint" id="hint">Гортайте — сторінки перегортаються</p>
<div class="track" id="track"><div class="stage"><div class="rail" id="rail">
  <section class="page cover" id="p1"><div class="two">
    <div><p class="eyebrow">Спільний мистецький проєкт · лімітований випуск 2026</p><h1>Trypillia —<br><i>The Art of Origins</i></h1><p class="lead">{LEAD}</p>
      <div class="cta"><a class="btn btn-main" href="#p7">Отримати ранній доступ</a><a class="btn btn-line" href="#p5">Побачити хустку</a></div>
      <div class="facts"><span><b>88 × 88</b> см</span><span><b>100%</b> шовк</span><span>Обмежений наклад</span><span>Підпис OBIIMY × Edem</span></div></div>
    <div class="mock">{img("photo/edem/scarf.webp", "Хустка KRAЇNA EDEM × OBIIMY «Trypillia — The Art of Origins», 88 × 88", sizes="(max-width: 980px) 90vw, 40vw", lazy=False, eager_priority=True)}</div>
  </div>{foot(0)}</section>
  <section class="page alt mani" id="p2"><div><div class="orn">{img("photo/edem/pendant-round.webp", "", sizes="120px")}</div><blockquote>{MANIFESTO}</blockquote></div>{foot(1)}</section>
  <section class="page" id="p3"><div class="two">
    <div><p class="eyebrow">Історія, що живе в нас</p><h2 class="ph2">Наше коріння сягає глибини тисячоліть</h2><div class="text">{"".join(f"<p>{t}</p>" for t in STORY)}</div></div>
    <figure class="fig">{img("photo/edem/art-corner.webp", "Фрагмент принту: трипільська фігурка й плетені шнури на кутку хустки", sizes="(max-width: 980px) 92vw, 44vw")}</figure>
  </div>{foot(2)}</section>
  <section class="page alt" id="p4"><div class="sym4wrap"><span class="eyebrow">Символи хустки</span><h2>Кожна деталь має значення</h2>
    <div class="sym4">{"".join(f'<figure><div class="pic{" lg" if k == "pendant-round" else ""}">{img(f"photo/edem/{k}.webp", a, sizes="260px")}</div><h3>{t}</h3><p>{d}</p></figure>' for k, t, d, a in SYMBOLS)}</div></div>{foot(3)}</section>
  <section class="page print" id="p5"><div class="two">
    <div class="big">{img("photo/edem/art-2400.webp", "Принт хустки «Trypillia — The Art of Origins» повністю", sizes="(max-width: 980px) 92vw, 72vw")}</div>
    <div><p class="eyebrow">Хустка · 88 × 88 см</p><h2 class="ph2">Мистецьке полотно, яке можна носити</h2><p class="lead" style="margin-top:12px">{SCARF_LEAD}</p><div class="spec" style="margin-top:18px">{spec_rows()}</div><p class="note">Ціну й дату старту повідомимо зареєстрованим першими.</p></div>
  </div>{foot(4)}</section>
  <section class="page alt" id="p6"><div class="brands">
    <article><p class="eyebrow">Партнер</p><h3>KRAЇNA EDEM</h3><p>{EDEM_P}</p><ul>{"".join(f"<li>{x}</li>" for x in EDEM_L)}</ul></article>
    <article><p class="eyebrow">Бренд</p><h3>OBIIMY</h3><p>{OB_P}</p><ul>{"".join(f"<li>{x}</li>" for x in OB_L)}</ul></article>
  </div>{foot(5)}</section>
  <section class="page reg" id="p7"><div class="two">
    <div><p class="eyebrow">Як придбати</p><h2>Ранній доступ до випуску</h2><p class="lead">Ціну й дату старту підтверджуємо з партнером. Щойно вони відомі — зареєстровані дізнаються першими й отримують персональне посилання на оплату.</p>
      <div class="steps">{"".join(f"<div><i>0{i + 1}</i><div><h3>{t}</h3><p>{d}</p></div></div>" for i, (t, d) in enumerate(STEPS))}</div>
      <div class="contacts">Питання: <a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="{TG}" target="_blank" rel="noopener">Telegram</a></div></div>
    <div class="panel">{form_html()}</div>
  </div>{foot(6)}</section>
</div></div></div>
</main>'''
    body = body.replace('href="#top">На початок', 'href="#p1">На початок')
    write("edem-book", BOOK_CSS + FORM_CSS, body, BOOK_JS)

if __name__ == "__main__":
    shop(); book()
