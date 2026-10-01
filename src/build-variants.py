#!/usr/bin/env python3
"""Design variants for the HR deck — one PDF (obiimy-variants.pdf) with 2–4 alternative layouts per key page, each labelled
«Варіант X · сторінка». Same design system as team-deck.html (its <style> is reused), same data (build-b2b-team-main.py,
review/cast.json). The client picks; the chosen layout then moves into build-team-pdf.py."""
import importlib.util, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
sys.path.insert(0, str(ROOT))
from imgs import typo
from PIL import Image
_spec = importlib.util.spec_from_file_location("main", ROOT / "build-b2b-team-main.py")
main = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(main)
PERKS, SOLO, TIERS, ASSORT, PERS, SETS4, WAYS, price, qr_svg, cast = main.PERKS, main.SOLO, main.TIERS, main.ASSORT, main.PERS, main.SETS4, main.WAYS, main.price, main.qr_svg, main.cast
CARD_PH, CARD_POS, PROD = main.CARD_PH, main.CARD_POS, main.PROD
team = main.team
PHONE, MAIL, SHOWROOM = team.PHONE, team.MAIL, team.SHOWROOM
LANDING = "https://obiimy-landing-production.up.railway.app/b2b-team-main"

def pic(src, cls="", pos=""):
    p = pathlib.Path(src); lb = OUT / "review" / "lb"; lb.mkdir(parents=True, exist_ok=True)
    j = lb / (p.stem + ".jpg")
    if not j.exists():
        im = Image.open(OUT / src).convert("RGB"); im.thumbnail((1200, 1200)); im.save(j, quality=72, optimize=True)
    st = f' style="object-position:{pos}"' if pos else ""
    return f'<img src="review/lb/{j.name}" class="{cls}" alt=""{st}>'
def cp(slot, f, pos="", cls=""):
    ff, pp = cast(slot, f, pos); return pic(ff, cls, pp)

deck_css = re.search(r"<style>(.*?)</style>", (OUT / "team-deck.html").read_text(), re.S).group(1)
PAGES = []
def page(label, html, cls=""):
    PAGES.append(f'<section class="pg {cls}"><div class="vlab">{label}</div>{html}</section>')

S0, S1, S2, S3 = SETS4
NAMES4 = ["Твіллі", "Хустка 44 × 44 і кільце", "Маска й резинка", "Хустка, твіллі, МК"]
def t2_cards():
    out = []
    for i, ((lb, n, t, pr, note, ph), S) in enumerate(zip(TIERS, SETS4)):
        out.append('<div class="t2">' + pic(S["tier"][0], "", S["tier"][1]) + f'<div class="t2-t"><p class="eb">0{i + 1} · {lb}</p><b>{n}</b><span>{t}</span></div>'
                   + '<div class="chip">' + pic(S["gal"][PROD[i]][0], "chip-ph") + f'<div><span>{NAMES4[i]}</span><em>{pr}</em></div></div></div>')
    return "".join(out)
def ladder():
    return "".join(f'<div><span class="n">0{i + 1}</span><div><b>{n}</b><small>{t}</small></div><em>{pr}</em></div>' for i, (lb, n, t, pr, note, ph) in enumerate(TIERS))
def kv(items): return "".join(f'<div><span>{k}</span><span>{v}</span></div>' for k, v in items)
def rb_items(): return "".join('<div class="rB-i">' + pic(ph) + f'<div><b>{n}</b><em>від {price(pr)}</em></div></div>' for n, pr, ph in ASSORT)
def pb_cols():
    return "".join(f'<div><b>0{i + 1}</b><h3>{n}</h3><p>{t}</p><small>{tm if i else "Безкоштовно · у кожному корпоративному замовленні"}</small></div>' for i, (n, t, tm, ph) in enumerate(PERS))
