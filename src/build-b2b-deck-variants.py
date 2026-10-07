#!/usr/bin/env python3
"""Two more corporate landings in the deck's style (paper, Playfair, gold captions on photographs, the yellow band, SOLO on black)
with their own logic rather than the deck's page order — built on the helpers and CSS of build-b2b-deck.py:
  b2b-deck-budget — the HR's way in: three shelves by budget per person, the mixed team, what is in the price, steps, FAQ;
  b2b-deck-story  — the editorial way in: one frame to the edge, «one thing — many looks», three ways companies give, SOLO.
Facts and prices: review/SITE-FACTS.md (retail, obiimy.world); nothing promises a discount, a deadline or a minimum."""
import importlib.util, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
D = load("build-b2b-deck")
deck, main, team, b2b, img, typo, money, tile, cutimg = D.deck, D.main, D.team, D.b2b, D.img, D.typo, D.money, D.tile, D.cutimg
shop = main.shop

# ── shared pieces ─────────────────────────────────────────────────────────────────────────────────────────────────
def request(pid):
    return main.with_qr(team.request_section(pid, "Подарунки для команди", "Зв’яжіться з нами — <i>разом підберемо все для вашої команди</i>",
                                             "Нагода, кількість людей і дата вручення — цього досить для першого листа. У відповідь надішлемо добірку з фото й розрахунок.", "top", corp=True)) + team.script(pid, D.CHIPS_JS + STRIP_JS)
def trust():
    F = ["100% натуральний шовк", "Виготовлено в Україні", "Авторські принти Світлани Сніжко", "У INTERTOP і UFD London", "Шоурум у Києві"]
    return '<section class="dq-trust"><div class="wrap">' + "".join(f"<span>{x}</span>" for x in F) + "</div></section>"
def chips(nav): return '<nav class="dk-chips" aria-label="Розділи сторінки">' + "".join(f'<a href="#{h}">{t}</a>' for t, h in nav) + '</nav>'
def item(name, price, f, pos, kind="photo", zoom=1.0):
    """A thing on a shelf: a photograph with the gold caption, or a cut-out on black with the same gold caption."""
    if kind == "cut":
        return f'<figure class="dq-cut"><div>{img(f, name, sizes="(max-width: 640px) 50vw, 25vw")}</div><figcaption><i>{name}</i><span>{price}</span></figcaption></figure>'
    return tile(f, pos, name, price, zoom=zoom, sz="(max-width: 640px) 50vw, (max-width: 1100px) 33vw, 25vw")

# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# A · by budget
SHELVES = [   # every shelf holds only what its heading says (audit 07.10)
    ("До 1 000 грн", "Знак уваги на всю команду", "Маленькі речі з того самого шовку — або кільце чи сертифікат. Один принт на всіх або кожному свій.",
     [("Кільце для хустки Gold", "450 грн", "photo/site/ring-zoloto-01.jpg", "50% 42%", "photo", 1.5), ("Резинка", "700 грн", "photo/solo/flirt-scr-3.webp", "38% 50%", "photo"),
      ("Закладка для книги", "800 грн", "photo/site/bookmark-melodiia-dvokh-01.jpg", "55% 30%", "photo"), ("Сертифікат", "1 000 грн", "img/cert-card.png", "50% 50%", "photo")]),
    ("1 600 – 2 700 грн", "Подарунок, який носять", "Хустка 44 × 44 — їй на шию, йому в кишеню піджака; твіллі — у волосся чи на сумку; маска для сну — тим, хто аксесуарів не носить.",
     [("Хустка 44 × 44", "1 600 грн", "photo/site/khustka-potsilunok-sontsia-44x44-02.jpg", "50% 0%", "photo"), ("Твіллі", "1 600 грн", "photo/solo/krok-tw-2.webp", "50% 30%", "photo"),
      ("Твіллі + резинка в коробці", "від 2 200 грн", "img/cut/box-twscr-smilyvist.webp", "", "cut"), ("Маска для сну", "від 2 700 грн", "photo/site/mask-vpevnenist-04.jpg", "50% 0%", "photo")]),
    ("Від 3 000 грн", "Ключовим людям — у коробці", "Набори в святковій коробці та великі хустки. Підберемо набір із наявних речей; власний принт — за запитом.",
     [("Маска + резинка", "від 3 100 грн", "img/cut/box-maskscr-litnie-pole.webp", "", "cut"), ("Твіллі + хустка", "від 3 200 грн", "img/cut/box-sctw-spokusa.webp", "", "cut"),
      ("Велика хустка 65 × 65 / 88 × 88", "від 3 200 грн", "photo/solo/avantiura-88-3.webp", "50% 20%", "photo"), ("Сертифікат", "2 500 або 4 000 грн", "img/cert-card.png", "50% 50%", "photo")]),
]
def budget_hero():
    return f'''
  <section class="hero dq-hero" id="top">
    <figure class="dq-hero-ph">{img("photo/solo/zolote-44-5.webp", "Хустка «Золоте світло» на плечах", sizes="100vw", lazy=False, eager_priority=True, style="object-position:50% 12%")}</figure>
    <div class="dk-band dq-band"><div class="wrap"><div class="dk-band-t"><p class="eyebrow">Obiimy · преміальні шовкові вироби</p><h1>Подарунок команді — <i>за вашим бюджетом</i></h1>
      <p class="dk-band-lead">Три полиці за бюджетом на людину. Пакування й наліпка з вашим логотипом — у ціні.</p>
      <div class="cta"><a class="btn btn-gold" href="#request">Отримати розрахунок</a><a class="btn btn-line" href="#shelves">Що на полицях</a></div></div>
      <nav class="dq-index" aria-label="Полиці"><a href="#shelf1"><b>до 1 000</b><span>грн · знак уваги</span></a><a href="#shelf2"><b>1 600–2 700</b><span>грн · подарунок, який носять</span></a><a href="#shelf3"><b>від 3 000</b><span>грн · у коробці</span></a></nav></div></div>
  </section>'''
def shelves():
    out = ""
    for i, (b, t, d, items) in enumerate(SHELVES):
        grid = "".join(item(*x) for x in items)
        out += f'<div class="dq-shelf" id="shelf{i + 1}"><div class="dq-shelf-h"><p class="eyebrow">Полиця {i + 1}</p><h2>{b}</h2><p class="dq-t">{t}</p><p class="dq-d">{d}</p></div><div class="dq-grid">{grid}</div></div>'
    return f'<section class="dq-shelves" id="shelves"><div class="wrap">{out}</div></section>'
def mixed():
    return f'''
  <section class="dq-mixed" id="mixed"><div class="wrap">
    <div class="dq-mixed-t"><h2>Змішана команда — <i>однаковий бюджет</i></h2>
      <p>Жінкам — твіллі, чоловікам — хустка-паше: обидва по 1 600 грн, обидва в одному принті або кожному свій. Маска для сну — 2 700 грн для будь-кого; тим, хто аксесуарів не носить, — закладка для книги, однотонна наволочка або сертифікат.</p>
      <p class="dq-fine">Доставка Новою поштою в офіс однією посилкою або кожному окремо — зручно, коли частина команди віддалено.</p></div>
    <div class="dq-mixed-g">{tile("photo/solo/flirt-tw-1.webp", "50% 20%", "Їй — твіллі", "1 600 грн", sz="(max-width: 640px) 50vw, 25vw")}{tile("photo/site/pashe-svoboda-02.jpg", "50% 30%", "Йому — паше", "1 600 грн", sz="(max-width: 640px) 50vw, 25vw")}</div>
  </div></section>'''
def inprice():
    P = [("Подарункове пакування", "Кожна річ — у подарунковому пакуванні Obiimy."), ("Наліпка з вашим логотипом", "Усередині коробки — у ціні."), ("Нашивна бирка чи власний принт", "За запитом — строки й вартість у розрахунку."),
         ("Доставка", "Новою поштою в офіс або кожному окремо; безкоштовно від 5 000 грн — як це діє для розсилки кожному, напишемо в розрахунку."), ("Документи", "Рахунок на юридичну особу; ПДВ і перелік документів підтвердимо в розрахунку."), ("Шоурум", f"{team.SHOWROOM} — подивитися й потримати речі до замовлення.")]
    rows = "".join(f'<div><h3>{k}</h3><p>{v}</p></div>' for k, v in P)
    return f'<section class="dq-inprice" id="inprice"><div class="wrap"><h2>Що у ціні — <i>і що поруч</i></h2><div class="dq-kv">{rows}</div></div></section>'
