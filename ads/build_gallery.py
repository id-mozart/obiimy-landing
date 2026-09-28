"""Creatives gallery page for the Railway hub: site/creatives.html + site/creatives/<series>/<file>.
Called from build-site.py; images: full JPG for download, 540px WebP preview for the grid."""
import hashlib, html, pathlib, shutil
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent

SOLO_GROUPS = [
    ("cover-", "Обкладинки журналу SOLO", "Колекція натхненна ретро-обкладинками модних журналів 40–50-х. По одному випуску на кожен принт; журнал лежить на шовку цього принта."),
    ("spot-", "Кольорова хустка", "«Світ навколо стає темно-сірим» — кольорова лише хустка."),
    ("states-", "Сім станів", "Сім принтів — сім станів на шляху жінки до себе. Описи станів — за релізом."),
    ("ya-", "Я є. Я продовжую жити. Я обираю себе.", "Три сторіс поспіль — слова релізу."),
    ("manifest-", "Маніфести", "Цитати з релізу: маленькі акти свободи, гідність і право на жіночність."),
    ("editor-", "Слово бренду", "Органічна сторіс без ціни — дослівна цитата з релізу."),
    ("film-", "Кадр із фільму", "Кіно 50-х: титри, субтитри — слова релізу. «У головній ролі — ви»."),
    ("decades-", "Крізь десятиліття", "1940-ві, 1950-ті, 2026: як хустка змінювалася разом із жінкою."),
    ("epoch-", "Дві епохи в одному кадрі", "Змінювалися епохи й силуети, але хустка залишалася поруч."),
    ("word-", "Стан буквами з шовку", "Назва стану, набрана принтом, і хустка."),
    ("back-", "Задня обкладинка", "Хустка на кольорі свого принта."),
    ("route-", "Маршрут", "Сім станів як сім зупинок на шляху до себе."),
    ("sale-", "Продажі", "Сторіс, що відповідають на питання покупательниці: ціна, подарунок, оплата, доставка, примірка, довіра."),
    ("product-", "Картки товару", "Хустка, стан, формати й роздрібні ціни з obiimy.world."),
    ("twilly-", "Вхідна ціна", "Твіллі — 1 600 грн: сім принтів поруч."),
    ("flirt-", "Один принт — три формати", "«Флірт»: резинка, твіллі, хустка."),
    ("box-", "Жовта коробка", "Фірмове пакування й найдоступніша річ колекції."),
    ("ways-", "Як носити", "Шия, волосся, сумка, зап’ястя."),
    ("price-", "Каталог і ціни", "Усі формати колекції з роздрібними цінами."),
    ("gazette-", "Вісник SOLO", "Передовиця ретрогазети."),
]
OLD = [
    ("final", "Серія 1 · бренд", "Перші 10 сторіс: маска, хустки, жовта коробка, двосторонній друк, «Співоча душа»."),
    ("final2", "Серія 2 · Париж і Рив’єра", "10 сторіс на фешн-зйомках: пояс із хустки, твіллі у волоссі, сумка, ритуал."),
]

def fmt(im):
    w, h = im.size
    return ("Сторіс 9:16", "st") if h / w > 1.6 else (("Стрічка 4:5", "fd") if h / w > 1.1 else ("Квадрат 1:1", "sq"))