def nums_big():
    return "".join(f"<div><b>{b}</b><span>{d}</span></div>" for b, d in [("100%", "натуральний італійський шовк; кутики кожної хустки — вручну"), ("5", "авторських колекцій: Сніжко та українські художниці"), ("38", "принтів твіллі на вибір"), ("45", "готових наборів на obiimy.world")])
T = '<p class="eb">Для HR і офіс-менеджерів · 2026</p><h1>Подарунки<br>для команди</h1><p class="it">Авторські принти на натуральному італійському шовку</p>'

# ───────────── обкладинки A–E
page("A · Обкладинка — кабріолет, текст ліворуч", f'<div class="fullp cv">{pic("photo/solo/tysha-88-2.webp", "full", "50% 22%")}<div class="fullp-t cov-t"><img src="brand/logo-white.png" class="logo">{T}<p class="cov-line">Чотири рівні від 1 600 грн на людину · пакування й наліпка з вашим логотипом — безкоштовно · нова колекція SOLO</p></div></div>', "cover nopad")
page("B · Обкладинка — фото ліворуч, кремова панель", f'<div class="cov">{pic("photo/dotyk-1.webp", "full", "50% 20%")}<div class="cov-p"><img src="brand/logo-ink.png" class="logo"><div class="cov-m">{T}</div><div class="cov-f"><div><b>Чотири рівні</b><span>від 1 600 грн на людину</span></div><div><b>Ваш логотип</b><span>пакування й наліпка — безкоштовно</span></div><div><b>Колекція SOLO</b><span>сім нових авторських принтів</span></div></div></div></div>', "cover nopad")
page("C · Обкладинка — як SOLO-креатив: курсив і чип", f'<div class="fullp cv dk">{pic("photo/solo/zolote-tw-2.webp", "full", "35% 45%")}<div class="fullp-t cov-t"><img src="brand/logo-white.png" class="logo"><p class="eb">Для HR і офіс-менеджерів · 2026</p><h1 class="gi">Подарунки,<br>які носять</h1><p class="sub-w">Шовкові подарунки для команди — чотири рівні від 1 600 грн</p><div class="chip inl">{pic("img/twilly-zolote.webp", "chip-ph")}<div><span>Твіллі «Золоте світло» · на людину</span><em>1 600 грн</em></div></div></div></div>', "cover nopad")
page("D · Обкладинка — портрет з лукбуку на білому", f'<div class="cov r"><div class="cov-p white"><img src="brand/logo-ink.png" class="logo"><div class="cov-m">{T}<p class="line-ink">Чотири рівні від 1 600 грн · логотип — безкоштовно · колекція SOLO</p></div><p class="toc">Рівні й ціни — 7 · Набори — 8–12 · Запит — 15</p></div>{pic("photo/lookbook/lb05-06-L.webp", "full", "50% 20%")}</div>', "cover nopad")
page("E · Обкладинка — тренч у полі, текст по центру", f'<div class="fullp">{pic("photo/kolo-3.webp", "full", "50% 30%")}<div class="fullp-q"><img src="brand/logo-white.png" class="logo c"><h1 class="c">Подарунки для команди</h1><p class="it">Шовк Obiimy · авторські принти · чотири рівні від 1 600 грн</p></div></div>', "cover nopad")

