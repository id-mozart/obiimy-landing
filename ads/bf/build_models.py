"""Black Friday, the second series (07.11.2026, client: «ещё варианты — больше картинок с моделями»). The same idea — a silk
brand's Black Friday is not black — told through the campaign photographs with models: the brand lookbook (photo/lookbook),
the campaign frames (photo/*.webp) and the set galleries of obiimy.world (photo/site). Nothing from SOLO. The discount is the
client's range only («Знижки до −40 %» in the pill), no per-item percentage, no crossed-out prices. Print names and collections
as in review/SITE-FACTS.md («Колекції»); the English names of the lookbook pages mapped through review/catalog.json.
Output: bfm[-<format>].html → out-models[-<format>]/*.jpg  (cd ads && ADS=bf/bfm.html OUT=bf/out-models node render.mjs)."""
import pathlib
from common import *
HERE = pathlib.Path(__file__).parent
LB = "lookbook/"; ST = "site/"

def tall(id, img, pos, big, small, note="", size=84, zoom=1.0, origin="50% 50%", label=None, veil=.5, lift=0):
    """The photograph fills the whole frame, the words stand at the bottom on a long dark gradient — the fashion-ad layout.
    In the square the photo takes the left half (as in `full`)."""
    if SQ: return full(id, img, pos, big, small, note, dark=True, size=size, root=True, zoom=zoom, label=label, origin=origin)
    body = f'''
  <div style="inset:0;background:{INK}"></div>
  <div class="ph" style="inset:0"><img src="{PR}{img}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:0;right:0;top:0;height:{int(280 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,{veil}),rgba(12,9,8,0))"></div>
  <div style="left:0;right:0;bottom:0;height:{int(H * .62)}px;background:linear-gradient(0deg,rgba(20,17,16,1) 0,rgba(20,17,16,.96) 28%,rgba(20,17,16,.55) 62%,rgba(20,17,16,0) 100%)"></div>
  {header(True, hdr_text(big))}
  <div class="light" style="left:64px;right:64px;bottom:{H - Y1 + int(lift * K)}px;z-index:4">{words(big, small, size, True)}</div>
  {bar(True, label)}'''
    ad(id, body, note)

# ─── the series ───────────────────────────────────────────────────────────────────────────────────────────────────────

COLL = "принти «Співочої душі», «Поклику душі», «Пробудження» й «Дикої стихії»"

# 01 · the faces: six portraits in a grid, the day's name under them
def faces():
    ph = [(LB + "lb24-26-L.webp", "50% 15%"), (LB + "lb07-08-L.webp", "50% 20%"), (LB + "lb51-53-L.webp", "50% 25%"),
          (LB + "lb26-28-R.webp", "50% 15%"), (LB + "lb43-45-L.webp", "50% 20%"), (LB + "lb47-49-L.webp", "50% 15%")]
    gap = 8
    cols, rows = (2, 3) if FORMAT in ("plain", "story") else (3, 2)
    text_h = int((360 if cols == 2 else 270) * K)
    avail = Y1 - Y0 - text_h
    tw = (1080 - gap * (cols - 1)) // cols; th = min((avail - gap * (rows - 1)) // rows, int(tw * 1.25))
    top = Y0
    tiles = "".join(f'<div class="ph" style="left:{(i % cols) * (tw + gap)}px;top:{top + (i // cols) * (th + gap)}px;width:{tw}px;height:{th}px"><img src="{PR}{f}" alt="" style="object-position:{p}"></div>' for i, (f, p) in enumerate(ph))
    ty = top + rows * th + (rows - 1) * gap
    body = f'''
  <div style="inset:0;background:{INK}"></div>{tiles}
  {header()}
  <div class="light" style="left:64px;right:64px;top:{ty + int(56 * K)}px;bottom:{H - Y1}px;z-index:4">{words("Усі обличчя Чорної п’ятниці.", "Хустки, твіллі, маски для сну й набори чотирьох колекцій — зі знижкою.", 76 if cols == 2 else 64, True)}</div>
  {bar()}'''
    ad("bfm-01-faces", body, "Six lookbook portraits in a grid, the headline under them")
