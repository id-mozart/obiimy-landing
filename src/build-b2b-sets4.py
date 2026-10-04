#!/usr/bin/env python3
"""Four set pages for the team series (one per gift tier): b2b-set-twilly, b2b-set-scarf-ring, b2b-set-mask, b2b-set-scarf-twilly.
Data — SETS4 in build-b2b-team-main.py (facts from SITE-FACTS and the client's letter; photos: product + the SOLO shoot).
Not in the hub or menus: linked from the tiers section of b2b-team-main and from the deck."""
import importlib.util, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from imgs import img, typo
_spec = importlib.util.spec_from_file_location("main", ROOT / "build-b2b-team-main.py")
main = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(main)
b2b, team, SETS4, PERS, with_qr = main.b2b, main.team, main.SETS4, main.PERS, main.with_qr
def opos(o): return f"object-position:{o['hero'][2]}" if o["hero"][2] else ""
PROD = [3, 2, 1, 2]
M1POS = ["50% 12%", "55% 30%", "50% 30%", "50% 18%"]
KEEP = ("Що всередині", "Шовк", "Шовк і друк", "Друк", "Принти", "Майстер-клас", "Пакування", "Кому")

CSS = main.DECK_SKIN + """
  .hero.set { padding: 0 0 clamp(28px, 4vw, 48px); }
  .set-split { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); min-height: min(calc(100vh - 104px), 860px); }
  .set-ph { position: relative; overflow: hidden; } .set-ph img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
  .hero.set .set-cap { margin-top: 12px; font-size: .78rem; color: var(--ink3); }
  .hero.set .set-more .cutimg { object-fit: contain; border-radius: 0; filter: drop-shadow(0 14px 18px rgba(0,0,0,.18)); }
  .set-t { padding: clamp(28px, 4vw, 64px) max(clamp(16px, 4vw, 48px), calc((100vw - 1280px) / 2 + clamp(16px, 4vw, 48px))) clamp(28px, 4vw, 64px) clamp(16px, 5vw, 80px); display: flex; flex-direction: column; justify-content: center; }
  .crumb span::before { content: " · "; } .crumb span { white-space: nowrap; } .o4 span { display: block; } .o4-m { margin-top: 2px; }
  @media (max-width: 640px) { .crumb a { display: block; margin-bottom: 4px; } .crumb span::before { content: ""; } }
  .set-more { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; align-items: start; margin-top: clamp(20px, 3vw, 36px); } .set-more figure { margin: 0; } .set-more figcaption { font-size: .78rem; color: var(--ink3); margin-top: 8px; line-height: 1.35; }
  .hero.set .set-more img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: var(--radius); display: block; }
  .hero.set .set-more .m3 { object-fit: contain; border-radius: 0; filter: drop-shadow(0 14px 18px rgba(0,0,0,.18)); }
  @media (max-width: 960px) { .set-split { grid-template-columns: 1fr; min-height: 0; } .set-ph { aspect-ratio: 1 / 1; max-height: 62vh; width: 100%; } .set-t { max-width: none; } }
  .hero.set h1 { font-size: clamp(2.2rem, 4vw, 3.6rem); line-height: 1; margin-top: 12px; }
  .hero.set .lead { margin-top: 16px; text-wrap: pretty; }
  .hero.set .cta { margin-top: 20px; }
  @media (max-width: 640px) { .others4 { gap: 10px; } .o4 img { aspect-ratio: 3 / 4; } .o4 b { font-size: 1rem; line-height: 1.15; margin-top: 8px; min-height: 2.3em; } .o4 span { font-size: .78rem; } }
  .qrbox { margin: 8px 0 0; display: grid; grid-template-columns: 112px 1fr; gap: 14px; align-items: center; max-width: 340px; } .qrbox svg { width: 112px; height: 112px; } @media (max-width: 640px) { .qrbox { display: none; } } .qrbox figcaption { font-size: .85rem; color: var(--ink2); }
  @media (max-width: 960px) {  }
  .o4 { display: block; text-decoration: none; color: inherit; } .o4 img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: var(--radius); } .o4 b { display: block; font-family: var(--display); font-weight: 400; font-size: 1.25rem; margin-top: 12px; } .o4 span { color: var(--ink2); font-size: .9rem; }
  .hero.set h1 { font-size: clamp(2rem, 3.6vw, 3.2rem); }
  .hero.set .price { font-family: var(--display); font-size: clamp(1.6rem, 2.6vw, 2.2rem); margin-top: 18px; line-height: 1.1; }
  .hero.set .price small { display: block; font-family: var(--body); font-size: .82rem; line-height: 1.5; color: var(--ink3); margin-top: 6px; white-space: normal; max-width: 34em; }
  .hero.set figure img { aspect-ratio: 4 / 5; }
  .hero.set h1 i { font-style: italic; color: #8E8A84; }
  .b3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); max-width: 420px; gap: 8px 20px; margin: 16px 0 0; padding: 12px 0; border-block: 1px solid var(--line); } .b3 div { display: grid; } .b3 dt { font-size: .74rem; color: var(--ink3); } .b3 dd { margin: 0; white-space: nowrap; } .b3 dd span { display: block; }
  .gal { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }
  .gal figure { margin: 0; } .gal img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: var(--radius); }
  .gal figcaption { font-size: .82rem; color: var(--ink3); margin-top: 8px; }
  .det { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(24px, 5vw, 72px); align-items: start; }
  .kv { width: 100%; border-collapse: collapse; font-size: .95rem; }
  .kv th { text-align: left; font-weight: 600; padding: 12px 14px 12px 0; border-top: 1px solid var(--line); width: 38%; vertical-align: top; }
  .kv td { padding: 12px 0; border-top: 1px solid var(--line); color: var(--ink2); vertical-align: top; }
  .ways { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .way { border-top: 1px solid var(--ink); padding-top: 12px; } .way h3 { font-size: 1.2rem; margin: 0 0 4px; } .way p { color: var(--ink2); font-size: .92rem; margin: 0; }
  .men { margin: 26px 0 0; display: grid; grid-template-columns: 120px 1fr; gap: 16px; align-items: center; border-top: 1px solid var(--line); padding-top: 18px; } .men img { width: 120px; aspect-ratio: 4 / 5; object-fit: cover; border-radius: var(--radius); } .men figcaption { color: var(--ink2); font-size: .92rem; } .men b { display: block; font-family: var(--display); font-weight: 400; font-size: 1.2rem; color: var(--ink); margin-bottom: 4px; }
  .det-cut { margin: 28px 0 0; max-width: 300px; } .det-cut img { width: 100%; height: auto; filter: drop-shadow(0 14px 18px rgba(0,0,0,.16)); } .det-cut figcaption { font-size: .78rem; color: var(--ink3); margin-top: 10px; }
  .who { font-family: var(--display); font-size: clamp(1.3rem, 2.2vw, 1.8rem); line-height: 1.25; max-width: 24em; }
  .pers4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; }
  .per4 { border-top: 1px solid var(--ink); padding-top: 12px; } .per4 .n { font-family: var(--display); font-size: 1.3rem; display: block; margin-bottom: 8px; }
  .per4 h3 { font-size: 1.15rem; margin: 0 0 6px; } .per4 p { color: var(--ink2); font-size: .9rem; margin: 0; } .per4 .tm { color: var(--ink3); font-size: .8rem; margin-top: 6px; } .per4.free .tm { color: var(--ink); font-weight: 600; }
  .others4 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }
  @media (max-width: 960px) { .gal, .pers4 { grid-template-columns: 1fr 1fr; } .det { grid-template-columns: 1fr; } }
  @media (max-width: 640px) { .ways { grid-template-columns: 1fr; } .pers4 { grid-template-columns: 1fr; } .gal { gap: 10px; } }
"""

