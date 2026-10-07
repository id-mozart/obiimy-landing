#!/usr/bin/env python3
"""The corporate-sales landing built from the team deck (obiimy-podarunky-dlia-komandy.pdf, 07.10.2026) — the same eleven
pages as sections, the same words, photographs and prices: the mosaic cover, «Про нас», scarves, twillies, accessories, the three
sets, the other sets, gifts for men, SOLO, questions and answers, the request. Data comes from src/build-team-pdf.py so that
the deck and the page never disagree; the shell, form and typography come from build-b2b*.py."""
import importlib.util, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
deck = load("build-team-pdf")                 # pages are built on import, nothing is rendered
main = load("build-b2b-team-main")
shop = main.shop; team = main.team; b2b, img, typo = team.b2b, team.img, team.typo
PHONE, PHONE_HREF, TG, MAIL, SHOWROOM = team.PHONE, team.PHONE_HREF, team.TG, team.MAIL, team.SHOWROOM
money = deck.money

# ── data straight from the deck ───────────────────────────────────────────────────────────────────────────────────
MOSAIC = [("photo/solo/iskra-65-4.webp", "50% 15%"), ("photo/solo/flirt-tw-1.webp", "50% 20%"), ("photo/site/mask-shchyri-pochuttia-04.jpg", "0% 50%"), ("photo/solo/zolote-44-2.webp", "50% 15%"),
          ("photo/site/maska-dlia-snu-ta-rezynka-vpevnenist-03.jpg", "50% 50%"), ("photo/solo/tysha-88-4.webp", "50% 10%"), ("photo/solo/krok-44-2.webp", "50% 20%"), ("photo/solo/flirt-65-4.webp", "50% 15%")]   # the cover (cvz9)
MORE = [("Сертифікат", "На будь-яку суму від 1 000 до 4 000 грн.", 1000, "img/sets/cert-2000.webp"),
        ("Маска, закладка й резинка", "Три речі в одному принті, у коробці.", 3600, "img/cut/sleep-pidnesennia.webp"),
        ("Хустка й кільце", "Хустка 65 × 65 і кільце для хустки.", 3650, "img/cut/duo-iskra-ring.webp"),
        ("Три твіллі", "Три принти на вибір в одній коробці.", 4800, "img/cut/three-twilly-2.webp")]   # deck p. 7 (src/build-deck-variants.py MORE)
ST7 = dict(deck.ST7)
SZ6 = "(max-width: 640px) 50vw, (max-width: 1100px) 33vw, 22vw"

def tile(f, pos, cap, sub="", zoom=1.0, alt=""):
    z = f"transform:scale({zoom});transform-origin:{pos};" if zoom != 1.0 else ""
    return (f'<figure class="dk-w6">{img(f, alt or cap, sizes=SZ6, style=f"object-position:{pos};{z}")}'
            f'<figcaption><i>{cap}</i>{f"<span>{sub}</span>" if sub else ""}</figcaption></figure>')
def cutimg(name, alt, w=240): return img(f"img/cut/{name}.webp", alt, sizes=f"{w}px")

# ── sections ──────────────────────────────────────────────────────────────────────────────────────────────────────
def hero():
    frames = "".join(img(f, "", sizes="(max-width: 640px) 50vw, 25vw", lazy=i > 3, style=f"object-position:{p}") for i, (f, p) in enumerate(MOSAIC))
    return f'''
  <section class="hero dk-cover" id="top">
    <div class="dk-mosaic">{frames}</div>
    <div class="dk-band"><div class="wrap">
      <img src="brand/logo-ink-480.webp" alt="Obiimy" width="150" height="32" class="dk-band-logo">
      <div class="dk-band-t"><h1>Подарунки для команди</h1><p class="eyebrow">Преміальні шовкові вироби · 2026</p></div>
      <div class="cta"><a class="btn btn-gold" href="#request">Отримати розрахунок</a><a class="btn btn-line" href="obiimy-podarunky-dlia-komandy.pdf" download="Obiimy-podarunky-dlia-komandy.pdf" type="application/pdf">Презентація (PDF, {team.PDF_MB} МБ) ↓</a></div>
    </div></div>
  </section>'''

