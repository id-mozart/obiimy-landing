#!/usr/bin/env python3
"""B2B set landings: a catalogue of corporate sets (Maison), one print for the whole company (Journal),
and a scroll-driven CSS 3D unboxing (dark art template src/b2b-unboxing.html)."""
import importlib.util, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
_spec = importlib.util.spec_from_file_location("b2b", ROOT / "build-b2b.py")
b2b = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(b2b)
img, typo, hero, facts_html, proof_html, form_html, shell = b2b.img, b2b.typo, b2b.hero, b2b.facts_html, b2b.proof_html, b2b.form_html, b2b.shell
PHONE, PHONE_HREF, MAIL, DOCS_FAQ, BATCH_FAQ = b2b.PHONE, b2b.PHONE_HREF, b2b.MAIL, b2b.DOCS_FAQ, b2b.BATCH_FAQ
_x = importlib.util.spec_from_file_location("x", ROOT / "build-b2b-extra.py"); X = importlib.util.module_from_spec(_x); _x.loader.exec_module(X)
BASE_FIELDS, PAY, contact = X.BASE_FIELDS, X.PAY, X.contact
PROOF = proof_html("Де вже є Obiimy", "Obiimy продається у роздрібних партнерів в Україні та за кордоном, а історію бренду розповідали LIGA.net та INSIDER UA.")

def price(n): return f"{n:,}".replace(",", " ") + " грн"

# ---------- catalogue items (verified retail prices) ----------
ITEM = {
    "scr":  ("Резинка для волосся", 700,  "img/scrunchie-energiia.webp"),
    "tw":   ("Твіллі 84 × 5", 1600, "img/twilly-zolote.webp"),
    "h44":  ("Хустка 44 × 44", 1600, "img/melodiia.webp"),
    "h65":  ("Хустка 65 × 65", 3200, "img/tysha-sertsia.webp"),
    "d65":  ("Двостороння 65 × 65", 4800, "img/probudzhennia.webp"),
    "h88":  ("Шаль 88 × 88", 4400, "img/kolo-sontsia.webp"),
    "mask": ("Маска для сну", 2700, "img/mask-vpevnenist.webp"),
}
# existing sets on obiimy.world (price from the site) and proposed combinations (sum of retail prices, «під запит»)
SETS = [
    dict(id="first-day", name="«Перший день»", who="Новим співробітникам · welcome-box", items=["scr"], card=True, price=700, kind="Під запит",
         line="Резинка у фірмовій коробочці й листівка з привітанням від команди. Маленький жест, який запам’ятовується з першого дня."),
    dict(id="prystrast", name="Набір «Пристрасть»", who="Усій команді", items=["tw", "scr"], price=2200, kind="Каталог",
         line="Твіллі й резинка в одному принті — набір із каталогу Obiimy. Універсальний подарунок, який не залежить від розміру."),
    dict(id="natkhnennia", name="Набір «Натхнення»", who="Ключовим людям", photo="img/set-natkhnennia.webp", items=["tw", "h44"], price=3200, kind="Каталог",
         line="Твіллі й хустка 44 × 44 в одному принті, у жовтій коробці з тонким папером — набір із каталогу."),
    dict(id="son", name="Набір для сну «Піднесення»", who="Wellbeing-програмам", photo="img/set-mask.webp", items=["mask"], price=3600, kind="Каталог",
         line="Шовкова маска та аксесуари для сну в одній коробці — подарунок про відпочинок, а не про роботу."),
    dict(id="song", name="«Співоча душа»", who="Подарунок із сенсом", items=["h65"], card=True, price=3200, kind="Під запит",
         line="Хустка 65 × 65 «Тиша серця» з колекції, частина коштів від якої йде на гніздівлі для сиворакші, і листівка з історією колекції."),
    dict(id="three", name="Три твіллі", who="Партнерам", photo="img/set-3twilly.webp", items=["tw", "tw", "tw"], price=4800, kind="Каталог",
         line="Три стрічки в одній коробці — для партнерів, які носять шовк по-різному: на сумці, у волоссі, на зап’ясті."),
    dict(id="trip", name="«Відрядження»", who="Тим, хто багато літає", items=["mask", "tw", "scr"], price=5000, kind="Під запит",
         line="Маска для сну, твіллі й резинка — усе, що займає мало місця у валізі й робить готельний номер своїм."),
    dict(id="mono", name="«Монопринт»", who="Керівникам команд", items=["h65", "tw", "scr"], price=5500, kind="Під запит",
         line="Хустка 65 × 65, твіллі й резинка в одному принті — набір, який виглядає як колекція, а не як збірка."),
    dict(id="head", name="«Керівнику»", who="Топменеджменту й VIP-клієнтам", items=["h88", "tw"], price=6000, kind="Під запит",
         line="Шаль 88 × 88 і твіллі в одній коробці — найбільший формат Obiimy і найменший, поруч."),
]

