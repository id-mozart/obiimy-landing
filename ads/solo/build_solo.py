"""SOLO. Шлях до себе — ad creatives. Copy follows the press release (Desktop/! РЕЛІЗ OBIIMY_SOLO.docx);
prices from obiimy.world/solo-shliakh-do-sebe (28.09.2026). Output: solo.html, rendered by ../render.mjs."""
import pathlib

HERE = pathlib.Path(__file__).parent

# press-release order = the journey
P = [
    dict(id="iskra", name="Іскра", c="#2F63A8", flat="iskra-65-1", life="iskra-65-2", fmt="65 × 65", price="4 800",
         short="Сміливість бути помітною",
         state="Внутрішня енергія, сміливість бути помітною та здатність запалювати зміни навколо себе."),
    dict(id="flirt", name="Флірт", c="#7E9468", flat="flirt-65-1", life="flirt-65-2", fmt="65 × 65", price="4 800",
         short="Флірт — це стан",
         state="Віра в перемогу, оптимізм і мистецтво невимушеної жіночності. Уміння насолоджуватися собою, життям і моментом."),
    dict(id="puls", name="Пульс", c="#4E8B3A", flat="puls-44-1", life="puls-44-4", fmt="44 × 44", price="2 400",
         short="Внутрішній ритм",
         state="Природна сила та внутрішня опора. Ритм, що залишається незмінним, навіть коли навколо змінюється все."),
    dict(id="zolote", name="Золоте світло", c="#B8741F", flat="zolote-44-1", life="zolote-44-2", fmt="44 × 44", price="2 400",
         short="Момент ясності",
         state="Моменти ясності, коли все стає на свої місця."),
    dict(id="avantiura", name="Авантюра", c="#7B1F24", flat="avantiura-88-1", life="avantiura-88-2", fmt="88 × 88", price="6 600",
         short="За межі звичного",
         state="Готовність виходити за межі звичного та відкриватися новому досвіду."),
    dict(id="tysha", name="Тиша всередині", c="#26231F", flat="tysha-88-1", life="tysha-88-2", fmt="88 × 88", price="6 600",
         short="Чути себе",
         state="Баланс і здатність чути себе серед зовнішнього шуму. Більше не потрібно доводити, поспішати чи відповідати чужим очікуванням."),
    dict(id="krok", name="Сміливий крок", c="#8E2A2C", flat="krok-44-1", life="krok-44-2", fmt="44 × 44", price="2 400",
         short="Довіра до себе",
         state="Рішення рухатися вперед, навіть коли немає повної визначеності. Не тому, що страх зникає, а тому, що з’являється довіра до себе."),
]
LOGO_W = "../../brand/logo-white.png"
LOGO_K = "../../brand/logo-ink.png"
def S(name): return f"src/{name}.webp"

CSS = """
:root { --paper: #F3EADB; --paper2: #E9DCC6; --ink: #1B1613; --ink2: #4B423B; --ink3: #8B7F74; --wine: #7B1F24; --gold: #C58B2A; --yellow: #F2B705; }
* { box-sizing: border-box; }
body { margin: 0; background: #555; font-family: 'Onest', Arial, sans-serif; color: var(--ink); -webkit-font-smoothing: antialiased; }
.ad { position: relative; overflow: hidden; background: var(--paper); margin: 24px auto; }
.st { width: 1080px; height: 1920px; } .fd { width: 1080px; height: 1350px; } .sq { width: 1080px; height: 1080px; }
.ad > * { position: absolute; margin: 0; }
.ad p, .ad h1, .ad h2 { margin: 0; }
.cover img, img.cover { width: 100%; height: 100%; object-fit: cover; display: block; }
.fill { inset: 0; }
.grain::after { content: ""; position: absolute; inset: 0; pointer-events: none; opacity: .16; mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .9 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
.film::after { opacity: .22; mix-blend-mode: overlay; }
.pf { font-family: 'Playfair Display', serif; }
.cg { font-family: 'Cormorant Garamond', serif; }
.os { font-family: 'Oswald', sans-serif; text-transform: uppercase; }
.mk { font-family: 'Marck Script', cursive; }
.mono { font-family: 'IBM Plex Mono', monospace; }
.logo { height: 40px; } .logo img { height: 100%; width: auto; display: block; }
.solo { font-family: 'Playfair Display', serif; font-weight: 900; font-style: italic; letter-spacing: -.02em; line-height: .8; }
.shadow { box-shadow: 0 40px 60px -30px rgba(0,0,0,.45); }
.tag { font-family: 'Oswald'; text-transform: uppercase; letter-spacing: .18em; font-size: 24px; }
.price-dot { border-radius: 50%; display: grid; place-items: center; text-align: center; font-family: 'Oswald'; text-transform: uppercase; line-height: 1.05; }
.url { font-family: 'Onest'; font-weight: 500; letter-spacing: .08em; font-size: 26px; }
"""

