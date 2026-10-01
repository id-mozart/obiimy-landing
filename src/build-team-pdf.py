#!/usr/bin/env python3
"""PDF presentation for HR: «Подарунки для команди» — team-deck.html (A4 landscape) -> obiimy-podarunky-dlia-komandy.pdf via headless Chrome.
Eight pages: cover, brand, three reasons, SOLO collection, four tiers, the whole range, personalisation, contacts.
Same facts and data as b2b-team-main (PERKS, SOLO, TIERS, ASSORT, PERS); retail prices from obiimy.world, the rest «у розрахунку»."""
import importlib.util, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
sys.path.insert(0, str(ROOT))
from imgs import typo
_spec = importlib.util.spec_from_file_location("main", ROOT / "build-b2b-team-main.py")
main = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(main)
PERKS, SOLO, TIERS, ASSORT, PERS, SETS4, price, qr_svg = main.PERKS, main.SOLO, main.TIERS, main.ASSORT, main.PERS, main.SETS4, main.price, main.qr_svg
team = main.team
PHONE, MAIL, SHOWROOM = team.PHONE, team.MAIL, team.SHOWROOM

def pic(src, cls="", pos=""):
    from PIL import Image
    p = pathlib.Path(src); lb = OUT / "review" / "lb"; lb.mkdir(parents=True, exist_ok=True)
    j = lb / (p.stem + ".jpg")
    if not j.exists():
        im = Image.open(OUT / src).convert("RGB"); im.thumbnail((1200, 1200)); im.save(j, quality=72, optimize=True)
    st = f' style="object-position:{pos}"' if pos else ""
    return f'<img src="review/lb/{j.name}" class="{cls}" alt=""{st}>'

PAGES = []
def page(html, cls=""): PAGES.append(f'<section class="pg {cls}">{html}</section>')
def foot(): return f'<p class="pf"><span>Obiimy · подарунки для команди · 2026</span><span>{PHONE} · {MAIL} · obiimy.world</span></p>'

# 1 cover
page(f'''<div class="cover">{pic("photo/solo/zolote-44-5.webp", "full", "50% 30%")}<div class="cover-t"><img src="brand/logo-white.png" class="logo" alt="Obiimy">
  <p class="eb">Для HR і офіс-менеджерів · 2026</p><h1>Подарунки<br>для команди</h1><p>Чотири рівні подарунка від 1 600 грн. Пакування й наліпка з вашим логотипом — безкоштовно.</p></div></div>''', "nopad")

# 2 brand
page(f'''<div class="two"><div>{pic("photo/solo/krok-tw-3.webp", "tall", "50% 30%")}</div><div class="txt">
  <p class="eb">Про бренд</p><h2>Obiimy — обійми з шовку</h2>
  <p>Український бренд шовкових аксесуарів із Києва. Засновниця й художниця — Світлана Сніжко. Хустки, твіллі, резинки, маски для сну, аксесуари для дому.</p>
  <p>Бренд заснований під час війни й бере участь у благодійних ініціативах. Колекція «Співоча душа» присвячена рідкісним птахам: частина коштів іде на гнізда для сиворакші з Червоної книги України.</p>
  <p>Шовк Obiimy продають INTERTOP і Hram в Україні, Be Brave у Канаді, UFD London. Про бренд писали LIGA.net та INSIDER UA.</p>
  <p class="foot">Шоурум: {SHOWROOM} — шовк можна побачити й відчути на дотик.</p>
</div></div>''')

# 3 three reasons
adv = "".join(f'<div class="adv-i"><b>0{i + 1}</b><div><h3>{b}</h3><p>{t}</p></div></div>' for i, (b, t) in enumerate(PERKS[:3]))
page(f'''<div class="two adv"><div class="txt adv-t">
  <p class="eb">Чому ми</p><h2>Три причини обрати шовк Obiimy</h2>{adv}
</div><div>{pic("photo/solo/avantiura-tw-1.webp", "tall", "50% 15%")}</div></div>''')

