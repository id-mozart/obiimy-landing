"""Gift-set creatives, second series (05.11.2026, client: «більше варіантів про подарункові набори, картинки краще, вибудувати
композицію»; and: no cut-outs — the shop's photographs as they are). Where the first series put one photograph under a dark veil,
this one composes with whole photographs: a lifestyle frame with the packshot pinned over the seam as a card, pure-white packshots
on a white field under a yellow header block (the products seem to float, nothing is cut), three packshots fanned like cards, a split
frame (worn / boxed), a nine-set mosaic, a triptych of hairstyles, a price poster, a row of no-size gifts. 1080×1920 plain plus
story / feed / square via FORMAT. Photos: photo/site (downloaded from obiimy.world); prices and names from review/SITE-FACTS.md
(19.10.2026). Output: sets2[-<format>].html → out-sets2[-<format>]/*.jpg  (cd ads && ADS=solo/sets2.html OUT=solo/out-sets2 node render.mjs)."""
import os, pathlib, re, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit import nb, LOGO_W, LOGO_K, GRAIN

def nbh(text):
    text = re.sub(r"(?<![\w’'])(у|в|з|і|й|а|о|на|до|за|та|не|чи|із|зі|від|для|що|як|це)\s+(?=[^\s<])", lambda m: m.group(1) + " ", text, flags=re.I)
    return re.sub(r"\s+([—–])", lambda m: " " + m.group(1), text)

FORMAT = os.environ.get("FORMAT", "plain")   # plain | story | feed | square
H = {"feed": 1350, "square": 1080}.get(FORMAT, 1920)
K = .72 if FORMAT == "square" else (.86 if FORMAT == "feed" else 1)
SHORT = FORMAT != "plain"                     # less room for words below the picture
TOPL = 250 if FORMAT == "story" else 58
BOTB = 340 if FORMAT == "story" else 60
ROW = int(170 * K)                            # the product row
Y0 = TOPL + int(100 * K)                      # content starts under the logo line
Y1 = H - BOTB - ROW - int(36 * K)             # and ends above the product row
PH = "../../photo/site/"
YEL, INK, PAPER, CREAM, WHITE = "#F2B705", "#141110", "#F1E8D8", "#F3EADB", "#FFFFFF"

CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #555; font-family: 'Onest', Arial, sans-serif; -webkit-font-smoothing: antialiased; }
.ad { width: 1080px; height: HPXpx; position: relative; overflow: hidden; background: #141110; margin: 20px auto; color: #F3EADB; }
.ad > * { position: absolute; margin: 0; }
.ad p { margin: 0; }
.ad::after { content: ""; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: .22; mix-blend-mode: soft-light; background-image: GRAIN; }
.ph { overflow: hidden; } .ph img { width: 100%; height: 100%; object-fit: cover; display: block; }
.fit img { object-fit: contain; }
.mult img { mix-blend-mode: multiply; }   /* a white packshot on the white field: its edges vanish */
.big { font-family: 'Playfair Display', serif; font-weight: 900; font-style: italic; line-height: .95; letter-spacing: -.01em; text-wrap: balance; }
.small { font-family: 'EB Garamond', 'Cormorant Garamond', serif; font-weight: 500; line-height: 1.16; text-wrap: pretty; }
.kicker { font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: .14em; color: #E0B040; white-space: nowrap; }
.hdr { font-family: Montserrat, sans-serif; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; white-space: nowrap; }
.cta { font-family: 'Onest'; font-weight: 600; border-radius: 999px; background: #F2B705; color: #141216; white-space: nowrap; flex: none; }
.plate { display: flex; align-items: center; border-radius: 20px; flex: 0 1 auto; min-width: 0; }
.plate .nm { font-weight: 600; line-height: 1.1; text-wrap: balance; }
.plate .pr { font-family: 'Playfair Display', serif; font-weight: 700; line-height: 1; margin-top: 8px; }
.ink { color: #1B1613; } .ink .kicker { color: #8A6A12; }
.card { background: #fff; box-shadow: 0 30px 60px -20px rgba(20,12,6,.5), 0 4px 10px rgba(20,12,6,.16); }
.card img { width: 100%; height: 100%; object-fit: cover; display: block; }
.cap { font-size: CAPpx; line-height: 1.2; }
.cap b { font-family: 'Playfair Display', serif; font-weight: 700; color: #F2B705; white-space: nowrap; }
""".replace("GRAIN", GRAIN).replace("HPX", str(H)).replace("CAP", str(int(24 * K)))

ads = []
def ad(id, body, note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad" id="{id}">{body}\n</section>')

def header(dark=True):
    col = CREAM if dark else "#1B1613"
    return (f'<img src="{LOGO_W if dark else LOGO_K}" alt="" style="left:64px;top:{TOPL}px;height:{int(58 * K)}px;z-index:5">'
            f'<p class="hdr" style="right:64px;top:{TOPL + int(18 * K)}px;font-size:{int(26 * K)}px;color:{col};z-index:5">Авторські шовкові вироби</p>')

def plate(title, price, cta="Обрати набір", dark=True, ink_cta=False):
    """The product row at the bottom: the set's name, the retail price; the yellow button to the right. No thumbnails — no cut-outs."""
    bg, bd, fg = ("rgba(243,234,219,.1)", "1.5px solid rgba(243,234,219,.3)", CREAM) if dark else ("rgba(27,22,19,.06)", "1.5px solid rgba(27,22,19,.18)", "#1B1613")
    return f'''
  <div style="left:64px;right:64px;bottom:{BOTB}px;display:flex;align-items:center;justify-content:space-between;gap:{int(24 * K)}px;z-index:6">
    <div class="plate" style="padding:{int(14 * K)}px {int(28 * K)}px;background:{bg};border:{bd};color:{fg}">
      <div style="min-width:0"><p class="nm" style="font-size:{int(27 * K)}px">{nb(title)}</p><p class="pr" style="font-size:{int(44 * K)}px">{price}</p></div></div>
    <div class="cta" style="font-size:{int(32 * K)}px;padding:{int(26 * K)}px {int(44 * K)}px;{"background:#141110;color:#F3EADB" if ink_cta else ""}">{cta}</div>
  </div>'''

def words(kicker, big, small, size, ink=False, width=None):
    sc = "#4B423B" if ink else "#D9CDB9"
    w = f"max-width:{width}px;" if width else ""
    return (f'<p class="kicker" style="font-size:{int(26 * K)}px">{kicker}</p>'
            f'<p class="big" style="font-size:{int(size * K)}px;margin-top:{int(16 * K)}px;{w}">{nbh(big)}</p>'
            + (f'<p class="small" style="font-size:{int(38 * K)}px;margin-top:{int(20 * K)}px;color:{sc};{w}">{nb(small)}</p>' if small else ""))

def ink_band():
    return f'<div style="left:0;right:0;bottom:0;height:{BOTB + ROW + int(24 * K)}px;background:{INK}"></div>'

# ─── templates ─────────────────────────────────────────────────────────────────────────────────────────────────────────

def duo(id, life, life_pos, pack, pack_pos, kicker, big, small, product, note="", size=82, bg=PAPER):
    """Worn above, given below: a lifestyle frame on top, a paper field under it, the packshot pinned as a tilted card over the seam.
    The words sit on the paper — under the card (plain) or beside it (short frames)."""
    yph = int(H * (.5 if SHORT else .55))
    cs = int(420 * K); cx = 1080 - 64 - cs; cy = yph - int(cs * .45)
    body = f'''
  <div style="inset:0;background:{bg}"></div>
  <div class="ph" style="left:0;right:0;top:0;height:{yph}px"><img src="{PH}{life}.jpg" alt="" style="object-position:{life_pos}"></div>
  <div style="left:0;right:0;top:0;height:{int(260 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,.5),rgba(12,9,8,0))"></div>
  {header()}
  <div class="card" style="left:{cx}px;top:{cy}px;width:{cs}px;height:{cs}px;padding:{int(14 * K)}px;transform:rotate(-4deg);z-index:4"><img src="{PH}{pack}.jpg" alt="" style="object-position:{pack_pos}"></div>'''
    if SHORT:
        body += f'<div class="ink" style="left:64px;top:{yph + int(34 * K)}px;width:{cx - 64 - int(30 * K)}px;bottom:{H - Y1}px">{words(kicker, big, small, size, ink=True)}</div>'
    else:
        body += f'<div class="ink" style="left:64px;right:64px;top:{cy + cs + int(36 * K)}px;bottom:{H - Y1}px">{words(kicker, big, small, size, ink=True)}</div>'
    body += ink_band() + plate(*product)
    ad(id, body, note)

def white(id, photo, pos, kicker, big, small, product, note="", size=96, inside=None, band=YEL, band_ink=True, ar=1.0, shift=0, zoom=1.0):
    """A pure-white packshot on a white field — the products seem to float, nothing is cut — under a colour block that carries the
    headline. `photo_box` = (left, top, width, height) as fractions of the frame; `second` = another white packshot (photo, pos, box)."""
    head_h = int((250 if SHORT else 330) * K)
    top = Y0 + head_h + int(10 * K)
    if SHORT:        # short frames: the words in a left column, the photo takes the whole height on the right
        col = int(400 * K); under = 0
        ph_h = Y1 - top; ph_w = min(1080 - 64 - col, int(ph_h * ar))
        if ph_w < int(ph_h * ar): ph_h = int(ph_w / ar)
        px = 64 + col + (1080 - 64 - col - ph_w) // 2
    else:
        under = int((190 if inside else 110) * K) if (inside or small) else 0
        ph_h = Y1 - top - under; ph_w = min(1080, int(ph_h * ar))
        if ph_w < int(ph_h * ar): ph_h = int(ph_w / ar)
        px = (1080 - ph_w) // 2 + int(shift * K)
    tc = "ink" if band_ink else ""
    body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  <div style="left:0;right:0;top:0;height:{Y0 + head_h - int(10 * K)}px;background:{band}"></div>
  {header(dark=not band_ink)}
  <div class="{tc}" style="left:64px;right:64px;top:{Y0}px"><p class="kicker" style="font-size:{int(26 * K)}px;color:{"#1B1613" if band_ink else "#E0B040"}">{kicker}</p><p class="big" style="font-size:{int(size * K)}px;margin-top:{int(14 * K)}px">{nbh(big)}</p></div>
  <div class="ph mult" style="left:{px}px;top:{top}px;width:{ph_w}px;height:{ph_h}px;z-index:2"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos};transform:scale({zoom})"></div>'''
    if inside:
        rows = "".join(f'<p style="display:flex;gap:{int(14 * K)}px;align-items:baseline;font-size:{int(28 * K)}px;line-height:1.2;margin-top:{int(10 * K)}px"><b style="font-family:Playfair Display,serif;font-style:italic;color:#8A6A12">0{i + 1}</b><span>{nb(t)}</span></p>' for i, t in enumerate(inside))
        body += f'<div class="ink" style="left:64px;bottom:{H - Y1 + int(6 * K)}px;width:{int((360 if SHORT else 440) * K)}px;z-index:5"><p class="kicker" style="font-size:{int(22 * K)}px">У коробці</p>{rows}</div>'
    if small:
        body += f'<p class="small ink" style="left:64px;bottom:{H - Y1 + int(10 * K)}px;width:{int((360 if SHORT else 600) * K)}px;font-size:{int(36 * K)}px;color:#4B423B;z-index:5">{nb(small)}</p>'
    body += plate(*product, dark=False)
    ad(id, body, note)

def fan(id, cards, kicker, big, foot, cta, note="", bg=INK, dark=True):
    """Three packshots fanned like cards on the table — three sets, three prices — with a legend row under them."""
    n = len(cards); cs = int((560 if SHORT else 600) * K)
    head_h = int(210 * K); legend_h = int(96 * K)
    area_top = Y0 + head_h; area_h = Y1 - area_top - legend_h
    cyc = area_top + area_h // 2
    spread = int(190 * K)
    body = f'''
  <div style="inset:0;background:{bg}"></div>
  {header(dark)}
  <div class="{'' if dark else 'ink'}" style="left:64px;right:64px;top:{Y0}px"><p class="kicker" style="font-size:{int(26 * K)}px">{kicker}</p><p class="big" style="font-size:{int(92 * K)}px;margin-top:{int(14 * K)}px">{nbh(big)}</p></div>'''
    for i, (photo, pos, name, price) in enumerate(cards):
        k = i - (n - 1) / 2
        x = 540 + int(k * spread) - cs // 2; y = cyc - cs // 2 + int(abs(k) * 34 * K)
        body += f'<div class="card" style="left:{x}px;top:{y}px;width:{cs}px;height:{cs}px;padding:{int(14 * K)}px;transform:rotate({k * 8:.0f}deg);z-index:{3 + (n - abs(int(k * 2)))}"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos}"></div>'
    cols = "".join(f'<div style="flex:1;border-top:1.5px solid {"rgba(243,234,219,.25)" if dark else "rgba(27,22,19,.18)"};padding-top:{int(12 * K)}px"><p class="cap" style="color:{CREAM if dark else "#1B1613"}">{nb(name)}<br><b style="color:{YEL if dark else "#8A6A12"}">{price}</b></p></div>' for _, _, name, price in cards)
    body += f'<div style="left:64px;right:64px;top:{Y1 - legend_h + int(8 * K)}px;display:flex;gap:{int(20 * K)}px">{cols}</div>'
    body += f'''
  <div style="left:64px;right:64px;bottom:{BOTB}px;display:flex;align-items:center;justify-content:space-between;gap:24px;z-index:6">
    <p class="small" style="font-size:{int(34 * K)}px;color:{"#CFC4B2" if dark else "#4B423B"}">{nb(foot)}</p>
    <div class="cta" style="font-size:{int(32 * K)}px;padding:{int(26 * K)}px {int(44 * K)}px">{cta}</div></div>'''
    ad(id, body, note)

def split(id, life, life_pos, side_bg, dark_side, piece_photo, piece_pos, kicker, big, small, product, note="", size=84, piece_w=440, piece_rot=-5):
    """Worn on the left, boxed on the right: a tall lifestyle crop takes the left part, a colour panel the right one with the packshot
    as a card and the words under it; the product row runs across the bottom on an ink band."""
    lw = int(1080 * .46)
    pw = int(piece_w * K); px = lw + (1080 - lw - pw) // 2; py = Y0 + int(20 * K)
    body = f'''
  <div style="inset:0;background:{side_bg}"></div>
  <div class="ph" style="left:0;top:0;width:{lw}px;height:{H}px"><img src="{PH}{life}.jpg" alt="" style="object-position:{life_pos}"></div>
  <div style="left:0;top:0;width:{lw}px;height:{int(220 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,.5),rgba(12,9,8,0))"></div>
  <img src="{LOGO_W}" alt="" style="left:64px;top:{TOPL}px;height:{int(58 * K)}px;z-index:5">
  <p class="hdr" style="left:{lw + int(40 * K)}px;top:{TOPL + int(18 * K)}px;font-size:{int(22 * K)}px;color:{CREAM if dark_side else "#1B1613"};z-index:5">Авторські шовкові вироби</p>
  <div class="card" style="left:{px}px;top:{py}px;width:{pw}px;height:{pw}px;padding:{int(12 * K)}px;transform:rotate({piece_rot}deg);z-index:4"><img src="{PH}{piece_photo}.jpg" alt="" style="object-position:{piece_pos}"></div>
  <div class="{'' if dark_side else 'ink'}" style="left:{lw + int(40 * K)}px;right:56px;top:{py + pw + int(44 * K)}px;bottom:{H - Y1}px">{words(kicker, big, small, size, ink=not dark_side)}</div>
  {ink_band()}
  {plate(*product)}'''
    ad(id, body, note)

def mosaic(id, cells, kicker, big, foot, cta, note=""):
    """Nine sets on one page: packshots in a 3 × 3 grid on paper, name and price under each — the catalogue of gifts."""
    head_h = int(200 * K); gap = int(16 * K); cap_h = int(74 * K)
    gy = Y0 + head_h; gh = Y1 - gy; cols = 3
    cw = (1080 - 128 - gap * (cols - 1)) // cols; rows = (len(cells) + cols - 1) // cols
    ch = (gh - gap * (rows - 1)) // rows
    body = f'''
  <div style="inset:0;background:{PAPER}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0}px"><p class="kicker" style="font-size:{int(26 * K)}px">{kicker}</p><p class="big" style="font-size:{int(92 * K)}px;margin-top:{int(14 * K)}px">{nbh(big)}</p></div>'''
    for i, (photo, pos, name, price) in enumerate(cells):
        x = 64 + (i % cols) * (cw + gap); y = gy + (i // cols) * (ch + gap)
        body += f'''
  <div class="card" style="left:{x}px;top:{y}px;width:{cw}px;height:{ch - cap_h}px;padding:{int(8 * K)}px;box-shadow:0 10px 24px -12px rgba(40,25,10,.35)"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos}"></div>
  <div class="ink" style="left:{x}px;top:{y + ch - cap_h + int(10 * K)}px;width:{cw}px"><p class="cap" style="color:#1B1613">{nb(name)}<br><b style="color:#8A6A12">{price}</b></p></div>'''
    body += f'''
  <div style="left:64px;right:64px;bottom:{BOTB}px;display:flex;align-items:center;justify-content:space-between;gap:24px;z-index:6">
    <p class="small ink" style="font-size:{int(34 * K)}px;color:#4B423B">{nb(foot)}</p>
    <div class="cta" style="font-size:{int(32 * K)}px;padding:{int(26 * K)}px {int(44 * K)}px">{cta}</div></div>'''
    ad(id, body, note)

def strip3(id, photos, kicker, big, small, product, note="", size=84):
    """Three tall frames side by side — three hairstyles with one set — the words under them on paper."""
    gap = int(14 * K); n = len(photos)
    sw = (1080 - 128 - gap * (n - 1)) // n; sh = int((Y1 - Y0) * (.56 if SHORT else .6))
    body = f'''
  <div style="inset:0;background:{PAPER}"></div>
  {header(dark=False)}'''
    for i, (photo, pos) in enumerate(photos):
        body += f'<div class="ph" style="left:{64 + i * (sw + gap)}px;top:{Y0}px;width:{sw}px;height:{sh}px;border-radius:4px"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos}"></div>'
    body += f'''
  <div class="ink" style="left:64px;right:64px;top:{Y0 + sh + int(40 * K)}px;bottom:{H - Y1}px">{words(kicker, big, small, size, ink=True)}</div>
  {ink_band()}
  {plate(*product)}'''
    ad(id, body, note)

def poster(id, bg, dark, price_big, unit, caption, photo, pos, kicker, product, note="", card_w=560, rot=6):
    """A price poster: the number set huge, the packshot leaning on it as a card, one line of explanation."""
    fg = CREAM if dark else "#1B1613"
    num = int((250 if SHORT else 290) * K)
    ny = Y0 + int(70 * K)
    cw = int(card_w * K)
    body = f'''
  <div style="inset:0;background:{bg}"></div>
  {header(dark)}
  <p class="kicker" style="left:64px;top:{Y0}px;font-size:{int(28 * K)}px;color:{"#E0B040" if dark else "#1B1613"}">{kicker}</p>
  <p class="big" style="left:56px;top:{ny}px;font-size:{num}px;line-height:.85;white-space:nowrap;color:{fg};z-index:2">{price_big}<span style="font-size:{int(num * .34)}px;font-weight:700;font-style:italic;margin-left:.08em">{unit}</span></p>
  <div class="card" style="right:{int(56 * K)}px;top:{ny + int(num * .95)}px;width:{cw}px;height:{cw}px;padding:{int(14 * K)}px;transform:rotate({rot}deg);z-index:3"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos}"></div>
  <p class="small" style="left:64px;bottom:{H - Y1 + int(10 * K)}px;width:{int(440 * K)}px;font-size:{int(40 * K)}px;color:{"#D9CDB9" if dark else "#4B423B"};z-index:4">{nb(caption)}</p>
  {plate(*product, dark=dark, ink_cta=bg == YEL)}'''
    ad(id, body, note)

def row(id, items, kicker, big, small, product, note=""):
    """Four gifts that need no size, in a row on white: pure-white packshots, the name, the price."""
    head_h = int(230 * K); gap = int(18 * K); cols = 2; cap_h = int(80 * K)
    cw = (1080 - 128 - gap) // cols; ry = Y0 + head_h
    rows_n = (len(items) + cols - 1) // cols
    free = Y1 - ry - int(110 * K); rh = min(cw + cap_h, (free - gap * (rows_n - 1)) // rows_n)
    body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  <div style="left:0;right:0;top:0;height:{Y0 + head_h - int(30 * K)}px;background:{YEL}"></div>
  {header(dark=False)}
  <div class="ink" style="left:64px;right:64px;top:{Y0}px"><p class="kicker" style="font-size:{int(26 * K)}px;color:#1B1613">{kicker}</p><p class="big" style="font-size:{int(88 * K)}px;margin-top:{int(14 * K)}px">{nbh(big)}</p></div>'''
    for i, (photo, pos, name, price) in enumerate(items):
        x = 64 + (i % cols) * (cw + gap); y = ry + (i // cols) * (rh + gap)
        body += f'''
  <div class="ph mult" style="left:{x}px;top:{y}px;width:{cw}px;height:{rh - cap_h}px"><img src="{PH}{photo}.jpg" alt="" style="object-position:{pos}"></div>
  <div class="ink" style="left:{x}px;top:{y + rh - cap_h}px;width:{cw}px;border-top:1.5px solid rgba(27,22,19,.18);padding-top:{int(10 * K)}px"><p class="cap" style="color:#1B1613">{nb(name)}<br><b style="color:#8A6A12">{price}</b></p></div>'''
    body += f'''
  <p class="small ink" style="left:64px;right:64px;bottom:{H - Y1 + int(10 * K)}px;font-size:{int(36 * K)}px;color:#4B423B">{nb(small)}</p>
  {plate(*product, dark=False)}'''
    ad(id, body, note)

# ─── the sixteen ───────────────────────────────────────────────────────────────────────────────────────────────────────

duo("n01-natkhnennia", "set-tvilli-845-ta-khustky-4444-natkhne-02", "50% 12%", "set-tvilli-845-ta-khustky-4444-natkhne-01", "50% 50%",
    "Подарункові набори", "Так носять. Так дарують.", "Хустка 44 × 44 і твіллі «Натхнення» — в одному принті, в одній жовтій коробці.",
    ("Набір «Натхнення» · твіллі + хустка", "3 100 грн"), "worn on the back, boxed on the card")

duo("n02-smilyvist", "set-smilyvist-02", "60% 20%", "set-smilyvist-01", "50% 50%",
    "Подарункові набори", "Подарунок, який одразу надягають.", "Твіллі у волосся й резинка в тон — набір «Сміливість» у святковій коробці.",
    ("Твіллі + резинка «Сміливість»", "2 200 грн"), "the bun with the twilly, the box on the card", bg="#EDE4D3")

duo("n03-vpevnenist", "set-tvilli-845-ta-khustky-4444-vpevnen-02", "50% 14%", "set-tvilli-845-ta-khustky-4444-vpevnen-01", "50% 50%",
    "Подарункові набори", "Її принт — на двох речах.", "Червона хустка з блакитними квітами і твіллі «Впевненість»: разом у коробці або кожна окремо.",
    ("Набір «Впевненість» · твіллі + хустка", "3 100 грн"), "the red scarf on the back")

duo("n04-makiv", "set-makovyi-tsvit-02", "50% 40%", "set-makovyi-tsvit-01", "50% 50%",
    "Подарункові набори", "Замість букета.", "Твіллі «Маків цвіт» бантом на зап’ясті й резинка в тон — подарунок, який не зів’яне.",
    ("Твіллі + резинка «Маків цвіт»", "2 200 грн"), "the tulip and the bow on the wrist", bg="#F4ECDD")

white("n05-sleep-inside", "set-maska-rezynka-28-01", "50% 50%", "Набір для сну", "Що всередині.", "",
      ("Набір для сну · маска + резинка", "3 280 грн"), "the sleep set laid out on white", inside=["Шовкова маска для сну", "Резинка в тому ж принті", "Фірмова жовта коробка"],
      shift=120, zoom=1.12)

white("n06-three-twilly", "set-3-shovkovykh-tvilli-13", "50% 50%", "Подарункові набори", "Три твіллі. Принти — на ваш вибір.",
      "Набір із трьох твіллі 84 × 5 у фірмовій коробці: у волосся, на сумку, на шию.", ("Набір із трьох твіллі", "4 650 грн"), "three twillies, the third one out of the box",
      size=92, ar=1060 / 1500)

white("n07-melodiia", "set-maska-zakladka-rezynka-melodiia-01", "50% 50%", "Колекція «Співоча душа»", "Три речі для вечора з книгою.", "",
      ("«Мелодія двох» · маска, закладка, резинка", "4 080 грн"), "mask, bookmark and scrunchie on white", size=90,
      inside=["Маска для сну", "Закладка для книги", "Резинка для волосся"], band=PAPER, shift=100, zoom=1.12)

white("n08-hearts", "set-masok-dlia-snu-sertsebyttia-chervo-02", "50% 50%", "Подарункові набори", "Серцебиття — на двох.",
      "Пара шовкових масок для сну: червона та чорна. Для неї і для нього.", ("Набір масок «Серцебиття»", "4 200 грн"), "two heart masks on white",
      size=104, band="#5A1A22", band_ink=False, ar=1250 / 1500, zoom=1.3)

fan("n09-budgets", [("set-smilyvist-01", "50% 50%", "Твіллі + резинка «Сміливість»", "2 200 грн"),
                    ("set-tvilli-845-ta-khustky-4444-natkhne-01", "50% 50%", "Твіллі + хустка 44 × 44", "3 100 грн"),
                    ("set-3-shovkovykh-tvilli-03", "50% 50%", "Три твіллі", "4 650 грн")],
    "Подарунок за бюджетом", "Три подарунки — три бюджети.", "Усі набори — у фірмовій жовтій коробці.", "Обрати набір", "three cards fanned")

fan("n10-sleep-prints", [("set-maska-rezynka-10-01", "50% 50%", "Набір для сну «Літнє поле»", "3 280 грн"),
                         ("set-maska-rezynka-26-02", "50% 50%", "Набір для сну «Свобода»", "3 280 грн"),
                         ("set-maska-rezynka-34-01", "50% 50%", "Набір для сну «Серцебиття»", "3 280 грн")],
    "Набір для сну", "Один набір — вісім принтів.", "Маска для сну та резинка в одному принті.", "Обрати принт", "three sleep sets fanned", bg=PAPER, dark=False)

split("n11-na-nii", "set-tvilli-845-ta-khustky-4444-natkhne-04", "40% 20%", YEL, False, "set-tvilli-845-ta-khustky-4444-natkhne-01", "50% 50%",
      "Подарункові набори", "На ній — і в коробці.", "Хустка 44 × 44 на плечі, твіллі у хвості. Набір «Натхнення».",
      ("Набір «Натхнення» · твіллі + хустка", "3 100 грн"), "worn / boxed, yellow")

split("n12-kravatka", "set-prystrast-02", "50% 12%", INK, True, "set-prystrast-01", "50% 50%",
      "Подарункові набори", "Твіллі краваткою.", "Набір «Пристрасть»: твіллі 84 × 5 і резинка в одному принті — у святковій коробці.",
      ("Твіллі + резинка «Пристрасть»", "2 200 грн"), "the tie, the packshot card on ink", piece_rot=5)

mosaic("n13-all-sets", [("set-smilyvist-01", "50% 50%", "Твіллі + резинка", "2 200 грн"),
                        ("set-tvilli-845-ta-khustky-4444-natkhne-01", "50% 50%", "Твіллі + хустка 44 × 44", "3 100 грн"),
                        ("set-tvilli-845-ta-khustky-4444-nizhnis-01", "50% 50%", "Твіллі + хустка «Ніжність»", "3 100 грн"),
                        ("set-maska-rezynka-10-01", "50% 50%", "Набір для сну", "3 280 грн"),
                        ("set-masok-dlia-snu-sertsebyttia-chervo-01", "50% 50%", "Маски «Серцебиття»", "4 200 грн"),
                        ("set-maska-zakladka-rezynka-melodiia-01", "50% 50%", "Маска, закладка, резинка", "4 080 грн"),
                        ("set-3-shovkovykh-tvilli-03", "50% 50%", "Три твіллі", "4 650 грн"),
                        ("set-iz-5-ty-shovkovykh-rezynok-zero-west-03", "50% 50%", "П’ять резинок zero waste", "2 420 грн"),
                        ("set-tvilli-845-ta-khustky-4444-vpevnen-01", "50% 50%", "Твіллі + хустка «Впевненість»", "3 100 грн")],
       "Подарункові набори", "Усі набори в коробці.", "Роздрібні ціни obiimy.world.", "Усі набори", "nine sets on paper")

strip3("n14-three-hair", [("set-tvilli-845-ta-khustky-4444-natkhne-02", "50% 12%"), ("set-tvilli-845-ta-khustky-4444-hratsii-02", "50% 16%"), ("set-tvilli-845-ta-khustky-4444-smilyvy-02", "50% 20%")],
       "Подарункові набори", "Одна твіллі — три зачіски.", "У хвості, у косі, вузлом на потилиці: твіллі з набору «твіллі + хустка 44 × 44».",
       ("Твіллі + хустка 44 × 44 — від", "3 100 грн"), "three hairstyles side by side")

poster("n15-price", YEL, False, "2 200", "грн", "Твіллі 84 × 5 і шовкова резинка в одному принті — у фірмовій коробці. Вісім принтів на вибір.",
       "set-smilyvist-01", "50% 50%", "Твіллі + резинка", ("Твіллі + резинка", "2 200 грн"), "the price poster on yellow", card_w=620)

row("n16-no-size", [("mask-litnie-pole-01", "50% 50%", "Маска для сну", "2 700 грн"), ("tvilli-flat-pidnesennia-01", "50% 50%", "Твіллі 84 × 5", "1 600 грн"),
                    ("set-litnie-pole-01", "50% 50%", "Твіллі + резинка", "2 200 грн"), ("set-maska-rezynka-10-01", "50% 50%", "Набір для сну", "3 280 грн")],
    "Коли не знаєте розмір", "Подарунки без розміру.", "Кожна річ — у фірмовій коробці; набори з двох речей — від 2 200 грн.",
    ("Подарунки без розміру — від", "1 600 грн", "Обрати подарунок"), "four no-size gifts in a row")

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · gift sets, series 2</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=EB+Garamond:wght@500;600&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Oswald:wght@500&family=Montserrat:wght@300;400;500&family=Onest:wght@400;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / ("sets2" + ("" if FORMAT == "plain" else "-" + FORMAT) + ".html")).write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "gift-set banners (series 2)", FORMAT)