ads = []
def ad(id, cls, body, note):
    ads.append(f'\n<!-- {note} -->\n<section class="ad {cls}" id="{id}">{body}\n</section>')

# ---------- 1. Retro magazine covers (feed 4:5), two layouts
for i, p in enumerate(P, 1):
    num = f"№{i}"
    if i % 2:  # A: paper masthead band, framed photo
        body = f'''
  <div class="fill grain" style="background:var(--paper)"></div>
  <p class="solo" style="left:56px;top:50px;font-size:250px;color:{p['c']}">SOLO</p>
  <p class="os" style="right:60px;top:78px;font-size:24px;letter-spacing:.2em;text-align:right;line-height:1.5;color:var(--ink2)">Осінь 2026<br>Випуск {num}<br>Obiimy</p>
  <p class="cg" style="left:62px;top:300px;font-size:34px;font-style:italic;color:var(--ink2)">Шлях до себе · жіноча сила крізь десятиліття</p>
  <div class="cover shadow" style="left:56px;right:56px;top:362px;bottom:56px"><img src="{S(p['life'])}" alt="" style="object-position:50% 30%"></div>
  <div style="left:56px;bottom:56px;right:56px;height:520px;background:linear-gradient(180deg,transparent,rgba(20,14,10,.78))"></div>
  <p class="os" style="left:100px;bottom:250px;font-size:30px;letter-spacing:.24em;color:#F3EADB">Хустка «{p['name']}»</p>
  <p class="pf" style="left:96px;right:340px;bottom:112px;font-size:72px;line-height:1.02;font-style:italic;color:#fff">{p['short']}</p>
  <div class="price-dot" style="right:96px;bottom:110px;width:190px;height:190px;background:{p['c']};color:#fff;font-size:26px;transform:rotate(-10deg)">твіллі<br><b style="font-size:44px;font-weight:600">1 600</b>грн</div>'''
    else:  # B: full bleed, masthead over the sky, cover lines left
        body = f'''
  <div class="cover fill"><img src="{S(p['life'])}" alt="" style="object-position:50% 40%"></div>
  <div style="left:0;right:0;top:0;height:520px;background:linear-gradient(180deg,rgba(15,10,8,.55),transparent)"></div>
  <div style="left:0;right:0;bottom:0;height:640px;background:linear-gradient(0deg,rgba(15,10,8,.8),transparent)"></div>
  <p class="solo" style="left:0;right:0;top:36px;text-align:center;font-size:330px;color:#F3EADB;text-shadow:0 6px 30px rgba(0,0,0,.25)">SOLO</p>
  <p class="os" style="left:0;right:0;top:318px;text-align:center;font-size:24px;letter-spacing:.34em;color:#F3EADB">Шлях до себе · осінь 2026 · випуск {num}</p>
  <p class="os" style="left:64px;bottom:360px;font-size:28px;letter-spacing:.2em;color:{'#F2B705' if p['id'] != 'zolote' else '#F3EADB'}">Нова колекція Obiimy</p>
  <p class="pf" style="left:60px;right:60px;bottom:170px;font-size:88px;line-height:1;font-weight:700;color:#fff">«{p['name']}»</p>
  <p class="cg" style="left:64px;right:360px;bottom:70px;font-size:36px;font-style:italic;line-height:1.2;color:#F3EADB">{p['state'].split('.')[0]}.</p>
  <p class="os" style="right:64px;bottom:76px;font-size:26px;letter-spacing:.14em;color:#F3EADB;text-align:right">Хустка {p['fmt']}<br><b style="font-size:40px;font-weight:600">{p['price']} грн</b></p>'''
    ad(f"cover-{i:02d}-{p['id']}", "fd", body, f"Retro magazine cover {num}: {p['name']}")

# ---------- 2. Carousel «Сім станів» (square)
ad("states-00-intro", "sq", f'''
  <div class="fill grain" style="background:var(--ink)"></div>
  <p class="os" style="left:80px;top:90px;font-size:26px;letter-spacing:.3em;color:var(--gold)">Obiimy · нова колекція</p>
  <p class="solo" style="left:70px;top:170px;font-size:260px;color:#F3EADB">SOLO</p>
  <p class="pf" style="left:80px;top:420px;font-size:70px;font-style:italic;color:#F3EADB">Шлях до себе</p>
  <p class="cg" style="left:80px;right:80px;top:560px;font-size:44px;line-height:1.3;color:rgba(243,234,219,.85)">Сім авторських принтів — сім станів на шляху жінки до себе. Гортайте →</p>
  <div style="left:80px;right:80px;bottom:90px;height:90px;display:flex;gap:14px">{''.join(f'<span style="flex:1;background:url({S(p["flat"])}) center/cover;border:3px solid #F3EADB"></span>' for p in P)}</div>''', "Carousel intro")
