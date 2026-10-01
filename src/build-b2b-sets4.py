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
b2b, team, SETS4, PERS = main.b2b, main.team, main.SETS4, main.PERS

CSS = """
  .hero.set { padding-block: clamp(20px, 4vw, 52px) clamp(20px, 4vw, 44px); }
  .hero.set h1 { font-size: clamp(2rem, 3.6vw, 3.2rem); }
  .hero.set .price { font-family: var(--display); font-size: clamp(1.6rem, 2.6vw, 2.2rem); margin-top: 18px; line-height: 1.1; }
  .hero.set .price small { display: block; font-family: var(--body); font-size: .82rem; color: var(--ink3); margin-top: 6px; white-space: normal; max-width: 34em; }
  .hero.set figure img { aspect-ratio: 4 / 5; }
  .gal { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }
  .gal figure { margin: 0; } .gal img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: var(--radius); background: #fff; }
  .gal figcaption { font-size: .82rem; color: var(--ink3); margin-top: 8px; }
  .det { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(24px, 5vw, 72px); align-items: start; }
  .kv { width: 100%; border-collapse: collapse; font-size: .95rem; }
  .kv th { text-align: left; font-weight: 600; padding: 12px 14px 12px 0; border-top: 1px solid var(--line); width: 38%; vertical-align: top; }
  .kv td { padding: 12px 0; border-top: 1px solid var(--line); color: var(--ink2); vertical-align: top; }
  .ways { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .way { border-top: 1px solid var(--ink); padding-top: 12px; } .way h3 { font-size: 1.2rem; margin: 0 0 4px; } .way p { color: var(--ink2); font-size: .92rem; margin: 0; }
  .who { font-family: var(--display); font-size: clamp(1.3rem, 2.2vw, 1.8rem); line-height: 1.25; max-width: 24em; }
  .pers4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; }
  .per4 { border-top: 1px solid var(--ink); padding-top: 12px; } .per4 .n { font-family: var(--display); font-size: 1.3rem; display: block; margin-bottom: 8px; }
  .per4 h3 { font-size: 1.15rem; margin: 0 0 6px; } .per4 p { color: var(--ink2); font-size: .9rem; margin: 0; } .per4 .tm { color: var(--ink3); font-size: .8rem; margin-top: 6px; } .per4.free .tm { color: var(--ink); font-weight: 600; }
  .others4 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
  .o4 { display: grid; grid-template-columns: 72px 1fr; gap: 12px; align-items: center; text-decoration: none; color: inherit; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 10px 12px; }
  .o4 img { width: 72px; height: 72px; object-fit: cover; border-radius: var(--radius); } .o4 b { font-family: var(--display); font-weight: 400; font-size: 1.05rem; display: block; line-height: 1.15; } .o4 span { color: var(--ink2); font-size: .85rem; }
  @media (max-width: 960px) { .gal, .pers4 { grid-template-columns: 1fr 1fr; } .det { grid-template-columns: 1fr; } .others4 { grid-template-columns: 1fr; } }
  @media (max-width: 640px) { .ways { grid-template-columns: 1fr; } .pers4 { grid-template-columns: 1fr; } .gal { gap: 10px; } }
"""

def page(i, S):
    hp, ha, hpos = S["hero"]
    fig = '<figure>' + img(hp, ha, sizes="(max-width: 960px) 100vw, 50vw", lazy=False, eager_priority=True, style=f"object-position:{hpos}" if hpos else "") + f'<div class="tag">{ha}</div></figure>'
    gal = "".join(f'<figure>{img(p, a, sizes="(max-width: 640px) 50vw, 25vw", style=f"object-position:{pos}" if pos else "")}<figcaption>{a}</figcaption></figure>' for p, a, pos in S["gal"])
    kv = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in S["inside"])
    ways = "".join(f'<div class="way"><h3>{h}</h3><p>{t}</p></div>' for h, t in S["ways"])
    pers = "".join(f'<div class="per4{" free" if j == 0 else ""}"><b class="n">0{j + 1}</b><h3>{n}</h3><p>{t}</p><p class="tm">{tm}</p></div>' for j, (n, t, tm, ph) in enumerate(PERS))
    others = "".join(f'<a class="o4" href="{o["slug"]}">{img(o["gal"][0][0], o["short"], sizes="72px")}<div><b>{o["short"]}</b><span>{o["pr"]} · детальніше →</span></div></a>' for o in SETS4 if o is not S)
    body = f'''
  <section class="hero set ph-first"><div class="wrap">
    <div>
      <p class="eyebrow"><a href="b2b-team-main#tiers">← Усі чотири рівні</a> · <span style="white-space:nowrap">{S["lb"]}</span></p>
      <h1>{S["name"]}</h1>
      <p class="lead">{S["lead"]}</p>
      <p class="price num">{S["pr"]}<small>{S["prnote"]}</small></p>
      <p class="note">Команді з 50 людей — {S["b50"]} за роздрібними цінами; доставку й персоналізацію рахуємо окремо.</p>
      <div class="cta"><a class="btn btn-gold" href="#request">Отримати розрахунок</a><a class="btn btn-line" href="#details">Що всередині</a></div>
    </div>
    {fig}
  </div></section>
  <section class="block" style="padding-top:0"><div class="wrap"><div class="gal">{gal}</div></div></section>
  <section class="block alt" id="details"><div class="wrap det">
    <div><div class="head"><p class="eyebrow">Деталі</p><h2>Що всередині</h2></div><table class="kv">{kv}</table></div>
    <div><div class="head"><p class="eyebrow">Як носити</p><h2>Чотири способи</h2></div><div class="ways">{ways}</div><p class="who" style="margin-top:28px">{S["who"]}</p></div>
  </div></section>
  <section class="block" id="logo"><div class="wrap">
    <div class="head"><p class="eyebrow">Персоналізація</p><h2>З вашим логотипом</h2><p class="sub">Перший рівень — безкоштовно в кожному корпоративному замовленні. Решта — залежно від строків, у розрахунку.</p></div>
    <div class="pers4">{pers}</div>
  </div></section>
  <section class="block alt"><div class="wrap"><div class="head"><p class="eyebrow">Інші рівні</p><h2>Ще три подарунки</h2></div><div class="others4">{others}</div><p style="margin-top:18px"><a href="b2b-team-main#tiers">← Порівняти всі чотири рівні</a></p></div></section>
  {team.request_section("f-set", f"Подарунки для команди · {S['short']}", "Отримати добірку й розрахунок", "Напишіть кількість і дату — у відповідь надішлемо принти на вибір і розрахунок окремими рядками: речі, персоналізація, доставка.", "details", alt=False)}
  ''' + team.script("f-set", "")
    return dict(slug=S["slug"], skin="form", bar=team.BAR, title=f"{S['short']} — подарунок для команди від Obiimy", desc=S["lead"][:150], og=hp,
                nav=[("Деталі", "details"), ("Логотип", "logo"), ("Запит", "request")], cta="Запит", sticky=f"{S['short']} · {S['pr']}", body=body)

def build():
    b2b.CSS += team.CSS + CSS
    for i, S in enumerate(SETS4):
        p = page(i, S)
        html = typo(team.bind(b2b.shell(p, p["body"])))
        (b2b.OUT / f"{p['slug']}.html").write_text(html)
        print(p["slug"], len(html) // 1024, "KB")

if __name__ == "__main__":
    build()
