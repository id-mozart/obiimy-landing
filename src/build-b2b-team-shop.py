#!/usr/bin/env python3
"""Three down-to-earth B2B pages for gifts inside a company: the goods, the prices and the reasons on the first screen.
  b2b-team-catalog  a catalogue with prices and a budget filter, a request list instead of a cart
  b2b-team-budget   three shelves by budget: up to 1 000, 2 500, 5 000 грн per person
  b2b-team-offer    a one-screen commercial proposal: table of positions + reasons + form
Data, prices and helpers come from build-b2b-team.py (retail prices from obiimy.world, review/SITE-FACTS.md).
Nothing here promises a discount, a deadline or a minimum order."""
import importlib.util, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("team", ROOT / "build-b2b-team.py")
team = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(team)
b2b, img, price, typo, J = team.b2b, team.img, team.price, team.typo, team.J
CATALOG, CAT, FEATURED, SHORT_N = team.CATALOG, team.CAT, team.FEATURED, team.SHORT_N
PHONE, PHONE_HREF, MAIL, SAMPLE, BAR = team.PHONE, team.PHONE_HREF, team.MAIL, team.SAMPLE, team.BAR

# «for whom» in one or two words — our recommendation, shown on the cards
FOR = {"scr": "Знак уваги", "book": "Усім · знак уваги", "cert1": "Усім · на вибір", "cert15": "Усім · на вибір", "tw": "Універсальний подарунок", "scrset": "Набір у коробці",
       "cert2": "Усім · на вибір", "twscr": "Набір у коробці", "h44": "Ключовим людям", "mask": "Усім · відпочинок", "maskscr": "Набір у коробці", "tw44": "Ключовим людям",
       "h65": "Ключовим людям", "song": "Набір із сенсом", "cert4": "Усім · на вибір", "pil": "Усім · для дому", "h88": "Керівникам", "three": "Керівникам"}
SHORT = {"scr": "Шовкова резинка", "book": "Закладка для книги", "cert1": "Сертифікат 1 000 грн", "cert15": "Сертифікат 1 500 грн", "tw": "Твіллі 84 × 5",
         "scrset": "Три резинки", "cert2": "Сертифікат 2 000 грн", "twscr": "Твіллі та резинка", "h44": "Хустка 44 × 44", "mask": "Маска для сну",
         "maskscr": "Маска та резинка", "tw44": "Твіллі та хустка 44 × 44", "h65": "Хустка 65 × 65", "song": "Маска, закладка й резинка", "cert4": "Сертифікат 4 000 грн",
         "pil": "Наволочка 50 × 70", "h88": "Хустка 88 × 88", "three": "Три твіллі"}
WHY = [  # the reasons, only facts from SITE-FACTS
    ("100% італійський шовк", "Виготовлено в Україні, ручна обробка краю."),
    ("Авторські принти", "Художниця й засновниця — Світлана Сніжко."),
    ("Набори — у святковій коробці", "Пакування окремих речей покажемо на фото в добірці."),
    ("Привітання вашими словами", "Підпис до подарунка за вашим текстом."),
    ("Кожному або в офіс", "Новою поштою по Україні та за кордон, як домовимось."),
    ("Є речі для всіх", "Маска для сну, закладка, наволочка, сертифікат — і тим, хто аксесуари не носить."),
]
SHELVES = [
    ("1000", "До 1 000 грн", "Знак уваги кожному", ["scr", "book", "cert1"]),
    ("2500", "До 2 500 грн", "Подарунок, який носять", ["tw", "twscr", "h44", "scrset", "cert15", "cert2"]),
    ("5000", "До 5 000 грн", "Керівникам — і речі для всіх", ["h65", "tw44", "song", "three", "h88", "maskscr", "mask", "pil", "cert4"]),
]
OFFER = ["tw", "twscr", "mask", "h44", "scr", "book", "cert2", "h65"]

