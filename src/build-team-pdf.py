#!/usr/bin/env python3
"""HR deck «Подарунки для команди», v4 (04.10.2026) — team-deck.html (A4 landscape) → obiimy-podarunky-dlia-komandy.pdf.

System agreed with three reviewers (presentation expert, sales lead, designer):
- grid: 12 columns × 16.5 mm, 6 mm gutters, 16.5 mm margins; photo block is 148.5 mm (half page) or 297 mm; 3 mm between photos;
- four templates: frame (full-bleed photo, bottom gradient only), split (photo + paper panel), strip (header + tiles to the edge),
  sheet (running head, rule, table);
- seven type sizes: 54/54, 40/42, 28/30, 13/16.5 (Playfair), 9.5 pt / 4.5 mm, 8 pt / 3.75 mm, 7 pt caps (Tenor); nothing below 8 pt;
- paper #F1EFEA, dark #0E0E0E only for the SOLO section and the last page, accent #E7D9A6 only on dark;
- client rule: no «product in a white rectangle» — products are transparent cut-outs (img/cut, src/cutout.py) sitting on the page;
- no frame is used twice; the build checks duplicates, overflow and collisions with the folio.
Facts: review/SITE-FACTS.md, review/SOLO-RELEASE.md; retail prices from obiimy.world; what is unknown is «у розрахунку»."""
import importlib.util, json, os, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
sys.path.insert(0, str(ROOT))
from imgs import typo
from PIL import Image
_spec = importlib.util.spec_from_file_location("main", ROOT / "build-b2b-team-main.py")
main = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(main)
SOLO, qr_svg, team = main.SOLO, main.qr_svg, main.team
ARGS, RANGE, RANGE_MORE, ASK, STEPS, TERMS, EXAMPLE, INTRO = main.ARGS, main.RANGE, main.RANGE_MORE, main.ASK, main.STEPS, main.TERMS, main.EXAMPLE, main.INTRO
COVER_CAP = "Корпоративні подарунки 2026 · український бренд шовкових хусток і аксесуарів"
COVER_H1 = "Подарунки<br>для команди —<br><i>шовк, який носять</i>"                      # the cold-buyer test: the headline must name the material
COVER_PRICE = "Чотири варіанти подарунка — від 1 600 до 3 600 грн на людину"           # «чотири подарунки на людину» read as four gifts each
PHONE, PHONE_HREF, MAIL, SHOWROOM = team.PHONE, team.PHONE_HREF, team.MAIL, team.SHOWROOM
TG = "https://t.me/OBIIMY_sales"
COVER_LINE = (f'<p class="folio"><span>Пакування й наліпка з вашим логотипом — у ціні</span>'
              f'<span><a href="https://obiimy.world/">obiimy.world</a> · <a href="{PHONE_HREF}">{PHONE}</a> · <a href="{TG}">Telegram @OBIIMY_sales</a></span></p>')   # shared with the landing
LANDING = "https://obiimy-landing-production.up.railway.app/b2b-team-main"
LB = OUT / "review" / "lb"; LB.mkdir(parents=True, exist_ok=True)
USED = []   # model shots, to prove no frame repeats

def pic(src, w, h, pos="50% 50%", cls="", hi=False, once=True, zoom=1.0, box=None):
    """Photo cropped to its slot (w × h mm, object-position pos, optional zoom) and exported at 200 ppi — exact framing, small file.
    hi=True takes the 2400 px master of a SOLO frame for full-bleed pages."""
    p = pathlib.Path(src); srcp = OUT / src
    k2 = OUT / "ads" / "solo" / "src" / (p.stem + "-2k.webp")
    if hi and k2.exists(): srcp = k2
    px, py = [float(v.strip("%")) / 100 for v in pos.split()]
    j = LB / f"{p.stem}-{int(w * 10)}x{int(h * 10)}-{int(px * 100)}-{int(py * 100)}-z{int(zoom * 100)}{'-2k' if srcp == k2 else ''}.jpg"
    if box: j = LB / f"{p.stem}-{int(w * 10)}x{int(h * 10)}-box{'-'.join(map(str, box))}.jpg"        # box=(x0, y0, x1, y1) in source pixels
    if not j.exists() or j.stat().st_mtime < srcp.stat().st_mtime:
        im = Image.open(srcp).convert("RGB"); W, H = im.size
        cw, ch = (W, W * h / w) if W * h / w <= H else (H * w / h, H)          # object-fit: cover
        cw, ch = cw / zoom, ch / zoom
        x0, y0 = (W - cw) * px, (H - ch) * py
        im = im.crop(box if box else (round(x0), round(y0), round(x0 + cw), round(y0 + ch)))
        if box: cw, ch = im.size
        tw = round(w / 25.4 * 200)
        if im.width > tw: im = im.resize((tw, round(tw * ch / cw)), Image.LANCZOS)
        im.save(j, quality=84, optimize=True, progressive=True)
    if once: USED.append(src)
    return f'<img src="review/lb/{j.name}" class="{cls}" alt="" data-src="{src}">'

def cut(name, mm=46, cls="", fix=False):
    """Transparent cut-out → PNG with alpha, sized for its slot (mm on the long side, 220 ppi); refreshed when the cut-out changes.
    fix=True writes the size in mm into the tag: without it the picture takes whatever the CSS of its slot allows."""
    px = round(mm / 25.4 * (220 if mm <= 60 else 170)); srcp = OUT / "img" / "cut" / f"{name}.webp"      # large cut-outs at 170 ppi: PNG with alpha is heavy in a PDF
    j = LB / f"cut-{name}-{px}.png"
    if not j.exists() or j.stat().st_mtime < srcp.stat().st_mtime:
        im = Image.open(srcp).convert("RGBA"); im.thumbnail((px, px), Image.LANCZOS); im.save(j, optimize=True)
    st = ""
    if fix:
        w, h = Image.open(j).size; k = mm / max(w, h); st = f' style="width:{w * k:.1f}mm;height:{h * k:.1f}mm"'
    return f'<img src="review/lb/{j.name}" class="{cls}" alt="" data-src="img/cut/{name}.webp"{st}>'

def cutsh(name, w_mm, layers=((0.6, 0.5, 0.20), (3.2, 4.0, 0.16)), tint=(30, 22, 8), ppi=170):
    """A large cut-out with its shadow baked into the PNG: (file, pad_mm, height_mm). A CSS drop-shadow makes Chrome rasterise
    the whole element at ~300 dpi into the PDF (4–5 MB per page with big objects); a baked shadow keeps our resolution.
    layers: (offset down mm, blur mm, opacity); the picture is padded on all sides by pad_mm so that it can be turned around its centre."""
    from PIL import ImageFilter
    srcp = OUT / "img" / "cut" / f"{name}.webp"; k = ppi / 25.4
    pad_mm = max(dy + 2.5 * bl for dy, bl, _a in layers); pad = round(pad_mm * k)
    j = LB / f"cutsh-{name}-{round(w_mm * 10)}-{ppi}-{abs(hash(layers + tint)) % 9973}.png"
    im = Image.open(srcp).convert("RGBA"); w = round(w_mm * k)
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    if not j.exists() or j.stat().st_mtime < srcp.stat().st_mtime:
        out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
        for dy, bl, al in layers:
            sh = Image.new("L", out.size, 0); sh.paste(im.getchannel("A").point(lambda v: int(v * al)), (pad + round(dy * k / 2), pad + round(dy * k)))
            lay = Image.new("RGBA", out.size, tint + (0,)); lay.putalpha(sh.filter(ImageFilter.GaussianBlur(bl * k / 2))); out = Image.alpha_composite(out, lay)
        out.alpha_composite(im, (pad, pad)); out.save(j, optimize=True)
    return j.name, pad / k, im.height / k

def money(n): return f"{n:,}".replace(",", " ")
PAGES = []
TERMS_P = 16   # the page with terms and the sample quote — page 3 refers to it; checked after the pages are built
def page(html, cls, folio=True, short=False):
    n = len(PAGES) + 1
    tg = "@OBIIMY_sales" if short else "Telegram @OBIIMY_sales"      # short=True — a folio that fits a narrow panel
    f = (f'<p class="folio"><span></span><span>{n:02d}</span></p>' if folio else "")   # 07.10: the page number only — the contacts are on the last page
    PAGES.append(f'<section class="pg {cls}">{html}{f}</section>')
def rh(section): return f'<p class="rh"><span>{section}</span><span>Obiimy · Подарунки для команди · 2026</span></p>'

# ── 1 · cover (frame) ───────────────────────────────────────────────────────────────────────────────
page(f"""{pic("photo/solo/zolote-44-2.webp", 297, 210, "50% 24%", "bg", hi=True)}<img src="brand/logo-white.png" class="logo" alt="Obiimy">
<div class="fr-t"><p class="cap">{COVER_CAP}</p>
<h1 class="h54">{COVER_H1}</h1>
<div class="chip">{cut("zolote-44-1", 13)}<div><span>Чотири варіанти подарунка · на людину</span><em>від 1 600 до 3 600 грн</em></div></div></div>
{COVER_LINE}""", "frame", folio=False)

