#!/usr/bin/env python3
"""Three light, art-led variants of the KRAЇNA EDEM × OBIIMY landing (client, 03.11.2026: «полегче, похудожественней, крупнее
хустка»). Same copy, facts, pictures and registration API as src/build-edem.py; the print itself is the biggest thing on every screen:
  edem-canvas — a poster on warm white paper: a thin headline across the top, the whole print edge to edge under it, then a quiet page;
  edem-spread — a magazine spread: the scarf mock bleeds off the right edge over an enormous italic title, the print full-bleed below;
  edem-silk   — the print blurred into a watercolour wash behind everything, the framed print in the centre, sections on translucent panels,
                a horizontal stroll along the fragments.
Output: edem-canvas.html, edem-spread.html, edem-silk.html (HIDDEN in build-site: deployed, in the variants bar, not in the hub)."""
import importlib.util, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from imgs import img
_spec = importlib.util.spec_from_file_location("edemv", ROOT / "src" / "build-edem-variants.py"); V = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(V)
MANIFESTO, STORY, SYMBOLS, SPEC, EDEM_P, EDEM_L, OB_P, OB_L, STEPS = V.MANIFESTO, V.STORY, V.SYMBOLS, V.SPEC, V.EDEM_P, V.EDEM_L, V.OB_P, V.OB_L, V.STEPS
PHONE, PHONE_HREF, MAIL, TG = V.PHONE, V.PHONE_HREF, V.MAIL, V.TG
form_html, FORM_CSS, write, spec_rows, sym_img = V.form_html, V.FORM_CSS, V.write, V.spec_rows, V.sym_img

LEAD = "Мистецтво бути ближче. Шовкова хустка за трипільськими мотивами — спільна робота KRAЇNA EDEM та OBIIMY."
SCARF_LEAD = "Хустка тут — більше, ніж аксесуар: мистецьке полотно, що поєднує сучасний дизайн із пам’яттю про давні культури."
ART_ALT = "Принт хустки «Trypillia — The Art of Origins» повністю"
FRAGS = [("art-center", "Центральний медальйон крупно", "Медальйон"), ("art-pendants", "Гроно підвісок на плетених шнурах — фрагмент принту", "Підвіски на шнурах"),
         ("art-corner", "Фрагмент принту: трипільська фігурка й плетені шнури на кутку хустки", "Кут хустки · пластика"), ("art-sign", "Підпис OBIIMY × Edem на полотні хустки", "Підпис двох брендів")]

