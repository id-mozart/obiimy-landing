#!/usr/bin/env python3
"""Build the deployable static site into ./site: every landing version wrapped in a full HTML document, assets copied, hub index generated."""
import pathlib, shutil, re, subprocess, os

ROOT = pathlib.Path(__file__).resolve().parent
SITE = ROOT / "site"

VERSIONS = [
    ("garden",   "garden.html",     "Garden",    "Мега-арт: одна 3D-сцена на весь скрол. Частинки збираються в логотип, шовк пропливає каруселлю, тунель зі станів, зграя і жовта коробка з тканиною (WebGL)."),
    ("maison",   "maison.html",     "Maison",    "Головна преміум-версія. Фото-hero, каталог за настроєм, підбір подарунка, довіра, FAQ. Доведена до 9/10 арт-директором і маркетологом."),
    ("journal",  "f-journal.html",  "Journal",   "Журнал бренду: обкладинка, три фотоісторії з кредитами, натюрморти, розмова із засновницею."),
    ("campaign", "f-campaign.html", "Campaign",  "Темна кампейн-версія: сім повноекранних образів із хотспотами «shop the look»."),
    ("lookbook", "f-lookbook.html", "Lookbook",  "Сім способів носити шовк: закріплене фото змінюється разом із текстом."),
    ("studio",   "v-studio.html",   "Studio",    "Світла студія: хустка на двох булавках під вітром, симуляція тканини, фактура шовку (WebGL)."),
    ("noir",     "v-noir.html",     "Noir",      "Нуар: невагомий шовк з анізотропним блиском і 3D-стрічка твіллі (WebGL)."),
    ("form",     "v-form.html",     "Form",      "Хустка падає на форму й драпірується, розмір змінює драпіровку (WebGL)."),
    ("art",      "art.html",        "Art",       "Артова версія: 3D-хустка з реальним принтом, дев’ять станів, зали-галереї."),
    ("classic",  "index.html",      "Classic",   "Перша, класична версія: колекції, хіти, розміри у масштабі, місія, подарунки."),
]
B2B = [
    ("b2b-newyear",   "maison",   "Новий рік · корпоративні подарунки", "Подарунки для команди та партнерів: чотири бюджети від 700 до 4 800 грн, листівка від компанії, графік до свят, доставка кожному співробітнику, форма запиту."),
    ("b2b-horeca",    "noir",     "HoReCa · уніформа",                  "Шовк у дрес-коді готелів, ресторанів, авіації, банків і салонів: шість сценаріїв, три речі для уніформи, догляд і дозамовлення, запит капсули принтів."),
    ("b2b-wholesale", "journal",  "Опт · для магазинів",                "Obiimy на полиці бутика чи корнера: шість категорій, що отримує партнер, три формати співпраці, запит оптового прайсу."),
    ("b2b-calendar",  "lookbook", "Календар · подарунки цілий рік",     "Річна програма корпоративних подарунків: вісім приводів від Нового року до welcome-box, бюджети, один список адрес — і відправки за графіком."),
]
EXTRA_PRODUCTS = {"maison": [("twilly", "твіллі"), ("set", "набір")], "journal": [("twilly", "твіллі")], "campaign": [("mask", "маска для сну")], "lookbook": [("set", "набір")], "studio": [("mask", "маска для сну")], "noir": [("scrunchie", "резинка")], "form": [("set", "набір")], "art": [("twilly", "твіллі")], "garden": [("mask", "маска для сну")], "classic": [("scrunchie", "резинка")]}
ASSET_DIRS = ["img", "photo", "tex", "brand"]

KEEP = {"", "/", "/pro-nas/", "/vidhuky/", "/oplata-i-dostavka/", "/obmin-ta-povernennya/", "/rekomendatsii-po-dohliadu/", "/en/", "/en"}
def relink(src: str, slug: str) -> str:
    def sub(m):
        path = m.group(1) or ""
        return m.group(0) if path in KEEP else f"product-{slug}"
    return re.sub(r'https://obiimy\.world(/[A-Za-z0-9\-]+/?)?(?=["\'\s<>?])', sub, src)

def wrap(src: str) -> str:
    i = src.index("</style>") + len("</style>")
    head, body = src[:i], src[i:]
    head = re.sub(r'<meta charset="utf-8">\s*', "", head, count=1)
    return f'<!DOCTYPE html>\n<html lang="uk">\n<head>\n<meta charset="utf-8">\n{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n'

