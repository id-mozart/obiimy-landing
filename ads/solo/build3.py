"""SOLO creatives, sales batch (1080×1920): each story answers one buying question —
price, gift, fit to wardrobe, payment, delivery, trust, try-on. Facts: review/pp/AUDIT-README.txt, review/SITE-FACTS.md.
Output: solo3.html → out/*.jpg"""
import pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit import *

ads = []
def ad(id, cls, body, note=""):
    ads.append(f'\n<!-- {note} -->\n<section class="ad {cls}" id="{id}">{body}\n</section>')

def head(label):
    return f'<div class="row foot"><p class="lbl" style="color:var(--ink3)">{label}</p>{logo()}</div>'

def price_tag(txt, color="var(--ink)"):
    return f'<p class="h" style="font-size:96px;line-height:1;font-weight:700;color:{color};flex:none">{txt} <span style="font-size:46px">грн</span></p>'

# ---------- 1. Launch: the collection is on sale now
grid = "".join(f'<div style="display:grid;justify-items:center;gap:6px"><span style="width:250px;height:250px;background:url({HI(p)}) center/150%;box-shadow:0 14px 22px -12px rgba(0,0,0,.5)"></span><span class="t" style="font-size:32px;font-style:italic;white-space:nowrap">«{p["name"]}»</span></div>' for p in P)
ad("sale-01-launch", "st", f'''
  {base(PP['krok'])}
  <div class="safe col">
    {head("Нова колекція · осінь 2026")}
    <p class="solo" style="font-size:190px;color:var(--wine);margin:24px 0 0 -6px">SOLO</p>
    <p class="h" style="font-size:54px;line-height:1.08;margin-top:12px">Сім авторських принтів на натуральному шовку — <i>уже на сайті</i></p>
    <div style="margin-top:30px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px 6px;justify-items:center">{grid}</div>
    <p class="lbl" style="margin-top:auto;font-weight:600;letter-spacing:.08em">Твіллі — 1 600 грн · хустки — від 2 400 грн</p>
    <p class="lbl" style="margin-top:14px;font-size:30px">{CTA}</p>
  </div>''', "Launch: collection on sale")

# ---------- 2. Gift by budget
LADDER = [("до 1 000 грн", "Резинка «Флірт»", "700", "flirt-scr-1", "raw"),
          ("до 2 000 грн", "Твіллі 84 × 5 · будь-який із 7 принтів", "1 600", "zolote-tw-1-cut", "cut"),
          ("до 3 000 грн", "Хустка 44 × 44 · «Пульс», «Золоте світло», «Сміливий крок»", "2 400", "puls-44-1-cut", "cut"),
          ("до 5 000 грн", "Хустка 65 × 65 · «Іскра», «Флірт»", "4 800", "iskra-65-1-cut", "cut"),
          ("особливий", "Хустка 88 × 88 · «Авантюра», «Тиша всередині»", "6 600", "avantiura-88-1-cut", "cut")]
def ladder_row(b, what, price, img, kind):
    pic = (f'<span style="width:124px;height:124px;flex:none;background:url(src/{img}.webp) center/cover;box-shadow:0 8px 14px -8px rgba(0,0,0,.5)"></span>' if kind == "raw"
           else f'<img src="src/{img}.webp" alt="" style="width:124px;height:124px;object-fit:contain;flex:none;filter:drop-shadow(0 10px 12px rgba(40,25,10,.3))">')
    return f'''<div class="row" style="align-items:center;gap:26px;border-bottom:1px solid rgba(27,22,19,.3);padding:16px 0">{pic}
      <p style="flex:1"><span class="lbl" style="font-size:28px;color:var(--wine);font-weight:600">{b}</span><br><span class="t" style="font-size:36px;line-height:1.1">{what}</span></p>
      <p class="h" style="font-size:52px;flex:none">{price}</p></div>'''