# ─── the light base shared by the three ─────────────────────────────────────────────────────────────────────────────────────
BASE = """
:root { --paper: #FBF7F0; --paper2: #F4ECDF; --ink: #2A2017; --ink2: #6B5A48; --gold: #B48A3A; --gold2: #D9B86A; --line: rgba(42,32,23,.14); --acc: #B48A3A; --fb: rgba(42,32,23,.25); --fbg: #FFFFFF; --fink: #2A2017; }
* { box-sizing: border-box; } html { scroll-behavior: smooth; }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: Montserrat, Arial, sans-serif; font-size: 17px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
img { max-width: 100%; height: auto; display: block; } p { margin: 0; } a { color: inherit; } figure { margin: 0; }
h1, h2, h3 { margin: 0; font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 300; line-height: 1.02; text-wrap: balance; }
.wrap { max-width: 1240px; margin: 0 auto; padding: 0 24px; }
section[id] { scroll-margin-top: 20px; }
.eyebrow { font-size: 11px; font-weight: 600; letter-spacing: .28em; text-transform: uppercase; color: var(--gold); }
.lead { font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(21px, 2vw, 27px); font-weight: 300; line-height: 1.4; color: var(--ink2); }
.btn-main { background: var(--ink); color: var(--paper); } .btn-main:hover { background: #3B2A1C; }
.btn-line { border-color: var(--ink); color: var(--ink); } .btn-line:hover { background: rgba(42,32,23,.06); }
.cta { display: flex; flex-wrap: wrap; gap: 14px; }
.text { color: var(--ink2); } .text p + p { margin-top: 1.1em; } .text .first::first-letter { font-family: 'Cormorant Garamond', serif; font-size: 3.4em; float: left; line-height: .8; margin: .08em .12em 0 0; color: var(--gold); }
.spec div { display: flex; justify-content: space-between; gap: 20px; padding: 14px 0; border-bottom: 1px solid var(--line); font-size: 15px; } .spec span { color: var(--ink2); } .spec b { font-weight: 600; text-align: right; }
.note { margin-top: 18px; font-family: 'Cormorant Garamond', serif; font-size: 20px; font-style: italic; color: var(--ink2); }
.sym4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 40px; }
.sym4 .pic { height: 230px; display: flex; align-items: center; justify-content: center; } .sym4 .pic img { max-height: 100%; width: auto; filter: drop-shadow(0 18px 24px rgba(58,42,28,.18)); } .sym4 .pic.lg img { transform: scale(1.3); transform-origin: 50% 60%; }
.sym4 h3 { font-size: 30px; margin-top: 20px; font-weight: 400; } .sym4 p { margin-top: 10px; font-size: 15px; color: var(--ink2); }
.brands { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; } .brands article { border-top: 1px solid var(--ink); padding-top: 24px; } .brands h3 { font-size: 32px; font-weight: 400; letter-spacing: .04em; margin-top: 10px; } .brands p { margin-top: 12px; color: var(--ink2); font-size: 15px; }
.brands ul { margin: 14px 0 0; padding: 0; list-style: none; } .brands li { padding: 9px 0; border-top: 1px solid var(--line); font-size: 14px; color: var(--ink2); }
.reg .wrap { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: clamp(32px, 5vw, 80px); align-items: start; }
.reg h2 { font-size: clamp(36px, 4.2vw, 60px); margin-top: 14px; } .reg .lead { margin-top: 18px; }
.steps { margin-top: 30px; display: grid; gap: 0; } .steps > div { display: grid; grid-template-columns: 44px minmax(0, 1fr); gap: 14px; padding: 16px 0; border-top: 1px solid var(--line); } .steps h3 { font-size: 24px; font-weight: 400; } .steps p { font-size: 14px; color: var(--ink2); margin-top: 4px; } .steps i { font-family: 'Cormorant Garamond', serif; font-style: normal; font-size: 24px; color: var(--gold); }
.contacts { margin-top: 26px; font-size: 14px; color: var(--ink2); } .contacts a { text-decoration: none; border-bottom: 1px solid var(--line); }
.panel { background: #fff; border: 1px solid var(--line); padding: clamp(24px, 3vw, 40px); }
footer { padding: 34px 24px; font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--ink2); display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; border-top: 1px solid var(--line); }
.done h3 { font-weight: 400; }
@media (max-width: 980px) { .sym4 { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 28px 20px; } .brands, .reg .wrap { grid-template-columns: 1fr; } }
@media (max-width: 600px) { body { font-size: 16px; } .sym4 { grid-template-columns: 1fr; } .cta .btn { flex: 1 1 100%; justify-content: center; } .top, .hero .top { font-size: 9px; letter-spacing: .16em; } }
"""

def steps_html(): return "".join(f"<div><i>0{i + 1}</i><div><h3>{t}</h3><p>{d}</p></div></div>" for i, (t, d) in enumerate(STEPS))
def brands_html(): return f'''<div class="brands">
    <article class="rv"><p class="eyebrow">Партнер</p><h3>KRAЇNA EDEM</h3><p>{EDEM_P}</p><ul>{"".join(f"<li>{x}</li>" for x in EDEM_L)}</ul></article>
    <article class="rv"><p class="eyebrow">Бренд</p><h3>OBIIMY</h3><p>{OB_P}</p><ul>{"".join(f"<li>{x}</li>" for x in OB_L)}</ul></article></div>'''