def about():
    paras = "".join(f"<p>{x}</p>" for x in deck.ABOUT)
    return f'''
  <section class="dk-split" id="about"><div class="wrap">
    <figure>{img("photo/solo/iskra-65-2.webp", "Хустка «Іскра» 65 × 65 на плечах", sizes="(max-width: 900px) 100vw, 50vw", style="object-position:44% 0%")}</figure>
    <div class="dk-ab"><p class="dk-ab-lead">{deck.ABOUT_LEAD}</p>{paras}</div>
  </div></section>'''

def ways(sid, title, frm, leads, tiles, aside, cls=""):
    return f'''
  <section class="dk-ways {cls}" id="{sid}"><div class="wrap">
    <div class="dk-panel"><h2>{title}</h2><p class="dk-from">від {money(frm)} грн</p>{"".join(f'<p class="dk-lead">{x}</p>' for x in leads)}{aside}</div>
    <div class="dk-w6g">{tiles}</div>
  </div></section>'''

def scarves():
    tiles = "".join(tile(t[1], t[2], t[0], zoom=(t[3] if len(t) > 3 else 1.0)) for t in deck.W6)
    nest = "".join(f'<figure class="dk-n{i}">{img(f"img/cut/{c}.webp", f"Хустка {n}", sizes="200px")}</figure>' for i, (c, mm, n, p) in enumerate(deck.NEST))
    legend = "".join(f'<p><b>{n}</b><span>від {money(p)} грн</span></p>' for c, mm, n, p in deck.NEST)
    aside = f'<div class="dk-nest">{nest}<div class="dk-nl">{legend}</div></div>'
    return ways("scarves", "Хустки", 1600, ["Хустка — подарунок, який носять по-різному: на шиї, на голові, на сумці, поясом чи топом. Одна річ — багато образів, тому вона підходить і тим, кого ви знаєте добре, і тим, кого — ще ні.",
                                           "Три розміри — для різних образів і нагод. Принт один на всю команду або кожному свій."], tiles, aside)

def twilly():
    tiles = "".join(tile(f, ps, n, zoom=z) for n, f, ps, z in deck.WAYS)
    pair = "".join(f'<figure>{img(f, "Хустка й твіллі одного принту", sizes="200px", style=f"object-position:{p}")}</figure>' for f, p in deck.PAIR)
    aside = f'<div class="dk-pair">{pair}</div><p class="dk-pair-cap">Твіллі добре працює в парі: хустка й твіллі одного принту — на плечах і на сумці.</p>'
    return ways("twilly", "Твіллі", 1600, ["Твіллі — вузька шовкова стрічка. Її зав’язують у волоссі, на шиї, на зап’ясті, краваткою або на ручці сумки — і носять щодня.",
                                         "Найдоступніший подарунок у каталозі й найлегший у виборі: підходить усім, хто носить аксесуари. Десятки авторських принтів — один на всю команду або кожному свій."], tiles, aside)

def accessories():
    tiles = "".join(tile(t[2], t[3], t[0], t[1], zoom=(t[4] if len(t) > 4 else 1.0)) for t in deck.ACC4)
    aside = f'<figure class="dk-setcut">{cutimg("box-maskscr-melodiia", "Набір: маска для сну й резинка в коробці")}</figure><p class="dk-pair-cap">Кілька аксесуарів чудово складаються в набір — наприклад, маска для сну й резинка одного принту в коробці.</p>'
    return ways("acc", "Аксесуари", 700, ["Речі з того самого шовку — для тих, хто хустки не носить, і для подарунка «про відпочинок»: маска для сну, резинка для волосся, закладка для книги, тримач для хустки.",
                                        "Шовк м’який і дбайливий до шкіри, тому маска для сну з нього — одна з найкращих. Резинка — найпростіший знак уваги на всю команду. Тримач — маленьке кільце, яке тримає хустку чи твіллі й робить із них готовий образ."], tiles, aside, cls="dk-w4")

