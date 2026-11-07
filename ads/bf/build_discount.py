"""Black Friday, the third series (07.11.2026, client: «ещё варианты и с акцентом на скидку»). The number is the hero: «до −40 %»
and «−20…−40 %» huge over the campaign photographs with models, digits filled with the silk print itself, yellow stickers and
price tags, the three tiers −20 / −30 / −40 as a column. The discount stays the client's range — «до −40 %» or «−20…−40 %» —
never a percentage pinned to one product (the big number always carries «до» or the whole range). Photos: obiimy.world as they
are, nothing from SOLO. Output: bfd[-<format>].html → out-discount[-<format>]/*.jpg
(cd ads && ADS=bf/bfd.html OUT=bf/out-discount node render.mjs)."""
import pathlib, re
from common import *
HERE = pathlib.Path(__file__).parent
LB = "lookbook/"; ST = "site/"
CATS = "Хустки · твіллі · маски · набори"
LINE = "Чорна п’ятниця на шовк із авторськими принтами — хустки, твіллі, маски для сну, набори."
BIGF = "font-family:'Montserrat',sans-serif;font-weight:300;line-height:.9;letter-spacing:-.04em;font-variant-numeric:tabular-nums;white-space:nowrap;"

def do40(size, color=YEL, do="до"):
    """«до −40 %» — the small word before the big number, so the number never reads as one product's price cut."""
    return (f'<p style="{BIGF}font-size:{int(size * K)}px;color:{color}"><span style="font-size:.26em;font-weight:500;letter-spacing:.08em;vertical-align:.95em;margin-right:.35em">{do}</span>'
            f'−40<span style="font-size:.5em;letter-spacing:0;margin-left:.08em"> %</span></p>')

def rng(size, color=YEL):
    return f'<p style="{BIGF}font-size:{int(size * K)}px;color:{color}">−20…−40<span style="font-size:.5em;letter-spacing:0"> %</span></p>'

def kick(text, color=CREAM, size=24):
    return f'<p class="kicker" style="font-size:{int(size * K)}px;color:{color}">{nb(text)}</p>'

# ─── templates ─────────────────────────────────────────────────────────────────────────────────────────────────────────

def giant(id, img, pos, small, note="", num="do", zoom=1.0, origin="50% 50%", veil=.45, size=330, lead="Чорна п’ятниця · знижки на шовк"):
    """The photograph fills the frame; the number — huge, yellow, thin — stands at the bottom on the dark gradient."""
    numh = do40(size) if num == "do" else rng(size * .62)
    if SQ:
        pw = 560
        body = f'''
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="left:0;top:0;width:{pw}px;height:{H}px"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:{pw - 160}px;top:0;width:160px;height:{H}px;background:linear-gradient(90deg,rgba(20,17,16,0),{INK})"></div>
  {header()}
  <div class="light" style="left:{pw - 50}px;right:64px;top:{Y0 + int(40 * K)}px;z-index:4">{kick(lead, YEL)}<div style="margin-top:{int(16 * K)}px">{do40(size * .66) if num == "do" else rng(size * .42)}</div>
    <p class="small" style="font-size:{int(34 * K)}px;margin-top:{int(22 * K)}px">{nb(small)}</p></div>
  {bar(label=CATS)}'''
    else:
        body = f'''
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="inset:0"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:0;right:0;top:0;height:{int(280 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,{veil}),rgba(12,9,8,0))"></div>
  <div style="left:0;right:0;bottom:0;height:{int(H * .6)}px;background:linear-gradient(0deg,rgba(20,17,16,1) 0,rgba(20,17,16,.96) 30%,rgba(20,17,16,.5) 66%,rgba(20,17,16,0) 100%)"></div>
  {header()}
  <div class="light" style="left:64px;right:64px;bottom:{H - Y1}px;z-index:4">{kick(lead, YEL)}<div style="margin-top:{int(10 * K)}px">{numh}</div>
    <p class="small" style="font-size:{int(36 * K)}px;margin-top:{int(18 * K)}px;max-width:900px">{nb(small)}</p></div>
  {bar(label=CATS)}'''
    ad(id, body, note)

def band(id, img, pos, small, note="", zoom=1.0, split=.4, origin="50% 50%"):
    """The top half yellow with the range in ink, the photograph below with a hard edge — a poster."""
    if SQ:
        pw = 540
        body = f'''
  <div style="inset:0;background:{YEL}"></div>
  <div class="ph" style="left:{pw}px;top:0;width:{1080 - pw}px;height:{H}px"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  {header(False)}
  <div class="ink" style="left:64px;width:{pw - 100}px;top:{Y0 + int(50 * K)}px;z-index:4">{kick("Чорна п’ятниця", INK)}
    <p style="{BIGF}font-size:{int(150 * K)}px;color:{INK};margin-top:{int(14 * K)}px;line-height:.95">−20…<br>−40<span style="font-size:.5em;letter-spacing:0"> %</span></p>
    <p class="small" style="font-size:{int(32 * K)}px;margin-top:{int(22 * K)}px;color:#4B3F10">{nb(small)}</p></div>
  <div style="left:64px;bottom:{BOTB}px;height:{BAR}px;display:flex;align-items:center;z-index:6"><span class="pill" style="background:{INK};color:{YEL};font-size:{int(30 * K)}px;padding:{int(20 * K)}px {int(36 * K)}px">obiimy.world</span></div>'''
    else:
        yb = int(H * split)
        body = f'''
  <div style="inset:0;background:{YEL}"></div>
  <div class="ph" style="left:0;right:0;top:{yb}px;bottom:0"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:0;right:0;bottom:0;height:{int(360 * K)}px;background:linear-gradient(0deg,rgba(20,17,16,.85),rgba(20,17,16,0))"></div>
  {header(False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0 + int(30 * K)}px;z-index:4">{kick("Чорна п’ятниця", INK)}
    <p style="{BIGF}font-size:{int(198 * K)}px;color:{INK};margin-top:{int(14 * K)}px">−20…−40<span style="font-size:.5em;letter-spacing:0"> %</span></p>
    <p class="small" style="font-size:{int(36 * K)}px;margin-top:{int(18 * K)}px;color:#4B3F10;max-width:880px">{nb(small)}</p>
    <span class="pill" style="position:static;margin-top:{int(34 * K)}px;background:{INK};color:{YEL};font-size:{int(30 * K)}px;padding:{int(18 * K)}px {int(34 * K)}px">{nb(CATS)}</span></div>
  <div class="light" style="left:64px;right:64px;bottom:{BOTB}px;height:{BAR}px;display:flex;align-items:center;justify-content:flex-end;z-index:6">
    <span class="hdr" style="font-size:{int(26 * K)}px;color:{CREAM};letter-spacing:.1em;text-transform:none">obiimy.world</span></div>'''
    ad(id, body, note)

def clip(id, img, small, note="", pos="50% 50%", big="Чорна п’ятниця — з принтом.", root=True, bgsize="cover"):
    """The digits filled with the silk itself: «40» as a window onto the print, on the black field."""
    src = (PR if root else PS) + img
    dsz = int((520 if not SQ else 380) * K)
    digits = (f'<p style="font-family:Montserrat,sans-serif;font-weight:500;line-height:.86;letter-spacing:-.06em;font-size:{dsz}px;white-space:nowrap;'
              f'background:url({src}) {pos}/{bgsize};-webkit-background-clip:text;background-clip:text;color:transparent;filter:saturate(1.1)">40</p>')
    sign = f'<span class="kicker" style="font-size:{int(dsz * .085)}px;color:{CREAM};margin-right:{int(dsz * .04)}px;padding-bottom:{int(dsz * .1)}px">до</span><span style="{BIGF}font-size:{int(dsz * .3)}px;color:{YEL};font-weight:400">−</span>'
    pct = f'<span style="{BIGF}font-size:{int(dsz * .3)}px;color:{YEL};font-weight:400">%</span>'
    if SQ:
        body = f'''
  <div style="inset:0;background:{INK}"></div>
  {header()}
  <div class="light" style="left:64px;top:{Y0 + int(40 * K)}px;z-index:4">{kick("Чорна п’ятниця · знижки", YEL)}
    <div style="display:flex;align-items:flex-end;gap:{int(10 * K)}px;margin-top:{int(6 * K)}px">{sign}{digits}{pct}</div></div>
  <div class="light" style="left:64px;right:64px;top:{Y0 + int(40 * K) + dsz + int(90 * K)}px;z-index:4"><p class="big" style="font-size:{int(56 * K)}px">{nbh(big)}</p><p class="small" style="font-size:{int(30 * K)}px;margin-top:{int(14 * K)}px">{nb(small)}</p></div>
  {bar(label=CATS)}'''
    else:
        body = f'''
  <div style="inset:0;background:{INK}"></div>
  {header()}
  <div class="light" style="left:64px;top:{Y0 + int(60 * K)}px;z-index:4">{kick("Чорна п’ятниця · знижки", YEL)}
    <div style="display:flex;align-items:flex-end;gap:{int(12 * K)}px;margin-top:{int(8 * K)}px">{sign}{digits}{pct}</div></div>
  <div class="light" style="left:64px;right:64px;top:{Y0 + int(60 * K) + dsz + int(150 * K)}px;bottom:{H - Y1}px;z-index:4"><p class="big" style="font-size:{int(76 * K)}px">{nbh(big)}</p><p class="small" style="font-size:{int(36 * K)}px;margin-top:{int(20 * K)}px">{nb(small)}</p></div>
  {bar(label=CATS)}'''
    ad(id, body, note)

