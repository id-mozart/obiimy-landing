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


# ═════════════ РАДИКАЛЬНО НОВІ НАПРЯМИ ═════════════
def cut(src, cls=""):
    """RGBA cut-outs (img/cut) — copied as PNG so the transparency survives."""
    p = pathlib.Path(src); lb = OUT / "review" / "lb"; lb.mkdir(parents=True, exist_ok=True)
    j = lb / (p.stem + "-cut.png")
    if not j.exists():
        im = Image.open(OUT / src); im.thumbnail((1100, 1100)); im.save(j)
    return f'<img src="review/lb/{j.name}" class="{cls}" alt="">'
def mg_rows():
    return "".join('<div class="mg-tr"><span class="n">0%d</span>%s<div><b>%s</b><span>%s</span></div><em>%s</em></div>' % (i + 1, pic(S["gal"][PROD[i]][0], "th"), n, t, pr) for i, ((lb, n, t, pr, note, ph), S) in enumerate(zip(TIERS, SETS4)))
def yl_cards():
    cuts = ["img/cut/zolote-tw-1.webp", "img/cut/iskra-65-1.webp", "img/cut/flirt-scr-1.webp", "img/cut/zolote-44-1.webp"]
    return "".join('<div class="yl-c">%s<p class="eb">0%d · %s</p><b>%s</b><em>%s</em></div>' % (cut(c, "yl-ci"), i + 1, lb, n, pr) for i, ((lb, n, t, pr, note, ph), c) in enumerate(zip(TIERS, cuts)))
def nr4_cards():
    lines = ["Знак уваги.", "Спосіб носити.", "Про відпочинок.", "Більше, ніж річ."]
    return "".join('<div class="nr4-c">%s<div class="nr4-t"><p class="eb">0%d</p><b>%s</b><div class="chip">%s<div><span>%s</span><em>%s</em></div></div></div></div>' % (pic(S["tier"][0], "", S["tier"][1]), i + 1, lines[i], pic(S["gal"][PROD[i]][0], "chip-ph"), NAMES4[i], pr) for i, ((lb, n, t, pr, note, ph), S) in enumerate(zip(TIERS, SETS4)))
def solo_list():
    return "".join("<div><b>%s</b><span>%s</span></div>" % (n, st) for n, st, fm, pr, ph, fl in SOLO)

# R1 · Magazine — white paper, huge serif, wide margins, thin rules
page("R1 · Magazine — обкладинка: білий папір, великий сериф", f'<div class="mg cov"><div class="mg-top"><img src="brand/logo-ink.png" class="logo"><span>№ 01 · Подарунки для команди · 2026</span></div><h1 class="mg-h">Подарунки,<br>які <i>носять</i></h1><div class="mg-row">{pic("photo/lookbook/lb07-08-L.webp", "mg-ph", "50% 20%")}<div class="mg-side"><p class="eb">Для HR і офіс-менеджерів</p><p>Авторські принти на натуральному італійському шовку. Чотири рівні подарунка від 1 600 грн на людину. Пакування й наліпка з вашим логотипом — безкоштовно.</p><p class="mg-idx">Бренд — 2 · SOLO — 4 · Рівні й ціни — 7 · Набори — 8 · Запит — 15</p></div></div></div>', "white")
page("R1 · Magazine — SOLO: розворот із колонкою", f'<div class="mg"><div class="mg-top"><span>Колекція</span><span>SOLO · Шлях до себе</span></div><div class="mg-two">{pic("photo/solo/zolote-44-3.webp", "mg-big", "50% 18%")}<div class="mg-col"><h2 class="mg-h2">Шовкова свобода: <i>жіноча сила крізь десятиліття</i></h2><p>Натхнення — обкладинки модних журналів 40–50-х: змінювалися епохи й силуети, а хустка залишалася поруч. Сім авторських принтів — сім етапів шляху жінки до себе.</p><div class="mg-list">{solo_list()}</div><p class="mg-note">Твіллі — 1 600 грн · хустки з двостороннім друком від 2 400 грн · для команди: кожному свій принт або один на всіх</p></div></div></div>', "white")
page("R1 · Magazine — рівні як прайс-таблиця з великими цифрами", f'<div class="mg"><div class="mg-top"><span>Ціни</span><span>Чотири рівні подарунка</span></div><h2 class="mg-h2 big">Від 1 600 до 3 200 грн <i>на людину</i></h2><div class="mg-tbl">{mg_rows()}</div><p class="mg-note">Роздрібні ціни obiimy.world · команді з 50 людей — 80 000–160 000 грн за речі · майстер-клас і доставка — у розрахунку · чоловікам — сертифікат, маска, наволочка, закладка</p></div>', "white")