for i, p in enumerate(P, 1):
    ad(f"states-{i:02d}-{p['id']}", "sq", f'''
  <div class="fill grain" style="background:var(--paper)"></div>
  <div style="left:0;top:0;bottom:0;width:22px;background:{p['c']}"></div>
  <p class="os" style="left:80px;top:80px;font-size:28px;letter-spacing:.3em;color:var(--ink3)">Стан {i:02d} / 07</p>
  <p class="pf" style="left:76px;top:130px;width:540px;font-size:84px;line-height:1;font-style:italic;color:{p['c']}">«{p['name']}»</p>
  <p class="cg" style="left:80px;top:{400 if len(p['name']) < 10 else 480}px;width:500px;font-size:40px;line-height:1.28;color:var(--ink2)">{p['state']}</p>
  <div class="shadow" style="right:70px;top:170px;width:400px;height:400px;background:url({S(p['flat'])}) center/cover;transform:rotate({(-1) ** i * 5}deg)"></div>
  <div class="cover" style="right:120px;bottom:80px;width:300px;height:300px;border:10px solid #fff;transform:rotate({(-1) ** (i + 1) * 4}deg);box-shadow:0 20px 40px -20px rgba(0,0,0,.5)"><img src="{S(p['life'])}" alt="" style="object-position:50% 30%"></div>
  <p class="os" style="left:80px;bottom:84px;font-size:24px;letter-spacing:.2em;color:var(--ink3)">SOLO · Шлях до себе · Obiimy</p>''', f"Carousel state {i}: {p['name']}")
ad("states-08-outro", "sq", f'''
  <div class="fill cover"><img src="{S('zolote-44-5')}" alt="" style="object-position:50% 40%"></div>
  <div class="fill" style="background:linear-gradient(0deg,rgba(15,10,8,.85) 10%,rgba(15,10,8,.1) 70%)"></div>
  <p class="pf" style="left:80px;right:80px;bottom:300px;font-size:72px;line-height:1.05;font-style:italic;color:#fff">Справжня свобода — самій обирати, якою бути.</p>
  <p class="os" style="left:80px;bottom:200px;font-size:28px;letter-spacing:.2em;color:#F2B705">Колекція SOLO · від 700 грн</p>
  <p class="url" style="left:80px;bottom:120px;color:#F3EADB">obiimy.world</p>
  <div class="logo" style="right:80px;bottom:118px"><img src="{LOGO_W}" alt=""></div>''', "Carousel outro")

# ---------- 3. Manifesto stories
ad("manifest-01-ya-ie", "st", f'''
  <div class="fill grain" style="background:var(--paper)"></div>
  <div class="logo" style="left:50%;transform:translateX(-50%);top:110px"><img src="{LOGO_K}" alt=""></div>
  <div style="left:90px;right:90px;top:330px;display:grid;gap:40px">
    <p class="pf" style="position:static;font-size:150px;line-height:1;font-weight:700">Я є.</p>
    <p class="pf" style="position:static;font-size:130px;line-height:1;font-style:italic;color:var(--ink2)">Я продовжую жити.</p>
    <p class="pf" style="position:static;font-size:140px;line-height:1;font-weight:900;color:var(--wine)">Я обираю себе.</p>
  </div>
  <div class="shadow" style="left:90px;bottom:300px;width:420px;height:420px;background:url({S('avantiura-tw-2')}) center/115% #fff;transform:rotate(-6deg)"></div>
  <p class="cg" style="left:560px;right:90px;bottom:420px;font-size:40px;line-height:1.3;font-style:italic;color:var(--ink2)">Шовкова хустка — маленький акт свободи.</p>
  <p class="os" style="left:90px;right:90px;bottom:120px;font-size:28px;letter-spacing:.24em;color:var(--ink3)">SOLO · Шлях до себе · obiimy.world</p>''', "Manifesto: Я є")
ad("manifest-02-krasa-nedorechna", "st", f'''
  <div class="fill cover"><img src="{S('tysha-88-2')}" alt="" style="object-position:40% 50%"></div>
  <div class="fill" style="background:linear-gradient(180deg,rgba(12,9,8,.82) 0%,rgba(12,9,8,.35) 45%,rgba(12,9,8,.85) 100%)"></div>
  <div class="logo" style="left:90px;top:110px"><img src="{LOGO_W}" alt=""></div>
  <p class="cg" style="left:90px;right:90px;top:280px;font-size:66px;line-height:1.2;color:#F3EADB">Є часи, коли краса здається недоречною.</p>
  <p class="pf" style="left:90px;right:90px;bottom:420px;font-size:92px;line-height:1.02;font-style:italic;color:#fff">Саме тоді вона набуває особливої сили.</p>
  <p class="os" style="left:90px;bottom:300px;font-size:28px;letter-spacing:.22em;color:#F2B705">SOLO · нова колекція Obiimy</p>
  <p class="url" style="left:90px;bottom:220px;color:#F3EADB">obiimy.world</p>''', "Manifesto: beauty in hard times")
