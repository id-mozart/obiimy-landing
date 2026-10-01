#!/usr/bin/env python3
"""PDF presentation for HR: «Подарунки для команди» — team-deck.html (A4 landscape) -> obiimy-podarunky-dlia-komandy.pdf via headless Chrome.
Design system (01.10, evening): photos bleed to the page edge, Playfair Display + Tenor Sans, cream #F1EFEA / black #0E0E0E pages,
pale-gold accent #E7D9A6 on dark pages (as in the SOLO banners), a running folio. Pages:
cover · brand · three reasons · SOLO manifesto (dark) · SOLO seven prints (dark) · how to wear (dark, like the t05 banner) ·
four tiers · four set pages (editorial mosaics) · the whole range · personalisation · contacts (QR).
Data and facts come from build-b2b-team-main.py (PERKS, SOLO, TIERS, ASSORT, PERS, SETS4, WAYS); retail prices from obiimy.world."""
import importlib.util, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
sys.path.insert(0, str(ROOT))
from imgs import typo
_spec = importlib.util.spec_from_file_location("main", ROOT / "build-b2b-team-main.py")
main = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(main)
PERKS, SOLO, TIERS, ASSORT, PERS, SETS4, WAYS, price, qr_svg, cast = main.PERKS, main.SOLO, main.TIERS, main.ASSORT, main.PERS, main.SETS4, main.WAYS, main.price, main.qr_svg, main.cast
CARD_PH, CARD_POS = main.CARD_PH, main.CARD_POS
def cp(slot, f, pos="", cls=""):
    ff, pp = cast(slot, f, pos); return pic(ff, cls, pp)
team = main.team
PHONE, MAIL, SHOWROOM = team.PHONE, team.MAIL, team.SHOWROOM
LANDING = "https://obiimy-landing-production.up.railway.app/b2b-team-main"

def pic(src, cls="", pos=""):
    from PIL import Image
    p = pathlib.Path(src); lb = OUT / "review" / "lb"; lb.mkdir(parents=True, exist_ok=True)
    j = lb / (p.stem + ".jpg")
    if not j.exists():
        im = Image.open(OUT / src).convert("RGB"); im.thumbnail((1200, 1200)); im.save(j, quality=72, optimize=True)
    st = f' style="object-position:{pos}"' if pos else ""
    return f'<img src="review/lb/{j.name}" class="{cls}" alt=""{st}>'

PAGES = []
def page(html, cls=""):
    n = len(PAGES) + 1
    folio = "" if "cover" in cls else f'<p class="folio"><span>Obiimy · подарунки для команди</span><span>{n:02d}</span></p>'
    PAGES.append(f'<section class="pg {cls}">{html}{folio}</section>')

# 1 cover: full-page photo, logo and title bottom-left, three facts in one line
page(f'''<div class="fullp cv">{cp("D01", "photo/solo/zolote-44-5.webp", "50% 22%", "full")}<div class="fullp-t cov-t"><img src="brand/logo-white.png" class="logo" alt="Obiimy">
  <p class="eb">Для HR і офіс-менеджерів · 2026</p><h1>Подарунки<br>для команди</h1><p class="it">Авторські принти на натуральному італійському шовку</p>
  <p class="cov-line">Чотири рівні від 1 600 грн на людину · пакування й наліпка з вашим логотипом — безкоштовно · нова колекція SOLO</p>
  <p class="toc">Рівні й ціни — 10 · Набори — 11–14 · Асортимент — 15 · Персоналізація — 16 · Запит — 17</p></div></div>''', "cover nopad")

# 2 about I — full-page photo with the brand manifesto
page(f'''<div class="fullp">{cp("D02", "photo/solo/puls-44-5.webp", "50% 30%", "full")}<div class="fullp-t">
  <p class="eb">Про бренд</p><h1>Обійми з шовку</h1>
  <p>Український бренд шовкових аксесуарів із Києва. Засновниця й художниця — Світлана Сніжко: кожен принт — авторський. Хустки, твіллі, резинки, маски для сну, аксесуари для дому.</p>
  <p class="quote-l">«Кожна коробочка — це обійми, що нагадують: ти варта краси»</p>
</div></div>''', "cover nopad")

