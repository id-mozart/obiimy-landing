#!/usr/bin/env python3
"""Two more B2B pages.
  b2b-sets-gallery  the sets shown four ways on one page: a mosaic with a print switcher, rows by occasion,
                    a set builder from real product photos, a comparison table — with the shared request list
  b2b-team-details  the reasons and the details: silk and print, formats and sizes, collections, packaging, care,
                    greeting, delivery and payment, certificates, the brand — only facts from review/SITE-FACTS.md
Photos are the brand's own; nothing is generated. Prices are retail prices from obiimy.world."""
import importlib.util, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
shop = load("build-b2b-team-shop")
team = shop.team
b2b, img, price, typo, J, hero = team.b2b, team.img, team.price, team.typo, team.J, team.hero
CATALOG, CAT = team.CATALOG, team.CAT
PHONE, PHONE_HREF, MAIL, TG, SHOWROOM, SAMPLE, BAR = team.PHONE, team.PHONE_HREF, team.MAIL, team.TG, team.SHOWROOM, team.SAMPLE, team.BAR

# ─────────────────────────────────────────────────────────────── the set families (site: /podarunkovi-nabory/, review/SITE-FACTS.md)
# k, name, base price, note, what is inside, packaging (only where the facts say so), for whom (our advice), occasions for the filter,
# prints on the site (text for the comparison), prints with photos [(slug, name, photo, price)]
FAM = [
    dict(k="tw44", n="Твіллі та хустка 44 × 44", p=3200, note="двосторонні принти й новинка «Золоте світло» — 3 600 грн", inside=["Твіллі 84 × 5", "Хустка 44 × 44"], box="", who="Ключовим людям · до річниці", occ=["bday", "key"],
         site="18 принтів, з них 6 двосторонніх", prints=[("vpevnenist", "Впевненість", "img/sets/tw44-vpevnenist.webp", 3200), ("zolote", "Золоте світло, новинка", "img/sets/tw44-zolote.webp", 3600), ("hratsiia", "Грація", "img/sets/tw44-hratsiia.webp", 3200), ("natkhnennia", "Натхнення", "img/sets/tw44-natkhnennia.webp", 3200),
                 ("balans", "Баланс", "img/sets/tw44-balans.webp", 3200), ("vyr", "Вир почуттів", "img/sets/tw44-vyr.webp", 3200), ("dotyk", "Сміливий дотик", "img/sets/tw44-smilyvyi-dotyk.webp", 3200), ("probudzhennia", "Пробудження, двосторонній", "img/sets/tw44-probudzhennia.webp", 3600), ("nizhnist", "Ніжність, двосторонній", "img/sets/tw44-nizhnist.webp", 3600)]),
    dict(k="twscr", n="Твіллі та резинка", p=2200, note="довга твіллі 140 × 5 — 2 700 грн", inside=["Твіллі 84 × 5", "Шовкова резинка"], box="святкова коробка", who="Хто носить аксесуари · до дня народження", occ=["bday"],
         site="10 принтів, з них 2 — з твіллі 140 × 5", prints=[("makiv", "Маків цвіт", "img/sets/twscr-makiv.webp", 2200), ("prystrast", "Пристрасть", "img/sets/twscr-prystrast.webp", 2200), ("litnie", "Літнє поле", "img/sets/twscr-litnie-pole.webp", 2200), ("enerhiia", "Енергія", "img/sets/twscr-enerhiia.webp", 2200), ("smilyvist", "Сміливість", "img/sets/twscr-smilyvist.webp", 2200), ("vinochok", "Літній віночок, 140 × 5", "img/sets/twscr-vinochok140.webp", 2700)]),
    dict(k="maskscr", n="Маска для сну та резинка", p=3100, note="", inside=["Маска для сну", "Шовкова резинка"], box="", who="Про відпочинок · підтримка, відпустка", occ=["bday", "rest"],
         site="8 принтів", prints=[("litnie", "Літнє поле", "img/sets/maskscr-litnie-pole.webp", 3100), ("enerhiia", "Енергія", "img/sets/maskscr-enerhiia.webp", 3100), ("sertse", "Серцебиття", "img/sets/maskscr-sertsebyttia.webp", 3100)]),
    dict(k="song", n="Маска, закладка й резинка", p=3600, note="колекція «Співоча душа»", inside=["Маска для сну", "Закладка для книги", "Шовкова резинка"], box="", who="Подарунок із сенсом · частина коштів — на гнізда для сиворакші", occ=["key", "rest"],
         site="2 принти", prints=[("pidnesennia", "Піднесення", "img/sets/sleep-pidnesennia.webp", 3600), ("melodiia", "Мелодія двох", "img/sets/sleep-melodiia.webp", 3600)]),
    dict(k="three", n="Три твіллі на вибір", p=4800, note="принти можна обрати різні", inside=["Три твіллі 84 × 5"], box="святкове пакування", who="Керівникам · до вагомої нагоди", occ=["key"],
         site="три принти на вибір із каталогу твіллі", prints=[("three", "Три принти на вибір", "img/sets/three-twilly.webp", 4800)]),
    dict(k="masks2", n="Дві маски «Серцебиття»", p=4200, note="червона та чорна", inside=["Дві маски для сну"], box="", who="Для двох · до вагомої нагоди", occ=["all", "rest"],
         site="червона й чорна", prints=[("sertse", "Серцебиття", "img/sets/masks-sertsebyttia.webp", 4200)]),
    dict(k="scrset", n="Три резинки", p=1800, note="zero waste: 3 шт. — 1 250 грн, 5 шт. — 2 000 грн", inside=["Три шовкові резинки"], box="", who="Невеликий знак уваги", occ=["bday"],
         site="варіанти: 3 шт., zero waste 3 і 5 шт.", prints=[("scr3", "Три резинки", "img/sets/scr3.webp", 1800), ("zero5", "Zero waste, 5 шт.", "img/sets/scr5-zero.webp", 2000)]),
    dict(k="pil", n="Наволочка 50 × 70", p=4200, note="з принтом — 5 700 грн", inside=["Шовкова наволочка"], box="", who="Для дому · підходить усім", occ=["all", "key", "rest"],
         site="3 однотонні, 2 з принтом", prints=[("tuman", "Туман", "img/sets/pillow-tuman.webp", 4200), ("khmara", "Хмара", "img/sets/pillow-khmara.webp", 4200), ("kapuchyno", "Капучино", "img/sets/pillow-kapuchyno.webp", 4200), ("enerhiia", "Енергія, з принтом", "img/sets/pillow-enerhiia.webp", 5700), ("shchyri", "Щирі почуття, з принтом", "img/sets/pillow-shchyri.webp", 5700)]),
]
NEUTRAL = {"masks2", "pil"}
OCC = [("", "Усі набори"), ("bday", "До дня народження"), ("key", "Ключовим людям"), ("all", "Для всіх у команді"), ("rest", "Про відпочинок")]
def vkey(f, slug): return f'{f["k"]}-{slug}'
def vname(f, n): return f'{f["n"]} — «{n}»' if len(f["prints"]) > 1 else f["n"]
# the set builder: catalogue key, label, photo; ready sets with the same content
BUILD = [("tw", "Твіллі 84 × 5", "img/twilly-zolote.webp"), ("scr", "Шовкова резинка", "img/scrunchie-pole.webp"), ("h44", "Хустка 44 × 44 двостороння", "img/pidnesennia.webp"),
         ("h65", "Хустка 65 × 65", "img/kolo-sontsia.webp"), ("mask", "Маска для сну", "img/mask-svoboda.webp"), ("book", "Закладка для книги", "img/sets/bookmark-melodiia.webp")]