# 4 SOLO collection — black presentational page: manifesto (press release), cinematic shot, seven prints
prints = "".join(f'<div class="sd-p">{pic(fl)}<b>{n}</b><span>{st}</span></div>' for n, st, fm, pr, ph, fl in SOLO)
page(f'''<div class="sd-top"><div class="sd-t"><p class="eb">Нова колекція · 2026</p><h2>SOLO.<br>Шлях до себе</h2><p class="sd-slogan">Шовкова свобода: жіноча сила крізь десятиліття</p>
<p class="sd-note" style="margin-top:0;border:0;padding:0">Для команди: кожному — свій принт, під стан, який хочете побажати, або один на всіх. Твіллі — 1 600 грн; хустки 44 × 44 з двостороннім друком — від 2 400 грн.</p>
<p>У 40-х жінка підкреслювала силу бездоганною елегантністю — за м’якістю шовку ховався характер. У 50-х правила почали руйнуватися: колір, форма, власна ідентичність. Змінювалися епохи й силуети, а хустка залишалася поруч — як символ жіночності, що не суперечить силі.</p>
<p>SOLO — історія про шлях жінки до себе: моменти, коли ми шукаємо відповіді, відкриваємо власну силу й робимо сміливі кроки вперед. Сім авторських принтів — сім етапів цієї подорожі. Натуральний шовк, двосторонній друк.</p>
</div>
<div class="sd-ph">{pic("photo/solo/tysha-88-2.webp")}{pic("photo/solo/zolote-44-5.webp", "", "50% 25%")}{pic("photo/solo/avantiura-tw-1.webp", "", "50% 15%")}</div></div>
<div class="sd-prints">{prints}</div>''', "dark")

# 5 four tiers — variant A (editorial) chosen after the audit: one model shot, four rows with product thumbs, price breakdown
H5 = '<p class="eb">Ціновий діапазон</p><h2>Чотири рівні подарунка — від 1 600 до 3 200 грн за речі</h2>'
F5 = '<p class="foot">Команді з 50 людей — 80 000–160 000 грн за речі, зі 100 — 160 000–320 000 (роздрібні ціни; доставка й майстер-клас — окремо). Кожен рівень — на стор. 6–9.</p>'
rows = "".join(f'<div class="tr">{pic(ph)}<div><p class="eb">{lb}</p><b>{n}</b><span>{t}</span><small>{note}</small></div><em>{pr}</em></div>' for (lb, n, t, pr, note, ph), S in zip(TIERS, SETS4))
page(f'''<div class="ta"><div>{pic("photo/solo/zolote-44-3.webp", "tall", "50% 20%")}</div><div class="txt">{H5}<p class="sub">Від однієї стрічки до набору з майстер-класом. Ціни роздрібні, obiimy.world; кожному — свій принт із добірки.</p><div class="ta-l">{rows}</div>{F5}</div></div>''', "tiers")

# 5b one page per set: editorial mosaic bleeding to the page edge (tall model shot, second model shot, product), text column
PROD = [3, 2, 1, 2]   # which gallery item is the product shot per set
M1POS = ["50% 12%", "50% 8%", "50% 30%", "50% 18%"]   # the tall tile crops higher than the web hero
for i, S in enumerate(SETS4):
    hp, ha, hpos = S["hero"]
    g2 = S["gal"][0]; g3 = S["gal"][PROD[i]]
    kv = "".join(f'<div><span>{k}</span><span>{v}</span></div>' for k, v in S["inside"])
    ways = "".join(f'<div><b>{h}</b>{t}</div>' for h, t in S["ways"])
    page(f'''<div class="set{" rev" if i % 2 else ""}"><div class="mos">{pic(hp, "m1", M1POS[i])}{pic(g2[0], "m2", g2[2])}{pic(g3[0], "m3", g3[2])}</div>
<div class="set-t"><p class="eb">{S["lb"]}</p><h2>{S["name"]}</h2><p class="sub">{S["lead"]}</p>
<p class="rrp">{S["pr"]}<small>{S["prnote"]}</small></p>
<div class="kv">{kv}</div>
<div class="ways">{ways}</div>
<p class="who">{S["who"]}</p></div></div>''', "setp")

# 6 the whole range
tiles = "".join(f'<figure>{pic(ph)}<figcaption><b>{n}</b><span>від {price(pr)}</span></figcaption></figure>' for n, pr, ph in ASSORT)
page(f'''<p class="eb">Асортимент</p><h2>Усе, з чого можна зібрати подарунок</h2><p class="sub">Роздрібні ціни obiimy.world, «від» — найдешевший формат чи принт. Принт і формат — у добірці.</p>
<div class="grid6">{tiles}</div><p class="foot" style="margin-top:4mm"><b>Чоловікам у команді</b> — сертифікат Obiimy на 1 000–4 000 грн (електронний або фізичний, на будь-який товар), маска для сну, наволочка або закладка — зберемо в один розрахунок. Будь-яку річ можна зробити рівнем подарунка або додати в коробку.</p>{foot()}''')

