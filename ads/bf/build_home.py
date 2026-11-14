"""Black Friday banners for the home page of obiimy.world (14.11.2026, «сделаем ещё варианты баннера на главную для чёрной пятницы»).
The Horoshop sizes of the SOLO and Edem home banners: Desktop LINE 1 3840 × 1152 (10:3, drawn at 1920 × 576) and Mobile LINE 1
3840 × 1536 (5:2, drawn at 1920 × 768), both rendered at DPR 2. The voice and the palette of the Black Friday series (ads/bf):
ink #141110, cream text, yellow #F2B705 only for the discount, no dates and no struck prices — the discount is the series' own
«−20…−40 %» / «Знижки до −40 %» (which product gets how much is not decided). Photos: obiimy.world and the campaign shoots as they
are, nothing from SOLO. The lock-up sits at the left, the picture melts into the field at the right (the technique of the chosen
SOLO banner); the drawn button «До знижок» — Horoshop banners are plain pictures with a link.
  python3 bf/build_home.py                                                       → bf/home.html
  cd ads && DPR=2 VW=2000 ADS=bf/home.html OUT=bf/out-home node render.mjs       → out-home/bfh-*.jpg (3840 × 1152 / 3840 × 1536)
  python3 bf/build_home.py finish                                                → out-home/final/*.jpg|webp named by placement"""
import pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "solo"))
from common import nbh, YEL, INK, CREAM, PILL, PS, PR
from kit import GRAIN

LB = PR + "lookbook/"
CTA = "До знижок"
SMALL = "Шовк з авторськими принтами: хустки, твіллі, маски для сну, резинки й подарункові набори."

CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #666; font-family: 'Montserrat', sans-serif; -webkit-font-smoothing: antialiased; }
.ad { width: 1920px; height: 576px; position: relative; overflow: hidden; background: INK; margin: 20px auto; color: CREAM; }
.ad.mobile { height: 768px; }
.ad > * { position: absolute; margin: 0; }
.ad p { margin: 0; }
.ad::after { content: ""; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: .18; mix-blend-mode: soft-light; background-image: GRAIN; }
.ph { overflow: hidden; } .ph img { width: 100%; height: 100%; object-fit: cover; display: block; }
.lock { left: 84px; top: 50%; transform: translateY(-50%); width: 820px; line-height: 1; z-index: 10; }
.lock .k { font-family: 'Onest', 'Montserrat', sans-serif; font-size: 22px; font-weight: 600; letter-spacing: .22em; text-transform: uppercase; color: #9A9088; }
.lock .big { margin-top: 18px; font-weight: 400; font-size: 84px; line-height: 1.04; letter-spacing: -.01em; text-wrap: balance; }
.lock .big em { font-style: normal; color: YEL; } .lock .big .g { color: #9A9088; }
.lock .num { margin-top: 10px; font-weight: 300; font-size: 176px; line-height: .92; letter-spacing: -.04em; color: YEL; white-space: nowrap; font-variant-numeric: tabular-nums; }
.lock .num span { font-size: .5em; letter-spacing: 0; } .lock .num i { font-style: normal; margin: 0 .05em; }
.tag.y { background: YEL; } .tag.y::before { box-shadow: inset 0 0 0 3px #c99a0a; }
.lock .small { margin-top: 22px; font-family: 'EB Garamond', serif; font-weight: 500; font-size: 31px; line-height: 1.25; color: #D9CDB9; max-width: 720px; text-wrap: pretty; }
.lock .row { display: flex; align-items: center; gap: 16px; margin-top: 30px; }
.lock .pill.xl { font-size: 34px; padding: 20px 34px; } .lock .more.xl { font-size: 32px; padding: 18px 32px 18px 34px; }
.lock .pill { display: inline-block; font-size: 26px; font-weight: 500; letter-spacing: .01em; padding: 17px 28px; border-radius: 999px; background: YEL; color: INK; line-height: 1; white-space: nowrap; }
.lock .more { display: flex; align-items: center; gap: 10px; font-size: 26px; font-weight: 500; letter-spacing: .02em; padding: 15px 28px 15px 30px; border: 1.5px solid rgba(243,234,219,.8); border-radius: 999px; color: CREAM; line-height: 1; white-space: nowrap; }
.lock .more::after, p.more::after { content: "→"; font-weight: 400; font-size: 24px; line-height: 1; transform: translateY(-1px); }
.yellow { background: YEL; color: #1B1613; } .yellow .lock .k { color: #8A6A12; } .yellow .lock .small { color: #4B423B; }
.yellow .lock .pill { background: INK; color: CREAM; } .yellow .lock .more { color: #1B1613; border-color: rgba(27,22,19,.75); }
.card { background: #fff; box-shadow: 0 40px 80px -24px rgba(0,0,0,.7), 0 6px 14px rgba(0,0,0,.3); } .card img { width: 100%; height: 100%; object-fit: cover; display: block; }
.tag { background: #F6F0E4; color: INK; border-radius: 10px; box-shadow: 0 24px 50px -20px rgba(0,0,0,.8); display: flex; flex-direction: column; align-items: center; justify-content: center; }
.tag::before { content: ""; position: absolute; top: 12px; left: 50%; width: 14px; height: 14px; margin-left: -7px; border-radius: 50%; background: INK; box-shadow: inset 0 0 0 3px #d9cfbd; }
.tag .n { font-weight: 400; font-size: 72px; line-height: 1; letter-spacing: -.03em; margin-top: 22px; font-variant-numeric: tabular-nums; }

.lock.r { left: auto; right: 84px; text-align: right; } .lock.r .row { justify-content: flex-end; } .lock.r .small { margin-left: auto; }
.lock.c { left: 50%; transform: translate(-50%, -50%); text-align: center; } .lock.c .row { justify-content: center; } .lock.c .small { margin: 22px auto 0; }
.lock .num .do { font-size: .42em; font-weight: 400; letter-spacing: 0; margin-right: .12em; vertical-align: .55em; color: #F3EADB; }
.yellow .lock .num { color: #141110; } .yellow .lock .num .do { color: #4B423B; }
.tk { background: #F2B705; color: #141110; border-radius: 22px; padding: 44px 52px; line-height: 1; } .tk::before, .tk::after { content: ""; position: absolute; top: 57%; width: 44px; height: 44px; margin-top: -22px; border-radius: 50%; background: #141110; } .tk::before { left: -22px; } .tk::after { right: -22px; }
.tk .k { font-family: 'Onest', sans-serif; font-size: 20px; font-weight: 600; letter-spacing: .22em; text-transform: uppercase; color: #8A6A12; }
.tk .num { font-weight: 300; font-size: 150px; letter-spacing: -.04em; line-height: .92; margin-top: 14px; white-space: nowrap; } .tk .num span { font-size: .5em; letter-spacing: 0; }
.tk .more { display: inline-flex; align-items: center; gap: 10px; margin-top: 26px; font-size: 26px; font-weight: 500; letter-spacing: .02em; padding: 15px 28px 15px 30px; border: 1.5px solid rgba(27,22,19,.75); border-radius: 999px; color: #141110; line-height: 1; white-space: nowrap; }
.tk .l { font-family: 'EB Garamond', serif; font-weight: 500; font-size: 28px; color: #4B423B; margin-top: 18px; border-top: 1.5px dashed rgba(27,22,19,.35); padding-top: 18px; }
.panel { background: rgba(20,17,16,.96); }
.tag .t { font-family: 'Onest', sans-serif; font-size: 14px; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; margin-top: 16px; color: #8A6A12; }
""".replace("GRAIN", GRAIN).replace("CREAM", CREAM).replace("INK", INK).replace("YEL", YEL)

ads = []
def ad(id, body, cls="", note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad {cls}" id="{id}">{body}\n</section>')

def _rgb(c): return f"{int(c[1:3], 16)},{int(c[3:5], 16)},{int(c[5:7], 16)}"

DO40 = '<span class="do">до</span>−40<span> %</span>'
RNG = '−20<i>…</i>−40<span> %</span>'
def lock(big=None, small=SMALL, kicker="Чорна п’ятниця · знижки на шовк", num=None, pill=PILL, more=CTA, k=1.0, width=820, side="l", bigsize=None, numsize=None, xl=False):
    """The words: kicker, headline (or the huge number), the serif line, the yellow pill and the outlined button; side l / r / c."""
    cls = {"l": "lock", "r": "lock r", "c": "lock c"}[side]
    inner = f'<div class="{cls}" style="position:absolute;width:{width}px"><p class="k">{kicker}</p>'
    ns = f' style="font-size:{numsize}px"' if numsize else ""
    if num: inner += f'<p class="num"{ns}>{num}</p>'
    bs = f' style="font-size:{bigsize}px"' if bigsize else ""
    if big: inner += f'<p class="big"{bs}>{nbh(big)}</p>'
    if small: inner += f'<p class="small">{nbh(small)}</p>'
    x = " xl" if xl else ""
    inner += '<div class="row">' + (f'<p class="pill{x}">{pill}</p>' if pill else "") + (f'<p class="more{x}">{more}</p>' if more else "") + '</div></div>'
    if k == 1: return inner
    if side == "r": return f'<div style="position:absolute;right:0;top:0;bottom:0;width:{width + 84}px;transform:scale({k});transform-origin:100% 50%">{inner}</div>'
    if side == "c": return f'<div style="position:absolute;left:0;right:0;top:0;bottom:0;transform:scale({k});transform-origin:50% 50%">{inner}</div>'
    return f'<div style="position:absolute;left:0;top:0;bottom:0;width:{width + 84}px;transform:scale({k});transform-origin:0 50%">{inner}</div>'

def feathered(src, left, feather, pos, field=INK, zoom=1.0, origin="50% 50%"):
    """The picture from `left` to the right edge, melting into the field over `feather` px — no hard edge."""
    return (f'<div class="ph" style="left:{left}px;right:0;top:0;bottom:0;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 {feather}px);mask-image:linear-gradient(90deg,transparent 0,#000 {feather}px)"><img src="{src}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>'
            f'<div style="left:{left}px;top:0;bottom:0;width:{int(feather * .9)}px;background:linear-gradient(90deg,{field} 0,rgba({_rgb(field)},.15) 40%,rgba({_rgb(field)},0) 100%)"></div>')

def feathered_l(src, right, feather, pos, field=INK, zoom=1.0, origin="50% 50%"):
    """The picture from the left edge to `right`, melting into the field over `feather` px at its right side."""
    return (f'<div class="ph" style="left:0;width:{right}px;top:0;bottom:0;-webkit-mask-image:linear-gradient(270deg,transparent 0,#000 {feather}px);mask-image:linear-gradient(270deg,transparent 0,#000 {feather}px)"><img src="{src}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>'
            f'<div style="left:{right - int(feather * .9)}px;top:0;bottom:0;width:{int(feather * .9)}px;background:linear-gradient(270deg,{field} 0,rgba({_rgb(field)},.15) 40%,rgba({_rgb(field)},0) 100%)"></div>')

def tiles(frames, left, w, gap, H, fade=200):
    """Portrait frames in a row from `left` to the right edge, the first one melting into the ink; `w` — one width or a list."""
    ws = w if isinstance(w, list) else [w] * len(frames); out = ""; x = left
    for (f, p), wi in zip(frames, ws):
        out += f'<div class="ph" style="left:{x}px;top:0;width:{wi}px;height:{H}px"><img src="{f}" alt="" style="object-position:{p}"></div>'; x += wi + gap
    return out + f'<div style="left:{left}px;top:0;bottom:0;width:{fade}px;background:linear-gradient(90deg,{INK} 0,rgba(20,17,16,.6) 45%,rgba(20,17,16,0) 100%)"></div>'

def both(id, build, note="", cls=""):
    """Each variant in two frames: desktop 1920 × 576 and the 5:2 mobile 1920 × 768 (the lock-up a fifth larger)."""
    ad(id, build(576, False), cls=cls, note=note)
    ad(id + "-mobile", build(768, True), cls=(cls + " mobile").strip(), note=note + " · mobile 5:2")

# 01 · the hero of the series: the day's name small, the range in yellow huge, three silk frames in a strip at the right
def v_hero(H, mob):
    fr = [(PS + "khustka-vidnovlennia-88x88-02.jpg", "62% 20%"), (PS + "tvilli-shovkovyi-sokovyti-spohady-02.jpg", "50% 30%"), (PS + "mask-vpevnenist-04.jpg", "56% 30%" if not mob else "55% 30%")]
    w = [356] * 3 if not mob else [290, 290, 400]; left = 1920 - sum(w) - 2 * 6
    return f'''
  <div style="inset:0;background:{INK}"></div>
  {tiles(fr, left, w, 6, H, fade=170 if not mob else 140)}
  {lock(num='−20<i>…</i>−40<span> %</span>', small=SMALL, pill=None, k=1.12 if mob else 1, width=820 if not mob else 720)}'''
both("bfh-01-hero", v_hero, "The hero: the range in yellow, three silk frames in a strip")

# 02 · «Чорна п’ятниця. Червона хустка.» — the Riviera frame
def v_red(H, mob):
    return f'''
  <div style="inset:0;background:{INK}"></div>
  {feathered(PR + "riviera-red.jpg", 900 if not mob else 820, 420 if not mob else 460, "50% 25%" if not mob else "50% 26%")}
  {lock('<span class="g">Чорна п’ятниця.</span><br><em style="color:#E24B3B">Червона</em> хустка.', "Хустки чотирьох колекцій зі знижкою. Шовк, авторський принт, ручна обробка краю.", k=1.2 if mob else 1)}'''
both("bfh-02-red", v_red, "The red scarf, the Riviera frame")

# 03 · «Квадрат. Не чорний.» — the flat scarf as a tilted card on the black field
def v_square(H, mob):
    cs = 624 if not mob else 740; cx = 1140 if not mob else 1100; cy = (H - cs) // 2
    return f'''
  <div style="inset:0;background:{INK}"></div>
  <div class="card" style="left:{cx}px;top:{cy}px;width:{cs}px;height:{cs}px;transform:rotate(-3deg);z-index:3"><img src="{PS}khustka-flat-kolo-sontsia-88x88-01.jpg" alt=""></div>
  {lock("Квадрат. Не чорний.", "Хустка 88 × 88 см «Коло сонця» зі «Співочої душі» — і всі принти чотирьох колекцій зі знижкою.", k=1.2 if mob else 1)}'''
both("bfh-03-square", v_square, "Malevich's square, only in silk")

# 04 · «У нас п’ятниця жовта.» — the brand's yellow instead of black, the yellow box with the dotted scarf
def v_yellow(H, mob):
    return f'''
  <div style="inset:0;background:{YEL}"></div>
  {feathered(PR + "box-dots.jpg", 820 if not mob else 880, 420, "58% 44%" if not mob else "58% 70%", field=YEL, zoom=1.09, origin="0 50%")}
  {lock("У нас п’ятниця жовта.", "Жовтий — наш колір. Чорний — лише назва п’ятниці. Знижки на шовк з авторськими принтами.", kicker="Знижки на шовк", k=1.2 if mob else 1)}'''
both("bfh-04-yellow", v_yellow, "The brand's yellow instead of black", cls="yellow")

# 05 · «Усі обличчя Чорної п’ятниці.» — four lookbook portraits in a row
def v_faces(H, mob):
    fr = [(LB + "lb47-49-L.webp", "50% 6%"), (LB + "lb07-08-L.webp", "50% 0%"), (LB + "lb43-45-L.webp", "50% 8%"), (LB + "lb26-28-R.webp", "50% 6%")]
    w = 250 if not mob else 240; left = 1920 - 4 * w - 3 * 6
    return f'''
  <div style="inset:0;background:{INK}"></div>
  {tiles(fr, left, w, 6, H, fade=150)}
  {lock("Усі обличчя Чорної п’ятниці.", "Хустки, твіллі, маски для сну<br>й подарункові набори — зі знижкою.", kicker="Знижки на шовк", k=1.2 if mob else 1)}'''
both("bfh-05-faces", v_faces, "Four lookbook portraits in a row")

# 06 · «Три бирки. Одна п’ятниця.» — three paper tags on strings, the orange scarf rising from below at the right
def v_tags(H, mob):
    tw, th = (230, 320) if not mob else (240, 340); gap = 60 if not mob else 50; x0 = 1920 - 84 - 3 * tw - 2 * gap; y0 = 70 if not mob else 110
    t = "".join(f'<div style="left:{x0 + i * (tw + gap) + tw // 2}px;top:0;width:2px;height:{y0 + 20 + i * 34}px;background:#8a7f70;z-index:2"></div>'
                f'<div class="tag{" y" if i == 2 else ""}" style="left:{x0 + i * (tw + gap)}px;top:{y0 + i * 34}px;width:{tw}px;height:{th}px;transform:rotate({(-4, 2, -2)[i]}deg);z-index:3"><p class="n">{v}</p><p class="t">Чорна п’ятниця</p></div>'
                for i, v in enumerate(["−20 %", "−30 %", "−40 %"]))
    return f'''
  <div style="inset:0;background:{INK}"></div>
  <div style="left:{x0 - 60}px;right:0;top:{int(H * .42)}px;bottom:0;-webkit-mask-image:linear-gradient(180deg,transparent,#000 75%);mask-image:linear-gradient(180deg,transparent,#000 75%)"><div class="ph" style="position:absolute;inset:0;-webkit-mask-image:linear-gradient(90deg,transparent,#000 200px);mask-image:linear-gradient(90deg,transparent,#000 200px)"><img src="{PR}hratsiia-flat.webp" alt="" style="object-position:50% 40%;opacity:.85;transform:scale(1.12)"></div></div>
  {t}
  {lock("Три бирки. Одна п’ятниця.", "Яка знижка на що — у каталозі. Хустки, твіллі, маски для сну, резинки й набори.", pill=None, k=1.2 if mob else 1, width=820 if not mob else 660)}'''
both("bfh-06-tags", v_tags, "Three paper tags: 20, 30, 40")

# 07 · «Проспати Чорну п’ятницю? Можна.» — the sleep mask
def v_sleep(H, mob):
    return f'''
  <div style="inset:0;background:{INK}"></div>
  {feathered(PS + "mask-nizhnist-03.jpg", 900 if not mob else 880, 420 if not mob else 440, "30% 40%" if not mob else "30% 34%")}
  {lock("Проспати Чорну п’ятницю? Можна. У шовковій масці.", "Маски для сну з авторськими принтами — зі знижкою. І хустки, твіллі, резинки й набори теж.", kicker="Знижки на шовк", k=1.2 if mob else 1)}'''
both("bfh-07-sleep", v_sleep, "The sleep mask")

# 08 · «Листопад темний. Хустка — ні.» — «Коло сонця» on the model
def v_kolo(H, mob):
    return f'''
  <div style="inset:0;background:{INK}"></div>
  {feathered(PR + "kolo-2.webp", 900 if not mob else 940, 440, "62% 8%", zoom=1.2, origin="0 50%")}
  {lock("Листопад темний. Хустка — ні.", "На ній — «Коло сонця» зі «Співочої душі». Хустки чотирьох колекцій зі знижкою: шовк, авторський принт, ручна обробка краю.", kicker="Чорна п’ятниця", k=1.2 if mob else 1)}'''
both("bfh-08-kolo", v_kolo, "The sun scarf against the dark month")


# ---- the second batch (14.11, «ещё варианты со скидками и фото, больше разнообразия»): other layouts — the photo at the left, the words
#      at the right or in the middle, a mosaic, a hard split, a coupon, a full-bleed frame with a veil; the number is the hero on most
# 09 · the open back — the photo at the left, the words at the right
def v_back(H, mob):
    return f'''
  <div style="inset:0;background:{INK}"></div>
  {feathered_l(PR + "enerhiia-back.webp", 1060 if not mob else 1000, 420, "50% 2%")}
  {lock("Відкрита спина. Відкриті знижки.", "Хустка «Енергія» у волоссі — і всі хустки, твіллі, маски для сну й набори зі знижкою.", num=None, side="r", k=1.2 if mob else 1, width=780, xl=True)}'''
both("bfh-09-back", v_back, "The open back: the photo at the left, the words at the right")

# 10 · the mosaic was dropped after the panel (the faces under the number read as a broken banner)

# 11 · «Ціни присіли.» — the crouching model with the red scarf, the number large
def v_sat(H, mob):
    return f'''
  <div style="inset:0;background:{INK}"></div>
  {feathered(LB + "lb40-42-R.webp", 860 if not mob else 900, 460, "50% 9%")}
  {lock("Ціни присіли.", "На хустки, твіллі, маски для сну, резинки й подарункові набори чотирьох колекцій.", num=RNG, kicker="Чорна п’ятниця", pill=None, k=1.15 if mob else 1, bigsize=64)}'''
both("bfh-11-sat", v_sat, "«Ціни присіли.» with the range large")

# 12 · the yellow field with the number in ink: small «до», huge «−40 %»; the yellow box with the red scarf at the right
def v_ynum(H, mob):
    return f'''
  <div style="inset:0;background:{YEL}"></div>
  {feathered(PR + "box-red-1200.webp", 900 if not mob else 940, 420, "50% 50%" if not mob else "50% 62%", field=YEL, zoom=1.06, origin="0 50%")}
  {lock("Знижки на шовк.", "Хустки, твіллі, маски для сну, резинки й подарункові набори з авторськими принтами.", num=DO40, kicker="Чорна п’ятниця", pill=None, k=1.15 if mob else 1, bigsize=56)}'''
both("bfh-12-ynum", v_ynum, "Yellow field, «до −40 %» in ink, the box with the red scarf", cls="yellow")

# 13 · three flat scarves as tilted cards fanned at the right
def v_cards(H, mob):
    cs = 400 if not mob else 500; cy = (H - cs) // 2; x0 = 1060 if not mob else 1000; step = 270 if not mob else 300
    cards = "".join(f'<div class="card" style="left:{x0 + i * step}px;top:{cy + dy}px;width:{cs}px;height:{cs}px;transform:rotate({r}deg);z-index:{3 + i}"><img src="{src}" alt=""></div>'
                    for i, (src, r, dy) in enumerate([(PR + "mizh-flat.webp", -7, 10), (PS + "khustka-flat-smilyvist-44x44-01.jpg", 2, -14), (PS + "khustka-flat-kolo-sontsia-88x88-01.jpg", 8, 12)]))
    return f'''
  <div style="inset:0;background:{INK}"></div>
  {cards}
  {lock("Не чорні. Зі знижкою.", "Хустки чотирьох колекцій: біла «Між нами», жовта «Сміливість», «Коло сонця» — і решта принтів.", k=1.2 if mob else 1, width=820 if not mob else 700, xl=True)}'''
both("bfh-13-cards", v_cards, "Three flat scarves as tilted cards")

# 14 · a hard split: the yellow block with the range at the left, the photo at the right, no feather
def v_split(H, mob):
    pw = 720 if not mob else 920   # the photo at the left, the model looks toward the words; the yellow block with the range at the right
    return f'''
  <div style="inset:0;background:{YEL}"></div>
  <div class="ph" style="left:0;top:0;bottom:0;width:{pw}px"><img src="{PR}dotyk-2.webp" alt="" style="object-position:50% 0%"></div>
  <div class="yellow" style="left:{pw}px;right:0;top:0;bottom:0;background:transparent">{lock("Чорна п’ятниця.", "Шовк з авторськими принтами: хустки, твіллі, маски для сну, резинки й набори.", num=RNG, kicker="Знижки на шовк", pill=None, k=1.0 if not mob else 1.12, width=820, bigsize=60, side="r")}</div>'''
both("bfh-14-split", v_split, "A hard split: the photo at the left, the yellow block with the range at the right")

# 15 · the white headscarf frame was dropped after the panel (a phone frame with other brands’ logos in it)

# 16 · a yellow coupon with the range at the left, the blue twilly bow at the right
def v_ticket(H, mob):
    k = 1.15 if mob else 1
    tk = (f'<div class="tk" style="position:absolute;left:84px;top:50%;transform:translateY(-50%)"><p class="k">Чорна п’ятниця · знижки на шовк</p><p class="num">−20<i>…</i>−40<span> %</span></p>'
          f'<p class="l">Хустки · твіллі · маски для сну · резинки · набори</p><p class="more">{CTA}</p></div>')
    wrap = tk if k == 1 else f'<div style="left:0;top:0;bottom:0;width:900px;transform:scale({k});transform-origin:0 50%">{tk}</div>'
    return f'''
  <div style="inset:0;background:{INK}"></div>
  {feathered(PR + "vyr-2.webp", 1000 if not mob else 1000, 440, "50% 46%")}
  {wrap}'''
both("bfh-16-ticket", v_ticket, "A yellow coupon with the range, the pink scarf on the back")

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · Black Friday home banners</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;600&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"

if "finish" in sys.argv:
    from PIL import Image
    src = HERE / "out-home"; out = src / "final"; out.mkdir(exist_ok=True)
    for f in sorted(src.glob("bfh-*.jpg")):
        mob = f.stem.endswith("-mobile"); base = f.stem.replace("-mobile", "")
        im = Image.open(f).convert("RGB"); size = (3840, 1536) if mob else (3840, 1152)
        if im.size != size: im = im.resize(size, Image.LANCZOS)
        name = f"{base}-{'mobile-line1-3840x1536' if mob else 'desktop-line1-3840x1152'}"
        im.save(out / f"{name}.jpg", "JPEG", quality=90, optimize=True, progressive=True)
        im.save(out / f"{name}.webp", "WEBP", quality=86, method=6)
        print(name, im.size, (out / f"{name}.jpg").stat().st_size // 1024, "KB jpg", (out / f"{name}.webp").stat().st_size // 1024, "KB webp")
else:
    (HERE / "home.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
    print(len(ads), "black friday home frames")