def reg_html(panel=True): return f'''<section class="reg" id="register"><div class="wrap">
  <div class="rv"><p class="eyebrow">Як придбати</p><h2>Ранній доступ до випуску</h2><p class="lead">Ціну й дату старту підтверджуємо з партнером. Щойно вони відомі — зареєстровані дізнаються першими й отримують персональне посилання на оплату.</p>
    <div class="steps">{steps_html()}</div>
    <div class="contacts">Питання: <a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="{TG}" target="_blank" rel="noopener">Telegram</a></div></div>
  <div class="rv{" panel" if panel else ""}">{form_html()}</div>
</div></section>'''
def sym4_html(sizes="300px"): return '<div class="sym4">' + "".join(f'<figure class="rv"><div class="pic{" lg" if k == "pendant-round" else ""}">{sym_img(k, a, sizes)}</div><h3>{t}</h3><p>{d}</p></figure>' for k, t, d, a in SYMBOLS) + "</div>"
def footer_html(): return f'<footer><span>Kraїna Edem × Obiimy · Trypillia — The Art of Origins · 2026</span><span><a href="{PHONE_HREF}" style="text-decoration:none">{PHONE}</a> · <a href="mailto:{MAIL}" style="text-decoration:none">{MAIL}</a></span></footer>'
def story_p(): return "".join(f'<p{" class=first" if i == 0 else ""}>{t}</p>' for i, t in enumerate(STORY))

# ═══ A · CANVAS — a poster on warm white paper ═════════════════════════════════════════════════════════════════════════════════
CANVAS_CSS = BASE + """
.top { display: flex; justify-content: space-between; align-items: center; padding: 26px 24px; font-size: 11px; letter-spacing: .26em; text-transform: uppercase; color: var(--ink2); } .top a { text-decoration: none; color: var(--ink); font-weight: 600; }
.hero { padding: clamp(20px, 4vw, 60px) 0 0; text-align: center; }
.hero h1 { font-size: clamp(54px, 10.5vw, 176px); letter-spacing: -.015em; line-height: .96; margin-top: 18px; padding: 0 16px; } .hero h1 i { font-style: italic; color: var(--gold); }
.canvas { margin: clamp(30px, 4vw, 64px) auto 0; max-width: 1560px; padding: 0 clamp(10px, 3vw, 48px); }
.canvas img { width: 100%; height: auto; box-shadow: 0 70px 120px -70px rgba(42,32,23,.45); }
.under { max-width: 760px; margin: clamp(34px, 5vw, 72px) auto 0; padding: 0 24px; }
.under .cta { justify-content: center; margin-top: 28px; }
.under .facts { margin-top: 30px; font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink2); } .under .facts b { color: var(--ink); }
section.s { padding: clamp(70px, 9vw, 140px) 0; }
.mani { text-align: center; } .mani blockquote { margin: 0 auto; max-width: 22em; font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: clamp(28px, 4vw, 58px); line-height: 1.2; font-weight: 300; } .mani b { font-style: normal; font-weight: 400; color: var(--gold); }
.mani .orn { width: 72px; margin: 0 auto 30px; }
.strip { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: clamp(14px, 2vw, 28px); } .strip figure img { width: 100%; height: auto; aspect-ratio: 1; object-fit: cover; }
.strip figcaption { margin-top: 12px; font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 19px; color: var(--ink2); }
.head { text-align: center; max-width: 760px; margin: 0 auto clamp(34px, 4vw, 60px); } .head h2 { font-size: clamp(38px, 5vw, 72px); margin-top: 14px; } .head .lead { margin-top: 16px; }
.story { display: grid; grid-template-columns: 160px minmax(0, 1fr) 160px; gap: clamp(24px, 4vw, 60px); align-items: start; } .story .side { padding-top: 10px; } .story .side img { width: 100%; height: auto; filter: drop-shadow(0 16px 20px rgba(58,42,28,.18)); } .story .side p { margin-top: 12px; font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink2); text-align: center; }
.story .text { columns: 2; column-gap: 40px; } .story .text p { break-inside: avoid; }
.specline { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); border-top: 1px solid var(--ink); border-bottom: 1px solid var(--ink); } .specline div { padding: 18px 16px; border-left: 1px solid var(--line); } .specline div:nth-child(3n+1) { border-left: 0; padding-left: 0; } .specline div:nth-child(n+4) { border-top: 1px solid var(--line); } .specline span { display: block; font-size: 11px; letter-spacing: .2em; text-transform: uppercase; color: var(--ink2); } .specline b { display: block; margin-top: 8px; font-family: 'Cormorant Garamond', serif; font-size: 24px; font-weight: 400; }
.scarf2 { display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: clamp(28px, 5vw, 80px); align-items: center; margin-top: clamp(34px, 4vw, 60px); } .scarf2 .mock img { width: 100%; height: auto; filter: drop-shadow(0 40px 60px rgba(58,42,28,.25)); }
@media (max-width: 980px) { .story { grid-template-columns: 1fr; } .story .side { display: none; } .story .text { columns: 1; } .specline { grid-template-columns: 1fr; } .specline div { border-left: 0; padding-left: 0; border-top: 1px solid var(--line); } .specline div:first-child { border-top: 0; } .scarf2 { grid-template-columns: 1fr; } .strip { grid-template-columns: 1fr; } .strip figure img { aspect-ratio: 4 / 3; } }
"""