def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    for d in ASSET_DIRS:
        shutil.copytree(ROOT / d, SITE / d)
    if (ROOT / "lookbook-obiimy-2026.pdf").exists():
        shutil.copy(ROOT / "lookbook-obiimy-2026.pdf", SITE / "lookbook-obiimy-2026.pdf")
    for slug, fname, title, desc in VERSIONS:
        (SITE / f"{slug}.html").write_text(wrap(relink((ROOT / fname).read_text(), slug)))
        pp = ROOT / f"p-{slug}.html"
        if pp.exists():
            (SITE / f"product-{slug}.html").write_text(wrap(pp.read_text()))
        for suffix, _ in EXTRA_PRODUCTS.get(slug, []):
            (SITE / f"product-{slug}-{suffix}.html").write_text(wrap((ROOT / f"p-{slug}-{suffix}.html").read_text()))
    for slug, skin, title, desc in B2B:
        (SITE / f"{slug}.html").write_text(wrap(relink((ROOT / f"{slug}.html").read_text(), skin)))
    # hub page
    cards = "\n".join(
        f'''      <div class="card">
        <a class="ph" href="{slug}"><img src="thumbs/{slug}.jpg" alt="{title}" loading="lazy"></a>
        <div class="body"><span class="no">{i+1:02d}</span><h2><a href="{slug}">{title}</a></h2><p>{desc}</p><div class="links"><a class="go" href="{slug}">Відкрити лендинг →</a><a class="go sub" href="product-{slug}">Товар: хустка →</a>{"".join(f'<a class="go sub" href="product-{slug}-{suf}">{lab} →</a>' for suf, lab in EXTRA_PRODUCTS.get(slug, []))}</div></div>
      </div>''' for i, (slug, fname, title, desc) in enumerate(VERSIONS))
    b2b_cards = "\n".join(
        f'''      <div class="card">
        <a class="ph" href="{slug}"><img src="thumbs/{slug}.jpg" alt="{title}" loading="lazy"></a>
        <div class="body"><span class="no">B2B · стиль {skin.capitalize()}</span><h2><a href="{slug}">{title}</a></h2><p>{desc}</p><div class="links"><a class="go" href="{slug}">Відкрити лендинг →</a></div></div>
      </div>''' for slug, skin, title, desc in B2B)
    hub = f'''<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Obiimy — версії лендингу та B2B</title>
<meta name="description" content="Десять версій преміум-лендингу для бренду шовкових хусток Obiimy.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Prata&family=Onest:wght@300;400;500;600&display=swap">
<style>
  :root {{ --bg:#F4F3EF; --card:#fff; --ink:#171519; --ink-2:#4A4750; --ink-3:#807C86; --line:rgba(23,21,25,.12); --gold:#F2B705; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font-family:'Onest','Helvetica Neue',Arial,sans-serif; line-height:1.6; -webkit-font-smoothing:antialiased; }}
  .wrap {{ width:min(1280px,100%); margin-inline:auto; padding:clamp(24px,5vw,64px) clamp(16px,4vw,48px); }}
  header {{ display:flex; justify-content:space-between; align-items:center; gap:20px; margin-bottom:clamp(28px,4vw,56px); }}
  header img {{ height:26px; width:auto; }}
  header a {{ color:var(--ink-2); text-decoration:none; font-size:.9rem; }}
  .grid.b2b .card:first-child {{ grid-column:auto; grid-template-columns:none; }}
  .grid.b2b .card:first-child .ph {{ aspect-ratio:16/10; border-right:0; border-bottom:1px solid var(--line); min-height:0; }}
  .grid.b2b .card:first-child .body {{ padding:18px 20px 22px; align-content:start; }}
  .grid.b2b .card:first-child h2 {{ font-size:1.5rem; }}
  h1 {{ font-family:'Prata',serif; font-weight:400; font-size:clamp(2rem,4.5vw,3.6rem); margin:0 0 10px; line-height:1.05; }}
  .lede {{ color:var(--ink-2); max-width:38em; font-weight:300; font-size:1.05rem; margin:0 0 clamp(28px,4vw,56px); }}
  .grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:20px; }}
  .card {{ display:grid; grid-template-rows:auto 1fr; background:var(--card); border-radius:6px; overflow:hidden; color:inherit; border:1px solid var(--line); transition:transform .3s ease, box-shadow .3s ease; }}
  .card:hover {{ transform:translateY(-4px); box-shadow:0 30px 60px -30px rgba(23,21,25,.35); }}
  .card .ph {{ display:block; aspect-ratio:16/10; overflow:hidden; background:#ECEAE4; border-bottom:1px solid var(--line); }}
  .card h2 a {{ text-decoration:none; color:inherit; }}
  .card .links {{ display:flex; flex-wrap:wrap; gap:6px 18px; margin-top:6px; }}
  .card img {{ width:100%; height:100%; object-fit:cover; object-position:top; }}
  .card .body {{ padding:18px 20px 22px; display:grid; gap:6px; align-content:start; }}
  .card .no {{ font-size:.7rem; letter-spacing:.2em; color:var(--ink-3); font-weight:600; }}
  .card h2 {{ font-family:'Prata',serif; font-weight:400; font-size:1.5rem; margin:0; }}
  .card p {{ margin:0; color:var(--ink-2); font-size:.92rem; }}
  .card .go {{ font-size:.82rem; font-weight:500; text-decoration:underline; text-underline-offset:4px; color:var(--ink); }}
  .card .go.sub {{ color:var(--ink-2); }}
  .card:first-child {{ grid-column:span 3; grid-template-columns:1.2fr 1fr; }}
  .card:first-child .ph {{ aspect-ratio:auto; border-bottom:0; border-right:1px solid var(--line); min-height:320px; }}
  .card:first-child .body {{ padding:32px; align-content:center; }}
  .card:first-child h2 {{ font-size:2.2rem; }}
  footer {{ margin-top:clamp(32px,5vw,64px); padding-top:20px; border-top:1px solid var(--line); font-size:.82rem; color:var(--ink-3); display:flex; flex-wrap:wrap; gap:8px 24px; justify-content:space-between; }}
  @media (max-width:900px) {{ .grid {{ grid-template-columns:1fr 1fr; }} .card:first-child {{ grid-column:span 2; grid-template-columns:1fr; }} .card:first-child .ph {{ border-right:0; border-bottom:1px solid var(--line); min-height:0; aspect-ratio:16/10; }} }}
  @media (max-width:560px) {{ .grid {{ grid-template-columns:1fr; }} .card:first-child {{ grid-column:span 1; }} }}
</style>
</head>
<body>
<div class="wrap">
  <header><img src="brand/logo-ink.png" alt="Obiimy"><a href="https://obiimy.world/" target="_blank" rel="noopener">obiimy.world ↗</a></header>
  <h1>Десять версій лендингу Obiimy</h1>
  <p class="lede">Український бренд шовкових хусток з авторськими принтами художниці Світлани Сніжко. Від класичного лендингу до 3D-сцен та фешн-лукбуків. Головна версія — Maison, найартовіша — Garden. У кожної версії є приклад сторінки товару в тому ж стилі.</p>
  <div class="grid">
{cards}
  </div>
  <h1 style="margin-top:72px">Корпоративні та B2B-лендинги</h1>
  <p class="lede">Чотири сценарії для бізнес-клієнтів у стилях основних версій: новорічні подарунки для команд, шовк для уніформи HoReCa, оптова співпраця з магазинами та річна програма подарунків. Ціни роздрібні з obiimy.world; корпоративні умови, мінімальні тиражі й терміни — пропозиція, яку має підтвердити бренд.</p>
  <div class="grid b2b">
{b2b_cards}
  </div>
  <footer><span>Фото та логотип — obiimy.world.</span><span>Зроблено за допомогою Claude Code.</span></footer>
</div>
</body>
</html>
'''
    (SITE / "index.html").write_text(hub)
    # thumbnails via headless chrome (first screen, 1440x900)
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    thumbs = SITE / "thumbs"; thumbs.mkdir()
    if os.path.exists(chrome):
        from PIL import Image
        for slug, *_ in VERSIONS + B2B:
            png = thumbs / f"{slug}.png"
            subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                            "--window-size=1440,900", "--virtual-time-budget=9000", f"--screenshot={png}", f"file://{SITE / (slug + '.html')}"],
                           capture_output=True)
            if png.exists():
                im = Image.open(png).convert("RGB"); im.thumbnail((960, 600)); im.save(thumbs / f"{slug}.jpg", quality=82); png.unlink()
    print("site built:", sorted(p.name for p in SITE.iterdir()))

if __name__ == "__main__":
    main()