# 3 about II — the brand in facts: four photo tiles and a numbers strip
FACTS = [
    ("Авторські принти", "Засновниця й художниця — Світлана Сніжко; принти — її та українських художниць. П’ять колекцій.", "photo/vyr-flat.webp", "50% 50%"),
    ("Італійський шовк", "Лише 100% натуральний шовк; кутики кожної хустки кравчині обробляють вручну.", "photo/dotyk-3.webp", "50% 40%"),
    ("Зроблено в Україні", "Бренд заснований під час війни; повністю українське виробництво, благодійні ініціативи.", "photo/box-gold.jpg", "50% 50%"),
    ("«Співоча душа»", "Колекція присвячена рідкісним птахам: частина коштів іде на гнізда для сиворакші з Червоної книги.", "img/melodiia.webp", "50% 30%"),
]
facts = "".join(f'<figure class="fact">{cp("D03" + "abcd"[i], ph, pos)}<figcaption><b>{t}</b><span>{d}</span></figcaption></figure>' for i, (t, d, ph, pos) in enumerate(FACTS))
page(f'''<div class="hd"><div><p class="eb">Бренд у фактах</p><h2>Що стоїть за кожною коробкою Obiimy</h2></div><p class="hd-r">Шовк Obiimy продають INTERTOP і Hram в Україні, Be Brave у Канаді, UFD London. Про бренд писали LIGA.net та INSIDER UA. Шоурум — Київ, Сагайдачного, 12.</p></div>
<div class="facts">{facts}</div>
<div class="nums"><div><b>100%</b><span>натуральний італійський шовк</span></div><div><b>5</b><span>авторських колекцій</span></div><div><b>38</b><span>принтів твіллі на вибір</span></div><div><b>45</b><span>готових подарункових наборів на obiimy.world</span></div></div>''')

# 3 three reasons
adv = "".join(f'<div class="adv-i"><b>0{i + 1}</b><div><h3>{b}</h3><p>{t}</p></div></div>' for i, (b, t) in enumerate(PERKS[:3]))
page(f'''<div class="split r"><div class="txt adv-t"><p class="eb">Чому ми</p><h2>Три причини обрати шовк Obiimy</h2>{adv}</div>{cp("D04", "photo/solo/avantiura-tw-1.webp", "50% 15%", "ph")}</div>''', "nopad fr")

# 4 SOLO I — manifesto on black
page(f'''<div class="solo1"><div class="txt"><p class="eb">Нова колекція · 2026</p><h1>SOLO.<br>Шлях до себе</h1><p class="it gold">Шовкова свобода: жіноча сила крізь десятиліття</p>
  <p>У 40-х жінка підкреслювала силу бездоганною елегантністю — за м’якістю шовку ховався характер. У 50-х правила почали руйнуватися: колір, форма, власна ідентичність. Змінювалися епохи й силуети, а хустка залишалася поруч — як символ жіночності, що не суперечить силі.</p>
  <p>SOLO — історія про шлях жінки до себе. Сім авторських принтів — сім етапів цієї подорожі. Натуральний шовк, двосторонній друк, натхнення — обкладинки модних журналів 40–50-х.</p>
  <p class="team">Для команди: кожному — свій принт, під стан, який хочете побажати, або один на всіх. Сім принтів — на наступній сторінці.</p></div>
<div class="solo1-ph">{cp("D05a", "photo/solo/tysha-88-2.webp", "", "big")}{cp("D05b", "photo/solo/puls-44-4.webp", "50% 20%")}{cp("D05c", "photo/solo/iskra-65-3.webp", "50% 50%")}</div></div>''', "dark nopad fr2")

# 5 SOLO II — the seven prints as tall cards (model shot, flat-lay inset, name, state, format · price)
cards = "".join(f'<div class="pc">{pic(CARD_PH[i], "m", CARD_POS[i])}<div class="pc-t">{pic(fl, "fl")}<b>{n}</b><span>{st}</span><small>{fm}</small></div></div>' for i, (n, st, fm, pr, ph, fl) in enumerate(SOLO))
page(f'''<div class="hd"><div><p class="eb">Колекція SOLO</p><h2>Сім принтів — сім станів</h2></div><p class="hd-r">Для HR стан принта — готовий текст привітання: «Сміливий крок» — на підвищення, «Тиша всередині» — після складного кварталу. Ціни роздрібні, двосторонній друк.</p></div>
<div class="pcs">{cards}</div>''', "dark")

# SOLO — full-page quote spread from the press release
page(f'''<div class="fullp q">{cp("D07", "photo/solo/zolote-44-4.webp", "50% 35%", "full")}<div class="fullp-q">
  <p class="bigq">«Я є. Я продовжую жити.<br>Я обираю себе»</p>
  <p>Для жінки краса — це спосіб зберегти себе. Улюблена сукня, шовкова хустка, червона помада — маленькі акти свободи.</p>
  <p class="eb">SOLO. Шлях до себе · хустка «Золоте світло» 44 × 44</p>
</div></div>''', "cover nopad")

