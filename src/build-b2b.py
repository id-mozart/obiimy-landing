#!/usr/bin/env python3
"""Generate B2B / corporate landing pages (b2b-<name>.html) reusing the visual skins of the consumer landings."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from imgs import img, typo

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
_src = (ROOT / "build-products.py").read_text()
_ns = {}
exec(_src[_src.index("SKINS = {"):_src.index("BASE_CSS = ")], {}, _ns)
SKINS = _ns["SKINS"]

PHONE = "+38 067 010 85 25"
PHONE_HREF = "tel:+380670108525"
MAIL = "sale@obiimy-world.com"
SITE_URL = "https://obiimy-landing-production.up.railway.app"
SAMPLE_URL = "https://obiimy.world/khustka-tvilli-shovkova-zolote-svitlo-84x5/"

CSS = """
  * { box-sizing: border-box; min-width: 0; }
  html { scroll-behavior: smooth; }
  body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased; overflow-x: hidden; }
  img { max-width: 100%; display: block; height: auto; }
  a { color: inherit; }
  h1, h2, h3 { font-family: var(--display); font-weight: 400; margin: 0; line-height: 1.08; text-wrap: balance; }
  h1 { font-size: clamp(2.3rem, 4.6vw, 4.2rem); }
  h2 { font-size: clamp(1.8rem, 3vw, 2.7rem); }
  h3 { font-size: 1.25rem; }
  p { margin: 0; }
  [id] { scroll-margin-top: calc(env(safe-area-inset-top, 0px) + 84px); }
  .wrap { width: min(1280px, 100%); margin-inline: auto; padding-inline: clamp(16px, 4vw, 48px); }
  .eyebrow { font-size: .76rem; letter-spacing: .2em; text-transform: uppercase; color: var(--ink3); font-weight: 600; }
  .num { font-variant-numeric: tabular-nums; white-space: nowrap; }
  .btn { display: inline-flex; align-items: center; justify-content: center; gap: 10px; min-height: 48px; padding: 14px 28px; border-radius: 999px; text-decoration: none; font-weight: 600; font-size: .95rem; border: 1px solid transparent; cursor: pointer; font-family: inherit; transition: transform .2s ease; }
  .btn:hover { transform: translateY(-1px); }
  .btn-gold { background: var(--gold); color: #17151A; }
  .btn-line { border-color: var(--ink); background: transparent; color: var(--ink); }
  .btn-sm { min-height: 44px; padding: 10px 18px; font-size: .82rem; }
  a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }
  [hidden] { display: none !important; }
  .bar { background: var(--ink); color: var(--bg); font-size: .78rem; text-align: center; padding: 9px 16px; letter-spacing: .04em; }
  .dark .bar { background: var(--gold); color: #17151A; }
  .nav { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 50; background: color-mix(in srgb, var(--bg) 85%, transparent); backdrop-filter: blur(14px); border-bottom: 1px solid var(--line); }
  .nav .wrap { display: flex; align-items: center; justify-content: space-between; gap: 20px; height: 68px; }
  .logo img { height: 24px; width: auto; }
  .nav-links { display: flex; gap: 24px; font-size: .88rem; font-weight: 500; }
  .nav-links a { text-decoration: none; color: var(--ink2); padding: 12px 0; }
  .nav-links a:hover { color: var(--ink); }
  @media (max-width: 900px) { .nav-links { display: none; } }

  .hero { padding-block: clamp(28px, 6vw, 88px) clamp(40px, 6vw, 88px); }
  .hero .wrap { display: grid; grid-template-columns: minmax(0, 6fr) minmax(0, 6fr); gap: clamp(28px, 5vw, 72px); align-items: center; }
  .hero .lead { font-size: 1.15rem; color: var(--ink2); max-width: 34em; margin-top: 20px; }
  .hero .cta { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 30px; }
  .hero .cta .btn { white-space: nowrap; }
  .h1-sm h1 { font-size: clamp(2.3rem, 4.2vw, 3.6rem); }
  .hero .fine { font-size: .85rem; color: var(--ink2); margin-top: 16px; }
  .hero .fine a { font-weight: 600; text-decoration: none; display: inline-block; padding: 12px 0; margin: -12px 0; }
  .note a, .steps a { display: inline-block; padding: 10px 0; margin: -10px 0; }
  .hero figure { margin: 0; position: relative; }
  .hero figure img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: var(--radius); }
  .hero figure .tag { position: absolute; left: 18px; bottom: 18px; background: var(--card); color: var(--ink); padding: 10px 14px; border-radius: var(--radius); font-size: .82rem; box-shadow: 0 20px 40px -20px rgba(0,0,0,.35); }
  .dark .hero figure .tag { background: var(--gold); color: #17151A; }
  .facts { display: grid; grid-template-columns: repeat(4, 1fr); border-block: 1px solid var(--line); }
  .facts div { padding: 22px 18px; border-right: 1px solid var(--line); }
  .facts div:last-child { border-right: 0; }
  .facts b { display: block; font-family: var(--display); font-weight: 400; font-size: 1.5rem; line-height: 1.15; }
  .facts span { font-size: .84rem; color: var(--ink2); }

  .block { padding-block: clamp(48px, 7vw, 100px); }
  .block.alt { background: var(--bg2); }
  .head { display: grid; gap: 10px; max-width: 42em; margin-bottom: clamp(24px, 4vw, 44px); }
  .head p.sub { color: var(--ink2); font-size: 1.05rem; }
  .grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
  .grid4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(24px, 4vw, 64px); align-items: center; }
  .grid2 > figure { margin: 0; }
  .grid2 > figure img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: var(--radius); }
  .card { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 22px; display: grid; gap: 10px; align-content: start; }
  .card .k { font-family: var(--display); font-size: 1.9rem; line-height: 1; }
  .card p { color: var(--ink2); font-size: .95rem; }
  .card > img { width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: calc(var(--radius) - 2px); background: #fff; }
  .dark .card > img { background: #F1EEE8; padding: 6%; }
  .card.photo { padding: 0; overflow: hidden; }
  .card.photo img { aspect-ratio: 4 / 5; border-radius: 0; object-fit: cover; width: 100%; }
  .card.photo .in { padding: 18px 20px 22px; display: grid; gap: 8px; }
  .price-row { display: flex; justify-content: space-between; gap: 12px; font-size: .92rem; padding: 8px 0; border-top: 1px solid var(--line); }
  .price-row:first-of-type { border-top: 0; }
  .price-row span:last-child { color: var(--ink2); }
  .steps { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; counter-reset: s; }
  .steps div { padding: 20px 0 0; border-top: 1px solid var(--ink); display: grid; gap: 8px; align-content: start; }
  .steps div::before { counter-increment: s; content: "0" counter(s); font-family: var(--display); font-size: 1.4rem; }
  .steps p { color: var(--ink2); font-size: .92rem; }
  .timeline { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
  .timeline div { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 22px; display: grid; gap: 6px; }
  .timeline b { font-family: var(--display); font-weight: 400; font-size: 1.5rem; }
  .timeline p { color: var(--ink2); font-size: .92rem; }
  .quote { font-family: var(--display); font-size: clamp(1.3rem, 2vw, 1.7rem); line-height: 1.35; max-width: 28em; }
  .quote + p { margin-top: 12px; color: var(--ink2); font-size: .85rem; }
  .proof { display: grid; gap: 0; border-top: 1px solid var(--line); }
  .proof div { display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr); gap: 16px; padding: 14px 0; border-bottom: 1px solid var(--line); font-size: .95rem; }
  .proof b { font-family: var(--display); font-weight: 400; font-size: 1.05rem; }
  .proof span { color: var(--ink2); }
  .faq details { border-top: 1px solid var(--line); }
  .faq details:last-child { border-bottom: 1px solid var(--line); }
  .faq summary { cursor: pointer; list-style: none; display: flex; justify-content: space-between; gap: 16px; align-items: center; min-height: 52px; padding: 12px 0; font-family: var(--display); font-size: 1.15rem; }
  .faq summary::-webkit-details-marker { display: none; }
  .faq summary::after { content: "+"; color: var(--ink2); flex: none; }
  .faq details[open] summary::after { content: "–"; }
  .faq p { padding: 0 0 16px; color: var(--ink2); font-size: .95rem; max-width: 48em; }
  .note { margin-top: 22px; color: var(--ink2); font-size: .85rem; }
  .others { border-top: 1px solid var(--line); padding-block: 28px; }
  .others .wrap { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 22px; font-size: .9rem; }
  .others span { color: var(--ink2); }
  .others a { text-decoration: none; font-weight: 500; padding: 10px 0; border-bottom: 1px solid var(--ink); }

  .calc { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: clamp(18px, 3vw, 32px); display: grid; gap: 16px; }
  .calc .row { display: grid; grid-template-columns: 1fr 1.7fr 1.5fr; gap: 14px; }
  .calc label { display: grid; gap: 6px; font-size: .8rem; color: var(--ink2); letter-spacing: .04em; }
  .calc .out { display: flex; flex-wrap: wrap; align-items: baseline; gap: 8px 16px; border-top: 1px solid var(--line); padding-top: 16px; }
  .calc .out b { font-family: var(--display); font-weight: 400; font-size: 2rem; }
  .calc .out span { color: var(--ink2); font-size: .9rem; }

  .form-block { padding-block: clamp(48px, 7vw, 100px); }
  .form-block .wrap { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: clamp(28px, 5vw, 72px); align-items: start; }
  .contact { display: grid; gap: 14px; color: var(--ink2); }
  .contact a { color: var(--ink); text-decoration: none; font-weight: 500; display: inline-block; padding: 4px 0; }
  .contact .big { font-family: var(--display); font-size: 1.6rem; }
  form { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: clamp(18px, 3vw, 32px); }
  form label { display: grid; gap: 6px; font-size: .82rem; color: var(--ink2); letter-spacing: .03em; }
  form label.full { grid-column: 1 / -1; }
  form label .req { color: var(--gold); }
  input, select, textarea { font: inherit; font-size: 1rem; color: var(--ink); background: var(--bg); border: 1px solid var(--line); border-radius: calc(var(--radius) - 2px); padding: 12px 14px; width: 100%; min-height: 48px; }
  .dark input, .dark select, .dark textarea { background: #1C1A22; border-color: rgba(236,233,239,.22); }
  select { appearance: none; -webkit-appearance: none; padding-right: 40px; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23807C86' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 14px center; }
  textarea { min-height: 96px; resize: vertical; }
  ::placeholder { color: var(--ink2); opacity: .8; }
  .dark ::placeholder { color: rgba(236,233,239,.62); opacity: 1; }
  form .err { display: none; font-size: .78rem; color: #C43B2E; letter-spacing: 0; }
  .dark form .err { color: #F08A7E; }
  form [aria-invalid="true"] { border-color: #C43B2E; }
  form [aria-invalid="true"] + .err { display: block; }
  form .actions { grid-column: 1 / -1; display: grid; gap: 12px; }
  form .hint { font-size: .82rem; color: var(--ink2); }
  .done { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: clamp(18px, 3vw, 32px); display: grid; gap: 14px; }
  .done h3 { font-size: 1.5rem; }
  .done p { color: var(--ink2); }
  .done .row { display: flex; flex-wrap: wrap; gap: 10px; }

  footer { border-top: 1px solid var(--line); padding-block: 26px calc(90px + env(safe-area-inset-bottom, 0px)); font-size: .84rem; color: var(--ink2); }
  footer .wrap { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px 24px; }
  footer a { text-decoration: none; color: var(--ink); display: inline-block; padding: 10px 0; }
  .sticky { position: fixed; left: 0; right: 0; bottom: 0; z-index: 60; background: var(--ink); color: var(--bg); display: none; align-items: center; justify-content: space-between; gap: 12px; padding: 10px 16px calc(10px + env(safe-area-inset-bottom, 0px)); transform: translateY(calc(100% + 24px)); transition: transform .25s ease; }
  .sticky.on { transform: none; }
  .sticky span { font-size: .85rem; }
  .sticky a { background: var(--gold); color: #17151A; text-decoration: none; font-weight: 600; padding: 13px 22px; border-radius: 999px; font-size: .9rem; white-space: nowrap; min-height: 44px; display: inline-flex; align-items: center; }
  .dark .sticky { background: var(--card); color: var(--ink); border-top: 1px solid var(--line); }

  @media (max-width: 960px) {
    .hero .wrap, .form-block .wrap, .grid2 { grid-template-columns: 1fr; }
    .grid2 > figure:first-child { order: 1; }
    .hero figure { order: -1; }
    .grid4, .steps, .calc .row { grid-template-columns: 1fr 1fr; }
    .facts { grid-template-columns: 1fr 1fr; }
    .facts div:nth-child(2) { border-right: 0; }
    .facts div:nth-child(-n+2) { border-bottom: 1px solid var(--line); }
    .timeline { grid-template-columns: 1fr; }
  }
  @media (max-width: 640px) {
    .m-hide { display: none; }
    .hero { padding-top: 16px; }
    .hero .lead { font-size: 1.05rem; }
    .hero .cta { flex-direction: column; align-items: flex-start; gap: 6px; }
    .hero .cta .btn-gold { width: 100%; }
    .hero .cta .btn-line { border: 0; padding: 10px 0; min-height: 44px; text-decoration: underline; text-underline-offset: 4px; font-weight: 500; }
    .hero figure img { aspect-ratio: 16 / 10; }
    .grid3, .steps, .calc .row { grid-template-columns: 1fr; }
    .grid4 { grid-template-columns: 1fr 1fr; gap: 10px; }
    .grid4 .card { padding: 16px; }
    .grid4 .card.photo img { aspect-ratio: 1; }
    .grid4 .card.photo .in { padding: 12px 14px 16px; }
    .grid4 .card h3 { font-size: 1.05rem; }
    .grid4 .card p { font-size: .86rem; }
    .price-row { font-size: .84rem; flex-direction: column; gap: 0; }
    .price-row span:last-child { font-family: var(--display); font-size: 1rem; color: var(--ink); }
    form { grid-template-columns: 1fr; }
    form label.full { grid-column: auto; }
    .sticky { display: flex; }
    .facts b { font-size: 1.15rem; }
    .facts div { padding: 16px 12px; }
    .proof div { grid-template-columns: 1fr; gap: 4px; }
  }
"""

def price(n): return f"{n:,}".replace(",", " ") + " грн"

def facts_html(items):
    return '<section class="wrap" aria-label="Коротко про бренд"><div class="facts">' + "".join(f'<div><b class="num">{b}</b><span>{s}</span></div>' for b, s in items) + "</div></section>"

def proof_html(title, lead, first=False):
    quote = "«Замовляла на подарунок хустку, якість неймовірна, подруга теж задоволена! Вирішила замовити собі твіллі — не можу нарадуватись, кожного дня хочеться додавати в образ»"
    return f'''
  <section class="block{"" if first else " alt"}" id="proof"><div class="wrap grid2" style="align-items:start">
    <div><p class="eyebrow">Довіра</p><h2 style="margin-top:10px">{title}</h2><p style="margin-top:14px;color:var(--ink2);max-width:36em">{lead}</p></div>
    <div>
      <div class="proof">
        <div><b>INTERTOP · Hram</b><span>Роздрібні партнери в Україні</span></div>
        <div><b>Be Brave · Канада</b><span>Партнер у Канаді</span></div>
        <div><b>UFD London</b><span>Партнер у Великій Британії</span></div>
        <div><b>LIGA.net · INSIDER UA</b><span>Писали про бренд</span></div>
        <div><b class="num">5,0</b><span>Рейтинг покупців на obiimy.world</span></div>
      </div>
      <p class="quote" style="margin-top:22px">{quote}</p><p>Анна Мелешак · покупниця, відгук на obiimy.world</p>
    </div>
  </div></section>'''

def form_html(pid, subject, fields, note):
    """fields: list of (name, label, kind, required, extra) where kind in input/tel/email/number/select:opts/textarea."""
    out = []
    for name, label, kind, req, extra in fields:
        full = ' class="full"' if kind in ("textarea",) or extra.get("full") else ""
        star = ' <span class="req">*</span>' if req else ""
        r = " required" if req else ""
        ac = f' autocomplete="{extra["ac"]}"' if extra.get("ac") else ""
        ph = f' placeholder="{extra["ph"]}"' if extra.get("ph") else ""
        err = f'<span class="err" id="{pid}-{name}-err" role="alert">{extra.get("err", "Заповніть це поле")}</span>' if req else ""
        if kind.startswith("select:"):
            opts = "".join(f"<option>{o}</option>" for o in kind[7:].split("|"))
            ctl = f'<select name="{name}" data-label="{label}"{r}><option value="">Оберіть</option>{opts}</select>'
        elif kind == "textarea":
            ctl = f'<textarea name="{name}" data-label="{label}"{ph}></textarea>'
        else:
            t = {"input": "text"}.get(kind, kind)
            mn = ' min="1" inputmode="numeric"' if kind == "number" else ""
            ctl = f'<input name="{name}" data-label="{label}" type="{t}"{mn}{ph}{ac}{r}' + (f' aria-describedby="{pid}-{name}-err"' if req else '') + '>'
        out.append(f'<label{full}><span>{label}{star}</span>{ctl}{err}</label>')
    return f'''
      <form id="{pid}" novalidate>
        {"".join(out)}
        <div class="actions"><button class="btn btn-gold" type="submit">Надіслати запит</button><span class="hint">{note} Натискаючи «Надіслати», ви відкриєте лист на {MAIL} із заповненими даними — нічого не надсилається без вашого підтвердження. Або одразу телефонуйте: <a href="{PHONE_HREF}">{PHONE}</a>.</span></div>
      </form>
      <div class="done" id="{pid}-done" hidden aria-live="polite">
        <h3 tabindex="-1">Лист підготовлено</h3>
        <p>Якщо поштова програма не відкрилась — скопіюйте текст нижче й надішліть на <a href="mailto:{MAIL}">{MAIL}</a>, або подзвоніть <a href="{PHONE_HREF}">{PHONE}</a>.</p>
        <textarea id="{pid}-txt" readonly rows="8" aria-label="Текст запиту"></textarea>
        <div class="row"><button class="btn btn-line btn-sm" type="button" id="{pid}-copy">Скопіювати текст</button><a class="btn btn-line btn-sm" href="{PHONE_HREF}">Подзвонити</a><button class="btn btn-line btn-sm" type="button" id="{pid}-back">Змінити запит</button></div>
      </div>
      <script>
      (function () {{
        var f = document.getElementById('{pid}'), done = document.getElementById('{pid}-done'), txt = document.getElementById('{pid}-txt');
        function valid(i) {{
          var v = i.value.trim();
          if (i.type === 'email') return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(v);
          if (i.type === 'tel') return v.replace(/\\D/g, '').length >= 9;
          return v.length > 1;
        }}
        f.querySelectorAll('[required]').forEach(function (i) {{ i.addEventListener('input', function () {{ if (i.getAttribute('aria-invalid') === 'true' && valid(i)) i.setAttribute('aria-invalid', 'false'); }}); }});
        f.addEventListener('submit', function (e) {{
          e.preventDefault();
          var first = null;
          f.querySelectorAll('[required]').forEach(function (i) {{ var ok = valid(i); i.setAttribute('aria-invalid', ok ? 'false' : 'true'); if (!ok && !first) first = i; }});
          if (first) {{ first.focus(); first.scrollIntoView({{ block: 'center', behavior: 'smooth' }}); return; }}
          var lines = [];
          f.querySelectorAll('[name]').forEach(function (i) {{ if (i.value.trim()) lines.push(i.dataset.label + ': ' + i.value.trim()); }});
          var body = '{subject}\\n\\n' + lines.join('\\n') + '\\n\\nНадіслано зі сторінки ' + location.href;
          txt.value = body;
          var company = f.querySelector('[name="company"]').value.trim();
          f.hidden = true; done.hidden = false; done.scrollIntoView({{ block: 'start', behavior: 'smooth' }}); done.querySelector('h3').focus({{ preventScroll: true }});
          window.location.href = 'mailto:{MAIL}?subject=' + encodeURIComponent('{subject} — ' + company) + '&body=' + encodeURIComponent(body);
        }});
        document.getElementById('{pid}-copy').addEventListener('click', function () {{ var b = this; txt.select(); (navigator.clipboard ? navigator.clipboard.writeText(txt.value) : Promise.reject()).then(function () {{ b.textContent = 'Скопійовано'; setTimeout(function () {{ b.textContent = 'Скопіювати текст'; }}, 2000); }}, function () {{ document.execCommand('copy'); }}); }});
        document.getElementById('{pid}-back').addEventListener('click', function () {{ done.hidden = true; f.hidden = false; f.scrollIntoView({{ block: 'start', behavior: 'smooth' }}); }});
      }})();
      </script>'''

OTHERS = [("b2b-newyear", "Новий рік"), ("b2b-calendar", "Річна програма"), ("b2b-horeca", "HoReCa та уніформа"), ("b2b-wholesale", "Опт для магазинів")]

def og_crop(src, slug):
    from PIL import Image
    out = OUT / "photo" / f"og-{slug}.jpg"
    if not out.exists():
        im = Image.open(OUT / src).convert("RGB"); w, h = im.size
        tw, th = 1200, 630; scale = max(tw / w, th / h)
        im = im.resize((round(w * scale), round(h * scale))); w, h = im.size
        top = int(h * 0.22) if h > th else 0
        im = im.crop(((w - tw) // 2, min(top, h - th), (w - tw) // 2 + tw, min(top, h - th) + th)); im.save(out, quality=84)
    return f"photo/og-{slug}.jpg"

def shell(page, body):
    skin = SKINS[page["skin"]]
    dark = skin["dark"]
    logo = "brand/logo-white-480.webp" if dark else "brand/logo-ink-480.webp"
    links = "".join(f'<a href="#{h}">{t}</a>' for t, h in page["nav"])
    others = "".join(f'<a href="{slug}">{t}</a>' for slug, t in OTHERS if slug != page["slug"])
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page["title"]}</title>
<meta name="description" content="{page["desc"]}">
<link rel="canonical" href="{SITE_URL}/{page["slug"]}">
<meta property="og:type" content="website">
<meta property="og:title" content="{page["title"]}">
<meta property="og:description" content="{page["desc"]}">
<meta property="og:image" content="{SITE_URL}/{og_crop(page["og"], page["slug"])}">
<meta property="og:url" content="{SITE_URL}/{page["slug"]}">
<meta property="og:locale" content="uk_UA">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={skin["fonts"]}&display=swap" rel="stylesheet">
<style>
  {skin["css"]}
  :root {{ --display: {skin["display"]}; --body: {skin["body"]}; --ink3: {"#A9A3B3" if dark else "#66626D"}; }}
  {CSS}
</style>
</head>
<body class="{"dark" if dark else ""}">
<div class="bar">Для бізнесу<span class="m-hide"> · відправка Новою поштою по Україні та за кордон</span> · безготівковий розрахунок для компаній</div>
<header class="nav"><div class="wrap">
  <a class="logo" href="https://obiimy.world/" aria-label="Obiimy — на сайт бренду"><img src="{logo}" alt="Obiimy" width="113" height="24"></a>
  <nav class="nav-links" aria-label="Розділи сторінки">{links}</nav>
  <a class="btn btn-gold btn-sm" href="#request">{page["cta"]}</a>
</div></header>
<main>
{body}
</main>
<section class="others" aria-label="Інші програми для бізнесу"><div class="wrap"><span>Інші програми для бізнесу:</span>{others}</div></section>
<footer><div class="wrap"><span>© Obiimy · 100% італійський шовк · виготовлено в Україні · художниця та засновниця — Світлана Сніжко</span><span><a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="https://obiimy.world/pro-nas/">Про нас</a> · <a href="https://obiimy.world/oplata-i-dostavka/">Доставка</a></span></div></footer>
<div class="sticky" id="sticky"><span>{page["sticky"]}</span><a href="#request">{page["cta"]}</a></div>
<script>
(function () {{
  var s = document.getElementById('sticky'), cta = document.querySelector('.hero .cta'), req = document.getElementById('request'), tick = false;
  function chk() {{ tick = false; var c = cta.getBoundingClientRect(), r = req.getBoundingClientRect(); s.classList.toggle('on', c.bottom < 0 && r.top > window.innerHeight * 0.8); }}
  window.addEventListener('scroll', function () {{ if (!tick) {{ tick = true; requestAnimationFrame(chk); }} }}, {{ passive: true }}); chk();
}})();
</script>
</body>
</html>
'''

def hero(eyebrow, h1, lead, cta1, cta2, cta2_href, fine, photo, alt, tag, cls=""):
    return f'''
  <section class="hero{cls}"><div class="wrap">
    <div>
      <p class="eyebrow">{eyebrow}</p>
      <h1 style="margin-top:14px">{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="cta"><a class="btn btn-gold" href="#request">{cta1}</a><a class="btn btn-line" href="{cta2_href}">{cta2}</a></div>
      <p class="fine">{fine} Або одразу: <a href="{PHONE_HREF}">{PHONE}</a></p>
    </div>
    <figure>{img(photo, alt, sizes="(max-width: 960px) 100vw, 50vw", lazy=False, eager_priority=True)}<div class="tag">{tag}</div></figure>
  </div></section>'''

DOCS_FAQ = '<details><summary>Які документи отримує компанія?</summary><p>Рахунок для безготівкової оплати та видаткова накладна. Працюємо з ТОВ і ФОП. Деталі щодо ПДВ уточнюйте в запиті — відповімо разом із розрахунком.</p></details>'
BATCH_FAQ = '<details><summary>Чи однакові речі в партії?</summary><p>Принт і колір у межах партії однакові. Розмір може відрізнятися на 0–2,5 см через ручну обробку краю — це особливість шовку, а не брак.</p></details>'

# ---------------------------------------------------------------- 1. New Year corporate gifts (Maison)
def newyear():
    tiers = [
        ("До 1 000 грн", "Маленький знак уваги", [("Резинка для волосся у коробочці", 700)], "photo/scrunchie.jpg", "Резинка у фірмовій коробочці"),
        ("До 2 000 грн", "Подарунок кожному в команді", [("Твіллі 84 × 5", 1600), ("Хустка паше 44 × 44", 1600)], "photo/paris-bag.jpg", "Твіллі на ручці сумки"),
        ("До 3 500 грн", "Для ключових людей", [("Набір «Пристрасть»: твіллі + резинка", 2200), ("Маска для сну", 2700), ("Хустка 65 × 65", 3200), ("Набір «Натхнення»: твіллі + хустка", 3200)], "photo/box-red.jpg", "Набір у жовтій коробці"),
        ("До 5 000 грн", "Для партнерів і VIP-клієнтів", [("Набір для сну «Піднесення»", 3600), ("Хустка 88 × 88", 4400), ("Набір із трьох твіллі", 4800)], "photo/paris-dots.jpg", "Хустка 88 × 88 на плечах"),
    ]
    tier_html = "".join(f'''
      <div class="card photo">{img(ph, alt, sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">{t}</p><h3>{sub}</h3><div>{"".join(f'<div class="price-row"><span>{n}</span><span class="num">{price(p)}</span></div>' for n, p in items)}</div></div></div>''' for t, sub, items, ph, alt in tiers)
    body = hero("Новий рік 2027 · корпоративні подарунки", "Подарунок, який не залишать у шухляді",
                "Шовкова річ ручної обробки у фірмовій жовтій коробці з листівкою від вашої компанії. Один принт на всю команду або добірка під кожного — від 700 грн.<span class=\"m-hide\"> Від резинки до набору з трьох твіллі.</span>",
                "Отримати добірку і розрахунок", "Замовити зразок у роздріб", SAMPLE_URL,
                "Зразок — від 1 600 грн у роздріб, у тій самій коробці, що й тираж.", "photo/box-dots.jpg", "Фірмова жовта коробка Obiimy з шовковою хусткою в горох", "Кожен подарунок — у фірмовій коробці з тонким папером і листівкою") + facts_html([
        ("100% шовк", "Італійський шовк, авторські принти, обробка вручну"),
        ("Україна", "Бренд народився під час війни й підтримує благодійні проєкти"),
        ("700 – 4 800 грн", "Роздрібні ціни: подарунок на будь-який бюджет"),
        ("Зразок сьогодні", "Роздрібні замовлення до 16:00 відправляємо того ж дня; тираж — за графіком"),
    ]) + f'''

  <section class="block" id="why"><div class="wrap">
    <div class="head"><p class="eyebrow">Чому шовк</p><h2>Замість солодощів і щоденників</h2><p class="sub">Корпоративний подарунок має трьох ворогів: його з’їдають, забувають або передаровують. Шовкова хустка живе в гардеробі роками й щоразу нагадує, хто її подарував.</p></div>
    <div class="grid4">
      <div class="card"><span class="k">01</span><h3>Зроблено в Україні</h3><p>Авторські принти художниці Світлани Сніжко, друк і ручна обробка в Україні. Подарунок, за який не соромно перед командою і партнерами.</p></div>
      <div class="card"><span class="k">02</span><h3>Один бюджет — різні речі</h3><p>Резинка, твіллі, маска для сну, хустка трьох розмірів, набори. Можна дати кожному вибір у межах однієї суми.</p></div>
      <div class="card"><span class="k">03</span><h3>Листівка від вас</h3><p>Підпис на подарунок за вашим текстом — стандартна послуга Obiimy. Для компаній — листівка з вашим привітанням у кожній коробці.</p></div>
      <div class="card"><span class="k">04</span><h3>Доставка кожному</h3><p>В офіс однією посилкою або кожному співробітнику на його відділення Нової пошти — зручно для віддалених команд.</p></div>
    </div>
  </div></section>

  <section class="block alt" id="budgets"><div class="wrap">
    <div class="head"><p class="eyebrow">Бюджети</p><h2>Чотири бюджети, один рівень якості</h2><p class="sub">Роздрібні ціни з obiimy.world. Умови для тиражу залежать від кількості й термінів — надішліть запит, і ми повернемось із розрахунком.</p></div>
    <div class="grid4">{tier_html}</div>
    <p style="margin-top:28px"><a class="btn btn-gold" href="#request">Отримати розрахунок на цей бюджет</a></p>
  </div></section>

  <section class="block" id="personal"><div class="wrap grid2">
    <figure>{img("photo/box-gold.jpg", "Набір «Золоте світло» у фірмовій коробці", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
    <div><p class="eyebrow">Персоналізація</p><h2 style="margin-top:10px">Ваш бренд — делікатно</h2>
      <div class="faq" style="margin-top:22px">
        <details open><summary>Листівка з вашим привітанням</summary><p>Текст від компанії або керівника, за бажанням — підпис від руки. Це та сама послуга «підпис на подарунок», яку Obiimy робить для кожного замовлення.</p></details>
        <details><summary>Принти під кольори бренду</summary><p>У колекціях є монограмні, геометричні та квіткові принти в різних кольорах. Підберемо ті, що збігаються з вашою айдентикою, — від стриманого до святкового.</p></details>
        <details><summary>Однакові чи різні</summary><p>Один принт на всю команду виглядає як уніформа події; добірка різних принтів у межах бюджету дає кожному відчуття особистого подарунка. Робимо обидва варіанти.</p></details>
        <details><summary>Сертифікати для віддалених команд</summary><p>Якщо зібрати розміри й адреси неможливо — подарункові сертифікати Obiimy: людина обирає річ сама, а ви дотримуєтесь бюджету.</p></details>
      </div>
    </div>
  </div></section>

  <section class="block alt" id="timeline"><div class="wrap">
    <div class="head"><p class="eyebrow">Терміни</p><h2>Щоб коробки були на столах до свят</h2><p class="sub">Рекомендований графік. Бюджети на подарунки затверджують у жовтні–листопаді, а Нова пошта перед святами перевантажена — тому відправляємо до 10 грудня.</p></div>
    <div class="timeline">
      <div><p class="eyebrow">Крок 1</p><b>Жовтень</b><p>Запит і зразок. Надсилаємо добірку принтів і комерційну пропозицію на тираж — для погодження бюджету.</p></div>
      <div><p class="eyebrow">Крок 2</p><b>До 15 листопада</b><p>Погодження принтів, тексту листівки та списку адрес. Оплата за рахунком.</p></div>
      <div><p class="eyebrow">Крок 3</p><b>До 10 грудня</b><p>Пакування й відправка: в офіс однією посилкою або кожному на відділення — до передсвяткового піку пошти.</p></div>
    </div>
    <p class="note">Запити після 15 листопада беремо в роботу з принтами, що є в наявності на складі. Зразок — одна річ у роздріб уже сьогодні, у тій самій коробці, що й тираж: <a href="{SAMPLE_URL}" style="font-weight:600">замовити зразок →</a></p>
  </div></section>

  <section class="block alt" id="sense"><div class="wrap grid2">
    <div><p class="eyebrow">Більше, ніж шовк</p><h2 style="margin-top:10px">Подарунок із продовженням</h2><p style="margin-top:16px;color:var(--ink2);max-width:36em">Колекція «Співоча душа» створена разом із художницею Анною Кловак та Українським товариством охорони птахів: частина коштів іде на гніздівлі для сиворакші — птаха, що зникає. Обравши цю колекцію для команди, ви даруєте не лише шовк.</p><a class="btn btn-line" style="margin-top:22px" href="https://obiimy.world/spivocha-dusha/">Колекція «Співоча душа»</a></div>
    <figure>{img("img/life2.webp", "Хустка з колекції «Співоча душа»", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
  </div></section>


  {proof_html("Де вже є Obiimy", "Obiimy продається у роздрібних партнерів в Україні та за кордоном, а історію бренду розповідали LIGA.net та INSIDER UA.")}

  <section class="block" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Питання</p><h2>Що зазвичай питають</h2></div>
    <div class="faq">
      <details><summary>Який мінімальний тираж?</summary><p>Фіксованого мінімуму немає — обговорюємо кожен запит окремо. Від кількості залежать терміни та умови, тому просимо вказати її в запиті.</p></details>
      {DOCS_FAQ}
      {BATCH_FAQ}
      <details><summary>Чи можна доставити кожному співробітнику окремо?</summary><p>Так. Надішліть список адресатів із відділеннями Нової пошти — відправимо кожному окремо, з листівкою всередині. Вартість відправок рахуємо в загальному розрахунку.</p></details>
      <details><summary>А якщо річ не підійде?</summary><p>Речі без слідів носіння обмінюємо на інший принт або розмір за стандартними умовами Obiimy. Умови для нерозданого залишку фіксуємо в рахунку.</p></details>
      <details><summary>Чи відправляєте за кордон?</summary><p>Так, міжнародна доставка — за тарифами перевізника. Для команд за кордоном зручні сертифікати або відправка на одну адресу.</p></details>
    </div>
    <p class="note" style="display:flex;flex-wrap:wrap;align-items:center;gap:12px 20px">Не знайшли відповіді — напишіть, відповімо разом із розрахунком. <a class="btn btn-gold btn-sm" href="#request">Запит</a></p>
  </div></section>

  <section class="form-block alt" id="request"><div class="wrap">
    <div class="contact"><p class="eyebrow">Напишіть нам</p><h2>Отримати добірку і розрахунок</h2><p>Розкажіть про команду й бюджет — повернемось із добіркою принтів, цінами на тираж і графіком.</p><p class="big"><a href="{PHONE_HREF}">{PHONE}</a></p><p><a href="mailto:{MAIL}">{MAIL}</a></p></div>
    <div>{form_html("f-ny", "Корпоративні подарунки до Нового року", [
        ("company", "Компанія", "input", True, {"ph": "Назва компанії", "ac": "organization"}),
        ("name", "Ваше ім’я", "input", True, {"ph": "Як до вас звертатись", "ac": "name"}),
        ("phone", "Телефон", "tel", True, {"ph": "+380", "ac": "tel", "err": "Вкажіть номер телефону"}),
        ("email", "Email", "email", True, {"ph": "для добірки та розрахунку", "ac": "email", "err": "Вкажіть коректний email"}),
        ("qty", "Кількість подарунків", "number", False, {"ph": "наприклад, 30"}),
        ("budget", "Бюджет на один подарунок", "select:до 1 000 грн|до 2 000 грн|до 3 500 грн|до 5 000 грн|інший", False, {}),
        ("delivery", "Доставка", "select:В офіс однією посилкою|Кожному на відділення Нової пошти|Ще не знаю", False, {}),
        ("payment", "Оплата", "select:Безготівково, ТОВ|Безготівково, ФОП|Карткою", False, {}),
        ("deadline", "Коли потрібно отримати", "input", False, {"ph": "наприклад, до 10 грудня", "full": True}),
        ("note", "Коментар", "textarea", False, {"ph": "Побажання до принтів, текст листівки, особливі терміни…"}),
    ], "Відповідаємо з добіркою та розрахунком.")}</div>
  </div></section>
  <section class="block alt" id="after"><div class="wrap">
    <div class="head"><p class="eyebrow">Після Нового року</p><h2>Подарунки не лише на Новий рік</h2><p class="sub">8 березня, дні народження, welcome-box для нових співробітників, подяка клієнтам. Для компаній, які дарують не раз на рік, є річна програма.</p></div>
    <div class="grid3">
      <div class="card"><p class="eyebrow">Березень</p><h3>8 березня</h3><p>Твіллі або паше в одному принті — подарунок жіночій частині команди, який не виглядає формальністю.</p></div>
      <div class="card"><p class="eyebrow">Щомісяця</p><h3>Дні народження</h3><p>Іменинникам за списком на місяць — відправляємо кожному на відділення.</p></div>
      <div class="card"><p class="eyebrow">Постійно</p><h3>Welcome-box</h3><p>Новому співробітнику в перший день — шовкова річ у фірмовій коробці з привітанням.</p></div>
    </div>
    <p class="note"><a href="b2b-calendar" style="font-weight:600">Річна програма подарунків →</a></p>
  </div></section>'''
    return dict(slug="b2b-newyear", skin="maison", title="Корпоративні подарунки на Новий рік 2027 — Obiimy",
                desc="Шовкові подарунки для команди та партнерів: від 700 до 4 800 грн, у фірмовій коробці з листівкою від вашої компанії. Доставка кожному співробітнику Новою поштою.",
                og="photo/box-dots.jpg", nav=[("Чому шовк", "why"), ("Бюджети", "budgets"), ("Терміни", "timeline"), ("Питання", "faq"), ("Контакт", "request")],
                cta="Запит", sticky="Корпоративні подарунки · від 700 грн", body=body)

# ---------------------------------------------------------------- 2. HoReCa / uniform (Noir)
def horeca():
    cases = [
        ("Готелі", "Твіллі для рецепції та консьєржів, шовкова маска для сну як VIP-amenity у номері.", "photo/turban-bath.jpg", "Шовковий тюрбан у ванній готелю"),
        ("Ресторани та бари", "Паше 44 × 44 як нашийна хустка хостес — один принт на команду, що не м’яється за вечір.", "photo/vyr-1.webp", "Шовкова хустка на білому пальті"),
        ("Авіація та бізнес-джети", "Хустка 65 × 65 у кольорах, близьких до айдентики авіакомпанії, — з колекцій Obiimy; твіллі в нагрудній кишені — для чоловічої частини команди.", "photo/makiv-knot.webp", "Хустка вузлом на білій сорочці"),
        ("Банки та private banking", "Стримані монограмні принти для менеджерів; та сама хустка — як подарунок клієнту.", "photo/hratsiia-1.webp", "Хустка на синьому жакеті"),
    ]
    cases_html = "".join(f'<div class="card photo">{img(ph, alt, sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><h3>{t}</h3><p>{d}</p></div></div>' for t, d, ph, alt in cases)
    body = hero("HoReCa · сервіс · уніформа", "Шовк у вашому дрес-коді",
                "Хустка на шиї хостес, твіллі на рецепції, маска для сну у VIP-номері — принти Obiimy під кольори вашого бренду.<span class=\"m-hide\"> Одна деталь зі 100% італійського шовку робить уніформу впізнаваною.</span>",
                "Запросити капсулу принтів", "Замовити зразок у роздріб", "https://obiimy.world/khustky/",
                "Виготовлено в Україні. Дозамовлення при зміні складу команди — з тих самих принтів.", "photo/paris-blazer.jpg", "Червона шовкова хустка на чорному жакеті", "Хустка 44 × 44 · один вузол — і образ зібраний") + facts_html([
        ("100% шовк", "Італійський шовк, авторські принти, обробка вручну"),
        ("від 1 600 грн", "Роздрібна ціна паше або твіллі на одну людину"),
        ("Поштучно", "Дозамовлення з наявності на складі — того ж дня, якщо до 16:00"),
        ("30 °C", "Ручне прання, сушити в тіні — картка догляду в коробці"),
    ]) + f'''

  <section class="block" id="cases"><div class="wrap">
    <div class="head"><p class="eyebrow">Сценарії</p><h2>Де шовк працює на бренд</h2><p class="sub">Чотири формати уніформи, які ми пропонуємо. У кожному — стандартні речі з каталогу Obiimy, тож зразок можна замовити сьогодні й приміряти на команді за кілька днів.</p></div>
    <div class="grid4">{cases_html}</div>
    <p class="note">Салони краси, бутики й шоуруми, яким шовк потрібен на продаж, — це <a href="b2b-wholesale" style="font-weight:600">оптова програма →</a></p>
  </div></section>

  <section class="block alt" id="range"><div class="wrap">
    <div class="head"><p class="eyebrow">Асортимент для уніформи</p><h2>Три речі, які тримають форму</h2></div>
    <div class="grid3">
      <div class="card photo">{img("photo/enerhiia-knot.webp", "Паше 44 × 44 вузлом на шиї", sizes="(max-width: 640px) 100vw, 33vw")}<div class="in"><h3>Паше 44 × 44</h3><p>Нашийна хустка або в кишеню жакета. Найпрактичніший розмір для щоденної зміни.</p><div class="price-row"><span>Роздріб</span><span class="num">від 1 600 грн</span></div></div></div>
      <div class="card photo">{img("photo/paris-belt.jpg", "Твіллі як пояс на тренчі", sizes="(max-width: 640px) 100vw, 33vw")}<div class="in"><h3>Твіллі 84 × 5</h3><p>На шию, зап’ястя, ручку сумки або в нагрудну кишеню. Один принт — на всю команду.</p><div class="price-row"><span>Роздріб</span><span class="num">1 600 грн</span></div></div></div>
      <div class="card photo">{img("photo/riviera-boat.jpg", "Хустка 65 × 65 на плечах", sizes="(max-width: 640px) 100vw, 33vw")}<div class="in"><h3>Хустка 65 × 65</h3><p>Класичний формат для авіації та рецепцій: вузол, пов’язка, на плечі.</p><div class="price-row"><span>Роздріб</span><span class="num">від 3 200 грн</span></div></div></div>
    </div>
    <p class="note">Ціни роздрібні з obiimy.world. Умови для команд — за запитом, залежно від кількості й термінів. Рекомендуємо дві речі на людину: одна в зміні, одна в пранні.</p>
  </div></section>

  <section class="block" id="calc"><div class="wrap grid2" style="align-items:start">
    <div><p class="eyebrow">Орієнтир</p><h2 style="margin-top:10px">Скільки це на команду</h2><p style="margin-top:14px;color:var(--ink2);max-width:34em">Порахуйте за роздрібними цінами — це верхня межа. Умови для тиражу надішлемо у відповідь на запит.</p></div>
    <div class="calc" id="calcbox">
      <div class="row">
        <label>Людей у команді<input type="number" id="c-n" value="12" min="1" inputmode="numeric"></label>
        <label>Річ<select id="c-item"><option value="1600">Паше 44 × 44 · 1 600 грн</option><option value="1600">Твіллі 84 × 5 · 1 600 грн</option><option value="3200">Хустка 65 × 65 · 3 200 грн</option><option value="2700">Маска для сну (amenity) · 2 700 грн</option></select></label>
        <label>На людину / номер<select id="c-per"><option value="1">1 річ</option><option value="2" selected>2 речі (зміна + прання)</option></select></label>
      </div>
      <div class="out"><b class="num" id="c-out">38 400 грн</b><span>орієнтовно за роздрібними цінами · <span id="c-pcs">24</span> шт.</span><a class="btn btn-line btn-sm" href="#request" id="c-send">Надіслати цей розрахунок у запит</a></div>
    </div>
  </div></section>
  <script>
  (function () {{
    var n = document.getElementById('c-n'), it = document.getElementById('c-item'), per = document.getElementById('c-per'), out = document.getElementById('c-out'), pcs = document.getElementById('c-pcs');
    function fmt(x) {{ return String(x).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, '\\u202f') + '\\u00a0грн'; }}
    function upd() {{ var q = Math.max(1, +n.value || 1) * +per.value; pcs.textContent = q; out.textContent = fmt(q * +it.value); }}
    [n, it, per].forEach(function (el) {{ el.addEventListener('input', upd); el.addEventListener('change', upd); }});
    upd();
    document.getElementById('c-send').addEventListener('click', function () {{ var t = document.querySelector('#f-hr [name="note"]'), ppl = document.querySelector('#f-hr [name="people"]'); if (ppl && !ppl.value) ppl.value = n.value; var sel = document.querySelector('#f-hr [name="items"]'); if (sel) {{ var txt = it.options[it.selectedIndex].text.split(' · ')[0]; for (var k = 0; k < sel.options.length; k++) if (txt.indexOf(sel.options[k].text.split(' (')[0]) === 0) sel.selectedIndex = k; }} if (t) {{ var line = 'Орієнтир із калькулятора: ' + it.options[it.selectedIndex].text + ', ' + pcs.textContent + ' шт., ' + out.textContent; t.value = t.value ? t.value + String.fromCharCode(10) + line : line; }} }});
  }})();
  </script>

  <section class="block alt" id="care"><div class="wrap grid2">
    <div><p class="eyebrow">Догляд і ресурс</p><h2 style="margin-top:10px">Що варто знати про шовк в уніформі</h2>
      <div class="faq" style="margin-top:22px">
        <details open><summary>Прання</summary><p>Ручне прання при температурі до 30 °C, без віджимання, сушити в тіні. Ми додаємо картку догляду в кожну коробку — можна повісити в службовій кімнаті.</p></details>
        <details><summary>Ресурс і дозамовлення</summary><p>Шовк із ручною обробкою краю служить роками. Коли змінюється склад команди — дозамовляєте той самий принт поштучно.</p></details>
        {BATCH_FAQ}
        {DOCS_FAQ}
        <details><summary>Індивідуальний принт</summary><p>Базова пропозиція — добірка з колекцій Obiimy під ваші кольори. Розробку окремого принту з вашою айдентикою обговорюємо індивідуально: терміни і тираж залежать від задачі.</p></details>
      </div>
    </div>
    <figure>{img("photo/turban.jpg", "Шовковий тюрбан", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
  </div></section>

  <section class="block" id="how"><div class="wrap">
    <div class="head"><p class="eyebrow">Як це працює</p><h2>Від запиту до першої зміни</h2></div>
    <div class="steps">
      <div><h3>Запит</h3><p>Тип закладу, кількість людей, кольори бренду.</p></div>
      <div><h3>Капсула</h3><p>Три–п’ять принтів під вашу айдентику з цінами на тираж.</p></div>
      <div><h3>Зразки</h3><p>Речі з каталогу — замовити в роздріб і приміряти на команді. <a href="https://obiimy.world/khustky/">Каталог →</a></p></div>
      <div><h3>Партія</h3><p>Пакування поштучно або в один короб — як зручно для видачі.</p></div>
      <div><h3>Дозамовлення</h3><p>Ті самі принти для нових співробітників.</p></div>
    </div>
  </div></section>
  {proof_html("Де вже є Obiimy", "Obiimy продається у роздрібних партнерів в Україні та за кордоном, а історію бренду розповідали LIGA.net та INSIDER UA.")}

  <section class="form-block" id="request"><div class="wrap">
    <div class="contact"><p class="eyebrow">Напишіть нам</p><h2>Запросити капсулу принтів</h2><p>Напишіть, що за заклад і скільки людей — повернемось із добіркою принтів під ваші кольори та розрахунком.</p><p class="big"><a href="{PHONE_HREF}">{PHONE}</a></p><p><a href="mailto:{MAIL}">{MAIL}</a></p></div>
    <div>{form_html("f-hr", "Шовк для уніформи / HoReCa", [
        ("company", "Заклад або компанія", "input", True, {"ph": "Назва", "ac": "organization"}),
        ("name", "Ваше ім’я", "input", True, {"ph": "Як до вас звертатись", "ac": "name"}),
        ("phone", "Телефон", "tel", True, {"ph": "+380", "ac": "tel", "err": "Вкажіть номер телефону"}),
        ("email", "Email", "email", True, {"ph": "для капсули та розрахунку", "ac": "email", "err": "Вкажіть коректний email"}),
        ("people", "Людей у команді", "number", False, {"ph": "наприклад, 12"}),
        ("items", "Що цікавить", "select:Паше 44 × 44|Твіллі 84 × 5|Хустка 65 × 65|Маска для сну (amenity)|Комбінація", False, {}),
        ("venue", "Тип закладу та кольори бренду", "input", False, {"ph": "наприклад, готель 5*, бордовий і золото", "full": True}),
        ("payment", "Оплата", "select:Безготівково, ТОВ|Безготівково, ФОП|Карткою", False, {}),
        ("start", "Коли потрібна перша партія", "input", False, {"ph": "наприклад, до відкриття 1 грудня"}),
        ("note", "Коментар", "textarea", False, {"ph": "Кількість змін, терміни, побажання до принтів…"}),
    ], "Відповідаємо з капсулою принтів і розрахунком.")}</div>
  </div></section>'''
    return dict(slug="b2b-horeca", skin="noir", title="Шовкові хустки для уніформи HoReCa — Obiimy",
                desc="Хустки, твіллі та маски для сну зі 100% італійського шовку для готелів, ресторанів, авіації та банків. Капсула принтів під кольори вашого бренду, дозамовлення поштучно.",
                og="photo/paris-blazer.jpg", nav=[("Сценарії", "cases"), ("Асортимент", "range"), ("Орієнтир", "calc"), ("Догляд", "care"), ("Контакт", "request")],
                cta="Запит", sticky="Шовк для уніформи · капсула принтів", body=body)

# ---------------------------------------------------------------- 3. Wholesale / retail partners (Journal)
def wholesale():
    cats = [
        ("Хустки 44 · 65 · 88", "Три розміри, дев’ять і більше принтів, хіти «Єднання» та «Пробудження».", "1 600 – 4 400 грн", "img/probudzhennia.webp"),
        ("Двосторонній друк", "Два принти на одній хустці — річ, яку покупчиня показує подругам.", "2 400 – 4 800 грн", "img/yednannia.webp"),
        ("Твіллі 84 × 5", "Імпульсний подарунок: на сумку, у волосся, на зап’ястя.", "1 600 грн", "img/twilly-zolote.webp"),
        ("Маски для сну", "Шовк, авторський принт, фірмова коробка. Категорія «догляд», не лише «аксесуар».", "2 700 грн", "img/mask-vpevnenist.webp"),
        ("Резинки", "Вхідна ціна в бренд і товар біля каси у фірмовій коробочці.", "700 грн", "img/scrunchie-energiia.webp"),
        ("Подарункові набори", "Твіллі + резинка, твіллі + хустка, набір для сну, три твіллі — у жовтій коробці.", "2 200 – 4 800 грн", "img/set-natkhnennia.webp"),
    ]
    cats_html = "".join(f'<div class="card">{img(ph, t, sizes="(max-width: 640px) 100vw, 33vw")}<h3>{t}</h3><p>{d}</p><div class="price-row"><span>Роздріб</span><span class="num">{pr}</span></div></div>' for t, d, pr, ph in cats)
    body = hero("Для магазинів, бутиків і корнерів", "Obiimy на вашій полиці",
                "Український бренд шовкових хусток із власними принтами, який уже продається в INTERTOP, Hram, Be Brave (Канада) та UFD London.<span class=\"m-hide\"> Пропонуємо партнерам готову вітрину: асортимент, коробки, фотоконтент та історію, яку легко розповісти покупцю.</span>",
                "Запросити оптовий прайс", "Асортимент", "#range",
                "Відправка Новою поштою по Україні, за кордон — за тарифами перевізника.", "photo/paris-dots.jpg", "Хустка 88 × 88 у горох на білому костюмі", "Фотоконтент двох зйомок — для ваших соцмереж і вітрини") + facts_html([
        ("3 країни", "Роздрібні партнери в Україні, Канаді та Великій Британії"),
        ("6 категорій", "Хустки, двосторонні, твіллі, маски для сну, резинки, набори"),
        ("700 – 4 800 грн", "Роздрібні ціни на obiimy.world — орієнтир для полиці"),
        ("Дозамовлення", "Поштучно з наявності — того ж дня, якщо до 16:00"),
    ]) + f'''

  <section class="block" id="range"><div class="wrap">
    <div class="head"><p class="eyebrow">Асортимент</p><h2>Шість категорій, один впізнаваний стиль</h2><p class="sub">Роздрібні ціни з obiimy.world — для орієнтиру. Оптові умови надсилаємо після запиту.</p></div>
    <div class="grid3">{cats_html}</div>
  </div></section>
  {proof_html("Де вже є Obiimy", "Obiimy продається у роздрібних партнерів в Україні та за кордоном, а історію бренду розповідали LIGA.net та INSIDER UA.")}

  <section class="block" id="partner"><div class="wrap grid2">
    <figure>{img("photo/box-green.jpg", "Набір Obiimy у фірмовій коробці", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
    <div><p class="eyebrow">Що отримує партнер</p><h2 style="margin-top:10px">Вітрина, готова до продажу</h2>
      <div class="faq" style="margin-top:22px">
        <details open><summary>Упаковка як частина продукту</summary><p>Кожна річ — у фірмовій жовтій коробці з тонким папером. На полиці це видно з іншого кінця залу.</p></details>
        <details><summary>Фото та відео</summary><p>Дві лукбук-зйомки (Париж, Рів’єра), пакшоти всіх речей і відео — для соцмереж, сайту й вітрини.</p></details>
        <details><summary>Історія, яку легко розповісти</summary><p>Художниця-засновниця Світлана Сніжко, 100% італійський шовк, ручна обробка, бренд, що народився під час війни, і колекція «Співоча душа» з благодійною складовою.</p></details>
        <details><summary>Пам’ятка для консультантів</summary><p>Коротка пам’ятка: три способи носити кожен розмір, догляд, аргументи для подарунка.</p></details>
        <details><summary>Дозамовлення</summary><p>Замовлення до 16:00 відправляємо з наявності того ж дня — партнер не тримає великий склад.</p></details>
      </div>
    </div>
  </div></section>

  <section class="block" id="formats"><div class="wrap">
    <div class="head"><p class="eyebrow">Формати співпраці</p><h2>Три формати</h2></div>
    <div class="grid3">
      <div class="card"><span class="k">A</span><h3>Оптова закупівля</h3><p>Ви купуєте партію за оптовими цінами й продаєте за своєю. Найпростіший формат для бутиків і мультибрендів.</p></div>
      <div class="card"><span class="k">B</span><h3>Корнер бренду</h3><p>Виділена зона Obiimy у вашому магазині з фірмовою викладкою та коробками. Для універмагів і концепт-сторів.</p></div>
      <div class="card"><span class="k">C</span><h3>Міжнародний партнер</h3><p>Для магазинів за кордоном: відправка партій за тарифами перевізника, англомовний контент і сайт obiimy-world.com.</p></div>
    </div>
    <div class="faq" style="margin-top:32px">
      <details><summary>Повернення нерозпроданого</summary><p>Умови для залишків узгоджуємо в договорі — це предмет домовленості, а не стандартна опція.</p></details>
      {DOCS_FAQ}
    </div>
  </div></section>

  <section class="form-block alt" id="request"><div class="wrap">
    <div class="contact"><p class="eyebrow">Напишіть нам</p><h2>Запросити оптовий прайс</h2><p>Розкажіть про магазин і місто. У відповідь надішлемо оптовий прайс із мінімальною партією та знижкою по категоріях, каталог із фото та умови для вашого формату — корнер чи ексклюзив у місті.</p><p class="big"><a href="{PHONE_HREF}">{PHONE}</a></p><p><a href="mailto:{MAIL}">{MAIL}</a></p></div>
    <div>{form_html("f-ws", "Оптова співпраця", [
        ("company", "Магазин або компанія", "input", True, {"ph": "Назва", "ac": "organization"}),
        ("name", "Ваше ім’я", "input", True, {"ph": "Як до вас звертатись", "ac": "name"}),
        ("phone", "Телефон", "tel", True, {"ph": "+380", "ac": "tel", "err": "Вкажіть номер телефону"}),
        ("email", "Email", "email", True, {"ph": "для прайсу та каталогу", "ac": "email", "err": "Вкажіть коректний email"}),
        ("store", "Місто, формат магазину, сайт або Instagram", "input", False, {"ph": "наприклад, концепт-стор у Львові, @store", "full": True}),
        ("format", "Формат співпраці", "select:Оптова закупівля|Корнер бренду|Міжнародний партнер|Ще не знаю", False, {}),
        ("qty", "Орієнтовна перша партія, шт.", "number", False, {"ph": "наприклад, 40"}),
        ("payment", "Оплата", "select:Безготівково, ТОВ|Безготівково, ФОП|Інше", False, {}),
        ("start", "Коли плануєте старт", "input", False, {"ph": "наприклад, перед святами"}),
        ("note", "Коментар", "textarea", False, {"ph": "Скільки брендів на полиці, які категорії цікавлять, побажання до асортименту…"}),
    ], "Відповідаємо з прайсом і каталогом.")}</div>
  </div></section>'''
    return dict(slug="b2b-wholesale", skin="journal", title="Шовкові хустки оптом для магазинів — Obiimy",
                desc="Український бренд шовкових хусток для бутиків, універмагів і магазинів за кордоном: асортимент, фірмова упаковка, фотоконтент, швидке дозамовлення поштучно.",
                og="photo/paris-dots.jpg", nav=[("Асортимент", "range"), ("Довіра", "proof"), ("Для партнера", "partner"), ("Формати", "formats"), ("Контакт", "request")],
                cta="Прайс", sticky="Оптова співпраця · прайс і каталог", body=body)

# ---------------------------------------------------------------- 4. Year-round corporate gifting programme (Lookbook)
def calendar():
    months = [
        ("Грудень", "Новий рік і Різдво", "Коробки для команди та партнерів. Найбільший сезон — плануємо з жовтня.", "img/set-3twilly.webp", "Набір із трьох твіллі"),
        ("Березень", "8 березня", "Подарунок жіночій частині команди, який не виглядає формальністю: твіллі або паше в одному принті.", "photo/paris-bun.jpg", "Шовкова резинка у зачісці"),
        ("Травень", "День матері", "Для клієнток і партнерок — хустка 65 × 65 із листівкою від компанії.", "photo/kolo-2.webp", "Хустка на бежевому пальті"),
        ("Червень–серпень", "Конференції та івенти", "Спікерам і гостям — твіллі в коробочці замість блокнота з логотипом.", "photo/dotyk-1.webp", "Хустка на тренчі"),
        ("Щомісяця", "Дні народження", "Іменинникам — подарунок за списком на місяць, відправляємо кожному на відділення.", "img/scrunchie-pole.webp", "Резинка у коробочці"),
        ("Постійно", "Welcome-box", "Новому співробітнику в перший день — шовкова річ у фірмовій коробці з привітанням.", "img/set-zolote.webp", "Набір у фірмовій коробці"),
        ("Постійно", "Подяка клієнтам", "Закриття великої угоди, річниця співпраці — набір «Натхнення» або хустка 88 × 88.", "photo/riviera-red.jpg", "Червона шовкова хустка на зап’ясті"),
        ("Дата компанії", "Річниця бренду", "Один принт на всю команду — і фото на згадку в один день.", "photo/riviera-car.jpg", "Хустка на голові за кермом кабріолета"),
    ]
    months_html = "".join(f'<div class="card photo">{img(ph, alt, sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">{m}</p><h3>{t}</h3><p>{d}</p></div></div>' for m, t, d, ph, alt in months)
    body = hero("Річна програма · корпоративні подарунки", "Один список адрес —\u00a0і подарунки їдуть самі",
                "Погоджений бюджет, добірка під кожну нагоду, відправка кожному адресату за графіком. Від вас — лише список.<span class=\"m-hide\"> Для компаній, які дарують не раз на рік — від Нового року до welcome-box.</span>",
                "Скласти річний план подарунків", "Календар нагод", "#year",
                "Від 700 грн за подарунок. Список адресатів — від вас, усе інше — від нас.", "photo/paris-green.jpg", "Зелена шовкова хустка на бежевому жакеті", "Вісім нагод на рік · один бюджет · один список", cls=" h1-sm") + facts_html([
        ("8 нагод", "Від Нового року до welcome-box і подяки клієнтам"),
        ("700 – 4 800 грн", "Роздрібні ціни: різні речі в межах одного бюджету"),
        ("Один список", "ПІБ, дати й відділення Нової пошти — решту робимо ми"),
        ("Звіт", "Після кожної відправки — номери накладних"),
    ]) + f'''

  <section class="block" id="year"><div class="wrap">
    <div class="head"><p class="eyebrow">Календар</p><h2>Рік у восьми коробках</h2><p class="sub">Нагоди, з якими до нас приходять компанії, і що ми для них пропонуємо. Усе — стандартні речі з каталогу Obiimy за роздрібними цінами від 700 до 4 800 грн.</p></div>
    <div class="grid4">{months_html}</div>
  </div></section>

  <section class="block alt" id="program"><div class="wrap grid2">
    <div><p class="eyebrow">Річна програма</p><h2 style="margin-top:10px">Як це влаштовано</h2>
      <div class="steps" style="grid-template-columns:1fr;gap:18px;margin-top:22px">
        <div><h3>Бюджет і нагоди</h3><p>Ви визначаєте, кому й на що даруєте протягом року, і бюджет на один подарунок.</p></div>
        <div><h3>Добірка на рік</h3><p>Ми пропонуємо речі та принти під кожну нагоду — так, щоб подарунки не повторювались.</p></div>
        <div><h3>Список адрес</h3><p>Один документ із ПІБ, датами та відділеннями Нової пошти. Оновлюєте, коли змінюється команда.</p></div>
        <div><h3>Відправки за графіком</h3><p>Перед кожною датою пакуємо, підписуємо листівки й відправляємо. Ви отримуєте звіт із номерами накладних.</p></div>
      </div>
    </div>
    <figure>{img("photo/vyr-2.webp", "Хустка на голові, вид зі спини", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
  </div></section>

  <section class="block" id="budgets"><div class="wrap">
    <div class="head"><p class="eyebrow">Бюджети</p><h2>Що входить у кожен бюджет</h2></div>
    <div class="grid4">
      <div class="card"><p class="eyebrow">До 1 000 грн</p><h3>Резинка</h3><p>У фірмовій коробочці. Для днів народження та welcome-box.</p><div class="price-row"><span>Роздріб</span><span class="num">700 грн</span></div></div>
      <div class="card"><p class="eyebrow">До 2 000 грн</p><h3>Твіллі або паше</h3><p>Універсальний подарунок для команди на 8 березня і до свят.</p><div class="price-row"><span>Роздріб</span><span class="num">1 600 грн</span></div></div>
      <div class="card"><p class="eyebrow">До 3 500 грн</p><h3>Набір або хустка 65</h3><p>Для ключових людей і клієнтів: набір «Пристрасть», маска для сну, набір «Натхнення», хустка 65 × 65.</p><div class="price-row"><span>Роздріб</span><span class="num">2 200 – 3 200 грн</span></div></div>
      <div class="card"><p class="eyebrow">До 5 000 грн</p><h3>Хустка 88 або три твіллі</h3><p>Партнерам і VIP: набір для сну, хустка 88 × 88, три твіллі в одній коробці.</p><div class="price-row"><span>Роздріб</span><span class="num">3 600 – 4 800 грн</span></div></div>
    </div>
    <p class="note">Умови річної програми залежать від загальної кількості подарунків — надішліть запит, і ми порахуємо.</p>
    <p style="margin-top:16px"><a class="btn btn-gold" href="#request">Скласти план на рік</a></p>
  </div></section>

  <section class="block alt" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Питання</p><h2>Що зазвичай питають</h2></div>
    <div class="faq">
      <details><summary>Скільки подарунків потрібно, щоб це мало сенс?</summary><p>Фіксованого мінімуму немає. Програма зручна вже для команди з десяти людей, якщо ви даруєте два-три рази на рік.</p></details>
      <details><summary>Як відбувається оплата?</summary><p>Поетапно перед кожною відправкою або за узгодженим графіком — фіксуємо в розрахунку.</p></details>
      {DOCS_FAQ}
      {BATCH_FAQ}
      <details><summary>Що, якщо список змінився?</summary><p>Надсилаєте оновлений документ до наступної дати — ми відправляємо за актуальним списком.</p></details>
    </div>
  </div></section>
  {proof_html("Де вже є Obiimy", "Obiimy продається у роздрібних партнерів в Україні та за кордоном, а історію бренду розповідали LIGA.net та INSIDER UA.", first=True)}

  <section class="form-block alt" id="request"><div class="wrap">
    <div class="contact"><p class="eyebrow">Напишіть нам</p><h2>Скласти річний план подарунків</h2><p>Кілька фактів про компанію — і ми запропонуємо календар, добірку та розрахунок на рік.</p><p class="big"><a href="{PHONE_HREF}">{PHONE}</a></p><p><a href="mailto:{MAIL}">{MAIL}</a></p></div>
    <div>{form_html("f-cal", "Річна програма корпоративних подарунків", [
        ("company", "Компанія", "input", True, {"ph": "Назва компанії", "ac": "organization"}),
        ("name", "Ваше ім’я", "input", True, {"ph": "Як до вас звертатись", "ac": "name"}),
        ("phone", "Телефон", "tel", True, {"ph": "+380", "ac": "tel", "err": "Вкажіть номер телефону"}),
        ("email", "Email", "email", True, {"ph": "для календаря та розрахунку", "ac": "email", "err": "Вкажіть коректний email"}),
        ("people", "Людей у команді", "number", False, {"ph": "наприклад, 40"}),
        ("budget", "Бюджет на один подарунок", "select:до 1 000 грн|до 2 000 грн|до 3 500 грн|до 5 000 грн|залежить від нагоди", False, {}),
        ("occasions", "Нагоди, які цікавлять", "input", False, {"ph": "наприклад, Новий рік, 8 березня, дні народження", "full": True}),
        ("delivery", "Доставка", "select:Кожному на відділення Нової пошти|В офіс однією посилкою|Комбіновано", False, {}),
        ("payment", "Оплата", "select:Безготівково, ТОВ|Безготівково, ФОП|Карткою", False, {}),
        ("note", "Коментар", "textarea", False, {"ph": "Побажання до принтів, найближча дата, особливості команди…"}),
    ], "Відповідаємо з календарем і розрахунком.")}</div>
  </div></section>'''
    return dict(slug="b2b-calendar", skin="lookbook", title="Корпоративні подарунки на рік — річна програма Obiimy",
                desc="Річна програма подарунків для компаній: Новий рік, 8 березня, дні народження, welcome-box, подяка клієнтам. Шовк від 700 грн, відправка кожному адресату за графіком.",
                og="photo/paris-green.jpg", nav=[("Календар", "year"), ("Програма", "program"), ("Бюджети", "budgets"), ("Питання", "faq"), ("Контакт", "request")],
                cta="Запит", sticky="Подарунки на цілий рік · від 700 грн", body=body)

for fn in (newyear, horeca, wholesale, calendar):
    page = fn()
    html = typo(shell(page, page["body"]))
    (OUT / f"{page['slug']}.html").write_text(html)
    print(page["slug"], len(html) // 1024, "KB")