# R2 · Yellow box — the brand's packaging colour as the page
page("R2 · Yellow — обкладинка кольору коробки Obiimy", f'<div class="yl cov"><img src="brand/logo-ink.png" class="logo"><div class="yl-mid"><h1 class="yl-h">Подарунки<br>для команди</h1><p class="yl-sub">Шовк Obiimy · авторські принти · чотири рівні від 1 600 грн</p></div>{cut("img/cut/zolote-44-1.webp", "yl-cut")}<p class="yl-foot">Для HR і офіс-менеджерів · 2026 · пакування й наліпка з вашим логотипом — безкоштовно</p></div>', "yellow nopad")
page("R2 · Yellow — чотири подарунки вирізками на жовтому", f'<div class="yl"><div class="yl-hd"><p class="eb">Чотири рівні</p><h2 class="yl-h2">Що в коробці — і скільки це коштує</h2></div><div class="yl-grid">{yl_cards()}</div><p class="yl-foot">Роздрібні ціни obiimy.world · на фото — приклади принтів · команді з 50 людей — 80 000–160 000 грн за речі</p></div>', "yellow nopad")
page("R2 · Yellow — контакти: чорний на жовтому", f'<div class="yl cont"><div><p class="eb">Запит</p><h1 class="yl-h">Напишіть —<br>надішлемо добірку<br>й розрахунок</h1><p class="yl-tel">{PHONE}</p><p class="yl-sub">Telegram @OBIIMY_sales · {MAIL} · obiimy.world<br>Шоурум: {SHOWROOM}</p></div><div class="yl-qr">{qr_svg(LANDING, 120)}<span>сторінка для команд<br>із формою запиту</span></div></div>', "yellow nopad")

# R3 · Noir — every page is one ad creative
page("R3 · Noir — обкладинка як креатив", f'<div class="nr">{pic("photo/solo/zolote-44-2.webp", "full", "50% 20%")}<div class="nr-t"><img src="brand/logo-white.png" class="logo"><p class="eb">Подарунки для команди · 2026</p><h1 class="gi x">Мистецтво,<br>яке можна носити.</h1><p class="sub-w">Авторські принти на шовку — чотири рівні подарунка від 1 600 грн.</p><div class="chip inl">{pic("img/sets/tw44-zolote.webp", "chip-ph")}<div><span>Набір хустка + твіллі «Золоте світло»</span><em>3 600 грн</em></div></div></div></div>', "dark nopad")
page("R3 · Noir — SOLO як креатив", f'<div class="nr">{pic("photo/solo/tysha-88-2.webp", "full", "50% 20%")}<div class="nr-t"><p class="eb">Нова колекція SOLO</p><h1 class="gi x">Змінювалися епохи.<br>Хустка залишалася поруч.</h1><p class="sub-w">Сім авторських принтів — сім станів. Для команди: кожному свій або один на всіх.</p><div class="chip inl">{pic("photo/site/solo-tysha-88kh88-01.jpg", "chip-ph")}<div><span>Хустка «Тиша» 88 × 88, двосторонній друк</span><em>6 600 грн</em></div></div></div></div>', "dark nopad")
page("R3 · Noir — чотири рівні як чотири креативи", f'<div class="nr4">{nr4_cards()}</div>', "dark nopad")

# R4 · Tear sheets — cream board, overlapping photo cards, italic captions
page("R4 · Tear sheets — обкладинка-колаж", f'<div class="ts"><img src="brand/logo-ink.png" class="logo"><div class="ts-board">{pic("photo/solo/krok-44-2.webp", "ts-c c1")}{pic("photo/lookbook/lb41-43-L.webp", "ts-c c2", "50% 20%")}{pic("photo/site/set-tvilli-845-ta-khustky-4444-natkhne-01.jpg", "ts-c c3")}{pic("photo/solo/flirt-tw-4.webp", "ts-c c4", "50% 35%")}<div class="ts-note n1"><i>твіллі у волоссі —</i><br>1 600 грн</div><div class="ts-note n2"><i>набір у коробці</i><br>3 200 грн</div></div><div class="ts-t"><h1>Подарунки<br>для команди</h1><p class="it">Шовк Obiimy · авторські принти · чотири рівні від 1 600 грн</p></div></div>', "nopad")
page("R4 · Tear sheets — набір як дошка натхнення", f'<div class="ts"><div class="ts-board wide">{pic(S1["hero"][0], "ts-c d1", S1["hero"][2])}{pic(S1["gal"][0][0], "ts-c d2", S1["gal"][0][2])}{pic(S1["gal"][PROD[1]][0], "ts-c d3")}{pic("photo/box-gold.jpg", "ts-c d4", "50% 45%")}<div class="ts-note m1"><i>хустка 44 × 44 —</i><br>на шиї, на сумці, поясом</div><div class="ts-note m2"><i>+ кільце Gold</i><br>450 грн</div></div><div class="ts-t r"><p class="eb">{S1["lb"]}</p><h2>{S1["name"]}</h2><p class="rrp">{S1["pr"]}<small>{S1["prnote"]}</small></p><div class="kv">{kv(S1["inside"][:4])}</div><p class="who">{S1["who"]}</p></div></div>', "nopad")