def canvas():
    body = f'''
<main id="top">
<header class="top"><a href="#top">Kraїna Edem × Obiimy</a><span>Лімітований випуск · 2026</span></header>
<section class="hero">
  <p class="eyebrow">Спільний мистецький проєкт</p>
  <h1>Trypillia — <i>The Art of Origins</i></h1>
  <div class="canvas">{img("photo/edem/art-2400.webp", ART_ALT, sizes="(max-width: 1560px) 96vw, 1460px", lazy=False, eager_priority=True)}</div>
  <div class="under rv"><p class="lead">{LEAD}</p>
    <div class="cta"><a class="btn btn-main" href="#register">Отримати ранній доступ</a><a class="btn btn-line" href="#story">Про проєкт</a></div>
    <p class="facts"><b>88 × 88 см</b> · <b>100% шовк</b> · обмежений наклад · підпис OBIIMY × Edem</p></div>
</section>

<section class="s mani" id="manifest"><div class="wrap rv"><div class="orn">{img("photo/edem/pendant-round.webp", "", sizes="72px")}</div><blockquote>{MANIFESTO}</blockquote></div></section>

<section class="s" id="scarf" style="padding-top:0"><div class="wrap">
  <div class="strip">{"".join(f'<figure class="rv">{img(f"photo/edem/{k}.webp", a, sizes="(max-width: 980px) 92vw, 30vw")}<figcaption>{c}</figcaption></figure>' for k, a, c in FRAGS[:3])}</div>
  <div class="scarf2">
    <div class="rv"><p class="eyebrow">Хустка · 88 × 88 см</p><h2 style="font-size:clamp(36px,4.6vw,66px);margin-top:14px">Мистецьке полотно, яке можна носити</h2><p class="lead" style="margin-top:16px">{SCARF_LEAD}</p>
      <div class="specline" style="margin-top:30px">{"".join(f"<div><span>{k}</span><b>{v}</b></div>" for k, v in SPEC)}</div>
      <p class="note">Ціну й дату старту повідомимо зареєстрованим першими.</p></div>
    <div class="mock rv">{img("photo/edem/scarf.webp", "Хустка KRAЇNA EDEM × OBIIMY «Trypillia — The Art of Origins»", sizes="(max-width: 980px) 90vw, 360px")}</div>
  </div>
</div></section>

<section class="s" id="story" style="background:var(--paper2)"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Історія, що живе в нас</p><h2>Наше коріння сягає глибини тисячоліть</h2></div>
  <div class="story">
    <div class="side rv">{img("photo/edem/figure.webp", "Трипільська фігурка — елемент принту", sizes="160px")}<p>Пластика</p></div>
    <div class="text rv">{story_p()}</div>
    <div class="side rv">{img("photo/edem/pendant-diamond.webp", "Ромбовидна підвіска — елемент принту", sizes="160px")}<p>Ромб</p></div>
  </div>
</div></section>

<section class="s" id="symbols"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Символи хустки</p><h2>Кожна деталь має значення</h2><p class="lead">Давні орнаментальні мотиви й символічні образи — переосмислені мовою сучасного дизайну, у золоті й глибокому синьому.</p></div>
  {sym4_html()}
</div></section>

<section class="s" id="brands" style="background:var(--paper2)"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Партнери</p><h2>Два бренди. Одна філософія. Спільне мистецтво.</h2></div>
  {brands_html()}
</div></section>

{reg_html().replace('<section class="reg"', '<section class="reg s"')}
{footer_html()}
</main>'''
    write("edem-canvas", CANVAS_CSS + FORM_CSS, body)