ad("sale-02-budget", "st", f'''
  {base(PP['zolote'])}
  <div class="safe col">
    {head("SOLO · подарунок")}
    <p class="h" style="font-size:84px;line-height:1.02;font-weight:700;margin-top:24px">Подарунок <i style="font-weight:400;color:var(--wine)">під ваш бюджет</i></p>
    <div style="margin-top:22px;border-top:3px solid var(--ink)">{"".join(ladder_row(*r) for r in LADDER)}</div>
    <p class="lbl" style="margin-top:auto;font-size:28px;color:var(--ink2)">Ціни в гривнях · натуральний шовк</p>
    <p class="lbl" style="margin-top:8px;font-weight:600">{CTA}</p>
  </div>''', "Gift by budget")

# ---------- 3. Gift by character: which state is she
CHAR = [("iskra", "любить бути помітною"), ("flirt", "вміє насолоджуватися моментом"), ("puls", "тримає свій ритм, що б не сталося"),
        ("zolote", "цінує ясність і спокій"), ("avantiura", "легко йде за межі звичного"), ("tysha", "вміє чути себе в шумі"), ("krok", "наважується на новий крок")]
rows = "".join(f'''<div class="row" style="align-items:center;gap:22px;padding:11px 0;border-bottom:1px solid rgba(27,22,19,.25)">
      <span style="width:92px;height:92px;border-radius:50%;flex:none;background:url({HI(PP[i])}) center/230%"></span>
      <p class="t" style="flex:1;font-size:37px;line-height:1.08">Якщо вона {t} —<br><b class="h" style="font-style:italic;color:{PP[i]['c']}">«{PP[i]['name']}»</b></p></div>''' for i, t in CHAR)
ad("sale-03-character", "st", f'''
  {base(PP['flirt'])}
  <div class="safe col">
    {head("SOLO · подарунок")}
    <p class="h" style="font-size:76px;line-height:1.02;font-weight:700;margin-top:20px">Подаруйте їй <i style="font-weight:400;color:var(--wine)">її стан</i></p>
    <div style="margin-top:16px">{rows}</div>
    {foot(size=28, style="margin-top:auto;padding-top:16px")}
  </div>''', "Gift by character")

# ---------- 4. Certificate: when you don't know which state
ad("sale-04-certificate", "st", f'''
  {base(PP['tysha'])}
  <div class="safe col">
    {head("Не знаєте, який стан їй ближчий?")}
    <p class="h" style="font-size:96px;line-height:1;font-weight:700;margin-top:30px">Нехай обере <i style="font-weight:400;color:var(--wine)">сама</i></p>
    <div style="flex:1;min-height:0;display:grid;place-items:center">
      <div class="shadow frame2" style="position:relative;width:820px;height:500px;background:var(--card);transform:rotate(-3deg);display:grid;place-items:center;text-align:center">
        <div><img src="{LOGO_K}" alt="" style="height:44px;margin:0 auto"><p class="lbl" style="margin-top:34px;color:var(--ink3)">Подарунковий сертифікат</p>
        <p class="h" style="font-size:120px;line-height:1;font-weight:700;margin-top:20px">від 1 000 <span style="font-size:56px">грн</span></p>
        <p class="t" style="font-size:36px;font-style:italic;color:var(--ink2);margin-top:14px">на будь-який товар Obiimy</p></div>
      </div>
    </div>
    <p class="t" style="font-size:42px;line-height:1.16">Номінали 1 000, 1 500, 2 000, 2 500 і 4 000 грн. Електронний або фізичний, діє 3 місяці.</p>
    {foot(text="Обрати сертифікат · obiimy.world", size=28, style="margin-top:24px;border-top:1px solid var(--ink);padding-top:16px")}
  </div>''', "Gift certificate")

# ---------- 5. Wardrobe match: to what you already wear
MATCH = [("До бежевого тренчу", "flirt-tw-3", "50% 30%", "flirt", "Твіллі 84 × 5 · 1 600 грн"),
         ("До чорного жакета", "zolote-44-4", "50% 25%", "zolote", "Хустка 44 × 44 · 2 400 грн"),
         ("До блакитного костюма", "iskra-tw-2", "50% 30%", "iskra", "Твіллі 84 × 5 · 1 600 грн"),
         ("До білої сорочки", "puls-tw-1", "50% 35%", "puls", "Твіллі 84 × 5 · 1 600 грн")]
