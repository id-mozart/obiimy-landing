#!/usr/bin/env python3
"""The one B2B page for gifts inside a company — the best of the seven after six audit rounds:
brand on the first screen, the catalogue with prices right after it, a yearly plan with three programmes as presets,
things for everyone, greetings, reasons, steps, FAQ, trust, request. Facts, prices and helpers come from
build-b2b-team.py and build-b2b-team-shop.py; nothing promises a discount, a deadline or a minimum order."""
import importlib.util, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
shop = load("build-b2b-team-shop")
team = shop.team
b2b, img, price, typo, J, hero = team.b2b, team.img, team.price, team.typo, team.J, team.hero
CATALOG, CAT, STAGES, PLANS, CARDS = team.CATALOG, team.CAT, team.STAGES, team.PLANS, team.CARDS
PHONE, PHONE_HREF, SAMPLE, BAR = team.PHONE, team.PHONE_HREF, team.SAMPLE, team.BAR

# three programmes as presets for the calculator: occasion row -> (silk, for everyone, share of the team)
PRESETS = [
    ("base", "«Знак уваги»", "Один подарунок на рік: шовкова резинка до дня народження (для всіх — закладка).", {"bday": ("scr", "book", 1)}),
    ("team", "«Команда»", "Два подарунки на рік: твіллі до дня народження й резинка до перемоги команди (для всіх — сертифікат 1 500 і закладка).", {"bday": ("tw", "cert15", 1), "team": ("scr", "book", 1)}),
    ("plus", "«Визнання»", "Два подарунки на рік: набір «твіллі та резинка» до дня народження й хустка 65 × 65 до річниці (для всіх — сертифікат 2 000 і маска).", {"bday": ("twscr", "cert2", 1), "years": ("h65", "mask", 1)}),
]
def preset_range(rows):
    s = sum(CAT[a]["p"] for a, _b, _sh in rows.values()); u = sum(CAT[b]["p"] for _a, b, _sh in rows.values())
    return price(s) if s == u else f"{min(s, u):,}".replace(",", " ") + "–" + price(max(s, u))

