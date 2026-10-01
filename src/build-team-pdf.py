#!/usr/bin/env python3
"""PDF presentation for HR: «Подарунки для команди» — team-deck.html (A4 landscape) -> obiimy-podarunky-dlia-komandy.pdf via headless Chrome.
Same facts as the b2b-team pages: retail prices from obiimy.world, nothing promised beyond «у розрахунку»."""
import importlib.util, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
sys.path.insert(0, str(ROOT))
from imgs import typo
_spec = importlib.util.spec_from_file_location("team", ROOT / "build-b2b-team.py")
team = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(team)
CAT, FEATURED, STAGES, PLANS, SHORT, price, sp = team.CAT, team.FEATURED, team.STAGES, team.PLANS, team.SHORT, team.price, team.sp
def full(k): return CAT[k]["n"] if k.startswith("cert") else f'{CAT[k]["n"]} — {price(CAT[k]["p"])}'
PHONE, MAIL, SHOWROOM = team.PHONE, team.MAIL, team.SHOWROOM
LANDING = "https://obiimy-landing-production.up.railway.app/b2b-team-main"
_sh = importlib.util.spec_from_file_location("shop", ROOT / "build-b2b-team-shop.py")
shop = importlib.util.module_from_spec(_sh); _sh.loader.exec_module(shop)
FOR, SHORTN, CERTS = shop.FOR, shop.SHORT, shop.CERTS

def pic(src, cls="", pos=""):
    from PIL import Image
    p = pathlib.Path(src); lb = OUT / "review" / "lb"; lb.mkdir(parents=True, exist_ok=True)
    j = lb / (p.stem + ".jpg")
    if not j.exists():
        im = Image.open(OUT / src).convert("RGB"); im.thumbnail((1400, 1400)); im.save(j, quality=74, optimize=True)
    st = f' style="object-position:{pos}"' if pos else ""
    return f'<img src="review/lb/{j.name}" class="{cls}" alt=""{st}>'

PAGES = []
def page(html, cls=""): PAGES.append(f'<section class="pg {cls}">{html}</section>')

# 1 cover
page(f'''<div class="cover">{pic("photo/hratsiia-2.webp", "full", "50% 30%")}<div class="cover-t"><img src="brand/logo-white.png" class="logo" alt="Obiimy">
  <h1>Подарунки<br>для команди</h1><p>Шовкові речі від українського бренду — до першого дня, дня народження, річниці в компанії. Пропозиція для HR і офіс-менеджерів · 2026</p></div></div>''', "nopad")

# 2 about
page(f'''<div class="two"><div>{pic("img/life2.webp", "tall")}</div><div class="txt">
  <p class="eb">Про бренд</p><h2>Obiimy — обійми з шовку</h2>
  <p>Український бренд шовкових аксесуарів із Києва. Засновниця й художниця — Світлана Сніжко. Хустки, твіллі, резинки, маски для сну, аксесуари для дому.</p>
  <p>Бренд заснований під час війни й бере участь у благодійних ініціативах. Колекція «Співоча душа» присвячена рідкісним птахам: частина коштів іде на гнізда для сиворакші з Червоної книги України.</p>
  <p class="foot">Шоурум: {SHOWROOM} — шовк можна побачити й відчути на дотик.</p>
</div></div>''')

# 2b advantages: prints, quality, brand — facts from review/SITE-FACTS.md (incl. the client's letter of 01.10)
page(f'''<div class="two adv"><div>{pic("photo/dotyk-1.webp", "tall", "50% 25%")}</div><div class="txt adv-t">
  <p class="eb">Чому ми</p><h2>Три причини обрати шовк Obiimy</h2>
  <div class="adv-i"><b>01</b><div><h3>Унікальні принти</h3><p>Авторські малюнки, а не стокові принти: роботи засновниці Світлани Сніжко та сучасних українських художниць. Принти для команди обираєте з добірки — не однакові для всіх.</p></div></div>
  <div class="adv-i"><b>02</b><div><h3>Якість, яку відчувають</h3><p>Лише 100% натуральний італійський шовк. Кутики кожної хустки кравчині обробляють вручну, щоб край був однаково щільним. Повністю українське виробництво. Річ, яку носитимуть, а не покладуть у шухляду.</p></div></div>
  <div class="adv-i"><b>03</b><div><h3>Український бренд, який упізнають</h3><p>Шовк Obiimy продають INTERTOP і Hram в Україні, Be Brave у Канаді, UFD London. Про бренд писали LIGA.net та INSIDER UA.</p></div></div>
</div></div>''')