cells = "".join(f'''<div class="col" style="min-height:0"><div class="ph" style="flex:1;min-height:0;position:relative"><img src="{S(ph)}" alt="" style="object-position:{pos}"></div>
      <p class="lbl" style="font-size:28px;margin-top:12px;letter-spacing:.08em">{t}</p>
      <p class="t" style="font-size:36px;line-height:1.05"><i class="h" style="color:{PP[pid]['c']}">«{PP[pid]['name']}»</i></p>
      <p class="lbl" style="font-size:28px;color:var(--ink2);letter-spacing:.04em">{pr}</p></div>''' for t, ph, pos, pid, pr in MATCH)
ad("sale-05-wardrobe", "st", f'''
  {base(PP['iskra'])}
  <div class="safe col">
    {head("SOLO · до вашого гардероба")}
    <p class="h" style="font-size:80px;line-height:1.02;font-weight:700;margin-top:18px">Уже маєте, <i style="font-weight:400;color:var(--wine)">з чим носити</i></p>
    <div style="flex:1;min-height:0;margin-top:22px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:22px 18px">{cells}</div>
    <p class="lbl" style="margin-top:20px;font-weight:600">{CTA}</p>
  </div>''', "Wardrobe match")

# ---------- 6. Complete look: scarf + twilly of one print → free delivery
LOOK = [("iskra", "iskra-65-4", "55% 30%", "iskra-tw-3", "50% 60%", "Хустка 65 × 65", "4 800", "6 400"),
        ("avantiura", "avantiura-88-2", "40% 35%", "avantiura-tw-3", "50% 40%", "Хустка 88 × 88", "6 600", "8 200")]
for k, (pid, ph1, pos1, ph2, pos2, big, bp, total) in enumerate(LOOK, 1):
    p = PP[pid]
    ad(f"sale-06-look-{pid}", "st", f'''
  {base(p)}
  <div class="safe col">
    {head("SOLO · образ цілком")}
    <p class="h" style="font-size:80px;line-height:1.02;font-weight:700;margin-top:18px">Один принт — <i style="font-weight:400;color:{p['c']}">«{p['name']}»</i></p>
    <div class="row" style="flex:1;min-height:0;gap:18px;margin-top:24px">
      <div class="col" style="flex:1.25;min-height:0">{photo(ph1, pos1, style="flex:1")}<p class="t" style="font-size:36px;margin-top:10px">{big} — <b>{bp} грн</b></p></div>
      <div class="col" style="flex:1;min-height:0">{photo(ph2, pos2, style="flex:1")}<p class="t" style="font-size:36px;margin-top:10px">Твіллі 84 × 5 — <b>1 600 грн</b></p></div>
    </div>
    <div class="row" style="justify-content:space-between;align-items:flex-end;margin-top:22px;border-top:3px solid var(--ink);padding-top:16px">
      <p class="t" style="font-size:40px;line-height:1.1">Разом<br><span class="lbl" style="font-size:28px;color:var(--wine);font-weight:600">доставка безкоштовна</span></p>
      {price_tag(total)}
    </div>
    <p class="lbl" style="margin-top:16px;font-weight:600">{CTA}</p>
  </div>''', f"Complete look: {p['name']}")

# ---------- 7. Free delivery threshold
ad("sale-07-delivery", "st", f'''
  {base(PP['puls'])}
  <div class="safe col">
    {head("SOLO · доставка")}
    <p class="h" style="font-size:96px;line-height:1;font-weight:700;margin-top:24px">Замовте до 16:00 —</p>
    <p class="h" style="font-size:96px;line-height:1;font-style:italic;color:var(--wine);margin-top:8px">відправимо сьогодні</p>
    <p class="t" style="font-size:44px;line-height:1.15;color:var(--ink2);margin-top:22px">Новою поштою в день замовлення. Від 5 000 грн — доставка безкоштовна.</p>
    <div style="flex:1;min-height:0;display:grid;place-items:center">
      <div style="position:relative;width:820px;height:560px">
        <div class="ph shadow" style="position:absolute;left:0;top:30px;width:520px;height:520px;transform:rotate(-4deg)"><img src="{S('flirt-scr-2')}" alt="" style="object-position:50% 40%"></div>
        <img class="cut" src="{CUT('puls-44-1')}" alt="" style="position:absolute;right:0;top:0;width:420px;transform:rotate(8deg)">
      </div>
    </div>
    <p class="lbl" style="font-weight:600">Хустка «Пульс» 44 × 44 — 2 400 грн · резинка «Флірт» — 700 грн</p>
    <p class="lbl" style="margin-top:8px;font-size:28px;color:var(--ink2)">{CTA}</p>
  </div>''', "Same-day dispatch and free delivery")

