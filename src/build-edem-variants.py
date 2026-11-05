#!/usr/bin/env python3
"""Three design variants of the KRAЇNA EDEM × OBIIMY landing (client asked for «unusual and beautiful», 02.11.2026). Same copy,
facts, pictures and registration API as src/build-edem.py (the «classic»); only the staging differs:
  edem-gold   — a dark warm hall: the medallion turns slowly behind the headline, chapters with roman numerals, a marquee of symbols;
  edem-museum — an exhibition catalogue on paper: sticky index, numbered plates «Fig. 01», a dimension line of 88 cm, the manifesto as a page;
  edem-zoom   — a scroll-driven journey into the print: a sticky stage zooms from the whole scarf into the medallion while four captions pass.
Output: edem-gold.html, edem-museum.html, edem-zoom.html (HIDDEN in build-site: deployed, linked from the variants bar, not in the hub)."""
import importlib.util, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from imgs import img, typo
_spec = importlib.util.spec_from_file_location("edem", ROOT / "src" / "build-edem.py"); edem = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(edem)
PHONE, PHONE_HREF, MAIL, TG, API_LOCAL, API_PROD, SITE_URL = edem.PHONE, edem.PHONE_HREF, edem.MAIL, edem.TG, edem.API_LOCAL, edem.API_PROD, edem.SITE_URL

# ─── shared copy (the press release and the deck) ─────────────────────────────────────────────────────────────────────────────
MANIFESTO = "Є речі, які неможливо виміряти часом. <b>Пам’ять землі.</b> Символи, що пережили тисячоліття. Образи, які залишили нам давні покоління. І культурний код, який продовжує жити, навіть коли змінюються епохи."
STORY = ["Задовго до сучасних кордонів і держав на землях нинішньої України розвивалися давні культури, які залишили по собі унікальну мистецьку спадщину. Особливе місце серед них посідає трипільська культура — одна з найяскравіших археологічних культур давньої Європи, що існувала впродовж VI–IV тисячоліть до нашої ери.",
         "Сьогодні ці стародавні знаки набувають нового звучання. Ми не можемо повернути час, але можемо зберегти пам’ять про тих, хто жив до нас, — відкрити для себе їхнє мистецтво й відчути зв’язок із землею, її історією та культурними витоками."]
SYMBOLS = [("figure", "Пластика", "Жіноча фігурка зі спіральним орнаментом — образ трипільської пластики, який чотири рази повторюється на полотні хустки.", "Золота жіноча фігурка зі спіралями — трипільська пластика в принті"),
           ("mandala", "Медальйон", "Центр композиції — спіраль у колі. У спіралях трипільського орнаменту дослідники вбачають плин часу, відродження та циклічність життя.", "Центральний медальйон принту: спіраль у золоті й синьому"),
           ("pendant-round", "Підвіски", "Круглі золоті підвіски на плетених синіх шнурах оточують медальйон — вісім, по дві з кожного боку.", "Кругла золота підвіска з двома спіралями"),
           ("pendant-diamond", "Ромби", "Чотири ромбовидні підвіски тримають композицію по діагоналях і замикають її в раму.", "Ромбовидна золота підвіска з орнаментом")]
SPEC = [("Розмір", "88 × 88 см"), ("Матеріал", "100% натуральний шовк"), ("Принт", "Авторський, спільний для двох брендів"), ("Підпис", "OBIIMY × Edem на полотні"), ("Наклад", "Обмежений"), ("Виготовлено", "в Україні")]
EDEM_P = "Збереження й популяризація української культурної спадщини вже багато років є невід’ємною частиною філософії KRAЇNA EDEM — через культурні ініціативи, мистецькі проєкти та простори, присвячені творчості."
EDEM_L = ["Park3020 — парк сучасної української скульптури, де мистецтво взаємодіє з природою", "Підтримка українських митців і популяризація сучасного мистецтва"]
OB_P = "Український бренд шовкових хусток і аксесуарів з авторськими принтами. Засновниця й художниця — Світлана Сніжко: перші колекції виросли з її картин."
OB_L = ["100% натуральний шовк, ручна обробка краю", "Авторські принти, виготовлено в Україні", "Шоурум: Київ, вул. Петра Сагайдачного, 12"]
STEPS = [("Реєстрація", "Залиште ім’я, телефон і позначте, що вас цікавить."), ("Персональне посилання", "Коли продажі відкриються, надішлемо вам посилання на оплату."), ("Підтвердження й доставка", "Після оплати — підтвердження замовлення та відправлення хустки.")]

def form_html(dark=False):
    return f'''
  <form class="f" id="reg" novalidate>
    <label><span>Ім’я *</span><input name="name" type="text" autocomplete="name" required aria-describedby="err-name"><span class="err" id="err-name" role="alert">Вкажіть ім’я</span></label>
    <label><span>Телефон *</span><input name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+380" required aria-describedby="err-phone"><span class="err" id="err-phone" role="alert">Вкажіть телефон, щонайменше 9 цифр</span></label>
    <label class="full"><span>Email <small style="font-weight:400">(необов’язково)</small></span><input name="email" type="email" autocomplete="email"></label>
    <fieldset><legend>Що вас цікавить</legend><div class="radios">
      <label><input type="radio" name="interest" value="Планую придбати на старті"> Планую придбати на старті</label>
      <label><input type="radio" name="interest" value="Хочу дізнатися ціну"> Хочу дізнатися ціну</label>
      <label><input type="radio" name="interest" value="Розглядаю як подарунок"> Розглядаю як подарунок</label>
    </div></fieldset>
    <div class="actions"><button class="btn btn-main" type="submit">Забронювати ранній доступ</button><span class="hint">Без розсилок — лише повідомлення про цей запуск.<br>* обов’язкові поля</span></div>
  </form>
  <div class="done" id="reg-done" hidden>
    <h3 id="done-h">Дякуємо — ви в списку раннього доступу</h3>
    <p id="done-p">Ви першими дізнаєтеся про ціну та відкриття продажів. Якщо є запитання — напишіть нам у Telegram.</p>
    <div class="row"><a class="btn btn-main" id="reg-tg" href="{TG}" target="_blank" rel="noopener">Написати в Telegram</a><a class="btn btn-line" href="#top">На початок</a></div>
  </div>'''