# 6 how to wear — like the brand banner: one print, four ways, italic labels on the photo
ways = "".join(f'<figure class="way">{pic(ph, "", pos)}<figcaption><b>{n}</b><span>{t}</span></figcaption></figure>' for n, t, ph, pos in WAYS)
page(f'''<div class="hd"><div><p class="eb">Як носити</p><h2>Один принт — чотири образи</h2></div><p class="hd-r">Хустка «Авантюра» 88 × 88 з двостороннім друком — 6 600 грн. Так само носять будь-яку хустку чи твіллі з каталогу. Для команди: один принт на всіх — і жодних однакових образів.</p></div>
<div class="ways">{ways}</div>''', "dark wayspg")

# chapter opener — gifts
page(f'''<div class="fullp op">{cp("D09", "photo/solo/puls-44-3.webp", "50% 30%", "full")}<div class="fullp-t">
  <p class="eb">Подарунки для команди</p><h1>Від стрічки<br>до майстер-класу</h1>
  <p>Чотири рівні подарунка за роздрібними цінами obiimy.world. Пакування й наліпка з вашим логотипом — безкоштовно. Кожному в команді — свій принт.</p>
</div></div>''', "cover nopad")

# 7 four tiers — editorial: photo bleeding left, four rows with product thumbs and price breakdown
rows = "".join(f'<div class="tr">{pic(ph)}<div><p class="eb">{lb}</p><b>{n}</b><span>{t}</span><small>{note}</small></div><em>{pr}</em></div>' for (lb, n, t, pr, note, ph), S in zip(TIERS, SETS4))
page(f'''<div class="split l">{cp("D10", "photo/solo/krok-tw-2.webp", "50% 20%", "ph")}<div class="txt tiers">
  <p class="eb">Ціновий діапазон</p><h2>Чотири рівні подарунка — від 1 600 до 3 200 грн за речі</h2>
  <div class="ta-l">{rows}</div>
  <p class="foot">Команді з 50 людей — 80 000–160 000 грн, зі 100 — 160 000–320 000 грн за речі за роздрібними цінами; доставку й майстер-клас рахуємо окремо. <b>Чоловікам у команді</b> — сертифікат 1 000–4 000 грн, маска для сну, наволочка або закладка: змішану команду рахуємо в одному розрахунку.</p>
</div></div>''', "nopad fl")

PROD = main.PROD
# four sets on one page — four columns bleeding to the edges, italic name on the photo, product chip with the price (as in the SOLO creatives)
CHIP_PH = [cast(f"P{i + 1}", S["gal"][PROD[i]][0])[0] for i, S in enumerate(SETS4)]
cols = "".join(f'''<div class="fs">{pic(S["tier"][0], "", S["tier"][1])}<div class="fs-t"><p class="eb">0{i + 1} · {lb}</p><b>{n}</b></div>
<div class="chip">{pic(CHIP_PH[i], "chip-ph")}<div><span>{S["short"]}</span><em>{pr}</em></div></div></div>''' for i, ((lb, n, t, pr, note, ph), S) in enumerate(zip(TIERS, SETS4)))
page(f'''<div class="fs-hd"><p class="eb">Чотири подарунки</p><h2>Від стрічки до набору з майстер-класом</h2></div><div class="fss">{cols}</div>''', "dark fourpg nopad")

# 8–11 one page per set: editorial mosaic bleeding to the page edge
KEEP = ("Що всередині", "Шовк", "Шовк і друк", "Майстер-клас", "Пакування", "Кому")
M1POS = ["50% 12%", "50% 8%", "50% 30%", "50% 18%"]
for i, S in enumerate(SETS4):
    hp, ha, hpos = S["hero"]; g2 = S["gal"][0]; g3 = S["gal"][PROD[i]]
    kv = "".join(f'<div><span>{k}</span><span>{v}</span></div>' for k, v in S["inside"] if k in KEEP)
    ways = "".join(f'<div><b>{h}</b>{t}</div>' for h, t in S["ways"])
    page(f'''<div class="set{" rev" if i % 2 else ""}"><div class="mos">{pic(hp, "m1", hpos if f"H{i + 1}" in main.load("cast").CAST else M1POS[i])}{pic(g2[0], "m2", g2[2])}{pic(g3[0], "m3", g3[2])}</div>
<div class="set-t"><p class="eb">{S["lb"]}</p><h2>{S["name"]}</h2><p class="sub">{S["lead"]}</p>
<p class="rrp">{S["pr"]}<small>{S["prnote"]}</small></p>
<div class="kv">{kv}</div>
<div class="ways4">{ways}</div>
<p class="who">{S["who"]}</p></div></div>''', "setp nopad")