# 3 why gifts inside the company
page(f'''<p class="eb">Навіщо</p><h2>Подарунок від компанії, який пам’ятають</h2>
<div class="cols3">
  <div><h3>Річ, а не сувенір</h3><p>Шовкову річ носять: на шию, у волосся, на сумку. Маска для сну чи наволочка — щодня вдома. Це не блокнот із логотипом, який лишається в шухляді.</p></div>
  <div><h3>Слова від компанії</h3><p>До кожного подарунка — привітання вашими словами: до дня народження, річниці, закритого проєкту. Текст пишете ви, оформлення узгоджуємо в розрахунку.</p></div>
  <div><h3>Для всієї команди</h3><p>У каталозі є речі, що підходять усім: закладка для книги, маска для сну, однотонна наволочка, сертифікат, який людина обирає сама.</p></div>
</div>
<div class="strip">{pic("photo/bag-1.webp")}{pic("img/sets/scr3.webp")}{pic("img/mask-svoboda.webp")}{pic("img/sets/pillow-tuman.webp")}</div>''')

# 3b catalogue with prices
ORDER = ["tw", "twscr", "mask", "h44", "scr", "book", "cert1", "scrset", "maskscr", "tw44", "h65", "song", "pil", "h88", "three"]
cells = "".join((f'<figure>{pic(CAT[k]["ph"])}<figcaption><b>Сертифікат</b><span>Усім · на вибір</span><em>1 000–4 000 грн</em></figcaption></figure>' if k == "cert1"
                 else f'<figure>{pic(CAT[k]["ph"])}<figcaption><b>{SHORTN[k]}</b><span>{FOR[k].replace("Універсальний подарунок", "Універсальний")}</span><em>{price(CAT[k]["p"])}</em></figcaption></figure>') for k in ORDER)
page(f'''<p class="eb">Каталог</p><h2>Речі, набори й ціни — 15 позицій</h2><p class="sub">Роздрібні ціни obiimy.world. Підписи «кому» — наші поради; фото — приклад принта, наявність у потрібному форматі підтвердимо в розрахунку.</p>
<div class="grid5">{cells}</div>''')

# 3c three budgets
shelves = ""
for v, t, sub, ks in shop.SHELVES:
    lis = "".join(f'<li><span>{"Сертифікат" if k.startswith("cert") else SHORTN[k]}</span><b>{price(CAT[k]["p"])}</b></li>' for k in ks)
    shelves += f'<div class="shelf"><h3>{t}</h3><p class="alt">{sub}</p><ul>{lis}</ul><p class="ex">20 людям — до {price(20 * int(v))}</p></div>'
page(f'''<p class="eb">За бюджетом</p><h2>Що подарувати на 1 000, 2 500 і 5 000 грн на людину</h2><p class="sub">Три полиці — усе, що є в бюджеті. Речі «усім» підходять і тим, хто аксесуари не носить.</p>
<div class="shelves">{shelves}</div>
<div class="strip">{pic("img/twilly-zolote.webp")}{pic("img/sets/twscr-makiv.webp")}{pic("img/sets/tw44-vpevnenist.webp")}{pic("img/sets/three-twilly.webp")}</div>''')

# 4 occasions
occ = "".join(f'<div class="occ"><b>{i + 1}</b><h3>{t}</h3><p>{full(s)}</p><p class="alt">{"Підходить усім" if s == n else "Для всіх: " + full(n)}</p></div>'
              for i, (sid, short, t, d, p, a, s, n, sh) in enumerate(STAGES))
