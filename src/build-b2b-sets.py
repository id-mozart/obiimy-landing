#!/usr/bin/env python3
"""B2B set landings: a catalogue of corporate sets (Maison), one print for the whole company (Journal),
and a scroll-driven CSS 3D unboxing (dark art template src/b2b-unboxing.html)."""
import importlib.util, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
_spec = importlib.util.spec_from_file_location("b2b", ROOT / "build-b2b.py")
b2b = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(b2b)
img, typo, hero, facts_html, proof_html, form_html, shell = b2b.img, b2b.typo, b2b.hero, b2b.facts_html, b2b.proof_html, b2b.form_html, b2b.shell
PHONE, PHONE_HREF, MAIL, DOCS_FAQ, BATCH_FAQ = b2b.PHONE, b2b.PHONE_HREF, b2b.MAIL, b2b.DOCS_FAQ, b2b.BATCH_FAQ
_x = importlib.util.spec_from_file_location("x", ROOT / "build-b2b-extra.py"); X = importlib.util.module_from_spec(_x); _x.loader.exec_module(X)
BASE_FIELDS, PAY, contact = X.BASE_FIELDS, X.PAY, X.contact
PROOF = proof_html("Де вже є Obiimy", "Obiimy продається у роздрібних партнерів в Україні та за кордоном, а історію бренду розповідали LIGA.net та INSIDER UA.")

def price(n): return f"{n:,}".replace(",", " ") + " грн"

# ---------- catalogue items (verified retail prices) ----------
ITEM = {
    "scr":  ("Резинка для волосся", 700,  "img/scrunchie-energiia.webp"),
    "tw":   ("Твіллі 84 × 5", 1600, "img/twilly-zolote.webp"),
    "h44":  ("Хустка 44 × 44", 1600, "img/melodiia.webp"),
    "h65":  ("Хустка 65 × 65", 3200, "img/tysha-sertsia.webp"),
    "d65":  ("Двостороння 65 × 65", 4800, "img/probudzhennia.webp"),
    "h88":  ("Шаль 88 × 88", 4400, "img/kolo-sontsia.webp"),
    "mask": ("Маска для сну", 2700, "img/mask-vpevnenist.webp"),
}
# existing sets on obiimy.world (price from the site) and proposed combinations (sum of retail prices, «під запит»)
SITE = "https://obiimy.world"
# Real gift-set families from obiimy.world/podarunkovi-nabory (checked 28.09.2026, see review/SITE-FACTS.md)
# plus B2B combinations of real catalogue items («Під запит», price = sum of item prices).
SETS = [
    dict(id="scrset", name="Набір шовкових резинок", who="Welcome-box і великі команди", price=1250, price_label="від 1 250 грн",
         prices="Zero waste 3 шт. — 1 250 · 3 шт. — 1 800 · Zero waste 5 шт. — 2 000 грн", photo="img/sets/scr3.webp", kind="Каталог",
         line="Кілька шовкових резинок у фірмовому стилі: найдоступніший подарунок Obiimy, який не залежить від розміру.", link=SITE + "/nabir-3-shovkovykh-rezynky/"),
    dict(id="twscr", name="Твіллі та резинка", who="Усій команді", price=2200, price_label="2 200 грн",
         prices="84 × 5 — 2 200 грн · довга 140 × 5 — 2 700 грн", photo="img/sets/twscr-makiv.webp", kind="Каталог",
         prints="Пристрасть, Сміливість, Літнє поле, Маків цвіт, Енергія, Свобода, Ніжність, Захоплення · 140 × 5: Літній віночок, Спокуса",
         line="Твіллі й резинка в одному принті у святковій коробці.", link=SITE + "/tvilli-ta-rezynka-prystrast/"),
    dict(id="maskscr", name="Маска для сну та резинка", who="Програмам турботи про команду", price=3100, price_label="3 100 грн",
         photo="img/sets/maskscr-litnie-pole.webp", kind="Каталог",
         prints="Літнє поле, Енергія, Свобода, Впевненість, Піднесення, Мелодія двох, Сміливість, Серцебиття",
         line="Подарунок про відпочинок, а не про роботу: шовкова маска й резинка в жовтій коробці.", link=SITE + "/maska-dlia-snu-ta-rezynka-litnie-pole/"),
    dict(id="tw44", name="Твіллі та хустка 44 × 44", who="Ключовим людям", price=3200, price_label="3 200 грн",
         prices="одностороння — 3 200 грн · двосторонній друк — 3 600 грн", photo="img/sets/tw44-vpevnenist.webp", kind="Каталог",
         prints="18 принтів: Впевненість, Натхнення, Грація, Вир почуттів, Сміливий дотик, Баланс, Свобода, Літнє поле… · двосторонні: Пробудження, Ніжність, Пристрасть, Закоханість, Захоплення, Літній віночок; новинка — Золоте світло (3 600 грн)",
         line="Класичне поєднання: стрічка й хустка в одному принті, у довгій жовтій коробці з тонким папером.", link=SITE + "/nabir-tvilli-845-ta-khustky-4444-vpevnenist/"),
    dict(id="song", name="Маска, закладка й резинка", who="Подарунок із сенсом · «Співоча душа»", price=3600, price_label="3 600 грн",
         photo="img/sets/sleep-pidnesennia.webp", kind="Каталог", prints="«Піднесення», «Мелодія двох»",
         line="Набір із колекції «Співоча душа»: частина коштів від колекції йде на гнізда для сиворакші — птаха з Червоної книги України.", link=SITE + "/maska-dlia-snu-zakladka-dlia-knyhy-ta-shovkova-rezynka-dlia-volossia-pidnesennia/"),
    dict(id="hearts", name="Дві маски «Серцебиття»", who="Подарунок на двох", price=4200, price_label="4 200 грн",
         photo="img/sets/masks-sertsebyttia.webp", kind="Каталог",
         line="Червона й чорна маска в одній коробці — подарунок на двох: партнерові та близькій людині.", link=SITE + "/nabir-masok-dlia-snu-sertsebyttia-chervone-ta-chorne/"),
    dict(id="three", name="Три твіллі на вибір", who="Партнерам", price=4800, price_label="4 800 грн",
         photo="img/sets/three-twilly.webp", kind="Каталог", note="Три стрічки — принти на ваш вибір",
         line="Три твіллі 84 × 5 у святковому пакуванні, які можна зібрати під стиль кожної людини.", link=SITE + "/nabir-3-shovkovykh-tvilli/"),
    dict(id="first-day", name="«Перший день»", who="Новим співробітникам", photo="img/scrunchie-pole.webp", card="Ласкаво просимо в команду. Раді, що ви з нами.", sign="— ваша команда",
         price=700, price_label="700 грн", kind="Під запит", tex="litnie-pole",
         comp="Резинка в коробочці + листівка", line="Шовкова резинка у фірмовій коробочці й листівка «Ласкаво просимо в команду». Маленький жест, з якого новенька людина стає своєю."),
    dict(id="ritual", name="«Ранковий ритуал»", who="Wellbeing для команди", confirm="колір", photos=["img/sets/turban-bilyi.webp", "img/sets/obruch.webp"],
         price=4200, price_label="4 200 грн", kind="Під запит", comp="Тюрбан для волосся 3 500 + шовковий обруч для вмивання 700",
         line="Дві речі з Obiimy HOME для ранку без поспіху: тюрбан після душу й обруч, щоб вмитися, не мочачи волосся."),
    dict(id="head", name="«Керівнику»", who="Топменеджменту й VIP-клієнтам", items=["h88", "tw"], price=6000, price_label="6 000 грн", kind="Під запит", tex="kolo-sontsia",
         comp="Шаль 88 × 88 + твіллі 84 × 5 в одному принті", line="Найбільша хустка Obiimy й найтонша стрічка поруч. Наприклад, у принті «Коло сонця» з колекції «Співоча душа»."),
    dict(id="sleep", name="«Шовковий сон»", confirm="колір, принт", who="Керівникам і VIP-партнерам", photos=["img/sets/pillow-khmara.webp", "img/mask-vpevnenist.webp"],
         price=6900, price_label="6 900 грн", kind="Під запит", comp="Шовкова наволочка 50 × 70 4 200 + маска для сну 2 700",
         line="Наволочка й маска з натурального шовку — подарунок, яким користуються щоночі й щоранку згадують, від кого він."),
    dict(id="cert", name="Подарунковий сертифікат", who="Коли обрати має сама людина", price=1000, price_label="1 000 – 4 000 грн",
         prices="1 000 · 1 500 · 2 000 · 2 500 · 4 000 грн · діє 3 місяці", photo="img/sets/cert-2000.webp", kind="Каталог",
         line="Електронний або фізичний сертифікат на будь-який товар Obiimy.", link="b2b-certificates"),
]

