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
.ad .more { display: flex; width: max-content; align-items: center; gap: 14px; margin-top: 20px; font-size: 24px; font-weight: 500; text-transform: none; letter-spacing: .02em; padding: 15px 28px 15px 30px; border: 1.5px solid rgba(243,234,219,.85); border-radius: 999px; color: #F3EADB; }
.ad .more::after { content: "→"; font-family: Montserrat, sans-serif; font-weight: 400; font-size: 26px; line-height: 1; transform: translateY(-1px); }
.ad .lock .cap { margin-top: 28px; font-size: 15px; letter-spacing: .16em; text-transform: uppercase; color: #6B655C; }
.logo { right: 0; top: 50%; height: 64px; width: auto; transform: translate(calc(50% - 80px), -50%) rotate(90deg); transform-origin: center; }
.tm { right: 73px; top: calc(50% + 164px); font-size: 14px; font-weight: 500; line-height: 1; color: #fff; }
.logo-k { filter: invert(1) brightness(.1); }
.dark .lock { color: #141110; } .dark .more { color: #141110; border-color: rgba(20,17,16,.7); } .dark .tm { color: #141110; }
.scrim-d { right: 0; top: 0; bottom: 0; width: 200px; background: linear-gradient(270deg, rgba(20,17,16,.7), rgba(20,17,16,0)); }
.scrim-l { right: 0; top: 0; bottom: 0; width: 220px; background: linear-gradient(270deg, rgba(240,235,225,.88), rgba(240,235,225,0)); }
.veil { inset: 0; background: linear-gradient(90deg, rgba(12,9,8,.82) 0%, rgba(12,9,8,.55) 34%, rgba(12,9,8,0) 62%); }
""".replace("GRAIN", GRAIN)

ads = []
import re as _re
def ad(id, body, cls="", note=""):
    # 27.10, the client: no print caption under the lock-up, and no OBIIMY™ on the banner — the site's header already carries the logo
    body = _re.sub(r'<p class="cap">.*?</p>', "", body, flags=_re.S)
    body = _re.sub(r'<img class="logo[^>]*>(<span class="tm"[^>]*>™</span>)?', "", body)
    ads.append(f'\n<!-- {note} -->\n<section class="ad {cls}" id="{id}">{body}\n</section>')

def lock(dark=False, pill=True, more=True, size=150):
    return (f'<div class="lock"><p class="k">Колекція</p><p class="s" style="font-size:{size}px">Соло</p><p class="t">Шлях до себе</p>'
            + ('<p class="pill">Жіноча сила крізь десятиліття</p>' if pill else "") + ('<p class="more">Дивитися колекцію</p>' if more else "") + '</div>')

def logo(dark=False):
    return ""      # the logo is no longer placed on the banners (27.10)

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
cuts = "".join(f'<div style="display:grid;justify-items:center;gap:14px"><img src="{CUT(p["flat"])}" alt="" style="height:230px;width:auto;max-width:165px;object-fit:contain;filter:drop-shadow(0 22px 26px rgba(0,0,0,.5));transform:rotate({(-7,5,-4,6,-5,4,-6)[i]}deg)"><p style="font-size:16px;letter-spacing:.06em;text-transform:uppercase;color:#E9D7A6;text-align:center;line-height:1.2;max-width:150px">{p["name"]}</p></div>' for i, p in enumerate(P))
ad("home-c-seven", f'''
  <div style="inset:0;background:radial-gradient(80% 90% at 70% 50%,#2A2320,#141110 75%)"></div>
  <div style="left:620px;right:190px;top:0;bottom:0;display:flex;align-items:center;justify-content:space-between;gap:4px">{cuts}</div>
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
    <p class="pill" style="background:transparent;border:2px solid #141110;color:#141110">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Brand yellow")

# G · the new close-up of «Авантюра» (studio, 16.10): a light banner — the curtain of the frame is continued to the left as a mirrored blur
RB = "src/reblum-avantiura-2k.webp"
ad("home-g-reblum-light", f'''
  <div class="ph" style="inset:0"><img src="{RB}" alt="" style="object-position:100% 38%;transform:scaleX(-1);filter:blur(56px) brightness(1.06) saturate(.5)"></div>
  <div style="inset:0;background:linear-gradient(90deg,rgba(239,234,226,.96) 0%,rgba(239,234,226,.82) 48%,rgba(239,234,226,.1) 66%)"></div>
  <div class="ph" style="left:1000px;right:0;top:0;bottom:0;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 18%);mask-image:linear-gradient(90deg,transparent 0,#000 18%)"><img src="{RB}" alt="" style="object-position:50% 40%"></div>
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p>
    <p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
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
  <div class="lock" style="left:1060px;right:200px;transform:translate(0,-50%)"><p class="k">Колекція</p><p class="s" style="font-size:150px">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
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
  <img src="{CUT('avantiura-88-1')}" alt="" style="left:940px;top:50%;transform:translateY(-50%) rotate(-8deg);height:500px;width:auto;filter:drop-shadow(0 30px 40px rgba(60,30,10,.35))">
  <img src="{CUT('iskra-65-1')}" alt="" style="left:1220px;top:50%;transform:translateY(-44%) rotate(7deg);height:420px;width:auto;filter:drop-shadow(0 30px 40px rgba(60,30,10,.3))">
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
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
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill" style="background:#141110;color:#F2B705">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
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
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p><p class="cap">Хустка «Авантюра»</p></div>
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
  <div class="lock"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill" style="background:#1A1816;color:#F2B705">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
  {logo()}''', note="Silk folds as the background")

# U · diptych of one woman: portrait left, the knot right, the lock-up on a dark strip between
ad("home-u-diptych", f'''
  <div class="ph" style="left:0;top:0;bottom:0;width:640px"><img src="{S2('tysha-88-2')}" alt="" style="object-position:62% 30%"></div>
  <div style="left:640px;top:0;bottom:0;width:640px;background:#141110"></div>
  <div class="ph" style="left:1280px;top:0;bottom:0;right:0"><img src="{S2('tysha-88-3')}" alt="" style="object-position:50% 55%"></div>
  <div class="lock" style="left:700px;right:760px;transform:translate(0,-50%)"><p class="k">Колекція</p><p class="s" style="font-size:130px">Соло</p><p class="t">Шлях до себе</p><p class="pill" style="font-size:22px;padding:16px 26px">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
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
  <div class="scrim-l"></div><div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
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
  
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Album print")

# round 4 (16.10): four with a different move — a twilly story, the empty seat, a split-tone portrait, the Riviera with the sea on the right
# V1 · twilly: the bag frame to the right, the lock-up left, the twilly as the hero of the frame
ad("home-v1-twilly", f'''
  <div style="inset:0;background:#1A1816"></div>
  <div class="ph" style="left:780px;right:0;top:0;bottom:0"><img src="{S2('iskra-tw-3')}" alt="" style="object-position:50% 48%"></div>
  <div style="left:780px;top:0;bottom:0;width:200px;background:linear-gradient(90deg,#1A1816,rgba(26,24,22,0))"></div><div class="scrim-d"></div>
  {lock()}{logo()}''', note="Twilly on the bag")

# V2 · the empty seat: the car interior with the twilly on the bag — no model, a quiet still life; lock-up on a dark panel
ad("home-v2-seat", f'''
  <div style="inset:0;background:#1A1816"></div>
  <div class="ph" style="left:720px;right:0;top:0;bottom:0"><img src="{S2('tysha-tw-2')}" alt="" style="object-position:40% 55%"></div>
  <div style="left:720px;top:0;bottom:0;width:220px;background:linear-gradient(90deg,#1A1816,rgba(26,24,22,0))"></div><div class="scrim-d"></div>
  {lock()}{logo()}''', note="The empty seat")

# V3 · Riviera: the terrace frame to the right, the sea in the far right under the logo; paper panel
ad("home-v3-riviera", f'''
  <div style="inset:0;background:#F0EBE1"></div>
  <div class="ph" style="left:760px;right:0;top:0;bottom:0;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 14%);mask-image:linear-gradient(90deg,transparent 0,#000 14%)"><img src="{S2('zolote-tw-2')}" alt="" style="object-position:40% 72%"></div>
  <div class="scrim-l"></div><div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Riviera")

# V4 · the look in two tones: the «Флірт» frame, the left half warmed and darkened under the lock-up, the right half as shot
ad("home-v4-tone", f'''
  <div class="ph" style="inset:0"><img src="{S2('flirt-65-3')}" alt="" style="object-position:70% 22%"></div>
  <div style="left:0;top:0;bottom:0;width:980px;background:rgba(26,24,22,.86);-webkit-mask-image:linear-gradient(90deg,#000 70%,transparent);mask-image:linear-gradient(90deg,#000 70%,transparent)"></div>
  <div class="scrim-d"></div>{lock()}{logo()}''', note="Two tones")

# round 5 (16.10): more on the studio close-up — six different moves
# S1 · the knot centred, mirrored symmetry: the same frame on both sides, the lock-up on a dark centre strip
ad("home-s1-mirror", f'''
  <div class="ph" style="left:0;top:0;bottom:0;width:640px"><img src="{RB}" alt="" style="object-position:60% 40%;transform:scaleX(-1)"></div>
  <div style="left:640px;top:0;bottom:0;width:640px;background:#141110"></div>
  <div class="ph" style="left:1280px;top:0;bottom:0;right:0"><img src="{RB}" alt="" style="object-position:60% 40%"></div>
  <div class="lock" style="left:700px;right:760px;transform:translate(0,-50%)"><p class="k">Колекція</p><p class="s" style="font-size:130px">Соло</p><p class="t">Шлях до себе</p><p class="pill" style="font-size:22px;padding:16px 26px">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
  <img class="logo" src="{LOGO_W}" alt="Obiimy" style="right:auto;left:980px;transform:translate(calc(50% - 80px),-50%) rotate(90deg)"><span class="tm" style="right:auto;left:1193px">™</span>''', note="Studio: mirror")

# S2 · red field: the print's own red (#B3121B) as the panel, white lock-up, the knot to the right
ad("home-s2-red", f'''
  <div style="inset:0;background:#B3121B"></div>
  <div class="ph" style="left:1040px;right:0;top:0;bottom:0"><img src="{RB}" alt="" style="object-position:50% 36%"></div>
  <div style="left:1040px;top:0;bottom:0;width:140px;background:linear-gradient(90deg,#B3121B,rgba(179,18,27,0))"></div><div class="scrim-d"></div>
  <div class="lock"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill" style="background:#141110;color:#F2B705">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>{logo()}''', note="Studio: red field")

# S3 · the hand and the knot only: a tight crop of the fingers at the knot across the right two thirds, dark gradient left
ad("home-s3-hand", f'''
  <div class="ph" style="inset:0"><img src="{RB}" alt="" style="object-position:38% 30%;transform:scale(1.35);transform-origin:38% 30%"></div>
  <div style="inset:0;background:linear-gradient(90deg,rgba(12,9,8,.86) 0%,rgba(12,9,8,.6) 32%,rgba(12,9,8,0) 56%)"></div><div class="scrim-d"></div>
  {lock()}{logo()}''', note="Studio: the hand")

# S4 · the frame in a tall rounded window on paper, the lock-up left, a print caption
ad("home-s4-window", f'''
  <div style="inset:0;background:#F0EBE1"></div>
  <div class="ph" style="left:1060px;top:40px;width:560px;height:496px;border-radius:280px"><img src="{RB}" alt="" style="object-position:50% 40%"></div>
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p><p class="cap">Хустка «Авантюра» · 88 × 88</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Studio: window on paper")

# S5 · the knot as a vertical strip between two dark fields, a wide quiet composition with air
ad("home-s5-strip", f'''
  <div style="inset:0;background:#1A1816"></div>
  <div class="ph" style="left:820px;top:0;bottom:0;width:520px"><img src="{RB}" alt="" style="object-position:50% 40%"></div>
  <div style="left:1420px;top:50%;transform:translateY(-50%);width:260px;color:#F3EADB"><p style="font-size:18px;letter-spacing:.18em;text-transform:uppercase;opacity:.7">Хустка</p><p style="font-size:40px;font-weight:300;letter-spacing:.02em;line-height:1.05;margin-top:10px">Авантюра</p><p style="font-size:22px;line-height:1.3;margin-top:16px;opacity:.85">{PP["avantiura"]["short"]}</p></div>
  {lock()}{logo()}''', note="Studio: strip with card")

# S6 · light: the frame to the full width, the curtain side warmed, the lock-up dark on the light part
ad("home-s6-light", f'''
  <div class="ph" style="inset:0"><img src="{RB}" alt="" style="object-position:100% 40%;transform:scaleX(-1)"></div>
  <div style="inset:0;background:linear-gradient(90deg,rgba(240,235,225,.94) 0%,rgba(240,235,225,.8) 36%,rgba(240,235,225,0) 58%)"></div><div class="scrim-l"></div>
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Studio: light mirrored")

# round 6 (19.10): six on frames the banners had not used yet
# N1 · the pair: dark field with the lock-up, two portrait panels — the white suit with «Іскра» and the black blazer with «Авантюра»
ad("home-n1-pair", f'''
  <div style="inset:0;background:#141110"></div>
  <div class="ph" style="left:820px;top:0;bottom:0;width:470px"><img src="{S2('iskra-65-2')}" alt="" style="object-position:50% 18%"></div>
  <div class="ph" style="left:1302px;top:0;bottom:0;width:470px"><img src="{S2('avantiura-tw-1')}" alt="" style="object-position:50% 14%"></div>
  <div style="left:820px;top:0;bottom:0;width:120px;background:linear-gradient(90deg,#141110,rgba(20,17,16,0))"></div>
  {lock()}{logo()}''', note="Pair: white and black")

# N2 · the white suit on the morning street: full bleed, light veil on the left, the dark lock-up
ad("home-n2-white", f'''
  <div class="ph" style="inset:0"><img src="{S2('iskra-65-2')}" alt="" style="object-position:62% 31%"></div>
  <div style="inset:0;background:linear-gradient(90deg,rgba(240,235,225,.94) 0%,rgba(240,235,225,.8) 34%,rgba(240,235,225,0) 60%)"></div><div class="scrim-l"></div>
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="White suit, light")

# N3 · seven twillies fanned on the dark field: the collection as an object
def _twcut(p):
    tw = p["tw"]
    return tw if (HERE / f"src/{tw}-cut.webp").exists() else tw[:-1] + "1"
fan = "".join(f'<img src="{CUT(_twcut(p))}" alt="" style="left:{640 + i * 100}px;top:50%;height:560px;width:auto;transform:translateY(-50%) rotate({-22 + i * 7}deg);transform-origin:50% 85%;filter:drop-shadow(0 24px 30px rgba(0,0,0,.55))">' for i, p in enumerate(P))
ad("home-n3-fan", f'''
  <div style="inset:0;background:radial-gradient(70% 90% at 72% 50%,#2A2320,#141110 75%)"></div>
  {fan}
  <div style="left:1680px;top:0;bottom:0;width:240px;background:linear-gradient(270deg,rgba(20,17,16,.85),rgba(20,17,16,0))"></div>
  {lock()}{logo()}''', note="Seven twillies fanned")

# N4 · from the back: the red twilly in the hair on the Paris street, warm veil, white lock-up
ad("home-n4-back", f'''
  <div class="ph" style="inset:0"><img src="{S2('avantiura-tw-3')}" alt="" style="object-position:58% 22%"></div>
  <div class="veil"></div><div class="scrim-d"></div>
  {lock()}{logo()}''', note="Back, twilly in the hair")

# N5 · the still life: the blue bag and the polka-dot scarf on the café table, paper panel with the lock-up
ad("home-n5-table", f'''
  <div style="inset:0;background:#F0EBE1"></div>
  <div class="ph" style="left:860px;right:0;top:0;bottom:0;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 18%);mask-image:linear-gradient(90deg,transparent 0,#000 18%)"><img src="{S2('iskra-65-3')}" alt="" style="object-position:0% 58%;transform:scale(1.1);transform-origin:0% 60%"></div>
  <div class="scrim-l"></div>
  <div class="lock" style="color:#141110"><p class="k">Колекція</p><p class="s">Соло</p><p class="t">Шлях до себе</p><p class="pill">Жіноча сила крізь десятиліття</p><p class="more">Дивитися колекцію</p><p class="cap">Хустка «Іскра» · 65 × 65</p></div>
  <img class="logo" src="{LOGO_K}" alt="Obiimy"><span class="tm">™</span>''', cls="dark", note="Still life on the table")

# N6 · evening street: «Пульс» twilly on the white shirt, the dark Paris street behind, the figure right
ad("home-n6-evening", f'''
  <div style="inset:0;background:#1A1816"></div>
  <div class="ph" style="left:720px;right:0;top:0;bottom:0"><img src="{S2('puls-tw-3')}" alt="" style="object-position:50% 10%"></div>
  <div style="left:720px;top:0;bottom:0;width:260px;background:linear-gradient(90deg,#1A1816,rgba(26,24,22,0))"></div><div class="scrim-d"></div>
  {lock()}{logo()}''', note="Evening street")

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · SOLO home banners</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / "home.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "home banners")
