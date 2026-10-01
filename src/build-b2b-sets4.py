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
M1POS = ["50% 12%", "50% 8%", "50% 30%", "50% 18%"]
KEEP = ("Що всередині", "Шовк", "Шовк і друк", "Майстер-клас", "Пакування", "Кому")

CSS = """
  .hero.set { padding: 0 0 clamp(28px, 4vw, 48px); }
  .mos { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); grid-template-rows: minmax(0, 1.35fr) minmax(0, 1fr); gap: 6px; height: clamp(520px, 84vh, 880px); overflow: hidden; }
  .mos img { width: 100%; height: 100%; max-height: 100%; min-height: 0; object-fit: cover; display: block; } .mos .m3 { object-fit: contain; background: #fff; padding: 4%; } .mos .m1 { grid-row: span 2; }
  .set-h { display: grid; grid-template-columns: minmax(0, 6fr) minmax(0, 6fr); gap: clamp(24px, 4vw, 64px); align-items: end; margin-top: clamp(28px, 4vw, 48px); }
  .hero.set h1 { font-size: clamp(2.2rem, 4vw, 3.6rem); line-height: 1; margin-top: 12px; }
  .hero.set .lead { margin-top: 0; }
  .hero.set .cta { margin-top: 20px; }
  @media (max-width: 640px) { .qrbox { display: none; } .others4 { gap: 12px; } .o4 { display: grid; grid-template-columns: 96px 1fr; gap: 12px; align-items: center; } .o4 img { aspect-ratio: 1 / 1; } .o4 b { margin-top: 0; font-size: 1.1rem; } }
  .qrbox { margin: 8px 0 0; display: grid; grid-template-columns: 96px 1fr; gap: 14px; align-items: center; max-width: 320px; } .qrbox svg { width: 96px; height: 96px; } .qrbox figcaption { font-size: .85rem; color: var(--ink2); }
  @media (max-width: 960px) { .mos { height: auto; grid-template-rows: auto auto; overflow: visible; } .mos img { max-height: none; } .mos .m1 { grid-column: span 2; grid-row: auto; aspect-ratio: 4 / 5; } .mos .m2, .mos .m3 { aspect-ratio: 1 / 1; } .set-h { grid-template-columns: 1fr; } }
  .o4 { display: block; text-decoration: none; color: inherit; } .o4 img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: var(--radius); } .o4 b { display: block; font-family: var(--display); font-weight: 400; font-size: 1.25rem; margin-top: 12px; } .o4 span { color: var(--ink2); font-size: .9rem; }
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
  .others4 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }
  @media (max-width: 960px) { .gal, .pers4 { grid-template-columns: 1fr 1fr; } .det { grid-template-columns: 1fr; } .others4 { grid-template-columns: 1fr; } }
  @media (max-width: 640px) { .ways { grid-template-columns: 1fr; } .pers4 { grid-template-columns: 1fr; } .gal { gap: 10px; } }
"""

def page(i, S):
    hp, ha, hpos = S["hero"]
    g2 = S["gal"][0]; g3 = S["gal"][PROD[i]]
    def ph(src, alt, pos, cls, sizes):
        return img(src, alt, sizes=sizes, lazy=False, cls=cls, style=f"object-position:{pos}" if pos else "")
    mos = ph(hp, ha, M1POS[i], "m1", "(max-width: 960px) 100vw, 55vw") + ph(g2[0], g2[1], g2[2], "m2", "(max-width: 960px) 50vw, 25vw") + ph(g3[0], g3[1], g3[2], "m3", "(max-width: 960px) 50vw, 25vw")
    kv = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in S["inside"] if k in KEEP)
    ways = "".join(f'<div class="way"><h3>{h}</h3><p>{t}</p></div>' for h, t in S["ways"])
    others = "".join(f'<a class="o4" href="{o["slug"]}">{img(o["hero"][0], o["short"], sizes="(max-width: 960px) 100vw, 33vw", style=opos(o))}<div><b>{o["short"]}</b><span>{o["pr"]} · детальніше →</span></div></a>' for o in SETS4 if o is not S)
    body = f'''
  <section class="hero set"><div class="mos">{mos}</div>
    <div class="wrap set-h">
      <div><p class="eyebrow"><a href="b2b-team-main#tiers">← Усі чотири рівні</a> · <span style="white-space:nowrap">{S["lb"]}</span></p>
      <h1>{S["name"]}</h1></div>
      <div><p class="lead">{S["lead"]}</p>
      <p class="price num">{S["pr"]}<small>{S["prnote"]}<br>Команді з 50 людей — {S["b50"]} за роздрібними цінами; доставку й персоналізацію рахуємо окремо.</small></p>
      <div class="cta"><a class="btn btn-gold" href="#request">Отримати розрахунок</a><a class="btn btn-line" href="#details">Що всередині</a></div></div>
    </div>
  </section>
  <section class="block alt" id="details"><div class="wrap det">
    <div><div class="head"><p class="eyebrow">Деталі</p><h2>Що всередині</h2></div><table class="kv">{kv}</table><p class="note" style="margin-top:14px">Пакування й наліпка з вашим логотипом — безкоштовно; бирка, листівка, власний принт — <a href="b2b-team-main#logo">у розрахунку</a>. Чоловікам у команді — сертифікат 1 000–4 000 грн, маска для сну, наволочка або закладка: змішану команду рахуємо в одному розрахунку.</p></div>
    <div><div class="head"><p class="eyebrow">{"Як носити" if i < 2 else "Що в наборі"}</p><h2>{"Чотири способи" if i < 2 else "Чотири деталі"}</h2></div><div class="ways">{ways}</div><p class="who" style="margin-top:28px">{S["who"]}</p></div>
  </div></section>
  <section class="block" id="others"><div class="wrap"><div class="head"><p class="eyebrow">Інші рівні</p><h2>Ще три подарунки</h2></div><div class="others4">{others}</div><p style="margin-top:18px"><a href="b2b-team-main#tiers">← Порівняти всі чотири рівні</a></p></div></section>
  {with_qr(team.request_section("f-set", "Подарунки для команди · " + S["short"], "Отримати добірку й розрахунок", "Кількість і дата — у відповідь принти на вибір і розрахунок.", "details", alt=True))}
  ''' + team.script("f-set", "")
    return dict(slug=S["slug"], skin="form", bar=team.BAR, title=f"{S['short']} — подарунок для команди від Obiimy", desc=S["lead"][:150], og=hp,
                nav=[("Деталі", "details"), ("Інші рівні", "others")], cta="Запит", sticky=f"{S['short']} · {S['pr']}", body=body)

def build():
    b2b.CSS += team.CSS + CSS
    for i, S in enumerate(SETS4):
        p = page(i, S)
        html = typo(team.bind(b2b.shell(p, p["body"])))
        (b2b.OUT / f"{p['slug']}.html").write_text(html)
        print(p["slug"], len(html) // 1024, "KB")

if __name__ == "__main__":
    build()