FORM_CSS = """
form.f { display: grid; grid-template-columns: 1fr 1fr; gap: 18px 16px; }
form.f label { display: grid; gap: 7px; font-size: 13px; font-weight: 600; letter-spacing: .04em; }
form.f label.full, form.f fieldset { grid-column: 1 / -1; }
form.f input { font: inherit; font-size: 16px; padding: 13px 14px; border: 1px solid var(--fb); border-radius: 2px; background: var(--fbg); color: var(--fink); width: 100%; }
form.f select, form.f textarea { font: inherit; font-size: 16px; padding: 13px 14px; border: 1px solid var(--fb); border-radius: 2px; background: var(--fbg); color: var(--fink); width: 100%; }
form.f textarea { min-height: 88px; resize: vertical; } form.f select { appearance: none; -webkit-appearance: none; background-image: linear-gradient(45deg, transparent 50%, currentColor 50%), linear-gradient(135deg, currentColor 50%, transparent 50%); background-position: calc(100% - 20px) 50%, calc(100% - 15px) 50%; background-size: 5px 5px; background-repeat: no-repeat; padding-right: 36px; }
form.f input:focus, form.f select:focus, form.f textarea:focus { outline: 2px solid var(--acc); outline-offset: 1px; border-color: transparent; }
form.f .total { grid-column: 1 / -1; display: flex; justify-content: space-between; align-items: baseline; gap: 16px; padding: 16px 0 4px; border-top: 1px solid var(--fb); font-size: 14px; } form.f .total b { font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 600; font-size: 30px; letter-spacing: .01em; }
form.f fieldset { border: 0; margin: 0; padding: 0; } form.f legend { font-size: 13px; font-weight: 600; letter-spacing: .04em; padding: 0; margin-bottom: 10px; }
form.f .radios { display: flex; flex-direction: column; gap: 6px; }
form.f .radios label { display: inline-flex; align-items: center; gap: 10px; font-weight: 500; font-size: 15px; letter-spacing: 0; padding: 6px 0; cursor: pointer; }
form.f .radios input { width: 17px; height: 17px; padding: 0; margin: 0; accent-color: var(--acc); }
form.f .actions { grid-column: 1 / -1; display: flex; flex-wrap: wrap; gap: 14px 20px; align-items: center; margin-top: 6px; }
form.f .hint { font-size: 13px; opacity: .75; }
form.f .err { color: #C0392B; font-size: 13px; display: none; } form.f label.bad .err { display: block; } form.f label.bad input { border-color: #C0392B; }
.done h3 { font-size: 34px; } .done p { margin-top: 14px; opacity: .85; } .done .row { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 22px; }
.btn { display: inline-flex; align-items: center; gap: 12px; padding: 17px 30px; border-radius: 2px; font-weight: 500; font-size: 13px; letter-spacing: .12em; text-transform: uppercase; text-decoration: none; border: 1px solid transparent; cursor: pointer; font-family: Montserrat, Arial, sans-serif; transition: background .2s, color .2s; }
.rv { opacity: 0; transform: translateY(22px); transition: opacity .7s cubic-bezier(.2,.7,.2,1), transform .7s cubic-bezier(.2,.7,.2,1); } .rv.in { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) { .rv { opacity: 1; transform: none; transition: none; } * { animation: none !important; } }
@media (max-width: 600px) { form.f { grid-template-columns: 1fr; } }
"""

SCRIPT = """
<script>
(function () {
  var API = /^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname) ? 'API_LOCAL' : 'API_PROD';
  var f = document.getElementById('reg'), done = document.getElementById('reg-done'), tg = document.getElementById('reg-tg');
  function valid(n, v) { return n === 'phone' ? v.replace(/\\D/g, '').length >= 9 : v.length > 1; }
  var req = [].filter.call(f.elements, function (el) { return el.required && el.name; });
  function label(el) { var l = el.closest('label'), s = l && l.querySelector('span'); return (s ? s.textContent : el.closest('fieldset') ? el.closest('fieldset').querySelector('legend').textContent : el.name).replace(/\\s*\\*.*$/, '').replace(/\\(.*\\)/, '').trim(); }
  f.addEventListener('submit', function (e) {
    e.preventDefault(); var bad = null;
    req.forEach(function (el) { var lab = el.closest('label'), ok = valid(el.name, el.value.trim()); lab.classList.toggle('bad', !ok); el.setAttribute('aria-invalid', ok ? 'false' : 'true'); if (!ok && !bad) bad = el; });
    if (bad) { bad.focus(); return; }
    var S = function (k, d) { return f.getAttribute('data-' + k) || d; };
    var data = { page: location.href, kind: S('kind', 'register') }, lines = [S('title', 'Ранній доступ · Trypillia — The Art of Origins')];
    [].forEach.call(f.elements, function (el) { if (!el.name || el.type === 'submit' || ((el.type === 'radio' || el.type === 'checkbox') && !el.checked)) return; data[el.name] = el.value.trim(); if (data[el.name]) lines.push(label(el) + ': ' + data[el.name]); });
    if (f.getAttribute('data-total')) { data.total = f.getAttribute('data-total'); lines.push(S('total-label', 'Разом') + ': ' + data.total); }
    var btn = f.querySelector('button[type=submit]'); btn.disabled = true; btn.textContent = S('sending', 'Надсилаємо…');
    tg.href = 'TG?text=' + encodeURIComponent(lines.join('\\n'));
    function finish(ok) { if (!ok) { var o = data.kind === 'order'; document.getElementById('done-h').textContent = S('fail-h', (o ? 'Замовлення' : 'Заявку') + ' не надіслано'); document.getElementById('done-p').textContent = S('fail-p', 'Не вдалося надіслати ' + (o ? 'замовлення' : 'заявку') + ' автоматично. Натисніть «Написати в Telegram» — текст уже підготовлено.'); } f.hidden = true; done.hidden = false; var h = document.getElementById('done-h'); h.setAttribute('tabindex', '-1'); h.focus(); }
    fetch(API + '/api/edem', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }).then(function (r) { return r.json(); }).then(function (j) { if (!j.ok) throw new Error('x'); finish(true); }).catch(function () { finish(false); });
  });
  req.forEach(function (el) { el.addEventListener('input', function () { this.closest('label').classList.remove('bad'); this.removeAttribute('aria-invalid'); }); });
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px', threshold: .05 });
    document.querySelectorAll('.rv').forEach(function (el, i) { el.style.transitionDelay = (i % 4) * 70 + 'ms'; io.observe(el); });
  } else { document.querySelectorAll('.rv').forEach(function (el) { el.classList.add('in'); }); }
  EXTRA
})();
</script>""".replace("API_LOCAL", API_LOCAL).replace("API_PROD", API_PROD).replace("TG?text", TG + "?text")

DESC = "Спільний мистецький проєкт KRAЇNA EDEM та OBIIMY: шовкова хустка 88 × 88, натхненна трипільською культурою. Лімітований випуск — зареєструйтесь, щоб дізнатися про ціну та старт продажів першими."
def head(slug, css, title_extra="", url=None, index=False, desc=DESC, lang="uk", extra=""):
    return f'''<html lang="{lang}">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KRAЇNA EDEM × OBIIMY — Trypillia: The Art of Origins{title_extra}</title>
<meta name="description" content="{desc}">
{"" if index else '<meta name="robots" content="noindex">'}<link rel="canonical" href="{url or SITE_URL + "/edem"}">
<meta property="og:type" content="website"><meta property="og:title" content="KRAЇNA EDEM × OBIIMY — Trypillia: The Art of Origins"><meta property="og:image" content="{SITE_URL}/photo/edem/art-1600-1200.webp"><meta property="og:url" content="{url or SITE_URL + "/" + slug}"><meta property="og:locale" content="{"en_US" if lang == "en" else "uk_UA"}">{extra}
<link rel="icon" href="brand/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style>'''

