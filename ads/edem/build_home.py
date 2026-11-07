"""KRAЇNA EDEM × OBIIMY banners for the home page of obiimy.world (1920 × 576, as the SOLO ones; 06.11.2026, «сделай несколько
вариантов баннеров для главной про эту коллаборацию, трипільську»). The lock-up: the partners' line, «Трипілля» in Cormorant,
«Мистецтво витоків» in italic (07.11: the Ukrainian name on the Ukrainian page, as on the landing), a gold pill with the facts (88 × 88 см, шовк, лімітований випуск), the outlined «Замовити хустку».
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
.ad .pill { display: inline-block; margin-top: 34px; font-size: 26px; font-weight: 500; letter-spacing: .01em; padding: 17px 28px; border-radius: 999px; background: GOLD; color: INK; line-height: 1; }
.ad .more { display: flex; width: max-content; align-items: center; gap: 14px; margin-top: 18px; font-size: 26px; font-weight: 500; letter-spacing: .02em; padding: 15px 28px 15px 30px; border: 1.5px solid rgba(243,233,216,.8); border-radius: 999px; color: CREAM; }
.ad .more::after { content: "→"; font-weight: 400; font-size: 24px; line-height: 1; transform: translateY(-1px); }
.light { background: PAPER; color: INK; } .light .lock .k { color: #9A7430; font-weight: 600; } .light .lock .t { color: rgba(22,16,12,.72); }
.light .more { color: INK; border-color: rgba(22,16,12,.7); }
.glow { border-radius: 50%; filter: blur(70px); opacity: .55; background: radial-gradient(circle, rgba(217,184,106,.55), rgba(217,184,106,0) 70%); }
.shadow { filter: drop-shadow(0 30px 40px rgba(22,16,12,.28)); }
/* G · the landing's header: the light page (--bg #F7F1E6, ink text, gold #B48A3A), the mandala faint behind, the scarf as a tilted card */
.hero { background: radial-gradient(70% 60% at 68% 45%, rgba(180,138,58,.18), transparent 65%), #F7F1E6; color: #2A2017; }
.hero .mandala { opacity: .14; filter: sepia(.4) saturate(.7); } .hero .mandala img { width: 100%; height: auto; display: block; }
.hero .card { perspective: 1400px; } .hero .card img { width: 100%; height: auto; display: block; transform: rotateY(-11deg) rotateX(5deg); filter: drop-shadow(0 40px 50px rgba(58,42,28,.42)) drop-shadow(0 4px 10px rgba(58,42,28,.2)); }
.hero .sheen { position: absolute; inset: 6% 10%; background: linear-gradient(115deg, transparent 38%, rgba(255,255,255,.26) 48%, transparent 58%); mix-blend-mode: screen; transform: rotateY(-11deg) rotateX(5deg); }
.hero .orn img { width: 100%; height: auto; display: block; filter: drop-shadow(0 18px 20px rgba(58,42,28,.3)); }
.hero .dust { width: 4px; height: 4px; border-radius: 50%; background: #B48A3A; box-shadow: 0 0 6px rgba(180,138,58,.9); }
.hero .copy { left: 84px; top: 50%; transform: translateY(-50%); line-height: 1; }
.hero .logos { display: flex; align-items: center; gap: 18px; } .hero .logos img { display: block; height: 26px; width: auto; } .hero .logos img.edem { height: 72px; margin-top: -6px; } .hero .logos i { font-family: 'Cormorant Garamond', serif; font-style: normal; font-size: 22px; opacity: .55; }
.hero .eyebrow { margin-top: 24px; font-size: 19px; font-weight: 600; letter-spacing: .28em; text-transform: uppercase; color: #8A6628; }
.hero h1 { margin: 10px 0 0 -4px; font-family: 'Cormorant Garamond', serif; font-weight: 400; font-size: 88px; line-height: .98; letter-spacing: -.005em; } .hero h1 i { font-style: italic; color: #B48A3A; }
.hero .lead { margin-top: 18px; max-width: 640px; font-family: 'Cormorant Garamond', serif; font-weight: 300; font-size: 31px; line-height: 1.3; color: rgba(42,32,23,.68); }
.hero .btn { display: inline-block; margin-top: 28px; font-size: 19px; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; padding: 21px 30px; background: #B48A3A; color: #F7F1E6; }
.hero .facts { margin-top: 24px; display: flex; gap: 28px; font-size: 16px; font-weight: 500; letter-spacing: .12em; text-transform: uppercase; color: rgba(42,32,23,.68); } .hero .facts b { color: #B48A3A; font-weight: 600; }
""".replace("GRAIN", GRAIN).replace("CREAM2", CREAM2).replace("CREAM", CREAM).replace("INK", INK).replace("GOLD2", GOLD2).replace("GOLD", GOLD).replace("PAPER", PAPER)