def sticker(id, img, pos, big, small, note="", zoom=1.0, origin="50% 50%", split=.6, tilt=-12, top_veil=.4, at="right"):
    """The `full` layout with a round yellow sticker «до −40 %» sitting on the seam between the photograph and the field."""
    d = int(400 * K)
    inner = (f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:{INK};transform:rotate({tilt}deg)">'
             f'<span style="{BIGF}font-size:{int(124 * K)}px;font-weight:400"><span style="font-size:.34em;font-weight:500;letter-spacing:.06em;vertical-align:.9em;margin-right:.3em">до</span>−40<span style="font-size:.5em;letter-spacing:0"> %</span></span>'
             f'<span class="kicker" style="font-size:{int(18 * K)}px;letter-spacing:.2em;margin-top:{int(14 * K)}px;color:#6b5a14">Чорна п’ятниця</span></div>')
    if SQ:
        full(id, img, pos, big, small, note, dark=True, size=76, root=True, zoom=zoom, label=CATS, origin=origin)
        sx, sy = 540 - d - 40, H - BOTB - BAR - d - int(20 * K)
        ads[-1] = ads[-1].replace("\n</section>", f'\n  <div style="left:{sx}px;top:{sy}px;width:{d}px;height:{d}px;border-radius:50%;background:{YEL};box-shadow:0 30px 60px -20px rgba(0,0,0,.7);z-index:7">{inner}</div>\n</section>')
    else:
        full(id, img, pos, big, small, note, dark=True, size=76, root=True, split=split, zoom=zoom, label=CATS, top_veil=top_veil, origin=origin)
        yph = int(H * split); sx = (1080 - 64 - d) if at == "right" else 64; sy = yph - d + int(40 * K)
        ads[-1] = ads[-1].replace("\n</section>", f'\n  <div style="left:{sx}px;top:{sy}px;width:{d}px;height:{d}px;border-radius:50%;background:{YEL};box-shadow:0 30px 60px -20px rgba(0,0,0,.7);z-index:7">{inner}</div>\n</section>')

def tiers(id, img, pos, small, note="", zoom=1.0, origin="50% 50%"):
    """The three steps −20 / −30 / −40 as a column on the black field; the photograph takes the rest."""
    col = 440 if not SQ else 400
    nums = "".join(f'<p style="{BIGF}font-size:{int((196 if not SQ else 128) * K)}px;color:{YEL if i == 2 else CREAM};opacity:{(.7, .85, 1)[i]};margin-top:{int(14 * K) if i else 0}px">−{n}<span style="font-size:.5em;letter-spacing:0"> %</span></p>' for i, n in enumerate((20, 30, 40)))
    body = f'''
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="left:{col}px;top:0;right:0;height:{H}px"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:{col}px;top:0;width:{int(180 * K)}px;height:{H}px;background:linear-gradient(90deg,{INK},rgba(20,17,16,0))"></div>
  <div style="left:0;right:0;top:0;height:{int(200 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,.5),rgba(12,9,8,0))"></div>
  <div style="left:{col}px;right:0;bottom:0;height:{int(520 * K)}px;background:linear-gradient(0deg,{INK},rgba(20,17,16,.9) 30%,rgba(20,17,16,0))"></div>
  {header()}
  <div class="light" style="left:64px;top:{Y0 + int(60 * K)}px;z-index:4">{kick("Чорна п’ятниця", YEL)}<div style="margin-top:{int(20 * K)}px">{nums}</div></div>
  <div class="light" style="left:64px;right:64px;bottom:{H - Y1}px;z-index:4"><p class="small" style="font-size:{int(34 * K)}px;max-width:{(1080 - 128) if not SQ else 1080 - 128}px">{nb(small)}</p></div>
  {bar(label=CATS)}'''
    ad(id, body, note)

def rows(id, img, pos, small, note="", text="Знижки до −40 % · Чорна п’ятниця · ", zoom=1.0):
    """A wall of the message in thin caps, row after row, and a portrait as a window in the middle of it."""
    rh = int(92 * K); n = H // rh + 2
    ww, wh = (int(640 * K), int(860 * K)) if not SQ else (int(520 * K), int(640 * K))
    wx, wy = (1080 - ww) // 2, Y0 + int(40 * K) + ((Y1 - Y0 - int(220 * K) - wh) // 2)
    def loud(i):   # a yellow row only where the window and the header do not cover it
        y = i * rh; return (y + rh < wy or y > wy + wh) and y > TOPL + int(70 * K) and i % 2 == 0
    lines = "".join(f'<p style="left:{-(i % 3) * 300}px;top:{i * rh}px;font-family:Montserrat,sans-serif;font-weight:400;font-size:{int(72 * K)}px;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap;color:{YEL if loud(i) else CREAM};opacity:{.95 if loud(i) else .22}">{(text * 8)}</p>' for i in range(n))
    body = f'''
  <div style="inset:0;background:{INK}"></div>
  <div style="inset:0;overflow:hidden">{lines}</div>
  <div style="inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(20,17,16,.0) 30%,rgba(20,17,16,.55) 100%)"></div>
  <div class="ph" style="left:{wx}px;top:{wy}px;width:{ww}px;height:{wh}px;box-shadow:0 50px 100px -30px rgba(0,0,0,.8);z-index:3"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  {header()}
  <div class="light" style="left:64px;right:64px;top:{wy + wh + int(40 * K)}px;bottom:{H - Y1}px;z-index:4;text-align:center"><p class="small" style="font-size:{int(34 * K)}px">{nb(small)}</p></div>
  {bar(label=CATS)}'''
    ad(id, body, note)

def tag(id, img, pos, big, small, note="", zoom=1.0, origin="50% 50%", dark=True, split=.6, tilt=9, ph_bg=None):
    """The `full` layout with a yellow price tag hanging from the top edge into the photograph."""
    tw, th = int(380 * K), int(470 * K)
    body = (f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:{INK};padding-top:{int(50 * K)}px">'
            f'<span style="{BIGF}font-size:{int(100 * K)}px;font-weight:400"><span style="font-size:.38em;font-weight:500;letter-spacing:.06em;vertical-align:.85em;margin-right:.3em">до</span>−40<span style="font-size:.5em;letter-spacing:0"> %</span></span>'
            f'<span class="kicker" style="font-size:{int(18 * K)}px;letter-spacing:.2em;margin-top:{int(26 * K)}px;color:#6b5a14">Чорна п’ятниця</span></div>')
    hole = f'<div style="position:absolute;left:50%;top:{int(28 * K)}px;width:{int(22 * K)}px;height:{int(22 * K)}px;margin-left:{-int(11 * K)}px;border-radius:50%;background:{INK};box-shadow:inset 0 0 0 {int(3 * K)}px #c9981a"></div>'
    full(id, img, pos, big, small, note, dark=dark, size=76, root=True, split=split, zoom=zoom, label=CATS, origin=origin, ph_bg=ph_bg)
    tx = (1080 - 64 - tw - 30) if not SQ else (540 - tw - 70)
    ty = int(140 * K) if not SQ else int(80 * K)
    string = f'<div style="left:{tx + tw // 2}px;top:0;width:3px;height:{ty + int(40 * K)}px;background:{YEL};opacity:.9;z-index:7;transform-origin:50% 0;transform:rotate({tilt}deg)"></div>'
    ads[-1] = re.sub(r'<p class="hdr"[^>]*>[^<]*</p>', "", ads[-1], count=1)   # the tag itself says «Чорна п’ятниця» — no header word under the string (panel r2)
    ads[-1] = ads[-1].replace("\n</section>", f'\n  {string}<div style="left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px;border-radius:{int(22 * K)}px;background:{YEL};box-shadow:0 30px 60px -20px rgba(0,0,0,.7);z-index:7;transform:rotate({tilt}deg);transform-origin:50% {-int(40 * K)}px">{hole}{body}</div>\n</section>')