READY = [(["scr", "tw"], "twscr"), (["h44", "tw"], "tw44"), (["mask", "scr"], "maskscr"), (["book", "mask", "scr"], "song")]

CSS = """
  .hero .quad { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .hero .quad a { position: relative; display: block; text-decoration: none; color: var(--ink); }
  .hero .quad img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: var(--radius); background: #fff; }
  .hero .quad span { position: absolute; left: 8px; bottom: 8px; right: 8px; background: color-mix(in srgb, var(--card) 92%, transparent); padding: 6px 10px; border-radius: 999px; font-size: .8rem; line-height: 1.3; width: fit-content; max-width: calc(100% - 16px); }
  .hero .quad span b { white-space: nowrap; font-variant-numeric: lining-nums; }
  .occf { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 18px; }
  .mosaic { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 14px; }
  .fam { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; display: flex; flex-direction: column; grid-column: span 2; }
  .fam[hidden] { display: none; }
  .fam.big { grid-column: 1 / -1; display: grid; grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); }
  .fam.big .ph { aspect-ratio: 16 / 11; } .fam.big .in { padding: clamp(18px, 3vw, 36px); align-content: center; } .fam.big h3 { font-size: clamp(1.6rem, 2.6vw, 2.2rem); }
  .mosaic:not(.filtered) .fam.tail { grid-column: span 3; } .mosaic:not(.filtered) .fam.tail .ph { aspect-ratio: 16 / 10; }
  .mosaic.filtered .fam.big { grid-column: span 2; display: flex; } .mosaic.filtered .fam.big .ph { aspect-ratio: 1; } .mosaic.filtered .fam.big .in { padding: 14px 16px 16px; } .mosaic.filtered .fam.big h3 { font-size: 1.2rem; }
  .fam .ph { position: relative; aspect-ratio: 1; background: #fff; overflow: hidden; }
  .fam .ph img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .fam .in { padding: 14px 16px 16px; display: flex; flex-direction: column; gap: 10px; flex: 1; }
  .fam .for { font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: var(--ink3); font-weight: 600; }
  .fam h3 { font-size: 1.2rem; }
  .fam .inside { display: flex; flex-wrap: wrap; gap: 6px; } .fam .inside span { font-size: .78rem; border: 1px solid var(--line); border-radius: 999px; padding: 4px 10px; color: var(--ink2); }
  .fam .inside span.box { border-style: dashed; }
  .pr-l { font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: var(--ink3); font-weight: 600; }
  .sw { display: flex; flex-wrap: wrap; gap: 6px; }
  .sw button { font: inherit; font-size: .8rem; min-height: 34px; padding: 5px 11px; border-radius: 999px; border: 1px solid var(--line); background: transparent; color: var(--ink); cursor: pointer; }
  .sw button[aria-pressed="true"] { background: var(--ink); color: var(--bg); border-color: var(--ink); }
  .fam .pr { margin-top: auto; padding-top: 8px; display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap; }
  .fam .pr b { font-family: var(--display); font-weight: 400; font-size: 1.35rem; white-space: nowrap; } .fam .pr small { display: block; color: var(--ink2); font-size: .76rem; }
  .more-card { grid-column: span 3; display: grid; align-content: center; gap: 10px; padding: 24px; border: 1px dashed var(--line); border-radius: var(--radius); background: transparent; text-decoration: none; color: var(--ink); }
  .more-card b { font-family: var(--display); font-weight: 400; font-size: 1.4rem; } .more-card span { color: var(--ink2); font-size: .9rem; }
  .more-card .mini { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 6px; } .more-card .mini img { width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: calc(var(--radius) - 2px); background: #fff; }
  .builder { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: clamp(20px, 4vw, 56px); align-items: start; }
  .picks { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .pick { position: relative; display: grid; grid-template-columns: 64px minmax(0, 1fr); gap: 12px; align-items: center; border: 1px solid var(--line); border-radius: var(--radius); padding: 10px; background: var(--card); cursor: pointer; }
  .pick input { position: absolute; inset: 0; width: 100%; height: 100%; min-height: 0; margin: 0; padding: 0; opacity: 0; cursor: pointer; }
  .pick:has(input:checked) { border-color: var(--ink); box-shadow: inset 0 0 0 1px var(--ink); } .pick:has(input:focus-visible) { outline: 2px solid var(--ink); outline-offset: 3px; }
  .pick img { width: 64px; height: 64px; object-fit: cover; border-radius: calc(var(--radius) - 2px); background: #fff; }
  .pick b { display: block; font-family: var(--display); font-weight: 400; font-size: 1.05rem; line-height: 1.15; } .pick span { color: var(--ink2); font-size: .82rem; }
  .comp { border: 1px solid var(--line); border-radius: var(--radius); background: var(--card); padding: 16px; }
  .comp .tiles { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; min-height: 120px; }
  .comp .tiles img { width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: calc(var(--radius) - 2px); background: #fff; }
  .comp .empty { grid-column: 1 / -1; display: grid; place-items: center; color: var(--ink2); font-size: .95rem; text-align: center; padding: 30px 10px; }
  .ready { display: grid; grid-template-columns: 96px minmax(0, 1fr); gap: 14px; align-items: center; margin-top: 14px; padding: 12px; border-radius: var(--radius); background: color-mix(in srgb, var(--gold) 16%, var(--card)); }
  .ready img { width: 96px; height: 96px; object-fit: cover; border-radius: calc(var(--radius) - 2px); background: #fff; } .ready b { font-family: var(--display); font-weight: 400; font-size: 1.1rem; }
  .bsum { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: end; gap: 12px 24px; margin-top: 16px; }
  .bsum b { font-family: var(--display); font-weight: 400; font-size: clamp(1.8rem, 3.2vw, 2.6rem); line-height: 1; } .bsum span { display: block; color: var(--ink2); font-size: .88rem; margin-top: 4px; }
  .cmp { width: 100%; border-collapse: collapse; font-size: .92rem; }
  .cmp th { text-align: left; font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; color: var(--ink3); font-weight: 600; padding: 8px 10px 10px 0; border-bottom: 1px solid var(--ink); vertical-align: bottom; }
  .cmp td { padding: 12px 10px 12px 0; border-bottom: 1px solid var(--line); vertical-align: middle; }
  .cmp td.ic { width: 76px; min-width: 76px; } .cmp td.ic img { width: 64px; height: 64px; min-width: 64px; object-fit: cover; border-radius: calc(var(--radius) - 2px); background: #fff; }
  .cmp .n, .cmp td.p { font-family: var(--display); font-size: 1.1rem; } .cmp th.n { padding: 12px 10px 12px 0; border-bottom: 1px solid var(--line); vertical-align: middle; letter-spacing: 0; text-transform: none; color: var(--ink); } .cmp th.n small { display: block; color: var(--ink2); font-size: .8rem; font-family: var(--body); } .cmp td.p { white-space: nowrap; } .cmp td small { display: block; color: var(--ink2); font-size: .8rem; font-family: var(--body); }
  .det { display: grid; grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); gap: clamp(24px, 4vw, 64px); align-items: start; }
  .det.flip > :first-child { order: 2; } .det.solo { grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); }
  .det h2 { font-size: clamp(1.6rem, 2.6vw, 2.2rem); margin-top: 8px; }
  .det .txt > p { color: var(--ink2); margin-top: 10px; max-width: 40em; }
  .kv { width: 100%; border-collapse: collapse; font-size: .95rem; margin-top: 18px; }
  .kv th { text-align: left; font-weight: 600; padding: 10px 12px 10px 0; border-bottom: 1px solid var(--line); width: 42%; vertical-align: top; }
  .kv td { padding: 10px 0; border-bottom: 1px solid var(--line); color: var(--ink2); vertical-align: top; } .kv td b { color: var(--ink); font-weight: 600; white-space: nowrap; font-variant-numeric: lining-nums tabular-nums; }
  .det { align-items: center; } .det.solo { align-items: start; } .det figure { margin: 0; } .det figure img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: var(--radius); } .det figcaption { color: var(--ink2); font-size: .82rem; margin-top: 8px; }
  .acc { margin: 16px 0 0; padding: 16px 18px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--card); } .acc b { display: block; margin-bottom: 6px; }
  .acc ul { margin: 0; padding-left: 18px; color: var(--ink2); font-size: .92rem; display: grid; gap: 4px; }
  .coll { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; }
  .coll div { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; } .coll img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; background: #fff; }
  .coll p { padding: 12px 14px 14px; margin: 0; } .coll b { font-family: var(--display); font-weight: 400; font-size: 1.15rem; display: block; margin-bottom: 4px; } .coll span { color: var(--ink2); font-size: .84rem; }
  .greet { display: grid; grid-template-columns: 1fr 1fr; gap: 16px 22px; margin-top: 18px; }
  .greet .paper { position: static; width: auto; max-height: none; transform: rotate(-1.5deg); padding: 20px 20px 16px; }
  .greet .paper:nth-child(2n) { transform: rotate(1deg); } .greet .paper .t { font-size: 1.15rem; }
  .greet .paper small { display: block; font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: #8A8480; margin-bottom: 8px; }
  .toc { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; } .toc a { font-size: .86rem; font-weight: 600; text-decoration: none; border: 1px solid var(--line); border-radius: 999px; padding: 8px 14px; color: var(--ink); background: var(--card); }
  @media (max-width: 960px) { .mosaic { grid-template-columns: 1fr 1fr; } .fam, .fam.big, .mosaic:not(.filtered) .fam.tail, .more-card { grid-column: span 1; } .fam.big { display: flex; } .fam.big .ph { aspect-ratio: 1; }
    .builder, .det, .det.solo { grid-template-columns: 1fr; } .det.flip > :first-child { order: 0; } .coll { grid-template-columns: 1fr 1fr; } .hero .quad { grid-template-columns: 1fr 1fr; order: 1; margin-top: 4px; } .hero .quad img { aspect-ratio: 4 / 3; } }
  .sw .more-sw { display: none; }
  @media (max-width: 640px) {
    .fam .in > .for { order: 0; } .fam .in > h3 { order: 1; } .fam .in > .pr { order: 2; margin-top: 0; padding-top: 0; } .fam .in > .inside { order: 3; } .fam .in > .pr-l { order: 4; } .fam .in > .sw { order: 5; }
    .sw .more-sw { display: inline-flex; } .sw:not(.open) button:nth-child(n+5):not(.more-sw) { display: none; }
    .hero .quad img { aspect-ratio: 1; } .hero .quad span { font-size: .72rem; padding: 4px 8px; left: 6px; bottom: 6px; } .hero .lead, .hero .toc { display: none; } .fam .ph, .fam.big .ph { aspect-ratio: 4 / 3; }
    .cmp td[data-label]::before { content: attr(data-label); display: block; font-size: .68rem; letter-spacing: .12em; text-transform: uppercase; color: var(--ink3); font-weight: 600; margin-top: 4px; }
    .toc { flex-wrap: nowrap; overflow-x: auto; padding-bottom: 4px; } .toc a { flex: none; }
  }
  @media (max-width: 640px) { .mosaic { grid-template-columns: 1fr; } .picks { grid-template-columns: 1fr; } .coll { grid-template-columns: 1fr; } .greet { grid-template-columns: 1fr; }
    .occf { flex-wrap: nowrap; overflow-x: auto; padding-bottom: 4px; } .occf label { flex: none; }
    .cmp thead { display: none; } .cmp, .cmp tbody, .cmp tr, .cmp td { display: block; } .cmp tr { border-bottom: 1px solid var(--line); padding: 10px 0; display: grid; grid-template-columns: 64px minmax(0, 1fr); gap: 4px 12px; } .cmp td, .cmp th.n { border: 0; padding: 0; display: block; } .cmp td.ic { grid-row: 1 / span 5; width: auto; min-width: 0; } .cmp td.p { white-space: normal; } }
"""