# ───────────── про бренд
page("A · Про бренд — фото на всю сторінку (поточна)", f'<div class="fullp">{cp("D02", "photo/solo/puls-44-5.webp", "50% 30%", "full")}<div class="fullp-t"><p class="eb">Про бренд</p><h1>Обійми з шовку</h1><p>Український бренд шовкових аксесуарів із Києва. Засновниця й художниця — Світлана Сніжко: кожен принт — авторський. Хустки, твіллі, резинки, маски для сну, аксесуари для дому.</p><p class="quote-l">«Кожна коробочка — це обійми, що нагадують: ти варта краси»</p></div></div>', "cover nopad")
page("B · Про бренд — чорна сторінка, цитата і три кадри", f'<div class="abB"><div class="abB-t"><p class="eb">Про бренд</p><p class="bigq l">«Кожна коробочка —<br>це обійми, що нагадують:<br>ти варта краси»</p><p>Український бренд шовкових аксесуарів із Києва, заснований під час війни. Засновниця й художниця — Світлана Сніжко. Колекція «Співоча душа» присвячена рідкісним птахам: частина коштів іде на гнізда для сиворакші.</p><p class="foot-w">INTERTOP · Hram · Be Brave, Канада · UFD London · LIGA.net · INSIDER UA</p></div><div class="abB-ph">{pic("photo/kolo-2.webp", "", "50% 20%")}{pic("photo/lookbook/lb02-01-R.webp", "", "50% 25%")}{pic("photo/dotyk-2.webp", "", "60% 20%")}</div></div>', "dark nopad")
page("C · Про бренд — біла панель і мозаїка з трьох", f'<div class="abC"><div class="abC-ph">{pic("photo/probudzhennia-2.webp", "big", "50% 20%")}{pic("photo/enerhiia-back.webp", "", "50% 20%")}{pic("photo/box-gold.jpg", "", "50% 45%")}</div><div class="abC-t"><p class="eb">Про бренд</p><h2>Obiimy — обійми з шовку</h2><p>Український бренд шовкових аксесуарів із Києва. Засновниця й художниця — Світлана Сніжко. Хустки, твіллі, резинки, маски для сну, аксесуари для дому.</p><p>Заснований під час війни; бере участь у благодійних ініціативах. «Співоча душа» — колекція про рідкісних птахів: частина коштів іде на гнізда для сиворакші.</p><div class="nums two"><div><b>100%</b><span>натуральний італійський шовк</span></div><div><b>5</b><span>авторських колекцій</span></div><div><b>38</b><span>принтів твіллі</span></div><div><b>45</b><span>готових наборів</span></div></div></div></div>', "white nopad")

# ───────────── факти
FACTS = [("Авторські принти", "Засновниця й художниця — Світлана Сніжко; принти — її та українських художниць.", "photo/dotyk-3.webp", "50% 40%"), ("Італійський шовк", "Лише 100% натуральний шовк; кутики кожної хустки обробляють вручну.", "photo/site/set-tvilli-845-ta-khustky-4444-natkhne-03.jpg", "50% 45%"), ("Зроблено в Україні", "Повністю українське виробництво, благодійні ініціативи.", "photo/site/set-ta-rezynka-litnie-pole-04.jpg", "50% 55%"), ("«Співоча душа»", "Частина коштів — на гнізда для сиворакші з Червоної книги.", "photo/lookbook/lb02-01-R.webp", "50% 30%")]
page("B · Факти — повносторінкове фото, цифри на градієнті", f'<div class="fullp"><!-- -->{pic("photo/lookbook/lb04-04-R.webp", "full", "50% 25%")}<div class="fnums"><div><b>100%</b><span>натуральний італійський шовк — кутики кожної хустки вручну</span></div><div><b>5</b><span>авторських колекцій засновниці Світлани Сніжко та українських художниць</span></div><div><b>38</b><span>принтів твіллі — кожному в команді свій</span></div><div><b>45</b><span>готових подарункових наборів на obiimy.world</span></div></div><p class="fnote">INTERTOP · Hram · Be Brave, Канада · UFD London · LIGA.net · INSIDER UA · шоурум: Київ, Сагайдачного, 12</p></div>', "cover nopad")
page("C · Факти — чорна сторінка, великі цифри, одне фото", f'<div class="fC">{pic("photo/solo/avantiura-88-5.webp", "ph", "50% 20%")}<div class="fC-t"><p class="eb">Бренд у фактах</p><h2>Що стоїть за кожною коробкою Obiimy</h2><div class="nums big">{nums_big()}</div><p class="foot-w">Продають INTERTOP і Hram, Be Brave (Канада), UFD London. Писали LIGA.net та INSIDER UA.</p></div></div>', "dark nopad")