CSS = """
  .presets { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-bottom: 26px; }
  .preset { position: relative; display: grid; gap: 6px; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 18px 20px; cursor: pointer; text-align: left; font: inherit; color: inherit; }
  .preset:hover { border-color: var(--ink); }
  .preset.on { border-color: var(--ink); box-shadow: inset 0 0 0 1px var(--ink); }
  .preset h3 { font-size: 1.3rem; }
  .preset .pp { font-family: var(--display); font-size: 1.3rem; font-variant-numeric: lining-nums tabular-nums; }
  .preset .pp small { display: block; font-family: var(--body); font-size: .78rem; color: var(--ink2); }
  .preset p { color: var(--ink2); font-size: .88rem; }
  .preset .tag { position: absolute; top: 12px; right: 14px; font-size: .7rem; letter-spacing: .12em; text-transform: uppercase; color: var(--ink3); font-weight: 600; }
  .preset.on .tag { color: var(--ink); }
  .occs { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-bottom: 26px; }
  .occ { display: grid; grid-template-columns: 56px minmax(0, 1fr); gap: 12px; align-items: center; padding: 12px 14px; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); }
  .occ img { width: 56px; height: 56px; object-fit: cover; border-radius: calc(var(--radius) - 2px); background: #F1EEE8; }
  .occ b { font-family: var(--display); font-weight: 400; font-size: 1.05rem; line-height: 1.15; display: block; }
  .occ span { color: var(--ink2); font-size: .82rem; }
  .greet { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px 28px; max-width: 900px; }
  .greet .paper { position: static; width: auto; max-height: none; transform: rotate(-1.5deg); padding: 22px 22px 18px; }
  .greet .paper:nth-child(2n) { transform: rotate(1deg); }
  .greet .paper .t { font-size: 1.3rem; }
  .greet .paper small { display: block; font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: #8A8480; margin-bottom: 8px; }
  .whyhow { display: grid; grid-template-columns: minmax(0, 6fr) minmax(0, 5fr); gap: clamp(24px, 4vw, 64px); align-items: start; }
  .whyhow .why { grid-template-columns: 1fr 1fr; }
  .whyhow .steps { grid-template-columns: 1fr; gap: 16px; }
  .hero.main { padding-block: clamp(20px, 4vw, 52px) clamp(20px, 4vw, 44px); }
  .hero.main h1 { font-size: clamp(2rem, 3.4vw, 3.1rem); }
  .hero.main .lead { margin-top: 14px; font-size: 1.05rem; }
  .hero.main .cta { margin-top: 22px; }
  .hero.main figure img { aspect-ratio: 3 / 2; object-position: 50% 24%; }
  @media (max-width: 640px) { .hero.main .lead, .hero.main .fine { display: none; } .hero.main figure img { aspect-ratio: 2 / 1; object-position: 50% 58%; } }
  .cathead { display: flex; flex-wrap: wrap; align-items: center; gap: 12px 28px; margin-bottom: 18px; }
  .cathead h2 { font-size: clamp(1.5rem, 2.4vw, 2rem); margin-right: auto; }
  .cathead .filters { margin: 0; }
  @media (max-width: 960px) { .presets, .occs, .greet { grid-template-columns: 1fr 1fr; } .whyhow { grid-template-columns: 1fr; } }
  .hero p.m-only, p.m-only { display: none; }
  @media (max-width: 640px) { p.m-only { display: block; } .items.collapsed .item:nth-child(n+9) { display: none; } }
  figure.wide { margin: 0; } figure.wide img { width: 100%; aspect-ratio: 21 / 9; object-fit: cover; object-position: 50% 22%; border-radius: var(--radius); }
  @media (max-width: 640px) { figure.wide img { aspect-ratio: 4 / 3; } .filters .chips { padding-right: 12px; } }
  @media (max-width: 640px) { .presets, .greet, .occs { grid-template-columns: 1fr; } .occs { gap: 8px; } .occ { grid-template-columns: 48px 1fr; padding: 8px 12px; } .occ img { width: 48px; height: 48px; } .occ b { display: inline; } .occ span { display: inline; } .occ span::before { content: " — "; } .whyhow .why { grid-template-columns: 1fr; } }
"""