ad("manifest-03-akty-svobody", "st", f'''
  <div class="fill grain" style="background:var(--paper2)"></div>
  <p class="os" style="left:90px;top:120px;font-size:28px;letter-spacing:.3em;color:var(--wine)">SOLO · Шлях до себе</p>
  <p class="pf" style="left:90px;right:90px;top:190px;font-size:112px;line-height:1;font-weight:700">Маленькі акти свободи</p>
  <div style="left:90px;right:90px;top:520px;display:grid;gap:26px">
    {''.join(f'<p class="cg" style="position:static;font-size:56px;display:flex;gap:26px;align-items:center;border-bottom:2px solid rgba(27,22,19,.18);padding-bottom:22px"><span style="width:54px;height:54px;border:3px solid var(--ink);display:grid;place-items:center;font-family:Onest;font-size:40px;color:var(--wine);flex:none">✓</span>{t}</p>' for t in ["улюблена сукня", "шовкова хустка", "червона помада", "звичка щоранку вкладати волосся"])}
  </div>
  <div class="cover shadow" style="left:90px;right:90px;bottom:250px;height:560px"><img src="{S('flirt-tw-1')}" alt="" style="object-position:50% 45%"></div>
  <p class="cg" style="left:90px;right:90px;bottom:130px;font-size:40px;font-style:italic;color:var(--ink2)">«Я є. Я продовжую жити. Я обираю себе».</p>''', "Manifesto: small acts of freedom checklist")
ad("manifest-04-sposib-zberehty", "st", f'''
  <div class="fill" style="background:var(--wine)"></div>
  <div class="fill grain"></div>
  <p class="pf" style="left:90px;right:90px;top:200px;font-size:128px;line-height:1;font-weight:900;color:#F3EADB">Краса —</p>
  <p class="pf" style="left:90px;right:90px;top:340px;font-size:128px;line-height:1.02;font-style:italic;color:#F3EADB">це спосіб зберегти себе.</p>
  <div class="cover" style="left:90px;right:90px;top:780px;height:760px;border:14px solid #F3EADB"><img src="{S('avantiura-88-5')}" alt="" style="object-position:50% 30%"></div>
  <p class="os" style="left:90px;bottom:220px;font-size:28px;letter-spacing:.22em;color:#F3EADB">«Авантюра» · SOLO · Obiimy</p>
  <p class="url" style="left:90px;bottom:150px;color:rgba(243,234,219,.8)">obiimy.world</p>''', "Manifesto: beauty is a way to keep yourself")

# ---------- 4. Decades triptych story
dec = [("1940-ті", "Сила — у бездоганній елегантності.", "zolote-44-2", "50% 25%"),
       ("1950-ті", "Правила починають руйнуватися. Колір, форма, сміливість.", "iskra-65-4", "50% 30%"),
       ("2026", "Свобода — самій обирати, якою бути.", "puls-44-3", "50% 30%")]
rows = "".join(f'''
  <div class="cover" style="left:0;right:0;top:{130 + k * 560}px;height:540px"><img src="{S(ph)}" alt="" style="object-position:{pos};{'filter:grayscale(1) contrast(1.1)' if k == 0 else ('filter:sepia(.35) saturate(1.2)' if k == 1 else '')}"></div>
  <div style="left:0;right:0;top:{130 + k * 560}px;height:540px;background:linear-gradient(90deg,rgba(12,9,8,.78),rgba(12,9,8,0) 70%)"></div>
  <p class="pf" style="left:70px;top:{180 + k * 560}px;font-size:110px;font-weight:900;font-style:italic;color:#F3EADB">{y}</p>
  <p class="cg" style="left:74px;width:540px;top:{330 + k * 560}px;font-size:44px;line-height:1.2;color:#F3EADB">{t}</p>''' for k, (y, t, ph, pos) in enumerate(dec))
ad("decades-01", "st", f'''
  <div class="fill" style="background:var(--ink)"></div>{rows}
  <p class="os" style="left:70px;top:70px;font-size:28px;letter-spacing:.3em;color:var(--gold)">SOLO · жіноча сила крізь десятиліття</p>
  <p class="cg" style="left:70px;right:70px;bottom:40px;font-size:34px;font-style:italic;color:rgba(243,234,219,.8)">Змінювалися епохи й силуети. Хустка залишалася поруч.</p>''', "Decades triptych")