def page_budget():
    nav = [("Полиці", "shelves"), ("Змішана команда", "mixed"), ("У ціні", "inprice"), ("Як це працює", "how"), ("Питання", "faq")]
    body = budget_hero() + chips(nav) + shelves() + trust() + D.midcta() + mixed() + inprice() + D.steps() + D.faq() + request("f-budget")
    return dict(slug="b2b-deck-budget", skin="deck", bar=team.BAR, title="Подарунок команді за вашим бюджетом — три полиці від 450 грн · Obiimy",
                desc="Корпоративні подарунки Obiimy за бюджетом на людину: до 1 000 грн — резинка, закладка, тримач, сертифікат; 1 600–2 700 — твіллі, паше, хустка, маска для сну; від 3 000 — набори в коробці й великі хустки. Пакування й наліпка з логотипом — у ціні.",
                og="photo/solo/zolote-44-5.webp", nav=nav, cta="Запит", sticky="Подарунки для команди · від 450 грн", body=body)

# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# B · the editorial way in
WAYS_STRIP = [("На сумці", "photo/solo/iskra-65-3.webp", "50% 50%"), ("На голові", "photo/solo/flirt-65-3.webp", "58% 6%", 1.9), ("На шиї", "photo/solo/krok-44-3.webp", "50% 20%"),
              ("На плечах", "photo/solo/avantiura-88-3.webp", "50% 20%"), ("Поясом", "photo/solo/avantiura-88-2.webp", "50% 40%"), ("У волоссі", "photo/solo/krok-tw-2.webp", "50% 30%"), ("Краваткою", "photo/solo/avantiura-tw-4.webp", "50% 15%"), ("На зап’ясті", "photo/solo/krok-tw-3.webp", "50% 35%")]
def story_hero():
    return f'''
  <section class="hero ds-hero" id="top">
    <figure class="ds-hero-ph">{img("photo/solo/tysha-88-2.webp", "Хустка «Тиша всередині» 88 × 88 на плечах", sizes="100vw", lazy=False, eager_priority=True, style="object-position:30% 30%")}</figure>
    <div class="ds-hero-t"><div class="wrap"><p class="eyebrow">Obiimy · подарунки для команди</p><h1>Подарунок, <i>який носять</i></h1>
      <p class="dk-band-lead">Шовкові хустки, твіллі й аксесуари з авторськими принтами — від 1 000 грн за подарунок.<span class="ds-more"> Один принт на всю команду або кожному свій; пакування й наліпка з вашим логотипом — у ціні.</span></p>
      <div class="cta"><a class="btn btn-gold" href="#request">Отримати розрахунок</a><a class="btn btn-line" href="#ways">Як це носять</a></div></div></div>
  </section>'''
def ways_strip():
    tiles = "".join(tile(w[1], w[2], w[0], zoom=(w[3] if len(w) > 3 else 1.0), sz=("(max-width: 640px) 120vw, 44vw" if len(w) > 3 else "(max-width: 640px) 60vw, 22vw")) for w in WAYS_STRIP)
    return f'''
  <section class="ds-ways" id="ways"><div class="wrap"><div class="ds-ways-h"><h2>Одна річ — <i>багато образів</i></h2><div><p>Хустку носять на шиї, на голові, на сумці чи поясом; твіллі — у волоссі, краваткою, на зап’ясті. Тому один подарунок підходить і тим, кого ви знаєте добре, і тим, кого — ще ні.</p>
    <div class="ds-arrows"><button type="button" class="ds-prev" aria-label="Попередні кадри">‹</button><button type="button" class="ds-next" aria-label="Наступні кадри">›</button></div></div></div></div>
    <div class="ds-strip" tabindex="0" role="region" aria-label="Як носять — стрічка кадрів, гортайте">{tiles}</div>
    <div class="wrap"><p class="ds-prices">Хустка 44 × 44 — 1 600 грн · 65 × 65 — від 3 200 · 88 × 88 — від 4 400 · твіллі — 1 600 грн</p></div>
  </section>'''