# ═══ B · SPREAD — a magazine spread, the scarf bleeding off the page ═══════════════════════════════════════════════════════
SPREAD_CSS = BASE + """
body { background: #F7F1E6; }
.hero { position: relative; min-height: 100vh; overflow: hidden; display: grid; align-items: center; padding: 100px 0 80px; }
.hero::before { content: ""; position: absolute; inset: 0; background: radial-gradient(60% 70% at 78% 50%, rgba(226,194,122,.26), transparent 70%); pointer-events: none; }
.hero .top { position: absolute; left: 24px; right: 24px; top: 30px; display: flex; justify-content: space-between; font-size: 11px; letter-spacing: .26em; text-transform: uppercase; color: var(--ink2); z-index: 3; }
.hero .mock { position: absolute; right: -12vw; top: 50%; width: min(64vw, 1100px); transform: translateY(-50%) rotate(-4deg); z-index: 1; pointer-events: none; }
.hero .mock img { width: 100%; height: auto; filter: drop-shadow(0 60px 80px rgba(58,42,28,.3)); }
.hero .wrap { position: relative; z-index: 2; width: 100%; } .hero .wrap > * { max-width: 50%; }
.hero h1 { font-size: clamp(60px, 9vw, 160px); font-style: italic; line-height: .9; letter-spacing: -.02em; max-width: 4.6em; } .hero h1 b { font-style: normal; font-weight: 300; }
.hero .lead { max-width: 20em; margin-top: 28px; background: rgba(247,241,230,.7); backdrop-filter: blur(6px); padding: 6px 0; }
.hero .cta { margin-top: 30px; }
.hero .facts { margin-top: 36px; font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink2); display: flex; flex-wrap: wrap; gap: 8px 26px; } .hero .facts b { color: var(--ink); }
.vert { position: absolute; left: 24px; bottom: 36px; writing-mode: vertical-rl; transform: rotate(180deg); font-size: 11px; letter-spacing: .3em; text-transform: uppercase; color: var(--ink2); z-index: 3; }
.bleed { position: relative; } .bleed img { width: 100%; height: auto; }
.bleed .cap { position: absolute; left: 24px; bottom: 24px; padding: 10px 14px; background: rgba(247,241,230,.86); backdrop-filter: blur(8px); font-size: 11px; letter-spacing: .18em; text-transform: uppercase; color: var(--ink); }
section.s { padding: clamp(70px, 9vw, 140px) 0; }
.pull { display: grid; grid-template-columns: 1px minmax(0, 1fr); gap: clamp(28px, 5vw, 80px); } .pull i { display: block; background: var(--gold); height: 100%; min-height: 160px; }
.pull blockquote { margin: 0; font-family: 'Cormorant Garamond', serif; font-size: clamp(30px, 4.6vw, 68px); line-height: 1.12; font-weight: 300; max-width: 16em; } .pull b { font-weight: 400; font-style: italic; color: var(--gold); }
.num { font-family: 'Cormorant Garamond', serif; font-size: clamp(90px, 12vw, 180px); line-height: .8; color: var(--gold2); font-weight: 300; }
.two { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(28px, 5vw, 80px); align-items: start; }
.two h2 { font-size: clamp(38px, 5vw, 72px); margin-top: 10px; } .two .text { margin-top: 24px; }
.fig img { width: 100%; height: auto; } .fig figcaption { margin-top: 12px; font-size: 11px; letter-spacing: .18em; text-transform: uppercase; color: var(--ink2); }
.spec2 { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, .85fr); gap: clamp(28px, 5vw, 80px); align-items: center; }
.spec2 .big img { width: 100%; height: auto; box-shadow: 0 50px 90px -50px rgba(42,32,23,.4); } .spec2 h2 { font-size: clamp(36px, 4.6vw, 66px); margin-top: 12px; }
.spec2 .zoom { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-top: 12px; } .spec2 .zoom img { width: 100%; height: auto; aspect-ratio: 1; object-fit: cover; }
.head { max-width: 760px; margin-bottom: clamp(30px, 4vw, 54px); } .head h2 { font-size: clamp(38px, 5vw, 72px); margin-top: 12px; }
@media (max-width: 980px) { .hero { min-height: 0; padding: 90px 0 0; display: block; } .hero .mock { position: static; width: 100%; max-width: 560px; margin: 40px auto -20px; transform: rotate(-4deg); } .hero h1 { font-size: clamp(52px, 13vw, 90px); max-width: none; } .hero .wrap > * { max-width: none; } .vert { display: none; } .pull { grid-template-columns: 1fr; } .pull i { height: 1px; min-height: 0; width: 120px; } .two, .spec2 { grid-template-columns: 1fr; } }
"""

