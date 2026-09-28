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

def band(top, height, b):
    photo, pos, big, small, look = b[:5]
    extra = b[5] if len(b) > 5 else {}
    size = extra.get("size", 118 if len(big) <= 8 else 84)
    tag = f'<p class="tag">{extra["tag"]}</p>' if extra.get("tag") else ""
    if look == "spot":
        pic = spot_photo(photo, pos, style="position:absolute;inset:0")
    elif photo.startswith("url("):
        pic = f'<div style="position:absolute;inset:0;background:{photo} {pos}"></div>'
    else:
        pic = f'<img src="{S(photo)}" alt="" style="object-position:{pos};{FILTERS[look]}">'
    return f'''
  <div class="band" style="top:{top}px;height:{height}px">{pic}<div class="veil"></div>
    <div class="txt"><p class="big" style="font-size:{size}px">{big}</p><p class="small">{nb(small)}</p>{tag}</div></div>'''

def triptych(id, kicker, bands, tagline, product, cta, note=""):
    """bands: 3 × (photo, object-position, big label, small line, look[, {tag, size}]); product: (cutouts, title, price)."""
    top, h, gap = 280, 406, 12
    body = "".join(band(top + k * (h + gap), h, b) for k, b in enumerate(bands))
    cuts, title, price = product
    thumbs = "".join(f'<img src="{CUT(c)}" alt="" style="height:118px;width:auto;max-width:124px;object-fit:contain;margin-left:{0 if i == 0 else -44}px;filter:drop-shadow(0 8px 10px rgba(0,0,0,.4));transform:rotate({(-6, 5, -3)[i]}deg)">' for i, c in enumerate(cuts))
    plate_bg = "#F2B705" if YELLOW else "rgba(243,234,219,.1)"
    plate_fg = "#141216" if YELLOW else "#F3EADB"
    plate_bd = "none" if YELLOW else "1.5px solid rgba(243,234,219,.3)"
    y0 = top + 3 * h + 2 * gap
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

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · SOLO triptych</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Oswald:wght@500&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("solo7.html" if YELLOW else "solo6.html")).write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "triptych banners", "(yellow)" if YELLOW else "")