# ═════════════ ЩЕ ШІСТЬ НАПРЯМІВ ═════════════
FLATS = [f for n, st, fm, pr, ph, f in SOLO]          # seven SOLO flat-lays
POOL = ["photo/solo/iskra-65-2.webp", "photo/solo/flirt-tw-4.webp", "photo/solo/puls-44-2.webp", "photo/solo/zolote-44-5.webp", "photo/solo/avantiura-88-5.webp", "photo/solo/tysha-88-3.webp", "photo/solo/krok-44-2.webp", "photo/solo/zolote-44-3.webp", "photo/solo/avantiura-88-2.webp", "photo/solo/krok-tw-3.webp", "photo/solo/iskra-tw-3.webp", "photo/solo/puls-44-4.webp", "photo/solo/tysha-88-2.webp", "photo/solo/zolote-tw-2.webp", "photo/solo/flirt-65-3.webp", "photo/solo/avantiura-tw-4.webp", "photo/solo/krok-44-4.webp", "photo/solo/puls-44-5.webp", "photo/dotyk-1.webp", "photo/kolo-1.webp", "photo/enerhiia-back.webp", "photo/lookbook/lb05-06-L.webp", "photo/lookbook/lb40-42-R.webp", "photo/site/set-smilyvist-02.jpg"]


def pr7_strips():
    return "".join('<div class="pr7-s">%s<div class="pr7-t"><b>%s</b><span>%s</span></div></div>' % (pic(f), n, st) for (n, st, fm, prc, ph, f) in SOLO)
def ty_cards():
    out = []
    for i, ((lb, n, t, pr, note, ph), S) in enumerate(zip(TIERS, SETS4)):
        num = pr.replace(" грн", "").replace("від ", "<small>від</small> ")
        out.append('<div class="ty-c"><em>%s</em><div class="ty-cl">%s<div><b>%s</b><span>%s</span></div></div></div>' % (num, pic(S["gal"][PROD[i]][0], "th"), n, lb))
    return "".join(out)
def fm3_frames():
    F = [("photo/solo/avantiura-88-2.webp", "50% 30%", "У 40-х жінка підкреслювала силу бездоганною елегантністю."), ("photo/solo/iskra-65-2.webp", "50% 25%", "У 50-х правила почали руйнуватися: колір, форма, власна ідентичність."), ("photo/solo/zolote-44-5.webp", "50% 25%", "Змінювалися епохи й силуети, а хустка залишалася поруч.")]
    return "".join('<div class="fm3-f">%s<p class="fm3-s">%s</p></div>' % (pic(f, "", ps), t) for f, ps, t in F)
def ga_works():
    W = [("g1", "photo/solo/iskra-65-5.webp", "50% 50%", "«Іскра»", "шовк, 65 × 65, 2026"), ("g2", "photo/solo/puls-44-1.webp", "50% 50%", "«Пульс»", "шовк, 44 × 44, 2026"), ("g3", "photo/solo/avantiura-88-1.webp", "50% 50%", "«Авантюра»", "шовк, 88 × 88, 2026")]
    return "".join('<figure class="ga-w %s">%s<figcaption><b>%s</b><span>%s</span></figcaption></figure>' % (c, pic(f, "", ps), n, d) for c, f, ps, n, d in W)
def cs_cells():
    return "".join(pic(f, "cs-i" + (" on" if i == 7 else "")) for i, f in enumerate(POOL))
def du4_cards():
    return "".join('<div class="du4-c">%s<div class="du-ov"></div><div class="du4-t"><span>0%d</span><b>%s</b><em>%s</em></div></div>' % (pic(S["tier"][0], "du-ph", S["tier"][1]), i + 1, NAMES4[i], pr) for i, ((lb, n, t, pr, note, ph), S) in enumerate(zip(TIERS, SETS4)))

# R5 · Print as the page — a flat-lay bleeds, a paper card floats on it
page("R5 · Print — принт як фон, картка на ньому", f'<div class="pr">{pic("photo/vyr-flat.webp", "full", "50% 50%")}<div class="pr-card"><img src="brand/logo-ink.png" class="logo"><p class="eb">Для HR і офіс-менеджерів · 2026</p><h1>Подарунки<br>для команди</h1><p class="it">Авторські принти на натуральному італійському шовку</p><p class="pr-line">Чотири рівні від 1 600 грн на людину · пакування й наліпка з вашим логотипом — безкоштовно</p></div></div>', "nopad")
page("R5 · Print — сім принтів смугами, модель у врізці", f'<div class="pr7">{pr7_strips()}<div class="pr7-in">{pic("photo/solo/zolote-44-3.webp", "", "50% 18%")}<div><p class="eb">Колекція SOLO</p><h2>Сім принтів —<br>сім станів</h2><p>Кожному в команді — свій принт, під стан, який хочете побажати. Твіллі — 1 600 грн, хустки з двостороннім друком — від 2 400 грн.</p></div></div></div>', "nopad")