def spread():
    body = f'''
<main id="top">
<section class="hero">
  <div class="top"><span>Kraїna Edem × Obiimy</span><span>Лімітований випуск · 2026</span></div>
  <div class="mock" aria-hidden="true">{img("photo/edem/scarf.webp", "", sizes="(max-width: 980px) 100vw, 70vw", lazy=False, eager_priority=True)}</div>
  <div class="wrap">
    <p class="eyebrow">Спільний мистецький проєкт</p>
    <h1 style="margin-top:18px"><b>Trypillia —</b><br>The Art of Origins</h1>
    <p class="lead">{LEAD}</p>
    <div class="cta"><a class="btn btn-main" href="#register">Отримати ранній доступ</a><a class="btn btn-line" href="#scarf">Побачити хустку</a></div>
    <div class="facts"><span><b>88 × 88</b> см</span><span><b>100%</b> шовк</span><span>Обмежений наклад</span><span>Підпис OBIIMY × Edem</span></div>
  </div>
  <p class="vert">Шовкова хустка за трипільськими мотивами</p>
</section>

<div class="bleed" id="scarf">{img("photo/edem/art-2400.webp", ART_ALT, sizes="100vw")}<p class="cap">Принт повністю · 88 × 88 см · 100% шовк</p></div>

<section class="s" id="manifest"><div class="wrap"><div class="pull rv"><i></i><blockquote>{MANIFESTO}</blockquote></div></div></section>

<section class="s" id="spec" style="padding-top:0"><div class="wrap"><div class="spec2">
  <div class="big rv">{img("photo/edem/art-center.webp", "Центральний медальйон крупно", sizes="(max-width: 980px) 92vw, 56vw")}
    <div class="zoom">{"".join(img(f"photo/edem/{k}.webp", a, sizes="18vw") for k, a, c in FRAGS[1:])}</div></div>
  <div class="rv"><p class="eyebrow">Хустка · 88 × 88 см</p><h2>Мистецьке полотно, яке можна носити</h2><p class="lead" style="margin-top:14px">{SCARF_LEAD}</p>
    <div class="spec" style="margin-top:24px">{spec_rows()}</div><p class="note">Ціну й дату старту повідомимо зареєстрованим першими.</p>
    <p style="margin-top:26px"><a class="btn btn-main" href="#register">Отримати ранній доступ</a></p></div>
</div></div></section>

<section class="s" id="story" style="background:#FBF7F0"><div class="wrap"><div class="two">
  <div class="rv"><p class="num">I</p><p class="eyebrow" style="margin-top:20px">Історія, що живе в нас</p><h2>Наше коріння сягає глибини тисячоліть</h2><div class="text">{story_p()}</div></div>
  <figure class="fig rv" style="margin-top:clamp(40px,8vw,140px)">{img("photo/edem/art-corner.webp", "Фрагмент принту: трипільська фігурка й плетені шнури на кутку хустки", sizes="(max-width: 980px) 92vw, 46vw")}<figcaption>Фрагмент принту · кут хустки</figcaption></figure>
</div></div></section>

<section class="s" id="symbols"><div class="wrap">
  <div class="head rv"><p class="num">II</p><p class="eyebrow" style="margin-top:20px">Символи хустки</p><h2>Кожна деталь має значення</h2></div>
  {sym4_html()}
</div></section>

<section class="s" id="brands" style="background:#FBF7F0"><div class="wrap">
  <div class="head rv"><p class="num">III</p><p class="eyebrow" style="margin-top:20px">Партнери</p><h2>Два бренди. Одна філософія. Спільне мистецтво.</h2></div>
  {brands_html()}
</div></section>

{reg_html().replace('<section class="reg"', '<section class="reg s"')}
{footer_html()}
</main>'''
    write("edem-spread", SPREAD_CSS + FORM_CSS, body)