def sets():
    cols = "".join(f'<div class="dk-scol"><figure>{cutimg(c, n, 420)}</figure><h3>{n}</h3><p>{d}</p><p class="dk-from">{pz}</p></div>' for n, d, pz, c, w in deck.SETS3)
    return f'''
  <section class="dk-sets" id="sets"><div class="wrap">
    <div class="dk-sh2"><h2>Подарункові набори</h2><p class="dk-note">Разом із вами підберемо або створимо<br>унікальний набір саме для вашої команди.</p></div>
    <div class="dk-scols">{cols}</div>
  </div></section>'''

def more():
    rows = "".join(f'<div class="dk-rw">{img(f, n, sizes="96px")}<h3>{n}</h3><p class="dk-pr"><small>від</small> {money(p)} <small>грн</small></p><span>{d}</span></div>' for n, d, p, f in MORE)
    return f'''
  <section class="dk-split dk-more" id="more"><div class="wrap">
    <figure>{img("photo/site/set-ta-rezynka-litnie-pole-04.jpg", "Набір «Літнє поле»: маска для сну й резинка в коробці", sizes="(max-width: 900px) 100vw, 50vw", style="object-position:42% 50%")}</figure>
    <div><h2>Є й інші набори — <i>і ще десятки варіантів</i></h2><div class="dk-rows">{rows}</div>
    <p class="dk-fine">У каталозі — 49 готових наборів у коробці. Підберемо під вашу нагоду й бюджет або зберемо власний.</p></div>
  </div></section>'''

def men():
    tiles = "".join((tile(t[2], t[3], t[0], t[1]) if t[2] else f'<figure class="dk-w6 dk-cert">{img("img/cert-card.png", "Подарунковий сертифікат Obiimy", sizes=SZ6)}<figcaption><i>{t[0]}</i><span>{t[1]}</span></figcaption></figure>') for t in deck.MEN4)
    aside = f'<figure class="dk-setcut">{cutimg("pillow-tuman", "Шовкова наволочка «Туман»")}</figure><p class="dk-pair-cap">Наволочка з однотонного шовку — подарунок про сон, для тих, хто не носить аксесуарів.</p>'
    return ways("men", "Для чоловіків", 800, ["Чоловікам у команді — речі з того самого шовку, тільки стриманіші: хустка-паше в кишеню піджака, маска для сну, закладка для книги або однотонна наволочка.",
                                            "Паше в нагрудній кишені — найкоротший шлях до святкового вигляду: без краватки й зайвих слів. А коли хочеться лишити вибір за людиною — сертифікат."], tiles, aside, cls="dk-w4")

def solo():
    tiles = "".join(f'<figure class="dk-t7">{img(f, f"Принт «{P[0]}»", sizes="(max-width: 640px) 50vw, 14vw", style=f"object-position:{ps};" + (f"transform:scale({z});transform-origin:{ps}" if z != 1 else ""))}<figcaption><b>{P[0]}</b><span>{ST7.get(P[0], P[1])}</span></figcaption></figure>'
                    for (f, ps, z), P in zip(deck.STRIP, deck.SOLO))
    return f'''
  <section class="dk-solo-dark" id="solo"><div class="wrap">
    <div class="dk-sh7"><div><p class="eyebrow">Нова колекція · 2026</p><h2>Колекція SOLO</h2><p class="dk-sub"><i>Шлях до себе.</i> Натхнення — обкладинки модних журналів 40–50-х.</p></div>
    <div class="dk-st"><p class="dk-st7">Сім принтів — сім станів</p><p>Кожен принт — про свій стан. Обирайте один для всієї команди або свій для кожного.</p></div></div>
    <div class="dk-strip">{tiles}</div>
  </div></section>'''

def faq():
    items = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(deck.FAQ9))
    return f'''
  <section class="dk-faq" id="faq"><div class="wrap"><h2>Запитання та відповіді</h2><div class="dk-faq2">{items}</div></div></section>'''