# R6 · Type — numbers as the hero, photo small
page("R6 · Type — обкладинка: гігантська цифра", f'<div class="ty"><div class="ty-top"><img src="brand/logo-ink.png" class="logo"><span>Подарунки для команди · 2026</span></div><div class="ty-big"><span class="num">4</span><div class="ty-side"><h1>рівні подарунка<br>від <i>1 600 грн</i></h1><p>Шовк Obiimy для команди: авторські принти, пакування з вашим логотипом — безкоштовно. Напишіть нагоду, кількість і дату.</p></div></div>{pic("photo/solo/krok-tw-4.webp", "ty-ph", "48% 50%")}</div>', "white nopad")
page("R6 · Type — ціни як дизайн", f'<div class="ty"><div class="ty-top"><span>Чотири рівні</span><span>роздрібні ціни obiimy.world</span></div><div class="ty-grid">{ty_cards()}</div><p class="ty-foot">грн на людину · команді з 50 людей — 80 000–160 000 грн за речі · майстер-клас і доставка — у розрахунку · чоловікам — сертифікат, маска, наволочка, закладка</p></div>', "white nopad")

# R7 · Film — letterbox frames and subtitles
page("R7 · Film — обкладинка з субтитрами", f'<div class="fm">{pic("photo/solo/tysha-88-2.webp", "fm-ph", "50% 30%")}<div class="fm-sub"><img src="brand/logo-white.png" class="logo"><p class="fm-l1">Подарунки для команди</p><p class="fm-l2">Авторські принти на італійському шовку · чотири рівні від 1 600 грн · 2026</p></div></div>', "dark nopad")
page("R7 · Film — SOLO трьома кадрами", f'<div class="fm3">{fm3_frames()}<div class="fm3-t"><p class="eb">Нова колекція</p><h2>SOLO. Шлях до себе</h2><p>Сім авторських принтів — сім станів. Для команди: кожному свій або один на всіх.</p></div></div>', "dark nopad")

# R8 · Gallery — framed works on a white wall, museum labels
page("R8 · Gallery — «Мистецтво, яке можна носити»: обкладинка-виставка", f'<div class="ga"><div class="ga-wall">{ga_works()}</div><div class="ga-t"><img src="brand/logo-ink.png" class="logo"><h1>Мистецтво,<br>яке можна носити</h1><p class="it">Подарунки для команди · авторські принти на шовку · чотири рівні від 1 600 грн</p></div></div>', "white nopad")
page("R8 · Gallery — набір як експонат", f'<div class="ga two"><figure class="ga-w big">{pic(S1["gal"][PROD[1]][0], "", "50% 50%")}<figcaption><b>{S1["short"]}</b><span>шовк, 44 × 44 · кільце Gold · {S1["pr"]}</span></figcaption></figure><div class="ga-side">{pic(S1["hero"][0], "ga-m", S1["hero"][2])}<div><p class="eb">{S1["lb"]}</p><h2>{S1["name"]}</h2><p class="ga-p">{S1["lead"]}</p><div class="kv">{kv(S1["inside"][:4])}</div></div></div></div>', "white nopad")

# R9 · Contact sheet — «обери свій принт»: a wall of frames, one lit
page("R9 · Contact sheet — стіна кадрів, один підсвічений", f'<div class="cs"><div class="cs-grid">{cs_cells()}</div><div class="cs-t"><img src="brand/logo-white.png" class="logo"><h1 class="gi x">Кожному —<br>свій принт.</h1><p class="sub-w">38 принтів твіллі, сім нових із SOLO. Подарунок для команди, який не повторюється. Від 1 600 грн на людину.</p></div></div>', "dark nopad")

