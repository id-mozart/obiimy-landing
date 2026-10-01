#!/usr/bin/env python3
"""B2B pages about gifts inside a company (HR, office managers): four entries to one offer.
  b2b-team        the path of a person in the company + a yearly plan
  b2b-team-quiz   the first screen is the tool: a pick in a few questions
  b2b-team-card   the gift with the words from the company
  b2b-team-plans  three example programmes for a year, price per person
Prices are retail prices from obiimy.world (review/SITE-FACTS.md). Nothing here promises a discount, a deadline or a minimum order:
whatever the brand has not confirmed is answered with «у розрахунку». «Who it suits», greeting texts and programmes are our examples."""
import importlib.util, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("b2b", ROOT / "build-b2b.py")
b2b = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(b2b)
img, typo, hero, form_html, price = b2b.img, b2b.typo, b2b.hero, b2b.form_html, b2b.price
PHONE, PHONE_HREF, MAIL, TG, SHOWROOM = b2b.PHONE, b2b.PHONE_HREF, b2b.MAIL, b2b.TG, b2b.SHOWROOM
BAR = "Для бізнесу · подарунки співробітникам<span class=\"m-hide\"> · добірка й розрахунок у відповідь на запит</span>"
SAMPLE = 'Хочете спершу побачити шовк? Твіллі — від 1 600 грн за роздрібною ціною: <a href="https://obiimy.world/khustka-tvilli-shovkova-zolote-svitlo-84x5/">замовити зразок →</a>'

def J(v): return json.dumps(v, ensure_ascii=False)

def opt(c, selected=False):
    """Short option label for a select: certificates already carry the price; «усім» marks neutral things."""
    lab = SHORT_N[c["k"]] if c["k"].startswith("cert") else f'{SHORT_N.get(c["k"], c["n"])} · {price(c["p"])}'
    return f'<option value="{c["k"]}"{" selected" if selected else ""}>{lab}{" · усім" if c["neutral"] else ""}</option>'

def bind(html):
    """Short prepositions and conjunctions stick to the next word (text nodes only)."""
    parts = re.split(r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>|<textarea[\s\S]*?</textarea>|<[^>]+>)', html)
    rx = re.compile(r"(?<![\w’'])(у|в|з|і|й|а|о|на|до|за|та|не|чи|із|зі|від|для|що|як|це|по|під|про|або|але|ми|ви)\s+(?=\S|$)", re.I)
    for i in range(0, len(parts), 2):
        parts[i] = rx.sub(lambda m: m.group(1) + " ", parts[i])
    return "".join(parts)

# ─────────────────────────────────────────────────────────────── catalogue (retail prices, obiimy.world)
# neutral: suits anyone in a mixed team; aud / occ: our recommendation, not a fact from the site
CATALOG = [
    dict(k="scr", n="Шовкова резинка", p=700, ph="img/scrunchie-pole.webp", neutral=False, aud=["team", "new"], occ=["bday", "holiday", "first"], why="Невелика шовкова річ."),
    dict(k="book", n="Закладка для книги", p=800, ph="img/sets/bookmark-melodiia.webp", neutral=True, aud=["team", "new", "remote"], occ=["first", "bday", "holiday", "thanks"], why="Нейтральна річ, доречна для кожного в команді."),
    dict(k="cert1", n="Сертифікат на 1 000 грн", p=1000, ph="img/sets/cert-2000.webp", neutral=True, aud=["team", "remote", "new"], occ=["bday", "holiday"], why="Людина обирає сама. Буває електронний і друкований."),
    dict(k="cert15", n="Сертифікат на 1 500 грн", p=1500, ph="img/sets/cert-2000.webp", neutral=True, aud=["team", "remote"], occ=["bday", "holiday"], why="Людина обирає сама. Буває електронний і друкований."),
    dict(k="tw", n="Твіллі 84 × 5", p=1600, ph="img/twilly-zolote.webp", neutral=False, aud=["team", "new", "key"], occ=["bday", "first", "thanks", "holiday"], why="Вузька шовкова стрічка: на шию, сумку чи зап’ястя."),
    dict(k="scrset", n="Набір із трьох резинок", p=1800, ph="img/sets/scr3.webp", neutral=False, aud=["team", "new"], occ=["first", "holiday"], why="Готовий набір у коробці."),
    dict(k="cert2", n="Сертифікат на 2 000 грн", p=2000, ph="img/sets/cert-2000.webp", neutral=True, aud=["team", "remote", "key"], occ=["bday", "years", "thanks"], why="Коли не знаєте смаків: людина обирає сама протягом трьох місяців."),
    dict(k="cert25", n="Сертифікат на 2 500 грн", p=2500, ph="img/sets/cert-2000.webp", neutral=True, aud=["team", "remote", "key"], occ=["bday", "years", "thanks"], why="Людина обирає сама протягом трьох місяців."),
    dict(k="twscr", n="Набір: твіллі та резинка", p=2200, ph="img/sets/twscr-makiv.webp", neutral=False, aud=["team", "new", "key"], occ=["bday", "holiday", "thanks"], why="Дві речі в одному принті у святковій коробці."),
    dict(k="h44", n="Хустка 44 × 44, двосторонній друк", p=2400, ph="img/pidnesennia.webp", neutral=False, aud=["key", "team"], occ=["years", "thanks", "bday"], why="Маленька хустка на шию."),
    dict(k="mask", n="Маска для сну", p=2700, ph="img/mask-svoboda.webp", neutral=True, aud=["team", "key", "remote"], occ=["thanks", "holiday", "bday", "years"], why="Подарунок про відпочинок. Підходить усім."),
    dict(k="maskscr", n="Набір: маска для сну та резинка", p=3100, ph="img/sets/maskscr-litnie-pole.webp", neutral=False, aud=["team", "key"], occ=["holiday", "thanks"], why="Готовий набір про відпочинок, а не про роботу."),
    dict(k="tw44", n="Набір: твіллі та хустка 44 × 44", p=3200, ph="img/sets/tw44-vpevnenist.webp", neutral=False, aud=["key", "lead"], occ=["years", "thanks"], why="Стрічка й хустка в одному принті."),
    dict(k="h65", n="Хустка 65 × 65", p=3200, ph="img/kolo-sontsia.webp", neutral=False, aud=["key", "lead"], occ=["years"], why="Класичний розмір: на шию, на голову, на плечі."),
    dict(k="song", n="Набір: маска, закладка й резинка", p=3600, ph="img/sets/sleep-pidnesennia.webp", neutral=False, aud=["key", "lead"], occ=["years", "thanks"], why="Із колекції «Співоча душа»: частина коштів від колекції йде на гнізда для сиворакші."),
    dict(k="cert4", n="Сертифікат на 4 000 грн", p=4000, ph="img/sets/cert-2000.webp", neutral=True, aud=["lead", "key", "remote"], occ=["years", "thanks"], why="Людина обирає сама — будь-який товар каталогу."),
    dict(k="pil", n="Шовкова наволочка 50 × 70", p=4200, ph="img/sets/pillow-tuman.webp", neutral=True, aud=["lead", "key"], occ=["years", "thanks"], why="Однотонна річ для дому. Підходить усім."),
    dict(k="h88", n="Хустка 88 × 88", p=4400, ph="img/prob88.webp", neutral=False, aud=["lead"], occ=["years"], why="Найбільша хустка Obiimy: на плечі, на голову, поясом."),
    dict(k="three", n="Набір: три твіллі", p=4800, ph="img/sets/three-twilly.webp", neutral=False, aud=["lead", "key"], occ=["years", "thanks"], why="Три стрічки у святковому пакуванні — принти можна обрати різні."),
]
CAT = {c["k"]: c for c in CATALOG}
SHORT_N = {"scr": "Резинка", "book": "Закладка", "tw": "Твіллі", "h44": "Хустка 44 × 44 двостор.", "h65": "Хустка 65 × 65", "h88": "Хустка 88 × 88", "pil": "Наволочка", "mask": "Маска для сну", "scrset": "Три резинки", "twscr": "Твіллі та резинка", "maskscr": "Маска та резинка", "tw44": "Твіллі та хустка 44", "song": "Маска, закладка, резинка", "three": "Три твіллі", "cert1": "Сертифікат 1 000 грн", "cert15": "Сертифікат 1 500 грн", "cert2": "Сертифікат 2 000 грн", "cert25": "Сертифікат 2 500 грн", "cert4": "Сертифікат 4 000 грн"}
def sp(k):
    """«name — price» for the lists; certificates carry the price in the name."""
    return SHORT[k] if k.startswith("cert") else f"{SHORT[k]} — {price(CAT[k]['p'])}"

FEATURED = [   # id in b2b-sets, name, label, photo, alt, price, price note, text
    ("twscr", "Твіллі та резинка", "Хто носить аксесуари", "img/sets/twscr-makiv.webp", "Твіллі й резинка у святковій коробці", 2200, "довга твіллі 140 × 5 — 2 700 грн", "Твіллі й резинка в одному принті у святковій коробці."),
    ("maskscr", "Маска для сну та резинка", "Про відпочинок", "img/sets/maskscr-litnie-pole.webp", "Маска для сну й резинка у коробці", 3100, "", "Подарунок про відпочинок, а не про роботу: шовкова маска й резинка."),
    ("tw44", "Твіллі та хустка 44 × 44", "Ключовим людям", "img/sets/tw44-vpevnenist.webp", "Твіллі й хустка в одному принті у довгій коробці", 3200, "двосторонній друк — 3 600 грн", "Стрічка й хустка в одному принті. До річниці в компанії чи підвищення."),
    ("song", "Маска, закладка й резинка", "Подарунок із сенсом", "img/sets/sleep-pidnesennia.webp", "Маска для сну, закладка й резинка", 3600, "", "Набір із колекції «Співоча душа»: частина коштів від колекції йде на гнізда для сиворакші — птаха з Червоної книги України."),
    ("three", "Три твіллі на вибір", "До вагомої нагоди", "img/sets/three-twilly.webp", "Три твіллі в одній коробці", 4800, "", "Три стрічки 84 × 5 у святковому пакуванні — принти можна обрати різні."),
    ("scrset", "Набір шовкових резинок", "Невеликий знак уваги", "img/sets/scr3.webp", "Три шовкові резинки у коробці", 1800, "zero waste — від 1 250 грн", "Три шовкові резинки у коробці."),
]

