#!/usr/bin/env python3
"""Hidden page for the sales team: /kp — builds a commercial proposal («Пропозиція корпоративного замовлення») like the
client's own offers (cover → photos → table with discount → packaging & personalisation → contacts). Nothing is invented:
prices come from the catalogue (retail, obiimy.world), discount, terms and extras are typed in by the manager.
State lives in the URL hash, so a proposal can be shared by link; printing gives an A4 PDF."""
import importlib.util, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
sys.path.insert(0, str(ROOT))
from imgs import variants, typo
_spec = importlib.util.spec_from_file_location("team", ROOT / "build-b2b-team.py")
team = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(team)
_b = importlib.util.spec_from_file_location("b2b", ROOT / "build-b2b.py")
b2b = importlib.util.module_from_spec(_b); _b.loader.exec_module(b2b)

def photo(src):
    vs, _ = variants(src)
    return next((p for p, w in vs if w >= 800), vs[-1][0])

ITEMS = [dict(k=c["k"], n=c["n"], p=c["p"], ph=photo(c["ph"])) for c in team.CATALOG]
ITEMS += [
    dict(k="h44s", n="Хустка 44 × 44, односторонній друк", p=1600, ph=photo("photo/hratsiia-flat.webp")),
    dict(k="h65d", n="Хустка 65 × 65, двосторонній друк", p=4800, ph=photo("img/kolo-sontsia.webp")),
    dict(k="h88d", n="Хустка 88 × 88, двосторонній друк", p=6600, ph=photo("img/prob88.webp")),
    dict(k="tw140", n="Твіллі 140 × 5 «Літній віночок»", p=1850, ph=photo("img/sets/twscr-vinochok140.webp")),
    dict(k="ring", n="Кільце для хустки Gold", p=450, ph=photo("photo/hratsiia-belt.webp")),
    dict(k="tw44d", n="Набір: твіллі та хустка 44 × 44, двосторонній друк", p=3600, ph=photo("img/sets/tw44-zolote.webp")),
    dict(k="twscr140", n="Набір: твіллі 140 × 5 та резинка", p=2700, ph=photo("img/sets/twscr-vinochok140.webp")),
    dict(k="masks2", n="Набір масок «Серцебиття», червона та чорна", p=4200, ph=photo("img/sets/masks-sertsebyttia.webp")),
    dict(k="pilp", n="Шовкова наволочка 50 × 70 з принтом", p=5700, ph=photo("img/sets/pillow-enerhiia.webp")),
    dict(k="custom", n="Інша позиція (вписати)", p=0, ph=photo("photo/box-gold.jpg")),
]
LIFE = {k: photo(f) for k, f in {   # a photograph of the thing worn or in use for the «Що пропонуємо» page (the catalogue carries renders)
    "scr": "photo/site/mask-shchyri-pochuttia-04.jpg", "book": "photo/site/bookmark-melodiia-dvokh-01.jpg", "tw": "photo/solo/krok-tw-2.webp", "tw140": "photo/solo/avantiura-tw-4.webp",
    "h44": "photo/solo/krok-44-3.webp", "h44s": "photo/site/khustka-potsilunok-sontsia-44x44-02.jpg", "h65": "photo/solo/iskra-65-3.webp", "h65d": "photo/solo/flirt-65-3.webp", "h88": "photo/solo/avantiura-88-3.webp", "h88d": "photo/solo/tysha-88-3.webp",
    "mask": "photo/site/mask-vpevnenist-04.jpg", "maskscr": "photo/site/set-ta-rezynka-litnie-pole-04.jpg", "masks2": "photo/site/set-ta-rezynka-litnie-pole-04.jpg", "ring": "photo/site/ring-zoloto-01.jpg",
    "twscr": "photo/site/tvilli-ta-rezynka-makovyi-tsvit-02.jpg", "twscr140": "photo/site/tvilli-ta-rezynka-makovyi-tsvit-02.jpg", "tw44": "photo/paris-dots.jpg", "tw44d": "photo/paris-bag.jpg", "pil": "photo/turban-bath.jpg", "pilp": "photo/turban-bath.jpg",
}.items()}
LIFE_POS = {"scr": "0% 50%", "book": "55% 30%", "tw": "50% 30%", "h44": "50% 20%", "h44s": "50% 0%", "h65": "50% 50%", "h65d": "58% 6%", "h88": "50% 20%", "h88d": "50% 50%", "mask": "50% 25%", "ring": "50% 40%", "twscr": "50% 30%", "tw44": "50% 30%", "tw44d": "50% 50%"}
MOSAIC = [photo(f) for f in ("photo/solo/iskra-65-4.webp", "photo/solo/flirt-tw-1.webp", "photo/site/mask-shchyri-pochuttia-04.jpg", "photo/solo/zolote-44-2.webp", "photo/site/maska-dlia-snu-ta-rezynka-vpevnenist-03.jpg",
                               "photo/solo/tysha-88-4.webp", "photo/solo/krok-44-2.webp", "photo/solo/flirt-65-4.webp")]   # the deck's cover (07.10)