page(f'''<p class="eb">Нагоди</p><h2>Шлях людини в компанії — вісім нагод</h2><p class="sub">Що радимо подарувати на кожну. Ціни роздрібні, obiimy.world.</p>
<div class="grid4t">{occ}</div>
<div class="strip" style="margin-top:8mm">{pic("img/twilly-zolote.webp")}{pic("img/scrunchie-pole.webp")}{pic("photo/kolo-3.webp", "", "50% 20%")}{pic("photo/mizh-1.webp", "", "50% 10%")}</div>''')

# 4b four tiers with prices — the price range at a glance; «від» only where a dearer variant exists
FOUR = [  # label, name, what is inside, price text, note, photo, img class
    ("Знак уваги", "Твіллі", "Шовкова стрічка 84 × 5 — на шию, у волосся, на сумку. 38 принтів на вибір.", "1 600 грн", "довга 140 × 5 «Літній віночок» — 1 850 грн", "img/twilly-zolote.webp", ""),
    ("Хто носить аксесуари", "Хустка та кільце", "Хустка 44 × 44 і кільце Gold до неї — на шию, на сумку чи поясом. Збираємо під замовлення.", "від 2 050 грн", "хустка 1 600 + кільце 450; двостороння хустка — 2 400 + 450", "photo/hratsiia-flat.webp", "ct"),
    ("Для відпочинку", "Маска для сну та резинка", "Шовкова маска й резинка в одному принті, у фірмовому пакуванні Obiimy.", "3 100 грн", "", "img/sets/maskscr-litnie-pole.webp", ""),
    ("Ключовим людям", "Хустка, твіллі й майстер-клас", "Хустка 44 × 44 і твіллі в одному принті — та запрошення на авторський майстер-клас від Світлани Сніжко.", "3 200 грн", "+ майстер-клас — формат і вартість у розрахунку; двосторонній друк — 3 600", "img/sets/tw44-natkhnennia.webp", ""),
]
four = "".join(f'<div class="four"><b class="n">0{i + 1}</b>{pic(ph, ic)}<p class="eb">{lb}</p><h3>{n}</h3><p>{t}</p><div class="pz"><p class="rrp">{pr}</p><p class="nt">{note}</p></div></div>' for i, (lb, n, t, pr, note, ph, ic) in enumerate(FOUR))
page(f'''<p class="eb">Ціновий діапазон</p><h2>Чотири рівні подарунка — від 1 600 до 3 200 грн на людину</h2><p class="sub">Якщо для бюджету потрібна одна цифра — ось чотири точки: від однієї стрічки до набору з хусткою й твіллі. Ціни роздрібні, obiimy.world; каталог — с. 5, за бюджетом — с. 6.</p>
<div class="grid4f">{four}</div>
<p class="foot">Команді з 50 людей — від 80 000 до 160 000 грн за речі за роздрібними цінами; доставку й майстер-клас рахуємо окремо. Склад можна змінити — перерахуємо. Напишіть нагоди й кількість — контакти на с. 14.</p>''')

# 5 sets
sets = "".join(f'<div class="cat">{pic(ph)}<p class="eb">{who}</p><h3>{name}</h3><p>{text}</p><p class="rrp">{price(pr)}{" · " + note if note else ""}</p></div>' for sid, name, who, ph, a, pr, note, text in FEATURED)
page(f'''<p class="eb">Готові набори</p><h2>Шість готових наборів із каталогу</h2><div class="grid3">{sets}</div>
<p class="foot">Набори Obiimy у фірмовому пакуванні. Ціни роздрібні; підписи над назвами — наші поради.</p>''')

