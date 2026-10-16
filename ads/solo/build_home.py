"""SOLO banners for the home page of obiimy.world (1920 × 576, as the current one): the collection lock-up «КОЛЕКЦІЯ / СОЛО /
ШЛЯХ ДО СЕБЕ» in a light geometric grotesque, the yellow pill «Жіноча сила крізь десятиліття», the vertical OBIIMY™ on the
right — six compositions on real SOLO frames. Copy from the press release. Output: home.html → out-home/*.jpg
(cd ads && ADS=solo/home.html OUT=solo/out-home node render.mjs)."""
import pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit import P, PP, S, CUT, HI, nb, LOGO_W, LOGO_K, GRAIN

def S2(name): return f"src/{name}-2k.webp" if (HERE / f"src/{name}-2k.webp").exists() else f"src/{name}.webp"

W, H = 1920, 576
CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #666; font-family: 'Montserrat', sans-serif; -webkit-font-smoothing: antialiased; }
.ad { width: 1920px; height: 576px; position: relative; overflow: hidden; background: #141110; margin: 20px auto; color: #fff; }
.ad > * { position: absolute; margin: 0; }
.ad p { margin: 0; }
.ad::after { content: ""; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: .18; mix-blend-mode: soft-light; background-image: GRAIN; }
.ph { overflow: hidden; } .ph img { width: 100%; height: 100%; object-fit: cover; display: block; }
.lock { left: 80px; top: 50%; transform: translateY(-50%); text-transform: uppercase; line-height: 1; }
.lock .k { font-size: 44px; font-weight: 400; letter-spacing: .06em; }
.ad .lock .s { font-size: 150px; font-weight: 300; letter-spacing: .02em; margin-top: 12px; }
.ad .lock .t { font-size: 44px; font-weight: 400; letter-spacing: .06em; margin-top: 18px; }
.ad .pill { display: inline-block; margin-top: 56px; font-size: 25px; font-weight: 500; letter-spacing: .01em; text-transform: none; padding: 18px 36px; border-radius: 999px; background: #F2B705; color: #141110; line-height: 1; }
.ad .more { display: block; margin-top: 34px; font-size: 21px; font-weight: 400; text-transform: none; letter-spacing: .04em; opacity: .85; }
.more::before { content: "⌄  "; }
.logo { right: 44px; top: 50%; transform: translateY(-50%) rotate(90deg); transform-origin: center; height: 48px; width: auto; }
.logo-k { filter: invert(1) brightness(.1); }
.dark .lock, .dark .more { color: #141110; }
.veil { inset: 0; background: linear-gradient(90deg, rgba(12,9,8,.82) 0%, rgba(12,9,8,.55) 34%, rgba(12,9,8,0) 62%); }
""".replace("GRAIN", GRAIN)

ads = []
def ad(id, body, cls="", note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad {cls}" id="{id}">{body}\n</section>')

def lock(dark=False, pill=True, more=True, size=150):
    return (f'<div class="lock"><p class="k">Колекція</p><p class="s" style="font-size:{size}px">Соло</p><p class="t">Шлях до себе</p>'
            + ('<p class="pill">Жіноча сила крізь десятиліття</p>' if pill else "") + ('<p class="more">Дізнатися першою</p>' if more else "") + '</div>')

def logo(dark=False):
    return f'<img class="logo{" logo-k" if dark else ""}" src="{LOGO_W}" alt="Obiimy">'

# A · one new frame to the edge: the polka-dot «Іскра» in the autumn street
ad("home-a-iskra", f'''
  <div class="ph" style="inset:0"><img src="{S2('iskra-65-4')}" alt="" style="object-position:62% 10%"></div>
  <div class="veil"></div>{lock()}{logo()}''', note="One frame: Iskra")

# B · the lock-up on dark and three frames of three prints
frames = [("krok-44-3", "50% 22%"), ("puls-44-4", "50% 30%"), ("zolote-44-2", "50% 34%")]
cells = "".join(f'<div class="ph" style="position:relative;flex:1;min-width:0"><img src="{S2(n)}" alt="" style="object-position:{p}"></div>' for n, p in frames)
ad("home-b-three", f'''
  <div style="left:0;top:0;bottom:0;width:760px;background:#141110"></div>
  <div style="left:760px;right:0;top:0;bottom:0;display:flex;gap:6px">{cells}</div>
  <div style="left:620px;top:0;bottom:0;width:200px;background:linear-gradient(90deg,#141110,rgba(20,17,16,0))"></div>
  {lock(size=140)}{logo()}''', note="Three prints")

# C · the seven scarves of the collection in a row on dark
cuts = "".join(f'<div style="display:grid;justify-items:center;gap:14px"><img src="{CUT(p["flat"])}" alt="" style="height:230px;width:auto;max-width:165px;object-fit:contain;filter:drop-shadow(0 22px 26px rgba(0,0,0,.5));transform:rotate({(-7,5,-4,6,-5,4,-6)[i]}deg)"><p style="font-size:16px;letter-spacing:.06em;text-transform:uppercase;color:#E9D7A6;white-space:nowrap">{p["name"]}</p></div>' for i, p in enumerate(P))
ad("home-c-seven", f'''
  <div style="inset:0;background:radial-gradient(80% 90% at 70% 50%,#2A2320,#141110 75%)"></div>
  <div style="left:640px;right:150px;top:0;bottom:0;display:flex;align-items:center;justify-content:space-between;gap:4px">{cuts}</div>
  {lock(size=140)}{logo()}''', note="Seven prints, seven states")

# D · the word «СОЛО» filled with silk, one square frame on the right
ad("home-d-type", f'''
  <div style="inset:0;background:#141110"></div>
  <div style="left:72px;top:50%;transform:translateY(-50%);text-transform:uppercase;line-height:1">
    <p style="font-size:44px;font-weight:400;letter-spacing:.06em">Колекція</p>
    <p style="font-size:330px;font-weight:300;letter-spacing:.02em;line-height:.9;margin-top:4px;background:url({HI(PP['iskra'])}) center/60% ;-webkit-background-clip:text;background-clip:text;color:transparent">Соло</p>
    <p style="font-size:44px;font-weight:400;letter-spacing:.06em;margin-top:10px">Шлях до себе</p></div>
  <div class="ph" style="left:1150px;top:0;bottom:0;width:620px"><img src="{S2('flirt-65-3')}" alt="" style="object-position:36% 30%"></div>
  <div style="left:1150px;top:0;bottom:0;width:140px;background:linear-gradient(90deg,#141110,rgba(20,17,16,0))"></div>
  <p class="pill" style="left:1150px;bottom:48px;margin:0">Жіноча сила крізь десятиліття</p>
  {logo()}''', note="Silk letters")

# E · two eras in one frame: a dimmed 1940s mood on the left, 2026 in colour on the right
ad("home-e-eras", f'''
  <div class="ph" style="left:0;top:0;bottom:0;width:50%"><img src="{S2('zolote-44-3')}" alt="" style="object-position:50% 25%;filter:grayscale(.85) contrast(1.08) brightness(.95)"></div>
  <div class="ph" style="left:50%;top:0;bottom:0;right:0"><img src="{S2('zolote-44-2')}" alt="" style="object-position:50% 36%"></div>
  <div style="inset:0;background:linear-gradient(90deg,rgba(12,9,8,.78) 0%,rgba(12,9,8,.45) 30%,rgba(12,9,8,.1) 50%,rgba(12,9,8,.1) 80%,rgba(12,9,8,.5) 100%)"></div>
  <p style="left:50%;top:40px;transform:translateX(-50%);font-size:22px;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap;color:#E9D7A6">1940-ві · 2026</p>
  {lock(size=140)}{logo()}''', note="Two eras")

# F · brand yellow with the scarf-and-twilly pair
ad("home-f-yellow", f'''
  <div style="inset:0;background:#F2B705"></div>
  <div class="ph" style="left:1040px;top:0;bottom:0;right:0"><img src="{S2('avantiura-88-5')}" alt="" style="object-position:62% 12%"></div>
  <div style="left:1040px;top:0;bottom:0;width:160px;background:linear-gradient(90deg,#F2B705,rgba(242,183,5,0))"></div>
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s" style="font-size:140px">Соло</p><p class="t">Шлях до себе</p>
    <p class="pill" style="background:#141110;color:#F2B705">Жіноча сила крізь десятиліття</p><p class="more" style="color:#141110">Дізнатися першою</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy">''', cls="dark", note="Brand yellow")

# G · the new close-up of «Авантюра» (studio, 16.10): a light banner — the curtain of the frame is continued to the left as a mirrored blur
RB = "src/reblum-avantiura-2k.webp"
ad("home-g-reblum-light", f'''
  <div class="ph" style="inset:0"><img src="{RB}" alt="" style="object-position:100% 38%;transform:scaleX(-1);filter:blur(28px) brightness(1.04) saturate(.8)"></div>
  <div style="inset:0;background:linear-gradient(90deg,rgba(236,228,218,.92) 0%,rgba(236,228,218,.7) 42%,rgba(236,228,218,0) 62%)"></div>
  <div class="ph" style="left:1000px;right:0;top:0;bottom:0;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 18%);mask-image:linear-gradient(90deg,transparent 0,#000 18%)"><img src="{RB}" alt="" style="object-position:50% 40%"></div>
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s" style="font-size:140px">Соло</p><p class="t">Шлях до себе</p>
    <p class="pill">Жіноча сила крізь десятиліття</p><p class="more" style="color:#141110">Дізнатися першою</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy">''', cls="dark", note="Reblum close-up, light")

# H · the same frame as a panel on dark
ad("home-h-reblum-dark", f'''
  <div style="inset:0;background:#141110"></div>
  <div class="ph" style="left:1060px;right:0;top:0;bottom:0"><img src="{RB}" alt="" style="object-position:50% 42%"></div>
  <div style="left:1060px;top:0;bottom:0;width:180px;background:linear-gradient(90deg,#141110,rgba(20,17,16,0))"></div>
  {lock(size=140)}{logo()}''', note="Reblum close-up, dark")

# I · the scarf knot to the edge: a horizontal band of the frame, the lock-up over a soft dark veil
ad("home-i-reblum-macro", f'''
  <div class="ph" style="inset:0"><img src="{RB}" alt="" style="width:150%;margin-left:-5%;object-position:50% 29%"></div>
  <div class="veil" style="background:linear-gradient(90deg,rgba(12,9,8,.78) 0%,rgba(12,9,8,.5) 32%,rgba(12,9,8,0) 56%)"></div>
  {lock(size=140)}{logo()}''', note="Reblum macro")

# J · split in two: the frame on the left, the lock-up centred on dark on the right
ad("home-j-split", f'''
  <div class="ph" style="left:0;top:0;bottom:0;width:50%"><img src="{S2('tysha-88-2')}" alt="" style="object-position:50% 40%"></div>
  <div style="left:50%;right:0;top:0;bottom:0;background:#141110"></div>
  <div style="left:46%;top:0;bottom:0;width:8%;background:linear-gradient(90deg,rgba(20,17,16,0),#141110)"></div>
  <div class="lock" style="left:50%;right:200px;transform:translate(0,-50%);text-align:center;padding-left:60px"><p class="k">Колекція</p><p class="s" style="font-size:150px">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дізнатися першою</p></div>
  {logo()}''', note="Split, centred")

# K · the lock-up in one line above a strip of four frames
strip = [("iskra-65-4", "50% 12%"), ("flirt-tw-1", "50% 30%"), ("zolote-44-2", "50% 32%"), ("krok-44-3", "50% 20%")]
scells = "".join(f'<div class="ph" style="position:relative;flex:1;min-width:0"><img src="{S2(n)}" alt="" style="object-position:{p}"></div>' for n, p in strip)
ad("home-k-strip", f'''
  <div style="inset:0;background:#141110"></div>
  <div style="left:80px;right:160px;top:40px;height:110px;display:flex;align-items:center;gap:34px;text-transform:uppercase;white-space:nowrap">
    <p style="font-size:34px;font-weight:400;letter-spacing:.08em">Колекція</p><p style="font-size:96px;font-weight:300;letter-spacing:.02em;line-height:.9">Соло</p><p style="font-size:34px;font-weight:400;letter-spacing:.08em">Шлях до себе</p>
    <p class="pill" style="margin:0 0 0 auto;font-size:22px;padding:14px 28px;align-self:center">Жіноча сила крізь десятиліття</p></div>
  <div style="left:80px;right:160px;top:180px;bottom:0;display:flex;gap:6px">{scells}</div>
  {logo()}''', note="One-line lock-up, strip of four")

# M · paper and the flat scarf: product first
ad("home-m-paper", f'''
  <div style="inset:0;background:#F1E8D8"></div>
  <img src="{CUT('avantiura-88-1')}" alt="" style="left:1120px;top:50%;transform:translateY(-50%) rotate(-8deg);height:520px;width:auto;filter:drop-shadow(0 30px 40px rgba(60,30,10,.35))">
  <img src="{CUT('iskra-65-1')}" alt="" style="left:1420px;top:50%;transform:translateY(-44%) rotate(7deg);height:440px;width:auto;filter:drop-shadow(0 30px 40px rgba(60,30,10,.3))">
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s" style="font-size:140px">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more" style="color:#141110">Дізнатися першою</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy">''', cls="dark", note="Paper and scarves")

# N · seven states as words on dark silk
states = "".join(f'<p style="font-size:28px;font-weight:300;letter-spacing:.1em;text-transform:uppercase;padding:13px 0;border-bottom:1px solid rgba(243,234,219,.22);display:flex;justify-content:space-between;align-items:baseline;gap:40px"><span>{p["name"]}</span><span style="opacity:.75;font-size:21px;letter-spacing:.02em;text-transform:none;white-space:nowrap">{p["short"]}</span></p>' for p in P)
ad("home-n-states", f'''
  <div style="inset:0;background:url({HI(PP['tysha'])}) center/140%"></div>
  <div style="inset:0;background:rgba(14,12,11,.82)"></div>
  <div style="left:1000px;right:190px;top:50%;transform:translateY(-50%)">{states}</div>
  {lock(size=140)}{logo()}''', note="Seven states as words")

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · SOLO home banners</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / "home.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "home banners")
