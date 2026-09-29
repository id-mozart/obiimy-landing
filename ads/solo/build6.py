"""SOLO triptych banners (1080×1920, plain banner — no story padding): three horizontal photo bands that tell
one story (decades, states, ways to wear, formats…), then a product line and a CTA at the bottom.
Copy from the press release; prices/facts from obiimy.world. YELLOW=1 → product line on the yellow brand plate.
Output: solo6.html / solo7.html → out6 / out7."""
import os, pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit import P, PP, S, CUT, HI, spot_photo, nb, LOGO_W, LOGO_K, GRAIN

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
.band .veil { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(12,9,8,.9) 0%, rgba(12,9,8,.66) 42%, rgba(12,9,8,0) 76%); }
.band .txt { position: absolute; left: 64px; top: 50%; transform: translateY(-50%); width: 620px; }
.big { font-family: 'Playfair Display', serif; font-weight: 900; font-style: italic; line-height: .95; letter-spacing: -.01em; text-wrap: balance; }
.small { font-family: 'EB Garamond', 'Cormorant Garamond', serif; font-weight: 500; font-size: 40px; line-height: 1.14; margin-top: 26px; text-wrap: pretty; text-shadow: 0 1px 10px rgba(0,0,0,.55); }
.kicker { font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: .14em; font-size: 28px; color: #E0B040; white-space: nowrap; }
.tag { display: inline-block; margin-top: 16px; font-family: 'Onest'; font-weight: 600; font-size: 28px; letter-spacing: .04em; padding: 10px 20px; border-radius: 999px; background: rgba(243,234,219,.16); border: 1.5px solid rgba(243,234,219,.4); }
.cta { font-family: 'Onest'; font-weight: 600; font-size: 30px; padding: 24px 38px; border-radius: 999px; background: #F2B705; color: #141216; white-space: nowrap; flex: none; }
""".replace("GRAIN", GRAIN)

ads = []
def ad(id, body, note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad" id="{id}">{body}\n</section>')

FILTERS = {"dim": "filter:grayscale(.62) contrast(1.1) brightness(1.04)", "bw": "filter:grayscale(1) contrast(1.12)", "sepia": "filter:sepia(.4) saturate(1.1) contrast(1.05)", "raw": "", "": ""}

def band(top, height, b, n=3):
    photo, pos, big, small, look = b[:5]
    extra = b[5] if len(b) > 5 else {}
    size = extra.get("size", 118 if len(big) <= 6 else 100 if len(big) <= 8 else 84)
    if n == 4: size = min(size, 84)
    if n == 1 and look not in ("grid",): size = extra.get("size", 130)
    tag_style = "" if small else ' style="margin-top:30px"'
    tag = f'<p class="tag"{tag_style}>{extra["tag"]}</p>' if extra.get("tag") else ""
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
    if look == "side":
        # sharp product photo as a square on the right, print colour on the left — nothing lies on the product
        return f'''
  <div class="band" style="top:{top}px;height:{height}px;background:{pos}">
    <img src="{photo}" alt="" style="position:absolute;right:0;top:0;width:{height}px;height:{height}px;object-fit:cover;object-position:{extra.get("at", "50% 50%")}">
    <div class="txt" style="width:{1080 - height - 64 - 40}px;color:#141216"><p class="big" style="font-size:{min(size, 96)}px">{big}</p>{f'<p class="small" style="text-shadow:none;margin-top:{extra.get("gap", 26)}px">{nb(small)}</p>' if small else ""}{tag.replace('class="tag"', 'class="tag" style="background:#141216;color:#F3EADB;border-color:#141216"')}</div></div>'''
    if look == "one":
        src = f"src/{photo}-2k.webp" if (HERE / f"src/{photo}-2k.webp").exists() else S(photo)
        return f'''
  <div class="band" style="top:{top}px;height:{height}px"><img src="{src}" alt="" style="object-position:{pos}{";transform-origin:50% 0;transform:translateY(-110px) scale(1.1)" if extra.get("lift") else ""}">
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,9,8,0) 52%,rgba(12,9,8,.62) 74%,rgba(12,9,8,.9) 100%)"></div>
    <div style="position:absolute;left:64px;right:64px;bottom:54px"><p class="big" style="font-size:{extra.get("size", 120)}px">{big}</p>{f'<p class="small" style="font-size:44px;margin-top:22px">{nb(small)}</p>' if small else ""}{tag}</div></div>'''
    if look == "html":
        return f'''
  <div class="band" style="top:{top}px;height:{height}px;background:{pos}">{photo}
    <div class="txt" style="width:{extra.get("tw", 470)}px"><p class="big" style="font-size:{size}px;line-height:1.02">{big}</p>{f'<p class="small" style="margin-top:30px">{nb(small)}</p>' if small else ""}{tag}</div></div>'''
    if look == "zoom":
        # macro view of the hand-finished corner: the flat product shot, enlarged, on the colour of the print
        return f'''
  <div class="band" style="top:{top}px;height:{height}px;background:{pos}">
    <img src="{CUT(photo)}" alt="" style="position:absolute;left:{extra.get("x", 470)}px;bottom:{extra.get("y", -60)}px;width:{extra.get("w", 1500)}px;height:auto;max-width:none;filter:drop-shadow(0 30px 40px rgba(0,0,0,.5))">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(12,9,8,.78) 0%,rgba(12,9,8,.35) 40%,rgba(12,9,8,0) 60%)"></div>
    <div class="txt" style="width:430px"><p class="big" style="font-size:{size}px;line-height:1.05">{big}</p>{f'<p class="small" style="margin-top:30px">{nb(small)}</p>' if small else ""}{tag}</div></div>'''
    if look == "cut":
        cuts = photo if isinstance(photo, list) else [photo]
        longest = max(len(w) for w in big.split()) if big else 1
        size = min(size, int(450 / (0.66 * longest)))
        imgs = "".join(f'<img src="{CUT(c)}" alt="" style="height:{int(height * extra.get("frac", 0.8 if len(cuts) == 1 else 0.72))}px;width:auto;max-width:{460 if len(cuts) == 1 else int(440 / len(cuts)) + 40}px;object-fit:contain;margin-left:{0 if i == 0 else -40}px;filter:drop-shadow(0 26px 30px rgba(0,0,0,.45));transform:rotate({(-6, 7, -3)[i % 3]}deg)">' for i, c in enumerate(cuts))
        pic = (f'<div style="position:absolute;inset:0;background:radial-gradient(70% 90% at 72% 50%,rgba(255,255,255,.2),rgba(0,0,0,0) 70%),{pos}"></div>'
               f'<div style="position:absolute;right:40px;top:0;bottom:0;display:flex;align-items:center">{imgs}</div>')
        return f'''
  <div class="band" style="top:{top}px;height:{height}px">{pic}
    <div class="txt" style="width:450px"><p class="big" style="font-size:{size}px">{big}</p>{f'<p class="small" style="text-shadow:none;margin-top:{extra.get("gap", 26)}px">{nb(small)}</p>' if small else ""}{tag}</div></div>'''
    if look == "grid":
        cells = "".join(f'<div style="display:grid;justify-items:center;gap:8px;text-align:center"><img src="{CUT(c)}" alt="" style="height:{extra.get("h", 230)}px;width:auto;max-width:230px;object-fit:contain;filter:drop-shadow(0 16px 18px rgba(0,0,0,.45))"><p style="font-family:Cormorant Garamond,serif;font-style:italic;font-size:34px;line-height:1">{n}</p><p style="font-family:Onest;font-weight:600;font-size:26px;line-height:1.3;color:#E9D7A6">{pr.replace(" · ", "<br>")}</p></div>' for c, n, pr in photo)
        cols = extra.get("cols", 4)
        return f'''
  <div class="band" style="top:{top}px;height:{height}px;background:{pos}">
    <div style="position:absolute;left:64px;top:44px"><p class="big" style="font-size:{size}px;line-height:1.05">{big}</p>{f'<p class="small" style="margin-top:30px">{nb(small)}</p>' if small else ""}</div>
    <div style="position:absolute;left:40px;right:40px;top:{extra.get("gtop", 250)}px;bottom:40px;display:grid;grid-template-columns:repeat({cols},1fr);align-content:center;gap:40px 10px">{cells}</div></div>'''
    fit = extra.get("fit")      # the photo takes only the right part of the band: more of the figure and the scarf fits in
    fade = "-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 30%);mask-image:linear-gradient(90deg,transparent 0,#000 30%)"
    if look == "spot":
        pic = spot_photo(photo, pos, style=f"position:absolute;top:0;bottom:0;right:0;width:{fit}%;{fade}" if fit else "position:absolute;inset:0")
    elif photo.startswith("url("):
        pic = f'<div style="position:absolute;inset:0;background:{photo} {pos}"></div>'
    else:
        more = (";transform:scaleX(-1)" if extra.get("flip") else "") + (";width:%d%%" % extra["wide"] if extra.get("wide") else "") + (f";width:{fit}%;margin-left:auto;{fade}" if fit else "")
        pic = f'<img src="{S(photo)}" alt="" style="object-position:{pos};{FILTERS[look]}{more}">'
    return f'''
  <div class="band" style="top:{top}px;height:{height}px">{pic}<div class="veil"{' style="background:' + extra["veil"] + '"' if extra.get("veil") else ""}></div>
    <div class="txt"><p class="big" style="font-size:{size}px">{big}</p>{f'<p class="small" style="font-size:{36 if n == 4 else 40}px;max-width:{extra.get("cw", 480)}px;margin-top:{extra.get("gap", 26)}px">{nb(small)}</p>' if small else ""}{tag}</div></div>'''

def triptych(id, kicker, bands, tagline, product, cta, note="", plain=False):
    """bands: 3 × (photo, object-position, big label, small line, look[, {tag, size}]); product: (cutouts, title, price)."""
    n = len(bands); top, gap = (176 if plain else 280), 12
    if plain: tagline = ""
    h = ((1676 if plain else 1522) - top - (n - 1) * gap) // n
    body = "".join(band(top + k * (h + gap), h, b, n) for k, b in enumerate(bands))
    cuts, title, price = product
    if len(cuts) == 3 and len(cta) > 13: cuts = cuts[:2]
    thumbs = "".join(f'<img src="{CUT(c)}" alt="" style="height:112px;width:auto;max-width:112px;object-fit:contain;margin-left:{0 if i == 0 else -52}px;filter:drop-shadow(0 8px 10px rgba(0,0,0,.4));transform:rotate({(-6, 5, -3)[i]}deg)">' for i, c in enumerate(cuts))
    plate_bg = "#F2B705" if YELLOW else "rgba(243,234,219,.1)"
    plate_fg = "#141216" if YELLOW else "#F3EADB"
    plate_bd = "none" if YELLOW else "1.5px solid rgba(243,234,219,.3)"
    y0 = top + n * h + (n - 1) * gap
    header = (f'''<img src="{LOGO_W}" alt="" style="left:64px;top:58px;height:58px">
  <p style="right:64px;top:76px;font-family:Montserrat,sans-serif;font-size:26px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap;color:#F3EADB">Авторські шовкові вироби</p>''' if plain else f'''  <div style="left:64px;top:44px;font-family:Montserrat,sans-serif;text-transform:uppercase;color:#fff;line-height:1">
    <p style="font-size:34px;font-weight:400;letter-spacing:.02em">Колекція</p>
    <p style="font-size:132px;font-weight:300;letter-spacing:-.01em;margin-top:6px">Соло</p>
    <p style="font-size:34px;font-weight:400;letter-spacing:.02em;margin-top:8px">Шлях до себе</p></div>
  <img src="{LOGO_W}" alt="" style="right:64px;top:46px;height:50px">
  <p style="right:64px;top:110px;font-family:Montserrat,sans-serif;font-size:21px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;white-space:nowrap;color:#F3EADB">Авторські шовкові вироби</p>
  <p style="right:64px;top:176px;font-family:Montserrat,sans-serif;font-size:26px;font-weight:500;padding:16px 28px;border-radius:999px;background:#F2B705;color:#141216;white-space:nowrap">{kicker}</p>''')
    ad(id, f'''
  <div style="left:0;right:0;top:0;height:{top}px;background:#141110"></div>
  {header}
  {body}
  {f"""<p style="left:64px;right:64px;top:{y0 + 34}px;font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:600;font-size:44px;line-height:1.15;text-wrap:balance">{nb(tagline)}</p>""" if tagline else ""}
  <div style="left:64px;right:64px;bottom:60px;display:flex;align-items:center;justify-content:space-between;gap:24px">
    <div style="display:flex;align-items:center;gap:20px;padding:12px 28px 12px 14px;border-radius:{6 if YELLOW else 20}px;background:{plate_bg};border:{plate_bd};color:{plate_fg};flex:0 1 auto;min-width:0">
      <div style="display:flex;align-items:center;flex:none">{thumbs}</div>
      <div style="min-width:0"><p style="font-size:{29 if len(title) < 30 else 25}px;font-weight:600;line-height:1.18;text-wrap:balance">{nb(title)}</p>{f"""<p style="font-family:'Playfair Display',serif;font-size:46px;line-height:1.05;margin-top:4px;white-space:nowrap">{price}</p>""" if price else ""}</div>
    </div>
    <div class="cta" style="{"background:#F3EADB;color:#141216" if YELLOW else ""}">{cta}</div>
  </div>''', note)

def grad(pid, a=160): return f"linear-gradient({a}deg,{PP[pid]['c']},{PP[pid]['deep']})"
DARK = "linear-gradient(170deg,#2A2320,#141110)"
SCARVES = (["zolote-44-1", "iskra-65-1", "puls-44-1"], "Шовкові хустки SOLO", "від 2 400 грн")

# ================================================================= STORIES in bands
triptych("t01-decades", "Жіноча сила крізь десятиліття", [
    ("zolote-44-2", "50% 20%", "1940-ві", "Сила — у бездоганній елегантності.", "dim", {"fit": 68}),
    ("iskra-65-4", "50% 12%", "1950-ті", "Правила починають руйнуватися. Колір, форма, сміливість.", "sepia", {"fit": 68}),
    ("puls-44-4", "50% 3%", "2026", "Свобода — самій обирати, якою бути.", "raw", {"fit": 68}),
], "", SCARVES, "Обрати хустку", "Decades", plain=True)

triptych("t03-three-states", "Три стани", [
    ("tysha-88-3", "50% 45%", "Тиша", "Почути себе серед зовнішнього шуму.", "raw", {"size": 118}),
    ("zolote-44-2", "50% 22%", "Ясність", "Момент, коли все стає на свої місця.", "raw", {"size": 110}),
    ("krok-44-2", "50% 30%", "Крок", "Рух уперед — з довірою до себе.", "raw", {"size": 118}),
], "Після пошуку й внутрішньої тиші настає момент руху вперед.", (["tysha-88-1", "zolote-44-1", "krok-44-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Знайти свій стан", "Three states")

triptych("t04-flirt-three-ways", "Один принт — три образи", [
    ("flirt-65-3", "35% 30%", "На голові", "Флірт — це насамперед стан.", "raw", {"tag": "Хустка · 4 800 грн", "size": 96}),
    ("flirt-tw-1", "50% 40%", "У волоссі", "Невимушена жіночність щодня.", "raw", {"tag": "Твіллі · 1 600 грн", "size": 96}),
    ("flirt-tw-4", "50% 72%", "На тренчі", "Бант на спинці — замість пряжки.", "raw", {"tag": "Твіллі · 1 600 грн", "size": 96}),
], "«Флірт»: хустка й твіллі одного принту.", (["flirt-65-1", "flirt-tw-5"], "Хустка й твіллі «Флірт»", "від 1 600 грн"), "Обрати «Флірт»", "Flirt three ways")

triptych("t05-avantiura-ways", "Одна хустка — три способи", [
    ("avantiura-88-5", "62% 12%", "У волоссі", "Бант, який помічають.", "raw", {"size": 96, "wide": 112}),
    ("avantiura-88-4", "50% 6%", "На шиї", "Класика, що не виходить<br>з моди.", "raw", {"size": 96, "wide": 125}),
    ("avantiura-88-2", "45% 76%", "Поясом", "Акцент на талії.", "raw", {"size": 96, "wide": 112}),
], "", (["avantiura-88-1"], "Шовкова хустка «Авантюра»", "6 600 грн"), "Обрати хустку", "Avantiura three ways", plain=True)

triptych("t06-formats", "Оберіть свій формат", [
    ("krok-tw-2", "50% 45%", "Твіллі", "Стрічка у волосся, на сумку чи зап’ястя.", "raw", {"tag": "1 600 грн", "size": 110}),
    ("krok-44-2", "50% 30%", "Хустка", "Маленька — на шию.", "raw", {"tag": "від 2 400 грн", "size": 110}),
    ("avantiura-88-2", "45% 52%", "Велика", "На плечі, поясом, на голову.", "raw", {"tag": "6 600 грн", "size": 110}),
], "Сім принтів — від стрічки до великої хустки.", (["krok-tw-5", "krok-44-1", "avantiura-88-1"], "Шовк SOLO", "від 1 600 грн"), "Обрати формат", "Formats")

triptych("t07-gift", "Шовк у подарунок", [
    ("iskra-tw-2", "50% 35%", "День народження", "Твіллі «Іскра».", "raw", {"size": 84, "tag": "1 600 грн", "wide": 128}),
    ("tysha-88-3", "50% 30%", "Річниця", "Хустка<br>«Тиша всередині».", "raw", {"size": 104, "tag": "6 600 грн"}),
    ("zolote-44-2", "50% 36%", "Просто так", "Хустка<br>«Золоте світло».", "raw", {"size": 84, "tag": "2 400 грн", "wide": 145}),
], "Відправимо в день замовлення до 16:00.<br>Підпишемо вашими словами.", (["iskra-tw-4", "tysha-88-1", "zolote-44-1"], "Шовк SOLO", "від 1 600 грн"), "Обрати подарунок", "Gift occasions")

triptych("t08-premium-details", "Преміум у деталях", [
    ("avantiura-88-1", grad("avantiura"), "Принт", "Авторський — від художниці й засновниці бренду.", "cut", {"size": 118, "frac": .84}),
    ("url(src/avantiura-88-5-2k.webp)", "78% 66%/175%", "Шовк", "100% італійський шовк, двосторонній друк.", "raw", {"size": 118}),
    ("avantiura-88-1", grad("avantiura", 200), "Край", "Кожну хустку обробляють вручну.", "zoom", {"size": 118}),
], "Український бренд Obiimy. Зроблено в Україні.", (["avantiura-88-1"], "Шовкова хустка «Авантюра»", "6 600 грн"), "Роздивитися", "Premium details")

triptych("t09-then-now", "Тоді й тепер", [
    ("zolote-44-3", "50% 22%", "Натхнення", "Ретро-обкладинки 40–50-х.", "bw", {"size": 100}),
    (f"url({HI(PP['zolote'])})", "center/160%", "Шовк", "Хустка «Золоте світло».", "raw", {"size": 118}),
    ("zolote-44-2", "50% 22%", "Тепер", "Та сама сила — ваш образ.", "raw", {"size": 118}),
], "Колекцію натхнили ретро-обкладинки модних журналів.", (["zolote-44-1"], "Шовкова хустка «Золоте світло»", "2 400 грн"), "Обрати хустку", "Then and now")

triptych("t10-three-states", "Знайдіть свій стан", [
    ("iskra-65-2", "40% 28%", "Іскра", "Сміливість бути помітною.", "raw"),
    ("flirt-65-3", "35% 28%", "Флірт", "Насолоджуватися моментом.", "raw"),
    ("avantiura-88-5", "62% 35%", "Авантюра", "Виходити за межі звичного.", "raw", {"size": 88}),
], "Сім авторських принтів — сім станів на шляху жінки до себе.", (["iskra-65-1", "flirt-65-1", "avantiura-88-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Обрати хустку", "Find your state")

triptych("t11-acts-of-freedom", "Маленькі акти свободи", [
    ("puls-44-2", "42% 40%", "«Я є.", "", "raw", {"size": 110}),
    ("krok-44-2", "50% 45%", "Я продовжую жити.", "", "raw", {"size": 84}),
    ("tysha-88-3", "50% 45%", "Я обираю себе»", "", "raw", {"size": 84}),
], "Улюблена сукня, шовкова хустка, червона помада — маленькі акти свободи.", (["krok-44-1"], "Колекція SOLO. Шлях до себе", ""), "Дивитися колекцію", "Small acts of freedom (no price)")

triptych("t12-one-print-look", "Хустка й твіллі одного принту", [
    ("iskra-65-2", "40% 28%", "Хустка", "«Іскра» на плечах.", "raw", {"tag": "4 800 грн", "size": 110}),
    ("iskra-tw-3", "50% 60%", "Твіллі", "Та сама «Іскра» — на сумці.", "raw", {"tag": "1 600 грн", "size": 110}),
], "Разом — 6 400 грн, доставка безкоштовна.", (["iskra-65-1", "iskra-tw-4"], "Хустка + твіллі «Іскра»", "6 400 грн"), "Зібрати образ", "One print, whole look")

triptych("t13-through-the-day", "Шовк на весь день", [
    ("puls-44-2", "42% 40%", "Ранок", "Кава й хустка на зап’ясті.", "raw"),
    ("iskra-tw-2", "50% 25%", "День", "Твіллі до ділового образу.", "raw"),
    ("zolote-44-3", "50% 22%", "Вечір", "Хустка, що ловить світло.", "raw"),
], "Одна колекція — від ранку до вечора.", (["puls-44-1", "iskra-tw-4", "zolote-44-1"], "Шовк SOLO", "від 1 600 грн"), "Обрати шовк", "Through the day")

triptych("t14-where-to-wear", "Як носити шовк", [
    ("zolote-44-2", "50% 22%", "На шиї", "", "raw", {"tag": "Хустка · 2 400 грн"}),
    ("avantiura-tw-3", "50% 40%", "У волоссі", "", "raw", {"tag": "Твіллі · 1 600 грн"}),
    ("iskra-tw-3", "50% 60%", "На сумці", "", "raw", {"tag": "Твіллі · 1 600 грн"}),
], "На шиї, у волоссі, на сумці чи зап’ясті.", (["zolote-44-1", "avantiura-tw-5", "iskra-tw-4"], "Хустки й твіллі SOLO", "від 1 600 грн"), "Обрати шовк", "Where to wear")

triptych("t15-for-whom", "Кому подарувати", [
    ("tysha-88-2", "50% 47%", "Мамі", "«Тиша всередині» — баланс і вміння чути себе.", "raw", {"size": 118, "tag": "6 600 грн"}),
    ("flirt-65-3", "35% 12%", "Подрузі", "«Флірт» — невимушена жіночність.", "raw", {"size": 100, "tag": "4 800 грн"}),
    ("krok-44-2", "50% 45%", "Собі", "«Сміливий крок» — довіра до себе.", "raw", {"size": 118, "tag": "2 400 грн"}),
], "Індивідуальне пакування. Підпишемо вашими словами.", (["tysha-88-1", "flirt-65-1", "krok-44-1"], "Хустки SOLO", "від 2 400 грн"), "Обрати подарунок", "For whom")

triptych("t16-ua-it-you", "Український преміум", [
    (f"url({HI(PP['avantiura'])})", "center/140%", "Україна", "Авторський принт і ручна обробка краю.", "raw", {"size": 104}),
    ("url(src/avantiura-88-5-2k.webp)", "70% 50%/cover", "Італія", "100% італійський шовк.", "raw", {"size": 118}),
    ("avantiura-88-2", "45% 72%", "Ви", "Хустка «Авантюра» — поясом.", "raw", {"size": 130}),
], "Український бренд Obiimy — шовкові вироби з авторськими принтами.", (["avantiura-88-1"], "Шовкова хустка «Авантюра»", "6 600 грн"), "Роздивитися", "UA · IT · You")

triptych("t17-grey-colour", "Шовкова свобода", [
    ("puls-44-4", "50% 58%", "Сірий світ", "Мода — це про гідність, про право на жіночність навіть тоді, коли світ навколо стає темно‑сірим.", "bw", {"size": 96}),
    ("puls-44-4", "50% 58%", "Ваш колір", "", "spot", {"size": 96}),
], "Для жінки краса — це спосіб зберегти себе.", (["puls-44-1"], "Колекція SOLO. Шлях до себе", ""), "Дивитися колекцію", "Grey world, your colour (no price)")

triptych("t18-twilly-three-ways", "Твіллі — три образи", [
    ("krok-tw-2", "50% 40%", "У волоссі", "Бант на хвіст чи косу.", "raw", {"size": 100}),
    ("iskra-tw-3", "50% 60%", "На сумці", "Акцент, що оживляє класику.", "raw", {"size": 100}),
    ("flirt-tw-4", "50% 72%", "На тренчі", "Бант на спинці — замість пряжки.", "raw", {"size": 100}),
], "Твіллі — у кожному з семи принтів колекції.", (["krok-tw-5", "iskra-tw-4", "flirt-tw-5"], "Шовкова твіллі", "1 600 грн"), "Обрати твіллі", "Twilly three ways")

triptych("t19-krok-path", "«Сміливий крок»", [
    ("krok-44-3", "50% 20%", "Пошук", "Сумніви й відкриття.", "bw"),
    ("krok-tw-3", "50% 40%", "Тиша", "Почути себе.", "sepia"),
    ("krok-44-2", "50% 30%", "Крок", "Бо з’являється довіра до себе.", "raw"),
], "Після пошуку й внутрішньої тиші настає момент руху вперед.", (["krok-44-1", "krok-tw-5"], "«Сміливий крок»", "від 1 600 грн"), "Зробити крок", "Krok path")


# ================================================================= PRODUCT-FIRST banners (colour of the print + the product)
SIZE = {"iskra": "65 × 65 см", "flirt": "65 × 65 см", "puls": "44 × 44 см", "zolote": "44 × 44 см", "avantiura": "88 × 88 см", "tysha": "88 × 88 см", "krok": "44 × 44 см"}
HERO = [("iskra", "iskra-65-1", "4 800 грн", "iskra-65-2", "40% 28%", "На плечах", "Накиньте на жакет — як акцент кольору."),
        ("flirt", "flirt-65-1", "4 800 грн", "flirt-65-3", "35% 28%", "На голові", "Вузол на потилиці, кінці — на плечі."),
        ("puls", "puls-44-1", "2 400 грн", "puls-44-4", "50% 22%", "На шиї", "Вузол спереду, кінці — вільно."),
        ("zolote", "zolote-44-1", "2 400 грн", "zolote-44-3", "50% 22%", "На шиї", "Вузол збоку, під жакет."),
        ("avantiura", "avantiura-88-1", "6 600 грн", "avantiura-88-5", "62% 35%", "У волоссі", "Складіть стрічкою й зав’яжіть на хвіст."),
        ("tysha", "tysha-88-1", "6 600 грн", "tysha-88-3", "50% 45%", "На голові", "Вузол на потилиці, кінці — на плечі."),
        ("krok", "krok-44-1", "2 400 грн", "krok-44-2", "50% 30%", "На шиї", "Вузол спереду, кінці — вільно.")]
for i, (pid, cut, price, ph, pos, how, line) in enumerate(HERO, 1):
    p = PP[pid]
    triptych(f"q{i:02d}-{pid}", "Шовкова хустка", [
        (cut, grad(pid), f"«{p['name']}»", "Шовкова хустка.", "cut", {"tag": SIZE[pid], "size": 96}),
        (ph, pos, how, line, "raw", {"size": 104}),
    ], p["state"].split(". ")[0].rstrip(".") + ".", ([cut], f"Хустка «{p['name']}»", price), "Обрати хустку", f"Product hero: {p['name']}")

triptych("q08-ladder", "Оберіть свій формат", [
    ("krok-tw-5", grad("krok"), "Твіллі", "Шовкова стрічка.", "cut", {"tag": "1 600 грн"}),
    ("puls-44-1", grad("puls"), "Мала", "Хустка 44 × 44.", "cut", {"tag": "2 400 грн"}),
    ("iskra-65-1", grad("iskra"), "Класична", "Хустка 65 × 65.", "cut", {"tag": "4 800 грн"}),
    ("avantiura-88-1", grad("avantiura"), "Велика", "Хустка 88 × 88.", "cut", {"tag": "6 600 грн"}),
], "Сім авторських принтів — від стрічки до великої хустки.", (["krok-tw-5", "puls-44-1", "avantiura-88-1"], "Шовк SOLO", "від 1 600 грн"), "Обрати формат", "Format ladder")

triptych("q09-twillies", "Твіллі SOLO", [
    ([(p["tw"], f"«{p['name']}»", "1 600 грн") for p in P], DARK, "Сім твіллі.", "Одна ціна — 1 600 грн.", "grid", {"size": 104, "h": 320, "gtop": 270}),
], "Шовкова твіллі — у волосся, на шию, на сумку чи зап’ястя.", ([P[0]["tw"], P[4]["tw"], P[6]["tw"]], "Шовкова твіллі", "1 600 грн"), "Обрати твіллі", "Twilly catalogue")

SC = [("iskra", "4 800"), ("flirt", "4 800"), ("puls", "2 400"), ("zolote", "2 400"), ("avantiura", "6 600"), ("tysha", "6 600"), ("krok", "2 400")]
triptych("q10-scarves", "Хустки SOLO", [
    ([(PP[i]["flat"], f"«{PP[i]['name']}»", f"{SIZE[i]} · {pr} грн") for i, pr in SC], DARK, "Сім хусток.", "Сім станів.", "grid", {"size": 104, "h": 230, "gtop": 270}),
], "Натуральний шовк, двосторонній друк, авторські принти.", (["iskra-65-1", "tysha-88-1", "krok-44-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Обрати хустку", "Scarf catalogue")

triptych("q11-double", "Двосторонній друк", [
    ("iskra-65-1", grad("iskra"), "Лицьовий бік", "Принт «Іскра».", "cut", {"size": 84}),
    ("iskra-65-5", grad("iskra", 200), "І зворот", "Такий самий яскравий.", "cut", {"size": 96}),
], "Жодного вивороту — зав’язуйте як завгодно.", (["iskra-65-1"], "Шовкова хустка «Іскра»", "4 800 грн"), "Роздивитися", "Double-sided")

triptych("q12-box", "Маленький подарунок", [
    ("src/flirt-scr-1-2k.webp", "linear-gradient(160deg,#F7C928,#EDB400)", "Резинка", "Шовкова «Флірт».", "side", {"tag": "700 грн", "at": "50% 50%"}),
    ("url(src/flirt-scr-2-2k.webp)", "0% 27%/165%", "У волоссі", "У подарунок — підпишемо вашими словами.", "raw", {"size": 104}),
], "Перше знайомство з Obiimy — у фірмовій жовтій коробочці.", (["flirt-scr-1"], "Шовкова резинка «Флірт»", "700 грн"), "Подарувати", "Yellow box")

SETS = [("avantiura", "avantiura-88-1", "6 600", "8 200"), ("tysha", "tysha-88-1", "6 600", "8 200"), ("krok", "krok-44-1", "2 400", "4 000")]
for k, (pid, cut, pr, total) in enumerate(SETS, 13):
    p = PP[pid]
    triptych(f"q{k:02d}-set-{pid}", "Хустка + твіллі одного принту", [
        (cut, grad(pid), "Хустка", f"«{p['name']}»", "cut", {"tag": f"{pr} грн", "size": 110}),
        (p["tw"], grad(pid, 200), "Твіллі", f"«{p['name']}»", "cut", {"tag": "1 600 грн", "size": 110}),
    ], "Один принт — хустка на шию, стрічка у волосся чи на сумку." + (" Доставка безкоштовна." if int(total.replace(" ", "")) >= 5000 else ""),
       ([cut, p["tw"]], f"Хустка + твіллі «{p['name']}»", f"{total} грн"), "Зібрати образ", f"Set: {p['name']}")


# ================================================================= DOWN-TO-EARTH product banners: what it is, price, how to buy
ABOUT = {"iskra": "про сміливість бути помітною", "flirt": "про мистецтво невимушеної жіночності", "puls": "про внутрішній ритм", "zolote": "про моменти ясності",
         "avantiura": "про готовність виходити за межі звичного", "tysha": "про здатність чути себе", "krok": "про довіру до себе"}
CARD = [("iskra", "65 × 65 см", "4 800 грн", "iskra-65-4", "50% 15%", "На плечах", "Яскравий акцент<br>до пальта.", {"wide": 128}),
        ("flirt", "65 × 65 см", "4 800 грн", "flirt-65-3", "35% 12%", "На голові", "Класичний спосіб носити хустку.", {}),
        ("puls", "44 × 44 см", "2 400 грн", "puls-44-5", "50% 58%", "На зап’ясті", "Замість браслета.", {"flip": True, "wide": 142, "size": 84}),
        ("zolote", "44 × 44 см", "2 400 грн", "zolote-44-3", "50% 26%", "На шиї", "Маленька хустка —<br>вузлом збоку.", {"wide": 122}),
        ("avantiura", "88 × 88 см", "6 600 грн", "avantiura-88-4", "50% 13%", "На шиї", "Класика, що не виходить<br>з моди.", {"wide": 125}),
        ("tysha", "88 × 88 см", "6 600 грн", "tysha-88-2", "50% 47%", "На плечах", "Велика хустка —<br>на плечі.", {"wide": 118}),
        ("krok", "44 × 44 см", "2 400 грн", "krok-44-2", "50% 45%", "На шиї", "Маленька хустка — на шию.", {})]
for i, (pid, size_, price, ph, pos, how, line, opt) in enumerate(CARD, 1):
    p = PP[pid]; cut = p["flat"]
    triptych(f"k{i:02d}-card-{pid}", "Шовкова хустка", [
        (cut, grad(pid), f"«{p['name']}»", "Шовкова хустка.", "cut", {"tag": size_, "size": 96}),
        ([("Матеріал", "100% натуральний шовк"), ("Друк", "двосторонній"), ("Край", "оброблений вручну"), ("Зроблено", "в Україні")], "", "", "", "spec", {"fs": 40, "lw": 300}),
        (ph, pos, how, line, "raw", {"size": 100, **opt}),
    ], f"«{p['name']}» — {ABOUT[pid]}.", ([cut], f"Хустка «{p['name']}»", price), "Купити", f"Product card: {p['name']}")

triptych("k08-card-twilly", "Шовкова твіллі", [
    (["iskra-tw-4", "avantiura-tw-5", "zolote-tw-3"], DARK, "Твіллі", "Вузька шовкова стрічка.", "cut", {"tag": "84 × 5 см · 1 600 грн", "frac": .8}),
    ([("Матеріал", "натуральний шовк"), ("Принти", "7 на вибір"), ("Як носити", "волосся, шия, сумка, зап’ястя"), ("Зроблено", "в Україні")], "", "", "", "spec", {"fs": 44, "lw": 300}),
], "Одна ціна для всіх семи принтів колекції.", (["iskra-tw-4", "avantiura-tw-5", "krok-tw-5"], "Шовкова твіллі", "1 600 грн"), "Купити", "Twilly card")

triptych("k09-card-scrunchie", "Шовкова резинка", [
    ("src/flirt-scr-1-2k.webp", "linear-gradient(160deg,#F7C928,#EDB400)", "Резинка", "Шовкова, для волосся.", "side", {"tag": "700 грн", "at": "50% 50%"}),
    ([("Матеріал", "натуральний шовк"), ("Принт", "«Флірт»"), ("Пакування", "фірмова жовта коробочка"), ("Зроблено", "в Україні")], "", "", "", "spec", {"fs": 44, "lw": 300}),
], "Маленький подарунок у фірмовій жовтій коробочці.", (["flirt-scr-1"], "Шовкова резинка «Флірт»", "700 грн"), "Купити", "Scrunchie card")

triptych("k10-sizes", "Який розмір обрати?", [
    ("puls-44-1", grad("puls"), "44 × 44", "На шию, на зап’ястя, на ручку сумки.", "cut", {"tag": "2 400 грн", "frac": .5}),
    ("iskra-65-1", grad("iskra"), "65 × 65", "На шию, на голову, на плечі.", "cut", {"tag": "4 800 грн", "frac": .72}),
    ("avantiura-88-1", grad("avantiura"), "88 × 88", "На плечі, на голову, поясом.", "cut", {"tag": "6 600 грн", "frac": .96}),
], "Що більша хустка, то більше способів її зав’язати.", (["puls-44-1", "iskra-65-1", "avantiura-88-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Обрати розмір", "Which size")

triptych("k11-what-is-twilly", "Що таке твіллі?", [
    ("krok-tw-5", grad("krok"), "Твіллі", "Вузька шовкова стрічка.", "cut", {"tag": "1 600 грн", "frac": .86}),
    ("avantiura-tw-3", "50% 40%", "У волосся", "Бантом на хвіст чи косу.", "raw"),
    ("iskra-tw-3", "50% 60%", "На сумку", "Обвийте ручку або зав’яжіть бантом.", "raw"),
], "Сім принтів, одна ціна — 1 600 грн.", (["krok-tw-5", "avantiura-tw-5", "iskra-tw-4"], "Шовкова твіллі", "1 600 грн"), "Обрати твіллі", "What is a twilly")

triptych("k12-how-to-order", "Як замовити", [
    ("iskra-65-1", grad("iskra"), "1", "Оберіть принт<br>на obiimy.world.", "cut", {"size": 150, "frac": .7}),
    ("zolote-44-1", grad("zolote"), "2", "Оплатіть карткою або частинами.", "cut", {"size": 150, "frac": .7}),
    ("krok-44-1", grad("krok"), "3", "Замовте до 16:00 — відправимо Новою поштою того ж дня.", "cut", {"size": 150, "frac": .7}),
], "Від 5 000 грн доставка по Україні безкоштовна.", (["iskra-65-1", "zolote-44-1", "krok-44-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Замовити", "How to order")

triptych("k13-prices", "Ціни колекції", [
    ([("Резинка для волосся", "700 грн", "flirt-scr-1"), ("Твіллі", "1 600 грн", "iskra-tw-4"), ("Хустка 44 × 44", "2 400 грн", "puls-44-1"),
      ("Хустка 65 × 65", "4 800 грн", "flirt-65-1"), ("Хустка 88 × 88", "6 600 грн", "tysha-88-1")], "", "Скільки коштує SOLO", "", "spec", {"size": 84, "fs": 50, "lw": 400}),
], "Натуральний шовк, авторські принти, двосторонній друк хусток.", (["flirt-scr-1", "iskra-tw-4", "tysha-88-1"], "Шовкові вироби SOLO", "від 700 грн"), "До каталогу", "Price list")

triptych("k14-budget", "Подарунок за бюджетом", [
    ("src/flirt-scr-1-2k.webp", "linear-gradient(160deg,#F7C928,#EDB400)", "До 1 000", "Резинка «Флірт» у жовтій коробочці.", "side", {"tag": "700 грн", "at": "50% 50%", "gap": 36}),
    ("zolote-tw-3", grad("zolote"), "До 2 000", "Шовкова твіллі, 7 принтів.", "cut", {"tag": "1 600 грн", "frac": .86, "gap": 36}),
    ("krok-44-1", grad("krok"), "До 3 000", "Шовкова хустка 44 × 44.", "cut", {"tag": "2 400 грн", "frac": .8, "gap": 36}),
    ("iskra-65-1", grad("iskra"), "До 5 000", "Шовкова хустка 65 × 65.", "cut", {"tag": "4 800 грн", "frac": .86, "gap": 36}),
], "Підпишемо вашими словами. Не певні — сертифікат від 1 000 грн.", (["flirt-scr-1", "zolote-tw-3", "iskra-65-1"], "Шовкові вироби SOLO", "від 700 грн"), "Обрати подарунок", "Gift by budget")

triptych("k15-scarves-44", "Хустки 44 × 44 см", [
    ("puls-44-1", grad("puls"), "«Пульс»", "Графічні іриси на зеленому.", "cut", {"tag": "2 400 грн"}),
    ("zolote-44-1", grad("zolote"), "«Золоте світло»", "Карамельна, з геометрією.", "cut", {"tag": "2 400 грн"}),
    ("krok-44-1", grad("krok"), "«Сміливий крок»", "Літерний візерунок, бордова кайма.", "cut", {"tag": "2 400 грн"}),
], "Маленька шовкова хустка: на шию, зап’ястя чи сумку.", (["puls-44-1", "zolote-44-1", "krok-44-1"], "Хустка 44 × 44", "2 400 грн"), "Обрати принт", "Scarves 44")

triptych("k16-scarves-65", "Хустки 65 × 65 см", [
    ("iskra-65-1", grad("iskra"), "«Іскра»", "Великий синій горошок, помаранчева кайма.", "cut", {"tag": "4 800 грн", "frac": .8}),
    ("flirt-65-1", grad("flirt"), "«Флірт»", "Дрібний горошок, оливкова кайма.", "cut", {"tag": "4 800 грн", "frac": .8}),
], "Класичний розмір: на шию, на голову, на плечі.", (["iskra-65-1", "flirt-65-1"], "Хустка 65 × 65", "4 800 грн"), "Обрати принт", "Scarves 65")

triptych("k17-scarves-88", "Хустки 88 × 88 см", [
    ("avantiura-88-1", grad("avantiura"), "«Авантюра»", "Білі іриси на бордовому.", "cut", {"tag": "6 600 грн", "frac": .8}),
    ("tysha-88-1", grad("tysha"), "«Тиша всередині»", "Графічні іриси на білому.", "cut", {"tag": "6 600 грн", "frac": .8}),
], "Велика хустка: на плечі, на голову, поясом. Оплата частинами — ПриватБанк, monobank.", (["avantiura-88-1", "tysha-88-1"], "Хустка 88 × 88", "6 600 грн"), "Обрати принт", "Scarves 88")

triptych("k18-delivery-payment", "Доставка й оплата", [
    ([("Нова пошта", "відправка в день замовлення до 16:00"), ("Безкоштовно", "від 5 000 грн"), ("За кордон", "за тарифами перевізника"),
      ("Оплата", "карткою Visa / Mastercard"), ("Частинами", "ПриватБанк — 4, monobank — 3"), ("Подарунок", "підпишемо вашими словами"), ("Сертифікат", "1 000–4 000 грн, діє 3 місяці"), ("Шоурум", "Київ, вул. П. Сагайдачного, 12")], "", "", "", "spec", {"fs": 32, "lw": 280}),
    (["puls-44-1", "avantiura-tw-5"], DARK, "Хустки й твіллі", "Сім авторських принтів.", "cut", {"tag": "від 1 600 грн", "frac": .62, "size": 80}),
], "Замовляйте на obiimy.world або приходьте приміряти в шоурум.", (["puls-44-1", "avantiura-tw-5"], "Шовкові вироби SOLO", "від 1 600 грн"), "Замовити", "Delivery and payment")

# ───────── one look, one photo: a single large frame, the print, its state and the price
ONE = [("iskra", "iskra-65-2", "38% 50%", "Хустка", "65 × 65 см", "4 800 грн", "iskra-65-1", "Накиньте на жакет — як акцент кольору."),
       ("flirt", "flirt-65-3", "36% 50%", "Хустка", "65 × 65 см", "4 800 грн", "flirt-65-1", "На голові: вузол на потилиці, кінці — на плечі."),
       ("puls", "puls-44-4", "50% 50%", "Хустка", "44 × 44 см", "2 400 грн", "puls-44-1", "На шиї: вузол спереду, кінці — вільно."),
       ("zolote", "zolote-44-3", "50% 50%", "Хустка", "44 × 44 см", "2 400 грн", "zolote-44-1", "На шиї: вузол збоку, під жакет."),
       ("avantiura", "avantiura-88-5", "62% 50%", "Хустка", "88 × 88 см", "6 600 грн", "avantiura-88-1", "У волоссі: складіть стрічкою й зав’яжіть на хвіст."),
       ("tysha", "tysha-88-2", "50% 50%", "Хустка", "88 × 88 см", "6 600 грн", "tysha-88-1", "Велика хустка — на плечі."),
       ("krok", "krok-44-2", "50% 50%", "Хустка", "44 × 44 см", "2 400 грн", "krok-44-1", "На шиї: великий бант збоку."),
       ("iskra", "iskra-tw-2", "50% 50%", "Твіллі", "", "1 600 грн", "iskra-tw-4", "Твіллі на шиї — під жакет."),
       ("avantiura", "avantiura-tw-3", "50% 50%", "Твіллі", "", "1 600 грн", "avantiura-tw-5", "Твіллі у волоссі — бантом на хвіст."),
       ("flirt", "flirt-tw-1", "50% 50%", "Твіллі", "", "1 600 грн", "flirt-tw-5", "Твіллі у волоссі — навколо пучка.")]
for i, (pid, ph, pos, kind, size_, price, cut, how) in enumerate(ONE, 1):
    p = PP[pid]
    triptych(f"s{i:02d}-{'twilly' if kind == 'Твіллі' else 'scarf'}-{pid}", f"Шовкова {'твіллі' if kind == 'Твіллі' else 'хустка'}", [
        (ph, pos, f"«{p['name']}»", p["short"] + ".", "one", {"size": 120 if len(p["name"]) <= 9 else 92, "tag": size_ or "84 × 5 см", "lift": pid in ("iskra", "tysha") and kind == "Хустка" or (pid == "flirt" and kind == "Твіллі")}),
    ], how, ([cut], f"{kind} «{p['name']}»", price), "Обрати твіллі" if kind == "Твіллі" else "Обрати хустку", f"One look: {p['name']} {kind}")

# ───────── gifts: every banner answers a giver's question
CERT = f'''<div style="position:absolute;inset:0;background:url({HI(PP['zolote'])}) center/130%"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(12,9,8,.94) 0%,rgba(12,9,8,.9) 55%,rgba(12,9,8,.84) 100%)"></div>
    <div style="position:absolute;right:64px;top:50%;transform:translateY(-50%);width:400px;text-align:right;color:#F3EADB">
      <p style="font-family:Onest;font-weight:600;font-size:24px;letter-spacing:.14em;text-transform:uppercase;color:#E0B040">Номінали, грн</p>
      <p style="font-family:'Playfair Display',serif;font-weight:700;font-size:72px;line-height:1.08;margin-top:14px">1 000<br>1 500<br>2 000<br>2 500<br>4 000</p></div>'''
triptych("g01-certificate", "Подарунковий сертифікат", [
    (["iskra-65-1", "avantiura-88-1", "puls-44-1"], DARK, "Який принт її?", "Сім принтів — і не треба вгадувати.", "cut", {"size": 84, "frac": .6}),
    (CERT, "#141110", "Нехай обере сама", "Сертифікат у подарунок.", "html", {"size": 84, "tw": 500}),
], "На будь-який товар. Електронний або фізичний. Діє 3 місяці.", ([], "Сертифікат Obiimy", "від 1 000 грн"), "Подарувати", "Gift certificate")

triptych("g02-no-worries", "Подарунок без клопоту", [
    (["flirt-scr-1", "iskra-tw-4", "tysha-88-1"], DARK, "Шовк у\u00a0подарунок", "Резинка, твіллі або хустка.", "cut", {"tag": "від 700 грн", "frac": .6, "size": 70}),
    ([("Підпис", "вашими словами"), ("Відправка", "у день замовлення до 16:00"), ("Доставка", "безкоштовно від 5 000 грн"),
      ("Оплата", "карткою або частинами"), ("Пакування", "індивідуальне"), ("Не певні", "сертифікат від 1 000 грн")], "", "", "", "spec", {"fs": 38, "lw": 290}),
], "Оберіть — підпишемо й відправимо.", (["flirt-scr-1", "iskra-tw-4", "tysha-88-1"], "Шовкові вироби SOLO", "від 700 грн"), "Обрати подарунок", "Answers for the giver")

triptych("g03-pair-flirt", "Подарунок із двох речей", [
    ("flirt-65-1", grad("flirt"), "Хустка", "«Флірт» · 65 × 65 см", "cut", {"tag": "4 800 грн", "size": 110}),
    ("src/flirt-scr-1-2k.webp", "linear-gradient(160deg,#F7C928,#EDB400)", "Резинка", "«Флірт» — у жовтій коробочці.", "side", {"tag": "700 грн", "at": "50% 50%"}),
], "Хустка й резинка одного принту. Разом — 5 500 грн, доставка безкоштовна.", (["flirt-65-1", "flirt-scr-1"], "Хустка + резинка «Флірт»", "5 500 грн"), "Подарувати", "Scarf + scrunchie")

triptych("g04-no-size", "Шовкова хустка в подарунок", [
    ("puls-44-2", "50% 36%", "Не треба знати її\u00a0розмір", "Шовкова хустка «Пульс» у подарунок.", "raw", {"size": 78, "wide": 158, "gap": 34, "veil": "linear-gradient(90deg,rgba(12,9,8,.92) 0%,rgba(12,9,8,.8) 50%,rgba(12,9,8,.35) 66%,rgba(12,9,8,0) 84%)"}),
    ("puls-44-1", grad("puls"), "«Пульс»", "Шовкова хустка.", "cut", {"tag": "2 400 грн", "size": 100}),
], "Індивідуальне пакування. Підпишемо вашими словами.", (["puls-44-1"], "Шовкова хустка «Пульс»", "2 400 грн"), "Обрати подарунок", "No size needed")

triptych("g06-twilly-gift", "Твіллі в подарунок", [
    ("iskra-tw-3", "50% 70%", "На сумку", "Твіллі «Іскра».", "raw", {"size": 104}),
    ("krok-tw-2", "50% 35%", "У волосся", "Твіллі «Сміливий крок».", "raw", {"size": 104}),
    (["iskra-tw-4", "krok-tw-5", "zolote-tw-3"], DARK, "У\u00a0подарунок", "Сім принтів, одна ціна.", "cut", {"tag": "1 600 грн", "frac": .78, "size": 70}),
], "Твіллі в подарунок — підпишемо вашими словами.", (["iskra-tw-4"], "Шовкова твіллі SOLO", "1 600 грн"), "Подарувати", "Twilly as a gift")

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · SOLO triptych</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=EB+Garamond:wght@500;600&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Oswald:wght@500&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("solo7.html" if YELLOW else "solo6.html")).write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "triptych banners", "(yellow)" if YELLOW else "")