def sw_label(f):
    n = f["site"].split(" ")[0]
    if f["k"] in ("pil", "scrset") or not n.isdigit(): return "Варіант"
    return f'{n} принтів · {len(f["prints"])} на фото' if int(n) > len(f["prints"]) else "Принт"

def fam_card(f, cls=""):
    p0 = f["prints"][0]
    sw = "".join(f'<button type="button" data-ph="{ph}" data-name="{n}" data-p="{pp}" data-key="{vkey(f, slug)}" aria-pressed="{"true" if i == 0 else "false"}">{n}</button>' for i, (slug, n, ph, pp) in enumerate(f["prints"])) if len(f["prints"]) > 1 else ""
    if len(f["prints"]) > 4: sw += f'<button type="button" class="more-sw" aria-expanded="false">+ ще {len(f["prints"]) - 4}</button>'
    box = f'<span class="box">{f["box"]}</span>' if f["box"] else ""
    return (f'<div class="fam {cls}" id="fam-{f["k"]}" data-occ="{" ".join(f["occ"])}"><div class="ph">{img(p0[2], vname(f, p0[1]), sizes="(max-width: 640px) 100vw, 60vw")}</div>'
            f'<div class="in"><p class="for">{f["who"]}</p><h3>{f["n"]}</h3><div class="inside">{"".join(f"<span>{x}</span>" for x in f["inside"])}{box}</div>'
            + (f'<p class="pr-l">{sw_label(f)}</p><div class="sw" role="group" aria-label="{sw_label(f)}: {f["n"]}">{sw}</div>' if sw else "")
            + f'<div class="pr"><div><b class="num" data-k="pp">{price(p0[3])}</b><small>{"роздрібна ціна · " + f["note"] if f["note"] else "роздрібна ціна"}</small></div>'
            f'<button type="button" class="add" data-add="{vkey(f, p0[0])}" aria-label="До списку: {f["n"]}">+ До списку</button></div></div></div>')