CSS = """
  body { font-variant-numeric: lining-nums; }
  .num, .fig b, .pr b { font-variant-numeric: lining-nums tabular-nums; }
  a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible { outline: 2px solid var(--ink); outline-offset: 3px; }
  input, select, textarea { border-color: color-mix(in srgb, var(--ink) 46%, transparent); font-size: 1rem; }
  form .err { font-size: .84rem; color: #A32A1F; }
  @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } *, *::before, *::after { transition: none !important; animation: none !important; } }
  .sr { position: absolute; width: 1px; height: 1px; margin: -1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
  .facts b { overflow-wrap: anywhere; }
  @media (max-width: 960px) { .hero figure { order: 1; } }
  @media (max-width: 640px) { .hero figure img { aspect-ratio: 4 / 5; object-position: var(--hero-pos, 50% 30%); } .hero.ph-first figure { order: -1; } .hero.ph-first figure img { aspect-ratio: 2 / 1; } .hero.ph-first h1 { font-size: clamp(1.6rem, 6.6vw, 2.1rem); } .hero.ph-first .lead { font-size: .98rem; }
  .hero.ph-first .wrap > div { display: grid; gap: 14px; } .hero.ph-first .wrap > div > * { margin: 0 !important; } .hero.ph-first .cta { order: 3; } .hero.ph-first .lead { order: 4; } .hero.ph-first .fine { order: 5; } }
  @media (max-width: 960px) { .hero p.m-only { display: flex; } }

  .chips { display: flex; flex-wrap: wrap; gap: 8px; }
  .chips label { position: relative; display: inline-flex; }
  .chips input { position: absolute; inset: 0; width: 100%; height: 100%; min-height: 0; margin: 0; padding: 0; opacity: 0; cursor: pointer; }
  .chips span { display: inline-flex; align-items: center; min-height: 46px; padding: 10px 18px; border: 1px solid color-mix(in srgb, var(--ink) 46%, transparent); border-radius: 999px; background: var(--card); color: var(--ink); font-weight: 500; font-size: .92rem; }
  .chips input:checked + span { background: var(--ink); color: var(--bg); border-color: var(--ink); }
  .chips input:focus-visible + span { outline: 2px solid var(--ink); outline-offset: 3px; }
  .q { border: 0; padding: 0; margin: 0 0 24px; min-width: 0; }
  .q legend, .q .l { font-family: var(--display); font-size: 1.3rem; line-height: 1.15; padding: 0; margin-bottom: 12px; display: block; color: var(--ink); }
  .q .hint { color: var(--ink2); font-size: .85rem; margin-top: 8px; }
  .tog { display: flex; align-items: flex-start; gap: 12px; cursor: pointer; font-weight: 500; line-height: 1.35; min-height: 44px; }
  .tog input { width: 24px; height: 24px; min-height: 0; padding: 0; flex: none; margin: 2px 0 0; accent-color: var(--accent); cursor: pointer; }
  .tog small { display: block; font-weight: 400; color: var(--ink2); font-size: .85rem; margin-top: 2px; }

  .path { display: grid; grid-template-columns: repeat(8, 1fr); gap: 0; margin-bottom: 28px; position: relative; counter-reset: st; }
  .path::before { content: ""; position: absolute; left: 6%; right: 6%; top: 17px; height: 1px; background: var(--ink); opacity: .35; }
  .path button { font: inherit; color: var(--ink2); background: none; border: 0; padding: 0 4px 12px; cursor: pointer; display: grid; justify-items: center; gap: 10px; text-align: center; font-size: .82rem; line-height: 1.25; min-height: 84px; position: relative; }
  .path button::before { content: counter(st); counter-increment: st; width: 34px; height: 34px; border-radius: 50%; border: 1px solid var(--ink); background: var(--bg); display: grid; place-items: center; font-family: var(--display); font-size: 1rem; color: var(--ink); position: relative; z-index: 1; }
  .path button[aria-selected="true"] { color: var(--ink); font-weight: 600; }
  .path button[aria-selected="true"]::before { background: var(--ink); color: var(--bg); }
  .stage { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: clamp(20px, 4vw, 56px); align-items: center; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; }
  .stage img { width: 100%; height: 100%; aspect-ratio: 4 / 3.4; object-fit: cover; object-position: 50% 18%; background: #F1EEE8; }
  .stage .in { padding: clamp(20px, 3vw, 40px) clamp(20px, 3vw, 40px) clamp(20px, 3vw, 40px) 0; display: grid; gap: 14px; align-content: center; }
  .stage .in > p { color: var(--ink2); max-width: 34em; }
  .stage .gift { display: grid; gap: 6px; padding-top: 14px; border-top: 1px solid var(--line); }
  .stage .gift div { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 14px; }
  .stage .gift b { font-family: var(--display); font-weight: 400; font-size: 1.25rem; }
  .stage .gift span { color: var(--ink2); font-size: .92rem; }
  .plan { display: grid; gap: 0; border-top: 1px solid var(--ink); }
  .plan .row { display: grid; grid-template-columns: 28px minmax(0, 1fr) 90px minmax(0, 1.5fr) minmax(0, 1.5fr) 150px; gap: 12px; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--line); scroll-margin-top: 140px; }
  .plan .sel { display: grid; gap: 4px; min-width: 0; } .plan .sel small { display: none; color: var(--ink2); font-size: .78rem; }
  .plan select { width: 100%; min-width: 0; }
  .plan.one .sel:nth-of-type(2), .plan.one .hd span:nth-child(5) { opacity: .45; }
  .plan .row.off > *:not(input[type=checkbox]):not(.n) { opacity: .7; }
  .plan .row.off .n { color: var(--ink2); }
  .plan .row.flash { background: color-mix(in srgb, var(--gold) 22%, transparent); }
  .plan label.n { font-weight: 600; cursor: pointer; }
  .plan input[type=checkbox] { width: 24px; height: 24px; min-height: 0; padding: 0; accent-color: var(--accent); margin: 0; cursor: pointer; }
  .plan .qty { display: flex; align-items: center; gap: 8px; }
  .plan .qty small { color: var(--ink2); font-size: .8rem; white-space: nowrap; display: none; }
  .plan .sum { text-align: right; display: grid; gap: 2px; } .plan .sum b { font-weight: 500; white-space: nowrap; } .plan .sum small { color: var(--ink2); font-size: .74rem; line-height: 1.25; }
  .plan .hd { font-size: .74rem; letter-spacing: .14em; text-transform: uppercase; color: var(--ink3); font-weight: 600; padding: 10px 0; }
  .team { display: grid; grid-template-columns: 200px 300px; gap: 16px 36px; align-items: start; margin-bottom: 26px; }
  .team label.p { display: grid; gap: 6px; font-weight: 600; } .team label.p input { max-width: 200px; } .team small { font-weight: 400; color: var(--ink2); font-size: .8rem; }
  .total { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px 28px; padding-top: 24px; }
  .fig { display: grid; gap: 4px; }
  .fig b { font-family: var(--display); font-weight: 400; font-size: clamp(2rem, 4vw, 3.2rem); line-height: 1; }
  .fig span { color: var(--ink2); font-size: .92rem; }
  .acts { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
  .acts [aria-disabled="true"] { opacity: .5; pointer-events: none; }

  .sets { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
  .sets .card.photo { display: flex; flex-direction: column; }
  .sets .card.photo img { aspect-ratio: 4 / 3.2; background: #fff; }
  .sets .in { display: flex !important; flex-direction: column; gap: 10px; flex: 1; }
  .sets .in h3 { font-size: 1.35rem; }
  .sets .pr { margin-top: auto; padding-top: 12px; border-top: 1px solid var(--line); display: grid; gap: 2px; }
  .sets .pr b { font-family: var(--display); font-weight: 400; font-size: 1.5rem; white-space: nowrap; }
  .sets .pr span { color: var(--ink2); font-size: .82rem; }
  .sets .act { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 16px; }
  .sets .act a.more { font-size: .88rem; font-weight: 600; padding: 12px 0; }

  .lab { display: grid; grid-template-columns: minmax(0, 6fr) minmax(0, 5fr); gap: clamp(24px, 4vw, 64px); align-items: start; }
  .res { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: clamp(18px, 2.4vw, 28px); display: grid; gap: 14px; }
  .opts { display: grid; gap: 10px; }
  .opt { position: relative; display: grid; grid-template-columns: 92px minmax(0, 1fr); gap: 14px; align-items: center; border: 1px solid var(--line); border-radius: var(--radius); padding: 10px; cursor: pointer; }
  .opt input { position: absolute; inset: 0; width: 100%; height: 100%; min-height: 0; margin: 0; padding: 0; opacity: 0; cursor: pointer; }
  .opt:has(input:checked) { border-color: var(--ink); box-shadow: inset 0 0 0 1px var(--ink); }
  .opt:has(input:focus-visible) { outline: 2px solid var(--ink); outline-offset: 3px; }
  .opt img { width: 92px; height: 92px; object-fit: cover; border-radius: calc(var(--radius) - 2px); background: #F1EEE8; }
  .opt .k { font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; font-weight: 600; color: var(--ink3); }
  .opt b { font-family: var(--display); font-weight: 400; font-size: 1.2rem; line-height: 1.15; display: block; margin-top: 2px; }
  .opt .w { color: var(--ink2); font-size: .86rem; margin-top: 4px; }
  .opt .p { font-variant-numeric: lining-nums tabular-nums; font-weight: 600; margin-top: 4px; white-space: nowrap; }
  .res .fig { padding-top: 14px; border-top: 1px solid var(--line); }
  .res .fig b { font-size: clamp(1.9rem, 3.2vw, 2.6rem); }
  .res .msg { color: var(--ink2); font-size: .88rem; }
  .tool h1 { font-size: clamp(2.1rem, 3.8vw, 3.3rem); }
  .tool .wrap { align-items: start; }
  .tool .qs { margin-top: 30px; }
  .tool .side { display: grid; gap: 18px; align-content: start; } .tool .side .res { position: sticky; top: 92px; }
  .qph { margin: 0; } .qph img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; object-position: 50% 22%; border-radius: var(--radius); }
  .qph figcaption { color: var(--ink2); font-size: .82rem; margin-top: 8px; }

  .pv { margin: 0; }
  .pv .shot { position: relative; }
  .pv .shot > img { width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: var(--radius); background: #F1EEE8; }
  .paper { position: absolute; right: -2%; bottom: -5%; width: 62%; max-height: 62%; overflow: hidden; background: #FBF7EE; color: #231E2A; padding: 6% 7% 5%; transform: rotate(-3deg); box-shadow: 0 24px 50px -18px rgba(20,14,8,.55); display: grid; align-content: start; gap: 12px; }
  .hero .paper { right: auto; left: -2%; bottom: -6%; width: 56%; transform: rotate(2deg); }
  @media (max-width: 640px) { .paper { right: 10px; } .hero .paper { left: 10px; } }
  .paper img { height: 18px !important; width: auto !important; aspect-ratio: auto !important; border-radius: 0 !important; background: none !important; }
  .paper .t { font-family: var(--display); font-style: italic; font-size: clamp(1.05rem, 1.8vw, 1.5rem); line-height: 1.25; overflow-wrap: anywhere; white-space: pre-line; }
  .paper.long .t { font-size: clamp(.9rem, 1.35vw, 1.1rem); }
  .paper .s { font-size: .82rem; color: #5A5560; }
  .pv figcaption { margin-top: 26px; color: var(--ink2); font-size: .85rem; }
  .cardlab { display: grid; grid-template-columns: minmax(0, 6fr) minmax(0, 5fr); grid-template-areas: "a pv" "b pv"; gap: 0 clamp(24px, 4vw, 64px); align-items: start; }
  .cardlab .a { grid-area: a; } .cardlab .b { grid-area: b; } .cardlab .pv { grid-area: pv; position: sticky; top: 92px; }
  .count { color: var(--ink2); font-size: .84rem; margin-top: 8px; display: flex; flex-wrap: wrap; gap: 6px 18px; align-items: center; }
  .dim { opacity: .5; }
  .count button { font: inherit; font-size: .84rem; font-weight: 600; background: none; border: 0; padding: 10px 0; color: var(--ink); text-decoration: underline; text-underline-offset: 3px; cursor: pointer; }

  .tiers { display: grid; gap: 12px; } .tnote { color: var(--ink2); font-size: .82rem; margin: 0 0 -2px; }
  .tier { position: relative; display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 6px 18px; align-items: start; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 20px 22px; cursor: pointer; }
  .tier input { position: absolute; inset: 0; width: 100%; height: 100%; min-height: 0; margin: 0; padding: 0; opacity: 0; cursor: pointer; }
  .tier:has(input:checked) { border-color: var(--ink); box-shadow: inset 0 0 0 1px var(--ink); }
  .tier:has(input:focus-visible) { outline: 2px solid var(--ink); outline-offset: 3px; }
  .tier h3 { font-size: 1.45rem; }
  .tier .who { color: var(--ink2); font-size: .9rem; grid-column: 1 / -1; }
  .tier .pp { text-align: right; }
  .tier .pp b { font-family: var(--display); font-weight: 400; font-size: 1.45rem; white-space: nowrap; font-variant-numeric: lining-nums tabular-nums; display: block; }
  .tier .pp span { color: var(--ink2); font-size: .78rem; }
  .tier ul { list-style: none; margin: 4px 0 0; padding: 0; display: grid; gap: 0; grid-column: 1 / -1; }
  .tier li { font-size: .9rem; padding: 8px 0; border-top: 1px solid var(--line); display: grid; grid-template-columns: 72px minmax(0, 1fr); gap: 14px; align-items: center; }
  .tier li > div { display: grid; gap: 2px; min-width: 0; }
  .tier li img { width: 72px; height: 72px; object-fit: cover; border-radius: calc(var(--radius) - 2px); background: #F1EEE8; }
  @media (max-width: 640px) { .tier { grid-template-columns: 1fr; } .tier .pp { text-align: left; } }
  .tier li b { font-weight: 600; }
  .tier li span { color: var(--ink2); }
  .calc3 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px 22px; align-items: start; }
  .calcwrap { grid-template-columns: minmax(0, 2fr) minmax(0, 3fr); align-items: start; }
  .cph { margin: 0; position: sticky; top: 92px; } .cph img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; object-position: 50% 20%; border-radius: var(--radius); }
  .cph figcaption { color: var(--ink2); font-size: .82rem; margin-top: 8px; }
  @media (max-width: 960px) { .calcwrap { grid-template-columns: 1fr; } .calcwrap > .cph:first-child { position: static; order: -1; } .cph img { aspect-ratio: 3 / 2; } }
  .calc3 label { display: grid; gap: 6px; font-weight: 600; font-size: .92rem; }
  .calc3 small { font-weight: 400; color: var(--ink2); font-size: .8rem; }
  .warn { color: #8A4B00; font-size: .88rem; margin-top: 10px; min-height: 1.3em; }

  .trust { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: clamp(24px, 4vw, 64px); align-items: start; }
  .trust .start { margin-top: 22px; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 22px; display: grid; gap: 8px; }
  .trust .start h3 { font-size: 1.3rem; }
  .trust .start p { color: var(--ink2); font-size: .95rem; }
  .added { grid-column: 1 / -1; background: color-mix(in srgb, var(--gold) 20%, var(--card)); border: 1px solid var(--line); border-radius: var(--radius); padding: 14px 18px; margin-bottom: 16px; font-size: .95rem; }
  .added a { font-weight: 600; display: inline-block; padding: 8px 0; }
  .contact a.btn { justify-self: start; padding: 13px 24px; }
  .contact .pdf a { text-decoration: underline; text-underline-offset: 3px; }
  .grid4 .price-row { flex-wrap: wrap; } .grid4 .price-row .num { white-space: nowrap; }
  .lnk { font-weight: 600; text-decoration: underline; text-underline-offset: 3px; display: inline-block; padding: 10px 0; }
  .hero p.m-only { display: none; }
  .stage .in .fine, .pv .fine { color: var(--ink2); font-size: .82rem; margin: 0; }

  @media (max-width: 960px) {
    .path { grid-template-columns: repeat(4, 1fr); row-gap: 14px; } .path::before { display: none; }
    .path button { font-size: .74rem; overflow-wrap: anywhere; hyphens: auto; padding-inline: 2px; }
    .stage { grid-template-columns: 1fr; } .stage .in { padding: 0 20px 24px; }
    .plan .row { grid-template-columns: 28px minmax(0, 1fr); } .plan .row .qty, .plan .row .sel, .plan .row .sum { grid-column: 2; } .plan .sel small { display: block; }
    .plan .row.off .qty, .plan .row.off .sel, .plan .row.off .sum { display: none; }
    .plan .row .sum { text-align: left; font-weight: 600; } .plan .hd { display: none !important; } .plan .qty small { display: inline; } .plan .qty input { max-width: 120px; }
    .team { grid-template-columns: 1fr; }
    .sets { grid-template-columns: 1fr 1fr; }
    .lab, .cardlab, .trust { grid-template-columns: 1fr; } .cardlab { grid-template-areas: "a" "pv" "b"; } .cardlab .pv { position: static; margin-bottom: 28px; }
  }
  @media (max-width: 600px) { .sets { grid-template-columns: 1fr; } .calc3 { grid-template-columns: 1fr; } .paper { width: 70%; } }
"""

