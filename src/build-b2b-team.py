#!/usr/bin/env python3
"""B2B page for internal gifts (HR, office managers): b2b-team.html.
Occasions follow a person's path in the company; a yearly plan calculator fills the request form.
Prices are retail prices from obiimy.world (review/SITE-FACTS.md); nothing here promises a discount or a deadline."""
import importlib.util, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("b2b", ROOT / "build-b2b.py")
b2b = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(b2b)
img, hero, facts_html, proof_html, form_html = b2b.img, b2b.hero, b2b.facts_html, b2b.proof_html, b2b.form_html
PHONE, PHONE_HREF, MAIL, TG, SHOWROOM = b2b.PHONE, b2b.PHONE_HREF, b2b.MAIL, b2b.TG, b2b.SHOWROOM

# retail prices, obiimy.world
ITEMS = [
    ("scr", "Шовкова резинка", 700), ("book", "Закладка для книги", 800), ("cert1", "Сертифікат 1 000 грн", 1000),
    ("tw", "Твіллі 84 × 5", 1600), ("tee", "Футболка Obiimy", 1700), ("cert2", "Сертифікат 2 000 грн", 2000),
    ("set", "Набір: твіллі + резинка", 2200), ("h44", "Хустка 44 × 44, двосторонній друк", 2400), ("mask", "Маска для сну", 2700),
    ("h65", "Хустка 65 × 65", 3200), ("cert4", "Сертифікат 4 000 грн", 4000), ("pil", "Шовкова наволочка 50 × 70", 4200),
    ("h88", "Хустка 88 × 88", 4400),
]
NAME = {k: n for k, n, _ in ITEMS}; PRICE = {k: p for k, _, p in ITEMS}

# occasion: id, short label, title, text, photo, alt, default item, default share of the team per year (editable on the page)
STAGES = [
    ("first", "Перший день", "Перший день у компанії", "Людина ще не знає, де кавоварка, а на столі вже лежить шовкова річ із привітанням від команди. Найкоротший шлях до «мені тут раді».", "img/set-zolote.webp", "Шовковий набір у фірмовій коробці", "tw", .15),
    ("trial", "Випробувальний", "Випробувальний позаду", "Три місяці минули, людина залишається. Невеликий знак: твіллі або закладка для книги з листівкою від керівника.", "photo/bag-2.webp", "Шовкова твіллі на ручці сумки", "book", .15),
    ("bday", "День народження", "День народження", "Подарунок за списком на місяць: відправляємо кожному на відділення Нової пошти або однією посилкою в офіс. Не знаєте смаків — сертифікат.", "img/scrunchie-pole.webp", "Шовкова резинка у коробочці", "scr", 1),
    ("years", "Річниця в компанії", "Рік, три, п’ять, десять", "Що довше людина з вами, то більша річ: твіллі на перший рік, хустка 65 × 65 на третій, велика хустка 88 × 88 на п’ятий.", "photo/kolo-3.webp", "Хустка на бежевому пальті", "h65", .2),
    ("up", "Підвищення", "Нова роль", "Підвищення, перший власний відділ, перший великий клієнт. Хустка, яку носитимуть на зустрічі, — і листівка з вашими словами.", "photo/probudzhennia-2.webp", "Шовкова хустка на плечах", "h44", .1),
    ("team", "Перемога команди", "Закритий проєкт", "Реліз, складний квартал, виграний тендер. Один принт на всю команду — і спільне фото того ж дня.", "img/set-3twilly.webp", "Три твіллі в одній коробці", "tw", .3),
    ("care", "Підтримка", "Коли людині потрібна підтримка", "Одужання, повернення після довгої перерви, народження дитини. Річ для відпочинку — маска для сну або шовкова наволочка.", "img/mask-vpevnenist.webp", "Шовкова маска для сну", "mask", .05),
    ("bye", "Прощання", "Останній день", "Людина йде далі — і забирає з собою добру пам’ять про компанію. Велика хустка або сертифікат, щоб обрала сама.", "photo/mizh-1.webp", "Велика шовкова хустка на голові", "h88", .05),
]

