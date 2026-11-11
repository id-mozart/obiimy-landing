# -*- coding: utf-8 -*-
"""Personal business cards for Світлана Сніжко, CEO of OBIIMY (10.11.2026, client: «сделай отдельную страницу где-то и сделай на ней
макеты визитных карточек клевых личных для обиймы»). A service page (HIDDEN in build-site.py): thirty-six pairs front / back at the true
proportion 90 × 50 mm, 6 px per mm, on a dark studio field. Facts: name and title from the brief; the phone +380 97 773 09 21 is the client's (11.11.2026); the e-mail from the brief; the prints are the real flat scarves of obiimy.world; the QR codes point at https://obiimy.world
(segno). Nothing about foil or paper is a promise — the «тиснення» card is a mock-up of the effect, said so on the page.
python3 src/build-cards.py → cards.html → python3 build-site.py → site/cards.html"""
import pathlib, re, sys
import segno
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ads" / "solo"))
from kit import nb

NAME, TITLE, PHONE, MAIL, SITE = "Світлана Сніжко", "CEO", "+380 97 773 09 21", "svitlana@obiimy.world", "obiimy.world"
LAT = "Svitlana Snizhko"
YEL, INK, CREAM, PAPER = "#F2B705", "#141110", "#F3EADB", "#F1E8D8"
LOGO_W, LOGO_K = "brand/logo-white.png", "brand/logo-ink.png"
PRINTS = {"kolo": "photo/site/khustka-flat-kolo-sontsia-88x88-01.jpg", "kava": "photo/site/khustka-flat-rankova-kava-65x65-01.jpg",
          "smil": "photo/site/khustka-flat-smilyvist-44x44-01.jpg", "mizh": "photo/mizh-flat.webp", "vyr": "photo/vyr-flat.webp",
          "dotyk": "photo/dotyk-flat.webp", "hrat": "photo/hratsiia-flat.webp", "tw-melodiia": "photo/site/tvilli-flat-melodiia-dvokh-01.jpg", "tryp": "photo/edem/art-corner.webp"}

def qr(color, bg=None):
    """A real QR code to the shop, as inline SVG (segno), dark modules in `color`, no quiet-zone box."""
    q = segno.make("https://obiimy.world", error="m")
    svg = q.svg_inline(scale=1, border=0, dark=color, light=bg, omitsize=True)
    return svg.replace("<svg ", '<svg class="qr" ', 1)

_qr_n = [0]
def qr_styled(style="dots", dark=INK, finder=None, hole=None, fill=None, light=None, shade=.5, outline=0):
    """A real QR to the shop drawn from segno's matrix (error level H, so a centre hole and rounded modules stay readable):
    style dots | round | square; finder — colour of the three finder patterns (rounded rings); hole — (w, h) modules cleared
    in the centre for a logo; fill — an image path used as the module fill (SVG pattern) instead of a flat colour; outline — a dark
    stroke (in modules) around each filled module: with a print fill it gives the binarizer a hard edge (OpenCV and jsQR both decode with .15)."""
    q = segno.make("https://obiimy.world", error="h")
    m = q.matrix; n = len(m)
    def in_finder(r, c): return (r < 7 and c < 7) or (r < 7 and c >= n - 7) or (r >= n - 7 and c < 7)
    fcol = finder or dark
    _qr_n[0] += 1; pid = f"pf{_qr_n[0]}"
    paint = f"url(#{pid})" if fill else dark
    parts = []
    if fill:   # the photo twice the code's size (only its centre, no white margin), darkened with `shade` so every module stays dark enough to scan
        parts.append(f'<defs><pattern id="{pid}" patternUnits="userSpaceOnUse" x="{-n * .55}" y="{-n * .55}" width="{n * 2.1}" height="{n * 2.1}"><image href="{fill}" width="{n * 2.1}" height="{n * 2.1}" preserveAspectRatio="xMidYMid slice"/><rect width="{n * 2.1}" height="{n * 2.1}" fill="{dark}" opacity="{shade}"/></pattern></defs>')
    if light: parts.append(f'<rect width="{n}" height="{n}" fill="{light}"/>')
    for r0, c0 in ((0, 0), (0, n - 7), (n - 7, 0)):
        parts.append(f'<rect x="{c0 + .5}" y="{r0 + .5}" width="6" height="6" rx=".8" fill="none" stroke="{fcol}" stroke-width="1"/>')   # rounder finders (rx 1.5) stop OpenCV's detector; .8 still decodes
        parts.append(f'<rect x="{c0 + 2}" y="{r0 + 2}" width="3" height="3" rx=".5" fill="{fcol}"/>')
    cx = cy = n / 2
    for r, row in enumerate(m):
        for c, v in enumerate(row):
            if not v or in_finder(r, c): continue
            if hole and abs(c + .5 - cx) < hole[0] / 2 and abs(r + .5 - cy) < hole[1] / 2: continue
            if style == "dots": parts.append(f'<circle cx="{c + .5}" cy="{r + .5}" r=".47" fill="{paint}"/>')   # .43 was too airy for OpenCV once the logo pill sits in the centre
            elif style == "round": parts.append(f'<rect x="{c + .07}" y="{r + .07}" width=".86" height=".86" rx=".3" fill="{paint}"{f" stroke={chr(34)}{dark}{chr(34)} stroke-width={chr(34)}{outline}{chr(34)}" if outline else ""}/>')
            else: parts.append(f'<rect x="{c}" y="{r}" width="1" height="1" fill="{paint}"/>')
    return f'<svg class="qr" viewBox="0 0 {n} {n}" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'

def tel(): return "tel:" + re.sub(r"[^\d+]", "", PHONE)

# ─── the cards: each a function returning (front_html, back_html, extra_css) ──────────────────────────────────────────

def c_ink():
    f = f'''<div class="face ink">
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:5mm;left:6mm;top:6mm">
  <div class="who" style="left:6mm;bottom:6mm;color:{CREAM}"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm;color:{CREAM}"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    b = f'''<div class="face ink"><img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:7mm;left:50%;top:44%;transform:translate(-50%,-50%)">
  <p class="ct" style="left:0;right:0;top:58%;text-align:center;color:{CREAM};font-size:2.4mm">{SITE}</p>
  <div style="position:absolute;left:0;right:0;bottom:0;height:2mm;background:{YEL}"></div></div>'''
    return f, b

def c_print_back(key="kolo", pos="50% 50%"):
    f = f'''<div class="face white">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:6mm;top:5.4mm">
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    b = f'''<div class="face"><img class="fill" src="{PRINTS[key]}" alt="" style="object-position:{pos};transform:scale(1.3)"></div>'''   # the print carries the brand's own mark — no second logo on top of it
    return f, b