CSS = """
  .why { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
  .why div { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 18px 20px; display: grid; gap: 4px; }
  .why b { font-family: var(--display); font-weight: 400; font-size: 1.2rem; line-height: 1.15; }
  .why span { color: var(--ink2); font-size: .9rem; }
  .why.tight { gap: 10px; } .why.tight div { padding: 12px 14px; } .why.tight b { font-size: 1.05rem; } .why.tight span { font-size: .84rem; }
  .filters { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 22px; margin-bottom: 22px; }
  .filters .cnt { color: var(--ink2); font-size: .88rem; margin-left: auto; }
  .items { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }
  .nom { min-height: 40px; padding: 6px 26px 6px 10px; font-size: 16px; font-weight: 600; max-width: 124px; }
  .item { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; display: flex; flex-direction: column; }
  .item > img { width: 100%; object-fit: cover; background: #fff; }
  .dark .item > img { background: #F1EEE8; }
  .item .in { padding: 14px 16px 16px; display: grid; gap: 6px; flex: 1; align-content: start; }
  .item .for { font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: var(--ink3); font-weight: 600; }
  .item h3 { font-size: 1.12rem; }
  .item .why { display: block; color: var(--ink2); font-size: .86rem; }
  .item .pr { padding-top: 4px; display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap; }
  .item > img { aspect-ratio: 5 / 4; }
  .item .pr b { font-family: var(--display); font-weight: 400; font-size: 1.35rem; white-space: nowrap; }
  .item .pr small { color: var(--ink2); font-size: .78rem; }
  .add { font: inherit; font-weight: 600; font-size: .82rem; min-height: 40px; padding: 8px 14px; border-radius: 999px; border: 1px solid var(--ink); background: transparent; color: var(--ink); cursor: pointer; white-space: nowrap; }
  .add.on { background: var(--ink); color: var(--bg); }
  .item[hidden] { display: none; }
  .qtyc { display: inline-flex; align-items: center; border: 1px solid var(--ink); border-radius: 999px; overflow: hidden; }
  .qtyc button { font: inherit; font-weight: 600; width: 40px; min-height: 40px; border: 0; background: transparent; color: var(--ink); cursor: pointer; }
  .qtyc input { width: 60px; min-height: 40px; border: 0; border-inline: 1px solid var(--ink); text-align: center; font: inherit; font-size: 16px; font-weight: 600; background: transparent; color: var(--ink); padding: 0; border-radius: 0; }
  .qtyc input:focus-visible { outline-offset: -2px; }
  .listbox { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: clamp(18px, 2.4vw, 28px); display: grid; gap: 14px; }
  .listbox .row { display: grid; grid-template-columns: minmax(0, 1fr) auto auto auto; gap: 12px; align-items: center; padding: 10px 0; border-top: 1px solid var(--line); font-size: .95rem; }
  .listbox .row:first-of-type { border-top: 0; }
  .listbox .row .s { font-variant-numeric: tabular-nums; white-space: nowrap; min-width: 6.5em; text-align: right; }
  .listbox .row .x { font: inherit; background: none; border: 0; color: var(--ink2); cursor: pointer; padding: 8px; min-height: 44px; min-width: 44px; }
  .qtyc { justify-self: start; }
  .listbox .empty { color: var(--ink2); font-size: .95rem; }
  .listbox.is-empty { padding-block: 18px; gap: 8px; } .listbox.is-empty h2 { font-size: 1.2rem !important; } .listbox.is-empty > div:first-child p { display: none; }
  .listbox .tot { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: end; gap: 10px 24px; padding-top: 12px; border-top: 1px solid var(--ink); }
  .listbox .tot b { font-family: var(--display); font-weight: 400; font-size: clamp(1.8rem, 3.4vw, 2.6rem); line-height: 1; }
  .listbox .tot span { color: var(--ink2); font-size: .88rem; }
  .people { display: inline-grid; gap: 6px; font-weight: 600; font-size: .92rem; } .people input { max-width: 140px; }
  .acts { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
  .acts [aria-disabled="true"] { opacity: .5; pointer-events: none; }
  .two { display: grid; grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); gap: clamp(24px, 4vw, 56px); align-items: start; }
  .two .side { position: sticky; top: 92px; display: grid; gap: 16px; }
  .shelf { padding-block: clamp(28px, 4vw, 52px); border-top: 1px solid var(--line); }
  .hero .strip { grid-template-columns: 1fr 1fr; align-self: center; }
  .hero.h1-xs .lead { margin-top: 12px; font-size: 1.05rem; }
  .shelf .top { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 22px; margin-bottom: 18px; }
  .shelf .top h2 { font-size: clamp(1.6rem, 2.6vw, 2.2rem); }
  .shelf .top .sub { color: var(--ink2); }
  .shelf .top .ex { margin-left: auto; color: var(--ink2); font-size: .9rem; }
  .rows { display: grid; gap: 0; border-top: 1px solid var(--line); }
  .rowi { display: grid; grid-template-columns: 88px minmax(0, 1.4fr) minmax(0, 1.6fr) auto auto; gap: 16px; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--line); }
  .rowi img { width: 88px; height: 88px; object-fit: cover; border-radius: calc(var(--radius) - 2px); background: #fff; }
  .rowi .n { font-family: var(--display); font-size: 1.15rem; line-height: 1.15; }
  .rowi .n small { display: block; font-family: var(--body); font-size: .74rem; letter-spacing: .1em; text-transform: uppercase; color: var(--ink3); font-weight: 600; margin-top: 2px; }
  .rowi .w { color: var(--ink2); font-size: .88rem; }
  .rowi .p { font-family: var(--display); font-size: 1.25rem; white-space: nowrap; }
  .strip { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
  .strip img { width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: var(--radius); background: #fff; }
  .offer table { width: 100%; border-collapse: collapse; font-size: .95rem; }
  .offer th { text-align: left; font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; color: var(--ink3); font-weight: 600; padding: 8px 10px 10px 0; border-bottom: 1px solid var(--ink); }
  .offer td { padding: 10px 10px 10px 0; border-bottom: 1px solid var(--line); vertical-align: middle; }
  .offer td.n { font-family: var(--display); font-size: 1.1rem; }
  .offer td.n small { display: block; font-family: var(--body); font-size: .8rem; color: var(--ink2); }
  .offer td.p { font-family: var(--display); font-size: 1.15rem; white-space: nowrap; text-align: right; }
  .offer td.a { text-align: right; width: 1%; }
  .offer td img { width: 64px; height: 64px; object-fit: cover; border-radius: calc(var(--radius) - 2px); background: #fff; }
  .side .card { display: grid; gap: 12px; }
  .side ul { margin: 0; padding: 0; list-style: none; display: grid; gap: 8px; font-size: .92rem; color: var(--ink2); }
  .side li { display: grid; grid-template-columns: 18px 1fr; gap: 8px; } .side li::before { content: "✓"; color: var(--gold); font-weight: 700; }
  .h1-xs h1 { font-size: clamp(1.9rem, 3.4vw, 3rem); }
  .hero.one .wrap { grid-template-columns: 1fr; }
  .hero.one .lead { max-width: 44em; }
  .hero.one { padding-bottom: clamp(16px, 3vw, 36px); }
  @media (max-width: 640px) { .hero.one .lead { display: none; } .hero.one .cta { margin-top: 12px; } .hero .cta .btn-sm { width: auto; flex: 0 0 auto; } .hero.h1-xs h1 { font-size: clamp(1.6rem, 6.8vw, 2rem); } .hero.h1-xs { padding-bottom: 14px; }
    .hero .cta.row { flex-direction: row; flex-wrap: wrap; gap: 8px; } .hero .cta.row .btn-line { border: 1px solid var(--ink); padding: 8px 14px; text-decoration: none; min-height: 40px; } .hero .cta.row .btn-gold { width: auto; } }
  @media (max-width: 1280px) { .items { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
  @media (max-width: 960px) {
    .why { grid-template-columns: 1fr 1fr; } .items { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .two { grid-template-columns: 1fr; } .two .side { position: static; }
    .rowi { grid-template-columns: 64px minmax(0, 1fr) auto; gap: 10px 12px; } .rowi img { width: 64px; height: 64px; grid-column: 1; grid-row: 1 / span 2; } .rowi .w { display: none; }
    .rowi .n { grid-column: 2; grid-row: 1 / span 2; } .rowi .p { grid-column: 3; grid-row: 1; } .rowi .add { grid-column: 3; grid-row: 2; justify-self: end; }
    .strip { grid-template-columns: repeat(4, 1fr); }
  }
  @media (max-width: 640px) {
    .why { grid-template-columns: 1fr; } .items { grid-template-columns: 1fr 1fr; gap: 10px; }
    .item .in { padding: 10px 12px 12px; } .item h3 { font-size: 1rem; } .item .why { display: none; }
    .item .pr { flex-wrap: wrap; } .item .pr b { font-size: 1.15rem; }
    .filters { gap: 8px 14px; margin-bottom: 14px; } .filters .cnt { display: none; }
    .filters .chips { flex-wrap: nowrap; overflow-x: auto; max-width: 100%; padding-bottom: 4px; scrollbar-width: none; } .filters .chips span { white-space: nowrap; min-height: 40px; padding: 8px 14px; } .filters .chips label { flex: none; }
    .hero.h1-xs .lead { display: none; }
    .listbox .row { grid-template-columns: minmax(0, 1fr) auto; } .listbox .row .s { grid-column: 1; text-align: left; } .listbox .row .qtyc { grid-column: 1; } .listbox .row .x { grid-column: 2; grid-row: 1 / span 3; }
    .offer table, .offer tbody, .offer tr, .offer td { display: block; } .offer thead { display: none; }
    .offer tr { border-bottom: 1px solid var(--line); padding: 10px 0; display: grid; grid-template-columns: 64px minmax(0, 1fr) auto; gap: 6px 12px; align-items: center; }
    .offer td { border: 0; padding: 0; } .offer td.n { grid-column: 2; } .offer td.p { grid-column: 3; } .offer td.a { grid-column: 2 / -1; text-align: left; width: auto; }
    .strip { grid-template-columns: 1fr 1fr; } .hero .strip { display: none; }
  }
"""