# 7 personalisation
def terms(i, tm): return '<p class="free">Безкоштовно</p><p class="nt">у кожному корпоративному замовленні</p>' if i == 0 else f'<p class="nt">{tm}</p>'
pers = "".join(f'<div class="per"><b>0{i + 1}</b><h3>{n}</h3><p>{t}</p>{terms(i, tm)}{pic(ph)}</div>' for i, (n, t, tm, ph) in enumerate(PERS))
page(f'''<p class="eb">Персоналізація</p><h2>Подарунок із вашим логотипом — чотири рівні</h2><p class="sub">Перший рівень — безкоштовно в кожному корпоративному замовленні. Решта — залежно від строків: що встигаємо до вашої дати й скільки це коштує, пишемо в розрахунку.</p>
<div class="grid4p">{pers}</div>
<p class="foot">Фото — приклади пакування, речей і сертифіката Obiimy; як виглядатиме наліпка чи бирка з вашим логотипом, покажемо в добірці.</p>''')

# 8 contacts
page(f'''<div class="two"><div class="txt"><p class="eb">Запит</p><h2>Напишіть — надішлемо добірку й розрахунок</h2>
  <ol class="steps"><li><b>Нагода, кількість, дата.</b> Цього досить для першого листа.</li><li><b>Добірка й розрахунок</b> окремими рядками: речі, персоналізація, доставка. Чи встигаємо до вашої дати — пишемо одразу.</li><li><b>Відправка</b> Новою поштою в день замовлення до 16:00 — кожному окремо чи в офіс; безкоштовно від 5 000 грн.</li></ol>
  <p class="cond">Оплата й документи для юридичної особи, мінімальна кількість — уточнимо в розрахунку. Сторінка для команд: <a href="https://obiimy-landing-production.up.railway.app/b2b-team-main" style="color:inherit">obiimy-landing-production.up.railway.app/b2b-team-main</a></p>
  <div class="qrrow">{qr_svg("https://obiimy-landing-production.up.railway.app/b2b-team-main", 110)}<p class="contact"><b>{PHONE}</b><br>Telegram @OBIIMY_sales<br>{MAIL}<br>obiimy.world<br><small>Скануйте — сторінка для команд із формою запиту</small></p></div>
  <p class="foot">Шоурум: {SHOWROOM}<br>пн–пт 10:00–18:00, сб 11:00–18:00</p>
</div><div>{pic("photo/solo/zolote-tw-2.webp", "tall", "50% 40%")}</div></div>''')