ads = []
def ad(id, body, cls="", note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad {cls}" id="{id}">{body}\n</section>')

def lock(size=168, pill=True, more=True, sub=64):
    return (f'<div class="lock"><p class="k">KRAЇNA EDEM<i>×</i>OBIIMY</p><p class="s" style="font-size:{size}px">Трипілля</p>'
            f'<p class="t" style="font-size:{sub}px">Мистецтво витоків</p>'
            + ('<p class="pill">Шовк · 88 × 88 см · лімітований випуск</p>' if pill else "") + ('<p class="more">Замовити хустку</p>' if more else "") + '</div>')

def feathered(img, left, feather, pos, veil=INK, w=None):
    """The picture from `left` to the right edge, melting into the field over `feather` px (as the chosen SOLO banner)."""
    r, g, b = int(veil[1:3], 16), int(veil[3:5], 16), int(veil[5:7], 16)
    return (f'<div class="ph" style="left:{left}px;right:0;top:0;bottom:0;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 {feather}px);mask-image:linear-gradient(90deg,transparent 0,#000 {feather}px)"><img src="{img}" alt="" style="object-position:{pos}"></div>'
            f'<div style="left:{left}px;top:0;bottom:0;width:{int(feather * .9)}px;background:linear-gradient(90deg,{veil} 0,rgba({r},{g},{b},.15) 40%,rgba({r},{g},{b},0) 100%)"></div>')

# A · the print itself to the right edge, melting into the ink — the medallion and the figures in the window
ad("home-e-canvas-dark", f'''
  <div style="inset:0;background:{INK}"></div>
  <div style="left:640px;right:0;top:0;bottom:0;overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 320px);mask-image:linear-gradient(90deg,transparent 0,#000 320px)"><img src="{E('art-2400.webp')}" alt="" style="position:absolute;left:10px;top:-482px;width:1500px;height:1500px"></div>
  <div style="left:640px;top:0;bottom:0;width:290px;background:linear-gradient(90deg,{INK} 0,rgba(22,16,12,.15) 40%,rgba(22,16,12,0) 100%)"></div>
  {lock()}''', note="The print on ink, feathered")

# B · the same on the print's own cream — the picture simply continues into the field, no mask needed
ad("home-e-canvas-light", f'''
  <img src="{E('art-2400.webp')}" alt="" style="left:860px;top:-262px;width:1100px;height:1100px">
  <div style="left:880px;top:0;bottom:0;width:140px;background:linear-gradient(90deg,{PAPER} 0,{PAPER} 30%,rgba(245,234,215,0))"></div>
  {lock()}''', cls="light", note="The print on its own cream")

# C · the medallion alone on ink, a warm glow behind it, the pendants beside
ad("home-e-medallion-dark", f'''
  <div class="glow" style="left:965px;top:-160px;width:900px;height:900px"></div>
  <div class="cut" style="left:1105px;top:53px;width:470px"><img src="{E('mandala.webp')}" alt=""></div>
  {lock()}''', note="The medallion on ink")

# D · the scarf as a thing: the draped square on cream, a soft shadow under it
ad("home-e-scarf-light", f'''
  <div class="cut shadow" style="left:1080px;top:2px;width:580px"><img src="{E('scarf.webp')}" alt=""></div>
  {lock()}''', cls="light", note="The scarf on cream")

# E · the corner of the print close up — the Trypillian figure among the cords, the border and the corner ornament — melting into the ink
ad("home-e-figure-dark", f'''
  <div style="inset:0;background:{INK}"></div>
  {feathered(E("art-corner.webp"), 820, 460, "50% 28%")}
  {lock()}''', note="The corner of the print on ink")

# F · the print full-bleed: a horizontal band through the medallion, the lock-up on a cream veil at the left
ad("home-e-strip", f'''
  <img src="{E('art-2400.webp')}" alt="" style="left:700px;top:-412px;width:1400px;height:1400px">
  <div style="inset:0;background:linear-gradient(90deg,{PAPER} 0%,{PAPER} 42%,rgba(245,234,215,0) 52%)"></div>
  {lock()}''', cls="light", note="The print full width, cream veil")

# G · the landing's header as a banner: logos, eyebrow, the title in two lines with the italic gold second one, the lead, the gold
#     button and the facts at the left; the faint mandala, the tilted scarf card, the figurine and the pendants at the right (edem-motion-light)
_dust = "".join(f'<i class="dust" style="left:{x}px;top:{y}px;opacity:{o}"></i>' for x, y, o in
                [(960, 110, .7), (1010, 470, .6), (1270, 540, .5), (1610, 520, .7), (1700, 300, .5), (1860, 150, .8), (1880, 470, .6), (1420, 560, .6), (1790, 60, .5)])
def hero(id, card, fig, pend=None, mandala="left:900px;top:-130px;width:860px", tilt=None, note=""):   # mandala=None — without the faint medallion
    """The header banner with the scarf card placed by `card` (left/top/width css); 07.11 «давай несколько вариантов, так, чтобы крупнее была сама хустка»."""
    t = f' style="transform:{tilt}"' if tilt else ""
    ad(id, f'''
  {f'<div class="mandala" style="{mandala}"><img src="{E("mandala.webp")}" alt=""></div>' if mandala else ""}
  {_dust}
  <div class="card" style="{card}"><img src="{E('scarf.webp')}" alt=""{t}><i class="sheen"{t}></i></div>
  {f'<div class="orn" style="{pend}"><img src="{E("pendant-round.webp")}" alt=""></div>' if pend else ""}
  <div class="orn" style="{fig}"><img src="{E('figure.webp')}" alt=""></div>
  <div class="copy">
    <div class="logos"><img src="../../brand/logo-ink.svg" alt="OBIIMY"><i>×</i><img class="edem" src="../../brand/edem-mark.png" alt="Kraїna Edem"></div>
    <p class="eyebrow">Спільний мистецький проєкт</p>
    <h1>Трипілля —<br><i>Мистецтво витоків</i></h1>
    <p class="lead">Мистецтво бути ближче. Шовкова хустка за трипільськими мотивами.</p>
    <p class="btn">Замовити хустку</p>
  </div>''', cls="hero", note=note)

# G · as the page: the card 446 wide, the figurine standing on the field and touching the card's lower-left corner, one pendant (70 px) at its upper-right corner (panel, round 5)
hero("home-e-hero-light", card="left:1112px;top:64px;width:446px", fig="left:1022px;top:326px;width:118px", pend="left:1478px;top:14px;width:70px", note="The landing's header as a banner")
# H · the scarf a size up: the card 720 wide, the full height of the banner, a hair over the top and bottom edges
hero("home-e-hero-big", card="left:1070px;top:-60px;width:720px", fig="left:1030px;top:332px;width:118px", mandala="left:860px;top:-200px;width:1000px;opacity:.08", note="The header, the scarf larger")
# H2 · the same a touch smaller, so the scarf stays clear of the top and bottom edges («чуточку поменьше хустка, чтобы в края не влипало», 07.11)
hero("home-e-hero-mid", card="left:1120px;top:-22px;width:636px", fig="left:1066px;top:330px;width:112px", mandala="left:880px;top:-170px;width:940px;opacity:.12", note="The header, the scarf large but clear of the edges")
# I · the scarf over the edges: the card 920 wide, the medallion of the print in the middle of the field, the corners cut by the frame
hero("home-e-hero-bleed", card="left:980px;top:-160px;width:920px", fig="left:958px;top:326px;width:118px", mandala="left:820px;top:-260px;width:1100px", note="The header, the scarf over the edges")
# J · the scarf tilted as a card in perspective: 820 wide, a stronger turn, so it keeps the height but reads as a thing in space
hero("home-e-hero-tilt", card="left:1150px;top:-110px;width:820px", fig="left:1196px;top:328px;width:118px", mandala="left:880px;top:-230px;width:1050px", tilt="rotateY(-13deg) rotateX(4deg)", note="The header, the scarf tilted and larger")
# K · the scarf entering from the right edge: 840 wide, cut by the right side of the frame, more air for the text
hero("home-e-hero-right", card="left:1140px;top:-120px;width:840px", fig="left:1110px;top:324px;width:118px", mandala=None, note="The header, the scarf at the right edge")

# V · frames from the client's video (photo/edem/video, 720 × 1280 stills from edem-video.mp4, 07.11 «пару вариантов из кадров из видео»):
#     the photo from x = 960 to the right edge melting into the ink over 420 px, the lock-up at the left — the technique of the chosen SOLO banner
# panel, round 7: a shorter melt on the tree frame (the pendants and the border of the print stay), the sky frame a moment earlier (the sun behind
# the silk) with a dark vignette from the top, the portrait replaced by the frame at the sculpture (1:09) where the scarf lies across the body
for id, img, left, feather, pos, extra, note in [
        ("home-e-video-tree", "frame-tree.jpg", 1000, 300, "50% 9%", "", "Video frame: the scarf open, in the tree"),
        ("home-e-video-sky", "frame-sky.jpg", 1100, 420, "50% 32%", '<div style="left:1100px;right:0;top:0;height:260px;background:linear-gradient(180deg,rgba(22,16,12,.55),rgba(22,16,12,0))"></div>', "Video frame: the scarf flying against the sun"),
        ("home-e-video-portrait", "frame-sculpture.jpg", 1250, 380, "50% 30%", "", "Video frame: the scarf across the body, at the sculpture")]:   # a narrower window: the face and the scarf down to the waist
    ad(id, f'''
  <div style="inset:0;background:{INK}"></div>
  {feathered(E("video/" + img), left, feather, pos)}{extra}
  {lock()}''', note=note)

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · EDEM home banners</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,300;1,400&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / "home.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "edem home banners")