POS = {1: [(50, 44, 58, -3)], 2: [(35, 42, 46, -7), (66, 50, 46, 6)], 3: [(28, 40, 40, -9), (70, 38, 40, 7), (50, 58, 40, -2)]}

SHAPE = {"scr": "ring", "tw": "strip", "h44": "sq s44", "h65": "sq", "d65": "sq", "h88": "sq big", "mask": "mask"}
SILK_CSS = """
  .sk { position: absolute; display: block; background-size: cover; background-position: center; }
  .sk::after { content: ""; position: absolute; inset: 0; background: linear-gradient(115deg, rgba(255,255,255,.32), rgba(255,255,255,0) 38%, rgba(0,0,0,.2)); mix-blend-mode: soft-light; pointer-events: none; border-radius: inherit; }
  .sk.sq { width: var(--sq, 84px); aspect-ratio: 1; border-radius: 2px; box-shadow: 0 1px 0 rgba(255,255,255,.3) inset; }
  .sk.sq.s44 { --sq: 66px; } .sk.sq.big { --sq: 104px; }
  .sk.strip { width: var(--stw, 118px); height: calc(var(--stw, 118px) * .12); background-size: auto 100%; background-repeat: repeat-x; border-radius: 2px; }
  .sk.strip::before { content: ""; position: absolute; inset: 0; background: inherit; transform: rotate(36deg); border-radius: 2px; }
  .sk.ring { width: var(--rg, 50px); aspect-ratio: 1; border-radius: 50%;
    -webkit-mask: radial-gradient(circle, transparent 30%, #000 31%, #000 68%, transparent 70%), repeating-conic-gradient(#000 0 7deg, rgba(0,0,0,.72) 7deg 14deg); -webkit-mask-composite: source-in;
    mask: radial-gradient(circle, transparent 30%, #000 31%, #000 68%, transparent 70%) intersect, repeating-conic-gradient(#000 0 7deg, rgba(0,0,0,.72) 7deg 14deg); }
  .sk.mask { width: var(--mk, 84px); aspect-ratio: 2.3 / 1; border-radius: 50% 50% 46% 46% / 58% 58% 42% 42%; -webkit-mask: radial-gradient(38% 46% at 50% 112%, transparent 98%, #000 100%); mask: radial-gradient(38% 46% at 50% 112%, transparent 98%, #000 100%); }
  .sk.bm { width: var(--bw, 26px); height: calc(var(--bw, 26px) * 3.8); background-size: 300% auto; clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 90%, 0 100%); }
  .sk.note { width: var(--nt, 120px); padding: 10px 12px; background: #F6F1E7; color: #231E2A; font-family: var(--display, Georgia), serif; font-style: italic; font-size: .78rem; line-height: 1.25; border-radius: 2px; }
  .sk.note small { display: block; margin-top: 6px; font-family: var(--body, Arial), sans-serif; font-style: normal; font-size: .56rem; letter-spacing: .12em; text-transform: uppercase; color: #6B6477; }
"""
MBOX_CSS = """
  .mbox { position: absolute; inset: 0; perspective: 900px; perspective-origin: 50% 20%; }
  .mbox .b3 { position: absolute; left: 50%; top: 64%; --W: 184px; --D: 122px; --H: 46px; width: var(--W); height: var(--H); margin: calc(var(--H) / -2) 0 0 calc(var(--W) / -2); transform-style: preserve-3d; transform: rotateX(-38deg) rotateY(-24deg) scale3d(.78, .78, .78); }
  .mbox .fc { position: absolute; left: 50%; top: 50%; }
  .mbox .fr, .mbox .bk { width: var(--W); height: var(--H); margin: calc(var(--H) / -2) 0 0 calc(var(--W) / -2); }
  .mbox .lf, .mbox .rt { width: var(--D); height: var(--H); margin: calc(var(--H) / -2) 0 0 calc(var(--D) / -2); }
  .mbox .bt, .mbox .ts { width: var(--W); height: var(--D); margin: calc(var(--D) / -2) 0 0 calc(var(--W) / -2); }
  .mbox .fr { transform: translateZ(calc(var(--D) / 2)); background: linear-gradient(180deg, #F2B705, #D99E00); }
  .mbox .bk { transform: rotateY(180deg) translateZ(calc(var(--D) / 2)); background: #C99400; }
  .mbox .lf { transform: rotateY(-90deg) translateZ(calc(var(--W) / 2)); background: #CF9700; }
  .mbox .rt { transform: rotateY(90deg) translateZ(calc(var(--W) / 2)); background: linear-gradient(180deg, #F7C21A, #DDA200); }
  .mbox .bt { transform: rotateX(-90deg) translateZ(calc(var(--H) / 2)); background: #8C6400; }
  .mbox .ts { transform: translateY(calc(var(--H) / -2 + 14px)) rotateX(90deg); background: linear-gradient(135deg, #D8C4EA, #BFA6D6 60%, #E4D6F0); }
  .mbox .lid { position: absolute; left: 50%; top: 50%; transform-style: preserve-3d; transform: translateY(calc(var(--H) / -2 - 1px)) translateZ(calc(var(--D) / -2 - 2px)) rotateX(100deg); }
  .mbox .lid i { position: absolute; width: calc(var(--W) + 4px); height: calc(var(--D) + 4px); left: calc((var(--W) + 4px) / -2); top: calc((var(--D) + 4px) / -2); transform: translateZ(calc(var(--D) / 2 + 2px)) rotateX(90deg); background: linear-gradient(160deg, #FFD23A, #F2B705 55%, #E3A800); }
  .mbox .lay { position: absolute; left: 50%; top: 50%; transform-style: preserve-3d; transform: translateY(calc(var(--H) / -2 + 12px)) rotateX(90deg); }
  .mbox .lay .sk { transform: translate(-50%, -50%) translate(var(--x, 0px), var(--y, 0px)) rotate(var(--r, 0deg)); box-shadow: 0 6px 10px rgba(60,30,80,.25); }
  .mbox .stand { position: absolute; left: 50%; top: 50%; transform: translate3d(calc(var(--x, 0px) - 50%), calc(var(--H) / -2 - 44px), calc(var(--D) / -2 + 24px)) rotateX(-8deg) rotateZ(var(--r, 0deg)); }
"""
LAY = {1: [(-6, 4, -4)], 2: [(-36, -4, -8), (46, 12, 10)], 3: [(-48, -6, -6), (40, -18, 12), (36, 28, -4)]}
POS_T = {1: [(50, 44, 0)], 2: [(38, 42, -8), (66, 50, 6)], 3: [(28, 44, -8), (66, 36, 5), (58, 64, -3)]}