def page():
    body = hero() + about() + scarves() + twilly() + accessories() + sets() + more() + men() + solo() + faq() + main.with_qr(
        team.request_section("f-deck", "Подарунки для команди (презентація)", "Зв’яжіться з нами — <i>разом підберемо все для вашої команди</i>",
                             "Нагода, кількість людей і дата вручення — цього досить для першого листа. У відповідь надішлемо добірку з фото й розрахунок.", "sets", corp=True)) + team.script("f-deck", "")
    return dict(slug="b2b-deck", skin="deck", bar=team.BAR, title="Подарунки для команди — преміальні шовкові вироби Obiimy · хустки, твіллі, аксесуари, набори",
                desc="Корпоративні подарунки Obiimy за презентацією для команд: хустки від 1 600 грн, твіллі від 1 600, аксесуари від 700, набори в коробці від 2 200 грн, подарунки для чоловіків, нова колекція SOLO. Пакування й наліпка з вашим логотипом — у ціні.",
                og="photo/solo/iskra-65-4.webp", nav=[("Хустки", "scarves"), ("Твіллі", "twilly"), ("Аксесуари", "acc"), ("Набори", "sets"), ("Чоловікам", "men"), ("SOLO", "solo"), ("Питання", "faq")],
                cta="Запит", sticky="Подарунки для команди · преміальний шовк", body=body)