def page(i, S):
    hp, ha, hpos = S["hero"]
    g2 = S["gal"][0]; g3 = S["gal"][PROD[i]]
    def ph(src, alt, pos, cls, sizes):
        return img(src, alt, sizes=sizes, lazy=False, cls=cls, style=f"object-position:{pos}" if pos else "")
    m1 = ph(hp, ha, M1POS[i], "m1", "(max-width: 960px) 100vw, 50vw")
    more = (f'<figure>{img(g2[0], g2[1], sizes="(max-width: 960px) 45vw, 22vw", cls="m2 cutimg" if g2[0].startswith("img/cut/") else "m2", style=f"object-position:{g2[2]}" if g2[2] else "")}<figcaption>{g2[1]}</figcaption></figure>'
            f'<figure>{img(g3[0], g3[1], sizes="(max-width: 960px) 45vw, 22vw", cls="m3")}<figcaption>{g3[1]}</figcaption></figure>')
    b3 = "".join(f'<div><dt>{k} людей</dt><dd class="num">{main.bud(i, k)}</dd></div>' for k in (20, 50, 100))
    a, _dash, b = S["name"].partition(" — "); h1 = f"{a} — <i>{b}</i>" if b else a
    men = "" if True else f'<figure class="men">{img("photo/site/mask-synii-02.jpg", "Чоловік у шовковій масці для сну «Синій»", sizes="160px", style="object-position:50% 20%")}<figcaption><b>Чоловікам — маска окремо</b>2 700 грн; у наборі з резинкою — 3 100 грн.</figcaption></figure>' if i == 2 else ""
    mixed = ("Чоловікам у команді — маска окремо (2 700 грн), закладка для книги, наволочка або сертифікат на 1 000–4 000 грн" if i == 2 else "Тим, хто не носить аксесуари, — маска для сну, закладка для книги, наволочка або сертифікат на 1 000–4 000 грн") + ": змішану команду рахуємо в одному розрахунку."
    two = i >= 2
    BOX2 = {0: ("img/cut/avantiura-tw-2.webp", "Твіллі «Авантюра», 84 × 5"), 1: ("img/cut/hratsiia-flat.webp", "Хустка «Грація» 44 × 44"), 2: ("img/cut/mask-vpevnenist.webp", "Маска для сну «Впевненість» — той самий принт, що на фото вгорі"), 3: ("img/cut/set-vpevnenist-box.webp", "Той самий набір у принті «Впевненість»")}
    boxfig = f'<figure class="det-cut">{img(BOX2[i][0], BOX2[i][1], sizes="(max-width: 960px) 80vw, 360px")}<figcaption>{BOX2[i][1]}</figcaption></figure>' if i in BOX2 else ""
    kv = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in S["inside"] if k in KEEP)
    ways = "".join(f'<div class="way"><h3>{h}</h3><p>{t}</p></div>' for h, t in (S["ways"][:2] if i >= 2 else S["ways"]))
    others = "".join(f'<a class="o4" href="{o["slug"]}">{img(o["hero"][0], o["short"], sizes="(max-width: 960px) 100vw, 33vw", style=opos(o))}<div><b>{o["short"]}</b><span>{o["pr"]}</span><span class="o4-m">детальніше →</span></div></a>' for o in SETS4 if o is not S)
    body = f'''
  <section class="hero set"><div class="set-split">
    <div class="set-ph">{m1}</div>
    <div class="set-t">
      <p class="eyebrow crumb"><a href="b2b-team-main#tiers">← Усі чотири подарунки</a><span>{S["lb"]}</span></p>
      <h1>{h1}</h1>
      <p class="lead">{S["lead"]}</p>
      <p class="price num">{S["pr"]}<small>{S["prnote"]}</small></p>
      <dl class="b3" aria-label="Бюджет команди, грн">{b3}</dl><p class="note" style="margin-top:8px">Бюджет — за роздрібними цінами, грн; пакування й наліпка з вашим логотипом — безкоштовно; доставку рахуємо окремо. <a href="b2b-team-main#terms">Строки, доставка, оплата — умови →</a></p>
      <div class="cta"><a class="btn btn-gold" href="#request">Отримати розрахунок</a><a class="btn btn-line" href="#details">Що всередині</a></div>
      <div class="set-more">{more}</div>
      <p class="note set-cap">{ha}.</p>
    </div>
  </div></section>
  <section class="block alt" id="details"><div class="wrap det">
    <div><div class="head"><p class="eyebrow">Деталі</p><h2>Що всередині</h2></div><table class="kv">{kv}</table><p class="note" style="margin-top:14px">Пакування й наліпка з вашим логотипом — безкоштовно; бирка, листівка, власний принт — <a href="b2b-team-main#logo">у розрахунку</a>. {mixed}</p></div>
    <div><div class="head"><p class="eyebrow">{"Як носити" if i < 2 else "Що в наборі"}</p><h2>{"Чотири способи" if i < 2 else "Дві речі — один принт"}</h2></div><div class="ways">{ways}</div><p class="who" style="margin-top:28px">{S["who"]}</p>{men}{boxfig}</div>
  </div></section>
  <section class="block" id="others"><div class="wrap"><div class="head"><p class="eyebrow">Інші подарунки</p><h2>Ще три подарунки</h2></div><div class="others4">{others}</div><p style="margin-top:18px"><a href="b2b-team-main#tiers">← Порівняти всі чотири подарунки</a></p></div></section>
  {with_qr(team.request_section("f-set", "Подарунки для команди · " + S["short"], "Напишіть — <i>надішлемо добірку й розрахунок</i>", "Нагода, кількість і дата — цього досить для першого листа.", "details", alt=True, corp=True))}
  ''' + team.script("f-set", "")
    return dict(slug=S["slug"], skin="deck", bar=team.BAR, title=f"{S['short']} — подарунок для команди від Obiimy", desc=f"{S['short']} — подарунок для команди від Obiimy, {S['pr']} на людину. Пакування й наліпка з логотипом компанії — безкоштовно.", og=hp,
                nav=[("Деталі", "details"), ("Інші подарунки", "others")], cta="Запит", sticky=f"{S['short']} · {S['pr']}", others=False, body=body)

def build():
    b2b.CSS += team.CSS + CSS
    for i, S in enumerate(SETS4):
        p = page(i, S)
        html = main.snap_type(typo(team.bind(b2b.shell(p, p["body"]))))
        (b2b.OUT / f"{p['slug']}.html").write_text(html)
        print(p["slug"], len(html) // 1024, "KB")

if __name__ == "__main__":
    build()
