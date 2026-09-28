"""Creatives gallery page for the Railway hub: site/creatives.html + site/creatives/<series>/<file>.
Called from build-site.py; images: full JPG for download, 540px WebP preview for the grid."""
import html, pathlib, shutil
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent

SOLO_GROUPS = [
    ("cover-0", "Ретро-обкладинки", "Колекція натхненна обкладинками модних журналів 40–50-х. Журнал SOLO: по одному випуску на кожен принт."),
    ("cover-story", "Обкладинка для сторіс", "Той самий журнальний прийом у вертикальному форматі."),
    ("states-", "Карусель «Сім станів»", "Сім принтів — сім станів на шляху жінки до себе. Опис кожного стану — з релізу."),
    ("manifest-", "Маніфести", "Типографіка на цитатах з релізу: «Я є. Я продовжую жити. Я обираю себе», маленькі акти свободи, краса як спосіб зберегти себе."),
    ("decades-", "Крізь десятиліття", "1940-ті, 1950-ті, 2026: як хустка змінювалася разом із жінкою."),
    ("film-", "Кадр із фільму", "Кіно 50-х: леттербокс, зерно, субтитри. «У головній ролі — ви»."),
    ("ticket-", "Квиток до себе", "Посадковий талон: рейс SOLO, звідки — сумніви, куди — до себе."),
    ("gazette-", "Жіночий вісник", "Передовиця ретрогазети: «Жінка обирає себе. Знову»."),
    ("letter-", "Лист собі", "Рукописна записка: право на красу навіть зараз."),
    ("poll-", "Опитування", "«Який у тебе сьогодні стан?» — сім принтів як варіанти відповіді для сторіс зі стікером-опитуванням."),
    ("palette-", "Палітра", "Сім принтів поруч: знайомство з колекцією одним кадром."),
    ("price-", "Каталог і ціни", "Сторінка каталогу з форматами й роздрібними цінами з obiimy.world."),
    ("ways-", "Як носити", "Шия, волосся, сумка, зап’ястя — чотири способи з релізу."),
    ("double-", "Двосторонній друк", "Технологія колекції: принт з обох боків."),
    ("minimal-", "Мінімалізм і slow fashion", "Чистий знак колекції та меседж «речі зі змістом»."),
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
    def add(title, desc, files, series):
        d = out / series; d.mkdir(exist_ok=True)
        cards = []
        for f in files:
            shutil.copy(f, d / f.name)
            im = Image.open(f).convert("RGB"); label, cls = fmt(im)
            prev = d / (f.stem + "-540.webp")
            t = im.copy(); t.thumbnail((540, 960)); t.save(prev, quality=80)
            cards.append(f'''<figure class="c {cls}" data-f="{cls}"><a href="creatives/{series}/{f.name}" target="_blank" rel="noopener"><img src="creatives/{series}/{prev.name}" alt="{html.escape(title)}" loading="lazy" width="{t.width}" height="{t.height}"></a>
        <figcaption><span>{label}</span><a href="creatives/{series}/{f.name}" download>JPG ↓</a></figcaption></figure>''')
        sections.append(f'''<section class="grp"><div class="gh"><h3>{title}</h3><p>{desc}</p></div><div class="grid">{"".join(cards)}</div></section>''')
    solo = sorted((ROOT / "ads/solo/out").glob("*.jpg"))
    n_solo = 0
    for prefix, title, desc in SOLO_GROUPS:
        fs = [f for f in solo if f.name.startswith(prefix)]
        if fs: add(title, desc, fs, "solo"); n_solo += len(fs)
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
.grp {{ margin-top: 40px; }}
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
<p class="lede"><b>Шлях до себе.</b> {n_solo} креативів для запуску нової колекції Obiimy: сім авторських принтів — сім станів на шляху жінки до себе. Тексти — за прес-релізом колекції, фото й ціни — з obiimy.world. Натисніть на картинку, щоб відкрити в повному розмірі (1080 px), або «JPG ↓», щоб завантажити.</p>
<div class="bar" role="group" aria-label="Формат"><button type="button" data-f="all" aria-pressed="true">Усі</button><button type="button" data-f="st" aria-pressed="false">Сторіс 9:16</button><button type="button" data-f="fd" aria-pressed="false">Стрічка 4:5</button><button type="button" data-f="sq" aria-pressed="false">Квадрат 1:1</button></div>
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