CSS = """
  /* b2b-deck: the deck's pages as sections */
  .hero.dk-cover { padding: 0; }
  .dk-mosaic { display: grid; grid-template-columns: repeat(4, 1fr); } .dk-mosaic img { width: 100%; aspect-ratio: 74.25 / 105; object-fit: cover; display: block; }
  .dk-band { background: #FDD31A; color: #141414; padding: clamp(18px, 3vw, 34px) 0; } .dk-band .wrap { display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: clamp(16px, 3vw, 40px); }
  .dk-band-logo { width: clamp(110px, 12vw, 150px); height: auto; } .dk-band h1 { font-size: clamp(1.6rem, 2.8vw, 2.4rem); margin: 0 0 6px; } .dk-band .eyebrow { color: #141414; font-weight: 400; }
  .dk-band .cta { display: flex; gap: 10px; flex-wrap: wrap; } .dk-band .btn-gold { background: #141414; color: #F1EFEA; } .dk-band .btn-line { border-color: #141414; color: #141414; }
  @media (max-width: 900px) { .dk-band .wrap { grid-template-columns: 1fr; } .dk-mosaic { grid-template-columns: repeat(2, 1fr); } }
  .dk-split { padding-block: clamp(40px, 6vw, 96px); } .dk-split .wrap { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(24px, 5vw, 72px); align-items: center; }
  .dk-split figure { margin: 0; } .dk-split figure img { width: 100%; aspect-ratio: 148.5 / 210; object-fit: cover; display: block; }
  .dk-ab { color: var(--ink2); line-height: 1.6; } .dk-ab p { margin: 0 0 12px; } .dk-ab-lead { font-family: var(--display); font-size: clamp(1.2rem, 1.8vw, 1.5rem); line-height: 1.35; color: var(--ink); margin-bottom: 20px !important; }
  @media (max-width: 900px) { .dk-split .wrap { grid-template-columns: 1fr; } .dk-split figure img { aspect-ratio: 4 / 3; } }
  .dk-ways { padding-block: clamp(40px, 6vw, 96px); border-top: 1px solid var(--line); } .dk-ways .wrap { display: grid; grid-template-columns: 1fr 2fr; gap: clamp(24px, 4vw, 56px); align-items: start; }
  .dk-ways .dk-panel { display: flex; flex-direction: column; min-height: 100%; } .dk-ways h2 { margin: 0 0 4px; } .dk-ways .dk-from { font-family: var(--display); font-style: italic; font-size: 1.15rem; color: var(--ink2); margin: 0 0 20px; }
  .dk-ways .dk-lead { color: var(--ink2); line-height: 1.6; margin: 0 0 14px; } .dk-ways .dk-lead:first-of-type { color: var(--ink); font-size: 1.05rem; }
  .dk-w6g { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; } .dk-ways.dk-w4 .dk-w6g { grid-template-columns: repeat(2, 1fr); }
  .dk-w6 { position: relative; margin: 0; overflow: hidden; background: #ddd; } .dk-w6 img { width: 100%; aspect-ratio: 61.5 / 103.5; object-fit: cover; display: block; } .dk-ways.dk-w4 .dk-w6 img { aspect-ratio: 93.75 / 103.5; }
  .dk-w6::after { content: ""; position: absolute; inset: 52% 0 0; background: linear-gradient(0deg, rgba(0,0,0,.78) 0%, rgba(0,0,0,.4) 45%, rgba(0,0,0,0) 100%); }
  .dk-w6 figcaption { position: absolute; left: 14px; bottom: 12px; z-index: 2; color: #E7D9A6; font-family: var(--display); font-size: clamp(1.1rem, 1.6vw, 1.5rem); line-height: 1.1; }
  .dk-w6 figcaption span { display: block; font-family: var(--body); font-size: .8rem; color: rgba(231,217,166,.85); margin-top: 4px; }
  .dk-w6.dk-cert img { aspect-ratio: 93.75 / 103.5; }
  .dk-nest { position: relative; margin-top: auto; padding-top: 24px; display: grid; grid-template-columns: 1fr auto; gap: 16px; align-items: end; min-height: 200px; }
  .dk-nest figure { position: absolute; bottom: 0; margin: 0; } .dk-nest img { display: block; filter: drop-shadow(0 4px 8px rgba(0,0,0,.16)); } .dk-nest .dk-n0 { left: 0; width: 44%; } .dk-nest .dk-n1 { left: 13%; width: 33%; } .dk-nest .dk-n2 { left: 26%; width: 22%; }
  .dk-nest .dk-nl { grid-column: 2; display: flex; flex-direction: column; gap: 10px; } .dk-nest .dk-nl p { margin: 0; } .dk-nest .dk-nl b { display: block; font-family: var(--display); font-weight: 400; font-size: 1.1rem; } .dk-nest .dk-nl span { font-size: .8rem; color: var(--ink2); }
  .dk-pair { margin-top: auto; padding-top: 24px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; max-width: 320px; } .dk-pair figure { margin: 0; } .dk-pair img { width: 100%; aspect-ratio: 40.5 / 50; object-fit: cover; display: block; }
  .dk-pair-cap { font-size: .9rem; color: var(--ink2); margin: 12px 0 0; max-width: 360px; } .dk-setcut { margin: auto 0 0; padding-top: 24px; max-width: 260px; } .dk-setcut img { width: 100%; height: auto; display: block; }
  @media (max-width: 900px) { .dk-ways .wrap { grid-template-columns: 1fr; } .dk-nest, .dk-pair, .dk-setcut { margin-top: 20px; } }
  @media (max-width: 640px) { .dk-w6 figcaption { left: 10px; bottom: 9px; font-size: .95rem; } .dk-w6 figcaption span { font-size: .7rem; } .dk-w6g { gap: 6px; } }
  .dk-sets { padding-block: clamp(40px, 6vw, 96px); border-top: 1px solid var(--line); } .dk-sh2 { display: flex; justify-content: space-between; align-items: end; gap: 24px; padding-bottom: 20px; border-bottom: 1px solid var(--line); }
  .dk-sh2 .dk-note { font-size: .85rem; color: var(--ink2); text-align: right; margin: 0; }
  .dk-scols { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(20px, 3vw, 48px); padding-top: 28px; } .dk-scol figure { margin: 0 0 18px; height: 300px; display: flex; align-items: center; justify-content: center; }
  .dk-scol figure img { max-width: 100%; max-height: 100%; width: auto; height: auto; filter: drop-shadow(0 6px 10px rgba(40,25,10,.18)); } .dk-scol h3 { font-size: clamp(1.4rem, 2vw, 1.9rem); margin: 0 0 8px; } .dk-scol p { color: var(--ink2); margin: 0; }
  .dk-scol .dk-from { font-family: var(--display); font-size: 1.35rem; color: var(--ink); margin-top: 14px; } .dk-scol .dk-from::first-letter { font-style: italic; }
  @media (max-width: 900px) { .dk-sh2 { flex-direction: column; align-items: start; } .dk-sh2 .dk-note { text-align: left; } .dk-scols { grid-template-columns: 1fr; } .dk-scol figure { height: 220px; } }
  .dk-more .dk-rows { margin-top: 24px; } .dk-more .dk-rw { display: grid; grid-template-columns: 72px 1fr auto; column-gap: 16px; padding: 14px 0; border-top: 1px solid var(--line); align-items: center; }
  .dk-more .dk-rw img { grid-row: 1 / 3; width: 72px; height: 72px; object-fit: contain; } .dk-more .dk-rw h3 { font-size: 1.15rem; margin: 0; white-space: nowrap; } .dk-more .dk-rw .dk-pr { font-family: var(--display); font-size: 1.5rem; margin: 0; white-space: nowrap; }
  .dk-more .dk-rw .dk-pr small { font-family: var(--display); font-style: italic; font-size: .85rem; color: var(--ink2); } .dk-more .dk-rw span { grid-column: 2 / 4; font-size: .85rem; color: var(--ink2); } .dk-more .dk-rw:last-child { border-bottom: 1px solid var(--line); }
  .dk-more .dk-fine { font-size: .85rem; color: var(--ink2); margin-top: 18px; } .dk-more .wrap { align-items: start; }
  .dk-solo-dark { background: #0E0E0E; color: #F1EFEA; padding-block: clamp(40px, 6vw, 96px); } .dk-solo-dark h2 { color: #F1EFEA; font-size: clamp(2.2rem, 4vw, 3.4rem); margin: 6px 0 10px; }
  .dk-sh7 { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: start; margin-bottom: 32px; } .dk-sh7 .eyebrow { color: rgba(255,255,255,.78); }
  .dk-sh7 .dk-sub { margin: 0; color: #C9C6C0; } .dk-sh7 .dk-sub i { color: #E7D9A6; font-family: var(--display); font-size: 1.15rem; } .dk-sh7 .dk-st { padding-top: 34px; } .dk-sh7 .dk-st7 { font-family: var(--display); font-style: italic; font-size: 1.3rem; color: #E7D9A6; margin: 0 0 8px; } .dk-sh7 .dk-st p:last-child { color: #C9C6C0; margin: 0; }
  .dk-strip { display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; } .dk-t7 { margin: 0; overflow: hidden; } .dk-t7 img { width: 100%; aspect-ratio: 35.14 / 98; object-fit: cover; display: block; }
  .dk-t7 figcaption { padding-top: 12px; } .dk-t7 b { display: block; font-family: var(--display); font-style: italic; font-weight: 400; color: #E7D9A6; font-size: 1.05rem; margin-bottom: 4px; } .dk-t7 span { font-size: .8rem; color: #C9C6C0; line-height: 1.4; }
  @media (max-width: 900px) { .dk-sh7 { grid-template-columns: 1fr; } .dk-sh7 .dk-st { padding-top: 0; } .dk-strip { grid-template-columns: repeat(4, 1fr); } } @media (max-width: 640px) { .dk-strip { grid-template-columns: repeat(2, 1fr); } .dk-t7 img { aspect-ratio: 3 / 4; } }
  .dk-faq { padding-block: clamp(40px, 6vw, 96px); } .dk-faq2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0 48px; margin-top: 24px; } .dk-faq2 details { border-top: 1px solid var(--line); padding: 14px 0; }
  .dk-faq2 summary { font-family: var(--display); font-size: 1.15rem; cursor: pointer; list-style: none; display: flex; justify-content: space-between; gap: 12px; } .dk-faq2 summary::after { content: "+"; color: var(--ink2); } .dk-faq2 details[open] summary::after { content: "–"; }
  .dk-faq2 p { color: var(--ink2); margin: 8px 0 0; line-height: 1.55; } @media (max-width: 900px) { .dk-faq2 { grid-template-columns: 1fr; } }
"""

def build():
    b2b.CSS += team.CSS + shop.CSS + main.CSS + CSS
    p = page()
    html = main.snap_type(typo(team.bind(b2b.shell(p, p["body"]))))
    (b2b.OUT / f"{p['slug']}.html").write_text(html)
    print(p["slug"], len(html) // 1024, "KB")

if __name__ == "__main__":
    build()