def silk(kind, tex):
    return f'<span class="sk {SHAPE[kind]}" style="background-image:url(tex/{tex}{"-strip" if kind == "tw" else ""}.jpg)"></span>'

def setviz(s, sizes="(max-width: 640px) 100vw, 33vw"):
    card = s.get("card")
    if s.get("photos"):
        a, b = s["photos"]
        return f'<figure class="setviz dip" aria-label="{s["name"]}"><span class="d1">{img(a, "", sizes="(max-width: 640px) 50vw, 17vw")}</span><span class="d2">{img(b, "", sizes="(max-width: 640px) 50vw, 17vw")}</span></figure>'
    if s.get("photo"):
        fit = ' style="object-fit:contain;padding:8%"' if s.get("photo_fit") == "contain" else ""
        inner = f'<span class="ph">{img(s["photo"], s["name"], sizes=sizes).replace("<img ", "<img" + fit + " ", 1)}</span>'
        if card:
            inner += f'<span class="cardlet">{card}<small>{s.get("sign", "— від вашої компанії")}</small></span>'
        return f'<figure class="setviz" aria-label="{s["name"]}">{inner}</figure>'
    t = s.get("tex", "tysha-sertsia"); items = s["items"]
    lay = "".join(f'<span style="--x:{x}px;--y:{y}px;--r:{r}deg;display:contents">{silk(k, t).replace(chr(34) + " style=" + chr(34), chr(34) + " style=" + chr(34) + f"--x:{x}px;--y:{y}px;--r:{r}deg;", 1)}</span>' for k, (x, y, r) in zip(items, LAY[len(items)]))
    note = f'<span class="stand" style="--x:40px;--r:4deg"><span class="sk note" style="--nt:96px;position:relative;font-size:.66rem;padding:7px 9px">{card}<small>{s.get("sign", "— від вашої компанії")}</small></span></span>' if card else ""
    box = f'<span class="mbox"><span class="b3"><i class="fc bt"></i><i class="fc bk"></i><i class="fc lf"></i><i class="fc rt"></i><i class="fc ts"></i><span class="lay">{lay}</span>{note}<i class="fc fr"></i><span class="lid"><i></i></span></span></span>'
    return f'<figure class="setviz" aria-label="{s["name"]}">{box}<span class="ex">Принт — приклад</span></figure>'

