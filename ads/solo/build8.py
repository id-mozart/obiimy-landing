"""SOLO laconic single-product banners (1080×1920, plain banner): one product, its name, price and a button.
No sizes, no descriptions. Three looks: on the print colour, on paper, on dark. Prices from obiimy.world.
Output: solo8.html → out8/*.jpg"""
import pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit import P, PP, CUT, LOGO_W, LOGO_K, GRAIN

CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #555; font-family: 'Onest', Arial, sans-serif; -webkit-font-smoothing: antialiased; }
.ad { width: 1080px; height: 1920px; position: relative; overflow: hidden; margin: 20px auto; }
.ad p { margin: 0; }
.ad::after { content: ""; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: .22; mix-blend-mode: soft-light; background-image: GRAIN; }
.in { position: absolute; inset: 70px 70px 96px; display: flex; flex-direction: column; align-items: center; text-align: center; }
.top { align-self: stretch; display: flex; justify-content: space-between; align-items: center; }
.top img { height: 44px; display: block; }
.lbl { font-family: 'Montserrat', sans-serif; font-size: 26px; font-weight: 500; letter-spacing: .16em; text-transform: uppercase; white-space: nowrap; }
.stage { flex: 1; min-height: 0; align-self: stretch; position: relative; margin: 60px 0 70px; }
.stage img { position: absolute; left: 4%; top: 4%; width: 92%; height: 92%; object-fit: contain; filter: drop-shadow(0 50px 60px rgba(0,0,0,.4)); }
.kick { font-family: 'Montserrat', sans-serif; font-size: 32px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; }
.ad .name { font-family: 'Playfair Display', serif; font-style: italic; font-weight: 700; line-height: 1; letter-spacing: -.01em; margin-top: 16px; text-wrap: balance; }
.ad .price { font-family: 'Playfair Display', serif; font-weight: 400; font-size: 84px; line-height: 1; margin-top: 44px; white-space: nowrap; }
.cta { font-family: 'Onest'; font-weight: 600; font-size: 34px; padding: 28px 70px; border-radius: 999px; margin-top: 44px; white-space: nowrap; }
""".replace("GRAIN", GRAIN)

LOOKS = {
    # look: (background, text colour, kicker colour, logo, button bg, button text, price style)
    "colour": ("linear-gradient(165deg,{c},{deep})", "#fff", "rgba(255,255,255,.85)", LOGO_W, "#F2B705", "#141216", ""),
    "paper": ("#F1E8D8", "#1B1613", "#6B5F55", LOGO_K, "#1B1613", "#F3EADB", ""),
    "dark": ("radial-gradient(80% 50% at 50% 38%,#3A302B,#141110 75%)", "#F3EADB", "rgba(243,234,219,.75)", LOGO_W, "#F3EADB", "#141216",
             "background:#F2B705;color:#141216;padding:12px 40px;border-radius:999px;font-size:72px"),
}

ads = []
def one(id, look, cut, kicker, name, price, cta, colour="#2A2320", deep="#141110", rot=-5, note="", pic=None, bg_override=None):
    bg, fg, kc, logo, bbg, bfg, pstyle = LOOKS[look]
    bg = bg_override or bg.format(c=colour, deep=deep)
    pic = pic or f'<img src="{CUT(cut)}" alt="" style="transform:rotate({rot}deg)">'
    size = 150 if len(name) <= 9 else 112
    ads.append(f'''
<!-- {note} -->
<section class="ad" id="{id}" style="background:{bg};color:{fg}">
  <div class="in">
    <div class="top"><img src="{logo}" alt="Obiimy"><p class="lbl" style="color:{kc}">Шовкові вироби</p></div>
    <div class="stage">{pic}</div>
    <p class="kick" style="color:{kc}">{kicker}</p>
    <p class="name" style="font-size:{size}px">«{name}»</p>
    <p class="price" style="{pstyle}">{price}</p>
    <div class="cta" style="background:{bbg};color:{bfg}">{cta}</div>
  </div>
</section>''')

PRICE = {"iskra": "4 800 грн", "flirt": "4 800 грн", "puls": "2 400 грн", "zolote": "2 400 грн", "avantiura": "6 600 грн", "tysha": "6 600 грн", "krok": "2 400 грн"}

# 1 — every scarf on the colour of its print
for i, p in enumerate(P, 1):
    one(f"m{i:02d}-scarf-{p['id']}", "colour", p["flat"], "Шовкова хустка", p["name"], PRICE[p["id"]], "Купити",
        colour=p["c"], deep=p["deep"], rot=-5 if i % 2 else 5, note=f"Scarf on colour: {p['name']}")

# 2 — every twilly on paper
for i, p in enumerate(P, 8):
    one(f"m{i:02d}-twilly-{p['id']}", "paper", p["tw"], "Шовкова твіллі", p["name"], "1 600 грн", "Обрати твіллі",
        rot=-4 if i % 2 else 4, note=f"Twilly on paper: {p['name']}")

# 3 — every scarf on dark, price on the yellow brand pill
for i, p in enumerate(P, 15):
    one(f"m{i:02d}-scarf-dark-{p['id']}", "dark", p["flat"], "Шовкова хустка", p["name"], PRICE[p["id"]], "Замовити",
        rot=6 if i % 2 else -6, note=f"Scarf on dark: {p['name']}")

# 4 — the scrunchie
one("m22-scrunchie-flirt", "paper", "flirt-scr-1", "Шовкова резинка", "Флірт", "700 грн", "Купити", note="Scrunchie", bg_override="#F1F1F1",
    pic='<img src="src/flirt-scr-1-2k.webp" alt="" style="left:0;top:0;width:100%;height:100%;object-fit:cover;object-position:50% 55%;filter:none;mix-blend-mode:multiply;-webkit-mask-image:radial-gradient(70% 70% at 50% 50%,#000 72%,transparent 100%);mask-image:radial-gradient(70% 70% at 50% 50%,#000 72%,transparent 100%)">')

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · SOLO single product</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;1,700&family=Montserrat:wght@500&family=Onest:wght@600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / "solo8.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "single-product banners")