# ═══ C · SILK — the print as a watercolour wash, panels on top, a stroll along the fragments ═══════════════════════════════
SILK_CSS = BASE + """
body { background: #F8F2E8; }
.wash { position: fixed; inset: -14%; z-index: 0; pointer-events: none; } .wash img { width: 100%; height: 100%; object-fit: cover; filter: blur(70px) saturate(.9); opacity: .38; }
.wash::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(248,242,232,.2), rgba(248,242,232,.55)); }
main { position: relative; z-index: 1; }
.top { display: flex; justify-content: space-between; align-items: center; padding: 26px 24px; font-size: 11px; letter-spacing: .26em; text-transform: uppercase; color: var(--ink2); } .top a { text-decoration: none; color: var(--ink); font-weight: 600; }
.hero { text-align: center; padding: clamp(10px, 2vw, 30px) 24px 0; }
.hero h1 { font-size: clamp(44px, 6.4vw, 104px); margin-top: 14px; } .hero h1 i { font-style: italic; color: var(--gold); }
.frame { width: min(88vh, 100%); max-width: 1180px; margin: clamp(26px, 3.5vw, 50px) auto 0; padding: clamp(10px, 1.4vw, 18px); background: rgba(255,255,255,.72); backdrop-filter: blur(14px); border: 1px solid rgba(255,255,255,.9); box-shadow: 0 60px 100px -60px rgba(42,32,23,.45); }
.frame img { width: 100%; height: auto; }
.hero .under { max-width: 720px; margin: clamp(26px, 4vw, 54px) auto 0; } .hero .cta { justify-content: center; margin-top: 26px; }
.hero .facts { margin-top: 26px; font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink2); } .hero .facts b { color: var(--ink); }
section.s { padding: clamp(60px, 8vw, 120px) 0; }
.glass { background: rgba(255,255,255,.66); backdrop-filter: blur(18px); border: 1px solid rgba(255,255,255,.9); padding: clamp(28px, 4vw, 64px); }
.mani blockquote { margin: 0 auto; max-width: 24em; text-align: center; font-family: 'Cormorant Garamond', serif; font-size: clamp(28px, 4vw, 56px); line-height: 1.2; font-weight: 300; } .mani b { font-weight: 400; font-style: italic; color: var(--gold); }
.stroll { display: flex; gap: clamp(14px, 2vw, 28px); overflow-x: auto; scroll-snap-type: x mandatory; padding: 6px 24px 24px; scrollbar-width: thin; -webkit-overflow-scrolling: touch; }
.stroll figure { flex: 0 0 min(72vw, 620px); scroll-snap-align: center; } .stroll figure img { width: 100%; height: auto; aspect-ratio: 1; object-fit: cover; background: rgba(255,255,255,.5); padding: 10px; }
.stroll figcaption { margin-top: 12px; font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 20px; color: var(--ink2); }
.stroll::before, .stroll::after { content: ""; flex: 0 0 max(0px, calc(50vw - 620px / 2 - 24px)); }
.head { text-align: center; max-width: 760px; margin: 0 auto clamp(30px, 4vw, 54px); } .head h2 { font-size: clamp(36px, 4.8vw, 68px); margin-top: 12px; } .head .lead { margin-top: 14px; }
.two { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(28px, 5vw, 80px); align-items: center; } .two h2 { font-size: clamp(34px, 4.4vw, 62px); margin-top: 10px; } .two .text { margin-top: 20px; }
.two .pic img { width: 100%; height: auto; }
.spec2 { display: grid; grid-template-columns: 300px minmax(0, 1fr); gap: clamp(28px, 5vw, 70px); align-items: center; } .spec2 .mock img { width: 100%; height: auto; filter: drop-shadow(0 30px 50px rgba(58,42,28,.25)); }
.spec2 .spec { columns: 2; column-gap: 40px; margin-top: 20px; } .spec2 .spec div { break-inside: avoid; }
@media (max-width: 980px) { .two, .spec2 { grid-template-columns: 1fr; } .spec2 .mock { max-width: 300px; margin: 0 auto; } .spec2 .spec { columns: 1; } .frame { width: 100%; } }
"""

