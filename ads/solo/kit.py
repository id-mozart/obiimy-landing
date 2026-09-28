"""Shared kit for SOLO creatives: data, CSS, helpers.
Copy follows the press release (review/SOLO-RELEASE.md); prices and formats from obiimy.world (28.09.2026)."""

SLOGAN = "Шовкова свобода: жіноча сила крізь десятиліття"
CTA = "Обрати свій принт · obiimy.world"
LOGO_W = "../../brand/logo-white.png"
LOGO_K = "../../brand/logo-ink.png"

# press-release order = the journey
P = [
    dict(id="iskra", name="Іскра", c="#2F63A8", deep="#1E4A86", flat="iskra-65-1", tw="iskra-tw-1",
         short="Сміливість бути помітною",
         state="Внутрішня енергія, сміливість бути помітною та здатність запалювати зміни навколо себе.",
         formats=[("Хустка", "65 × 65", "4 800"), ("Твіллі", "84 × 5", "1 600")]),
    dict(id="flirt", name="Флірт", c="#6F8A58", deep="#566F42", flat="flirt-65-1", tw="flirt-tw-2",
         short="Флірт — це насамперед стан",
         state="Віра в перемогу, оптимізм і мистецтво невимушеної жіночності. Флірт — це насамперед стан, уміння насолоджуватися собою, життям і моментом.",
         formats=[("Хустка", "65 × 65", "4 800"), ("Твіллі", "84 × 5", "1 600"), ("Резинка", "для волосся", "700")]),
    dict(id="puls", name="Пульс", c="#4E8B3A", deep="#35692A", flat="puls-44-1", tw="puls-tw-2",
         short="Внутрішній ритм",
         state="Природна сила та внутрішня опора. Внутрішній ритм, що залишається незмінним, навіть коли навколо змінюється все.",
         formats=[("Хустка", "44 × 44", "2 400"), ("Твіллі", "84 × 5", "1 600")]),
    dict(id="zolote", name="Золоте світло", c="#B8741F", deep="#8F5A17", flat="zolote-44-1", tw="zolote-tw-1",
         short="Момент ясності",
         state="Моменти ясності, коли все стає на свої місця.",
         formats=[("Хустка", "44 × 44", "2 400"), ("Твіллі", "84 × 5", "1 600")]),
    dict(id="avantiura", name="Авантюра", c="#8A2226", deep="#6E1B1F", flat="avantiura-88-1", tw="avantiura-tw-2",
         short="За межі звичного",
         state="Готовність виходити за межі звичного та відкриватися новому досвіду.",
         formats=[("Хустка", "88 × 88", "6 600"), ("Твіллі", "84 × 5", "1 600")]),
    dict(id="tysha", name="Тиша всередині", c="#26231F", deep="#26231F", flat="tysha-88-1", tw="tysha-tw-1",
         short="Чути себе",
         state="Баланс і здатність чути себе серед зовнішнього шуму. Стан, у якому більше не потрібно доводити, поспішати чи відповідати чужим очікуванням.",
         formats=[("Хустка", "88 × 88", "6 600"), ("Твіллі", "84 × 5", "1 600")]),
    dict(id="krok", name="Сміливий крок", c="#8E2A2C", deep="#6F2022", flat="krok-44-1", tw="krok-tw-1",
         short="Довіра до себе",
         state="Рішення рухатися вперед, навіть коли немає повної визначеності. Не тому, що страх зникає, а тому, що з’являється щось важливіше — довіра до себе.",
         formats=[("Хустка", "44 × 44", "2 400"), ("Твіллі", "84 × 5", "1 600")]),
]
PP = {p["id"]: p for p in P}

def S(name): return f"src/{name}.webp"
def HI(p): return f"src/{p['flat']}-hi.webp"
def CUT(name): return f"src/{name}-cut.webp"

def offer(p, k=0):
    kind, size, price = p["formats"][k]
    return f"{kind} «{p['name']}» · {size} · {price} грн"

def price_rows(p, color="rgba(27,22,19,.18)"):
    return "".join(f'<span class="prow" style="border-color:{color}"><span>{kind} {size}</span><b>{price} грн</b></span>' for kind, size, price in p["formats"])

def logo(dark=False, h=40, style=""):
    return f'<img class="lg" src="{LOGO_W if dark else LOGO_K}" alt="Obiimy" style="height:{h}px;{style}">'

def photo(name, pos="50% 50%", cls="", style="", img_style=""):
    return f'<div class="ph {cls}" style="{style}"><img src="{S(name)}" alt="" style="object-position:{pos};{img_style}"></div>'

def foot(dark=False, text=CTA, size=30, style=""):
    col = "#F3EADB" if dark else "var(--ink)"
    return f'<div class="row foot" style="{style}"><p class="lbl" style="font-size:{size}px;color:{col}">{text}</p>{logo(dark)}</div>'

GRAIN = "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .9 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>\")"