SET_CSS = "\n<style>" + SILK_CSS + MBOX_CSS + """
  .setviz { position: relative; margin: 0; aspect-ratio: 4 / 3; overflow: hidden; border-radius: var(--radius); background: radial-gradient(90% 80% at 50% 30%, var(--card), var(--bg2)); }
  .setviz .box { position: absolute; left: 12%; right: 12%; bottom: -10%; height: 30%; background: linear-gradient(180deg, #F7C928, #EDB400); border-radius: 4px; box-shadow: 0 -10px 30px -12px rgba(60,40,0,.35), inset 0 10px 14px rgba(120,80,0,.18); display: grid; place-items: center; }
  .setviz .box img { height: 16px; width: auto; opacity: .85; margin-top: 18%; }
  .setviz.dip { display: grid; grid-template-columns: 1fr 1fr; gap: 0; padding: 4% 6%; background: #fff; }
  .setviz.dip span.d1, .setviz.dip span.d2 { display: block; overflow: hidden; }
  .setviz.dip img { width: 100%; height: 100%; object-fit: contain; mix-blend-mode: multiply; }
  .setviz.dip .plus { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 32px; height: 32px; border-radius: 50%; background: var(--gold); color: #17151A; display: grid; place-items: center; font-weight: 600; }
  .set .acts { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: 8px; flex-wrap: wrap; }
  .set .acts .pick { margin-top: 0; }
  .set .more { font-size: .84rem; font-weight: 500; padding: 12px 0; }
  .setviz .ph img { object-fit: cover; }
  .setviz .tv { position: absolute; transform: translate(-50%, -50%) rotate(var(--r, 0deg)); background-size: cover; background-position: center; box-shadow: 0 18px 30px -16px rgba(0,0,0,.5); }
  .setviz .tv.sq { width: 40%; aspect-ratio: 1; border-radius: 2px; }
  .setviz .tv.sq.big { width: 50%; }
  .setviz .tv.strip { width: 62%; height: 9%; background-size: auto 100%; background-repeat: repeat-x; border-radius: 2px; }
  .setviz .tv.ring { width: 26%; aspect-ratio: 1; border-radius: 50%; -webkit-mask-image: radial-gradient(circle, transparent 33%, #000 34%, #000 69%, transparent 70%); mask-image: radial-gradient(circle, transparent 33%, #000 34%, #000 69%, transparent 70%); box-shadow: none; filter: drop-shadow(0 10px 12px rgba(0,0,0,.35)); }
  .setviz .tv.mask { width: 34%; aspect-ratio: 2.1 / 1; border-radius: 48% 48% 44% 44% / 60% 60% 40% 40%; }
  .setviz .ex { position: absolute; left: 10px; top: 10px; font-size: .66rem; letter-spacing: .12em; text-transform: uppercase; color: var(--ink3); background: color-mix(in srgb, var(--card) 80%, transparent); padding: 3px 8px; border-radius: 999px; }
  .setviz .it { position: absolute; aspect-ratio: 1; background: #fff; border-radius: 6px; box-shadow: 0 18px 30px -16px rgba(0,0,0,.45); overflow: hidden; }
  .setviz .it img { width: 100%; height: 100%; object-fit: contain; padding: 6%; }
  .setviz .ph { position: absolute; inset: 0; overflow: hidden; background: #fff; }
  .setviz .ph img { width: 100%; height: 100%; object-fit: cover; }
  .setviz .cardlet { position: absolute; right: 8%; top: 12%; width: 38%; background: #F6F1E7; color: #231E2A; font-family: var(--display); font-style: italic; font-size: .82rem; line-height: 1.25; padding: 10px 12px; border-radius: 2px; transform: rotate(5deg); box-shadow: 0 14px 24px -14px rgba(0,0,0,.45); display: grid; gap: 6px; }
  .setviz .cardlet small { font-family: var(--body); font-style: normal; font-size: .62rem; letter-spacing: .12em; text-transform: uppercase; color: #6B6477; }
  .sets { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }
  .set { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; display: grid; grid-template-rows: auto 1fr; }
  .set[hidden] { display: none !important; }
  .set .in { padding: 18px 20px 20px; display: grid; gap: 8px; align-content: start; }
  .set .who { font-size: .76rem; letter-spacing: .16em; text-transform: uppercase; color: var(--ink3); font-weight: 600; }
  .set h3 { font-size: 1.35rem; }
  .set .comp { font-size: .88rem; color: var(--ink2); }
  .set .line { font-size: .92rem; color: var(--ink2); }
  .set .foot { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: 6px; padding-top: 12px; border-top: 1px solid var(--line); }
  .set .foot b { font-family: var(--display); font-weight: 400; font-size: 1.3rem; }
  .set .tag { font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; padding: 3px 8px; border-radius: 999px; border: 1px solid var(--line); color: var(--ink2); }
  .set .tag.cat { border-color: #8A6500; color: #7A5900; }
  .dark .set .tag.cat { border-color: var(--gold); color: var(--gold); }
  .set .pick { margin-top: 8px; }
  .set .pick[aria-pressed="true"] { background: var(--ink); color: var(--bg); border-color: var(--ink); }
  .set .pack { font-size: .8rem; color: var(--ink3); }
  .cart { display: grid; gap: 8px; margin-top: 18px; }
  .cart .row { display: grid; grid-template-columns: 1fr 86px 44px; gap: 8px; align-items: center; font-size: .92rem; border-bottom: 1px solid var(--line); padding-bottom: 8px; }
  .cart .row input { min-height: 44px; padding: 8px 10px; }
  .cart .row button { all: unset; cursor: pointer; text-align: center; min-height: 44px; color: var(--ink2); }
  .cart .tot { font-family: var(--display); font-size: 1.5rem; }
  .cart .empty { color: var(--ink2); font-size: .92rem; }
  .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 22px; }
  .chips button { all: unset; cursor: pointer; font-size: .86rem; padding: 12px 16px; border: 1px solid var(--line); border-radius: 999px; color: var(--ink2); }
  .chips button[aria-pressed="true"] { border-color: var(--ink); color: var(--ink); background: color-mix(in srgb, var(--ink) 6%, transparent); }
  .chips button:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }
  @media (max-width: 960px) { .sets { grid-template-columns: 1fr 1fr; } }
  @media (max-width: 640px) { .sets { grid-template-columns: 1fr; } }
</style>"""