def plan_section():
    """Eight occasions with a recommended thing, three programmes as presets, the calculator with a silk / for-everyone split."""
    opts = "".join(team.opt(c) for c in CATALOG)
    occs = "".join(f'<div class="occ">{img(CAT[silk]["ph"], CAT[silk]["n"], sizes="56px")}<div><b>{short}</b><span>{shop.SHORT[silk]} · {price(CAT[silk]["p"])}</span></div></div>' for sid, short, _t, _d, p, a, silk, _n, _sh in STAGES)
    presets = "".join(f'<button type="button" class="preset" data-preset="{pid}" aria-pressed="false" aria-label="Програма {name}, {preset_range(rows)} на людину на рік"><span class="tag" aria-hidden="true">Обрати</span><h3>{name}</h3><span class="pp">{preset_range(rows)}<small>на людину на рік · роздрібні ціни</small></span><p>{who}</p></button>' for pid, name, who, rows in PRESETS)
    rows = "".join(f'''<div class="row" data-id="{sid}" data-share="{share}" data-silk="{silk}" data-neutral="{neu}">
        <input type="checkbox" id="c-{sid}" {"checked" if sid in ("first", "bday", "years") else ""} aria-label="{short}: враховувати в плані">
        <label class="n" for="c-{sid}">{short}</label>
        <span class="qty"><input type="number" min="0" inputmode="numeric" aria-label="{short}: скільки подарунків на рік" data-k="n"><small>шт. на рік</small></span>
        <span class="sel"><small>Шовкова річ</small><select aria-label="{short}: шовкова річ" data-k="silk">{opts}</select></span>
        <span class="sel"><small>Тим, хто не носить аксесуари</small><select aria-label="{short}: річ для тих, хто не носить аксесуари" data-k="neu">{opts}</select></span>
        <span class="sum"><b class="num" data-k="sum"></b><small data-k="split"></small></span></div>''' for sid, short, _t, _d, _p, _a, silk, neu, share in STAGES)
    js = """
    var P = __P__, N = __N__, SN = __SN__, PRE = __PRE__;
    var rows = [].slice.call(document.querySelectorAll('#rows .row[data-id]')), tpeople = document.getElementById('t-people'), tneu = document.getElementById('t-neu');
    function defaults() {
      var n = int(tpeople, 1);
      rows.forEach(function (r) { var q = r.querySelector('[data-k=n]'); if (!q.dataset.touched) q.value = Math.max(1, Math.round(n * parseFloat(r.dataset.share))); });
    }
    rows.forEach(function (r) { r.querySelector('[data-k=silk]').value = r.dataset.silk; r.querySelector('[data-k=neu]').value = r.dataset.neutral; });
    var state = { total: 0, gifts: 0, lines: [], n: 0, m: 0 };
    function calc() {
      var total = 0, g = 0, lines = [], n = int(tpeople, 1), m = Math.min(n, int(tneu, 0));
      document.getElementById('t-warn').textContent = int(tneu, 0) > n ? 'Людей у команді менше, ніж тих, хто не носить аксесуари, — рахуємо для ' + n + '.' : '';
      document.getElementById('rows').classList.toggle('one', !m);
      rows.forEach(function (r) {
        var on = r.querySelector('input[type=checkbox]').checked, q = int(r.querySelector('[data-k=n]'), 0);
        var ks = r.querySelector('[data-k=silk]').value, kn = r.querySelector('[data-k=neu]').value;
        var qn = Math.min(q, Math.round(q * m / n)), qs = q - qn, same = ks === kn || !qn, s = qs * P[ks] + qn * P[kn];
        if (same) { qs = q; qn = 0; s = q * P[ks]; }
        r.classList.toggle('off', !on);
        r.querySelector('[data-k=sum]').textContent = on ? fmt(s) : '—';
        r.querySelector('[data-k=split]').textContent = on && qn ? (qs + ' × ' + SN[ks]).replace(/ /g, '\\u00a0') + ' + ' + (qn + ' × ' + SN[kn]).replace(/ /g, '\\u00a0') : '';
        if (on && q > 0) { total += s; g += q; lines.push('— ' + r.querySelector('label.n').textContent + ': ' + qs + ' × ' + N[ks] + (qn ? ' + ' + qn + ' × ' + N[kn] : '') + ' = ' + plain(fmt(s))); }
      });
      state = { total: total, gifts: g, lines: lines, n: n, m: m };
      document.getElementById('tot').textContent = fmt(total);
      document.getElementById('tot-s').textContent = g ? gifts(g) + ' на рік · роздрібні ціни, без доставки' : 'Позначте хоча б одну нагоду';
      ['send', 'copy'].forEach(function (id) { document.getElementById(id).setAttribute('aria-disabled', g ? 'false' : 'true'); });
      [].forEach.call(document.querySelectorAll('.preset'), function (b) { var on = b.dataset.preset === curPreset; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.querySelector('.tag').textContent = on ? 'Обрано ✓' : 'Обрати'; });
    }
    var curPreset = '';
    function applyPreset(id, quiet) {
      var n = int(tpeople, 1), cfg = PRE[id]; curPreset = id;
      rows.forEach(function (r) {
        var c = cfg[r.dataset.id]; r.querySelector('input[type=checkbox]').checked = !!c;
        if (c) { r.querySelector('[data-k=silk]').value = c[0]; r.querySelector('[data-k=neu]').value = c[1]; var q = r.querySelector('[data-k=n]'); q.value = Math.max(1, Math.round(n * c[2])); q.dataset.touched = '1'; }
      });
      calc();
      if (!quiet) document.getElementById('rows').scrollIntoView({ block: 'start', behavior: 'smooth' });
    }
    [].forEach.call(document.querySelectorAll('.preset'), function (b) { b.addEventListener('click', function () { applyPreset(b.dataset.preset); }); });
    function ptext() { return ['План на рік' + (curPreset ? ' · програма ' + document.querySelector('.preset.on h3').textContent : '') + ' · людей у команді: ' + state.n + (state.m ? ', із них не носять аксесуари: ' + state.m : '') + ' (роздрібні ціни obiimy.world, без доставки):'].concat(state.lines, ['Разом: ' + plain(fmt(state.total)) + ' · ' + gifts(state.gifts)]); }
    rows.forEach(function (r) {
      r.querySelector('[data-k=n]').addEventListener('input', function () { this.dataset.touched = '1'; curPreset = ''; calc(); });
      [].forEach.call(r.querySelectorAll('select'), function (s) { s.addEventListener('change', function () { curPreset = ''; calc(); }); });
      r.querySelector('input[type=checkbox]').addEventListener('change', function () { curPreset = ''; calc(); });
    });
    tpeople.addEventListener('input', function () { if (curPreset) applyPreset(curPreset, true); else { defaults(); calc(); } });
    tneu.addEventListener('input', calc);
    function mirror(a, b) { a.addEventListener('input', function () { if (b.value !== a.value) { b.value = a.value; b.dispatchEvent(new Event('input')); } }); }
    mirror(people, tpeople); mirror(tpeople, people); mirror(neu, tneu); mirror(tneu, neu);
    defaults(); calc();
    document.getElementById('send').addEventListener('click', function (e) { if (!state.gifts) { e.preventDefault(); return; } put(ptext(), state.gifts, fmt(state.total) + ' · ' + gifts(state.gifts) + ' на рік', 'План на рік'); });
    document.getElementById('copy').addEventListener('click', function () { if (state.gifts) copyText(ptext().join('\\n'), this); });
    """.replace("__P__", J({c["k"]: c["p"] for c in CATALOG})).replace("__N__", J({c["k"]: c["n"] for c in CATALOG})).replace("__SN__", J({c["k"]: team.SHORT_N.get(c["k"], c["n"]).lower() for c in CATALOG})).replace("__PRE__", J({pid: {k: list(v) for k, v in rows.items()} for pid, _n, _w, rows in PRESETS}))
    html = f'''
  <section class="block alt" id="plan"><div class="wrap">
    <div class="head"><p class="eyebrow">План на рік</p><h2>Вісім нагод — і скільки це коштує вашій команді</h2><p class="sub">Від першого дня до прощання. Оберіть програму або позначте нагоди самі — сума рахується за роздрібними цінами й додається до запиту одним натиском.</p></div>
    <div class="occs">{occs}</div>
    <div class="presets" role="group" aria-label="Програми на рік">{presets}</div>
    <div class="team"><label class="p" for="t-people">Людей у команді<input id="t-people" type="number" min="1" inputmode="numeric" value="40"></label>{team.split_field("t-neu", 16)}</div>
    <p class="warn" id="t-warn" aria-live="polite" style="margin:-10px 0 14px"></p>
    <div class="plan" id="rows">
      <div class="row hd" aria-hidden="true"><span></span><span>Нагода</span><span>На рік</span><span>Шовкова річ</span><span>Тим, хто не носить аксесуари</span><span style="text-align:right">Сума</span></div>
      {rows}
    </div>
    <div class="total"><div class="fig" aria-live="polite"><b id="tot" class="num">0 грн</b><span id="tot-s"></span></div>
      <div class="acts"><button class="btn btn-line" type="button" id="copy">Скопіювати план</button><a class="btn btn-gold" href="#request" id="send" role="button">Надіслати план на розрахунок</a></div></div>
    <p class="note">Програми — приклади: нагоди й речі можна замінити. Підписи «кому» — наші поради; фото — приклад принта. Точний розрахунок для вашої компанії надішлемо у відповідь на запит.</p>
  </div></section>'''
    return html, js

