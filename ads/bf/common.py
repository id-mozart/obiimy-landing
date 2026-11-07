"""Shared helpers of the Black Friday series (07.11.2026): the format (FORMAT = plain | story | feed | square), the palette,
the header, the discount pill row, the words, the photo-melting-into-field templates. Used by build.py (the product series)
and build_models.py (the series on the campaign photos with models)."""
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
RANGE = "−20…−40 %"
PILL = "Знижки до −40 %"   # the pill is the only carrier of the number (panel, round 1)
FOUR = "і всі принти чотирьох колекцій"

def hdr_text(big):
    """The top-right word: «Чорна п’ятниця», unless the headline already says it (then «Знижки на шовк»)."""
    import re as _re
    return "Знижки на шовк" if _re.search(r"[Чч]орн\w* п’ятниц", big) else "Чорна п’ятниця"

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

def header(dark=True, text="Чорна п’ятниця"):
    col = CREAM if dark else "#1B1613"
    return (f'<img src="{LOGO_W if dark else LOGO_K}" alt="" style="left:64px;top:{TOPL}px;height:{int(56 * K)}px;z-index:5">'
            f'<p class="hdr" style="right:64px;top:{TOPL + int(16 * K)}px;font-size:{int(24 * K)}px;color:{col};z-index:5">{text}</p>')

def bar(dark=True, label=None, cta="obiimy.world"):
    """The bottom row: the discount in a yellow pill (the only loud thing on the page) and the address."""
    label = label or PILL
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

def melt(dark=True, h=320, bottom=True, rgb=None):
    """The seam between the photograph and the field: the field's colour rises into the picture."""
    c = rgb or ("20,17,16" if dark else "255,255,255")
    return f"linear-gradient({'0deg' if bottom else '180deg'},rgba({c},1),rgba({c},.85) 30%,rgba({c},0))"

def _rgb(hexcol):
    h = hexcol.lstrip("#"); return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))

# ─── templates ─────────────────────────────────────────────────────────────────────────────────────────────────────────

def full(id, img, pos, big, small, note="", dark=True, split=.56, size=84, kicker=None, root=False, zoom=1.0, label=None, ph_bg=None, ptop=0, field=None, top_veil=.6, origin="50% 50%", side_fade=False, top_light=0.0):
    """`ptop` — the photograph starts under the logo line instead of the frame's top edge (for flat scarves and white packshots,
    where the white logo would drown in the picture)."""
    """A photograph edge to edge across the top, melting into the field; the words in the field, the discount row below.
    In the square the photo takes the left half at full height and the words stand on the right."""
    src = (PR if root else PS) + img
    field = field or (INK if dark else WHITE)
    cls = "light" if dark else "ink"
    hd = hdr_text(big)
    sf = "-webkit-mask-image:linear-gradient(90deg,transparent,#000 9%,#000 91%,transparent);mask-image:linear-gradient(90deg,transparent,#000 9%,#000 91%,transparent);" if side_fade else ""
    if SQ:
        pw = 540
        body = f'''
  <div style="inset:0;background:{field}"></div>
  <div class="ph" style="left:0;top:{ptop}px;width:{pw}px;height:{H - ptop}px;{f"background:{ph_bg}" if ph_bg else ""}"><img src="{src}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:{pw - 140}px;top:0;width:140px;height:{H}px;background:linear-gradient(90deg,rgba({_rgb(field)},0),{field})"></div>
  {f'<div style="left:0;top:0;width:{pw}px;height:{int(240 * K)}px;background:linear-gradient(180deg,rgba(244,244,244,{top_light}),rgba(244,244,244,0))"></div>' if top_light else ""}
  {header(dark, hd)}
  <div class="{cls}" style="left:{pw - 40}px;right:64px;top:{Y0 + int(40 * K)}px;z-index:4">{words(big, small, size, dark, kicker=kicker)}</div>
  {bar(dark, label)}'''
    else:
        yph = int(H * split)
        body = f'''
  <div style="inset:0;background:{field}"></div>
  <div class="ph" style="left:0;right:0;top:{ptop}px;height:{yph + int(60 * K) - ptop}px;{sf}{f"background:{ph_bg}" if ph_bg else ""}"><img src="{src}" alt="" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin}"></div>
  <div style="left:0;right:0;top:{yph - int(260 * K)}px;height:{int(320 * K) + 2}px;background:{melt(dark, bottom=True, rgb=_rgb(field))}"></div>
  {"" if ptop else f'<div style="left:0;right:0;top:0;height:{int(220 * K)}px;background:linear-gradient(180deg,rgba(12,9,8,{top_veil if dark else .18}),rgba(12,9,8,0))"></div>'}
  {f'<div style="left:0;right:0;top:0;height:{int(240 * K)}px;background:linear-gradient(180deg,rgba(244,244,244,{top_light}),rgba(244,244,244,0))"></div>' if top_light else ""}
  {header(dark, hd)}
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
  {header(False, hdr_text(big))}
  <div class="ink" style="left:64px;width:{col - 30}px;top:{Y0 + int(20 * K)}px;z-index:4">{words(big, small, size, False, kicker=kicker)}</div>
  <div class="ph mult" style="left:{px}px;top:{top}px;width:{ph_w}px;height:{ph_h}px;z-index:2"><img src="{src}" alt="" style="object-position:{pos};transform:scale({zoom})"></div>
  {bar(False, label)}'''
    else:
        top = Y0 + head_h + int(20 * K); ph_h = Y1 - top; ph_w = min(1080, int(ph_h * ar))
        if ph_w < int(ph_h * ar): ph_h = int(ph_w / ar)
        px = (1080 - ph_w) // 2 + int(shift * K)
        body = f'''
  <div style="inset:0;background:{WHITE}"></div>
  {header(False, hdr_text(big))}
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
        cs = min(840, Y1 - Y0 - text_h - int(40 * K)); cx = (1080 - cs) // 2; cy = Y0 + int(30 * K)
        body = f'''
  <div style="inset:0;background:{INK}"></div>
  {header()}
  <div class="card" style="left:{cx}px;top:{cy}px;width:{cs}px;height:{cs}px;transform:rotate({tilt}deg);z-index:3"><img src="{src}" alt=""></div>
  <div class="light" style="left:64px;right:64px;top:{cy + cs + int(70 * K)}px;bottom:{H - Y1}px;z-index:4">{words(big, small, size, True)}</div>
  {bar()}'''
    ad(id, body, note)


__all__ = [n for n in dir() if not n.startswith('__')]