def three():
    C = [("Усім, хто носить аксесуари · 1 600 на людину", "Твіллі або паше", "Жінкам — твіллі, чоловікам — хустка-паше: за ту саму ціну, в одному принті або кожному свій. Найлегший у виборі подарунок.", "1 600 грн", tile("photo/solo/flirt-tw-1.webp", "50% 20%", "Твіллі", sz="(max-width: 900px) 100vw, 33vw")),
         ("Коли бюджет 2 000–3 500 · набір у коробці", "Набір у коробці", "Твіллі з хусткою, твіллі з резинкою або маска для сну з резинкою — в одному принті, у святковій коробці.", "від 2 200 грн", f'<figure class="dq-cut ds-cut"><div>{img("img/cut/box-sctw-spokusa.webp", "Набір: твіллі й хустка в коробці", sizes="(max-width: 900px) 100vw, 33vw")}</div></figure>'),
         ("Коли лишаєте вибір за людиною", "Сертифікат", "Номінали 1 000, 1 500, 2 000, 2 500 і 4 000 грн; діє три місяці, на будь-який товар.", "від 1 000 грн", f'<figure class="dk-w6 dk-cert"><div>{img("img/cert-card.png", "Подарунковий сертифікат Obiimy", sizes="(max-width: 900px) 100vw, 33vw")}</div></figure>')]
    cards = "".join(f'<div class="ds-card">{ph}<p class="eyebrow">{k}</p><h3>{n}</h3><p>{d}</p><p class="dk-from">{p}</p></div>' for k, n, d, p, ph in C)
    return f'<section class="ds-three" id="three"><div class="wrap"><h2>Три способи <i>подарувати</i></h2><div class="ds-cards">{cards}</div></div></section>'
def men_short():
    return f'''
  <section class="ds-men" id="men"><div class="wrap">
    <div class="ds-men-g">{tile("photo/site/pashe-probudzhennia-02.jpg", "50% 50%", "Хустка-паше", "1 600 грн", sz="(max-width: 640px) 50vw, 25vw")}{tile("photo/site/pashe-svoboda-02.jpg", "50% 30%", "Паше в сорочці", "1 600 грн", sz="(max-width: 640px) 50vw, 25vw")}</div>
    <div class="ds-men-t"><h2>Для чоловіків — <i>той самий бюджет</i></h2><p>Паше в нагрудній кишені — простий спосіб виглядати святково без краватки й зайвих слів. Маска для сну (від 2 700 грн), закладка для книги або однотонна наволочка — для тих, хто аксесуарів не носить. А коли хочеться лишити вибір за людиною — сертифікат.</p>
      <p class="dq-fine">Жінкам — твіллі, чоловікам — паше: обидва по 1 600 грн.</p></div>
  </div></section>'''
def solo_short():
    tiles = "".join(f'<figure class="dk-t7"><div class="dk-t7i">{img(f, f"Принт «{P[0]}»", sizes="(max-width: 640px) 50vw, 14vw", style=f"object-position:{ps};" + (f"transform:scale({z});transform-origin:{ps}" if z != 1 else ""))}</div><figcaption><b>{P[0]}</b></figcaption></figure>'
                    for (f, ps, z), P in zip(deck.STRIP, deck.SOLO))
    return f'''
  <section class="dk-solo-dark ds-solo" id="solo"><div class="wrap">
    <div class="dk-sh7"><div><p class="eyebrow">Нова колекція · 2026</p><h2>Колекція SOLO</h2></div>
    <div class="dk-st"><p class="dk-st7">Сім принтів в одній колекції</p><p>Один стиль на всю команду — і кожному свій принт. Який принт пасує кому — підкажемо в добірці.</p></div></div>
    <div class="dk-strip">{tiles}</div>
  </div></section>'''

