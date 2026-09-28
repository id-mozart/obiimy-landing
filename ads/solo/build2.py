"""SOLO creatives, extra concepts (1080×1920). Output: solo2.html → out2/*.jpg"""
import pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit import *

ads = []
def ad(id, cls, body, note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad {cls}" id="{id}">{body}\n</section>')

# ---------- A. Route: the path to yourself, seven stops
stops = "".join(f'''<div class="row" style="align-items:center;gap:30px;height:128px">
      <p class="lbl" style="width:56px;color:var(--ink3);font-size:30px">{i:02d}</p>
      <span style="width:96px;height:96px;flex:none;background:url({HI(p)}) center/230%"></span>
      <p style="flex:1"><span class="h" style="font-size:54px;line-height:1;font-style:italic;font-weight:700;color:{p['c']}">«{p['name']}»</span><br><span class="t" style="font-size:36px;line-height:1.1;color:var(--ink2)">{p['short'].lower() if p['id'] != 'flirt' else 'флірт — це насамперед стан'}</span></p>
    </div>''' for i, p in enumerate(P, 1))
ad("route-01", "st", f'''
  {base(PP['puls'])}
  <div class="safe col">
    <div class="row foot"><p class="lbl" style="color:var(--ink3)">SOLO · колекція Obiimy</p>{logo()}</div>
    <p class="h" style="font-size:110px;line-height:1;font-weight:700;margin-top:22px">Шлях <i style="font-weight:400;color:var(--wine)">до себе</i></p>
    <p class="t" style="font-size:42px;line-height:1.15;color:var(--ink2);margin-top:10px">{nb("Сім авторських принтів — сім етапів внутрішньої подорожі.")}</p>
    <div style="position:relative;margin-top:18px">
      <div style="position:absolute;left:133px;top:60px;bottom:60px;border-left:3px dashed rgba(27,22,19,.35)"></div>
      <div style="position:relative">{stops}</div>
    </div>
    <p class="lbl" style="margin-top:auto;font-weight:600;border-top:1px solid var(--ink);padding-top:16px">{CTA}</p>
  </div>''', "Route: seven stops")

# ---------- B. Editor's letter
ad("editor-01", "st", f'''
  {base(PP['zolote'])}
  <div class="safe col">
    <div class="row foot" style="border-bottom:3px solid var(--ink);padding-bottom:12px"><p class="lbl">SOLO · слово бренду</p>{logo()}</div>
    <p class="h" style="font-size:58px;line-height:1.14;font-style:italic;margin-top:40px">«{nb("Кожна українська жінка під час війни щодня демонструє особливу стійкість. Ми волонтеримо, працюємо, виховуємо дітей, допомагаємо армії, а також знаходимо сили залишатися красивими, мріяти, створювати, кохати.")}»</p>
    <p class="h" style="font-size:66px;line-height:1.06;font-weight:700;color:var(--wine);margin-top:36px">Для жінки краса — це спосіб зберегти себе.</p>
    <div style="flex:1;min-height:0;display:grid;place-items:center end"><img class="cut" src="{CUT('zolote-tw-1')}" alt="" style="height:100%;max-height:330px;transform:rotate(-12deg);margin-right:40px"></div>
    <p class="lbl" style="font-size:28px;color:var(--ink2);border-top:1px solid var(--ink);padding-top:16px">Колекція SOLO. Шлях до себе · obiimy.world</p>
  </div>''', "Brand word: resilience (organic, no price)")

# ---------- C. Back cover: one product on its colour
for i, p in enumerate(P, 1):
    if p["id"] not in ("iskra", "puls", "zolote", "tysha"):
        continue
    ad(f"back-{i:02d}-{p['id']}", "st dark", f'''
  <div class="fill" style="background:{p['deep']}"></div>
  <div class="fill" style="background:radial-gradient(70% 45% at 50% 46%,rgba(255,255,255,.16),rgba(0,0,0,.25))"></div>
  <div class="safe col" style="align-items:center;color:var(--cream);text-align:center">
    {logo(dark=True, h=44)}
    <div style="flex:1;min-height:0;display:grid;place-items:center"><img class="cut" src="{CUT(p['flat'])}" alt="" style="height:760px;transform:rotate({-6 if i % 2 else 6}deg);filter:drop-shadow(0 50px 60px rgba(0,0,0,.55))"></div>
    <p class="h" style="font-size:{110 if len(p['name']) < 9 else 92}px;line-height:1;font-style:italic;font-weight:700">«{p['name']}»</p>
    <p class="lbl" style="margin-top:16px;color:var(--yellow);font-weight:600">{p['formats'][0][0]} {p['formats'][0][1]} · {p['formats'][0][2]} грн</p>
    <p class="lbl" style="margin-top:8px;font-size:28px">{CTA}</p>
  </div>''', f"Back cover: {p['name']}")

# ---------- D. The state spelled in silk
WORD_BG = {"puls": "1100px", "zolote": "1300px", "tysha": "1200px", "krok": "2000px"}
for i, p in enumerate(P, 1):
    if p["id"] not in WORD_BG:
        continue
    words = p["name"].upper().split()
    n = max(len(w) for w in words)
    size = min(250, int(900 / (n * 0.74)))
    glyph = "font-size:{size}px;line-height:1;padding-bottom:.12em;font-weight:900;white-space:nowrap"
    letters = "".join(f'''<div style="position:relative"><p class="h" style="{glyph.format(size=size)};color:var(--cream);-webkit-text-stroke:5px var(--cream)">{w}</p>
      <p class="h" style="position:absolute;left:0;top:0;{glyph.format(size=size)};background:url({HI(p)}) center/{WORD_BG[p["id"]]};-webkit-background-clip:text;background-clip:text;color:transparent">{w}</p></div>''' for w in words)
    ad(f"word-{i:02d}-{p['id']}", "st dark", f'''
  <div class="fill" style="background:#141110"></div>
  <div class="safe col" style="color:var(--cream)">
    <div class="row foot"><p class="lbl" style="color:rgba(243,234,219,.75)">SOLO · стан {i:02d} / 07</p>{logo(dark=True)}</div>
    <div style="margin-top:50px">{letters}</div>
    <p class="t" style="font-size:44px;line-height:1.16;margin-top:20px">{nb(p['state'])}</p>
    <div style="flex:1;min-height:0;display:grid;place-items:center"><img class="cut" src="{CUT(p['flat'])}" alt="" style="height:100%;max-height:380px;transform:rotate(-6deg);filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))"></div>
    <p class="lbl" style="color:var(--yellow);font-weight:600;letter-spacing:.06em;border-top:1px solid rgba(243,234,219,.5);padding-top:16px">{offer(p)}</p>
    <p class="lbl" style="margin-top:8px;font-size:28px">{CTA}</p>
  </div>''', f"Word in silk: {p['name']}")

# ---------- E. Colour spot: the scarf is the only colour
SPOT = [("puls", "puls-44-4", "50% 20%", "Хустка ставала яскравим акцентом, сміливою деталлю образу."),
        ("avantiura", "avantiura-88-5", "62% 30%", "Мода завжди була більше, ніж одяг."),
        ("iskra", "iskra-65-2", "40% 30%", "Сміливість бути помітною.")]
for k, (pid, ph, pos, text) in enumerate(SPOT, 1):
    p = PP[pid]
    ad(f"spot-{k:02d}-{pid}", "st dark", f'''
  <div class="fill" style="background:#111"></div>
  {spot_photo(ph, pos, style="position:absolute;left:0;right:0;top:236px;height:1368px")}
  <div style="left:0;right:0;top:1000px;height:604px;background:linear-gradient(180deg,transparent,rgba(10,8,7,.86) 55%)"></div>
  <div class="row foot" style="left:80px;right:80px;top:280px"><p class="lbl" style="color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.6)">SOLO · Шлях до себе</p>{logo(dark=True)}</div>
  <div class="col" style="left:80px;right:80px;top:1150px;height:390px;color:var(--cream)">
    <p class="h" style="font-size:{70 if len(text) > 40 else 96}px;line-height:1.02;font-style:italic;font-weight:700;margin-top:auto">{nb(text)}</p>
    <p class="lbl" style="margin-top:22px;color:var(--yellow);font-weight:600">{offer(p)}</p>
    <p class="lbl" style="margin-top:6px;font-size:28px">{CTA}</p>
  </div>''', f"Colour spot: {p['name']}")

# ---------- F. Three stories in a row: Я є. / Я продовжую жити. / Я обираю себе.
TRI = [("Я є.", "zolote-44-2", "50% 20%", "zolote", 190), ("Я продовжую жити.", "puls-44-2", "50% 35%", "puls", 120), ("Я обираю себе.", "tysha-88-3", "50% 45%", "tysha", 140)]
for k, (text, ph, pos, pid, size) in enumerate(TRI, 1):
    p = PP[pid]
    ad(f"ya-{k:02d}", "st", f'''
  {base(p)}
  {photo(ph, pos, style="left:0;right:0;top:236px;height:844px")}
  <div class="col" style="left:80px;right:80px;top:1110px;bottom:380px">
    <div class="row" style="justify-content:space-between"><p class="lbl" style="color:var(--ink3)">SOLO · Шлях до себе</p><p class="lbl" style="color:var(--ink3)">{k} / 3</p></div>
    <p class="h" style="font-size:{size}px;line-height:.98;font-weight:900;color:{'var(--wine)' if k == 3 else 'var(--ink)'};margin-top:14px;{'font-style:italic;font-weight:700' if k == 2 else ''}">{text}</p>
    <p class="lbl" style="margin-top:auto;font-weight:600;color:{p['c']};letter-spacing:.06em">{offer(p)}</p>
    {foot(size=28, style="margin-top:10px;border-top:1px solid var(--ink);padding-top:14px")}
  </div>''', f"Sequence: {text}")

(HERE / "solo2.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "creatives (extra)")
