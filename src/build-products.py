#!/usr/bin/env python3
"""Generate one example product page per landing version. Output: ../p-<skin>.html"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
ENGINE = (ROOT / "silk-engine.js").read_text()

# ---------- products ----------
PRODUCTS = {
    "probudzhennia": {
        "name": "Пробудження", "collection": "Пробудження", "state": "Про емоції, що ростуть зсередини",
        "story": "Картина «Іриси» була написана саме від пробудження нових емоцій та нових ідей. Вони переповнюють всю тебе, і назовні виривається все те, що вже так давно дозрівало в тобі. Принт «Пробудження» — про ті незабутні емоції, котрі «ростуть» зсередини в перші хвилини пізнання чогось нового.",
        "quote": "Немов увесь світ зупинився тільки для того, щоб сказати тобі: «Привіт!»",
        "tex": "probudzhennia", "back": "litnie-pole", "backname": "Літнє поле", "double": True,
        "photos": ["photo/probudzhennia-2.webp", "photo/probudzhennia-1.webp", "photo/probudzhennia-3.webp", "img/probudzhennia.webp"],
        "sizes": [("44 × 44", 1600, 2400), ("65 × 65", 3200, 4800), ("88 × 88", 4400, None)], "default": 1, "sale": {"65 × 65": 4320},
        "wear": [("Тюрбан", "photo/probudzhennia-3.webp"), ("На плечах", "photo/probudzhennia-1.webp"), ("На шиї", "photo/probudzhennia-2.webp")],
        "url": "https://obiimy.world/shovkova-khustka-probudzhennia-65x65/", "sku": "65-14",
    },
    "dotyk": {
        "name": "Сміливий дотик", "collection": "Дика стихія", "state": "Про сміливість бути помітною",
        "story": "Леопард і степові квіти на одному полотні. Принт із колекції «Дика стихія» — для образів, у яких хустка головна, а не доповнення. Шаль 88 × 88 лягає на плечі поверх тренча, як накидка, або збирається у тюрбан.",
        "quote": "Хустка — головна, а не доповнення.",
        "tex": "prystrast", "back": None, "backname": None, "double": False,
        "photos": ["photo/dotyk-1.webp", "photo/dotyk-2.webp", "photo/dotyk-3.webp", "photo/dotyk-flat.webp"],
        "sizes": [("44 × 44", 1600, None), ("65 × 65", 3200, None), ("88 × 88", 4400, None)], "default": 2, "sale": {},
        "wear": [("На тренчі", "photo/dotyk-2.webp"), ("На плечах", "photo/dotyk-1.webp"), ("Деталь", "photo/dotyk-3.webp")],
        "url": "https://obiimy.world/shovkova-khustka-smilyvyi-dotyk-88x88/", "sku": "88-22",
    },
    "enerhiia": {
        "name": "Енергія", "collection": "Дика стихія", "state": "Про вечір, який починається з деталі",
        "story": "Чорний з бузковим. Хустка, зав’язана на відкритій спині, працює як прикраса: біла сорочка, чорний вузол, і більше нічого не треба. «Енергія» — один із найтемніших принтів колекції, тому світиться на світлому.",
        "quote": "Одна хустка робить те, чого не роблять прикраси: дає обличчю світло.",
        "tex": "mizh-namy", "back": None, "backname": None, "double": False,
        "photos": ["photo/enerhiia-back.webp", "photo/enerhiia-still.webp", "photo/enerhiia-knot.webp"],
        "sizes": [("44 × 44", 1600, None), ("65 × 65", 3200, None), ("88 × 88", 4400, None)], "default": 2, "sale": {},
        "wear": [("На спині", "photo/enerhiia-back.webp"), ("Вузол", "photo/enerhiia-knot.webp"), ("Натюрморт", "photo/enerhiia-still.webp")],
        "url": "https://obiimy.world/shovkova-khustka-enerhiia-88x88/", "sku": "88-6",
    },
    "mizh": {
        "name": "Між нами", "collection": "Поклик душі", "state": "Про те, що лишається тільки між двома",
        "story": "Гортензії по краю сірого шовку. Найстаріший спосіб носити хустку — на голові, під підборіддя — і найактуальніший цього сезону. Біле пальто, темні окуляри, і «Між нами» робить усе інше.",
        "quote": "Найстаріший спосіб і найактуальніший.",
        "tex": "mizh-namy", "back": "prystrast", "backname": "Пристрасть", "double": True,
        "photos": ["photo/mizh-1.webp", "photo/mizh-2.webp", "photo/mizh-flat.webp"],
        "sizes": [("44 × 44", 1600, 2400), ("65 × 65", 3200, 4800), ("88 × 88", 4400, None)], "default": 2, "sale": {"65 × 65": 4320},
        "wear": [("На голові", "photo/mizh-1.webp"), ("На плечі", "photo/mizh-2.webp"), ("Розкладена", "photo/mizh-flat.webp")],
        "url": "https://obiimy.world/shovkova-khustka-mizh-namy-88x88/", "sku": "88-17",
    },
    "kolo": {
        "name": "Коло сонця", "collection": "Співоча душа", "state": "Про тепло, яке щоразу повертається",
        "story": "Вінок із сонячних квітів на рожевому шовку. Колекція «Співоча душа» присвячена рідкісним птахам України: частина коштів від кожної хустки йде на гнізда для сиворакші, птаха з Червоної книги. Роботи створені разом із художницею Анною Кловак.",
        "quote": "Ця колекція про тендітність і силу, про птахів, які співають і зникають, про красу, яка може рятувати.",
        "tex": "kolo-sontsia", "back": None, "backname": None, "double": False,
        "photos": ["photo/kolo-2.webp", "photo/kolo-1.webp", "photo/kolo-3.webp", "img/kolo-sontsia.webp"],
        "sizes": [("44 × 44", 1600, None), ("65 × 65", 3200, None), ("88 × 88", 4400, None)], "default": 2, "sale": {},
        "wear": [("На плечі", "photo/kolo-2.webp"), ("Накидкою", "photo/kolo-1.webp"), ("На тренчі", "photo/kolo-3.webp")],
        "url": "https://obiimy.world/shovkova-khustka-kolo-sontsia-88x88/", "sku": "88-30",
    },
    "melodiia": {
        "name": "Мелодія двох", "collection": "Співоча душа", "state": "Про розмову, для якої не потрібні слова",
        "story": "Дві пташки серед верболозу на глибокому бірюзовому. Хустка паше 44 × 44 — на ручку сумки, як браслет, у нагрудну кишеню жакета. Частина коштів від колекції йде на гнізда для сиворакші.",
        "quote": "Дві пташки серед верболозу.",
        "tex": "melodiia", "back": None, "backname": None, "double": False,
        "photos": ["img/melodiia.webp", "tex/melodiia.jpg"],
        "sizes": [("44 × 44", 1600, None), ("65 × 65", 3200, None), ("88 × 88", 4400, None)], "default": 0, "sale": {},
        "wear": [("На сумку", "photo/bag-2.webp"), ("Паше", "img/melodiia.webp"), ("Принт", "tex/melodiia.jpg")],
        "url": "https://obiimy.world/spivocha-dusha/", "sku": "44-27",
    },
}
REVIEW = ("Замовляла на подарунок хустку, якість неймовірна, подруга теж задоволена! Вирішила замовити собі твіллі — не можу нарадуватись, кожного дня хочеться додавати в образ.", "Анна Мелешак · відгук на obiimy.world")
RELATED = [
    ("Хустка «Єднання»", "44 × 44 · двосторонній", "2 400 грн", "img/yednannia.webp", "https://obiimy.world/spivocha-dusha/"),
    ("Твіллі «Золоте світло»", "84 × 5", "1 600 грн", "img/twilly-zolote.webp", "https://obiimy.world/khustka-tvilli-shovkova-zolote-svitlo-84x5/"),
    ("Маска для сну «Впевненість»", "італійський шовк", "2 700 грн", "img/mask-vpevnenist.webp", "https://obiimy.world/maska-dlia-snu-z-naturalnoho-shovku-vpevnenist/"),
    ("Набір «Натхнення»", "твіллі + хустка", "3 200 грн", "img/set-natkhnennia.webp", "https://obiimy.world/nabir-tvilli-845-ta-khustky-4444-natkhnennia/"),
]

# ---------- skins ----------
SKINS = {
    "classic": dict(title="Obiimy Silk", landing="classic.html", product="probudzhennia", viewer="photos", dark=False,
        fonts="Prata&family=Manrope:wght@400;500;600;700", display="'Prata', serif", body="'Manrope', sans-serif",
        css=":root{--bg:#F5F2F6;--bg2:#ECE7EF;--card:#fff;--ink:#1E1830;--ink2:#4A4358;--ink3:#7B7489;--line:#D9D2DE;--accent:#5B3E9E;--gold:#F2B705;--radius:6px}"),
    "maison": dict(title="Obiimy Maison", landing="maison.html", product="probudzhennia", viewer="photos", dark=False,
        fonts="Prata&family=Onest:wght@300;400;500;600", display="'Prata', serif", body="'Onest', sans-serif",
        css=":root{--bg:#F4F3EF;--bg2:#ECEAE4;--card:#fff;--ink:#171519;--ink2:#4A4750;--ink3:#807C86;--line:rgba(23,21,25,.12);--accent:#4B3D8F;--gold:#F2B705;--radius:6px}"),
    "journal": dict(title="Obiimy Journal", landing="journal.html", product="dotyk", viewer="photos", dark=False,
        fonts="Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Tenor+Sans", display="'Cormorant Garamond', serif", body="'Tenor Sans', sans-serif",
        css=":root{--bg:#FAFAF8;--bg2:#F1F0EC;--card:#fff;--ink:#111;--ink2:#4A4A47;--ink3:#8A8984;--line:rgba(17,17,17,.14);--accent:#111;--gold:#E0A800;--radius:0} h1,h2,h3{font-weight:300} .btn{border-radius:0} .size button,.chip{border-radius:0}"),
    "campaign": dict(title="Obiimy Campaign", landing="campaign.html", product="enerhiia", viewer="photos", dark=True,
        fonts="Forum&family=Golos+Text:wght@400;500;600", display="'Forum', serif", body="'Golos Text', sans-serif",
        css=":root{--bg:#0A0A0A;--bg2:#141414;--card:#161616;--ink:#F2EFEA;--ink2:#B9B4AC;--ink3:#7C7871;--line:rgba(242,239,234,.16);--accent:#D9A400;--gold:#D9A400;--radius:0}"),
    "lookbook": dict(title="Obiimy Lookbook", landing="lookbook.html", product="mizh", viewer="photos", dark=False,
        fonts="Playfair+Display:ital,wght@0,400;0,500;1,400&family=Golos+Text:wght@400;500;600", display="'Playfair Display', serif", body="'Golos Text', sans-serif",
        css=":root{--bg:#EDEAE5;--bg2:#E3DFD8;--card:#F6F4F0;--ink:#141414;--ink2:#4B4945;--ink3:#85817B;--line:rgba(20,20,20,.14);--accent:#141414;--gold:#C89B00;--radius:0}"),
    "studio": dict(title="Obiimy Studio", landing="studio.html", product="kolo", viewer="hang", dark=False,
        fonts="Cormorant:ital,wght@0,300;0,400;1,300&family=Onest:wght@300;400;500;600", display="'Cormorant', serif", body="'Onest', sans-serif",
        css=":root{--bg:#F1F0F2;--bg2:#E8E6EB;--card:#fff;--ink:#16151A;--ink2:#4C4955;--ink3:#7D7887;--line:rgba(22,21,26,.12);--accent:#4F3F96;--gold:#C99A00;--radius:0} h1,h2,h3{font-weight:300}"),
    "noir": dict(title="Obiimy Noir", landing="noir.html", product="melodiia", viewer="float", dark=True,
        fonts="Unbounded:wght@200;300;400&family=Onest:wght@300;400;500", display="'Unbounded', sans-serif", body="'Onest', sans-serif",
        css=":root{--bg:#0C0B0F;--bg2:#14121A;--card:#16141C;--ink:#ECE9EF;--ink2:#B4AEBE;--ink3:#7A7386;--line:rgba(236,233,239,.12);--accent:#F2B705;--gold:#F2B705;--radius:0} h1,h2,h3{font-weight:200;letter-spacing:-.01em}"),
    "form": dict(title="Obiimy Form", landing="form.html", product="kolo", viewer="drape", dark=False,
        fonts="Oranienbaum&family=Golos+Text:wght@400;500;600", display="'Oranienbaum', serif", body="'Golos Text', sans-serif",
        css=":root{--bg:#DED9D2;--bg2:#D3CDC5;--card:#ECE8E2;--ink:#1B1A19;--ink2:#4E4A46;--ink3:#807A74;--line:rgba(27,26,25,.14);--accent:#0F4C5C;--gold:#B98A00;--radius:0}"),
    "art": dict(title="Obiimy Silk Atelier", landing="art.html", product="probudzhennia", viewer="float", dark=True,
        fonts="Prata&family=Manrope:wght@400;500;600;700", display="'Prata', serif", body="'Manrope', sans-serif",
        css=":root{--bg:#0B0912;--bg2:#141020;--card:#1B1626;--ink:#F3EEF4;--ink2:#C6BFD0;--ink3:#8B8399;--line:rgba(243,238,244,.14);--accent:#F2B705;--gold:#F2B705;--radius:0}"),
    "garden": dict(title="Obiimy Garden", landing="garden.html", product="probudzhennia", viewer="float", dark=True,
        fonts="Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Onest:wght@300;400;500", display="'Cormorant Garamond', serif", body="'Onest', sans-serif",
        css=":root{--bg:#0C0914;--bg2:#1B1430;--card:#171226;--ink:#F1ECF3;--ink2:#BDB5C9;--ink3:#7F7690;--line:rgba(241,236,243,.14);--accent:#F2B705;--gold:#F2B705;--radius:0} h1,h2,h3{font-weight:300} body{background:radial-gradient(120% 80% at 50% 0%,#1B1430 0%,#0C0914 55%,#070510 100%) fixed}"),
}

BASE_CSS = """
  * { box-sizing: border-box; min-width: 0; }
  html { scroll-behavior: smooth; }
  body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased; overflow-x: hidden; }
  img { max-width: 100%; display: block; }
  a { color: inherit; }
  h1, h2, h3 { font-family: var(--display); font-weight: 400; margin: 0; line-height: 1.08; text-wrap: balance; }
  h1 { font-size: clamp(2.2rem, 4vw, 3.6rem); }
  h2 { font-size: clamp(1.8rem, 3vw, 2.6rem); }
  h3 { font-size: 1.3rem; }
  p { margin: 0; }
  .wrap { width: min(1280px, 100%); margin-inline: auto; padding-inline: clamp(16px, 4vw, 48px); }
  .eyebrow { font-size: .7rem; letter-spacing: .22em; text-transform: uppercase; color: var(--ink3); font-weight: 600; }
  .num { font-variant-numeric: tabular-nums; white-space: nowrap; }
  .btn { display: inline-flex; align-items: center; justify-content: center; gap: 10px; padding: 16px 28px; border-radius: 999px; text-decoration: none; font-weight: 600; font-size: .95rem; border: 1px solid transparent; cursor: pointer; font-family: inherit; transition: transform .2s ease; }
  .btn:hover { transform: translateY(-1px); }
  .btn-gold { background: var(--gold); color: #17151A; }
  .btn-line { border-color: var(--ink); background: transparent; color: var(--ink); }
  a:focus-visible, button:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }

  .bar { background: var(--ink); color: var(--bg); font-size: .78rem; text-align: center; padding: 9px 16px; letter-spacing: .04em; }
  .dark .bar { background: var(--gold); color: #17151A; }
  .nav { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 50; background: color-mix(in srgb, var(--bg) 85%, transparent); backdrop-filter: blur(14px); border-bottom: 1px solid var(--line); }
  .nav .wrap { display: flex; align-items: center; justify-content: space-between; gap: 20px; height: 68px; }
  .logo img { height: 24px; width: auto; }
  .nav-links { display: flex; gap: 24px; font-size: .88rem; font-weight: 500; }
  .nav-links a { text-decoration: none; color: var(--ink2); }
  .nav-links a:hover { color: var(--ink); }
  @media (max-width: 860px) { .nav-links { display: none; } }
  .crumbs { font-size: .78rem; color: var(--ink3); padding-block: 18px 0; display: flex; gap: 10px; flex-wrap: wrap; }
  .crumbs a { text-decoration: none; }
  .crumbs a:hover { color: var(--ink); }

  /* product hero */
  .product { padding-block: clamp(20px, 3vw, 40px) clamp(56px, 8vw, 100px); }
  .product .wrap { display: grid; grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); gap: clamp(28px, 5vw, 72px); align-items: start; }
  .gallery { display: grid; gap: 12px; position: sticky; top: 88px; }
  .main { aspect-ratio: 4 / 5; overflow: hidden; border-radius: var(--radius); background: var(--bg2); position: relative; }
  .main img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 15%; }
  .main canvas { width: 100%; height: 100%; display: block; cursor: grab; touch-action: pan-y; }
  .main canvas.grabbing { cursor: grabbing; }
  .main .hint { position: absolute; left: 14px; bottom: 14px; font-size: .66rem; letter-spacing: .2em; text-transform: uppercase; color: var(--ink3); background: color-mix(in srgb, var(--bg) 70%, transparent); padding: 6px 10px; backdrop-filter: blur(6px); pointer-events: none; }
  .thumbs { display: flex; gap: 10px; }
  .thumbs button { all: unset; cursor: pointer; width: 84px; aspect-ratio: 1; overflow: hidden; border-radius: var(--radius); border: 1.5px solid transparent; background: var(--bg2); }
  .thumbs button img { width: 100%; height: 100%; object-fit: cover; }
  .thumbs button[aria-current="true"] { border-color: var(--ink); }
  .thumbs button.viewer { display: grid; place-items: center; font-size: .62rem; letter-spacing: .16em; text-transform: uppercase; font-weight: 600; color: var(--ink2); text-align: center; line-height: 1.3; }
  .info { display: grid; gap: 18px; }
  .info h1 { margin-top: 6px; }
  .state { font-family: var(--display); font-size: 1.25rem; color: var(--ink2); }
  .pricebox { display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; padding-top: 6px; }
  .price { font-family: var(--display); font-size: 2.2rem; line-height: 1; }
  .old { font-size: 1rem; color: var(--ink3); text-decoration: line-through; }
  .part { font-size: .82rem; color: var(--ink3); }
  .label { font-size: .68rem; letter-spacing: .2em; text-transform: uppercase; color: var(--ink3); font-weight: 600; display: flex; justify-content: space-between; }
  .size { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
  .size button { all: unset; cursor: pointer; display: grid; gap: 2px; padding: 12px 14px; border: 1px solid var(--line); border-radius: var(--radius); text-align: center; }
  .size button b { font-family: var(--display); font-weight: 400; font-size: 1.15rem; }
  .size button small { font-size: .74rem; color: var(--ink3); }
  .size button[aria-pressed="true"] { border-color: var(--ink); background: color-mix(in srgb, var(--ink) 6%, transparent); }
  .toggle { display: flex; gap: 8px; }
  .toggle button { all: unset; cursor: pointer; padding: 9px 14px; border: 1px solid var(--line); border-radius: 999px; font-size: .82rem; font-weight: 500; }
  .toggle button[aria-pressed="true"] { background: var(--ink); color: var(--bg); border-color: var(--ink); }
  .dark .toggle button[aria-pressed="true"], .dark .size button[aria-pressed="true"] { background: var(--gold); color: #17151A; border-color: var(--gold); }
  .buy { display: grid; grid-template-columns: 1fr auto; gap: 10px; }
  .buy .btn-line { padding-inline: 18px; }
  .ship { display: grid; gap: 8px; font-size: .88rem; color: var(--ink2); padding-top: 14px; border-top: 1px solid var(--line); }
  .ship span { display: flex; gap: 10px; align-items: baseline; }
  .ship span::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--gold); flex: none; transform: translateY(-2px); }
  .acc details { border-top: 1px solid var(--line); }
  .acc details:last-child { border-bottom: 1px solid var(--line); }
  .acc summary { cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; padding: 14px 0; font-family: var(--display); font-size: 1.1rem; }
  .acc summary::-webkit-details-marker { display: none; }
  .acc summary::after { content: "+"; color: var(--ink3); font-size: 1.4rem; line-height: 1; }
  .acc details[open] summary::after { content: "–"; }
  .acc p, .acc ul { color: var(--ink2); font-size: .92rem; padding-bottom: 14px; margin: 0; }
  .acc ul { padding-left: 18px; display: grid; gap: 4px; }
  @media (max-width: 860px) { .product .wrap { grid-template-columns: 1fr; } .gallery { position: static; } }

  section.block { padding-block: clamp(56px, 8vw, 100px); border-top: 1px solid var(--line); }
  .head { display: grid; gap: 10px; max-width: 40em; margin-bottom: clamp(24px, 3vw, 40px); }
  .story { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(28px, 5vw, 72px); align-items: center; }
  .story figure { margin: 0; aspect-ratio: 1; overflow: hidden; border-radius: var(--radius); }
  .story img { width: 100%; height: 100%; object-fit: cover; }
  .story p.txt { color: var(--ink2); font-size: 1.05rem; margin-top: 16px; }
  blockquote { margin: 22px 0 0; font-family: var(--display); font-size: clamp(1.2rem, 1.8vw, 1.5rem); line-height: 1.4; border-left: 2px solid var(--gold); padding-left: 18px; }
  @media (max-width: 860px) { .story { grid-template-columns: 1fr; } }
  .wear { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
  .wear figure { margin: 0; display: grid; gap: 10px; }
  .wear .ph { aspect-ratio: 3 / 4; overflow: hidden; border-radius: var(--radius); background: var(--bg2); }
  .wear img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 15%; }
  .wear figcaption { font-family: var(--display); font-size: 1.15rem; }
  @media (max-width: 640px) { .wear { grid-template-columns: 1fr 1fr; } }
  .pair { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(28px, 5vw, 72px); align-items: center; }
  .pair .two { position: relative; aspect-ratio: 1; }
  .pair .two figure { position: absolute; margin: 0; width: 70%; aspect-ratio: 1; overflow: hidden; box-shadow: 0 40px 80px -30px rgba(0,0,0,.5); }
  .pair .two img { width: 100%; height: 100%; object-fit: cover; }
  .pair .two .f { left: 0; top: 0; z-index: 2; transform: rotate(-4deg); }
  .pair .two .b { right: 0; bottom: 0; transform: rotate(5deg); }
  .pair .two figcaption { position: absolute; left: 10px; bottom: 8px; font-size: .64rem; letter-spacing: .16em; text-transform: uppercase; font-weight: 700; background: rgba(0,0,0,.6); color: #fff; padding: 4px 8px; }
  @media (max-width: 860px) { .pair { grid-template-columns: 1fr; } }
  .specs { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background: var(--line); border: 1px solid var(--line); }
  .specs div { background: var(--card); padding: 22px; display: grid; gap: 4px; }
  .specs b { font-family: var(--display); font-weight: 400; font-size: 1.15rem; }
  .specs span { font-size: .88rem; color: var(--ink2); }
  @media (max-width: 860px) { .specs { grid-template-columns: 1fr 1fr; } }
  .trust { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, .8fr); gap: 18px; }
  .card { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 24px; display: grid; gap: 10px; align-content: start; }
  .stars { color: var(--gold); letter-spacing: .1em; font-size: .9rem; }
  .who { font-size: .8rem; color: var(--ink3); }
  .card dl { margin: 0; display: grid; gap: 8px; font-size: .9rem; }
  .card dt { font-size: .66rem; letter-spacing: .16em; text-transform: uppercase; color: var(--ink3); font-weight: 600; }
  .card dd { margin: 0; color: var(--ink2); }
  @media (max-width: 860px) { .trust { grid-template-columns: 1fr; } }
  .related { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
  .rel { display: grid; gap: 8px; text-decoration: none; }
  .rel .ph { aspect-ratio: 1; overflow: hidden; border-radius: var(--radius); background: #fff; }
  .rel img { width: 100%; height: 100%; object-fit: cover; transition: transform .6s ease; }
  .rel:hover img { transform: scale(1.04); }
  .rel b { font-weight: 600; font-size: .92rem; }
  .rel span { font-size: .78rem; color: var(--ink3); }
  .rel .p { font-family: var(--display); font-size: 1.1rem; color: var(--ink); }
  @media (max-width: 860px) { .related { grid-template-columns: 1fr 1fr; } }
  footer { border-top: 1px solid var(--line); padding-block: 26px calc(90px + env(safe-area-inset-bottom, 0px)); font-size: .82rem; color: var(--ink3); }
  footer .wrap { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px 24px; }
  footer a { text-decoration: none; color: var(--ink2); }
  @media (min-width: 861px) { footer { padding-bottom: 26px; } }
  .sticky { display: none; }
  @media (max-width: 860px) { .sticky { display: grid; grid-template-columns: 1fr auto; gap: 10px; position: fixed; left: 12px; right: 12px; bottom: calc(12px + env(safe-area-inset-bottom, 0px)); z-index: 60; background: rgba(23,21,25,.92); backdrop-filter: blur(10px); border-radius: 999px; padding: 8px 8px 8px 18px; color: #fff; align-items: center; } .sticky .t { font-size: .8rem; line-height: 1.25; } .sticky .t b { display: block; font-weight: 600; } .sticky a { background: var(--gold); color: #17151A; text-decoration: none; font-weight: 600; font-size: .82rem; padding: 11px 16px; border-radius: 999px; white-space: nowrap; } }
"""

def price(n): return f"{n:,}".replace(",", " ") + " грн"

def build(skin_key, skin):
    p = PRODUCTS[skin["product"]]
    dark = skin["dark"]
    logo = "brand/logo-white.png" if dark else "brand/logo-ink.png"
    viewer = skin["viewer"]
    sizes_js = json.dumps([{"s": s, "one": one, "two": two} for s, one, two in p["sizes"]], ensure_ascii=False)
    sale_js = json.dumps(p["sale"], ensure_ascii=False)
    # gallery
    thumbs = ""
    if viewer != "photos":
        thumbs += '<button type="button" class="viewer" data-i="-1" aria-current="true">3D<br>шовк</button>'
    for i, ph in enumerate(p["photos"]):
        cur = "true" if (viewer == "photos" and i == 0) else "false"
        thumbs += f'<button type="button" data-i="{i}" aria-current="{cur}"><img src="{ph}" alt=""></button>'
    main_first = p["photos"][0]
    canvas = '<canvas id="silk" aria-label="Тривимірна хустка з цим принтом. Потягніть за тканину."></canvas><span class="hint">Потягніть за тканину</span>' if viewer != "photos" else ""
    main = f'<div class="main" id="main">{canvas}<img id="mainImg" src="{main_first}" alt="Хустка «{p["name"]}»" {"hidden" if viewer != "photos" else ""}></div>'
    size_buttons = "".join(
        f'<button type="button" data-i="{i}" aria-pressed="{"true" if i == p["default"] else "false"}"><b class="num">{s}</b><small class="num">{price(one)}</small></button>'
        for i, (s, one, two) in enumerate(p["sizes"]))
    toggle = ('<div><p class="label">Друк</p><div class="toggle" id="side" style="margin-top:8px"><button type="button" data-v="one" aria-pressed="true">Односторонній</button>'
              '<button type="button" data-v="two" aria-pressed="false">Двосторонній · зворот «' + p["backname"] + '»</button></div></div>') if p["double"] else ""
    d0 = p["sizes"][p["default"]]
    pair = ""
    if p["double"]:
        pair = f'''
  <section class="block"><div class="wrap pair">
    <div><p class="eyebrow">Двосторонній друк</p><h2 style="margin-top:10px">Один вузол. Два образи.</h2><p class="story" style="display:block;color:var(--ink2);margin-top:14px;max-width:32em">Друк на обох боках шовку: лицем — «{p["name"]}», зворотом — «{p["backname"]}». Перевернули хустку — і на плечах уже інший принт. Двосторонні хустки 44 × 44 від 2 400 грн, 65 × 65 від 4 800 грн.</p></div>
    <div class="two"><figure class="f"><img src="tex/{p["tex"]}.jpg" alt="Лице"><figcaption>Лице</figcaption></figure><figure class="b"><img src="tex/{p["back"]}.jpg" alt="Зворот"><figcaption>Зворот</figcaption></figure></div>
  </div></section>'''
    wear = "".join(f'<figure><div class="ph"><img src="{src}" alt="{cap}" loading="lazy"></div><figcaption>{cap}</figcaption></figure>' for cap, src in p["wear"])
    related = "".join(f'<a class="rel" href="{u}"><div class="ph"><img src="{im}" alt="" loading="lazy"></div><b>{n}</b><span>{s}</span><span class="p num">{pr}</span></a>' for n, s, pr, im, u in RELATED)
    engine = ""
    if viewer != "photos":
        opts = {
            "hang": "mode: 'hang', size: 1.5, resolution: 34, camDist: 4.2, camY: -0.05, groundShadow: true, groundY: -1.25, envTop: '#ffffff', envBottom: '#B9B4C2', gloss: 0.32, aniso: 0.9, envStrength: 0.45, weaveScale: 0.4, wind: [1.1, 0.05, 0.8], idleSway: 0.06",
            "float": "mode: 'float', size: 1.6, resolution: 34, camDist: 4.6, rotate: true, rotY: 0.3, tiltX: 0.1, envTop: '#FFFFFF', envBottom: '#0C0B0F', envTint: '#FFF1C2', gloss: 0.28, aniso: 1.0, envStrength: 0.22, weaveScale: 0.5, idleSway: 0.25",
            "drape": "mode: 'drape', size: 1.9, resolution: 38, camDist: 6.0, camY: -0.15, sphereRadius: 0.48, sphereY: 0.15, formColor: '#CFC8BF', rotate: true, rotY: 0.2, gravity: -7, envTop: '#FFFFFF', envBottom: '#9A938A', envTint: '#FFF6DD', gloss: 0.34, aniso: 0.9, envStrength: 0.45, weaveScale: 0.4, idleSway: 0.1",
        }[viewer]
        back = p["back"] or p["tex"]
        engine = f'''
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
{ENGINE}
</script>
<script>
(function () {{
  var silk = window.SilkEngine && SilkEngine.create({{ canvas: document.getElementById('silk'), texPath: 'tex/', front: '{p["tex"]}', back: '{back}', {opts} }});
  if (!silk) {{ document.getElementById('silk').hidden = true; document.getElementById('mainImg').hidden = false; }}
  window.__silk = silk;
}})();
</script>'''
    html = f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{skin["title"]} · {p["name"]}</title>
<meta name="description" content="Шовкова хустка «{p["name"]}» Obiimy: 100% італійський шовк, авторський принт, {d0[0]} см, {price(d0[1])}. Відправка того ж дня, оплата частинами.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={skin["fonts"]}&display=swap">
<style>
  {skin["css"]}
  :root {{ --display: {skin["display"]}; --body: {skin["body"]}; color-scheme: {"dark" if dark else "light"}; }}
{BASE_CSS}
</style>
<body class="{"dark" if dark else "light"}">
<div class="bar">Замовлення до 16:00 відправляємо того ж дня · Безкоштовна доставка від 5 000 грн · Оплата частинами</div>
<header class="nav"><div class="wrap">
  <a class="logo" href="{skin["landing"]}" aria-label="Obiimy"><img src="{logo}" alt="Obiimy"></a>
  <nav class="nav-links"><a href="{skin["landing"]}">Лендинг</a><a href="https://obiimy.world/khustky/">Хустки</a><a href="https://obiimy.world/tvilli/">Твіллі</a><a href="https://obiimy.world/podarunkovi-nabory/">Подарунки</a></nav>
  <a class="btn btn-gold" style="padding:10px 16px;font-size:.8rem" href="https://obiimy.world/khustky/">Каталог</a>
</div></header>

<main>
  <div class="wrap"><nav class="crumbs"><a href="{skin["landing"]}">Obiimy</a><span>/</span><a href="https://obiimy.world/khustky/">Хустки</a><span>/</span><span>«{p["name"]}»</span></nav></div>
  <section class="product">
    <div class="wrap">
      <div class="gallery">
        {main}
        <div class="thumbs" id="thumbs">{thumbs}</div>
      </div>
      <div class="info">
        <div><p class="eyebrow">Колекція «{p["collection"]}» · арт. {p["sku"]}</p><h1>Шовкова хустка «{p["name"]}»</h1><p class="state">{p["state"]}</p></div>
        <div class="pricebox"><span class="price num" id="price">{price(p["sale"].get(d0[0], d0[1]))}</span><span class="old num" id="old" {"" if d0[0] in p["sale"] else "hidden"}>{price(d0[1])}</span><span class="part num" id="part"></span></div>
        <div><p class="label"><span>Розмір</span><a href="#sizes" style="font-weight:500;letter-spacing:0;text-transform:none">Який обрати?</a></p><div class="size" id="size" style="margin-top:8px">{size_buttons}</div></div>
        {toggle}
        <div class="buy"><a class="btn btn-gold" id="buy" href="{p["url"]}">Купити</a><a class="btn btn-line" href="{p["url"]}">У бажання</a></div>
        <div class="ship"><span>Замовлення до 16:00 — відправка того ж дня Новою поштою</span><span>Безкоштовна доставка від 5 000 грн</span><span id="upsell" hidden>+ резинка 700 грн = безкоштовна доставка</span><span>Підпис на подарунок за вашим текстом</span></div>
        <div class="acc">
          <details open><summary>Матеріал і друк</summary><p>100% італійський шовк, високоякісний цифровий друк. Обробка вручну, тому розмір може відхилятися на 0–2,5 см. Індивідуальне пакування. Країна виробник — Україна.</p></details>
          <details><summary>Догляд</summary><ul><li>Суха чистка або ручне прання при температурі до 30°</li><li>Не віджимати, сушити в тіні</li><li>Прасування в режимі «шовк» через тонку тканину</li></ul></details>
          <details><summary>Оплата і повернення</summary><p>Оплата карткою онлайн або частинами: 4 платежі від ПриватБанку чи 3 від monobank. Умови обміну та повернення — на сторінці <a href="https://obiimy.world/obmin-ta-povernennya/">Обмін та повернення</a>.</p></details>
        </div>
      </div>
    </div>
  </section>

  <section class="block"><div class="wrap story">
    <div><p class="eyebrow">Спершу картина</p><h2 style="margin-top:10px">Історія принту</h2><p class="txt">{p["story"]}</p><blockquote>{p["quote"]}</blockquote></div>
    <figure><img src="tex/{p["tex"]}.jpg" alt="Принт «{p["name"]}» крупно" loading="lazy"></figure>
  </div></section>
  {pair}
  <section class="block" id="sizes"><div class="wrap">
    <div class="head"><p class="eyebrow">Розміри</p><h2>Один принт, три способи носити</h2></div>
    <div class="specs">
      <div><b class="num">44 × 44</b><span>Паше: на сумку, зап’ястя, у кишеню</span><span class="num">від 1 600 грн</span></div>
      <div><b class="num">65 × 65</b><span>Класика: на шию, у волосся, на пояс</span><span class="num">від 3 200 грн</span></div>
      <div><b class="num">88 × 88</b><span>Шаль: на плечі, як топ, тюрбан</span><span class="num">від 4 400 грн</span></div>
      <div><b>2D</b><span>Двосторонній друк: два принти на одній хустці</span><span class="num">від 2 400 грн</span></div>
    </div>
  </div></section>
  <section class="block"><div class="wrap">
    <div class="head"><p class="eyebrow">Як носити</p><h2>«{p["name"]}» у трьох образах</h2></div>
    <div class="wear">{wear}</div>
  </div></section>
  <section class="block"><div class="wrap">
    <div class="head"><p class="eyebrow">Довіра</p><h2>Відгук і партнери</h2></div>
    <div class="trust">
      <div class="card"><span class="stars">★★★★★</span><p>«{REVIEW[0]}»</p><span class="who">{REVIEW[1]}</span></div>
      <div class="card"><dl><div><dt>Ритейл</dt><dd>INTERTOP, Hram, Be Brave (Канада), UFD London</dd></div><div><dt>Преса</dt><dd>LIGA.net, INSIDER UA</dd></div><div><dt>Рейтинг</dt><dd>5.0 за відгуками покупців на obiimy.world</dd></div></dl></div>
    </div>
  </div></section>
  <section class="block"><div class="wrap">
    <div class="head"><p class="eyebrow">Поруч</p><h2>Вам також сподобається</h2></div>
    <div class="related">{related}</div>
  </div></section>
</main>
<footer><div class="wrap"><span>© Obiimy. Художниця та засновниця — Світлана Сніжко.</span><span><a href="https://obiimy.world/pro-nas/">Про нас</a> · <a href="https://obiimy.world/oplata-i-dostavka/">Доставка</a> · <a href="https://www.instagram.com/obiimy.world/">Instagram</a></span></div></footer>
<div class="sticky"><div class="t"><b id="stickyPrice">{price(p["sale"].get(d0[0], d0[1]))}</b><span>«{p["name"]}» · <span id="stickySize">{d0[0]}</span></span></div><a href="{p["url"]}">Купити</a></div>
{engine}
<script>
(function () {{
  var SIZES = {sizes_js}, SALE = {sale_js}, side = 'one', cur = {p["default"]};
  var priceEl = document.getElementById('price'), oldEl = document.getElementById('old'), partEl = document.getElementById('part'), upsell = document.getElementById('upsell'), sp = document.getElementById('stickyPrice'), ss = document.getElementById('stickySize');
  function fmt(n) {{ return String(n).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ' ') + ' грн'; }}
  function render() {{
    var s = SIZES[cur], base = side === 'two' && s.two ? s.two : s.one, sale = side === 'one' && SALE[s.s] ? SALE[s.s] : null;
    var final = sale || base;
    priceEl.textContent = fmt(final); oldEl.hidden = !sale; oldEl.textContent = fmt(base);
    partEl.textContent = 'або 4 × ' + fmt(Math.round(final / 4)) + ' частинами';
    upsell.hidden = !(final + 700 >= 5000 && final < 5000);
    sp.textContent = fmt(final); ss.textContent = s.s;
    document.querySelectorAll('#size button').forEach(function (b, i) {{ b.setAttribute('aria-pressed', i === cur ? 'true' : 'false'); b.querySelector('small').textContent = fmt(side === 'two' && SIZES[i].two ? SIZES[i].two : SIZES[i].one); b.disabled = side === 'two' && !SIZES[i].two; b.style.opacity = b.disabled ? .4 : 1; }});
  }}
  document.querySelectorAll('#size button').forEach(function (b) {{ b.addEventListener('click', function () {{ cur = +b.dataset.i; render(); }}); }});
  var sideEl = document.getElementById('side');
  if (sideEl) sideEl.querySelectorAll('button').forEach(function (b) {{ b.addEventListener('click', function () {{ side = b.dataset.v; sideEl.querySelectorAll('button').forEach(function (x) {{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }}); if (side === 'two' && !SIZES[cur].two) cur = 1; render(); if (window.__silk && side === 'two') window.__silk.flip(); }}); }});
  render();
  var mainImg = document.getElementById('mainImg'), canvas = document.getElementById('silk');
  document.querySelectorAll('#thumbs button').forEach(function (b) {{
    b.addEventListener('click', function () {{
      document.querySelectorAll('#thumbs button').forEach(function (x) {{ x.setAttribute('aria-current', x === b ? 'true' : 'false'); }});
      var i = +b.dataset.i;
      if (i < 0) {{ if (canvas) canvas.hidden = false; mainImg.hidden = true; }}
      else {{ if (canvas) canvas.hidden = true; mainImg.hidden = false; mainImg.src = b.querySelector('img').src; }}
    }});
  }});
}})();
</script>
'''
    (OUT / f"p-{skin_key}.html").write_text(html)
    print("p-" + skin_key, len(html) // 1024, "KB")

for k, v in SKINS.items():
    build(k, v)
