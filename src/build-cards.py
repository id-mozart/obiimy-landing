# -*- coding: utf-8 -*-
"""Personal business cards for Світлана Сніжко, CEO of OBIIMY (10.11.2026, client: «сделай отдельную страницу где-то и сделай на ней
макеты визитных карточек клевых личных для обиймы»). A service page (HIDDEN in build-site.py): ten pairs front / back at the true
proportion 90 × 50 mm, 6 px per mm, on a dark studio field. Facts: name and title from the brief; the phone is a placeholder the client
replaces; the e-mail from the brief; the prints are the real flat scarves of obiimy.world; the QR codes point at https://obiimy.world
(segno). Nothing about foil or paper is a promise — the «тиснення» card is a mock-up of the effect, said so on the page.
python3 src/build-cards.py → cards.html → python3 build-site.py → site/cards.html"""
import pathlib, re, sys
import segno
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ads" / "solo"))
from kit import nb

NAME, TITLE, PHONE, MAIL, SITE = "Світлана Сніжко", "CEO", "+380 67 123 45 67", "svitlana@obiimy.world", "obiimy.world"
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
  <div class="who" style="left:6mm;bottom:6mm"><p class="nm" style="font-size:5.2mm;font-weight:600">{NAME}</p><p class="tt">{TITLE}</p></div>
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
  <p class="nm c" style="position:absolute;left:0;right:0;top:17mm;text-align:center;font-size:5.2mm">{NAME}</p>
  <p class="tt c" style="position:absolute;left:0;right:0;top:24.5mm;text-align:center">{TITLE}</p>
  <p class="caps" style="position:absolute;left:0;right:0;bottom:6.5mm;text-align:center;font-size:2.3mm;color:#4B423B">OBIIMY · шовк · Україна</p></div>'''
    b = f'''<div class="face" style="background:{PAPER};border-radius:3mm">
  <div class="stitch"></div>
  <div class="ct c" style="left:0;right:0;top:50%;transform:translateY(-50%);text-align:center;font-size:2.8mm;line-height:1.7"><p>{PHONE}</p><p>{MAIL}</p><p>{SITE}</p></div></div>'''
    return f, b

def c_vertical():
    f = f'''<div class="face ink">
  <img class="logo" src="{LOGO_W}" alt="OBIIMY" style="height:4.6mm;left:50%;top:7mm;transform:translateX(-50%)">
  <div class="who" style="left:6mm;bottom:6mm;color:{CREAM}"><p class="nm" style="font-size:5mm;line-height:1.1">Світлана<br>Сніжко</p><p class="tt">{TITLE}</p></div></div>'''
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
  <p class="nm foil" style="position:absolute;left:6mm;bottom:12.5mm;font-size:6.4mm;font-weight:600">{NAME}</p>
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
  <div class="who" style="left:51mm;bottom:6mm"><p class="nm" style="font-size:4.4mm;line-height:1.1">Світлана<br>Сніжко</p><p class="tt">{TITLE}</p></div></div>'''
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

CARDS = [
    ("01", "Чорнило", "Чорна картка, білий логотип, ім’я антиквою; зворот — логотип по центру, адреса й жовта кромка 2 мм знизу.", c_ink, ""),
    ("02", "Шовк на звороті", "Білий лицьовий бік; на звороті — хустка «Коло сонця» на всю картку, кадр усередині кайми.", c_print_back, ""),
    ("03", "Жовта", "Фірмовий жовтий на лицьовому боці; зворот чорний з логотипом і рядком «100 % натуральний шовк».", c_yellow, ""),
    ("04", "Монограма", "Монограма «СС» світлою антиквою на білому; зворот чорний зі смугою принту «Вир почуттів».", c_monogram, ""),
    ("05", "Кант", "Смуга принту «Сміливість» 12 мм уздовж краю, як кант хустки; на звороті смуга з протилежного боку.", c_twilly, ""),
    ("06", "Етикетка", "Картка-ярлик на щільному папері: скруглені кути, пунктир «стібка», ім’я по центру; контакти на звороті.", c_label, ""),
    ("07", "Вертикальна", "50 × 90, чорна; зворот — фрагмент хустки «Коло сонця» на всю картку, контакти внизу на темній плашці.", c_vertical, "v"),
    ("08", "QR", "Білий лицьовий бік; на звороті справжній QR-код на obiimy.world і рядок категорій.", c_qr, ""),
    ("09", "Тиснення", "Чорна картка, ім’я й логотип на звороті — золотом (на макеті імітація фольги; у друку — тиснення фольгою, антиква напівжирна, щоб засічки не обривалися).", c_foil, ""),
    ("10", "Підпис", "Кремовий папір, ім’я курсивом Playfair як підпис (у друк — справжній підпис зі скану); рядок «CEO · засновниця · художниця»; зворот — хустка «Сміливість».", c_signature, ""),
    ("11", "Навпіл", "Половина картки — принт «Сміливий дотик», половина — біла з ім’ям; зворот чорний з контактами і QR.", c_split, ""),
    ("12", "Двомовна", "Лицьовий бік чорний українською, зворот кремовий латиницею — Svitlana Snizhko, CEO · Founder — для закордонних зустрічей.", c_bilingual, ""),
    ("13", "Трипілля", "Зворот — фрагмент хустки «Trypillia — The Art of Origins» (Kraїna Edem × OBIIMY); лицьовий бік чорний з рядком «CEO · засновниця · художниця».", c_trypillia, ""),
]