# 6 for everyone + key people
ev = [("img/mask-svoboda.webp", "Маска для сну", "2 700 грн"), ("img/sets/bookmark-melodiia.webp", "Закладка для книги", "800 грн"), ("img/sets/pillow-tuman.webp", "Наволочка 50 × 70, однотонна", "4 200 грн"), ("img/sets/cert-2000.webp", "Сертифікат", "1 000–4 000 грн")]
ky = [("img/mask-svoboda.webp", "Маска для сну", "2 700 грн"), ("img/sets/tw44-vpevnenist.webp", "Твіллі та хустка 44 × 44", "3 200 грн"), ("img/sets/sleep-pidnesennia.webp", "Маска, закладка й резинка", "3 600 грн"), ("img/sets/three-twilly.webp", "Три твіллі на вибір", "4 800 грн")]
row = lambda items: "".join(f'<figure>{pic(ph)}<figcaption><b>{n}</b><span>{p}</span></figcaption></figure>' for ph, n, p in items)
page(f'''<div class="two-rows"><div><p class="eb">Для всієї команди</p><h2>Речі, що підходять усім</h2><div class="grid4s">{row(ev)}</div></div>
<div><p class="eb">Ключовим людям</p><h2>Окремий подарунок понад програму</h2><div class="grid4s">{row(ky)}</div></div></div>''')

# 7 programmes
tiers = ""
for pid, name, who, rows in PLANS:
    s = sum(CAT[a]["p"] for _o, a, _b in rows); u = sum(CAT[b]["p"] for _o, _a, b in rows)
    rng = price(s) if s == u else f"{min(s, u):,}".replace(",", " ") + "–" + price(max(s, u))
    lis = "".join(f'<li><b>{o}</b><span>{sp(a)}</span><span>для всіх: {sp(b)}</span></li>' for o, a, b in rows)
    tiers += f'<div class="tier"><h3>{name}</h3><p class="pp">{rng}<small>на людину на рік</small></p><p>{who}</p><ul>{lis}</ul></div>'
page(f'''<p class="eb">Програма на рік</p><h2>Три приклади — від 700 грн на людину на рік</h2><p class="sub">Для кожної нагоди — шовкова річ і річ, що підходить усім. Склад можна змінити: перерахуємо суму.</p>
<div class="tiers">{tiers}</div>
<p class="foot" style="font-size:10pt;color:#4A4A47">Приклад: команда з 40 людей, програма «Команда», 16 отримують речі «для всіх» — 40 × 2 300 = 92 000 грн на рік (шовкова річ і річ «для всіх» у цій програмі коштують однаково) за роздрібними цінами, без доставки.</p>''')

# 7b personalisation: level 1 is free (client's letter, 01.10); the rest — «у розрахунку»
PERS = [  # name, text, terms line, photo, position
    ("Пакування й наліпка", "Подарункове пакування для кожної речі та наліпка з логотипом вашої компанії всередині коробки.", "", "photo/box-gold.jpg", ""),
    ("Бирка з логотипом", "Нашивна бирка з логотипом компанії на самій хустці чи твіллі.", "Строки й вартість — у розрахунку", "photo/dotyk-3.webp", ""),
    ("Друковані матеріали", "Листівка з привітанням — з вашим логотипом і вашим текстом; інші друковані матеріали — обговоримо.", "Формат і вартість — у розрахунку", "img/sets/cert-2000.webp", ""),
    ("Індивідуальний принт", "Принт, створений для вашої компанії: кольори бренду, символи, історія.", "Тираж, строки й вартість — у розрахунку", "photo/vyr-flat.webp", ""),
]
def _per_terms(i, tm):
    return '<p class="free">Безкоштовно</p><p class="nt">у кожному корпоративному замовленні</p>' if i == 0 else f'<p class="nt">{tm}</p>'
pers = "".join(f'<div class="per"><b>0{i + 1}</b><h3>{n}</h3><p>{t}</p>{_per_terms(i, tm)}{pic(ph, "", pos)}</div>' for i, (n, t, tm, ph, pos) in enumerate(PERS))
page(f'''<p class="eb">Персоналізація</p><h2>Подарунок із вашим логотипом — чотири рівні</h2><p class="sub">Перший рівень — безкоштовно в кожному корпоративному замовленні. Решта — залежно від строків: що встигаємо до вашої дати й скільки це коштує, пишемо в розрахунку.</p>
<div class="grid4p">{pers}</div>
<p class="foot">Фото — приклади пакування, речей і сертифіката Obiimy; як виглядатиме наліпка чи бирка з вашим логотипом, покажемо в добірці. Напишіть дату — скажемо, які рівні встигаємо; контакти на с. 14.</p>''')