# ---------- 5. Film stills
films = [("film-01-tysha", "tysha-88-3", "40% 50%", "— Куди ти?<br>— До себе.", "«Тиша всередині»"),
         ("film-02-krok", "krok-44-3", "50% 35%", "Не тому, що страх зникає.<br>А тому, що з’являється довіра до себе.", "«Сміливий крок»"),
         ("film-03-avantiura", "avantiura-88-3", "50% 30%", "Готовність вийти за межі звичного —<br>теж різновид сміливості.", "«Авантюра»")]
for fid, ph, pos, sub, name in films:
    ad(fid, "st film grain", f'''
  <div class="fill" style="background:#000"></div>
  <div class="cover" style="left:0;right:0;top:330px;height:1260px"><img src="{S(ph)}" alt="" style="object-position:{pos};filter:contrast(1.08) saturate(.9) sepia(.12)"></div>
  <p class="mono" style="left:0;right:0;top:130px;text-align:center;font-size:26px;letter-spacing:.3em;color:rgba(255,255,255,.7)">OBIIMY PRESENTS</p>
  <p class="solo" style="left:0;right:0;top:180px;text-align:center;font-size:110px;color:#F3EADB">SOLO</p>
  <div style="left:0;right:0;top:1330px;height:260px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.75))"></div>
  <p class="cg" style="left:70px;right:70px;top:1420px;text-align:center;font-size:52px;line-height:1.2;font-weight:500;color:#FFF3B0;text-shadow:0 2px 6px #000,0 0 18px rgba(0,0,0,.8)">{sub}</p>
  <p class="mono" style="left:0;right:0;top:1650px;text-align:center;font-size:26px;letter-spacing:.14em;color:rgba(255,255,255,.75)">У головній ролі — ви. Хустка {name}.</p>
  <p class="mono" style="left:0;right:0;top:1720px;text-align:center;font-size:24px;letter-spacing:.2em;color:rgba(255,255,255,.5)">obiimy.world</p>''', f"Film still {name}")

# ---------- 6. Boarding pass «Квиток до себе»
ad("ticket-01", "st", f'''
  <div class="fill cover"><img src="{S('zolote-44-5')}" alt="" style="object-position:50% 40%"></div>
  <div class="fill" style="background:linear-gradient(180deg,rgba(12,9,8,.1),rgba(12,9,8,.55))"></div>
  <div style="left:70px;right:70px;bottom:150px;height:720px;background:var(--paper);border-radius:28px;box-shadow:0 40px 80px -30px rgba(0,0,0,.6)" class="grain"></div>
  <p class="os" style="left:120px;bottom:790px;font-size:26px;letter-spacing:.3em;color:var(--ink3)">Посадковий талон · Obiimy</p>
  <p class="pf" style="left:118px;bottom:690px;font-size:78px;font-style:italic;font-weight:700;color:var(--ink)">Квиток до себе</p>
  <div style="left:120px;right:120px;bottom:470px;display:grid;grid-template-columns:1fr 1fr;gap:26px 40px">
    {''.join(f'<div style="position:static"><p class="mono" style="position:static;font-size:22px;letter-spacing:.2em;color:var(--ink3)">{a}</p><p class="mono" style="position:static;font-size:40px;font-weight:500;color:var(--ink)">{b}</p></div>' for a, b in [("Рейс", "SOLO 2026"), ("Місце", "1A, біля вікна"), ("Звідки", "Сумніви"), ("Куди", "До себе")])}
  </div>
  <div style="left:120px;right:120px;bottom:430px;border-top:3px dashed rgba(27,22,19,.3)"></div>
  <p class="mono" style="left:120px;right:120px;bottom:290px;font-size:30px;line-height:1.45;color:var(--ink2)">Ручна поклажа: шовкова хустка<br>«Золоте світло» · 44 × 44 · 2 400 грн</p>
  <p class="os" style="left:120px;bottom:200px;font-size:26px;letter-spacing:.2em;color:var(--wine)">Посадку відкрито · obiimy.world</p>
  <div style="right:120px;bottom:196px;width:210px;height:44px;background:repeating-linear-gradient(90deg,var(--ink) 0 4px,transparent 4px 9px,var(--ink) 9px 11px,transparent 11px 15px)"></div>''', "Boarding pass")

