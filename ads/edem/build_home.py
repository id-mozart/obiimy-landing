"""KRAЇNA EDEM × OBIIMY banners for the home page of obiimy.world (1920 × 576, as the SOLO ones; 06.11.2026, «сделай несколько
вариантов баннеров для главной про эту коллаборацию, трипільську»). The lock-up: the partners' line, «Trypillia» in Cormorant,
«The Art of Origins» in italic, a gold pill with the facts (88 × 88 см, шовк, лімітований випуск), the outlined «Замовити хустку».
No price on the banners (06.11: the price lives only in the order section of the page). Art: the client's print and its cut-outs
(photo/edem) — the figure, the medallion, the pendants, the scarf; palette from the sale page (ink #16100C, cream #F3E9D8, gold #D9B86A).
  python3 edem/build_home.py                                   → edem/home.html
  cd ads && VW=2000 ADS=edem/home.html OUT=edem/out-home node render.mjs"""
import pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "solo"))
from kit import GRAIN

INK, INK2, CREAM, CREAM2, GOLD, GOLD2, PAPER = "#16100C", "#1F1610", "#F3E9D8", "rgba(243,233,216,.72)", "#D9B86A", "#B48A3A", "#F5EAD7"   # PAPER = the print's own background
PH = "../../photo/edem"
def E(name): return f"{PH}/{name}"

CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #666; font-family: 'Montserrat', sans-serif; -webkit-font-smoothing: antialiased; }
.ad { width: 1920px; height: 576px; position: relative; overflow: hidden; background: INK; margin: 20px auto; color: CREAM; }
.ad > * { position: absolute; margin: 0; }
.ad p { margin: 0; }
.ad::after { content: ""; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: .16; mix-blend-mode: soft-light; background-image: GRAIN; }
.ph { overflow: hidden; } .ph img { width: 100%; height: 100%; object-fit: cover; display: block; }
.cut img { display: block; width: 100%; height: auto; }
.lock { left: 84px; top: 50%; transform: translateY(-50%); line-height: 1; }
.lock .k { font-size: 24px; font-weight: 500; letter-spacing: .2em; text-transform: uppercase; color: GOLD; }
.lock .k i { font-style: normal; font-family: 'Cormorant Garamond', serif; font-weight: 400; font-size: 28px; letter-spacing: 0; margin: 0 10px; opacity: .8; }
.lock .s { font-family: 'Cormorant Garamond', serif; font-weight: 400; font-size: 168px; letter-spacing: -.005em; margin-top: 16px; margin-left: -6px; }
.lock .t { font-family: 'Cormorant Garamond', serif; font-style: italic; font-weight: 400; font-size: 64px; letter-spacing: .005em; margin-top: 2px; color: CREAM2; }
.ad .pill { display: inline-block; margin-top: 34px; font-size: 22px; font-weight: 500; letter-spacing: .01em; padding: 17px 28px; border-radius: 999px; background: GOLD; color: INK; line-height: 1; }
.ad .more { display: flex; width: max-content; align-items: center; gap: 14px; margin-top: 18px; font-size: 22px; font-weight: 500; letter-spacing: .02em; padding: 15px 28px 15px 30px; border: 1.5px solid rgba(243,233,216,.8); border-radius: 999px; color: CREAM; }
.ad .more::after { content: "→"; font-weight: 400; font-size: 24px; line-height: 1; transform: translateY(-1px); }
.light { background: PAPER; color: INK; } .light .lock .k { color: GOLD2; } .light .lock .t { color: rgba(22,16,12,.72); }
.light .more { color: INK; border-color: rgba(22,16,12,.7); }
.glow { border-radius: 50%; filter: blur(70px); opacity: .55; background: radial-gradient(circle, rgba(217,184,106,.55), rgba(217,184,106,0) 70%); }
.shadow { filter: drop-shadow(0 30px 40px rgba(22,16,12,.28)); }
""".replace("GRAIN", GRAIN).replace("CREAM2", CREAM2).replace("CREAM", CREAM).replace("INK", INK).replace("GOLD2", GOLD2).replace("GOLD", GOLD).replace("PAPER", PAPER)

ads = []
def ad(id, body, cls="", note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad {cls}" id="{id}">{body}\n</section>')

def lock(size=168, pill=True, more=True, sub=64):
    return (f'<div class="lock"><p class="k">KRAЇNA EDEM<i>×</i>OBIIMY</p><p class="s" style="font-size:{size}px">Trypillia</p>'
            f'<p class="t" style="font-size:{sub}px">The Art of Origins</p>'
            + ('<p class="pill">Шовкова хустка 88 × 88 см · лімітований випуск</p>' if pill else "") + ('<p class="more">Замовити хустку</p>' if more else "") + '</div>')

def feathered(img, left, feather, pos, veil=INK, w=None):
    """The picture from `left` to the right edge, melting into the field over `feather` px (as the chosen SOLO banner)."""
    r, g, b = int(veil[1:3], 16), int(veil[3:5], 16), int(veil[5:7], 16)
    return (f'<div class="ph" style="left:{left}px;right:0;top:0;bottom:0;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 {feather}px);mask-image:linear-gradient(90deg,transparent 0,#000 {feather}px)"><img src="{img}" alt="" style="object-position:{pos}"></div>'
            f'<div style="left:{left}px;top:0;bottom:0;width:{int(feather * .9)}px;background:linear-gradient(90deg,{veil} 0,rgba({r},{g},{b},.15) 40%,rgba({r},{g},{b},0) 100%)"></div>')

# A · the print itself to the right edge, melting into the ink — the medallion and the figures in the window
ad("home-e-canvas-dark", f'''
  <div style="inset:0;background:{INK}"></div>
  {feathered(E("art-2400.webp"), 760, 520, "50% 50%")}
  {lock()}''', note="The print on ink, feathered")

# B · the same on the print's own cream — the picture simply continues into the field, no mask needed
ad("home-e-canvas-light", f'''
  <div class="ph" style="left:1020px;top:-80px;width:736px;height:736px"><img src="{E('art-2400.webp')}" alt="" style="object-position:50% 50%"></div>
  <div style="left:1000px;top:0;bottom:0;width:140px;background:linear-gradient(90deg,{PAPER},rgba(245,234,215,0))"></div>
  <div style="right:0;top:0;bottom:0;width:170px;background:linear-gradient(270deg,{PAPER},rgba(245,234,215,0))"></div>
  <div style="left:0;right:0;top:0;height:60px;background:linear-gradient(180deg,{PAPER},rgba(245,234,215,0))"></div>
  <div style="left:0;right:0;bottom:0;height:60px;background:linear-gradient(0deg,{PAPER},rgba(245,234,215,0))"></div>
  {lock()}''', cls="light", note="The print on its own cream")

# C · the medallion alone on ink, a warm glow behind it, the pendants beside
ad("home-e-medallion-dark", f'''
  <div class="glow" style="left:1180px;top:-120px;width:820px;height:820px"></div>
  <div class="cut" style="left:1270px;top:38px;width:500px"><img src="{E('mandala.webp')}" alt=""></div>
  <div class="cut" style="left:1130px;top:300px;width:92px;opacity:.95"><img src="{E('pendant-round.webp')}" alt=""></div>
  <div class="cut" style="left:1790px;top:120px;width:92px;opacity:.95"><img src="{E('pendant-diamond.webp')}" alt=""></div>
  {lock()}''', note="The medallion on ink")

# D · the scarf as a thing: the draped square on cream, a soft shadow under it
ad("home-e-scarf-light", f'''
  <div class="cut shadow" style="left:1250px;top:14px;width:560px"><img src="{E('scarf.webp')}" alt=""></div>
  {lock()}''', cls="light", note="The scarf on cream")

# E · the golden figure — the Trypillian goddess — with the two pendants, on ink
ad("home-e-figure-dark", f'''
  <div class="glow" style="left:1240px;top:-80px;width:700px;height:740px;opacity:.4"></div>
  <div class="cut" style="left:1450px;top:28px;width:368px"><img src="{E('figure.webp')}" alt=""></div>
  <div class="cut" style="left:1270px;top:170px;width:110px"><img src="{E('pendant-round.webp')}" alt=""></div>
  <div class="cut" style="left:1230px;top:330px;width:100px;opacity:.9"><img src="{E('pendant-diamond.webp')}" alt=""></div>
  {lock()}''', note="The figure on ink")

# F · the print full-bleed: a horizontal band through the medallion, the lock-up on a cream veil at the left
ad("home-e-strip", f'''
  <div class="ph" style="inset:0"><img src="{E('art-2400.webp')}" alt="" style="object-position:50% 46%"></div>
  <div style="inset:0;background:linear-gradient(90deg,rgba(245,234,215,.97) 0%,rgba(245,234,215,.94) 36%,rgba(245,234,215,.55) 52%,rgba(245,234,215,0) 66%)"></div>
  {lock()}''', cls="light", note="The print full width, cream veil")

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · EDEM home banners</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,300;1,400&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / "home.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "edem home banners")