POS = {1: [(50, 44, 58, -3)], 2: [(35, 42, 46, -7), (66, 50, 46, 6)], 3: [(28, 40, 40, -9), (70, 38, 40, 7), (50, 58, 40, -2)]}

def setviz(s, sizes="(max-width: 640px) 100vw, 33vw"):
    if s.get("photo"):
        inner = f'<span class="ph">{img(s["photo"], s["name"], sizes=sizes)}</span>'
    else:
        items = s["items"]; pos = POS[len(items)]
        inner = "".join(f'<span class="it" style="left:{x}%;top:{y}%;width:{w}%;transform:translate(-50%,-50%) rotate({r}deg)">{img(ITEM[k][2], ITEM[k][0], sizes="200px")}</span>' for k, (x, y, w, r) in zip(items, pos))
        if s.get("card"):
            inner += '<span class="cardlet">Дякуємо, що цього року ви були поруч.<small>— від вашої компанії</small></span>'
    return f'<figure class="setviz" aria-label="{s["name"]}"><span class="box"><img src="brand/logo-ink-480.webp" alt="" width="94" height="20"></span>{inner}</figure>'

SET_CSS = """
<style>
  .setviz { position: relative; margin: 0; aspect-ratio: 4 / 3; overflow: hidden; border-radius: var(--radius); background: radial-gradient(90% 80% at 50% 30%, var(--card), var(--bg2)); }
  .setviz .box { position: absolute; left: 12%; right: 12%; bottom: -8%; height: 34%; background: linear-gradient(180deg, #F7C928, #EDB400); border-radius: 4px; box-shadow: 0 -10px 30px -12px rgba(60,40,0,.35), inset 0 10px 14px rgba(120,80,0,.18); display: grid; place-items: center; }
  .setviz .box img { height: 16px; width: auto; opacity: .85; margin-top: -8%; }
  .setviz .it { position: absolute; aspect-ratio: 1; background: #fff; border-radius: 6px; box-shadow: 0 18px 30px -16px rgba(0,0,0,.45); overflow: hidden; }
  .setviz .it img { width: 100%; height: 100%; object-fit: contain; padding: 6%; }
  .setviz .ph { position: absolute; inset: 6% 14% 16% 14%; border-radius: 6px; overflow: hidden; box-shadow: 0 18px 30px -16px rgba(0,0,0,.45); background: #fff; }
  .setviz .ph img { width: 100%; height: 100%; object-fit: cover; }
  .setviz .cardlet { position: absolute; right: 8%; top: 12%; width: 38%; background: #F6F1E7; color: #231E2A; font-family: var(--display); font-style: italic; font-size: .82rem; line-height: 1.25; padding: 10px 12px; border-radius: 2px; transform: rotate(5deg); box-shadow: 0 14px 24px -14px rgba(0,0,0,.45); display: grid; gap: 6px; }
  .setviz .cardlet small { font-family: var(--body); font-style: normal; font-size: .62rem; letter-spacing: .12em; text-transform: uppercase; color: #6B6477; }
  .sets { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }
  .set { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; display: grid; grid-template-rows: auto 1fr; }
  .set[hidden] { display: none !important; }
  .set .in { padding: 18px 20px 20px; display: grid; gap: 8px; align-content: start; }
  .set .who { font-size: .76rem; letter-spacing: .16em; text-transform: uppercase; color: var(--ink3); font-weight: 600; }
  .set h3 { font-size: 1.35rem; }
  .set .comp { font-size: .88rem; color: var(--ink2); }
  .set .line { font-size: .92rem; color: var(--ink2); }
  .set .foot { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: 6px; padding-top: 12px; border-top: 1px solid var(--line); }
  .set .foot b { font-family: var(--display); font-weight: 400; font-size: 1.3rem; }
  .set .tag { font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; padding: 3px 8px; border-radius: 999px; border: 1px solid var(--line); color: var(--ink2); }
  .set .tag.cat { border-color: #8A6500; color: #7A5900; }
  .dark .set .tag.cat { border-color: var(--gold); color: var(--gold); }
  .set .pick { margin-top: 8px; }
  .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 22px; }
  .chips button { all: unset; cursor: pointer; font-size: .86rem; padding: 12px 16px; border: 1px solid var(--line); border-radius: 999px; color: var(--ink2); }
  .chips button[aria-pressed="true"] { border-color: var(--ink); color: var(--ink); background: color-mix(in srgb, var(--ink) 6%, transparent); }
  .chips button:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }
  @media (max-width: 960px) { .sets { grid-template-columns: 1fr 1fr; } }
  @media (max-width: 640px) { .sets { grid-template-columns: 1fr; } }
</style>"""