STRIP_JS = """
  var strip = document.querySelector('.ds-strip');
  if (strip) { var step = function () { return strip.clientWidth * 0.8; };
    var pv = document.querySelector('.ds-prev'), nx = document.querySelector('.ds-next');
    if (pv) pv.addEventListener('click', function () { strip.scrollBy({ left: -step(), behavior: 'smooth' }); });
    if (nx) nx.addEventListener('click', function () { strip.scrollBy({ left: step(), behavior: 'smooth' }); });
    strip.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { strip.scrollBy({ left: step(), behavior: 'smooth' }); e.preventDefault(); } if (e.key === 'ArrowLeft') { strip.scrollBy({ left: -step(), behavior: 'smooth' }); e.preventDefault(); } }); }
"""
def page_story():
    nav = [("Як носять", "ways"), ("Три способи", "three"), ("Чоловікам", "men"), ("У ціні", "inprice"), ("SOLO", "solo"), ("Питання", "faq")]
    body = story_hero() + chips(nav) + ways_strip() + trust() + three() + men_short() + D.midcta() + inprice() + D.solo() if False else story_hero() + chips(nav) + ways_strip() + trust() + three() + men_short() + D.midcta() + inprice() + solo_short() + D.steps() + D.faq() + request("f-story")
    return dict(slug="b2b-deck-story", skin="deck", bar=team.BAR, title="Подарунок, який носять — шовк Obiimy для команди · від 1 000 грн",
                desc="Корпоративні подарунки Obiimy: хустки, твіллі й аксесуари з авторськими принтами від 1 000 грн за подарунок; три способи подарувати — твіллі всім, набір у коробці ключовим людям, сертифікат на вибір; нова колекція SOLO. Пакування й наліпка з логотипом — у ціні.",
                og="photo/solo/tysha-88-2.webp", nav=nav, cta="Запит", sticky="Подарунок, який носять · від 1 000 грн", body=body)