html = f'''<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>Obiimy — подарунки для команди 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=Tenor+Sans&display=swap" rel="stylesheet">
<style>
  @page {{ size: A4 landscape; margin: 0; }}
  * {{ box-sizing: border-box; font-variant-numeric: lining-nums; }}
  html, body {{ margin: 0; background: #F1EFEA; color: #141414; font-family: 'Tenor Sans', sans-serif; font-size: 10.5pt; line-height: 1.5; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .pg {{ width: 297mm; height: 210mm; padding: 16mm 18mm 14mm; page-break-after: always; break-after: page; overflow: hidden; position: relative; display: flex; flex-direction: column; background: #F1EFEA; }}
  .pg.nopad {{ padding: 0; }}
  h1, h2, h3 {{ font-family: 'Playfair Display', serif; font-weight: 400; margin: 0; line-height: 1.08; letter-spacing: -.01em; }}
  h1 {{ font-size: 46pt; }} h2 {{ font-size: 25pt; margin-bottom: 5mm; }} h3 {{ font-size: 14pt; margin-top: 2mm; }}
  p {{ margin: 0 0 3mm; }}
  .eb {{ font-size: 7.5pt; letter-spacing: .24em; text-transform: uppercase; color: #6B6772; margin-bottom: 2.5mm; }}
  .sub {{ color: #4A4A47; margin-top: -2mm; margin-bottom: 5mm; max-width: 190mm; }}
  img {{ display: block; object-fit: cover; }}
  .cover {{ position: relative; width: 100%; height: 100%; }}
  .cover .full {{ width: 100%; height: 100%; }}
  .cover::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,0,0,.6) 0%, rgba(0,0,0,.3) 45%, rgba(0,0,0,0) 70%), linear-gradient(0deg, rgba(0,0,0,.55) 0%, rgba(0,0,0,0) 45%); }}
  .cover-t {{ z-index: 1; position: absolute; left: 18mm; bottom: 18mm; max-width: 46%; color: #fff; }}
  .cover-t .eb {{ color: rgba(255,255,255,.8); }}
  .cover-t .logo {{ height: 11mm; width: auto; margin-bottom: 10mm; object-fit: contain; }}
  .cover-t p {{ font-size: 12pt; margin-top: 5mm; color: rgba(255,255,255,.92); }}
  .two {{ display: grid; grid-template-columns: 1fr 1.1fr; gap: 14mm; height: 100%; }}
  .tall {{ width: 100%; height: 180mm; }}
  .txt {{ align-self: center; }}
  .adv-t {{ align-self: stretch; display: flex; flex-direction: column; justify-content: center; }}
  .adv-i {{ display: grid; grid-template-columns: 14mm 1fr; gap: 3mm; border-top: 1px solid #C9C6C0; padding: 5mm 0 4mm; }}
  .adv-i b {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: 18pt; line-height: 1; }}
  .adv-i h3 {{ font-size: 15pt; margin: 0 0 1.5mm; }} .adv-i p {{ font-size: 10pt; color: #4A4A47; margin: 0; }}
  .solo {{ display: grid; grid-template-columns: 1fr 1.05fr; gap: 12mm; height: 100%; }}
  .solo-ph {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; height: 180mm; grid-template-rows: 1fr 1fr; }}
  .solo-ph img {{ width: 100%; height: 100%; }} .solo-ph img:first-child {{ grid-column: span 2; }}
  .solo .sub {{ font-size: 9.5pt; }}
  .solo-l {{ display: grid; }}
  .sp {{ display: grid; grid-template-columns: 15mm 1fr; gap: 4mm; align-items: center; padding: 1.8mm 0; border-top: 1px solid #DAD7D0; }}
  .sp:first-child {{ border-top: 0; }}
  .sp img {{ width: 15mm; height: 15mm; background: #fff; }}
  .sp b {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: 12pt; display: block; line-height: 1.1; }}
  .sp span {{ display: block; font-size: 9pt; color: #4A4A47; }} .sp small {{ font-size: 8pt; color: #6B6772; }}
  .grid4f {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8mm; flex: 1; align-content: start; }}
  .four {{ display: flex; flex-direction: column; border-top: 1px solid #C9C6C0; padding-top: 3mm; }}
  .four .n {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: 15pt; line-height: 1; margin-bottom: 2mm; }}
  .four img {{ width: 100%; aspect-ratio: 1 / 1; background: #fff; border: 1px solid #E5E3DD; }} .four img.ct {{ object-fit: contain; padding: 3mm; }}
  .four .eb {{ margin: 3mm 0 0; min-height: 8mm; }}
  .four h3 {{ font-size: 15pt; margin: 1mm 0 2mm; min-height: 13mm; }}
  .four p {{ font-size: 10pt; color: #4A4A47; margin: 0 0 1.5mm; }}
  .four .pz {{ margin-top: auto; padding-top: 3mm; }}
  .four .rrp {{ font-family: 'Playfair Display', serif; font-size: 19pt; color: #141414; line-height: 1.1; white-space: nowrap; }}
  .four .nt {{ font-size: 8pt; min-height: 10mm; margin: 1mm 0 0; color: #6B6772; }}
  .pg.dark {{ background: #0E0E0E; color: #F3F1EC; }} .pg.dark .eb {{ color: #B8B3AA; }}
  .sd-top {{ display: grid; grid-template-columns: 1fr 1.25fr; gap: 12mm; flex: none; height: 118mm; align-items: center; }}
  .sd-t h2 {{ font-size: 36pt; line-height: .98; margin: 1mm 0 4mm; }}
  .sd-slogan {{ font-family: 'Playfair Display', serif; font-style: italic; font-size: 13pt; color: #E7D9A6; margin-bottom: 4mm; }}
  .sd-t p {{ font-size: 9.5pt; color: #C9C5BE; }} .sd-note {{ color: #F3F1EC; border-top: 1px solid rgba(255,255,255,.2); padding-top: 3mm; margin-top: 4mm; }}
  .sd-ph {{ display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: minmax(0, 1.4fr) minmax(0, 1fr); gap: 3mm; height: 118mm; min-height: 0; }}
  .sd-ph img {{ width: 100%; height: 100%; min-height: 0; }} .sd-ph img:first-child {{ grid-column: span 2; }}
  .sd-prints {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 4mm; margin-top: 5mm; padding-top: 4mm; border-top: 1px solid rgba(255,255,255,.16); }}
  .sd-p img {{ width: 100%; height: 28mm; background: #fff; }}
  .sd-p b {{ display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 10.5pt; margin-top: 2mm; line-height: 1.1; }}
  .sd-p span {{ display: block; color: #8E8A84; font-size: 7pt; margin-top: .5mm; line-height: 1.3; }}
  .ta {{ display: grid; grid-template-columns: 1fr 1.15fr; gap: 12mm; height: 100%; }}
  .ta .txt {{ align-self: stretch; display: flex; flex-direction: column; justify-content: center; }}
  .ta-l {{ display: grid; }}
  .tr {{ display: grid; grid-template-columns: 18mm 1fr auto; gap: 4mm; align-items: center; padding: 2.2mm 0; border-top: 1px solid #C9C6C0; }}
  .tr:last-child {{ border-bottom: 1px solid #C9C6C0; }}
  .pg.tiers .tr {{ padding: 2mm 0; }} .pg.tiers .tr b {{ font-size: 13pt; }} .pg.tiers .foot {{ margin-top: 3mm; }}
  .tr img {{ width: 18mm; height: 18mm; background: #fff; border: 1px solid #E5E3DD; }}
  .tr .eb {{ margin-bottom: .5mm; }} .tr b {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: 14pt; display: block; line-height: 1.1; }}
  .tr span {{ display: block; font-size: 9pt; color: #4A4A47; }} .tr small {{ display: block; font-size: 7.5pt; color: #6B6772; margin-top: .5mm; }} .tr em {{ font-style: normal; font-family: 'Playfair Display', serif; font-size: 16pt; white-space: nowrap; }}
  .tbs {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 5mm; flex: 1; min-height: 0; }}
  .tb {{ position: relative; overflow: hidden; color: #fff; }} .tb > img:first-child {{ width: 100%; height: 100%; }}
  .tb::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 45%, rgba(0,0,0,.72) 100%); }}
  .tb-t {{ position: absolute; left: 5mm; right: 5mm; bottom: 5mm; z-index: 1; }} .tb-t .eb {{ color: rgba(255,255,255,.75); margin-bottom: 1mm; }}
  .tb-t b {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: 14pt; display: block; line-height: 1.1; }} .tb-t em {{ font-style: normal; font-family: 'Playfair Display', serif; font-size: 13pt; display: block; margin-top: 1.5mm; }}
  .tb-p {{ position: absolute; top: 4mm; right: 4mm; width: 18mm; height: 18mm; border: 2px solid #fff; z-index: 1; }}
  .tcs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; flex: 1; min-height: 0; }}
  .tc {{ display: grid; grid-template-columns: 1fr 1.2fr; background: #fff; border: 1px solid #E5E3DD; overflow: hidden; }}
  .tc-ph {{ position: relative; }} .tc-ph > img:first-child {{ width: 100%; height: 100%; }}
  .tc-p {{ position: absolute; left: 3mm; bottom: 3mm; width: 18mm; height: 18mm; border: 2px solid #fff; background: #fff; }}
  .tc-t {{ padding: 5mm 6mm; display: flex; flex-direction: column; }} .tc-t h3 {{ font-size: 14pt; margin: 1mm 0 2mm; }} .tc-t p {{ font-size: 9pt; color: #4A4A47; margin: 0; }}
  .tc-t em {{ font-style: normal; font-family: 'Playfair Display', serif; font-size: 16pt; margin-top: auto; padding-top: 3mm; }} .tc-t small {{ font-size: 7.5pt; color: #6B6772; }}
  .pg.setp {{ padding: 0; }}
  .set {{ display: grid; grid-template-columns: 168mm 1fr; height: 210mm; }}
  .set.rev {{ grid-template-columns: 1fr 168mm; }} .set.rev .mos {{ order: 2; }}
  .mos {{ display: grid; grid-template-columns: 1.1fr 1fr; grid-template-rows: 1.35fr 1fr; gap: 3mm; height: 210mm; min-height: 0; }}
  .mos img {{ width: 100%; height: 100%; min-height: 0; }} .mos .m1 {{ grid-row: span 2; }}
  .set-t {{ display: flex; flex-direction: column; padding: 14mm 16mm 12mm 14mm; min-width: 0; }}
  .set.rev .set-t {{ padding: 14mm 14mm 12mm 18mm; }}
  .set-t h2 {{ font-size: 19pt; margin-bottom: 2.5mm; }} .set-t .sub {{ font-size: 8.8pt; margin-bottom: 2.5mm; line-height: 1.45; }}
  .set-t .rrp {{ font-family: 'Playfair Display', serif; font-size: 19pt; line-height: 1.1; margin-bottom: 2.5mm; }} .set-t .rrp small {{ display: block; font-family: 'Tenor Sans', sans-serif; font-size: 7pt; color: #6B6772; margin-top: 1mm; line-height: 1.35; }}
  .set-t .kv div {{ display: grid; grid-template-columns: 24mm 1fr; gap: 3mm; font-size: 7.8pt; padding: 1.4mm 0; border-top: 1px solid #DAD7D0; line-height: 1.4; }} .set-t .kv span:first-child {{ color: #6B6772; }}
  .set-t .ways {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5mm 4mm; margin-top: 3mm; font-size: 7.8pt; color: #4A4A47; line-height: 1.4; }} .set-t .ways b {{ display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 10pt; color: #141414; }}
  .set-t .who {{ margin-top: auto; font-family: 'Playfair Display', serif; font-size: 12pt; line-height: 1.25; padding-top: 3mm; }}
  .grid6 {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 5mm 5mm; flex: 1; align-content: start; }}
  .grid6 figure {{ margin: 0; }}
  .grid6 img {{ width: 100%; aspect-ratio: 1 / 1; background: #fff; border: 1px solid #E5E3DD; }}
  .grid6 figcaption b {{ display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 11.5pt; line-height: 1.1; margin-top: 2mm; }}
  .grid6 figcaption span {{ font-size: 9.5pt; color: #4A4A47; }}
  .grid4p {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8mm; flex: 1; min-height: 0; margin-bottom: 4mm; }}
  .per {{ border-top: 1px solid #C9C6C0; padding-top: 3mm; display: flex; flex-direction: column; }}
  .per b {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: 18pt; line-height: 1; }}
  .per h3 {{ font-size: 14pt; margin: 1.5mm 0 2mm; }} .per p {{ font-size: 9.5pt; color: #4A4A47; margin: 0; }}
  .per .nt {{ font-size: 8.5pt; color: #6B6772; margin: 1mm 0 5mm; }}
  .per .free {{ font-family: 'Playfair Display', serif; font-size: 15pt; line-height: 1; margin: 2mm 0 0; color: #141414; }} .per .free + .nt {{ margin-top: 1mm; }}
  .per img {{ width: 100%; height: 64mm; margin-top: auto; background: #fff; border: 1px solid #E5E3DD; }}
  .steps {{ margin: 0 0 4mm; padding-left: 5mm; }} .steps li {{ margin-bottom: 2.5mm; color: #4A4A47; }} .steps b {{ color: #141414; font-weight: 400; font-family: 'Playfair Display', serif; font-size: 11.5pt; }}
  .cond {{ font-size: 8.5pt; color: #6B6772; border-top: 1px solid #DAD7D0; padding-top: 3mm; }}
  .qrrow {{ display: grid; grid-template-columns: 30mm 1fr; gap: 6mm; align-items: center; margin-top: 4mm; }} .qrrow svg {{ width: 30mm; height: 30mm; }} .qrrow .contact {{ margin-top: 0; }} .qrrow small {{ font-size: 8pt; color: #6B6772; }}
  .contact {{ margin-top: 4mm; font-size: 13pt; line-height: 1.6; }} .contact b {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: 20pt; }}
  .foot {{ font-size: 8.5pt; color: #6B6772; margin-top: auto; }}
  .pf {{ margin-top: auto; padding-top: 3mm; border-top: 1px solid #DAD7D0; font-size: 8pt; color: #6B6772; display: flex; justify-content: space-between; }}
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