# 8 how it works
page(f'''<div class="two"><div class="txt"><p class="eb">Що буде після запиту</p><h2>Від запиту до відправки</h2>
  <ol class="steps"><li><b>Запит.</b> Нагоди, кількість і дата, до якої потрібні подарунки.</li>
  <li><b>Добірка й розрахунок.</b> Речі та принти, розрахунок окремими рядками: речі, оформлення привітання, доставка. Чи встигаємо до вашої дати — пишемо одразу.</li>
  <li><b>Список і привітання.</b> Ви надсилаєте список отримувачів і текст привітання.</li>
  <li><b>Відправка.</b> Новою поштою — кожному окремо чи в офіс, як домовимось. Для колег за кордоном — спосіб і вартість назвемо в розрахунку; найпростіше для них — електронний сертифікат.</li></ol>
  <p class="foot">Не впевнені — почніть із малого: подарунки на дні народження одного місяця. Побачите речі, пакування й привітання, перш ніж планувати рік.</p>
</div><div>{pic("photo/kolo-3.webp", "tall", "50% 20%")}</div></div>''')

# 9 contact
page(f'''<div class="two"><div class="txt"><p class="eb">Запит</p><h2>Отримати добірку й розрахунок</h2>
  <p>Напишіть, скільки подарунків потрібно, на які нагоди й до якої дати, — у відповідь надішлемо добірку та розрахунок. На сторінці для команд є калькулятор плану на рік і форма запиту.</p>
  <p class="contact"><b>Співпраця</b><br>{PHONE} · Telegram @OBIIMY_sales<br>{MAIL} · obiimy.world<br>Шоурум: {SHOWROOM}</p>
  <p class="foot">Ціни на сторінках — роздрібні, obiimy.world. Розрахунок для компанії — у відповідь на запит.</p>
</div><div>{pic("img/set-zolote.webp", "tall")}</div></div>''')

