"""SOLO — original concepts from scratch (1080×1920, plain banner).
Seven ideas, none of them a photo with a plate: postage stamps, a dictionary, a concert programme,
a museum wall, a contact sheet, a care label, a weekly planner.
Copy: press release (review/SOLO-RELEASE.md); facts and prices: obiimy.world. Output: solo9.html → out9/*.jpg"""
import pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit import P, PP, S, CUT, HI, nb, LOGO_W, LOGO_K, GRAIN

PRICE = {"iskra": "4 800", "flirt": "4 800", "puls": "2 400", "zolote": "2 400", "avantiura": "6 600", "tysha": "6 600", "krok": "2 400"}
SIZE = {"iskra": "65 × 65", "flirt": "65 × 65", "puls": "44 × 44", "zolote": "44 × 44", "avantiura": "88 × 88", "tysha": "88 × 88", "krok": "44 × 44"}
INK, CREAM, YELLOW = "#141216", "#F3EADB", "#F2B705"

CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #555; font-family: 'Onest', Arial, sans-serif; -webkit-font-smoothing: antialiased; }
.ad { width: 1080px; height: 1920px; position: relative; overflow: hidden; margin: 20px auto; }
.ad p, .ad h1 { margin: 0; }
.ad::after { content: ""; position: absolute; inset: 0; z-index: 90; pointer-events: none; opacity: .26; mix-blend-mode: soft-light; background-image: GRAIN; }
.a { position: absolute; }
.lbl { font-family: 'Montserrat', sans-serif; font-size: 26px; font-weight: 500; letter-spacing: .16em; text-transform: uppercase; white-space: nowrap; }
.kick { font-family: 'Montserrat', sans-serif; font-size: 27px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; }
.h { font-family: 'Playfair Display', serif; font-weight: 700; line-height: 1.02; letter-spacing: -.01em; text-wrap: balance; }
.h em { font-style: italic; font-weight: 700; }
.tag { font-family: 'EB Garamond', serif; font-style: italic; font-weight: 500; font-size: 44px; line-height: 1.16; text-wrap: balance; }
.cta { font-family: 'Onest'; font-weight: 600; font-size: 30px; padding: 24px 38px; border-radius: 999px; white-space: nowrap; flex: none; }
.hand { font-family: 'Marck Script', cursive; }
""".replace("GRAIN", GRAIN)

ads = []
def ad(id, bg, body, note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad" id="{id}" style="background:{bg}">{body}\n</section>')

def head(dark=True):
    col = CREAM if dark else "#4A4750"
    return (f'<img class="a" src="{LOGO_W if dark else LOGO_K}" alt="Obiimy" style="left:64px;top:56px;height:44px">'
            f'<p class="a lbl" style="right:64px;top:66px;color:{col}">Шовкові вироби</p>')

def foot(product, cta, dark=True, tagline=""):
    cuts, title, price = product
    fg = CREAM if dark else INK
    thumbs = "".join(f'<img src="{CUT(c)}" alt="" style="height:112px;width:auto;max-width:112px;object-fit:contain;margin-left:{0 if i == 0 else -52}px;filter:drop-shadow(0 8px 10px rgba(0,0,0,.35));transform:rotate({(-6, 5, -3)[i]}deg)">' for i, c in enumerate(cuts))
    plate = "background:rgba(243,234,219,.1);border:1.5px solid rgba(243,234,219,.3)" if dark else "background:rgba(255,255,255,.55);border:1.5px solid rgba(20,18,22,.2)"
    btn = f"background:{YELLOW};color:{INK}" if dark else f"background:{INK};color:{CREAM}"
    tl = f'<p class="a tag" style="left:64px;right:64px;bottom:232px;color:{fg}">{nb(tagline)}</p>' if tagline else ""
    return tl + f'''
  <div class="a" style="left:64px;right:64px;bottom:60px;display:flex;align-items:center;justify-content:space-between;gap:24px;color:{fg}">
    <div style="display:flex;align-items:center;gap:20px;padding:12px 28px 12px 14px;border-radius:20px;{plate};flex:0 1 auto;min-width:0">
      <div style="display:flex;align-items:center;flex:none">{thumbs}</div>
      <div style="min-width:0"><p style="font-size:29px;font-weight:600;line-height:1.18;text-wrap:balance">{nb(title)}</p><p style="font-family:'Playfair Display',serif;font-size:46px;line-height:1.05;margin-top:4px;white-space:nowrap">{price}</p></div>
    </div>
    <div class="cta" style="{btn}">{cta}</div>
  </div>'''

def lockup(dark=True, top=150, align="left"):
    col = "rgba(243,234,219,.78)" if dark else "#6B5F55"
    pos = "left:64px" if align == "left" else "left:0;right:0;text-align:center"
    return f'<p class="a kick" style="{pos};top:{top}px;color:{col}">Колекція Соло · Шлях до себе</p>'

# ═════════════════════════════════════════════ 1. POSTAGE STAMPS
def stamp(pid, cw, ch, s=30, left=0, top=0, rot=0, kind="scarf", price=True):
    """A perforated stamp: the print, its name and the price as the denomination. Size = cw×ch cells of s px."""
    p = PP[pid]; W, H = cw * s, ch * s; r = int(s * .3)
    mask = (f"linear-gradient(#000,#000) {s // 2}px {s // 2}px/calc(100% - {s}px) calc(100% - {s}px) no-repeat,"
            f"radial-gradient(circle at center,transparent {r}px,#000 {r + 1}px) -{s // 2}px -{s // 2}px/{s}px {s}px")
    k = W / 270
    cut = p["flat"] if kind == "scarf" else p["tw"]
    denom = PRICE[pid] if kind == "scarf" else "1 600"
    small = f'<p style="font-family:Montserrat,sans-serif;font-weight:500;font-size:{max(20, int(10 * k))}px;letter-spacing:.14em;text-transform:uppercase;color:#6B5F55;white-space:nowrap">Соло · 2026</p>' if k > 1.6 else "<span></span>"
    cost = (f'<p style="font-family:Playfair Display,serif;font-weight:700;font-size:{max(30, int(28 * k))}px;line-height:1;white-space:nowrap">{denom}'
            + (f'<span style="font-family:Onest;font-weight:600;font-size:{max(26, int(11 * k))}px;letter-spacing:.04em;margin-left:{int(4 * k)}px">грн</span>' if k > 1.6 else "") + '</p>') if price else ""
    return f'''
  <div class="a" style="left:{left}px;top:{top}px;width:{W}px;height:{H}px;transform:rotate({rot}deg);filter:drop-shadow(0 {int(14 * k)}px {int(18 * k)}px rgba(0,0,0,.4))">
    <div style="position:absolute;inset:0;background:#FBF6EC;-webkit-mask:{mask};mask:{mask}">
      <div style="position:absolute;left:{s}px;right:{s}px;top:{s}px;bottom:{int(98 * k) + s // 2}px;background:radial-gradient(80% 80% at 50% 40%,rgba(255,255,255,.25),rgba(255,255,255,0) 70%),linear-gradient(160deg,{p['c']},{p['deep']});display:grid;place-items:center;overflow:hidden">
        <img src="{CUT(cut)}" alt="" style="width:80%;height:80%;object-fit:contain;transform:rotate(-5deg);filter:drop-shadow(0 {int(8 * k)}px {int(10 * k)}px rgba(0,0,0,.4))"></div>
      <div style="position:absolute;left:{s}px;right:{s}px;bottom:{s // 2 + int(6 * k)}px;height:{int(84 * k)}px;display:flex;flex-direction:column;justify-content:flex-end;color:{INK}">
        <p style="font-family:'Playfair Display',serif;font-style:italic;font-weight:700;font-size:{max(26, int(27 * k))}px;line-height:1.05;white-space:nowrap">{p['name']}</p>
        <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:{int(5 * k)}px">{small}{cost}</div>
      </div>
    </div>
  </div>'''

def postmark(left, top, size=300, rot=-14, col="rgba(20,18,22,.72)", waves=True):
    return f'''
  <svg class="a" viewBox="0 0 520 300" style="left:{left}px;top:{top}px;width:{int(size * 520 / 300)}px;height:{size}px;transform:rotate({rot}deg);mix-blend-mode:multiply" fill="none" stroke="{col}">
    <defs><path id="pm" d="M150,150 m-108,0 a108,108 0 1,1 216,0 a108,108 0 1,1 -216,0"/></defs>
    <circle cx="150" cy="150" r="140" stroke-width="5"/><circle cx="150" cy="150" r="86" stroke-width="3"/>
    <text font-family="Montserrat" font-weight="500" font-size="24" letter-spacing="5" fill="{col}" stroke="none"><textPath href="#pm">КОЛЕКЦІЯ СОЛО · ШЛЯХ ДО СЕБЕ ·</textPath></text>
    <text x="150" y="146" text-anchor="middle" font-family="Playfair Display" font-weight="700" font-size="46" fill="{col}" stroke="none">2026</text>
    <text x="150" y="182" text-anchor="middle" font-family="Montserrat" font-weight="500" font-size="19" letter-spacing="4" fill="{col}" stroke="none">OBIIMY</text>
    {"".join(f'<path d="M300,{96 + i * 36} q27,-18 54,0 t54,0 t54,0 t54,0" stroke-width="5"/>' for i in range(4)) if waves else ""}
  </svg>'''

PAPER = "radial-gradient(120% 80% at 50% 30%,#EFE6D4,#DDD0B8)"
# 1a — a sheet of seven stamps
s_, cw, ch = 32, 9, 11
W, H, gap = cw * s_, ch * s_, 24
rows = [["iskra", "flirt"], ["puls", "zolote", "avantiura"], ["tysha", "krok"]]
body = head(False) + lockup(False, 160) + f'<h1 class="a h" style="left:64px;right:64px;top:206px;font-size:88px;color:{INK}">Сім марок<br><em>на шляху до себе.</em></h1>'
for r, row in enumerate(rows):
    x0 = (1080 - (len(row) * W + (len(row) - 1) * gap)) // 2
    for c, pid in enumerate(row):
        body += stamp(pid, cw, ch, s_, x0 + c * (W + gap), 432 + r * (H + gap), rot=(-2, 1.5, -1, 2, -1.5, 1, -2)[(r * 3 + c) % 7])
body += postmark(778, 344, 190, -12, waves=False)
body += foot((["iskra-65-1", "avantiura-88-1", "krok-44-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Обрати принт", False, "Сім авторських принтів. Двосторонній друк.")
ad("o01-stamps-sheet", PAPER, body, "Stamps: the sheet of seven")

# 1b — one big stamp, the delivery fact
body = head(True) + lockup(True, 160) + f'<h1 class="a h" style="left:64px;right:64px;top:212px;font-size:100px;color:{CREAM}">Поштою —<br><em style="color:#E9D7A6">до себе.</em></h1>'
body += stamp("avantiura", 20, 25, 36, 180, 500, rot=-3)
body += foot((["avantiura-88-1"], "Шовкова хустка «Авантюра»", "6 600 грн"), "Обрати хустку", True, "Замовлення до 16:00 відправимо Новою поштою того\u00a0ж\u00a0дня.")
ad("o02-stamp-avantiura", "radial-gradient(90% 60% at 50% 45%,#5A1A1E,#2A0D10 80%)", body, "Stamps: one stamp and same-day dispatch")

# 1c — a postcard with the giver's words
card = f'''
  <div class="a" style="left:80px;top:500px;width:920px;height:600px;background:#FBF6EC;transform:rotate(-3deg);box-shadow:0 40px 70px -30px rgba(0,0,0,.6)">
    <div style="position:absolute;left:50%;top:60px;bottom:60px;width:2px;background:rgba(20,18,22,.25)"></div>
    <p class="hand" style="position:absolute;left:54px;top:84px;width:400px;font-size:66px;line-height:1.14;color:#2B3A67">Мамо,<br>це тобі.<br>Просто так.</p>
    <p class="hand" style="position:absolute;left:54px;bottom:70px;font-size:52px;color:#2B3A67">Обіймаю, О.</p>
    <p style="position:absolute;left:520px;top:392px;font-family:Montserrat;font-size:20px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:#8A8592">Приклад підпису</p>
    <p style="position:absolute;left:520px;right:60px;top:428px;font-family:'EB Garamond',serif;font-style:italic;font-size:38px;line-height:1.15;color:#4A4750">Текст — ваш.<br>Підпис додамо до подарунка.</p>
  </div>'''
body = head(True) + lockup(True, 160) + f'<h1 class="a h" style="left:64px;right:64px;top:212px;font-size:88px;color:{CREAM}">Підпишемо подарунок<br><em style="color:#E9D7A6">вашими словами.</em></h1>'
body += f'<img class="a" src="{CUT("flirt-65-1")}" alt="" style="left:330px;top:1080px;width:460px;transform:rotate(7deg);filter:drop-shadow(0 40px 50px rgba(0,0,0,.5))">'
body += card + stamp("flirt", 9, 11, 26, 730, 560, rot=2, price=False)
body += foot((["flirt-65-1"], "Шовкова хустка «Флірт»", "4 800 грн"), "Обрати подарунок", True, "Індивідуальне пакування.<br>Замовлення до 16:00 відправимо того\u00a0ж\u00a0дня.")
ad("o03-postcard-gift", "radial-gradient(90% 60% at 50% 45%,#5C6B45,#2A3320 80%)", body, "Stamps: postcard, gift note in your words")

body = head(True) + lockup(True, 160) + f'<h1 class="a h" style="left:64px;right:64px;top:212px;font-size:100px;color:{CREAM}">Поштою —<br><em style="color:#E9D7A6">до неї.</em></h1>'
body += stamp("zolote", 20, 25, 36, 180, 480, rot=-3, price=False)
body += foot((["zolote-44-1"], "Шовкова хустка «Золоте світло»", "2 400 грн"), "Надіслати подарунок", True, "Замовлення до 16:00 відправимо того\u00a0ж\u00a0дня.<br>Подарунок підпишемо вашими словами.")
ad("o21-stamp-gift", "radial-gradient(90% 60% at 50% 45%,#6B4414,#2C1B08 80%)", body, "Stamps: a gift by post")

body = head(False) + lockup(False, 160) + f'<h1 class="a h" style="left:64px;right:64px;top:212px;font-size:82px;color:{INK};white-space:nowrap">Хустка — одразу.<br><em>Оплата — частинами.</em></h1>'
body += stamp("tysha", 20, 25, 36, 180, 500, rot=3) + postmark(784, 384, 240, -12, waves=False)
body += foot((["tysha-88-1"], "Шовкова хустка «Тиша всередині»", "6 600 грн"), "Обрати хустку", False, "Оплата частинами: ПриватБанк — 4 платежі, monobank — 3.")
ad("o20-stamp-tysha-parts", PAPER, body, "Stamps: payment in parts")

# ═════════════════════════════════════════════ 2. DICTIONARY
def entry(id, pid, word, gram, defs, see, letter, fs=170):
    p = PP[pid]
    items = "".join(f'<p style="display:flex;gap:22px;margin-top:{0 if i == 0 else 26}px"><span style="font-family:\'Playfair Display\',serif;font-weight:700;color:#7B1F24;flex:none;width:52px">{i + 1}.</span><span>{nb(d)}</span></p>' for i, d in enumerate(defs))
    body = head(False) + f'''
  <p class="a" style="right:40px;top:120px;font-family:'Playfair Display',serif;font-weight:900;font-size:620px;line-height:.8;color:rgba(20,18,22,.06)">{letter}</p>
  <p class="a kick" style="left:64px;top:160px;color:#6B5F55">Словник колекції Соло</p>
  <div class="a" style="left:64px;top:222px;width:952px;height:3px;background:{INK}"></div>
  <h1 class="a h" style="left:64px;right:64px;top:270px;font-size:{fs}px;line-height:.95;color:{INK}">{word}</h1>
  <div class="a" style="left:64px;top:{270 + (fs if "<br>" not in word else 2 * fs) + 40}px;width:900px;color:{INK}">
    <p style="font-family:'EB Garamond',serif;font-style:italic;font-size:42px;color:#6B5F55">{gram}</p>
    <div style="font-family:'EB Garamond',serif;font-weight:500;font-size:46px;line-height:1.18;margin-top:30px">{items}</div>
    <p style="font-family:'EB Garamond',serif;font-style:italic;font-size:40px;color:#6B5F55;margin-top:34px">Пор.: {see}.</p>
  </div>
  <img class="a" src="{CUT(p['flat'])}" alt="" style="left:340px;top:{1120 if "<br>" in word else 1050}px;width:{510 if "<br>" in word else 590}px;transform:rotate(6deg);filter:drop-shadow(0 30px 36px rgba(40,25,10,.4))">
  <p class="a" style="left:64px;top:1420px;width:230px;font-family:'EB Garamond',serif;font-style:italic;font-size:36px;line-height:1.15;color:#6B5F55">мал. 1.<br>Хустка<br>«{p['name']}»</p>'''
    body += foot(([p["flat"]], f"Шовкова хустка «{p['name']}»", f"{PRICE[pid]} грн"), "Обрати хустку", False)
    ad(id, "linear-gradient(180deg,#F4EEE1,#ECE3D2)", body, f"Dictionary: {p['name']}")

entry("o04-dict-flirt", "flirt", "флірт", "ім., ч. р.",
      ["Насамперед стан, уміння насолоджуватися собою, життям і моментом.", "Шовкова хустка 65 × 65 см. Двосторонній друк, край оброблено вручну."], "іскра, авантюра", "Ф")
entry("o05-dict-tysha", "tysha", "ти́ша<br>всере́дині", "словоспол.",
      ["Баланс і здатність чути себе серед зовнішнього шуму, стан, у якому більше не потрібно доводити, поспішати чи відповідати чужим очікуванням.", "Шовкова хустка 88 × 88 см. Двосторонній друк, край оброблено вручну."], "пульс, золоте світло", "Т", fs=132)
entry("o06-dict-krok", "krok", "сміли́вий<br>крок", "словоспол.",
      ["Рішення рухатися вперед навіть тоді, коли немає повної визначеності.", "Шовкова хустка 44 × 44 см. Двосторонній друк, край оброблено вручну."], "довіра до себе", "С", fs=150)

# ═════════════════════════════════════════════ 3. CONCERT PROGRAMME — «Соло»
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII"]
def staff(top, gap=44, col="rgba(243,234,219,.5)"):
    return "".join(f'<div class="a" style="left:0;right:0;top:{top + i * gap}px;height:2px;background:{col}"></div>' for i in range(5))
def note(pid, cx, cy, d=132, stem=True, up=True):
    p = PP[pid]
    st = f'<div class="a" style="left:{cx + d // 2 - 5}px;top:{cy - 180}px;width:5px;height:180px;background:{CREAM}"></div>' if stem and up else (f'<div class="a" style="left:{cx - d // 2}px;top:{cy}px;width:5px;height:180px;background:{CREAM}"></div>' if stem else "")
    return st + f'<div class="a" style="left:{cx - d // 2}px;top:{cy - d // 2}px;width:{d}px;height:{d}px;border-radius:50%;background:url({HI(p)}) center/210%;box-shadow:0 0 0 5px {CREAM},0 18px 30px rgba(0,0,0,.5);transform:rotate(-14deg)"></div>'
body = head(True) + lockup(True, 160) + f'<h1 class="a h" style="left:64px;right:64px;top:212px;font-size:104px;color:{CREAM}">Соло в семи<br>частинах. <em style="color:#E9D7A6">Виконуєте ви.</em></h1>'
body += staff(780)
ys = [956, 912, 868, 824, 780, 912, 824]
for i, p in enumerate(P):
    body += note(p["id"], 110 + i * 143, ys[i], 124, up=ys[i] >= 868)
prog = "".join(f'<div style="display:flex;align-items:baseline;gap:22px;padding:10px 0;border-bottom:1.5px solid rgba(243,234,219,.22)"><span style="font-family:\'Playfair Display\',serif;font-weight:700;font-size:34px;color:#E0B040;width:70px;flex:none">{ROMAN[i]}</span><span style="font-family:\'Playfair Display\',serif;font-style:italic;font-weight:700;font-size:42px;white-space:nowrap">{p["name"]}</span><span style="font-family:\'EB Garamond\',serif;font-size:36px;color:rgba(243,234,219,.78);margin-left:auto;text-align:right;white-space:nowrap">{p["short"].lower() if p["id"] != "flirt" else "насолода моментом"}</span></div>' for i, p in enumerate(P))
body += f'<div class="a" style="left:64px;right:64px;top:1130px;color:{CREAM}">{prog}</div>'
body += foot((["iskra-65-1", "tysha-88-1", "krok-44-1"], "Шовкові хустки SOLO", "від 2 400 грн"), "Обрати принт", True)
ad("o07-solo-programme", "radial-gradient(100% 60% at 50% 35%,#2B2140,#120E1C 80%)", body, "Concert programme: seven parts")

# ═════════════════════════════════════════════ 4. MUSEUM WALL
def museum(id, pid, h1, em, frame="#241C17", hs=96, extra="Край оброблено вручну.", tagline="", cta="Обрати хустку", tl_w=0):
    p = PP[pid]
    body = head(False) + lockup(False, 160) + f'<h1 class="a h" style="left:64px;right:64px;top:212px;font-size:{hs}px;color:{INK};white-space:nowrap">{h1}<br><em>{em}</em></h1>'
    body += f'''
  <div class="a" style="left:0;right:0;top:0;height:1300px;background:radial-gradient(60% 46% at 50% 56%,rgba(255,255,255,.55),rgba(255,255,255,0) 70%)"></div>
  <div class="a" style="left:140px;top:480px;width:800px;height:800px;background:{frame};padding:22px;box-shadow:0 50px 60px -24px rgba(40,30,20,.55),0 6px 10px rgba(40,30,20,.3)">
    <div style="width:100%;height:100%;background:#F6F1E7;padding:44px;box-shadow:inset 0 0 0 2px rgba(20,18,22,.12),inset 0 6px 14px rgba(20,18,22,.18)">
      <div style="width:100%;height:100%;display:grid;place-items:center"><img src="{CUT(p['flat'])}" alt="" style="width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 10px 14px rgba(40,30,20,.35))"></div></div></div>
  <div class="a" style="left:576px;top:1330px;width:440px;background:#FDFCF9;padding:28px 32px;box-shadow:0 10px 18px -8px rgba(40,30,20,.4);color:{INK}">
    <p style="font-family:Onest;font-weight:600;font-size:30px">Світлана Сніжко</p>
    <p style="font-family:'EB Garamond',serif;font-style:italic;font-size:{38 if len(p['name']) < 12 else 32}px;line-height:1.15;margin-top:6px;white-space:nowrap">«{p['name']}», 2026</p>
    <p style="font-family:Onest;font-size:26px;line-height:1.35;color:#4A4750;margin-top:10px">Шовк, двосторонній друк.<br>{SIZE[pid]} см.<br>{extra}</p></div>'''
    body += foot(([p["flat"]], f"Шовкова хустка «{p['name']}»", f"{PRICE[pid]} грн"), cta, False, "" if tl_w else tagline)
    if tl_w: body += f'<p class="a tag" style="left:64px;top:1400px;width:{tl_w}px;color:{INK}">{tagline}</p>'
    ad(id, "linear-gradient(180deg,#DDD6CA 0%,#D3CBBD 72%,#BDB4A4 72.2%,#C9C0B1 100%)", body, f"Museum wall: {p['name']}")
museum("o09-museum-avantiura", "avantiura", "Експонат,", "який можна носити.", hs=88)
museum("o10-museum-zolote", "zolote", "Просимо", "торкатися.", "#8A6A2C")
museum("o11-museum-iskra", "iskra", "Приміряти", "дозволено.", "#1E3556")
museum("o17-museum-tysha", "tysha", "Просимо дотримуватися", "тиші всередині.", "#1B1815", hs=78)
museum("o18-museum-krok", "krok", "Можна підійти", "ближче.", "#3B2A22")
museum("o23-museum-gift", "avantiura", "Експонат, який", "можна подарувати.", "#3A1114", hs=88, extra="Підпис до подарунка —<br>вашими словами.", cta="Подарувати", tagline="Індивідуальне пакування.<br>Доставка по Україні безкоштовна.", tl_w=470)

# ═════════════════════════════════════════════ 5. CONTACT SHEET
FW, FH = 620, 420
def strip(top, frames, shift, first_no, pick=None):
    """A strip of 35 mm film: frames 620×420, sprocket holes, edge numbers. pick = index of the circled frame."""
    holes = "repeating-linear-gradient(90deg,rgba(233,228,218,0) 0 24px,rgba(233,228,218,.4) 24px 44px,rgba(233,228,218,0) 44px 68px)"
    out = f'<div class="a" style="left:0;right:0;top:{top}px;height:{FH + 84}px;background:#0B0A09"></div>'
    out += f'<div class="a" style="left:0;right:0;top:{top + 8}px;height:13px;background:{holes};background-position:{shift}px 0"></div>'
    out += f'<div class="a" style="left:0;right:0;top:{top + FH + 58}px;height:13px;background:{holes};background-position:{shift}px 0"></div>'
    for i, (ph, pos) in enumerate(frames):
        x = shift + i * (FW + 22)
        out += f'<div class="a" style="left:{x}px;top:{top + 42}px;width:{FW}px;height:{FH}px;background:url({S(ph)}) {pos} no-repeat"></div>'
        if 0 <= x and x + 330 <= 1080: out += f'<p class="a" style="left:{x + 10}px;top:{top + 28}px;font-family:Montserrat;font-weight:500;font-size:13px;letter-spacing:.2em;color:#E0B040;line-height:1;white-space:nowrap">{first_no + i} &nbsp; OBIIMY SOLO &nbsp; {first_no + i}A</p>'
        if pick == i:
            out += f'''<svg class="a" viewBox="0 0 520 380" style="left:{x - 50}px;top:{top - 6}px;width:{FW + 100}px;height:{FH + 96}px;overflow:visible" fill="none" stroke="{YELLOW}" stroke-width="6" stroke-linecap="round">
      <path d="M262,22 C420,10 508,90 500,196 C492,306 380,366 250,360 C110,354 14,290 22,180 C30,76 130,28 290,30"/></svg>
  <p class="a hand" style="left:{x + FW - 150}px;top:{top - 58}px;font-size:76px;color:{YELLOW};transform:rotate(-7deg);text-shadow:0 2px 10px rgba(0,0,0,.8)">оцей!</p>'''
    return out
def contact(id, pid, rows, pick_row, pick, h1, em, tagline, product, cta, hs=100):
    p = PP[pid]
    body = head(True) + f'<p class="a kick" style="left:64px;top:160px;color:rgba(243,234,219,.78)">Контактний аркуш · «{p["name"]}»</p>'
    body += f'<h1 class="a h" style="left:64px;right:64px;top:212px;font-size:{hs}px;color:{CREAM}">{h1} <em style="color:#E9D7A6">{em}</em></h1>'
    for r, (frames, shift) in enumerate(rows):
        body += strip(470 + r * 540, frames, shift, 11 + r * 3, pick if r == pick_row else None)
    body += foot(product, cta, True, tagline)
    ad(id, "#161412", body, f"Contact sheet: {p['name']}")
contact("o12-contact-iskra", "iskra",
        [([("iskra-tw-3", "50% 66%/100%"), ("iskra-65-3", "50% 45%/100%")], -200),
         ([("iskra-tw-2", "55% 34%/150%"), ("iskra-65-2", "50% 24%/100%")], -262)],
        1, 1, "Обираю", "цей кадр.", "Серед усіх кадрів — той, де вас помітно.",
        (["iskra-65-1", "iskra-tw-4"], "Хустка й твіллі «Іскра»", "від 1 600 грн"), "Обрати «Іскру»")
contact("o13-contact-krok", "krok",
        [([("krok-44-3", "30% 86%/170%"), ("krok-44-3", "50% 32%/100%")], -200),
         ([("krok-44-2", "52% 60%/190%"), ("krok-44-2", "50% 36%/100%")], -262)],
        1, 1, "Крок, після якого", "не озираються.", "Рішення рухатися вперед — з довірою до себе.",
        (["krok-44-1"], "Хустка «Сміливий крок» 44 × 44 см", "2 400 грн"), "Обрати хустку", hs=84)

# ═════════════════════════════════════════════ 6. CARE LABEL
def label(id, pid, lines, h1, em, care=True, cta="Обрати хустку", hs=96, bg=None):
    """A hang tag tied to the scarf: the scarf lies whole on the colour of its print, the tag is the copy."""
    p = PP[pid]
    def row(a, b):
        num = a.endswith("%")
        if not num:
            return (f'<div style="padding:16px 0;border-bottom:2px solid rgba(20,18,22,.16)"><p style="font-family:Montserrat;font-weight:500;font-size:20px;letter-spacing:.18em;text-transform:uppercase;color:#6B5F55">{a}</p>'
                    f'<p style="font-family:Onest;font-weight:500;font-size:31px;line-height:1.2;margin-top:6px">{b}</p></div>')
        left = f"font-size:{70 if num else 38}px;" + ("" if num else "font-style:italic;")
        return (f'<div style="display:flex;justify-content:space-between;align-items:baseline;gap:18px;padding:18px 0;border-bottom:2px solid rgba(20,18,22,.16)">'
                f'<span style="font-family:Playfair Display,serif;font-weight:700;{left}line-height:1;white-space:nowrap">{a}</span>'
                f'<span style="font-family:Onest;font-weight:500;font-size:27px;line-height:1.15;text-align:right">{b}</span></div>')
    rows = "".join(row(a, b) for a, b in lines)
    caret = ('<p style="font-family:Montserrat;font-weight:500;font-size:22px;letter-spacing:.2em;text-transform:uppercase;color:#6B5F55;margin-top:34px">Догляд</p>'
             '<p style="font-family:Onest;font-weight:500;font-size:30px;line-height:1.3;margin-top:10px">Прасувати в режимі «шовк».</p>') if care else ""
    base = bg or f'linear-gradient(165deg,{p["c"]},{p["deep"]} 60%,color-mix(in srgb,{p["deep"]} 60%,#000))'
    body = f'<div class="a" style="inset:0;background:radial-gradient(80% 50% at 62% 66%,rgba(255,255,255,.2),rgba(255,255,255,0) 70%),{base}"></div>'
    body += head(True) + lockup(True, 160) + f'<h1 class="a h" style="left:64px;right:64px;top:212px;font-size:{hs}px;color:{CREAM}">{h1}<br><em style="color:#E9D7A6">{em}</em></h1>'
    body += f'''
  <img class="a" src="{CUT(p['flat'])}" alt="" style="left:400px;top:900px;width:620px;transform:rotate(-7deg);filter:drop-shadow(0 50px 60px rgba(0,0,0,.5))">
  <svg class="a" viewBox="0 0 400 500" style="left:270px;top:400px;width:440px;height:600px;overflow:visible" fill="none" stroke="#E9E1D0" stroke-width="4" stroke-linecap="round"><path d="M38,196 C120,60 300,40 360,300 C372,360 360,420 330,470"/></svg>
  <div class="a" style="left:64px;top:540px;width:500px;height:{720 if care else 810}px;background:linear-gradient(100deg,#FBF9F4,#F1EDE4 50%,#FBF9F4);border-radius:14px;transform:rotate(4deg);box-shadow:0 40px 60px -26px rgba(0,0,0,.65),0 4px 8px rgba(0,0,0,.3);color:{INK};padding:100px 42px 40px">
    <div style="position:absolute;left:50%;top:30px;width:34px;height:34px;margin-left:-17px;border-radius:50%;background:{p["deep"]};box-shadow:inset 0 3px 6px rgba(0,0,0,.5),0 0 0 5px #D9D2C2"></div>
    <img src="{LOGO_K}" alt="" style="height:36px;display:block">
    <p style="font-family:Montserrat;font-weight:500;font-size:22px;letter-spacing:.2em;text-transform:uppercase;color:#6B5F55;margin-top:34px">Склад</p>
    {rows}
    {caret}
    <p style="position:absolute;left:42px;right:42px;bottom:36px;font-family:'EB Garamond',serif;font-style:italic;font-size:32px;line-height:1.15;color:#4A4750">Хустка «{p['name']}»<br>{SIZE[pid]} см · зроблено в Україні</p>
  </div>'''
    body += foot(([p["flat"]], f"Шовкова хустка «{p['name']}»", f"{PRICE[pid]} грн"), cta, True)
    ad(id, "#141110", body, f"Hang tag: {p['name']}")
label("o14-label-tysha", "tysha", [("100%", "італійський шовк"), ("0%", "чужих очікувань")], "Читайте", "склад.")
label("o22-label-gift", "flirt", [("100%", "італійський шовк"), ("Підпис", "вашими словами"), ("Пакування", "індивідуальне"), ("Відправка", "того ж дня<br>при замовленні до 16:00")],
      "Читайте склад", "подарунка.", care=False, cta="Обрати подарунок", bg="linear-gradient(165deg,#4C5A39,#2A3320 70%,#1A2013)")
label("o19-label-avantiura", "avantiura", [("100%", "італійський шовк"), ("0%", "звичного")], "Склад:", "0% звичного.")

HEAD = """<!DOCTYPE html>
<html lang="uk"><head><meta charset="utf-8"><title>Obiimy · SOLO original concepts</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=EB+Garamond:ital,wght@0,500;1,500&family=Montserrat:wght@500&family=Onest:wght@400;500;600&family=Marck+Script&display=swap">
<style>""" + CSS + "</style></head><body>"
(HERE / "solo9.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "original concepts")
