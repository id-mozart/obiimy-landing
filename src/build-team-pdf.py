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
LANDING = "https://obiimy-landing-production.up.railway.app/b2b-team"

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
  <p>Український бренд шовкових аксесуарів. Засновниця й художниця — Світлана Сніжко: кожен принт авторський. 100% італійський шовк, виготовлено в Україні, край хустки обробляють вручну.</p>
  <p>Бренд заснований під час війни й бере участь у благодійних ініціативах. Колекція «Співоча душа» присвячена рідкісним птахам: частина коштів іде на гнізда для сиворакші з Червоної книги України.</p>
  <p>Роздрібні партнери: INTERTOP і Hram в Україні, Be Brave у Канаді, UFD London. Про бренд писали LIGA.net та INSIDER UA.</p>
  <p class="foot">Шоурум: {SHOWROOM} — шовк можна побачити й відчути на дотик.</p>
</div></div>''')

# 3 why gifts inside the company
page(f'''<p class="eb">Навіщо</p><h2>Подарунок від компанії, який пам’ятають</h2>
<div class="cols3">
  <div><h3>Річ, а не сувенір</h3><p>Шовкову річ носять: на шию, у волосся, на сумку. Маска для сну чи наволочка — щодня вдома. Це не блокнот із логотипом, який лишається в шухляді.</p></div>
  <div><h3>Слова від компанії</h3><p>До кожного подарунка — привітання вашими словами: до дня народження, річниці, закритого проєкту. Текст пишете ви, оформлення узгоджуємо в розрахунку.</p></div>
  <div><h3>Для всієї команди</h3><p>У каталозі є речі, що підходять усім: закладка для книги, маска для сну, однотонна наволочка, сертифікат, який людина обирає сама.</p></div>
</div>
<div class="strip">{pic("photo/bag-1.webp")}{pic("img/sets/scr3.webp")}{pic("img/mask-svoboda.webp")}{pic("img/sets/pillow-tuman.webp")}</div>''')

# 4 occasions
occ = "".join(f'<div class="occ"><b>{i + 1}</b><h3>{t}</h3><p>{full(s)}</p><p class="alt">{"Підходить усім" if s == n else "Для всіх: " + full(n)}</p></div>'
              for i, (sid, short, t, d, p, a, s, n, sh) in enumerate(STAGES))
page(f'''<p class="eb">Нагоди</p><h2>Шлях людини в компанії — вісім нагод</h2><p class="sub">Що радимо подарувати на кожну. Ціни роздрібні, obiimy.world.</p>
<div class="grid4t">{occ}</div>
<div class="strip" style="margin-top:8mm">{pic("img/twilly-zolote.webp")}{pic("img/scrunchie-pole.webp")}{pic("photo/kolo-3.webp", "", "50% 20%")}{pic("photo/mizh-1.webp", "", "50% 10%")}</div>''')

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
<p class="foot" style="font-size:10pt;color:#4A4A47">Приклад: команда з 40 людей, програма «Команда», 16 отримують речі «для всіх», 5 ключовим людям — набір «твіллі та хустка» = 108 000 грн на рік за роздрібними цінами, без доставки.</p>''')

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
  <p class="foot">Сторінка для команд: {LANDING}</p>
</div><div>{pic("img/set-zolote.webp", "tall")}</div></div>''')

html = f'''<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>Obiimy — подарунки для команди 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Tenor+Sans&display=swap" rel="stylesheet">
<style>
  @page {{ size: A4 landscape; margin: 0; }}
  * {{ box-sizing: border-box; }}
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
