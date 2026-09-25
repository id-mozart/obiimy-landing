#!/usr/bin/env python3
"""Static wholesale lookbook: lookbook.html (A4 landscape pages) -> lookbook-obiimy-2026.pdf via headless Chrome."""
import pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent

def pic(src, cls=""):
    p = pathlib.Path(src)
    from PIL import Image
    lb = OUT / "review" / "lb"; lb.mkdir(parents=True, exist_ok=True)
    j = lb / (p.stem + ".jpg")
    if not j.exists():
        im = Image.open(OUT / src).convert("RGB"); im.thumbnail((1100, 1100)); im.save(j, quality=72, optimize=True)
    src = "review/lb/" + j.name
    return f'<img src="{src}" class="{cls}" alt="">'

PAGES = []
def page(html, cls=""): PAGES.append(f'<section class="pg {cls}">{html}</section>')

page(f'''
  <div class="cover">{pic("photo/paris-dots.jpg", "full")}<div class="cover-t"><img src="brand/logo-white.png" class="logo" alt="Obiimy"><h1>Лукбук<br>для партнерів</h1><p>Шовкові хустки з авторськими принтами · 2026</p></div></div>''', "nopad")

page(f'''
  <div class="two"><div>{pic("img/life2.webp", "tall")}</div><div class="txt">
    <p class="eb">Про бренд</p><h2>Obiimy — обійми з шовку</h2>
    <p>Український бренд шовкових хусток, заснований художницею Світланою Сніжко. Кожен принт — авторська картина, надрукована на 100% італійському шовку; край обробляється вручну, тому розмір може відхилятися на 0–2,5 см.</p>
    <p>Бренд народився під час війни й підтримує благодійні проєкти: колекція «Співоча душа» створена разом із художницею Анною Кловак та Українським товариством охорони птахів — частина коштів іде на гніздівлі для сиворакші.</p>
    <p>Роздрібні партнери: INTERTOP, Hram (Україна), Be Brave (Канада), UFD London (Велика Британія). Про бренд писали LIGA.net та INSIDER UA. Рейтинг покупців на obiimy.world — 5,0.</p>
  </div></div>''')

cats = [
    ("Хустки 44 × 44 · 65 × 65 · 88 × 88", "Три розміри, авторські принти, хіти «Єднання» та «Пробудження».", "1 600 · 3 200 · 4 400 грн", "img/probudzhennia.webp"),
    ("Двосторонній друк", "Два принти на одній хустці: 44 × 44 та 65 × 65.", "2 400 · 4 800 грн", "img/yednannia.webp"),
    ("Твіллі 84 × 5", "На сумку, у волосся, на зап’ястя, як пояс.", "1 600 грн", "img/twilly-zolote.webp"),
    ("Маски для сну", "Шовк, авторський принт, фірмова коробка.", "2 700 грн", "img/mask-vpevnenist.webp"),
    ("Резинки для волосся", "У фірмовій жовтій коробочці.", "700 грн", "img/scrunchie-energiia.webp"),
    ("Подарункові набори", "Твіллі + резинка · твіллі + хустка · набір для сну · три твіллі.", "2 200 · 3 200 · 3 600 · 4 800 грн", "img/set-natkhnennia.webp"),
]
page('<p class="eb">Асортимент</p><h2>Шість категорій</h2><div class="grid3">' + "".join(f'<div class="cat">{pic(ph)}<h3>{t}</h3><p>{d}</p><p class="rrp">РРЦ {pr}</p></div>' for t, d, pr, ph in cats) + '</div><p class="foot">РРЦ — рекомендована роздрібна ціна на obiimy.world. Оптові умови — в прайсі за запитом.</p>')

