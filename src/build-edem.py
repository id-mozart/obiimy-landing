#!/usr/bin/env python3
"""KRAЇNA EDEM × OBIIMY — the landing of the collaboration scarf «TRYPILLIA — THE ART OF ORIGINS» (88 × 88, limited edition).
Copy: the partners' press release (Google Doc «Прес реліз Obiimy x Edem», variants 1 and 2) and the launch deck
(OBIIMY x EDEM Launch.pdf: «Мистецтво бути ближче», the register → personal payment link → delivery mechanics). Price and the
sales start are not confirmed in the deck, so the page promises only to tell the registered first. Pictures: the artwork
(88x88cm trypilla.ai rendered to photo/edem/), the four element illustrations and the deck's scarf mock — all the client's own,
converted to WebP so no PNG lands in a srcset. Registrations go to the editor service (/api/edem) and are kept on its volume;
the Telegram link is the fallback. Round 2 after three experts (02.11): no cards, square-cut buttons in navy, sticky spec
column, the signature crop as proof, the steps inside the registration block, a shorter form.
Output: edem.html (wrapped into site/ by build-site.py)."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from imgs import img, typo

PHONE, PHONE_HREF, MAIL, TG = "+38 067 010 85 25", "tel:+380670108525", "sale@obiimy.world", "https://t.me/OBIIMY_sales"
API_LOCAL, API_PROD = "http://127.0.0.1:8770", "https://deck-editor-production.up.railway.app"
SITE_URL = "https://obiimy-landing-production.up.railway.app"

CSS = """
:root { --paper: #F3E9D8; --cream: #FBF4E7; --navy: #3B2A1C; --deep: #2A1D13; --gold: #7F6020; --gold2: #E2C27A; --rule: #C9A95A; --ink: #2A2017; --ink2: #5A4B3C; --line: rgba(58,42,28,.16); }
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: Montserrat, Arial, sans-serif; font-size: 17px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
img { max-width: 100%; height: auto; display: block; }
a { color: inherit; }
p { margin: 0; }
h1, h2, h3 { margin: 0; font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 500; line-height: 1.05; letter-spacing: -.005em; text-wrap: balance; }
.wrap { max-width: 1240px; margin: 0 auto; padding: 0 24px; }
section[id], .reg { scroll-margin-top: 72px; }
.eyebrow { font-size: 12px; font-weight: 600; letter-spacing: .22em; text-transform: uppercase; color: var(--gold); }
.lead { font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(22px, 2.2vw, 28px); line-height: 1.35; color: var(--ink2); text-wrap: pretty; }
.btn { display: inline-flex; align-items: center; gap: 12px; padding: 17px 30px; border-radius: 2px; font-weight: 500; font-size: 13px; letter-spacing: .12em; text-transform: uppercase; text-decoration: none; border: 1px solid transparent; transition: background .2s, color .2s, border-color .2s; }
.btn-gold { background: var(--navy); color: var(--cream); }
.btn-gold:hover { background: var(--deep); }
.btn-line { border-color: var(--navy); color: var(--navy); } .btn-line:hover { background: rgba(30,53,87,.06); }
.btn-line.light { border-color: rgba(251,247,239,.7); color: var(--cream); }
.top { position: sticky; top: 0; z-index: 20; background: rgba(244,238,227,.92); backdrop-filter: blur(10px); border-bottom: 1px solid var(--line); }
.top .wrap { display: flex; justify-content: space-between; align-items: center; height: 64px; gap: 20px; }
.top .brand { font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 600; font-size: 20px; letter-spacing: .08em; text-transform: uppercase; color: var(--navy); white-space: nowrap; text-decoration: none; }
.top .brand span { color: var(--rule); margin: 0 10px; }
.top nav { display: flex; gap: 26px; font-size: 14px; }
.top nav a { text-decoration: none; color: var(--ink2); } .top nav a:hover { color: var(--navy); }
.top .btn { padding: 11px 18px; font-size: 12px; white-space: nowrap; }
/* hero */
.hero { position: relative; overflow: hidden; padding: clamp(48px, 7vw, 110px) 0 clamp(56px, 7vw, 100px); }
.hero .wrap { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: clamp(32px, 5vw, 80px); align-items: center; }
.hero h1 { font-size: clamp(44px, 6.2vw, 92px); color: var(--navy); margin: 18px 0 22px; }
.hero h1 i { font-style: italic; font-weight: 400; color: #B48A3A; }
.hero .lead { max-width: 30em; }
.hero .cta { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 34px; }
.hero .facts { display: flex; flex-wrap: wrap; gap: 10px 28px; margin-top: 44px; padding-top: 22px; border-top: 1px solid var(--line); font-size: 13px; letter-spacing: .08em; text-transform: uppercase; color: var(--ink2); }
.hero .facts b { color: var(--navy); font-weight: 600; }
.hero .art { position: relative; aspect-ratio: 1; }
.hero .art::before { content: ""; position: absolute; inset: 6%; border-radius: 50%; border: 1px solid rgba(180,138,58,.5); }
.hero .art img { position: relative; z-index: 1; width: 100%; height: 100%; object-fit: contain; filter: drop-shadow(0 28px 44px rgba(58,42,28,.22)); transform: rotate(-4deg); }
/* manifesto */
.band { background: var(--navy); color: var(--cream); padding: clamp(56px, 7vw, 110px) 0; position: relative; overflow: hidden; }
.band .wrap { position: relative; display: grid; grid-template-columns: minmax(0, 1fr) 280px; gap: 60px; align-items: center; }
.band blockquote { margin: 0; font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(26px, 3.2vw, 46px); line-height: 1.25; font-weight: 400; text-wrap: balance; }
.band blockquote b { color: var(--gold2); font-weight: 500; }
.band .sym img { width: 100%; height: auto; filter: drop-shadow(0 20px 30px rgba(0,0,0,.4)); }
.band .eyebrow { color: var(--gold2); }
/* sections */
section.s { padding: clamp(56px, 7vw, 110px) 0; }
section.s.alt { background: var(--cream); }
#scarf { padding-top: clamp(72px, 9vw, 140px); }
.head { max-width: 760px; margin-bottom: clamp(32px, 4vw, 56px); }
.head h2 { font-size: clamp(34px, 4.2vw, 60px); color: var(--navy); margin-top: 14px; }
.head .lead { margin-top: 18px; }
h3 { font-size: 28px; color: var(--navy); }
.cols { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: clamp(28px, 4vw, 64px); align-items: center; }
.text p + p { margin-top: 1.1em; }
.text .first::first-letter { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 3.4em; float: left; line-height: .8; margin: .08em .12em 0 0; color: #B48A3A; }
.fig img { width: 100%; height: auto; border-radius: 2px; }
.fig figcaption { margin-top: 12px; font-size: 13px; letter-spacing: .06em; text-transform: uppercase; color: var(--ink2); }
figure { margin: 0; }
/* symbols: the illustrations float on the cream, a gold hairline under the picture */
.sym4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 40px; }
.sym4 figure { display: flex; flex-direction: column; }
.sym4 .pic { height: 260px; display: flex; align-items: center; justify-content: center; }
.sym4 .pic img { height: auto; max-height: 100%; width: auto; max-width: 100%; filter: drop-shadow(0 18px 24px rgba(58,42,28,.2)); }
.sym4 .pic.lg img { transform: scale(1.3); transform-origin: 50% 60%; }
.sym4 h3 { margin-top: 26px; padding-top: 18px; border-top: 1px solid var(--rule); }
.sym4 p { margin-top: 10px; font-size: 15px; color: var(--ink2); line-height: 1.55; }
/* the scarf */
.scarf { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, .8fr); gap: clamp(28px, 4vw, 64px); align-items: start; }
.scarf > div:last-child { position: sticky; top: 96px; }
.scarf .full img { width: 100%; height: auto; border-radius: 2px; box-shadow: 0 50px 90px -40px rgba(58,42,28,.45); }
.scarf .zoom { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px; }
.scarf .zoom figure img { width: 100%; height: auto; aspect-ratio: 1; object-fit: cover; border-radius: 2px; }
.scarf .zoom figcaption { margin-top: 10px; font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--ink2); }
.spec { border-top: 1px solid var(--line); }
.spec div { display: flex; justify-content: space-between; gap: 20px; padding: 16px 0; border-bottom: 1px solid var(--line); font-size: 15px; }
.spec div span:first-child { color: var(--ink2); }
.spec div b { font-weight: 600; color: var(--navy); text-align: right; }
.note { margin-top: 22px; padding: 20px 22px; border-left: 2px solid var(--rule); background: var(--cream); font-size: 15px; color: var(--ink2); border-radius: 2px; }
/* brands */
.brands { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 48px; }
.brands article { border-top: 1px solid var(--rule); padding-top: 28px; }
.brands .eyebrow { margin-bottom: 14px; }
.brands p { margin-top: 14px; color: var(--ink2); }
.brands ul { margin: 16px 0 0; padding: 0; list-style: none; }
.brands li { padding: 10px 0; border-top: 1px solid var(--line); font-size: 15px; }
/* registration: the mechanics and the form */
.reg { background: var(--navy); color: var(--cream); padding: clamp(56px, 7vw, 110px) 0; }
.reg .wrap { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); grid-template-areas: "text form" "steps form"; gap: 0 clamp(32px, 5vw, 80px); align-items: start; }
.reg .rtext { grid-area: text; } .reg .rsteps { grid-area: steps; } .reg .rform { grid-area: form; }
.reg h2 { font-size: clamp(34px, 4vw, 56px); margin-top: 14px; }
.reg .eyebrow { color: var(--gold2); }
.reg .lead { color: rgba(251,247,239,.82); margin-top: 18px; }
.steps { margin-top: 30px; counter-reset: st; }
.steps div { position: relative; padding: 18px 0 18px 64px; border-top: 1px solid rgba(251,247,239,.18); }
.steps div::before { counter-increment: st; content: "0" counter(st); position: absolute; left: 0; top: 16px; font-family: 'Cormorant Garamond', Georgia, serif; font-size: 34px; color: var(--gold2); line-height: 1; }
.steps h3 { font-size: 24px; color: var(--cream); }
.steps p { margin-top: 6px; font-size: 15px; color: rgba(251,247,239,.75); }
.reg .contacts { margin-top: 30px; font-size: 15px; color: rgba(251,247,239,.75); line-height: 1.9; }
.reg .contacts a { color: var(--cream); text-decoration: none; border-bottom: 1px solid rgba(251,247,239,.35); }
form.f { background: var(--cream); color: var(--ink); border-radius: 2px; padding: 34px 32px 30px; display: grid; grid-template-columns: 1fr 1fr; gap: 18px 16px; }
form.f label { display: grid; gap: 7px; font-size: 13px; font-weight: 600; letter-spacing: .04em; color: var(--ink2); }
form.f label.full, form.f fieldset { grid-column: 1 / -1; }
form.f input { font: inherit; font-size: 16px; padding: 13px 14px; border: 1px solid rgba(27,22,19,.22); border-radius: 2px; background: #fff; color: var(--ink); width: 100%; }
form.f input:focus { outline: 2px solid var(--rule); outline-offset: 1px; border-color: transparent; }
form.f fieldset { border: 0; margin: 0; padding: 0; } form.f legend { font-size: 13px; font-weight: 600; letter-spacing: .04em; color: var(--ink2); padding: 0; margin-bottom: 10px; }
form.f .radios { display: flex; flex-wrap: wrap; gap: 10px; }
form.f .radios { flex-direction: column; gap: 6px; }
form.f .radios label { display: inline-flex; align-items: center; gap: 10px; font-weight: 500; font-size: 15px; letter-spacing: 0; color: var(--ink); padding: 6px 0; cursor: pointer; }
form.f .radios input { width: 17px; height: 17px; padding: 0; margin: 0; }
form.f .radios input { accent-color: var(--navy); }
form.f .actions { grid-column: 1 / -1; display: flex; flex-wrap: wrap; gap: 14px 20px; align-items: center; margin-top: 6px; }
form.f .hint { font-size: 13px; color: var(--ink2); }
form.f .err { color: #A33; font-size: 13px; display: none; } form.f label.bad .err { display: block; } form.f label.bad input { border-color: #A33; }
.done { background: var(--cream); color: var(--ink); border-radius: 2px; padding: 40px 34px; }
.done h3 { font-size: 34px; } .done p { margin-top: 14px; color: var(--ink2); }
.done .row { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 22px; }
/* footer */
footer { padding: 34px 0 44px; font-size: 13px; color: var(--ink2); }
footer .wrap { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px 30px; }
footer a { text-decoration: none; }
/* reveal */
.rv { opacity: 0; transform: translateY(22px); transition: opacity .7s cubic-bezier(.2,.7,.2,1), transform .7s cubic-bezier(.2,.7,.2,1); }
.rv.in { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) { .rv { opacity: 1; transform: none; transition: none; } html { scroll-behavior: auto; } }
@media (max-width: 980px) {
  .hero .wrap, .cols, .scarf, .reg .wrap, .band .wrap { grid-template-columns: 1fr; }
  .reg .wrap { grid-template-areas: "text" "form" "steps"; gap: 28px 0; } .reg .rsteps .steps { margin-top: 6px; }
  .scarf > div:last-child { position: static; }
  .band .wrap { gap: 32px; } .band .sym { max-width: 220px; margin: 0 auto; }
  .sym4 { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px 24px; }
  .brands { grid-template-columns: 1fr; gap: 32px; }
  .top nav { display: none; }
  .hero .art { max-width: 520px; margin: 0 auto; }
}
@media (max-width: 600px) {
  body { font-size: 16px; }
  .sym4 { grid-template-columns: 1fr; } .sym4 .pic { height: 220px; }
  form.f { grid-template-columns: 1fr; padding: 26px 20px 22px; }
  .top .wrap { gap: 10px; } .top .brand { font-size: 14px; letter-spacing: .06em; } .top .brand span { margin: 0 6px; } .top .btn { display: inline-flex; padding: 9px 11px; font-size: 11px; letter-spacing: .06em; }
  .hero .cta .btn { flex: 1 1 100%; justify-content: center; }
  .hero .facts { gap: 8px 18px; font-size: 12px; }
  .steps div { padding-left: 52px; }
}
"""

VARIANTS = [("edem", "Класика"), ("edem-gold", "Золото"), ("edem-museum", "Музей"), ("edem-zoom", "Занурення"), ("edem-canvas", "Полотно"), ("edem-spread", "Розворот"), ("edem-silk", "Шовк"), ("edem-motion", "Рух"), ("edem-motion-light", "Рух світлий")]
def variants_bar(current):
    """A small fixed strip to switch between the design variants of the collaboration landing (client review, 02.11)."""
    links = "".join(f'<a href="{slug}"{" class=on" if slug == current else ""}>{name}</a>' for slug, name in VARIANTS)
    return f'''<nav class="vbar" aria-label="Варіанти дизайну"><span>Варіант</span>{links}</nav>
<style>.vbar {{ position: fixed; right: 16px; bottom: 16px; z-index: 50; display: flex; gap: 2px; align-items: center; padding: 6px 8px 6px 12px; border-radius: 999px; background: rgba(42,32,23,.88); color: #F3E9D8; font: 500 12px/1 Montserrat, Arial, sans-serif; backdrop-filter: blur(8px); box-shadow: 0 10px 30px rgba(0,0,0,.25); }}
.vbar span {{ opacity: .6; margin-right: 8px; letter-spacing: .08em; text-transform: uppercase; font-size: 10px; }}
.vbar a {{ color: inherit; text-decoration: none; padding: 8px 12px; border-radius: 999px; }} .vbar a:hover {{ background: rgba(255,255,255,.1); }} .vbar a.on {{ background: #E2C27A; color: #2A2017; }}
@media (max-width: 600px) {{ .vbar {{ right: 10px; bottom: 10px; left: 10px; justify-content: center; flex-wrap: wrap; gap: 0; border-radius: 16px; }} .vbar a {{ padding: 7px 9px; font-size: 11px; }} .vbar span {{ display: none; }} }}</style>'''

def main():
    scarf = img("photo/edem/scarf.webp", "Хустка KRAЇNA EDEM × OBIIMY «Trypillia — The Art of Origins», 88 × 88", sizes="(max-width: 980px) 90vw, 46vw", lazy=False, eager_priority=True)
    body = f'''
<header class="top"><div class="wrap">
  <a class="brand" href="#top">Kraїna Edem<span>×</span>Obiimy</a>
  <nav><a href="#scarf">Хустка</a><a href="#story">Історія</a><a href="#symbols">Символи</a><a href="#brands">Партнери</a><a href="#register">Як придбати</a></nav>
  <a class="btn btn-gold" href="#register">Ранній доступ</a>
</div></header>
<main id="top">
<section class="hero"><div class="wrap">
  <div>
    <p class="eyebrow">Спільний мистецький проєкт · лімітований випуск</p>
    <h1>Trypillia —<br><i>The Art of Origins</i></h1>
    <p class="lead">Мистецтво бути ближче. Шовкова хустка за трипільськими мотивами — спільна робота KRAЇNA EDEM та OBIIMY.</p>
    <div class="cta"><a class="btn btn-gold" href="#register">Отримати ранній доступ</a><a class="btn btn-line" href="#story">Про проєкт</a></div>
    <div class="facts"><span><b>88 × 88 см</b></span><span><b>100%</b> шовк</span><span>Обмежений наклад</span><span>Підпис OBIIMY × Edem</span></div>
  </div>
  <div class="art">{scarf}</div>
</div></section>

<section class="band"><div class="wrap">
  <div class="rv">
    <p class="eyebrow">Маніфест</p>
    <blockquote style="margin-top:18px">Є речі, які неможливо виміряти часом. <b>Пам’ять землі.</b> Символи, що пережили тисячоліття. Образи, які залишили нам давні покоління. І культурний код, який продовжує жити, навіть коли змінюються епохи.</blockquote>
  </div>
  <div class="sym rv">{img("photo/edem/pendant-diamond.webp", "Золота підвіска з трипільським орнаментом — елемент принту", sizes="280px")}</div>
</div></section>

<section class="s" id="scarf"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Хустка · 88 × 88 см</p><h2>Мистецьке полотно, яке можна носити</h2><p class="lead">Хустка тут — більше, ніж аксесуар: мистецьке полотно, що поєднує сучасний дизайн із пам’яттю про давні культури.</p></div>
  <div class="scarf">
    <div class="rv">
      <div class="full">{img("photo/edem/art-1600.webp", "Принт хустки «Trypillia — The Art of Origins» повністю", sizes="(max-width: 980px) 92vw, 58vw")}</div>
      <div class="zoom">
        <figure>{img("photo/edem/art-pendants.webp", "Гроно підвісок на плетених шнурах — фрагмент принту", sizes="(max-width: 980px) 45vw, 28vw")}<figcaption>Підвіски на шнурах</figcaption></figure>
        <figure>{img("photo/edem/art-sign.webp", "Підпис OBIIMY × Edem на полотні хустки", sizes="(max-width: 980px) 45vw, 28vw")}<figcaption>Підпис двох брендів на полотні</figcaption></figure>
      </div>
    </div>
    <div class="rv">
      <div class="spec">
        <div><span>Розмір</span><b>88 × 88 см</b></div>
        <div><span>Матеріал</span><b>100% натуральний шовк</b></div>
        <div><span>Принт</span><b>Авторський, спільний для двох брендів</b></div>
        <div><span>Підпис</span><b>OBIIMY × Edem на полотні</b></div>
        <div><span>Наклад</span><b>Обмежений</b></div>
        <div><span>Виготовлено</span><b>в Україні</b></div>
      </div>
      <div class="note">Ціну й дату старту повідомимо зареєстрованим першими.</div>
      <p style="margin-top:26px"><a class="btn btn-gold" href="#register">Отримати ранній доступ</a></p>
    </div>
  </div>
</div></section>

<section class="s" id="story"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Історія, що живе в нас</p><h2>Наше коріння сягає глибини тисячоліть</h2></div>
  <div class="cols">
    <div class="text rv">
      <p class="first">Задовго до сучасних кордонів і держав на землях нинішньої України розвивалися давні культури, які залишили по собі унікальну мистецьку спадщину. Особливе місце серед них посідає трипільська культура — одна з найяскравіших археологічних культур давньої Європи, що існувала впродовж VI–IV тисячоліть до нашої ери.</p>
      <p>Сьогодні ці стародавні знаки набувають нового звучання. Ми не можемо повернути час, але можемо зберегти пам’ять про тих, хто жив до нас, — відкрити для себе їхнє мистецтво й відчути зв’язок із землею, її історією та культурними витоками.</p>
    </div>
    <figure class="fig rv">{img("photo/edem/art-corner.webp", "Фрагмент принту: трипільська фігурка й плетені шнури на кутку хустки", sizes="(max-width: 980px) 92vw, 46vw")}<figcaption>Фрагмент принту · кут хустки</figcaption></figure>
  </div>
</div></section>

<section class="s alt" id="symbols"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Символи хустки</p><h2>Кожна деталь має значення</h2><p class="lead">Давні орнаментальні мотиви й символічні образи стали основою нової естетичної історії — переосмислені мовою сучасного дизайну, у золоті й глибокому синьому.</p></div>
  <div class="sym4">
    <figure class="rv"><div class="pic">{img("photo/edem/figure.webp", "Золота жіноча фігурка зі спіралями — трипільська пластика в принті", sizes="300px")}</div><h3>Пластика</h3><p>Жіноча фігурка зі спіральним орнаментом — образ трипільської пластики, який чотири рази повторюється на полотні хустки.</p></figure>
    <figure class="rv"><div class="pic">{img("photo/edem/mandala.webp", "Центральний медальйон принту: спіраль у золоті й синьому", sizes="300px")}</div><h3>Медальйон</h3><p>Центр композиції — спіраль у колі. У спіралях трипільського орнаменту дослідники вбачають плин часу, відродження та циклічність життя.</p></figure>
    <figure class="rv"><div class="pic lg">{img("photo/edem/pendant-round.webp", "Кругла золота підвіска з двома спіралями", sizes="300px")}</div><h3>Підвіски</h3><p>Круглі золоті підвіски на плетених синіх шнурах оточують медальйон — вісім, по дві з кожного боку.</p></figure>
    <figure class="rv"><div class="pic">{img("photo/edem/pendant-diamond.webp", "Ромбовидна золота підвіска з орнаментом", sizes="300px")}</div><h3>Ромби</h3><p>Чотири ромбовидні підвіски тримають композицію по діагоналях і замикають її в раму.</p></figure>
  </div>
</div></section>

<section class="s" id="brands"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Партнери</p><h2>Два бренди. Одна філософія. Спільне мистецтво.</h2><p class="lead">Ідея проєкту сформувалася на перетині цінностей KRAЇNA EDEM та OBIIMY: культурна спадщина — не лише історія минулого, а жива частина нашої ідентичності.</p></div>
  <div class="brands">
    <article class="rv"><p class="eyebrow">Партнер</p><h3>KRAЇNA EDEM</h3>
      <p>Збереження й популяризація української культурної спадщини вже багато років є невід’ємною частиною філософії KRAЇNA EDEM — через культурні ініціативи, мистецькі проєкти та простори, присвячені творчості.</p>
      <ul><li>Park3020 — парк сучасної української скульптури, де мистецтво взаємодіє з природою</li><li>Підтримка українських митців і популяризація сучасного мистецтва</li></ul></article>
    <article class="rv"><p class="eyebrow">Бренд</p><h3>OBIIMY</h3>
      <p>Український бренд шовкових хусток і аксесуарів з авторськими принтами. Засновниця й художниця — Світлана Сніжко: перші колекції виросли з її картин.</p>
      <ul><li>100% натуральний шовк, ручна обробка краю</li><li>Авторські принти, виготовлено в Україні</li><li>Шоурум: Київ, вул. Петра Сагайдачного, 12</li></ul></article>
  </div>
</div></section>

<section class="reg" id="register"><div class="wrap">
  <div class="rv rtext">
    <p class="eyebrow">Як придбати</p>
    <h2>Ранній доступ до випуску</h2>
    <p class="lead">Ціну й дату старту підтверджуємо з партнером. Щойно вони відомі — зареєстровані дізнаються першими й отримують персональне посилання на оплату.</p>
  </div>
  <div class="rv rsteps">
    <div class="steps">
      <div><h3>Реєстрація</h3><p>Залиште ім’я, телефон і позначте, що вас цікавить.</p></div>
      <div><h3>Персональне посилання</h3><p>Коли продажі відкриються, надішлемо вам посилання на оплату.</p></div>
      <div><h3>Підтвердження й доставка</h3><p>Після оплати — підтвердження замовлення та відправлення хустки.</p></div>
    </div>
    <div class="contacts">Питання: <a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="{TG}" target="_blank" rel="noopener">Telegram</a></div>
  </div>
  <div class="rv rform">
  <form class="f" id="reg" novalidate>
    <label><span>Ім’я *</span><input name="name" type="text" autocomplete="name" required aria-describedby="err-name"><span class="err" id="err-name" role="alert">Вкажіть ім’я</span></label>
    <label><span>Телефон *</span><input name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+380" required aria-describedby="err-phone"><span class="err" id="err-phone" role="alert">Вкажіть телефон, щонайменше 9 цифр</span></label>
    <label class="full"><span>Email <small style="font-weight:400">(необов’язково)</small></span><input name="email" type="email" autocomplete="email"></label>
    <fieldset><legend>Що вас цікавить</legend><div class="radios">
      <label><input type="radio" name="interest" value="Планую придбати на старті"> Планую придбати на старті</label>
      <label><input type="radio" name="interest" value="Хочу дізнатися ціну"> Хочу дізнатися ціну</label>
      <label><input type="radio" name="interest" value="Розглядаю як подарунок"> Розглядаю як подарунок</label>
    </div></fieldset>
    <div class="actions"><button class="btn btn-gold" type="submit">Забронювати ранній доступ</button><span class="hint">Без розсилок — лише повідомлення про цей запуск.<br>* обов’язкові поля</span></div>
  </form>
  <div class="done" id="reg-done" hidden>
    <h3 id="done-h">Дякуємо — ви в списку раннього доступу</h3>
    <p id="done-p">Ви першими дізнаєтеся про ціну та відкриття продажів. Якщо є запитання — напишіть нам у Telegram.</p>
    <div class="row"><a class="btn btn-gold" id="reg-tg" href="{TG}" target="_blank" rel="noopener">Написати в Telegram</a><a class="btn btn-line" href="#top">На початок</a></div>
  </div>
  </div>
</div></section>
</main>
<footer><div class="wrap">
  <span>KRAЇNA EDEM × OBIIMY · Trypillia — The Art of Origins · 2026</span>
  <span><a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="https://obiimy.world/" target="_blank" rel="noopener">obiimy.world</a></span>
</div></footer>
<script>
(function () {{
  var API = /^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname) ? '{API_LOCAL}' : '{API_PROD}';
  var f = document.getElementById('reg'), done = document.getElementById('reg-done'), tg = document.getElementById('reg-tg');
  function valid(n, v) {{ return n === 'phone' ? v.replace(/\\D/g, '').length >= 9 : v.length > 1; }}
  f.addEventListener('submit', function (e) {{
    e.preventDefault();
    var bad = null;
    ['name', 'phone'].forEach(function (n) {{ var el = f.elements[n], lab = el.closest('label'), ok = valid(n, el.value.trim()); lab.classList.toggle('bad', !ok); el.setAttribute('aria-invalid', ok ? 'false' : 'true'); if (!ok && !bad) bad = el; }});
    if (bad) {{ bad.focus(); return; }}
    var data = {{ name: f.elements.name.value.trim(), phone: f.elements.phone.value.trim(), email: f.elements.email.value.trim(), interest: (f.querySelector('input[name=interest]:checked') || {{}}).value || '', note: '', page: location.href }};
    var btn = f.querySelector('button'); btn.disabled = true; btn.textContent = 'Надсилаємо…';
    var text = 'Ранній доступ · Trypillia — The Art of Origins\\n' + 'Ім’я: ' + data.name + '\\nТелефон: ' + data.phone + (data.email ? '\\nEmail: ' + data.email : '') + (data.interest ? '\\nІнтерес: ' + data.interest : '');
    tg.href = '{TG}?text=' + encodeURIComponent(text);
    function finish(ok) {{
      if (!ok) {{ document.getElementById('done-h').textContent = 'Заявку не надіслано'; document.getElementById('done-p').textContent = 'Не вдалося надіслати заявку автоматично. Натисніть «Написати в Telegram» — текст уже підготовлено.'; }}
      f.hidden = true; done.hidden = false; var h = document.getElementById('done-h'); h.setAttribute('tabindex', '-1'); h.focus();
    }}
    fetch(API + '/api/edem', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify(data) }})
      .then(function (r) {{ return r.json(); }}).then(function (j) {{ if (!j.ok) throw new Error(j.error || 'x'); finish(true); }})
      .catch(function () {{ finish(false); }});
  }});
  ['name', 'phone'].forEach(function (n) {{ f.elements[n].addEventListener('input', function () {{ this.closest('label').classList.remove('bad'); this.removeAttribute('aria-invalid'); }}); }});
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {{
    var io = new IntersectionObserver(function (es) {{ es.forEach(function (e) {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }}); }}, {{ rootMargin: '0px 0px -8% 0px', threshold: .05 }});
    document.querySelectorAll('.rv').forEach(function (el, i) {{ el.style.transitionDelay = (i % 4) * 70 + 'ms'; io.observe(el); }});
  }} else {{ document.querySelectorAll('.rv').forEach(function (el) {{ el.classList.add('in'); }}); }}
}})();
</script>'''
    head = f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KRAЇNA EDEM × OBIIMY — Trypillia: The Art of Origins · шовкова хустка 88 × 88</title>
<meta name="description" content="Спільний мистецький проєкт KRAЇNA EDEM та OBIIMY: шовкова хустка 88 × 88, натхненна трипільською культурою. Лімітований випуск — зареєструйтесь, щоб дізнатися про ціну та старт продажів першими.">
<link rel="canonical" href="{SITE_URL}/edem">
<meta property="og:type" content="website"><meta property="og:title" content="KRAЇNA EDEM × OBIIMY — Trypillia: The Art of Origins"><meta property="og:description" content="Шовкова хустка 88 × 88, натхненна трипільською культурою. Лімітований випуск двох брендів — ранній доступ за реєстрацією."><meta property="og:image" content="{SITE_URL}/photo/edem/art-1600-1200.webp"><meta property="og:url" content="{SITE_URL}/edem"><meta property="og:locale" content="uk_UA">
<link rel="icon" href="brand/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>'''
    html = head + typo(body) + variants_bar("edem")
    (ROOT / "edem.html").write_text(html)
    print("edem", len(html) // 1024, "KB")

if __name__ == "__main__":
    main()