# ───────────── SOLO
page("B · SOLO — кінематографічний кадр, маніфест у правій панелі", f'<div class="sB">{pic("photo/solo/tysha-88-2.webp", "ph", "35% 25%")}<div class="sB-t"><p class="eb">Нова колекція · 2026</p><h1>SOLO.<br>Шлях до себе</h1><p class="it gold">Шовкова свобода: жіноча сила крізь десятиліття</p><p>Натхнення — обкладинки модних журналів 40–50-х: змінювалися епохи й силуети, а хустка залишалася поруч. Сім авторських принтів — сім етапів шляху жінки до себе. Натуральний шовк, двосторонній друк.</p><p class="team">Для команди: кожному — свій принт, під стан, який хочете побажати, або один на всіх.</p></div></div>', "dark nopad")
strip = "".join(f'<div class="fs2">{pic(CARD_PH[i], "", CARD_POS[i])}<div class="fs2-t"><b>{n}</b><span>{st}</span></div></div>' for i, (n, st, fm, pr, ph, fl) in enumerate(SOLO))
page("C · SOLO — сім принтів кінострічкою на всю ширину", f'<div class="hd pad"><div><p class="eb">Колекція SOLO</p><h2>Сім принтів — сім станів</h2></div><p class="hd-r">Твіллі — 1 600 грн · хустки з двостороннім друком від 2 400 грн. Для HR стан принта — готовий текст привітання.</p></div><div class="strip7">{strip}</div>', "dark nopad")

# ───────────── рівні
page("C · Рівні — два на два, кадр на моделі + чип", f'<div class="hd pad"><div><p class="eb">Чотири рівні</p><h2>Від стрічки до набору з майстер-класом</h2></div><p class="hd-r">Роздрібні ціни obiimy.world; майстер-клас і доставку рахуємо окремо. Команді з 50 людей — 80 000–160 000 грн за речі.</p></div><div class="t22">{t2_cards()}</div>', "dark nopad")
page("D · Рівні — одне велике фото і драбина цін на чорному", f'<div class="tD">{cp("D10", "photo/solo/krok-tw-4.webp", "48% 50%", "ph")}<div class="tD-t"><p class="eb">Ціновий діапазон</p><h2>Чотири рівні подарунка</h2><div class="ladder">{ladder()}</div><p class="foot-w">Роздрібні ціни obiimy.world · команді з 50 людей — 80 000–160 000 грн за речі · чоловікам — сертифікат, маска, наволочка, закладка</p></div></div>', "dark nopad")

# ───────────── сторінка набору (на прикладі 02 «Хустка і кільце»)
S = S1
page("B · Набір — кадр навиліт, чип і панель внизу (як креатив)", f'<div class="setB">{pic(S["hero"][0], "ph", S["hero"][2])}<div class="setB-t"><div><p class="eb">{S["lb"]}</p><h1 class="gi m">{S["name"]}</h1><p class="sub-w">{S["lead"]}</p></div><div class="setB-r"><div class="chip">{pic(S["gal"][PROD[1]][0], "chip-ph")}<div><span>{S["short"]}</span><em>{S["pr"]}</em></div></div><div class="kv-w">{kv(S["inside"][:4])}</div></div></div></div>', "dark nopad")
page("C · Набір — товар крупно на білому, лайфстайл поруч", f'<div class="setC"><div class="setC-ph">{pic(S["gal"][PROD[1]][0], "prod")}<div class="setC-s">{pic(S["hero"][0], "", S["hero"][2])}{pic(S["gal"][0][0], "", S["gal"][0][2])}</div></div><div class="set-t"><p class="eb">{S["lb"]}</p><h2>{S["name"]}</h2><p class="sub">{S["lead"]}</p><p class="rrp">{S["pr"]}<small>{S["prnote"]}</small></p><div class="kv">{kv(S["inside"][:5])}</div><p class="who">{S["who"]}</p></div></div>', "white nopad")