CSS = f"""
@font-face {{ font-family: 'Playfair'; src: url('brand/fonts/playfair-latin-400-italic.woff2') format('woff2'); font-style: italic; font-weight: 400; unicode-range: U+0000-00FF; }}
@font-face {{ font-family: 'Playfair'; src: url('brand/fonts/playfair-cyrillic-400-italic.woff2') format('woff2'); font-style: italic; font-weight: 400; unicode-range: U+0400-04FF; }}
* {{ box-sizing: border-box; }}
html {{ --mm: 5px; }}
body {{ margin: 0; background: #1B1715; color: {CREAM}; font-family: 'Onest', system-ui, sans-serif; -webkit-font-smoothing: antialiased; }}
.wrap {{ max-width: 1320px; margin: 0 auto; padding: 56px 24px 96px; }}
header {{ display: flex; justify-content: space-between; align-items: flex-end; gap: 24px; flex-wrap: wrap; margin-bottom: 18px; }}
header img {{ height: 34px; }}
h1 {{ font-family: 'EB Garamond', serif; font-weight: 500; font-size: 44px; line-height: 1.05; margin: 22px 0 10px; letter-spacing: -.01em; }}
.lead {{ color: #B8AC98; font-size: 17px; line-height: 1.55; max-width: 760px; margin: 0; }}
.lead b {{ color: {CREAM}; font-weight: 500; }}
.spec {{ display: flex; gap: 10px 28px; flex-wrap: wrap; margin: 26px 0 54px; padding: 18px 0; border-top: 1px solid #2E2824; border-bottom: 1px solid #2E2824; font-size: 14px; color: #B8AC98; }}
.spec span b {{ color: {CREAM}; font-weight: 500; }}
.spec .warn {{ color: {YEL}; }}
.tog {{ margin-left: auto; background: transparent; color: {CREAM}; border: 1px solid #4A423C; border-radius: 999px; padding: 8px 16px; font: 500 13px/1 'Montserrat', sans-serif; letter-spacing: .04em; cursor: pointer; }}
.tog[aria-pressed="true"] {{ background: {YEL}; color: {INK}; border-color: {YEL}; }}
.set {{ display: grid; grid-template-columns: 240px 1fr; gap: 28px 40px; align-items: start; padding: 44px 0; border-top: 1px solid #2E2824; }}
.set:first-of-type {{ border-top: 0; padding-top: 0; }}
.set h2 {{ font-family: 'EB Garamond', serif; font-weight: 500; font-size: 30px; margin: 0 0 8px; line-height: 1.1; }}
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
.nm {{ font-family: 'EB Garamond', serif; font-weight: 500; font-size: 4.6mm; line-height: 1.15; letter-spacing: .005em; white-space: nowrap; }}
.tt {{ font-family: 'Montserrat', sans-serif; font-weight: 500; font-size: 2.1mm; letter-spacing: .22em; text-transform: uppercase; margin-top: 1.2mm !important; color: #4B423B; }}
.face.ink .tt {{ color: {CREAM}; }}
.ct {{ position: absolute; font-family: 'Onest', sans-serif; font-weight: 400; font-size: 2.45mm; line-height: 1.55; letter-spacing: .01em; }}
.face.ink .ct {{ font-size: 2.6mm; font-weight: 500; }}
.ct.r {{ text-align: right; }}
.caps {{ font-family: 'Montserrat', sans-serif; font-weight: 500; letter-spacing: .2em; text-transform: uppercase; }}
.mono {{ position: absolute; left: 5mm; top: -2mm; font-family: 'EB Garamond', serif; font-weight: 500; font-size: 36mm; line-height: 1; color: #E8E1D5; letter-spacing: -.02em; }}
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

sets = []
for num, title, desc, fn, kind in CARDS:
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;1,500&family=Montserrat:wght@400;500&family=Onest:wght@400;500&display=swap">
<style>{mm_to_calc(CSS)}</style>
<div class="wrap">
<header><img src="{LOGO_W}" alt="OBIIMY"><span style="font-family:Montserrat,sans-serif;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:#8C8275">Макети · 10.11.2026</span></header>
<h1>Особисті візитки<br>Світлани Сніжко</h1>
<p class="lead">Тринадцять варіантів особистої візитки CEO OBIIMY: лицьовий бік і зворот у справжній пропорції картки. Ім’я, посада, телефон, пошта й адреса крамниці; принти — справжні хустки з obiimy.world; QR-коди робочі, ведуть на <b>obiimy.world</b>.</p>
<div class="spec"><span><b>Формат</b> 90 × 50 мм (варіант 07 — 50 × 90)</span><span><b>Вильоти</b> +3 мм з кожного боку</span><span><b>Шрифти</b> EB Garamond · Montserrat · Onest · Playfair</span><span class="warn">Телефон {PHONE} — заглушка, замінити на справжній перед друком; скриньку {MAIL} підтвердити</span><button type="button" id="scale" class="tog">Натуральний розмір 1:1</button></div>
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