# ─── the series ───────────────────────────────────────────────────────────────────────────────────────────────────────

giant("bfd-01-sat", LB + "lb40-42-R.webp", "50% 25%", LINE, "The crouching model by the columns under the giant «до −40 %»", veil=.3, zoom=1.02)
band("bfd-02-band", "probudzhennia-1.webp", "50% 0%", "Хустки, твіллі, маски для сну й набори — принти чотирьох колекцій.", "The yellow poster top, the iris scarf below", zoom=1.0)
clip("bfd-03-clip-kolo", ST + "khustka-flat-kolo-sontsia-88x88-01.jpg", "Хустка «Коло сонця» зі «Співочої душі» — і всі принти чотирьох колекцій.", "The digits 40 filled with the Circle of the Sun print", pos="40% 50%", bgsize="140%")
# bfd-04 (the sticker on the two scarves) dropped after panel round 2: the sticker had nowhere to sit without covering a scarf, and the subject is in 13
tiers("bfd-05-tiers", LB + "lb15-17-R.webp", "75% 20%", "Три кроки Чорної п’ятниці — на хустки, твіллі, маски для сну й набори. Хустка «Пробудження» на плечах.", "The three tiers in a column, the Awakening scarf on the right", zoom=1.15, origin="75% 20%")
rows("bfd-06-rows", LB + "lb24-26-L.webp", "50% 20%", "Хустка «З чистого листа» з «Дикої стихії». Знижки — на принти чотирьох колекцій.", "A wall of the message, the From Scratch portrait as a window")
tag("bfd-07-tag-back", "enerhiia-back.webp", "50% 18%", "Бирка вже висить.", "Принт «Енергія» з «Поклику душі» — на відкритій спині. Чорна п’ятниця на шовк.", "The yellow price tag hanging into the back-shot", split=.6)
giant("bfd-08-blue", "hratsiia-1.webp", "50% 5%", "Хустка «Грація» з «Дикої стихії» — як пояс. " + LINE, "The blue blazer with the scarf belt under the giant number", veil=.25, zoom=1.1, origin="50% 0%")
clip("bfd-09-clip-leo", "hratsiia-flat.webp", "Хустка «Грація» з «Дикої стихії» — і всі принти чотирьох колекцій.", "The digits 40 filled with the leopard print of Grace", pos="35% 50%", bgsize="130%", big="Цифри в леопарді. Чорна п’ятниця.")
band("bfd-10-band-bows", LB + "lb45-47-L.webp", "50% 0%", "Твіллі «Енергія» з «Поклику душі» — бантами у волоссі. Знижки на всі принти чотирьох колекцій.", "The yellow top meets the yellow top of the model with the Energy bows")
sticker("bfd-11-sticker-trench", "kolo-1.webp", "50% 30%", "Сядьте зручніше. Ціни вже сіли.", "Хустка «Коло сонця» зі «Співочої душі» — на плечі тренча.", "The crouching model in the trench, the sticker on the left", at="left", tilt=10, top_veil=.3, split=.64)
giant("bfd-12-field", LB + "lb34-36-R.webp", "50% 20%", "Хустка «Відновлення» з «Дикої стихії» — через плече. " + LINE, "The camel coat in the field under the range", num="range", veil=.25)
tiers("bfd-13-tiers-two", LB + "lb30-32-R.webp", "70% 15%", "Три кроки Чорної п’ятниці. «Сміливий дотик» і «Натхнення» — на плечах тренча.", "The three tiers, the two scarves on the right", zoom=1.08, origin="70% 15%")
tag("bfd-14-tag-light", "probudzhennia-3.webp", "40% 12%", "Бирка на п’ятницю.", "Хустка «Пробудження» — як косинка, на білому жакеті.", "The price tag over the light headscarf frame; the white field", dark=False, split=.66, tilt=-8)
rows("bfd-15-rows-twilly", LB + "lb07-08-L.webp", "50% 15%", "Твіллі «Коло сонця» зі «Співочої душі» — зі знижкою.", "The wall of the message, the Circle of the Sun twilly portrait as a window", text="−20…−40 % · Чорна п’ятниця · ")
giant("bfd-16-dress", "probudzhennia-2.webp", "50% 25%", "Хустка «Пробудження» на чорній сукні. " + LINE, "The iris scarf on the black dress under the giant number", veil=.55)


# ─── the second batch (client: «еще») ─────────────────────────────────────────────────────────────────────────────────

def outline(id, img, pos, small, note="", zoom=1.0, origin="50% 50%", veil=.4, size=330):
    """The number as a yellow contour only — the photograph shows through the digits."""
    num = (f'<p style="{BIGF}font-size:{int(size * K)}px;color:transparent;-webkit-text-stroke:{max(2, int(4 * K))}px {YEL}">'
           f'<span style="font-size:.22em;font-weight:500;letter-spacing:.08em;vertical-align:1.1em;margin-right:.3em;color:{YEL};-webkit-text-stroke:0">до</span>−40<span style="font-size:.5em;letter-spacing:0"> %</span></p>')
    if SQ:
        giant(id, img, pos, small, note, zoom=zoom, origin=origin); return
    body = f'''
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="inset:0"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:0;right:0;top:0;height:{int(280 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,{veil}),rgba(12,9,8,0))"></div>
  <div style="left:0;right:0;bottom:0;height:{int(H * .5)}px;background:linear-gradient(0deg,rgba(20,17,16,1) 0,rgba(20,17,16,.9) 34%,rgba(20,17,16,0) 100%)"></div>
  {header()}
  <div class="light" style="left:64px;right:64px;bottom:{H - Y1}px;z-index:4">{kick("Чорна п’ятниця · знижки на шовк", YEL)}<div style="margin-top:{int(6 * K)}px">{num}</div>
    <p class="small" style="font-size:{int(36 * K)}px;margin-top:{int(14 * K)}px;max-width:900px">{nb(small)}</p></div>
  {bar(label=CATS)}'''
    ad(id, body, note)

def vertical(id, img, pos, small, note="", zoom=1.0, origin="50% 50%", side="right"):
    """The photograph on one side, a black column with the number written vertically on the other."""
    col = int((300 if not SQ else 250) * K) + (0 if not SQ else 40)
    pw = 1080 - col
    px = 0 if side == "right" else col; cx = pw if side == "right" else 0
    num = (f'<p style="{BIGF}font-size:{int((250 if not SQ else 170) * K)}px;color:{YEL};writing-mode:vertical-rl;transform:rotate(180deg)">'
           f'<span style="font-size:.26em;font-weight:500;letter-spacing:.08em;margin-bottom:.4em;color:{CREAM}">до</span>−40<span style="font-size:.5em;letter-spacing:0"> %</span></p>')
    body = f'''
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="left:{px}px;top:0;width:{pw}px;height:{H}px"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:0;right:0;top:0;height:{int(220 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,.5),rgba(12,9,8,0))"></div>
  <div style="left:{px}px;width:{pw}px;bottom:0;height:{int(620 * K)}px;background:linear-gradient(0deg,{INK},rgba(20,17,16,.9) 25%,rgba(20,17,16,0))"></div>
  {header()}
  <div style="left:{cx}px;top:{Y0 + int(20 * K)}px;width:{col}px;height:{Y1 - Y0 - int(20 * K)}px;display:flex;align-items:flex-end;justify-content:center;z-index:4">{num}</div>
  <div class="light" style="left:{px + 64 if side == "right" else col + 40}px;width:{pw - 110}px;bottom:{H - Y1}px;z-index:4"><p class="small" style="font-size:{int(34 * K)}px">{nb(small)}</p></div>
  {bar(label=CATS)}'''
    ad(id, body, note)