def c_yellow():
    f = f'''<div class="face" style="background:{YEL}">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:5mm;left:6mm;top:6mm">
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm" style="font-size:4.4mm;font-weight:600">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    b = f'''<div class="face ink"><img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:7mm;left:50%;top:50%;transform:translate(-50%,-50%)">
  <p class="caps" style="position:absolute;left:0;right:0;bottom:6mm;text-align:center;color:{YEL};font-size:2.2mm">100 % натуральний шовк</p></div>'''
    return f, b

def c_monogram():
    f = f'''<div class="face white">
  <p class="mono">С<span style="margin-left:-.28em">С</span></p>
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    b = f'''<div class="face ink">
  <div style="position:absolute;left:0;top:0;bottom:0;width:30mm;overflow:hidden"><img class="fill" src="{PRINTS['vyr']}" alt="" style="object-position:40% 50%;transform:scale(1.35)"></div>
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:5mm;right:6mm;bottom:6mm"></div>'''
    return f, b

def c_twilly():
    f = f'''<div class="face white">
  <div style="position:absolute;left:0;top:0;bottom:0;width:12mm;overflow:hidden"><img class="fill" src="{PRINTS['smil']}" alt="" style="object-position:12% 50%;transform:scale(1.15)"></div>
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;right:6mm;top:5.4mm">
  <div class="who" style="left:18mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    b = f'''<div class="face ink">
  <div style="position:absolute;right:0;top:0;bottom:0;width:12mm;overflow:hidden"><img class="fill" src="{PRINTS['smil']}" alt="" style="object-position:88% 50%;transform:scale(1.15)"></div>
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:6mm;left:39mm;top:50%;transform:translate(-50%,-50%)"></div>'''
    return f, b

def c_label():
    f = f'''<div class="face" style="background:{PAPER};border-radius:3mm">
  <div class="stitch"></div>
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.6mm;left:50%;top:7mm;transform:translateX(-50%)">
  <p class="nm c" style="position:absolute;left:0;right:0;top:17.5mm;text-align:center;font-size:4.4mm">{NAME}</p>
  <p class="tt c" style="position:absolute;left:0;right:0;top:24.5mm;text-align:center">{TITLE}</p>
  <p class="caps" style="position:absolute;left:0;right:0;bottom:6.5mm;text-align:center;font-size:2.3mm;color:#4B423B">OBIIMY · шовк · Україна</p></div>'''
    b = f'''<div class="face" style="background:{PAPER};border-radius:3mm">
  <div class="stitch"></div>
  <div class="ct c" style="left:0;right:0;top:50%;transform:translateY(-50%);text-align:center;font-size:2.8mm;line-height:1.7"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    return f, b

def c_vertical():
    f = f'''<div class="face ink">
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:4.6mm;left:50%;top:7mm;transform:translateX(-50%)">
  <div class="who" style="left:6mm;bottom:6mm;color:{CREAM}"><p class="nm" style="font-size:4.6mm;line-height:1.15;font-weight:400">Світлана<br>Сніжко</p><p class="tt">{TITLE}</p></div></div>'''
    b = f'''<div class="face"><img class="fill" src="{PRINTS['kolo']}" alt="" style="object-position:50% 30%;transform:scale(1.6)">
  <div style="position:absolute;left:0;right:0;bottom:0;height:30mm;background:linear-gradient(0deg,rgba(20,17,16,.92),rgba(20,17,16,.75) 60%,rgba(20,17,16,0))"></div>
  <div class="ct c" style="left:0;right:0;bottom:6mm;text-align:center;color:{CREAM};font-size:2.6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    return f, b

def c_qr():
    f = f'''<div class="face white">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:6mm;top:5.4mm">
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    b = f'''<div class="face ink">
  <div style="position:absolute;left:6mm;top:50%;transform:translateY(-50%);width:22mm;height:22mm;background:#fff;padding:2.8mm">{qr(INK)}</div>
  <div class="ct" style="left:33mm;top:50%;transform:translateY(-50%);color:{CREAM}"><p class="caps" style="color:{YEL};font-size:2.2mm;margin-bottom:1.2mm">Крамниця</p><p style="font-size:3.4mm">{SITE}</p><p style="font-size:2.4mm;color:#B8AC98;margin-top:1mm">хустки · твіллі · маски для сну · набори</p></div></div>'''
    return f, b

def c_foil():
    f = f'''<div class="face ink">
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:4.6mm;left:6mm;top:6mm;opacity:.92">
  <p class="nm foil" style="position:absolute;left:6mm;bottom:12.5mm;font-size:5.2mm;font-weight:600">{NAME}</p>
  <p class="tt" style="position:absolute;left:6mm;bottom:6mm;color:#B8AC98">{TITLE}</p>
  <div class="ct r" style="right:6mm;bottom:6mm;color:{CREAM}"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    b = f'''<div class="face ink"><div class="foil-logo" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:34mm;height:7.2mm"></div></div>'''
    return f, b

def c_signature():
    f = f'''<div class="face" style="background:{CREAM}">
  <p class="sig">{NAME}</p>
  <p class="tt" style="position:absolute;left:6mm;bottom:6mm">{TITLE} · засновниця · художниця</p>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    b = f'''<div class="face"><img class="fill" src="{PRINTS['smil']}" alt="" style="object-position:50% 50%;transform:scale(1.25)">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:5mm;right:6mm;bottom:6mm"></div>'''
    return f, b

def c_split():
    f = f'''<div class="face white">
  <div style="position:absolute;left:0;top:0;bottom:0;width:45mm;overflow:hidden;border-right:.3mm solid {INK}"><img class="fill" src="{PRINTS['dotyk']}" alt="" style="object-position:50% 50%;transform:scale(1.3)"></div>
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.2mm;left:51mm;top:6mm">
  <div class="who" style="left:51mm;bottom:6mm"><p class="nm" style="font-size:4mm;line-height:1.15">Світлана<br>Сніжко</p><p class="tt">{TITLE}</p></div></div>'''
    b = f'''<div class="face ink">
  <div class="ct" style="left:6mm;top:50%;transform:translateY(-50%);color:{CREAM};font-size:3mm;line-height:1.7"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div>
  <div style="position:absolute;right:6mm;top:50%;transform:translateY(-50%);width:18mm;height:18mm;background:#fff;padding:2.4mm">{qr(INK)}</div></div>'''
    return f, b