CSS = """
  .path { display: grid; grid-template-columns: repeat(8, 1fr); gap: 0; margin-bottom: 28px; position: relative; }
  .path::before { content: ""; position: absolute; left: 6%; right: 6%; top: 17px; height: 1px; background: var(--ink); opacity: .35; }
  .path button { font: inherit; color: var(--ink2); background: none; border: 0; padding: 0 4px 12px; cursor: pointer; display: grid; justify-items: center; gap: 10px; text-align: center; font-size: .82rem; line-height: 1.25; min-height: 84px; position: relative; }
  .path button::before { content: counter(st); counter-increment: st; width: 34px; height: 34px; border-radius: 50%; border: 1px solid var(--ink); background: var(--bg); display: grid; place-items: center; font-family: var(--display); font-size: 1rem; color: var(--ink); position: relative; z-index: 1; transition: background .2s, color .2s; }
  .path { counter-reset: st; }
  .path button[aria-selected="true"] { color: var(--ink); font-weight: 600; }
  .path button[aria-selected="true"]::before { background: var(--ink); color: var(--bg); }
  .stage { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: clamp(20px, 4vw, 56px); align-items: center; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; }
  .stage img { width: 100%; height: 100%; aspect-ratio: 4 / 3.4; object-fit: cover; object-position: 50% 18%; }
  .stage .in { padding: clamp(20px, 3vw, 40px) clamp(20px, 3vw, 40px) clamp(20px, 3vw, 40px) 0; display: grid; gap: 14px; align-content: center; }
  .stage .in > p { color: var(--ink2); max-width: 34em; }
  .stage .gift { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 14px; padding-top: 14px; border-top: 1px solid var(--line); }
  .stage .gift b { font-family: var(--display); font-weight: 400; font-size: 1.3rem; }
  .stage .gift span { color: var(--ink2); }
  .plan { display: grid; gap: 0; border-top: 1px solid var(--ink); }
  .plan .row { display: grid; grid-template-columns: 28px minmax(0, 1.3fr) 110px minmax(0, 1.6fr) 130px; gap: 14px; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--line); }
  .plan .row.off { opacity: .45; }
  .plan label.n { font-weight: 600; cursor: pointer; }
  .plan input[type=checkbox] { width: 22px; height: 22px; accent-color: var(--accent); margin: 0; cursor: pointer; }
  .plan input[type=number], .plan select, .team input { font: inherit; width: 100%; min-height: 44px; padding: 8px 12px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--card); color: var(--ink); }
  .plan .sum { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
  .plan .hd { font-size: .74rem; letter-spacing: .14em; text-transform: uppercase; color: var(--ink3); font-weight: 600; padding: 10px 0; }
  .team { display: flex; flex-wrap: wrap; align-items: end; gap: 16px 28px; margin-bottom: 26px; }
  .team label { display: grid; gap: 6px; font-weight: 600; width: 200px; }
  .team p { color: var(--ink2); max-width: 36em; font-size: .95rem; }
  .total { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px 28px; padding-top: 24px; }
  .total .fig { display: grid; gap: 2px; }
  .total .fig b { font-family: var(--display); font-weight: 400; font-size: clamp(2rem, 4vw, 3.2rem); line-height: 1; font-variant-numeric: tabular-nums; }
  .total .fig span { color: var(--ink2); font-size: .92rem; }
  @media (max-width: 960px) {
    .path { grid-template-columns: repeat(4, 1fr); row-gap: 14px; } .path::before { display: none; }
    .path button { font-size: .74rem; overflow-wrap: anywhere; hyphens: auto; padding-inline: 2px; }
    .stage { grid-template-columns: 1fr; } .stage .in { padding: 0 20px 24px; }
    .plan .row { grid-template-columns: 28px minmax(0, 1fr) 96px; } .plan .row select { grid-column: 2 / 4; } .plan .row .sum { grid-column: 2 / 4; text-align: left; color: var(--ink2); }
    .plan .hd { display: none; }
  }
"""