prints = [("Пробудження", "img/probudzhennia.webp"), ("Єднання", "img/yednannia.webp"), ("Тиша серця", "img/tysha-sertsia.webp"), ("Пристрасть", "img/prystrast.webp"), ("Коло сонця", "img/kolo-sontsia.webp"), ("Мелодія двох", "img/melodiia.webp"), ("Піднесення", "img/pidnesennia.webp"), ("Між нами", "img/mizh-namy.webp"), ("Літнє поле", "img/litnie-pole.webp"), ("Поцілунок", "img/potsilunok.webp")]
page('<p class="eb">Принти</p><h2>Авторські картини на шовку</h2><div class="grid5">' + "".join(f'<figure>{pic(ph)}<figcaption>{n}</figcaption></figure>' for n, ph in prints) + '</div>')

def shoot(title, sub, photos, cls="grid4"):
    page(f'<p class="eb">Зйомка</p><h2>{title}</h2><p class="sub">{sub}</p><div class="{cls}">' + "".join(pic(p) for p in photos) + '</div>')
shoot("Париж, осінь", "Хустки, твіллі та резинки у міському гардеробі.", ["photo/paris-blazer.jpg", "photo/paris-green.jpg", "photo/paris-bag.jpg", "photo/paris-belt.jpg", "photo/paris-bun.jpg", "photo/paris-dots.jpg", "photo/box-gold.jpg", "photo/box-dots.jpg"])
shoot("Рів’єра, літо", "Хустки 65 і 88 як головний убір, на шиї, на сумці.", ["photo/riviera-car.jpg", "photo/riviera-boat.jpg", "photo/riviera-red.jpg", "photo/turban.jpg", "photo/kolo-2.webp", "photo/dotyk-1.webp", "photo/vyr-2.webp", "photo/makiv-knot.webp"])

page(f'''
  <div class="two"><div>{pic("photo/box-red.jpg", "tall")}</div><div class="txt">
    <p class="eb">Упаковка і сервіс</p><h2>Готова вітрина</h2>
    <p><b>Фірмова жовта коробка</b> з тонким папером і листівкою — для кожної речі. На полиці видно з іншого кінця залу.</p>
    <p><b>Дозамовлення поштучно.</b> Замовлення до 16:00 відправляємо з наявності того ж дня Новою поштою. За кордон — за тарифами перевізника.</p>
    <p><b>Догляд.</b> Ручне прання при температурі до 30 °C, не віджимати, сушити в тіні, прасувати в режимі «шовк» через тонку тканину.</p>
    <p><b>Для консультантів.</b> Три способи носити кожен розмір, догляд, аргументи для подарунка — коротка пам’ятка надається партнерам.</p>
  </div></div>''')

page(f'''
  <div class="two"><div class="txt">
    <p class="eb">Співпраця</p><h2>Три формати</h2>
    <p><b>A · Оптова закупівля.</b> Партія за оптовими цінами, продаж за своєю. Для бутиків і мультибрендів.</p>
    <p><b>B · Корнер бренду.</b> Виділена зона Obiimy з фірмовою викладкою та коробками. Для універмагів і концепт-сторів.</p>
    <p><b>C · Міжнародний партнер.</b> Відправка партій за тарифами перевізника, англомовний контент, сайт obiimy-world.com.</p>
    <p class="contact"><b>Запит оптового прайсу</b><br>+38 067 010 85 25<br>sale@obiimy-world.com<br>obiimy.world</p>
  </div><div>{pic("photo/box-green.jpg", "tall")}</div></div>''')