def c_bilingual():
    f = f'''<div class="face ink">
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:5mm;left:6mm;top:6mm">
  <div class="who" style="left:6mm;bottom:6mm;color:{CREAM}"><p class="nm">{NAME}</p><p class="tt">{TITLE} · засновниця</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm;color:{CREAM}"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    b = f'''<div class="face" style="background:{CREAM}">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:5mm;left:6mm;top:6mm">
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{LAT}</p><p class="tt">{TITLE} · Founder</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    return f, b

def c_trypillia():
    f = f'''<div class="face ink">
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:5mm;left:6mm;top:6mm">
  <div class="who" style="left:6mm;bottom:6mm;color:{CREAM}"><p class="nm">{NAME}</p><p class="tt">{TITLE} · засновниця · художниця</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm;color:{CREAM}"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    b = f'''<div class="face"><img class="fill" src="{PRINTS['tryp']}" alt="" style="object-position:50% 50%;transform:scale(1.15)">
  <div style="position:absolute;left:0;right:0;bottom:0;height:16mm;background:linear-gradient(0deg,rgba(20,17,16,.85),rgba(20,17,16,0))"></div>
  <p class="caps" style="position:absolute;left:6mm;bottom:5.5mm;font-size:2mm;color:{CREAM}">Trypillia — The Art of Origins · Kraїna Edem × OBIIMY</p></div>'''
    return f, b

def c_bigname():
    f = f"""<div class="face" style="background:{CREAM}">
  <p style="position:absolute;left:6mm;top:6mm;font-family:Montserrat,sans-serif;font-weight:300;font-size:8.2mm;line-height:1.02;letter-spacing:-.02em;color:{INK}">Світлана<br>Сніжко</p>
  <p class="tt" style="position:absolute;left:6mm;bottom:6mm">{TITLE} · OBIIMY</p>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face ink"><img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:6.4mm;left:50%;top:50%;transform:translate(-50%,-50%)"></div>"""
    return f, b

def c_frame():
    fr = f'<div style="position:absolute;inset:4mm;border:.3mm solid {INK}"></div>'   # 4 mm in: a ±0.5 mm trim does not show on the frame
    f = f"""<div class="face white">{fr}
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4mm;left:50%;top:8.5mm;transform:translateX(-50%)">
  <p class="nm" style="position:absolute;left:0;right:0;top:19mm;text-align:center">{NAME}</p>
  <p class="tt" style="position:absolute;left:0;right:0;top:25mm;text-align:center">{TITLE}</p>
  <p class="ct" style="left:0;right:0;bottom:7.5mm;text-align:center;font-size:2.3mm;line-height:1.5">{PHONE} · {MAIL}<br>{SITE}</p></div>"""
    b = f"""<div class="face" style="background:{YEL}"><div style="position:absolute;inset:4mm;border:.3mm solid {INK}"></div>
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:6mm;left:50%;top:50%;transform:translate(-50%,-50%)"></div>"""
    return f, b

def c_band():
    f = f"""<div class="face white">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:6mm;top:5.4mm">
  <div class="who" style="left:6mm;bottom:18mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:18mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:12mm;overflow:hidden"><img class="fill" src="{PRINTS['smil']}" alt="" style="object-position:50% 50%;transform:scale(1.6)"></div></div>"""
    b = f"""<div class="face ink">
  <div style="position:absolute;left:0;right:0;top:0;height:12mm;overflow:hidden"><img class="fill" src="{PRINTS['smil']}" alt="" style="object-position:50% 50%;transform:scale(1.6)"></div>
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:5.4mm;left:50%;top:29.5mm;transform:translate(-50%,-50%)">
  <p class="ct" style="left:0;right:0;bottom:5mm;text-align:center;color:#B8AC98;font-size:2.2mm;font-weight:400">{SITE}</p></div>"""
    return f, b

def c_porthole():
    f = f"""<div class="face white">
  <div style="position:absolute;right:6mm;top:50%;transform:translateY(-50%);width:36mm;height:36mm;border-radius:50%;overflow:hidden"><img class="fill" src="{PRINTS['hrat']}" alt="" style="object-position:50% 50%;transform:scale(1.2)"></div>
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:6mm;top:5.4mm">
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm" style="font-size:3.7mm">Світлана<br>Сніжко</p><p class="tt">{TITLE}</p></div></div>"""
    b = f"""<div class="face ink">
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:5mm;right:6mm;bottom:6mm">
  <div class="ct" style="left:6mm;top:50%;transform:translateY(-50%);color:{CREAM};font-size:2.8mm;line-height:1.7"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    return f, b

def c_topbottom():
    f = f"""<div class="face white">
  <div style="position:absolute;left:0;right:0;top:0;height:24mm;overflow:hidden"><img class="fill" src="{PRINTS['dotyk']}" alt="" style="object-position:50% 50%;transform:scale(1.5)"></div>
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face ink"><img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:6mm;left:50%;top:50%;transform:translate(-50%,-50%)">
  <div style="position:absolute;left:0;right:0;top:0;height:1.5mm;background:{YEL}"></div></div>"""
    return f, b

def c_lookbook():
    f = f"""<div class="face ink">
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:5mm;left:6mm;top:6mm">
  <div class="who" style="left:6mm;bottom:6mm;color:{CREAM}"><p class="nm">{NAME}</p><p class="tt">{TITLE} · засновниця</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm;color:{CREAM}"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face"><img class="fill" src="photo/lookbook/lb13-15-L.webp" alt="" style="object-position:50% 42%">
  <div style="position:absolute;left:0;right:0;bottom:0;height:14mm;background:linear-gradient(0deg,rgba(20,17,16,.7),rgba(20,17,16,0))"></div>
  <p class="caps" style="position:absolute;right:6mm;bottom:5.5mm;font-size:2.4mm;color:{CREAM}">{SITE}</p></div>"""
    return f, b

def c_rule():
    f = f"""<div class="face white">
  <div style="position:absolute;left:0;top:0;bottom:0;width:2.5mm;background:{YEL}"></div>
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:9mm;top:5.4mm">
  <div class="who" style="left:9mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face ink">
  <div style="position:absolute;right:0;top:0;bottom:0;width:2.5mm;background:{YEL}"></div>
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:6mm;left:50%;top:50%;transform:translate(-50%,-50%)"></div>"""
    return f, b

def c_sash():
    f = f"""<div class="face white">
  <div style="position:absolute;left:-10mm;width:120mm;height:14mm;top:19mm;transform:rotate(-18deg);overflow:hidden;box-shadow:0 .4mm 1mm rgba(0,0,0,.18)"><img src="{PRINTS['kava']}" alt="" style="position:absolute;width:240mm;height:240mm;left:-60mm;top:-206mm"></div>
  <div class="who" style="left:6mm;top:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face ink"><img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:6mm;left:50%;top:50%;transform:translate(-50%,-50%)">
  <p class="caps" style="position:absolute;left:0;right:0;bottom:6mm;text-align:center;font-size:2mm;color:#B8AC98">хустка «Ранкова кава»</p></div>"""
    return f, b

def c_triptych():
    strips = "".join(f'<div style="position:absolute;top:0;bottom:0;left:{i*45}mm;width:45mm;overflow:hidden;border-right:{".3mm solid #fff" if i<1 else "0"}"><img class="fill" src="{PRINTS[k]}" alt="" style="object-position:{pos};transform:scale({sc})"></div>' for i, (k, pos, sc) in enumerate((("kolo", "50% 20%", 1.5), ("smil", "50% 50%", 1.6))))
    f = f"""<div class="face white">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:6mm;top:5.4mm">
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face white">{strips}</div>"""
    return f, b

def c_swatch():
    f = f"""<div class="face white">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:6mm;top:5.4mm">
  <div style="position:absolute;right:6mm;top:6mm;width:13mm;height:13mm;overflow:hidden"><img class="fill" src="{PRINTS['kolo']}" alt="" style="object-position:50% 16%;transform:scale(2.2)"></div>
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face ink"><img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:6mm;left:50%;top:45%;transform:translate(-50%,-50%)">
  <p class="caps" style="position:absolute;left:0;right:0;bottom:6mm;text-align:center;font-size:2mm;color:#B8AC98">хустка «Коло сонця» · 88 × 88 см</p></div>"""
    return f, b

def c_marker():
    f = f"""<div class="face white">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:6mm;top:5.4mm">
  <p style="position:absolute;left:6mm;top:19mm;font-family:Montserrat,sans-serif;font-weight:500;font-size:4.6mm;line-height:1;padding:1.6mm 2.4mm 1.4mm;background:{YEL};color:{INK};white-space:nowrap;clip-path:polygon(.5mm 0,100% .3mm,calc(100% - .4mm) 100%,0 calc(100% - .4mm))">{NAME}</p>
  <p class="tt" style="position:absolute;left:6mm;top:28.2mm">{TITLE}</p>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face" style="background:{YEL}"><img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:6.4mm;left:50%;top:50%;transform:translate(-50%,-50%)"></div>"""
    return f, b

def c_plate():
    f = f"""<div class="face"><img class="fill" src="{PRINTS['vyr']}" alt="" style="object-position:50% 50%;transform:scale(1.3)">
  <div style="position:absolute;left:6mm;bottom:6mm;background:#fff;padding:3mm 4mm 2.8mm;min-width:40mm"><p class="nm" style="font-size:3.6mm">{NAME}</p><p class="tt">{TITLE}</p></div></div>"""
    b = f"""<div class="face ink">
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:5mm;left:6mm;top:6mm">
  <div class="ct" style="left:6mm;bottom:6mm;color:{CREAM}"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div>
  <p class="caps" style="position:absolute;right:6mm;bottom:6mm;font-size:2mm;color:#B8AC98">«Вир почуттів»</p></div>"""
    return f, b

def c_edge():
    f = f"""<div class="face white">
  <div style="position:absolute;right:0;top:0;bottom:0;width:28mm;overflow:hidden"><img class="fill" src="{PRINTS['smil']}" alt="" style="object-position:70% 50%;transform:scale(1.3)"></div>
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.2mm;left:5mm;bottom:6mm;transform-origin:left bottom;transform:rotate(-90deg) translate(0,100%)">
  <div class="ct" style="left:14mm;top:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div>
  <div class="who" style="left:14mm;bottom:6mm"><p class="nm">Світлана<br>Сніжко</p><p class="tt">{TITLE}</p></div></div>"""
    b = f"""<div class="face ink"><img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:6mm;left:50%;top:50%;transform:translate(-50%,-50%)"></div>"""
    return f, b

def c_qr_dots():
    f = f"""<div class="face" style="background:{CREAM}">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:6mm;top:5.4mm">
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face" style="background:{CREAM}">
  <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:32mm;height:32mm">{qr_styled("dots", INK, hole=(9, 3))}
    <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:9.4mm;height:2.9mm;border-radius:1.6mm;background:{YEL}"><img src="{LOGO_K}" alt="OBIIMY" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);height:1.6mm"></div></div>
  <p class="caps" style="position:absolute;left:6mm;top:50%;transform:translateY(-50%);font-size:2mm;color:#4B423B;line-height:1.8">Крамниця<br><span style="font-weight:600;letter-spacing:.06em;text-transform:none;font-size:2.6mm">{SITE}</span></p></div>"""
    return f, b

def c_qr_yellow():
    f = f"""<div class="face" style="background:{YEL}">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.6mm;left:6mm;top:6mm">
  <div style="position:absolute;right:6mm;top:50%;transform:translateY(-50%);width:26mm;height:26mm">{qr_styled("round", INK)}</div>
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm" style="font-size:4.4mm">Світлана<br>Сніжко</p><p class="tt">{TITLE}</p></div></div>"""
    b = f"""<div class="face ink">
  <div class="ct" style="left:6mm;top:50%;transform:translateY(-50%);color:{CREAM};font-size:2.8mm;line-height:1.7"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div>
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:5mm;right:6mm;bottom:6mm"></div>"""
    return f, b

def c_qr_print():
    f = f"""<div class="face white">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:6mm;top:5.4mm">
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face white">
  <div style="position:absolute;right:6mm;top:50%;transform:translateY(-50%);width:32mm;height:32mm">{qr_styled("round", INK, fill=PRINTS['smil'], shade=.65, outline=.15)}</div>
  <div style="position:absolute;left:6mm;top:50%;transform:translateY(-50%)"><p class="caps" style="font-size:2mm;color:#4B423B">Крамниця</p><p style="font-family:Montserrat,sans-serif;font-weight:500;font-size:3.2mm;margin-top:1.2mm">{SITE}</p><p class="ct" style="position:static;font-size:2.2mm;color:#4B423B;margin-top:1.2mm;max-width:38mm">хустки · твіллі · маски для сну · набори</p></div></div>"""
    return f, b

def c_qr_silk():
    f = f"""<div class="face ink">
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:5mm;left:6mm;top:6mm">
  <div class="who" style="left:6mm;bottom:6mm;color:{CREAM}"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm;color:{CREAM}"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face"><img class="fill" src="{PRINTS['kolo']}" alt="" style="object-position:50% 50%;transform:scale(1.3)">
  <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:30mm;height:30mm;background:#fff;border-radius:2mm;padding:2.6mm;box-shadow:0 .6mm 2mm rgba(0,0,0,.18)">{qr_styled("round", INK)}</div></div>"""
    return f, b

def c_qr_square():
    f = f"""<div class="face ink">
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:5mm;left:6mm;top:6mm">
  <div class="who" style="left:6mm;bottom:6mm;color:{CREAM}"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm;color:{CREAM}"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face ink">
  <div style="position:absolute;right:6mm;top:50%;transform:translateY(-50%);width:30mm;height:30mm;background:{YEL};padding:4mm">{qr_styled("square", INK)}</div>
  <div class="ct" style="left:6mm;top:50%;transform:translateY(-50%);color:{CREAM};max-width:44mm"><p class="caps" style="color:{YEL};font-size:2.2mm;margin-bottom:1.2mm">Крамниця</p><p style="font-size:3.4mm">{SITE}</p><p style="font-size:2.4mm;color:#B8AC98;margin-top:1mm;line-height:1.5">хустки · твіллі<br>маски для сну · набори</p></div></div>"""
    return f, b

def c_qr_tag():
    f = f"""<div class="face" style="background:{CREAM}">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:6mm;top:5.4mm">
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face" style="background:{CREAM}">
  <div style="position:absolute;left:58.5mm;top:9.2mm;width:.5mm;height:16mm;background:{YEL};transform-origin:top left;transform:rotate(34deg) translate(-50%,-15.4mm)"></div>
  <div style="position:absolute;left:46mm;top:5mm;width:30mm;height:40mm;background:#fff;border-radius:2mm;box-shadow:0 .6mm 2mm rgba(0,0,0,.14)">
    <div style="position:absolute;left:50%;top:2.6mm;transform:translateX(-50%);width:2.6mm;height:2.6mm;border-radius:50%;background:{CREAM};border:.35mm solid {INK}"></div>
    <div style="position:absolute;left:50%;top:8.2mm;transform:translateX(-50%);width:23mm;height:23mm">{qr_styled("round", INK)}</div>
    <p class="caps" style="position:absolute;left:0;right:0;top:33.4mm;text-align:center;font-size:1.9mm;letter-spacing:.12em;text-transform:none;font-weight:600">{SITE}</p></div>
  <p class="caps" style="position:absolute;left:6mm;top:50%;transform:translateY(-50%);font-size:2mm;color:#4B423B;line-height:1.8">Крамниця<br><span style="font-weight:600;letter-spacing:.06em;text-transform:none;font-size:2.6mm">{SITE}</span></p></div>"""
    return f, b

def c_qr_half():
    f = f"""<div class="face white">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:6mm;top:5.4mm">
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face white">
  <div style="position:absolute;left:0;top:0;width:42mm;height:50mm;overflow:hidden"><img class="fill" src="{PRINTS['smil']}" alt="" style="object-position:50% 50%;transform:scale(1.6)"></div>
  <div style="position:absolute;left:42mm;top:0;width:48mm;height:50mm">
    <div style="position:absolute;left:50%;top:10mm;transform:translateX(-50%);width:24mm;height:24mm">{qr_styled("square", INK)}</div>
    <p class="caps" style="position:absolute;left:0;right:0;top:39.5mm;text-align:center;font-size:2mm;color:#4B423B">Крамниця</p>
    <p style="position:absolute;left:0;right:0;top:42.6mm;text-align:center;font-family:Montserrat,sans-serif;font-weight:600;font-size:2.6mm;letter-spacing:.04em">{SITE}</p></div></div>"""
    return f, b

def c_qr_front():
    f = f"""<div class="face white">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.4mm;left:6mm;top:5.4mm">
  <div style="position:absolute;right:6mm;top:6mm;width:16mm;height:16mm">{qr(INK)}</div>
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face"><img class="fill" src="{PRINTS['dotyk']}" alt="" style="object-position:50% 50%;transform:scale(1.3)"></div>"""
    return f, b

def c_qr_vertical():
    f = f"""<div class="face ink">
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:4.6mm;left:50%;top:7mm;transform:translateX(-50%)">
  <div class="who" style="left:6mm;bottom:6mm;color:{CREAM}"><p class="nm" style="font-size:4.6mm;line-height:1.15;font-weight:400">Світлана<br>Сніжко</p><p class="tt">{TITLE}</p></div></div>"""
    b = f"""<div class="face" style="background:{CREAM}">
  <div style="position:absolute;left:50%;top:8mm;transform:translateX(-50%);width:30mm;height:30mm">{qr_styled("dots", INK)}</div>
  <p class="caps" style="position:absolute;left:0;right:0;top:46mm;text-align:center;font-size:2mm;color:#4B423B">Крамниця</p>
  <p style="position:absolute;left:0;right:0;top:49.4mm;text-align:center;font-family:Montserrat,sans-serif;font-weight:600;font-size:3mm;letter-spacing:.04em">{SITE}</p>
  <div style="position:absolute;left:0;right:0;bottom:0;height:26mm;background:{YEL}">
    <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:3.8mm;left:50%;top:6mm;transform:translateX(-50%)">
    <div class="ct" style="left:0;right:0;bottom:6mm;text-align:center;font-size:2.4mm;font-weight:500"><p>{PHONE}</p><p>{MAIL}</p></div></div></div>"""
    return f, b

def c_qr_big():
    f = f"""<div class="face" style="background:{YEL}">
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4.6mm;left:6mm;top:6mm">
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm">{NAME}</p><p class="tt">{TITLE}</p></div>
  <div class="ct r" style="right:6mm;bottom:6mm"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>"""
    b = f"""<div class="face white">
  <div style="position:absolute;left:6mm;top:6mm;width:38mm;height:38mm">{qr_styled("square", INK)}</div>
  <img class="logo" src="{LOGO_K}" alt="OBIIMY" style="height:4mm;right:6mm;top:6.2mm">
  <div class="ct r" style="right:6mm;bottom:6mm"><p class="caps" style="font-size:2mm;color:#4B423B;margin-bottom:1mm">Крамниця</p><p style="font-family:Montserrat,sans-serif;font-weight:600;font-size:3.2mm;letter-spacing:.03em">{SITE}</p></div></div>"""
    return f, b

CARDS = [
    ("01", "Чорнило", "Чорна картка, білий логотип, ім’я Montserrat; зворот — логотип по центру, адреса й жовта кромка 2 мм знизу.", c_ink, ""),
    ("02", "Шовк на звороті", "Білий лицьовий бік; на звороті — хустка «Коло сонця» на всю картку, кадр усередині кайми.", c_print_back, ""),
    ("03", "Жовта", "Фірмовий жовтий на лицьовому боці; зворот чорний з логотипом і рядком «100 % натуральний шовк».", c_yellow, ""),
    ("04", "Монограма", "Монограма «СС» тонким Montserrat на білому; зворот чорний зі смугою принту «Вир почуттів».", c_monogram, ""),
    ("05", "Кант", "Смуга принту «Сміливість» 12 мм уздовж краю, як кант хустки; на звороті смуга з протилежного боку.", c_twilly, ""),
    ("06", "Етикетка", "Картка-ярлик на щільному папері: скруглені кути, пунктир «стібка», ім’я по центру; контакти на звороті.", c_label, ""),
    ("07", "Вертикальна", "50 × 90, чорна; зворот — фрагмент хустки «Коло сонця» на всю картку, контакти внизу на темній плашці.", c_vertical, "v"),
    ("08", "QR", "Білий лицьовий бік; на звороті справжній QR-код на obiimy.world і рядок категорій.", c_qr, ""),
    ("09", "Тиснення", "Чорна картка, ім’я й логотип на звороті — золотом (на макеті імітація фольги; у друку — тиснення фольгою, гротеск напівжирний, щоб тонкі штрихи не обривалися).", c_foil, ""),
    ("10", "Підпис", "Кремовий папір, ім’я курсивом як підпис-заглушка (у друк — справжній підпис зі скану); рядок «CEO · засновниця · художниця»; зворот — хустка «Сміливість».", c_signature, ""),
    ("11", "Навпіл", "Половина картки — принт «Сміливий дотик», половина — біла з ім’ям; зворот чорний з контактами і QR.", c_split, ""),
    ("12", "Двомовна", "Лицьовий бік чорний українською, зворот кремовий латиницею — Svitlana Snizhko, CEO · Founder — для закордонних зустрічей.", c_bilingual, ""),
    ("13", "Трипілля", "Зворот — фрагмент хустки «Trypillia — The Art of Origins» (Kraїna Edem × OBIIMY); лицьовий бік чорний з рядком «CEO · засновниця · художниця».", c_trypillia, ""),
    ("14", "Велике ім’я", "Кремовий папір, ім’я тонким Montserrat Light на 8 мм у два рядки — типографічна картка без зображень; зворот чорний з логотипом.", c_bigname, ""),
    ("15", "Рамка", "Тонка лінія-рамка 0,3 мм за 4 мм від краю, логотип зверху, ім’я по центру, контакти у два рядки; зворот жовтий у тій самій рамці.", c_frame, ""),
    ("16", "Смуга", "Смуга принту «Сміливість» 12 мм унизу лицьового боку, ім’я й контакти над нею; на звороті смуга зверху й логотип.", c_band, ""),
    ("17", "Ілюмінатор", "Круглий фрагмент хустки «Грація» 36 мм праворуч, ім’я у два рядки ліворуч; зворот чорний з контактами й логотипом.", c_porthole, ""),
    ("18", "Верх і низ", "Верхня половина — принт «Сміливий дотик», нижня біла з ім’ям і контактами; зворот чорний із жовтою кромкою зверху.", c_topbottom, ""),
    ("19", "Лукбук", "Лицьовий бік чорний; зворот — кадр із лукбуку: твіллі «Поцілунок сонця» бантом на зап’ястку, адреса крамниці внизу. Кадр 850 × 1100 px дає ≈ 225 dpi — у друк лише з вихідником від клієнта.", c_lookbook, ""),
    ("20", "Жовта лінія", "Біла картка з жовтою смугою 2,5 мм по лівому краю; на звороті смуга по правому краю і логотип по центру.", c_rule, ""),
    ("21", "Стрічка", "Діагональна стрічка зі смугастої кайми «Ранкової кави» через білу картку, як пов’язана твіллі; зворот чорний з логотипом і назвою принту.", c_sash, ""),
    ("22", "Диптих", "Зворот — дві половини: «Коло сонця» і «Сміливість», два жовті принти в одному тоні, між ними біла лінія 0,3 мм; лицьовий бік білий, мінімальний.", c_triptych, ""),
    ("23", "Зразок", "Квадрат принту «Коло сонця» 13 мм у правому верхньому куті, як зразок тканини; на звороті логотип і рядок «хустка «Коло сонця» · 88 × 88 см».", c_swatch, ""),
    ("24", "Маркер", "Ім’я на жовтій плашці, наче виділене маркером, на білій картці; зворот жовтий з логотипом.", c_marker, ""),
    ("25", "Плашка на шовку", "Лицьовий бік — принт «Вир почуттів» на всю картку, ім’я на білій плашці в куті; зворот чорний з логотипом, контактами й назвою принту.", c_plate, ""),
    ("26", "Корінець", "Логотип вертикально вздовж лівого краю, як корінець; ім’я горизонтально, смуга принту «Сміливість» 28 мм праворуч; зворот чорний з логотипом.", c_edge, ""),
    ("27", "QR крапками", "Кремова картка; на звороті QR-код круглими модулями, логотип на жовтій пілюлі у вирізі посередині (рівень корекції H — код читається).", c_qr_dots, ""),
    ("28", "QR на жовтому", "Жовтий лицьовий бік, QR-код 26 мм зі скругленими модулями поруч з ім’ям — «робоча» картка для виставок; зворот чорний з контактами.", c_qr_yellow, ""),
    ("29", "QR із принту", "Модулі QR-коду залиті притемненим на 65 % принтом «Сміливість» у чорній обводці — темна золотаво-синя текстура, кутові мітки чорні; читається обома декодерами, перед тиражем — тестовий оттиск.", c_qr_print, ""),
    ("30", "QR у шовку", "Зворот — хустка «Коло сонця» на всю картку, QR-код на білій плашці зі скругленими кутами посередині; лицьовий бік чорний.", c_qr_silk, ""),
    ("31", "Жовтий квадрат", "Чорна картка з обох боків; на звороті жовтий квадрат 30 мм із QR-кодом (квадратні модулі — на жовтому читаються краще за скруглені), ліворуч — адреса крамниці.", c_qr_square, ""),
    ("32", "Бирка", "Кремова картка; на звороті QR-код на білій бирці з отвором і жовтою ниткою — як етикетка на подарунку.", c_qr_tag, ""),
    ("33", "Половина", "Зворот навпіл: ліворуч 42 мм принту «Сміливість», праворуч QR-код 24 мм квадратними модулями на білому з тихою зоною 12 мм від принту й адресою крамниці; лицьовий бік білий.", c_qr_half, ""),
    ("34", "Усе на лицьовому", "QR-код 16 мм у куті лицьового боку поруч з ім’ям і контактами; зворот — принт «Сміливий дотик» на всю картку без тексту.", c_qr_front, ""),
    ("35", "Вертикальна QR", "Картка 50 × 90: чорний лицьовий бік з логотипом та ім’ям; зворот кремовий — QR-код крапками 30 мм, адреса, жовта смуга 26 мм з логотипом і контактами знизу.", c_qr_vertical, "v"),
    ("36", "Великий QR", "Зворот — QR-код 38 мм на всю висоту білої картки, логотип і адреса в правому куті; лицьовий бік жовтий.", c_qr_big, ""),
]

CSS = f"""
@font-face {{ font-family: 'Playfair'; src: url('brand/fonts/playfair-latin-400-italic.woff2') format('woff2'); font-style: italic; font-weight: 400; unicode-range: U+0000-00FF; }}
@font-face {{ font-family: 'Playfair'; src: url('brand/fonts/playfair-cyrillic-400-italic.woff2') format('woff2'); font-style: italic; font-weight: 400; unicode-range: U+0400-04FF; }}
* {{ box-sizing: border-box; }}
html {{ --mm: 5px; }}
body {{ margin: 0; background: #1B1715; color: {CREAM}; font-family: 'Montserrat', system-ui, sans-serif; -webkit-font-smoothing: antialiased; }}
.wrap {{ max-width: 1320px; margin: 0 auto; padding: 56px 24px 96px; }}
header {{ display: flex; justify-content: space-between; align-items: flex-end; gap: 24px; flex-wrap: wrap; margin-bottom: 18px; }}
header img {{ height: 34px; }}
h1 {{ font-family: 'Montserrat', sans-serif; font-weight: 400; font-size: 40px; line-height: 1.08; margin: 22px 0 10px; letter-spacing: -.01em; }}
.lead {{ color: #B8AC98; font-size: 17px; line-height: 1.55; max-width: 760px; margin: 0; }}
.lead b {{ color: {CREAM}; font-weight: 500; }}
.spec {{ display: flex; gap: 10px 28px; flex-wrap: wrap; margin: 26px 0 54px; padding: 18px 0; border-top: 1px solid #2E2824; border-bottom: 1px solid #2E2824; font-size: 14px; color: #B8AC98; }}
.spec span b {{ color: {CREAM}; font-weight: 500; }}
.spec .warn {{ color: {YEL}; }}
.tog {{ margin-left: auto; background: transparent; color: {CREAM}; border: 1px solid #4A423C; border-radius: 999px; padding: 8px 16px; font: 500 13px/1 'Montserrat', sans-serif; letter-spacing: .04em; cursor: pointer; }}
.tog[aria-pressed="true"] {{ background: {YEL}; color: {INK}; border-color: {YEL}; }}
.set {{ display: grid; grid-template-columns: 240px 1fr; gap: 28px 40px; align-items: start; padding: 44px 0; border-top: 1px solid #2E2824; }}
h2.ch {{ font-family: 'Montserrat', sans-serif; font-weight: 400; font-size: 32px; margin: 72px 0 6px; padding-top: 28px; border-top: 2px solid {YEL}; }}
h2.ch small {{ font-size: 14px; color: #8C8275; letter-spacing: .1em; margin-left: 10px; }}
h2.ch:first-of-type {{ margin-top: 0; }}
p.chd {{ color: #B8AC98; font-size: 15px; margin: 0 0 18px; max-width: 760px; }}
.toc {{ display: flex; gap: 10px 22px; flex-wrap: wrap; align-items: center; margin: 0 0 8px; font-size: 14px; }}
.toc a {{ color: {CREAM}; text-decoration: none; border-bottom: 1px solid #4A423C; padding-bottom: 2px; }}
.toc .pick {{ color: {YEL}; margin-left: auto; }}
.toc .pick a {{ color: {YEL}; border-color: {YEL}; }}
.set h2 {{ font-family: 'Montserrat', sans-serif; font-weight: 400; font-size: 26px; margin: 0 0 8px; line-height: 1.15; }}
.set h2 small {{ display: block; font-family: 'Montserrat', sans-serif; font-weight: 500; font-size: 12px; letter-spacing: .22em; text-transform: uppercase; color: {YEL}; margin-bottom: 10px; }}
.set p.d {{ color: #B8AC98; font-size: 15px; line-height: 1.5; margin: 0; }}
.pair {{ display: flex; gap: 32px; flex-wrap: wrap; align-items: flex-start; }}
.side {{ display: flex; flex-direction: column; gap: 10px; }}
.side em {{ font-style: normal; font-family: 'Montserrat', sans-serif; font-size: 11px; letter-spacing: .2em; text-transform: uppercase; color: #8C8275; }}
.card {{ width: calc(90 * var(--mm)); height: calc(50 * var(--mm)); position: relative; border-radius: 1.2px; overflow: hidden; box-shadow: 0 30px 60px -22px rgba(0,0,0,.85), 0 2px 6px rgba(0,0,0,.4); font-size: 10px; }}
.card.v {{ width: calc(50 * var(--mm)); height: calc(90 * var(--mm)); }}
.face {{ position: absolute; inset: 0; background: #fff; color: {INK}; overflow: hidden; }}
.face.ink {{ background: {INK}; color: {CREAM}; }}
.face.white {{ background: #fff; }}
.face > * {{ position: absolute; margin: 0; }}
.face p {{ margin: 0; }}
.fill {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.logo {{ position: absolute; display: block; }}
.nm {{ font-family: 'Montserrat', sans-serif; font-weight: 500; font-size: 3.9mm; line-height: 1.2; letter-spacing: .01em; white-space: nowrap; }}
.tt {{ font-family: 'Montserrat', sans-serif; font-weight: 500; font-size: 2mm; letter-spacing: .22em; text-transform: uppercase; margin-top: 1.3mm !important; color: #4B423B; }}
.face.ink .tt {{ color: {CREAM}; }}
.ct {{ position: absolute; font-family: 'Montserrat', sans-serif; font-weight: 400; font-size: 2.3mm; line-height: 1.6; letter-spacing: .01em; font-variant-numeric: lining-nums tabular-nums; }}
.face.ink .ct {{ font-size: 2.4mm; font-weight: 500; }}
.ct.r {{ text-align: right; }}
.caps {{ font-family: 'Montserrat', sans-serif; font-weight: 500; letter-spacing: .2em; text-transform: uppercase; }}
.mono {{ position: absolute; left: 4mm; top: -1mm; font-family: 'Montserrat', sans-serif; font-weight: 300; font-size: 34mm; line-height: 1; color: #E8E1D5; letter-spacing: -.04em; }}
.stitch {{ position: absolute; inset: 2.2mm; border: .35mm dashed #B9AE9C; border-radius: 1.6mm; }}
.foil-logo {{ -webkit-mask: url(brand/logo-ink.svg) center / contain no-repeat; mask: url(brand/logo-ink.svg) center / contain no-repeat; background: linear-gradient(100deg, #8A6A14 0%, #E2BC55 28%, #FFF0B8 50%, #D9B14B 70%, #7E5F10 100%); }}
.foil {{ background: linear-gradient(100deg, #8A6A14 0%, #E2BC55 28%, #FFF0B8 50%, #D9B14B 70%, #7E5F10 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.sig {{ position: absolute; left: 6mm; top: 9mm; font-family: 'Playfair', serif; font-style: italic; font-weight: 400; font-size: 9mm; line-height: 1; color: {INK}; letter-spacing: -.02em; white-space: nowrap; }}
.qr {{ width: 100%; height: 100%; display: block; shape-rendering: crispEdges; }}
.who {{ position: absolute; }}
.set .card .face {{ font-size: calc(1 * var(--mm)); }}
.note {{ margin-top: 56px; padding-top: 24px; border-top: 1px solid #2E2824; color: #B8AC98; font-size: 14px; line-height: 1.6; max-width: 820px; }}
@media (max-width: 900px) {{ .set {{ grid-template-columns: 1fr; gap: 18px; }} html {{ --mm: 4.2px; }} .wrap {{ padding: 36px 16px 64px; }} h1 {{ font-size: 34px; }} }}
@media (max-width: 460px) {{ html {{ --mm: 3.6px; }} }}
"""
# mm inside the cards: every `Nmm` in the faces is scaled through --mm so the page can shrink on a phone
def mm_to_calc(html):
    return re.sub(r"(-?\d*\.?\d+)mm", lambda m: f"calc({m.group(1)} * var(--mm))", html)

CHAPTERS = [("klasyka", "Класика", "Без зображень: чорні, білі, жовті, кремові картки — типографіка й логотип.", ("01", "03", "04", "06", "07", "09", "10", "12", "14", "15", "20", "24", "26")),
            ("prynt", "З принтом", "Справжні хустки obiimy.world на звороті, смугою, колом або на всю картку.", ("02", "05", "11", "13", "16", "17", "18", "19", "21", "22", "23", "25")),
            ("qr", "QR", "Картки, де QR-код на obiimy.world — частина композиції; усі коди справжні й перевірені. Порядок за висновком панелі: рекомендовані — 27, 32, 30, 34; робочі, для виставок — 35, 08, 28, 31, 36; потребують тестового оттиску перед тиражем — 29, 33.", ("27", "32", "30", "34", "35", "08", "28", "31", "36", "29", "33"))]
BY = {c[0]: c for c in CARDS}
assert sorted(n for ch in CHAPTERS for n in ch[3]) == sorted(BY), "every card in exactly one chapter"
sets = []
for slug, chtitle, chdesc, nums in CHAPTERS:
  sets.append(f'<h2 class="ch" id="{slug}">{chtitle} <small>{len(nums)}</small></h2><p class="chd">{nb(chdesc)}</p>')
  for num in nums:
    _, title, desc, fn, kind = BY[num]
    f, b = fn()
    sets.append(f'''