# ---------- 7. Four ways to wear (feed)
ways = [("На шиї", "puls-44-4", "50% 35%"), ("У волоссі", "avantiura-tw-3", "50% 40%"), ("На сумці", "iskra-tw-3", "50% 60%"), ("На зап’ясті", "puls-44-5", "60% 50%")]
cells = "".join(f'<div class="cover" style="position:relative"><img src="{S(ph)}" alt="" style="object-position:{pos}"><p class="os" style="position:absolute;left:24px;bottom:22px;font-size:30px;letter-spacing:.18em;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.6)">{t}</p></div>' for t, ph, pos in ways)
ad("ways-01", "fd", f'''
  <div class="fill" style="background:var(--paper)"></div>
  <p class="pf" style="left:60px;right:60px;top:56px;font-size:66px;line-height:1.05;font-weight:700">Одна хустка — <i style="font-weight:400">чотири способи</i> сказати про себе</p>
  <div style="left:60px;right:60px;top:250px;bottom:130px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:14px">{cells}</div>
  <p class="os" style="left:60px;bottom:58px;font-size:26px;letter-spacing:.2em;color:var(--ink3)">SOLO · Шлях до себе · твіллі від 1 600 грн</p>
  <div class="logo" style="right:60px;bottom:50px;height:34px"><img src="{LOGO_K}" alt=""></div>''', "Four ways to wear")

# ---------- 8. Palette of seven prints (feed)
chips = "".join(f'''<div style="position:static;display:grid;justify-items:center;gap:14px"><span style="width:210px;height:210px;border-radius:50%;background:url({S(p['flat'])}) center/135%;box-shadow:0 20px 30px -18px rgba(0,0,0,.5);border:6px solid #fff"></span><span class="cg" style="font-size:32px;font-style:italic;white-space:nowrap">«{p['name']}»</span></div>''' for p in P)
ad("palette-01", "fd", f'''
  <div class="fill grain" style="background:var(--paper)"></div>
  <p class="solo" style="left:0;right:0;top:60px;text-align:center;font-size:150px;color:var(--wine)">SOLO</p>
  <p class="os" style="left:0;right:0;top:220px;text-align:center;font-size:28px;letter-spacing:.3em;color:var(--ink2)">Сім принтів · сім станів</p>
  <div style="left:30px;right:30px;top:320px;display:grid;grid-template-columns:repeat(4,1fr);justify-items:center;gap:40px 10px">{chips}</div>
  <p class="cg" style="left:0;right:0;bottom:70px;text-align:center;font-size:36px;font-style:italic;color:var(--ink2)">Який із них — ваш? · obiimy.world</p>''', "Palette of seven")

# ---------- 9. Price page (story)
rows = [("Твіллі 84 × 5", "усі 7 принтів", "1 600"), ("Хустка 44 × 44", "«Пульс», «Золоте світло», «Сміливий крок»", "2 400"),
        ("Хустка 65 × 65", "«Іскра», «Флірт»", "4 800"), ("Шаль 88 × 88", "«Авантюра», «Тиша»", "6 600"), ("Резинка для волосся", "«Флірт»", "700")]
ad("price-01", "st", f'''
  <div class="fill grain" style="background:var(--paper)"></div>
  <div class="logo" style="left:90px;top:110px"><img src="{LOGO_K}" alt=""></div>
  <p class="os" style="right:90px;top:118px;font-size:26px;letter-spacing:.24em;color:var(--ink3)">Каталог · осінь 2026</p>
  <p class="solo" style="left:84px;top:220px;font-size:230px;color:var(--ink)">SOLO</p>
  <p class="pf" style="left:90px;top:440px;font-size:62px;font-style:italic;color:var(--wine)">Шлях до себе</p>
  <div class="shadow" style="left:90px;right:90px;top:570px;height:400px;background:url({S('krok-tw-4')}) 50% 35%/cover"></div>
  <div style="left:90px;right:90px;top:1010px;display:grid">
    {''.join(f'<div style="position:static;display:grid;grid-template-columns:1fr auto;align-items:baseline;border-bottom:2px solid rgba(27,22,19,.2);padding:20px 0"><p style="position:static"><span class="pf" style="font-size:46px;font-weight:700">{a}</span><br><span class="cg" style="font-size:32px;font-style:italic;color:var(--ink2)">{b}</span></p><p class="pf" style="position:static;font-size:50px">{c} <span style="font-size:30px">грн</span></p></div>' for a, b, c in rows)}
  </div>
  <p class="os" style="left:90px;bottom:90px;font-size:26px;letter-spacing:.2em;color:var(--ink3)">Натуральний шовк · двосторонній друк · obiimy.world</p>''', "Price list")