# ---------- 8. Pay in parts
ad("sale-08-parts", "st dark", f'''
  <div class="fill" style="background:{PP['tysha']['deep']}"></div>
  <div class="fill" style="background:radial-gradient(70% 45% at 50% 50%,rgba(255,255,255,.14),rgba(0,0,0,.25))"></div>
  <div class="safe col" style="color:var(--cream)">
    <div class="row foot"><p class="lbl" style="color:rgba(243,234,219,.75)">SOLO · оплата</p>{logo(dark=True)}</div>
    <p class="h" style="font-size:84px;line-height:1.02;font-weight:700;margin-top:24px">Найбільша хустка колекції — <i style="font-weight:400">частинами</i></p>
    <div style="flex:1;min-height:0;display:grid;place-items:center"><img class="cut" src="{CUT('tysha-88-1')}" alt="" style="height:620px;transform:rotate(-6deg);filter:drop-shadow(0 50px 60px rgba(0,0,0,.6))"></div>
    <p class="h" style="font-size:64px;line-height:1;font-style:italic">«Тиша всередині» · 88 × 88</p>
    <p class="lbl" style="margin-top:14px;color:var(--yellow);font-weight:600">6 600 грн · оплата частинами</p>
    <p class="t" style="font-size:40px;line-height:1.15;margin-top:8px">ПриватБанк — 4 платежі, monobank — 3 платежі</p>
    <p class="lbl" style="margin-top:18px;font-size:28px;border-top:1px solid rgba(243,234,219,.5);padding-top:16px">{CTA}</p>
  </div>''', "Pay in parts")

# ---------- 9. Try on in the showroom
ad("sale-09-showroom", "st", f'''
  {base(PP['iskra'])}
  {photo("iskra-tw-2", "50% 35%", style="left:0;right:0;top:236px;height:744px")}
  <div class="col" style="left:80px;right:80px;top:1020px;bottom:380px">
    <p class="lbl" style="color:var(--ink3)">SOLO · шоурум</p>
    <p class="h" style="font-size:80px;line-height:1.02;font-weight:700;margin-top:12px">Приміряйте <i style="font-weight:400;color:var(--wine)">наживо</i></p>
    <p class="t" style="font-size:40px;line-height:1.15;margin-top:12px">Шовк Obiimy можна подивитися й приміряти в шоурумі: Київ, вул. Петра Сагайдачного, 12.</p>
    <p class="lbl" style="margin-top:auto;font-weight:600;letter-spacing:.08em">Пн–пт 10:00–18:00 · сб 11:00–18:00</p>
    <div class="row foot" style="margin-top:12px;border-top:1px solid var(--ink);padding-top:16px"><p class="lbl" style="font-size:28px">або obiimy.world</p>{logo()}</div>
  </div>''', "Showroom")

# ---------- 10. Trust: where Obiimy is sold and written about
ad("sale-10-trust", "st", f'''
  {base(PP['avantiura'])}
  <div class="safe col">
    {head("Obiimy · український бренд шовку")}
    <p class="h" style="font-size:82px;line-height:1.02;font-weight:700;margin-top:22px">Obiimy обирають <i style="font-weight:400;color:var(--wine)">не лише в Україні</i></p>
    {photo("avantiura-tw-4", "50% 30%", style="height:560px;margin-top:26px")}
    <div class="row" style="gap:40px;margin-top:26px">
      <div style="flex:1"><p class="lbl" style="font-size:28px;color:var(--ink3)">Продається в</p><p class="t" style="font-size:40px;line-height:1.15;margin-top:6px">INTERTOP, Hram, Be Brave (Канада), UFD London</p></div>
      <div style="flex:1"><p class="lbl" style="font-size:28px;color:var(--ink3)">Про бренд писали</p><p class="t" style="font-size:40px;line-height:1.15;margin-top:6px">LIGA.net, INSIDER UA</p></div>
    </div>
    <p class="t" style="font-size:38px;line-height:1.15;color:var(--ink2);margin-top:auto">Натуральний шовк, авторські принти художниці Світлани Сніжко, зроблено в Україні.</p>
    <p class="lbl" style="margin-top:16px;font-weight:600;border-top:1px solid var(--ink);padding-top:16px">Колекція SOLO · obiimy.world</p>
  </div>''', "Trust: retail and press")