# ───────────── асортимент
page("B · Асортимент — на чорному, з чипами", f'<div class="hd pad"><div><p class="eb">Асортимент</p><h2>Усе, з чого можна зібрати подарунок</h2></div><p class="hd-r">Роздрібні ціни obiimy.world, «від» — найдешевший формат чи принт. Будь-яку річ можна зробити подарунком або додати в коробку.</p></div><div class="rB">{rb_items()}</div>', "dark nopad")

# ───────────── персоналізація
page("B · Персоналізація — фото навиліт, чотири колонки на градієнті", f'<div class="fullp">{cp("D16", "photo/box-gold.jpg", "50% 40%", "full")}<div class="pB"><div class="pB-h"><p class="eb">Персоналізація</p><h2>Подарунок із вашим логотипом — чотири рівні</h2></div><div class="pB-g">{pb_cols()}</div></div></div>', "cover nopad")

# ───────────── контакти
page("B · Контакти — фото навиліт, картка з QR", f'<div class="fullp">{cp("D17", "photo/solo/zolote-tw-2.webp", "40% 40%", "full")}<div class="cB"><p class="eb">Запит</p><h2>Напишіть — надішлемо добірку й розрахунок</h2><p>Нагода, кількість і дата — цього досить для першого листа. У відповідь: принти на вибір і розрахунок окремими рядками.</p><div class="qrrow">{qr_svg(LANDING, 110)}<p class="contact"><b>{PHONE}</b><br>Telegram @OBIIMY_sales<br>{MAIL}<br>obiimy.world</p></div><p class="foot">Шоурум: {SHOWROOM}</p></div></div>', "cover nopad")
page("C · Контакти — чорна сторінка, великий телефон", f'<div class="cC"><div class="cC-t"><p class="eb">Запит</p><p class="bigq l">Напишіть —<br>надішлемо добірку<br>й розрахунок</p><p class="tel">{PHONE}</p><p class="cC-l">Telegram @OBIIMY_sales · {MAIL} · obiimy.world<br>Шоурум: {SHOWROOM}</p><div class="qrrow w">{qr_svg(LANDING, 100, ink="#F3F1EC")}<p class="contact w">Сторінка для команд<br><small>із формою запиту</small></p></div></div>{pic("photo/solo/krok-tw-3.webp", "ph", "50% 30%")}</div>', "dark nopad")