def build(site: pathlib.Path):
    out = site / "creatives"; out.mkdir(exist_ok=True)
    sections = []
    toc = []
    HOME = {"out4": "solo-main", "out5": "solo-yellow", "out6": "solo-tri", "out7": "solo-tri-y", "out8": "solo-one", "out9": "solo-orig"}
    def add(title, desc, files, series):
        cards = []
        for f in files:
            # a banner shown in two groups is stored once, in the folder of its own series
            series = HOME.get(f.parent.name, series)
            d = out / series; d.mkdir(exist_ok=True)
            shutil.copy(f, d / f.name)
            im = Image.open(f).convert("RGB"); label, cls = fmt(im)
            prev = d / (f.stem + "-540.webp")
            t = im.copy(); t.thumbnail((540, 960)); t.save(prev, quality=80)
            v = hashlib.md5(f.read_bytes()).hexdigest()[:8]
            cards.append(f'''<figure class="c {cls}" data-f="{cls}"><a href="creatives/{series}/{f.name}?v={v}" target="_blank" rel="noopener"><img src="creatives/{series}/{prev.name}?v={v}" alt="{html.escape(title)}" loading="lazy" width="{t.width}" height="{t.height}"></a>
        <figcaption><span>{label}</span><a href="creatives/{series}/{f.name}?v={v}" download="{f.name}">JPG ↓</a></figcaption></figure>''')
        anchor = f"s{len(toc) + 1}"; toc.append((anchor, title, len(cards)))
        sections.append(f'''<section class="grp" id="{anchor}"><div class="gh"><h3>{title} <span style="font-weight:400;color:var(--ink2)">· {len(cards)}</span></h3><p>{desc}</p></div><div class="grid">{"".join(cards)}</div></section>''')
    classic = sorted((ROOT / "ads/solo/out4").glob("*.jpg"))
    yellow = sorted((ROOT / "ads/solo/out5").glob("*.jpg"))
    isc = lambda f, lo, hi: f.name[0] == "c" and lo <= f.name[:3] <= hi
    tri = sorted((ROOT / "ads/solo/out6").glob("*.jpg")); tri_y = sorted((ROOT / "ads/solo/out7").glob("*.jpg"))
    mono = sorted((ROOT / "ads/solo/out8").glob("m*.jpg"))
    gift_names = ["k14", "t15", "t07"]
    pick = lambda fs, names: [f for n in names for f in fs if f.name.startswith(n)]
    gifts = ([f for f in tri if f.name[0] == "g"] + sorted((ROOT / "ads/solo/out8").glob("g*.jpg")) + pick(tri, gift_names)
             + pick(classic, ["p09", "u06"]))
    gifts_y = [f for f in tri_y if f.name[0] == "g"] + pick(tri_y, gift_names) + pick(yellow, ["p09", "u06"])
    add("Подарункові · варіант A", "Для того, хто дарує: сертифікат, подарунок за бюджетом, кому що подарувати, підпис вашими словами, жовта коробочка, відправка в день замовлення.", gifts, "solo-gift")
    add("Подарункові · варіант B", "Те саме з жовтою плашкою товару.", gifts_y, "solo-gift-y")
    orig = sorted((ROOT / "ads/solo/out9").glob("*.jpg"))
    add("Оригінальні концепції", "Шість ідей з нуля: поштові марки, словник колекції, концертна програма «Соло», музейна стіна, контактний аркуш плівки, бирка зі складом. Є подарункові версії: листівка з підписом, марка «Поштою — до неї», бирка «склад подарунка», «експонат, який можна подарувати».", orig, "solo-orig")
    add("Один образ · одне фото · варіант A", "Один великий кадр на банер: принт, його стан за релізом, ціна; під фото — як носити, товар і кнопка. Сім хусток і три твіллі.", [f for f in tri if f.name[0] == "s"], "solo-tri")
    add("Один образ · одне фото · варіант B", "Те саме з жовтою плашкою товару.", [f for f in tri_y if f.name[0] == "s"], "solo-tri-y")
    add("Лаконічні · один товар", "Одна річ, назва, ціна й кнопка — без розмірів та описів. Хустки на кольорі свого принту й на темному, твіллі на світлому, резинка.", mono, "solo-one")
    add("Приземлені про товар · варіант A", "Без лірики: картка кожної хустки з характеристиками, твіллі й резинка, який розмір обрати, що таке твіллі, як замовити, ціни, подарунок за бюджетом, доставка й оплата.", [f for f in tri if f.name[0] == "k"], "solo-tri")
    add("Приземлені про товар · варіант B", "Те саме з жовтою плашкою товару.", [f for f in tri_y if f.name[0] == "k"], "solo-tri-y")
    add("Продуктові · варіант A", "Товар крупно на кольорі свого принту: кожна хустка окремо, формати від твіллі до 88 × 88, каталоги стрічок і хусток, двосторонній друк, жовта коробка, образи «хустка + твіллі».", [f for f in tri if f.name[0] == "q"], "solo-tri")
    add("Продуктові · варіант B", "Те саме з жовтою плашкою товару.", [f for f in tri_y if f.name[0] == "q"], "solo-tri-y")
    add("Смуги-історії · варіант A", "Дві, три або чотири смуги — одна історія: крізь десятиліття, стани, образи, як носити, кому подарувати, український преміум. Унизу — товар і кнопка.", [f for f in tri if f.name[0] == "t"], "solo-tri")
    add("Смуги-історії · варіант B", "Те саме з жовтою плашкою товару.", [f for f in tri_y if f.name[0] == "t"], "solo-tri-y")
    add("Варіант A · тихий преміум", "Коротко й делікатно: один рядок, товар і ціна без розмірів, м’які заклики.", [f for f in classic if f.name[0] == "p"], "solo-main")
    add("Варіант B · тихий преміум", "Тихий преміум з жовтою плашкою товару.", [f for f in yellow if f.name[0] == "p"], "solo-yellow")
    add("Варіант A · український преміум", "Одне повідомлення, розказане по-різному: це українські шовкові аксесуари преміум-класу.", [f for f in classic if f.name[0] == "u"], "solo-main")
    add("Варіант B · український преміум", "Український преміум з жовтою плашкою товару.", [f for f in yellow if f.name[0] == "u"], "solo-yellow")
    add("Варіант A · повноекранні", "Героїня на весь кадр, внизу — картка товару: вирізана хустка чи твіллі, назва, принт, розмір, ціна.", [f for f in classic if isc(f, "c01", "c13")], "solo-main")
    add("Варіант B · повноекранні", "Те саме, але товар названо на жовтій фірмовій плашці.", [f for f in yellow if isc(f, "c01", "c13")], "solo-yellow")
    add("Варіант A · товарні", "Хустка, твіллі, подарунок, доставка, шоурум — світлий кадр і ціна.", [f for f in classic if isc(f, "c14", "c99")], "solo-main")
    add("Варіант B · товарні", "Світлі кадри з жовтою плашкою: що продаємо, деталі й ціна.", [f for f in yellow if isc(f, "c14", "c99")], "solo-yellow")
    main_html = "".join(sections); sections.clear()
    main_ids = {a for a, _, _ in toc}
    solo = sorted((ROOT / "ads/solo/out").glob("*.jpg"))
    n_solo = len(classic)
    for prefix, title, desc in SOLO_GROUPS:
        fs = [f for f in solo if f.name.startswith(prefix)]
        if fs: add(title, desc, fs, "solo")
    solo_html = "".join(sections); sections.clear()
    n_old = 0
    for folder, title, desc in OLD:
        fs = sorted(f for f in (ROOT / "ads" / folder).glob("obiimy-*.jpg"))
        add(title, desc, fs, folder); n_old += len(fs)
    old_html = "".join(sections)
    page = f'''<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Креативи Obiimy</title>
<meta name="description" content="Рекламні креативи Obiimy: колекція SOLO. Шлях до себе та попередні серії сторіс.">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,900&family=Onest:wght@400;500;600&display=swap">
<style>
:root {{ --bg: #F3EADB; --card: #FBF6EC; --ink: #1B1613; --ink2: #5A5048; --line: rgba(27,22,19,.14); --acc: #7B1F24; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg: #151210; --card: #1F1B18; --ink: #F3EADB; --ink2: #B9AEA3; --line: rgba(243,234,219,.14); --acc: #E3A15A; }} }}
:root[data-theme="dark"] {{ --bg: #151210; --card: #1F1B18; --ink: #F3EADB; --ink2: #B9AEA3; --line: rgba(243,234,219,.14); --acc: #E3A15A; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: 'Onest', Arial, sans-serif; }}
.wrap {{ max-width: 1320px; margin: 0 auto; padding: 32px 24px 80px; }}
header {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; }}
header a {{ color: var(--ink2); text-decoration: none; font-size: .92rem; padding: 10px 0; }}
h1 {{ font-family: 'Playfair Display', serif; font-weight: 900; font-style: italic; font-size: clamp(3rem, 9vw, 7rem); line-height: .9; margin: 48px 0 12px; }}
h2 {{ font-family: 'Playfair Display', serif; font-size: clamp(1.6rem, 3vw, 2.2rem); margin: 64px 0 8px; }}
.lede {{ color: var(--ink2); max-width: 46em; line-height: 1.55; margin: 0; }}
.bar {{ position: sticky; top: 0; z-index: 5; background: var(--bg); border-bottom: 1px solid var(--line); margin: 28px -24px 0; padding: 12px 24px; display: flex; flex-wrap: wrap; gap: 8px; }}
.bar button {{ font: inherit; font-size: .88rem; border: 1px solid var(--line); background: transparent; color: var(--ink); border-radius: 999px; padding: 10px 16px; cursor: pointer; }}
.bar button[aria-pressed="true"] {{ background: var(--ink); color: var(--bg); border-color: var(--ink); }}
.grp {{ margin-top: 40px; scroll-margin-top: 20px; }}
.toc {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 28px; }}
.toc a {{ font-size: .88rem; border: 1px solid var(--line); border-radius: 999px; padding: 10px 16px; color: var(--ink); text-decoration: none; }}
.toc a span {{ color: var(--ink2); }}
.gh h3 {{ margin: 0 0 4px; font-size: 1.15rem; }}
.gh p {{ margin: 0 0 16px; color: var(--ink2); font-size: .92rem; max-width: 60em; line-height: 1.5; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; align-items: start; }}
.c {{ margin: 0; background: var(--card); border: 1px solid var(--line); border-radius: 6px; overflow: hidden; }}
.c img {{ display: block; width: 100%; height: auto; }}
.c figcaption {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; font-size: .8rem; color: var(--ink2); }}
.c figcaption a {{ color: var(--acc); font-weight: 600; text-decoration: none; padding: 6px 0; }}
.hide {{ display: none; }}
footer {{ margin-top: 72px; color: var(--ink2); font-size: .85rem; border-top: 1px solid var(--line); padding-top: 20px; }}
@media (max-width: 560px) {{ .grid {{ grid-template-columns: 1fr 1fr; gap: 10px; }} }}
</style></head><body><div class="wrap">
<header><a href="./">← Усі лендинги Obiimy</a><a href="https://obiimy.world/solo-shliakh-do-sebe/" target="_blank" rel="noopener">Колекція на obiimy.world ↗</a></header>
<h1>SOLO</h1>
<p class="lede"><b>Шлях до себе.</b> Основна серія — {n_solo} банерів 1080 × 1920 для запуску нової колекції Obiimy у стилі попередніх кампаній бренду, у двох варіантах подачі товару: сім авторських принтів — сім станів на шляху жінки до себе. Тексти — за прес-релізом колекції, фото й ціни — з obiimy.world. Увесь текст стоїть у безпечній зоні сторіс. Натисніть на картинку, щоб відкрити в повному розмірі, або «JPG ↓», щоб завантажити.</p>

<nav class="toc">{"".join(f'<a href="#{a}">{t} <span>{n}</span></a>' for a, t, n in toc if a in main_ids)}</nav>
{main_html}
<h2>Альтернативні напрями SOLO</h2>
<p class="lede">Інші підходи до тієї ж колекції: обкладинки журналу, сім станів, кіно, продажні сторіс.</p>
{solo_html}
<h2>Попередні серії</h2>
<p class="lede">{n_old} сторіс для бренду Obiimy загалом.</p>
{old_html}
<footer>Фото й логотип — obiimy.world. Креативи зроблено за допомогою Claude Code.</footer>
</div>
<script>
document.querySelectorAll('.bar button').forEach(function (b) {{
  b.addEventListener('click', function () {{
    document.querySelectorAll('.bar button').forEach(function (x) {{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }});
    var f = b.dataset.f;
    document.querySelectorAll('.c').forEach(function (c) {{ c.classList.toggle('hide', f !== 'all' && c.dataset.f !== f); }});
    document.querySelectorAll('.grp').forEach(function (g) {{ g.classList.toggle('hide', !g.querySelector('.c:not(.hide)')); }});
  }});
}});
</script>
</body></html>
'''
    (site / "creatives.html").write_text(page)
    return n_solo + n_old

if __name__ == "__main__":
    print(build(ROOT / "site"), "creatives")