faces()

# 02 · black is what everyone wears; the silk is you
full("bfm-02-black", LB + "lb43-45-L.webp", "30% 12%", "Чорне носять усі. Шовк — ви.",
     "Твіллі «Сміливість» із «Поклику душі» — туго на шиї, на чорному топі.", "Courage twilly tight around the neck on a black top (panel r1: `full` instead of `tall` — the 850 px lookbook page is not stretched 1.75×)", root=True, split=.6, top_veil=.72)

# 03 · the open back
full("bfm-03-back", "enerhiia-back.webp", "50% 18%", "Відкрита спина. Відкриті знижки.",
     "Принт «Енергія» з «Поклику душі» — на спущеному плечі білої сорочки.", "The model from the back, the Energy scarf on the shoulder", root=True, split=.6, top_veil=.35)

# 04 · the prices squatted
full("bfm-04-sat", LB + "lb40-42-R.webp", "50% 30%", "Ціни присіли.",
     "Хустка «Впевненість» із «Поклику душі». Хустки 44 · 65 · 88 см — зі знижкою.", "The model crouching by the white columns in the low sun", root=True, split=.6, top_veil=.25)

# 05 · a knot to remember
full("bfm-05-knot", LB + "lb13-15-L.webp", "50% 55%", "Вузлик на пам’ять: Чорна п’ятниця.",
     "«Поцілунок сонця» з «Пробудження» — бантом на зап’ясті, на чорному жакеті.", "Sun Kiss twilly tied as a bow on the wrist, black blazer", root=True, split=.64, top_veil=.6)

# 06 · don't lose your head — tie it
tall("bfm-06-head", LB + "lb48-50-R.webp", "50% 6%", "Не втрачайте голову. Пов’яжіть її.",
     "Хустка «Літнє поле» з «Поклику душі» — як косинка.", "Summer Field headscarf, profile, bare shoulders", zoom=1.02, veil=.5)

# 07 · hats off — and the prices
tall("bfm-07-hat", LB + "lb42-44-R.webp", "50% 8%", "Знімаємо капелюха. І ціни.",
     "Хустка «Сміливість» із «Поклику душі» — на тулії чорного солом’яного капелюха.", "The model from the back holding the black hat above her head, the twilly around its crown", zoom=1.0, veil=.6)

# 08 · the dress code of the Friday
full("bfm-08-tie", ST + "set-prystrast-02.jpg", "50% 30%", "Дрес-код п’ятниці: шовк.",
     "Твіллі «Пристрасть» із «Поклику душі» — як краватка під комір білої сорочки.", "The twilly as a tie on the white shirt; the white field", root=True, dark=False, split=.6, ph_bg="#f3f3f3")

# 09 · in sunglasses, because the discounts are blinding (panel r1: the brick-wall frame had a branded temple on the glasses — swapped for the lookbook page with plain glasses)
full("bfm-09-glasses", LB + "lb54-56-R.webp", "50% 18%", "В окулярах. Бо знижки сліпучі.",
     "Хустка — як косинка, під підборіддя. Хустки 44 · 65 · 88 см зі знижкою.", "Sitting in the black chair in dark glasses, the lavender headscarf; the white field", root=True, dark=False, split=.6, ph_bg="#ececec", zoom=1.08)

# 10 · braid the discount in
full("bfm-10-braid", ST + "set-tvilli-845-ta-khustky-4444-smilyvy-02.jpg", "50% 42%", "Заплетіть знижку в косу.",
     "Набір «твіллі 84 × 5 + хустка 44 × 44» «Сміливий дотик» з «Дикої стихії» — твіллі вплетений у хвіст.", "The braid with the twilly, close, on the grey studio (the slug smilyvy- is «Сміливий дотик», smilyvist- is «Сміливість»)", root=True, dark=False, split=.6, ph_bg="#e9e7e4", zoom=1.15, origin="50% 60%", top_light=.85)