css = deck_css + '''
  .vlab { position: absolute; top: 4mm; right: 5mm; z-index: 9; background: #fff; color: #111; font-size: 7.5pt; padding: 1.4mm 3mm; border-radius: 2mm; font-family: 'Tenor Sans', sans-serif; box-shadow: 0 1px 4px rgba(0,0,0,.25); }
  .gi { font-style: italic; color: #F3EBD0; } .gi.m { font-size: 30pt; }
  .sub-w { color: rgba(255,255,255,.9); font-size: 11pt; margin: 0 0 5mm; max-width: 120mm; }
  .chip.inl { display: inline-grid; position: static; left: auto; right: auto; bottom: auto; grid-template-columns: 14mm 1fr; padding: 2mm 4mm 2mm 2mm; } .chip.inl .chip-ph { width: 14mm; height: 14mm; } .chip.inl em { font-size: 15pt; } .chip.inl span { font-size: 7.5pt; }
  .fullp.cv.dk::after { background: linear-gradient(90deg, rgba(0,0,0,.75) 0%, rgba(0,0,0,.35) 55%, rgba(0,0,0,.1) 100%), linear-gradient(0deg, rgba(0,0,0,.7) 0%, rgba(0,0,0,0) 60%); }
  .cov.r { grid-template-columns: 1fr 150mm; } .cov-p.white { background: #fff; padding: 16mm 14mm 14mm 18mm; } .line-ink { font-size: 9.5pt; border-top: 1px solid #C9C6C0; padding-top: 3mm; margin-top: 5mm; color: #4A4A47; }
  .toc { font-size: 7pt; letter-spacing: .08em; color: #8E8A84; margin: 0; }
  .fullp-q .logo.c { height: 10mm; width: auto; margin: 0 auto 8mm; } .fullp-q h1.c { font-size: 44pt; color: #fff; margin-bottom: 3mm; } .fullp-q .it { color: #F3EBD0; }
  .abB { display: grid; grid-template-columns: 1fr 150mm; height: 210mm; } .abB-t { padding: 16mm 12mm 16mm 18mm; display: flex; flex-direction: column; justify-content: center; } .abB-t p { color: #C9C5BE; font-size: 9.6pt; }
  .bigq.l { text-align: left; font-size: 26pt; margin: 2mm 0 6mm; } .foot-w { font-size: 8pt; color: #8E8A84; margin-top: 4mm; }
  .abB-ph { display: grid; grid-template-rows: 1.4fr 1fr; grid-template-columns: 1fr 1fr; gap: 3mm; height: 210mm; } .abB-ph img { width: 100%; height: 100%; min-height: 0; } .abB-ph img:first-child { grid-column: span 2; }
  .abC { display: grid; grid-template-columns: 150mm 1fr; height: 210mm; } .abC-ph { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1.5fr 1fr; gap: 3mm; } .abC-ph img { width: 100%; height: 100%; min-height: 0; } .abC-ph .big { grid-column: span 2; }
  .abC-t { padding: 16mm 18mm 14mm 14mm; display: flex; flex-direction: column; justify-content: center; } .abC-t p { font-size: 9.8pt; color: #4A4A47; } .nums.two { grid-template-columns: 1fr 1fr; margin-top: 4mm; }
  .fnums { position: absolute; left: 18mm; right: 18mm; bottom: 24mm; z-index: 1; display: grid; grid-template-columns: repeat(4, 1fr); gap: 8mm; color: #fff; }
  .fnums b { display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 34pt; line-height: 1; color: #F3EBD0; } .fnums span { font-size: 8.5pt; color: rgba(255,255,255,.88); line-height: 1.4; display: block; margin-top: 2mm; }
  .fnote { position: absolute; left: 18mm; right: 18mm; bottom: 12mm; z-index: 1; font-size: 7.5pt; letter-spacing: .1em; text-transform: uppercase; color: rgba(255,255,255,.7); margin: 0; }
  .fC { display: grid; grid-template-columns: 118mm 1fr; height: 210mm; } .fC .ph { width: 100%; height: 100%; } .fC-t { padding: 16mm 18mm 16mm 14mm; display: flex; flex-direction: column; justify-content: center; }
  .nums.big { border-top: 0; grid-template-columns: 1fr 1fr; gap: 6mm 8mm; } .nums.big b { font-size: 40pt; color: #F3EBD0; } .nums.big span { color: #B8B3AA; font-size: 9pt; }
  .sB { display: grid; grid-template-columns: 1fr 112mm; height: 210mm; } .sB .ph { width: 100%; height: 100%; } .sB-t { padding: 16mm 16mm 16mm 12mm; display: flex; flex-direction: column; justify-content: center; } .sB-t h1 { font-size: 36pt; margin: 1mm 0 4mm; } .sB-t p { font-size: 9.4pt; color: #C9C5BE; } .sB-t .team { color: #F3F1EC; border-top: 1px solid rgba(255,255,255,.2); padding-top: 3.5mm; margin-top: 2mm; }
  .hd.pad { padding: 14mm 18mm 0; margin-bottom: 5mm; }
  .strip7 { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2mm; flex: 1; min-height: 0; } .fs2 { position: relative; overflow: hidden; } .fs2 img { width: 100%; height: 100%; }
  .fs2::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 50%, rgba(0,0,0,.82) 100%); } .fs2-t { position: absolute; left: 4mm; right: 3mm; bottom: 6mm; z-index: 2; color: #fff; }
  .fs2-t b { display: block; font-family: 'Playfair Display', serif; font-style: italic; font-weight: 400; font-size: 15pt; line-height: 1.05; color: #E7D9A6; } .fs2-t span { display: block; font-size: 6.8pt; margin-top: 1.5mm; color: rgba(255,255,255,.85); }
  .t22 { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 3mm; flex: 1; min-height: 0; padding: 0 18mm 12mm; } .t2 { position: relative; overflow: hidden; } .t2 img:first-child { width: 100%; height: 100%; }
  .t2::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,0,0,.72) 0%, rgba(0,0,0,.25) 50%, rgba(0,0,0,0) 80%); }
  .t2-t { position: absolute; left: 6mm; top: 6mm; max-width: 70mm; z-index: 2; color: #fff; } .t2-t .eb { color: rgba(255,255,255,.75); } .t2-t b { display: block; font-family: 'Playfair Display', serif; font-style: italic; font-weight: 400; font-size: 17pt; line-height: 1.05; color: #F3EBD0; } .t2-t span { display: block; font-size: 7.8pt; color: rgba(255,255,255,.88); margin-top: 2mm; }
  .t2 .chip { left: 6mm; right: auto; bottom: 6mm; min-width: 62mm; }
  .tD { display: grid; grid-template-columns: 128mm 1fr; height: 210mm; } .tD .ph { width: 100%; height: 100%; } .tD-t { padding: 16mm 18mm 16mm 14mm; display: flex; flex-direction: column; justify-content: center; }
  .ladder { display: grid; } .ladder > div { display: grid; grid-template-columns: 12mm 1fr auto; gap: 4mm; align-items: center; padding: 3.2mm 0; border-top: 1px solid rgba(255,255,255,.18); } .ladder .n { font-family: 'Playfair Display', serif; font-size: 15pt; color: #8E8A84; }
  .ladder b { display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 14pt; line-height: 1.1; } .ladder small { display: block; font-size: 8pt; color: #B8B3AA; margin-top: .5mm; } .ladder em { font-style: normal; font-family: 'Playfair Display', serif; font-size: 17pt; color: #E7D9A6; white-space: nowrap; }
  .setB { position: relative; width: 297mm; height: 210mm; } .setB .ph { width: 100%; height: 100%; }
  .setB::after { content: ""; position: absolute; inset: 0; background: linear-gradient(0deg, rgba(0,0,0,.85) 0%, rgba(0,0,0,.35) 40%, rgba(0,0,0,0) 65%); }
  .setB-t { position: absolute; left: 18mm; right: 18mm; bottom: 14mm; z-index: 1; display: grid; grid-template-columns: 1fr 100mm; gap: 12mm; align-items: end; color: #fff; } .setB-t .eb { color: rgba(255,255,255,.75); }
  .setB-r .chip { position: static; display: inline-grid; grid-template-columns: 13mm 1fr; margin-bottom: 4mm; } .kv-w div { display: grid; grid-template-columns: 26mm 1fr; gap: 3mm; font-size: 7.8pt; padding: 1.4mm 0; border-top: 1px solid rgba(255,255,255,.2); } .kv-w span:first-child { color: rgba(255,255,255,.6); }
  .setC { display: grid; grid-template-columns: 160mm 1fr; height: 210mm; } .setC-ph { display: grid; grid-template-rows: 1fr 60mm; height: 210mm; } .setC-ph .prod { width: 100%; height: 100%; object-fit: contain; background: #fff; padding: 10mm; }
  .setC-s { display: grid; grid-template-columns: 1fr 1fr; gap: 2mm; } .setC-s img { width: 100%; height: 100%; min-height: 0; } .setC .set-t { padding: 14mm 16mm 12mm 12mm; }
  .rB { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(3, 1fr); gap: 3mm; flex: 1; min-height: 0; padding: 0 18mm 12mm; } .rB-i { display: grid; grid-template-columns: 30mm 1fr; gap: 3mm; align-items: center; background: #171717; border: 1px solid rgba(255,255,255,.1); }
  .rB-i img { width: 30mm; height: 100%; min-height: 0; object-fit: contain; background: #fff; } .rB-i b { display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 11pt; line-height: 1.1; color: #F3F1EC; } .rB-i em { font-style: normal; font-size: 9pt; color: #E7D9A6; }
  .pB { position: absolute; left: 18mm; right: 18mm; bottom: 14mm; z-index: 1; color: #fff; } .pB-h h2 { color: #fff; } .pB .eb { color: rgba(255,255,255,.75); }
  .pB-g { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6mm; } .pB-g > div { border-top: 1px solid rgba(255,255,255,.35); padding-top: 2.5mm; } .pB-g b { font-family: 'Playfair Display', serif; font-weight: 400; font-size: 16pt; } .pB-g h3 { font-size: 12pt; margin: 1mm 0 1.5mm; color: #fff; } .pB-g p { font-size: 8.3pt; color: rgba(255,255,255,.85); margin: 0 0 1.5mm; } .pB-g small { font-size: 7.5pt; color: #E7D9A6; }
  .cB { position: absolute; left: 18mm; bottom: 16mm; width: 128mm; z-index: 1; background: rgba(241,239,234,.94); padding: 10mm 10mm 8mm; } .cB h2 { font-size: 20pt; } .cB p { font-size: 9.5pt; color: #4A4A47; }
  .cC { display: grid; grid-template-columns: 1fr 118mm; height: 210mm; } .cC .ph { width: 100%; height: 100%; } .cC-t { padding: 16mm 12mm 16mm 18mm; display: flex; flex-direction: column; justify-content: center; }
  .tel { font-family: 'Playfair Display', serif; font-size: 36pt; color: #E7D9A6; margin: 0 0 3mm; line-height: 1; } .cC-l { font-size: 10pt; color: #C9C5BE; line-height: 1.7; } .qrrow.w { margin-top: 8mm; } .contact.w { color: #F3F1EC; font-size: 12pt; } .contact.w small { color: #8E8A84; }
  .pg.dark .set-t h2, .pg.dark .hd h2 { color: #F7F5F0; }
  .cov .cov-m h1 { font-size: 40pt; } .cov .cov-f { gap: 2mm; } .cov .cov-f div { padding-top: 1.5mm; font-size: 8pt; } .cov .cov-f b { font-size: 10.5pt; }
  .abC-t p { font-size: 9.2pt; margin-bottom: 2.5mm; } .abC-t .nums.two b { font-size: 22pt; } .abC-t .nums.two { gap: 3mm 6mm; padding-top: 3mm; } .abC-t h2 { font-size: 22pt; margin-bottom: 3mm; }
'''
html = f'''<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>Obiimy — варіанти сторінок</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400;1,500&family=Tenor+Sans&display=swap" rel="stylesheet">
<style>{css}</style></head><body>{"".join(PAGES)}</body></html>'''
(OUT / "variants.html").write_text(typo(html))
script = OUT / "review" / "pp" / "pdf-variants.mjs"
script.write_text('''import puppeteer from 'puppeteer-core';
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--no-sandbox', '--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: 1123, height: 794 });
await p.goto('file:///Users/ivan/obiimy/variants.html', { waitUntil: 'networkidle0', timeout: 120000 }); await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: '/Users/ivan/obiimy/obiimy-variants.pdf', printBackground: true, preferCSSPageSize: true });
const els = await p.$$('.pg'); for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: `/Users/ivan/obiimy/review/pp/team/variants/v${String(i + 1).padStart(2, '0')}.png` });
await b.close(); console.log('variants', els.length);
''')
(OUT / "review" / "pp" / "team" / "variants").mkdir(parents=True, exist_ok=True)
subprocess.run(["node", str(script)], cwd=OUT / "review" / "pp", check=True)
print("pages:", len(PAGES), "size:", (OUT / "obiimy-variants.pdf").stat().st_size // 1024, "KB")