def stamp(id, img, pos, big, small, note="", zoom=1.0, origin="50% 50%", split=.6, tilt=-14, top_veil=.35, at="right"):
    """The `full` layout with a round rubber-stamp ring — «ЧОРНА П’ЯТНИЦЯ · OBIIMY» around «до −40 %» — pressed on the seam."""
    d = int((400 if not SQ else 300) * K)
    ring = (f'<svg viewBox="0 0 400 400" style="position:absolute;inset:0;width:100%;height:100%;transform:rotate({tilt}deg)">'
            f'<defs><path id="rp-{id}" d="M200,200 m-146,0 a146,146 0 1,1 292,0 a146,146 0 1,1 -292,0"/></defs>'
            f'<circle cx="200" cy="200" r="190" fill="none" stroke="{YEL}" stroke-width="7"/><circle cx="200" cy="200" r="112" fill="none" stroke="{YEL}" stroke-width="4"/>'
            f'<text font-family="Montserrat,sans-serif" font-weight="500" font-size="31" letter-spacing="4" fill="{YEL}"><textPath href="#rp-{id}">ЧОРНА П’ЯТНИЦЯ · OBIIMY · ЧОРНА П’ЯТНИЦЯ · OBIIMY ·</textPath></text>'
            f'<text x="200" y="176" text-anchor="middle" font-family="Montserrat,sans-serif" font-weight="500" font-size="24" letter-spacing="3" fill="{CREAM}">ДО</text>'
            f'<text x="200" y="248" text-anchor="middle" font-family="Montserrat,sans-serif" font-weight="400" font-size="78" letter-spacing="-3" fill="{YEL}">−40<tspan font-size="40" letter-spacing="0"> %</tspan></text></svg>')
    if SQ:
        full(id, img, pos, big, small, note, dark=True, size=76, root=True, zoom=zoom, label=CATS, origin=origin)
        sx, sy = 540 - d - 10, H - BOTB - BAR - d - int(16 * K)
    else:
        full(id, img, pos, big, small, note, dark=True, size=76, root=True, split=split, zoom=zoom, label=CATS, top_veil=top_veil, origin=origin)
        yph = int(H * split); sx = (1080 - 64 - d) if at == "right" else 64; sy = yph - d - int(20 * K)
    ads[-1] = ads[-1].replace("\n</section>", f'\n  <div style="left:{sx}px;top:{sy}px;width:{d}px;height:{d}px;z-index:7;filter:drop-shadow(0 20px 30px rgba(0,0,0,.5))">{ring}</div>\n</section>')

def half(id, img, pos, small, note="", zoom=1.0, origin="50% 50%", split=.56):
    """The photograph on top with a hard edge, the yellow block below with the range in ink — `band` upside down."""
    if SQ:
        band(id, img, pos, small, note, zoom=zoom, origin=origin); return
    yb = int(H * split)
    body = f'''
  <div style="inset:0;background:{YEL}"></div>
  <div class="ph" style="left:0;right:0;top:0;height:{yb}px"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:0;right:0;top:0;height:{int(240 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,.5),rgba(12,9,8,0))"></div>
  {header()}
  <div class="ink" style="left:64px;right:64px;top:{yb + int(70 * K)}px;z-index:4">{kick("Чорна п’ятниця", INK)}
    <p style="{BIGF}font-size:{int(198 * K)}px;color:{INK};margin-top:{int(10 * K)}px">−20…−40<span style="font-size:.5em;letter-spacing:0"> %</span></p>
    <p class="small" style="font-size:{int(36 * K)}px;margin-top:{int(16 * K)}px;color:#4B3F10;max-width:900px">{nb(small)}</p></div>
  <div style="left:64px;right:64px;bottom:{BOTB}px;height:{BAR}px;display:flex;align-items:center;justify-content:space-between;z-index:6">
    <span class="pill" style="background:{INK};color:{YEL};font-size:{int(32 * K)}px;padding:{int(20 * K)}px {int(36 * K)}px">{nb(CATS)}</span><span class="hdr" style="font-size:{int(26 * K)}px;color:{INK};letter-spacing:.1em;text-transform:none">obiimy.world</span></div>'''
    ad(id, body, note)

def grid4(id, imgs, small, note=""):
    """Four portraits in a 2 × 2 grid and a yellow square with «до −40 %» sitting on the cross."""
    gap = 8; text_h = int(250 * K)
    tw = (1080 - gap) // 2; th = (Y1 - Y0 - text_h - gap) // 2
    tiles = "".join(f'<div class="ph" style="left:{(i % 2) * (tw + gap)}px;top:{Y0 + (i // 2) * (th + gap)}px;width:{tw}px;height:{th}px"><img src="{PR}{f}" alt="" style="object-position:{p}"></div>' for i, (f, p) in enumerate(imgs))
    d = int(360 * K); cx = (1080 - d) // 2; cy = Y0 + th + gap // 2 - d // 2 - int(30 * K)
    sq = (f'<div style="left:{cx}px;top:{cy}px;width:{d}px;height:{d}px;background:{YEL};transform:rotate(-6deg);box-shadow:0 30px 60px -20px rgba(0,0,0,.7);z-index:5;display:flex;flex-direction:column;align-items:center;justify-content:center;color:{INK}">'
          f'<span class="kicker" style="font-size:{int(26 * K)}px;letter-spacing:.14em">до</span><span style="{BIGF}font-size:{int(140 * K)}px;font-weight:400;margin-top:{int(6 * K)}px">−40<span style="font-size:.5em;letter-spacing:0"> %</span></span>'
          f'<span class="kicker" style="font-size:{int(18 * K)}px;letter-spacing:.2em;margin-top:{int(18 * K)}px;color:#6b5a14">Чорна п’ятниця</span></div>')
    body = f'''
  <div style="inset:0;background:{INK}"></div>{tiles}{sq}
  {header()}
  <div class="light" style="left:64px;right:64px;top:{Y0 + 2 * th + gap + int(40 * K)}px;bottom:{H - Y1}px;z-index:4;text-align:center"><p class="small" style="font-size:{int(34 * K)}px">{nb(small)}</p></div>
  {bar(label=CATS)}'''
    ad(id, body, note)

def strike(id, img, pos, small, note="", zoom=1.0, origin="50% 50%", split=.54, veil=.35):
    """«Чорна» crossed out, «Жовта» in yellow — the brand's Friday is yellow; the number under it."""
    if SQ:
        full(id, img, pos, f'<span style="text-decoration:line-through;text-decoration-color:{YEL};text-decoration-thickness:.09em;color:#9A9088">Чорна</span> <em>Жовта</em> п’ятниця.', small, note, dark=True, size=72, root=True, zoom=zoom, label=CATS, origin=origin)
        ads[-1] = ads[-1].replace('<p class="small"', f'<div style="margin-top:{int(10 * K)}px">{do40(150)}</div><p class="small"', 1); return
    yph = int(H * split)
    body = f'''
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="left:0;right:0;top:0;height:{yph + int(80 * K)}px"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:0;right:0;top:{yph - int(240 * K)}px;height:{int(322 * K)}px;background:{melt(True, bottom=True)}"></div>
  <div style="left:0;right:0;top:0;height:{int(220 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,{veil}),rgba(12,9,8,0))"></div>
  {header(text="Знижки на шовк")}
  <div class="light" style="left:64px;right:64px;top:{yph + int(30 * K)}px;bottom:{H - Y1}px;z-index:4">
    <p class="big" style="font-size:{int(96 * K)}px"><span style="text-decoration:line-through;text-decoration-color:{YEL};text-decoration-thickness:.09em;color:#9A9088">Чорна</span> <em>Жовта</em> п’ятниця.</p>
    <div style="margin-top:{int(24 * K)}px">{do40(250)}</div>
    <p class="small" style="font-size:{int(36 * K)}px;margin-top:{int(16 * K)}px;max-width:900px">{nb(small)}</p></div>
  {bar(label=CATS)}'''
    ad(id, body, note)

def pct(id, img, small, note="", pos="50% 50%", big="Відсотки з принтом."):
    """The giant «%» sign as a window onto the silk; «до −40» in yellow beside it."""
    src = PR + img
    dsz = int((600 if not SQ else 420) * K)
    sign = (f'<p style="font-family:Montserrat,sans-serif;font-weight:500;line-height:.86;letter-spacing:-.04em;font-size:{dsz}px;white-space:nowrap;'
            f'background:url({src}) {pos}/cover;-webkit-background-clip:text;background-clip:text;color:transparent;filter:saturate(1.1)">%</p>')
    num = f'<p style="{BIGF}font-size:{int(dsz * .3)}px;color:{YEL};font-weight:400;margin-bottom:{int(dsz * .06)}px"><span style="font-size:.4em;font-weight:500;letter-spacing:.08em;vertical-align:.8em;margin-right:.3em;color:{CREAM}">до</span>−40</p>'
    top = Y0 + int(40 * K)
    body = f'''
  <div style="inset:0;background:{INK}"></div>
  {header()}
  <div style="left:64px;right:64px;top:{top}px;display:flex;align-items:flex-end;gap:{int(20 * K)}px;z-index:4">{num}{sign}</div>
  <div class="light" style="left:64px;right:64px;top:{top + dsz + int(60 * K)}px;z-index:4"><p class="big" style="font-size:{int((76 if not SQ else 52) * K)}px">{nbh(big)}</p><p class="small" style="font-size:{int(34 * K)}px;margin-top:{int(16 * K)}px">{nb(small)}</p></div>
  {"" if SQ else f'<div class="ph" style="left:0;right:0;top:{Y1 - int(420 * K)}px;bottom:0;-webkit-mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent);mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)"><img src="{src}" alt="" style="object-position:{pos};opacity:.9"></div><div style="left:0;right:0;top:{Y1 - int(420 * K)}px;height:{int(240 * K)}px;background:{melt(True, bottom=False)}"></div><div style="left:0;right:0;bottom:0;height:{BOTB + BAR + int(60 * K)}px;background:{melt(True, bottom=True)}"></div>'}
  {bar(label=CATS)}'''
    ad(id, body, note)