# ---------------------------------------------------------------- A. catalogue of sets (Maison)
def sets_catalogue():
    cards = []
    for s in SETS:
        comp = " + ".join(ITEM[k][0] for k in s["items"]) + (" + листівка" if s.get("card") else "")
        cards.append(f'''
      <article class="set" data-price="{s["price"]}" id="set-{s["id"]}">
        {setviz(s)}
        <div class="in"><span class="who">{s["who"]}</span><h3>{s["name"]}</h3><p class="comp">{comp}</p><p class="line">{s["line"]}</p>
          <div class="foot"><b class="num">{price(s["price"])}</b><span class="tag{" cat" if s["kind"] == "Каталог" else ""}">{s["kind"]}</span></div>
          <button class="btn btn-line btn-sm pick" type="button" data-set="{s["name"]} — {price(s["price"])}">Запросити цей набір</button></div>
      </article>''')
    hero_fig = '<figure class="setsfig">' + setviz(SETS[7], sizes="(max-width: 960px) 100vw, 50vw") + '</figure>'
    body = SET_CSS + hero("Корпоративні набори · Новий рік і не тільки", "Дев’ять наборів — від welcome-box до подарунка керівнику",
        "Готові комбінації з шовку Obiimy у фірмовій жовтій коробці: для всієї команди, ключових людей, партнерів і тих, хто багато подорожує.<span class=\"m-hide\"> Оберіть набір — ми повернемось із розрахунком на ваш тираж.</span>",
        "Обрати набір", "Зібрати свій у 3D", "b2b-atelier", "Від 700 до 6 000 грн за роздрібними цінами.", "photo/box-dots.jpg", "", "", figure=hero_fig) + facts_html([
        ("9 наборів", "Чотири з каталогу Obiimy, п’ять — комбінації під запит"),
        ("700 – 6 000 грн", "Роздрібні ціни; для комбінацій — сума цін речей"),
        ("Жовта коробка", "Кожен набір у фірмовій коробці з листівкою"),
        ("Один принт", "Або різні — узгоджуємо в розрахунку"),
    ]) + f'''

  <section class="block" id="sets"><div class="wrap">
    <div class="head"><p class="eyebrow">Набори</p><h2>Оберіть за бюджетом на людину</h2><p class="sub">«Каталог» — набір, який уже є на obiimy.world. «Під запит» — наша комбінація з речей каталогу: склад, принти й ціну на тираж підтвердимо в розрахунку.</p></div>
    <div class="chips" id="chips" role="group" aria-label="Бюджет на людину"><button type="button" data-b="0" aria-pressed="true">Усі</button><button type="button" data-b="1000">до 1 000 грн</button><button type="button" data-b="3500">до 3 500 грн</button><button type="button" data-b="5000">до 5 000 грн</button><button type="button" data-b="99999">понад 5 000 грн</button></div>
    <div class="sets" id="setsGrid">{"".join(cards)}</div>
    <p class="note">Не знайшли свій? <a href="b2b-atelier" style="font-weight:600">Зберіть набір у 3D-конструкторі →</a> або <a href="b2b-monoprint" style="font-weight:600">один принт на всю компанію →</a></p>
  </div></section>

  <section class="block alt" id="personal"><div class="wrap grid2">
    <figure>{img("photo/box-gold.jpg", "Набір у фірмовій жовтій коробці", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
    <div><p class="eyebrow">Що в кожному наборі</p><h2 style="margin-top:10px">Коробка, папір, листівка</h2>
      <div class="faq" style="margin-top:22px">
        <details open><summary>Фірмова жовта коробка</summary><p>Кожен набір — у жовтій коробці Obiimy з тонким папером. Її впізнають ще до того, як відкриють.</p></details>
        <details><summary>Листівка від компанії</summary><p>Ваш текст привітання в кожній коробці; підпис від руки — за бажанням.</p></details>
        <details><summary>Один принт чи різні</summary><p>Один принт на всіх читається як подарунок від команди; різні — як особистий кожному. Узгоджуємо в розрахунку.</p></details>
        <details><summary>Доставка</summary><p>В офіс однією посилкою або кожному адресату на відділення Нової пошти.</p></details>
      </div>
    </div>
  </div></section>

  <section class="block" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Питання</p><h2>Що зазвичай питають</h2></div>
    <div class="faq">
      <details><summary>Чим «Каталог» відрізняється від «Під запит»?</summary><p>Набори «Каталог» уже продаються на obiimy.world. «Під запит» — наші комбінації з речей каталогу: наявність принтів і ціну на тираж підтвердимо в розрахунку.</p></details>
      <details><summary>Чи можна змінити склад набору?</summary><p>Так — замінити річ, принт або додати позицію. Найзручніше зібрати свій варіант у <a href="b2b-atelier">3D-конструкторі</a>.</p></details>
      <details><summary>Мінімальний тираж?</summary><p>Фіксованого мінімуму немає — обговорюємо кожен запит окремо.</p></details>
      {DOCS_FAQ}
      {BATCH_FAQ}
    </div>
  </div></section>
  {PROOF}

  <section class="form-block alt" id="request"><div class="wrap">
    {contact("Запросити набір", "Оберіть набір і кількість — повернемось із розрахунком, принтами та графіком.")}
    <div>{form_html("f-sets", "Корпоративні набори", BASE_FIELDS + [
        ("set", "Набір", "select:" + "|".join(f'{s["name"]} — {price(s["price"])}' for s in SETS) + "|Свій варіант", False, {"full": True}),
        ("qty", "Кількість наборів", "number", False, {"ph": "наприклад, 30"}),
        ("deadline", "Коли потрібно", "select:До 10 грудня|До 20 грудня|Після свят|Інша дата", False, {}),
        PAY,
        ("note", "Коментар", "textarea", False, {"ph": "Нагода, принти, текст листівки…"}),
    ], "")}</div>
  </div></section>
  <script>
  (function () {{
    var chips = document.getElementById('chips'), cards = [].slice.call(document.querySelectorAll('.set'));
    chips.querySelectorAll('button').forEach(function (b) {{ b.addEventListener('click', function () {{
      var v = +b.dataset.b; chips.querySelectorAll('button').forEach(function (x) {{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }});
      cards.forEach(function (c) {{ var p = +c.dataset.price; c.hidden = v === 0 ? false : (v === 99999 ? p <= 5000 : p > v); }});
    }}); }});
    document.querySelectorAll('.set .pick').forEach(function (b) {{ b.addEventListener('click', function () {{
      var sel = document.querySelector('#f-sets [name="set"]'); for (var i = 0; i < sel.options.length; i++) if (sel.options[i].text === b.dataset.set) sel.selectedIndex = i;
      document.getElementById('request').scrollIntoView({{ behavior: 'smooth' }}); setTimeout(function () {{ var q = document.querySelector('#f-sets [name="qty"]'); if (q) q.focus({{ preventScroll: true }}); }}, 600);
    }}); }});
  }})();
  </script>'''
    return dict(slug="b2b-sets", skin="maison", title="Корпоративні подарункові набори — Obiimy",
        desc="Дев’ять корпоративних наборів із шовку Obiimy: від welcome-box за 700 грн до подарунка керівнику за 6 000 грн. Жовта коробка, листівка від компанії, доставка кожному адресату.",
        og="photo/box-dots.jpg", nav=[("Набори", "sets"), ("Що всередині", "personal"), ("Питання", "faq"), ("Контакт", "request")],
        cta="Запит", sticky="Корпоративні набори · від 700 грн", body=body)