html = f'''<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>Obiimy — лукбук для партнерів 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Tenor+Sans&display=swap" rel="stylesheet">
<style>
  @page {{ size: A4 landscape; margin: 0; }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; background: #FAFAF8; color: #111; font-family: 'Tenor Sans', sans-serif; font-size: 11pt; line-height: 1.5; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .pg {{ width: 297mm; height: 210mm; padding: 16mm 18mm; page-break-after: always; break-after: page; overflow: hidden; position: relative; display: flex; flex-direction: column; }}
  .pg.nopad {{ padding: 0; }}
  h1, h2, h3 {{ font-family: 'Cormorant Garamond', serif; font-weight: 300; margin: 0; line-height: 1.05; }}
  h1 {{ font-size: 44pt; }} h2 {{ font-size: 26pt; margin-bottom: 6mm; }} h3 {{ font-size: 14pt; margin-top: 3mm; }}
  p {{ margin: 0 0 3mm; }}
  .eb {{ font-size: 7.5pt; letter-spacing: .22em; text-transform: uppercase; color: #6B6772; margin-bottom: 2mm; }}
  .sub {{ color: #4A4A47; margin-top: -3mm; margin-bottom: 5mm; }}
  img {{ display: block; object-fit: cover; }}
  .cover {{ position: relative; width: 100%; height: 100%; }}
  .cover .full {{ width: 100%; height: 100%; object-position: 50% 20%; }}
  .cover::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 35%, rgba(0,0,0,.62) 100%); }}
  .cover-t {{ z-index: 1; position: absolute; left: 18mm; bottom: 14mm; max-width: 50%; color: #fff; text-shadow: 0 2px 30px rgba(0,0,0,.4); }}
  .cover-t .logo {{ height: 12mm; width: auto; margin-bottom: 8mm; object-fit: contain; }}
  .cover-t p {{ font-size: 12pt; margin-top: 4mm; }}
  .two {{ display: grid; grid-template-columns: 1fr 1.1fr; gap: 14mm; height: 100%; }}
  .tall {{ width: 100%; height: 178mm; }}
  .txt {{ align-self: center; }}
  .grid3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6mm 8mm; }}
  .cat img {{ width: 100%; aspect-ratio: 16/9; object-fit: contain; background: #fff; border: 1px solid #E5E3DD; }}
  .cat p {{ font-size: 9.5pt; color: #4A4A47; margin: 1mm 0; }}
  .cat .rrp {{ font-family: 'Cormorant Garamond', serif; font-size: 12pt; color: #111; }}
  .grid5 {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 5mm 6mm; }}
  .grid5 img {{ width: 100%; aspect-ratio: 1; }}
  .grid5 figure {{ margin: 0; }} .grid5 figcaption {{ font-size: 9pt; margin-top: 1.5mm; color: #4A4A47; }}
  .grid4 {{ display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(2, 1fr); gap: 4mm; flex: 1; min-height: 0; }}
  .grid4 img {{ width: 100%; height: 100%; }}
  .foot {{ font-size: 8.5pt; color: #6B6772; margin-top: auto; }}
  .contact {{ margin-top: 8mm; font-size: 12pt; line-height: 1.6; }}
</style></head><body>{"".join(PAGES)}</body></html>'''
sys.path.insert(0, str(ROOT))
from imgs import typo
(OUT / "lookbook.html").write_text(typo(html))
import re as _re
nop = _re.sub(r'<p class="rrp">[^<]*</p>', '', html)
nop = nop.replace('<p class="foot">РРЦ — рекомендована роздрібна ціна на obiimy.world. Оптові умови — в прайсі за запитом.</p>', '<p class="foot">Ціни та умови — за запитом.</p>')
(OUT / "lookbook-noprice.html").write_text(typo(nop))
print("lookbook.html", len(html) // 1024, "KB")

# render to PDF with puppeteer (review/pp has puppeteer-core)
script = OUT / "review" / "pp" / "pdf.mjs"
script.write_text('''import puppeteer from 'puppeteer-core';
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--no-sandbox', '--allow-file-access-from-files'] });
const p = await b.newPage();
await p.goto('file:///Users/ivan/obiimy/lookbook.html', { waitUntil: 'networkidle0', timeout: 120000 });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: '/Users/ivan/obiimy/lookbook-obiimy-2026.pdf', printBackground: true, preferCSSPageSize: true });
await p.goto('file:///Users/ivan/obiimy/lookbook-noprice.html', { waitUntil: 'networkidle0', timeout: 120000 });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: '/Users/ivan/obiimy/lookbook-obiimy-2026-noprice.pdf', printBackground: true, preferCSSPageSize: true });
await b.close();
console.log('pdf ok');
''')
subprocess.run(["node", str(script)], cwd=str(script.parent), check=True)