def sash(id, img, pos, big, small, note="", zoom=1.0, origin="50% 50%", veil=.35):
    """A yellow ribbon across the top corner with «ДО −40 %» running along it, over the full-height photograph."""
    txt = "ДО −40 % · ЧОРНА П’ЯТНИЦЯ · " * 6
    rib = (f'<div style="left:-400px;top:{int(H * .55)}px;width:2200px;height:{int(110 * K)}px;background:{YEL};transform:rotate(-28deg);transform-origin:50% 50%;z-index:6;display:flex;align-items:center;overflow:hidden;box-shadow:0 20px 40px -10px rgba(0,0,0,.5)">'
           f'<span style="font-family:Montserrat,sans-serif;font-weight:500;font-size:{int(44 * K)}px;letter-spacing:.14em;color:{INK};white-space:nowrap;padding-left:60px">{txt}</span></div>')
    if SQ:
        full(id, img, pos, big, small, note, dark=True, size=72, root=True, zoom=zoom, label=CATS, origin=origin)
        rib = rib.replace("left:-400px", "left:-300px").replace(f"top:{int(H * .55)}px", f"top:{int(H * .66)}px").replace("width:2200px", "width:800px")
        ads[-1] = ads[-1].replace("\n</section>", f"\n  {rib}\n</section>"); return
    body = f'''
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="inset:0"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:0;right:0;top:0;height:{int(280 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,{veil}),rgba(12,9,8,0))"></div>
  <div style="left:0;right:0;bottom:0;height:{int(H * .5)}px;background:linear-gradient(0deg,rgba(20,17,16,1) 0,rgba(20,17,16,.92) 30%,rgba(20,17,16,0) 100%)"></div>
  {rib}
  {header()}
  <div class="light" style="left:64px;right:64px;bottom:{H - Y1}px;z-index:4">{words(big, small, 84, True)}</div>
  {bar(label=CATS)}'''
    ad(id, body, note)

outline("bfd-17-outline", LB + "lb02-01-R.webp", "50% 20%", "Хустка «Піднесення» зі «Співочої душі» — на плечах шкіряного блейзера.", "The leather blazer in the wooden chair, the contour digits over it", veil=.3)
vertical("bfd-18-vertical", LB + "lb52-54-R.webp", "20% 20%", "Хустка «Маків цвіт» з «Поклику душі» — на голові. Чорна п’ятниця на шовк із авторськими принтами.", "The poppy scarf profile, the number written vertically in the right column", zoom=1.0)
stamp("bfd-19-stamp", LB + "lb26-28-R.webp", "50% 15%", "Печатка п’ятниці.", "Хустка «Ранкова кава» з «Дикої стихії» — вузлом на шиї.", "The Morning Coffee knot, the round stamp on the seam", split=.6, at="right", tilt=-14)
half("bfd-20-half", "hratsiia-2.webp", "50% 26%", "Хустка «Грація» з «Дикої стихії» — як пояс на синьому блейзері. Хустки, твіллі, маски для сну й набори.", "The dynamic blue-blazer frame on top, the yellow block with the range below", zoom=1.0)
grid4("bfd-21-grid", [(LB + "lb50-52-R.webp", "50% 20%"), (LB + "lb47-49-L.webp", "50% 15%"), (LB + "lb36-38-R.webp", "50% 15%"), (LB + "lb28-30-R.webp", "50% 15%")],
      "Хустки, твіллі, маски для сну й набори — принти чотирьох колекцій зі знижкою.", "Four lookbook portraits, the yellow square on the cross")
strike("bfd-22-strike", LB + "lb29-31-L.webp", "50% 0%", "Жовтий — наш колір. Твіллі «Натхнення» з «Дикої стихії» — на тренчі.", "«Чорна» crossed out, «Жовта» in yellow, the trench with the Inspiration twilly", veil=.3)
pct("bfd-23-pct", "vyr-flat.webp", "Хустка «Вир почуттів» із «Пробудження» — і всі принти чотирьох колекцій.", "The giant percent sign filled with the Whirlpool print", pos="50% 50%")
sash("bfd-24-sash", "kolo-3.webp", "50% 10%", "Стрічка на п’ятницю.", "Хустка «Коло сонця» зі «Співочої душі» — на плечі довгого тренча.", "The full-length trench, the yellow ribbon across the top corner", zoom=1.0)
vertical("bfd-25-vertical-left", "makiv-1.webp", "55% 15%", "Хустка «Маків цвіт» з «Поклику душі» — на білому жакеті. Чорна п’ятниця на шовк із авторськими принтами.", "The white jacket, the number in the left column", side="left")
band("bfd-26-band-freedom", LB + "lb56-58-R.webp", "50% 0%", "Хустка «Свобода» з «Поклику душі» — через плече, під ременем. Знижки на всі принти чотирьох колекцій.", "The blue-and-yellow Freedom scarf under the yellow poster top")


# ─── the third batch (client: «еще», again) ───────────────────────────────────────────────────────────────────────────

def do40ink(size): return do40(size, color=INK).replace(f"color:{INK}", f"color:{INK}")

def frame(id, img, pos, small, note="", zoom=1.0):
    """A yellow passe-partout: the photograph inset on the yellow field, the number in the margin under it."""
    m = 40
    if SQ:
        pw = 500
        body = f"""
  <div style="inset:0;background:{YEL}"></div>
  <div class="ph" style="left:{m}px;top:{Y0}px;width:{pw}px;height:{Y1 - Y0}px"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  {header(False)}
  <div class="ink" style="left:{m + pw + 50}px;right:64px;top:{Y0 + int(40 * K)}px;z-index:4">{kick("Чорна п’ятниця", INK)}<div style="margin-top:{int(10 * K)}px">{do40(150, INK)}</div><p class="small" style="font-size:{int(30 * K)}px;margin-top:{int(16 * K)}px;color:#4B3F10">{nb(small)}</p></div>
  <div style="left:64px;right:64px;bottom:{BOTB}px;height:{BAR}px;display:flex;align-items:center;justify-content:flex-end;z-index:6"><span class="pill" style="background:{INK};color:{YEL};font-size:{int(30 * K)}px;padding:{int(18 * K)}px {int(34 * K)}px">obiimy.world</span></div>"""
    else:
        text_h = int(420 * K); ph_h = Y1 - Y0 - text_h
        body = f"""
  <div style="inset:0;background:{YEL}"></div>
  <div class="ph" style="left:{m}px;right:{m}px;top:{Y0}px;height:{ph_h}px"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  {header(False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0 + ph_h + int(44 * K)}px;z-index:4">{kick("Чорна п’ятниця", INK)}<div style="margin-top:{int(6 * K)}px">{do40(210, INK)}</div><p class="small" style="font-size:{int(34 * K)}px;margin-top:{int(12 * K)}px;color:#4B3F10;max-width:900px">{nb(small)}</p></div>
  <div style="left:64px;right:64px;bottom:{BOTB}px;height:{BAR}px;display:flex;align-items:center;justify-content:space-between;z-index:6"><span class="pill" style="background:{INK};color:{YEL};font-size:{int(32 * K)}px;padding:{int(20 * K)}px {int(36 * K)}px">{nb(CATS)}</span><span class="hdr" style="font-size:{int(26 * K)}px;color:{INK};letter-spacing:.1em;text-transform:none">obiimy.world</span></div>"""
    ad(id, body, note)