def gallery():
    fams = {f["k"]: f for f in FAM}
    cards = [fam_card(f, "big" if i == 0 else ("tail" if i >= len(FAM) - 1 else "")) for i, f in enumerate(FAM)]
    mosaic = "".join(cards) + '<a class="more-card" href="https://obiimy.world/podarunkovi-nabory/"><b>Усі 45 наборів — на obiimy.world →</b><span>Тут — вісім родин, які ми радимо для команди. Інші набори теж можна додати до запиту: напишіть назву в коментарі.</span><span class="mini">' + "".join(img(ph, "", sizes="120px") for ph in ("img/set-natkhnennia.webp", "img/set-zolote.webp", "img/sets/twscr-prystrast.webp")) + '</span></a>'
    occf = shop.chips("occ", OCC, "")
    picks = "".join(f'<label class="pick"><input type="checkbox" name="bk" value="{k}"{" checked" if k in ("tw", "scr") else ""}>{img(ph, CAT[k]["n"], sizes="64px")}<span><b>{lab}</b><span>{price(CAT[k]["p"])}</span></span></label>' for k, lab, ph in BUILD)
    cmp_rows = "".join(f'<tr><td class="ic">{img(f["prints"][0][2], "", sizes="64px")}</td><th scope="row" class="n" style="text-align:left;font-weight:400">{f["n"]}<small>{f["who"]}</small></th><td data-label="Що всередині">{", ".join(f["inside"])}{"<small>" + f["box"] + "</small>" if f["box"] else ""}</td><td data-label="Принти на сайті">{f["site"]}</td><td class="p" data-label="Ціна">{price(f["p"])}<small>{f["note"]}</small></td><td>{fam_btn(f)}</td></tr>' for f in FAM)
    C = {c["k"]: dict(n=c["n"], p=c["p"], all=c["neutral"]) for c in CATALOG}
    for f in FAM:
        for slug, n, _ph, pp in f["prints"]:
            C[vkey(f, slug)] = dict(n=vname(f, n), p=pp, all=f["k"] in NEUTRAL)
    ready = {"+".join(sorted(ks)): dict(key=vkey(fams[fk], fams[fk]["prints"][0][0]), n=fams[fk]["n"], p=fams[fk]["p"], ph=fams[fk]["prints"][0][2], box=fams[fk]["box"] or ("у готовому наборі — хустка з одностороннім друком; двосторонній — 3 600 грн" if fk == "tw44" else "")) for ks, fk in READY}
    js = shop.LIST_JS.replace("__C__", J(C)).replace("__STICKY__", "Набори Obiimy · від 1 800 грн").replace("__TAG__", "undefined") + """
    // the print switcher: photo, price and the list key follow the chosen print
    [].forEach.call(document.querySelectorAll('.sw .more-sw'), function (b) {
      b.addEventListener('click', function () { var sw = b.parentNode; sw.classList.add('open'); b.setAttribute('aria-expanded', 'true'); b.hidden = true; var nx = sw.querySelector('button:nth-child(5)'); if (nx) nx.focus(); });
    });
    [].forEach.call(document.querySelectorAll('.sw button:not(.more-sw)'), function (b) {
      b.addEventListener('click', function () {
        var card = b.closest('.fam'), im = card.querySelector('.ph img'), add = card.querySelector('.add');
        im.removeAttribute('srcset'); im.src = b.dataset.ph; im.alt = C[b.dataset.key].n;
        card.querySelector('[data-k=pp]').textContent = fmt(parseInt(b.dataset.p, 10));
        add.dataset.add = b.dataset.key;
        [].forEach.call(card.querySelectorAll('.sw button:not(.more-sw)'), function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        render();
      });
    });
    // occasion filter over the mosaic
    var mos = document.getElementById('mos');
    [].forEach.call(document.querySelectorAll('input[name=occ]'), function (r) {
      r.addEventListener('change', function () {
        var v = r.value; mos.classList.toggle('filtered', !!v);
        [].forEach.call(mos.querySelectorAll('.fam'), function (c) { c.hidden = !!v && c.dataset.occ.split(' ').indexOf(v) < 0; });
        mos.querySelector('.more-card').hidden = !!v; document.getElementById('occ-note').hidden = v !== 'all';
        var shown = [].filter.call(mos.querySelectorAll('.fam'), function (c) { return !c.hidden; }).length; document.getElementById('occ-cnt').textContent = 'Показано ' + shown + ' із ' + mos.querySelectorAll('.fam').length + ' наборів';
      });
    });
    // the set builder: real photos, the sum of retail prices; a ready set with the same content is shown with its own price
    var READY = __READY__, tiles = document.getElementById('b-tiles'), bsum = document.getElementById('b-sum'), bnote = document.getElementById('b-note'), rbox = document.getElementById('b-ready');
    function build() {
      var ks = [].map.call(document.querySelectorAll('input[name=bk]:checked'), function (i) { return i.value; }), total = 0;
      tiles.textContent = '';
      ks.forEach(function (k) { total += C[k].p; var i = document.createElement('img'); i.src = document.querySelector('input[name=bk][value=' + k + ']').parentNode.querySelector('img').getAttribute('src'); i.alt = C[k].n; tiles.appendChild(i); });
      if (!ks.length) { var e = document.createElement('p'); e.className = 'empty'; e.textContent = 'Позначте речі зліва — побачите склад і суму.'; tiles.appendChild(e); }
      bsum.textContent = fmt(total);
      bnote.textContent = ks.length ? ks.map(function (k) { return C[k].n; }).join(' + ') + ' · роздрібні ціни окремих речей' : '';
      var r = READY[ks.slice().sort().join('+')], btn = document.getElementById('b-add');
      rbox.hidden = !r;
      if (r) {
        rbox.querySelector('img').src = r.ph; rbox.querySelector('img').alt = r.n;
        rbox.querySelector('b').textContent = 'Такий набір уже є готовим — «' + r.n + '», ' + fmt(r.p) + (r.box ? ', ' + r.box : '');
        rbox.querySelector('button').dataset.key = r.key; rbox.querySelector('button').textContent = 'Додати готовий набір — ' + fmt(r.p);
        bsum.textContent = 'Окремими речами — ' + fmt(total); bsum.style.fontSize = '1.2rem';
        btn.className = 'btn btn-line btn-sm'; btn.textContent = 'Додати окремими речами';
      } else { bsum.style.fontSize = ''; btn.className = 'btn btn-gold'; btn.textContent = 'Додати речі до списку'; }
      btn.setAttribute('aria-disabled', ks.length ? 'false' : 'true'); btn.dataset.keys = ks.join(',');
    }
    [].forEach.call(document.querySelectorAll('input[name=bk]'), function (i) { i.addEventListener('change', build); }); build();
    function toList() { document.getElementById('list').scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    document.getElementById('b-add').addEventListener('click', function () { var ks = this.dataset.keys ? this.dataset.keys.split(',') : []; if (!ks.length) return; ks.forEach(function (k) { if (!n(k)) set(k, dflt(k)); }); toList(); });
    rbox.querySelector('button').addEventListener('click', function () { var k = this.dataset.key; if (!n(k)) set(k, dflt(k)); toList(); });
    """.replace("__READY__", J(ready))
    quad = "".join(f'<a href="#fam-{k}">{img(ph, a, sizes="(max-width: 640px) 50vw, 22vw")}<span>{a} · <b>{price(pr)}</b></span></a>' for k, ph, a, pr in [("twscr", "img/sets/twscr-makiv.webp", "Твіллі та резинка", 2200), ("maskscr", "img/sets/maskscr-litnie-pole.webp", "Маска та резинка", 3100), ("three", "img/sets/three-twilly.webp", "Три твіллі", 4800), ("song", "img/sets/sleep-pidnesennia.webp", "Маска, закладка й резинка", 3600)])
    body = f'''
  <section class="hero h1-xs" style="padding-bottom:clamp(12px,2vw,28px)"><div class="wrap" style="align-items:center">
    <div>
      <p class="eyebrow">Для HR і офіс-менеджерів<span class="m-hide"> · подарункові набори</span></p>
      <h1 style="margin-top:14px">Набори Obiimy для команди: вісім родин, принти на вибір, ціни</h1>
      <p class="lead">Оберіть родину й принт — фото й ціна змінюються. Відфільтруйте за нагодою, зберіть свій набір або порівняйте всі поруч. Роздрібні ціни obiimy.world.</p>
      <div class="cta"><a class="btn btn-gold btn-sm" href="#request" data-go>Отримати розрахунок</a><a class="btn btn-line btn-sm" href="#cmp">Порівняти всі</a></div>
      <div class="toc"><a href="#mosaic">Родини й принти</a><a href="#build">Свій набір</a><a href="#cmp">Порівняння</a><a href="b2b-team-details">Переваги й деталі →</a></div>
    </div>
    <div class="quad">{quad}</div>
  </div></section>

  <section class="block" id="mosaic" style="padding-top:clamp(20px,3vw,40px)"><div class="wrap">
    <p class="note" style="margin:0 0 12px">Оберіть принт — фото й ціна змінюються. Фото з obiimy.world; підписи «кому» — наші поради; наявність принта в потрібному форматі підтвердимо в розрахунку.</p>
    <fieldset class="q" style="margin:0"><legend class="sr">Нагода</legend><div class="occf">{occf}</div></fieldset>
    <p class="sr" id="occ-cnt" aria-live="polite">Показано 8 із 8 наборів</p>
    <p class="note" id="occ-note" hidden style="margin:-6px 0 14px">Окремі речі, що підходять усім, — маска для сну, закладка, сертифікат — <a href="b2b-team-main#catalog">у каталозі для команд →</a></p>
    <div class="mosaic" id="mos">{mosaic}</div>
  </div></section>

  <section class="block alt" id="build"><div class="wrap">
    <div class="head" style="margin-bottom:18px"><p class="eyebrow">Свій набір</p><h2>Зберіть набір із окремих речей</h2><p class="sub">Позначте речі — побачите склад і суму за роздрібними цінами. Якщо такий набір уже є готовим, покажемо його й ціну. Пакування для свого набору покажемо на фото в добірці разом із розрахунком.</p></div>
    <div class="builder">
      <div class="picks">{picks}</div>
      <div>
        <div class="comp"><p class="pr-l" style="margin-bottom:10px">Склад набору</p><div class="tiles" id="b-tiles" aria-live="polite"></div></div>
        <div class="ready" id="b-ready" hidden><img src="" alt=""><div><b></b><p style="margin-top:10px"><button type="button" class="btn btn-gold btn-sm" id="b-ready-add">Додати готовий набір</button></p></div></div>
        <div class="bsum"><div><b id="b-sum" class="num">0 грн</b><span id="b-note"></span></div><button type="button" class="btn btn-gold" id="b-add" aria-disabled="true">Додати речі до списку</button></div>
      </div>
    </div>
  </div></section>

  <section class="block" id="cmp"><div class="wrap">
    <div class="head" style="margin-bottom:18px"><p class="eyebrow">Порівняння</p><h2>Вісім родин поруч</h2></div>
    <table class="cmp"><thead><tr><th></th><th>Набір</th><th>Що всередині</th><th>Принти на сайті</th><th>Ціна</th><th></th></tr></thead><tbody>{cmp_rows}</tbody></table>
    <p class="note" style="margin-top:14px">Роздрібні ціни obiimy.world; підписи «кому» — наші поради. Усі 45 наборів — на <a href="https://obiimy.world/podarunkovi-nabory/">obiimy.world</a>; окремі речі з цінами — у <a href="b2b-team-main#catalog">каталозі для команд</a>.</p>
    <div style="margin-top:34px">{shop.listbox("f-gallery", "Список для запиту", "Набори з цієї сторінки збираються тут — з обраним принтом і його ціною.").replace('href="b2b-team#plan"', 'href="b2b-team-main#plan"')}</div>
  </div></section>
  {shop.how_short(alt=True)}
  {team.faq_section(alt=False)}
  {team.proof_section(alt=True)}
  {team.request_section("f-gallery", "Подарункові набори для команди", "Отримати добірку й розрахунок", "Залиште контакти й дату, до якої потрібні подарунки. Список наборів додається до запиту одним натиском.", "list", alt=False)}
  ''' + team.script("f-gallery", js)
    return dict(slug="b2b-sets-gallery", skin="maison", bar=BAR, title="Подарункові набори Obiimy для команди — родини, принти, ціни",
                desc="Вісім родин подарункових наборів Obiimy: перемикач принтів, фільтр за нагодою, свій набір з окремих речей і таблиця порівняння. Роздрібні ціни від 1 800 грн.",
                og="img/sets/tw44-zolote.webp", nav=[("Родини й принти", "mosaic"), ("Свій набір", "build"), ("Порівняння", "cmp"), ("Питання", "faq")],
                cta="Запит", sticky="Набори Obiimy · від 1 800 грн", body=body)

