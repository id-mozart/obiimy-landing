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
    groups = []      # {part, title, desc, cards: [(id, html)]}
    part = ["main"]
    keep_file = ROOT / "ads" / "keep.txt"
    keep = [l.strip() for l in keep_file.read_text().splitlines() if l.strip() and not l.startswith("#")] if keep_file.exists() else []
    keep_set = set(keep)
    HOME = {"out4": "solo-main", "out5": "solo-yellow", "out6": "solo-tri", "out7": "solo-tri-y", "out8": "solo-one", "out9": "solo-orig"}
    def add(title, desc, files, series):
        cards = []
        for f in files:
            # a banner shown in two groups is stored once, in the folder of its own series
            series = HOME.get(f.parent.name, series)
            d = out / series; d.mkdir(exist_ok=True)
            prev = d / (f.stem + "-540.webp"); dst = d / f.name
            fresh = dst.exists() and prev.exists() and dst.stat().st_mtime >= f.stat().st_mtime and prev.stat().st_mtime >= f.stat().st_mtime
            if fresh:       # unchanged since the last build: keep the copy and the preview
                with Image.open(prev) as t: t.load()
                with Image.open(f) as im0: label, cls = fmt(im0)
            else:
                shutil.copy(f, dst)
                im = Image.open(f).convert("RGB"); label, cls = fmt(im)
                t = im.copy(); t.thumbnail((540, 960)); t.save(prev, quality=80)
            v = hashlib.md5(f.read_bytes()).hexdigest()[:8]
            cards.append((f"{series}/{f.name}", f'''<figure class="c {cls}" data-f="{cls}" data-id="{series}/{f.name}"><a href="creatives/{series}/{f.name}?v={v}" target="_blank" rel="noopener"><img src="creatives/{series}/{prev.name}?v={v}" alt="{html.escape(title)}" loading="lazy" width="{t.width}" height="{t.height}"></a>
        <figcaption><label class="pick"><input type="checkbox" data-id="{series}/{f.name}"><span>Залишити</span></label><span class="fid">{f.stem.split("-")[0]}</span><a href="creatives/{series}/{f.name}?v={v}" download="{f.name}">JPG ↓</a></figcaption></figure>'''))
        groups.append(dict(part=part[0], title=title, desc=desc, cards=cards))
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
    part[0] = "solo"
    solo = sorted((ROOT / "ads/solo/out").glob("*.jpg"))
    n_solo = len(classic)
    for prefix, title, desc in SOLO_GROUPS:
        fs = [f for f in solo if f.name.startswith(prefix)]
        if fs: add(title, desc, fs, "solo")
    part[0] = "old"
    n_old = 0
    for folder, title, desc in OLD:
        fs = sorted(f for f in (ROOT / "ads" / folder).glob("obiimy-*.jpg"))
        add(title, desc, fs, folder); n_old += len(fs)
    H2 = {"solo": ("Альтернативні напрями SOLO", "Інші підходи до тієї ж колекції: обкладинки журналу, сім станів, кіно, продажні сторіс."),
          "old": ("Попередні серії", "Сторіс для бренду Obiimy загалом.")}
    def pl(n):
        """Ukrainian plural of «банер»."""
        return "банер" if n % 10 == 1 and n % 100 != 11 else ("банери" if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14 else "банерів")
    def body(select):
        """Sections of the page for the cards that pass `select(id)`; returns (toc_html, body_html, number of cards)."""
        toc, html_, n, seen = [], [], 0, set()
        for pt in ("main", "solo", "old"):
            secs = []
            for g in groups:
                if g["part"] != pt: continue
                cards = [c for i, c in g["cards"] if select(i)]
                if not cards: continue
                seen.update(i for i, _ in g["cards"] if select(i))
                anchor = f"s{len(toc) + 1}"; toc.append((anchor, g["title"], len(cards), pt))
                secs.append(f'''<section class="grp" id="{anchor}"><div class="gh"><h3>{g["title"]} <span style="font-weight:400;color:var(--ink2)">· {len(cards)}</span></h3><p>{g["desc"]}</p></div><div class="grid">{"".join(cards)}</div></section>''')
            if secs:
                if pt in H2: html_.append(f'<h2>{H2[pt][0]}</h2>\n<p class="lede">{H2[pt][1]}</p>')
                html_ += secs
        toc_html = "".join(f'<a href="#{a}">{t} <span>{k}</span></a>' for a, t, k, pt in toc)
        return toc_html, "\n".join(html_), len(seen)
    def flat(select):
        """One gallery without groups: every selected banner once, in the order of the series."""
        seen, cards = set(), []
        for g in groups:
            for i, c in g["cards"]:
                if select(i) and i not in seen: seen.add(i); cards.append(c)
        return f'<section class="grp flat"><div class="grid">{"".join(cards)}</div></section>', len(cards)
    all_ids = {i for g in groups for i, _ in g["cards"]}
    n_keep = len(keep_set & all_ids)
    import json
    defaults = json.dumps(sorted(keep_set & all_ids), ensure_ascii=False)

    def render(top, toc_html, body_html):
        return f'''<!DOCTYPE html>
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
.grp.flat {{ margin-top: 28px; }}
header.solo {{ justify-content: flex-end; }}
.vh {{ position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; font-size: 1rem; }}
.c > a {{ display: block; cursor: zoom-in; }}
#lb {{ border: 0; padding: 0; margin: 0; background: transparent; color: #F3EADB; width: 100vw; height: 100dvh; max-width: 100vw; max-height: 100dvh; overflow: hidden; }}
#lb::backdrop {{ background: rgba(10,8,7,.88); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); }}
#lb .stage {{ position: absolute; inset: 0; display: grid; grid-template-rows: 1fr auto; justify-items: center; align-items: center; gap: 14px; padding: 20px 16px 18px; }}
#lb img {{ display: block; max-width: min(100%, calc(100vw - 32px)); max-height: calc(100dvh - 118px); width: auto; height: auto; border-radius: 10px; box-shadow: 0 30px 80px rgba(0,0,0,.6); background: #1F1B18; }}
#lb[open] img {{ animation: lbin .28s cubic-bezier(.2,.7,.2,1); }}
@keyframes lbin {{ from {{ opacity: .35; transform: scale(.96) translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
@media (prefers-reduced-motion: reduce) {{ #lb[open] img {{ animation: none; }} }}
#lb .row {{ display: flex; align-items: center; gap: 18px; flex-wrap: wrap; justify-content: center; font-size: .95rem; }}
#lb .row a {{ color: #E3A15A; font-weight: 600; text-decoration: none; padding: 10px 4px; }}
#lb .row .pick {{ color: #F3EADB; }}
#lb .n {{ opacity: .7; font-variant-numeric: tabular-nums; }}
#lb button {{ font: inherit; color: #F3EADB; background: rgba(243,234,219,.12); border: 1px solid rgba(243,234,219,.28); border-radius: 999px; width: 52px; height: 52px; font-size: 1.4rem; line-height: 1; cursor: pointer; position: absolute; z-index: 2; display: grid; place-items: center; }}
#lb button:hover {{ background: rgba(243,234,219,.22); }}
#lb button:focus-visible, #lb a:focus-visible {{ outline: 2px solid #E3A15A; outline-offset: 2px; }}
#lb .x {{ top: 16px; right: 16px; }}
#lb .pv {{ left: 16px; top: 50%; margin-top: -26px; }}
#lb .nx {{ right: 16px; top: 50%; margin-top: -26px; }}
@media (max-width: 640px) {{ #lb .pv, #lb .nx {{ top: auto; bottom: 70px; margin: 0; }} #lb img {{ max-height: calc(100dvh - 190px); }} #lb .stage {{ padding-bottom: 14px; }} }}
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
.picks {{ position: sticky; top: 0; z-index: 6; background: var(--bg); border-bottom: 1px solid var(--line); margin: 24px -24px 0; padding: 10px 24px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
.picks b {{ font-size: .95rem; margin-right: 8px; white-space: nowrap; }}
.picks button {{ font: inherit; font-size: .88rem; border: 1px solid var(--line); background: transparent; color: var(--ink); border-radius: 999px; padding: 10px 16px; cursor: pointer; }}
.picks button[aria-pressed="true"], .picks button.ok {{ background: var(--ink); color: var(--bg); border-color: var(--ink); }}
.pick {{ display: inline-flex; align-items: center; gap: 8px; cursor: pointer; color: var(--ink); font-weight: 500; padding: 6px 0; min-height: 32px; }}
.pick input {{ width: 22px; height: 22px; accent-color: var(--acc); cursor: pointer; margin: 0; }}
.fid {{ font-variant-numeric: tabular-nums; opacity: .7; }}
.c.on {{ outline: 3px solid var(--acc); outline-offset: -1px; }}
.grp.flat .c {{ position: relative; border: 0; background: transparent; }}
.grp.flat .c img {{ border-radius: 6px; }}
.grp.flat .c figcaption {{ position: absolute; left: 0; right: 0; bottom: 0; border-radius: 0 0 6px 6px; color: #F3EADB; background: linear-gradient(180deg, rgba(12,9,8,0), rgba(12,9,8,.86) 46%); padding: 34px 14px 10px; opacity: 0; transition: opacity .15s; }}
.grp.flat .c figcaption a {{ color: #E3A15A; }}
.grp.flat .c .pick {{ color: #F3EADB; }}
.grp.flat .c:hover figcaption, .grp.flat .c:focus-within figcaption {{ opacity: 1; }}
@media (hover: none) {{ .grp.flat .c figcaption {{ opacity: 1; }} }}
.c .pick {{ opacity: 0; transition: opacity .15s; }}
.c figcaption a {{ white-space: nowrap; }}
@media (max-width: 560px) {{ .c .pick span {{ display: none; }} .c figcaption {{ padding: 6px 10px; }} }}
.c:hover .pick, .c:focus-within .pick {{ opacity: 1; }}
@media (hover: none) {{ .c .pick {{ opacity: 1; }} }}
.grp.flat .c.on {{ outline: none; }}
.grp.flat .c:not(.on) img {{ opacity: .45; }}
.grp.flat .c:not(.on):hover img, .grp.flat .c:not(.on):focus-within img {{ opacity: 1; }}
.grp, h2 {{ scroll-margin-top: 76px; }}
#out {{ display: none; width: 100%; min-height: 120px; margin-top: 8px; font: .85rem/1.4 ui-monospace, Menlo, monospace; padding: 10px; border: 1px solid var(--line); border-radius: 6px; background: var(--card); color: var(--ink); }}
footer {{ margin-top: 72px; color: var(--ink2); font-size: .85rem; border-top: 1px solid var(--line); padding-top: 20px; }}
@media (max-width: 560px) {{ .grid {{ grid-template-columns: 1fr 1fr; gap: 10px; }} }}
</style></head><body><div class="wrap">
{top}

<div class="picks" role="region" aria-label="Відбір банерів"><b id="pn">Відмічено: 0</b>
<button type="button" id="only" aria-pressed="false">Лише відмічені</button>
<button type="button" id="copy">Скопіювати список</button>
<button type="button" id="link">Скопіювати посилання з відбором</button>
<button type="button" id="clear">Очистити</button>
<textarea id="out" readonly aria-label="Список відмічених банерів"></textarea></div>
{f'<nav class="toc">{toc_html}</nav>' if toc_html else ""}
{body_html}
<footer>Фото й логотип — obiimy.world. Креативи зроблено за допомогою Claude Code.</footer>
</div>
<dialog id="lb" aria-label="Перегляд банера">
  <div class="stage">
    <img alt="" width="1080" height="1920">
    <div class="row"><label class="pick"><input type="checkbox" id="lbc"><span>Залишити</span></label><span class="n" id="lbn"></span><a id="lbd" download>JPG ↓</a></div>
  </div>
  <button type="button" class="pv" aria-label="Попередній банер">←</button>
  <button type="button" class="nx" aria-label="Наступний банер">→</button>
  <button type="button" class="x" aria-label="Закрити">×</button>
</dialog>
<script>
document.querySelectorAll('.bar button').forEach(function (b) {{
  b.addEventListener('click', function () {{
    document.querySelectorAll('.bar button').forEach(function (x) {{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }});
    var f = b.dataset.f;
    document.querySelectorAll('.c').forEach(function (c) {{ c.classList.toggle('hide', f !== 'all' && c.dataset.f !== f); }});
    document.querySelectorAll('.grp').forEach(function (g) {{ g.classList.toggle('hide', !g.querySelector('.c:not(.hide)')); }});
  }});
}});
(function () {{
  var KEY = 'obiimy-picks-v1', picks = new Set(), only = false;
  var DEF = {defaults}, stored = null;
  try {{ stored = localStorage.getItem(KEY); }} catch (e) {{}}
  try {{ (stored ? JSON.parse(stored) : DEF).forEach(function (x) {{ picks.add(x); }}); }} catch (e) {{}}
  var m = location.hash.match(/sel=([^&]+)/);
  if (m) decodeURIComponent(m[1]).split(',').forEach(function (x) {{ if (x) picks.add(x); }});
  var boxes = [].slice.call(document.querySelectorAll('.c .pick input'));
  function list() {{
    var seen = new Set(), out = [];
    boxes.forEach(function (b) {{ if (b.checked && !seen.has(b.dataset.id)) {{ seen.add(b.dataset.id); out.push(b.dataset.id); }} }});
    picks.forEach(function (x) {{ if (!seen.has(x)) {{ seen.add(x); out.push(x); }} }});   // picked on the other page
    return out;
  }}
  function paint() {{
    boxes.forEach(function (b) {{
      b.checked = picks.has(b.dataset.id);
      var c = b.closest('.c'); c.classList.toggle('on', b.checked);
      c.classList.toggle('hide', only && !b.checked);
    }});
    document.querySelectorAll('.grp').forEach(function (g) {{ g.classList.toggle('hide', !g.querySelector('.c:not(.hide)')); }});
    document.getElementById('pn').textContent = 'Відмічено: ' + list().length;
    try {{ localStorage.setItem(KEY, JSON.stringify(Array.from(picks))); }} catch (e) {{}}
  }}
  boxes.forEach(function (b) {{ b.addEventListener('change', function () {{ if (b.checked) picks.add(b.dataset.id); else picks.delete(b.dataset.id); paint(); }}); }});
  function copy(text, btn) {{
    var out = document.getElementById('out'); out.value = text; out.style.display = 'block';
    function done() {{ var t = btn.textContent; btn.textContent = 'Скопійовано'; btn.classList.add('ok'); setTimeout(function () {{ btn.textContent = t; btn.classList.remove('ok'); out.style.display = 'none'; }}, 1600); }}
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function () {{ out.focus(); out.select(); }});
    else {{ out.focus(); out.select(); try {{ document.execCommand('copy'); done(); }} catch (e) {{}} }}
  }}
  document.getElementById('only').addEventListener('click', function () {{ only = !only; this.setAttribute('aria-pressed', only ? 'true' : 'false'); paint(); }});
  document.getElementById('copy').addEventListener('click', function () {{ var l = list(); copy('Залишити для подальшої роботи (' + l.length + '):\\n' + l.join('\\n'), this); }});
  document.getElementById('link').addEventListener('click', function () {{ copy(location.origin + location.pathname + '#sel=' + encodeURIComponent(list().join(',')), this); }});
  document.getElementById('clear').addEventListener('click', function () {{ if (confirm('Зняти всі позначки?')) {{ picks.clear(); paint(); }} }});
  paint();

  // popup viewer
  var lb = document.getElementById('lb'), im = lb.querySelector('img'), items = [], cur = 0;
  var lbc = document.getElementById('lbc'), lbn = document.getElementById('lbn'), lbd = document.getElementById('lbd');
  function show(i) {{
    items = [].slice.call(document.querySelectorAll('.c:not(.hide)'));
    if (!items.length) return;
    cur = (i + items.length) % items.length;
    var c = items[cur], a = c.querySelector('a');
    im.style.animation = 'none'; im.offsetWidth; im.style.animation = '';
    im.src = a.href; im.alt = 'Банер ' + c.querySelector('.fid').textContent;
    lbd.href = a.href; lbd.setAttribute('download', c.dataset.id.split('/').pop());
    lbc.checked = picks.has(c.dataset.id);
    lbn.textContent = c.querySelector('.fid').textContent + ' · ' + (cur + 1) + ' / ' + items.length;
    var nx = items[(cur + 1) % items.length].querySelector('a'); (new Image()).src = nx.href;
  }}
  document.addEventListener('click', function (e) {{
    var a = e.target.closest ? e.target.closest('.c > a') : null;
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    if (!lb.showModal) return;
    e.preventDefault();
    var all = [].slice.call(document.querySelectorAll('.c:not(.hide)'));
    show(all.indexOf(a.parentNode)); lb.showModal();
  }});
  lb.querySelector('.x').addEventListener('click', function () {{ lb.close(); }});
  lb.querySelector('.pv').addEventListener('click', function () {{ show(cur - 1); }});
  lb.querySelector('.nx').addEventListener('click', function () {{ show(cur + 1); }});
  lb.addEventListener('click', function (e) {{ if (e.target === lb || e.target.classList.contains('stage')) lb.close(); }});
  lb.addEventListener('keydown', function (e) {{ if (e.key === 'ArrowLeft') show(cur - 1); else if (e.key === 'ArrowRight') show(cur + 1); }});
  lbc.addEventListener('change', function () {{ var id = items[cur].dataset.id; if (lbc.checked) picks.add(id); else picks.delete(id); paint(); }});
}})();
</script>
</body></html>
'''
    lede_main = '''<p class="lede"><b>Шлях до себе.</b> Основна серія — {n_solo} банерів 1080 × 1920 для запуску нової колекції Obiimy у стилі попередніх кампаній бренду, у двох варіантах подачі товару: сім авторських принтів — сім станів на шляху жінки до себе. Тексти — за прес-релізом колекції, фото й ціни — з obiimy.world. Увесь текст стоїть у безпечній зоні сторіс. Натисніть на картинку, щоб відкрити в повному розмірі, або «JPG ↓», щоб завантажити.</p>'''.replace("{n_solo}", str(n_solo))
    arch_nav = '<a href="https://obiimy.world/solo-shliakh-do-sebe/" target="_blank" rel="noopener">Колекція на obiimy.world ↗</a>'
    if n_keep:
        body_html, n = flat(lambda i: i in keep_set); toc_html = ""
        lede = (f'<p class="lede"><b>Шлях до себе.</b> Відібрано для подальшої роботи — {n} {pl(n)} 1080 × 1920. Решта не видалена: вона лежить в архіві. '
                f'Натисніть на картинку, щоб відкрити в повному розмірі, або «JPG ↓», щоб завантажити.</p>')
        a_toc, a_body, a_n = body(lambda i: i not in keep_set)
        nav = ""    # the archive page is built, but not linked for now
        (site / "creatives.html").write_text(render(f'<h1 class="vh">Відібрані банери колекції SOLO</h1>', toc_html, body_html))
        a_lede = (f'<p class="lede"><b>Архів.</b> {a_n} {pl(a_n)} поза відбором. Нічого не видалено: файли можна відкрити й завантажити. '
                  f'Позначте «Залишити», щоб повернути банер до відібраних, і надішліть оновлений список.</p>')
        (site / "creatives-archive.html").write_text(render(f'<header><a href="creatives">← До відібраних</a></header>\n<h1>Архів</h1>\n{a_lede}', a_toc, a_body).replace("<title>Креативи Obiimy</title>", "<title>Архів креативів Obiimy</title>"))
    else:
        toc_html, body_html, n = body(lambda i: True)
        (site / "creatives.html").write_text(render(f'<header><a href="./">← Усі лендинги Obiimy</a>{arch_nav}</header>\n<h1>SOLO</h1>\n{lede_main}', toc_html, body_html))
        (site / "creatives-archive.html").unlink(missing_ok=True)
    return n_solo + n_old

if __name__ == "__main__":
    print(build(ROOT / "site"), "creatives")