# ---------------------------------------------------------------- A. catalogue of sets (Maison)
def sets_catalogue():
    cards = []
    for s in SETS:
        comp = s.get("comp", "")
        extra = "".join(f'<p class="comp">{x}</p>' for x in [s.get("prices"), s.get("note")] if x)
        pr = s.get("prints")
        if pr:
            n = pr.count(",") + 1 + pr.count("·") if not pr.startswith("18") else 18
            extra += f'<p class="comp">Принти: {pr}</p>' if n <= 3 else f'<details class="prints"><summary>Принти в каталозі · {n}</summary><p>{pr}</p></details>'
        pack = '' if s["kind"].startswith("Каталог") else '<p class="pack">Комбінація з речей каталогу: ' + s.get("confirm", "принти") + ' й пакування підтвердимо в розрахунку.</p>'
        link = f'<a class="more" href="{s["link"]}">{"Детальніше" if s["link"].startswith("b2b") else "На obiimy.world"} →</a>' if s.get("link") else ""
        cards.append(f'''
      <article class="set" data-price="{s["price"]}" id="set-{s["id"]}">
        {setviz(s)}
        <div class="in"><span class="who">{s["who"]}</span><h3>{s["name"]}</h3>{f'<p class="comp">{comp}</p>' if comp else ""}{extra}<p class="line">{s["line"]}</p>{pack}
          <div class="foot"><b class="num">{s["price_label"]}</b><span class="tag{" cat" if s["kind"].startswith("Каталог") else ""}">{s["kind"]}</span></div>
          <div class="acts"><button class="btn btn-line btn-sm pick" type="button" data-name="{s["name"]}" data-price="{s["price"]}" aria-pressed="false">Додати до запиту</button>{link}</div></div>
      </article>''')
    body = SET_CSS + hero("Корпоративні набори · Новий рік і не тільки", "Набори Obiimy для команди, партнерів і клієнтів",
        "Подарункові набори з каталогу Obiimy у фірмових коробках і кілька комбінацій, які ми зібрали для бізнесу.<span class=\"m-hide\"> Оберіть один або кілька наборів — повернемось із розрахунком на ваш тираж.</span>",
        "Обрати набори", "Зібрати свій у 3D", "b2b-atelier", "Від 700 грн за «Перший день» до 6 900 грн за «Шовковий сон». Ціни — роздрібні з obiimy.world.", "img/sets/tw44-natkhnennia.webp", "Набір твіллі та хустки «Натхнення» у жовтій коробці", "Набір «Натхнення» з каталогу — твіллі й хустка 44 × 44", pos="50% 50%") + facts_html([
        ("8 наборів з каталогу", "Сім сімейств наборів і сертифікати — з цінами obiimy.world"),
        ("4 комбінації", "Для бізнесу з речей каталогу — під запит"),
        ("Десятки принтів", "У кожному сімействі — свій вибір принтів"),
        ("Шоурум у Києві", "Зразки можна подивитися наживо на Сагайдачного, 12"),
    ]) + f'''

  <section class="block" id="sets"><div class="wrap">
    <div class="head"><p class="eyebrow">Набори</p><h2>Оберіть за бюджетом на людину</h2><p class="sub">«Каталог» — набір, який уже є на obiimy.world. «Під запит» — наша комбінація з речей каталогу: склад, принти й ціну на тираж підтвердимо в розрахунку.</p></div>
    <div class="chips" id="chips" role="group" aria-label="Бюджет на людину"><button type="button" data-b="0" aria-pressed="true">Усі</button><button type="button" data-b="1500">до 1 500 грн</button><button type="button" data-b="2500">до 2 500 грн</button><button type="button" data-b="3500">до 3 500 грн</button><button type="button" data-b="5000">до 5 000 грн</button><button type="button" data-b="99999">понад 5 000 грн</button></div>
    <div class="sets" id="setsGrid">{"".join(cards)}</div>
    <p class="note">Не знайшли свій? <a href="b2b-atelier" style="font-weight:600">Зберіть набір у 3D-конструкторі →</a> або <a href="b2b-monoprint" style="font-weight:600">один принт на всю компанію →</a></p>
  </div></section>

  <section class="block alt" id="personal"><div class="wrap grid2">
    <figure>{img("photo/box-gold.jpg", "Набір у фірмовій жовтій коробці", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
    <div><p class="eyebrow">Що в кожному наборі</p><h2 style="margin-top:10px">Коробка, папір, листівка</h2>
      <div class="faq" style="margin-top:22px">
        <details open><summary>Фірмова жовта коробка</summary><p>Кожен набір — у жовтій коробці Obiimy з тонким папером. Її впізнають ще до того, як відкриють.</p></details>
        <details><summary>Листівка від компанії</summary><p>Ваш текст привітання в кожній коробці; підпис від руки — за бажанням.</p></details>
        <details><summary>Один принт чи різні</summary><p>Один принт на всіх читається як подарунок від команди; різні — як особистий кожному. Узгоджуємо в розрахунку.</p></details>
        <details><summary>Доставка</summary><p>В офіс однією посилкою або кожному адресату на відділення Нової пошти.</p></details>
      </div>
    </div>
  </div></section>

  <section class="block" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Питання</p><h2>Що зазвичай питають</h2></div>
    <div class="faq">
      <details><summary>Чим «Каталог» відрізняється від «Під запит»?</summary><p>Набори «Каталог» уже продаються на obiimy.world. «Під запит» — наші комбінації з речей каталогу: наявність принтів і ціну на тираж підтвердимо в розрахунку.</p></details>
      <details><summary>Чи можна змінити склад набору?</summary><p>Так — замінити річ, принт або додати позицію. Найзручніше зібрати свій варіант у <a href="b2b-atelier">3D-конструкторі</a>.</p></details>
      <details><summary>Не знаєте, що обрати кожному?</summary><p><a href="b2b-certificates">Сертифікати</a>: людина обирає сама, ви тримаєте бюджет.</p></details>
      <details><summary>Мінімальний тираж?</summary><p>Фіксованого мінімуму немає — обговорюємо кожен запит окремо.</p></details>
      {DOCS_FAQ}
      {BATCH_FAQ}
    </div>
  </div></section>
  {PROOF}

  <section class="form-block alt" id="request"><div class="wrap">
    <div class="contact"><p class="eyebrow">Ваш запит</p><h2>Набори в запиті</h2><div class="cart" id="cart" aria-live="polite"><p class="empty">Додайте один або кілька наборів кнопкою «Додати до запиту» — наприклад, команді й ключовим людям.</p></div><p class="big"><a href="{PHONE_HREF}">{PHONE}</a></p><p><a href="mailto:{MAIL}">{MAIL}</a></p></div>
    <div>{form_html("f-sets", "Корпоративні набори", BASE_FIELDS + [
        ("deadline", "Коли потрібно", "select:До 10 грудня|До 20 грудня|Після свят|Інша дата", False, {}),
        PAY,
        ("note", "Коментар", "textarea", False, {"ph": "Нагода, принти, текст листівки…"}),
    ], "").replace('<div class="actions">', '<input type="hidden" name="config" data-label="Набори"><div class="actions">', 1)}</div>
  </div></section>
  <script>
  (function () {{
    var chips = document.getElementById('chips'), cards = [].slice.call(document.querySelectorAll('.set'));
    chips.querySelectorAll('button').forEach(function (b) {{ b.addEventListener('click', function () {{
      var v = +b.dataset.b; chips.querySelectorAll('button').forEach(function (x) {{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }});
      cards.forEach(function (c) {{ var p = +c.dataset.price; c.hidden = c.id === 'set-cert' ? false : (v === 0 ? false : (v === 99999 ? p <= 5000 : p > v)); }});
    }}); }});
    var cart = [], box = document.getElementById('cart'), hid = document.querySelector('#f-sets [name="config"]');
    function fmt(n) {{ return String(n).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, '\\u202f') + '\\u00a0грн'; }}
    function draw() {{
      document.querySelectorAll('.set .pick').forEach(function (b) {{ var on = cart.some(function (c) {{ return c.name === b.dataset.name; }}); b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.textContent = on ? 'У запиті ✓' : 'Додати до запиту'; }});
      if (!cart.length) {{ box.innerHTML = '<p class="empty">Додайте один або кілька наборів кнопкою «Додати до запиту» — наприклад, команді й ключовим людям.</p>'; hid.value = ''; return; }}
      box.innerHTML = ''; var tot = 0;
      cart.forEach(function (c, i) {{
        var r = document.createElement('div'); r.className = 'row';
        r.innerHTML = '<span></span><input type="number" min="1" max="5000" inputmode="numeric" aria-label="Кількість"><button type="button" aria-label="Прибрати набір">✕</button>';
        r.firstChild.textContent = c.name + ' · ' + fmt(c.price); var inp = r.querySelector('input'); inp.value = c.q;
        inp.addEventListener('input', function () {{ c.q = Math.max(1, +inp.value || 1); sum(); }});
        r.querySelector('button').addEventListener('click', function () {{ cart.splice(i, 1); draw(); }});
        box.appendChild(r);
      }});
      var t = document.createElement('p'); t.className = 'tot num'; box.appendChild(t); sum();
    }}
    function sum() {{ var tot = 0; cart.forEach(function (c) {{ tot += c.q * c.price; }}); var t = box.querySelector('.tot'); if (t) t.textContent = 'Разом ≈ ' + fmt(tot) + ' за роздрібом';
      hid.value = cart.map(function (c) {{ return c.name + ' × ' + c.q; }}).join('; ') + ' · орієнтир ' + fmt(tot); }}
    document.querySelectorAll('.set .pick').forEach(function (b) {{ b.addEventListener('click', function () {{
      var k = cart.findIndex(function (c) {{ return c.name === b.dataset.name; }});
      if (k >= 0) cart.splice(k, 1); else cart.push({{ name: b.dataset.name, price: +b.dataset.price, q: cart.length ? 5 : 30 }});
      draw();
    }}); }});
  }})();
  </script>'''
    return dict(slug="b2b-sets", skin="maison", title="Корпоративні подарункові набори — Obiimy",
        desc="Подарункові набори Obiimy для компаній: твіллі й резинка, маска й резинка, твіллі й хустка, сертифікати та комбінації з Obiimy HOME. Від 700 грн, листівка від компанії.",
        og="photo/box-dots.jpg", nav=[("Набори", "sets"), ("Що всередині", "personal"), ("Питання", "faq"), ("Контакт", "request")],
        cta="Запит", sticky="Корпоративні набори · від 700 грн", body=body)