def fam_btn(f):
    return f'<button type="button" class="add" data-add="{vkey(f, f["prints"][0][0])}" aria-label="До списку: {f["n"]}">+ До списку</button>'

# ─────────────────────────────────────────────────────────────── the reasons and the details (facts only)
def det(idn, eyebrow, h2, text, rows, photo=None, alt="", cap="", alt_bg=False, flip=False, extra=""):
    tbl = (f'<table class="kv" aria-labelledby="h-{idn}">' + "".join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows) + "</table>") if rows else ""
    left = f'<div class="txt"><p class="eyebrow">{eyebrow}</p><h2 id="h-{idn}">{h2}</h2>{"".join(f"<p>{t}</p>" for t in text)}{tbl}{extra}</div>'
    right = f'<figure>{img(photo, alt, sizes="(max-width: 960px) 100vw, 40vw")}<figcaption>{cap}</figcaption></figure>' if photo else ""
    cls = "det" + (" flip" if flip and photo else "") + ("" if photo else " solo")
    if not photo:   # text on the left, the table takes the wide right column
        left = f'<div class="txt"><p class="eyebrow">{eyebrow}</p><h2 id="h-{idn}">{h2}</h2>{"".join(f"<p>{t}</p>" for t in text)}{extra}</div>'
        right = f'<div>{tbl}</div>'
    return f'''
  <section class="block{" alt" if alt_bg else ""}" id="{idn}"><div class="wrap {cls}">{left}{right}</div></section>'''