def diag(id, img, pos, small, note="", zoom=1.0, origin="50% 50%"):
    """The photograph, and a yellow triangle cut across the lower right with the range inside."""
    cut = "polygon(0 100%, 100% 44%, 100% 100%)" if not SQ else "polygon(0 100%, 100% 36%, 100% 100%)"
    body = f"""
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="inset:0"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:0;right:0;top:0;height:{int(260 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,.5),rgba(12,9,8,0))"></div>
  <div style="inset:0;background:{YEL};clip-path:{cut};z-index:3"></div>
  {header()}
  <div class="ink" style="right:64px;bottom:{H - Y1 + int(10 * K)}px;width:{int(880 * K)}px;text-align:right;z-index:4">{kick("Чорна п’ятниця", INK)}<div style="margin-top:{int(8 * K)}px">{rng(150 if not SQ else 110, INK)}</div><p class="small" style="font-size:{int(32 * K)}px;margin-top:{int(14 * K)}px;color:#4B3F10;margin-left:auto;max-width:{int(560 * K)}px">{nb(small)}</p></div>
  <div style="left:64px;right:64px;bottom:{BOTB}px;height:{BAR}px;display:flex;align-items:center;justify-content:space-between;z-index:6"><span class="pill" style="background:{INK};color:{YEL};font-size:{int(30 * K)}px;padding:{int(18 * K)}px {int(34 * K)}px">{nb(CATS)}</span><span class="hdr" style="font-size:{int(26 * K)}px;color:{INK};letter-spacing:.1em;text-transform:none">obiimy.world</span></div>"""
    ad(id, body, note)

def circle(id, img, pos, small, note="", zoom=1.0):
    """The photograph in a big round porthole on the black field, the number under it."""
    if SQ:
        d = min(560, Y1 - Y0 + 20); cx, cy = 40, (H - d) // 2
        body = f"""
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="left:{cx}px;top:{cy}px;width:{d}px;height:{d}px;border-radius:50%"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  {header()}
  <div class="light" style="left:{cx + d + 40}px;right:64px;top:{Y0 + int(60 * K)}px;z-index:4">{kick("Чорна п’ятниця", YEL)}<div style="margin-top:{int(10 * K)}px">{do40(150)}</div><p class="small" style="font-size:{int(30 * K)}px;margin-top:{int(16 * K)}px">{nb(small)}</p></div>
  {bar(label=CATS)}"""
    else:
        d = min(820, Y1 - Y0 - int(440 * K)); cx = (1080 - d) // 2; cy = Y0 - int(10 * K)
        body = f"""
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="left:{cx}px;top:{cy}px;width:{d}px;height:{d}px;border-radius:50%"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  {header()}
  <div class="light" style="left:64px;right:64px;top:{cy + d + int(60 * K)}px;bottom:{H - Y1}px;z-index:4;text-align:center">{kick("Чорна п’ятниця", YEL)}<div style="margin-top:{int(6 * K)}px">{do40(220)}</div><p class="small" style="font-size:{int(34 * K)}px;margin-top:{int(12 * K)}px">{nb(small)}</p></div>
  {bar(label=CATS)}"""
    ad(id, body, note)

def arch(id, img, pos, small, note="", zoom=1.0):
    """The photograph as an arch on the yellow field, the number in ink under it."""
    if SQ:
        aw = 460; ah = Y1 - Y0 + 10; ax = 50
        body = f"""
  <div style="inset:0;background:{YEL}"></div>
  <div class="ph" style="left:{ax}px;top:{Y0 - 10}px;width:{aw}px;height:{ah}px;border-radius:{aw // 2}px {aw // 2}px 0 0"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  {header(False)}
  <div class="ink" style="left:{ax + aw + 50}px;right:64px;top:{Y0 + int(60 * K)}px;z-index:4">{kick("Чорна п’ятниця", INK)}<div style="margin-top:{int(10 * K)}px">{do40(150, INK)}</div><p class="small" style="font-size:{int(30 * K)}px;margin-top:{int(16 * K)}px;color:#4B3F10">{nb(small)}</p></div>
  <div style="left:64px;right:64px;bottom:{BOTB}px;height:{BAR}px;display:flex;align-items:center;justify-content:flex-end;z-index:6"><span class="pill" style="background:{INK};color:{YEL};font-size:{int(30 * K)}px;padding:{int(18 * K)}px {int(34 * K)}px">obiimy.world</span></div>"""
    else:
        aw = 780; ah = Y1 - Y0 - int(420 * K); ax = (1080 - aw) // 2
        body = f"""
  <div style="inset:0;background:{YEL}"></div>
  <div class="ph" style="left:{ax}px;top:{Y0 + int(10 * K)}px;width:{aw}px;height:{ah}px;border-radius:{aw // 2}px {aw // 2}px 0 0"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  {header(False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0 + ah + int(50 * K)}px;z-index:4;text-align:center">{kick("Чорна п’ятниця", INK)}<div style="margin-top:{int(6 * K)}px">{do40(210, INK)}</div><p class="small" style="font-size:{int(34 * K)}px;margin-top:{int(12 * K)}px;color:#4B3F10">{nb(small)}</p></div>
  <div style="left:64px;right:64px;bottom:{BOTB}px;height:{BAR}px;display:flex;align-items:center;justify-content:space-between;z-index:6"><span class="pill" style="background:{INK};color:{YEL};font-size:{int(32 * K)}px;padding:{int(20 * K)}px {int(36 * K)}px">{nb(CATS)}</span><span class="hdr" style="font-size:{int(26 * K)}px;color:{INK};letter-spacing:.1em;text-transform:none">obiimy.world</span></div>"""
    ad(id, body, note)

def ticket(id, img, pos, big, small, note="", zoom=1.0, origin="50% 50%", veil=.4):
    """A tear-off coupon — yellow, with notches and a perforation — lying at the bottom of the full-height photograph."""
    cw, ch = (952, int(300 * K)) if not SQ else (470, int(260 * K))
    coupon = (f'<div style="width:{cw}px;height:{ch}px;background:{YEL};border-radius:{int(24 * K)}px;position:relative;box-shadow:0 30px 60px -20px rgba(0,0,0,.7);overflow:hidden;color:{INK}">'
              f'<div style="position:absolute;left:0;top:0;bottom:0;width:{int(cw * .66)}px;display:flex;flex-direction:column;justify-content:center;padding-left:{int(44 * K)}px">{kick("Чорна п’ятниця", INK, 22)}<div style="margin-top:{int(4 * K)}px">{do40(140 if not SQ else 104, INK)}</div></div>'
              f'<div style="position:absolute;left:{int(cw * .66)}px;top:{int(18 * K)}px;bottom:{int(18 * K)}px;border-left:{max(2, int(3 * K))}px dashed rgba(20,17,16,.45)"></div>'
              f'<div style="position:absolute;left:{int(cw * .66)}px;right:0;top:0;bottom:0;display:flex;align-items:center;justify-content:center"><span class="kicker" style="font-size:{int(22 * K)}px;letter-spacing:.2em;writing-mode:vertical-rl;transform:rotate(180deg);color:#4B3F10">obiimy.world</span></div>'
              f'<div style="position:absolute;left:{int(cw * .66) - int(16 * K)}px;top:{-int(16 * K)}px;width:{int(32 * K)}px;height:{int(32 * K)}px;border-radius:50%;background:{INK}"></div>'
              f'<div style="position:absolute;left:{int(cw * .66) - int(16 * K)}px;bottom:{-int(16 * K)}px;width:{int(32 * K)}px;height:{int(32 * K)}px;border-radius:50%;background:{INK}"></div></div>')
    if SQ:
        full(id, img, pos, big, small, note, dark=True, size=68, root=True, zoom=zoom, label=CATS, origin=origin)
        ads[-1] = ads[-1].replace("\n</section>", f'\n  <div style="left:{1080 - 64 - cw}px;top:{H - BOTB - BAR - ch - int(30 * K)}px;z-index:7">{coupon}</div>\n</section>'); return
    body = f"""
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="inset:0"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:0;right:0;top:0;height:{int(280 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,{veil}),rgba(12,9,8,0))"></div>
  <div style="left:0;right:0;bottom:0;height:{int(H * .5)}px;background:linear-gradient(0deg,rgba(20,17,16,1) 0,rgba(20,17,16,.9) 30%,rgba(20,17,16,0) 100%)"></div>
  {header()}
  <div class="light" style="left:64px;right:64px;bottom:{H - Y1 + ch + int(24 * K)}px;z-index:4">{words(big, small, 72, True)}</div>
  <div style="left:64px;bottom:{H - Y1}px;z-index:7;transform:rotate(-2deg);transform-origin:0 100%">{coupon}</div>
  {bar(label=CATS)}"""
    ad(id, body, note)