def silk():
    body = f'''
<div class="wash" aria-hidden="true">{img("photo/edem/art-1600.webp", "", sizes="100vw")}</div>
<main id="top">
<header class="top"><a href="#top">Kraїna Edem × Obiimy</a><span>Лімітований випуск · 2026</span></header>
<section class="hero">
  <p class="eyebrow">Спільний мистецький проєкт</p>
  <h1>Trypillia — <i>The Art of Origins</i></h1>
  <div class="frame">{img("photo/edem/art-2400.webp", ART_ALT, sizes="(max-width: 1200px) 96vw, 1150px", lazy=False, eager_priority=True)}</div>
  <div class="under rv"><p class="lead">{LEAD}</p>
    <div class="cta"><a class="btn btn-main" href="#register">Отримати ранній доступ</a><a class="btn btn-line" href="#story">Про проєкт</a></div>
    <p class="facts"><b>88 × 88 см</b> · <b>100% шовк</b> · обмежений наклад · підпис OBIIMY × Edem</p></div>
</section>

<section class="s mani" id="manifest"><div class="wrap"><div class="glass rv"><blockquote>{MANIFESTO}</blockquote></div></div></section>

<section class="s" id="scarf" style="padding-top:0">
  <div class="head rv"><p class="eyebrow">Прогулянка принтом</p><h2>Мистецьке полотно, яке можна носити</h2><p class="lead">{SCARF_LEAD}</p></div>
  <div class="stroll">{"".join(f'<figure class="rv">{img(f"photo/edem/{k}.webp", a, sizes="(max-width: 980px) 72vw, 620px")}<figcaption>{c}</figcaption></figure>' for k, a, c in FRAGS)}</div>
  <div class="wrap" style="margin-top:clamp(30px,4vw,60px)"><div class="glass spec2 rv">
    <div class="mock">{img("photo/edem/scarf.webp", "Хустка KRAЇNA EDEM × OBIIMY «Trypillia — The Art of Origins»", sizes="300px")}</div>
    <div><p class="eyebrow">Хустка · 88 × 88 см</p><div class="spec">{spec_rows()}</div><p class="note">Ціну й дату старту повідомимо зареєстрованим першими.</p><p style="margin-top:24px"><a class="btn btn-main" href="#register">Отримати ранній доступ</a></p></div>
  </div></div>
</section>

<section class="s" id="story" style="padding-top:0"><div class="wrap"><div class="glass two">
  <div class="rv"><p class="eyebrow">Історія, що живе в нас</p><h2>Наше коріння сягає глибини тисячоліть</h2><div class="text">{story_p()}</div></div>
  <div class="pic rv">{img("photo/edem/art-corner.webp", "Фрагмент принту: трипільська фігурка й плетені шнури на кутку хустки", sizes="(max-width: 980px) 92vw, 44vw")}</div>
</div></div></section>

<section class="s" id="symbols" style="padding-top:0"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Символи хустки</p><h2>Кожна деталь має значення</h2></div>
  {sym4_html()}
</div></section>

<section class="s" id="brands" style="padding-top:0"><div class="wrap"><div class="glass">
  <div class="head rv" style="text-align:left;margin-left:0"><p class="eyebrow">Партнери</p><h2>Два бренди. Одна філософія. Спільне мистецтво.</h2></div>
  {brands_html()}
</div></div></section>

{reg_html().replace('<section class="reg"', '<section class="reg s" style="padding-top:0"')}
{footer_html()}
</main>'''
    write("edem-silk", SILK_CSS + FORM_CSS, body)

if __name__ == "__main__":
    canvas(); spread(); silk()