COLL = [
    ("«Співоча душа»", "Піднесення, Мелодія двох, Тиша серця, Коло сонця, Єднання. Присвячена рідкісним птахам: частина коштів — на гнізда для сиворакші.", "img/pidnesennia.webp", "Принт «Піднесення»"),
    ("«Поклик душі»", "Пристрасть, Маків цвіт, Літнє поле, Впевненість, Енергія, Сміливість, Спокуса, Свобода, Захоплення, Ніжність.", "img/litnie-pole.webp", "Принт «Літнє поле»"),
    ("«Пробудження»", "Пробудження, Поцілунок сонця, Вир почуттів, Між нами, Закоханість, Щирі почуття, Соковиті спогади.", "img/probudzhennia.webp", "Принт «Пробудження»"),
    ("«Дика стихія»", "Дика спокуса, З чистого листа, Баланс, Грація, Сміливий дотик, Натхнення, Ранкова кава, Відновлення.", "img/set-natkhnennia.webp", "Набір із принтом «Натхнення»"),
    ("«Соло: шлях до себе»", "Сім принтів в естетиці ретрообкладинок 1940–50-х.", "img/solo-scarf.webp", "Хустка з колекції «Соло», кадр кампанії з obiimy.world"),
]
DETAILS_FAQ_DROP = ["У чому приїдуть подарунки?", "Як доставляєте — і що з колегами за кордоном?", "Оплата й документи для компанії", "Чи однакові речі за розміром?", "Що входить у суму на сторінці?", "Що подарувати чоловікам?", "Чи можна додати логотип компанії?", "Що, якщо із замовленням щось не так?"]