# ── 2 · who we are: the «Про нас» text of obiimy.world, word for word (the client, 07.10); the «Іскра» photo on the left half ─────
# 07.10, second pass: no caption on the photo, no kicker, no headline — the text alone, as on the site.
ABOUT_LEAD = "Obiimy — український бренд натуральних шовкових виробів з авторськими принтами художниці та засновниці Світлани Сніжко. Ми створюємо речі, що поєднують красу, мистецтво та турботу — і дарують емоції з першого дотику."
ABOUT_LIST = ["шовкові хустки та твіллі;", "резинки та маски для сну;", "аксесуари для дому й догляду;", "витончені прикраси."]
ABOUT = ["Усі вироби — зі 100% натурального шовку преміум-⁠класу: ніжний блиск, м’яка текстура, вишуканість у кожному образі.",
         "Obiimy — це про любов до себе, до природи, до людей. Кожна коробочка — це обійми, що нагадують: ти варта краси.",
         "Шовк м’який і дбайливий до шкіри, не викликає подразнень — саме тому з нього виходять найкращі маски для сну.",
         "«Обійми» були засновані в часи війни. Бренд бере участь у благодійних ініціативах на допомогу військовим і тим, хто постраждав від конфлікту, — і кожен, хто обирає «Обійми», стає частиною цієї місії.",
         "Ми створюємо не просто аксесуари, а спосіб виразити власну індивідуальність та почуття. Дозволь собі насолоджуватися любов’ю та вишуканістю разом з «Обійми»."]   # 07.10: shortened at the client's request
about = f'<p class="ab-lead">{ABOUT_LEAD}</p>' + "".join(f"<p>{x}</p>" for x in ABOUT)   # the list of categories is no longer printed (07.10)
page(f"""<figure class="ph">{pic("photo/solo/iskra-65-2.webp", 148.5, 210, "44% 0%", hi=True)}</figure>
<div class="panel ab"><div class="ab-t">{about}</div></div>""", "split l about")

# ── 3 · scarves: three sizes nested one in another (scale), the price from 1 600, six looks to the edge ─────────────────
W6 = [("На сумці", "photo/solo/iskra-65-3.webp", "50% 50%"), ("На голові", "photo/site/khustka-spokusa-44x44-02.jpg", "50% 0%"), ("На шиї", "photo/site/khustka-potsilunok-sontsia-44x44-02.jpg", "50% 0%"),
      ("На плечах", "photo/site/khustka-vidnovlennia-88x88-02.jpg", "50% 15%"), ("Поясом", "photo/solo/avantiura-88-2.webp", "50% 40%"), ("Топом", "photo/site/khustka-balans-44x44-04.jpg", "50% 0%")]   # 07.10: SOLO frames and site editorials, different women and ages
tiles6 = "".join(f'<figure class="w6">{pic(f, 61.5, 103.5, ps, hi=True)}<figcaption class="h28"><i>{n}</i></figcaption></figure>' for n, f, ps in W6)
NEST = [("avantiura-88-1", 44, "88 × 88", 4400), ("iskra-65-1", 32.5, "65 × 65", 3200), ("zolote-44-1", 22, "44 × 44", 1600)]   # mm on the long side = cm / 2 → true proportions; prices from the listing (05.10)
nest = ("".join(f'<figure class="n{i}">{cut(c, mm, fix=True)}</figure>' for i, (c, mm, n, pz) in enumerate(NEST))
        + '<div class="nl">' + "".join(f'<p><b class="h13">{n}</b><span class="t8">від {money(pz)} грн</span></p>' for c, mm, n, pz in NEST) + '</div>')
page(f"""<div class="panel"><h2 class="h28">Хустки</h2>
<span class="from">від 1 600 грн</span>
<p class="lead">Хустка — подарунок, який носять по-різному: на шиї, на голові, на сумці, поясом чи топом. Одна річ — багато образів, тому вона підходить і тим, кого ви знаєте добре, і тим, кого — ще ні.</p>
<p class="lead">Три розміри: маленька — на шию й на сумку, середня — на голову й на плечі, велика — як шаль. Принт один на всю команду або кожному свій.</p>
<div class="nest">{nest}</div></div>
<div class="w6g">{tiles6}</div>""", "ways6", short=True)

# ── 4 · twillies: the price from 1 600, four looks to the edge ─────────────────────────────────────────
WAYS = [("У волоссі", "photo/solo/krok-tw-2.webp", "50% 30%", 1.0), ("На шиї", "photo/solo/flirt-tw-3.webp", "50% 15%", 1.0), ("На сумці", "photo/solo/iskra-tw-3.webp", "50% 50%", 1.0),   # SOLO campaign frames and one editorial frame from the site (07.10)
        ("На зап’ясті", "photo/solo/krok-tw-3.webp", "50% 35%", 1.0), ("Краваткою", "photo/solo/avantiura-tw-4.webp", "50% 15%", 1.0), ("Бантом", "photo/solo/puls-tw-1.webp", "50% 45%", 1.0)]
tiles4 = "".join(f'<figure class="w6">{pic(f, 61.5, 103.5, ps, hi=True, zoom=z)}<figcaption class="h28"><i>{n}</i></figcaption></figure>' for n, f, ps, z in WAYS)
PAIR = [("photo/paris-dots.jpg", "50% 30%"), ("photo/paris-bag.jpg", "50% 50%")]   # scarf and twilly of one print — the pair from the c18 banner
pair = "".join(f'<figure>{pic(f, 40.5, 50, ps)}</figure>' for f, ps in PAIR)
TW4 = [("tw-flat-sokovyti-spohady", "«Соковиті спогади»"), ("tw-flat-melodiia-dvokh", "«Мелодія двох»"), ("tw-flat-yednannia", "«Єднання»"), ("tw-flat-pidnesennia", "«Піднесення»")]   # the prints worn on the four photographs
prints4 = "".join(f'<figure>{cut(c, 27, fix=True)}</figure>' for c, n in TW4)
page(f"""<div class="panel"><h2 class="h28">Твіллі</h2>
<span class="from">від 1 600 грн</span>
<p class="lead">Твіллі — вузька шовкова стрічка. Її зав’язують у волоссі, на шиї, на зап’ясті, краваткою або на ручці сумки — і носять щодня.</p>
<p class="lead">Найдоступніший подарунок у каталозі й найлегший у виборі: підходить усім, хто носить аксесуари. Десятки авторських принтів — один на всю команду або кожному свій.</p>
<div class="pair">{pair}</div>
<p class="pair-cap">Твіллі добре працює в парі: хустка й твіллі одного принту — на плечах і на сумці.</p></div>
<div class="w6g">{tiles4}</div>""", "ways6", short=True)

# ── 5 · accessories: sleep masks, scrunchies, bookmarks, pillowcases, turbans — the things for everyone ───────────────
ACC4 = [("Маска для сну", "від 2 700 грн", "photo/site/mask-vpevnenist-04.jpg", "50% 25%"), ("Резинка", "від 700 грн", "photo/site/mask-shchyri-pochuttia-04.jpg", "0% 15%", 1.6),
        ("Закладка", "від 800 грн", "photo/site/bookmark-melodiia-dvokh-01.jpg", "55% 30%"), ("Тримач для хустки", "від 450 грн", "photo/site/ring-zoloto-01.jpg", "50% 40%")]   # four things, the price in the caption
tilesA = "".join(f'<figure class="w6">{pic(t[2], 93.75, 103.5, t[3], zoom=(t[4] if len(t) > 4 else 1.0))}<figcaption class="h28"><i>{t[0]}</i><span class="wp">{t[1]}</span></figcaption></figure>' for t in ACC4)
page(f"""<div class="panel"><h2 class="h28">Аксесуари</h2>
<span class="from">від 700 грн</span>
<p class="lead">Речі з того самого шовку — для тих, хто хустки не носить, і для подарунка «про відпочинок»: маска для сну, резинка для волосся, закладка для книги, тримач для хустки.</p>
<p class="lead">Шовк м’який і дбайливий до шкіри, тому маска для сну з нього — одна з найкращих. Резинка — найпростіший знак уваги на всю команду. Тримач — маленьке кільце, яке тримає хустку чи твіллі й робить із них готовий образ.</p>
<figure class="setcut">{cut("box-maskscr-melodiia", 64, fix=True)}</figure>
<p class="pair-cap">Кілька аксесуарів чудово складаються в набір — наприклад, маска для сну й резинка одного принту в коробці.</p></div>
<div class="w6g w4g">{tilesA}</div>""", "ways6", short=True)

# ── 6 · gift sets: three columns, one open box per set (the shop's own cut-outs on the paper), the words and the price under it ──
SETS3 = [  # name, inside, price line, box cut-out, width mm
    ("Твіллі + хустка", "Стрічка й маленька хустка в одному принті, у довгій коробці. Разом або окремо — на шиї, у волоссі, на сумці.", "від 3 200 грн", "box-sctw-spokusa", 84),
    ("Твіллі + резинка", "Дві речі в одному принті, у святковій коробці. Найпростіший набір для всієї команди.", "від 2 200 грн", "box-twscr-smilyvist", 82),
    ("Маска + резинка", "Подарунок про відпочинок, а не про роботу. Підходить і тим, хто хустки не носить.", "від 3 100 грн", "box-maskscr-litnie-pole", 78),
]
cols = "".join(f'<div class="scol"><figure>{cut(c, w, fix=True)}</figure><h3 class="h28">{n}</h3><p>{d}</p><span class="from">{pz}</span></div>' for n, d, pz, c, w in SETS3)
page(f"""<div class="setsp"><div class="sh2"><h2 class="h28">Подарункові набори</h2><p class="brand-note">Разом із вами підберемо або створимо<br>унікальний набір саме для вашої команди.</p></div><div class="scols">{cols}</div></div>""", "sets3", short=True)