# ---------- 10. Newspaper front page (feed)
ad("gazette-01", "fd", f'''
  <div class="fill grain" style="background:#EFE7D6"></div>
  <p class="pf" style="left:50px;right:50px;top:40px;text-align:center;font-size:96px;font-weight:900;letter-spacing:-.01em">Жіночий вісник</p>
  <div style="left:50px;right:50px;top:160px;border-top:3px solid var(--ink);border-bottom:1px solid var(--ink);height:44px"></div>
  <p class="os" style="left:60px;right:60px;top:166px;font-size:22px;letter-spacing:.2em;display:flex;justify-content:space-between;line-height:32px"><span>Київ · осінь 2026</span><span>Спецвипуск SOLO</span><span>Ціна: ваша увага</span></p>
  <p class="pf" style="left:50px;right:50px;top:240px;font-size:104px;line-height:.98;font-weight:900;text-transform:uppercase">Жінка обирає себе. Знову.</p>
  <div class="cover" style="left:50px;width:560px;top:500px;height:760px"><img src="{S('krok-44-2')}" alt="" style="filter:grayscale(1) contrast(1.25);object-position:40% 30%"></div>
  <div style="left:50px;width:560px;top:500px;height:760px;background:radial-gradient(circle,rgba(0,0,0,.18) 1px,transparent 1.6px) 0 0/6px 6px;mix-blend-mode:multiply"></div>
  <p class="cg" style="left:640px;right:50px;top:500px;font-size:31px;line-height:1.28;text-align:justify;hyphens:auto">У 40-х жінка підкреслювала силу через бездоганну елегантність. У 50-х правила почали руйнуватися: колір, форма, власна ідентичність. <br><br>Український бренд Obiimy презентує колекцію SOLO — сім авторських принтів на натуральному шовку, сім станів на шляху жінки до себе.<br><br><b>Справжня свобода — самій обирати, якою бути.</b></p>
  <p class="os" style="left:640px;right:50px;bottom:92px;font-size:24px;letter-spacing:.14em;border-top:2px solid var(--ink);padding-top:14px">Читайте далі: obiimy.world</p>''', "Newspaper front page")

# ---------- 11. Poll story
opts = "".join(f'<div style="position:static;display:flex;align-items:center;gap:24px;background:rgba(243,234,219,.95);border-radius:999px;padding:14px 30px 14px 14px"><span style="width:76px;height:76px;border-radius:50%;background:url({S(p["flat"])}) center/140%;flex:none"></span><span class="pf" style="font-size:40px;font-style:italic">{p["name"]}</span><span class="cg" style="margin-left:auto;font-size:32px;font-style:italic;color:var(--ink2)">{p["short"].lower()}</span></div>' for p in P)
ad("poll-01", "st", f'''
  <div class="fill cover"><img src="{S('flirt-65-3')}" alt="" style="object-position:50% 40%;filter:blur(2px) brightness(.55)"></div>
  <p class="os" style="left:0;right:0;top:150px;text-align:center;font-size:28px;letter-spacing:.3em;color:#F2B705">SOLO · Obiimy</p>
  <p class="pf" style="left:80px;right:80px;top:210px;text-align:center;font-size:92px;line-height:1.02;font-weight:700;color:#fff">Який у тебе сьогодні стан?</p>
  <div style="left:80px;right:80px;top:520px;display:grid;gap:22px">{opts}</div>
  <p class="cg" style="left:80px;right:80px;bottom:130px;text-align:center;font-size:38px;font-style:italic;color:#F3EADB">Сім принтів — сім станів на шляху до себе</p>''', "Poll: which state are you in today")

# ---------- 12. Letter to yourself (story)
ad("letter-01", "st", f'''
  <div class="fill grain" style="background:#E6DAC4"></div>
  <div class="shadow" style="left:110px;right:110px;top:190px;height:1040px;background:#FBF6EC;transform:rotate(-2deg)" ></div>
  <p class="mk" style="left:180px;right:170px;top:280px;font-size:64px;line-height:1.35;color:#2A2230;transform:rotate(-2deg)">Дорога я!<br>Ти маєш право на красу — навіть зараз. Вдягни улюблену сукню, зав’яжи хустку, нафарбуй губи. Не для когось. Для себе.<br><span style="display:block;text-align:right;margin-top:40px">— Я</span></p>
  <div class="shadow" style="left:560px;top:1150px;width:420px;height:420px;background:url({S('flirt-65-1')}) center/cover;transform:rotate(7deg)"></div>
  <p class="os" style="left:110px;bottom:260px;font-size:28px;letter-spacing:.2em;color:var(--wine)">SOLO · Шлях до себе</p>
  <p class="cg" style="left:110px;width:420px;bottom:140px;font-size:34px;font-style:italic;color:var(--ink2)">Хустка «Флірт», 65 × 65 · obiimy.world</p>''', "Letter to yourself")