html = f'''<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>Obiimy — подарунки для команди 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Tenor+Sans&display=swap" rel="stylesheet">
<style>
  @page {{ size: A4 landscape; margin: 0; }}
  * {{ box-sizing: border-box; font-variant-numeric: lining-nums; }}
  html, body {{ margin: 0; background: #FAFAF8; color: #111; font-family: 'Tenor Sans', sans-serif; font-size: 10.5pt; line-height: 1.5; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .pg {{ width: 297mm; height: 210mm; padding: 16mm 18mm; page-break-after: always; break-after: page; overflow: hidden; position: relative; display: flex; flex-direction: column; }}
  .pg.nopad {{ padding: 0; }}
  h1, h2, h3 {{ font-family: 'Cormorant Garamond', serif; font-weight: 300; margin: 0; line-height: 1.05; }}
  h1 {{ font-size: 44pt; }} h2 {{ font-size: 26pt; margin-bottom: 6mm; }} h3 {{ font-size: 14pt; margin-top: 2mm; }}
  p {{ margin: 0 0 3mm; }}
  .eb {{ font-size: 7.5pt; letter-spacing: .22em; text-transform: uppercase; color: #6B6772; margin-bottom: 2mm; }}
  .sub {{ color: #4A4A47; margin-top: -3mm; margin-bottom: 5mm; }}
  img {{ display: block; object-fit: cover; }}
  .cover {{ position: relative; width: 100%; height: 100%; }}
  .cover .full {{ width: 100%; height: 100%; }}
  .cover::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 35%, rgba(0,0,0,.62) 100%); }}
  .cover-t {{ z-index: 1; position: absolute; left: 18mm; bottom: 14mm; max-width: 52%; color: #fff; text-shadow: 0 2px 30px rgba(0,0,0,.4); }}
  .cover-t .logo {{ height: 12mm; width: auto; margin-bottom: 8mm; object-fit: contain; }}
  .cover-t p {{ font-size: 12pt; margin-top: 4mm; }}
  .two {{ display: grid; grid-template-columns: 1fr 1.1fr; gap: 14mm; height: 100%; }}
  .tall {{ width: 100%; height: 178mm; }}
  .txt {{ align-self: center; }}
  .cols3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10mm; margin-bottom: 8mm; }}
  .cols3 p {{ color: #4A4A47; font-size: 10pt; }}
  .strip {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; flex: 1; min-height: 0; }}
  .strip img {{ width: 100%; height: 100%; background: #fff; }}
  .grid4t {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 5mm 8mm; }}
  .occ {{ border-top: 1px solid #111; padding-top: 3mm; }}
  .occ b {{ font-family: 'Cormorant Garamond', serif; font-size: 18pt; font-weight: 300; }}
  .occ h3 {{ font-size: 13pt; margin: 1mm 0 2mm; }}
  .occ p {{ font-size: 9.5pt; margin: 0 0 1mm; }}
  .grid4t + .strip {{ min-height: 0; }}
  .occ .alt {{ color: #4A4A47; }}
  .grid5 {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 3mm 6mm; flex: 1; min-height: 0; align-content: start; }}
  .grid5 figure {{ margin: 0; }}
  .grid5 img {{ width: 100%; aspect-ratio: 16/10; object-fit: cover; background: #fff; border: 1px solid #E5E3DD; }}
  .grid5 figcaption b {{ display: block; font-family: 'Cormorant Garamond', serif; font-weight: 400; font-size: 11pt; line-height: 1.05; margin-top: 1.5mm; }}
  .grid5 figcaption span {{ display: block; font-size: 6.5pt; letter-spacing: .1em; text-transform: uppercase; color: #6B6772; margin: .5mm 0; }}
  .grid5 figcaption em {{ display: block; font-style: normal; font-family: 'Cormorant Garamond', serif; font-size: 11.5pt; font-variant-numeric: lining-nums; }}
  .shelves {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8mm; flex: 1; }}
  .shelf {{ border-top: 1px solid #111; padding-top: 4mm; }}
  .shelf h3 {{ font-size: 18pt; margin: 0; }} .shelf .alt {{ color: #4A4A47; font-size: 9.5pt; margin: 1mm 0 3mm; }}
  .shelf ul {{ list-style: none; margin: 0; padding: 0; }} .shelf li {{ display: flex; justify-content: space-between; gap: 4mm; font-size: 10pt; padding: 1.6mm 0; border-bottom: 1px solid #E5E3DD; }}
  .shelf li b {{ font-family: 'Cormorant Garamond', serif; font-weight: 400; font-size: 12pt; white-space: nowrap; font-variant-numeric: lining-nums; }}
  .shelves + .strip {{ margin-top: 6mm; max-height: 42mm; }}
  .shelf .ex {{ margin-top: 3mm; font-size: 9.5pt; color: #4A4A47; }}
  .grid3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 5mm 8mm; }}
  .cat img {{ width: 100%; aspect-ratio: 16/8; object-fit: cover; background: #fff; border: 1px solid #E5E3DD; }}
  .cat h3 {{ font-size: 12.5pt; }}
  .cat p {{ font-size: 9pt; color: #4A4A47; margin: 1mm 0; }}
  .cat .rrp {{ font-family: 'Cormorant Garamond', serif; font-size: 12pt; color: #111; }}
  .two-rows {{ display: grid; grid-template-rows: 1fr 1fr; gap: 6mm; height: 100%; }}
  .grid4s {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6mm; }}
  .grid4s figure {{ margin: 0; display: grid; grid-template-columns: 34mm 1fr; gap: 4mm; align-items: center; }}
  .grid4s img {{ width: 34mm; height: 34mm; background: #fff; border: 1px solid #E5E3DD; }}
  .grid4s figcaption b {{ display: block; font-family: 'Cormorant Garamond', serif; font-weight: 400; font-size: 12pt; line-height: 1.15; }}
  .grid4s figcaption span {{ font-size: 9.5pt; color: #4A4A47; }}
  .tiers {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8mm; }}
  .tiers {{ flex: 1; align-content: start; }}
  .tier {{ border: 1px solid #DDD9D1; padding: 8mm; background: #fff; }}
  .tier .pp {{ font-family: 'Cormorant Garamond', serif; font-size: 26pt; line-height: 1; margin: 2mm 0 3mm; }}
  .tier .pp small {{ display: block; font-family: 'Tenor Sans', sans-serif; font-size: 8pt; color: #6B6772; margin-top: 1mm; }}
  .tier p {{ font-size: 10pt; color: #4A4A47; }}
  .tier ul {{ list-style: none; margin: 0; padding: 0; }}
  .tier li {{ border-top: 1px solid #E5E3DD; padding: 3.5mm 0; font-size: 10pt; }}
  .tier li b {{ display: block; color: #111; }} .tier li span {{ display: block; color: #4A4A47; }}
  .steps {{ margin: 0; padding-left: 5mm; }} .steps li {{ margin-bottom: 3mm; color: #4A4A47; }} .steps b {{ color: #111; }}
  .adv-t {{ align-self: stretch; display: flex; flex-direction: column; justify-content: center; }}
  .adv-i {{ display: grid; grid-template-columns: 14mm 1fr; gap: 3mm; border-top: 1px solid #C9C6C0; padding: 5mm 0 4mm; }}
  .adv-i b {{ font-family: 'Cormorant Garamond', serif; font-weight: 300; font-size: 20pt; line-height: 1; }}
  .adv-i h3 {{ font-size: 15pt; margin: 0 0 1.5mm; }} .adv-i p {{ font-size: 10pt; color: #4A4A47; margin: 0; }}
  .grid4f {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8mm; flex: 1; align-content: start; }}
  .four {{ display: flex; flex-direction: column; border-top: 1px solid #C9C6C0; padding-top: 3mm; }}
  .four .eb {{ margin: 3mm 0 0; min-height: 8mm; }}
  .four img.ct {{ object-fit: contain; padding: 3mm; }}
  .four .n {{ display: block; font-family: 'Cormorant Garamond', serif; font-weight: 300; font-size: 16pt; line-height: 1; margin-bottom: 2mm; }}
  .four img {{ width: 100%; aspect-ratio: 1/1; object-fit: cover; background: #fff; border: 1px solid #E5E3DD; }}
  .four h3 {{ font-size: 16pt; margin: 1mm 0 2mm; min-height: 13mm; }}
  .four p {{ font-size: 10.5pt; color: #4A4A47; margin: 0 0 1.5mm; }}
  .four .pz {{ margin-top: auto; padding-top: 3mm; }}
  .four .rrp {{ font-family: 'Cormorant Garamond', serif; font-size: 20pt; color: #111; line-height: 1.1; white-space: nowrap; }}
  .four .nt {{ font-size: 8pt; min-height: 10mm; margin: 1mm 0 0; color: #6B6772; }}
  .grid4p {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8mm; flex: 1; min-height: 0; margin-bottom: 4mm; }}
  .per {{ border-top: 1px solid #C9C6C0; padding-top: 3mm; display: flex; flex-direction: column; }}
  .per .nt {{ font-size: 8.5pt; color: #6B6772; margin: 1mm 0 5mm; }} .per .nt.free {{ color: #111; }}
  .per .free {{ font-family: 'Cormorant Garamond', serif; font-size: 16pt; line-height: 1; margin: 2mm 0 0; }}
  .per .free + .nt {{ margin-top: 1mm; }}
  .per img {{ width: 100%; height: 64mm; flex: none; margin-top: auto; padding-top: 0; background: #fff; border: 1px solid #E5E3DD; }}
  .per b {{ font-family: 'Cormorant Garamond', serif; font-weight: 300; font-size: 20pt; line-height: 1; }}
  .per h3 {{ font-size: 14pt; margin: 1.5mm 0 2mm; }} .per p {{ font-size: 9.5pt; color: #4A4A47; margin: 0; }}
  .foot {{ font-size: 8.5pt; color: #6B6772; margin-top: auto; }}
  .contact {{ margin-top: 6mm; font-size: 12pt; line-height: 1.6; }}
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