# ---------------------------------------------------------------- B. one print for the whole company (Journal)
def _states():
    src = (ROOT / "build.py").read_text(); ns = {}
    exec(src[src.index("STATES = ["):src.index("GARDEN = ")], {}, ns)
    return ns["STATES"]

def monoprint():
    st = _states()
    tiers = [
        ("team", "Уся команда", "Твіллі 84 × 5", 1600, 30, "tw"),
        ("key", "Ключові люди", "Хустка 65 × 65", 3200, 10, "k65"),
        ("lead", "Керівники й партнери", "Шаль 88 × 88", 4400, 3, "k88"),
        ("new", "Нові співробітники", "Резинка у коробочці", 700, 10, "scr"),
    ]
    sw = "".join(f'<button type="button" data-i="{i}" aria-label="Принт «{s["name"]}»" aria-pressed="{"true" if i == 2 else "false"}"><img src="tex/{s["id"]}-160.webp" alt="" width="80" height="80" loading="lazy"></button>' for i, s in enumerate(st))
    tier_html = "".join(f'''
      <div class="tier" data-k="{k}" data-p="{p}" data-fmt="{fmt}">
        <div class="viz v-{fmt}"><span class="tex"></span></div>
        <div class="in"><p class="who">{who}</p><h3>{name}</h3><p class="catline"></p>
          <div class="row"><label>Кількість<input type="number" min="0" max="5000" value="{q}" inputmode="numeric" aria-label="{who}: кількість"></label><b class="num sum"></b></div></div>
      </div>''' for k, who, name, p, q, fmt in tiers)
    css = """
<style>
  .mp-swatches { display: grid; grid-template-columns: repeat(9, minmax(0, 1fr)); gap: 10px; max-width: 760px; }
  .mp-swatches button { all: unset; cursor: pointer; aspect-ratio: 1; border-radius: 50%; overflow: hidden; border: 2px solid transparent; box-shadow: 0 0 0 1px var(--line); }
  .mp-swatches button img { width: 100%; height: 100%; object-fit: cover; transform: scale(1.3); }
  .mp-swatches button[aria-pressed="true"] { border-color: var(--ink); }
  .mp-swatches button:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }
  .mp-name { margin-top: 16px; font-family: var(--display); font-size: 1.6rem; }
  .mp-line { color: var(--ink2); max-width: 44em; margin-top: 4px; }
  .tiers { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; margin-top: 30px; }
  .tier { background: var(--card); border: 1px solid var(--line); display: grid; grid-template-rows: auto 1fr; }
  .tier .viz { position: relative; aspect-ratio: 1; background: var(--bg2); display: grid; place-items: center; overflow: hidden; }
  .tier .tex { display: block; background-size: cover; background-position: center; box-shadow: 0 20px 30px -18px rgba(0,0,0,.45); transition: background-image .3s ease; }
  .v-k65 .tex { width: 64%; aspect-ratio: 1; transform: rotate(-6deg); }
  .v-k88 .tex { width: 78%; aspect-ratio: 1; transform: rotate(4deg); }
  .v-tw .tex { width: 90%; height: 13%; transform: rotate(-24deg); border-radius: 2px; background-size: auto 100%; background-repeat: repeat-x; }
  .v-scr .tex { width: 52%; aspect-ratio: 1; border-radius: 50%; -webkit-mask-image: radial-gradient(circle, transparent 34%, #000 35%, #000 69%, transparent 70%); mask-image: radial-gradient(circle, transparent 34%, #000 35%, #000 69%, transparent 70%); }
  .tier .in { padding: 16px 18px 18px; display: grid; gap: 6px; align-content: start; }
  .tier .who { font-size: .76rem; letter-spacing: .16em; text-transform: uppercase; color: var(--ink3); font-weight: 600; }
  .tier h3 { font-size: 1.25rem; }
  .tier .catline { font-size: .82rem; color: var(--ink2); }
  .tier.req .catline { color: #7A5900; }
  .tier .row { display: flex; align-items: end; justify-content: space-between; gap: 10px; border-top: 1px solid var(--line); padding-top: 12px; margin-top: 4px; }
  .tier label { display: grid; gap: 4px; font-size: .78rem; color: var(--ink2); }
  .tier input { font: inherit; width: 96px; min-height: 44px; padding: 8px 10px; border: 1px solid var(--line); background: var(--bg); color: var(--ink); }
  .tier .sum { font-family: var(--display); font-weight: 400; font-size: 1.15rem; }
  .mp-total { margin-top: 26px; display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px 22px; border-top: 1px solid var(--ink); padding-top: 18px; }
  .mp-total b { font-family: var(--display); font-weight: 400; font-size: 2.2rem; }
  .mp-total span { color: var(--ink2); font-size: .9rem; }
  @media (max-width: 960px) { .tiers { grid-template-columns: 1fr 1fr; } .mp-swatches { grid-template-columns: repeat(5, minmax(0, 1fr)); } }
  @media (max-width: 640px) { .tier .viz { aspect-ratio: 4 / 3; } }
</style>"""
    hero_fig = f'<figure class="mphero" style="margin:0;position:relative;aspect-ratio:4/5;overflow:hidden;border-radius:var(--radius)">{img("photo/paris-green.jpg", "Шовкова хустка на жакеті", sizes="(max-width: 960px) 100vw, 50vw", lazy=False, eager_priority=True)}<div class="tag">Один принт на всіх читається як подарунок від команди</div></figure>'
    body = css + hero("Монопринт · корпоративні подарунки", "Один принт — уся компанія",
        "Один принт — у чотирьох форматах: твіллі для команди, хустка для ключових людей, шаль для керівників, резинка для новеньких.<span class=\"m-hide\"> Разом це виглядає як колекція вашої компанії, а не як набір випадкових подарунків.</span>",
        "Обрати принт", "Готові набори", "b2b-sets", "Роздрібні ціни — від 700 до 4 800 грн за річ.", "photo/paris-green.jpg", "", "", pos="50% 14%", figure=hero_fig, cta1_href="#print") + facts_html([
        ("9 принтів", "Авторські картини на шовку"),
        ("4 рівні", "Команда, ключові люди, керівники, нові співробітники"),
        ("Одна історія", "Той самий принт у різних форматах і на різних людях"),
        ("3 формати в кожному", "Твіллі, резинка й двостороння хустка 65 × 65 є в каталозі для всіх 9 принтів"),
    ]) + f'''

  <section class="block" id="print"><div class="wrap">
    <div class="head"><p class="eyebrow">Крок 1 · Принт</p><h2>Оберіть принт компанії</h2><p class="sub">Принт одразу з’явиться на всіх рівнях нижче. «Каталог» — формат уже є на obiimy.world; «під запит» — наявність і терміни підтвердимо в розрахунку.</p></div>
    <div class="mp-swatches" id="mpSw" role="group" aria-label="Принти">{sw}</div>
    <p class="mp-name" id="mpName"></p><p class="mp-line" id="mpLine"></p>
  </div></section>

  <section class="block alt" id="tiers"><div class="wrap">
    <div class="head"><p class="eyebrow">Крок 2 · Рівні</p><h2>Хто що отримує</h2><p class="sub">Змініть кількість — сума рахується за роздрібними цінами. Поставте 0, якщо рівень не потрібен. Умови для тиражу надішлемо в розрахунку.</p></div>
    <div class="tiers" id="tiersGrid">{tier_html}</div>
    <div class="mp-total"><b class="num" id="mpTotal"></b><span id="mpPeople"></span><a class="btn btn-gold" href="#request" id="mpSend">Надіслати розрахунок</a></div>
  </div></section>

  <section class="block" id="why"><div class="wrap grid2">
    <div><p class="eyebrow">Чому один принт</p><h2 style="margin-top:10px">Колекція вашої компанії</h2>
      <div class="faq" style="margin-top:22px">
        <details open><summary>Видно, що це від команди</summary><p>Коли в офісі, на конференції чи на фото один принт — подарунок читається як спільний, а не випадковий.</p></details>
        <details><summary>Різні формати — різні люди</summary><p>Твіллі носять на сумці чи у волоссі, хустку — на шиї, шаль — на плечах. Один принт працює на кожного.</p></details>
        <details><summary>Історія принту</summary><p>Кожен принт — авторська картина. У листівці можна розповісти, чому обрали саме його.</p></details>
      </div>
    </div>
    <figure>{img("photo/paris-belt.jpg", "Твіллі як пояс на тренчі", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
  </div></section>

  <section class="block alt" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Питання</p><h2>Що зазвичай питають</h2></div>
    <div class="faq">
      <details><summary>Чи є кожен принт у кожному форматі?</summary><p>Твіллі 84 × 5 і резинка є в каталозі в усіх дев’яти принтах, двостороння хустка 65 × 65 — теж. Шаль 88 × 88 у каталозі — «Коло сонця» й «Між нами»; для інших принтів шаль — під запит: наявність і терміни підтвердимо в розрахунку.</p></details>
      <details><summary>Чи можна два принти — наприклад, для різних команд?</summary><p>Так, напишіть у коментарі — підберемо пару принтів, які поєднуються.</p></details>
      {DOCS_FAQ}
      {BATCH_FAQ}
    </div>
  </div></section>
  {PROOF}

  <section class="form-block" id="request"><div class="wrap">
    {contact("Надіслати розрахунок", "Розрахунок із калькулятора вже в запиті — повернемось із наявністю принту та цінами на тираж.")}
    <div>{form_html("f-mono", "Монопринт для компанії", BASE_FIELDS + [
        ("deadline", "Коли потрібно", "select:До 10 грудня|До 20 грудня|Після свят|Інша дата", False, {}),
        PAY,
        ("note", "Коментар", "textarea", False, {"ph": "Нагода, текст листівки, побажання…"}),
    ], "").replace('<div class="actions">', '<input type="hidden" name="config" data-label="Розрахунок"><div class="actions">', 1)}</div>
  </div></section>
  <script>
  (function () {{
    var ST = {json.dumps([dict(id=s["id"], name=s["name"], line=s["line"], size=s["size"]) for s in st], ensure_ascii=False)}, cur = 2;
    // obiimy.world, 28.09.2026: twilly, scrunchie and 2-sided 65 exist for all nine prints
    var ONE65 = {{ 'tysha-sertsia': 1, 'prystrast': 1 }}, SHAWL = {{ 'kolo-sontsia': 1, 'mizh-namy': 1 }};
    function spec(s, f) {{
      if (f === 'k65') return ONE65[s.id] ? {{ n: 'Хустка 65 × 65', p: 3200, c: 1 }} : {{ n: 'Двостороння хустка 65 × 65', p: 4800, c: 1 }};
      if (f === 'k88') return {{ n: 'Шаль 88 × 88', p: 4400, c: !!SHAWL[s.id] }};
      return {{ c: 1 }};
    }}
    function gifts(n) {{ var d = n % 10, h = n % 100; return n + ' ' + (d === 1 && h !== 11 ? 'подарунок' : (d >= 2 && d <= 4 && (h < 12 || h > 14) ? 'подарунки' : 'подарунків')); }}
    function fmt(n) {{ return String(n).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, '\\u202f') + '\\u00a0грн'; }}
    var tiers = [].slice.call(document.querySelectorAll('.tier'));
    function render() {{
      var s = ST[cur], total = 0, people = 0, lines = [];
      document.getElementById('mpName').textContent = '«' + s.name + '»'; document.getElementById('mpLine').textContent = s.line;
      document.querySelectorAll('#mpSw button').forEach(function (b, i) {{ b.setAttribute('aria-pressed', i === cur ? 'true' : 'false'); }});
      tiers.forEach(function (t) {{
        var f = t.dataset.fmt, sp = spec(s, f), p = sp.p || +t.dataset.p, q = Math.max(0, Math.min(5000, +t.querySelector('input').value || 0));
        if (sp.n) t.querySelector('h3').textContent = sp.n;
        t.querySelector('.tex').style.backgroundImage = 'url(tex/' + s.id + (f === 'tw' ? '-strip' : '') + '.jpg)';
        t.querySelector('.catline').textContent = (sp.c ? 'Каталог · ' : 'Під запит · ') + fmt(p) + ' за річ';
        t.classList.toggle('req', !sp.c);
        t.querySelector('.sum').textContent = fmt(p * q); total += p * q; people += q;
        if (q) lines.push(q + ' × ' + t.querySelector('h3').textContent + ' (' + t.querySelector('.who').textContent.toLowerCase() + (sp.c ? '' : ', під запит') + ')');
      }});
      document.getElementById('mpTotal').textContent = fmt(total);
      document.getElementById('mpPeople').textContent = gifts(people) + ' · за роздрібними цінами — це верхня межа';
      var h = document.querySelector('#f-mono [name="config"]'); if (h) h.value = 'Принт «' + s.name + '»: ' + lines.join('; ') + '. Орієнтир: ' + fmt(total) + '.';
    }}
    document.querySelectorAll('#mpSw button').forEach(function (b) {{ b.addEventListener('click', function () {{ cur = +b.dataset.i; render(); }}); }});
    tiers.forEach(function (t) {{ t.querySelector('input').addEventListener('input', render); }});
    render();
  }})();
  </script>'''
    return dict(slug="b2b-monoprint", skin="journal", title="Один принт на всю компанію — корпоративні подарунки Obiimy",
        desc="Один принт Obiimy для всієї компанії: твіллі команді, хустка ключовим людям, шаль керівникам, резинка новеньким. Калькулятор за роздрібними цінами.",
        og="photo/paris-green.jpg", nav=[("Принт", "print"), ("Рівні", "tiers"), ("Чому один принт", "why"), ("Питання", "faq"), ("Контакт", "request")],
        cta="Запит", sticky="Один принт — уся компанія", body=body)


# ---------------------------------------------------------------- C. unboxing (dark art template)
def unboxing():
    tpl = (ROOT / "b2b-unboxing.html").read_text().replace("/*SILK*/", SILK_CSS)
    form = form_html("f-unbox", "Набір зі сторінки «Розпакування»", BASE_FIELDS + [
        ("set", "Набір", "select:Твіллі й резинка — 2 200 грн|Маска й резинка — 3 100 грн|Твіллі й хустка 44 × 44 — 3 200 грн|«Співоча душа»: маска, закладка й резинка — 3 600 грн|Інший набір з каталогу", False, {"full": True}),
        ("qty", "Кількість наборів", "number", False, {"ph": "наприклад, 30"}),
        ("deadline", "Коли потрібно", "select:До 10 грудня|До 20 грудня|Після свят|Інша дата", False, {}),
        PAY,
        ("note", "Коментар", "textarea", False, {"ph": "Нагода, принти, текст листівки…"}),
    ], "")
    return typo(tpl.replace("<!--FORM-->", form))


if __name__ == "__main__":
    b2b.build_all([sets_catalogue, monoprint])
    h = unboxing(); (OUT / "b2b-unboxing.html").write_text(h); print("b2b-unboxing", len(h) // 1024, "KB")