def greetings():
    cards = "".join(f'<div class="paper"><small>{lab}</small><p class="t">{t.replace(chr(10), "<br>")}</p><p class="s">— ваша команда</p></div>' for k, lab, t in CARDS if k in ("first", "bday", "years", "team"))
    return f'''
  <section class="block" id="words"><div class="wrap">
    <div class="head"><p class="eyebrow">Привітання</p><h2>Слова від компанії — разом із подарунком</h2><p class="sub">Текст — ваш: до кожної нагоди свій або один на всіх. Оформлення привітання узгодимо у розрахунку. Нижче — наші приклади.</p></div>
    <div class="greet">{cards}</div>
  </div></section>'''

def whyhow():
    return f'''
  <section class="block alt" id="why"><div class="wrap whyhow">
    <div><div class="head"><p class="eyebrow">Чому Obiimy</p><h2>Чотири причини</h2></div>{shop.why_html(items=shop.WHY[:3] + shop.WHY[5:])}</div>
    <div><div class="head"><p class="eyebrow">Як це працює</p><h2>Три кроки</h2></div>
      <div class="steps">
        <div><h3>Список</h3><p>Оберіть речі й кількість на цій сторінці або просто напишіть, скільки подарунків потрібно і до якої дати.</p></div>
        <div><h3>Добірка й розрахунок</h3><p>У відповідь — принти на вибір і розрахунок окремими рядками: речі, привітання, доставка. Чи встигаємо до дати — пишемо одразу.</p></div>
        <div><h3>Відправка</h3><p>Ви надсилаєте список отримувачів і текст привітання. Відправляємо Новою поштою — кожному окремо чи в офіс, по Україні; за кордон — як домовимось.</p></div>
      </div>
      <p class="note" style="margin-top:18px"><a href="obiimy-podarunky-dlia-komandy.pdf" download="Obiimy-podarunky-dlia-komandy.pdf" type="application/pdf">Презентація для HR (PDF, 1,8 МБ) ↓</a> · <a href="b2b-team-details">Усе про шовк, пакування й доставку →</a></p>
    </div>
  </div></section>
  <section class="block alt" style="padding-top:0" aria-hidden="true"><div class="wrap"><figure class="wide">{img("photo/kolo-3.webp", "Шовкова хустка на плечах поверх бежевого пальта", sizes="100vw")}</figure></div></section>'''