MOSAIC_POS = ["50% 15%", "50% 20%", "0% 50%", "50% 15%", "50% 50%", "50% 10%", "50% 20%", "50% 15%"]
import os as _os
def _lib():
    out = []
    for d, title in (("photo/solo", "SOLO"), ("photo/site", "Сайт"), ("photo", "Редакційні")):
        folder = OUT / d
        for f in sorted(folder.iterdir()):
            if not f.is_file() or f.suffix.lower() not in (".jpg", ".webp") or f.name.startswith(".") or any(f.stem.endswith(x) for x in ("-480", "-800", "-1200", "-wide")): continue
            if d == "photo" and not f.name.startswith(("paris", "riviera", "turban", "dotyk", "enerhiia", "hratsiia", "kolo", "makiv", "mizh", "probudzhennia", "vyr")): continue
            if "flat" in f.name or f.name.endswith("-1.webp") and d == "photo/solo": continue
            out.append(dict(f=photo(str(f.relative_to(OUT))), t=photo(str(f.relative_to(OUT))), g=title, n=f.name))
    return out
LIBRARY = _lib()
FONTS = "".join(f'@font-face {{ font-family: {fam}; font-style: {st}; font-weight: 400; src: url(brand/fonts/{f}) format("woff2"); {ur} }}'
                for fam, st, f, ur in (("Playfair", "normal", "playfair-cyrillic-400-normal.woff2", "unicode-range: U+0400-04FF;"), ("Playfair", "normal", "playfair-latin-400-normal.woff2", ""),
                                       ("Playfair", "italic", "playfair-cyrillic-400-italic.woff2", "unicode-range: U+0400-04FF;"), ("Playfair", "italic", "playfair-latin-400-italic.woff2", ""),
                                       ("Tenor", "normal", "tenor-cyrillic-400-normal.woff2", "unicode-range: U+0400-04FF;"), ("Tenor", "normal", "tenor-latin-400-normal.woff2", "")))
EXTRAS = [  # personalisation levels: id, name, default note; price is typed by the manager (facts: level 1 free)
    ("pack", "Подарункове пакування кожної речі", "безкоштовно"),
    ("stick", "Наліпка з логотипом компанії всередині коробки", "безкоштовно"),
    ("tag", "Нашивна бирка з логотипом", ""),
    ("print", "Друковані матеріали з логотипом (листівка з привітанням)", ""),
    ("design", "Індивідуальний принт для компанії", ""),
    ("deliv", "Доставка", ""),
]
DEFAULT = dict(client="", contact="", manager="", date="", valid="", title="Пропозиція корпоративного замовлення", sub="",
               rows=[dict(k="tw", d="asst", q=100, disc=0, price=None)], ex={}, terms="", pay="", note="", html={})   # html: {page key: edited innerHTML}