# R10 · Duotone — brand yellow over black-and-white photography
page("R10 · Duotone — жовто-чорний постер", f'<div class="du">{pic("photo/solo/zolote-44-2.webp", "du-ph", "50% 20%")}<div class="du-ov"></div><div class="du-t"><img src="brand/logo-ink.png" class="logo"><h1>Подарунки<br>для команди</h1><p class="du-l">Шовк Obiimy · чотири рівні від 1 600 грн · логотип — безкоштовно</p></div></div>', "nopad")
page("R10 · Duotone — чотири рівні постерами", f'<div class="du4">{du4_cards()}</div>', "nopad")

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

  /* R5 print */
  .pr { position: relative; width: 297mm; height: 210mm; } .pr .full { width: 100%; height: 100%; }
  .pr-card { position: absolute; left: 18mm; top: 22mm; width: 118mm; background: #F8F6F1; padding: 12mm 12mm 10mm; box-shadow: 0 10mm 20mm rgba(0,0,0,.25); } .pr-card .logo { height: 9mm; width: auto; margin-bottom: 10mm; } .pr-card h1 { font-size: 40pt; margin: 1mm 0 4mm; } .pr-card .it { color: #4A4A47; font-size: 12pt; } .pr-line { font-size: 8.5pt; color: #6B6772; border-top: 1px solid #C9C6C0; padding-top: 3mm; margin: 6mm 0 0; }
  .pr7 { position: relative; display: grid; grid-template-columns: repeat(7, 1fr); width: 297mm; height: 210mm; } .pr7-s { position: relative; overflow: hidden; } .pr7-s img { width: 100%; height: 100%; }
  .pr7-t { position: absolute; left: 0; right: 0; bottom: 0; padding: 4mm 3mm; background: linear-gradient(0deg, rgba(0,0,0,.7), rgba(0,0,0,0)); color: #fff; } .pr7-t b { display: block; font-family: 'Playfair Display', serif; font-style: italic; font-weight: 400; font-size: 12pt; color: #F3EBD0; } .pr7-t span { font-size: 6.5pt; opacity: .85; }
  .pr7-in { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 170mm; display: grid; grid-template-columns: 70mm 1fr; background: #F8F6F1; box-shadow: 0 10mm 24mm rgba(0,0,0,.35); } .pr7-in img { width: 100%; height: 100%; } .pr7-in > div { padding: 10mm 10mm 8mm; } .pr7-in h2 { font-size: 24pt; margin: 1mm 0 3mm; } .pr7-in p { font-size: 9pt; color: #4A4A47; }
  /* R6 type */
  .ty { padding: 14mm 18mm 12mm; height: 210mm; display: flex; flex-direction: column; position: relative; } .ty-top { display: flex; justify-content: space-between; align-items: center; font-size: 7.5pt; letter-spacing: .2em; text-transform: uppercase; color: #6B6772; border-bottom: 1px solid #141414; padding-bottom: 3mm; } .ty-top .logo { height: 8mm; width: auto; }
  .ty-big { display: grid; grid-template-columns: auto 1fr; gap: 10mm; align-items: center; flex: 1; } .ty-big .num { font-family: 'Playfair Display', serif; font-size: 330pt; line-height: .8; letter-spacing: -.04em; } .ty-side h1 { font-size: 36pt; line-height: 1.05; margin: 0 0 5mm; } .ty-side h1 i { color: #8E8A84; } .ty-side p { font-size: 10pt; color: #4A4A47; max-width: 90mm; }
  .ty-ph { position: absolute; right: 18mm; bottom: 12mm; width: 62mm; height: 78mm; object-fit: cover; }
  .ty-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 14mm; flex: 1; align-content: center; } .ty-c { border-bottom: 1px solid #141414; padding: 6mm 0; } .ty-c em { display: block; font-style: normal; font-family: 'Playfair Display', serif; font-size: 58pt; line-height: .9; letter-spacing: -.03em; white-space: nowrap; } .ty-c em small { font-size: 22pt; color: #8E8A84; letter-spacing: 0; }
  .ty-cl { display: grid; grid-template-columns: 16mm 1fr; gap: 4mm; align-items: center; margin-top: 4mm; } .ty-cl .th { width: 16mm; height: 16mm; object-fit: cover; } .ty-cl b { display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 13pt; line-height: 1.05; } .ty-cl span { font-size: 7.5pt; letter-spacing: .14em; text-transform: uppercase; color: #6B6772; }
  .ty-foot { font-size: 8pt; color: #6B6772; margin: 4mm 0 0; }
  /* R7 film */
  .fm { position: relative; width: 297mm; height: 210mm; background: #000; display: flex; align-items: center; } .fm-ph { width: 100%; height: 124mm; object-fit: cover; }
  .fm-sub { position: absolute; left: 0; right: 0; bottom: 14mm; text-align: center; color: #fff; } .fm-sub .logo { height: 8mm; width: auto; margin: 0 auto 4mm; } .fm-l1 { font-family: 'Playfair Display', serif; font-size: 22pt; margin: 0 0 1.5mm; color: #F3EBD0; } .fm-l2 { font-size: 9.5pt; letter-spacing: .06em; color: rgba(255,255,255,.85); margin: 0; }
  .fm3 { position: relative; width: 297mm; height: 210mm; background: #000; display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; align-content: center; padding: 0 0 36mm; } .fm3-f { position: relative; } .fm3-f img { width: 100%; height: 100mm; object-fit: cover; }
  .fm3-s { position: absolute; left: 4mm; right: 4mm; bottom: 4mm; margin: 0; text-align: center; font-size: 8.5pt; color: #fff; text-shadow: 0 1px 3px rgba(0,0,0,.8); }
  .fm3-t { position: absolute; left: 18mm; right: 18mm; bottom: 12mm; display: grid; grid-template-columns: auto 1fr; gap: 10mm; align-items: end; color: #fff; } .fm3-t h2 { margin: 0; font-size: 26pt; color: #F3EBD0; } .fm3-t p { margin: 0; font-size: 9.5pt; color: rgba(255,255,255,.85); max-width: 120mm; } .fm3-t .eb { color: rgba(255,255,255,.6); }
  /* R8 gallery */
  .ga { position: relative; width: 297mm; height: 210mm; background: #fff; } .ga-wall { position: absolute; inset: 0; background: linear-gradient(180deg, #fff 0, #fff 78%, #ECE9E3 78%, #ECE9E3 100%); }
  .ga-w { position: absolute; margin: 0; background: #fff; padding: 6mm; box-shadow: 0 0 0 1px #141414, 0 8mm 16mm rgba(0,0,0,.14); } .ga-w img { display: block; object-fit: cover; width: 100%; height: 100%; }
  .ga-w figcaption { position: absolute; left: 0; bottom: -14mm; font-size: 7pt; color: #4A4A47; } .ga-w figcaption b { display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 9.5pt; color: #141414; }
  .g1 { left: 118mm; top: 24mm; width: 70mm; height: 70mm; } .g2 { left: 196mm; top: 40mm; width: 56mm; height: 56mm; } .g3 { left: 236mm; top: 10mm; width: 44mm; height: 44mm; }
  .ga-t { position: absolute; left: 18mm; bottom: 20mm; max-width: 96mm; } .ga-t .logo { height: 9mm; width: auto; margin-bottom: 10mm; } .ga-t h1 { font-size: 40pt; line-height: 1; margin: 0 0 4mm; } .ga-t .it { color: #4A4A47; font-size: 11pt; }
  .ga.two { display: grid; grid-template-columns: 150mm 1fr; background: #fff; } .ga-w.big { position: relative; left: auto; top: auto; margin: 22mm 18mm 30mm 24mm; width: auto; height: auto; } .ga-w.big img { height: 120mm; object-fit: contain; }
  .ga-side { padding: 22mm 18mm 16mm 0; display: grid; grid-template-rows: 70mm 1fr; gap: 8mm; } .ga-m { width: 100%; height: 100%; object-fit: cover; } .ga-side h2 { font-size: 20pt; margin: 1mm 0 3mm; } .ga-p { font-size: 9pt; color: #4A4A47; }
  .ga-side .kv div { display: grid; grid-template-columns: 24mm 1fr; gap: 3mm; font-size: 7.8pt; padding: 1.4mm 0; border-top: 1px solid #DAD7D0; } .ga-side .kv span:first-child { color: #6B6772; }
  /* R9 contact sheet */
  .cs { position: relative; width: 297mm; height: 210mm; background: #0A0A0A; } .cs-grid { position: absolute; inset: 0; display: grid; grid-template-columns: repeat(8, 1fr); grid-template-rows: repeat(3, 1fr); gap: 1.5mm; padding: 1.5mm; }
  .cs-i { width: 100%; height: 100%; object-fit: cover; filter: grayscale(1) brightness(.45); } .cs-i.on { filter: none; outline: 2px solid #E7D9A6; outline-offset: -2px; }
  .cs-t { position: absolute; left: 18mm; bottom: 16mm; max-width: 150mm; z-index: 2; color: #fff; background: rgba(0,0,0,.55); padding: 8mm 10mm; backdrop-filter: blur(4px); } .cs-t .logo { height: 8mm; width: auto; margin-bottom: 6mm; }
  /* R10 duotone */
  .du { position: relative; width: 297mm; height: 210mm; background: #F7C600; } .du-ph { width: 100%; height: 100%; object-fit: cover; filter: grayscale(1) contrast(1.15); mix-blend-mode: multiply; }
  .du-ov { position: absolute; inset: 0; background: linear-gradient(0deg, rgba(0,0,0,.6) 0%, rgba(0,0,0,0) 50%); pointer-events: none; }
  .du-t { position: absolute; left: 18mm; bottom: 16mm; z-index: 2; color: #F3EBD0; } .du-t .logo { height: 10mm; width: auto; margin-bottom: 8mm; filter: invert(1) brightness(2); } .du-t h1 { font-size: 54pt; line-height: .96; margin: 0 0 4mm; } .du-l { font-size: 10pt; margin: 0; }
  .du4 { display: grid; grid-template-columns: repeat(4, 1fr); width: 297mm; height: 210mm; gap: 2mm; background: #141414; } .du4-c { position: relative; background: #F7C600; overflow: hidden; } .du4-c .du-ph { height: 100%; }
  .du4-t { position: absolute; left: 5mm; right: 5mm; bottom: 7mm; z-index: 2; color: #F3EBD0; } .du4-t span { font-size: 8pt; letter-spacing: .2em; } .du4-t b { display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 16pt; line-height: 1.05; margin: 1mm 0 2mm; } .du4-t em { font-style: normal; font-family: 'Playfair Display', serif; font-size: 15pt; }
  /* R1 magazine */
  .pg.white .mg { padding: 0; height: 100%; display: flex; flex-direction: column; }
  .mg-top { display: flex; justify-content: space-between; align-items: center; font-size: 7.5pt; letter-spacing: .2em; text-transform: uppercase; color: #6B6772; border-bottom: 1px solid #141414; padding-bottom: 3mm; margin-bottom: 8mm; } .mg-top .logo { height: 8mm; width: auto; }
  .mg-h { font-size: 64pt; line-height: .95; margin: 0 0 8mm; letter-spacing: -.02em; } .mg-h i, .mg-h2 i { font-style: italic; font-weight: 400; color: #8E8A84; }
  .mg-row { display: grid; grid-template-columns: 118mm 1fr; gap: 12mm; flex: 1; min-height: 0; align-items: end; } .mg-ph { width: 100%; height: 100%; min-height: 0; object-fit: cover; }
  .mg-side p { font-size: 10pt; color: #4A4A47; max-width: 92mm; } .mg-idx { font-size: 7.5pt; letter-spacing: .12em; text-transform: uppercase; color: #8E8A84; border-top: 1px solid #DAD7D0; padding-top: 3mm; margin-top: 6mm; }
  .mg-two { display: grid; grid-template-columns: 150mm 1fr; gap: 12mm; flex: 1; min-height: 0; } .mg-big { width: 100%; height: 100%; min-height: 0; object-fit: cover; }
  .mg-h2 { font-size: 28pt; line-height: 1.05; margin: 0 0 5mm; } .mg-h2.big { font-size: 40pt; margin-bottom: 8mm; } .mg-col p { font-size: 9.6pt; color: #4A4A47; }
  .mg-list { display: grid; grid-template-columns: 1fr 1fr; gap: 1mm 6mm; margin: 4mm 0; } .mg-list div { border-top: 1px solid #DAD7D0; padding: 1.8mm 0; } .mg-list b { display: block; font-family: 'Playfair Display', serif; font-style: italic; font-weight: 400; font-size: 11.5pt; } .mg-list span { font-size: 7.5pt; color: #6B6772; }
  .mg-note { font-size: 8pt; color: #6B6772; border-top: 1px solid #141414; padding-top: 3mm; margin-top: auto; }
  .mg-tbl { display: grid; flex: 1; align-content: start; } .mg-tr { display: grid; grid-template-columns: 16mm 22mm 1fr auto; gap: 6mm; align-items: center; padding: 5mm 0; border-top: 1px solid #141414; }
  .mg-tr .n { font-family: 'Playfair Display', serif; font-size: 22pt; color: #8E8A84; } .mg-tr .th { width: 22mm; height: 22mm; object-fit: cover; } .mg-tr b { display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 18pt; line-height: 1.05; } .mg-tr span { font-size: 9pt; color: #4A4A47; } .mg-tr em { font-style: normal; font-family: 'Playfair Display', serif; font-size: 26pt; white-space: nowrap; }
  /* R2 yellow */
  .pg.yellow { background: #F7C600; color: #141414; } .yl { padding: 16mm 18mm 14mm; height: 210mm; display: flex; flex-direction: column; position: relative; } .yl .logo { height: 11mm; width: auto; align-self: flex-start; }
  .yl-mid { margin: auto 0; max-width: 150mm; } .yl-h { font-size: 56pt; line-height: .96; margin: 0 0 5mm; } .yl-sub { font-size: 12pt; margin: 0; }
  .yl-cut { position: absolute; right: 10mm; top: 24mm; width: 128mm; height: auto; transform: rotate(8deg); filter: drop-shadow(0 12mm 10mm rgba(0,0,0,.18)); }
  .yl-foot { font-size: 8pt; letter-spacing: .1em; text-transform: uppercase; margin: 0; border-top: 1px solid rgba(0,0,0,.35); padding-top: 3mm; }
  .yl-hd .eb { color: rgba(0,0,0,.6); } .yl-h2 { font-size: 30pt; margin: 0 0 6mm; }
  .yl-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6mm; flex: 1; min-height: 0; margin-bottom: 6mm; } .yl-c { background: #fff; padding: 6mm; display: flex; flex-direction: column; min-height: 0; }
  .yl-ci { width: 100%; flex: 1; min-height: 0; object-fit: contain; margin-bottom: 4mm; } .yl-c .eb { color: #8E8A84; margin-bottom: 1mm; } .yl-c b { font-family: 'Playfair Display', serif; font-weight: 400; font-size: 14pt; line-height: 1.05; } .yl-c em { font-style: normal; font-family: 'Playfair Display', serif; font-size: 17pt; margin-top: 1.5mm; }
  .yl.cont { justify-content: center; } .yl-tel { font-family: 'Playfair Display', serif; font-size: 40pt; margin: 6mm 0 3mm; line-height: 1; } .yl.cont .yl-h { font-size: 40pt; }
  .yl-qr { position: absolute; right: 18mm; bottom: 16mm; display: grid; grid-template-columns: auto 1fr; gap: 5mm; align-items: center; font-size: 8.5pt; }
  /* R3 noir */
  .nr { position: relative; width: 297mm; height: 210mm; } .nr .full { width: 100%; height: 100%; filter: saturate(.9); }
  .nr::after { content: ""; position: absolute; inset: 0; background: radial-gradient(120% 90% at 70% 40%, rgba(0,0,0,0) 30%, rgba(0,0,0,.75) 100%), linear-gradient(0deg, rgba(0,0,0,.7) 0%, rgba(0,0,0,0) 50%); }
  .nr-t { position: absolute; left: 18mm; bottom: 16mm; max-width: 160mm; z-index: 1; color: #fff; } .nr-t .logo { height: 9mm; width: auto; margin-bottom: 8mm; } .nr-t .eb { color: rgba(255,255,255,.7); }
  .gi.x { font-size: 40pt; line-height: 1.02; margin: 1mm 0 4mm; }
  .nr4 { display: grid; grid-template-columns: repeat(4, 1fr); height: 210mm; } .nr4-c { position: relative; overflow: hidden; } .nr4-c img:first-child { width: 100%; height: 100%; }
  .nr4-c::after { content: ""; position: absolute; inset: 0; background: linear-gradient(0deg, rgba(0,0,0,.85) 0%, rgba(0,0,0,.2) 55%, rgba(0,0,0,0) 100%); }
  .nr4-t { position: absolute; left: 5mm; right: 5mm; bottom: 6mm; z-index: 2; color: #fff; } .nr4-t .eb { color: rgba(255,255,255,.7); } .nr4-t b { display: block; font-family: 'Playfair Display', serif; font-style: italic; font-weight: 400; font-size: 19pt; line-height: 1.05; color: #F3EBD0; margin-bottom: 4mm; }
  .nr4-t .chip { position: static; display: grid; }
  /* R4 tear sheets */
  .ts { position: relative; width: 297mm; height: 210mm; background: #EDE8DF; overflow: hidden; } .ts .logo { position: absolute; top: 14mm; left: 18mm; height: 9mm; width: auto; z-index: 3; }
  .ts-board { position: absolute; inset: 0; } .ts-c { position: absolute; object-fit: cover; box-shadow: 0 10mm 14mm rgba(0,0,0,.22); background: #fff; }
  .c1 { left: 118mm; top: 18mm; width: 86mm; height: 112mm; transform: rotate(-4deg); } .c2 { left: 190mm; top: 44mm; width: 84mm; height: 110mm; transform: rotate(3deg); } .c3 { left: 150mm; top: 118mm; width: 72mm; height: 72mm; transform: rotate(-2deg); } .c4 { left: 232mm; top: 10mm; width: 50mm; height: 66mm; transform: rotate(6deg); }
  .ts-note { position: absolute; font-family: 'Playfair Display', serif; font-size: 11pt; line-height: 1.2; background: #fff; padding: 3mm 4mm; box-shadow: 0 4mm 8mm rgba(0,0,0,.15); } .n1 { left: 104mm; top: 128mm; transform: rotate(-6deg); } .n2 { left: 236mm; top: 160mm; transform: rotate(4deg); }
  .ts-t { position: absolute; left: 18mm; bottom: 18mm; max-width: 90mm; z-index: 3; } .ts-t h1 { font-size: 44pt; line-height: .98; margin: 0 0 4mm; } .ts-t .it { color: #4A4A47; font-size: 11pt; }
  .ts-board.wide .d1 { left: 14mm; top: 14mm; width: 96mm; height: 128mm; transform: rotate(-3deg); } .d2 { left: 96mm; top: 24mm; width: 70mm; height: 70mm; transform: rotate(4deg); } .d3 { left: 60mm; top: 118mm; width: 64mm; height: 64mm; transform: rotate(-5deg); } .d4 { left: 124mm; top: 102mm; width: 54mm; height: 72mm; transform: rotate(5deg); }
  .m1 { left: 20mm; top: 152mm; transform: rotate(-3deg); } .m2 { left: 132mm; top: 40mm; transform: rotate(6deg); }
  .ts-t.r { left: auto; right: 18mm; top: 16mm; bottom: auto; max-width: 96mm; } .ts-t.r h2 { font-size: 22pt; margin: 1mm 0 3mm; } .ts-t.r .rrp { font-family: 'Playfair Display', serif; font-size: 19pt; margin: 0 0 3mm; } .ts-t.r .rrp small { display: block; font-family: 'Tenor Sans', sans-serif; font-size: 7pt; color: #6B6772; margin-top: 1mm; }
  .ts-t.r .kv div { display: grid; grid-template-columns: 24mm 1fr; gap: 3mm; font-size: 7.8pt; padding: 1.4mm 0; border-top: 1px solid #C9C6C0; } .ts-t.r .kv span:first-child { color: #6B6772; } .ts-t.r .who { font-family: 'Playfair Display', serif; font-style: italic; font-size: 12pt; margin-top: 4mm; }

  .cov .cov-p { height: 210mm; overflow: hidden; justify-content: space-between; } .cov .cov-m { margin: 0; } .cov .cov-m h1 { font-size: 40pt; } .cov .cov-f { gap: 2mm; } .cov .cov-f div { padding-top: 1.5mm; font-size: 8pt; } .cov .cov-f b { font-size: 10.5pt; }
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