def main():
    order = ["tw", "twscr", "mask", "h44", "scr", "book", "cert1", "scrset", "maskscr", "tw44", "h65", "song", "pil", "h88", "three"]
    items = "".join(shop.cert_card(shop.CERTS, "nom-cat") if k == "cert1" else shop.item_card(CAT[k]) for k in order)
    plan_html, plan_js = plan_section()
    js = shop.list_js("Подарунки для команди · від 700 грн", "Список із каталогу") + """
    var cards = [].slice.call(document.querySelectorAll('.items .item')), onlyAll = document.getElementById('f-all');
    function filt() {
      var b = parseInt(document.querySelector('input[name=fb]:checked').value, 10), shown = 0;
      cards.forEach(function (c) { var ok = (!b || parseInt(c.dataset.p, 10) <= b) && (!onlyAll.checked || c.dataset.all === '1'); c.hidden = !ok; if (ok) shown++; });
      var nom = document.getElementById('nom-cat');
      if (nom) { [].forEach.call(nom.options, function (o) { o.disabled = b && C[o.value].p > b; }); if (nom.selectedOptions[0] && nom.selectedOptions[0].disabled) { var ok = [].filter.call(nom.options, function (o) { return !o.disabled; }); if (ok.length) nom.value = ok[ok.length - 1].value; } render(); }
      document.getElementById('f-cnt').textContent = shown === cards.length ? 'Усі ' + cards.length + ' позицій' : 'Показано ' + shown + ' із ' + cards.length;
      // a filter shows everything it matches: no collapsed tail on the phone
      var all = shown === cards.length; document.getElementById('items').classList.toggle('collapsed', all && !opened); document.getElementById('more').parentNode.hidden = !all || opened;
    }
    var opened = false;
    [].forEach.call(document.querySelectorAll('input[name=fb]'), function (r) { r.addEventListener('change', filt); }); onlyAll.addEventListener('change', filt); filt();
    document.getElementById('more').addEventListener('click', function () { opened = true; this.setAttribute('aria-expanded', 'true'); document.getElementById('items').classList.remove('collapsed'); this.parentNode.hidden = true; var c = cards[8]; if (c) { c.setAttribute('tabindex', '-1'); c.focus({ preventScroll: true }); c.scrollIntoView({ block: 'start', behavior: 'smooth' }); } });
    """ + plan_js
    body = hero("Для HR і офіс-менеджерів<span class=\"m-hide\"> · подарунки співробітникам</span>", "Шовкові подарунки для команди: ціни й план на рік",
        "Речі й набори від 700 грн за роздрібною ціною, привітання вашими словами, відправка кожному або в офіс. Оберіть речі чи програму на рік — у відповідь на запит надішлемо добірку принтів і розрахунок.",
        "До каталогу з цінами", "План на рік", "#plan", SAMPLE,
        "photo/hratsiia-2.webp", "Шовкова хустка поясом на синьому жакеті", "Шовкова хустка — поясом на жакеті", cls=" h1-sm ph-first main", pos="50% 58%", cta1_href="#catalog") + f'''

  <section class="block" id="catalog" style="padding-top:clamp(20px,3vw,40px)"><div class="wrap">
    <div class="cathead"><h2>Речі, набори й ціни</h2>
    <div class="filters">
      <fieldset class="q" style="margin:0"><legend class="sr">Бюджет на людину</legend>{shop.chips("fb", [("0", "Усі ціни"), ("1000", "до 1 000"), ("2500", "до 2 500"), ("5000", "до 5 000")], "0")}</fieldset>
      <label class="tog" style="min-height:0"><input type="checkbox" id="f-all"><span>Лише те, що підходить усім</span></label>
      <span class="cnt" id="f-cnt" aria-live="polite"></span>
    </div></div>
    <div class="items collapsed" id="items">{items}</div>
    <p class="m-only" style="margin-top:12px"><button type="button" class="btn btn-line btn-sm" id="more" style="width:100%" aria-expanded="false" aria-controls="items">Показати всі 15 позицій</button></p>
    <p class="note" style="margin-top:14px">Роздрібні ціни obiimy.world. Підписи «кому» — наші поради. Фото — приклад принта; наявність у потрібному форматі підтвердимо в розрахунку. Набори з принтами на вибір — у <a href="b2b-sets-gallery">вітрині наборів</a>.</p>
    <div style="margin-top:34px">{shop.listbox("f-main").replace('value="20"', 'value="40"').replace('id="neu" type="number" min="0" inputmode="numeric" value="0"', 'id="neu" type="number" min="0" inputmode="numeric" value="16"').replace('Плануєте подарунки на рік по нагодах? <a href="b2b-team#plan">Порахуйте на сторінці для команди →</a>', 'Плануєте на рік? <a href="#plan">План по нагодах — нижче ↓</a>')}</div>
  </div></section>
  {team.facts([("700–4 800 грн", "Роздрібні ціни речей і наборів"), ("15 позицій", "Аксесуари, набори, речі для дому, сертифікат на 1 000–4 000 грн"), ("Є речі для всіх", "Маска, закладка, наволочка, сертифікат"), ("Привітання", "Вашими словами — разом із подарунком")])}
  {plan_html}
  {greetings().replace('<section class="block" id="words">', '<section class="block alt" id="words">')}
  {whyhow().replace('<section class="block alt" id="why">', '<section class="block" id="why">')}
  {team.faq_section(alt=True)}
  {team.proof_section(alt=False)}
  {team.request_section("f-main", "Подарунки для команди", "Отримати добірку й розрахунок", "Залиште контакти й дату, до якої потрібні подарунки. Список із каталогу та план на рік додаються до запиту одним натиском.", "catalog")}
  ''' + team.script("f-main", js)
    return dict(slug="b2b-team-main", skin="form", bar=BAR, title="Шовкові подарунки для команди з цінами й планом на рік — Obiimy",
                desc="Подарунки співробітникам від Obiimy: 15 речей і наборів із роздрібними цінами від 700 грн, речі для всіх, три програми на рік і калькулятор по нагодах, привітання вашими словами.",
                og="photo/hratsiia-2.webp", nav=[("Каталог", "catalog"), ("План на рік", "plan"), ("Привітання", "words"), ("Чому Obiimy", "why"), ("Питання", "faq")],
                cta="Запит", sticky="Подарунки для команди · від 700 грн", body=body)

def build():
    b2b.CSS += team.CSS + shop.CSS + CSS
    p = main()
    html = typo(team.bind(b2b.shell(p, p["body"])))
    (b2b.OUT / f"{p['slug']}.html").write_text(html)
    print(p["slug"], len(html) // 1024, "KB")

if __name__ == "__main__":
    build()