# ── 7 · the offer (sheet): four gifts, price per person, budgets ────────────────────────────────────
GIFTS = [  # label, name, description, price, ceiling (double-sided print) or None, cut-out
    ("Знак уваги", "Твіллі", "Шовкова стрічка 84 × 5: на шию, у волосся, на сумку. 38 принтів.", 1600, None, "krok-tw-1"),
    ("Тим, хто носить аксесуари", "Хустка й кільце", "Хустка 44 × 44 і кільце для хустки Gold. Збираємо під замовлення.", 2050, 2850, "duo-hratsiia-ring"),
    ("Для відпочинку", "Маска для сну й резинка", "Один принт, фірмове пакування Obiimy. Підходить і тим, хто не носить хустки.", 3100, None, "maskscr-litnie-pole"),
    ("Ключовим людям", "Хустка й твіллі в коробці", "Один принт, святкова коробка. Майстер-клас від засновниці — окремо, за бажанням.", 3200, 3600, "set-natkhnennia-box"),
]
def pr(p, frm, big="h28"): return f'<span class="pv {big}">{"<small>від</small> " if frm else ""}{money(p)} <small>грн</small></span>'
def prt(p, hi):   # «від» in its own slot: the figures share one vertical; the ceiling under the figure
    top = f'<span class="t8">до {money(hi)} грн</span>' if hi else ""
    return f'<span class="pt h28"><small>{"від" if hi else ""}</small><span>{money(p)}</span><small>грн</small>{top}</span>'
def bud(p, hi, n): return money(p * n) + (f"–{money(hi * n)}" if hi else "")
def gift_row(i, G):
    lb, n, d, p, hi, c = G
    return (f'<div class="gr"><b class="num">0{i + 1}</b>{cut(c, 23, "th")}<div><p class="cap">{lb}</p><h3 class="h13">{n}</h3><p>{d}</p></div>'
            f'{prt(p, hi)}<span class="bd">{bud(p, hi, 20)}</span><span class="bd">{bud(p, hi, 50)}</span><span class="bd">{bud(p, hi, 100)}</span></div>')
rows = "".join(gift_row(i, G) for i, G in enumerate(GIFTS))
page(f"""{rh("Чотири подарунки")}<div class="sheet">
<div class="hd"><h2 class="h28">Що в коробці — <i>і скільки це коштує</i></h2><p>Базові роздрібні ціни obiimy.world на людину, без акцій сайту, жовтень 2026; «від — до» — друк з одного чи з двох боків. Бюджети команди — у гривнях. Пакування й наліпка — безкоштовно.</p></div>
<div class="gt"><div class="gr head"><span></span><span></span><span class="cap">Подарунок</span><span class="cap">На людину</span><span class="cap bd">20 людей</span><span class="cap bd">50 людей</span><span class="cap bd">100 людей</span></div>{rows}</div>
<div class="three"><div><p class="cap">Змішана команда</p><p>Тим, хто не носить аксесуари, — маска для сну (2 700 грн), закладка для книги (800 грн), наволочка (від 4 200 грн) або сертифікат на 1 000–4 000 грн. Усе — в одному розрахунку.</p></div>
<div><p class="cap">До 1 000 грн на людину</p><p>Шовкова резинка — 700 грн, закладка для книги — 800 грн, сертифікат Obiimy — 1 000 грн.</p></div>
<div><p class="cap">Приклад: 50 людей</p><p>30 твіллі (48 000 грн) + 20 сертифікатів по 1 500 грн (30 000 грн) = 78 000 грн. Ціну для вашої кількості підтвердимо в розрахунку — приклад на стор. {TERMS_P}.</p></div></div></div>""", "paper")

# ── 6–9 · one page per gift (split, alternating) ────────────────────────────────────────────────────
def kv(items): return "".join(f'<div><span class="t8">{k}</span><span>{v}</span></div>' for k, v in items)
INCL = ("У ціні", "Пакування й наліпка з вашим логотипом")
SETS = [
    dict(cap="01 · Знак уваги", h="Твіллі — подарунок", hi="на всю команду",
         lead="Шовкова стрічка 84 × 5 см: на шию, у волосся, на сумку, на зап’ястя. 38 авторських принтів — кожному в команді свій.",
         p=1600, frm=False, note="На вирізці — твіллі SOLO «Золоте світло», «Флірт», «Сміливий крок». Довга 140 × 5 «Літній віночок» — 1 850 грн.",
         photo=("photo/site/set-smilyvist-02.jpg", "55% 22%", 1.0), phcap="На фото — твіллі з резинкою в тон: набір «Сміливість», 2 200 грн. Твіллі окремо — 1 600 грн.",
         cuts=["zolote-tw-1", "flirt-tw-2", "krok-tw-1"], cutcls="trio", ccap="",
         kv=[("Принти", "38, зокрема з нової колекції SOLO"), ("Кому", "Усій команді, новим співробітникам, гостям події")],
         tag="Одна річ — на шию, у волосся й на сумку."),
    dict(cap="02 · Тим, хто носить аксесуари", h="Хустка й кільце —", hi="готовий образ",
         lead="Невелика шовкова хустка 44 × 44 і кільце для хустки Gold: воно фіксує хустку на шиї, сумці чи поясі.",
         p=2050, frm=True, note="На вирізці — «Грація» 44 × 44 і кільце «Н стиль»: 1 600 + 450 = 2 050 грн; принти з двостороннім друком — 2 400 + 450 = 2 850 грн.",
         photo=("photo/site/khustka-litnie-pole-44x44-02.jpg", "50% 40%", 1.0), phcap="На фото — хустка «Літнє поле» 44 × 44 на шиї.",
         cuts=["duo-hratsiia-ring"], cutcls="one", ccap="Хустка «Грація» 44 × 44 і кільце «Н стиль» Gold",
         extra=("cut:ring-in-use", "", 1.0, "Кільце замість вузла", "Gold, 450 грн — п’ять моделей на вибір. На фото — «Н стиль»."),
         kv=[("Принти", "Із чотирьох колекцій і SOLO"), ("Строк", "Під замовлення; строк — у розрахунку")],
         tag=""),
    dict(cap="03 · Для відпочинку", h="Маска й резинка —", hi="набір про відпочинок",
         lead="Шовкова маска для сну й резинка в одному принті, у фірмовому пакуванні Obiimy. Підходить і тим, хто не носить хустки.",
         p=3100, frm=False, note="На вирізці — набір «Літнє поле» в коробці. Набором — на 300 грн менше, ніж окремо: маска — 2 700, резинка — 700 грн.",
         photo=("photo/site/mask-vpevnenist-04.jpg", "50% 30%", 1.0), phcap="На фото — маска для сну «Впевненість».",
         extra=("cut:men-mask", "", 1.0, "Чоловікам — маска окремо", "2 700 грн. На фото — маска «Синій»."),
         cuts=["maskscr-litnie-pole"], cutcls="one", ccap="Набір «Літнє поле»: маска й резинка в коробці",
         kv=[("Принти", "8: Літнє поле, Енергія, Свобода, Впевненість, Піднесення, Мелодія двох, Сміливість, Серцебиття")],
         tag=""),
    dict(cap="04 · Ключовим людям", h="Хустка й твіллі —", hi="пара в одній коробці",
         lead="Хустка 44 × 44 і твіллі в одному принті: носять разом або окремо. Для керівників, ключових людей, до річниці в компанії.",
         p=3200, frm=True, note="На вирізці — набір «Натхнення» у святковій коробці Obiimy. Односторонній друк — 3 200 грн, двосторонній — 3 600 грн.",
         photo=("photo/site/set-tvilli-845-ta-khustky-4444-natkhne-04.jpg", "50% 25%", 1.0), phcap="На фото — набір «Натхнення».",
         cuts=["set-natkhnennia-box"], cutcls="box", ccap="Набір «Натхнення» у святковій коробці Obiimy",
         kv=[("Принти", "11 — по 3 200 грн і 7 з двостороннім друком — по 3 600 грн"), ("Майстер-клас", "Від засновниці Світлани Сніжко — за бажанням; формат, дату й вартість узгодимо окремо")],
         tag="Коли подарунок має сказати більше, ніж річ."),
]
for i, S in enumerate(SETS):
    side = "l" if i % 2 == 0 else "r"
    extra = ""
    if S.get("extra"):
        f, ps, z, t, d = S["extra"]; ph = cut(f[4:], 26, "round") if f.startswith("cut:") else pic(f, 18, 22.5, ps, zoom=z)
        extra = f'<div class="men">{ph}<div><h3 class="h13">{t}</h3><p>{d}</p></div></div>'
    tag = f'<p class="h13 tag"><i>{S["tag"]}</i></p>' if S["tag"] else ""
    wide = S["cutcls"] == "fan"
    cuts = "".join(cut(c, 37 if wide else 48) for c in S["cuts"])
    fig = f'<figure class="cuts {S["cutcls"]}"><div>{cuts}</div>' + (f'<figcaption class="t8">{S["ccap"]}</figcaption>' if wide else "") + '</figure>'
    price = pr(S["p"], S["frm"], "h40"); note = f'<p class="t8 pnote">{S["note"]}</p>'
    body = f'{fig}<div class="prow wide">{price}{note}</div>' if wide else f'<div class="prow"><div class="pcell">{price}</div>{fig}</div>{note}'
    if S["cutcls"] == "box":   # the lid is cut by the photo's frame at the left and the top: the box comes out of the page edge, under a rule
        body = f'<div class="prow boxl"><figure class="cuts box">{cut(S["cuts"][0], 62)}</figure><div class="pcell">{price}</div></div>{note}'
    page(f"""<figure class="ph">{pic(S["photo"][0], 148.5, 210, S["photo"][1], zoom=S["photo"][2])}</figure>
<div class="panel"><p class="cap">{S["cap"]}</p><h2 class="h28">{S["h"]}<br><i>{S["hi"]}</i></h2><p class="lead">{S["lead"]}</p>
{body}
<div class="kv">{kv(S["kv"] + [INCL])}</div>{extra}
{tag}<p class="t8 phc{"" if S["tag"] else " solo"}">{S["phcap"]}</p></div>""", f"split {side} gift")