CSS = """
  /* A · by budget */
  .hero.dq-hero { padding: 0; position: relative; } .dq-hero-ph { margin: 0; } .dq-hero-ph img { width: 100%; height: clamp(300px, 46vh, 520px); object-fit: cover; display: block; }
  .dk-band.dq-band { position: relative; top: auto; transform: none; box-shadow: none; } .dq-band .wrap { grid-template-columns: 1fr auto; align-items: center; }
  .dq-index { display: grid; gap: 10px; } .dq-index a { display: block; text-decoration: none; color: #141414; border-left: 2px solid #141414; padding: 4px 0 4px 14px; } .dq-index b { display: block; font-family: var(--display); font-weight: 400; font-size: 1.5rem; line-height: 1.1; } .dq-index span { font-size: .78rem; letter-spacing: .08em; text-transform: uppercase; color: #4A4A47; }
  .dq-trust { border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); } .dq-trust .wrap { display: flex; flex-wrap: wrap; gap: 8px 28px; padding-block: 16px; font-size: .78rem; letter-spacing: .14em; text-transform: uppercase; color: var(--ink2); } .dq-trust span::before { content: "·"; margin-right: 10px; color: var(--ink3); } .dq-trust span:first-child::before { content: none; }
  @media (max-width: 900px) { .dq-index { display: none; } .dq-hero-ph img { height: auto; aspect-ratio: 4 / 3; } }
  .dq-shelves { padding-block: clamp(32px, 5vw, 72px); } .dq-shelf { display: grid; grid-template-columns: 1fr 3fr; gap: clamp(24px, 4vw, 56px); padding: clamp(28px, 4vw, 48px) 0; border-top: 1px solid var(--line); align-items: start; }
  .dq-shelf-h h2 { margin: 6px 0 8px; font-size: clamp(1.9rem, 2.6vw, 2.6rem); white-space: nowrap; } .dq-t { font-family: var(--display); font-size: 1.2rem; margin: 0 0 10px; } .dq-d { color: var(--ink2); margin: 0; line-height: 1.55; }
  .dq-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; } .dq-grid .dk-w6 img { aspect-ratio: 3 / 4; } .dq-grid .dk-w6 figcaption span, .dq-cut figcaption span { font-size: .95rem; color: #E7D9A6; }
  .dq-cut { margin: 0; background: #141414; display: flex; flex-direction: column; } .dq-cut > div { flex: 1; aspect-ratio: 3 / 4; display: flex; align-items: center; justify-content: center; padding: 10%; } .dq-cut img { max-width: 100%; max-height: 100%; width: auto; height: auto; filter: drop-shadow(0 12px 24px rgba(0,0,0,.5)); }
  .dq-cut figcaption { padding: 0 14px 14px; font-family: var(--display); font-style: italic; font-size: clamp(1.05rem, 1.5vw, 1.35rem); color: #E7D9A6; } .dq-cut figcaption span { display: block; font-family: var(--body); font-style: normal; font-size: .8rem; color: var(--ink2); margin-top: 4px; }
  @media (max-width: 900px) { .dq-shelf { grid-template-columns: 1fr; } .dq-grid { grid-template-columns: repeat(2, 1fr); } }
  .dq-mixed { padding-block: clamp(40px, 6vw, 96px); border-top: 1px solid var(--line); } .dq-mixed .wrap { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(24px, 4vw, 56px); align-items: center; }
  .dq-mixed .wrap { align-items: start; } .dq-mixed-t h2 { margin: 0 0 14px; } .dq-mixed-t p { color: var(--ink2); line-height: 1.6; } .dq-fine { font-size: .9rem; color: var(--ink3); } .dq-mixed-g { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  @media (max-width: 900px) { .dq-mixed .wrap { grid-template-columns: 1fr; } }
  .dq-inprice { padding-block: clamp(40px, 6vw, 96px); border-top: 1px solid var(--line); } .dq-kv { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(20px, 3vw, 48px); margin-top: 28px; }
  .dq-kv div { border-top: 1px solid var(--ink); padding-top: 14px; } .dq-kv h3 { font-size: 1.15rem; margin: 0 0 6px; } .dq-kv p { color: var(--ink2); margin: 0; line-height: 1.55; } @media (max-width: 900px) { .dq-kv { grid-template-columns: 1fr; } }
  /* B · editorial */
  .hero.ds-hero { padding: 0; position: relative; color: #F1EFEA; } .ds-hero-ph { margin: 0; } .ds-hero-ph img { width: 100%; height: clamp(560px, 86vh, 860px); object-fit: cover; display: block; }
  .ds-hero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(0deg, rgba(0,0,0,.72) 0%, rgba(0,0,0,.3) 45%, rgba(0,0,0,0) 70%); }
  .ds-hero::after { background: linear-gradient(0deg, rgba(0,0,0,.78) 0%, rgba(0,0,0,.42) 50%, rgba(0,0,0,.08) 85%); }
  .ds-hero-t { position: absolute; left: 0; right: 0; bottom: clamp(28px, 5vw, 64px); z-index: 2; } .ds-hero-t .wrap { display: block; max-width: 1280px; } .ds-hero-t .wrap > * { max-width: 680px; } .ds-hero-t h1 { text-shadow: 0 2px 24px rgba(0,0,0,.45); } .ds-hero-t .eyebrow { color: rgba(255,255,255,.8); } .ds-hero-t h1 { font-size: clamp(2.6rem, 5.4vw, 4.8rem); line-height: 1; margin: 10px 0 14px; color: #F1EFEA; } .ds-hero-t h1 i { color: #E7D9A6; }
  .ds-hero-t .dk-band-lead { color: #F1EFEA; max-width: 680px; } .ds-hero-t .cta { display: flex; gap: 10px; flex-wrap: wrap; } .ds-hero-t .btn-gold { background: #E7D9A6; color: #141414; } .ds-hero-t .btn-line { border-color: #F1EFEA; color: #F1EFEA; }
  @media (max-width: 640px) { .ds-hero-ph img { height: auto; aspect-ratio: 4 / 3; } .ds-hero::after { display: none; } .ds-hero-t { position: static; background: #141414; padding: 22px 0 24px; } .ds-more { display: none; } .hero.ds-hero .cta .btn-line, .hero.dq-hero .cta .btn-line { width: 100%; border: 1px solid currentColor; text-decoration: none; min-height: 48px; justify-content: center; } }
  .ds-ways { padding-block: clamp(40px, 6vw, 96px); } .ds-ways-h { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: end; margin-bottom: 24px; } .ds-ways-h p { color: var(--ink2); margin: 0; line-height: 1.6; }
  .ds-ways-h > div { display: flex; flex-direction: column; gap: 14px; } .ds-arrows { display: flex; gap: 8px; } .ds-arrows button { width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--ink); background: transparent; color: var(--ink); font-size: 1.4rem; cursor: pointer; } .ds-arrows button:hover { background: var(--ink); color: #F1EFEA; }
  .ds-prices { margin: 14px 0 0; font-size: .9rem; color: var(--ink2); } .ds-strip:focus-visible { outline: 2px solid var(--ink); outline-offset: 4px; }
  .ds-strip { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(220px, 1fr); gap: 10px; overflow-x: auto; padding: 0 max(16px, calc((100vw - 1184px) / 2)); scroll-padding-inline: max(16px, calc((100vw - 1184px) / 2)); scroll-snap-type: x mandatory; scrollbar-width: none; } .ds-strip::-webkit-scrollbar { display: none; } .ds-strip .dk-w6 { scroll-snap-align: start; }
  @media (max-width: 900px) { .ds-ways-h { grid-template-columns: 1fr; } .ds-arrows { display: none; } .ds-strip { grid-auto-columns: 62vw; padding: 0 16px; scroll-padding-inline: 16px; } }
  .ds-three { padding-block: clamp(40px, 6vw, 96px); border-top: 1px solid var(--line); } .ds-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(20px, 3vw, 40px); margin-top: 28px; }
  .ds-card .dk-w6 img, .ds-card .dq-cut > div { aspect-ratio: 4 / 5; } .ds-card .dk-w6::after { display: none; } .ds-card .dk-w6 figcaption { display: none; } .ds-card .eyebrow { margin: 18px 0 6px; } .ds-card h3 { font-size: clamp(1.4rem, 2vw, 1.9rem); margin: 0 0 8px; } .ds-card p { color: var(--ink2); margin: 0; line-height: 1.55; }
  .ds-card .dk-from { font-family: var(--display); font-style: italic; font-size: 1.2rem; color: var(--ink); margin-top: 10px; } .ds-cut > div { padding: 8%; } .ds-card .eyebrow { font-weight: 400; color: var(--ink2); } .ds-card .dk-cert div { aspect-ratio: 4 / 5; } .ds-card .dk-cert img { height: 100%; }
  @media (max-width: 900px) { .ds-cards { grid-template-columns: 1fr; } }
  .ds-men { padding-block: clamp(40px, 6vw, 96px); border-top: 1px solid var(--line); } .ds-men .wrap { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(24px, 4vw, 56px); align-items: center; } .ds-men-g { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .ds-men .wrap { align-items: start; } .ds-men-t h2 { margin: 0 0 14px; } .ds-men-t p { color: var(--ink2); line-height: 1.6; } .ds-solo .dk-t7 figcaption { padding-top: 10px; }
  @media (max-width: 640px) { .ds-solo .dk-t7:last-child { grid-column: 1 / -1; } .ds-solo .dk-t7:last-child .dk-t7i { aspect-ratio: 16 / 10; } } @media (max-width: 900px) { .ds-men .wrap { grid-template-columns: 1fr; } .ds-men-g { order: 2; } }
"""

def build():
    b2b.CSS += team.CSS + shop.CSS + main.CSS + D.CSS + CSS
    for p in (page_budget(), page_story()):
        html = main.snap_type(typo(team.bind(b2b.shell(p, p["body"]))))
        (b2b.OUT / f"{p['slug']}.html").write_text(html)
        print(p["slug"], len(html) // 1024, "KB")

if __name__ == "__main__":
    build()
