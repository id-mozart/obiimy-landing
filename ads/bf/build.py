"""Black Friday creatives (07.11.2026, client: «новая порция креативов к чёрной пятнице — хустки и прочие товары из коллекций,
которые не SOLO, скидки от −20 до −40 %, подойди творчески и необычно»). The idea: a silk brand's Black Friday is not black —
«Чорна п'ятниця. Біла хустка.» The black field is the stage, the silk is the colour, the brand's yellow is the discount.
Photos: obiimy.world as they are (photo/site, photo/) — the four print collections («Співоча душа», «Поклик душі», «Пробудження»,
«Дика стихія»), masks, twillies, bookmarks, pocket squares, the yellow boxes; nothing from SOLO. The discount is always the
client's range «−20…−40 %» — which product gets which is not decided, so no crossed-out prices and no per-item percentage.
1080×1920 plain plus story / feed / square via FORMAT. Output: bf[-<format>].html → out[-<format>]/*.jpg
(cd ads && ADS=bf/bf.html OUT=bf/out node render.mjs; FORMAT=story python3 bf/build.py → ADS=bf/bf-story.html OUT=bf/out-story)."""
import pathlib
from common import *
HERE = pathlib.Path(__file__).parent

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
  {header(text="Знижки на шовк")}
  <div class="light" style="left:{pw - 60}px;right:64px;top:{Y0 + int(30 * K)}px;z-index:4">
    <p class="big" style="font-size:{int(64 * K)}px;font-weight:300;text-transform:uppercase;letter-spacing:.06em;line-height:1.1">Чорна<br>п’ятниця</p>
    <p class="num" style="font-size:{int(118 * K)}px;color:{YEL};margin-top:{int(24 * K)}px">−20…−40<span style="font-size:.5em;letter-spacing:0"> %</span></p>
    <p class="small" style="font-size:{int(34 * K)}px;margin-top:{int(26 * K)}px">{nb("На шовк із авторськими принтами: хустки, твіллі, маски для сну, резинки й подарункові набори.")}</p></div>
  {bar(label="Хустки · твіллі · маски · набори")}'''
    else:
        sh = int(880 * K); sy = Y1 - sh
        tiles = "".join(f'<div class="ph" style="left:{i * 360}px;top:{sy}px;width:356px;height:{sh}px"><img src="{PS}{f}" alt="" style="object-position:{p}"></div>' for i, (f, p) in enumerate(strip))
        body = f'''
  <div style="inset:0;background:{INK}"></div>
  {header(text="Знижки на шовк")}
  <div class="light" style="left:64px;right:64px;top:{Y0 + int(10 * K)}px;z-index:4">
    <p class="big" style="font-size:{int(96 * K)}px;font-weight:300;text-transform:uppercase;letter-spacing:.06em;line-height:1.08">Чорна<br>п’ятниця</p>
    <p class="num" style="font-size:{int(196 * K)}px;color:{YEL};margin-top:{int(20 * K)}px">−20…−40<span style="font-size:.5em;letter-spacing:0"> %</span></p>
    <p class="small" style="font-size:{int(42 * K)}px;margin-top:{int(28 * K)}px;max-width:900px">{nb("На шовк із авторськими принтами: хустки, твіллі, маски для сну, резинки й подарункові набори.")}</p></div>
  {tiles}
  <div style="left:0;right:0;top:{sy - 2}px;height:{int(140 * K)}px;background:{melt(True, bottom=False)}"></div>
  {bar(label="Хустки · твіллі · маски · набори")}'''
    ad("bf-01-hero", body, "The hero: the day's name thin and huge, the range in yellow, three silk frames in a strip")
hero()

# 02 · the square that is not black
square_card("bf-02-square", "khustka-flat-kolo-sontsia-88x88-01.jpg",
            "Квадрат. Не чорний.", f"Хустка 88 × 88 «Коло сонця» зі «Співочої душі» — {FOUR} зі знижкою.",
            "Malevich's square, only in silk: the flat scarf as a card on the black field")

# 03–05 · «Чорна п’ятниця. Біла хустка.» — a series of three: the colour of the scarf in the headline
full("bf-03-white", "mizh-flat.webp", "50% 50%", "<span style='color:#9A9088'>Чорна п’ятниця.</span> <em style='color:#fff'>Біла</em> хустка.",
     f"«Між нами» з колекції «Пробудження» — {FOUR} зі знижкою.", "The white scarf on the black field", root=True, split=.56, zoom=.9, ptop=TOPL + int(90 * K), side_fade=True)
full("bf-04-yellow", "khustka-flat-smilyvist-44x44-01.jpg", "50% 50%", "<span style='color:#9A9088'>Чорна п’ятниця.</span> <em>Жовта</em> хустка.",
     f"«Сміливість» із «Поклику душі», 44 × 44 — {FOUR} зі знижкою.", "The yellow scarf on the black field", split=.56, zoom=.88, ptop=TOPL + int(90 * K), side_fade=True)
full("bf-05-red", "riviera-red.jpg", "50% 18%", "<span style='color:#9A9088'>Чорна п’ятниця.</span> <em style='color:#E24B3B'>Червона</em> хустка.",
     f"Хустки чотирьох колекцій зі знижкою. Шовк, авторський принт, ручна обробка краю.", "The red scarf, the Riviera frame", root=True, split=.58, top_veil=.65)

# 06 · the only black thing worth buying
objw("bf-06-heart", "mask-sertsebyttia-chorna-v-chok-01.jpg", "Єдине чорне, що варто купити цієї п’ятниці.",
     f"Маска для сну «Серцебиття», чорна. Маски для сну зі знижкою.", "The black heart mask alone on white", ar=1250 / 1500, zoom=1.7, pos="50% 72%")

# 07 · the barcode of twillies
def barcode():
    tw = ["tvilli-shovkovyi-probudzhennia-04.jpg"] * 5; hs = [1.0, .66, .84, .52, .92]   # the one vertical twilly in columns of five heights — bars of five thicknesses, the tips in frame
    if SQ:
        col = 440; n = 4; top = Y0; hgt = Y1 - top; w = (1080 - 64 - col) // n
        strip = "".join(f'<div class="ph mult" style="left:{64 + col + i * w}px;top:{top + hgt - int(hgt * hs[i])}px;width:{w}px;height:{int(hgt * hs[i])}px"><img src="{PS}{f}" alt="" style="object-position:50% 50%"></div>' for i, f in enumerate(tw[:n]))
        lines = "".join(f'<i style="display:inline-block;width:{wd}px;height:100%;background:#141110;margin-right:{gap}px"></i>' for wd, gap in [(3, 4), (6, 3), (2, 5), (8, 4), (3, 3), (5, 6), (2, 3), (7, 4), (3, 5), (4, 3), (9, 4), (2, 4), (5, 3), (3, 6), (6, 3)] * 2)
        body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;width:{col - 40}px;top:{Y0 + int(20 * K)}px;z-index:4">{words("Штрихкод знижки.", f"Твіллі 84 × 5 «Пробудження» — і всі твіллі чотирьох колекцій зі знижкою. Скануйте очима.", 72, False)}
    <div style="height:{int(60 * K)}px;margin-top:{int(30 * K)}px;white-space:nowrap;overflow:hidden">{lines}</div></div>
  {strip}
  {bar(False)}'''
    else:
        n = 5; top = Y0 + int(200 * K); hgt = Y1 - top - int(120 * K); w = (1080 - 128) // n
        strip = "".join(f'<div class="ph mult" style="left:{64 + i * w}px;top:{top + hgt - int(hgt * hs[i])}px;width:{w}px;height:{int(hgt * hs[i])}px"><img src="{PS}{f}" alt="" style="object-position:50% 50%"></div>' for i, f in enumerate(tw[:n]))
        lines = "".join(f'<i style="display:inline-block;width:{wd}px;height:100%;background:#141110;margin-right:{gap}px"></i>' for wd, gap in [(3, 4), (6, 3), (2, 5), (8, 4), (3, 3), (5, 6), (2, 3), (7, 4), (3, 5), (4, 3), (9, 4), (2, 4), (5, 3), (3, 6), (6, 3)] * 5)
        body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0}px;z-index:4">{words("Штрихкод знижки.", f"Твіллі 84 × 5 «Пробудження» — і всі твіллі чотирьох колекцій зі знижкою. Скануйте очима.", 84, False)}</div>
  {strip}
  <div style="left:64px;right:64px;top:{top + hgt}px;height:{int(70 * K)}px;white-space:nowrap;overflow:hidden">{lines}</div>
  <p class="num ink" style="left:64px;top:{top + hgt + int(76 * K)}px;font-size:{int(22 * K)}px;letter-spacing:.3em;font-weight:400">2 0 3 0 4 0 · O B I I M Y · S I L K</p>
  {bar(False)}'''
    ad("bf-07-barcode", body, "Four twillies stand like the bars of a barcode; a barcode strip under them")
barcode()

# 08 · the belt
full("bf-08-belt", "hratsiia-belt.webp", "50% 40%", "Затягнути пояси? Навпаки.",
     f"Хустка «Грація» з «Дикої стихії» — як пояс. Хустки чотирьох колекцій зі знижкою.", "The scarf as a belt — the pun on belts", root=True, split=.58, zoom=1.0)

# 09 · sleep through it
full("bf-09-sleep", "mask-nizhnist-03.jpg", "22% 30%", "Проспати Чорну п’ятницю? Можна. У шовковій масці.",
     f"Маска для сну «Ніжність» із «Поклику душі». Маски для сну зі знижкою.", "The woman in the mask, the grey-white field", dark=False, split=.6, zoom=1.0, ph_bg="#f4f4f4", field="#f4f4f4")

# 10 · the bookmark
full("bf-10-bookmark", "bookmark-melodiia-dvokh-01.jpg", "45% 60%", "Зробіть закладку: Чорна п’ятниця.",
     f"Шовкова закладка для книги «Мелодія двох» — і вся «Співоча душа» зі знижкою.", "The silk bookmark in the book — a bookmark for the day", dark=False, split=.6, zoom=1.15, ptop=TOPL + int(90 * K))

# 11 · for him
full("bf-11-pashe", "pashe-svoboda-02.jpg", "100% 0%", "Чорна п’ятниця. І для нього.",
     f"Паше 44 × 44 «Свобода» в нагрудну кишеню — і хустки чотирьох колекцій зі знижкою.", "The pocket square — the men's frame", split=.58, zoom=1.9, origin="100% 0%", top_veil=.2)

# 12 · the sun in November
full("bf-12-kolo", "kolo-2.webp", "55% 30%", "Листопад темний. Хустка — ні.",
     f"«Коло сонця» 88 × 88 зі «Співочої душі» — {FOUR} зі знижкою.", "The sunflower scarf in the beige coat", root=True, split=.6)

# 13 · our Friday is yellow
def yellow():
    if SQ:
        pw = 520
        body = f'''
  <div style="inset:0;background:{YEL}"></div>
  <div class="ph" style="left:{1080 - pw}px;top:{Y0 - 20}px;width:{pw}px;height:{H - Y0 + 20}px;background:#fff"><img src="{PR}box-dots.jpg" alt="" style="object-position:60% 45%;transform:scale(1.35)"></div>
  <div style="left:{1080 - pw}px;top:0;width:140px;height:{H}px;background:linear-gradient(90deg,{YEL},rgba(242,183,5,0))"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;width:{1080 - pw - 64 + 60}px;top:{Y0 + int(30 * K)}px;z-index:4">{words("У нас п’ятниця жовта.", "Жовтий — наш колір. Чорний — лише назва п’ятниці. Знижки на шовк із авторськими принтами.", 76, False)}</div>
  {bar(False)}'''
    else:
        yph = int(H * .5)
        body = f'''
  <div style="inset:0;background:{YEL}"></div>
  <div class="ph" style="left:0;right:0;top:{Y0 - 10}px;height:{yph + 70 - Y0}px;background:#fff"><img src="{PR}box-dots.jpg" alt="" style="object-position:60% 45%;transform:scale(1.25)"></div>
  <div style="left:0;right:0;top:{yph - 200}px;height:262px;background:linear-gradient(0deg,{YEL},rgba(242,183,5,.85) 30%,rgba(242,183,5,0))"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;right:64px;top:{yph + int(30 * K)}px;z-index:4">{words("У нас п’ятниця жовта.", "Жовтий — наш колір. Чорний — лише назва п’ятниці. Знижки на шовк із авторськими принтами.", 92, False)}</div>
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
  <div class="ph" style="left:0;right:0;bottom:0;height:{int(H * .5)}px;-webkit-mask-image:linear-gradient(180deg,transparent,#000 60%);mask-image:linear-gradient(180deg,transparent,#000 60%)"><img src="{PR}hratsiia-flat.webp" alt="" style="object-position:50% 50%;opacity:.9;transform:scale(1.1)"></div>
  <div style="left:0;right:0;bottom:0;height:{BOTB + BAR + int(120 * K)}px;background:linear-gradient(0deg,rgba(20,17,16,.95) 50%,rgba(20,17,16,0));z-index:5"></div>
  {header()}
  <div class="light" style="left:64px;width:{x0 - 64 - 30}px;top:{Y0 + int(20 * K)}px;z-index:4">{words("Три бирки. Одна п’ятниця.", "Яка знижка на що — на obiimy.world. Хустки, твіллі, маски для сну, резинки й набори.", 68, True)}</div>
  {t}{bar()}'''
    else:
        tw, th = int(270 * K), int(380 * K); gap = int(36 * K); x0 = (1080 - 3 * tw - 2 * gap) // 2; y0 = Y0 + int(120 * K)
        t = "".join(f'<div style="left:{x0 + i * (tw + gap) + tw // 2}px;top:0;width:2px;height:{y0 + 20 + i * int(40 * K)}px;background:#8a7f70"></div><div class="tag" style="left:{x0 + i * (tw + gap)}px;top:{y0 + i * int(40 * K)}px;width:{tw}px;height:{th}px;transform:rotate({(-4, 2, -2)[i]}deg)"><p class="num" style="font-size:{int(96 * K)}px;font-weight:400;margin-top:{int(30 * K)}px">{v}</p><p class="kicker" style="font-size:{int(18 * K)}px;margin-top:{int(20 * K)}px;color:#8A6A12">Чорна п’ятниця</p></div>' for i, v in enumerate(vals))
        wy = y0 + th + int(170 * K); py = wy + int(300 * K)   # the words right under the tags; the scarf rises from under the words
        body = f'''
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="left:0;right:0;top:{py}px;bottom:0;-webkit-mask-image:linear-gradient(180deg,transparent,#000 60%);mask-image:linear-gradient(180deg,transparent,#000 60%)"><img src="{PR}hratsiia-flat.webp" alt="" style="object-position:50% 50%;opacity:.9;transform:scale(1.1)"></div>
  <div style="left:0;right:0;bottom:0;height:{BOTB + BAR + int(200 * K)}px;background:linear-gradient(0deg,rgba(20,17,16,.95) 40%,rgba(20,17,16,0));z-index:5"></div>
  {header()}
  {t}
  <div class="light" style="left:64px;right:64px;top:{wy}px;z-index:4">{words("Три бирки. Одна п’ятниця.", "Яка знижка на що — на obiimy.world. Хустки, твіллі, маски для сну, резинки й набори.", 84, True)}</div>
  {bar()}'''
    ad("bf-14-tags", body, "Three paper tags on strings: 20, 30, 40; the orange scarf rising from below")
tags()

# 15 · from behind
full("bf-15-back", "tvilli-shovkovyi-sokovyti-spohady-03.jpg", "50% 35%", "Чорна п’ятниця. Гарна і зі спини.",
     f"Твіллі 84 × 5 «Соковиті спогади» з «Пробудження» — у волоссі, на зап’ясті, на сумці. Твіллі зі знижкою.", "The twilly in the hair, seen from behind", split=.6, top_veil=.65, zoom=1.12)

# 16 · close your eyes to the prices
def masks():
    ms = [("mask-enerhiia-01.jpg", "50% 50%"), ("mask-melodiia-dvokh-01.jpg", "50% 50%"), ("mask-vpevnenist-01.jpg", "50% 50%")]
    if SQ:
        col = 470; top = Y0; hgt = (Y1 - top) // 3; px = 64 + col; pw = 1080 - 64 - px
        rows = "".join(f'<div class="ph mult" style="left:{px}px;top:{top + i * hgt}px;width:{pw}px;height:{hgt}px"><img src="{PS}{f}" alt="" style="object-position:{p};transform:scale(1.5)"></div>' for i, (f, p) in enumerate(ms))
        body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;width:{col - 30}px;top:{Y0 + int(20 * K)}px;z-index:4">{words("Заплющте очі. Ціни впали.", "Маски для сну «Енергія», «Мелодія двох», «Впевненість» — і решта принтів зі знижкою.", 72, False)}</div>
  {rows}{bar(False)}'''
    else:
        top = Y0 + int(300 * K); hgt = (Y1 - top) // 3
        rows = "".join(f'<div class="ph mult" style="left:0;right:0;top:{top + i * hgt}px;height:{hgt}px"><img src="{PS}{f}" alt="" style="object-position:{p};transform:scale({(1.15, 1.25, 1.2)[i] if K == 1 else 1.0}) translateX({(-3, 6, -3)[i]}%)"></div>' for i, (f, p) in enumerate(ms))
        body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0}px;z-index:4">{words("Заплющте очі. Ціни впали.", "Маски для сну «Енергія», «Мелодія двох», «Впевненість» — і решта принтів зі знижкою.", 84, False)}</div>
  {rows}{bar(False)}'''
    ad("bf-16-masks", body, "Three sleep masks stacked on white, each a little off-centre")
masks()

# 17 · 88 centimetres of silk
full("bf-17-88", "khustka-vidnovlennia-88x88-02.jpg", "60% 15%", "88 × 88 см шовку. До −40 %.",
     f"Хустка «Відновлення» 88 × 88 із «Дикої стихії». Хустки 44 · 65 · 88 см зі знижкою.", "The big pink shawl in the field", split=.6)

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · Black Friday</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;600&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("bf" + ("" if FORMAT == "plain" else "-" + FORMAT) + ".html")).write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "Black Friday banners", FORMAT)