# ---------- 13. Minimal / slow fashion
ad("minimal-01-black", "st", f'''
  <div class="fill" style="background:#0F0D0C"></div>
  <p class="os" style="left:0;right:0;top:170px;text-align:center;font-size:28px;letter-spacing:.5em;color:rgba(243,234,219,.6)">Obiimy</p>
  <div style="left:190px;right:190px;top:430px;height:700px;background:url({S('tysha-tw-1')}) center/contain no-repeat;filter:invert(0)"></div>
  <p class="solo" style="left:0;right:0;top:1250px;text-align:center;font-size:190px;color:#F3EADB">SOLO</p>
  <p class="cg" style="left:0;right:0;top:1440px;text-align:center;font-size:52px;font-style:italic;color:rgba(243,234,219,.85)">Шлях до себе</p>
  <p class="url" style="left:0;right:0;bottom:130px;text-align:center;color:rgba(243,234,219,.6)">obiimy.world</p>''', "Minimal black")
ad("minimal-02-slow", "fd", f'''
  <div class="fill grain" style="background:var(--paper)"></div>
  <div class="cover" style="left:0;top:0;bottom:0;width:540px"><img src="{S('puls-tw-3')}" alt="" style="object-position:50% 30%"></div>
  <p class="os" style="left:600px;top:120px;font-size:26px;letter-spacing:.3em;color:var(--ink3)">Slow fashion</p>
  <p class="pf" style="left:596px;right:60px;top:190px;font-size:74px;line-height:1.05;font-weight:700">У світі швидких трендів —</p>
  <p class="pf" style="left:596px;right:60px;top:460px;font-size:74px;line-height:1.05;font-style:italic;color:var(--wine)">речі зі змістом.</p>
  <p class="cg" style="left:600px;right:60px;top:700px;font-size:38px;line-height:1.3;color:var(--ink2)">Аксесуари, які стають частиною особистої історії своєї власниці.</p>
  <p class="os" style="left:600px;bottom:130px;font-size:26px;letter-spacing:.2em;color:var(--ink)">SOLO · «Пульс»</p>
  <div class="logo" style="left:600px;bottom:60px;height:34px"><img src="{LOGO_K}" alt=""></div>''', "Slow fashion")

# ---------- 14. Double-sided print (square)
ad("double-01", "sq", f'''
  <div class="fill" style="background:{P[0]['c']}"></div>
  <div class="fill grain"></div>
  <p class="pf" style="left:110px;right:110px;top:100px;font-size:100px;line-height:1;font-weight:700;color:#fff">Двосторонній друк</p>
  <div class="shadow" style="right:100px;top:330px;width:440px;height:440px;background:url({S('iskra-65-5')}) center/cover #fff;transform:rotate(-7deg)"></div>
  <p class="cg" style="left:110px;width:390px;top:360px;font-size:42px;line-height:1.3;color:rgba(255,255,255,.92)">Принт однаково яскравий з обох боків — хустку можна носити як завгодно.</p>
  <p class="os" style="left:120px;bottom:120px;font-size:30px;letter-spacing:.2em;color:#fff">«Іскра» · 65 × 65 · 4 800 грн</p>
  <p class="url" style="left:120px;bottom:70px;color:rgba(255,255,255,.8)">obiimy.world</p>''', "Double-sided print")

# ---------- 15. Story version of a cover (for Stories placement)
p = P[4]
ad("cover-story-avantiura", "st", f'''
  <div class="fill cover"><img src="{S('avantiura-88-4')}" alt="" style="object-position:50% 35%"></div>
  <div style="left:0;right:0;top:0;height:700px;background:linear-gradient(180deg,rgba(15,10,8,.6),transparent)"></div>
  <div style="left:0;right:0;bottom:0;height:800px;background:linear-gradient(0deg,rgba(15,10,8,.85),transparent)"></div>
  <p class="solo" style="left:0;right:0;top:140px;text-align:center;font-size:360px;color:#F3EADB">SOLO</p>
  <p class="os" style="left:0;right:0;top:440px;text-align:center;font-size:28px;letter-spacing:.34em;color:#F3EADB">Шовкова свобода · жіноча сила крізь десятиліття</p>
  <p class="pf" style="left:80px;right:80px;bottom:420px;font-size:100px;line-height:1;font-weight:700;color:#fff">«Авантюра»</p>
  <p class="cg" style="left:84px;right:80px;bottom:300px;font-size:44px;font-style:italic;color:#F3EADB">{p['state']}</p>
  <p class="os" style="left:84px;bottom:180px;font-size:30px;letter-spacing:.2em;color:#F2B705">Шаль 88 × 88 · 6 600 грн · твіллі 1 600 грн</p>''', "Story cover Avantiura")

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · SOLO creatives</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700;1,900&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Oswald:wght@400;500;600&family=Marck+Script&family=IBM+Plex+Mono:wght@400;500&family=Onest:wght@300;400;500;600&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / "solo.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "creatives")