def polaroid(id, img, pos, small, note="", zoom=1.0, tilt=-4):
    """An instant-photo card on the black field, the number written in its white margin."""
    if SQ:
        cw = 520; ph = cw - 60; ch = ph + int(200 * K); cx, cy = 50, (H - ch) // 2
        tx = cx + cw + 50
    else:
        cw = 820; ph = cw - 60; ch = ph + int(240 * K); cx, cy = (1080 - cw) // 2, Y0 + int(30 * K); tx = None
    card = (f'<div class="card" style="left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px;transform:rotate({tilt}deg);z-index:3;background:#fff">'
            f'<div class="ph" style="position:absolute;left:30px;top:30px;width:{ph}px;height:{ph}px"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>'
            f'<div style="position:absolute;left:30px;right:30px;top:{30 + ph}px;bottom:0;display:flex;align-items:center;justify-content:space-between;color:{INK}">{do40(130 if not SQ else 96, INK)}<span class="kicker" style="font-size:{int(20 * K)}px;letter-spacing:.2em;color:#6b6258">Чорна п’ятниця</span></div></div>')
    if SQ:
        body = f"""
  <div style="inset:0;background:{INK}"></div>{card}
  {header()}
  <div class="light" style="left:{tx}px;right:64px;top:{Y0 + int(60 * K)}px;z-index:4"><p class="big" style="font-size:{int(60 * K)}px">Знімок на пам’ять. Ціни — ні.</p><p class="small" style="font-size:{int(30 * K)}px;margin-top:{int(16 * K)}px">{nb(small)}</p></div>
  {bar(label=CATS)}"""
    else:
        body = f"""
  <div style="inset:0;background:{INK}"></div>{card}
  {header()}
  <div class="light" style="left:64px;right:64px;top:{cy + ch + int(70 * K)}px;bottom:{H - Y1}px;z-index:4"><p class="big" style="font-size:{int(76 * K)}px">Знімок на пам’ять. Ціни — ні.</p><p class="small" style="font-size:{int(34 * K)}px;margin-top:{int(16 * K)}px">{nb(small)}</p></div>
  {bar(label=CATS)}"""
    ad(id, body, note)

def bars(id, img, pos, small, note="", zoom=1.0, split=.56):
    """The photograph on top; under it three yellow bars growing from −20 to −40 % — the steps as a chart."""
    rowsh = "".join(f'<div style="position:relative;height:{int(76 * K)}px;margin-top:{int(14 * K) if i else 0}px;width:{(58, 79, 100)[i]}%;background:{YEL};opacity:{(.55, .78, 1)[i]};border-radius:{int(6 * K)}px;display:flex;align-items:center;justify-content:flex-end;padding-right:{int(28 * K)}px"><span style="{BIGF}font-size:{int(54 * K)}px;font-weight:400;color:{INK}">−{n}<span style="font-size:.6em;letter-spacing:0"> %</span></span></div>' for i, n in enumerate((20, 30, 40)))
    if SQ:
        full(id, img, pos, "Три кроки Чорної п’ятниці.", small, note, dark=True, size=60, root=True, zoom=zoom, label=CATS)
        ads[-1] = ads[-1].replace('<p class="small"', f'<div style="margin-top:{int(24 * K)}px;margin-bottom:{int(8 * K)}px">{rowsh}</div><p class="small"', 1); return
    yph = int(H * split)
    body = f"""
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="left:0;right:0;top:0;height:{yph + int(60 * K)}px"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  <div style="left:0;right:0;top:{yph - int(260 * K)}px;height:{int(322 * K)}px;background:{melt(True, bottom=True)}"></div>
  <div style="left:0;right:0;top:0;height:{int(220 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,.45),rgba(12,9,8,0))"></div>
  {header()}
  <div class="light" style="left:64px;right:64px;top:{yph + int(10 * K)}px;bottom:{H - Y1}px;z-index:4">{kick("Чорна п’ятниця · три рівні знижок", YEL)}<div style="margin-top:{int(24 * K)}px">{rowsh}</div><p class="small" style="font-size:{int(34 * K)}px;margin-top:{int(30 * K)}px;max-width:900px">{nb(small)}</p></div>
  {bar(label=CATS)}"""
    ad(id, body, note)

def typeonly(id, note=""):
    """No photograph at all: the yellow field, the range, the four categories — the loudest and the plainest."""
    cats = "".join(f'<p class="small" style="font-size:{int((66 if not SQ else 44) * K)}px;color:{INK};line-height:1.25">{c}</p>' for c in ("Хустки", "Твіллі", "Маски для сну", "Подарункові набори"))
    body = f"""
  <div style="inset:0;background:{YEL}"></div>
  {header(False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0 + int(60 * K)}px;z-index:4">{kick("Чорна п’ятниця · знижки на шовк", INK)}
    <p style="{BIGF}font-size:{int((330 if not SQ else 200) * K)}px;color:{INK};margin-top:{int(16 * K)}px;line-height:.9">−20…<br>−40<span style="font-size:.5em;letter-spacing:0"> %</span></p>
    <div style="margin-top:{int(50 * K)}px;border-top:{max(2, int(3 * K))}px solid {INK};padding-top:{int(30 * K)}px">{cats}</div>
    <p class="small" style="font-size:{int(30 * K)}px;margin-top:{int(30 * K)}px;color:#4B3F10">{nb("На шовк із авторськими принтами чотирьох колекцій.")}</p></div>
  <div style="left:64px;right:64px;bottom:{BOTB}px;height:{BAR}px;display:flex;align-items:center;justify-content:space-between;z-index:6"><span class="pill" style="background:{INK};color:{YEL};font-size:{int(32 * K)}px;padding:{int(20 * K)}px {int(36 * K)}px">obiimy.world</span></div>"""
    ad(id, body, note)

def film(id, imgs, small, note=""):
    """A strip of film — four set frames with sprocket holes — beside the number."""
    def holes(x, h):
        n = h // int(44 * K)
        return "".join(f'<div style="position:absolute;left:{x}px;top:{i * int(44 * K) + int(12 * K)}px;width:{int(18 * K)}px;height:{int(24 * K)}px;border-radius:{int(4 * K)}px;background:{INK}"></div>' for i in range(n))
    if SQ:
        sw = 1080; fh = int(330 * K); fw = (sw - 5 * 10) // 4; top = Y0
        frames = "".join(f'<div class="ph" style="position:absolute;left:{10 + i * (fw + 10)}px;top:{int(30 * K)}px;width:{fw}px;height:{fh - int(60 * K)}px"><img src="{PR}{f}" alt="" style="object-position:{p}"></div>' for i, (f, p) in enumerate(imgs))
        strip = f'<div style="left:0;top:{top}px;width:{sw}px;height:{fh}px;background:#0a0908;overflow:hidden">{frames}</div>'
        body = f"""
  <div style="inset:0;background:{INK}"></div>{strip}
  {header()}
  <div class="light" style="left:64px;right:64px;top:{top + fh + int(40 * K)}px;z-index:4">{kick("Чорна п’ятниця", YEL)}<div style="margin-top:{int(6 * K)}px">{do40(150)}</div><p class="small" style="font-size:{int(30 * K)}px;margin-top:{int(12 * K)}px">{nb(small)}</p></div>
  {bar(label=CATS)}"""
    else:
        sw = 430; sh_ = Y1 - Y0 + int(20 * K); fh = (sh_ - 5 * 12) // 4; fw = sw - 2 * int(52 * K)
        frames = "".join(f'<div class="ph" style="position:absolute;left:{int(52 * K)}px;top:{12 + i * (fh + 12)}px;width:{fw}px;height:{fh}px"><img src="{PR}{f}" alt="" style="object-position:{p}"></div>' for i, (f, p) in enumerate(imgs))
        strip = f'<div style="left:40px;top:{Y0 - int(10 * K)}px;width:{sw}px;height:{sh_}px;background:#0a0908;overflow:hidden;box-shadow:0 40px 80px -30px rgba(0,0,0,.8)">{holes(int(16 * K), sh_)}{holes(sw - int(34 * K), sh_)}{frames}</div>'
        body = f"""
  <div style="inset:0;background:{INK}"></div>{strip}
  {header()}
  <div class="light" style="left:{40 + sw + 50}px;right:64px;top:{Y0 + int(60 * K)}px;z-index:4">{kick("Чорна п’ятниця", YEL)}<div style="margin-top:{int(10 * K)}px">{do40(190)}</div><p class="small" style="font-size:{int(32 * K)}px;margin-top:{int(20 * K)}px">{nb(small)}</p></div>
  {bar(label=CATS)}"""
    ad(id, body, note)