# ---------------------------------------------------------------- B. one print for the whole company (Journal)
def _states():
    src = (ROOT / "build.py").read_text(); ns = {}
    exec(src[src.index("STATES = ["):src.index("GARDEN = ")], {}, ns)
    return ns["STATES"]

def monoprint():
    st = _states()
    tiers = [
        ("team", "Уся команда", "Твіллі 84 × 5", 1600, 30, "tw"),
        ("key", "Ключові люди", "Хустка 65 × 65", 3200, 10, "k65"),
        ("lead", "Керівники й партнери", "Шаль 88 × 88", 4400, 3, "k88"),
        ("new", "Нові співробітники", "Резинка у коробочці", 700, 0, "scr"),
    ]
    sw = "".join(f'<button type="button" data-i="{i}" aria-label="Принт «{s["name"]}»" aria-pressed="{"true" if i == 2 else "false"}"><img src="tex/{s["id"]}-160.webp" alt="" width="80" height="80" loading="lazy"></button>' for i, s in enumerate(st))
    tier_html = "".join(f'''
      <div class="tier" data-k="{k}" data-p="{p}" data-fmt="{fmt}">
        <div class="viz v-{fmt}"><span class="tex"></span></div>
        <div class="in"><p class="who">{who}</p><h3>{name}</h3><p class="catline"></p>
          <div class="row"><label>Кількість<input type="number" min="0" max="5000" value="{q}" inputmode="numeric" aria-label="{who}: кількість"></label><b class="num sum"></b></div></div>
      </div>''' for k, who, name, p, q, fmt in tiers)
    css = """
<style>
  .mp-swatches { display: grid; grid-template-columns: repeat(9, minmax(0, 1fr)); gap: 10px; max-width: 760px; }
  .mp-swatches button { all: unset; cursor: pointer; aspect-ratio: 1; border-radius: 50%; overflow: hidden; border: 2px solid transparent; box-shadow: 0 0 0 1px var(--line); }
  .mp-swatches button img { width: 100%; height: 100%; object-fit: cover; transform: scale(1.3); }
  .mp-swatches button[aria-pressed="true"] { border-color: var(--ink); }
  .mp-swatches button:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }
  .mp-name { margin-top: 16px; font-family: var(--display); font-size: 1.6rem; }
  .mp-line { color: var(--ink2); max-width: 44em; margin-top: 4px; }
  .tiers { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; margin-top: 30px; }
  .tier { background: var(--card); border: 1px solid var(--line); display: grid; grid-template-rows: auto 1fr; }
  .tier .viz { position: relative; aspect-ratio: 1; background: var(--bg2); display: grid; place-items: center; overflow: hidden; }
  .tier .tex { display: block; background-size: cover; background-position: center; box-shadow: 0 20px 30px -18px rgba(0,0,0,.45); transition: background-image .3s ease; }
  .v-k65 .tex { width: 64%; aspect-ratio: 1; transform: rotate(-6deg); }
  .v-k88 .tex { width: 78%; aspect-ratio: 1; transform: rotate(4deg); }
  .v-tw .tex { width: 90%; height: 13%; transform: rotate(-24deg); border-radius: 2px; background-size: auto 100%; background-repeat: repeat-x; }
  .v-scr .tex { width: 52%; aspect-ratio: 1; border-radius: 50%; -webkit-mask-image: radial-gradient(circle, transparent 34%, #000 35%, #000 69%, transparent 70%); mask-image: radial-gradient(circle, transparent 34%, #000 35%, #000 69%, transparent 70%); }
  .tier .in { padding: 16px 18px 18px; display: grid; gap: 6px; align-content: start; }
  .tier .who { font-size: .76rem; letter-spacing: .16em; text-transform: uppercase; color: var(--ink3); font-weight: 600; }
  .tier h3 { font-size: 1.25rem; }
  .tier .catline { font-size: .82rem; color: var(--ink2); min-height: 2.4em; }
  .tier .row { display: flex; align-items: end; justify-content: space-between; gap: 10px; border-top: 1px solid var(--line); padding-top: 12px; margin-top: 4px; }
  .tier label { display: grid; gap: 4px; font-size: .78rem; color: var(--ink2); }
  .tier input { font: inherit; width: 96px; min-height: 44px; padding: 8px 10px; border: 1px solid var(--line); background: var(--bg); color: var(--ink); }
  .tier .sum { font-family: var(--display); font-weight: 400; font-size: 1.15rem; }
  .mp-total { margin-top: 26px; display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px 22px; border-top: 1px solid var(--ink); padding-top: 18px; }
  .mp-total b { font-family: var(--display); font-weight: 400; font-size: 2.2rem; }
  .mp-total span { color: var(--ink2); font-size: .9rem; }
  @media (max-width: 960px) { .tiers { grid-template-columns: 1fr 1fr; } .mp-swatches { grid-template-columns: repeat(5, minmax(0, 1fr)); } }
  @media (max-width: 640px) { .tier .viz { aspect-ratio: 4 / 3; } }
</style>"""
    hero_fig = f'<figure class="mphero" style="margin:0;position:relative;aspect-ratio:4/5;overflow:hidden;border-radius:var(--radius)">{img("photo/paris-green.jpg", "Шовкова хустка на жакеті", sizes="(max-width: 960px) 100vw, 50vw", lazy=False, eager_priority=True)}<div class="tag">Один принт на всіх читається як подарунок від команди</div></figure>'
    body = css + hero("Монопринт · корпоративні подарунки", "Один принт — уся компанія",
        "Оберіть принт, і він стане подарунком для кожного рівня: твіллі — команді, хустка — ключовим людям, шаль — керівникам, резинка — новим співробітникам.<span class=\"m-hide\"> Разом це виглядає як колекція вашої компанії, а не як набір випадкових подарунків.</span>",
        "Обрати принт", "Готові набори", "b2b-sets", "Роздрібні ціни від 700 до 4 400 грн за річ.", "photo/paris-green.jpg", "", "", pos="50% 14%", figure=hero_fig) + facts_html([
        ("9 принтів", "Авторські картини художниці Світлани Сніжко"),
        ("4 рівні", "Команда, ключові люди, керівники, нові співробітники"),
        ("Одна історія", "Той самий принт у різних форматах і на різних людях"),
        ("Розрахунок", "Кількість по рівнях — і одразу сума за роздрібом"),
    ]) + f'''

  <section class="block" id="print"><div class="wrap">
    <div class="head"><p class="eyebrow">Крок 1 · Принт</p><h2>Оберіть принт компанії</h2><p class="sub">Принт одразу з’явиться на всіх рівнях подарунків нижче. Формат, у якому принт є в каталозі, позначено; інші — під запит.</p></div>
    <div class="mp-swatches" id="mpSw" role="group" aria-label="Принти">{sw}</div>
    <p class="mp-name" id="mpName"></p><p class="mp-line" id="mpLine"></p>
  </div></section>

  <section class="block alt" id="tiers"><div class="wrap">
    <div class="head"><p class="eyebrow">Крок 2 · Рівні</p><h2>Хто що отримує</h2><p class="sub">Змініть кількість — сума рахується за роздрібними цінами; умови для тиражу надішлемо в розрахунку.</p></div>
    <div class="tiers" id="tiersGrid">{tier_html}</div>
    <div class="mp-total"><b class="num" id="mpTotal"></b><span id="mpPeople"></span><a class="btn btn-gold" href="#request" id="mpSend">Надіслати розрахунок</a></div>
  </div></section>

  <section class="block" id="why"><div class="wrap grid2">
    <div><p class="eyebrow">Чому один принт</p><h2 style="margin-top:10px">Колекція вашої компанії</h2>
      <div class="faq" style="margin-top:22px">
        <details open><summary>Видно, що це від команди</summary><p>Коли в офісі, на конференції чи на фото один принт — подарунок читається як спільний, а не випадковий.</p></details>
        <details><summary>Різні формати — різні люди</summary><p>Твіллі носять на сумці чи в волоссі, хустку — на шиї, шаль — на плечах. Один принт працює на кожного.</p></details>
        <details><summary>Історія принту</summary><p>Кожен принт — авторська картина. У листівці можна розповісти, чому обрали саме його.</p></details>
      </div>
    </div>
    <figure>{img("photo/paris-belt.jpg", "Твіллі як пояс на тренчі", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
  </div></section>

  <section class="block alt" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Питання</p><h2>Що зазвичай питають</h2></div>
    <div class="faq">
      <details><summary>Чи є кожен принт у кожному форматі?</summary><p>Ні — у каталозі кожен принт має свої формати. Інші формати того ж принта — під запит: наявність і терміни підтвердимо в розрахунку.</p></details>
      <details><summary>Чи можна два принти — для жінок і чоловіків?</summary><p>Так, додайте в коментарі — підберемо пару принтів, які поєднуються.</p></details>
      {DOCS_FAQ}
      {BATCH_FAQ}
    </div>
  </div></section>
  {PROOF}

  <section class="form-block" id="request"><div class="wrap">
    {contact("Надіслати розрахунок", "Розрахунок із калькулятора вже в запиті — повернемось із наявністю принту та цінами на тираж.")}
    <div>{form_html("f-mono", "Монопринт для компанії", BASE_FIELDS + [
        ("deadline", "Коли потрібно", "select:До 10 грудня|До 20 грудня|Після свят|Інша дата", False, {}),
        PAY,
        ("note", "Коментар", "textarea", False, {"ph": "Нагода, текст листівки, побажання…"}),
    ], "").replace('<div class="actions">', '<input type="hidden" name="config" data-label="Розрахунок"><div class="actions">', 1)}</div>
  </div></section>
  <script>
  (function () {{
    var ST = {json.dumps([dict(id=s["id"], name=s["name"], line=s["line"], size=s["size"]) for s in st], ensure_ascii=False)}, cur = 2;
    function cat(s) {{ var z = s.size, two = z.indexOf('двосторон') >= 0; if (z.indexOf('88') === 0) return 'k88'; if (z.indexOf('44') === 0) return two ? 'd44' : 'p44'; return two ? 'd65' : 'k65'; }}
    function fmt(n) {{ return String(n).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, '\\u202f') + '\\u00a0грн'; }}
    var tiers = [].slice.call(document.querySelectorAll('.tier'));
    function render() {{
      var s = ST[cur], c = cat(s), total = 0, people = 0, lines = [];
      document.getElementById('mpName').textContent = '«' + s.name + '»'; document.getElementById('mpLine').textContent = s.line + ' У каталозі: ' + s.size.replace(' см', '') + '.';
      document.querySelectorAll('#mpSw button').forEach(function (b, i) {{ b.setAttribute('aria-pressed', i === cur ? 'true' : 'false'); }});
      tiers.forEach(function (t) {{
        var f = t.dataset.fmt, p = +t.dataset.p, q = Math.max(0, +t.querySelector('input').value || 0);
        t.querySelector('.tex').style.backgroundImage = 'url(tex/' + s.id + (f === 'tw' ? '-strip' : '') + '.jpg)';
        t.querySelector('.catline').textContent = f === c ? 'Каталог — принт є в цьому форматі' : 'Під запит — цей формат принта підтвердимо';
        t.querySelector('.sum').textContent = fmt(p * q); total += p * q; people += q;
        if (q) lines.push(q + ' × ' + t.querySelector('h3').textContent + ' (' + t.querySelector('.who').textContent + ')');
      }});
      document.getElementById('mpTotal').textContent = fmt(total);
      document.getElementById('mpPeople').textContent = people + ' подарунків · за роздрібними цінами — верхня межа';
      var h = document.querySelector('#f-mono [name="config"]'); if (h) h.value = 'Принт «' + s.name + '»: ' + lines.join('; ') + '. Орієнтир: ' + fmt(total) + '.';
    }}
    document.querySelectorAll('#mpSw button').forEach(function (b) {{ b.addEventListener('click', function () {{ cur = +b.dataset.i; render(); }}); }});
    tiers.forEach(function (t) {{ t.querySelector('input').addEventListener('input', render); }});
    render();
  }})();
  </script>'''
    return dict(slug="b2b-monoprint", skin="journal", title="Один принт на всю компанію — корпоративні подарунки Obiimy",
        desc="Оберіть один принт Obiimy для всієї компанії: твіллі команді, хустка ключовим людям, шаль керівникам, резинка новим співробітникам. Калькулятор тиражу за роздрібними цінами.",
        og="photo/paris-green.jpg", nav=[("Принт", "print"), ("Рівні", "tiers"), ("Чому один принт", "why"), ("Питання", "faq"), ("Контакт", "request")],
        cta="Запит", sticky="Один принт — уся компанія", body=body)


# ---------------------------------------------------------------- C. unboxing (dark art template)
def unboxing():
    tpl = (ROOT / "b2b-unboxing.html").read_text()
    form = form_html("f-unbox", "Набір із розпаковки", BASE_FIELDS + [
        ("set", "Набір", "select:«Перший день» — 700 грн|«Відрядження» — 5 000 грн|«Керівнику» — 6 000 грн|«Співоча душа» — 3 200 грн|Інший", False, {"full": True}),
        ("qty", "Кількість наборів", "number", False, {"ph": "наприклад, 30"}),
        PAY,
        ("note", "Коментар", "textarea", False, {"ph": "Нагода, принти, текст листівки…"}),
    ], "")
    return typo(tpl.replace("<!--FORM-->", form))


if __name__ == "__main__":
    b2b.build_all([sets_catalogue, monoprint])
    h = unboxing(); (OUT / "b2b-unboxing.html").write_text(h); print("b2b-unboxing", len(h) // 1024, "KB")