def page():
    tabs = "".join(f'<button type="button" role="tab" id="t-{sid}" aria-controls="stage" aria-selected="{"true" if i == 0 else "false"}" data-i="{i}">{short}</button>' for i, (sid, short, *_r) in enumerate(STAGES))
    opts = "".join(f'<option value="{k}">{n} — {b2b.price(p)}</option>' for k, n, p in ITEMS)
    rows = "".join(f'''<div class="row" data-id="{sid}" data-share="{share}">
        <input type="checkbox" id="c-{sid}" {"checked" if sid in ("first", "bday", "years") else ""} aria-label="{short}: враховувати в плані">
        <label class="n" for="c-{sid}">{short}</label>
        <input type="number" min="0" inputmode="numeric" aria-label="{short}: скільки подарунків на рік" data-k="n">
        <select aria-label="{short}: що даруємо" data-k="item" data-def="{item}">{opts}</select>
        <span class="sum num" data-k="sum"></span></div>''' for sid, short, _t, _d, _p, _a, item, share in STAGES)
    data = json.dumps([dict(id=s, title=t, text=d, photo=p, alt=a, item=NAME[i], price=PRICE[i]) for s, _sh, t, d, p, a, i, _x in STAGES], ensure_ascii=False)
    first = STAGES[0]
    body = hero("Для HR і офіс-менеджерів · подарунки всередині компанії", "Подарунки для своїх",
        "Перший день, день народження, п’ять років у компанії, закритий проєкт. Шовкова річ із листівкою від компанії — кожному на відділення Нової пошти або в офіс.<span class=\"m-hide\"> Ви надсилаєте список, ми пакуємо, підписуємо й відправляємо.</span>",
        "Порахувати план на рік", "Вісім нагод", "#path",
        "Зразок — від 1 600 грн у роздріб: <a href=\"https://obiimy.world/khustka-tvilli-shovkova-zolote-svitlo-84x5/\">замовити твіллі →</a>",
        "photo/hratsiia-2.webp", "Шовкова хустка поясом на синьому жакеті", "Від першого дня до п’яти років у компанії", pos="50% 10%", cta1_href="#plan") + facts_html([
        ("8 нагод", "Від першого дня до останнього — увесь шлях людини в компанії"),
        ("700 – 4 400 грн", "Роздрібні ціни каталогу: річ під будь-який бюджет на людину"),
        ("Не лише хустки", "Маски для сну, закладки, наволочки, футболки, сертифікати"),
        ("Листівка", "Привітання вашими словами — у кожному подарунку"),
    ]) + f'''

  <section class="block" id="path"><div class="wrap">
    <div class="head"><p class="eyebrow">Нагоди</p><h2>Шлях людини в компанії</h2><p class="sub">Вісім моментів, коли подарунок від роботодавця запам’ятовується. Оберіть нагоду — покажемо, що зазвичай дарують і скільки це коштує в роздріб.</p></div>
    <div class="path" role="tablist" aria-label="Нагоди для подарунка">{tabs}</div>
    <div class="stage" id="stage" role="tabpanel" aria-labelledby="t-{first[0]}" aria-live="polite">
      {img(first[4], first[5], sizes="(max-width: 960px) 100vw, 45vw")}
      <div class="in"><p class="eyebrow" id="st-k">Нагода 1 / 8</p><h3 id="st-t" style="font-size:clamp(1.5rem,2.4vw,2.1rem)">{first[2]}</h3><p id="st-d">{first[3]}</p>
        <div class="gift"><b id="st-i">{NAME[first[6]]}</b><span id="st-p" class="num">{b2b.price(PRICE[first[6]])} у роздріб</span></div>
        <p style="margin-top:4px"><a class="btn btn-line btn-sm" href="#plan" id="st-add">Додати в план на рік</a></p></div>
    </div>
  </div></section>

  <section class="block alt" id="plan"><div class="wrap">
    <div class="head"><p class="eyebrow">План на рік</p><h2>Скільки це коштує для вашої команди</h2><p class="sub">Вкажіть розмір команди, позначте нагоди й оберіть річ для кожної. Кількість подарунків ми підставили для прикладу — змініть під себе.</p></div>
    <div class="team"><label for="people">Людей у команді<input id="people" type="number" min="1" inputmode="numeric" value="40"></label><p>Суми — за роздрібними цінами obiimy.world. Умови для компанії залежать від кількості подарунків на рік: порахуємо у відповідь на запит.</p></div>
    <div class="plan" id="rows">
      <div class="row hd" aria-hidden="true"><span></span><span>Нагода</span><span>Подарунків на рік</span><span>Що даруємо</span><span style="text-align:right">Сума</span></div>
      {rows}
    </div>
    <div class="total"><div class="fig"><b id="tot" class="num">0 грн</b><span id="tot-s">на рік за роздрібними цінами</span></div>
      <a class="btn btn-gold" href="#request" id="send">Надіслати цей план на розрахунок</a></div>
  </div></section>

  <section class="block" id="all"><div class="wrap">
    <div class="head"><p class="eyebrow">Для всієї команди</p><h2>Не лише шовкові хустки</h2><p class="sub">У команді різні люди. У каталозі Obiimy є речі, які доречно подарувати кожному — і тим, хто хустку не носить.</p></div>
    <div class="grid4">
      <div class="card photo">{img("img/mask-vpevnenist.webp", "Шовкова маска для сну", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">Відпочинок</p><h3>Маска для сну</h3><p>Після відрядження, перед відпусткою, на підтримку.</p><div class="price-row"><span>Роздріб</span><span class="num">2 700 грн</span></div></div></div>
      <div class="card photo">{img("img/sets/bookmark-melodiia.webp", "Шовкова закладка для книги", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">Знак уваги</p><h3>Закладка для книги</h3><p>До корпоративної бібліотеки чи книжкового клубу.</p><div class="price-row"><span>Роздріб</span><span class="num">800 грн</span></div></div></div>
      <div class="card photo">{img("img/sets/tee-men-obiimy.webp", "Чоловіча футболка Obiimy", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">Для всіх</p><h3>Футболка</h3><p>Є жіночі й чоловічі моделі.</p><div class="price-row"><span>Роздріб</span><span class="num">1 700 грн</span></div></div></div>
      <div class="card photo">{img("img/sets/cert-2000.webp", "Подарунковий сертифікат Obiimy", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">На вибір</p><h3>Сертифікат</h3><p>Людина обирає сама протягом трьох місяців. <a href="b2b-certificates">Докладніше →</a></p><div class="price-row"><span>Номінали</span><span class="num">1 000 – 4 000 грн</span></div></div></div>
    </div>
    <p class="note">Потрібна одна річ на всю компанію? Подивіться <a href="b2b-monoprint">«Один принт — уся компанія»</a>. Готові набори — у <a href="b2b-sets">каталозі наборів</a>.</p>
  </div></section>

  <section class="block alt" id="how"><div class="wrap grid2">
    <div><p class="eyebrow">Як це влаштовано</p><h2 style="margin-top:10px">Від вас — список. Решту робимо ми</h2>
      <div class="steps" style="grid-template-columns:1fr;gap:18px;margin-top:22px">
        <div><h3>Нагоди й бюджет</h3><p>Ви обираєте нагоди та суму на один подарунок. Можна почати з однієї — наприклад, із днів народження.</p></div>
        <div><h3>Добірка</h3><p>Пропонуємо речі й принти під кожну нагоду — так, щоб подарунки не повторювались рік у рік.</p></div>
        <div><h3>Список і листівки</h3><p>Один документ: імена, дати, відділення Нової пошти. Текст листівки — ваш, для кожної нагоди свій.</p></div>
        <div><h3>Відправка</h3><p>Пакуємо й відправляємо кожному окремо або однією посилкою в офіс. Після відправки надсилаємо номери накладних.</p></div>
      </div>
    </div>
    <figure>{img("photo/bag-1.webp", "Шовкова твіллі на ручці білої сумки", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
  </div></section>

  <section class="block" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Питання</p><h2>Що питають HR і офіс-менеджери</h2></div>
    <div class="faq">
      <details><summary>Є мінімальна кількість?</summary><p>Фіксованого мінімуму немає. Можна замовити подарунок одній людині — наприклад, до річниці в компанії.</p></details>
      <details><summary>Що подарувати чоловікам?</summary><p>Маску для сну, закладку для книги, шовкову наволочку, футболку або сертифікат. Якщо хочете один подарунок для всіх — сертифікат найпростіший.</p></details>
      <details><summary>Як не помилитися з принтом?</summary><p>Надішліть кілька слів про людину чи команду — запропонуємо два-три принти на вибір. Або подаруйте сертифікат: людина обере сама.</p></details>
      <details><summary>Чи можна відправити кожному додому?</summary><p>Так: кожному на відділення Нової пошти за вашим списком або однією посилкою в офіс. За кордон — за тарифами перевізника.</p></details>
      {b2b.DOCS_FAQ}
      {b2b.BATCH_FAQ}
      <details><summary>Що, якщо людина звільнилась або список змінився?</summary><p>Надішліть оновлений список до наступної відправки — відправимо за актуальним.</p></details>
    </div>
  </div></section>
  {proof_html("Де вже є Obiimy", "Obiimy продається у роздрібних партнерів в Україні та за кордоном, а історію бренду розповідали LIGA.net та INSIDER UA.")}

  <section class="form-block" id="request"><div class="wrap">
    <div class="contact"><p class="eyebrow">Напишіть нам</p><h2>Порахувати подарунки для команди</h2><p>Кілька фактів про компанію — і ми надішлемо добірку та розрахунок. План із калькулятора підставиться в коментар.</p><p class="big"><a href="{PHONE_HREF}">{PHONE}</a></p><p><a href="mailto:{MAIL}">{MAIL}</a> · <a href="{TG}">Telegram @OBIIMY_sales</a></p><p class="show">Шоурум: {SHOWROOM} — шовк можна подивитися й торкнутися наживо.</p></div>
    <div>{form_html("f-team", "Подарунки для команди", [
        ("company", "Компанія", "input", True, {"ph": "Назва компанії", "ac": "organization"}),
        ("name", "Ваше ім’я", "input", True, {"ph": "Як до вас звертатись", "ac": "name"}),
        ("phone", "Телефон", "tel", True, {"ph": "+380", "ac": "tel", "err": "Вкажіть номер телефону"}),
        ("email", "Email", "email", True, {"ph": "для добірки та розрахунку", "ac": "email", "err": "Вкажіть коректний email"}),
        ("people", "Людей у команді", "number", False, {"ph": "наприклад, 40"}),
        ("delivery", "Доставка", "select:Кожному на відділення Нової пошти|В офіс однією посилкою|Комбіновано", False, {}),
        ("payment", "Оплата", "select:Безготівково, ТОВ|Безготівково, ФОП|Карткою", False, {}),
        ("note", "План і коментар", "textarea", False, {"ph": "Нагоди, найближча дата, побажання до принтів…"}),
    ], "Відповідаємо з добіркою та розрахунком.")}</div>
  </div></section>
  <script>
  (function () {{
    var S = {data}, P = {json.dumps(PRICE)}, N = {json.dumps(NAME, ensure_ascii=False)};
    var fmt = function (n) {{ return String(Math.round(n)).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, '\\u00a0') + '\\u00a0грн'; }};
    // path
    var tabs = [].slice.call(document.querySelectorAll('.path button')), cur = 0, im = document.querySelector('#stage img');
    function show(i, focus) {{
      cur = (i + S.length) % S.length; var s = S[cur];
      tabs.forEach(function (t, k) {{ t.setAttribute('aria-selected', k === cur ? 'true' : 'false'); t.tabIndex = k === cur ? 0 : -1; }});
      document.getElementById('stage').setAttribute('aria-labelledby', tabs[cur].id);
      document.getElementById('st-k').textContent = 'Нагода ' + (cur + 1) + ' / ' + S.length;
      document.getElementById('st-t').textContent = s.title; document.getElementById('st-d').textContent = s.text;
      document.getElementById('st-i').textContent = s.item; document.getElementById('st-p').textContent = fmt(s.price) + ' у роздріб';
      im.removeAttribute('srcset'); im.removeAttribute('sizes'); im.src = s.photo; im.alt = s.alt;
      if (focus) tabs[cur].focus();
    }}
    tabs.forEach(function (t, k) {{
      t.addEventListener('click', function () {{ show(k); }});
      t.addEventListener('keydown', function (e) {{ if (e.key === 'ArrowRight') {{ e.preventDefault(); show(cur + 1, true); }} else if (e.key === 'ArrowLeft') {{ e.preventDefault(); show(cur - 1, true); }} }});
    }});
    show(0);
    // plan
    var people = document.getElementById('people'), rows = [].slice.call(document.querySelectorAll('#rows .row[data-id]'));
    function defaults() {{
      var n = Math.max(1, parseInt(people.value, 10) || 0);
      rows.forEach(function (r) {{ var q = r.querySelector('[data-k=n]'); if (!q.dataset.touched) q.value = Math.max(1, Math.round(n * parseFloat(r.dataset.share))); }});
    }}
    function calc() {{
      var total = 0, gifts = 0;
      rows.forEach(function (r) {{
        var on = r.querySelector('input[type=checkbox]').checked, q = Math.max(0, parseInt(r.querySelector('[data-k=n]').value, 10) || 0), k = r.querySelector('select').value;
        r.classList.toggle('off', !on);
        var s = q * P[k]; r.querySelector('[data-k=sum]').textContent = on ? fmt(s) : '—';
        if (on) {{ total += s; gifts += q; }}
      }});
      document.getElementById('tot').textContent = fmt(total);
      document.getElementById('tot-s').textContent = gifts + ' подарунків на рік · за роздрібними цінами';
    }}
    rows.forEach(function (r) {{
      var sel = r.querySelector('select'); sel.value = sel.dataset.def;
      r.querySelector('[data-k=n]').addEventListener('input', function () {{ this.dataset.touched = '1'; calc(); }});
      sel.addEventListener('change', calc); r.querySelector('input[type=checkbox]').addEventListener('change', calc);
    }});
    people.addEventListener('input', function () {{ defaults(); calc(); }});
    defaults(); calc();
    document.getElementById('st-add').addEventListener('click', function () {{
      var r = rows[cur]; r.querySelector('input[type=checkbox]').checked = true; calc();
    }});
    document.getElementById('send').addEventListener('click', function () {{
      var lines = ['План на рік (роздрібні ціни):'];
      rows.forEach(function (r) {{
        if (!r.querySelector('input[type=checkbox]').checked) return;
        var q = parseInt(r.querySelector('[data-k=n]').value, 10) || 0, k = r.querySelector('select').value;
        lines.push('— ' + r.querySelector('label.n').textContent + ': ' + q + ' × ' + N[k] + ' = ' + fmt(q * P[k]).replace(/\\u00a0/g, ' '));
      }});
      lines.push('Разом: ' + document.getElementById('tot').textContent.replace(/\\u00a0/g, ' '));
      var f = document.getElementById('f-team'); f.querySelector('[name=note]').value = lines.join('\\n'); f.querySelector('[name=people]').value = people.value;
    }});
  }})();
  </script>'''
    return dict(slug="b2b-team", skin="form", title="Подарунки для команди — Obiimy для HR і офіс-менеджерів",
                desc="Подарунки співробітникам від компанії: перший день, день народження, річниця в компанії, закритий проєкт. Шовк, маски для сну, сертифікати від 700 грн; відправка кожному або в офіс.",
                og="photo/hratsiia-2.webp", nav=[("Нагоди", "path"), ("План на рік", "plan"), ("Для всіх", "all"), ("Як це працює", "how"), ("Питання", "faq"), ("Контакт", "request")],
                cta="Запит", sticky="Подарунки для команди · від 700 грн", body=body)

if __name__ == "__main__":
    b2b.CSS += CSS
    b2b.build_all([page])