def clipyellow(id, img, small, note="", pos="50% 50%", bgsize="cover", big="Чорна п’ятниця. Жовта."):
    """`clip` on the yellow field: the digits are a window onto the photograph, everything else in ink."""
    clip(id, img, small, note, pos=pos, big=big, bgsize=bgsize)
    a = ads[-1]
    a = a.replace(f'<div style="inset:0;background:{INK}"></div>', f'<div style="inset:0;background:{YEL}"></div>', 1)
    a = a.replace('filter:saturate(1.1)', 'filter:saturate(1.3) contrast(1.12)')
    a = a.replace(f'color:{YEL};font-weight:400">−', f'color:{INK};font-weight:400">−').replace(f'color:{YEL};font-weight:400">%', f'color:{INK};font-weight:400">%')
    a = a.replace(f'class="kicker" style="font-size', f'class="kicker" style="color:{INK};font-size', 1)
    a = a.replace(f'color:{CREAM};margin-right', f'color:{INK};margin-right')
    a = a.replace('<div class="light"', '<div class="ink"').replace(f'<div class="light"', '<div class="ink"')
    a = a.replace(f'src="{LOGO_W}"', f'src="{LOGO_K}"').replace(f'color:{CREAM};z-index:5">', f'color:{INK};z-index:5">')
    a = a.replace(f'background:{YEL};color:{INK};font-size', f'background:{INK};color:{YEL};font-size').replace(f'color:{CREAM};letter-spacing:.1em;text-transform:none">obiimy', f'color:{INK};letter-spacing:.1em;text-transform:none">obiimy')
    ads[-1] = a

def marquee(id, img, pos, big, small, note="", zoom=1.0, text="Чорна п’ятниця · до −40 % · "):
    """The photograph as a central column, the message running vertically along both margins."""
    cw = 700 if not SQ else 520; cx = (1080 - cw) // 2
    side = lambda x, flip: f'<div style="left:{x}px;top:{Y0}px;width:{cx}px;height:{Y1 - Y0}px;display:flex;align-items:center;justify-content:center;overflow:hidden"><span class="kicker" style="font-size:{int(40 * K)}px;letter-spacing:.18em;color:{YEL};writing-mode:vertical-rl;{"transform:rotate(180deg);" if flip else ""}white-space:nowrap">{(text * 6).upper()}</span></div>'
    body = f"""
  <div style="inset:0;background:{INK}"></div>
  {side(0, True)}{side(cx + cw, False)}
  <div class="ph" style="left:{cx}px;top:0;width:{cw}px;height:{H}px"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  <div style="left:{cx}px;width:{cw}px;top:0;height:{int(260 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,.5),rgba(12,9,8,0))"></div>
  <div style="left:{cx}px;width:{cw}px;bottom:0;height:{int(H * .5)}px;background:linear-gradient(0deg,rgba(20,17,16,1) 0,rgba(20,17,16,.9) 30%,rgba(20,17,16,0) 100%)"></div>
  {header()}
  <div class="light" style="left:{cx + 40}px;width:{cw - 80}px;bottom:{H - Y1}px;z-index:4">{words(big, small, 64 if not SQ else 48, True)}</div>
  {bar(label=CATS)}"""
    ad(id, body, note)

def fold(id, img, pos, big, small, note="", zoom=1.0, origin="50% 50%", veil=.4):
    """The full-height photograph with a folded-down yellow corner at the top right carrying the number."""
    d = int((520 if not SQ else 320) * K)
    corner = (f'<div style="left:{1080 - d}px;top:0;width:{d}px;height:{d}px;z-index:7;background:{YEL};clip-path:polygon(0 0, 100% 0, 100% 100%);filter:drop-shadow(-10px 14px 24px rgba(0,0,0,.45))">'
              f'<div style="position:absolute;left:{int(d * .68 - d * .5)}px;top:{int(d * .32 - (70 if not SQ else 36) * K)}px;width:{d}px;transform:rotate(45deg);text-align:center;color:{INK}">{do40(96 if not SQ else 50, INK)}</div></div>')
    if SQ:
        full(id, img, pos, big, small, note, dark=True, size=68, root=True, zoom=zoom, label=CATS, origin=origin)
        # the square: the corner at the frame's top right, over the words' half; no header word there, the words start lower
        ads[-1] = re.sub(r'<p class="hdr"[^>]*>[^<]*</p>', "", ads[-1], count=1)
        ads[-1] = ads[-1].replace(f"top:{Y0 + int(40 * K)}px;z-index:4", f"top:{Y0 + int(d * .55)}px;z-index:4", 1)
        ads[-1] = ads[-1].replace("\n</section>", f'\n  {corner}\n</section>'); return
    body = f"""
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="inset:0"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:0;right:0;top:0;height:{int(280 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,{veil}),rgba(12,9,8,0))"></div>
  <div style="left:0;right:0;bottom:0;height:{int(H * .5)}px;background:linear-gradient(0deg,rgba(20,17,16,1) 0,rgba(20,17,16,.9) 30%,rgba(20,17,16,0) 100%)"></div>
  {corner}
  <img src="{LOGO_W}" alt="" style="left:64px;top:{TOPL}px;height:{int(56 * K)}px;z-index:5">
  <div class="light" style="left:64px;right:64px;bottom:{H - Y1}px;z-index:4">{words(big, small, 84, True)}</div>
  {bar(label=CATS)}"""
    ad(id, body, note)

frame("bfd-27-frame", LB + "lb06-07-R.webp", "50% 15%", "Хустка «Коло сонця» зі «Співочої душі» — на бежевому тренчі. Хустки, твіллі, маски для сну й набори.", "The yellow passe-partout around the trench frame")
diag("bfd-28-diag", LB + "lb32-34-R.webp", "50% 0%", "Хустка «Баланс» з «Дикої стихії» — як топ. Хустки, твіллі, маски для сну й набори.", "The halter-top frame with the yellow triangle across the lower right")
circle("bfd-29-circle", LB + "lb50-52-R.webp", "50% 20%", "Хустка «Ніжність» з «Поклику душі» — під білою федорою.", "The fedora portrait in a round porthole")
arch("bfd-30-arch", LB + "lb46-48-R.webp", "50% 15%", "Хустка «Пристрасть» з «Поклику душі» — на голові, під білим капелюхом.", "The headscarf profile as an arch on the yellow field")
ticket("bfd-31-ticket", LB + "lb12-14-R.webp", "50% 10%", "Відривний купон не потрібен.", "Хустка «Поцілунок сонця» з «Пробудження» — бантом на потилиці. Знижки вже на сайті.", "The bow on the back of the neck, the coupon lying at the bottom", veil=.3)
polaroid("bfd-32-polaroid", ST + "set-smilyvist-02.jpg", "50% 25%", "Набір «твіллі + резинка» «Сміливість» — у волоссі. Хустки, твіллі, маски для сну й набори зі знижкою.", "The set frame as an instant-photo card")
bars("bfd-33-bars", LB + "lb14-16-L.webp", "50% 20%", "Твіллі «Соковиті спогади» з «Пробудження» — у волоссі. Хустки, твіллі, маски для сну й набори.", "The twilly in the hair above the three growing bars")
typeonly("bfd-34-type", "No photograph: the yellow field, the range, the four categories")
film("bfd-35-film", [(ST + "set-tvilli-845-ta-khustky-4444-natkhne-04.jpg", "50% 20%"), (ST + "set-tvilli-845-ta-khustky-4444-probudz-01.jpg", "50% 20%"), (ST + "set-tvilli-845-ta-khustky-4444-vpevnen-03.jpg", "50% 20%"), (ST + "set-tvilli-845-ta-khustky-4444-smilyvy-03.jpg", "50% 20%")],
     "Набори «твіллі 84 × 5 + хустка 44 × 44»: «Натхнення», «Пробудження», «Впевненість», «Сміливий дотик».", "Four set frames as a strip of film beside the number")
clipyellow("bfd-36-clip-yellow", "dotyk-flat.webp", "Хустка «Сміливий дотик» з «Дикої стихії» — і всі принти чотирьох колекцій.", "The digits as a window onto the Bold Touch print, on the yellow field", pos="40% 50%", bgsize="140%")
# bfd-37 (marquee, the profile under the cap) dropped: the cap carries another brand's name, legible in the square (panel)
fold("bfd-38-fold", LB + "lb55-57-L.webp", "50% 15%", "Загніть кутик на п’ятницю.", "Твіллі — вузлом на шиї. Твіллі 84 × 5 зі знижкою.", "The Delight twilly profile with the folded yellow corner (the print is not named: Delight has no confirmed Ukrainian name in SITE-FACTS)", veil=.5)

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · Black Friday · discount</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;600&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("bfd" + ("" if FORMAT == "plain" else "-" + FORMAT) + ".html")).write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "Black Friday discount banners", FORMAT)