def chips(name, options, checked):
    return '<div class="chips">' + "".join(f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{t}</span></label>' for v, t in options) + "</div>"

def lc(t): return t if t.startswith("Новою") else t[0].lower() + t[1:]
def why_html(cls="", items=None):
    return f'<div class="why {cls}">' + "".join(f"<div><b>{b}</b><span>{s}</span></div>" for b, s in (items or WHY)) + "</div>"

CERTS = ["cert1", "cert15", "cert2", "cert4"]
def add_btn(k):
    return f'<button type="button" class="add" data-add="{k}" aria-label="До списку: {CAT[k]["n"]}">+ До списку</button>'

def nom_select(keys, idn):
    """One certificate card for several nominals: the select picks the real catalogue key."""
    return (f'<select class="nom" id="{idn}" aria-label="Номінал сертифіката">' + "".join(f'<option value="{k}">{price(CAT[k]["p"])}</option>' for k in keys) + '</select>')

def cert_card(keys, idn):
    c = CAT[keys[0]]
    return (f'<div class="item" data-k="cert" data-p="{c["p"]}" data-pmax="{CAT[keys[-1]]["p"]}" data-all="1">{img(c["ph"], "Подарунковий сертифікат Obiimy", sizes="(max-width: 640px) 50vw, (max-width: 960px) 33vw, 25vw")}'
            f'<div class="in"><p class="for">Усім · на вибір</p><h3>Сертифікат</h3>'
            f'<div class="pr">{nom_select(keys, idn)}<button type="button" class="add" data-add="{keys[0]}" data-nom="{idn}" aria-label="До списку: сертифікат">+ До списку</button></div><span class="why">Людина обирає сама протягом трьох місяців. Буває електронний і друкований.</span></div></div>')

def cert_row(keys, idn):
    c = CAT[keys[0]]
    return (f'<div class="rowi" data-k="cert">{img(c["ph"], "", sizes="88px")}<p class="n">Сертифікат<small>Усім · на вибір</small></p><p class="w">Людина обирає сама протягом трьох місяців. Буває електронний і друкований.</p>'
            f'<p class="p">{nom_select(keys, idn)}</p><button type="button" class="add" data-add="{keys[0]}" data-nom="{idn}" aria-label="До списку: сертифікат">+ До списку</button></div>')

def item_card(c):
    return (f'<div class="item" data-k="{c["k"]}" data-p="{c["p"]}" data-all="{1 if c["neutral"] else 0}">{img(c["ph"], c["n"], sizes="(max-width: 640px) 50vw, (max-width: 960px) 33vw, 25vw")}'
            f'<div class="in"><p class="for">{FOR[c["k"]]}</p><h3>{SHORT[c["k"]]}</h3>'
            f'<div class="pr"><b class="num">{price(c["p"])}</b>{add_btn(c["k"])}</div><span class="why">{c["why"]}</span></div></div>')

def item_row(c):
    return (f'<div class="rowi" data-k="{c["k"]}">{img(c["ph"], "", sizes="88px")}<p class="n">{SHORT[c["k"]]}<small>{FOR[c["k"]]}</small></p><p class="w">{c["why"]}</p>'
            f'<p class="p num">{price(c["p"])}</p>{add_btn(c["k"])}</div>')

def listbox(pid, title="Список для запиту", lead="Додайте речі з каталогу, вкажіть кількість — і надішліть список: у відповідь отримаєте добірку принтів і розрахунок."):
    return f'''
    <div class="listbox" id="list">
      <div><p class="eyebrow">Ваш список</p><h2 style="font-size:clamp(1.5rem,2.4vw,2rem);margin-top:6px">{title}</h2><p style="color:var(--ink2);margin-top:8px;font-size:.95rem">{lead}</p></div>
      <div class="team" style="margin:0;grid-template-columns:auto auto;gap:12px 28px"><label class="people" for="people">Людей у команді<input id="people" type="number" min="1" inputmode="numeric" value="20"><small style="font-weight:400;color:var(--ink2);font-size:.8rem">Стільки підставимо, коли додаєте річ</small></label>
      <label class="people" for="neu">Із них не носять аксесуари<input id="neu" type="number" min="0" inputmode="numeric" value="0"><small style="font-weight:400;color:var(--ink2);font-size:.8rem">Якщо вкажете: речам «усім» підставимо цю кількість, шовковим — решту</small></label></div>
      <div id="list-rows"><p class="empty">Список порожній. Натисніть «+ До списку» біля речі.</p></div>
      <div class="tot" id="l-foot"><div><b id="l-tot" class="num">0 грн</b><br><span id="l-sub">роздрібні ціни, без доставки</span><br><span>Кожен рядок — окрема кількість. Якщо порівнюєте варіанти, залиште одну позицію або зменшіть кількість.</span></div>
        <div class="acts"><button class="btn btn-line btn-sm" type="button" id="l-copy" aria-disabled="true">Скопіювати</button><a class="btn btn-gold" href="#request" id="l-send" role="button" aria-disabled="true">Надіслати список на розрахунок</a></div></div>
      <p class="note" id="l-plan" hidden>Плануєте подарунки на рік по нагодах? <a href="b2b-team#plan">Порахуйте на сторінці для команди →</a></p>
    </div>'''

LIST_JS = """
    var C = __C__, people = document.getElementById('people'), neu = document.getElementById('neu'), L = {}, order = [];
    function dflt(k) { var n = int(people, 1), m = Math.min(n, int(neu, 0)); return m ? (C[k].all ? m : n - m) || n : n; }
    window.C = C;
    var rowsBox = document.getElementById('list-rows'), focusKey = '';
    function n(k) { return L[k] || 0; }
    function set(k, q) { q = Math.max(0, q | 0); if (q) { if (!L[k]) order.push(k); L[k] = q; } else { delete L[k]; order = order.filter(function (x) { return x !== k; }); } render(); }
    function total() { return order.reduce(function (t, k) { return t + n(k) * C[k].p; }, 0); }
    function count() { return order.reduce(function (t, k) { return t + n(k); }, 0); }
    function qtyc(k) {
      var w = document.createElement('span'); w.className = 'qtyc';
      var m = document.createElement('button'); m.type = 'button'; m.textContent = '−'; m.dataset.q = k + '-'; m.setAttribute('aria-label', 'Менше: ' + C[k].n); m.addEventListener('click', function () { focusKey = k + '-'; set(k, Math.max(1, n(k) - 1)); });
      var i = document.createElement('input'); i.type = 'number'; i.min = '1'; i.inputMode = 'numeric'; i.value = n(k); i.dataset.q = k + '='; i.setAttribute('aria-label', 'Кількість: ' + C[k].n);
      i.addEventListener('change', function () { var v = parseInt(i.value, 10); if (!v || v < 1) { i.value = n(k); return; } focusKey = k + '='; set(k, v); });
      var p = document.createElement('button'); p.type = 'button'; p.textContent = '+'; p.dataset.q = k + '+'; p.setAttribute('aria-label', 'Більше: ' + C[k].n); p.addEventListener('click', function () { focusKey = k + '+'; set(k, n(k) + 1); });
      w.appendChild(m); w.appendChild(i); w.appendChild(p); return w;
    }
    function render() {
      rowsBox.textContent = '';
      if (!order.length) { var e = document.createElement('p'); e.className = 'empty'; e.textContent = 'Список порожній. Натисніть «+ До списку» біля речі.'; rowsBox.appendChild(e); }
      order.forEach(function (k) {
        var r = document.createElement('div'); r.className = 'row';
        var nm = document.createElement('span'); nm.textContent = C[k].n;
        var s = document.createElement('span'); s.className = 's num'; s.textContent = fmt(n(k) * C[k].p);
        var x = document.createElement('button'); x.type = 'button'; x.className = 'x'; x.textContent = '✕'; x.setAttribute('aria-label', 'Прибрати: ' + C[k].n); x.addEventListener('click', function () { set(k, 0); if (!order.length) people.focus({ preventScroll: true }); });
        r.appendChild(nm); r.appendChild(qtyc(k)); r.appendChild(s); r.appendChild(x); rowsBox.appendChild(r);
      });
      if (focusKey) { var fe = rowsBox.querySelector('[data-q="' + focusKey + '"]'); if (fe) fe.focus({ preventScroll: true }); focusKey = ''; }
      document.getElementById('l-foot').hidden = !order.length; document.getElementById('l-plan').hidden = !order.length; document.getElementById('list').classList.toggle('is-empty', !order.length);
      document.getElementById('l-tot').textContent = fmt(total());
      document.getElementById('l-sub').textContent = order.length ? gifts(count()) + ' · ' + order.length + ' ' + pl(order.length, 'позиція', 'позиції', 'позицій') + ' · роздрібні ціни, без доставки' : 'роздрібні ціни, без доставки';
      ['l-send', 'l-copy'].forEach(function (id) { document.getElementById(id).setAttribute('aria-disabled', order.length ? 'false' : 'true'); });
      [].forEach.call(document.querySelectorAll('[data-add]'), function (b) {
        var k = key(b), on = n(k) > 0; b.classList.toggle('on', on); b.textContent = on ? 'У списку: ' + n(k) + ' ✓' : '+ До списку';
      });
      sticky(order.length ? 'Список: ' + plain(fmt(total())) + ' · ' + gifts(count()) : '__STICKY__');
      [].forEach.call(document.querySelectorAll('#sticky a, a[data-go]'), function (a) { a.href = order.length ? '#list' : '#request'; });
    }
    function key(b) { var s = b.dataset.nom && document.getElementById(b.dataset.nom); return s ? s.value : b.dataset.add; }
    [].forEach.call(document.querySelectorAll('[data-add]'), function (b) {
      b.addEventListener('click', function () { var k = key(b); if (n(k)) { document.getElementById('list').scrollIntoView({ behavior: 'smooth', block: 'center' }); return; } set(k, dflt(k)); });
    });
    [].forEach.call(document.querySelectorAll('select.nom'), function (s) { s.addEventListener('change', render); });
    function text() {
      var m = Math.min(int(people, 1), int(neu, 0));
      return ['Список для розрахунку · людей у команді: ' + int(people, 1) + (m ? ', із них не носять аксесуари: ' + m : '') + ' (роздрібні ціни obiimy.world, без доставки):']
        .concat(order.map(function (k) { return '— ' + C[k].n + ': ' + n(k) + ' × ' + plain(fmt(C[k].p)) + ' = ' + plain(fmt(n(k) * C[k].p)); }), ['Разом: ' + plain(fmt(total())) + ' · ' + gifts(count())]);
    }
    document.getElementById('l-send').addEventListener('click', function (e) { if (!order.length) { e.preventDefault(); return; } put(text(), count(), fmt(total()) + ' · ' + gifts(count())); });
    document.getElementById('l-copy').addEventListener('click', function () { if (order.length) copyText(text().join('\\n'), this); });
    render();
"""

def list_js(sticky_text):
    return LIST_JS.replace("__C__", J({c["k"]: dict(n=c["n"], p=c["p"], all=c["neutral"]) for c in CATALOG})).replace("__STICKY__", sticky_text)

def how_short(alt=False):
    return f"""
  <section class="block{" alt" if alt else ""}" id="how"><div class="wrap">
    <div class="head"><p class="eyebrow">Як це працює</p><h2>Три кроки до подарунків</h2></div>
    <div class="steps">
      <div><h3>Список</h3><p>Оберіть речі й кількість на цій сторінці або просто напишіть, скільки подарунків потрібно і до якої дати.</p></div>
      <div><h3>Добірка й розрахунок</h3><p>У відповідь — принти на вибір і розрахунок окремими рядками: речі, привітання, доставка. Чи встигаємо до дати — пишемо одразу.</p></div>
      <div><h3>Відправка</h3><p>Ви надсилаєте список отримувачів і текст привітання. Відправляємо Новою поштою — кожному окремо чи в офіс.</p></div>
    </div>
  </div></section>"""

# ─────────────────────────────────────────────────────────────── 1. catalogue with prices (Classic)
def catalog():
    order = ["tw", "twscr", "mask", "h44", "scr", "book", "cert1", "scrset", "maskscr", "tw44", "h65", "song", "pil", "h88", "three"]
    items = "".join(cert_card(CERTS, "nom-cat") if k == "cert1" else item_card(CAT[k]) for k in order)
    js = """
    var cards = [].slice.call(document.querySelectorAll('.items .item')), onlyAll = document.getElementById('f-all');
    function filt() {
      var b = parseInt(document.querySelector('input[name=fb]:checked').value, 10), shown = 0;
      cards.forEach(function (c) { var ok = (!b || parseInt(c.dataset.p, 10) <= b) && (!onlyAll.checked || c.dataset.all === '1'); c.hidden = !ok; if (ok) shown++; });
      var nom = document.getElementById('nom-cat');
      if (nom) { [].forEach.call(nom.options, function (o) { o.disabled = b && C[o.value].p > b; }); if (nom.selectedOptions[0] && nom.selectedOptions[0].disabled) { var ok = [].filter.call(nom.options, function (o) { return !o.disabled; }); if (ok.length) nom.value = ok[ok.length - 1].value; } render(); }
      document.getElementById('f-cnt').textContent = shown === cards.length ? 'Усі ' + cards.length + ' позицій' : 'Показано ' + shown + ' із ' + cards.length;
    }
    [].forEach.call(document.querySelectorAll('input[name=fb]'), function (r) { r.addEventListener('change', filt); }); onlyAll.addEventListener('change', filt); filt();
    """
    js = list_js("Подарунки для команди · від 700 грн") + js
    body = f'''
  <style>:root{{--bg:#F5F2ED;--bg2:#ECE8E1;--card:#FFFFFF;--line:#D9D2C6}}</style>
  <section class="hero one h1-xs"><div class="wrap">
    <div>
      <p class="eyebrow">Для HR і офіс-менеджерів<span class="m-hide"> · подарунки співробітникам</span></p>
      <h1 style="margin-top:14px">Подарунки для команди: 15 речей і наборів із цінами</h1>
      <p class="lead">Шовкові аксесуари, маски для сну, наволочки й сертифікати — від 700 до 4 800 грн за роздрібною ціною. Оберіть речі й кількість, надішліть список — у відповідь отримаєте добірку принтів і розрахунок.</p>
      <div class="cta" style="margin-top:18px"><a class="btn btn-gold btn-sm" href="#request" data-go>Отримати розрахунок</a><a class="btn btn-line btn-sm m-hide" href="b2b-sets">Готові набори</a></div>
    </div>
  </div></section>

  <section class="block" id="catalog" style="padding-top:0"><div class="wrap">
    <div class="filters">
      <fieldset class="q" style="margin:0"><legend class="sr">Бюджет на людину</legend>{chips("fb", [("0", "Усі ціни"), ("1000", "до 1 000"), ("2500", "до 2 500"), ("5000", "до 5 000")], "0")}</fieldset>
      <label class="tog" style="min-height:0"><input type="checkbox" id="f-all"><span>Лише те, що підходить усім</span></label>
      <span class="cnt" id="f-cnt" aria-live="polite"></span>
    </div>
    <div class="items">{items}</div>
    <p class="note" style="margin-top:14px">Роздрібні ціни obiimy.world. Підписи «кому» — наші поради. Фото — приклад принта; наявність у потрібному форматі підтвердимо в розрахунку.</p>
    <div style="margin-top:34px">{listbox("f-catalog")}</div>
  </div></section>
  {team.facts([("700–4 800 грн", "Роздрібні ціни речей і наборів"), ("15 позицій", "Аксесуари, набори, речі для дому, сертифікат на 1 000–4 000 грн"), ("Є речі для всіх", "Маска, закладка, наволочка, сертифікат"), ("Привітання", "Вашими словами — разом із подарунком")])}

  <section class="block alt" id="why"><div class="wrap">
    <div class="head"><p class="eyebrow">Чому Obiimy</p><h2>Шість причин</h2></div>
    {why_html()}
    <p class="note" style="margin-top:22px">Усі набори, зокрема зібрані під запит, — у <a href="b2b-sets">каталозі корпоративних наборів</a>. Плануєте подарунки на рік? <a href="b2b-team#plan">Порахуйте по нагодах →</a></p>
  </div></section>
  {how_short(alt=False)}
  {team.faq_section(alt=True)}
  {team.proof_section(alt=False)}
  {team.request_section("f-catalog", "Список подарунків для команди", "Отримати добірку й розрахунок", "Залиште контакти й дату, до якої потрібні подарунки. Список із каталогу додається до запиту одним натиском.", "list", alt=False)}
  ''' + team.script("f-catalog", js)
    return dict(slug="b2b-team-catalog", skin="classic", bar=BAR, title="Подарунки для команди з цінами — каталог Obiimy для HR",
                desc="15 речей і наборів для співробітників із роздрібними цінами від 700 до 4 800 грн: шовкові аксесуари, маски для сну, наволочки, сертифікати. Список і розрахунок для компанії.",
                og="img/sets/twscr-makiv.webp", nav=[("Каталог", "catalog"), ("Чому Obiimy", "why"), ("Як це працює", "how"), ("Питання", "faq")],
                cta="Запит", sticky="Подарунки для команди · від 700 грн", body=body)

# ─────────────────────────────────────────────────────────────── 2. three shelves by budget (Lookbook)
def budget():
    shelves = ""
    for v, t, sub, ks in SHELVES:
        certs = [k for k in ks if k in CERTS]
        rows = "".join(cert_row(certs, f"nom-{v}") if k == certs[0] else item_row(CAT[k]) for k in ks if k not in certs[1:]) if certs else "".join(item_row(CAT[k]) for k in ks)
        shelves += f'''
  <section class="shelf" id="b{v}"><div class="wrap">
    <div class="top"><h2>{t}</h2><span class="sub">{sub}</span><span class="ex num" data-ex="{v}"></span></div>
    {'<p class="note" style="margin:-8px 0 12px">Роздрібні ціни obiimy.world. Підписи «кому» — наші поради; фото — приклад принта.</p>' if v == "1000" else ""}
    <div class="rows">{rows}</div>
  </div></section>'''
    shelves = shelves.replace('<section class="shelf" id="b1000">', '<section class="shelf" id="b1000" style="border-top:0;padding-top:0">', 1)
    js = list_js("Три бюджети · від 700 грн") + """
    function ex() {
      var p = int(people, 1);
      [].forEach.call(document.querySelectorAll('[data-ex]'), function (e) { var b = parseInt(e.dataset.ex, 10); e.textContent = p + ' людям — до ' + plain(fmt(p * b)); });
    }
    people.addEventListener('input', ex); ex();
    """
    strip = "".join(img(ph, a, sizes="(max-width: 640px) 50vw, 25vw") for ph, a in [("img/sets/twscr-makiv.webp", "Твіллі й резинка у святковій коробці"), ("img/twilly-zolote.webp", "Шовкова твіллі"), ("img/mask-svoboda.webp", "Шовкова маска для сну"), ("img/sets/three-twilly.webp", "Три твіллі в одній коробці")])
    body = f'''
  <section class="hero h1-xs" style="padding-bottom:clamp(12px,2vw,28px)"><div class="wrap" style="align-items:center;grid-template-columns:minmax(0,7fr) minmax(0,5fr)">
    <div>
      <p class="eyebrow">Для HR і офіс-менеджерів<span class="m-hide"> · подарунки співробітникам</span></p>
      <h1 style="margin-top:14px">Що подарувати команді на 1 000, 2 500 і 5 000 грн на людину</h1>
      <p class="lead">Три полиці за бюджетом — кожна річ із роздрібною ціною з obiimy.world. Додайте те, що підходить, у список і надішліть на розрахунок.</p>
      <div class="cta row" style="margin-top:18px"><a class="btn btn-line btn-sm" href="#b1000">До 1 000</a><a class="btn btn-line btn-sm" href="#b2500">До 2 500</a><a class="btn btn-line btn-sm" href="#b5000">До 5 000</a><a class="btn btn-gold btn-sm" href="#request" data-go>Отримати розрахунок</a></div>
      <p class="fine m-hide">{SAMPLE} Або одразу: <a href="{PHONE_HREF}">{PHONE}</a></p>
    </div>
    <div class="strip m-hide">{strip}</div>
  </div></section>
  {shelves}
  {team.facts([("3 бюджети", "До 1 000, 2 500 і 5 000 грн на людину"), ("15 позицій", "Аксесуари, набори, речі для дому, сертифікат на 1 000–4 000 грн"), ("Є речі для всіх", "Маска, закладка, наволочка, сертифікат"), ("Привітання", "Вашими словами — разом із подарунком")])}
  <section class="block alt" id="list-block"><div class="wrap two">
    {listbox("f-budget", "Список для запиту", "Речі з полиць збираються тут. Вкажіть кількість і надішліть на розрахунок.")}
    <div class="side"><div class="card"><p class="eyebrow">Чому Obiimy</p><ul>{"".join(f"<li><span><b>{b}</b> — {lc(s)}</span></li>" for b, s in WHY)}</ul></div></div>
  </div></section>
  {how_short(alt=False)}
  {team.faq_section(alt=True)}
  {team.proof_section(alt=False)}
  {team.request_section("f-budget", "Подарунки для команди за бюджетом", "Отримати добірку й розрахунок", "Залиште контакти й дату, до якої потрібні подарунки. Список із полиць додається до запиту одним натиском.", "list", alt=False)}
  ''' + team.script("f-budget", js)
    return dict(slug="b2b-team-budget", skin="lookbook", bar=BAR, title="Подарунки команді на 1 000, 2 500 і 5 000 грн — Obiimy",
                desc="Три полиці за бюджетом на людину: до 1 000, 2 500 і 5 000 грн. Шовкові аксесуари, маски для сну, наволочки, сертифікати з роздрібними цінами. Список і розрахунок для компанії.",
                og="img/sets/three-twilly.webp", nav=[("До 1 000", "b1000"), ("До 2 500", "b2500"), ("До 5 000", "b5000"), ("Список", "list"), ("Питання", "faq")],
                cta="Запит", sticky="Три бюджети · від 700 грн", body=body)

# ─────────────────────────────────────────────────────────────── 3. a one-screen commercial proposal (Campaign, dark)
def offer():
    rows = "".join(f'<tr><td>{img(CAT[k]["ph"], "", sizes="64px")}</td><td class="n">{SHORT[k]}<small>{FOR[k]} · {CAT[k]["why"]}</small></td><td class="p num">{price(CAT[k]["p"])}</td><td class="a">{add_btn(k)}</td></tr>' for k in OFFER)
    js = list_js("Пропозиція для команди · від 700 грн")
    body = f'''
  <section class="hero h1-xs" style="padding-bottom:clamp(24px,4vw,48px)"><div class="wrap" style="grid-template-columns:1fr">
    <div>
      <p class="eyebrow">Для HR і офіс-менеджерів<span class="m-hide"> · комерційна пропозиція</span></p>
      <h1 style="margin-top:14px">Подарунки для команди: вісім позицій, ціни й що далі — на одному екрані</h1>
      <p class="lead">Роздрібні ціни з obiimy.world. Оберіть позиції, вкажіть кількість — надішлемо добірку принтів і розрахунок для компанії.</p>
      <div class="cta"><a class="btn btn-gold" href="#request" data-go>Отримати розрахунок</a><a class="btn btn-line" href="b2b-team-catalog">Усі 15 позицій</a></div>
    </div>
  </div></section>
  <section class="block offer" style="padding-top:0" id="offer"><div class="wrap two">
    <div>
      <table>
        <thead><tr><th></th><th>Позиція</th><th style="text-align:right">Ціна</th><th></th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      <p class="note" style="margin-top:14px">Підписи «кому» — наші поради. Фото — приклад принта; наявність у потрібному форматі підтвердимо в розрахунку. Усі 15 позицій — у <a href="b2b-team-catalog">каталозі з цінами</a>, набори — у <a href="b2b-sets">каталозі наборів</a>.</p>
    </div>
    <div class="side" style="position:static">
      <div class="card"><p class="eyebrow">Що буде після запиту</p><ul>
        <li><span><b>Привітання</b> вашими словами — разом із подарунком.</span></li>
        <li><span><b>Відправка</b> Новою поштою: кожному окремо чи в офіс, по Україні; за кордон — як домовимось у розрахунку.</span></li>
        <li><span><b>Строки</b> залежать від кількості й наявності принтів — вкажіть дату, відповімо, чи встигаємо.</span></li>
        <li><span><b>Оплата й документи</b> для компанії — підтвердимо разом із розрахунком.</span></li>
        <li><span><b>Ціни роздрібні</b>, з obiimy.world; умови для вашої кількості — у розрахунку.</span></li>
      </ul><a class="btn btn-gold" href="#request" data-go style="justify-self:start">Отримати розрахунок</a></div>
      <div class="card"><p class="eyebrow">Одразу</p><p><a href="{PHONE_HREF}" style="font-family:var(--display);font-size:1.4rem;text-decoration:none">{PHONE}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p><p style="font-size:.88rem">{SAMPLE}</p></div>
      {listbox("f-offer", "Ваш список", "Кількість підставляємо з поля «Людей у команді» — змініть під себе.")}
    </div>
  </div></section>
  {team.everyone_section(alt=True)}
  <section class="block" id="why"><div class="wrap"><div class="head"><p class="eyebrow">Чому Obiimy</p><h2>Чотири причини</h2></div>{why_html(items=WHY[:3] + WHY[5:])}</div></section>
  {how_short(alt=True)}
  {team.faq_section(alt=False)}
  {team.proof_section(alt=True)}
  {team.request_section("f-offer", "Комерційна пропозиція: подарунки для команди", "Отримати добірку й розрахунок", "Залиште контакти й дату, до якої потрібні подарунки. Список позицій додається до запиту одним натиском.", "list", alt=False)}
  ''' + team.script("f-offer", js)
    return dict(slug="b2b-team-offer", skin="maison", bar=BAR, title="Комерційна пропозиція: подарунки для команди — Obiimy",
                desc="Вісім позицій із роздрібними цінами від 700 до 3 200 грн, що буде після запиту й форма — на одному екрані. Шовкові аксесуари, маски для сну, сертифікати для співробітників.",
                og="img/sets/tw44-vpevnenist.webp", nav=[("Пропозиція", "offer"), ("Для всіх", "all"), ("Чому Obiimy", "why"), ("Як це працює", "how"), ("Питання", "faq")],
                cta="Запит", sticky="Пропозиція для команди · від 700 грн", body=body)

def build():
    b2b.CSS += team.CSS + CSS
    for fn in (catalog, budget, offer):
        p = fn()
        html = typo(team.bind(b2b.shell(p, p["body"])))
        (b2b.OUT / f"{p['slug']}.html").write_text(html)
        print(p["slug"], len(html) // 1024, "KB")

if __name__ == "__main__":
    build()