# ---------- 11. Gift note in your words
ad("sale-11-note", "st", f'''
  {base(PP['avantiura'])}
  {photo("avantiura-tw-1", "50% 30%", style="left:0;right:0;top:236px;height:664px")}
  <div class="page shadow" style="left:560px;top:700px;width:440px;height:300px;background:var(--card);transform:rotate(-5deg)">
    <p class="t" style="position:absolute;left:34px;right:30px;top:30px;font-size:40px;line-height:1.14;font-style:italic">«Обирай себе. Завжди.»</p>
    <p class="lbl" style="position:absolute;left:34px;bottom:30px;font-size:26px;color:var(--ink3)">— ваш текст</p>
  </div>
  <div class="col" style="left:80px;right:80px;top:1050px;bottom:380px">
    <p class="h" style="font-size:78px;line-height:1.02;font-weight:700">Підпис до подарунка — <i style="font-weight:400;color:var(--wine)">вашими словами</i></p>
    <p class="t" style="font-size:40px;line-height:1.15;color:var(--ink2);margin-top:14px">Напишіть текст у коментарі до замовлення — ми підпишемо подарунок.</p>
    <p class="lbl" style="margin-top:auto;font-weight:600">{offer(PP['avantiura'], 1)}</p>
    {foot(size=28, style="margin-top:12px;border-top:1px solid var(--ink);padding-top:16px")}
  </div>''', "Gift note")

# ---------- 12. Twilly as the first step into the collection
ad("sale-12-first", "st", f'''
  {base(PP['krok'])}
  {photo("krok-tw-2", "50% 40%", style="left:0;right:0;top:236px;height:764px")}
  <div class="col" style="left:80px;right:80px;top:1040px;bottom:380px">
    <p class="lbl" style="color:var(--ink3)">SOLO · твіллі</p>
    <div class="row" style="justify-content:space-between;align-items:flex-end;gap:30px;margin-top:10px">
      <p class="h" style="font-size:76px;line-height:1.02;font-weight:700">Почніть <i style="font-weight:400;color:var(--wine)">зі стрічки</i></p>
      {price_tag("1 600")}
    </div>
    <p class="t" style="font-size:40px;line-height:1.15;color:var(--ink2);margin-top:14px">Твіллі 84 × 5 у кожному з семи принтів: у волосся, на шию, на сумку чи зап’ястя.</p>
    {foot(size=28, style="margin-top:auto;border-top:1px solid var(--ink);padding-top:16px")}
  </div>''', "Twilly as entry")

# ---------- 13. On the bag: twilly for everyday
ad("sale-13-bag", "st", f'''
  {base(PP['tysha'])}
  {photo("tysha-tw-2", "50% 45%", style="left:0;right:0;top:236px;height:804px")}
  <div class="col" style="left:80px;right:80px;top:1080px;bottom:380px">
    <p class="lbl" style="color:var(--ink3)">SOLO · твіллі</p>
    <div class="row" style="justify-content:space-between;align-items:flex-end;gap:30px;margin-top:10px">
      <p class="h" style="font-size:72px;line-height:1.02;font-weight:700">Одна стрічка — <i style="font-weight:400;color:var(--wine)">нова сумка</i></p>
      {price_tag("1 600")}
    </div>
    <p class="t" style="font-size:40px;line-height:1.15;color:var(--ink2);margin-top:14px">{nb("Твіллі «Тиша всередині» 84 × 5 на ручці сумки — найпростіший спосіб змінити образ.")}</p>
    {foot(size=28, style="margin-top:auto;border-top:1px solid var(--ink);padding-top:16px")}
  </div>''', "Twilly on the bag")

(HERE / "solo3.html").write_text(HEAD + "".join(ads) + "\n</body></html>")
print(len(ads), "creatives (sales)")
