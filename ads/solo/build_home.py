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
.lock .k { font-size: 44px; font-weight: 400; letter-spacing: .04em; }
.ad .lock .s { font-size: 150px; font-weight: 300; letter-spacing: 0; margin-top: 14px; margin-left: -8px; }
.ad .lock .t { font-size: 44px; font-weight: 400; letter-spacing: .04em; margin-top: 6px; }
.ad .pill { display: inline-block; margin-top: 40px; font-size: 24px; font-weight: 500; letter-spacing: .01em; text-transform: none; padding: 18px 30px; border-radius: 999px; background: #F2B705; color: #141110; line-height: 1; }
.ad .more { display: flex; align-items: center; gap: 12px; margin-top: 28px; font-size: 23px; font-weight: 400; text-transform: none; letter-spacing: .02em; }
.ad .more::before { content: ""; width: 9px; height: 9px; border-right: 1.5px solid #F2B705; border-bottom: 1.5px solid #F2B705; transform: rotate(45deg) translateY(-3px); flex: none; }
.ad .lock .cap { margin-top: 28px; font-size: 15px; letter-spacing: .16em; text-transform: uppercase; color: #6B655C; }
.logo { right: 0; top: 50%; height: 64px; width: auto; transform: translate(calc(50% - 80px), -50%) rotate(90deg); transform-origin: center; }
.tm { right: 73px; top: calc(50% + 164px); font-size: 14px; font-weight: 500; line-height: 1; color: #fff; }
.logo-k { filter: invert(1) brightness(.1); }
.dark .lock { color: #141110; } .dark .more { color: #3A3530; } .dark .more::before { border-color: #141110; } .dark .tm { color: #141110; }
.scrim-d { right: 0; top: 0; bottom: 0; width: 200px; background: linear-gradient(270deg, rgba(20,17,16,.7), rgba(20,17,16,0)); }
.scrim-l { right: 0; top: 0; bottom: 0; width: 220px; background: linear-gradient(270deg, rgba(240,235,225,.88), rgba(240,235,225,0)); }
.veil { inset: 0; background: linear-gradient(90deg, rgba(12,9,8,.82) 0%, rgba(12,9,8,.55) 34%, rgba(12,9,8,0) 62%); }
""".replace("GRAIN", GRAIN)

ads = []
def ad(id, body, cls="", note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad {cls}" id="{id}">{body}\n</section>')

def lock(dark=False, pill=True, more=True, size=150):
    return (f'<div class="lock"><p class="k">Колекція</p><p class="s" style="font-size:{size}px">Соло</p><p class="t">Шлях до себе</p>'
            + ('<p class="pill">Жіноча сила крізь десятиліття</p>' if pill else "") + ('<p class="more">Дізнатися першою</p>' if more else "") + '</div>')

def logo(dark=False):
    return f'<img class="logo{" logo-k" if dark else ""}" src="{LOGO_W}" alt="Obiimy"><span class="tm">™</span>'

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
  {lock()}{logo()}''', note="Three prints")

# C · the seven scarves of the collection in a row on dark
cuts = "".join(f'<div style="display:grid;justify-items:center;gap:14px"><img src="{CUT(p["flat"])}" alt="" style="height:230px;width:auto;max-width:165px;object-fit:contain;filter:drop-shadow(0 22px 26px rgba(0,0,0,.5));transform:rotate({(-7,5,-4,6,-5,4,-6)[i]}deg)"><p style="font-size:16px;letter-spacing:.06em;text-transform:uppercase;color:#E9D7A6;white-space:nowrap">{p["name"]}</p></div>' for i, p in enumerate(P))
ad("home-c-seven", f'''
  <div style="inset:0;background:radial-gradient(80% 90% at 70% 50%,#2A2320,#141110 75%)"></div>
  <div style="left:640px;right:150px;top:0;bottom:0;display:flex;align-items:center;justify-content:space-between;gap:4px">{cuts}</div>
  {lock()}{logo()}''', note="Seven prints, seven states")

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
  {lock()}{logo()}''', note="Two eras")

# F · brand yellow with the scarf-and-twilly pair
ad("home-f-yellow", f'''
  <div style="inset:0;background:#F2B705"></div>
  <div class="ph" style="left:1080px;top:0;bottom:0;right:0"><img src="{S2('avantiura-88-5')}" alt="" style="object-position:55% 12%"></div>
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p>
    <p class="pill" style="background:transparent;border:2px solid #141110;color:#141110">Жіноча сила крізь десятиліття</p><p class="more">Дізнатися першою</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Brand yellow")

# G · the new close-up of «Авантюра» (studio, 16.10): a light banner — the curtain of the frame is continued to the left as a mirrored blur
RB = "src/reblum-avantiura-2k.webp"
ad("home-g-reblum-light", f'''
  <div class="ph" style="inset:0"><img src="{RB}" alt="" style="object-position:100% 38%;transform:scaleX(-1);filter:blur(56px) brightness(1.06) saturate(.5)"></div>
  <div style="inset:0;background:linear-gradient(90deg,rgba(239,234,226,.96) 0%,rgba(239,234,226,.82) 48%,rgba(239,234,226,.1) 66%)"></div>
  <div class="ph" style="left:1000px;right:0;top:0;bottom:0;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 18%);mask-image:linear-gradient(90deg,transparent 0,#000 18%)"><img src="{RB}" alt="" style="object-position:50% 40%"></div>
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p>
    <p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дізнатися першою</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Reblum close-up, light")

# H · the same frame as a panel on dark
ad("home-h-reblum-dark", f'''
  <div style="inset:0;background:#141110"></div>
  <div class="ph" style="left:880px;right:0;top:0;bottom:0"><img src="{RB}" alt="" style="object-position:40% 36%"></div>
  <div style="left:880px;top:0;bottom:0;width:160px;background:linear-gradient(90deg,#1A1816,rgba(26,24,22,0))"></div><div class="scrim-d"></div>
  {lock()}{logo()}''', note="Reblum close-up, dark")

# I · the scarf knot to the edge: a horizontal band of the frame, the lock-up over a soft dark veil
ad("home-i-reblum-macro", f'''
  <div class="ph" style="inset:0"><img src="{RB}" alt="" style="width:150%;margin-left:-5%;object-position:50% 29%"></div>
  <div class="veil" style="background:linear-gradient(90deg,rgba(12,9,8,.78) 0%,rgba(12,9,8,.5) 32%,rgba(12,9,8,0) 56%)"></div>
  {lock()}{logo()}''', note="Reblum macro")

# J · split in two: the frame on the left, the lock-up centred on dark on the right
ad("home-j-split", f'''
  <div class="ph" style="left:0;top:0;bottom:0;width:50%"><img src="{S2('tysha-88-2')}" alt="" style="object-position:50% 40%"></div>
  <div style="left:50%;right:0;top:0;bottom:0;background:#141110"></div>
  <div style="left:46%;top:0;bottom:0;width:8%;background:linear-gradient(90deg,rgba(20,17,16,0),#141110)"></div>
  <div class="lock" style="left:1060px;right:200px;transform:translate(0,-50%)"><p class="k">Колекція</p><p class="s" style="font-size:150px">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дізнатися першою</p></div>
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
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дізнатися першою</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Paper and scarves")

# N · seven states as words on dark silk
states = "".join(f'<p style="font-size:28px;font-weight:300;letter-spacing:.1em;text-transform:uppercase;padding:13px 0;border-bottom:1px solid rgba(243,234,219,.22);display:flex;justify-content:space-between;align-items:baseline;gap:40px"><span>{p["name"]}</span><span style="opacity:.75;font-size:21px;letter-spacing:.02em;text-transform:none;white-space:nowrap">{p["short"]}</span></p>' for p in P)
ad("home-n-states", f'''
  <div style="inset:0;background:url({HI(PP['tysha'])}) center/140%"></div>
  <div style="inset:0;background:rgba(14,12,11,.82)"></div>
  <div style="left:1000px;right:190px;top:50%;transform:translateY(-50%)">{states}</div>
  {lock()}{logo()}''', note="Seven states as words")

# more on the studio close-up (16.10)
# O · the photo mirrored to the left: the knot in the centre, the lock-up on the left over the shirt
ad("home-o-reblum-wide", f'''
  <div class="ph" style="left:0;top:0;bottom:0;width:50%"><img src="{RB}" alt="" style="object-position:0% 40%;transform:scaleX(-1);filter:blur(18px) brightness(.9)"></div>
  <div class="ph" style="left:50%;right:0;top:0;bottom:0"><img src="{RB}" alt="" style="object-position:0% 40%"></div>
  <div class="ph" style="left:40%;top:0;bottom:0;width:10%"><img src="{RB}" alt="" style="object-position:0% 40%;transform:scaleX(-1);filter:blur(18px) brightness(.9);-webkit-mask-image:linear-gradient(90deg,#000,transparent);mask-image:linear-gradient(90deg,#000,transparent)"></div>
  <div style="inset:0;background:linear-gradient(90deg,rgba(12,9,8,.86) 0%,rgba(12,9,8,.6) 30%,rgba(12,9,8,0) 52%)"></div>
  {lock()}{logo()}''', note="Reblum wide, mirrored fill")

# P · brand yellow panel on the left, the knot large on the right, the pill becomes a dark one
ad("home-p-reblum-yellow", f'''
  <div style="inset:0;background:#F2B705"></div>
  <div class="ph" style="left:860px;right:0;top:0;bottom:0"><img src="{RB}" alt="" style="object-position:55% 40%"></div>
  <div style="left:860px;top:0;bottom:0;width:120px;background:linear-gradient(90deg,#F2B705,rgba(242,183,5,0))"></div>
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill" style="background:#141110;color:#F2B705">Жіноча сила крізь десятиліття</p><p class="more">Дізнатися першою</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Reblum on yellow")

# Q · the knot as a tall slice in the middle between two dark fields: lock-up left, seven state words right
words = "".join(f'<p style="font-size:26px;font-weight:300;letter-spacing:.12em;text-transform:uppercase;padding:9px 0;opacity:{1 if p["id"] == "avantiura" else .55}">{p["name"]}</p>' for p in P)
ad("home-q-reblum-slice", f'''
  <div style="inset:0;background:#141110"></div>
  <div class="ph" style="left:760px;top:0;bottom:0;width:640px"><img src="{RB}" alt="" style="object-position:50% 42%"></div>
  <div style="left:1440px;top:50%;transform:translateY(-50%)">{words}</div>
  {lock()}{logo()}''', note="Reblum slice with states")

# R · light paper, the photo as a soft-edged frame on the right, print name as a caption
ad("home-r-reblum-paper", f'''
  <div style="inset:0;background:#F0EBE1"></div>
  <div class="ph" style="left:1000px;right:0;top:0;bottom:0;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 22%);mask-image:linear-gradient(90deg,transparent 0,#000 22%)"><img src="{RB}" alt="" style="object-position:50% 40%"></div>
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дізнатися першою</p><p class="cap">Хустка «Авантюра»</p></div>
  <div class="scrim-l"></div><img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Reblum on paper")

# S · wind: the scarf in motion to the edge, text over a gradient only (as the reference)
ad("home-s-wind", f'''
  <div class="ph" style="inset:0"><img src="{S2('avantiura-88-3')}" alt="" style="object-position:70% 18%"></div>
  <div style="inset:0;background:linear-gradient(90deg,rgba(12,9,8,.72) 0%,rgba(12,9,8,.45) 24%,rgba(12,9,8,0) 40%)"></div>
  {lock()}{logo()}''', note="Wind: scarf in motion")

# T · silk as the background: the folds of one print to the full frame, no person
ad("home-t-silk", f'''
  <div style="inset:0;background:url({HI(PP['zolote'])}) 50% 45%/125%"></div>
  <div style="inset:0;background:linear-gradient(90deg,rgba(12,9,8,.7) 0%,rgba(12,9,8,.4) 30%,rgba(12,9,8,.08) 55%)"></div>
  <div class="lock"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill" style="background:#1A1816;color:#F2B705">Жіноча сила крізь десятиліття</p><p class="more">Дізнатися першою</p></div>
  {logo()}''', note="Silk folds as the background")

# U · diptych of one woman: portrait left, the knot right, the lock-up on a dark strip between
ad("home-u-diptych", f'''
  <div class="ph" style="left:0;top:0;bottom:0;width:640px"><img src="{S2('tysha-88-2')}" alt="" style="object-position:62% 30%"></div>
  <div style="left:640px;top:0;bottom:0;width:640px;background:#141110"></div>
  <div class="ph" style="left:1280px;top:0;bottom:0;right:0"><img src="{S2('tysha-88-3')}" alt="" style="object-position:50% 55%"></div>
  <div class="lock" style="left:700px;right:760px;transform:translate(0,-50%)"><p class="k">Колекція</p><p class="s" style="font-size:130px">Соло</p><p class="t">Шлях до себе</p><p class="pill" style="font-size:22px;padding:16px 26px">Жіноча сила крізь десятиліття</p><p class="more">Дізнатися першою</p></div>
  <img class="logo" src="{LOGO_W}" alt="Obiimy" style="right:auto;left:980px;transform:translate(calc(50% - 80px),-50%) rotate(90deg)"><span class="tm" style="right:auto;left:1193px">™</span>''', note="Diptych of one woman")

# V · seven prints as seven vertical strips of real silk on the right, the lock-up on dark on the left
strips = "".join(f'<div style="flex:1;background:url({HI(p)}) {(37 * i) % 100}% 50%/{520}px;"></div>' for i, p in enumerate(P))
ad("home-v-strips", f'''
  <div style="inset:0;background:#141110"></div>
  <div style="left:800px;right:0;top:0;bottom:0;display:flex">{strips}</div>
  <div style="left:800px;top:0;bottom:0;width:140px;background:linear-gradient(90deg,#141110,rgba(20,17,16,0))"></div>
  {lock()}{logo()}''', note="Seven prints as strips")

# round 3 (16.10): three compositions on other frames — a dark portrait, a warm street, a classic knot
# W · «Золоте світло» at the door: dark frame to the edge, the lock-up on the left, the scarf at the throat lit
ad("home-w-door", f'''
  <div style="inset:0;background:#1A1816"></div>
  <div class="ph" style="left:700px;right:0;top:0;bottom:0"><img src="{S2('zolote-44-3')}" alt="" style="object-position:78% 18%"></div>
  <div style="left:700px;top:0;bottom:0;width:260px;background:linear-gradient(90deg,#1A1816,rgba(26,24,22,0))"></div>
  {lock()}{logo()}''', note="Zolote at the door")

# X · «Пульс» at the café: a warm street frame to the right, paper panel with the lock-up
ad("home-x-cafe", f'''
  <div style="inset:0;background:#F0EBE1"></div>
  <div class="ph" style="left:790px;right:0;top:0;bottom:0;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 16%);mask-image:linear-gradient(90deg,transparent 0,#000 16%)"><img src="{S2('puls-44-5')}" alt="" style="object-position:62% 45%"></div>
  <div class="scrim-l"></div><div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дізнатися першою</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Puls at the café")

# Y · «Сміливий крок» classic knot: the frame centred, two dark fields, the lock-up left and the state right
ad("home-y-knot", f'''
  <div style="inset:0;background:#141110"></div>
  <div class="ph" style="left:700px;top:0;bottom:0;width:640px"><img src="{S2('krok-44-2')}" alt="" style="object-position:50% 22%"></div>
  <div style="left:1420px;top:50%;transform:translateY(-50%);width:260px;color:#F3EADB"><p style="font-size:18px;letter-spacing:.18em;text-transform:uppercase;opacity:.7">Хустка</p><p style="font-size:40px;font-weight:300;letter-spacing:.02em;line-height:1.05;margin-top:10px">Сміливий крок</p><p style="font-size:22px;line-height:1.3;margin-top:16px;opacity:.85">{PP["krok"]["short"]}</p></div>
  {lock()}{logo()}''', note="Krok knot, print card")

# round 3, the art director's four: monochrome + yellow, the arch, the diagonal seam, the album print
ad("home-z1-mono", f'''
  <div style="inset:0;background:#111"></div>
  <div class="ph" style="left:520px;right:0;top:0;bottom:0"><img src="{S2('tysha-88-2')}" alt="" style="object-position:30% 36%;filter:grayscale(1) contrast(1.1)"></div>
  <div style="left:520px;top:0;bottom:0;width:220px;background:linear-gradient(90deg,#111,rgba(17,17,17,0))"></div>
  <div style="right:0;top:0;bottom:0;width:220px;background:linear-gradient(270deg,rgba(17,17,17,.65),rgba(17,17,17,0))"></div>
  {lock()}{logo()}''', note="Monochrome + yellow")

ad("home-z2-arch", f'''
  <div style="inset:0;background:#1A1816"></div>
  <div class="ph" style="left:1020px;top:36px;width:600px;height:600px;border-radius:300px 300px 0 0"><img src="{S2('krok-44-2')}" alt="" style="object-position:50% 40%;transform:scale(1.12);transform-origin:50% 100%"></div>
  {lock()}{logo()}''', note="The arch")

ad("home-z3-diag", f'''
  <div class="ph" style="left:1000px;right:0;top:0;bottom:0"><img src="{S2('puls-44-4')}" alt="" style="object-position:54% 0%"></div>
  <div style="left:0;top:0;bottom:0;width:1060px;background:#1A1816;clip-path:polygon(0 0,930px 0,1060px 100%,0 100%)"></div><div class="scrim-d" style="width:180px;opacity:.85"></div>
  {lock()}{logo()}''', note="Diagonal seam")

ad("home-z4-album", f'''
  <div style="inset:0;background:#F0EBE1"></div>
  <div style="left:960px;top:54px;width:700px;height:462px;background:#fff;padding:14px;box-shadow:0 12px 32px rgba(60,40,20,.18)"><div class="ph" style="position:relative;width:100%;height:100%"><img src="{S2('iskra-65-4')}" alt="" style="object-position:50% 22%"></div></div>
  <p style="left:960px;top:536px;font-size:15px;letter-spacing:.16em;text-transform:uppercase;color:#6B655C">Хустка «Іскра»</p>
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дізнатися першою</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Album print")

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · SOLO home banners</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / "home.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "home banners")