# 12 the whole range — white page, products float without frames
tiles = "".join(f'<figure>{pic(ph)}<figcaption><b>{n}</b><span>від {price(pr)}</span></figcaption></figure>' for n, pr, ph in ASSORT)
page(f'''<div class="hd"><div><p class="eb">Асортимент</p><h2>Усе, з чого можна зібрати подарунок</h2></div><p class="hd-r">Роздрібні ціни obiimy.world, «від» — найдешевший формат чи принт. Будь-яку річ можна зробити подарунком або додати в коробку.</p></div>
<div class="grid6">{tiles}</div>
<p class="foot"><b>Чоловікам у команді</b> — сертифікат Obiimy на 1 000–4 000 грн (електронний або фізичний, на будь-який товар), маска для сну, наволочка або закладка — зберемо в один розрахунок.</p>''', "white")

# 13 personalisation
def terms(i, tm): return '<p class="free">Безкоштовно</p><p class="nt">у кожному корпоративному замовленні</p>' if i == 0 else f'<p class="nt">{tm}</p>'
pers = "".join(f'<div class="per"><b>0{i + 1}</b><h3>{n}</h3><p>{t}</p>{terms(i, tm)}</div>' for i, (n, t, tm, ph) in enumerate(PERS))
page(f'''<div class="hd"><div><p class="eb">Персоналізація</p><h2>Подарунок із вашим логотипом — чотири рівні</h2></div><p class="hd-r">Перший рівень — безкоштовно в кожному корпоративному замовленні. Решта — залежно від строків: що встигаємо до вашої дати й скільки це коштує, пишемо в розрахунку.</p></div>
<div class="grid4p">{pers}</div>
<div class="per-ph">{cp("D16", "photo/box-gold.jpg", "50% 45%")}</div>
<p class="foot">Подарункове пакування Obiimy; наліпка з вашим логотипом — усередині коробки. Як виглядатиме наліпка чи бирка — покажемо в добірці.</p>''')

# 14 contacts
page(f'''<div class="split r"><div class="txt"><p class="eb">Запит</p><h2>Напишіть — надішлемо добірку й розрахунок</h2>
  <ol class="steps"><li><b>Нагода, кількість, дата.</b> Цього досить для першого листа.</li><li><b>Добірка й розрахунок</b> окремими рядками: речі, персоналізація, доставка. Чи встигаємо до вашої дати — пишемо одразу.</li><li><b>Відправка</b> Новою поштою в день замовлення до 16:00 — в офіс однією посилкою або кожному окремо; безкоштовно від 5 000 грн за відправку, адресні відправки кожному — у розрахунку.</li></ol>
  <p class="cond">Оплата й документи для юридичної особи, мінімальна кількість — уточнимо в розрахунку.</p>
  <div class="qrrow">{qr_svg(LANDING, 110)}<p class="contact"><b>{PHONE}</b><br>Telegram @OBIIMY_sales<br>{MAIL}<br>obiimy.world<br><small>Скануйте — <a href="{LANDING}">сторінка для команд</a> із формою запиту</small></p></div>
  <p class="foot">Шоурум: {SHOWROOM} · пн–пт 10:00–18:00, сб 11:00–18:00</p>
</div>{cp("D17", "photo/solo/krok-tw-3.webp", "50% 30%", "ph")}</div>''', "nopad fr")