HTML = f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Obiimy — конструктор комерційної пропозиції</title>
<style>
  {FONTS}
  :root {{ --ink: #141414; --ink2: #4A4A47; --ink3: #6E6A63; --line: #C9C6C0; --bg: #E7E4DD; --paper: #F1EFEA; --gold: #E7D9A6; --yellow: #FDD31A; --radius: 0; }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: Tenor, 'Tenor Sans', sans-serif; font-size: 14px; line-height: 1.5; font-variant-numeric: lining-nums tabular-nums; }}
  h1, h2, h3 {{ font-family: Playfair, 'Playfair Display', serif; font-weight: 400; margin: 0; line-height: 1.08; letter-spacing: -.01em; }}
  .app {{ display: grid; grid-template-columns: 420px minmax(0, 1fr); min-height: 100vh; }}
  .panel {{ background: var(--paper); border-right: 1px solid var(--line); padding: 22px 22px 60px; overflow: auto; height: 100vh; position: sticky; top: 0; }}
  .panel h1 {{ font-size: 1.7rem; margin-bottom: 4px; }}
  .panel .hint {{ color: var(--ink3); font-size: .8rem; margin: 0 0 16px; }}
  .f {{ display: grid; gap: 4px; margin-bottom: 10px; }}
  .f label {{ font-size: .7rem; letter-spacing: .18em; text-transform: uppercase; color: var(--ink3); }}
  input, select, textarea {{ font: inherit; color: inherit; border: 1px solid var(--line); border-radius: 0; padding: 8px 10px; background: #fff; width: 100%; }}
  textarea {{ min-height: 64px; resize: vertical; }}
  .two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .sec {{ border-top: 1px solid var(--line); padding-top: 14px; margin-top: 14px; }}
  .sec h2 {{ font-size: 1.25rem; margin-bottom: 10px; }}
  .row {{ border: 1px solid var(--line); padding: 10px; margin-bottom: 10px; display: grid; gap: 8px; background: #fff; }}
  .row .g {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }}
  .row .g2 {{ display: grid; grid-template-columns: 1fr auto; gap: 8px; align-items: end; }}
  .row small {{ color: var(--ink3); }}
  .ex {{ display: grid; grid-template-columns: 1fr 110px; gap: 8px; align-items: center; margin-bottom: 6px; font-size: .9rem; }}
  .btn {{ font: inherit; border: 1px solid var(--ink); background: var(--ink); color: #F1EFEA; border-radius: 999px; padding: 9px 16px; cursor: pointer; letter-spacing: .02em; }}
  .btn.line {{ background: transparent; color: var(--ink); }}
  .btn.gold {{ background: var(--yellow); border-color: var(--yellow); color: var(--ink); }}
  .btn.sm {{ padding: 5px 11px; font-size: .82rem; }}
  .acts {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; position: sticky; bottom: 0; background: var(--paper); padding: 12px 0; border-top: 1px solid var(--line); box-shadow: 0 -8px 16px var(--paper); }}
  .ok {{ color: #2b7a3d; font-size: .82rem; }}
  /* document — the deck's pages: paper #F1EFEA, Playfair, gold italic captions on the tiles */
  .doc {{ padding: 28px; display: grid; gap: 22px; justify-items: center; }}
  .pg {{ width: 210mm; height: 297mm; min-height: 297mm; overflow: hidden; background: var(--paper); box-shadow: 0 4px 30px rgba(0,0,0,.1); padding: 16.5mm 16.5mm 14mm; position: relative; display: flex; flex-direction: column; break-after: page; page-break-after: always; }}
  .pg .logo {{ width: 38mm; height: 8.1mm; flex: none; align-self: flex-start; object-fit: contain; object-position: left center; }}
  .pg .foot {{ margin-top: auto; color: var(--ink3); font-size: 7.5pt; letter-spacing: .2em; text-transform: uppercase; display: flex; justify-content: space-between; gap: 10mm; padding-top: 4mm; }}
  .cover {{ padding: 0; display: grid; grid-template-rows: 1fr auto 1fr; }} .cover .mos {{ min-height: 0; }} .cover .mos img {{ height: 100%; }}
  .cover .mos {{ display: grid; grid-template-columns: repeat(2, 1fr); grid-template-rows: repeat(2, 1fr); }} .cover .mos img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .cover .band {{ background: var(--yellow); padding: 10mm 16.5mm; display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 8mm; }}
  .cover .band img {{ width: 46mm; height: auto; display: block; margin-bottom: 4mm; }}
  .cover h1 {{ font-size: 24pt; }} .cover h1 i {{ font-style: italic; color: #4A4A47; }}
  .cover .for {{ font-size: 8pt; letter-spacing: .24em; text-transform: uppercase; margin: 3mm 0 0; color: #141414; }}
  .cover .meta {{ text-align: right; font-size: 8.5pt; line-height: 1.7; color: #141414; }}
  .eb {{ font-size: 7pt; letter-spacing: .24em; text-transform: uppercase; color: var(--ink3); margin: 0 0 3mm; }}
  .pg h2.t {{ font-size: 26pt; margin: 0 0 6mm; }} .pg h2.t i {{ color: #8E8A84; }}
  .pg .from {{ font-family: Playfair, serif; font-style: italic; font-size: 13pt; color: var(--ink2); margin: -4mm 0 6mm; }}
  .photos {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }}
  .photos figure {{ margin: 0; position: relative; overflow: hidden; }}
  .photos img {{ width: 100%; aspect-ratio: 86 / 96; object-fit: cover; display: block; background: #ddd; }}
  .photos figure::after {{ content: ""; position: absolute; inset: 52% 0 0; background: linear-gradient(0deg, rgba(0,0,0,.78) 0%, rgba(0,0,0,.4) 45%, rgba(0,0,0,0) 100%); }}
  .photos figcaption {{ position: absolute; left: 6mm; bottom: 5mm; z-index: 2; color: var(--gold); font-family: Playfair, serif; font-style: italic; font-size: 17pt; line-height: 1.1; }}
  .photos figure.flat::after {{ display: none; }} .photos figure.flat img {{ object-fit: contain; background: #fff; padding: 6mm; }} .photos figure.flat figcaption {{ color: var(--ink); }} .photos figure.flat figcaption span {{ color: var(--ink3); }}
  .photos figcaption span {{ display: block; font-family: Tenor, sans-serif; font-style: normal; font-size: 8.5pt; color: rgba(231,217,166,.85); margin-top: 1mm; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 10pt; }}
  th, td {{ border: 0; border-top: .35pt solid var(--line); padding: 3mm 2mm; text-align: left; vertical-align: top; }}
  th {{ font-weight: 400; font-size: 7pt; letter-spacing: .2em; text-transform: uppercase; color: var(--ink3); border-top: 0; padding-top: 0; }}
  td.num, th.num {{ text-align: right; white-space: nowrap; }}
  tr.tot td {{ border-top: .5pt solid var(--ink); font-family: Playfair, serif; font-size: 12pt; }}
  tr.sum td {{ border-top: .5pt solid var(--ink); border-bottom: .5pt solid var(--ink); font-size: 16pt; font-family: Playfair, serif; }}
  tr.sum td.num small, tr.tot td.num small {{ font-family: Playfair, serif; font-style: italic; font-size: 9pt; color: var(--ink3); }}
  .kv {{ display: grid; grid-template-columns: 1fr; gap: 0; margin-top: 6mm; }}
  .kv div {{ display: grid; grid-template-columns: 48mm 1fr; gap: 6mm; padding: 3mm 0; border-top: .35pt solid var(--line); font-size: 10pt; }}
  .kv div span:first-child {{ font-family: Playfair, serif; font-size: 12pt; color: var(--ink); }}
  .pg p {{ margin: 0 0 3mm; }}
  .contact {{ font-size: 11pt; line-height: 1.8; margin-top: 8mm; }} .contact b {{ font-family: Playfair, serif; font-weight: 400; font-size: 16pt; display: block; margin-bottom: 2mm; }}
  .why3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6mm; margin: 8mm 0 6mm; }}
  .why3 div {{ border-top: .35pt solid var(--ink); padding-top: 3mm; font-size: 9.5pt; color: var(--ink2); }}
  .why3 b {{ display: block; font-family: Playfair, serif; font-weight: 400; font-size: 13pt; color: var(--ink); margin-bottom: 1.5mm; }}
  .fine {{ color: var(--ink3); font-size: 8.5pt; margin-top: 5mm; }}
  .hide {{ display: none; }}
  /* in-place editing: every page is contenteditable, pictures are replaced by a click */
  .pg [contenteditable]:focus {{ outline: none; }} .pg.edit {{ outline: 2px dashed rgba(36,89,201,.45); outline-offset: -2px; }}
  .doc img {{ cursor: pointer; }} .doc img:hover {{ outline: 2px solid #2459c9; outline-offset: -2px; }}
  .pgtools {{ position: absolute; right: 8mm; top: 6mm; display: flex; gap: 6px; opacity: 0; transition: opacity .15s; z-index: 5; }} .pg:hover .pgtools {{ opacity: 1; }}
  .pgtools button {{ font: inherit; font-size: 11px; border: 1px solid var(--line); background: #fff; border-radius: 999px; padding: 4px 10px; cursor: pointer; }}
  .pgtools .on {{ background: #FFF5C2; border-color: #e3c84a; }}
  #pick {{ position: fixed; inset: 0; z-index: 50; background: rgba(20,20,20,.5); display: grid; place-items: center; }} #pick[hidden] {{ display: none; }}
  #pick .box {{ width: min(960px, calc(100vw - 40px)); max-height: calc(100vh - 60px); background: #fff; display: flex; flex-direction: column; }}
  #pick .head {{ display: flex; gap: 10px; align-items: center; padding: 12px 16px; border-bottom: 1px solid var(--line); }} #pick .head h3 {{ font-size: 1.1rem; margin-right: auto; }}
  #pick .grid {{ overflow: auto; padding: 12px 16px; display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 8px; }}
  #pick .grid img {{ width: 100%; aspect-ratio: 1; object-fit: cover; cursor: pointer; display: block; }} #pick .grid img:hover {{ outline: 3px solid #2459c9; }}
  #pick .grid figure {{ margin: 0; }} #pick .grid figcaption {{ font-size: 10px; color: var(--ink3); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  @media print {{ .pgtools, #pick {{ display: none !important; }} .doc img {{ outline: none !important; }} }}
  @media (max-width: 1100px) {{ .app {{ grid-template-columns: 1fr; }} .panel {{ position: static; height: auto; border-right: 0; border-bottom: 1px solid var(--line); }} .doc {{ padding: 12px; overflow: auto; }} }}
  @media print {{
    @page {{ size: A4 portrait; margin: 0; }}
    .pg.edit {{ outline: none; }}
    html, body {{ background: #fff; }} .panel {{ display: none; }} .app {{ display: block; }} .doc {{ padding: 0; gap: 0; display: block; }}
    .pg {{ box-shadow: none; width: 210mm; height: 297mm; min-height: 0; overflow: hidden; }}
    .pg, .cover .band, .photos figure::after, th, tr.tot td {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  }}
</style>
<div class="app">
<aside class="panel">
  <h1>Комерційна пропозиція</h1>
  <p class="hint">Службова сторінка для менеджерів. Заповніть поля — документ праворуч оновлюється одразу. Будь-який текст у документі можна правити просто на сторінці, картинку — замінити клацанням (своя або з бібліотеки); правки зберігаються з документом. «Друк / PDF» збереже A4; «Посилання» скопіює адресу з усіма даними, щоб переслати колезі.</p>
  <div class="f"><label>Компанія-клієнт</label><input id="client" placeholder="DIAME"></div>
  <div class="two"><div class="f"><label>Контактна особа</label><input id="contact" placeholder="Ім’я, посада"></div><div class="f"><label>Менеджер Obiimy</label><input id="manager" placeholder="Ім’я, телефон"></div></div>
  <div class="two"><div class="f"><label>Дата</label><input id="date" type="date"></div><div class="f"><label>Дійсна до</label><input id="valid" type="date"></div></div>
  <div class="f"><label>Заголовок</label><input id="title" value="Пропозиція корпоративного замовлення"></div>
  <div class="f"><label>Підзаголовок (що й скільки)</label><input id="sub" placeholder="Шовковий твіллі 84 × 5, 100 штук"></div>

  <div class="sec"><h2>Позиції</h2><div id="rows"></div><button type="button" class="btn line sm" id="addrow">+ Додати позицію</button></div>

  <div class="sec"><h2>Пакування й персоналізація</h2>
    <p class="hint">Перші два пункти безкоштовні в кожному корпоративному замовленні. Для решти впишіть вартість або «у розрахунку»; порожнє — не показується.</p>
    <div id="extras"></div>
  </div>

  <div class="sec"><h2>Умови</h2>
    <div class="f"><label>Строки виготовлення й відправки</label><textarea id="terms" placeholder="Напр.: 11 робочих днів від передоплати; авторський дизайн — 3 тижні"></textarea></div>
    <div class="f"><label>Оплата</label><textarea id="pay" placeholder="Напр.: безготівковий рахунок, 50% передоплата"></textarea></div>
    <div class="f"><label>Примітка</label><textarea id="note" placeholder="Що ще важливо для клієнта"></textarea></div>
  </div>
  <div class="acts"><button type="button" class="btn gold" id="print">Друк / PDF</button><button type="button" class="btn line" id="share">Посилання</button><button type="button" class="btn line" id="reset">Очистити</button><span class="ok" id="ok"></span></div>
</aside>
<main class="doc" id="doc"></main>
<div id="pick" hidden><div class="box"><div class="head"><h3>Замінити картинку</h3><input id="pickfile" type="file" accept="image/*" hidden><button type="button" class="btn line sm" onclick="document.getElementById('pickfile').click()">Завантажити свою…</button><button type="button" class="btn line sm" data-pickclose>Закрити</button></div><div class="grid"></div></div></div>
</div>
<script>
var ITEMS = {json.dumps(ITEMS, ensure_ascii=False)};
var EXTRAS = {json.dumps(EXTRAS, ensure_ascii=False)};
var MOSAIC = {json.dumps(MOSAIC)}, MOSAIC_POS = {json.dumps(MOSAIC_POS)}, LIFE = {json.dumps(LIFE)}, LIFE_POS = {json.dumps(LIFE_POS)};
var LIBRARY = {json.dumps(LIBRARY, ensure_ascii=False)};
var DEF = {json.dumps(DEFAULT, ensure_ascii=False)};
var BY = {{}}; ITEMS.forEach(function (i) {{ BY[i.k] = i; }});
var PHONE = {json.dumps(b2b.PHONE)}, MAIL = {json.dumps(b2b.MAIL)}, SHOWROOM = {json.dumps(b2b.SHOWROOM)};
var S = load();
function load() {{
  try {{ var h = location.hash.slice(1); if (h) return Object.assign(JSON.parse(JSON.stringify(DEF)), JSON.parse(decodeURIComponent(escape(atob(h))))); }} catch (e) {{}}
  try {{ var l = localStorage.getItem('kp'); if (l) return Object.assign(JSON.parse(JSON.stringify(DEF)), JSON.parse(l)); }} catch (e) {{}}
  return JSON.parse(JSON.stringify(DEF));
}}
function save() {{ try {{ localStorage.setItem('kp', JSON.stringify(S)); }} catch (e) {{}} }}
function money(n) {{ return Math.round(n).toLocaleString('uk-UA').replace(/,/g, ' ') + ' грн'; }}
function esc(s) {{ return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {{ return {{'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}}[c]; }}); }}
function nl(s) {{ return esc(s).replace(/\\n/g, '<br>'); }}
function fmtDate(d) {{ if (!d) return ''; var p = d.split('-'); return p.length === 3 ? p[2] + '.' + p[1] + '.' + p[0] : d; }}
function rowPrice(r) {{ var it = BY[r.k] || BY.custom; var base = (r.price != null && r.price !== '') ? Number(r.price) : it.p; return base; }}
function rowName(r) {{ var it = BY[r.k] || BY.custom; return r.k === 'custom' ? (r.name || 'Інша позиція') : it.n; }}
var DESIGN = {{ asst: 'Дизайн із наявного асортименту', author: 'Розробка авторського дизайну' }};

function renderForm() {{
  ['client', 'contact', 'manager', 'date', 'valid', 'title', 'sub', 'terms', 'pay', 'note'].forEach(function (id) {{ document.getElementById(id).value = S[id] || ''; }});
  var rows = document.getElementById('rows'); rows.innerHTML = '';
  S.rows.forEach(function (r, i) {{
    var d = document.createElement('div'); d.className = 'row';
    d.innerHTML = '<div class="g2"><select data-i="' + i + '" data-f="k">' + ITEMS.map(function (it) {{ return '<option value="' + it.k + '"' + (it.k === r.k ? ' selected' : '') + '>' + esc(it.n) + (it.p ? ' — ' + money(it.p) : '') + '</option>'; }}).join('') + '</select><button type="button" class="btn line sm" data-del="' + i + '">×</button></div>'
      + (r.k === 'custom' ? '<input data-i="' + i + '" data-f="name" placeholder="Назва позиції" value="' + esc(r.name || '') + '">' : '')
      + '<div class="g"><div class="f"><label>Кількість</label><input type="number" min="1" data-i="' + i + '" data-f="q" value="' + esc(r.q) + '"></div>'
      + '<div class="f"><label>Знижка, %</label><input type="number" min="0" max="100" data-i="' + i + '" data-f="disc" value="' + esc(r.disc || 0) + '"></div>'
      + '<div class="f"><label>Ціна за шт.</label><input type="number" min="0" data-i="' + i + '" data-f="price" placeholder="' + (BY[r.k] ? BY[r.k].p : '') + '" value="' + (r.price != null && r.price !== '' ? esc(r.price) : '') + '"></div></div>'
      + '<div class="f"><label>Дизайн</label><select data-i="' + i + '" data-f="d"><option value="asst"' + (r.d !== 'author' ? ' selected' : '') + '>Із наявного асортименту</option><option value="author"' + (r.d === 'author' ? ' selected' : '') + '>Авторський дизайн для клієнта</option></select></div>'
      + '<small>Роздрібна ціна obiimy.world — ' + (BY[r.k] && BY[r.k].p ? money(BY[r.k].p) : 'вписати') + '. Порожнє поле ціни = роздрібна.</small>';
    rows.appendChild(d);
  }});
  var ex = document.getElementById('extras'); ex.innerHTML = '';
  EXTRAS.forEach(function (e) {{
    var v = S.ex[e[0]]; if (v == null) v = e[2];
    var d = document.createElement('div'); d.className = 'ex';
    d.innerHTML = '<span>' + esc(e[1]) + '</span><input data-ex="' + e[0] + '" value="' + esc(v) + '" placeholder="вартість">';
    ex.appendChild(d);
  }});
}}

function renderDoc() {{
  var logo = '<img class="logo" src="brand/logo-ink.png" alt="Obiimy">';
  var foot = '<div class="foot"><span>Obiimy · шоурум: ' + esc(SHOWROOM) + '</span><span>' + esc(PHONE) + ' · ' + esc(MAIL) + ' · obiimy.world</span></div>';
  var pages = [];
  var mos = function (from) {{ var o = ''; for (var i = from; i < from + 4; i++) o += '<img src="' + MOSAIC[i] + '" style="object-position:' + MOSAIC_POS[i] + '" alt="">'; return '<div class="mos">' + o + '</div>'; }};
  pages.push('<section class="pg cover" data-key="cover">' + mos(0) + '<div class="band"><div><img src="brand/logo-ink.png" alt="Obiimy"><h1>' + esc(S.title) + (S.client ? '<br><i>для ' + esc(S.client) + '</i>' : '') + '</h1>'
    + '<p class="for">Преміальні шовкові вироби' + (S.sub ? ' · ' + esc(S.sub) : '') + '</p></div>'
    + '<div class="meta">' + (S.date ? 'Дата: ' + fmtDate(S.date) + '<br>' : '') + (S.valid ? 'Дійсна до ' + fmtDate(S.valid) + '<br>' : '') + (S.contact ? 'Для: ' + esc(S.contact) : '') + '</div></div>' + mos(4) + '</section>');
  // photos of the chosen items (unique)
  var seen = {{}}, figs = [];
  S.rows.forEach(function (r) {{ var it = BY[r.k] || BY.custom, ph = LIFE[r.k] || it.ph, life = !!LIFE[r.k]; if (seen[ph]) return; seen[ph] = 1; figs.push('<figure class="' + (life ? '' : 'flat') + '"><img src="' + ph + '" style="object-position:' + (LIFE_POS[r.k] || '50% 50%') + '" alt=""><figcaption>' + esc(rowName(r)) + (BY[r.k] && BY[r.k].p ? '<span>від ' + money(BY[r.k].p) + '</span>' : '') + '</figcaption></figure>'); }});
  if (figs.length) pages.push('<section class="pg" data-key="photos">' + logo + '<p class="eb" style="margin-top:10mm">Що пропонуємо</p><h2 class="t">' + esc(S.sub || 'Речі з каталогу Obiimy') + '</h2><div class="photos">' + figs.slice(0, 4).join('') + '</div><p class="fine">Фото — приклад принта; принти обираються з добірки. 100% натуральний шовк, авторські принти, виготовлено в Україні. Пакування й наліпка з вашим логотипом — у ціні.</p>' + foot + '</section>');
  // table
  var tr = '', total = 0, totalFull = 0, qty = 0, hasDisc = false;
  S.rows.forEach(function (r) {{ var q = Number(r.q) || 0, p = rowPrice(r), d = Number(r.disc) || 0, pd = p * (1 - d / 100); if (d) hasDisc = true; total += pd * q; totalFull += p * q; qty += q;
    tr += '<tr><td>' + esc(rowName(r)) + '<br><small style="color:var(--ink3)">' + DESIGN[r.d === 'author' ? 'author' : 'asst'] + '</small></td><td class="num">' + q + '</td><td class="num">' + money(p) + '</td><td class="num">' + (d ? d + '%' : '—') + '</td><td class="num">' + money(pd) + '</td><td class="num">' + money(pd * q) + '</td></tr>'; }});
  var exr = '';
  EXTRAS.forEach(function (e) {{ var v = S.ex[e[0]]; if (v == null) v = e[2]; v = String(v).trim(); if (!v) return; var n = Number(v.replace(/\\s/g, '')); exr += '<tr><td colspan="5">' + esc(e[1]) + '</td><td class="num">' + (isNaN(n) ? esc(v) : (n ? money(n) : 'безкоштовно')) + '</td></tr>'; if (!isNaN(n)) total += n; }});
  var sum = '<tr class="tot"><td colspan="5">Разом за позиції' + (hasDisc ? ' з корпоративною знижкою' : '') + ' (' + qty + ' шт.)</td><td class="num">' + money(total) + '</td></tr>'
    + (hasDisc && totalFull > total ? '<tr><td colspan="5">Загальна сума знижки</td><td class="num">' + money(totalFull - (total - extrasSum())) + '</td></tr>' : '')
    + '<tr class="sum"><td colspan="5">До сплати</td><td class="num">' + money(total) + '</td></tr>';
  function extrasSum() {{ var s = 0; EXTRAS.forEach(function (e) {{ var v = S.ex[e[0]]; if (v == null) v = e[2]; var n = Number(String(v).replace(/\\s/g, '')); if (!isNaN(n)) s += n; }}); return s; }}
  var kv = '';
  if (S.terms) kv += '<div><span>Строки</span><span>' + nl(S.terms) + '</span></div>';
  if (S.pay) kv += '<div><span>Оплата</span><span>' + nl(S.pay) + '</span></div>';
  if (S.note) kv += '<div><span>Примітка</span><span>' + nl(S.note) + '</span></div>';
  pages.push('<section class="pg" data-key="table">' + logo + '<p class="eb" style="margin-top:10mm">Розрахунок</p><h2 class="t">' + esc(S.title) + '</h2><table><thead><tr><th>Виріб</th><th class="num">К-сть</th><th class="num">Ціна, грн</th><th class="num">Знижка</th><th class="num">Ціна зі знижкою</th><th class="num">Сума, грн</th></tr></thead><tbody>' + tr + exr + sum + '</tbody></table>'
    + '<div class="kv">' + kv + '</div><p class="fine">Ціни в колонці «Ціна» — роздрібні, obiimy.world. Пропозиція не є публічною офертою.</p>' + foot + '</section>');
  // packaging, personalisation, why
  pages.push('<section class="pg" data-key="terms">' + logo + '<p class="eb" style="margin-top:10mm">Пакування й персоналізація</p><h2 class="t">Що входить у корпоративне замовлення</h2>'
    + '<div class="kv"><div><span>Подарункове пакування</span><span>Кожна річ — у подарунковому пакуванні Obiimy. Безкоштовно.</span></div><div><span>Наліпка з логотипом</span><span>Наліпка з логотипом вашої компанії всередині коробки. Безкоштовно.</span></div><div><span>Бирка з логотипом</span><span>Нашивна бирка з логотипом компанії на самій хустці чи твіллі — строки й вартість у розрахунку.</span></div><div><span>Друковані матеріали</span><span>Листівка з привітанням — з вашим логотипом і вашим текстом.</span></div><div><span>Індивідуальний принт</span><span>Принт, створений для вашої компанії: кольори бренду, символи, історія. Тираж і строки — у розрахунку.</span></div></div>'
    + '<div class="why3"><div><b>Унікальні принти</b>Авторські малюнки засновниці Світлани Сніжко та сучасних українських художниць.</div><div><b>Якість, яку відчувають</b>Лише 100% натуральний італійський шовк; кутики кожної хустки обробляють вручну. Повністю українське виробництво.</div><div><b>Бренд, який упізнають</b>INTERTOP і Hram в Україні, Be Brave у Канаді, UFD London; LIGA.net та INSIDER UA.</div></div>'
    + '<p class="contact"><b>Контакти</b><br>' + (S.manager ? esc(S.manager) + '<br>' : '') + esc(PHONE) + ' · Telegram @OBIIMY_sales<br>' + esc(MAIL) + ' · obiimy.world<br>Шоурум: ' + esc(SHOWROOM) + '</p>' + foot + '</section>');
  document.getElementById('doc').innerHTML = pages.join('');
  document.querySelectorAll('#doc .pg').forEach(function (pg) {{
    var key = pg.dataset.key, edited = S.html && S.html[key];
    if (edited) {{ pg.innerHTML = edited; pg.classList.add('edit'); }}
    pg.setAttribute('contenteditable', 'true'); pg.setAttribute('spellcheck', 'false');
    var tools = document.createElement('div'); tools.className = 'pgtools'; tools.setAttribute('contenteditable', 'false');
    tools.innerHTML = (edited ? '<button type="button" class="on" data-pgreset="' + key + '" title="Повернути сторінку до вигляду з форми">Правлено вручну · скинути</button>' : '<span class="hint" style="font-size:11px;color:#999">текст — правити тут, картинка — клацнути</span>');
    pg.appendChild(tools);
  }});
}}
// ---------- in-place editing: text and pictures ----------
var editTimer = null;
function pageSnapshot(pg) {{ var c = pg.cloneNode(true); c.querySelectorAll('.pgtools').forEach(function (t) {{ t.remove(); }}); return c.innerHTML; }}
document.getElementById('doc').addEventListener('input', function (e) {{
  var pg = e.target.closest('.pg'); if (!pg || e.target.closest('.pgtools')) return;
  clearTimeout(editTimer); editTimer = setTimeout(function () {{ S.html = S.html || {{}}; S.html[pg.dataset.key] = pageSnapshot(pg); pg.classList.add('edit'); save();
    var t = pg.querySelector('.pgtools'); if (t && !t.querySelector('[data-pgreset]')) t.innerHTML = '<button type="button" class="on" data-pgreset="' + pg.dataset.key + '" title="Повернути сторінку до вигляду з форми">Правлено вручну · скинути</button>'; }}, 400);
}});
document.getElementById('doc').addEventListener('paste', function (e) {{ if (!e.target.closest('.pg')) return; e.preventDefault(); document.execCommand('insertText', false, (e.clipboardData || window.clipboardData).getData('text/plain')); }});
document.getElementById('doc').addEventListener('click', function (e) {{
  var b = e.target.closest('[data-pgreset]');
  if (b) {{ if (!confirm('Скинути ручні правки цієї сторінки?')) return; delete S.html[b.dataset.pgreset]; save(); renderDoc(); return; }}
  var im = e.target.closest('img'); if (im && !e.target.closest('.pgtools')) {{ e.preventDefault(); pickOpen(im); }}
}});
var PICK = null;
function pickOpen(img) {{
  PICK = img; var box = document.getElementById('pick'); box.hidden = false;
  var grid = box.querySelector('.grid'); grid.innerHTML = LIBRARY.map(function (f, i) {{ return '<figure><img src="' + f.t + '" data-i="' + i + '" alt="" loading="lazy"><figcaption>' + esc(f.g + ' · ' + f.n) + '</figcaption></figure>'; }}).join('');
}}
function pickSet(src) {{ if (!PICK) return; PICK.src = src; PICK.removeAttribute('srcset'); var pg = PICK.closest('.pg'); document.getElementById('pick').hidden = true; S.html = S.html || {{}}; S.html[pg.dataset.key] = pageSnapshot(pg); save(); renderDoc(); PICK = null; }}
document.getElementById('pick').addEventListener('click', function (e) {{
  if (e.target.id === 'pick' || e.target.closest('[data-pickclose]')) {{ document.getElementById('pick').hidden = true; PICK = null; return; }}
  var im = e.target.closest('.grid img'); if (im) pickSet(LIBRARY[Number(im.dataset.i)].f);
}});
document.getElementById('pickfile').addEventListener('change', function (e) {{
  var f = e.target.files && e.target.files[0]; e.target.value = ''; if (!f) return;
  if (f.size > 4 * 1048576) {{ alert('Файл більший за 4 МБ — зменшіть його перед завантаженням.'); return; }}
  var r = new FileReader(); r.onload = function () {{ pickSet(r.result); }}; r.readAsDataURL(f);
}});

function onInput(e) {{
  var t = e.target, i = t.dataset.i, f = t.dataset.f;
  if (t.dataset.ex) {{ S.ex[t.dataset.ex] = t.value; }}
  else if (i != null) {{ S.rows[i][f] = t.value; if (f === 'k') {{ S.rows[i].price = null; renderForm(); }} }}
  else if (t.id) S[t.id] = t.value;
  save(); renderDoc();
}}
document.addEventListener('input', onInput);
document.addEventListener('change', function (e) {{ if (e.target.tagName === 'SELECT') onInput(e); }});
document.addEventListener('click', function (e) {{ var b = e.target.closest('[data-del]'); if (b) {{ S.rows.splice(Number(b.dataset.del), 1); if (!S.rows.length) S.rows.push(JSON.parse(JSON.stringify(DEF.rows[0]))); save(); renderForm(); renderDoc(); }} }});
document.getElementById('addrow').addEventListener('click', function () {{ S.rows.push(JSON.parse(JSON.stringify(DEF.rows[0]))); save(); renderForm(); renderDoc(); }});
document.getElementById('print').addEventListener('click', function () {{ var t = document.title; document.title = 'Obiimy — пропозиція' + (S.client ? ' для ' + S.client : ''); window.print(); document.title = t; }});
document.getElementById('share').addEventListener('click', function () {{ var h = btoa(unescape(encodeURIComponent(JSON.stringify(S)))); location.hash = h; var ok = document.getElementById('ok'); (navigator.clipboard ? navigator.clipboard.writeText(location.href) : Promise.reject()).then(function () {{ ok.textContent = 'Посилання скопійовано'; }}, function () {{ ok.textContent = 'Скопіюйте адресу з рядка браузера'; }}); setTimeout(function () {{ ok.textContent = ''; }}, 4000); }});
document.getElementById('reset').addEventListener('click', function () {{ if (!confirm('Очистити всі поля й ручні правки сторінок?')) return; S = JSON.parse(JSON.stringify(DEF)); location.hash = ''; save(); renderForm(); renderDoc(); }});
renderForm(); renderDoc();
</script>
'''
(OUT / "kp.html").write_text(typo(HTML))
print("kp", len(HTML) // 1024, "KB")
