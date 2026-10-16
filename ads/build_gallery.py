"""Creatives gallery page for the Railway hub: site/creatives.html + site/creatives/<series>/<file>.
Called from build-site.py; images: full JPG for download, 540px WebP preview for the grid."""
import hashlib, html, json, pathlib, shutil
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
                im = Image.open(f).convert("RGB"); label, cls = fmt(im)
                im.save(dst, "JPEG", quality=85, optimize=True, progressive=True)   # the deploy upload must stay well under 200 MB
                t = im.copy(); t.thumbnail((540, 960)); t.save(prev, quality=80)
            v = hashlib.md5(f.read_bytes()).hexdigest()[:8]
            # the other formats of the same banner, rendered next to the plain one: <out>-story/<file> (story UI zones kept free) and <out>-feed/<file> (1080 × 1350)
            alts = {}
            for key, suf in (("story", "-story"), ("feed", "-45"), ("square", "-1x1")):
                src = f.parent.with_name(f.parent.name + "-" + key) / f.name
                if not src.exists(): continue
                vd = d / (f.stem + suf + ".jpg"); vp = d / (f.stem + suf + "-540.webp")
                if not (vd.exists() and vp.exists() and vd.stat().st_mtime >= src.stat().st_mtime and vp.stat().st_mtime >= src.stat().st_mtime):
                    im2 = Image.open(src).convert("RGB"); im2.save(vd, "JPEG", quality=85, optimize=True, progressive=True); t2 = im2.copy(); t2.thumbnail((540, 960)); t2.save(vp, quality=80)
                with Image.open(vp) as t2: tw, th = t2.size
                vv = hashlib.md5(src.read_bytes()).hexdigest()[:8]
                alts[key] = dict(f=f"creatives/{series}/{vd.name}?v={vv}", p=f"creatives/{series}/{vp.name}?v={vv}", n=vd.name, w=tw, h=th)
            plain = dict(f=f"creatives/{series}/{f.name}?v={v}", p=f"creatives/{series}/{prev.name}?v={v}", n=f.name, w=t.width, h=t.height)
            data_alt = f' data-alt="{html.escape(json.dumps(alts, ensure_ascii=False), quote=True)}"' if alts else ""
            cards.append((f"{series}/{f.name}", f'''<figure class="c {cls}" data-f="{cls}" data-id="{series}/{f.name}" data-plain="{html.escape(json.dumps(plain, ensure_ascii=False), quote=True)}"{data_alt}><a href="creatives/{series}/{f.name}?v={v}" target="_blank" rel="noopener"><img src="creatives/{series}/{prev.name}?v={v}" alt="{html.escape(title)}" loading="lazy" width="{t.width}" height="{t.height}"></a>
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
        order = {k: n for n, k in enumerate(keep)}
        ids = [i for g in groups for i, _ in g["cards"] if select(i)]
        ids = list(dict.fromkeys(ids)); by = dict(zip(ids, cards))
        cards = [by[i] for i in sorted(ids, key=lambda i: order.get(i, 10 ** 6))]
        return f'<section class="grp flat"><div class="grid">{"".join(cards)}</div></section>', len(cards)
    all_ids = {i for g in groups for i, _ in g["cards"]}
    n_keep = len(keep_set & all_ids)
    defaults = json.dumps(sorted(keep_set & all_ids), ensure_ascii=False)
    keep_ver = hashlib.md5("\n".join(sorted(keep_set)).encode()).hexdigest()[:8]

    def render(top, toc_html, body_html):
        return f'''<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Креативи Obiimy</title>
<meta name="description" content="Рекламні креативи Obiimy: колекція SOLO. Шлях до себе та попередні серії сторіс.">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,900&family=Onest:wght@400;500;600&display=swap">
<style>
:root {{ --bg: #F3EADB; --card: #FBF6EC; --ink: #1B1613; --ink2: #5A5048; --line: rgba(27,22,19,.14); --acc: #7B1F24; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg: #2B2B2F; --card: #36363B; --ink: #F3EADB; --ink2: #B9AEA3; --line: rgba(243,234,219,.14); --acc: #E3A15A; }} }}
:root[data-theme="dark"] {{ --bg: #2B2B2F; --card: #36363B; --ink: #F3EADB; --ink2: #B9AEA3; --line: rgba(243,234,219,.14); --acc: #E3A15A; }}
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
@media (hover: none) {{ .grp.flat .c figcaption {{ display: none; }} }}     /* touch: «Залишити» and JPG live in the popup */
@media (max-width: 700px) {{ .picks {{ position: static; gap: 6px; padding: 10px 16px; }} .picks b {{ width: 100%; }} .picks button {{ padding: 9px 13px; font-size: .82rem; }} }}
body.shared .picks, body.shared .pick, body.shared .fid {{ display: none; }}
body.shared .c figcaption {{ justify-content: flex-end; }}
body.shared #lb .row {{ gap: 22px; }}
.fmt {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 14px 0 0; }}
.fmt b {{ font-size: .95rem; margin-right: 8px; white-space: nowrap; }}
.fmt button {{ font: inherit; font-size: .88rem; border: 1px solid var(--line); background: transparent; color: var(--ink); border-radius: 999px; padding: 10px 16px; cursor: pointer; }}
.fmt button[aria-pressed="true"] {{ background: var(--ink); color: var(--bg); border-color: var(--ink); }}
.fmt .fn {{ font-size: .85rem; color: var(--ink2); }} .fmt .zip {{ margin-left: auto; background: var(--acc); color: #fff; border-color: var(--acc); }} .fmt .zip[disabled] {{ opacity: .6; cursor: progress; }}
.c.nov img {{ opacity: .3; }} .c.nov::before {{ content: "немає в цьому форматі"; position: absolute; left: 10px; top: 10px; z-index: 1; font-size: .72rem; padding: 4px 8px; border-radius: 999px; background: var(--card); color: var(--ink2); border: 1px solid var(--line); }}
.c {{ position: relative; }}
.all {{ display: none; margin: 40px 0 0; text-align: center; }}
body.shared .all {{ display: block; }}
.all a {{ color: var(--ink2); font-size: .9rem; text-decoration: none; border: 1px solid var(--line); border-radius: 999px; padding: 12px 20px; display: inline-block; }}
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
<div class="fmt" role="group" aria-label="Формат банерів"><b>Формат:</b><button type="button" data-fmt="plain" aria-pressed="true">Банер 9:16</button><button type="button" data-fmt="story" aria-pressed="false">Сторіс · безпечна зона</button><button type="button" data-fmt="feed" aria-pressed="false">Стрічка 4:5</button><button type="button" data-fmt="square" aria-pressed="false">Квадрат 1:1</button><span class="fn" id="fmtn"></span><button type="button" id="zipall" class="zip" title="Усі формати всіх показаних банерів одним архівом">Завантажити все (ZIP)</button></div>
{f'<nav class="toc">{toc_html}</nav>' if toc_html else ""}
{body_html}
<p class="all"><a href="creatives">Показати всі банери</a></p>
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
  var KEY = 'obiimy-picks-{keep_ver}', picks = new Set(), only = false;     // a new selection starts from the saved list
  var DEF = {defaults}, stored = null;
  try {{ stored = localStorage.getItem(KEY); }} catch (e) {{}}
  var m = location.hash.match(/sel=([^&]+)/), shared = !!m, mf = location.hash.match(/fmt=(plain|story|feed|square)/);
  if (shared) {{
    // a link with a selection: show exactly these banners and nothing else; the saved working selection is not touched
    decodeURIComponent(m[1]).split(',').forEach(function (x) {{ if (x) picks.add(x); }});
    only = true; document.body.classList.add('shared');
  }} else {{
    try {{ (stored ? JSON.parse(stored) : DEF).forEach(function (x) {{ picks.add(x); }}); }} catch (e) {{}}
  }}
  window.addEventListener('hashchange', function () {{ location.reload(); }});
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
    if (!shared) try {{ localStorage.setItem(KEY, JSON.stringify(Array.from(picks))); }} catch (e) {{}}
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
  document.getElementById('link').addEventListener('click', function () {{ copy(location.origin + location.pathname + '#sel=' + encodeURIComponent(list().join(',')) + (FMT !== 'plain' ? '&fmt=' + FMT : ''), this); }});
  // the format of every card: the plain banner, the story with free UI zones or the 4:5 feed version
  var FMT = 'plain';
  function applyFmt(f) {{
    FMT = f; var have = 0, all = 0;
    document.querySelectorAll('.fmt button').forEach(function (b) {{ b.setAttribute('aria-pressed', b.dataset.fmt === f ? 'true' : 'false'); }});
    document.querySelectorAll('.c').forEach(function (c) {{
      var plain = JSON.parse(c.dataset.plain), alt = c.dataset.alt ? JSON.parse(c.dataset.alt) : {{}}, v = f === 'plain' ? plain : alt[f];
      all++; if (v) have++; c.classList.toggle('nov', !v); if (!v) v = plain;
      var a = c.querySelector('a'), img = a.querySelector('img'), dl = c.querySelector('figcaption a[download]');
      if (a.getAttribute('href') !== v.f) {{ a.href = v.f; img.src = v.p; img.width = v.w; img.height = v.h; }}
      if (dl) {{ dl.href = v.f; dl.setAttribute('download', v.n); }}
    }});
    document.getElementById('fmtn').textContent = f === 'plain' ? '' : 'є для ' + have + ' з ' + all;
    try {{ localStorage.setItem('obiimy-fmt', f); }} catch (e) {{}}
  }}
  document.querySelectorAll('.fmt button').forEach(function (b) {{ b.addEventListener('click', function () {{ applyFmt(b.dataset.fmt); }}); }});
  var f0 = mf ? mf[1] : null; if (!f0) try {{ f0 = localStorage.getItem('obiimy-fmt'); }} catch (e) {{}}
  if (f0 && f0 !== 'plain') applyFmt(f0);
  // «Завантажити все»: every format of every banner on view, one ZIP, built in the browser
  var FOLDER = {{ plain: '9x16', story: 'story-9x16', feed: '4x5', square: '1x1' }};
  function zipAll() {{
    var btn = document.getElementById('zipall'), note = document.getElementById('fmtn'), items = [];
    document.querySelectorAll('.c:not(.hide)').forEach(function (c) {{
      var plain = JSON.parse(c.dataset.plain), alt = c.dataset.alt ? JSON.parse(c.dataset.alt) : {{}};
      items.push([FOLDER.plain, plain]); Object.keys(alt).forEach(function (k) {{ items.push([FOLDER[k] || k, alt[k]]); }});
    }});
    if (!items.length) return Promise.resolve(0);
    btn.disabled = true; var was = note.textContent;
    function withLib() {{ return window.JSZip ? Promise.resolve() : new Promise(function (ok, no) {{ var sc = document.createElement('script'); sc.src = 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js'; sc.onload = ok; sc.onerror = no; document.head.appendChild(sc); }}); }}
    return withLib().then(function () {{
      var zip = new JSZip(), done = 0;
      return Promise.all(items.map(function (it) {{ return fetch(it[1].f).then(function (r) {{ if (!r.ok) throw new Error(it[1].n); return r.blob(); }}).then(function (b) {{ zip.folder(it[0]).file(it[1].n, b); done++; note.textContent = 'Пакую: ' + done + ' з ' + items.length; }}); }}))
        .then(function () {{ return zip.generateAsync({{ type: 'blob' }}); }})
        .then(function (blob) {{ var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'obiimy-creatives-' + items.length + '.zip'; a.click(); setTimeout(function () {{ URL.revokeObjectURL(a.href); }}, 60000); note.textContent = was; btn.disabled = false; return blob.size; }});
    }}).catch(function (e) {{ note.textContent = 'Не вдалося зібрати архів: ' + (e && e.message || e); btn.disabled = false; throw e; }});
  }}
  window.zipAll = zipAll;
  document.getElementById('zipall').addEventListener('click', function () {{ zipAll(); }});
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
    var dl0 = c.querySelector('figcaption a[download]'); lbd.href = a.href; lbd.setAttribute('download', dl0 ? dl0.getAttribute('download') : c.dataset.id.split('/').pop());
    lbc.checked = picks.has(c.dataset.id);
    lbn.textContent = (shared ? '' : c.querySelector('.fid').textContent + ' · ') + (cur + 1) + ' / ' + items.length;
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
  var tx = null, ty = 0;
  lb.addEventListener('touchstart', function (e) {{ tx = e.touches[0].clientX; ty = e.touches[0].clientY; }}, {{ passive: true }});
  lb.addEventListener('touchend', function (e) {{
    if (tx === null) return;
    var dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty; tx = null;
    if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.5) show(cur + (dx < 0 ? 1 : -1));
  }});
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
        (site / "creatives.html").write_text(render(f'<header><a href="./">← Усі лендинги Obiimy</a><a href="home-banners">Банери для головної obiimy.world →</a></header><h1 class="vh">Відібрані банери колекції SOLO</h1>', toc_html, body_html))
        a_lede = (f'<p class="lede"><b>Архів.</b> {a_n} {pl(a_n)} поза відбором. Нічого не видалено: файли можна відкрити й завантажити. '
                  f'Позначте «Залишити», щоб повернути банер до відібраних, і надішліть оновлений список.</p>')
        (site / "creatives-archive.html").write_text(render(f'<header><a href="creatives">← До відібраних</a></header>\n<h1>Архів</h1>\n{a_lede}', a_toc, a_body).replace("<title>Креативи Obiimy</title>", "<title>Архів креативів Obiimy</title>"))
    else:
        toc_html, body_html, n = body(lambda i: True)
        (site / "creatives.html").write_text(render(f'<header><a href="./">← Усі лендинги Obiimy</a>{arch_nav}</header>\n<h1>SOLO</h1>\n{lede_main}', toc_html, body_html))
        (site / "creatives-archive.html").unlink(missing_ok=True)
    build_home(site, render)
    return n_solo + n_old

HOME = [
        ("home-h-reblum-dark", "Студійний кадр · темний", "Той самий кадр панеллю праворуч на темному полі.", "ok"),
        ("home-z1-mono", "Монохром + жовтий", "«Тиша всередині» в кабріолеті чорно-білим; жовта плашка — єдина кольорова пляма банера.", "ok"),
        ("home-w-door", "Біля дверей", "«Золоте світло» на темному кадрі на весь банер, хустка біля шиї освітлена; лок-ап на вуалі.", "ok"),
        ("home-y-knot", "Класичний вузол", "«Сміливий крок» у центрі між двома темними полями; ліворуч лок-ап, праворуч картка принта зі станом.", "ok"),
        ("home-r-reblum-paper", "Студійний кадр · папір", "Світле поле, кадр з м’яким краєм праворуч, підпис із назвою хустки.", "ok"),
        ("home-z4-album", "Відбиток в альбомі", "Папір, фото «Іскри» в білій рамці з тінню і підписом — редакційна подача.", "ok"),
        ("home-f-yellow", "Фірмовий жовтий", "Жовте поле бренду, темний лок-ап; праворуч — бант «Авантюра» у волоссі.", "ok"),
        ("home-u-diptych", "Диптих", "Портрет і вузол однієї зйомки «Тиші всередині», між ними темна смуга з лок-апом.", "ok"),
        ("home-x-cafe", "Кафе", "«Пульс» у теплому вуличному кадрі праворуч, папір і темний лок-ап ліворуч.", "ok"),
        ("home-z2-arch", "Арка", "Темне поле, кадр «Сміливого кроку» в масці-арці — перегук із круглими категоріями під слайдером.", "ok"),
        ("home-z3-diag", "Діагональний стик", "«Пульс» праворуч, темна панель із косим краєм — динаміка без вітру.", "ok"),
        ("home-g-reblum-light", "Студійний кадр · світлий", "Новий крупний план «Авантюри» на шиї; штора кадру продовжена ліворуч м’яким розмиттям, лок-ап темний.", "res"),
        ("home-j-split", "Навпіл", "Кадр «Тиша всередині» ліворуч, лок-ап по центру темного поля праворуч.", "res"),
        ("home-b-three", "Три принти", "Лок-ап на темному, праворуч три кадри трьох принтів: «Сміливий крок», «Пульс», «Золоте світло».", "res"),
        ("home-o-reblum-wide", "Студійний кадр · широкий", "Вузол по центру, ліва частина добудована з того ж кадру дзеркалом і розмиттям, лок-ап на вуалі.", "res"),
        ("home-p-reblum-yellow", "Студійний кадр · жовтий", "Жовте поле бренду зліва, вузол крупно справа, темна плашка.", "res"),
        ("home-q-reblum-slice", "Студійний кадр · сім станів", "Кадр вертикальною смугою між двома темними полями; праворуч — сім станів, «Авантюра» виділена.", "res"),
        ("home-c-seven", "Сім принтів", "Сім хусток колекції в ряд з назвами — сім станів на шляху до себе.", "res"),
        ("home-m-paper", "Папір і хустки", "Світле поле, дві хустки колекції як предмет — товар на перший план.", "res")]
TIERS = [('ok', 'Рекомендовані · прийняті арт-директором'), ('new', 'Новий раунд · на оцінку'), ('res', 'Запасні · для другого-третього слайда')]

def build_home(site, render):
    """site/home-banners.html — the SOLO banners for the home page of obiimy.world (1920 × 576), from ads/solo/out-home:
    grouped by tier (accepted / new round / reserve), every card with a phone crop (the slider on a 390 px screen shows the
    central 1 : 1 part), JPG per banner and a ZIP of all."""
    src = ROOT / "ads/solo/out-home"
    if not src.exists(): return
    out = site / "creatives" / "home"; out.mkdir(parents=True, exist_ok=True)
    cards = {k: [] for k, _ in TIERS}; files = []
    for id, title, desc, tier in HOME:
        f = src / f"{id}.jpg"
        if not f.exists(): continue
        dst = out / f.name; prev = out / f"{id}-1200.webp"; ph = out / f"{id}-phone.webp"
        if not (dst.exists() and prev.exists() and ph.exists() and dst.stat().st_mtime >= f.stat().st_mtime):
            im = Image.open(f).convert("RGB"); im.save(dst, "JPEG", quality=88, optimize=True, progressive=True)
            t = im.copy(); t.thumbnail((1200, 400)); t.save(prev, quality=82)
            # the phone: the slider keeps the banner's height and crops the sides — a 1.3 : 1 window from the centre-left (the lock-up side)
            w, h = im.size; cw = int(h * 1.3); x0 = max(0, min(w - cw, int(w * .02)))
            im.crop((x0, 0, x0 + cw, h)).resize((520, 400)).save(ph, quality=82)
        v = hashlib.md5(f.read_bytes()).hexdigest()[:8]; files.append(f"creatives/home/{f.name}?v={v}")
        cards[tier].append(f'''<figure class="hb"><div class="hbv"><a href="creatives/home/{f.name}?v={v}" target="_blank" rel="noopener"><img src="creatives/home/{prev.name}?v={v}" alt="{html.escape(title)}" loading="lazy" width="1200" height="360"></a><div class="hbp" title="Як обріже слайдер на телефоні (ліва частина з лок-апом)"><img src="creatives/home/{ph.name}?v={v}" alt="" loading="lazy" width="520" height="400"><span>телефон</span></div></div>
      <figcaption><div><b>{html.escape(title)}</b><p>{html.escape(desc)}</p></div><div class="hba"><a href="home-preview?b={id}">На макеті →</a><a href="creatives/home/{f.name}?v={v}" download="{f.name}">JPG 1920 × 576 ↓</a></div></figcaption></figure>''')
    secs = "".join(f'<section class="hbt {k}"><h2>{t} <span>· {len(cards[k])}</span></h2><div class="hbs">{"".join(cards[k])}</div></section>' for k, t in TIERS if cards[k])
    body = f'''<header><a href="./">← Усі лендинги Obiimy</a><a href="creatives">Рекламні креативи →</a></header>
<h1>Банери для головної</h1>
<p class="lede"><b>Колекція SOLO на головній obiimy.world.</b> Формат поточного банера сайту — 1920 × 576: лок-ап «КОЛЕКЦІЯ / СОЛО / ШЛЯХ ДО СЕБЕ», жовта плашка «Жіноча сила крізь десятиліття», вертикальний OBIIMY™. Фото — зйомки колекції й студійний кадр клієнта, тексти — за прес-релізом. Поруч із кожним — як його обріже слайдер на телефоні.</p>
<p class="lede hbl"><a href="home-preview">Подивитися на макеті головної (слайдер) →</a><button type="button" id="hbzip">Завантажити всі (ZIP)</button><span id="hbn"></span></p>
{secs}
<style>.hbl {{ display:flex; flex-wrap:wrap; gap:14px; align-items:center; margin-top:14px; }} .hbl a {{ color:var(--acc); font-weight:600; }} .hbl button {{ font:inherit; font-size:.88rem; border:0; background:var(--acc); color:#fff; border-radius:999px; padding:10px 16px; cursor:pointer; }} .hbl button[disabled] {{ opacity:.6; }} #hbn {{ font-size:.85rem; color:var(--ink2); }}
.hbt {{ margin-top: 48px; }} .hbt h2 {{ margin: 0 0 18px; font-size: 1.5rem; }} .hbt h2 span {{ color: var(--ink2); font-weight: 400; }} .hbt.ok h2::before {{ content: "✓ "; color: #2b7a3d; }}
.hbs {{ display: grid; gap: 28px; }} .hb {{ margin: 0; background: var(--card); border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }} .hbt.ok .hb {{ border-color: #2b7a3d; }}
.hbv {{ display: grid; grid-template-columns: 1fr 160px; gap: 10px; align-items: start; background: var(--bg); padding: 10px; }} .hbv > a img {{ display: block; width: 100%; height: auto; }}
.hbp {{ position: relative; }} .hbp img {{ display: block; width: 100%; height: auto; border-radius: 14px; border: 3px solid var(--ink); }} .hbp span {{ position: absolute; left: 0; right: 0; bottom: -18px; text-align: center; font-size: .72rem; color: var(--ink2); }}
.hb figcaption {{ display: flex; justify-content: space-between; align-items: center; gap: 24px; padding: 22px 18px 14px; font-size: .92rem; color: var(--ink2); }} .hb b {{ color: var(--ink); font-size: 1.05rem; }} .hb p {{ margin: 4px 0 0; max-width: 60em; line-height: 1.45; }} .hba {{ display: flex; gap: 16px; }} .hba a {{ color: var(--acc); font-weight: 600; text-decoration: none; white-space: nowrap; }}
@media (max-width: 700px) {{ .hbv {{ grid-template-columns: 1fr; }} .hbp {{ max-width: 200px; }} .hb figcaption {{ flex-direction: column; align-items: flex-start; }} }}
.picks, .fmt, .toc, .all, #lb {{ display: none !important; }}</style>
<script>
document.getElementById('hbzip').addEventListener('click', function () {{
  var btn = this, n = document.getElementById('hbn'), items = {json.dumps(files)}; btn.disabled = true;
  (window.JSZip ? Promise.resolve() : new Promise(function (ok, no) {{ var s = document.createElement('script'); s.src = 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js'; s.onload = ok; s.onerror = no; document.head.appendChild(s); }}))
  .then(function () {{ var zip = new JSZip(), done = 0; return Promise.all(items.map(function (u) {{ return fetch(u).then(function (r) {{ return r.blob(); }}).then(function (b) {{ zip.file(u.split('/').pop().split('?')[0], b); n.textContent = 'Пакую: ' + (++done) + ' з ' + items.length; }}); }})).then(function () {{ return zip.generateAsync({{ type: 'blob' }}); }}); }})
  .then(function (blob) {{ var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'obiimy-home-banners.zip'; a.click(); n.textContent = ''; btn.disabled = false; }})
  .catch(function (e) {{ n.textContent = 'Не вдалося: ' + e; btn.disabled = false; }});
}});
</script>'''
    page = render(body, "", "").replace("<title>Креативи Obiimy</title>", "<title>Банери для головної obiimy.world — SOLO</title>")
    (site / "home-banners.html").write_text(page)
    build_home_mock(site, out, [(id, title) for id, title, _, _ in HOME if (src / f"{id}.jpg").exists()])

def build_home_mock(site, out, items):
    """site/home-preview.html — the banners inside a mock of the obiimy.world home page: the site's header, the slider with
    arrows and dots, the category circles under it. Keys ←/→ and the dots switch the variant; «?b=<id>» opens one."""
    cuts = [("SALE", "yellow"), ("«Соло: шлях до себе»", "krok-44-1"), ("«Поклик душі»", "puls-44-1"), ("«Пробудження»", "zolote-44-1"), ("«Дика стихія»", "tysha-88-1"), ("«Співоча душа»", "flirt-65-1"), ("Подарункові набори", "box"), ("Хустки", "iskra-65-1"), ("Хустки 2D", "avantiura-88-1")]
    def circle(label, k):
        if k == "yellow": inner = '<span class="cc" style="background:#F2B705"></span>'
        elif k == "box": inner = '<span class="cc" style="background:#F2B705 url(photo/box-gold-480.webp) center/cover"></span>'
        else: inner = f'<span class="cc" style="background:#fff url(ads-src/{k}-cut.webp) center/82% no-repeat"></span>'
        return f'<div class="cat">{inner}<p>{html.escape(label)}</p></div>'
    (site / "ads-src").mkdir(exist_ok=True)
    for _, k in cuts:
        f = ROOT / "ads/solo/src" / f"{k}-cut.webp"
        if f.exists(): shutil.copy(f, site / "ads-src" / f.name)
    slides = "".join(f'<div class="sl" data-id="{id}"><img src="creatives/home/{id}.jpg" alt="{html.escape(t)}" loading="lazy"></div>' for id, t in items)
    dots = "".join(f'<button type="button" data-i="{i}" aria-label="{html.escape(t)}"></button>' for i, (id, t) in enumerate(items))
    opts = "".join(f'<option value="{i}">{html.escape(t)}</option>' for i, (id, t) in enumerate(items))
    page = f'''<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Банери SOLO на головній obiimy.world — превю</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap">
<style>
* {{ box-sizing: border-box; }} body {{ margin: 0; background: #fff; color: #222; font-family: Montserrat, Arial, sans-serif; font-size: 13px; }}
.top {{ background: #fff; text-align: center; padding: 7px 0; color: #5B4A9E; font-weight: 600; font-size: 12px; }}
.bar {{ background: #B9A3DC; color: #fff; font-size: 11px; }} .bar .in {{ max-width: 1240px; margin: 0 auto; padding: 7px 20px; display: flex; justify-content: center; gap: 14px; flex-wrap: wrap; }}
.hd {{ max-width: 1240px; margin: 0 auto; padding: 18px 20px; display: flex; align-items: center; gap: 36px; }} .hd img {{ height: 42px; }} .hd .srch {{ flex: 1; border: 1px solid #d9d9d9; border-radius: 999px; padding: 9px 16px; color: #999; }} .hd b {{ font-weight: 600; }}
.nav {{ border-top: 1px solid #eee; border-bottom: 1px solid #eee; }} .nav .in {{ max-width: 1240px; margin: 0 auto; padding: 12px 20px; display: flex; justify-content: space-between; gap: 10px; font-size: 14px; }}
.hero {{ max-width: 1536px; margin: 0 auto; position: relative; aspect-ratio: 1920 / 576; overflow: hidden; background: #141110; }}
.sl {{ position: absolute; inset: 0; opacity: 0; transition: opacity .35s; }} .sl.on {{ opacity: 1; }} .sl img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.ar {{ position: absolute; top: 50%; transform: translateY(-50%); width: 44px; height: 44px; border: 0; background: rgba(255,255,255,.18); color: #fff; font-size: 26px; cursor: pointer; border-radius: 50%; z-index: 2; }} .ar:hover {{ background: rgba(255,255,255,.32); }} .ar.l {{ left: 14px; }} .ar.r {{ right: 14px; }}
.dots {{ position: absolute; left: 0; right: 0; bottom: 12px; display: flex; justify-content: center; gap: 8px; z-index: 2; }} .dots button {{ width: 10px; height: 10px; border-radius: 50%; border: 0; background: rgba(255,255,255,.55); cursor: pointer; padding: 0; }} .dots button.on {{ background: #fff; }}
.cats {{ max-width: 1150px; margin: 30px auto 60px; border: 1px solid #eee; border-radius: 10px; padding: 22px 24px 26px; }} .cats h3 {{ margin: 0 0 18px; text-align: center; font-size: 16px; font-weight: 700; }}
.catrow {{ display: flex; justify-content: space-between; gap: 10px; }} .cat {{ text-align: center; width: 110px; }} .cc {{ display: block; width: 96px; height: 96px; margin: 0 auto 12px; border-radius: 50%; border: 3px solid #E8558F; background-color: #fff; }} .cat p {{ margin: 0; font-size: 12px; line-height: 1.3; }}
.ctl {{ max-width: 1240px; margin: 14px auto 0; padding: 0 20px; display: flex; gap: 12px; align-items: center; font-size: 13px; color: #555; }} .ctl select {{ font: inherit; padding: 6px 10px; }} .ctl a {{ color: #5B4A9E; }}
@media (max-width: 900px) {{ .nav, .bar, .hd .srch {{ display: none; }} .hd {{ justify-content: center; }} .catrow {{ overflow-x: auto; }} }}
</style></head><body>
<div class="top">Відправка день у день — при замовленні до 16:00.</div>
<div class="bar"><div class="in"><span>Каталог</span><span>Оплата і доставка</span><span>Обмін та повернення</span><span>Про нас</span><span>Рекомендації по догляду</span><span>Контактна інформація</span><span>Договір публічної оферти</span><span>Відгуки</span></div></div>
<div class="hd"><img src="brand/logo-original.png" alt="Obiimy"><div class="srch">пошук товарів</div><span>✳ Замовлення: <b>+38 067 010 85 25</b></span><b>🧺 Мій кошик</b></div>
<div class="nav"><div class="in"><span>SALE</span><span>ХІТ</span><span>Колекції</span><span>Подарункові набори</span><span>Хустки</span><span>Хустки 2D</span><span>Хустки паше</span><span>Твіллі</span><span>Резинки</span><span>Маски для сну</span><span>Прикраси</span><span>Obiimy HOME</span><span>Сертифікати</span></div></div>
<div class="hero" id="hero">{slides}<button type="button" class="ar l" id="prev" aria-label="Попередній">‹</button><button type="button" class="ar r" id="next" aria-label="Наступний">›</button><div class="dots" id="dots">{dots}</div></div>
<div class="ctl"><span>Варіант:</span><select id="pick">{opts}</select><a id="dl" href="#" download>JPG 1920 × 576 ↓</a><a href="home-banners">Усі банери списком →</a></div>
<div class="cats"><h3>Категорії</h3><div class="catrow">{"".join(circle(l, k) for l, k in cuts)}</div></div>
<script>
(function () {{
  var sl = [].slice.call(document.querySelectorAll('.sl')), dots = [].slice.call(document.querySelectorAll('#dots button')), pick = document.getElementById('pick'), dl = document.getElementById('dl'), cur = 0;
  var q = new URLSearchParams(location.search).get('b'); sl.forEach(function (s, i) {{ if (s.dataset.id === q) cur = i; }});
  function show(i) {{ cur = (i + sl.length) % sl.length; sl.forEach(function (s, k) {{ s.classList.toggle('on', k === cur); }}); dots.forEach(function (d, k) {{ d.classList.toggle('on', k === cur); }}); pick.value = cur; var im = sl[cur].querySelector('img'); dl.href = im.src; dl.setAttribute('download', sl[cur].dataset.id + '.jpg'); history.replaceState(null, '', '?b=' + sl[cur].dataset.id); }}
  dots.forEach(function (d) {{ d.addEventListener('click', function () {{ show(Number(d.dataset.i)); }}); }});
  pick.addEventListener('change', function () {{ show(Number(pick.value)); }});
  document.getElementById('prev').addEventListener('click', function () {{ show(cur - 1); }}); document.getElementById('next').addEventListener('click', function () {{ show(cur + 1); }});
  document.addEventListener('keydown', function (e) {{ if (e.key === 'ArrowLeft') show(cur - 1); if (e.key === 'ArrowRight') show(cur + 1); }});
  show(cur);
}})();
</script></body></html>'''
    (site / "home-preview.html").write_text(page)

if __name__ == "__main__":
    print(build(ROOT / "site"), "creatives")
