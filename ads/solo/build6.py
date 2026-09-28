"""SOLO triptych banners (1080×1920, plain banner — no story padding): three horizontal photo bands that tell
one story (decades, states, ways to wear, formats…), then a product line and a CTA at the bottom.
Copy from the press release; prices/facts from obiimy.world. YELLOW=1 → product line on the yellow brand plate.
Output: solo6.html / solo7.html → out6 / out7."""
import os, pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit import P, PP, S, CUT, HI, spot_photo, nb, LOGO_W, GRAIN

YELLOW = os.environ.get("YELLOW") == "1"

CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #555; font-family: 'Onest', Arial, sans-serif; -webkit-font-smoothing: antialiased; }
.ad { width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #141110; margin: 20px auto; color: #F3EADB; }
.ad > * { position: absolute; margin: 0; }
.ad p { margin: 0; }
.ad::after { content: ""; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: .3; mix-blend-mode: soft-light; background-image: GRAIN; }
.band { left: 0; right: 0; overflow: hidden; }
.band img { width: 100%; height: 100%; object-fit: cover; display: block; }
.band .veil { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(12,9,8,.82) 0%, rgba(12,9,8,.45) 46%, rgba(12,9,8,0) 72%); }
.band .txt { position: absolute; left: 64px; top: 50%; transform: translateY(-50%); width: 620px; }
.big { font-family: 'Playfair Display', serif; font-weight: 900; font-style: italic; line-height: .95; letter-spacing: -.01em; text-wrap: balance; }
.small { font-family: 'Cormorant Garamond', serif; font-weight: 500; font-size: 44px; line-height: 1.12; margin-top: 12px; text-wrap: pretty; }
.kicker { font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: .14em; font-size: 28px; color: #E0B040; white-space: nowrap; }
.tag { display: inline-block; margin-top: 16px; font-family: 'Onest'; font-weight: 600; font-size: 28px; letter-spacing: .04em; padding: 10px 20px; border-radius: 999px; background: rgba(243,234,219,.16); border: 1.5px solid rgba(243,234,219,.4); }
.cta { font-family: 'Onest'; font-weight: 600; font-size: 30px; padding: 24px 38px; border-radius: 999px; background: #F2B705; color: #141216; white-space: nowrap; }
""".replace("GRAIN", GRAIN)

ads = []
def ad(id, body, note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad" id="{id}">{body}\n</section>')

FILTERS = {"bw": "filter:grayscale(1) contrast(1.12)", "sepia": "filter:sepia(.4) saturate(1.1) contrast(1.05)", "raw": "", "": ""}

def band(top, height, b, n=3):
    photo, pos, big, small, look = b[:5]
    extra = b[5] if len(b) > 5 else {}
    size = extra.get("size", 118 if len(big) <= 8 else 84)
    if n == 4: size = min(size, 84)
    if n == 1 and look not in ("grid",): size = extra.get("size", 130)
    tag = f'<p class="tag">{extra["tag"]}</p>' if extra.get("tag") else ""
    if look == "spec":
        rows = photo
        def row(r):
            img = f'<img src="{CUT(r[2])}" alt="" style="height:120px;width:120px;object-fit:contain;flex:none;filter:drop-shadow(0 8px 10px rgba(40,25,10,.3))">' if len(r) > 2 else ""
            return (f'<div style="display:flex;align-items:center;gap:26px;flex:1;border-bottom:1.5px solid rgba(27,22,19,.18)">{img}'
                    f'<p style="font-family:Onest;font-size:26px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#6B5F55;width:{extra.get("lw", 250)}px;flex:none">{r[0]}</p>'
                    f'<p style="font-family:Onest;font-size:{extra.get("fs", 36)}px;line-height:1.2;font-weight:500;color:#1B1613;flex:1;text-align:right">{r[1]}</p></div>')
        title = f'<p class="big" style="font-size:{size}px;color:#1B1613;padding:14px 0 18px">{big}</p>' if big else ""
        return f'''
  <div class="band" style="top:{top}px;height:{height}px;background:{pos or "#F3EADB"}">
    <div style="position:absolute;left:64px;right:64px;top:16px;bottom:22px;display:flex;flex-direction:column">{title}{"".join(row(r) for r in rows)}</div></div>'''
    if look == "cut":
        cuts = photo if isinstance(photo, list) else [photo]
        imgs = "".join(f'<img src="{CUT(c)}" alt="" style="height:{int(height * extra.get("frac", 0.8 if len(cuts) == 1 else 0.72))}px;width:auto;max-width:{560 if len(cuts) == 1 else 300}px;object-fit:contain;margin-left:{0 if i == 0 else -40}px;filter:drop-shadow(0 26px 30px rgba(0,0,0,.45));transform:rotate({(-6, 7, -3)[i % 3]}deg)">' for i, c in enumerate(cuts))
        pic = (f'<div style="position:absolute;inset:0;background:radial-gradient(70% 90% at 72% 50%,rgba(255,255,255,.2),rgba(0,0,0,0) 70%),{pos}"></div>'
               f'<div style="position:absolute;right:40px;top:0;bottom:0;display:flex;align-items:center">{imgs}</div>')
        return f'''
  <div class="band" style="top:{top}px;height:{height}px">{pic}
    <div class="txt" style="width:470px"><p class="big" style="font-size:{size}px">{big}</p>{f'<p class="small">{nb(small)}</p>' if small else ""}{tag}</div></div>'''
    if look == "grid":
        cells = "".join(f'<div style="display:grid;justify-items:center;gap:8px;text-align:center"><img src="{CUT(c)}" alt="" style="height:{extra.get("h", 230)}px;width:auto;max-width:230px;object-fit:contain;filter:drop-shadow(0 16px 18px rgba(0,0,0,.45))"><p style="font-family:Cormorant Garamond,serif;font-style:italic;font-size:34px;line-height:1">{n}</p><p style="font-family:Onest;font-weight:600;font-size:26px;line-height:1.3;color:#E9D7A6">{pr.replace(" · ", "<br>")}</p></div>' for c, n, pr in photo)
        cols = extra.get("cols", 4)
        return f'''
  <div class="band" style="top:{top}px;height:{height}px;background:{pos}">
    <div style="position:absolute;left:64px;top:44px"><p class="big" style="font-size:{size}px">{big}</p>{f'<p class="small">{nb(small)}</p>' if small else ""}</div>
    <div style="position:absolute;left:40px;right:40px;top:{extra.get("gtop", 250)}px;bottom:40px;display:grid;grid-template-columns:repeat({cols},1fr);align-content:center;gap:40px 10px">{cells}</div></div>'''
    if look == "spot":
        pic = spot_photo(photo, pos, style="position:absolute;inset:0")
    elif photo.startswith("url("):
        pic = f'<div style="position:absolute;inset:0;background:{photo} {pos}"></div>'
    else:
        pic = f'<img src="{S(photo)}" alt="" style="object-position:{pos};{FILTERS[look]}">'
    return f'''
  <div class="band" style="top:{top}px;height:{height}px">{pic}<div class="veil"></div>
    <div class="txt"><p class="big" style="font-size:{size}px">{big}</p>{f'<p class="small" style="font-size:{38 if n == 4 else 44}px">{nb(small)}</p>' if small else ""}{tag}</div></div>'''

def triptych(id, kicker, bands, tagline, product, cta, note=""):
    """bands: 3 × (photo, object-position, big label, small line, look[, {tag, size}]); product: (cutouts, title, price)."""
    n = len(bands); top, gap = 280, 12
    h = (1242 - (n - 1) * gap) // n
    body = "".join(band(top + k * (h + gap), h, b, n) for k, b in enumerate(bands))
    cuts, title, price = product
    thumbs = "".join(f'<img src="{CUT(c)}" alt="" style="height:118px;width:auto;max-width:124px;object-fit:contain;margin-left:{0 if i == 0 else -44}px;filter:drop-shadow(0 8px 10px rgba(0,0,0,.4));transform:rotate({(-6, 5, -3)[i]}deg)">' for i, c in enumerate(cuts))
    plate_bg = "#F2B705" if YELLOW else "rgba(243,234,219,.1)"
    plate_fg = "#141216" if YELLOW else "#F3EADB"
    plate_bd = "none" if YELLOW else "1.5px solid rgba(243,234,219,.3)"
    y0 = top + n * h + (n - 1) * gap
    ad(id, f'''
  <div style="left:0;right:0;top:0;height:{top}px;background:#141110"></div>
  <div style="left:64px;top:44px;font-family:Montserrat,sans-serif;text-transform:uppercase;color:#fff;line-height:1">
    <p style="font-size:34px;font-weight:400;letter-spacing:.02em">Колекція</p>
    <p style="font-size:132px;font-weight:300;letter-spacing:-.01em;margin-top:6px">Соло</p>
    <p style="font-size:34px;font-weight:400;letter-spacing:.02em;margin-top:8px">Шлях до себе</p></div>
  <img src="{LOGO_W}" alt="" style="right:64px;top:50px;height:40px">
  <p style="right:64px;top:106px;font-family:Montserrat,sans-serif;font-size:26px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;white-space:nowrap;color:#F3EADB">Шовкові вироби</p>
  <p style="right:64px;top:176px;font-family:Montserrat,sans-serif;font-size:26px;font-weight:500;padding:16px 28px;border-radius:999px;background:#F2B705;color:#141216;white-space:nowrap">{kicker}</p>
  {body}
  <p style="left:64px;right:64px;top:{y0 + 34}px;font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:500;font-size:44px;line-height:1.15;text-wrap:balance">{nb(tagline)}</p>
  <div style="left:64px;right:64px;bottom:60px;display:flex;align-items:center;justify-content:space-between;gap:24px">
    <div style="display:flex;align-items:center;gap:22px;padding:12px 30px 12px 14px;border-radius:{6 if YELLOW else 20}px;background:{plate_bg};border:{plate_bd};color:{plate_fg}">
      <div style="display:flex;align-items:center">{thumbs}</div>
      <div><p style="font-size:30px;font-weight:600;line-height:1.2;white-space:nowrap">{title}</p><p style="font-family:'Playfair Display',serif;font-size:46px;line-height:1.05;margin-top:4px;white-space:nowrap">{price}</p></div>
    </div>
    <div class="cta" style="{"background:#F3EADB;color:#141216" if YELLOW else ""}">{cta}</div>
  </div>''', note)

# 1 — decades (the layout the client liked), now with product and CTA
triptych("t01-decades", "Жіноча сила крізь десятиліття", [
    ("zolote-44-3", "50% 22%", "1940-ві", "Сила — у бездоганній елегантності.", "bw"),
    ("iskra-65-4", "55% 28%", "1950-ті", "Правила починають руйнуватися. Колір, форма, сміливість.", "sepia"),
    ("puls-44-4", "50% 12%", "2026", "Свобода — самій обирати, якою бути.", "raw"),
], "Змінювалися епохи й силуети. Хустка залишалася поруч.", (["zolote-44-1", "iskra-65-1", "puls-44-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Обрати свою", "Decades")

# 2 — one scarf through the decades
triptych("t02-avantiura-decades", "«Авантюра» крізь десятиліття", [
    ("avantiura-88-5", "62% 35%", "1940-ві", "За м’якістю шовку приховувався характер.", "spot"),
    ("avantiura-88-2", "45% 40%", "1950-ті", "Хустка ставала яскравим акцентом.", "sepia"),
    ("avantiura-88-4", "50% 25%", "2026", "Готовність виходити за межі звичного.", "raw"),
], "Одна хустка — три епохи жіночої сили.", (["avantiura-88-1"], "Шовкова хустка «Авантюра»", "6 600 грн"), "Обрати «Авантюру»", "One scarf, three decades")

# 3 — the path to yourself in three states
triptych("t03-three-states", "Три стани", [
    ("tysha-88-3", "50% 45%", "Тиша", "Почути себе серед зовнішнього шуму.", "raw", {"size": 118}),
    ("zolote-44-2", "50% 22%", "Ясність", "Момент, коли все стає на свої місця.", "raw", {"size": 110}),
    ("krok-44-2", "50% 30%", "Крок", "Рух уперед — з довірою до себе.", "raw", {"size": 118}),
], "Після пошуку й внутрішньої тиші настає момент руху вперед.", (["tysha-88-1", "zolote-44-1", "krok-44-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Знайти свій стан", "Three states")

# 4 — one print, three looks (product and price on each band)
triptych("t04-flirt-three-ways", "Один принт — три образи", [
    ("flirt-65-3", "35% 30%", "На голові", "Флірт — це насамперед стан.", "raw", {"tag": "Хустка 65 × 65 · 4 800 грн", "size": 96}),
    ("flirt-tw-1", "50% 40%", "У волоссі", "Невимушена жіночність щодня.", "raw", {"tag": "Твіллі · 1 600 грн", "size": 96}),
    ("flirt-tw-4", "50% 72%", "Поясом", "Акцент, що збирає образ.", "raw", {"tag": "Твіллі · 1 600 грн", "size": 96}),
], "«Флірт»: хустка й твіллі одного принту.", (["flirt-65-1", "flirt-tw-2"], "Шовковий «Флірт»", "від 1 600 грн"), "Обрати «Флірт»", "Flirt three ways")

# 5 — one scarf, three ways to wear
triptych("t05-avantiura-ways", "Одна хустка — три способи", [
    ("avantiura-88-5", "62% 35%", "У волоссі", "Бант, який помічають.", "raw", {"size": 96}),
    ("avantiura-88-4", "50% 22%", "На шиї", "Класика, що не виходить з моди.", "raw", {"size": 96}),
    ("avantiura-88-2", "45% 55%", "Поясом", "Акцент на талії.", "raw", {"size": 96}),
], "Велика хустка 88 × 88 — стільки образів, скільки захочете.", (["avantiura-88-1"], "Шовкова хустка «Авантюра»", "6 600 грн"), "Обрати «Авантюру»", "Avantiura three ways")

# 6 — formats: from twilly to 88 × 88
triptych("t06-formats", "Оберіть свій формат", [
    ("krok-tw-2", "50% 45%", "Твіллі", "Стрічка у волосся, на сумку чи зап’ястя.", "raw", {"tag": "84 × 5 см · 1 600 грн", "size": 110}),
    ("krok-44-2", "50% 30%", "44 × 44", "Маленька хустка на шию.", "raw", {"tag": "Хустка · 2 400 грн", "size": 110}),
    ("tysha-88-4", "40% 30%", "88 × 88", "Велика хустка — на плечі, поясом, на голову.", "raw", {"tag": "Хустка · 6 600 грн", "size": 110}),
], "Сім принтів у різних форматах — від стрічки до великої хустки.", (["krok-tw-1", "krok-44-1", "tysha-88-1"], "Шовк SOLO", "від 1 600 грн"), "Обрати формат", "Formats")

# 7 — who to give it to
triptych("t07-gift", "Кому подарувати", [
    ("iskra-65-2", "40% 28%", "Сміливій", "«Іскра» — сміливість бути помітною.", "raw", {"size": 104}),
    ("tysha-88-3", "50% 45%", "Спокійній", "«Тиша всередині» — чути себе.", "raw", {"size": 104}),
    ("krok-44-3", "50% 25%", "Рішучій", "«Сміливий крок» — довіра до себе.", "raw", {"size": 104}),
], "Подаруйте не річ, а стан — у фірмовій жовтій коробці.", (["iskra-65-1", "tysha-88-1", "krok-44-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Підібрати подарунок", "Gift")

# 8 — Ukrainian premium in details
triptych("t08-premium-details", "Український шовк преміум-класу", [
    (f"url({HI(PP['avantiura'])})", "center/120%", "Картина", "Авторський принт художниці-засновниці бренду.", "raw", {"size": 110}),
    (f"url(src/avantiura-88-5-2k.webp)", "65% 45%/cover", "Шовк", "100% італійський шовк, двосторонній друк.", "raw", {"size": 118}),
    (f"url(src/{PP['iskra']['flat']}-hi.webp)", "0% 100%/190%", "Руки", "Край кожної хустки обробляють вручну.", "raw", {"size": 118}),
], "Зроблено в Україні — від картини до жовтої коробки.", (["avantiura-88-1"], "Шовкова хустка «Авантюра»", "6 600 грн"), "Роздивитися деталі", "Premium details")

# 9 — then and now (two bands would break the rhythm: three bands, the middle one is the product)
triptych("t09-then-now", "Тоді й тепер", [
    ("zolote-44-3", "50% 22%", "Тоді", "Образи акторок 40–50-х.", "bw", {"size": 118}),
    (f"url({HI(PP['zolote'])})", "center/160%", "Шовк", "Хустка «Золоте світло».", "raw", {"size": 118}),
    ("zolote-44-2", "50% 22%", "Тепер", "Та сама сила — ваш образ.", "raw", {"size": 118}),
], "Колекцію натхнили ретро-обкладинки модних журналів.", (["zolote-44-1"], "Шовкова хустка «Золоте світло»", "2 400 грн"), "Обрати «Золоте світло»", "Then and now")


# ---------------------------------------------------------------- more stories
triptych("t10-four-states", "Знайдіть свій стан", [
    ("iskra-65-2", "40% 28%", "Іскра", "Сміливість бути помітною.", "raw"),
    ("flirt-65-3", "35% 28%", "Флірт", "Насолоджуватися моментом.", "raw"),
    ("puls-44-4", "50% 22%", "Пульс", "Свій ритм, що б не сталося.", "raw"),
    ("avantiura-88-5", "62% 35%", "Авантюра", "За межі звичного.", "raw"),
], "Сім авторських принтів — сім станів на шляху жінки до себе.", (["iskra-65-1", "flirt-65-1", "puls-44-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Знайти свій", "Four states")

triptych("t11-acts-of-freedom", "Маленькі акти свободи", [
    ("puls-44-2", "42% 40%", "Сукня", "Улюблена — як нагадування: я є.", "raw"),
    ("krok-44-2", "50% 30%", "Хустка", "Шовкова — щоранку, для себе.", "raw"),
    ("tysha-88-3", "50% 45%", "Помада", "Червона — навіть коли світ сірий.", "raw"),
], "Я є. Я продовжую жити. Я обираю себе.", (["krok-44-1"], "Шовкова хустка «Сміливий крок»", "2 400 грн"), "Обрати для себе", "Small acts of freedom")

triptych("t12-one-print-look", "Хустка й твіллі одного принту", [
    ("iskra-65-2", "40% 28%", "Хустка", "«Іскра» на плечах.", "raw", {"tag": "65 × 65 · 4 800 грн", "size": 110}),
    ("iskra-tw-3", "50% 60%", "Твіллі", "Та сама «Іскра» — на сумці.", "raw", {"tag": "84 × 5 · 1 600 грн", "size": 110}),
], "Разом — 6 400 грн, доставка безкоштовна.", (["iskra-65-1", "iskra-tw-1"], "Образ «Іскра»", "6 400 грн"), "Зібрати образ", "One print, whole look")

triptych("t13-through-the-day", "Шовк на весь день", [
    ("puls-44-2", "42% 40%", "Ранок", "Кава й хустка на зап’ясті.", "raw"),
    ("iskra-tw-2", "50% 25%", "День", "Твіллі до ділового образу.", "raw"),
    ("zolote-44-3", "50% 22%", "Вечір", "Хустка, що ловить світло.", "raw"),
], "Одна колекція — від ранку до вечора.", (["puls-44-1", "iskra-tw-1", "zolote-44-1"], "Шовк SOLO", "від 1 600 грн"), "Обрати свій", "Through the day")

triptych("t14-where-to-wear", "Як носити шовк", [
    ("zolote-44-2", "50% 22%", "На шиї", "", "raw", {"tag": "Хустка · 2 400 грн"}),
    ("avantiura-tw-3", "50% 40%", "У волоссі", "", "raw", {"tag": "Твіллі · 1 600 грн"}),
    ("iskra-tw-3", "50% 60%", "На сумці", "", "raw", {"tag": "Твіллі · 1 600 грн"}),
    ("puls-44-5", "45% 60%", "На зап’ясті", "", "raw", {"tag": "Хустка · 2 400 грн"}),
], "Традиційно на шиї, у волоссі, на сумці чи зап’ясті.", (["zolote-44-1", "avantiura-tw-2", "puls-44-1"], "Хустки й твіллі SOLO", "від 1 600 грн"), "Спробувати", "Where to wear")

triptych("t15-for-whom", "Для кого", [
    ("tysha-88-2", "50% 5%", "Мамі", "«Тиша всередині» — спокій і гідність.", "raw", {"size": 118}),
    ("flirt-65-3", "35% 28%", "Подрузі", "«Флірт» — легкість і усмішка.", "raw", {"size": 118}),
    ("krok-44-3", "50% 22%", "Собі", "«Сміливий крок» — бо час.", "raw", {"size": 118}),
], "Шовкова хустка у фірмовій жовтій коробці.", (["tysha-88-1", "flirt-65-1", "krok-44-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Обрати подарунок", "For whom")

triptych("t16-ua-it-you", "Український преміум", [
    (f"url({HI(PP['tysha'])})", "center/140%", "Україна", "Авторський принт і ручна обробка краю.", "raw", {"size": 104}),
    ("url(src/avantiura-88-5-2k.webp)", "70% 50%/cover", "Італія", "100% натуральний шовк.", "raw", {"size": 118}),
    ("avantiura-88-4", "50% 22%", "Ви", "І ваш образ.", "raw", {"size": 130}),
], "Український бренд Obiimy — шовкові вироби з авторськими принтами.", (["avantiura-88-1"], "Шовкова хустка «Авантюра»", "6 600 грн"), "Роздивитися", "UA · IT · You")

triptych("t17-grey-colour", "Шовкова свобода", [
    ("puls-44-2", "42% 40%", "Сірий світ", "Коли навколо тривоги й невизначеність…", "bw", {"size": 96}),
    ("puls-44-2", "42% 40%", "Ваш колір", "…краса стає способом зберегти себе.", "spot", {"size": 96}),
], "Мода — це про гідність і право на жіночність.", (["puls-44-1"], "Шовкова хустка «Пульс»", "2 400 грн"), "Знайти свій колір", "Grey world, your colour")

triptych("t18-twilly-three-ways", "Одна стрічка — три образи", [
    ("krok-tw-2", "50% 40%", "У волоссі", "Замість резинки — шовк.", "raw", {"size": 100}),
    ("iskra-tw-3", "50% 60%", "На сумці", "Акцент, що оживляє класику.", "raw", {"size": 100}),
    ("flirt-tw-4", "50% 72%", "Поясом", "На тренчі — як у п’ятдесятих.", "raw", {"size": 100}),
], "Твіллі — у кожному з семи принтів колекції.", (["krok-tw-1", "iskra-tw-1", "flirt-tw-2"], "Шовкова твіллі", "1 600 грн"), "Обрати стрічку", "Twilly three ways")

triptych("t19-krok-path", "«Сміливий крок»", [
    ("krok-44-3", "50% 20%", "Пошук", "Сумніви й відкриття.", "bw"),
    ("krok-tw-3", "50% 40%", "Тиша", "Почути себе.", "sepia"),
    ("krok-44-2", "50% 30%", "Крок", "Бо з’являється довіра до себе.", "raw"),
], "Після пошуку й внутрішньої тиші настає момент руху вперед.", (["krok-44-1", "krok-tw-1"], "«Сміливий крок»", "від 1 600 грн"), "Зробити крок", "Krok path")


# ================================================================= PRODUCT-FIRST banners (colour of the print + the product)
def deep(pid): return PP[pid]["deep"]
HERO = [("iskra", "iskra-65-1", "Хустка 65 × 65", "4 800 грн", "iskra-65-2", "40% 28%", "На плечах", "Обрати «Іскру»"),
        ("flirt", "flirt-65-1", "Хустка 65 × 65", "4 800 грн", "flirt-65-3", "35% 28%", "На голові", "Обрати «Флірт»"),
        ("puls", "puls-44-1", "Хустка 44 × 44", "2 400 грн", "puls-44-4", "50% 22%", "На шиї", "Обрати «Пульс»"),
        ("zolote", "zolote-44-1", "Хустка 44 × 44", "2 400 грн", "zolote-44-3", "50% 22%", "На шиї", "Обрати «Золоте світло»"),
        ("avantiura", "avantiura-88-1", "Хустка 88 × 88", "6 600 грн", "avantiura-88-5", "62% 35%", "У волоссі", "Обрати «Авантюру»"),
        ("tysha", "tysha-88-1", "Хустка 88 × 88", "6 600 грн", "tysha-88-3", "50% 45%", "На голові", "Обрати «Тишу всередині»"),
        ("krok", "krok-44-1", "Хустка 44 × 44", "2 400 грн", "krok-44-2", "50% 30%", "На шиї", "Обрати «Сміливий крок»")]
for i, (pid, cut, fmt, price, ph, pos, how, cta) in enumerate(HERO, 1):
    p = PP[pid]
    triptych(f"q{i:02d}-{pid}", "Шовкова хустка", [
        (cut, f"linear-gradient(160deg,{p['c']},{p['deep']})", f"«{p['name']}»", p["short"] + ".", "cut", {"tag": f"{fmt} · {price}", "size": 92 if len(p["name"]) < 9 else 76}),
        (ph, pos, how, "Натуральний шовк, двосторонній друк.", "raw", {"size": 104}),
    ], p["state"].split(". ")[0].rstrip(".") + ".", ([cut], f"Хустка «{p['name']}»", price), "Обрати хустку" if len(p["name"]) > 8 else cta, f"Product hero: {p['name']}")

triptych("q08-ladder", "Оберіть свій формат", [
    ("krok-tw-1", f"linear-gradient(160deg,{PP['krok']['c']},{deep('krok')})", "Твіллі", "84 × 5 см", "cut", {"tag": "1 600 грн"}),
    ("puls-44-1", f"linear-gradient(160deg,{PP['puls']['c']},{deep('puls')})", "44 × 44", "Маленька хустка", "cut", {"tag": "2 400 грн"}),
    ("iskra-65-1", f"linear-gradient(160deg,{PP['iskra']['c']},{deep('iskra')})", "65 × 65", "Класична хустка", "cut", {"tag": "4 800 грн"}),
    ("avantiura-88-1", f"linear-gradient(160deg,{PP['avantiura']['c']},{deep('avantiura')})", "88 × 88", "Велика хустка", "cut", {"tag": "6 600 грн"}),
], "Сім авторських принтів — від стрічки до великої хустки.", (["krok-tw-1", "puls-44-1", "avantiura-88-1"], "Шовк SOLO", "від 1 600 грн"), "Обрати формат", "Format ladder")

triptych("q09-twillies", "Твіллі SOLO", [
    ([(p["tw"], f"«{p['name']}»", "1 600 грн") for p in P], "linear-gradient(170deg,#2A2320,#141110)", "Сім стрічок.", "Одна ціна — 1 600 грн.", "grid", {"size": 104, "h": 300, "gtop": 300}),
], "Шовкова твіллі 84 × 5 см — у волосся, на шию, на сумку чи зап’ястя.", ([P[0]["tw"], P[4]["tw"], P[6]["tw"]], "Шовкова твіллі", "1 600 грн"), "Обрати стрічку", "Twilly catalogue")

SC = [("iskra", "65 × 65", "4 800"), ("flirt", "65 × 65", "4 800"), ("puls", "44 × 44", "2 400"), ("zolote", "44 × 44", "2 400"), ("avantiura", "88 × 88", "6 600"), ("tysha", "88 × 88", "6 600"), ("krok", "44 × 44", "2 400")]
triptych("q10-scarves", "Хустки SOLO", [
    ([(PP[i]["flat"], f"«{PP[i]['name']}»", f"{f} · {pr} грн") for i, f, pr in SC], "linear-gradient(170deg,#2A2320,#141110)", "Сім хусток.", "Сім станів.", "grid", {"size": 104, "h": 210, "gtop": 300}),
], "Натуральний шовк, двосторонній друк, авторські принти.", (["iskra-65-1", "tysha-88-1", "krok-44-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Обрати хустку", "Scarf catalogue")

triptych("q11-double", "Двосторонній друк", [
    ("iskra-65-1", f"linear-gradient(160deg,{PP['iskra']['c']},{deep('iskra')})", "Лицьовий бік", "Принт «Іскра».", "cut", {"size": 84}),
    ("iskra-65-5", f"linear-gradient(200deg,{PP['iskra']['c']},{deep('iskra')})", "І зворот", "Такий самий яскравий.", "cut", {"size": 96}),
], "Жодного вивороту — зав’язуйте як завгодно.", (["iskra-65-1"], "Шовкова хустка «Іскра»", "4 800 грн"), "Роздивитися «Іскру»", "Double-sided")

triptych("q12-box", "Маленький подарунок", [
    ("url(src/flirt-scr-1-2k.webp)", "50% 55%/cover", "700 грн", "", "raw", {"size": 118}),
    ("flirt-scr-3", "50% 40%", "Резинка", "Шовкова «Флірт» — у фірмовій жовтій коробочці.", "raw", {"size": 110}),
], "Перше знайомство з Obiimy — шовк, який не лишає заломів.", (["flirt-scr-1"], "Шовкова резинка «Флірт»", "700 грн"), "Подарувати «Флірт»", "Yellow box")

SETS = [("avantiura", "avantiura-88-1", "Хустка 88 × 88", "6 600", "8 200"), ("tysha", "tysha-88-1", "Хустка 88 × 88", "6 600", "8 200"), ("krok", "krok-44-1", "Хустка 44 × 44", "2 400", "4 000")]
for k, (pid, cut, fmt, pr, total) in enumerate(SETS, 13):
    p = PP[pid]
    triptych(f"q{k:02d}-set-{pid}", "Хустка + твіллі одного принту", [
        (cut, f"linear-gradient(160deg,{p['c']},{p['deep']})", "Хустка", f"«{p['name']}»", "cut", {"tag": f"{fmt} · {pr} грн", "size": 110}),
        (p["tw"], f"linear-gradient(200deg,{p['c']},{p['deep']})", "Твіллі", f"«{p['name']}»", "cut", {"tag": "84 × 5 · 1 600 грн", "size": 110}),
    ], "Один принт — хустка на шию, стрічка у волосся чи на сумку." + (" Доставка безкоштовна." if int(total.replace(" ", "")) >= 5000 else ""),
       ([cut, p["tw"]], f"Образ «{p['name']}»", f"{total} грн"), "Зібрати образ", f"Set: {p['name']}")


# ================================================================= DOWN-TO-EARTH product banners: what it is, size, price, how to buy
def grad(pid, a=160): return f"linear-gradient({a}deg,{PP[pid]['c']},{PP[pid]['deep']})"
DARK = "linear-gradient(170deg,#2A2320,#141110)"
CARD = [("iskra", "iskra-65-1", "65 × 65 см", "4 800 грн", "iskra-65-3", "55% 50%", "На сумці чи на плечах"),
        ("flirt", "flirt-65-1", "65 × 65 см", "4 800 грн", "flirt-65-3", "35% 28%", "На голові чи на шиї"),
        ("puls", "puls-44-1", "44 × 44 см", "2 400 грн", "puls-44-5", "45% 60%", "На зап’ясті чи на шиї"),
        ("zolote", "zolote-44-1", "44 × 44 см", "2 400 грн", "zolote-44-2", "50% 22%", "На шиї"),
        ("avantiura", "avantiura-88-1", "88 × 88 см", "6 600 грн", "avantiura-88-2", "45% 50%", "Поясом, на шиї, у волоссі"),
        ("tysha", "tysha-88-1", "88 × 88 см", "6 600 грн", "tysha-88-2", "50% 5%", "На плечах чи на голові"),
        ("krok", "krok-44-1", "44 × 44 см", "2 400 грн", "krok-44-3", "50% 22%", "На шиї чи на зап’ясті")]
for i, (pid, cut, size_, price, ph, pos, how) in enumerate(CARD, 1):
    p = PP[pid]
    triptych(f"k{i:02d}-card-{pid}", "Шовкова хустка", [
        (cut, grad(pid), f"«{p['name']}»", "Шовкова хустка.", "cut", {"tag": f"{size_} · {price}", "size": 92 if len(p["name"]) < 9 else 76}),
        ([("Розмір", size_), ("Матеріал", "100% натуральний шовк"), ("Друк", "двосторонній"), ("Край", "оброблений вручну"), ("Принт", "авторський")], "", "", "", "spec"),
        (ph, pos, "Як носити", how + ".", "raw", {"size": 92}),
    ], "Шовкова хустка з авторським принтом. Зроблено в Україні.", ([cut], f"Хустка «{p['name']}»", price), "Купити", f"Product card: {p['name']}")

triptych("k08-card-twilly", "Шовкова твіллі", [
    (["iskra-tw-1", "avantiura-tw-2", "zolote-tw-1"], DARK, "Твіллі", "Вузька шовкова стрічка.", "cut", {"tag": "84 × 5 см · 1 600 грн", "frac": .8}),
    ([("Розмір", "84 × 5 см"), ("Матеріал", "натуральний шовк"), ("Принти", "7 на вибір"), ("Як носити", "волосся, шия, сумка, зап’ястя"), ("Ціна", "1 600 грн")], "", "", "", "spec"),
    ("krok-tw-2", "50% 40%", "У волоссі", "Замість звичайної резинки.", "raw", {"size": 100}),
], "Одна ціна для всіх семи принтів колекції.", (["iskra-tw-1", "avantiura-tw-2", "krok-tw-1"], "Шовкова твіллі", "1 600 грн"), "Купити", "Twilly card")

triptych("k09-card-scrunchie", "Шовкова резинка", [
    ("url(src/flirt-scr-1-2k.webp)", "50% 55%/cover", "Резинка", "Шовкова, для волосся.", "raw", {"tag": "700 грн", "size": 110}),
    ([("Виріб", "резинка для волосся"), ("Матеріал", "натуральний шовк"), ("Принт", "«Флірт»"), ("Упаковка", "фірмова жовта коробочка"), ("Ціна", "700 грн")], "", "", "", "spec"),
    ("flirt-scr-3", "50% 40%", "На щодень", "І як невеликий подарунок.", "raw", {"size": 100}),
], "Найдоступніша річ колекції SOLO.", (["flirt-scr-1"], "Шовкова резинка «Флірт»", "700 грн"), "Купити", "Scrunchie card")

triptych("k10-sizes", "Який розмір обрати?", [
    ("puls-44-1", grad("puls"), "44 × 44", "На шию, на зап’ястя, на ручку сумки.", "cut", {"tag": "2 400 грн", "frac": .5}),
    ("iskra-65-1", grad("iskra"), "65 × 65", "На шию, на голову, на плечі.", "cut", {"tag": "4 800 грн", "frac": .72}),
    ("avantiura-88-1", grad("avantiura"), "88 × 88", "На плечі, на голову, поясом.", "cut", {"tag": "6 600 грн", "frac": .96}),
], "Що більша хустка, то більше способів її зав’язати.", (["puls-44-1", "iskra-65-1", "avantiura-88-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Обрати розмір", "Which size")

triptych("k11-what-is-twilly", "Що таке твіллі?", [
    ("krok-tw-1", grad("krok"), "Твіллі", "Вузька шовкова стрічка 84 × 5 см.", "cut", {"tag": "1 600 грн", "frac": .86}),
    ("avantiura-tw-3", "50% 40%", "У волосся", "Бантом на хвіст чи косу.", "raw"),
    ("iskra-tw-3", "50% 60%", "На сумку", "На ручку — бантом або обмоткою.", "raw"),
    ("iskra-tw-2", "50% 28%", "На шию", "Як тонка краватка чи бант.", "raw"),
], "Сім принтів, одна ціна — 1 600 грн.", (["krok-tw-1", "avantiura-tw-2", "iskra-tw-1"], "Шовкова твіллі", "1 600 грн"), "Обрати твіллі", "What is a twilly")

triptych("k12-how-to-order", "Як замовити", [
    ("iskra-65-1", grad("iskra"), "1", "Оберіть принт і формат на obiimy.world.", "cut", {"size": 150, "frac": .7}),
    ("zolote-44-1", grad("zolote"), "2", "Оплатіть карткою або частинами — через ПриватБанк чи monobank.", "cut", {"size": 150, "frac": .7}),
    ("krok-44-1", grad("krok"), "3", "Відправимо Новою поштою в день замовлення — якщо замовити до 16:00.", "cut", {"size": 150, "frac": .7}),
], "Від 5 000 грн доставка по Україні безкоштовна.", (["iskra-65-1", "zolote-44-1", "krok-44-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Замовити", "How to order")

triptych("k13-prices", "Ціни колекції", [
    ([("Резинка для волосся", "700 грн", "flirt-scr-1"), ("Твіллі 84 × 5", "1 600 грн", "iskra-tw-1"), ("Хустка 44 × 44", "2 400 грн", "puls-44-1"),
      ("Хустка 65 × 65", "4 800 грн", "flirt-65-1"), ("Хустка 88 × 88", "6 600 грн", "tysha-88-1")], "", "Скільки коштує SOLO", "", "spec", {"size": 84, "fs": 50, "lw": 400}),
], "Натуральний шовк, авторські принти, двосторонній друк хусток.", (["flirt-scr-1", "iskra-tw-1", "tysha-88-1"], "Шовкові вироби SOLO", "від 700 грн"), "До каталогу", "Price list")

triptych("k14-budget", "Подарунок за бюджетом", [
    ("flirt-scr-1", DARK, "До 1 000", "Шовкова резинка «Флірт».", "cut", {"tag": "700 грн", "frac": .7}),
    ("zolote-tw-1", grad("zolote"), "До 2 000", "Шовкова твіллі, 7 принтів.", "cut", {"tag": "1 600 грн", "frac": .86}),
    ("krok-44-1", grad("krok"), "До 3 000", "Шовкова хустка 44 × 44.", "cut", {"tag": "2 400 грн", "frac": .8}),
    ("iskra-65-1", grad("iskra"), "До 5 000", "Шовкова хустка 65 × 65.", "cut", {"tag": "4 800 грн", "frac": .86}),
], "Підпишемо подарунок вашими словами — напишіть текст у замовленні.", (["flirt-scr-1", "zolote-tw-1", "iskra-65-1"], "Шовкові вироби SOLO", "від 700 грн"), "Обрати подарунок", "Gift by budget")

triptych("k15-scarves-44", "Хустки 44 × 44 см", [
    ("puls-44-1", grad("puls"), "«Пульс»", "Зелена, з квітковим малюнком.", "cut", {"tag": "2 400 грн"}),
    ("zolote-44-1", grad("zolote"), "«Золоте світло»", "Карамельна, з геометрією.", "cut", {"tag": "2 400 грн", "size": 72}),
    ("krok-44-1", grad("krok"), "«Сміливий крок»", "Бордова, з монограмою.", "cut", {"tag": "2 400 грн", "size": 72}),
], "Маленька шовкова хустка: на шию, зап’ястя чи сумку.", (["puls-44-1", "zolote-44-1", "krok-44-1"], "Хустка 44 × 44", "2 400 грн"), "Обрати принт", "Scarves 44")

triptych("k16-scarves-65", "Хустки 65 × 65 см", [
    ("iskra-65-1", grad("iskra"), "«Іскра»", "Великий синій горох, помаранчевий край.", "cut", {"tag": "4 800 грн", "frac": .86}),
    ("flirt-65-1", grad("flirt"), "«Флірт»", "Дрібний горох, оливковий край.", "cut", {"tag": "4 800 грн", "frac": .86}),
], "Класичний розмір: на шию, на голову, на плечі.", (["iskra-65-1", "flirt-65-1"], "Хустка 65 × 65", "4 800 грн"), "Обрати принт", "Scarves 65")

triptych("k17-scarves-88", "Хустки 88 × 88 см", [
    ("avantiura-88-1", grad("avantiura"), "«Авантюра»", "Білі іриси на бордовому.", "cut", {"tag": "6 600 грн", "frac": .86}),
    ("tysha-88-1", grad("tysha"), "«Тиша всередині»", "Графічні іриси на білому.", "cut", {"tag": "6 600 грн", "frac": .86, "size": 72}),
], "Велика хустка: на плечі, на голову, поясом. Можна частинами.", (["avantiura-88-1", "tysha-88-1"], "Хустка 88 × 88", "6 600 грн"), "Обрати принт", "Scarves 88")

triptych("k18-delivery-payment", "Доставка й оплата", [
    ([("Нова пошта", "відправка в день замовлення до 16:00"), ("Безкоштовно", "від 5 000 грн"), ("За кордон", "за тарифами перевізника"),
      ("Оплата", "карткою Visa / Mastercard"), ("Частинами", "ПриватБанк — 4, monobank — 3"), ("Шоурум", "Київ, вул. П. Сагайдачного, 12")], "", "", "", "spec", {"fs": 34, "lw": 280}),
    (["puls-44-1", "avantiura-tw-2"], DARK, "Хустки й твіллі", "Сім авторських принтів.", "cut", {"tag": "від 1 600 грн", "frac": .62, "size": 80}),
], "Замовляйте на obiimy.world або приходьте приміряти в шоурум.", (["puls-44-1", "avantiura-tw-2"], "Шовкові вироби SOLO", "від 1 600 грн"), "Замовити", "Delivery and payment")

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · SOLO triptych</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Oswald:wght@500&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("solo7.html" if YELLOW else "solo6.html")).write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "triptych banners", "(yellow)" if YELLOW else "")