def write(slug, css, body, extra_js="", **kw):
    html = head(slug, css, **kw) + typo(body) + SCRIPT.replace("EXTRA", extra_js) + edem.variants_bar(slug)
    (ROOT / f"{slug}.html").write_text(html); print(slug, len(html) // 1024, "KB")

def spec_rows(): return "".join(f"<div><span>{k}</span><b>{v}</b></div>" for k, v in SPEC)
def sym_img(k, alt, sizes="300px"): return img(f"photo/edem/{k}.webp", alt, sizes=sizes)

# ═══ A · GOLD — a dark warm hall ═══════════════════════════════════════════════════════════════════════════════════════════
GOLD_CSS = """
:root { --bg: #1C1410; --bg2: #26190F; --cream: #F3E9D8; --cream2: rgba(243,233,216,.7); --gold: #D9B86A; --gold2: #B48A3A; --line: rgba(217,184,106,.28); --acc: #D9B86A; --fb: rgba(42,32,23,.3); --fbg: #FBF4E7; --fink: #2A2017; }
* { box-sizing: border-box; } html { scroll-behavior: smooth; }
body { margin: 0; background: var(--bg); color: var(--cream); font-family: Montserrat, Arial, sans-serif; font-size: 17px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
img { max-width: 100%; height: auto; display: block; } p { margin: 0; } a { color: inherit; } figure { margin: 0; }
h1, h2, h3 { margin: 0; font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 400; line-height: 1.02; text-wrap: balance; }
.wrap { max-width: 1240px; margin: 0 auto; padding: 0 24px; }
section[id] { scroll-margin-top: 20px; }
.eyebrow { font-size: 11px; font-weight: 600; letter-spacing: .28em; text-transform: uppercase; color: var(--gold); }
.chap { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 15px; letter-spacing: .3em; color: var(--gold); }
.btn-main { background: var(--gold); color: #1C1410; } .btn-main:hover { background: #E8CB84; }
.btn-line { border-color: rgba(243,233,216,.6); color: var(--cream); } .btn-line:hover { border-color: var(--cream); }
/* hero: the medallion turning behind, gold frame lines like the scarf border */
.hero { position: relative; min-height: 100vh; display: grid; place-items: center; overflow: hidden; padding: 90px 0 60px; }
.hero .frame { position: absolute; inset: 22px; border: 1px solid var(--line); pointer-events: none; } .hero .frame::after { content: ""; position: absolute; inset: 8px; border: 1px solid rgba(217,184,106,.14); }
.hero .disc { position: absolute; left: 50%; top: 50%; width: min(140vh, 1500px); height: min(140vh, 1500px); transform: translate(-50%, -50%); opacity: .14; filter: saturate(.5) sepia(.6); animation: spin 140s linear infinite; pointer-events: none; }
.hero .disc img { width: 100%; height: 100%; object-fit: contain; }
@keyframes spin { to { transform: translate(-50%, -50%) rotate(360deg); } }
.hero .in { position: relative; display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: clamp(28px, 5vw, 80px); align-items: center; width: 100%; max-width: 1240px; padding: 0 24px; }
.hero .top { position: absolute; left: 24px; right: 24px; top: 34px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; letter-spacing: .22em; text-transform: uppercase; color: var(--cream2); }
.hero h1 { font-size: clamp(50px, 7vw, 108px); color: var(--cream); } .hero h1 i { font-style: italic; color: var(--gold); }
.hero .lead { font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(22px, 2.2vw, 30px); font-weight: 300; line-height: 1.35; color: var(--cream2); max-width: 28em; margin-top: 26px; }
.hero .cta { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 38px; }
.hero .facts { display: flex; flex-wrap: wrap; gap: 10px 26px; margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--line); font-size: 12px; letter-spacing: .1em; text-transform: uppercase; color: var(--cream2); } .hero .facts b { color: var(--gold); }
.hero .art img { width: 100%; height: auto; filter: drop-shadow(0 50px 70px rgba(0,0,0,.6)); transform: rotate(-5deg); }
.hang { position: absolute; top: 23px; width: 92px; display: flex; flex-direction: column; align-items: center; z-index: 2; transform-origin: 50% 0; animation: sway 9s ease-in-out infinite; } .hang i { display: block; width: 1px; background: linear-gradient(180deg, var(--gold), rgba(217,184,106,.4)); } .hang img { width: 100%; height: auto; filter: drop-shadow(0 18px 24px rgba(0,0,0,.7)); }
.hang.l { left: 34px; width: 68px; } .hang.l i { height: 150px; } .hang.r { right: 7%; animation-delay: -4s; } .hang.r i { height: 90px; }
@keyframes sway { 0%, 100% { transform: rotate(-1.6deg); } 50% { transform: rotate(1.6deg); } }
@media (max-width: 980px) { .hang { display: none; } }
/* marquee of symbols */
.marq { overflow: hidden; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); padding: 26px 0; background: var(--bg2); }
.marq .track { display: flex; gap: 64px; width: max-content; animation: slide 46s linear infinite; }
.marq .it { display: flex; align-items: center; gap: 22px; font-family: 'Cormorant Garamond', Georgia, serif; font-size: 28px; color: var(--cream2); white-space: nowrap; } .marq .it img { height: 64px; width: auto; filter: drop-shadow(0 8px 10px rgba(0,0,0,.5)); }
.marq .it i { color: var(--gold); font-style: normal; font-size: 18px; letter-spacing: .3em; }
@keyframes slide { to { transform: translateX(-50%); } }
/* chapters */
section.s { padding: clamp(80px, 10vw, 150px) 0; }
.head { display: grid; grid-template-columns: 120px minmax(0, 1fr); gap: 24px; align-items: start; margin-bottom: clamp(34px, 4vw, 60px); }
.head h2 { font-size: clamp(38px, 4.8vw, 68px); color: var(--cream); }
.head .sub { font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(20px, 2vw, 26px); font-weight: 300; color: var(--cream2); margin-top: 16px; max-width: 34em; }
.mani blockquote { margin: 0; font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(30px, 4.4vw, 66px); font-weight: 300; line-height: 1.15; text-align: center; max-width: 20em; margin: 0 auto; } .mani b { color: var(--gold); font-weight: 400; }
.mani .orn { width: 120px; margin: 0 auto 34px; opacity: .9; }
.cols { display: grid; grid-template-columns: 120px minmax(0, 1fr) minmax(0, 1fr); gap: 24px clamp(28px, 4vw, 64px); align-items: center; }
.text { color: var(--cream2); } .text p + p { margin-top: 1.1em; }
.fig img { width: 100%; height: auto; border: 1px solid var(--line); padding: 10px; background: #15100C; }
.fig figcaption { margin-top: 12px; font-size: 12px; letter-spacing: .1em; text-transform: uppercase; color: var(--cream2); }
.sym4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 40px; }
.sym4 .pic { height: 280px; display: flex; align-items: center; justify-content: center; border: 1px solid var(--line); background: radial-gradient(60% 60% at 50% 55%, rgba(217,184,106,.12), transparent 70%); }
.sym4 .pic img { max-height: 76%; width: auto; filter: drop-shadow(0 20px 26px rgba(0,0,0,.6)); } .sym4 .pic.lg img { transform: scale(1.3); }
.sym4 h3 { font-size: 30px; margin-top: 22px; color: var(--cream); } .sym4 .n { font-family: 'Cormorant Garamond', serif; color: var(--gold); letter-spacing: .3em; font-size: 14px; margin-right: 10px; }
.sym4 p { margin-top: 10px; font-size: 15px; color: var(--cream2); }
.scarf { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, .8fr); gap: clamp(28px, 4vw, 72px); align-items: start; }
.scarf .full img { width: 100%; height: auto; border: 1px solid var(--line); padding: 14px; background: #15100C; box-shadow: 0 60px 100px -50px rgba(0,0,0,.9); }
.scarf .zoom { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px; } .scarf .zoom img { width: 100%; height: auto; aspect-ratio: 1; object-fit: cover; }
.scarf .zoom figcaption { margin-top: 10px; font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--cream2); }
.scarf > div:last-child { position: sticky; top: 90px; }
.spec div { display: flex; justify-content: space-between; gap: 20px; padding: 16px 0; border-bottom: 1px solid var(--line); font-size: 15px; } .spec div span { color: var(--cream2); } .spec div b { font-weight: 500; color: var(--gold); text-align: right; }
.note { margin-top: 24px; font-family: 'Cormorant Garamond', serif; font-size: 22px; color: var(--cream2); font-style: italic; }
.brands { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 48px; } .brands article { border-top: 1px solid var(--gold); padding-top: 26px; }
.brands h3 { font-size: 34px; letter-spacing: .06em; color: var(--cream); } .brands p { margin-top: 14px; color: var(--cream2); }
.brands ul { margin: 16px 0 0; padding: 0; list-style: none; } .brands li { padding: 10px 0; border-top: 1px solid var(--line); font-size: 15px; color: var(--cream2); }
.reg { background: var(--cream); color: var(--fink); padding: clamp(70px, 9vw, 130px) 0; }
.reg .wrap { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: clamp(32px, 5vw, 80px); align-items: start; }
.reg .eyebrow { color: var(--gold2); } .reg h2 { font-size: clamp(36px, 4.4vw, 60px); margin-top: 14px; color: #2A2017; }
.reg .lead { font-family: 'Cormorant Garamond', serif; font-size: clamp(20px, 2vw, 26px); color: #5A4B3C; margin-top: 18px; }
.steps { margin-top: 30px; counter-reset: st; } .steps div { position: relative; padding: 16px 0 16px 60px; border-top: 1px solid rgba(42,32,23,.14); }
.steps div::before { counter-increment: st; content: "0" counter(st); position: absolute; left: 0; top: 14px; font-family: 'Cormorant Garamond', serif; font-size: 32px; color: var(--gold2); }
.steps h3 { font-size: 24px; color: #2A2017; } .steps p { margin-top: 4px; font-size: 15px; color: #5A4B3C; }
.reg .contacts { margin-top: 28px; font-size: 15px; color: #5A4B3C; } .reg .contacts a { color: #2A2017; }
.reg .btn-main { background: #2A2017; color: var(--cream); } .reg .btn-line { border-color: #2A2017; color: #2A2017; }
.reg form.f label, .reg form.f legend { color: #5A4B3C; } .reg .done h3 { color: #2A2017; }
footer { padding: 34px 0 44px; font-size: 12px; color: var(--cream2); letter-spacing: .04em; } footer .wrap { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px 30px; } footer a { text-decoration: none; }
@media (max-width: 980px) { .hero .in, .cols, .scarf, .reg .wrap, .brands { grid-template-columns: 1fr; } .head { grid-template-columns: 1fr; gap: 10px; } .cols .chap { display: none; } .scarf > div:last-child { position: static; } .sym4 { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 28px 20px; } .hero .art { max-width: 460px; margin: 0 auto; } .hero .top { font-size: 10px; } }
@media (max-width: 600px) { body { font-size: 16px; } .sym4 { grid-template-columns: 1fr; } .hero .cta .btn { flex: 1 1 100%; justify-content: center; } .hero { padding-top: 110px; } }
"""

def gold():
    marq_items = "".join(f'<span class="it">{img(f"photo/edem/{k}.webp", a, sizes="80px")}<span>{t}</span><i>✦</i></span>' for k, t, _, a in SYMBOLS)
    body = f'''
<main id="top">
<section class="hero">
  <div class="frame"></div>
  <div class="disc" aria-hidden="true">{img("photo/edem/mandala.webp", "", sizes="1500px")}</div>
  <div class="top"><span>Kraїna Edem × Obiimy</span><span>Лімітований випуск · 2026</span></div>
  <div class="hang l" aria-hidden="true"><i></i>{img("photo/edem/pendant-round.webp", "", sizes="92px", lazy=False)}</div><div class="hang r" aria-hidden="true"><i></i>{img("photo/edem/pendant-diamond.webp", "", sizes="92px", lazy=False)}</div>
  <div class="in">
    <div>
      <p class="eyebrow">Спільний мистецький проєкт</p>
      <h1 style="margin-top:20px">Trypillia —<br><i>The Art of Origins</i></h1>
      <p class="lead">Мистецтво бути ближче. Шовкова хустка за трипільськими мотивами — спільна робота KRAЇNA EDEM та OBIIMY.</p>
      <div class="cta"><a class="btn btn-main" href="#register">Отримати ранній доступ</a><a class="btn btn-line" href="#story">Про проєкт</a></div>
      <div class="facts"><span><b>88 × 88</b> см</span><span><b>100%</b> шовк</span><span>Обмежений наклад</span><span>Підпис OBIIMY × Edem</span></div>
    </div>
    <div class="art">{img("photo/edem/scarf.webp", "Хустка KRAЇNA EDEM × OBIIMY «Trypillia — The Art of Origins», 88 × 88", sizes="(max-width: 980px) 90vw, 44vw", lazy=False, eager_priority=True)}</div>
  </div>
</section>
<div class="marq" aria-hidden="true"><div class="track">{marq_items}{marq_items}</div></div>

<section class="s mani" id="manifest"><div class="wrap rv">
  <div class="orn">{img("photo/edem/pendant-round.webp", "", sizes="120px")}</div>
  <blockquote>{MANIFESTO}</blockquote>
</div></section>

<section class="s" id="scarf" style="background:var(--bg2)"><div class="wrap">
  <div class="head"><p class="chap rv">I</p><div class="rv"><h2>Мистецьке полотно, яке можна носити</h2><p class="sub">Хустка тут — більше, ніж аксесуар: мистецьке полотно, що поєднує сучасний дизайн із пам’яттю про давні культури.</p></div></div>
  <div class="scarf">
    <div class="rv"><div class="full">{img("photo/edem/art-1600.webp", "Принт хустки «Trypillia — The Art of Origins» повністю", sizes="(max-width: 980px) 92vw, 58vw")}</div>
      <div class="zoom"><figure>{img("photo/edem/art-pendants.webp", "Гроно підвісок на плетених шнурах — фрагмент принту", sizes="28vw")}<figcaption>Підвіски на шнурах</figcaption></figure><figure>{img("photo/edem/art-sign.webp", "Підпис OBIIMY × Edem на полотні хустки", sizes="28vw")}<figcaption>Підпис двох брендів</figcaption></figure></div></div>
    <div class="rv"><div class="spec">{spec_rows()}</div><p class="note">Ціну й дату старту повідомимо зареєстрованим першими.</p><p style="margin-top:26px"><a class="btn btn-main" href="#register">Отримати ранній доступ</a></p></div>
  </div>
</div></section>

<section class="s" id="story"><div class="wrap">
  <div class="cols">
    <p class="chap rv">II</p>
    <div class="rv"><h2 style="font-size:clamp(38px,4.8vw,68px)">Історія, що живе в нас</h2><div class="text" style="margin-top:26px">{"".join(f"<p>{t}</p>" for t in STORY)}</div></div>
    <figure class="fig rv">{img("photo/edem/art-corner.webp", "Фрагмент принту: трипільська фігурка й плетені шнури на кутку хустки", sizes="(max-width: 980px) 92vw, 40vw")}<figcaption>Фрагмент принту · кут хустки</figcaption></figure>
  </div>
</div></section>

<section class="s" id="symbols" style="background:var(--bg2)"><div class="wrap">
  <div class="head"><p class="chap rv">III</p><div class="rv"><h2>Кожна деталь має значення</h2><p class="sub">Давні орнаментальні мотиви й символічні образи — переосмислені мовою сучасного дизайну, у золоті й глибокому синьому.</p></div></div>
  <div class="sym4">{"".join(f'<figure class="rv"><div class="pic{" lg" if k == "pendant-round" else ""}">{sym_img(k, a)}</div><h3><span class="n">0{i + 1}</span>{t}</h3><p>{d}</p></figure>' for i, (k, t, d, a) in enumerate(SYMBOLS))}</div>
</div></section>

<section class="s" id="brands"><div class="wrap">
  <div class="head"><p class="chap rv">IV</p><div class="rv"><h2>Два бренди. Одна філософія.</h2><p class="sub">Культурна спадщина — не лише історія минулого, а жива частина нашої ідентичності.</p></div></div>
  <div class="brands">
    <article class="rv"><p class="eyebrow">Партнер</p><h3 style="margin-top:12px">KRAЇNA EDEM</h3><p>{EDEM_P}</p><ul>{"".join(f"<li>{x}</li>" for x in EDEM_L)}</ul></article>
    <article class="rv"><p class="eyebrow">Бренд</p><h3 style="margin-top:12px">OBIIMY</h3><p>{OB_P}</p><ul>{"".join(f"<li>{x}</li>" for x in OB_L)}</ul></article>
  </div>
</div></section>

<section class="reg" id="register"><div class="wrap">
  <div class="rv"><p class="eyebrow">Як придбати</p><h2>Ранній доступ до випуску</h2><p class="lead">Ціну й дату старту підтверджуємо з партнером. Щойно вони відомі — зареєстровані дізнаються першими й отримують персональне посилання на оплату.</p>
    <div class="steps">{"".join(f"<div><h3>{t}</h3><p>{d}</p></div>" for t, d in STEPS)}</div>
    <div class="contacts">Питання: <a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="{TG}" target="_blank" rel="noopener">Telegram</a></div></div>
  <div class="rv">{form_html()}</div>
</div></section>
</main>
<footer><div class="wrap"><span>KRAЇNA EDEM × OBIIMY · Trypillia — The Art of Origins · 2026</span><span><a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="https://obiimy.world/" target="_blank" rel="noopener">obiimy.world</a></span></div></footer>'''
    write("edem-gold", GOLD_CSS + FORM_CSS, body)

# ═══ B · MUSEUM — an exhibition catalogue ═══════════════════════════════════════════════════════════════════════════════════
MUSEUM_CSS = """
:root { --paper: #F6F0E4; --paper2: #EFE6D6; --ink: #2A2017; --ink2: #5F5247; --gold: #8C6B22; --rule: #C9A95A; --line: rgba(42,32,23,.18); --acc: #2A2017; --fb: rgba(42,32,23,.3); --fbg: #FFFDF8; --fink: #2A2017; }
* { box-sizing: border-box; } html { scroll-behavior: smooth; }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: Montserrat, Arial, sans-serif; font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
body::before { content: ""; position: fixed; inset: 0; pointer-events: none; opacity: .5; mix-blend-mode: multiply; background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .08 0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>"); z-index: 1; }
img { max-width: 100%; height: auto; display: block; } p { margin: 0; } a { color: inherit; } figure { margin: 0; }
h1, h2, h3 { margin: 0; font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 400; line-height: 1.04; text-wrap: balance; }
.layout { display: grid; grid-template-columns: 220px minmax(0, 1fr); max-width: 1320px; margin: 0 auto; padding: 0 24px; gap: 48px; position: relative; z-index: 2; }
.index { position: sticky; top: 0; align-self: start; height: 100vh; padding: 36px 0; display: flex; flex-direction: column; gap: 10px; font-size: 12px; letter-spacing: .14em; text-transform: uppercase; }
.index .brand { font-family: 'Cormorant Garamond', serif; text-transform: none; letter-spacing: .04em; font-size: 20px; margin-bottom: 34px; color: var(--ink); } .index .brand small { display: block; font-size: 12px; color: var(--gold); letter-spacing: .22em; text-transform: uppercase; margin-top: 6px; }
.index a { text-decoration: none; color: var(--ink2); display: flex; gap: 12px; padding: 6px 0; border-bottom: 1px solid var(--line); } .index a b { font-family: 'Cormorant Garamond', serif; font-weight: 400; color: var(--gold); width: 24px; }
.index .btn { margin-top: auto; justify-content: center; }
.index .exh { margin: 26px auto 0; width: 110px; } .index .exh img { width: 100%; height: auto; filter: drop-shadow(0 14px 18px rgba(42,32,23,.25)); } .index .exh p { font-size: 10px; letter-spacing: .18em; color: var(--ink2); text-align: center; margin-top: 8px; }
.plate { font-size: 11px; letter-spacing: .22em; text-transform: uppercase; color: var(--gold); font-weight: 600; }
.cap { font-size: 12px; color: var(--ink2); letter-spacing: .04em; line-height: 1.5; margin-top: 10px; }
.btn-main { background: var(--ink); color: var(--paper); } .btn-main:hover { background: #40342A; } .btn-line { border-color: var(--ink); color: var(--ink); }
section { padding: clamp(60px, 8vw, 110px) 0; border-bottom: 1px solid var(--line); scroll-margin-top: 10px; }
.hero { padding-top: 44px; display: grid; grid-template-columns: minmax(0, .85fr) minmax(0, 1.15fr); gap: 48px; align-items: end; }
.hero h1 { font-size: clamp(48px, 6vw, 96px); } .hero h1 i { font-style: italic; color: var(--gold); }
.hero .lead { font-family: 'Cormorant Garamond', serif; font-size: clamp(22px, 2vw, 28px); color: var(--ink2); margin-top: 22px; max-width: 26em; }
.hero .cta { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 32px; }
.hero figure img { width: 100%; height: auto; } .hero figure { position: relative; }
.dim { display: flex; align-items: center; gap: 12px; margin-top: 16px; font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink2); } .dim i { flex: 1; height: 1px; background: var(--ink2); position: relative; } .dim i::before, .dim i::after { content: ""; position: absolute; top: -5px; width: 1px; height: 11px; background: var(--ink2); } .dim i::before { left: 0; } .dim i::after { right: 0; }
.mani blockquote { margin: 0; font-family: 'Cormorant Garamond', serif; font-size: clamp(30px, 4vw, 58px); font-weight: 300; line-height: 1.18; max-width: 22em; } .mani b { font-weight: 400; color: var(--gold); }
.two { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 48px; align-items: start; }
.text p + p { margin-top: 1.1em; } .text { color: var(--ink2); }
h2 { font-size: clamp(34px, 4vw, 56px); margin-top: 14px; }
.plates { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 40px 48px; margin-top: 40px; }
.plates figure { display: grid; grid-template-columns: 200px minmax(0, 1fr); gap: 24px; align-items: center; padding-top: 22px; border-top: 1px solid var(--ink); }
.plates .pic { height: 220px; display: flex; align-items: center; justify-content: center; background: var(--paper2); } .plates .pic img { max-height: 84%; width: auto; filter: drop-shadow(0 12px 16px rgba(42,32,23,.2)); } .plates .pic.lg img { transform: scale(1.3); }
.plates h3 { font-size: 28px; margin-top: 8px; } .plates p { margin-top: 8px; font-size: 14px; color: var(--ink2); }
.full img { width: 100%; height: auto; } .zoom { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 16px; } .zoom img { width: 100%; height: auto; aspect-ratio: 1; object-fit: cover; }
.spec { margin-top: 32px; columns: 2; column-gap: 48px; } .spec div { display: flex; justify-content: space-between; gap: 16px; padding: 12px 0; border-bottom: 1px solid var(--line); font-size: 14px; break-inside: avoid; } .spec span { color: var(--ink2); } .spec b { font-weight: 600; }
.brands { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; margin-top: 30px; } .brands article { border-top: 1px solid var(--ink); padding-top: 22px; } .brands h3 { font-size: 30px; letter-spacing: .05em; } .brands p { margin-top: 12px; color: var(--ink2); font-size: 15px; }
.brands ul { margin: 14px 0 0; padding: 0; list-style: none; } .brands li { padding: 8px 0; border-top: 1px solid var(--line); font-size: 14px; }
.reg { border: 0; } .reg .two { align-items: start; } .steps { margin-top: 26px; counter-reset: st; } .steps div { position: relative; padding: 14px 0 14px 56px; border-top: 1px solid var(--line); }
.steps div::before { counter-increment: st; content: "0" counter(st); position: absolute; left: 0; top: 12px; font-family: 'Cormorant Garamond', serif; font-size: 30px; color: var(--gold); } .steps h3 { font-size: 22px; } .steps p { font-size: 14px; color: var(--ink2); margin-top: 4px; }
.reg form.f, .reg .done { background: #FFFDF8; padding: 30px 28px; border: 1px solid var(--line); } .reg form.f label, .reg form.f legend { color: var(--ink2); } .reg .lead { font-family: 'Cormorant Garamond', serif; font-size: clamp(20px, 2vw, 26px); color: var(--ink2); margin-top: 16px; }
.reg .contacts { margin-top: 24px; font-size: 14px; color: var(--ink2); }
footer { padding: 30px 0 40px; font-size: 12px; color: var(--ink2); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 12px 30px; } footer a { text-decoration: none; }
@media (max-width: 980px) { .layout { grid-template-columns: 1fr; gap: 0; } .index { position: static; height: auto; flex-direction: row; flex-wrap: wrap; gap: 6px 14px; padding: 20px 0 10px; border-bottom: 1px solid var(--line); } .index .brand { width: 100%; margin-bottom: 8px; } .index a { border: 0; padding: 4px 0; } .index .btn { margin: 8px 0 0; width: 100%; } .index .exh { display: none; } .hero, .two, .plates, .brands { grid-template-columns: 1fr; } .plates figure { grid-template-columns: 140px 1fr; } .spec { columns: 1; } .zoom { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 600px) { .plates figure { grid-template-columns: 1fr; } .plates .pic { height: 180px; } .hero .cta .btn { flex: 1 1 100%; justify-content: center; } }
"""

def museum():
    idx = [("hero", "I", "Випуск"), ("manifest", "II", "Маніфест"), ("scarf", "III", "Хустка"), ("story", "IV", "Історія"), ("symbols", "V", "Символи"), ("brands", "VI", "Партнери"), ("register", "VII", "Як придбати")]
    body = f'''
<div class="layout" id="top">
<aside class="index"><a class="brand" href="#top" style="border:0;display:block">Kraїna Edem × Obiimy<small>Каталог випуску · 2026</small></a>{"".join(f'<a href="#{h}"><b>{n}</b>{t}</a>' for h, n, t in idx)}<div class="exh">{img("photo/edem/figure.webp", "Трипільська фігурка — елемент принту", sizes="110px")}<p>Експонат · пластика</p></div><a class="btn btn-main" href="#register">Ранній доступ</a></aside>
<main>
<section class="hero" id="hero">
  <div><p class="plate">Fig. 00 · Спільний мистецький проєкт · лімітований випуск</p>
    <h1 style="margin-top:18px">Trypillia —<br><i>The Art of Origins</i></h1>
    <p class="lead">Мистецтво бути ближче. Шовкова хустка за трипільськими мотивами — спільна робота KRAЇNA EDEM та OBIIMY.</p>
    <div class="cta"><a class="btn btn-main" href="#register">Отримати ранній доступ</a><a class="btn btn-line" href="#story">Про проєкт</a></div></div>
  <figure>{img("photo/edem/art-1600.webp", "Принт хустки «Trypillia — The Art of Origins» повністю", sizes="(max-width: 980px) 92vw, 44vw", lazy=False, eager_priority=True)}<div class="dim"><span>0</span><i></i><span>88 см</span></div><p class="cap">Хустка 88 × 88 см · 100% натуральний шовк · обмежений наклад · підпис OBIIMY × Edem на полотні</p></figure>
</section>
<section class="mani" id="manifest"><p class="plate rv">II · Маніфест</p><blockquote class="rv" style="margin-top:22px">{MANIFESTO}</blockquote></section>
<section id="scarf"><p class="plate rv">III · Хустка</p><h2 class="rv">Мистецьке полотно, яке можна носити</h2>
  <div class="full rv" style="margin-top:30px">{img("photo/edem/art-1600.webp", "Принт хустки повністю", sizes="(max-width: 980px) 92vw, 70vw")}</div>
  <div class="zoom rv">{img("photo/edem/art-center.webp", "Центральний медальйон крупно", sizes="24vw")}{img("photo/edem/art-pendants.webp", "Гроно підвісок на шнурах", sizes="24vw")}{img("photo/edem/art-sign.webp", "Підпис OBIIMY × Edem на полотні", sizes="24vw")}</div>
  <p class="cap rv">Fig. 01–03 · Медальйон · підвіски на шнурах · підпис двох брендів на полотні</p>
  <div class="spec rv">{spec_rows()}</div>
  <p class="cap rv" style="margin-top:18px">Ціну й дату старту повідомимо зареєстрованим першими.</p></section>
<section id="story"><p class="plate rv">IV · Історія, що живе в нас</p><div class="two" style="margin-top:14px">
  <div class="rv"><h2>Наше коріння сягає глибини тисячоліть</h2><div class="text" style="margin-top:22px">{"".join(f"<p>{t}</p>" for t in STORY)}</div></div>
  <figure class="rv">{img("photo/edem/art-corner.webp", "Фрагмент принту: трипільська фігурка й плетені шнури на кутку хустки", sizes="(max-width: 980px) 92vw, 40vw")}<p class="cap">Fig. 04 · Фрагмент принту, кут хустки: фігурка, плетені шнури, рамка</p></figure></div></section>
<section id="symbols"><p class="plate rv">V · Символи хустки</p><h2 class="rv">Кожна деталь має значення</h2>
  <div class="plates">{"".join(f'<figure class="rv"><div class="pic{" lg" if k == "pendant-round" else ""}">{sym_img(k, a, "200px")}</div><div><p class="plate">Fig. 0{i + 5}</p><h3>{t}</h3><p>{d}</p></div></figure>' for i, (k, t, d, a) in enumerate(SYMBOLS))}</div></section>
<section id="brands"><p class="plate rv">VI · Партнери</p><h2 class="rv">Два бренди. Одна філософія. Спільне мистецтво.</h2>
  <div class="brands"><article class="rv"><p class="plate">Партнер</p><h3 style="margin-top:10px">KRAЇNA EDEM</h3><p>{EDEM_P}</p><ul>{"".join(f"<li>{x}</li>" for x in EDEM_L)}</ul></article>
  <article class="rv"><p class="plate">Бренд</p><h3 style="margin-top:10px">OBIIMY</h3><p>{OB_P}</p><ul>{"".join(f"<li>{x}</li>" for x in OB_L)}</ul></article></div></section>
<section class="reg" id="register"><p class="plate rv">VII · Як придбати</p><div class="two" style="margin-top:14px">
  <div class="rv"><h2>Ранній доступ до випуску</h2><p class="lead">Ціну й дату старту підтверджуємо з партнером. Щойно вони відомі — зареєстровані дізнаються першими й отримують персональне посилання на оплату.</p>
    <div class="steps">{"".join(f"<div><h3>{t}</h3><p>{d}</p></div>" for t, d in STEPS)}</div>
    <div class="contacts">Питання: <a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="{TG}" target="_blank" rel="noopener">Telegram</a></div></div>
  <div class="rv">{form_html()}</div></div></section>
<footer><span>KRAЇNA EDEM × OBIIMY · Trypillia — The Art of Origins · 2026</span><span><a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="https://obiimy.world/" target="_blank" rel="noopener">obiimy.world</a></span></footer>
</main></div>'''
    write("edem-museum", MUSEUM_CSS + FORM_CSS, body)

# ═══ C · ZOOM — a scroll-driven journey into the print ═════════════════════════════════════════════════════════════════════
ZOOM_CSS = """
:root { --bg: #1C1410; --paper: #F3E9D8; --cream: #FBF4E7; --ink: #2A2017; --ink2: #5A4B3C; --gold: #7F6020; --gold2: #E2C27A; --rule: #C9A95A; --line: rgba(42,32,23,.16); --acc: #3B2A1C; --fb: rgba(42,32,23,.3); --fbg: #fff; --fink: #2A2017; }
* { box-sizing: border-box; } html { scroll-behavior: smooth; }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: Montserrat, Arial, sans-serif; font-size: 17px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
img { max-width: 100%; height: auto; display: block; } p { margin: 0; } a { color: inherit; } figure { margin: 0; }
h1, h2, h3 { margin: 0; font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 400; line-height: 1.04; text-wrap: balance; }
.wrap { max-width: 1240px; margin: 0 auto; padding: 0 24px; } section[id] { scroll-margin-top: 20px; }
.eyebrow { font-size: 12px; font-weight: 600; letter-spacing: .22em; text-transform: uppercase; color: var(--gold); }
.btn-main { background: #3B2A1C; color: var(--cream); } .btn-main:hover { background: #2A1D13; } .btn-line { border-color: #3B2A1C; color: #3B2A1C; } .btn-line.light { border-color: rgba(251,244,231,.7); color: var(--cream); }
/* the journey: a 420vh track, a sticky stage, the artwork scales and the captions pass */
.journey { position: relative; height: 420vh; background: var(--bg); color: var(--cream); }
.stage { position: sticky; top: 0; height: 100vh; overflow: hidden; }
.stage .art { position: absolute; left: 62%; top: 50%; width: min(92vmin, 900px); height: min(92vmin, 900px); transform: translate(-50%, -50%) scale(1); transform-origin: 50% 50%; will-change: transform; }
.stage .art img { width: 100%; height: 100%; object-fit: contain; filter: drop-shadow(0 40px 80px rgba(0,0,0,.7)); }
.stage .veil { position: absolute; inset: 0; background: radial-gradient(70% 70% at 60% 50%, transparent 40%, rgba(28,20,16,.55) 100%); pointer-events: none; }
.stage .scrim { position: absolute; inset: 0; pointer-events: none; background: linear-gradient(90deg, rgba(28,20,16,.92) 0%, rgba(28,20,16,.78) 30%, rgba(28,20,16,.2) 52%, transparent 65%), linear-gradient(0deg, rgba(28,20,16,.9) 0%, rgba(28,20,16,.5) 28%, transparent 55%); z-index: 2; }
.stage .top { position: absolute; left: 24px; right: 24px; top: 28px; display: flex; justify-content: space-between; font-size: 11px; letter-spacing: .24em; text-transform: uppercase; color: rgba(243,233,216,.75); z-index: 3; }
.stage .cap { position: absolute; left: 0; right: 0; bottom: 0; padding: 0 24px 48px; z-index: 3; }
.stage .cap .in { max-width: 1240px; margin: 0 auto; display: grid; grid-template-columns: minmax(0, 560px); }
.stage .c { grid-area: 1 / 1; opacity: 0; visibility: hidden; transform: translateY(14px); transition: opacity .35s, transform .35s, visibility 0s .35s; pointer-events: none; }
.stage .c.on { opacity: 1; visibility: visible; transform: none; transition: opacity .45s .1s, transform .45s .1s, visibility 0s; pointer-events: auto; }
.stage .c .eyebrow { color: var(--gold2); }
.stage .c h1, .stage .c h2 { font-size: clamp(38px, 5.2vw, 78px); color: var(--cream); margin-top: 12px; } .stage .c h1 i { font-style: italic; color: var(--gold2); }
.stage .c p.t { font-family: 'Cormorant Garamond', serif; font-size: clamp(20px, 2vw, 26px); font-weight: 300; color: rgba(243,233,216,.82); margin-top: 14px; max-width: 30em; }
.stage .c .cta { margin-top: 24px; display: flex; gap: 12px; flex-wrap: wrap; }
.stage .dots { position: absolute; right: 28px; top: 50%; transform: translateY(-50%); display: grid; gap: 14px; z-index: 3; } .stage .dots i { width: 6px; height: 6px; border-radius: 50%; background: rgba(243,233,216,.3); display: block; } .stage .dots i.on { background: var(--gold2); }
.stage .hintsc { position: absolute; left: 50%; bottom: 20px; transform: translateX(-50%); font-size: 10px; letter-spacing: .3em; text-transform: uppercase; color: rgba(243,233,216,.5); z-index: 3; }
/* after the journey */
section.s { padding: clamp(60px, 8vw, 120px) 0; } section.s.alt { background: var(--cream); }
.head { max-width: 760px; margin-bottom: clamp(30px, 4vw, 54px); } .head h2 { font-size: clamp(34px, 4.2vw, 60px); color: #3B2A1C; margin-top: 14px; } .head .lead { font-family: 'Cormorant Garamond', serif; font-size: clamp(21px, 2vw, 27px); color: var(--ink2); margin-top: 16px; }
.sym4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 40px; } .sym4 .pic { height: 240px; display: flex; align-items: center; justify-content: center; } .sym4 .pic img { max-height: 100%; width: auto; filter: drop-shadow(0 18px 24px rgba(58,42,28,.2)); } .sym4 .pic.lg img { transform: scale(1.3); }
.sym4 h3 { font-size: 28px; margin-top: 22px; padding-top: 16px; border-top: 1px solid var(--rule); color: #3B2A1C; } .sym4 p { margin-top: 10px; font-size: 15px; color: var(--ink2); }
.two { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(28px, 4vw, 64px); align-items: start; }
.spec div { display: flex; justify-content: space-between; gap: 20px; padding: 16px 0; border-bottom: 1px solid var(--line); font-size: 15px; } .spec span { color: var(--ink2); } .spec b { font-weight: 600; color: #3B2A1C; text-align: right; }
.zoom { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; } .zoom img { width: 100%; height: auto; aspect-ratio: 1; object-fit: cover; border-radius: 2px; }
.text p + p { margin-top: 1.1em; } .text { color: var(--ink2); }
.scarf2 { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, .8fr); gap: clamp(28px, 4vw, 64px); align-items: start; } .scarf2 > div:last-child { position: sticky; top: 90px; }
.full img { width: 100%; height: auto; border-radius: 2px; box-shadow: 0 50px 90px -40px rgba(58,42,28,.45); } .note { margin-top: 18px; padding: 14px 16px; border-left: 2px solid var(--gold2); background: var(--cream); font-size: 14px; color: var(--ink2); }
.figc { margin-top: 12px; font-size: 12px; letter-spacing: .1em; text-transform: uppercase; color: var(--ink2); } .fig img { width: 100%; height: auto; border-radius: 2px; }
.brands { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; } .brands article { border-top: 1px solid var(--rule); padding-top: 26px; } .brands h3 { font-size: 30px; letter-spacing: .05em; color: #3B2A1C; } .brands p { margin-top: 14px; color: var(--ink2); }
.brands ul { margin: 16px 0 0; padding: 0; list-style: none; } .brands li { padding: 10px 0; border-top: 1px solid var(--line); font-size: 15px; }
.reg { background: #3B2A1C; color: var(--cream); padding: clamp(60px, 8vw, 120px) 0; } .reg .wrap { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: clamp(32px, 5vw, 80px); align-items: start; }
.reg .eyebrow { color: var(--gold2); } .reg h2 { font-size: clamp(34px, 4vw, 56px); margin-top: 14px; } .reg .lead { font-family: 'Cormorant Garamond', serif; font-size: clamp(20px, 2vw, 26px); color: rgba(251,244,231,.82); margin-top: 18px; }
.steps { margin-top: 30px; counter-reset: st; } .steps div { position: relative; padding: 16px 0 16px 60px; border-top: 1px solid rgba(251,244,231,.18); } .steps div::before { counter-increment: st; content: "0" counter(st); position: absolute; left: 0; top: 14px; font-family: 'Cormorant Garamond', serif; font-size: 32px; color: var(--gold2); } .steps h3 { font-size: 24px; color: var(--cream); } .steps p { margin-top: 4px; font-size: 15px; color: rgba(251,244,231,.75); }
.reg .contacts { margin-top: 28px; font-size: 15px; color: rgba(251,244,231,.75); } .reg .contacts a { color: var(--cream); }
.reg form.f, .reg .done { background: var(--cream); color: var(--ink); padding: 32px 30px; border-radius: 2px; } .reg form.f label, .reg form.f legend { color: var(--ink2); } .reg .done h3 { color: #3B2A1C; }
footer { padding: 34px 0 44px; font-size: 13px; color: var(--ink2); } footer .wrap { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px 30px; } footer a { text-decoration: none; }
@media (max-width: 980px) { .sym4 { grid-template-columns: repeat(2, 1fr); gap: 28px 20px; } .two, .brands, .reg .wrap, .scarf2 { grid-template-columns: 1fr; } .scarf2 > div:last-child { position: static; } .stage .dots { display: none; } .stage .art { left: 50%; width: 92vmin; height: 92vmin; top: 40%; } .stage .scrim { background: linear-gradient(0deg, rgba(28,20,16,.95) 0%, rgba(28,20,16,.7) 40%, transparent 70%); } }
@media (max-width: 600px) { .sym4 { grid-template-columns: 1fr; } .stage .cap { padding-bottom: 36px; } .stage .cap .cta .btn { flex: 1 1 100%; justify-content: center; } .stage .c h1, .stage .c h2 { font-size: 36px; } .stage .c p.t { font-size: 18px; } .stage .top { font-size: 9px; } }
"""

def zoom():
    caps = [("Спільний мистецький проєкт · лімітований випуск", "<h1>Trypillia —<br><i>The Art of Origins</i></h1>", "Мистецтво бути ближче. Шовкова хустка за трипільськими мотивами — спільна робота KRAЇNA EDEM та OBIIMY.", True),
            ("Пам’ять землі", "<h2>Символи, що пережили тисячоліття</h2>", "Образи, які залишили нам давні покоління, і культурний код, який продовжує жити, навіть коли змінюються епохи.", False),
            ("Трипільська пластика", "<h2>Фігурка, підвіски, шнури</h2>", "Жіноча фігурка повторюється чотири рази; круглі й ромбовидні підвіски на плетених синіх шнурах оточують центр.", False),
            ("Медальйон", "<h2>Спіраль у колі</h2>", "У спіралях трипільського орнаменту дослідники вбачають плин часу, відродження та циклічність життя.", False)]
    cap_html = "".join(f'<div class="c{" on" if i == 0 else ""}" data-i="{i}"><p class="eyebrow">{e}</p>{h}<p class="t">{t}</p>' + (f'<div class="cta"><a class="btn btn-main" style="background:var(--gold2);color:#2A2017" href="#register">Отримати ранній доступ</a><a class="btn btn-line light" href="#symbols">Пропустити</a></div>' if cta else "") + '</div>' for i, (e, h, t, cta) in enumerate(caps))
    body = f'''
<main id="top">
<div class="journey" id="journey">
  <div class="stage">
    <div class="art" id="art">{img("photo/edem/art-2400.webp", "Принт хустки «Trypillia — The Art of Origins»", sizes="100vmin", lazy=False, eager_priority=True)}</div>
    <div class="veil"></div><div class="scrim"></div>
    <div class="top"><span>Kraїna Edem × Obiimy</span><span>88 × 88 · шовк · обмежений наклад</span></div>
    <div class="dots" id="dots">{"".join('<i class="on"></i>' if i == 0 else "<i></i>" for i in range(4))}</div>
    <div class="cap"><div class="in">{cap_html}</div></div>
    <p class="hintsc" id="hintsc">Гортайте</p>
  </div>
</div>

<section class="s" id="scarf"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Хустка · 88 × 88 см</p><h2>Мистецьке полотно, яке можна носити</h2><p class="lead">Хустка тут — більше, ніж аксесуар: мистецьке полотно, що поєднує сучасний дизайн із пам’яттю про давні культури.</p></div>
  <div class="scarf2">
    <div class="rv"><div class="full">{img("photo/edem/art-1600.webp", "Принт хустки «Trypillia — The Art of Origins» повністю", sizes="(max-width: 980px) 92vw, 58vw")}</div>
      <div class="zoom" style="margin-top:14px">{img("photo/edem/art-center.webp", "Центральний медальйон крупно", sizes="19vw")}{img("photo/edem/art-pendants.webp", "Гроно підвісок на шнурах", sizes="19vw")}{img("photo/edem/art-sign.webp", "Підпис OBIIMY × Edem на полотні", sizes="19vw")}</div></div>
    <div class="rv"><div class="spec">{spec_rows()}</div><p class="note">Ціну й дату старту повідомимо зареєстрованим першими.</p><p style="margin-top:26px"><a class="btn btn-main" href="#register">Отримати ранній доступ</a></p></div>
  </div>
</div></section>

<section class="s alt" id="symbols"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Символи хустки</p><h2>Кожна деталь має значення</h2><p class="lead">Давні орнаментальні мотиви й символічні образи — переосмислені мовою сучасного дизайну, у золоті й глибокому синьому.</p></div>
  <div class="sym4">{"".join(f'<figure class="rv"><div class="pic{" lg" if k == "pendant-round" else ""}">{sym_img(k, a)}</div><h3>{t}</h3><p>{d}</p></figure>' for k, t, d, a in SYMBOLS)}</div>
</div></section>

<section class="s" id="story"><div class="wrap"><div class="two">
  <div class="rv"><p class="eyebrow">Історія, що живе в нас</p><h2 style="font-size:clamp(34px,4.2vw,60px);color:#3B2A1C;margin-top:14px">Наше коріння сягає глибини тисячоліть</h2><div class="text" style="margin-top:22px">{"".join(f"<p>{t}</p>" for t in STORY)}</div></div>
  <figure class="fig rv">{img("photo/edem/art-corner.webp", "Фрагмент принту: трипільська фігурка й плетені шнури на кутку хустки", sizes="(max-width: 980px) 92vw, 46vw")}<p class="figc">Фрагмент принту · кут хустки</p></figure>
</div></div></section>

<section class="s alt" id="brands"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Партнери</p><h2>Два бренди. Одна філософія. Спільне мистецтво.</h2></div>
  <div class="brands"><article class="rv"><p class="eyebrow">Партнер</p><h3 style="margin-top:10px">KRAЇNA EDEM</h3><p>{EDEM_P}</p><ul>{"".join(f"<li>{x}</li>" for x in EDEM_L)}</ul></article>
  <article class="rv"><p class="eyebrow">Бренд</p><h3 style="margin-top:10px">OBIIMY</h3><p>{OB_P}</p><ul>{"".join(f"<li>{x}</li>" for x in OB_L)}</ul></article></div>
</div></section>

<section class="reg" id="register"><div class="wrap">
  <div class="rv"><p class="eyebrow">Як придбати</p><h2>Ранній доступ до випуску</h2><p class="lead">Ціну й дату старту підтверджуємо з партнером. Щойно вони відомі — зареєстровані дізнаються першими й отримують персональне посилання на оплату.</p>
    <div class="steps">{"".join(f"<div><h3>{t}</h3><p>{d}</p></div>" for t, d in STEPS)}</div>
    <div class="contacts">Питання: <a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="{TG}" target="_blank" rel="noopener">Telegram</a></div></div>
  <div class="rv">{form_html()}</div>
</div></section>
</main>
<footer><div class="wrap"><span>KRAЇNA EDEM × OBIIMY · Trypillia — The Art of Origins · 2026</span><span><a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="https://obiimy.world/" target="_blank" rel="noopener">obiimy.world</a></span></div></footer>'''
    extra = """
  // the journey: progress 0..1 over the 420vh track → the artwork scales from 1 to 3.4 towards the medallion, captions switch by quarter
  var J = document.getElementById('journey'), A = document.getElementById('art'), caps = [].slice.call(document.querySelectorAll('.stage .c')), dots = [].slice.call(document.querySelectorAll('#dots i')), hint = document.getElementById('hintsc');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches, cur = 0;
  function tick() {
    var r = J.getBoundingClientRect(), total = J.offsetHeight - window.innerHeight, p = Math.min(1, Math.max(0, -r.top / total));
    var s = reduce ? 1 : 1 + p * 2.4, ty = reduce ? 0 : p * -6;          // the medallion is at the centre, so a plain scale zooms into it
    A.style.transform = 'translate(-50%, calc(-50% + ' + ty + '%)) scale(' + s + ')';
    var i = Math.min(3, Math.floor(p * 4 + 0.0001));
    if (i !== cur) { cur = i; caps.forEach(function (c, k) { c.classList.toggle('on', k === i); }); dots.forEach(function (d, k) { d.classList.toggle('on', k === i); }); }
    hint.style.opacity = p > .05 ? 0 : 1;
  }
  window.addEventListener('scroll', tick, { passive: true }); window.addEventListener('resize', tick); tick();"""
    write("edem-zoom", ZOOM_CSS + FORM_CSS, body, extra)

if __name__ == "__main__":
    gold(); museum(); zoom()