html = f'''<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>Obiimy — подарунки для команди 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400;1,500&family=Tenor+Sans&display=swap" rel="stylesheet">
<style>
  @page {{ size: A4 landscape; margin: 0; }}
  * {{ box-sizing: border-box; font-variant-numeric: lining-nums; }}
  html, body {{ margin: 0; background: #F1EFEA; color: #141414; font-family: 'Tenor Sans', sans-serif; font-size: 10.5pt; line-height: 1.5; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .pg {{ width: 297mm; height: 210mm; padding: 16mm 18mm 16mm; page-break-after: always; break-after: page; overflow: hidden; position: relative; display: flex; flex-direction: column; background: #F1EFEA; }}
  .pg.nopad {{ padding: 0; }} .pg.white {{ background: #fff; }}
  .pg.dark {{ background: #0E0E0E; color: #F3F1EC; }} .pg.dark .eb {{ color: #B8B3AA; }} .pg.dark h2, .pg.dark h1 {{ color: #F7F5F0; }}
  h1, h2, h3 {{ font-family: 'Playfair Display', serif; font-weight: 400; margin: 0; line-height: 1.06; letter-spacing: -.012em; }}
  h1 {{ font-size: 44pt; }} h2 {{ font-size: 24pt; margin-bottom: 5mm; }} h3 {{ font-size: 14pt; margin-top: 2mm; }}
  p {{ margin: 0 0 3mm; }}
  .eb {{ font-size: 7.3pt; letter-spacing: .26em; text-transform: uppercase; color: #6B6772; margin-bottom: 2.5mm; }}
  .it {{ font-family: 'Playfair Display', serif; font-style: italic; font-size: 13pt; }}
  .gold {{ color: #E7D9A6; }}
  .sub {{ color: #4A4A47; margin-top: -2mm; margin-bottom: 5mm; max-width: 190mm; }}
  img {{ display: block; object-fit: cover; }}
  .folio {{ position: absolute; left: 18mm; right: 18mm; bottom: 7mm; margin: 0; display: flex; justify-content: space-between; font-size: 6.8pt; letter-spacing: .2em; text-transform: uppercase; color: #8E8A84; }}
  .pg.fl .folio {{ left: 144mm; }} .pg.fr .folio {{ right: 142mm; }} .pg.fr2 .folio {{ right: 162mm; }} .pg.dark .folio {{ color: #6E6A64; }} .pg.setp .folio, .pg.cover .folio {{ display: none; }}
  /* cover */
  .cov {{ display: grid; grid-template-columns: 168mm 1fr; height: 210mm; }}
  .cov .full {{ width: 100%; height: 100%; }}
  .cov-p {{ padding: 16mm 16mm 14mm 14mm; display: flex; flex-direction: column; }}
  .cov-p .logo {{ height: 9mm; width: auto; align-self: flex-start; object-fit: contain; }}
  .cov-m {{ margin: auto 0; }} .cov-m h1 {{ font-size: 42pt; margin: 3mm 0 5mm; }} .cov-m .it {{ color: #4A4A47; font-size: 12.5pt; }}
  .cov-f {{ display: grid; gap: 2.5mm; }} .cov-f div {{ border-top: 1px solid #C9C6C0; padding-top: 2mm; font-size: 8.5pt; color: #6B6772; }} .cov-f b {{ display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 11.5pt; color: #141414; }}
  /* full-page photo pages */
  .fullp {{ position: relative; width: 297mm; height: 210mm; }} .fullp .full {{ width: 100%; height: 100%; }}
  .fullp::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,0,0,.66) 0%, rgba(0,0,0,.3) 48%, rgba(0,0,0,0) 72%), linear-gradient(0deg, rgba(0,0,0,.6) 0%, rgba(0,0,0,0) 52%); }}
  .fullp.q::after {{ background: linear-gradient(0deg, rgba(0,0,0,.7) 0%, rgba(0,0,0,.2) 55%, rgba(0,0,0,0) 100%); }}
  .fullp-t {{ position: absolute; left: 18mm; bottom: 20mm; max-width: 104mm; z-index: 1; color: #fff; }}
  .cov-t {{ max-width: 150mm; bottom: 16mm; }} .cov-t .logo {{ height: 10mm; width: auto; margin-bottom: 10mm; }} .cov-t h1 {{ font-size: 50pt; }} .cov-t .it {{ color: #F3EBD0; }}
  .cov-line {{ font-size: 9.5pt; color: rgba(255,255,255,.9) !important; border-top: 1px solid rgba(255,255,255,.35); padding-top: 3mm; margin-top: 5mm; }} .cov-t .toc {{ font-size: 7pt; letter-spacing: .08em; color: rgba(255,255,255,.6) !important; margin: 2mm 0 0; }}
  .fullp.cv::after {{ background: linear-gradient(90deg, rgba(0,0,0,.6) 0%, rgba(0,0,0,.25) 50%, rgba(0,0,0,0) 75%), linear-gradient(0deg, rgba(0,0,0,.62) 0%, rgba(0,0,0,0) 55%); }}
  .fullp-t .eb {{ color: rgba(255,255,255,.78); }} .fullp-t h1 {{ font-size: 40pt; margin: 1mm 0 5mm; }} .fullp-t p {{ color: rgba(255,255,255,.92); font-size: 10.5pt; }}
  .quote-l {{ font-family: 'Playfair Display', serif; font-style: italic; font-size: 15pt; line-height: 1.3; color: #F3EBD0 !important; margin-top: 4mm; }}
  .fullp-q {{ position: absolute; left: 18mm; right: 18mm; bottom: 18mm; z-index: 1; color: #fff; text-align: center; }}
  .bigq {{ font-family: 'Playfair Display', serif; font-style: italic; font-size: 34pt; line-height: 1.1; color: #F3EBD0; margin-bottom: 4mm; }}
  .fullp-q p {{ color: rgba(255,255,255,.9); font-size: 11pt; max-width: 150mm; margin-left: auto; margin-right: auto; }} .fullp-q .bigq {{ font-size: 34pt; max-width: none; }} .fullp-q .eb {{ color: rgba(255,255,255,.7); margin-top: 3mm; font-size: 7.3pt; }}
  /* facts */
  .facts {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6mm; flex: 1; min-height: 0; }}
  .fact {{ margin: 0; display: flex; flex-direction: column; min-height: 0; }} .fact img {{ width: 100%; flex: 1; min-height: 0; }}
  .fact figcaption {{ padding-top: 3mm; }} .fact b {{ display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 13pt; line-height: 1.1; margin-bottom: 1mm; }} .fact span {{ font-size: 8.6pt; color: #4A4A47; line-height: 1.4; }}
  .nums {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6mm; border-top: 1px solid #C9C6C0; padding-top: 4mm; margin: 6mm 0 6mm; }}
  .nums b {{ display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 26pt; line-height: 1; }} .nums span {{ font-size: 8.3pt; color: #6B6772; }}
  /* split pages with a bleeding photo */
  .split {{ display: grid; height: 210mm; }} .split.l {{ grid-template-columns: 128mm 1fr; }} .split.r {{ grid-template-columns: 1fr 128mm; }}
  .split .ph {{ width: 100%; height: 100%; }}
  .split .txt {{ padding: 16mm 18mm 16mm 16mm; display: flex; flex-direction: column; justify-content: center; }} .split.r .txt {{ padding: 16mm 14mm 16mm 18mm; }}
  .quote {{ font-family: 'Playfair Display', serif; font-style: italic; font-size: 15pt; line-height: 1.3; margin: 4mm 0 5mm; color: #141414; border-left: 2px solid #C9C6C0; padding-left: 5mm; }}
  .adv-i {{ display: grid; grid-template-columns: 14mm 1fr; gap: 3mm; border-top: 1px solid #C9C6C0; padding: 5mm 0 4mm; }}
  .adv-i b {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: 18pt; line-height: 1; }}
  .adv-i h3 {{ font-size: 15pt; margin: 0 0 1.5mm; }} .adv-i p {{ font-size: 10pt; color: #4A4A47; margin: 0; }}
  /* SOLO I */
  .solo1 {{ display: grid; grid-template-columns: 1fr 150mm; height: 210mm; }}
  .solo1 .txt {{ padding: 16mm 12mm 16mm 18mm; display: flex; flex-direction: column; justify-content: center; }}
  .solo1 h1 {{ font-size: 40pt; margin: 1mm 0 4mm; }} .solo1 .it {{ margin-bottom: 5mm; }} .solo1 p {{ font-size: 9.6pt; color: #C9C5BE; }}
  .solo1 .team {{ color: #F3F1EC; border-top: 1px solid rgba(255,255,255,.2); padding-top: 3.5mm; margin-top: 2mm; }}
  .solo1-ph {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); grid-template-rows: minmax(0, 1.5fr) minmax(0, 1fr); gap: 3mm; height: 210mm; }}
  .solo1-ph img {{ width: 100%; height: 100%; min-height: 0; }} .solo1-ph .big {{ grid-column: span 2; }}
  /* header rows */
  .hd {{ display: grid; grid-template-columns: 1fr 96mm; gap: 12mm; align-items: end; margin-bottom: 6mm; }}
  .hd h2 {{ margin-bottom: 0; }} .hd-r {{ font-size: 8.8pt; color: #6B6772; margin: 0 0 1mm; }} .pg.dark .hd-r {{ color: #B8B3AA; }}
  /* SOLO II cards */
  .pcs {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 4mm; flex: 1; min-height: 0; align-content: start; }}
  .pc {{ position: relative; }} .pc .m {{ width: 100%; height: 148mm; }}
  .pc::after {{ content: ""; position: absolute; left: 0; right: 0; top: 80mm; height: 68mm; background: linear-gradient(180deg, rgba(0,0,0,0), rgba(0,0,0,.85)); }}
  .pc .fl {{ width: 11mm; height: 11mm; border: 1px solid rgba(255,255,255,.7); margin-bottom: 2mm; }}
  .pc-t {{ position: absolute; left: 3.5mm; right: 3mm; bottom: 4mm; z-index: 2; color: #fff; }}
  .pc-t b {{ display: block; font-family: 'Playfair Display', serif; font-style: italic; font-weight: 400; font-size: 14.5pt; line-height: 1.05; color: #E7D9A6; }}
  .pc-t span {{ display: block; font-size: 6.8pt; line-height: 1.35; margin-top: 1.2mm; color: rgba(255,255,255,.88); }}
  .pc small {{ display: block; font-size: 6.6pt; color: rgba(255,255,255,.72); margin-top: 1.5mm; line-height: 1.35; }}
  /* how to wear */
  .wayspg {{ padding-bottom: 0; }}
  .ways {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; flex: 1; min-height: 0; margin: 0 -18mm; }}
  .way {{ position: relative; margin: 0; overflow: hidden; }} .way img {{ width: 100%; height: 100%; }}
  .way::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 50%, rgba(0,0,0,.8) 100%); }}
  .way figcaption {{ position: absolute; left: 7mm; right: 6mm; bottom: 15mm; z-index: 2; color: #fff; }}
  .way b {{ display: block; font-family: 'Playfair Display', serif; font-style: italic; font-weight: 400; font-size: 24pt; line-height: 1; color: #F3EBD0; }}
  .way span {{ display: block; font-family: 'Playfair Display', serif; font-size: 10.5pt; margin-top: 2mm; color: rgba(255,255,255,.9); }}
  .wayspg .folio {{ display: none; }}
  .cov-f .toc {{ font-size: 7pt; letter-spacing: .08em; color: #8E8A84; margin: 3mm 0 0; }}
  /* tiers */
  .tiers h2 {{ font-size: 22pt; }}
  .ta-l {{ display: grid; }}
  .tr {{ display: grid; grid-template-columns: 17mm 1fr auto; gap: 4mm; align-items: center; padding: 2.4mm 0; border-top: 1px solid #C9C6C0; }}
  .tr:last-child {{ border-bottom: 1px solid #C9C6C0; }}
  .tr img {{ width: 17mm; height: 17mm; background: #fff; }}
  .tr .eb {{ margin-bottom: .5mm; }} .tr b {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: 13pt; display: block; line-height: 1.1; }}
  .tr span {{ display: block; font-size: 8.6pt; color: #4A4A47; }} .tr small {{ display: block; font-size: 7.3pt; color: #6B6772; margin-top: .5mm; }}
  .tr em {{ font-style: normal; font-family: 'Playfair Display', serif; font-size: 15pt; white-space: nowrap; }}
  .tiers .foot {{ margin-top: 5mm; }}
  /* four sets page */
  .fourpg {{ padding: 14mm 0 0; }}
  .fs-hd {{ display: flex; align-items: baseline; gap: 8mm; margin: 0 18mm 6mm; }} .fs-hd h2 {{ margin: 0; font-size: 22pt; }}
  .fss {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; flex: 1; min-height: 0; }}
  .fs {{ position: relative; overflow: hidden; }} .fs > img:first-child {{ width: 100%; height: 100%; }}
  .fs::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 42%, rgba(0,0,0,.82) 100%); }}
  .fs-t {{ position: absolute; left: 6mm; right: 6mm; bottom: 26mm; z-index: 2; color: #fff; }} .fs-t .eb {{ color: rgba(255,255,255,.75); margin-bottom: 1.5mm; }}
  .fs-t b {{ display: block; font-family: 'Playfair Display', serif; font-style: italic; font-weight: 400; font-size: 17pt; line-height: 1.05; color: #F3EBD0; }}
  .chip {{ position: absolute; left: 6mm; right: 6mm; bottom: 7mm; z-index: 2; display: grid; grid-template-columns: 13mm 1fr; gap: 3mm; align-items: center; background: rgba(20,20,20,.72); border: 1px solid rgba(255,255,255,.18); border-radius: 3mm; padding: 2mm 3mm 2mm 2mm; backdrop-filter: blur(6px); color: #fff; }}
  .chip .chip-ph {{ width: 13mm; height: 13mm; border-radius: 2mm; background: #fff; object-fit: cover; }}
  .chip span {{ display: block; font-size: 7pt; color: rgba(255,255,255,.8); line-height: 1.2; }} .chip em {{ font-style: normal; font-family: 'Playfair Display', serif; font-size: 13pt; color: #E7D9A6; line-height: 1.1; }}
  .fourpg .folio {{ display: none; }}
  /* set pages */
  .set {{ display: grid; grid-template-columns: 168mm 1fr; height: 210mm; }}
  .set.rev {{ grid-template-columns: 1fr 168mm; }} .set.rev .mos {{ order: 2; }}
  .mos {{ display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr); grid-template-rows: minmax(0, 1.35fr) minmax(0, 1fr); gap: 3mm; height: 210mm; min-height: 0; }}
  .mos img {{ width: 100%; height: 100%; min-height: 0; }} .mos .m1 {{ grid-row: span 2; }} .mos .m3 {{ object-fit: contain; background: #fff; padding: 4mm; }}
  .set-t {{ display: flex; flex-direction: column; padding: 14mm 16mm 12mm 14mm; min-width: 0; }} .set.rev .set-t {{ padding: 14mm 14mm 12mm 18mm; }}
  .set-t h2 {{ font-size: 19pt; margin-bottom: 2.5mm; }} .set-t .sub {{ font-size: 8.8pt; margin-bottom: 2.5mm; line-height: 1.45; }}
  .set-t .rrp {{ font-family: 'Playfair Display', serif; font-size: 19pt; line-height: 1.1; margin-bottom: 2.5mm; }} .set-t .rrp small {{ display: block; font-family: 'Tenor Sans', sans-serif; font-size: 7pt; color: #6B6772; margin-top: 1mm; line-height: 1.35; }}
  .set-t .kv div {{ display: grid; grid-template-columns: 24mm 1fr; gap: 3mm; font-size: 7.8pt; padding: 1.4mm 0; border-top: 1px solid #DAD7D0; line-height: 1.4; }} .set-t .kv span:first-child {{ color: #6B6772; }}
  .ways4 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5mm 4mm; margin-top: 3mm; font-size: 7.8pt; color: #4A4A47; line-height: 1.4; }} .ways4 b {{ display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 10pt; color: #141414; }}
  .set-t .who {{ margin-top: auto; font-family: 'Playfair Display', serif; font-style: italic; font-size: 12.5pt; line-height: 1.25; padding-top: 3mm; }}
  /* range */
  .grid6 {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 6mm 6mm; flex: 1; min-height: 0; align-content: start; }}
  .grid6 figure {{ margin: 0; }} .grid6 img {{ width: 100%; height: 50mm; object-fit: contain; background: #fff; }}
  .grid6 figcaption b {{ display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 11.5pt; line-height: 1.1; margin-top: 2mm; }}
  .grid6 figcaption span {{ font-size: 9pt; color: #6B6772; }}
  /* personalisation */
  .grid4p {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8mm; margin-bottom: 5mm; }}
  .per-ph {{ flex: 1; min-height: 0; margin-bottom: 4mm; }} .per-ph img {{ width: 100%; height: 100%; min-height: 0; }}
  .per {{ border-top: 1px solid #C9C6C0; padding-top: 3mm; display: flex; flex-direction: column; }}
  .per b {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: 18pt; line-height: 1; }}
  .per h3 {{ font-size: 14pt; margin: 1.5mm 0 2mm; }} .per p {{ font-size: 9.5pt; color: #4A4A47; margin: 0; }}
  .per .nt {{ font-size: 8.5pt; color: #6B6772; margin: 1mm 0 5mm; }}
  .per .free {{ font-family: 'Playfair Display', serif; font-size: 15pt; line-height: 1; margin: 2mm 0 0; color: #141414; }} .per .free + .nt {{ margin-top: 1mm; }}

  /* contacts */
  .steps {{ margin: 0 0 4mm; padding-left: 5mm; }} .steps li {{ margin-bottom: 2.5mm; color: #4A4A47; }} .steps b {{ color: #141414; font-weight: 400; font-family: 'Playfair Display', serif; font-size: 11.5pt; }}
  .cond {{ font-size: 8.5pt; color: #6B6772; border-top: 1px solid #DAD7D0; padding-top: 3mm; }}
  .qrrow {{ display: grid; grid-template-columns: 30mm 1fr; gap: 6mm; align-items: center; margin-top: 4mm; }} .qrrow svg {{ width: 30mm; height: 30mm; }}
  .contact {{ font-size: 12.5pt; line-height: 1.6; margin: 0; }} .contact b {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: 19pt; }} .contact small {{ font-size: 8pt; color: #6B6772; }} .contact a {{ color: inherit; }}
  .foot {{ font-size: 8.5pt; color: #6B6772; margin-top: auto; }} .pg.white .foot {{ margin-bottom: 4mm; }}
</style></head><body>{"".join(PAGES)}</body></html>'''
(OUT / "team-deck.html").write_text(typo(html))
script = OUT / "review" / "pp" / "pdf-team.mjs"
script.write_text('''import puppeteer from 'puppeteer-core';
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--no-sandbox', '--allow-file-access-from-files'] });
const p = await b.newPage();
await p.goto('file:///Users/ivan/obiimy/team-deck.html', { waitUntil: 'networkidle0', timeout: 120000 });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: '/Users/ivan/obiimy/obiimy-podarunky-dlia-komandy.pdf', printBackground: true, preferCSSPageSize: true });
await b.close();
console.log('pdf ok');
''')
subprocess.run(["node", str(script)], cwd=OUT / "review" / "pp", check=True)
print("pages:", len(PAGES), "size:", (OUT / "obiimy-podarunky-dlia-komandy.pdf").stat().st_size // 1024, "KB")