<section class="set" id="card-{num}">
  <div><h2><small>Варіант {num}</small>{title}</h2><p class="d">{nb(desc)}</p></div>
  <div class="pair">
    <div class="side"><em>Лицьовий бік</em><div class="card {kind}">{mm_to_calc(f)}</div></div>
    <div class="side"><em>Зворот</em><div class="card {kind}">{mm_to_calc(b)}</div></div>
  </div>
</section>''')

page = f"""<html lang="uk">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Візитки · Світлана Сніжко · OBIIMY</title>
<link rel="icon" href="brand/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&display=swap">
<style>{mm_to_calc(CSS)}</style>
<div class="wrap">
<header><img src="{LOGO_W}" alt="OBIIMY"><span style="font-family:Montserrat,sans-serif;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:#8C8275">Макети · 10–11.11.2026</span></header>
<h1>Особисті візитки<br>Світлани Сніжко</h1>
<p class="lead">Тридцять шість варіантів особистої візитки CEO OBIIMY у трьох главах — класика, з принтом, QR: лицьовий бік і зворот у справжній пропорції картки. Ім’я, посада, телефон, пошта й адреса крамниці; принти — справжні хустки з obiimy.world; QR-коди справжні, ведуть на <b>obiimy.world</b> (стилізовані — з рівнем корекції H, перевірені декодером).</p>
<div class="spec"><span><b>Формат</b> 90 × 50 мм (варіант 07 — 50 × 90)</span><span><b>Вильоти</b> +3 мм з кожного боку</span><span><b>Шрифт</b> Montserrat — фірмовий, як на obiimy.world (підпис у варіанті 10 — заглушка курсивом до скану)</span><span><b>Телефон</b> {PHONE}</span><span class="warn">Скриньку {MAIL} підтвердити</span><button type="button" id="scale" class="tog">Натуральний розмір 1:1</button></div>
<p class="toc"><a href="#klasyka">Класика · 13</a><a href="#prynt">З принтом · 12</a><a href="#qr">QR · 11</a><span class="pick">Панель рекомендує: <a href="#card-13">13 Трипілля</a> · <a href="#card-09">09 Тиснення</a> · <a href="#card-27">27 QR крапками</a> · резерв <a href="#card-14">14</a>, <a href="#card-25">25</a>, <a href="#card-32">32</a></span></p>
{"".join(sets)}
<p class="note">Для друку кожен варіант зберемо у PDF 96 × 56 мм (з вильотами) у CMYK; для карток із принтом на всю площину («Сміливий дотик», «Вир почуттів») потрібні вихідні фото хусток від клієнта у вищій роздільності — наявні дають близько 265 dpi. «Тиснення» на макеті — імітація фольги на екрані. Будь-який варіант можна зібрати в іншому кольорі картону або з іншим принтом із колекцій.</p>
</div>
<script>
(function () {{
  var b = document.getElementById('scale'), on = false;
  if (!b) return;
  b.addEventListener('click', function () {{
    on = !on; b.setAttribute('aria-pressed', String(on));
    document.documentElement.style.setProperty('--mm', on ? (96 / 25.4) + 'px' : '');   /* 1 mm at 96 dpi; the page's own scale otherwise */
  }});
}})();
</script>
"""
(ROOT / "cards.html").write_text(page, encoding="utf-8")
print("cards.html", len(CARDS), "cards")