CSS = """
:root { --paper: #F1E8D8; --paper2: #E6D9C2; --card: #FBF6EC; --ink: #1B1613; --ink2: #4B423B; --ink3: #7A6E63; --wine: #7B1F24; --yellow: #F2B705; --cream: #F3EADB; }
* { box-sizing: border-box; }
body { margin: 0; background: #555; font-family: 'Cormorant Garamond', serif; color: var(--ink); -webkit-font-smoothing: antialiased; }
.ad { position: relative; overflow: hidden; background: var(--paper); margin: 24px auto; }
.st { width: 1080px; height: 1920px; } .fd { width: 1080px; height: 1350px; } .sq { width: 1080px; height: 1080px; }
.ad > *, .page > * { position: absolute; margin: 0; }
.ad p, .ad h1, .ad h2 { margin: 0; }
/* one print-like grain over the whole layout, photos included */
.ad::after { content: ""; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: .2; mix-blend-mode: multiply; background-image: GRAIN; }
.ad.dark::after { mix-blend-mode: soft-light; opacity: .5; }
.page { position: absolute; overflow: hidden; background: var(--paper); }
.fill { inset: 0; }
.col { display: flex; flex-direction: column; }
.row { display: flex; }
.safe { left: 80px; right: 80px; top: 280px; bottom: 380px; }
.box { left: 64px; right: 64px; top: 64px; bottom: 64px; }
.ph { overflow: hidden; }
.col > .ph, .row > .ph { position: relative; min-height: 0; }
.ph img { width: 100%; height: 100%; object-fit: cover; display: block; filter: contrast(1.05) saturate(.84) sepia(.12); }
.ph.bw img { filter: grayscale(1) contrast(1.16) brightness(1.04); }
.ph.raw img { filter: none; }
.cut { display: block; filter: drop-shadow(0 26px 30px rgba(40,25,10,.32)); }
.h { font-family: 'Playfair Display', serif; text-wrap: balance; }
.t { font-family: 'Cormorant Garamond', serif; font-weight: 500; text-wrap: pretty; }
.lbl { font-family: 'Jost', sans-serif; font-weight: 500; text-transform: uppercase; letter-spacing: .14em; font-size: 30px; line-height: 1.3; }
.solo { font-family: 'Bodoni Moda', 'Playfair Display', serif; font-weight: 900; font-style: italic; letter-spacing: -.02em; line-height: .78; }
.lg { display: block; width: auto; flex: none; }
.foot { justify-content: space-between; align-items: center; gap: 30px; }
.prow { display: flex; justify-content: space-between; gap: 30px; border-bottom: 2px solid; padding: 12px 0; font-family: 'Jost', sans-serif; font-size: 32px; letter-spacing: .04em; }
.prow b { font-weight: 600; }
.pill { font-family: 'Jost', sans-serif; font-weight: 600; font-size: 32px; letter-spacing: .04em; padding: 24px 46px; border-radius: 999px; background: var(--ink); color: var(--cream); white-space: nowrap; display: inline-block; }
.rule { height: 3px; width: 70px; }
.frame2::before { content: ""; position: absolute; inset: 18px; border: 2px solid rgba(27,22,19,.55); pointer-events: none; }
.frame2::after { content: ""; position: absolute; inset: 27px; border: 1px solid rgba(27,22,19,.35); pointer-events: none; }
.shadow { box-shadow: 0 40px 70px -30px rgba(0,0,0,.5); }
""".replace("GRAIN", GRAIN)

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · SOLO creatives</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@1,6..96,900&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700;1,900&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Jost:wght@400;500;600&display=swap">
<style>""" + CSS + "</style></head><body>"

def silk(p, size="auto 190%", pos="center"):
    return f'<div class="fill" style="background:url({HI(p)}) {pos}/{size}"></div><div class="fill" style="background:radial-gradient(90% 60% at 50% 45%,rgba(0,0,0,0),rgba(0,0,0,.3))"></div>'

def base(p, top=True, bg="var(--paper)"):
    """Paper page lying on silk: silk shows in the story UI zones, all text stays on paper."""
    return f'<div class="fill" style="background:url({HI(p)}) center/auto 190%"></div><div class="fill" style="background:rgba(0,0,0,.12)"></div><div class="fill" style="top:{236 if top else 0}px;bottom:316px;background:{bg};box-shadow:0 0 70px rgba(0,0,0,.5)"></div>'

MASKED = {"puls-44-4", "avantiura-88-5", "krok-44-2", "iskra-65-2"}

def spot_photo(name, pos="50% 50%", style=""):
    """Black-and-white frame, the scarf alone keeps its colour (mask: src/<name>-mask.png)."""
    bg = f"background:url(src/{name}.webp) {pos}/cover no-repeat"
    mk = f"-webkit-mask:url(src/{name}-mask.png) {pos}/cover no-repeat;mask:url(src/{name}-mask.png) {pos}/cover no-repeat;mask-mode:alpha"
    return (f'<div style="{style};overflow:hidden">'
            f'<div style="position:absolute;inset:0;{bg};filter:grayscale(1) contrast(1.12) brightness(1.02)"></div>'
            f'<div style="position:absolute;inset:0;{bg};{mk};filter:saturate(.95)"></div></div>')

def nb(text):
    """Non-breaking space before the last word, so no single word hangs on the last line."""
    i = text.rstrip().rfind(" ")
    return text if i < 0 else text[:i] + "\u00a0" + text[i + 1:]