# ─────────────────────────────────────────────────────────────── shared blocks
def facts(items):
    return '<section class="wrap" aria-label="Коротко"><div class="facts">' + "".join(f"<div><b>{b}</b><span>{s}</span></div>" for b, s in items) + "</div></section>"

def chips(name, options, checked):
    return '<div class="chips">' + "".join(f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{t}</span></label>' for v, t in options) + "</div>"

def split_field(idn, value, label="Із них не носять аксесуари"):
    """How many people get a thing «for everyone» instead of silk: bookmark, sleep mask, pillowcase, certificate."""
    return (f'<label class="p" for="{idn}">{label}<input id="{idn}" type="number" min="0" inputmode="numeric" value="{value}">'
            f'<small>Їм — річ, що підходить усім: закладка, маска для сну, наволочка, сертифікат.</small></label>')

def sets_section(alt=True):
    cards = ""
    for sid, name, who, ph, a, pr, note, text in FEATURED:
        cards += (f'<div class="card photo">{img(ph, a, sizes="(max-width: 600px) 100vw, (max-width: 960px) 50vw, 33vw")}<div class="in"><p class="eyebrow">{who}</p><h3>{name}</h3><p>{text}</p>'
                  f'<div class="pr"><b class="num">{price(pr)}</b><span>{"роздрібна ціна · " + note if note else "роздрібна ціна"}</span></div>'
                  f'<div class="act"><a class="btn btn-line btn-sm" href="#request" data-set="{name} — {price(pr)}">Додати до запиту</a><a class="more" href="b2b-sets#set-{sid}">Докладніше →</a></div></div></div>')
    return f"""
  <section class="block{" alt" if alt else ""}" id="sets"><div class="wrap">
    <div class="head"><p class="eyebrow">Готові набори</p><h2>Шість готових наборів із каталогу</h2><p class="sub">Набори Obiimy у фірмовому пакуванні. Ціни роздрібні; підписи над назвами — наші поради. Є ті, хто не носить аксесуари? Речі, що підходять усім, — у <a href="#all">наступному блоці</a>.</p></div>
    <div class="sets">{cards}</div>
    <p class="note">Усі набори, зокрема зібрані під запит, — у <a href="b2b-sets">каталозі корпоративних наборів</a>.</p>
  </div></section>"""

def everyone_section(alt=False):
    def c(ph, a, eb, h, p, lab, pr):
        return f'<div class="card photo">{img(ph, a, sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">{eb}</p><h3>{h}</h3><p>{p}</p><div class="price-row"><span>{lab}</span><span class="num">{pr}</span></div></div></div>'
    return f"""
  <section class="block{" alt" if alt else ""}" id="all"><div class="wrap">
    <div class="head"><p class="eyebrow">Для всієї команди</p><h2>Речі, що підходять усім</h2><p class="sub">У команді різні люди. Ці речі з каталогу Obiimy доречно подарувати кожному — і тим, хто хустку не носить.</p></div>
    <div class="grid4">
      {c("img/mask-svoboda.webp", "Шовкова маска для сну", "Відпочинок", "Маска для сну", "Після відрядження, перед відпусткою, на підтримку.", "Роздрібна ціна", "2 700 грн")}
      {c("img/sets/bookmark-melodiia.webp", "Шовкова закладка для книги", "Знак уваги", "Закладка для книги", "До першого дня чи дня народження.", "Роздрібна ціна", "800 грн")}
      {c("img/sets/pillow-tuman.webp", "Однотонна шовкова наволочка", "Для дому", "Наволочка 50 × 70", "Однотонна: «Туман», «Хмара», «Капучино».", "Роздрібна ціна", "4 200 грн")}
      {c("img/sets/cert-2000.webp", "Подарунковий сертифікат Obiimy", "На вибір", "Сертифікат", 'Людина обирає сама протягом трьох місяців. <a href="b2b-certificates">Докладніше →</a>', "Номінали", "1 000–4 000 грн")}
    </div>
  </div></section>"""

def how_section(photo, alt_text, alt=False):
    return f"""
  <section class="block{" alt" if alt else ""}" id="how"><div class="wrap grid2">
    <div><p class="eyebrow">Що буде після запиту</p><h2 style="margin-top:10px">Від запиту до відправки</h2>
      <div class="steps" style="grid-template-columns:1fr;gap:18px;margin-top:22px">
        <div><h3>Запит</h3><p>Ви надсилаєте запит із цієї сторінки: нагоди, кількість і дату, до якої потрібні подарунки.</p></div>
        <div><h3>Добірка й розрахунок</h3><p>У відповідь надсилаємо добірку речей і принтів та розрахунок окремими рядками: речі, оформлення привітання, доставка. Чи встигаємо до вашої дати — пишемо одразу.</p></div>
        <div><h3>Список і привітання</h3><p>Ви надсилаєте список отримувачів і текст привітання.</p></div>
        <div><h3>Відправка</h3><p>Відправляємо Новою поштою — кожному окремо чи в офіс, як домовимось.</p></div>
      </div>
    </div>
    <figure>{img(photo, alt_text, sizes="(max-width: 960px) 100vw, 50vw")}</figure>
  </div></section>"""

def faq_section(extra="", alt=True):
    return f"""
  <section class="block{" alt" if alt else ""}" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Питання</p><h2>Що питають HR і офіс-менеджери</h2></div>
    <div class="faq">
      <details><summary>Які строки?</summary><p>Залежать від кількості та наявності принтів. Вкажіть у запиті дату, до якої потрібні подарунки, — у відповіді напишемо, чи встигаємо, і запропонуємо варіанти з наявності.</p></details>
      <details><summary>Що входить у суму на сторінці?</summary><p>Роздрібні ціни речей на obiimy.world. Оформлення привітання й доставку покажемо в розрахунку окремими рядками.</p></details>
      <details><summary>У чому приїдуть подарунки?</summary><p>Набори — у святковій коробці Obiimy; як виглядає саме ваш — і пакування окремих речей — покажемо на фото в добірці разом із розрахунком.</p></details>
      <details><summary>Що подарувати чоловікам?</summary><p>Маску для сну, закладку для книги, однотонну шовкову наволочку або сертифікат. Якщо потрібен один подарунок для всіх — сертифікат найпростіший.</p></details>
      {extra}
      <details><summary>Чи є мінімальне замовлення?</summary><p>Напишіть, скільки подарунків потрібно, — навіть якщо це один подарунок до річниці. Умови для вашої кількості надішлемо разом із розрахунком.</p></details>
      <details><summary>Як доставляєте — і що з колегами за кордоном?</summary><p>Напишіть у запиті, як зручніше: кожному на відділення Нової пошти чи однією посилкою в офіс. Для колег за кордоном вкажіть країни — спосіб і вартість доставки назвемо в розрахунку. Найпростіше для них — електронний сертифікат.</p></details>
      <details><summary>Оплата й документи для компанії</summary><p>Вкажіть у запиті форму оплати й потрібні документи — підтвердимо разом із розрахунком.</p></details>
      <details><summary>Чи можна додати логотип компанії?</summary><p>Напишіть, що саме потрібно, — у розрахунку відповімо, чи можемо це зробити.</p></details>
      <details><summary>Чи однакові речі за розміром?</summary><p>Розмір хустки може відрізнятися на 0–2,5 см: так зазначено на сторінках товарів — це особливість обробки шовку.</p></details>
      <details><summary>Що, якщо із замовленням щось не так?</summary><p>Напишіть нам — розберемося. Умови обміну та повернення — на <a href="https://obiimy.world/obmin-ta-povernennya/">obiimy.world</a>.</p></details>
    </div>
  </div></section>"""

def proof_section(alt=False):
    return f"""
  <section class="block{" alt" if alt else ""}" id="proof"><div class="wrap trust">
    <div><p class="eyebrow">Довіра</p><h2 style="margin-top:10px">Хто стоїть за Obiimy</h2>
      <p style="margin-top:14px;color:var(--ink2);max-width:36em">Український бренд шовкових аксесуарів. Засновниця й художниця — Світлана Сніжко: принти авторські. 100% італійський шовк, виготовлено в Україні. Бренд заснований під час війни й бере участь у благодійних ініціативах на допомогу військовим і постраждалим.</p>
      <div class="start"><h3>Не впевнені — почніть із малого</h3><p>Замовте подарунки на дні народження одного місяця. Побачите речі, пакування й привітання, перш ніж планувати рік.</p></div>
    </div>
    <div class="proof">
      <div><b>INTERTOP · Hram</b><span>Роздрібні партнери в Україні</span></div>
      <div><b>Be Brave · UFD London</b><span>Партнери за кордоном: Канада, Лондон</span></div>
      <div><b>LIGA.net · INSIDER UA</b><span>Писали про бренд</span></div>
      <div><b>Шоурум у Києві</b><span>{SHOWROOM.replace("Київ, ", "")} — шовк можна побачити й відчути на дотик</span></div>
      <div><b>Співпраця</b><span><a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a></span></div>
    </div>
  </div></section>"""

def request_section(pid, subject, title, lead, back, alt=True):
    form = form_html(pid, subject, [
        ("company", "Компанія", "input", True, {"ph": "Назва компанії", "ac": "organization"}),
        ("name", "Ваше ім’я", "input", True, {"ph": "Як до вас звертатись", "ac": "name"}),
        ("email", "Email", "email", True, {"ph": "сюди надішлемо розрахунок", "ac": "email", "err": "Вкажіть коректний email"}),
        ("phone", "Телефон", "tel", False, {"ph": "+380 — якщо зручніше телефоном", "ac": "tel"}),
        ("people", "Скільки подарунків", "number", False, {"ph": "наприклад, 40"}),
        ("date", "Дата, до якої потрібно", "date", False, {}),
        ("delivery", "Доставка", "select:Кожному на відділення Нової пошти|В офіс однією посилкою|Комбіновано|Частина — за кордон", False, {"full": True}),
        ("note", "Розрахунок і коментар", "textarea", False, {"ph": "Нагода, побажання до принтів, склад команди…"}),
    ], "Відповідаємо з добіркою та розрахунком.")
    return f"""
  <section class="form-block{" alt" if alt else ""}" id="request"><div class="wrap">
    <div class="contact"><p class="eyebrow">Запит</p><h2>{title}</h2><p>{lead}</p><p class="big"><a href="{PHONE_HREF}">{PHONE}</a></p><p><a href="mailto:{MAIL}">{MAIL}</a></p><a class="btn btn-line" href="{TG}">Написати в Telegram</a><p class="pdf"><a href="obiimy-podarunky-dlia-komandy.pdf" download="Obiimy-podarunky-dlia-komandy.pdf" type="application/pdf">Презентація для HR (PDF, 4,3 МБ) ↓</a></p><p class="show">Шоурум: {SHOWROOM} — шовк можна побачити й відчути на дотик.</p></div>
    <div><p class="added" id="added" hidden><b>Додано до запиту:</b> <span id="added-t"></span> · <a href="#{back}">змінити</a></p>{form}</div>
  </div></section>"""

COMMON_JS = """
    function fmt(n) { return String(Math.round(n)).replace(/\\B(?=(\\d{3})+(?!\\d))/g, '\\u00a0') + '\\u00a0грн'; }
    function plain(s) { return s.replace(/\\u00a0/g, ' '); }
    function pl(n, a, b, c) { var m = n % 100, k = n % 10; return (m > 10 && m < 15) ? c : k === 1 ? a : (k > 1 && k < 5) ? b : c; }
    function gifts(n) { return n + ' ' + pl(n, 'подарунок', 'подарунки', 'подарунків'); }
    function int(el, min) { var v = parseInt(el.value, 10); return isNaN(v) ? min : Math.max(min, v); }
    var FORM = document.getElementById('__FORM__'), NOTE = FORM.querySelector('[name=note]'), M1 = '=== Розрахунок із сайту ===', M2 = '=== Кінець розрахунку ===';
    function grow() { NOTE.style.height = 'auto'; NOTE.style.height = Math.min(440, NOTE.scrollHeight + 4) + 'px'; }
    function added(text) {
      var a = document.getElementById('added'); a.hidden = false; document.getElementById('added-t').textContent = text.replace(/(\\d) (?=\\d|грн)/g, '$1\\u00a0');
      setTimeout(function () { a.scrollIntoView({ block: 'start', behavior: 'smooth' }); var f = FORM.querySelector('input'); if (f) f.focus({ preventScroll: true }); }, 60);
    }
    function put(lines, people, summary, tag) {
      var m1 = tag ? '=== ' + tag + ' ===' : M1, m2 = tag ? '=== Кінець: ' + tag + ' ===' : M2;
      var block = m1 + '\\n' + lines.join('\\n') + '\\n' + m2, v = NOTE.value, i = v.indexOf(m1), j = v.indexOf(m2);
      if (i >= 0 && j > i) v = v.slice(0, i) + block + v.slice(j + m2.length);
      else v = (v.trim() ? v.replace(/\\s+$/, '') + '\\n\\n' : '') + block;
      NOTE.value = v; grow();
      if (people) FORM.querySelector('[name=people]').value = people;
      added(summary);
    }
    NOTE.addEventListener('input', grow);
    [].forEach.call(document.querySelectorAll('[data-set]'), function (a) {
      a.addEventListener('click', function () {
        var line = 'Набір: ' + a.dataset.set;
        if (NOTE.value.indexOf(line) < 0) NOTE.value = (NOTE.value.trim() ? NOTE.value.replace(/\\s+$/, '') + '\\n' : '') + line;
        grow(); added(a.dataset.set);
      });
    });
    function copyText(text, btn) {
      var t = btn.textContent;
      function ok() { btn.textContent = 'Скопійовано'; setTimeout(function () { btn.textContent = t; }, 1800); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(ok, function () {});
      else { var x = document.createElement('textarea'); x.value = text; document.body.appendChild(x); x.select(); try { document.execCommand('copy'); ok(); } catch (e) {} document.body.removeChild(x); }
    }
    var stickyText = '';
    function sticky(text) { stickyText = text; var s = document.querySelector('#sticky span'); if (s) s.textContent = text; }
    document.addEventListener('DOMContentLoaded', function () { if (stickyText) sticky(stickyText); });
"""

def script(form_id, body):
    return "<script>(function () {" + COMMON_JS.replace("__FORM__", form_id) + body + "})();</script>"

# ─────────────────────────────────────────────────────────────── 1. the path of a person in the company (Form)
# occasion: id, short label, title, text, photo, alt, silk item, item for a mixed team, default share of the team per year (editable)
STAGES = [
    ("first", "Перший день", "Перший день у компанії", "Людина ще не знає, де кавоварка, а на столі вже лежить подарунок із привітанням від команди.", "img/twilly-zolote.webp", "Шовкова твіллі", "tw", "book", .15),
    ("trial", "Випробувальний", "Випробувальний позаду", "Три місяці минули, людина залишається. Невеликий знак уваги з привітанням від керівника.", "img/sets/bookmark-melodiia.webp", "Шовкова закладка для книги", "scr", "book", .15),
    ("bday", "День народження", "День народження", "Подарунок за списком на місяць. Не знаєте смаків — сертифікат: людина обере сама.", "img/twilly-zolote.webp", "Шовкова твіллі", "tw", "cert1", 1),
    ("years", "Річниця в компанії", "Рік, три, п’ять", "Що довше людина з вами, то більша річ: твіллі на перший рік, хустка 65 × 65 на третій, велика хустка 88 × 88 на п’ятий.", "photo/kolo-3.webp", "Хустка на бежевому пальті", "h65", "mask", .2),
    ("up", "Підвищення", "Нова роль", "Підвищення, перший власний відділ, перший великий клієнт. Річ, яка залишиться надовго, — і привітання вашими словами.", "photo/probudzhennia-2.webp", "Шовкова хустка на плечах", "h44", "mask", .1),
    ("team", "Перемога команди", "Закритий проєкт", "Реліз, складний квартал, виграний тендер. Однаковий подарунок кожному в команді.", "img/set-3twilly.webp", "Три твіллі в одній коробці", "tw", "book", .3),
    ("care", "Підтримка", "Коли людині потрібна підтримка", "Повернення після лікарняного чи довгої перерви, складний період у житті. Річ для відпочинку — без зайвих слів.", "img/sets/maskscr-litnie-pole.webp", "Маска для сну й резинка у коробці", "maskscr", "mask", .05),
    ("bye", "Прощання", "Останній робочий день", "Людина йде далі — і забирає з собою добру пам’ять про компанію. Велика хустка або сертифікат, щоб обрала сама.", "photo/mizh-1.webp", "Велика шовкова хустка на голові", "h88", "cert4", .05),
]

def page():
    tabs = "".join(f'<button type="button" role="tab" id="t-{sid}" aria-controls="stage" aria-selected="{"true" if i == 0 else "false"}">{short}</button>' for i, (sid, short, *_r) in enumerate(STAGES))
    opts = "".join(opt(c) for c in CATALOG)
    rows = "".join(f'''<div class="row" data-id="{sid}" data-share="{share}" data-silk="{silk}" data-neutral="{neu}">
        <input type="checkbox" id="c-{sid}" {"checked" if sid in ("first", "bday", "years") else ""} aria-label="{short}: враховувати в плані">
        <label class="n" for="c-{sid}">{short}</label>
        <span class="qty"><input type="number" min="0" inputmode="numeric" aria-label="{short}: скільки подарунків на рік" data-k="n"><small>шт. на рік</small></span>
        <span class="sel"><small>Шовкова річ</small><select aria-label="{short}: шовкова річ" data-k="silk">{opts}</select></span>
        <span class="sel"><small>Тим, хто не носить аксесуари</small><select aria-label="{short}: річ для тих, хто не носить аксесуари" data-k="neu">{opts}</select></span>
        <span class="sum"><b class="num" data-k="sum"></b><small data-k="split"></small></span></div>''' for sid, short, _t, _d, _p, _a, silk, neu, share in STAGES)
    data = J([dict(title=t, text=d, photo=p, alt=a, silk=CAT[s]["n"], sp=CAT[s]["p"], neu=CAT[n]["n"], np=CAT[n]["p"], same=s == n) for _i, _sh, t, d, p, a, s, n, _x in STAGES])
    f0 = STAGES[0]
    js = """
    var S = __S__, P = __P__, N = __N__, SN = __SN__;
    var tabs = [].slice.call(document.querySelectorAll('.path button')), cur = 0, im = document.querySelector('#stage img'), addBtn = document.getElementById('st-add');
    var rows = [].slice.call(document.querySelectorAll('#rows .row[data-id]')), people = document.getElementById('people'), neu = document.getElementById('neu');
    function rowOn(i) { return rows[i].querySelector('input[type=checkbox]').checked; }
    function show(i, focus) {
      cur = (i + S.length) % S.length; var s = S[cur];
      tabs.forEach(function (t, k) { t.setAttribute('aria-selected', k === cur ? 'true' : 'false'); t.tabIndex = k === cur ? 0 : -1; });
      document.getElementById('stage').setAttribute('aria-labelledby', tabs[cur].id);
      document.getElementById('st-k').textContent = 'Нагода ' + (cur + 1) + ' / ' + S.length;
      document.getElementById('st-t').textContent = s.title; document.getElementById('st-d').textContent = s.text;
      document.getElementById('st-i').textContent = s.silk; document.getElementById('st-p').textContent = fmt(s.sp);
      document.getElementById('st-n').hidden = s.same;
      document.getElementById('st-ni').textContent = s.neu; document.getElementById('st-np').textContent = fmt(s.np);
      im.removeAttribute('srcset'); im.removeAttribute('sizes'); im.src = s.photo; im.alt = s.alt;
      mark(); if (focus) tabs[cur].focus();
    }
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { show(k); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') { e.preventDefault(); show(cur + 1, true); } else if (e.key === 'ArrowLeft') { e.preventDefault(); show(cur - 1, true); }
        else if (e.key === 'Home') { e.preventDefault(); show(0, true); } else if (e.key === 'End') { e.preventDefault(); show(S.length - 1, true); }
      });
    });
    function mark() { var on = rowOn(cur); addBtn.className = on ? 'lnk' : 'btn btn-line btn-sm'; addBtn.textContent = on ? 'У плані на рік ✓ · змінити кількість' : 'Додати в план на рік'; }
    function defaults() {
      var n = int(people, 1);
      rows.forEach(function (r) {
        var q = r.querySelector('[data-k=n]');
        if (!q.dataset.touched) q.value = Math.max(1, Math.round(n * parseFloat(r.dataset.share)));
      });
    }
    rows.forEach(function (r) { r.querySelector('[data-k=silk]').value = r.dataset.silk; r.querySelector('[data-k=neu]').value = r.dataset.neutral; });
    var state = { total: 0, gifts: 0, lines: [], n: 0, m: 0 };
    function calc() {
      var total = 0, g = 0, lines = [], n = int(people, 1), m = Math.min(n, int(neu, 0));
      document.getElementById('t-warn').textContent = int(neu, 0) > n ? 'Людей у команді менше, ніж тих, хто не носить аксесуари, — рахуємо для ' + n + '.' : '';
      document.getElementById('rows').classList.toggle('one', !m);
      rows.forEach(function (r) {
        var on = r.querySelector('input[type=checkbox]').checked, q = int(r.querySelector('[data-k=n]'), 0);
        var ks = r.querySelector('[data-k=silk]').value, kn = r.querySelector('[data-k=neu]').value;
        var qn = Math.min(q, Math.round(q * m / n)), qs = q - qn, same = ks === kn || !qn, s = qs * P[ks] + qn * P[kn];
        if (same) { qs = q; qn = 0; s = q * P[ks]; }
        r.classList.toggle('off', !on);
        r.querySelector('[data-k=sum]').textContent = on ? fmt(s) : '—';
        r.querySelector('[data-k=split]').textContent = on && qn ? (qs + ' × ' + SN[ks]).replace(/ /g, '\\u00a0') + ' + ' + (qn + ' × ' + SN[kn]).replace(/ /g, '\\u00a0') : '';
        if (on && q > 0) { total += s; g += q; lines.push('— ' + r.querySelector('label.n').textContent + ': ' + qs + ' × ' + N[ks] + (qn ? ' + ' + qn + ' × ' + N[kn] : '') + ' = ' + plain(fmt(s))); }
      });
      state = { total: total, gifts: g, lines: lines, n: n, m: m };
      document.getElementById('tot').textContent = fmt(total);
      document.getElementById('tot-s').textContent = g ? gifts(g) + ' на рік · роздрібні ціни, без доставки' : 'Позначте хоча б одну нагоду';
      ['send', 'copy'].forEach(function (id) { document.getElementById(id).setAttribute('aria-disabled', g ? 'false' : 'true'); });
      sticky(g ? 'План на рік: ' + plain(fmt(total)) : 'Подарунки для команди · від 700 грн');
      mark();
    }
    function text() { return ['План на рік · людей у команді: ' + state.n + (state.m ? ', із них не носять аксесуари: ' + state.m : '') + ' (роздрібні ціни obiimy.world, без доставки):'].concat(state.lines, ['Разом: ' + plain(fmt(state.total)) + ' · ' + gifts(state.gifts)]); }
    rows.forEach(function (r) {
      r.querySelector('[data-k=n]').addEventListener('input', function () { this.dataset.touched = '1'; calc(); });
      [].forEach.call(r.querySelectorAll('select'), function (s) { s.addEventListener('change', calc); });
      r.querySelector('input[type=checkbox]').addEventListener('change', calc);
    });
    people.addEventListener('input', function () { defaults(); calc(); });
    neu.addEventListener('input', calc);

    defaults(); calc(); show(0);
    addBtn.addEventListener('click', function (e) {
      e.preventDefault(); var r = rows[cur]; r.querySelector('input[type=checkbox]').checked = true; calc();
      r.scrollIntoView({ block: 'center', behavior: 'smooth' }); r.classList.add('flash'); setTimeout(function () { r.classList.remove('flash'); }, 1600);
    });
    document.getElementById('send').addEventListener('click', function (e) {
      if (!state.gifts) { e.preventDefault(); return; }
      put(text(), state.gifts, fmt(state.total) + ' · ' + gifts(state.gifts));
    });
    document.getElementById('copy').addEventListener('click', function () { if (state.gifts) copyText(text().join('\\n'), this); });
    """.replace("__S__", data).replace("__P__", J({c["k"]: c["p"] for c in CATALOG})).replace("__N__", J({c["k"]: c["n"] for c in CATALOG})).replace("__SN__", J({c["k"]: SHORT_N.get(c["k"], c["n"]).lower() for c in CATALOG}))
    body = hero("Для HR і офіс-менеджерів · подарунки співробітникам", "Шовкові подарунки для команди — від першого дня до річниці в компанії",
        "Подарунок і привітання від компанії — до дня народження, річниці, закритого проєкту. Оберіть нагоди, порахуйте суму на рік і надішліть запит: у відповідь отримаєте добірку й розрахунок.",
        "Підібрати подарунок і порахувати", "Готові набори", "#sets", SAMPLE,
        "photo/hratsiia-2.webp", "Шовкова хустка поясом на синьому жакеті", "Шовкова хустка — поясом на жакеті", cls=" h1-sm ph-first", pos="50% 58%", cta1_href="#path") + facts([
        ("8 нагод", "Від першого дня до прощання — увесь шлях людини в компанії"),
        ("700–4 800 грн", "Роздрібні ціни речей і наборів із каталогу"),
        ("Для всієї команди", "Є речі, що підходять усім: маска для сну, закладка, сертифікат"),
        ("Привітання", "Вашими словами — разом із подарунком"),
    ]) + f'''

  <section class="block" id="path"><div class="wrap">
    <div class="head"><p class="eyebrow">Нагоди</p><h2>Шлях людини в компанії</h2><p class="sub">Вісім моментів, коли подарунок від роботодавця запам’ятовується. Оберіть нагоду — покажемо, що радимо подарувати і скільки це коштує за роздрібною ціною.</p></div>
    <div class="path" role="tablist" aria-label="Нагоди для подарунка">{tabs}</div>
    <div class="stage" id="stage" role="tabpanel" aria-labelledby="t-{f0[0]}">
      {img(f0[4], f0[5], sizes="(max-width: 960px) 100vw, 45vw")}
      <div class="in"><p class="eyebrow" id="st-k">Нагода 1 / 8</p><h3 id="st-t" style="font-size:clamp(1.5rem,2.4vw,2.1rem)">{f0[2]}</h3><p id="st-d">{f0[3]}</p>
        <div class="gift"><div><b id="st-i">{CAT[f0[6]]["n"]}</b><span id="st-p" class="num">{price(CAT[f0[6]]["p"])}</span></div>
          <div id="st-n"><span>Тим, хто не носить аксесуари:</span> <span id="st-ni">{CAT[f0[7]]["n"]}</span> <span id="st-np" class="num">{price(CAT[f0[7]]["p"])}</span></div></div>
        <p style="margin-top:4px"><a class="btn btn-line btn-sm" href="#plan" id="st-add" role="button">Додати в план на рік</a></p>
        <p class="fine">Фото — приклад принта; наявність у потрібному форматі підтвердимо в розрахунку.</p></div>
    </div>
  </div></section>

  <section class="block alt" id="plan"><div class="wrap">
    <div class="head"><p class="eyebrow">План на рік</p><h2>Скільки це коштує для вашої команди</h2><p class="sub">Вкажіть розмір команди, позначте нагоди й оберіть речі для кожної: шовкову — і ту, що підходить усім, для тих, хто аксесуари не носить. Кількість подарунків ми підставили для прикладу — змініть під себе.</p></div>
    <div class="team"><label class="p" for="people">Людей у команді<input id="people" type="number" min="1" inputmode="numeric" value="40"></label>{split_field("neu", 16)}</div>
    <p class="warn" id="t-warn" aria-live="polite" style="margin:-10px 0 14px"></p>
    <div class="plan" id="rows">
      <div class="row hd" aria-hidden="true"><span></span><span>Нагода</span><span>На рік</span><span>Шовкова річ</span><span>Тим, хто не носить аксесуари</span><span style="text-align:right">Сума</span></div>
      {rows}
    </div>
    <div class="total"><div class="fig" aria-live="polite"><b id="tot" class="num">0 грн</b><span id="tot-s"></span></div>
      <div class="acts"><button class="btn btn-line" type="button" id="copy">Скопіювати розрахунок</button><a class="btn btn-gold" href="#request" id="send" role="button">Надіслати план на розрахунок</a></div></div>
    <p class="note">Суми — за роздрібними цінами obiimy.world, без доставки. Точний розрахунок для вашої компанії надішлемо у відповідь на запит.</p>
  </div></section>
  {sets_section(alt=False)}
  {everyone_section(alt=True)}
  {how_section("photo/bag-1.webp", "Шовкова твіллі на ручці білої сумки", alt=False)}
  {faq_section('<details><summary>Як не помилитися з принтом?</summary><p>Надішліть кілька слів про людину чи команду — запропонуємо принти на вибір. Або подаруйте сертифікат: людина обере сама.</p></details><details><summary>Що, якщо список змінився?</summary><p>Надішліть оновлений список — врахуємо його в наступній відправці.</p></details>', alt=True)}
  {proof_section(alt=False)}
  {request_section("f-team", "Подарунки для команди", "Отримати добірку й розрахунок", "Залиште контакти й дату, до якої потрібні подарунки. План із калькулятора додається до запиту одним натиском.", "plan")}
  ''' + script("f-team", js)
    return dict(slug="b2b-team", skin="form", bar=BAR, title="Шовкові подарунки для команди — Obiimy для HR і офіс-менеджерів",
                desc="Подарунки співробітникам від компанії: перший день, день народження, річниця в компанії, закритий проєкт. Шовкові речі від 700 грн, маски для сну, сертифікати від 1 000 грн.",
                og="photo/hratsiia-2.webp", nav=[("Нагоди", "path"), ("План на рік", "plan"), ("Набори", "sets"), ("Для всіх", "all"), ("Після запиту", "how"), ("Питання", "faq")],
                cta="Запит", sticky="Подарунки для команди · від 700 грн", body=body)

# ─────────────────────────────────────────────────────────────── 2. the first screen is the tool (Studio)
WHO = [("team", "Усій команді"), ("new", "Новим співробітникам"), ("key", "Ключовим людям"), ("lead", "Керівникам"), ("remote", "Віддаленим колегам")]
OCC = [("bday", "День народження"), ("holiday", "Свято"), ("years", "Річниця в компанії"), ("first", "Перший день"), ("thanks", "Подяка за проєкт")]
BUD = [("1000", "до 1 000 грн"), ("2500", "до 2 500 грн"), ("3500", "до 3 500 грн"), ("5000", "до 5 000 грн")]

def quiz():
    js = """
    var C = __CAT__, WHO = __WHO__, OCC = __OCC__, BUD = __BUD__, box = document.getElementById('r-opts'), people = document.getElementById('q-people'), neu = document.getElementById('q-neu');
    var list = [], chosen = null, LAB = ['Економно', 'Оптимально', 'Максимум у бюджеті'];
    function val(n) { var r = document.querySelector('input[name=' + n + ']:checked'); return r ? r.value : ''; }
    function num() { return int(people, 1); }
    function split() { var n = num(); return { n: n, m: Math.min(n, int(neu, 0)) }; }
    function pick() {
      var who = val('who'), occ = val('occ'), b = parseInt(val('budget'), 10);
      function score(c) { return (c.aud.indexOf(who) >= 0 ? 2 : 0) + (c.occ.indexOf(occ) >= 0 ? 1 : 0); }
      var silk = C.filter(function (c) { return c.p <= b && !c.neutral; }), all = C.filter(function (c) { return c.p <= b && c.neutral; });
      silk.forEach(function (c) { c.s = score(c); }); all.forEach(function (c) { c.s = score(c); });
      // remote colleagues: a certificate is the honest answer, the person chooses on obiimy.world
      var base = who === 'remote' ? all.filter(function (c) { return c.k.indexOf('cert') === 0; }) : silk;
      // the best-fitting things first; if fewer than three, fill from the next scores, dearer first; then cheapest / middle / dearest
      var ranked = base.slice().sort(function (x, y) { return (y.s - x.s) || (y.p - x.p); }), top = ranked.length ? ranked.filter(function (c) { return c.s === ranked[0].s; }) : [];
      ranked.forEach(function (c) { if (top.length < 3 && top.indexOf(c) < 0) top.push(c); });
      top.sort(function (x, y) { return x.p - y.p; });
      list = top.length > 3 ? [top[0], top[Math.floor((top.length - 1) / 2)], top[top.length - 1]] : top;
      // the budget matters: the dearest thing that still fits the audience takes the top slot
      var max = base.filter(function (c) { return c.s >= 2; }).sort(function (x, y) { return y.p - x.p; })[0];
      if (max && list.length === 3 && list.indexOf(max) < 0 && max.p > list[2].p) list[2] = max;
      document.getElementById('r-h').textContent = list.length === 3 ? 'Три варіанти у вашому бюджеті' : list.length === 2 ? 'Два варіанти у вашому бюджеті' : 'Варіант у вашому бюджеті';
      // a companion that suits everyone: best fit first, not dearer than the silk thing if possible, then the closest price
      list.forEach(function (c) { c.mate = c.neutral ? null : all.slice().sort(function (x, y) { return (y.s - x.s) || ((x.p > c.p) - (y.p > c.p)) || (Math.abs(x.p - c.p) - Math.abs(y.p - c.p)); })[0] || null; });
      var fit = base.some(function (c) { return c.aud.indexOf(who) >= 0; }), msg = who === 'remote' ? 'Віддаленим колегам і колегам за кордоном найпростіше надіслати електронний сертифікат — людина обере сама на obiimy.world.' : '';
      if (!fit && who !== 'remote') {
        var near = C.filter(function (c) { return c.aud.indexOf(who) >= 0 && !c.neutral; }).sort(function (x, y) { return x.p - y.p; })[0];
        msg = 'У цьому бюджеті немає речей, які радимо саме ' + WHO[who].toLowerCase() + ', — показуємо найближчі.' + (near ? ' Для них радимо від ' + plain(fmt(near.p)) + ' — ' + near.n.toLowerCase() + '.' : '');
      }
      var lower = BUD.filter(function (x) { return x < b; }).pop();
      if (!msg && fit && max && lower && max.p <= lower) msg = 'Для цієї групи дорожчих речей не радимо — максимум ' + plain(fmt(max.p)) + '. Решту бюджету можна віддати на другий подарунок протягом року.';
      document.getElementById('r-msg').textContent = msg;
      var keep = chosen && list.filter(function (c) { return c.k === chosen.k; })[0];
      chosen = keep || list[Math.min(1, list.length - 1)];
      var hadFocus = document.activeElement && document.activeElement.name === 'opt';
      draw();
      if (hadFocus) { var r = box.querySelector('input:checked'); if (r) r.focus({ preventScroll: true }); }
      document.getElementById('r-status').textContent = 'Підбір оновлено: ' + list.map(function (c) { return c.n + ', ' + plain(fmt(c.p)); }).join('; ');
    }
    function draw() {
      var sp = split(); box.textContent = '';
      list.forEach(function (c, i) {
        var l = document.createElement('label'); l.className = 'opt';
        var r = document.createElement('input'); r.type = 'radio'; r.name = 'opt'; r.value = c.k; r.checked = c === chosen;
        r.addEventListener('change', function () { chosen = c; total(); });
        var im = document.createElement('img'); im.src = c.ph; im.alt = ''; im.width = 92; im.height = 92; im.loading = 'lazy';
        var d = document.createElement('span');
        var k = document.createElement('span'); k.className = 'k'; k.textContent = list.length === 3 ? LAB[i] : 'Варіант ' + (i + 1);
        var b = document.createElement('b'); b.textContent = c.n;
        var w = document.createElement('span'); w.className = 'w'; w.textContent = c.why;
        var p = document.createElement('span'); p.className = 'p'; p.textContent = fmt(c.p);
        var els = [k, b, w, p];
        if (sp.m && c.mate) { var m = document.createElement('span'); m.className = 'w'; m.textContent = 'Тим, хто не носить аксесуари: ' + c.mate.n.toLowerCase().replace(/(\\d) (?=\\d)/g, '$1\\u00a0') + (c.mate.k.indexOf('cert') === 0 ? '' : ' — ' + fmt(c.mate.p)); els.splice(3, 0, m); }
        els.forEach(function (e) { e.style.display = 'block'; d.appendChild(e); });
        l.appendChild(r); l.appendChild(im); l.appendChild(d); box.appendChild(l);
      });
      total();
    }
    function parts() {
      var sp = split(), mate = sp.m && chosen.mate, qs = mate ? sp.n - sp.m : sp.n, out = [];
      if (mate && mate.p === chosen.p) { mate = null; qs = sp.n; }
      if (qs) out.push({ q: qs, c: chosen }); if (mate) out.push({ q: sp.m, c: mate });
      return out;
    }
    function sum() { return parts().reduce(function (t, x) { return t + x.q * x.c.p; }, 0); }
    function total() {
      if (!chosen) return;
      document.getElementById('r-total').textContent = fmt(sum());
      document.getElementById('r-note').textContent = parts().map(function (x) { return x.q + ' × ' + plain(fmt(x.c.p)); }).join(' + ') + ' · роздрібні ціни, без доставки';
      sticky('Обрано: ' + chosen.n + ' · ' + plain(fmt(sum())));
    }
    function text() {
      var sp = split();
      return ['Підбір: ' + WHO[val('who')] + ' · ' + OCC[val('occ')] + ' · бюджет на людину до ' + plain(fmt(parseInt(val('budget'), 10))) + ' · людей: ' + sp.n + (sp.m ? ', із них не носять аксесуари: ' + sp.m : '')]
        .concat(parts().map(function (x) { return '— ' + x.c.n + ': ' + x.q + ' × ' + plain(fmt(x.c.p)) + ' = ' + plain(fmt(x.q * x.c.p)); }), ['Разом: ' + plain(fmt(sum())) + ' (роздрібні ціни, без доставки)']);
    }
    [].forEach.call(document.querySelectorAll('input[name=who], input[name=occ], input[name=budget]'), function (r) { r.addEventListener('change', pick); });
    people.addEventListener('input', draw); neu.addEventListener('input', draw); pick();
    document.getElementById('r-send').addEventListener('click', function () { put(text(), num(), chosen.n + ' · ' + fmt(sum())); });
    document.getElementById('r-copy').addEventListener('click', function () { copyText(text().join('\\n'), this); });
    """.replace("__CAT__", J(CATALOG)).replace("__WHO__", J(dict(WHO))).replace("__OCC__", J(dict(OCC))).replace("__BUD__", J([int(v) for v, _t in BUD]))
    body = f'''
  <section class="hero tool"><div class="wrap">
    <div>
      <p class="eyebrow">Для HR і офіс-менеджерів · підбір подарунка</p>
      <h1 style="margin-top:14px">Підберіть подарунок для команди — за хвилину</h1>
      <p class="lead">Кому, з якої нагоди й на яку суму. Поруч одразу з’являться три варіанти з каталогу Obiimy та сума за роздрібними цінами.</p>
      <div class="qs">
        <fieldset class="q"><legend>1. Кому даруємо?</legend>{chips("who", WHO, "team")}</fieldset>
        <fieldset class="q"><legend>2. З якої нагоди?</legend>{chips("occ", OCC, "bday")}</fieldset>
        <fieldset class="q"><legend>3. Бюджет на одну людину</legend>{chips("budget", BUD, "2500")}</fieldset>
        <div class="q team" style="margin-bottom:0"><label class="p" for="q-people"><span class="l">4. Скільки людей?</span><input id="q-people" type="number" min="1" inputmode="numeric" value="20"></label>{split_field("q-neu", 8)}</div>
      </div>
      <p class="m-only cta" style="margin-top:8px"><a class="lnk" href="#res">Дивитися варіанти ↓</a></p>
    </div>
    <div class="side"><div class="res" id="res">
      <p class="eyebrow" id="r-h">Три варіанти у вашому бюджеті</p>
      <p class="sr" id="r-status" aria-live="polite"></p>
      <div class="opts" id="r-opts" role="radiogroup" aria-label="Варіанти подарунка"></div>
      <p class="msg" id="r-msg"></p>
      <div class="fig"><b id="r-total" class="num"></b><span id="r-note"></span></div>
      <div class="acts"><a class="btn btn-gold" href="#request" id="r-send" role="button">Надіслати підбір на розрахунок</a><button class="btn btn-line btn-sm" type="button" id="r-copy">Скопіювати</button></div>
      <p class="msg">Поради «кому що підходить» — наші. Фото показують приклад принта; наявність принтів у потрібному форматі підтвердимо в розрахунку.</p>
      <p class="msg">Потрібен план на рік по нагодах? <a href="b2b-team#plan">Порахуйте на сторінці для команди →</a></p>
      <p class="msg"><a href="#sets">Готові набори</a> · <a href="#how">Що буде після запиту</a></p>
    </div>
    <figure class="qph">{img("photo/kolo-3.webp", "Шовкова хустка на плечах поверх бежевого пальта", sizes="(max-width: 960px) 100vw, 45vw")}<figcaption>Хустка «Коло сонця» — один із варіантів до річниці в компанії.</figcaption></figure></div>
  </div></section>''' + facts([
        ("4 запитання", "Кому, нагода, бюджет на людину, кількість"),
        ("3 варіанти", "Економно, оптимально, максимум у бюджеті — обираєте ви"),
        ("19 речей і наборів", "Із каталогу Obiimy: від 700 до 4 800 грн"),
        ("Привітання", "Вашими словами — разом із подарунком"),
    ]) + f'''
  {sets_section(alt=False)}
  {everyone_section(alt=True)}
  {how_section("photo/dotyk-3.webp", "Шовкова хустка з квітковим принтом, великий план", alt=False)}
  {faq_section('<details><summary>Як не помилитися з принтом?</summary><p>Надішліть кілька слів про людину чи команду — запропонуємо принти на вибір. Або подаруйте сертифікат: людина обере сама.</p></details>', alt=True)}
  {proof_section(alt=False)}
  {request_section("f-quiz", "Підбір подарунка для команди", "Отримати добірку й розрахунок", "Залиште контакти й дату, до якої потрібні подарунки. Підбір додається до запиту одним натиском.", "top")}
  ''' + script("f-quiz", js)
    return dict(slug="b2b-team-quiz", skin="studio", bar=BAR, title="Підбір подарунка для команди за хвилину — Obiimy",
                desc="Підбір подарунка співробітникам: кому, нагода, бюджет на людину, кількість. Три варіанти з каталогу Obiimy від 700 до 4 800 грн і сума одразу.",
                og="photo/probudzhennia-1.webp", nav=[("Підбір", "top"), ("Набори", "sets"), ("Для всіх", "all"), ("Після запиту", "how"), ("Питання", "faq")],
                cta="Запит", sticky="Підбір подарунка · від 700 грн", body=body.replace('<section class="hero tool">', '<section class="hero tool" id="top">', 1))

# ─────────────────────────────────────────────────────────────── 3. the gift with the words from the company (Journal)
CARDS = [  # occasion, label, greeting — our examples, the customer writes their own
    ("first", "Перший день", "Ласкаво просимо до команди.\nРаді, що ви з нами."),
    ("trial", "Випробувальний", "Три місяці позаду.\nРаді, що ми разом."),
    ("bday", "День народження", "З днем народження!\nДякуємо, що ви з нами."),
    ("years", "Річниця в компанії", "П’ять років разом.\nДякуємо за кожен із них."),
    ("up", "Підвищення", "Вітаємо з новою роллю.\nВи на своєму місці."),
    ("team", "Перемога команди", "Проєкт закрито.\nЦе зробили ви."),
    ("care", "Підтримка", "Бережіть себе.\nМи поруч."),
    ("bye", "Прощання", "Дякуємо за все, що зробили разом.\nНехай далі буде добре."),
]
CARD_GIFTS = ["scr", "twscr", "tw", "tw44", "h65", "three", "mask", "pil", "book", "cert2"]

def card():
    g0 = CAT["twscr"]; t0 = dict((k, t) for k, _l, t in CARDS)["bday"]
    opts = "".join(opt(CAT[k], k == "twscr") for k in CARD_GIFTS)
    opts2 = "".join(opt(CAT[k], k == "cert2") for k in CARD_GIFTS if CAT[k]["neutral"])
    js = """
    var T = __T__, G = __G__, L = __L__, ta = document.getElementById('c-text'), sg = document.getElementById('c-sign'), gift = document.getElementById('c-gift'), gift2 = document.getElementById('c-gift2'), people = document.getElementById('c-people'), neu = document.getElementById('c-neu');
    function parts() {
      var n = int(people, 1), m = Math.min(n, int(neu, 0)), g = G[gift.value], g2 = G[gift2.value];
      if (!m || g2.k === g.k) return [{ q: n, c: g }];
      return [{ q: n - m, c: g }, { q: m, c: g2 }].filter(function (x) { return x.q > 0; });
    }
    function sum() { return parts().reduce(function (t, x) { return t + x.q * x.c.p; }, 0); }
    function occ() { return document.querySelector('input[name=cocc]:checked').value; }
    function isTpl(v) { for (var k in T) if (T[k] === v) return true; return v.trim() === ''; }
    function clean() { var l = ta.value.split('\\n'); if (l.length > 6) ta.value = l.slice(0, 5).concat(l.slice(5).join(' ')).join('\\n'); }
    function draw() {
      clean();
      var g = G[gift.value], n = int(people, 1), long = ta.value.length > 80 || ta.value.split('\\n').length > 3;
      document.getElementById('c-g2').classList.toggle('dim', !int(neu, 0)); gift2.disabled = !int(neu, 0);
      ['cv', 'hv'].forEach(function (p) {
        document.getElementById(p + '-text').textContent = ta.value || ' ';
        document.getElementById(p + '-sign').textContent = sg.value;
        document.getElementById(p + '-paper').classList.toggle('long', long);
        var im = document.getElementById(p + '-img'); if (p === 'cv' && im.getAttribute('src') !== g.ph) { im.removeAttribute('srcset'); im.src = g.ph; im.alt = g.n; }
      });
      var ch = ta.value.length; document.getElementById('c-count').textContent = ch + ' ' + pl(ch, 'знак', 'знаки', 'знаків') + ' · радимо до 160 і до 6 рядків';
      document.getElementById('c-back').hidden = ta.value === T[occ()];
      document.getElementById('c-total').textContent = fmt(sum());
      document.getElementById('c-note').textContent = parts().map(function (x) { return x.q + ' × ' + plain(fmt(x.c.p)); }).join(' + ') + ' · роздрібні ціни, без доставки';
      sticky(g.n + ' із привітанням · ' + plain(fmt(sum())));
    }
    function text() {
      var t = ta.value.trim().replace(/\\n/g, ' '), n = int(people, 1), m = Math.min(n, int(neu, 0));
      return ['Нагода: ' + L[occ()] + ' · людей: ' + n + (m ? ', із них не носять аксесуари: ' + m : '')]
        .concat(parts().map(function (x) { return '— ' + x.c.n + ': ' + x.q + ' × ' + plain(fmt(x.c.p)) + ' = ' + plain(fmt(x.q * x.c.p)); }),
                ['Разом: ' + plain(fmt(sum())) + ' (роздрібні ціни, без доставки)', 'Текст привітання: ' + (t ? t + (sg.value ? ' ' + sg.value : '') : 'узгодимо окремо')]);
    }
    [].forEach.call(document.querySelectorAll('input[name=cocc]'), function (r) { r.addEventListener('change', function () { if (isTpl(ta.value)) ta.value = T[occ()]; draw(); }); });
    [ta, sg, people, neu].forEach(function (e) { e.addEventListener('input', draw); }); gift.addEventListener('change', draw); gift2.addEventListener('change', draw);
    document.getElementById('c-back').addEventListener('click', function () { ta.value = T[occ()]; draw(); ta.focus(); });
    ta.value = T[occ()]; draw();
    document.getElementById('c-send').addEventListener('click', function () { put(text(), int(people, 1), G[gift.value].n + ' із привітанням · ' + fmt(sum())); });
    document.getElementById('c-copy').addEventListener('click', function () { copyText(text().join('\\n'), this); });
    """.replace("__T__", J({k: t for k, _l, t in CARDS})).replace("__L__", J({k: l for k, l, _t in CARDS})).replace("__G__", J({k: CAT[k] for k in CARD_GIFTS}))
    def paper(p, photo=None):
        shot = img(photo, "Шовкова хустка на плечі поверх білого пальта", sizes="(max-width: 960px) 100vw, 45vw", lazy=False, eager_priority=True, extra=f'id="{p}-img"') if photo else f'<img id="{p}-img" src="{g0["ph"]}" alt="{g0["n"]}" width="900" height="900">'
        return (f'<div class="shot">{shot}'
                          f'<div class="paper" id="{p}-paper"><img src="brand/logo-ink-480.webp" alt="Obiimy" width="85" height="18"><p class="t" id="{p}-text">{t0}</p><p class="s" id="{p}-sign">— ваша команда</p></div></div>')
    body = f'''
  <section class="hero h1-sm"><div class="wrap">
    <div>
      <p class="eyebrow">Для HR і керівників · подарунок із привітанням</p>
      <h1 style="margin-top:14px">Шовковий подарунок співробітнику — з привітанням вашими словами</h1>
      <p class="lead">Ви обираєте річ і пишете привітання — ми додаємо його до подарунка й відправляємо. Приклади тексту для восьми нагод уже готові: змініть під себе.</p>
      <div class="cta"><a class="btn btn-gold" href="#words">Обрати подарунок і написати привітання</a><a class="btn btn-line" href="#sets">Готові набори</a></div>
      <p class="fine">{SAMPLE} Або одразу: <a href="{PHONE_HREF}">{PHONE}</a></p>
    </div>
    <figure class="pv" style="margin-bottom:6%">{paper("hv", "photo/mizh-2.webp")}<figcaption class="fine" style="margin-top:34px">Привітання — ваш текст, підпис — ваш.</figcaption></figure>
  </div></section>''' + facts([
        ("Річ + слова", "Подарунок із каталогу Obiimy та привітання від компанії"),
        ("8 нагод", "Від першого дня до прощання — приклади тексту для кожної"),
        ("700–4 800 грн", "Роздрібні ціни речей і наборів"),
        ("Для всієї команди", "Є речі, що підходять усім: маска, закладка, сертифікат"),
    ]) + f'''

  <section class="block" id="words"><div class="wrap">
    <div class="head"><p class="eyebrow">Привітання</p><h2>Оберіть подарунок і напишіть, що хочете сказати</h2><p class="sub">Оберіть нагоду — підставимо приклад тексту. Змініть його, додайте підпис і оберіть річ.</p></div>
    <div class="cardlab">
      <div class="a">
        <fieldset class="q"><legend>Нагода</legend>{chips("cocc", [(k, l) for k, l, _t in CARDS], "bday")}</fieldset>
        <div class="q"><label><span class="l">Текст привітання</span><textarea id="c-text" maxlength="240" rows="4" aria-describedby="c-count"></textarea></label>
          <p class="count"><span id="c-count"></span><button type="button" id="c-back" hidden>Повернути приклад</button></p></div>
      </div>
      <figure class="pv">{paper("cv")}
        <figcaption>Так звучить текст поруч із подарунком — це не макет. Оформлення привітання узгодимо у відповідь на запит. Фото — приклад принта.</figcaption></figure>
      <div class="b">
        <div class="q"><label><span class="l">Підпис</span><input id="c-sign" type="text" maxlength="40" value="— ваша команда"></label></div>
        <div class="q"><label><span class="l">Подарунок</span><select id="c-gift">{opts}</select></label></div>
        <div class="q team" style="margin-bottom:24px"><label class="p" for="c-people"><span class="l">Скільки людей?</span><input id="c-people" type="number" min="1" inputmode="numeric" value="20"></label>{split_field("c-neu", 8)}</div>
        <div class="q" id="c-g2"><label><span class="l">Їм — річ, що підходить усім</span><select id="c-gift2">{opts2}</select></label></div>
        <div class="res"><div class="fig" style="border:0;padding:0" aria-live="polite"><b id="c-total" class="num"></b><span id="c-note"></span></div>
          <div class="acts"><a class="btn btn-gold" href="#request" id="c-send" role="button">Надіслати на розрахунок</a><button class="btn btn-line btn-sm" type="button" id="c-copy">Скопіювати</button></div></div>
      </div>
    </div>
  </div></section>
  {sets_section(alt=True)}
  {everyone_section(alt=False)}
  {how_section("photo/makiv-1.webp", "Шовкова хустка, зав’язана поверх білого жакета", alt=True)}
  {faq_section('<details><summary>Чи може текст бути різним для кожної людини?</summary><p>Надішліть тексти разом зі списком — у розрахунку підтвердимо, як це оформити.</p></details>', alt=False)}
  {proof_section(alt=True)}
  {request_section("f-card", "Подарунок із привітанням для команди", "Отримати добірку й розрахунок", "Залиште контакти й дату, до якої потрібні подарунки. Нагода, річ і текст привітання додаються до запиту одним натиском.", "words", alt=False)}
  ''' + script("f-card", js)
    return dict(slug="b2b-team-card", skin="journal", bar=BAR, title="Шовковий подарунок співробітнику з привітанням від компанії — Obiimy",
                desc="Подарунок співробітникам із привітанням вашими словами: приклади тексту для восьми нагод, речі й набори Obiimy від 700 до 4 800 грн.",
                og="photo/mizh-2.webp", nav=[("Привітання", "words"), ("Набори", "sets"), ("Для всіх", "all"), ("Після запиту", "how"), ("Питання", "faq")],
                cta="Запит", sticky="Подарунок із привітанням · від 700 грн", body=body)

# ─────────────────────────────────────────────────────────────── 4. three example programmes for a year (Maison)
PLANS = [  # id, name, who, [(occasion, silk item, item that suits everyone)]
    ("base", "«Знак уваги»", "Один подарунок на рік кожному.", [("День народження", "scr", "book")]),
    ("team", "«Команда»", "Два подарунки на рік кожному.", [("День народження", "tw", "cert15"), ("Перемога команди", "scr", "book")]),
    ("plus", "«Визнання»", "Два подарунки на рік: до дня народження й до річниці в компанії.", [("День народження", "twscr", "cert2"), ("Річниця в компанії", "h65", "mask")]),
]
KEY_GIFTS = ["tw44", "mask", "song", "cert4", "pil", "h88", "three"]
SHORT = {"scr": "шовкова резинка", "book": "закладка для книги", "tw": "твіллі", "cert15": "сертифікат на 1 500 грн", "twscr": "набір «твіллі та резинка»", "cert2": "сертифікат на 2 000 грн", "h65": "хустка 65 × 65", "mask": "маска для сну"}

def plans():
    tiers = ""
    for pid, name, who, rows in PLANS:
        s = sum(CAT[a]["p"] for _o, a, _b in rows); u = sum(CAT[b]["p"] for _o, _a, b in rows)
        lis = "".join(f'<li>{img(CAT[a]["ph"], "", sizes="72px")}<div><b>{o}</b><span>{sp(a)} · для всіх: {sp(b)}</span></div></li>' for o, a, b in rows)
        rng = price(s) if s == u else f"{min(s, u):,}".replace(",", " ") + "–" + price(max(s, u))
        tiers += (f'<label class="tier"><input type="radio" name="plan" value="{pid}" data-s="{s}" data-u="{u}" data-n="{name}"{" checked" if pid == "team" else ""}>'
                  f'<h3>{name}</h3><span class="pp"><b>{rng}</b></span><p class="who">{who}</p><ul>{lis}</ul></label>')
    kopts = '<option value="">Не потрібно</option>' + "".join(opt(CAT[k], k == "tw44") for k in KEY_GIFTS)
    js = """
    var G = __G__, people = document.getElementById('p-people'), neu = document.getElementById('p-neu'), kn = document.getElementById('p-key'), kg = document.getElementById('p-gift'), st = {};
    function cur() { return document.querySelector('input[name=plan]:checked'); }
    function calc() {
      var n = int(people, 1), m = int(neu, 0), k = int(kn, 0), warn = [];
      if (!people.value.trim()) warn.push('Вкажіть, скільки людей у команді.');
      else if (m > n || k > n) warn.push('Людей у команді менше, ніж у полях нижче, — рахуємо для ' + n + '.');
      m = Math.min(m, n); k = Math.min(k, n);
      var s = parseInt(cur().dataset.s, 10), u = parseInt(cur().dataset.u, 10), g = G[kg.value];
      var sum = (n - m) * s + m * u + (g ? k * g.p : 0);
      st = { n: n, m: m, k: k, s: s, u: u, g: g, sum: sum, name: cur().dataset.n };
      document.getElementById('p-warn').textContent = warn.join(' ');
      document.getElementById('p-total').textContent = fmt(sum);
      var parts = []; if (s === u) parts.push(n + ' × ' + plain(fmt(s))); else { if (n - m) parts.push((n - m) + ' × ' + plain(fmt(s))); if (m) parts.push(m + ' × ' + plain(fmt(u))); } if (g && k) parts.push(k + ' × ' + plain(fmt(g.p)));
      document.getElementById('p-note').textContent = parts.join(' + ') + ' · на рік, роздрібні ціни, без доставки';
      sticky(st.name + ' · ' + plain(fmt(sum)) + ' на рік');
    }
    function text() {
      var l = ['Програма на рік ' + st.name + ' · людей у команді: ' + st.n + (st.m ? ', із них не носять аксесуари: ' + st.m : '') + ' (роздрібні ціни obiimy.world, без доставки):'];
      if (st.s === st.u) l.push('— кожному: ' + st.n + ' × ' + plain(fmt(st.s)) + ' = ' + plain(fmt(st.n * st.s)));
      else { if (st.n - st.m) l.push('— шовкові речі: ' + (st.n - st.m) + ' × ' + plain(fmt(st.s)) + ' = ' + plain(fmt((st.n - st.m) * st.s)));
      if (st.m) l.push('— речі для всіх: ' + st.m + ' × ' + plain(fmt(st.u)) + ' = ' + plain(fmt(st.m * st.u))); }
      if (st.g && st.k) l.push('— ключовим людям: ' + st.g.n + ' — ' + st.k + ' × ' + plain(fmt(st.g.p)) + ' = ' + plain(fmt(st.k * st.g.p)));
      l.push('Разом: ' + plain(fmt(st.sum))); return l;
    }
    [].forEach.call(document.querySelectorAll('input[name=plan]'), function (r) { r.addEventListener('change', calc); });
    [people, neu, kn].forEach(function (e) { e.addEventListener('input', calc); }); kg.addEventListener('change', calc); calc();
    document.getElementById('p-send').addEventListener('click', function () { put(text(), st.n, st.name + ' · ' + fmt(st.sum) + ' на рік'); });
    document.getElementById('p-copy').addEventListener('click', function () { copyText(text().join('\\n'), this); });
    """.replace("__G__", J({k: CAT[k] for k in KEY_GIFTS}))
    body = f'''
  <section class="hero h1-sm"><div class="wrap" style="align-items:start">
    <div>
      <p class="eyebrow">Для HR і керівників · програма на рік</p>
      <h1 style="margin-top:14px">Подарунки команді — від 700 грн на людину на рік</h1>
      <p class="lead">Три приклади річної програми з речей каталогу Obiimy. Для кожної нагоди — шовкова річ і річ, що підходить усім. Оберіть рівень і порахуйте суму для своєї команди.</p>
      <div class="cta"><a class="btn btn-gold" href="#calc">Порахувати для команди</a><a class="btn btn-line" href="#sets">Готові набори</a></div>
      <p class="fine">{SAMPLE} Або одразу: <a href="{PHONE_HREF}">{PHONE}</a></p>
    </div>
    <div class="tiers" id="plans" role="radiogroup" aria-label="Програма на рік"><p class="tnote">Ціни — на людину на рік, роздрібні, без доставки</p>{tiers}</div>
  </div></section>

''' + facts([
        ("3 програми", "Приклади на рік: від 700 до 5 400 грн на людину"),
        ("Для всієї команди", "У кожній нагоді є річ, що підходить усім"),
        ("Ключовим людям", "Окремий подарунок понад програму: від 2 700 грн"),
        ("Привітання", "Вашими словами — разом із подарунком"),
    ]) + f'''
  <section class="block alt" id="calc"><div class="wrap grid2 calcwrap">
    <figure class="cph">{img("photo/probudzhennia-2.webp", "Шовкова хустка на плечах", sizes="(max-width: 960px) 100vw, 40vw")}<figcaption>Хустка «Пробудження» — приклад речі до річниці в компанії.</figcaption></figure>
    <div>
    <div class="head" style="margin-bottom:22px"><p class="eyebrow">Розрахунок</p><h2>Порахуйте для своєї команди</h2><p class="sub">Програму оберіть вище. Вкажіть, скільки людей у команді не носять аксесуари, — вони отримають річ, що підходить усім, решта — шовкову.</p></div>
    <div class="calc3">
      <label>Людей у команді<input id="p-people" type="number" min="1" inputmode="numeric" value="40"></label>
      <label>Із них не носять аксесуари<input id="p-neu" type="number" min="0" inputmode="numeric" value="16"><small>Їм — річ, що підходить усім</small></label>
      <label>Ключових людей<input id="p-key" type="number" min="0" inputmode="numeric" value="5"></label>
      <label>Подарунок ключовим людям<select id="p-gift">{kopts}</select></label>
    </div>
    <p class="warn" id="p-warn" aria-live="polite"></p>
    <div class="total"><div class="fig" aria-live="polite"><b id="p-total" class="num"></b><span id="p-note"></span></div>
      <div class="acts"><button class="btn btn-line" type="button" id="p-copy">Скопіювати розрахунок</button><a class="btn btn-gold" href="#request" id="p-send" role="button">Надіслати програму на розрахунок</a></div></div>
    <p class="note">Програми — приклади: нагоди й речі можна замінити. Суми — за роздрібними цінами obiimy.world, без доставки. Точний розрахунок для вашої компанії надішлемо у відповідь на запит.</p>
    </div>
  </div></section>
  {sets_section(alt=False)}
  {everyone_section(alt=True)}
  {how_section("photo/hratsiia-belt.webp", "Шовкова хустка поясом на синьому жакеті", alt=False)}
  {faq_section('<details><summary>Чи можна змінити склад програми?</summary><p>Так. Програми на сторінці — приклади. Замініть річ, додайте нагоду або приберіть — перерахуємо суму.</p></details><details><summary>Що, якщо людина прийшла чи пішла посеред року?</summary><p>Надішліть оновлений список — врахуємо його в наступній відправці.</p></details><details><summary>Як відбувається оплата протягом року?</summary><p>Графік оплати узгодимо разом із розрахунком — напишіть, як зручно вашій бухгалтерії.</p></details>', alt=True)}
  {proof_section(alt=False)}
  {request_section("f-plans", "Річна програма подарунків для команди", "Отримати добірку й розрахунок", "Залиште контакти й дату першої відправки. Обрана програма додається до запиту одним натиском.", "calc")}
  ''' + script("f-plans", js)
    return dict(slug="b2b-team-plans", skin="maison", bar=BAR, title="Річна програма подарунків для команди — Obiimy",
                desc="Три приклади річної програми подарунків співробітникам: від 700 до 5 400 грн на людину на рік, речі для всієї команди, окремі подарунки ключовим людям.",
                og="photo/hratsiia-belt.webp", nav=[("Програми", "plans"), ("Розрахунок", "calc"), ("Набори", "sets"), ("Для всіх", "all"), ("Після запиту", "how"), ("Питання", "faq")],
                cta="Запит", sticky="Програма на рік · від 700 грн на людину", body=body)

def build():
    b2b.CSS += CSS
    for fn in (page, quiz, card, plans):
        p = fn()
        html = typo(bind(b2b.shell(p, p["body"])))
        (b2b.OUT / f"{p['slug']}.html").write_text(html)
        print(p["slug"], len(html) // 1024, "KB")

if __name__ == "__main__":
    build()
