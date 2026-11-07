"""Black Friday creatives (07.11.2026, client: «новая порция креативов к чёрной пятнице — хустки и прочие товары из коллекций,
которые не SOLO, скидки от −20 до −40 %, подойди творчески и необычно»). The idea: a silk brand's Black Friday is not black —
«Чорна п'ятниця. Біла хустка.» The black field is the stage, the silk is the colour, the brand's yellow is the discount.
Photos: obiimy.world as they are (photo/site, photo/) — the four print collections («Співоча душа», «Поклик душі», «Пробудження»,
«Дика стихія»), masks, twillies, bookmarks, pocket squares, the yellow boxes; nothing from SOLO. The discount is always the
client's range «−20…−40 %» — which product gets which is not decided, so no crossed-out prices and no per-item percentage.
1080×1920 plain plus story / feed / square via FORMAT. Output: bf[-<format>].html → out[-<format>]/*.jpg
(cd ads && ADS=bf/bf.html OUT=bf/out node render.mjs; FORMAT=story python3 bf/build.py → ADS=bf/bf-story.html OUT=bf/out-story)."""
import os, pathlib, re, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "solo"))
from kit import nb, LOGO_W, LOGO_K, GRAIN

FORMAT = os.environ.get("FORMAT", "plain")   # plain | story | feed | square
H = {"feed": 1350, "square": 1080}.get(FORMAT, 1920)
K = .72 if FORMAT == "square" else (.86 if FORMAT == "feed" else 1)
SQ = FORMAT == "square"
TOPL = 250 if FORMAT == "story" else 58
BOTB = 340 if FORMAT == "story" else 60
BAR = int(120 * K)                            # the bottom row: the discount pill and the address
Y0 = TOPL + int(96 * K)                       # content starts under the logo line
Y1 = H - BOTB - BAR - int(30 * K)             # and ends above the bottom row
PS = "../../photo/site/"; PR = "../../photo/"
YEL, INK, CREAM, WHITE, PAPER = "#F2B705", "#141110", "#F3EADB", "#FFFFFF", "#F1E8D8"
RANGE = "−20…−40 %"

def nbh(text):
    text = re.sub(r"(?<![\w’'])(у|в|з|і|й|а|о|на|до|за|та|не|чи|із|зі|від|для|що|як|це)\s+(?=[^\s<])", lambda m: m.group(1) + " ", text, flags=re.I)
    return re.sub(r"\s+([—–])", lambda m: " " + m.group(1), text)

CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #555; font-family: 'Onest', Arial, sans-serif; -webkit-font-smoothing: antialiased; }
.ad { width: 1080px; height: HPXpx; position: relative; overflow: hidden; background: #141110; margin: 20px auto; color: #F3EADB; }
.ad > * { position: absolute; margin: 0; }
.ad p { margin: 0; }
.ad::after { content: ""; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: .2; mix-blend-mode: soft-light; background-image: GRAIN; }
.ph { overflow: hidden; } .ph img { width: 100%; height: 100%; object-fit: cover; display: block; }
.fit img { object-fit: contain; }
.mult img { mix-blend-mode: multiply; }   /* a white packshot on the white field: its edges vanish */
.big { font-family: 'Montserrat', sans-serif; font-weight: 400; line-height: 1.06; letter-spacing: -.01em; text-wrap: balance; }
.big em { font-style: normal; color: #F2B705; }
.big mark { background: #F2B705; color: #141110; padding: 0 .12em; border-radius: .08em; box-decoration-break: clone; -webkit-box-decoration-break: clone; }
.small { font-family: 'EB Garamond', serif; font-weight: 500; line-height: 1.22; text-wrap: pretty; }
.kicker { font-family: 'Montserrat', sans-serif; font-weight: 500; text-transform: uppercase; letter-spacing: .2em; white-space: nowrap; }
.hdr { font-family: Montserrat, sans-serif; font-weight: 500; letter-spacing: .16em; text-transform: uppercase; white-space: nowrap; }
.num { font-family: 'Montserrat', sans-serif; font-weight: 300; line-height: .9; letter-spacing: -.04em; font-variant-numeric: tabular-nums; white-space: nowrap; }
.pill { display: inline-flex; align-items: center; gap: .5em; border-radius: 999px; font-family: 'Montserrat', sans-serif; font-weight: 500; white-space: nowrap; }
.ink { color: #1B1613; } .ink .small { color: #4B423B; }
.light .small { color: #D9CDB9; }
.card { background: #fff; box-shadow: 0 40px 80px -24px rgba(0,0,0,.7), 0 6px 14px rgba(0,0,0,.3); }
.card img { width: 100%; height: 100%; object-fit: cover; display: block; }
.tag { background: #F6F0E4; color: #141110; border-radius: 10px; box-shadow: 0 24px 50px -20px rgba(0,0,0,.8); font-family: 'Montserrat', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.tag::before { content: ""; position: absolute; top: 12px; left: 50%; width: 14px; height: 14px; margin-left: -7px; border-radius: 50%; background: #141110; box-shadow: inset 0 0 0 3px #d9cfbd; }
""".replace("GRAIN", GRAIN).replace("HPX", str(H))

ads = []
def ad(id, body, note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad" id="{id}">{body}\n</section>')

def header(dark=True):
    col = CREAM if dark else "#1B1613"
    return (f'<img src="{LOGO_W if dark else LOGO_K}" alt="" style="left:64px;top:{TOPL}px;height:{int(56 * K)}px;z-index:5">'
            f'<p class="hdr" style="right:64px;top:{TOPL + int(16 * K)}px;font-size:{int(24 * K)}px;color:{col};z-index:5">Чорна п’ятниця</p>')

def bar(dark=True, label=None, cta="obiimy.world"):
    """The bottom row: the discount in a yellow pill (the only loud thing on the page) and the address."""
    label = label or f"Знижки {RANGE}"
    fg = CREAM if dark else "#1B1613"
    return f'''
  <div style="left:64px;right:64px;bottom:{BOTB}px;height:{BAR}px;display:flex;align-items:center;justify-content:space-between;gap:{int(24 * K)}px;z-index:6">
    <span class="pill" style="background:{YEL};color:{INK};font-size:{int(34 * K)}px;padding:{int(22 * K)}px {int(40 * K)}px">{nb(label)}</span>
    <span class="hdr" style="font-size:{int(26 * K)}px;color:{fg};letter-spacing:.1em;text-transform:none">{cta}</span>
  </div>'''

def words(big, small, size=84, dark=True, width=None, kicker=None):
    w = f"max-width:{width}px;" if width else ""
    out = f'<p class="kicker" style="font-size:{int(24 * K)}px;color:{YEL if dark else "#8A6A12"};margin-bottom:{int(18 * K)}px">{kicker}</p>' if kicker else ""
    out += f'<p class="big" style="font-size:{int(size * K)}px;{w}">{nbh(big)}</p>'
    if small: out += f'<p class="small" style="font-size:{int(36 * K)}px;margin-top:{int(22 * K)}px;{w}">{nb(small)}</p>'
    return out

def melt(dark=True, h=320, bottom=True):
    """The seam between the photograph and the field: the field's colour rises into the picture."""
    c = "20,17,16" if dark else "255,255,255"
    return f"linear-gradient({'0deg' if bottom else '180deg'},rgba({c},1),rgba({c},.85) 30%,rgba({c},0))"

# ─── templates ─────────────────────────────────────────────────────────────────────────────────────────────────────────

def full(id, img, pos, big, small, note="", dark=True, split=.56, size=84, kicker=None, root=False, zoom=1.0, label=None, ph_bg=None, ptop=0):
    """`ptop` — the photograph starts under the logo line instead of the frame's top edge (for flat scarves and white packshots,
    where the white logo would drown in the picture)."""
    """A photograph edge to edge across the top, melting into the field; the words in the field, the discount row below.
    In the square the photo takes the left half at full height and the words stand on the right."""
    src = (PR if root else PS) + img
    field = INK if dark else WHITE
    cls = "light" if dark else "ink"
    if SQ:
        pw = 540
        body = f'''
  <div style="inset:0;background:{field}"></div>
  <div class="ph" style="left:0;top:{ptop}px;width:{pw}px;height:{H - ptop}px;{f"background:{ph_bg}" if ph_bg else ""}"><img src="{src}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  <div style="left:{pw - 140}px;top:0;width:140px;height:{H}px;background:linear-gradient(90deg,rgba({"20,17,16" if dark else "255,255,255"},0),{field})"></div>
  {header(dark)}
  <div class="{cls}" style="left:{pw - 40}px;right:64px;top:{Y0 + int(40 * K)}px;z-index:4">{words(big, small, size, dark, kicker=kicker)}</div>
  {bar(dark, label)}'''
    else:
        yph = int(H * split)
        body = f'''
  <div style="inset:0;background:{field}"></div>
  <div class="ph" style="left:0;right:0;top:{ptop}px;height:{yph + int(60 * K) - ptop}px;{f"background:{ph_bg}" if ph_bg else ""}"><img src="{src}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  <div style="left:0;right:0;top:{yph - int(260 * K)}px;height:{int(320 * K) + 2}px;background:{melt(dark, bottom=True)}"></div>
  {"" if ptop else f'<div style="left:0;right:0;top:0;height:{int(220 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,{.45 if dark else .18}),rgba(12,9,8,0))"></div>'}
  {header(dark=True if dark else False)}
  <div class="{cls}" style="left:64px;right:64px;top:{yph + int(20 * K)}px;bottom:{H - Y1}px;z-index:4">{words(big, small, size, dark, kicker=kicker)}</div>
  {bar(dark, label)}'''
    ad(id, body, note)

def objw(id, img, big, small, note="", size=84, pos="50% 50%", zoom=1.0, ar=1.0, kicker=None, root=False, label=None, shift=0):
    """A white packshot on the white field — the object floats, nothing is cut. The words above, the photo fills the rest."""
    src = (PR if root else PS) + img
    head_h = int((330 if not SQ else 0) * K)
    if SQ:   # square: the words left, the object right at full height
        col = 470; top = Y0; ph_h = Y1 - top; ph_w = min(1080 - 64 - col, int(ph_h * ar)); px = 64 + col + (1080 - 64 - col - ph_w) // 2
        body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;width:{col - 30}px;top:{Y0 + int(20 * K)}px;z-index:4">{words(big, small, size, False, kicker=kicker)}</div>
  <div class="ph mult" style="left:{px}px;top:{top}px;width:{ph_w}px;height:{ph_h}px;z-index:2"><img src="{src}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  {bar(False, label)}'''
    else:
        top = Y0 + head_h + int(20 * K); ph_h = Y1 - top; ph_w = min(1080, int(ph_h * ar))
        if ph_w < int(ph_h * ar): ph_h = int(ph_w / ar)
        px = (1080 - ph_w) // 2 + int(shift * K)
        body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0}px;z-index:4">{words(big, small, size, False, kicker=kicker)}</div>
  <div class="ph mult" style="left:{px}px;top:{top}px;width:{ph_w}px;height:{ph_h}px;z-index:2"><img src="{src}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  {bar(False, label)}'''
    ad(id, body, note)

def square_card(id, img, big, small, note="", root=False, tilt=-3, size=84):
    """A flat scarf as a square card on the black field — Malevich's square, only not black."""
    src = (PR if root else PS) + img
    if SQ:
        cs = int(H - Y0 - (H - Y1)) ; cs = min(cs + 60, 620); cx = 1080 - 64 - cs + 40; cy = (H - cs) // 2 + 20
        body = f'''
  <div style="inset:0;background:{INK}"></div>
  {header()}
  <div class="light" style="left:64px;width:{cx - 64 - 30}px;top:{Y0 + int(30 * K)}px;z-index:4">{words(big, small, size, True)}</div>
  <div class="card" style="left:{cx}px;top:{cy}px;width:{cs}px;height:{cs}px;transform:rotate({tilt}deg);z-index:3"><img src="{src}" alt=""></div>
  {bar()}'''
    else:
        text_h = int(380 * K)
        cs = min(1080 - 2 * 100, Y1 - Y0 - text_h - int(40 * K)); cx = (1080 - cs) // 2; cy = Y0 + int(10 * K)
        body = f'''
  <div style="inset:0;background:{INK}"></div>
  {header()}
  <div class="card" style="left:{cx}px;top:{cy}px;width:{cs}px;height:{cs}px;transform:rotate({tilt}deg);z-index:3"><img src="{src}" alt=""></div>
  <div class="light" style="left:64px;right:64px;top:{cy + cs + int(70 * K)}px;bottom:{H - Y1}px;z-index:4">{words(big, small, size, True)}</div>
  {bar()}'''
    ad(id, body, note)

# ─── the series ───────────────────────────────────────────────────────────────────────────────────────────────────────

COLL = "«Співоча душа», «Поклик душі», «Пробудження», «Дика стихія»"

# 01 · the hero: the name of the day thin and huge, the range in yellow, three silk frames in a strip below
def hero():
    strip = [("khustka-vidnovlennia-88x88-02.jpg", "50% 20%"), ("tvilli-shovkovyi-sokovyti-spohady-02.jpg", "50% 30%"), ("mask-vpevnenist-04.jpg", "50% 30%")]
    if SQ:
        pw = 500
        tiles = "".join(f'<div class="ph" style="left:{i * (pw // 3)}px;top:0;width:{pw // 3 - 4}px;height:{H}px"><img src="{PS}{f}" alt="" style="object-position:{p}"></div>' for i, (f, p) in enumerate(strip))
        body = f'''
  <div style="inset:0;background:{INK}"></div>{tiles}
  <div style="left:{pw - 160}px;top:0;width:160px;height:{H}px;background:linear-gradient(90deg,rgba(20,17,16,0),{INK})"></div>
  {header()}
  <div class="light" style="left:{pw - 60}px;right:64px;top:{Y0 + int(30 * K)}px;z-index:4">
    <p class="big" style="font-size:{int(64 * K)}px;font-weight:300;text-transform:uppercase;letter-spacing:.06em;line-height:1.1">Чорна<br>п’ятниця</p>
    <p class="num" style="font-size:{int(118 * K)}px;color:{YEL};margin-top:{int(24 * K)}px">−20…−40<span style="font-size:.5em;letter-spacing:0"> %</span></p>
    <p class="small" style="font-size:{int(34 * K)}px;margin-top:{int(26 * K)}px">{nb("На шовк із авторськими принтами: хустки, твіллі, маски для сну, резинки й подарункові набори.")}</p></div>
  {bar()}'''
    else:
        sh = int(560 * K); sy = Y1 - sh
        tiles = "".join(f'<div class="ph" style="left:{i * 360}px;top:{sy}px;width:356px;height:{sh}px"><img src="{PS}{f}" alt="" style="object-position:{p}"></div>' for i, (f, p) in enumerate(strip))
        body = f'''
  <div style="inset:0;background:{INK}"></div>
  {header()}
  <div class="light" style="left:64px;right:64px;top:{Y0 + int(10 * K)}px;z-index:4">
    <p class="big" style="font-size:{int(96 * K)}px;font-weight:300;text-transform:uppercase;letter-spacing:.06em;line-height:1.08">Чорна<br>п’ятниця</p>
    <p class="num" style="font-size:{int(196 * K)}px;color:{YEL};margin-top:{int(20 * K)}px">−20…−40<span style="font-size:.5em;letter-spacing:0"> %</span></p>
    <p class="small" style="font-size:{int(36 * K)}px;margin-top:{int(28 * K)}px;max-width:900px">{nb("На шовк із авторськими принтами: хустки, твіллі, маски для сну, резинки й подарункові набори.")}</p></div>
  {tiles}
  <div style="left:0;right:0;top:{sy - 2}px;height:{int(140 * K)}px;background:{melt(True, bottom=False)}"></div>
  {bar()}'''
    ad("bf-01-hero", body, "The hero: the day's name thin and huge, the range in yellow, three silk frames in a strip")
hero()

# 02 · the square that is not black
square_card("bf-02-square", "khustka-flat-kolo-sontsia-88x88-01.jpg",
            "Квадрат. Не чорний.", f"Хустка 88 × 88 «Коло сонця» зі «Співочої душі» — і решта принтів колекцій {COLL}: {RANGE} на Чорну п’ятницю.",
            "Malevich's square, only in silk: the flat scarf as a card on the black field")

# 03–05 · «Чорна п’ятниця. Біла хустка.» — a series of three: the colour of the scarf in the headline
full("bf-03-white", "mizh-flat.webp", "50% 50%", "Чорна п’ятниця. <em style='color:#fff'>Біла</em> хустка.",
     f"«Між нами» з колекції «Пробудження» — і всі хустки колекцій {COLL}: {RANGE}.", "The white scarf on the black field", root=True, split=.56, zoom=1.02, ptop=TOPL + int(90 * K))
full("bf-04-yellow", "khustka-flat-smilyvist-44x44-01.jpg", "50% 50%", "Чорна п’ятниця. <em>Жовта</em> хустка.",
     f"«Сміливість» із «Поклику душі», 44 × 44 — і всі хустки колекцій {COLL}: {RANGE}.", "The yellow scarf on the black field", split=.56, zoom=1.02, ptop=TOPL + int(90 * K))
full("bf-05-red", "riviera-red.jpg", "50% 18%", "Чорна п’ятниця. <em style='color:#E24B3B'>Червона</em> хустка.",
     f"Хустки колекцій {COLL}: {RANGE}. Шовк, авторський принт, ручна обробка краю.", "The red scarf, the Riviera frame", root=True, split=.58)

# 06 · the only black thing worth buying
objw("bf-06-heart", "mask-sertsebyttia-chorna-v-chok-01.jpg", "Єдине чорне, що варто купити цієї п’ятниці.",
     f"Маска для сну «Серцебиття», чорна — шовк з обох боків. Маски для сну: {RANGE}.", "The black heart mask alone on white", ar=1250 / 1500, zoom=1.5, pos="50% 60%")

# 07 · the barcode of twillies
def barcode():
    tw = ["tvilli-shovkovyi-probudzhennia-04.jpg"] * 5; sc = [1.0, 1.7, .85, 2.3, 1.25]   # the one vertical twilly at five scales — bars of five thicknesses
    if SQ:
        col = 440; n = 4; top = Y0; hgt = Y1 - top; w = (1080 - 64 - col) // n
        strip = "".join(f'<div class="ph mult" style="left:{64 + col + i * w}px;top:{top}px;width:{w}px;height:{hgt}px"><img src="{PS}{f}" alt="" style="object-position:50% 50%;transform:scale({sc[i]})"></div>' for i, f in enumerate(tw[:n]))
        lines = "".join(f'<i style="display:inline-block;width:{wd}px;height:100%;background:#141110;margin-right:{gap}px"></i>' for wd, gap in [(3, 4), (6, 3), (2, 5), (8, 4), (3, 3), (5, 6), (2, 3), (7, 4), (3, 5), (4, 3), (9, 4), (2, 4), (5, 3), (3, 6), (6, 3)] * 2)
        body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;width:{col - 40}px;top:{Y0 + int(20 * K)}px;z-index:4">{words("Штрихкод знижки.", f"Твіллі 84 × 5 «Пробудження» — і всі твіллі колекцій {COLL}: {RANGE}. Скануйте очима.", 72, False)}
    <div style="height:{int(60 * K)}px;margin-top:{int(30 * K)}px;white-space:nowrap;overflow:hidden">{lines}</div></div>
  {strip}
  {bar(False)}'''
    else:
        n = 5; top = Y0 + int(300 * K); hgt = Y1 - top - int(120 * K); w = (1080 - 128) // n
        strip = "".join(f'<div class="ph mult" style="left:{64 + i * w}px;top:{top}px;width:{w}px;height:{hgt}px"><img src="{PS}{f}" alt="" style="object-position:50% 50%;transform:scale({sc[i]})"></div>' for i, f in enumerate(tw[:n]))
        lines = "".join(f'<i style="display:inline-block;width:{wd}px;height:100%;background:#141110;margin-right:{gap}px"></i>' for wd, gap in [(3, 4), (6, 3), (2, 5), (8, 4), (3, 3), (5, 6), (2, 3), (7, 4), (3, 5), (4, 3), (9, 4), (2, 4), (5, 3), (3, 6), (6, 3)] * 5)
        body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0}px;z-index:4">{words("Штрихкод знижки.", f"Твіллі 84 × 5 «Пробудження» — і всі твіллі колекцій {COLL}: {RANGE}. Скануйте очима.", 84, False)}</div>
  {strip}
  <div style="left:64px;right:64px;top:{top + hgt + int(20 * K)}px;height:{int(70 * K)}px;white-space:nowrap;overflow:hidden">{lines}</div>
  <p class="num ink" style="left:64px;top:{top + hgt + int(96 * K)}px;font-size:{int(22 * K)}px;letter-spacing:.3em;font-weight:400">2 0 3 0 4 0 · O B I I M Y · S I L K</p>
  {bar(False)}'''
    ad("bf-07-barcode", body, "Four twillies stand like the bars of a barcode; a barcode strip under them")
barcode()

# 08 · the belt
full("bf-08-belt", "hratsiia-belt.webp", "50% 40%", "Затягнути пояси? Навпаки.",
     f"Хустка «Грація» 65 × 65 із «Дикої стихії» — як пояс. Хустки й твіллі: {RANGE}.", "The scarf as a belt — the pun on belts", root=True, split=.58, zoom=1.0)

# 09 · sleep through it
full("bf-09-sleep", "mask-nizhnist-03.jpg", "50% 30%", "Проспати Чорну п’ятницю? Можна. У шовковій масці.",
     f"Маска для сну «Ніжність» — шовк з обох боків, м’яка резинка. Маски для сну: {RANGE}.", "The woman in the mask, the white field", dark=False, split=.52, zoom=1.0, ph_bg="#f4f4f4")

# 10 · the bookmark
full("bf-10-bookmark", "bookmark-melodiia-dvokh-01.jpg", "50% 60%", "Зробіть закладку: Чорна п’ятниця.",
     f"Шовкова закладка для книги «Мелодія двох» — і вся «Співоча душа»: {RANGE}.", "The silk bookmark in the book — a bookmark for the day", dark=False, split=.55, zoom=1.0)

# 11 · for him
full("bf-11-pashe", "pashe-svoboda-02.jpg", "50% 30%", "Чорна п’ятниця. І для нього.",
     f"Паше 44 × 44 «Свобода» в нагрудну кишеню — і хустки чотирьох колекцій: {RANGE}.", "The pocket square — the men's frame", split=.58, zoom=1.0)

# 12 · the sun in November
full("bf-12-kolo", "kolo-2.webp", "50% 30%", "Листопад темний. Хустка — ні.",
     f"«Коло сонця» 88 × 88 зі «Співочої душі» — і решта колекцій {COLL}: {RANGE}.", "The sunflower scarf in the beige coat", root=True, split=.6)

# 13 · our Friday is yellow
def yellow():
    if SQ:
        pw = 520
        body = f'''
  <div style="inset:0;background:{YEL}"></div>
  <div class="ph" style="left:{1080 - pw}px;top:{Y0 - 20}px;width:{pw}px;height:{H - Y0 + 20}px;background:#fff"><img src="{PR}box-dots.jpg" alt="" style="object-position:50% 50%;transform:scale(1.35)"></div>
  <div style="left:{1080 - pw}px;top:0;width:140px;height:{H}px;background:linear-gradient(90deg,{YEL},rgba(242,183,5,0))"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;width:{1080 - pw - 64 + 60}px;top:{Y0 + int(30 * K)}px;z-index:4">{words("У нас п’ятниця жовта.", f"Чорна п’ятниця на obiimy.world: {RANGE} на шовк із авторськими принтами. У жовтій коробці — як завжди.", 76, False)}</div>
  {bar(False)}'''
    else:
        yph = int(H * .5)
        body = f'''
  <div style="inset:0;background:{YEL}"></div>
  <div class="ph" style="left:0;right:0;top:{Y0 - 10}px;height:{yph + 70 - Y0}px;background:#fff"><img src="{PR}box-dots.jpg" alt="" style="object-position:50% 45%;transform:scale(1.25)"></div>
  <div style="left:0;right:0;top:{yph - 200}px;height:262px;background:linear-gradient(0deg,{YEL},rgba(242,183,5,.85) 30%,rgba(242,183,5,0))"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;right:64px;top:{yph + int(30 * K)}px;z-index:4">{words("У нас п’ятниця жовта.", f"Чорна п’ятниця на obiimy.world: {RANGE} на шовк із авторськими принтами. У жовтій коробці — як завжди.", 92, False)}</div>
  {bar(False)}'''
    body = body.replace(f'background:{YEL};color:{INK};font-size', f'background:{INK};color:{CREAM};font-size')   # the pill inverts on the yellow field
    ad("bf-13-yellow", body, "The brand's yellow instead of black: the yellow box with the dotted scarf")
yellow()

# 14 · three tags
def tags():
    vals = ["−20 %", "−30 %", "−40 %"]
    if SQ:
        tw, th = 150, 210; x0 = 1080 - 64 - 3 * tw - 2 * 30; y0 = Y0 + 20
        t = "".join(f'<div style="left:{x0 + i * (tw + 30) + tw // 2}px;top:0;width:2px;height:{y0 + 20 + i * 28}px;background:#8a7f70"></div><div class="tag" style="left:{x0 + i * (tw + 30)}px;top:{y0 + i * 28}px;width:{tw}px;height:{th}px;transform:rotate({(-4, 2, -2)[i]}deg)"><p class="num" style="font-size:52px;font-weight:400;margin-top:14px">{v}</p><p class="kicker" style="font-size:12px;margin-top:10px;color:#8A6A12">Чорна п’ятниця</p></div>' for i, v in enumerate(vals))
        body = f'''
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="left:0;right:0;bottom:0;height:{int(H * .5)}px;-webkit-mask-image:linear-gradient(180deg,transparent,#000 60%);mask-image:linear-gradient(180deg,transparent,#000 60%)"><img src="{PR}hratsiia-flat.webp" alt="" style="object-position:50% 50%;opacity:.9"></div>
  {header()}
  <div class="light" style="left:64px;width:{x0 - 64 - 30}px;top:{Y0 + int(20 * K)}px;z-index:4">{words("Три бирки. Одна п’ятниця.", "Яка знижка на що — на obiimy.world. Хустки, твіллі, маски для сну, резинки й набори.", 68, True)}</div>
  {t}{bar()}'''
    else:
        tw, th = int(270 * K), int(380 * K); gap = int(36 * K); x0 = (1080 - 3 * tw - 2 * gap) // 2; y0 = Y0 + int(120 * K)
        t = "".join(f'<div style="left:{x0 + i * (tw + gap) + tw // 2}px;top:0;width:2px;height:{y0 + 20 + i * int(40 * K)}px;background:#8a7f70"></div><div class="tag" style="left:{x0 + i * (tw + gap)}px;top:{y0 + i * int(40 * K)}px;width:{tw}px;height:{th}px;transform:rotate({(-4, 2, -2)[i]}deg)"><p class="num" style="font-size:{int(96 * K)}px;font-weight:400;margin-top:{int(30 * K)}px">{v}</p><p class="kicker" style="font-size:{int(18 * K)}px;margin-top:{int(20 * K)}px;color:#8A6A12">Чорна п’ятниця</p></div>' for i, v in enumerate(vals))
        wy = y0 + th + int(170 * K); py = wy + int(150 * K)   # the words right under the tags; the scarf rises from under the words
        body = f'''
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="left:0;right:0;top:{py}px;bottom:0;-webkit-mask-image:linear-gradient(180deg,transparent,#000 60%);mask-image:linear-gradient(180deg,transparent,#000 60%)"><img src="{PR}hratsiia-flat.webp" alt="" style="object-position:50% 50%;opacity:.9"></div>
  {header()}
  {t}
  <div class="light" style="left:64px;right:64px;top:{wy}px;z-index:4">{words("Три бирки. Одна п’ятниця.", "Яка знижка на що — на obiimy.world. Хустки, твіллі, маски для сну, резинки й подарункові набори.", 84, True)}</div>
  {bar()}'''
    ad("bf-14-tags", body, "Three paper tags on strings: 20, 30, 40; the orange scarf rising from below")
tags()

# 15 · from behind
full("bf-15-back", "tvilli-shovkovyi-sokovyti-spohady-03.jpg", "50% 30%", "Чорна п’ятниця зі спини теж гарна.",
     f"Твіллі 84 × 5 «Соковиті спогади» з «Пробудження» — у волоссі, на зап’ясті, на сумці. Твіллі: {RANGE}.", "The twilly in the hair, seen from behind", split=.6)

# 16 · close your eyes to the prices
def masks():
    ms = [("mask-enerhiia-01.jpg", "50% 50%"), ("mask-melodiia-dvokh-01.jpg", "50% 50%"), ("mask-vpevnenist-01.jpg", "50% 50%")]
    if SQ:
        col = 470; top = Y0; hgt = (Y1 - top) // 3; px = 64 + col; pw = 1080 - 64 - px
        rows = "".join(f'<div class="ph mult" style="left:{px}px;top:{top + i * hgt}px;width:{pw}px;height:{hgt}px"><img src="{PS}{f}" alt="" style="object-position:{p};transform:scale(1.5)"></div>' for i, (f, p) in enumerate(ms))
        body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;width:{col - 30}px;top:{Y0 + int(20 * K)}px;z-index:4">{words("Заплющте очі на ціни.", f"Маски для сну «Енергія», «Мелодія двох», «Впевненість» — шовк з обох боків. {RANGE}.", 72, False)}</div>
  {rows}{bar(False)}'''
    else:
        top = Y0 + int(300 * K); hgt = (Y1 - top) // 3
        rows = "".join(f'<div class="ph mult" style="left:0;right:0;top:{top + i * hgt}px;height:{hgt}px"><img src="{PS}{f}" alt="" style="object-position:{p};transform:scale({1.25 if K == 1 else 1.0}) translateX({(-6, 6, -6)[i]}%)"></div>' for i, (f, p) in enumerate(ms))
        body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0}px;z-index:4">{words("Заплющте очі на ціни.", f"Маски для сну «Енергія», «Мелодія двох», «Впевненість» — шовк з обох боків. {RANGE}.", 84, False)}</div>
  {rows}{bar(False)}'''
    ad("bf-16-masks", body, "Three sleep masks stacked on white, each a little off-centre")
masks()

# 17 · 88 centimetres of silk
full("bf-17-88", "khustka-vidnovlennia-88x88-02.jpg", "50% 15%", "88 см шовку. До −40 %.",
     f"Хустка «Відновлення» 88 × 88 із «Дикої стихії». Хустки 44 · 65 · 88 см: {RANGE}.", "The big pink shawl in the field", split=.6)

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · Black Friday</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;600&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("bf" + ("" if FORMAT == "plain" else "-" + FORMAT) + ".html")).write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "Black Friday banners", FORMAT)
