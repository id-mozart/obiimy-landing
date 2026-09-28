"""SOLO. Шлях до себе — ad creatives, v2 (after the first audit round).
Rules: text inside story safe zone (y 280…1540); price always matches the product in the photo;
no third-party brands in frame; real Obiimy logo in every file. Output: solo.html → ../render.mjs → out/*.jpg"""
import pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit import *

ads = []
def ad(id, cls, body, note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad {cls}" id="{id}">{body}\n</section>')

def silk(p, size="auto 190%", pos="center"):
    return f'<div class="fill" style="background:url({HI(p)}) {pos}/{size}"></div><div class="fill" style="background:radial-gradient(90% 60% at 50% 45%,rgba(0,0,0,0),rgba(0,0,0,.3))"></div>'

def base(p, top=True, bg="var(--paper)"):
    """Paper page lying on silk: silk shows in the story UI zones, all text stays on paper."""
    return f'<div class="fill" style="background:url({HI(p)}) center/auto 190%"></div><div class="fill" style="background:rgba(0,0,0,.12)"></div><div class="fill" style="top:{236 if top else 0}px;bottom:316px;background:{bg};box-shadow:0 0 70px rgba(0,0,0,.5)"></div>'

def nm_size(p, big, small):
    return big if len(p["name"]) < 9 else small

# =====================================================================================
# 1. COVERS — magazine SOLO, one issue per print. Three layouts; story = the magazine lying on silk.
# =====================================================================================
LINES = "Сім принтів — сім станів<br>Натуральний шовк<br>Двосторонній друк"

def cover_a(p, i, ph, pos):
    kind, size, price = p["formats"][0]
    return f'''
  <div class="fill" style="background:var(--paper)"></div>
  <div class="box col">
    <p class="solo" style="font-size:236px;color:{p['c']};margin-left:-6px">SOLO</p>
    <div class="row" style="justify-content:space-between;border-top:3px solid var(--ink);border-bottom:1px solid var(--ink);padding:10px 0;margin-top:30px">
      <p class="lbl" style="font-size:32px;letter-spacing:.08em">Осінь 2026 · №{i}</p><p class="lbl" style="font-size:32px;letter-spacing:.08em;font-weight:600">{size} — {price} грн</p></div>
    <p class="t" style="font-size:40px;font-style:italic;color:var(--ink2);margin-top:14px">{SLOGAN}</p>
    {photo(ph, pos, style="flex:1;margin-top:16px")}
    <div class="row" style="justify-content:space-between;align-items:flex-end;gap:30px;margin-top:24px">
      <div><p class="h" style="font-size:{nm_size(p, 96, 80)}px;line-height:1;font-style:italic;font-weight:700;color:{p['c']}">«{p['name']}»</p>
        <p class="t" style="font-size:44px;line-height:1.1;color:var(--ink2);margin-top:8px">{p['short']}</p></div>
      <p class="lbl" style="font-size:32px;line-height:1.4;text-align:right;color:var(--ink2);flex:none;letter-spacing:.08em">{LINES}</p>
    </div>
    {foot(size=32, style="margin-top:22px;border-top:1px solid var(--ink);padding-top:18px")}
  </div>'''

def cover_c(p, i, ph, pos):
    kind, size, price = p["formats"][0]
    return f'''
  <div class="fill" style="background:var(--paper)"></div>
  {spot_photo(ph, pos, style="position:absolute;left:310px;right:0;top:0;height:1000px") if ph in MASKED else photo(ph, pos, cls="bw", style="left:310px;right:0;top:0;height:1000px")}
  <div style="left:40px;top:640px;width:500px;height:500px;border-radius:50%;background:{p['c']};mix-blend-mode:multiply;opacity:.92"></div>
  <p class="lbl" style="left:64px;top:64px;width:240px;font-size:32px;letter-spacing:.04em;line-height:1.4;color:var(--ink2);white-space:nowrap">Осінь 2026<br>Випуск №{i}<br><b style="color:var(--ink);font-weight:600">{size}<br>{price} грн</b></p>
  <p class="solo" style="left:58px;top:860px;font-size:240px;color:var(--ink)">SOLO</p>
  <div class="col" style="left:64px;right:64px;top:1100px;bottom:64px">
    <div class="row" style="justify-content:space-between;align-items:flex-end;gap:30px">
      <div><p class="h" style="font-size:{nm_size(p, 96, 80)}px;line-height:1;font-style:italic;font-weight:700;color:{p['c']}">«{p['name']}»</p>
        <p class="t" style="font-size:44px;line-height:1.1;color:var(--ink2);margin-top:8px">{p['short']}</p></div>
      <p class="lbl" style="font-size:32px;line-height:1.4;text-align:right;color:var(--ink2);flex:none;letter-spacing:.08em">{kind} «{p['name']}»<br>Натуральний шовк<br>Двосторонній друк</p>
    </div>
    {foot(size=32, style="margin-top:auto;border-top:1px solid var(--ink);padding-top:18px")}
  </div>'''

def cover_d(p, i, ph, pos):
    kind, size, price = p["formats"][0]
    return f'''
  <div class="fill" style="background:{p['deep']}"></div>
  <div class="box col" style="color:var(--cream);align-items:center">
    <div class="row" style="justify-content:space-between;align-items:flex-end;align-self:stretch">
      <p class="solo" style="font-size:210px;color:var(--cream);margin-left:-6px">SOLO</p>
      <p class="lbl" style="font-size:32px;line-height:1.4;text-align:right;padding-bottom:8px">Осінь 2026<br>Випуск №{i}</p>
    </div>
    <p class="t" style="font-size:40px;font-style:italic;margin-top:26px;align-self:stretch;border-top:1px solid rgba(243,234,219,.6);padding-top:12px">{SLOGAN}</p>
    {photo(ph, pos, style="flex:1;width:700px;margin-top:22px;border-radius:350px 350px 0 0;border:10px solid var(--cream)")}
    <p class="h" style="font-size:{nm_size(p, 96, 84)}px;line-height:1;font-style:italic;font-weight:700;margin-top:22px">«{p['name']}»</p>
    <p class="t" style="font-size:44px;line-height:1.1;margin-top:6px">{p['short']}</p>
    <p class="lbl" style="font-size:32px;color:var(--yellow);margin-top:12px;font-weight:600">{kind} {size} — {price} грн</p>
    {foot(dark=True, size=32, style="margin-top:20px;align-self:stretch;border-top:1px solid rgba(243,234,219,.6);padding-top:18px")}
  </div>'''

COVERS = [("iskra", cover_a, "iskra-65-2", "50% 30%"), ("flirt", cover_a, "flirt-65-3", "35% 25%"), ("puls", cover_d, "puls-44-4", "50% 20%"),
          ("zolote", cover_a, "zolote-44-3", "50% 25%"), ("avantiura", cover_d, "avantiura-88-5", "50% 25%"),
          ("tysha", cover_a, "tysha-88-2", "50% 40%"), ("krok", cover_c, "krok-44-2", "50% 30%")]
for i, (pid, fn, ph, pos) in enumerate(COVERS, 1):
    p = PP[pid]
    inner = fn(p, i, ph, pos)
    dark = " dark" if fn is cover_d else ""
    ad(f"cover-{i:02d}-{pid}", "st", f'''
  {silk(p)}
  <div class="page shadow{dark}" style="left:60px;top:272px;width:1080px;height:1450px;transform:scale(.8889);transform-origin:0 0">{inner}</div>''', f"Cover №{i} {p['name']} (story: magazine on silk)")

# =====================================================================================
# 2. SERIES «Сім станів» (stories): photo on top, state on paper below
# =====================================================================================
ST_PH = {"iskra": ("iskra-65-3", "50% 45%"), "flirt": ("flirt-tw-1", "50% 30%"), "puls": ("puls-44-2", "50% 40%"), "zolote": ("zolote-44-3", "50% 30%"),
         "avantiura": ("avantiura-88-2", "50% 40%"), "tysha": ("tysha-88-2", "50% 45%"), "krok": ("krok-tw-4", "50% 35%")}
for i, p in enumerate(P, 1):
    ph, pos = ST_PH[p["id"]]
    kind, size, price = p["formats"][0]
    L = len(p["state"])
    pb = 1110 if L < 60 else 1060 if L < 100 else 960
    ad(f"states-{i:02d}-{p['id']}", "st", f'''
  {base(p)}
  {photo(ph, pos, style=f"left:0;right:0;top:236px;height:{pb - 236}px")}
  <div style="left:0;top:{pb}px;right:0;height:14px;background:{p['c']}"></div>
  <img class="cut" src="{CUT(p['flat'])}" alt="" style="right:64px;top:{pb - 150}px;width:230px;transform:rotate(7deg)">
  <div class="col" style="left:80px;right:80px;top:{pb + 44}px;bottom:380px">
    <p class="lbl" style="color:var(--ink3)">Стан {i:02d} / 07</p>
    <p class="h" style="font-size:{nm_size(p, 104, 80)}px;line-height:1;font-style:italic;font-weight:700;color:{p['c']};margin-top:10px">«{p['name']}»</p>
    <p class="t" style="font-size:42px;line-height:1.16;color:var(--ink2);margin-top:16px">{nb(p['state'])}</p>
    <p class="lbl" style="margin-top:22px;font-weight:600;letter-spacing:.06em">{kind} {size} — {price} грн · твіллі — 1 600 грн</p>
    {foot(size=28, style="margin-top:14px;border-top:1px solid var(--ink);padding-top:16px")}
  </div>''', f"State {i}: {p['name']}")
ad("states-08-outro", "st", f'''
  {base(PP['krok'])}
  {photo("krok-44-3", "50% 25%", style="left:0;right:0;top:236px;height:824px")}
  <div class="col" style="left:80px;right:80px;top:1100px;bottom:380px">
    <p class="lbl" style="color:var(--ink3)">SOLO · Шлях до себе</p>
    <p class="h" style="font-size:76px;line-height:1.05;font-style:italic;font-weight:700;margin-top:20px">Справжня свобода жінки — самій обирати, якою бути.</p>
    <p class="lbl" style="margin-top:auto;font-weight:600;letter-spacing:.08em">Твіллі — 1 600 грн · хустки — від 2 400 грн</p>
    {foot(style="margin-top:14px;border-top:1px solid var(--ink);padding-top:16px")}
  </div>''', "States outro")

# =====================================================================================
# 3. MANIFESTS — quotes from the release
# =====================================================================================
def ya_ie(cls):
    st = cls == "st"
    box = "safe" if st else "box"
    return f'''
  {base(PP['krok'])}
  <div class="{box} col">
    <p class="h" style="font-size:{150 if st else 130}px;line-height:1;font-weight:700">Я є.</p>
    <p class="h" style="font-size:{124 if st else 108}px;line-height:1;font-style:italic;color:var(--ink2);margin-top:{34 if st else 24}px">Я продовжую жити.</p>
    <p class="h" style="font-size:{136 if st else 118}px;line-height:1;font-weight:900;color:var(--wine);margin-top:{34 if st else 24}px">Я обираю себе.</p>
    <div class="row" style="align-items:center;gap:40px;margin-top:auto">
      <img class="cut" src="{CUT('krok-44-1')}" alt="" style="width:{330 if st else 270}px;transform:rotate(-6deg)">
      <p class="t" style="font-size:{46 if st else 42}px;line-height:1.2;font-style:italic;color:var(--ink2)">Шовкова хустка — маленький акт свободи.</p>
    </div>
    {foot(style="margin-top:30px;border-top:1px solid var(--ink);padding-top:18px")}
  </div>'''
ad("manifest-01-ya-ie", "st", ya_ie("st"), "Manifesto: Я є")

ad("manifest-02-chasy", "st", f'''
  {base(PP['zolote'], bg='var(--paper2)')}
  <div class="safe col">
    <p class="h" style="font-size:70px;line-height:1.06;font-weight:700">Є часи, коли краса здається недоречною.</p>
    <p class="t" style="font-size:42px;line-height:1.16;color:var(--ink2);margin-top:18px">{nb("Коли навколо триває війна, тривоги й невизначеність, мода може сприйматися як щось другорядне.")}</p>
    {photo("zolote-44-4", "50% 30%", style="flex:1;margin-top:26px")}
    <p class="h" style="font-size:70px;line-height:1.06;font-style:italic;font-weight:700;margin-top:26px">Та саме тоді вона набуває особливої сили.</p>
    {foot(style="margin-top:28px;border-top:1px solid var(--ink);padding-top:18px")}
  </div>''', "Manifesto: beauty in hard times")

acts = "".join(f'<p class="t" style="font-size:54px;line-height:1;font-style:italic;border-bottom:1px solid rgba(27,22,19,.3);padding:0 0 16px;margin-top:20px;display:flex;gap:24px;align-items:baseline"><span class="lbl" style="font-size:28px;color:var(--wine);font-style:normal;width:50px">{n}</span>{t}</p>' for n, t in [("I", "улюблена сукня"), ("II", "шовкова хустка"), ("III", "червона помада"), ("IV", "звичка щоранку вкладати волосся")])
ad("manifest-03-akty", "st", f'''
  {base(PP['flirt'])}
  {photo("flirt-tw-4", "50% 45%", style="left:0;right:0;top:236px;height:664px")}
  <div class="col" style="left:80px;right:80px;top:940px;bottom:380px">
    <p class="h" style="font-size:84px;line-height:1;font-weight:700">Маленькі акти свободи</p>
    {acts}
    {foot(style="margin-top:auto")}
  </div>''', "Manifesto: small acts of freedom")

def krasa(cls):
    st = cls == "st"
    p = PP["avantiura"]
    return f'''
  <div class="fill" style="background:var(--wine)"></div>
  <div class="{'safe' if st else 'box'} col" style="color:var(--cream)">
    <p class="h" style="font-size:{92 if st else 84}px;line-height:1.02;font-weight:700">Для жінки краса —<br><i style="font-weight:400">це спосіб зберегти себе.</i></p>
    {photo("avantiura-88-4", "50% 30%", style="flex:1;margin-top:34px;border:12px solid var(--cream)")}
    {foot(dark=True, style="margin-top:26px;border-top:1px solid rgba(243,234,219,.6);padding-top:18px")}
  </div>'''
ad("manifest-04-krasa", "st dark", krasa("st"), "Manifesto: beauty is a way to keep yourself")

def grey(cls):
    st = cls == "st"
    return f'''
  <div class="fill" style="background:#2B2B2E"></div>
  <div class="{'safe' if st else 'box'} col" style="color:var(--cream)">
    <p class="lbl" style="color:rgba(243,234,219,.7)">SOLO · Шлях до себе</p>
    <p class="h" style="font-size:{66 if st else 60}px;line-height:1.1;margin-top:26px">Мода — це про гідність, про право на жіночність навіть тоді, коли світ навколо стає <i>темно-сірим</i>.</p>
    <div style="flex:1;min-height:0;display:grid;place-items:center"><img class="cut" src="{CUT('iskra-65-1')}" alt="" style="height:{600 if st else 520}px;transform:rotate(-7deg);filter:drop-shadow(0 40px 50px rgba(0,0,0,.6))"></div>
    {foot(dark=True, style="margin-top:16px;border-top:1px solid rgba(243,234,219,.5);padding-top:18px")}
  </div>'''
ad("manifest-05-temno-siryi", "st dark", grey("st"), "Manifesto: dark grey world")

ad("manifest-06-popry-strakh", "st", f'''
  {base(PP['tysha'])}
  {photo("tysha-88-4", "40% 0%", cls="bw", style="left:0;right:0;top:236px;height:844px")}
  <div class="page shadow frame2" style="left:70px;right:70px;top:930px;height:630px;background:var(--card)"></div>
  <div class="col" style="left:120px;right:120px;top:990px;height:510px">
    <p class="h" style="font-size:60px;line-height:1.1;font-style:italic;font-weight:700">Справжня сила сьогодні в тому, щоб попри страх обирати життя, красу й майбутнє.</p>
    <div class="row foot" style="margin-top:auto;border-top:1px solid var(--ink);padding-top:18px"><p class="lbl" style="font-size:28px;letter-spacing:.06em">{CTA}</p>{logo(h=34)}</div>
  </div>''', "Manifesto: despite fear")

# =====================================================================================
# 4. FILM STILLS — 4:3 frame, letterbox, subtitles from the release
# =====================================================================================
FILMS = [("tysha", "tysha-88-3", "50% 45%", "Більше не потрібно доводити, поспішати чи відповідати чужим очікуванням."),
         ("krok", "krok-tw-3", "50% 40%", "Не тому, що страх зникає, а тому, що з’являється щось важливіше — довіра до себе."),
         ("avantiura", "avantiura-88-4", "50% 25%", "Готовність виходити за межі звичного та відкриватися новому досвіду.")]
for k, (pid, ph, pos, sub) in enumerate(FILMS, 1):
    p = PP[pid]
    for cls, y0 in (("st", 290),):
        ad(f"film-{k:02d}-{pid}", cls + " dark", f'''
  <div class="fill" style="background:#0B0A09"></div>
  <div class="row" style="left:80px;right:80px;top:{y0}px;justify-content:space-between;align-items:center">
    <div class="row" style="align-items:center;gap:20px">{logo(dark=True, h=34)}<p class="lbl" style="font-size:28px;color:rgba(243,234,219,.85)">представляє</p></div>
    <p class="lbl" style="font-size:28px;color:rgba(243,234,219,.85)">У головній ролі — ви</p>
  </div>
  <p class="solo" style="left:0;right:0;top:{y0 + 56}px;text-align:center;font-size:110px;color:var(--cream)">SOLO</p>
  {photo(ph, pos, style=f"left:0;right:0;top:{y0 + 176}px;height:930px", img_style="filter:contrast(1.1) saturate(.78) sepia(.2)")}
  <div style="left:0;right:0;top:{y0 + 876}px;height:230px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.72))"></div>
  <p class="t" style="left:90px;right:90px;top:{y0 + 950}px;text-align:center;font-size:44px;line-height:1.14;font-style:italic;font-weight:600;color:#FFEFA8;text-shadow:0 2px 6px #000">{nb(sub)}</p>
  <p class="lbl" style="left:0;right:0;top:{y0 + 1130}px;text-align:center;font-size:30px;color:var(--cream);font-weight:600">{offer(p)}</p>
  <p class="lbl" style="left:0;right:0;top:{y0 + 1176}px;text-align:center;font-size:28px;color:rgba(243,234,219,.8)">{CTA}</p>''', f"Film still: {p['name']}")

# =====================================================================================
# 5. «Крізь десятиліття» (three stories) + epoch split
# =====================================================================================
SPREAD = [("1940-ві", "zolote-44-5", "50% 8%", "bw", "У 40-х жінка підкреслювала силу через бездоганну елегантність. Шовкова хустка доповнювала жіночний силует і створювала образ витонченої впевненості. За м’якістю шовку приховувався характер."),
          ("1950-ті", "flirt-tw-3", "50% 30%", "", "У 50-х правила почали руйнуватися. Жінка прагнула свободи — експериментувала з кольором, формою та власною ідентичністю. Хустка ставала яскравим акцентом, сміливою деталлю образу."),
          ("2026", "puls-tw-3", "50% 25%", "raw", "Змінювалися епохи й силуети, але хустка залишалася поруч — як символ жіночності, що не суперечить силі. Адже справжня свобода жінки — самій обирати, якою бути.")]
for k, (year, ph, pos, cls, text) in enumerate(SPREAD, 1):
    pid_d = ph.split("-")[0]
    ad(f"decades-{k:02d}", "st", f'''
  {base(PP[pid_d])}
  {photo(ph, pos, cls=cls, style="left:0;right:0;top:236px;height:700px")}
  <div class="col" style="left:80px;right:80px;top:966px;bottom:380px">
    <div class="row" style="justify-content:space-between;border-bottom:3px solid var(--ink);padding-bottom:10px"><p class="lbl">Жіноча сила крізь десятиліття</p><p class="lbl">{k} / 3</p></div>
    <p class="h" style="font-size:130px;line-height:.95;font-weight:900;font-style:italic;color:var(--wine);margin-top:14px">{year}</p>
    <p class="t" style="font-size:38px;line-height:1.16;color:var(--ink);margin-top:12px">{nb(text)}</p>
    {foot(size=28, style="margin-top:auto;border-top:1px solid var(--ink);padding-top:16px")}
  </div>''', f"Decades {year}")

ad("epoch-01", "st", f'''
  {base(PP['krok'])}
  {photo("krok-44-3", "50% 20%", cls="raw", style="left:0;right:0;top:236px;height:844px")}
  <div class="ph bw" style="left:0;top:236px;width:540px;height:844px"><img src="{S('krok-44-3')}" alt="" style="width:1080px;height:844px;max-width:none;object-position:50% 20%"></div>
  <div style="left:538px;top:236px;width:4px;height:844px;background:var(--cream)"></div>
  <p class="h" style="left:50px;top:910px;font-size:100px;font-weight:900;font-style:italic;color:var(--cream);text-shadow:0 4px 24px rgba(0,0,0,.7)">1950-ті</p>
  <p class="h" style="right:50px;top:910px;font-size:100px;font-weight:900;font-style:italic;color:var(--cream);text-shadow:0 4px 24px rgba(0,0,0,.7)">2026</p>
  <div class="col" style="left:80px;right:80px;top:1120px;bottom:380px">
    <p class="h" style="font-size:68px;line-height:1.05;font-weight:700">Змінювалися епохи й силуети, <i style="font-weight:400">але хустка залишалася поруч.</i></p>
    <p class="lbl" style="margin-top:auto;color:var(--wine);font-weight:600">{offer(PP['krok'])}</p>
    {foot(size=28, style="margin-top:12px;border-top:1px solid var(--ink);padding-top:16px")}
  </div>''', "Epoch split")

# =====================================================================================
# 6. PRODUCT HERO — carré (1:1), pattern poster (story), product cards (feed + story)
# =====================================================================================
for i, p in enumerate(P, 1):
    kind, size, price = p["formats"][0]
    if p["id"] not in ("iskra", "flirt", "avantiura", "tysha"):
        continue
    for cls in ("st",):
        st = True
        ad(f"product-{i:02d}-{p['id']}", cls, f'''
  {base(p)}
  <div class="safe col">
    <div class="row foot" style="margin-top:6px"><p class="lbl" style="color:var(--ink3)">SOLO · Шлях до себе</p>{logo()}</div>
    <div style="flex:1;min-height:0;display:grid;place-items:center;padding-top:40px"><img class="cut" src="{CUT(p['flat'])}" alt="" style="height:560px;transform:rotate({-5 if i % 2 else 5}deg)"></div>
    <p class="h" style="font-size:{nm_size(p, 116, 96)}px;line-height:1;font-style:italic;font-weight:700;color:{p['c']}">«{p['name']}»</p>
    <p class="t" style="font-size:44px;line-height:1.12;color:var(--ink2);margin-top:12px">{nb(p['short'] + ". Натуральний шовк, двосторонній друк.")}</p>
    <div class="col" style="margin-top:14px;border-top:2px solid rgba(27,22,19,.18)">{price_rows(p)}</div>
    <p class="lbl" style="margin-top:24px;font-weight:600">{CTA}</p>
  </div>''', f"Product card: {p['name']}")

# =====================================================================================
# 7. ENTRY PRICE — seven twillies; one print in three formats; the yellow box
# =====================================================================================
def twilly(cls):
    st = cls == "st"
    cell = lambda p: f'<div style="display:grid;justify-items:center;gap:10px"><img class="cut" src="{CUT(p["tw"])}" alt="" style="height:330px"><span class="t" style="font-size:32px;font-style:italic;white-space:nowrap">«{p["name"]}»</span></div>'
    return f'''
  {base(PP['avantiura'])}
  <div class="{'safe' if st else 'box'} col">
    <div class="row foot"><p class="lbl" style="color:var(--ink3)">SOLO · Шлях до себе</p>{logo()}</div>
    <p class="h" style="font-size:{100 if st else 92}px;line-height:1;font-weight:700;margin-top:{30 if st else 22}px">Твіллі — <i style="color:var(--wine)">1 600 грн</i></p>
    <p class="t" style="font-size:44px;line-height:1.15;color:var(--ink2);margin-top:12px">Сім принтів — сім станів. Шовкова стрічка 84\u00a0×\u00a05\u00a0см: на шию, у волосся, на сумку чи зап’ястя.</p>
    <div style="flex:1;min-height:0;display:grid;align-content:center;gap:{30 if st else 20}px">
      <div class="row" style="justify-content:space-around">{"".join(cell(p) for p in P[:4])}</div>
      <div class="row" style="justify-content:space-between;padding:0 20px">{"".join(cell(p) for p in P[4:])}</div>
    </div>
    <p class="lbl" style="font-weight:600">{CTA}</p>
  </div>'''
ad("twilly-01", "st", twilly("st"), "Entry price: seven twillies")

FL = PP["flirt"]
TRIO = [("Резинка для волосся", "700", "flirt-scr-3", "50% 40%", ""), ("Твіллі 84 × 5", "1 600", "flirt-tw-1", "50% 40%", ""), ("Хустка 65 × 65", "4 800", "flirt-65-3", "35% 30%", "")]
for k, (what, price, ph, pos, cls) in enumerate(TRIO, 1):
    ad(f"flirt-{k:02d}", "st", f'''
  {base(FL)}
  {photo(ph, pos, cls=cls, style="left:0;right:0;top:236px;height:804px")}
  <div style="left:0;top:1040px;right:0;height:14px;background:{FL['c']}"></div>
  <div class="col" style="left:80px;right:80px;top:1086px;bottom:380px">
    <p class="lbl" style="color:var(--ink3)">Один принт — три формати · {k} / 3</p>
    <div class="row" style="justify-content:space-between;align-items:flex-end;margin-top:18px;gap:30px">
      <div><p class="h" style="font-size:110px;line-height:1;font-style:italic;font-weight:700;color:{FL['c']}">«Флірт»</p>
        <p class="t" style="font-size:48px;line-height:1.1;color:var(--ink2);margin-top:10px">{what}</p></div>
      <p class="h" style="font-size:100px;line-height:1;font-weight:700;flex:none">{price} <span style="font-size:50px">грн</span></p>
    </div>
    <p class="t" style="font-size:40px;line-height:1.15;font-style:italic;color:var(--ink2);margin-top:14px">Флірт — це насамперед стан.</p>
    {foot(style="margin-top:auto;border-top:1px solid var(--ink);padding-top:16px")}
  </div>''', f"One print, three formats: {what}")

def box(cls):
    st = cls == "st"
    return f'''
  <div class="fill" style="background:var(--yellow)"></div>
  <div class="{'safe' if st else 'box'} col">
    <div class="row foot"><p class="lbl">SOLO · Шлях до себе</p>{logo()}</div>
    <p class="h" style="font-size:{104 if st else 84}px;line-height:1;font-weight:700;margin-top:{30 if st else 20}px">Маленький акт свободи</p>
    <div class="ph raw" style="flex:1;min-height:0;margin-top:{30 if st else 22}px;position:relative;border:16px solid var(--card);box-shadow:0 30px 40px -24px rgba(90,60,0,.5)"><img src="{S('flirt-scr-1')}" alt="" style="object-position:50% 45%"></div>
    <div class="row" style="justify-content:space-between;align-items:flex-end;margin-top:24px;gap:30px">
      <p class="t" style="font-size:{46 if st else 42}px;line-height:1.1;font-weight:600">Шовкова резинка «Флірт»<br><span style="font-weight:500">Натуральний шовк</span></p>
      <p class="h" style="font-size:{92 if st else 80}px;line-height:1;font-weight:700;flex:none">700 <span style="font-size:44px">грн</span></p>
    </div>
    <p class="lbl" style="margin-top:24px;font-weight:600">{CTA}</p>
  </div>'''
ad("box-01", "st", box("st"), "Yellow box")

# =====================================================================================
# 8. WAYS, PRICE LIST, CONTACT SHEET, DICTIONARY, GAZETTE, DOUBLE-SIDED
# =====================================================================================
WAYS = [("На шиї", "«Золоте світло»", "zolote-44-2", "50% 25%"), ("У волоссі", "«Авантюра»", "avantiura-tw-3", "50% 45%"),
        ("На сумці", "«Іскра»", "iskra-tw-3", "50% 60%"), ("На зап’ясті", "«Пульс»", "puls-44-5", "45% 60%")]
def ways(cls):
    st = cls == "st"
    cells = "".join(f'''<div class="ph" style="position:relative"><img src="{S(ph)}" alt="" style="object-position:{pos}"><div style="position:absolute;left:0;right:0;bottom:0;height:220px;background:linear-gradient(0deg,rgba(12,9,8,.8),transparent)"></div>
      <p class="lbl" style="position:absolute;left:24px;bottom:18px;font-size:32px;line-height:1.25;color:#fff;font-weight:600">{t}<br><span class="t" style="font-size:36px;font-weight:600;font-style:italic;text-transform:none;letter-spacing:0">{n}</span></p></div>''' for t, n, ph, pos in WAYS)
    return f'''
  {base(PP['puls'])}
  <div class="{'safe' if st else 'box'} col">
    <div class="row foot"><p class="lbl" style="color:var(--ink3)">SOLO · Шлях до себе</p>{logo()}</div>
    <p class="h" style="font-size:{84 if st else 72}px;line-height:1.02;font-weight:700;margin-top:20px">Чотири способи <i style="font-weight:400">носити SOLO</i></p>
    <div style="flex:1;min-height:0;margin-top:24px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:12px">{cells}</div>
    <p class="lbl" style="margin-top:22px;font-weight:600;letter-spacing:.08em">Твіллі — 1 600 грн · хустка 44 × 44 — 2 400 грн</p>
    <p class="lbl" style="margin-top:8px;font-size:28px;color:var(--ink2)">{CTA}</p>
  </div>'''
ad("ways-01", "st", ways("st"), "Four ways to wear")

ROWS = [("Твіллі 84 × 5", "усі сім принтів", "1 600"), ("Хустка 44 × 44", "«Пульс», «Золоте світло», «Сміливий крок»", "2 400"),
        ("Хустка 65 × 65", "«Іскра», «Флірт»", "4 800"), ("Хустка 88 × 88", "«Авантюра», «Тиша всередині»", "6 600"), ("Резинка для волосся", "«Флірт»", "700")]
def price(cls):
    st = cls == "st"
    rows = "".join(f'<div class="row" style="justify-content:space-between;align-items:baseline;gap:20px;border-bottom:1px solid rgba(27,22,19,.35);padding:{18 if st else 14}px 0"><p><span class="h" style="font-size:46px;font-weight:700">{a}</span><br><span class="t" style="font-size:34px;font-style:italic;color:var(--ink2)">{b}</span></p><p class="h" style="font-size:52px;flex:none">{c} <span style="font-size:32px">грн</span></p></div>' for a, b, c in ROWS)
    strip = "".join(f'<img class="cut" src="{CUT(p["flat"])}" alt="" style="width:{128 if st else 124}px;transform:rotate({(-1) ** k * 5}deg);filter:drop-shadow(0 12px 14px rgba(40,25,10,.3))">' for k, p in enumerate(P))
    return f'''
  {base(PP['tysha'])}
  <div class="{'safe' if st else 'box'} col">
    <div class="row foot"><p class="lbl" style="color:var(--ink3)">Каталог · осінь 2026</p>{logo()}</div>
    <div class="row" style="align-items:flex-end;gap:30px;margin-top:{26 if st else 16}px"><p class="solo" style="font-size:{190 if st else 170}px;margin-left:-6px">SOLO</p><p class="h" style="font-size:52px;font-style:italic;color:var(--wine);padding-bottom:6px">Шлях до себе</p></div>
    <div class="row" style="justify-content:space-between;margin-top:{34 if st else 24}px">{strip}</div>
    <div style="margin-top:{26 if st else 14}px;border-top:3px solid var(--ink)">{rows}</div>
    <p class="lbl" style="margin-top:auto;font-size:28px;color:var(--ink2)">Натуральний шовк · двосторонній друк</p>
    <p class="lbl" style="margin-top:8px;font-weight:600">{CTA}</p>
  </div>'''
ad("price-01", "st", price("st"), "Price list")

ad("gazette-01", "st", f'''
  {base(PP['krok'], bg='#EFE7D6')}
  <div class="safe col">
    <p class="h" style="text-align:center;font-size:120px;line-height:1;font-weight:900">Вісник SOLO</p>
    <div class="row" style="justify-content:space-between;border-top:3px solid var(--ink);border-bottom:1px solid var(--ink);padding:8px 0;margin-top:14px"><p class="lbl" style="font-size:28px">Київ · осінь 2026</p><p class="lbl" style="font-size:28px">Спецвипуск Obiimy</p></div>
    <p class="h" style="font-size:96px;line-height:.98;font-weight:900;text-transform:uppercase;margin-top:24px">Свобода — самій обирати, якою бути</p>
    <div class="row" style="gap:34px;margin-top:26px;flex:1;min-height:0">
      <div style="width:500px;flex:none;position:relative">{spot_photo("krok-44-2", "50% 25%", style="position:absolute;inset:0")}<div style="position:absolute;inset:0;background:radial-gradient(circle,rgba(0,0,0,.2) 1px,transparent 1.7px) 0 0/6px 6px;mix-blend-mode:multiply"></div></div>
      <div class="col" style="flex:1">
        <p class="t" style="font-size:40px;line-height:1.18">{nb("Український бренд Obiimy презентує колекцію SOLO. Шлях до себе: сім авторських принтів на натуральному шовку — сім станів на шляху жінки до себе.")}</p>
        <div style="margin-top:auto;border:2px solid var(--ink);padding:18px 20px">
          <p class="lbl" style="font-size:28px;letter-spacing:.06em;line-height:1.4">На фото: хустка «Сміливий крок»<br><b style="font-weight:600">44 × 44 · 2 400 грн</b></p>
        </div>
      </div>
    </div>
    {foot(style="margin-top:22px;border-top:3px solid var(--ink);padding-top:16px")}
  </div>''', "Gazette front page")

(HERE / "solo.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "creatives")