# ── 10 · your logo (sheet): the box bleeds off the left edge, its cut top sits on the rule ───────────
ask = "".join(f'<div class="arg"><b class="num">0{i + 1}</b><div><h3 class="h13">{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(ASK))
_f, _pad, _h = cutsh("box-book-makiv", 140.0, layers=((3.0, 4.0, 0.18),), tint=(0, 0, 0))   # the hinged gift box whole in the frame (obiimy.world, «Маків цвіт»)
page(f"""{rh("Персоналізація")}<figure class="boxcut" style="left:{6 - _pad:.1f}mm;top:{22 - _pad:.1f}mm;width:{140 + 2 * _pad:.1f}mm"><img src="review/lb/{_f}" alt=""></figure>
<div class="sheet logo2"><h2 class="h28">Ваш логотип —<br><i>від наліпки</i><br><i>до власного принта</i></h2>
<div class="free"><p class="cap">У кожному корпоративному замовленні</p><p class="h28">Безкоштовно</p><p>Подарункове пакування кожної речі й наліпка з логотипом вашої компанії всередині. Від вас — логотип. Пакування кожного подарунка покажемо в добірці.</p></div>
<p class="cap req">За запитом</p><div class="args">{ask}</div>
<p class="t8 end">Що встигаємо до вашої дати й скільки це коштує — пишемо в розрахунку. На фото — коробка-книжка набору «Маків цвіт»: твіллі й резинка, 2 200 грн.</p></div>""", "paper")

# ── 11 · the range (sheet): 6 × 2 cut-outs on a shelf line, sizes in three steps ─────────────────────
SIZE = main.SIZE   # mm on the long side
SHORT = {"Закладка для книги": ("Закладка", "для книги · "), "Обруч для вмивання": ("Обруч", "для вмивання · ")}   # the name fits a 39 mm cell
def range_cell(n, p, c, a):
    n, pre = SHORT.get(n, (n, "")); p = pre + p
    tag = '<em class="cap">усім</em>' if a else ""
    return f'<figure class="rc"><div>{cut(c, SIZE[c], fix=True)}</div><figcaption><b class="h13">{n}</b><span>{p}{tag}</span></figcaption></figure>'
cells = "".join(range_cell(*r) for r in RANGE + RANGE_MORE)
page(f"""{rh("Асортимент")}<div class="sheet">
<div class="hd"><h2 class="h28">Усе, з чого можна <i>зібрати подарунок</i></h2><p>Роздрібні ціни obiimy.world. Будь-яку річ можна додати в коробку або зробити окремим подарунком. «Усім» — речі для тих, хто не носить аксесуари.</p></div>
<div class="range">{cells}</div>
<p class="end">Також: сертифікат Obiimy на 1 000–4 000 грн — електронний або фізичний, на будь-який товар, діє 3 місяці · набори резинок — від 1 250 грн.</p></div>""", "paper")

# ── 12 · SOLO (dark frame) ───────────────────────────────────────────────────────────────────────────
page(f"""{pic("photo/solo/tysha-88-2.webp", 297, 210, "0% 30%", "bg", hi=True, zoom=1.05)}
<div class="fr-t"><p class="cap">Нова колекція SOLO · Шлях до себе · 2026</p>
<h1 class="h40">Змінювалися<br>епохи. <i>Хустка</i><br><i>залишалася</i><br><i>поруч.</i></h1>
<p class="fr-p">Натхнення — обкладинки модних журналів 40–50-х. Сім авторських принтів — сім етапів шляху жінки до себе. Натуральний шовк, двосторонній друк. Для команди: кожному — свій принт під стан, який хочете побажати, або один на всіх.</p>
<div class="chip">{cut("tysha-88-1", 13)}<div><span>Принт «Тиша всередині» · твіллі й хустки</span><em>від 1 600 грн</em></div></div></div>""", "frame dark")

# ── 13 · seven prints (dark strip): eye lines on one height (zoom and crop per frame) ───────────────
STRIP = [("photo/solo/iskra-65-4.webp", "50% 0%", 1.12),   # iskra-65-2 is on page 2 (07.10)
         ("photo/solo/flirt-65-3.webp", "61% 50%", 1.0), ("photo/solo/puls-44-3.webp", "50% 50%", 1.0), ("photo/solo/zolote-44-3.webp", "53% 60%", 1.1),
         ("photo/solo/avantiura-tw-1.webp", "50% 0%", 1.07), ("photo/solo/tysha-88-3.webp", "50% 50%", 1.0), ("photo/solo/krok-44-4.webp", "56% 60%", 1.1)]
import re as _re
def fmt7(fm): return "Твіллі · хустка " + _re.search(r"хустка (\d+ × \d+)", fm).group(1)
def tile7(F, P):
    f, ps, z = F; n, st, fm = P[:3]
    st = ST7.get(n, st)
    return f'<figure class="tile">{pic(f, 35.14, 108, ps, zoom=z)}<figcaption><b class="h13"><i>{n}</i></b><span class="t8">{st}</span></figcaption></figure>'
ST7 = {"Іскра": "Енергія і сміливість бути помітною.", "Флірт": "Оптимізм і невимушена жіночність."}   # 07.10: every state in two lines
tiles = "".join(tile7(F, P) for F, P in zip(STRIP, SOLO))
page(f"""<div class="sh sh7"><div><p class="cap">Нова колекція · 2026</p><h2 class="h40">Колекція SOLO</h2><p class="st7 sub">Шлях до себе. <span>Натхнення — обкладинки модних журналів 40–50-х.</span></p></div>
<div><p class="st7">Сім принтів — сім станів</p><p>Кожен принт — про свій стан. Обирайте один для всієї команди або свій для кожного.</p></div></div>
<div class="tiles t7">{tiles}</div>""", "strip dark")

# ── 14 · questions and answers (sheet) — 07.10: the terms page rewritten as eight short Q&A ──────────────────────────
FAQ9 = [("Як замовити?", "Напишіть нам нагоду, кількість людей і дату вручення. У відповідь надішлемо добірку з фото й розрахунок."),
        ("Один принт на всіх чи кожному свій?", "Як вам зручніше: обирайте з добірки один на всіх або кожному свій."),
        ("Чи можна з нашим логотипом?", "Так. Наліпка з логотипом на пакуванні — у ціні. Нашивна бирка чи власний принт — за запитом."),
        ("Чи є мінімальна кількість?", "Мінімальну кількість і наявність потрібного принта підтвердимо в розрахунку — напишіть, скільки людей у команді."),
        ("Скільки часу займає?", "Речі з наявності без наліпки відправляємо в день замовлення (до 16:00). З наліпкою й наборами під замовлення — строк у робочих днях у розрахунку."),
        ("Як доставляєте?", "Новою поштою: в офіс однією посилкою або кожному окремо. Безкоштовно від 5 000 грн. За кордон — за тарифами перевізника."),
        ("Як з оплатою й документами?", "Рахунок на юридичну особу, з ПДВ чи без, і потрібні документи — підтвердимо в розрахунку."),
        ("Чи можна побачити речі наживо?", f"Так, у шоурумі: {SHOWROOM}.")]
faq = "".join(f'<div><h3 class="h13">{q}</h3><p>{a}</p></div>' for q, a in FAQ9)
page(f"""{rh("Запитання та відповіді")}<div class="sheet"><h2 class="h28">Запитання та відповіді</h2><div class="faq2">{faq}</div></div>""", "paper")

# ── 15 · contacts (dark split, photo right) ─────────────────────────────────────────────────────────
page(f"""<figure class="ph">{pic("photo/site/khustka-pidnesennia-44x44-03.jpg", 148.5, 210, "50% 0%")}</figure>
<div class="panel"><p class="cap">Запит</p><h2 class="h28">Напишіть —<br><i>надішлемо добірку</i><br><i>й розрахунок</i></h2>
<p class="tel h40"><a href="{PHONE_HREF}">{PHONE}</a></p>
<p class="h13 lines"><a href="{TG}">Telegram @OBIIMY_sales</a><br><a href="mailto:{MAIL}">{MAIL}</a><br><a href="https://obiimy.world/">obiimy.world</a></p>
<div class="tpl"><p class="cap">Шаблон запиту — скопіюйте й допишіть</p><p>Нагода — … · людей — … · дата вручення — … · бюджет на людину — … · доставка: в офіс / кожному · рахунок на юрособу: так / ні</p></div>
<div class="qr">{qr_svg(TG, 132, ink="#141414", plate="#F1EFEA")}<p class="t8">Скануйте — чат із менеджером у Telegram.<br><a href="{LANDING}">Сторінка для команд із формою запиту</a><br>Шоурум: {SHOWROOM}</p></div></div>""", "split r dark last", folio=False)

assert "Запитання та відповіді" in PAGES[TERMS_P - 1], "TERMS_P does not point at the terms page"

CSS = """
@font-face { font-family: Playfair; font-style: normal; font-weight: 400; src: url(brand/fonts/playfair-cyrillic-400-normal.woff2) format("woff2"); unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116; }
@font-face { font-family: Playfair; font-style: normal; font-weight: 400; src: url(brand/fonts/playfair-latin-400-normal.woff2) format("woff2"); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+20AC, U+2122, U+2212, U+2215; }
@font-face { font-family: Playfair; font-style: italic; font-weight: 400; src: url(brand/fonts/playfair-cyrillic-400-italic.woff2) format("woff2"); unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116; }
@font-face { font-family: Playfair; font-style: italic; font-weight: 400; src: url(brand/fonts/playfair-latin-400-italic.woff2) format("woff2"); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+20AC, U+2122, U+2212, U+2215; }
@font-face { font-family: Tenor; font-style: normal; font-weight: 400; src: url(brand/fonts/tenor-cyrillic-400-normal.woff2) format("woff2"); unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116; }
@font-face { font-family: Tenor; font-style: normal; font-weight: 400; src: url(brand/fonts/tenor-latin-400-normal.woff2) format("woff2"); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+20AC, U+2122, U+2212, U+2215; }
@page { size: 297mm 210mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #F1EFEA; color: #141414; font: 400 9.5pt/4.5mm Tenor, sans-serif; font-variant-numeric: lining-nums; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
a { color: inherit; text-decoration: none; }
img { display: block; }
p { text-wrap: pretty; }
.pg { width: 297mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always; break-after: page; background: #F1EFEA; }
.pg.dark { background: #0E0E0E; color: #F1EFEA; }
/* type: seven sizes */
.h54, .h40, .h28, .h13 { font-family: Playfair, serif; font-weight: 400; letter-spacing: -.01em; }
.h54 { font-size: 54pt; line-height: 54pt; } .h40 { font-size: 40pt; line-height: 42pt; } .h28 { font-size: 28pt; line-height: 30pt; } .h13 { font-size: 13pt; line-height: 16.5pt; letter-spacing: 0; }
h1 i, h2 i, .h28 i, .h13 i { font-style: italic; }
h1 i, h2 i, .season i { color: #8E8A84; } .dark h1 i, .dark h2 i, .frame h1 i { color: #E7D9A6; }
.t8 { font-size: 8pt; line-height: 3.75mm; color: #6E6A63; } .dark .t8 { color: #C9C6C0; }
.cap { font-size: 7pt; line-height: 3.75mm; letter-spacing: .24em; text-transform: uppercase; color: #6E6A63; } .dark .cap, .frame .cap { color: rgba(255,255,255,.78); }
.num { font: 400 13pt/16.5pt Playfair, serif; color: #8E8A84; }
small { font-size: 13pt; letter-spacing: 0; }
/* folio and running head */
.folio { position: absolute; left: 16.5mm; right: 16.5mm; top: 196.4mm; display: flex; justify-content: space-between; font-size: 7pt; line-height: 3.75mm; letter-spacing: .24em; text-transform: uppercase; color: #8E8A84; }
.frame .folio, .strip .folio { color: rgba(255,255,255,.7); }
.fq { font-style: normal; } .split .fq { display: none; }
.split.l .folio { left: 174mm; } .split.r .folio { right: 174mm; }
.rh { position: absolute; left: 16.5mm; right: 16.5mm; top: 0; height: 16.5mm; display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 2.6mm; border-bottom: .5pt solid #141414; font-size: 7pt; line-height: 3.75mm; letter-spacing: .24em; text-transform: uppercase; color: #6E6A63; }
/* frame */
.frame .bg { position: absolute; inset: 0; width: 297mm; height: 210mm; object-fit: cover; }
.frame::after { content: ""; position: absolute; inset: 0; background: linear-gradient(0deg, rgba(0,0,0,.8) 0%, rgba(0,0,0,.42) 36%, rgba(0,0,0,0) 64%), linear-gradient(180deg, rgba(0,0,0,.42) 0%, rgba(0,0,0,0) 24%); }
.frame .logo { position: absolute; left: 16.5mm; top: 16.5mm; height: 9mm; width: 42.4mm; z-index: 2; }
.fr-t { position: absolute; left: 16.5mm; bottom: 22.5mm; width: 190mm; z-index: 2; color: #fff; }
.fr-t .cap { margin-bottom: 3.5mm; max-width: 150mm; white-space: nowrap; font-size: 9pt; letter-spacing: .3em; color: #fff; } .fr-t h1 { margin-bottom: 6mm; } .fr-p { max-width: 106.5mm; margin: -1.5mm 0 6mm; color: rgba(255,255,255,.92); }
.frame .folio { z-index: 2; }
.frame.dark::after { background: linear-gradient(90deg, rgba(0,0,0,.74) 0%, rgba(0,0,0,.5) 34%, rgba(0,0,0,0) 58%), linear-gradient(0deg, rgba(0,0,0,.84) 0%, rgba(0,0,0,.52) 14%, rgba(0,0,0,0) 52%); }
.frame.dark .fr-t { width: 112mm; }
.chip { display: inline-grid; grid-template-columns: 13mm auto; gap: 3.5mm; align-items: center; height: 17mm; padding: 2mm 5mm 2mm 2.5mm; border-radius: 2.5mm; background: rgba(14,14,14,.72); border: .35pt solid rgba(255,255,255,.22); }
.chip img { width: 13mm; height: 13mm; object-fit: contain; } .chip span { display: block; font-size: 8pt; line-height: 3.75mm; color: rgba(255,255,255,.85); } .chip em { display: block; font: 400 13pt/16.5pt Playfair, serif; color: #E7D9A6; }
/* split */
.split .ph { position: absolute; top: 0; width: 148.5mm; height: 210mm; } .split.l .ph { left: 0; } .split.r .ph { right: 0; }
.split .ph > img { width: 100%; height: 100%; object-fit: cover; }
.split .ph figcaption { position: absolute; left: 16.5mm; right: 16.5mm; bottom: 10.05mm; z-index: 2; color: #fff; text-wrap: balance; }
.shade .arg { padding: 2.25mm 0; } .shade .panel h2 { margin-bottom: 4.5mm; }
.split.shade .ph::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 75mm; background: linear-gradient(0deg, rgba(0,0,0,.74), rgba(0,0,0,.4) 45%, rgba(0,0,0,0)); }
.panel { position: absolute; top: 16.5mm; bottom: 19.5mm; width: 106.5mm; display: flex; flex-direction: column; } .split.l .panel { left: 174mm; } .split.r .panel { left: 16.5mm; }
.panel .cap { margin-bottom: 3.75mm; } .panel h2 { margin-bottom: 6mm; white-space: nowrap; }
.proof { color: #4A4A47; margin: -1.5mm 0 4.5mm; }
.args { display: grid; } .arg { display: grid; grid-template-columns: 10.5mm 1fr; padding: 3.75mm 0; border-top: .35pt solid #C9C6C0; } .arg h3 { margin-bottom: .75mm; } .arg p { color: #4A4A47; }
.dark .arg { border-color: rgba(255,255,255,.22); }
.end { margin-top: auto; }
/* page 2 · who we are: the photo on the left half, the «Про нас» text alone in the panel, centred on the page height */
.ab { justify-content: center; } .ab-t { color: #4A4A47; font-size: 9.5pt; line-height: 4.5mm; } .ab-t p { margin-bottom: 2.2mm; } .ab-t .ab-lead { font: 400 12.5pt/16pt Playfair, serif; color: #141414; margin-bottom: 3.5mm; }
.ab-t ul { list-style: none; margin: -.6mm 0 1.6mm; } .ab-t li { padding-left: 4.5mm; text-indent: -4.5mm; } .ab-t li::before { content: "— "; color: #8E8A84; }
/* gift pages */
.gift .lead { color: #4A4A47; margin-bottom: 4.5mm; min-height: 13.5mm; }
.prow { display: grid; grid-template-columns: 1fr 46mm; gap: 6mm; align-items: start; height: 46.5mm; margin-bottom: 3mm; } .pcell { padding-top: 21mm; }
.pnote { min-height: 7.5mm; margin-bottom: 3mm; }
.pv { display: block; white-space: nowrap; } .pv small { color: #8E8A84; font-style: italic; }
.cuts > div { height: 39mm; display: flex; align-items: center; justify-content: center; } .cuts img { max-width: 100%; max-height: 100%; object-fit: contain; filter: drop-shadow(0 2mm 2.5mm rgba(0,0,0,.16)); }
.cuts figcaption { margin-top: 2.25mm; }
.cuts.trio > div { justify-content: flex-end; } .cuts.trio img { height: 39mm; width: auto; margin-left: -9mm; } .cuts.trio img:first-child { margin-left: 0; }
.cuts.fan { margin-bottom: 4.5mm; } .cuts.fan > div { height: 36mm; align-items: flex-start; justify-content: space-between; padding: 0 9mm; border-top: .5pt solid #141414; } .cuts.fan img { height: 36mm; width: auto; filter: drop-shadow(0 1.5mm 2mm rgba(0,0,0,.14)); }
.prow.wide { grid-template-columns: auto 1fr; align-items: end; height: auto; } .prow.wide .pnote { margin: 0 0 2.25mm; min-height: 0; }
.prow.boxl { grid-template-columns: 31.5mm 1fr; position: relative; } .prow.boxl::before { content: ""; position: absolute; left: -16.5mm; right: 0; top: 0; border-top: .5pt solid #141414; } .cuts.box { margin-left: -16.5mm; width: 48mm; } .cuts.box img { width: 48mm; height: auto; max-width: none; max-height: none; } .bc { margin-top: 2.25mm; }
.kv > div { display: grid; grid-template-columns: 24mm 1fr; gap: 3mm; padding: 2.25mm 0; border-top: .35pt solid #C9C6C0; } .kv span { text-wrap: pretty; } .kv > div:last-child { border-bottom: .35pt solid #C9C6C0; }
.tag { margin-top: auto; } .phc { margin-top: 1.5mm; } .phc.solo { margin-top: auto; }
.men { display: grid; grid-template-columns: 24mm 1fr; gap: 6mm; align-items: center; margin-top: 1.5mm; } .men img { width: 24mm; height: 24mm; object-fit: contain; } .men p { color: #4A4A47; margin-top: .75mm; }
/* sheet */
.sheet { position: absolute; left: 16.5mm; right: 16.5mm; top: 24mm; bottom: 19.5mm; display: flex; flex-direction: column; }
.hd { display: grid; grid-template-columns: 1fr 84mm; gap: 6mm; align-items: start; margin-bottom: 6mm; } .hd h2 { white-space: nowrap; } .hd p { color: #4A4A47; padding-top: 1.5mm; }
.gt { display: grid; } .gr { display: grid; grid-template-columns: 10.5mm 22.5mm 1fr 45mm 25.5mm 28.5mm 28.5mm; column-gap: 4.5mm; align-items: center; padding: 2.25mm 0; border-top: .35pt solid #C9C6C0; }
.gr:not(.head) { height: 25.5mm; } .gr.head { border-top: 0; padding: 0 0 2.25mm; } .gr:last-child { border-bottom: .35pt solid #C9C6C0; } .gr.head span:nth-child(4) { padding-left: 9mm; }
.gr .th { width: 22.5mm; height: 21mm; object-fit: contain; filter: drop-shadow(0 1mm 1.5mm rgba(0,0,0,.14)); } .gr h3 { margin: .5mm 0; } .gr p:not(.cap) { color: #4A4A47; }
.pt { display: grid; grid-template-columns: 9mm auto 1fr; align-items: baseline; column-gap: 0; white-space: nowrap; } .pt small { color: #8E8A84; font-style: italic; } .pt > small:nth-of-type(2) { padding-left: 2mm; } .pt .t8 { grid-column: 2 / 4; font-family: Tenor, sans-serif; letter-spacing: 0; margin-top: .75mm; }
.bd { text-align: right; font-variant-numeric: lining-nums tabular-nums; }
.three { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6mm; margin-top: auto; padding-top: 4.5mm; } .three .cap { margin-bottom: 1.5mm; } .three p:not(.cap) { color: #4A4A47; }
.range { display: grid; grid-template-columns: repeat(6, 39mm); column-gap: 6mm; row-gap: 7.5mm; } .rc > div { height: 43.5mm; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 1.5mm; border-bottom: .35pt solid #C9C6C0; }
.rc img { max-width: 100%; max-height: 100%; object-fit: contain; filter: drop-shadow(0 1.5mm 2mm rgba(0,0,0,.14)); }
.rc { position: relative; } .rc figcaption { margin-top: 2.25mm; } .rc b { display: block; white-space: nowrap; } .rc span { color: #4A4A47; white-space: nowrap; } .rc em { display: block; width: fit-content; margin-top: 1.5mm; font-style: normal; color: #141414; border: .35pt solid #141414; border-radius: 2mm; padding: .2mm 1.6mm .1mm 2mm; letter-spacing: .18em; }
.sheet > .end { color: #4A4A47; }
.boxcut { position: absolute; } .boxcut img { width: 100%; height: auto; }
.logo2 { left: 174mm; } .logo2 h2 { margin-bottom: 6mm; white-space: nowrap; }
.free { border-top: .5pt solid #141414; border-bottom: .5pt solid #141414; padding: 3.75mm 0; margin-bottom: 4.5mm; } .free .h28 { margin: .75mm 0 1.5mm; } .free p:last-child { color: #4A4A47; }
.req { margin-bottom: 1.5mm; } .logo2 .arg { padding: 3mm 0; }
.terms { display: grid; grid-template-columns: 106.5mm 1fr; gap: 28.5mm; } .terms h2 { margin-bottom: 4.5mm; } .terms .arg { padding: 2.25mm 0; } .terms > div { display: flex; flex-direction: column; }
.faq2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0 18mm; margin-top: 9mm; } .faq2 div { border-top: .35pt solid #C9C6C0; padding: 6mm 0 7mm; } .faq2 h3 { font-size: 14.5pt; line-height: 18pt; margin-bottom: 2mm; } .faq2 p { color: #4A4A47; font-size: 10.5pt; line-height: 5.3mm; }
.got { margin-top: auto; border-top: .5pt solid #141414; padding-top: 3.75mm; } .got .cap { margin-bottom: 2.25mm; } .got .t8 { margin-top: 2.25mm; }
.cr { display: grid; grid-template-columns: 1fr 9mm 13.5mm 18mm; column-gap: 3mm; padding: 1.5mm 0; border-bottom: .35pt solid #C9C6C0; font-variant-numeric: lining-nums tabular-nums; } .cr span:not(:first-child) { text-align: right; }
.cr.th { padding-top: 0; } .cr.th span { font-size: 7pt; line-height: 3.75mm; letter-spacing: .2em; text-transform: uppercase; color: #6E6A63; } .cr.sum { border-bottom: .5pt solid #141414; } .cr.sum span { font: 400 13pt/16.5pt Playfair, serif; }
.kv.wide > div { grid-template-columns: 34.5mm 1fr; padding: 2.25mm 0; } .kv.wide > div span:last-child { color: #4A4A47; } .kv.wide .t8 { color: #141414; font: 400 13pt/16.5pt Playfair, serif; }
.season { margin-top: auto; padding-bottom: 1.5mm; color: #141414; text-wrap: balance; }
/* strip: header + tiles in the margins, captions under the photos */
.sh { position: absolute; left: 16.5mm; right: 16.5mm; top: 16.5mm; height: 30mm; display: grid; grid-template-columns: 1fr 106.5mm; gap: 6mm; align-items: start; }
.sh .cap { margin-bottom: 3.75mm; } .sh > p { color: #C9C6C0; padding-top: 9mm; }
.sh7 { align-items: start; top: 13mm; } .sh7 h2 { margin: 0 0 2.5mm; } .sh7 .cap { margin-bottom: 2.5mm; } .sh7 .sub { margin: 0; } .sh7 .sub span { color: #C9C6C0; font-style: normal; font-family: Tenor, sans-serif; font-size: 10.5pt; } .sh7 > div:last-child { padding-top: 6.5mm; } .strip .tiles { top: 58mm; } .strip .t7 .tile img { height: 98mm; } .sh7 .st7 { font: italic 400 15pt/18pt Playfair, serif; color: #E7D9A6; margin-bottom: 2mm; } .sh7 div > p:last-child { color: #C9C6C0; }   /* 07.10: SOLO as the heading, the seven states on the right */
.tiles { position: absolute; left: 16.5mm; right: 16.5mm; top: 49.5mm; bottom: 19.5mm; display: grid; gap: 3mm; } .t7 { grid-template-columns: repeat(7, 1fr); } .t4 { grid-template-columns: repeat(4, 1fr); }
.tile img { width: 100%; object-fit: cover; } .t7 .tile img { height: 108mm; } .t4 .tile img { height: 117mm; }
.tile figcaption { padding-top: 3.75mm; color: #fff; } .tile b { display: block; color: #E7D9A6; white-space: nowrap; margin-bottom: 1.5mm; }
.t7 .t8 { color: #C9C6C0; display: block; min-height: 11.25mm; } .t7 .fm { color: #8E8A84; margin-top: 1.5mm; min-height: 0; } .t4 span { color: #C9C6C0; } .t4 figcaption { padding-top: 3mm; } .t4 b { margin-bottom: .75mm; }
/* one scarf, six looks */
.ways6 .panel { left: 16.5mm; width: 84mm; } .ways6 .lead { color: #4A4A47; } .ways6 .folio { right: 196.5mm; } .ways6 .fq { display: none; }
.w6g { position: absolute; left: 106.5mm; right: 0; top: 0; bottom: 0; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: 1fr 1fr; gap: 3mm; }
.w6 { position: relative; overflow: hidden; } .w6 img { width: 100%; height: 100%; object-fit: cover; }
.w6::after { content: ""; position: absolute; inset: 52% 0 0; background: linear-gradient(0deg, rgba(0,0,0,.8) 0%, rgba(0,0,0,.45) 40%, rgba(0,0,0,0) 100%); }   /* the gold label stays legible on light frames */
.w6 figcaption { position: absolute; left: 6mm; bottom: 5.25mm; z-index: 2; color: #E7D9A6; }
.w6 .wp { display: block; font: 400 9.5pt/4.5mm Tenor, sans-serif; color: rgba(231,217,166,.85); letter-spacing: .02em; margin-top: 1mm; }   /* the price under the gold label */
.sz3 { margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end; } .sz3 figure { display: flex; flex-direction: column; align-items: flex-start; } .sz3 img { filter: drop-shadow(0 1.5mm 2mm rgba(0,0,0,.14)); }
.w4g { grid-template-columns: repeat(2, 1fr); } .tw4 { border-bottom: .35pt solid #C9C6C0; padding-bottom: 2.25mm; } .tw4 img { filter: drop-shadow(0 1mm 1.5mm rgba(0,0,0,.14)); }
.ways6 .panel h2 { margin-bottom: 1.5mm; }
.setsp { position: absolute; left: 16.5mm; right: 16.5mm; top: 16.5mm; bottom: 19.5mm; display: flex; flex-direction: column; }
.sh2 { display: flex; align-items: baseline; justify-content: space-between; gap: 6mm; margin-bottom: 4.5mm; } .sh2 .from { margin: 0; }
.scols { display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 9mm; flex: 1; align-items: start; border-top: .35pt solid #C9C6C0; padding-top: 6mm; }
.scol figure { height: 92mm; display: flex; align-items: center; justify-content: center; margin: 0 0 6mm; } .scol figure img { filter: drop-shadow(0 2mm 3mm rgba(40,25,10,.18)); }
.scol h3 { margin-bottom: 2.25mm; } .scol p { font-size: 10.5pt; line-height: 5.2mm; color: #4A4A47; } .scol .from { font: 400 18pt/20pt Playfair, serif; font-style: normal; color: #141414; margin: 4mm 0 0; } .scol .from::first-letter { font-style: italic; }
.pair { margin-top: auto; display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; } .pair figure { margin: 0; overflow: hidden; } .pair img { width: 40.5mm; height: 50mm; object-fit: cover; display: block; }
.setcut { margin: auto 0 0; } .setcut img { display: block; }
.pair-cap { margin-top: 3mm; font-size: 9.5pt; line-height: 4.5mm; color: #4A4A47; }
.sh2 .brand-note { text-align: right; font-size: 9.5pt; line-height: 4.5mm; color: #4A4A47; }
.sets3 .folio { left: 16.5mm; }
.from { display: block; font: italic 400 14pt/17pt Playfair, serif; color: #4A4A47; margin: 2mm 0 7mm; }   /* the price as a quiet line under the heading */
.ways6 .lead { font-size: 11pt; line-height: 5.6mm; color: #2E2C29; margin-bottom: 4.5mm; } .ways6 .lead + .lead { color: #4A4A47; }
/* 07.10: the three «ways» pages were tried on black and returned to light; the captions on the tiles stay a size smaller */
.ways6.dark .lead { color: #F1EFEA; } .ways6.dark .lead + .lead { color: #D9D6D0; } .ways6.dark .pair-cap, .ways6.dark .from { color: #C9C6C0; }
.ways6.dark .folio, .ways6.dark .folio a { color: rgba(255,255,255,.7); } .ways6.dark .nest img { filter: drop-shadow(0 1.5mm 2.5mm rgba(0,0,0,.6)); }
.ways6 .w6 figcaption.h28 { font-size: 20pt; line-height: 24pt; } .ways6.dark .sh2 .brand-note { color: #C9C6C0; }
.nest { position: relative; height: 52mm; margin-top: auto; } .nest figure { position: absolute; bottom: 0; } .nest img { filter: drop-shadow(0 1.5mm 2mm rgba(0,0,0,.16)); }
.nest .n0 { left: 0; } .nest .n1 { left: 13mm; } .nest .n2 { left: 26mm; }   /* each smaller square steps right: the three edges stay visible */
.nest .nl { position: absolute; left: 55mm; bottom: 1mm; display: flex; flex-direction: column; gap: 3mm; } .nest .nl p { white-space: nowrap; } .nest .nl b { display: block; } .nest .nl p:nth-child(1) { margin-bottom: 6mm; }
.sz3 figcaption { margin-top: 3mm; border-top: .35pt solid #C9C6C0; padding-top: 1.5mm; min-width: 24mm; } .sz3 b { display: block; } .ways6 .end { margin-top: 6mm; }
/* last page */
.last h2 { margin-bottom: 9mm; } .tel { color: #E7D9A6; margin-bottom: 4.5mm; white-space: nowrap; letter-spacing: -.035em; word-spacing: -.06em; } .lines { color: #F1EFEA; }
.tpl { margin-top: 9mm; border-top: .35pt solid rgba(255,255,255,.3); border-bottom: .35pt solid rgba(255,255,255,.3); padding: 3.75mm 0; } .tpl .cap { margin-bottom: 1.5mm; } .tpl p:last-child { color: #F1EFEA; }
.qr { margin-top: auto; display: grid; grid-template-columns: 33mm 1fr; gap: 6mm; align-items: center; } .qr svg { width: 33mm; height: 33mm; } .qr a { border-bottom: .35pt solid rgba(255,255,255,.4); }
"""
PIDS = ["cover", "who", "ways-scarf", "ways-twilly", "ways-acc", "sets", "offer", "gift-twilly", "gift-ring", "gift-mask", "gift-set", "logo", "range", "solo", "prints", "terms", "contacts"]
EDITS = OUT / "src" / "deck-edits.json"          # written by the WYSIWYG editor (src/deck-editor.py), applied on every build
EDITOR_PAGES = OUT / "review" / "deck-editor-pages.json"   # what the editor opens: every page (hidden ones too) as built

def apply_edits(pages, pids, builder, edits_file=None, pages_file=None):
    """Manual edits from the WYSIWYG editor. A page saved there replaces the generated one (its HTML is kept as is), hidden pages
    are not printed, the order is the editor's; with pages hidden or moved the folios are renumbered. Returns the pages to print.
    deck-edits.json: {"pages": {pid: {"html": …, "base": sha1 of the generated page it was made from}}, "hidden": [pid], "order": [pid]}."""
    import hashlib, json, re
    EDITS_F, PAGES_F = edits_file or EDITS, pages_file or EDITOR_PAGES
    ed = json.loads(EDITS_F.read_text(encoding="utf-8")) if EDITS_F.exists() else {}
    saved, hidden, order = ed.get("pages", {}), set(ed.get("hidden", [])), ed.get("order", [])
    items = []
    for html, pid in zip(pages, pids):
        gen = typo(re.sub(r"<section\b", f'<section data-pid="{pid}"', html, count=1)); h = hashlib.sha1(gen.encode("utf-8")).hexdigest()
        it = dict(pid=pid, generated=gen, base=h, html=gen, edited=False, stale=False, hidden=pid in hidden)
        if pid in saved:
            it.update(html=saved[pid]["html"], edited=True, stale=saved[pid].get("base") != h)
            if it["stale"]: print(f"edits: «{pid}» — the generator changed after the manual edit; the manual version is kept (reset the page in the editor to take the new one)")
        items.append(it)
    for pid, sv in saved.items():          # pages duplicated in the editor: no generated twin, printed from the saved html
        if pid not in pids and isinstance(sv, dict) and sv.get("html"):
            items.append(dict(pid=pid, generated=None, base=None, html=sv["html"], edited=True, stale=False, hidden=pid in hidden, copy_of=sv.get("copy_of")))
    if order:
        pos = {pid: i for i, pid in enumerate(order)}; key = {}; last = -1
        for it in items:                       # pages the editor has not seen stay after their generated neighbour
            if it["pid"] in pos: last = pos[it["pid"]]; key[it["pid"]] = (last, 0)
            else: key[it["pid"]] = (last, 1)
        items.sort(key=lambda it: key[it["pid"]])
    shown = [it for it in items if not it["hidden"]]
    if hidden or order:
        num = {it["pid"]: n + 1 for n, it in enumerate(shown)}
        for it in shown:
            it["html"] = re.sub(r'(<p class="folio"[^>]*>.*?<span[^>]*>)(\d\d)(</span></p>)', lambda m: f'{m.group(1)}{num[it["pid"]]:02d}{m.group(3)}', it["html"], flags=re.S)
            if "terms" in num: it["html"] = re.sub(r"(стор\.[\s\u00a0\u202f]*)(\d+)", lambda m: m.group(1) + str(num["terms"]), it["html"])
    PAGES_F.write_text(json.dumps(dict(builder=builder, pages=items), ensure_ascii=False), encoding="utf-8")
    if saved or hidden or order: print("edits:", len([i for i in items if i["edited"]]), "pages edited by hand ·", len(hidden & {i["pid"] for i in items}), "hidden ·", "order changed" if order else "order as built")
    return [it["html"] for it in shown]

def render(pages=None, css=None, pids=None, builder="src/build-team-pdf.py", out_html=None, out_pdf=None, shots=None, edits_file=None, pages_file=None):
    """Writes team-deck.html, the PDF and page screenshots. build-deck-variants.py passes the deck with variant pages inserted;
    build-team-pdf-v2.py passes its own pages and output paths."""
    out_html = out_html or OUT / "team-deck.html"; out_pdf = out_pdf or OUT / "obiimy-podarunky-dlia-komandy.pdf"; shots = shots or OUT / "review" / "pp" / "team" / "deck"
    pages = pages or PAGES; css = css or CSS
    pids = pids or (PIDS if len(pages) == len(PIDS) else [f"p{i + 1:02d}" for i in range(len(pages))])
    assert len(pids) == len(pages) == len(set(pids)), "every page needs its own id"
    pages = apply_edits(pages, pids, builder, edits_file, pages_file)
    head = typo(f'<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>Obiimy — подарунки для команди 2026</title><style>{css}</style></head><body>')
    out_html.write_text(head + "".join(pages) + "</body></html>")
    (OUT / "review" / "deck-editor.css").write_text(typo(css))

    dups = sorted({f for f in USED if USED.count(f) > 1})
    print("pages:", len(pages), "· model shots:", len(USED), "· repeated:", dups or "none")

    script = OUT / "review" / "pp" / "pdf-team.mjs"
    script.write_text('''import puppeteer from 'puppeteer-core';
    import fs from 'fs';
    const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--no-sandbox', '--allow-file-access-from-files'] });
    const p = await b.newPage(); await p.setViewport({ width: 1123, height: 794, deviceScaleFactor: 1.5 });
    await p.goto('file:///Users/ivan/obiimy/team-deck.html', { waitUntil: 'networkidle0', timeout: 120000 });
    await p.evaluate(() => document.fonts.ready);
    // layout checks: text outside its page, text over the folio, clipped text
    const issues = await p.evaluate(() => {
      const out = [], mm = 1123 / 297;
      document.querySelectorAll('.pg').forEach((pg, i) => {
        const R = pg.getBoundingClientRect(), fo = pg.querySelector('.folio'), F = fo && fo.getBoundingClientRect();
        pg.querySelectorAll('h1,h2,h3,p,span,b,em,figcaption,small').forEach(el => {
          if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
          const r = el.getBoundingClientRect(); if (!r.width) return;
          const t = el.textContent.trim().slice(0, 34), inFolio = fo && fo.contains(el);
          if (r.right > R.right - 6 * mm + 1 && !inFolio && !el.closest('.tile,.po,.chip,.w6,.cv') || r.left < R.left - 1 || r.bottom > R.bottom + 1 || r.top < R.top - 1) out.push(`p${i + 1} outside page/margin: «${t}»`);
          if (F && !inFolio && r.bottom > F.top - 1 && r.top < F.bottom && r.right > F.left && r.left < F.right && !el.closest('.tile,.ph,.fr-t')) out.push(`p${i + 1} over folio: «${t}»`);
          if (el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).whiteSpace === 'nowrap') out.push(`p${i + 1} too wide: «${t}»`);
        });
        pg.querySelectorAll('.panel a, .panel span, .panel p, .panel h2, .panel h3').forEach(el => { const P = el.closest('.panel').getBoundingClientRect(), r = el.getBoundingClientRect(); if (r.width && r.right > P.right + 1) out.push(`p${i + 1} wider than the panel by ${((r.right - P.right) / mm).toFixed(1)} mm: «${el.textContent.trim().slice(0, 30)}»`); });
        pg.querySelectorAll('.panel,.sheet').forEach(c => { if (c.scrollHeight > c.clientHeight + 2) out.push(`p${i + 1} container overflow by ${Math.round((c.scrollHeight - c.clientHeight) / mm)} mm`); });
        // text over text: line boxes of two text runs (not nested, not in one heading) overlap by more than 1 mm both ways
        const runs = [];
        pg.querySelectorAll('h1,h2,h3,p,span,b,em,small,dt,dd,a,i,figcaption').forEach(el => { [...el.childNodes].forEach(n => { if (n.nodeType !== 3 || !n.textContent.trim()) return; const rg = document.createRange(); rg.selectNodeContents(n); [...rg.getClientRects()].forEach(r => { if (r.width > 1 && r.height > 1) runs.push({ el, r, t: n.textContent.trim().slice(0, 22) }); }); }); });
        for (let a = 0; a < runs.length; a++) for (let b = a + 1; b < runs.length; b++) {
          const A = runs[a], B = runs[b]; if (A.el === B.el || A.el.contains(B.el) || B.el.contains(A.el)) continue;
          const ha = A.el.closest('h1,h2,h3'), hb = B.el.closest('h1,h2,h3'); if (ha && ha === hb) continue;
          const ox = Math.min(A.r.right, B.r.right) - Math.max(A.r.left, B.r.left), oy = Math.min(A.r.bottom, B.r.bottom) - Math.max(A.r.top, B.r.top);
          if (ox > mm && oy > 1.5 * mm) out.push(`p${i + 1} text over text: «${A.t}» / «${B.t}» (${(ox / mm).toFixed(1)} × ${(oy / mm).toFixed(1)} mm)`);
        }
        // text leaving the left margin or too close to the right trim on paper pages
        pg.querySelectorAll('h1,h2,h3,p,dt,dd,figcaption').forEach(el => { if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return; const r = el.getBoundingClientRect(); if (!r.width) return;
          if (r.left < R.left + 16.5 * mm - 1.5 && !el.closest('.frame,.cv,.lx,.ed,.po,.w6,.folio,.rh,.tile,.chip,.x2,.k1,.k3,.x1,.x3')) out.push(`p${i + 1} text in the left margin (${((r.left - R.left) / mm).toFixed(1)} mm): «${el.textContent.trim().slice(0, 22)}»`); });
        pg.querySelectorAll('h2').forEach(h => { const pr = h.parentElement.getBoundingClientRect(), r = h.getBoundingClientRect(); [...h.childNodes].forEach(n => { const rg = document.createRange(); rg.selectNodeContents(n); const w = rg.getBoundingClientRect(); if (w.right > pr.right + 1) out.push(`p${i + 1} heading wider than its column: «${h.textContent.trim().slice(0, 30)}»`); }); });
      });
      return [...new Set(out)];
    });
    console.log(issues.length ? 'LAYOUT ISSUES:\\n' + issues.join('\\n') : 'layout: clean');
    await p.pdf({ path: '/Users/ivan/obiimy/obiimy-podarunky-dlia-komandy.pdf', printBackground: true, preferCSSPageSize: true });
    const dir = process.env.DECK_SHOTS || '/Users/ivan/obiimy/review/pp/team/deck'; fs.mkdirSync(dir, { recursive: true });
    for (const f of fs.readdirSync(dir)) if (/^p\\d+\\.png$/.test(f)) fs.unlinkSync(dir + '/' + f);
    const els = await p.$$('.pg'); for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: `${dir}/p${String(i + 1).padStart(2, '0')}.png` });
    await b.close();
    ''')
    script.write_text(script.read_text().replace("file:///Users/ivan/obiimy/team-deck.html", out_html.resolve().as_uri()).replace("'/Users/ivan/obiimy/obiimy-podarunky-dlia-komandy.pdf'", repr(str(out_pdf.resolve()))))
    subprocess.run(["node", str(script)], cwd=OUT / "review" / "pp", check=True, env=dict(os.environ, DECK_SHOTS=str(shots)))
    print("size:", round(out_pdf.stat().st_size / 1048576, 1), "MB")

    def qr_ok(png):
        """The QR on the last page must decode (a slight blur stands in for a phone camera) — a styled code is easy to break."""
        try: import cv2
        except ImportError: return "not checked (no OpenCV)"
        im = cv2.imread(str(png)); h, w = im.shape[:2]; d = cv2.QRCodeDetector()
        crop = cv2.cvtColor(im[h // 2:, : w // 2], cv2.COLOR_BGR2GRAY)
        hits = []
        for sc in (0.75, 1, 1.5, 2):
            v = d.detectAndDecode(cv2.resize(crop, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA if sc < 1 else cv2.INTER_CUBIC))[0]
            if v: hits.append(v)
        return f"ok at {len(hits)}/4 scales without blur → {hits[0]}" if len(hits) >= 2 else f"WEAK: decodes at {len(hits)}/4 scales"
    print("QR:", qr_ok(pathlib.Path(shots) / f"p{len(pages):02d}.png"))

if __name__ == "__main__":
    render()