# 11 · two scarves, one Friday
tall("bfm-11-two", "dotyk-1.webp", "50% 28%", "Дві хустки. Одна п’ятниця.",
     "«Сміливий дотик» і «Натхнення» з «Дикої стихії» — обидві на тренчі.", "Two leopard-and-flower scarves on the trench, the field behind", zoom=1.0, veil=.3)

# 12 · Black Friday — and you in white
full("bfm-12-white", "mizh-2.webp", "60% 25%", "Чорна п’ятниця. Ви — в білому.",
     "Хустка «Між нами» з «Пробудження» — на плечі білого пальта.", "The white coat, the hydrangea scarf; the white field (panel r1: zoomed in and to the right, the glasses smaller)", root=True, dark=False, split=.6, zoom=1.2, origin="100% 30%")

# 13 · three ponytails, one Friday
def trio():
    ph = [(ST + "set-tvilli-845-ta-khustky-4444-natkhne-02.jpg", "50% 20%"), (ST + "set-tvilli-845-ta-khustky-4444-probudz-02.jpg", "50% 20%"), (ST + "set-tvilli-845-ta-khustky-4444-vpevnen-02.jpg", "50% 20%")]
    text_h = int((330 if FORMAT in ("plain", "story") else 250) * K)
    sy = Y0 + text_h; sh = min(int(1180 * K), Y1 - sy)   # the strip hugs the words; a little air above the pill row
    tiles = "".join(f'<div class="ph" style="left:{i * 360}px;top:{sy}px;width:356px;height:{sh}px;background:#e9e7e4"><img src="{PR}{f}" alt="" style="object-position:{p}"></div>' for i, (f, p) in enumerate(ph))
    body = f'''
  <div style="inset:0;background:{WHITE}"></div>{tiles}
  {header(False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0 + int(10 * K)}px;z-index:4">{words("Три хвости. Одна п’ятниця.", "Набори «твіллі 84 × 5 + хустка 44 × 44»: «Натхнення», «Пробудження», «Впевненість» — зі знижкою.", 76, False)}</div>
  {bar(False)}'''
    ad("bfm-13-three", body, "Three set photographs from the back in a strip, the words above")
trio()

# 14 · silk on the neck, a discount on silk
full("bfm-14-choker", LB + "lb09-11-L.webp", "40% 40%", "Шовк на шиї. Знижка на шовк.",
     "Твіллі «Тиша серця» зі «Співочої душі» — як чокер. Твіллі зі знижкою.", "The twilly as a choker with a pendant, close", root=True, split=.58, top_veil=.3)

# 15 · the only black thing here is the hat
full("bfm-15-blackhat", LB + "lb51-53-L.webp", "60% 20%", "Єдине чорне тут — капелюх.",
     "Твіллі «Ніжність» із «Поклику душі» — під підборіддям, під чорним солом’яним капелюхом.", "Portrait under the black straw hat, the blue twilly tied under the chin (panel r1: `full`, the left eye inside the frame)", root=True, split=.6, top_veil=.3)

# 16 · Black Friday from scratch
full("bfm-16-scratch", LB + "lb24-26-L.webp", "50% 25%", "Чорна п’ятниця з чистого листа.",
     "Хустка «З чистого листа» з «Дикої стихії» — на шиї, у полі.", "From Scratch scarf on the neck, the brunette looks into the camera", root=True, split=.6, top_veil=.25)

# 17 · the only black thing is the dress
tall("bfm-17-dress", "probudzhennia-2.webp", "50% 15%", "У чорному — лише сукня.",
     "Хустка «Пробудження» з однойменної колекції — на плечах, вузол у руці.", "The iris scarf on the shoulders of the black pleated dress", zoom=1.02, veil=.6)

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · Black Friday · models</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;600&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("bfm" + ("" if FORMAT == "plain" else "-" + FORMAT) + ".html")).write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "Black Friday model banners", FORMAT)