def details():
    cards = "".join(f'<div class="paper"><small>{lab}</small><p class="t">{t.replace(chr(10), "<br>")}</p><p class="s">— ваша команда</p></div>' for k, lab, t in team.CARDS if k in ("first", "years"))
    coll = "".join(f'<div>{img(ph, a, sizes="(max-width: 640px) 100vw, 20vw")}<p><b>{n}</b><span>{t}</span></p></div>' for n, t, ph, a in COLL)
    faq = team.faq_section(alt=True)
    for q in DETAILS_FAQ_DROP:
        faq = re.sub(r"\s*<details><summary>" + re.escape(q) + r"</summary>[\s\S]*?</details>", "", faq)
    body = hero("Для HR і офіс-менеджерів<span class=\"m-hide\"> · переваги й деталі</span>", "Що ви отримуєте: шовк, друк, формати, пакування, доставка",
        "Усе, про що питають перед корпоративним замовленням, — з цифрами з obiimy.world. Чого немає на сайті, уточнимо в розрахунку.",
        "Каталог із цінами", "Набори", "b2b-sets-gallery", SAMPLE,
        "photo/dotyk-3.webp", "Шовкова хустка з квітковим принтом, великий план", "Шовк, ручна обробка краю", cls=" h1-sm", pos="50% 50%", cta1_href="b2b-team-main#catalog") + f'''
  <div class="wrap"><nav class="toc" aria-label="Розділи сторінки" style="margin:-10px 0 10px"><a href="#silk">Шовк і друк</a><a href="#sizes">Формати й ціни</a><a href="#coll">Колекції</a><a href="#pack">Пакування</a><a href="#care">Догляд і розміри</a><a href="#words">Привітання</a><a href="#ship">Доставка й оплата</a><a href="#cert">Сертифікати</a><a href="#brand">Бренд</a></nav></div>
  {det("silk", "Шовк і друк", "100% італійський шовк, авторські принти, зроблено в Україні",
       ["Шовк — італійський, 100% натуральний, преміум-класу. Принти авторські: художниця й засновниця бренду — Світлана Сніжко. Друк — односторонній або двосторонній, край хустки оброблений вручну.", "Виробництво — в Україні. Бренд заснований під час війни й бере участь у благодійних ініціативах на допомогу військовим і постраждалим."],
       [("Матеріал", "100% італійський шовк"), ("Принти", "Авторські, Світлана Сніжко"), ("Друк", "Односторонній і двосторонній (двосторонній — дорожче)"), ("Край", "Ручна обробка"), ("Виробництво", "Україна")],
       "photo/makiv-1.webp", "Шовкова хустка, зав’язана поверх білого жакета", "Хустка поверх жакета.")}
  {det("sizes", "Формати й ціни", "Що є в каталозі — і скільки коштує",
       ["Роздрібні ціни obiimy.world. Умови для вашої кількості — у розрахунку. Двосторонні хустки коштують дорожче за односторонні."],
       [("Хустка 44 × 44", "<b>1 600 грн</b> · двостороння <b>2 400 грн</b>"), ("Хустка 65 × 65", "<b>3 200 грн</b> · двостороння <b>4 800 грн</b>"), ("Хустка 88 × 88", "<b>4 400 грн</b> · двостороння <b>6 600 грн</b>"), ("Твіллі 84 × 5", "<b>1 600 грн</b> · 38 принтів"), ("Твіллі 140 × 5 / 140 × 15", "<b>1 850 грн</b> / <b>2 400 грн</b>"), ("Резинка для волосся", "<b>700 грн</b> · міні <b>500 грн</b>"), ("Маска для сну", "<b>2 700 грн</b> · 15 принтів"), ("Закладка для книги", "<b>800 грн</b>"), ("Наволочка 50 × 70", "<b>4 200 грн</b> однотонна · з принтом <b>5 700 грн</b>"), ("Тюрбан", "<b>3 500 грн</b>"), ("Набори", "<b>1 250–4 800 грн</b> · <a href='b2b-sets-gallery'>вісім родин</a>"), ("Сертифікат", "<b>1 000–4 000 грн</b>")],
       alt_bg=True, extra='<p><a class="btn btn-gold btn-sm" href="b2b-team-main#catalog" style="margin-top:18px">Скласти список у каталозі →</a></p>')}
  <section class="block" id="coll"><div class="wrap">
    <div class="head"><p class="eyebrow">Колекції</p><h2>П’ять колекцій — принти на вибір</h2><p class="sub">Принт для команди можна обрати один на всіх або різні; фото принтів надішлемо в добірці.</p></div>
    <div class="coll">{coll}</div>
  </div></section>
  {det("pack", "Пакування", "Набори — у святковій коробці, окремі речі — в індивідуальному пакуванні",
       ["Набори приїздять у святковій коробці Obiimy — як виглядає саме ваш, покажемо на фото в добірці. Для окремих речей на сайті зазначено «індивідуальне пакування» — як саме виглядає, покажемо на фото в добірці разом із розрахунком.", "Логотип компанії на пакуванні чи речі — напишіть, що саме потрібно: у розрахунку відповімо, чи можемо це зробити."],
       [("Набори", "Святкова коробка Obiimy"), ("Окремі речі", "Індивідуальне пакування · фото в добірці"), ("Логотип компанії", "Уточнимо в розрахунку")],
       "photo/box-gold.jpg", "Набір у святковій коробці Obiimy", "Святкова коробка набору.", alt_bg=True, flip=True)}
  {det("care", "Догляд і розміри", "Що варто знати про шовк",
       ["На сторінках товарів зазначено режим прасування «шовк». Розмір хустки може відрізнятися на 0–2,5 см через ручну обробку краю — це особливість шовку, а не брак."],
       [("Прасування", "Режим «шовк»"), ("Допуск розміру", "0–2,5 см"), ("Обмін і повернення", '<a href="https://obiimy.world/obmin-ta-povernennya/">умови на obiimy.world</a>')])}
  {det("words", "Привітання", "Слова від компанії — разом із подарунком",
       ["Підпис до подарунка — за вашим текстом: один на всіх або свій до кожної нагоди. Оформлення привітання узгодимо у відповідь на запит. Нижче — наші приклади."],
       [("Текст", "Ваш"), ("Різний для кожного", "Так — надішліть разом зі списком"), ("Оформлення", "Узгодимо в розрахунку")],
       alt_bg=True, extra=f'<div class="greet">{cards}</div><p><a class="btn btn-line btn-sm" href="b2b-team-main#words" style="margin-top:18px">Ще приклади →</a></p>')}
  {det("ship", "Доставка й оплата", "Новою поштою — кожному або в офіс",
       ["Відправка Новою поштою по Україні: кожному на відділення чи однією посилкою в офіс — як домовимось. За кордон — за тарифами перевізника; для колег за кордоном найпростіше електронний сертифікат.", "Строки залежать від кількості й наявності принтів: вкажіть дату в запиті — відповімо, чи встигаємо. Форму оплати й документи для компанії підтвердимо разом із розрахунком."],
       [("По Україні", "Нова пошта · кожному або в офіс"), ("За кордон", "За тарифами перевізника"), ("Строки", "Відповімо на вашу дату"), ("Оплата й документи", "Підтвердимо в розрахунку")],
       "photo/bag-1.webp", "Шовкова твіллі на ручці білої сумки", "Твіллі — універсальний подарунок: на шию, сумку чи зап’ястя.", flip=True,
       extra='<div class="acc"><b>Що вказати в запиті для бухгалтерії</b><ul><li>Юрособа — ТОВ чи ФОП, код ЄДРПОУ</li><li>З ПДВ чи без</li><li>Потрібні документи: рахунок, видаткова накладна, акт, договір</li><li>Форма оплати й чи потрібна оплата окремо за кожну відправку</li></ul></div>')}
  {det("cert", "Сертифікати", "Коли не знаєте смаків — людина обирає сама",
       ["Подарункові сертифікати на 1 000, 1 500, 2 000, 2 500 і 4 000 грн, діють три місяці, електронні або фізичні, на будь-який товар obiimy.world."],
       [("Номінали", "1 000 · 1 500 · 2 000 · 2 500 · 4 000 грн"), ("Термін", "3 місяці"), ("Формат", "Електронний або фізичний"), ("На що", "Будь-який товар")],
       alt_bg=True, extra='<p><a class="btn btn-line btn-sm" href="b2b-certificates" style="margin-top:18px">Докладніше про сертифікати →</a></p>')}
  {det("brand", "Бренд", "Хто стоїть за Obiimy",
       ["Український бренд шовкових аксесуарів. Роздрібні партнери — INTERTOP і Hram в Україні, Be Brave у Канаді, UFD London; про бренд писали LIGA.net та INSIDER UA.", f"Шоурум: {SHOWROOM}, пн–пт 10:00–18:00, сб 11:00–18:00 — шовк можна побачити й відчути на дотик."],
       [("Засновниця", "Світлана Сніжко"), ("Партнери", "INTERTOP · Hram · Be Brave · UFD London"), ("Преса", "LIGA.net · INSIDER UA"), ("Шоурум", f"{SHOWROOM}"), ("Співпраця", f'<a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a>')],
       "photo/hratsiia-belt.webp", "Шовкова хустка поясом на синьому жакеті", "Хустка «Грація» — поясом на жакеті.")}
  {faq}
  {team.request_section("f-details", "Запит: подарунки для команди", "Отримати добірку й розрахунок", "Залиште контакти й дату, до якої потрібні подарунки, — надішлемо добірку принтів і розрахунок для компанії.", "silk", alt=False)}
  ''' + team.script("f-details", "")
    return dict(slug="b2b-team-details", skin="form", bar=BAR, title="Переваги й деталі: шовк, формати, пакування, доставка — Obiimy для команд",
                desc="Усе для корпоративного замовлення Obiimy: 100% італійський шовк і авторські принти, формати й роздрібні ціни, п’ять колекцій, пакування, догляд, привітання, доставка й оплата, сертифікати.",
                og="photo/dotyk-3.webp", nav=[("Шовк", "silk"), ("Формати й ціни", "sizes"), ("Пакування", "pack"), ("Доставка", "ship"), ("Сертифікати", "cert"), ("Питання", "faq")],
                cta="Запит", sticky="Переваги й деталі · Obiimy для команд", body=body)

def build():
    b2b.CSS += team.CSS + shop.CSS + CSS
    for fn in (gallery, details):
        p = fn()
        html = typo(team.bind(b2b.shell(p, p["body"])))
        (b2b.OUT / f"{p['slug']}.html").write_text(html)
        print(p["slug"], len(html) // 1024, "KB")

if __name__ == "__main__":
    build()
