#!/usr/bin/env python3
"""The one B2B page for gifts inside a company — the best of the seven after six audit rounds:
brand on the first screen, the catalogue with prices right after it, a yearly plan with three programmes as presets,
things for everyone, greetings, reasons, steps, FAQ, trust, request. Facts, prices and helpers come from
build-b2b-team.py and build-b2b-team-shop.py; nothing promises a discount, a deadline or a minimum order."""
import importlib.util, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
shop = load("build-b2b-team-shop")
qr_svg = load("qr").qr_svg
cast = load("cast").cast
QR_TG = '<figure class="qrbox">' + qr_svg("https://t.me/OBIIMY_sales", 112, plate="#F7F5F1") + '<figcaption>Скануйте — чат із менеджером у Telegram</figcaption></figure>'
def with_qr(html): return html.replace("Написати в Telegram</a>", "Написати в Telegram</a>" + QR_TG)
team = shop.team
b2b, img, price, typo, J, hero = team.b2b, team.img, team.price, team.typo, team.J, team.hero
CATALOG, CAT, STAGES, PLANS, CARDS = team.CATALOG, team.CAT, team.STAGES, team.PLANS, team.CARDS
PHONE, PHONE_HREF, SAMPLE, BAR = team.PHONE, team.PHONE_HREF, team.SAMPLE, team.BAR

# three programmes as presets for the calculator: occasion row -> (silk, for everyone, share of the team)
PRESETS = [
    ("base", "«Знак уваги»", "Один подарунок на рік: шовкова резинка до дня народження (для всіх — закладка).", {"bday": ("scr", "book", 1)}),
    ("team", "«Команда»", "Два подарунки на рік: твіллі до дня народження й резинка до перемоги команди (для всіх — сертифікат 1 500 і закладка).", {"bday": ("tw", "cert15", 1), "team": ("scr", "book", 1)}),
    ("plus", "«Визнання»", "Два подарунки на рік: набір «твіллі та резинка» до дня народження й хустка 65 × 65 до річниці (для всіх — сертифікат 2 000 і маска).", {"bday": ("twscr", "cert2", 1), "years": ("h65", "mask", 1)}),
]
def preset_range(rows):
    s = sum(CAT[a]["p"] for a, _b, _sh in rows.values()); u = sum(CAT[b]["p"] for _a, b, _sh in rows.values())
    return price(s) if s == u else f"{min(s, u):,}".replace(",", " ") + "–" + price(max(s, u))

def snap_type(html):
    """Every font-size in the page CSS snaps to a scale of eight: three fluid display sizes and 1.5 / 1.2 / 1 / .875 / .75 rem."""
    def size(v):
        v = v.strip()
        m = re.match(r"clamp\(([^,]+),([^,]+),\s*([\d.]+)rem\)", v)
        if m: return float(m.group(3))
        m = re.match(r"([\d.]+)(rem|px)$", v)
        return (float(m.group(1)) / (16 if m.group(2) == "px" else 1)) if m else None
    def snap(m):
        z = size(m.group(1))
        if z is None: return m.group(0)
        v = ("var(--fs-h1)" if z >= 3.4 else "var(--fs-h2)" if z >= 2.3 else "var(--fs-h3)" if z >= 1.7 else "1.5rem" if z >= 1.38 else "1.2rem" if z >= 1.12 else "1rem" if z >= .97 else ".875rem" if z >= .82 else ".75rem")
        return "font-size: " + v
    parts = re.split(r"(<style[\s\S]*?</style>)", html)
    return "".join(re.sub(r"font-size:\s*([^;}]+)", snap, p) if p.startswith("<style") else p for p in parts)

DECK_SKIN = """
  :root { --fs-h1: clamp(2.6rem, 5.2vw, 4.6rem); --fs-h2: clamp(1.9rem, 3.2vw, 2.8rem); --fs-h3: clamp(1.5rem, 2.2vw, 2rem); }
  html { font-synthesis: none; }
  form { align-items: start; } select:has(option[value=""]:checked) { color: var(--ink3); }
  .form-block h2 i { font-style: italic; color: #8E8A84; }
  @media (max-width: 640px) { body:has(.sticky.on) .nav .btn { visibility: hidden; } }
  .contact h2 { color: var(--ink); } footer a { white-space: nowrap; }
  h1, h2, h3 { letter-spacing: -.01em; }
  .btn-gold { color: #F1EFEA; } .hero.cover .btn-gold, .solo-dark .btn-gold, .sticky a { background: #E7D9A6; color: #141414; }
  .btn { letter-spacing: .02em; }
"""
CSS = DECK_SKIN + """
  .hero.cover { padding: 0; position: relative; }
  .hero.cover .cover-img { margin-top: 0; }
  .nav { background: var(--bg); backdrop-filter: none; }
  .hero.cover .cover-img { width: 100%; height: clamp(540px, 82vh, 860px); object-fit: cover; object-position: 50% 28%; display: block; }
  .hero.cover::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,0,0,.66) 0%, rgba(0,0,0,.34) 38%, rgba(0,0,0,0) 62%), linear-gradient(0deg, rgba(0,0,0,.6) 0%, rgba(0,0,0,0) 50%); pointer-events: none; }
  .hero.cover .wrap { display: block; }
  .hero.cover .cover-t { position: absolute; left: 0; right: 0; bottom: clamp(32px, 6vw, 72px); z-index: 1; color: #fff; }
  .hero.cover .eyebrow { color: rgba(255,255,255,.78); }
  .hero.cover h1 { font-size: clamp(2.6rem, 5.2vw, 4.6rem); line-height: 1; margin-top: 14px; }
  .hero.cover .lead { color: rgba(255,255,255,.92); max-width: 26em; margin-top: 16px; }
  .hero.cover .cta { margin-top: 24px; } .hero.cover .btn-line { border-color: rgba(255,255,255,.6); color: #fff; }
  @media (max-width: 640px) { .hero.cover .cover-img { height: 92vh; object-position: 50% 12%; } .hero.cover .lead { font-size: .95rem; } .hero.cover::after { background: linear-gradient(0deg, rgba(0,0,0,.86) 0%, rgba(0,0,0,.62) 34%, rgba(0,0,0,0) 62%); } }
  .qrbox { margin: 8px 0 0; display: grid; grid-template-columns: 112px 1fr; gap: 14px; align-items: center; max-width: 340px; }
  .qrbox svg { width: 112px; height: 112px; } .qrbox figcaption { font-size: .85rem; color: var(--ink2); }
  .nums { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; border-top: 1px solid var(--ink); padding-top: 16px; margin-top: 22px; }
  .nums b { display: block; font-family: var(--display); font-weight: 400; font-size: clamp(1.8rem, 3vw, 2.6rem); line-height: 1; } .nums span { font-size: .82rem; color: var(--ink3); }
  .quote-band { position: relative; background: #0E0E0E; } .quote-band img { width: 100%; height: clamp(520px, 80vh, 820px); object-fit: cover; display: block; }
  .quote-band::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,0,0,.78) 0%, rgba(0,0,0,.45) 36%, rgba(0,0,0,0) 60%); pointer-events: none; }
  .qb-t { position: absolute; left: 0; right: 0; bottom: clamp(36px, 6vw, 72px); z-index: 1; text-align: left; color: #fff; } .qb-in { max-width: 460px; }
  .bigq { font-family: var(--display); font-style: italic; font-size: clamp(1.9rem, 3.4vw, 3.2rem); line-height: 1.1; color: #E7D9A6; margin: 0 0 14px; }
  .qb-t p { color: rgba(255,255,255,.9); margin: 0 0 10px; } .qb-t .eyebrow { color: rgba(255,255,255,.7); }
  @media (max-width: 640px) { .nums { grid-template-columns: 1fr 1fr; } .quote-band img { height: 90vh; } }
  .perks { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: clamp(24px, 5vw, 72px); align-items: center; }
  .perks-ph { margin: 0; } .perks-ph img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; object-position: 50% 20%; border-radius: var(--radius); }
  .perk { display: grid; grid-template-columns: 44px 1fr; gap: 0 14px; border-top: 1px solid var(--ink); padding: 18px 0 16px; }
  .perk .n { font-family: var(--display); font-size: 1.5rem; line-height: 1; grid-row: span 2; }
  .perk h3 { font-size: 1.45rem; margin: 0 0 6px; } .perk p { color: var(--ink2); margin: 0; }
  .solo { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(20px, 4vw, 56px); align-items: start; }
  .solo-ph { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; } .solo-ph img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: var(--radius); }
  .solo-ph img:first-child { grid-column: span 2; aspect-ratio: 4 / 3; object-position: 50% 25%; }
  .solo-l { display: grid; }
  .sp { display: grid; grid-template-columns: 64px 1fr; gap: 14px; align-items: center; padding: 10px 0; border-top: 1px solid var(--line); }
  .sp:first-child { border-top: 0; padding-top: 0; }
  .sp img { width: 64px; height: 64px; object-fit: contain; }
  .sp b { font-family: var(--display); font-weight: 400; font-size: 1.15rem; display: block; line-height: 1.15; }
  .sp span { display: block; color: var(--ink2); font-size: .9rem; } .sp small { color: var(--ink3); font-size: .8rem; }
  .solo-dark { background: #0E0E0E; color: #F3F1EC; --ink: #F3F1EC; --ink2: #C9C5BE; --ink3: #8E8A84; --line: rgba(255,255,255,.16); --card: #171717; }
  .solo-dark .eyebrow { color: #B8B3AA; }
  .sd-top { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: clamp(28px, 5vw, 72px); align-items: center; }
  .sd-t h2 { font-size: clamp(2.6rem, 5vw, 4.4rem); line-height: .98; margin: 10px 0 18px; }
  .sd-slogan { font-family: var(--display); font-style: italic; font-size: clamp(1.2rem, 1.8vw, 1.45rem); color: #E7D9A6; margin-bottom: 18px; }
  .sd-t p { color: #C9C5BE; margin-bottom: 14px; } .sd-note { color: #F3F1EC; border-top: 1px solid rgba(255,255,255,.2); padding-top: 14px; margin-top: 18px; font-size: .95rem; }
  .sd-ph { margin: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .sd-ph img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: var(--radius); }
  .sd-ph img:first-child { grid-column: span 2; aspect-ratio: 16 / 10; }
  .sd-hd { display: grid; grid-template-columns: 1fr minmax(0, 420px); gap: 24px; align-items: end; margin-top: clamp(32px, 4vw, 56px); padding-top: 24px; border-top: 1px solid rgba(255,255,255,.16); margin-bottom: 22px; }
  .sd-hd.top { margin-top: 0; padding-top: 0; border-top: 0; margin-bottom: clamp(20px, 3vw, 32px); }
  .sd-hd h3 { font-size: clamp(1.5rem, 2.4vw, 2rem); margin: 0; } .sd-hd p { color: #B8B3AA; font-size: .88rem; margin: 0; }
  .pcs { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }
  .pc-ph { position: relative; overflow: hidden; } .pc .m { width: 100%; aspect-ratio: 3 / 4.6; object-fit: cover; display: block; }
  .pc-ph::after { content: ""; position: absolute; inset: 45% 0 0; background: linear-gradient(180deg, rgba(0,0,0,0), rgba(0,0,0,.82)); pointer-events: none; }
  .pc-b { display: grid; grid-template-columns: 44px 1fr; gap: 12px; align-items: center; margin-top: 12px; } .pc .fl { width: 44px; height: 44px; object-fit: contain; }
  .pc-t { position: absolute; left: 14px; right: 12px; bottom: 14px; z-index: 2; color: #fff; }
  .pc-t b { display: block; font-family: var(--display); font-style: italic; font-weight: 400; font-size: clamp(1.5rem, 2.2vw, 2rem); line-height: 1.05; color: #E7D9A6; }
  .pc-t span { display: block; font-size: .88rem; line-height: 1.35; margin-top: 6px; min-height: 2.7em; color: rgba(255,255,255,.88); }
  .pc-cta { display: flex; flex-direction: column; justify-content: flex-end; aspect-ratio: 3 / 4.6; border: 1px solid rgba(255,255,255,.22); border-radius: var(--radius); padding: 18px; text-decoration: none; color: #F3F1EC; align-self: start; } .pc-cta::after { display: none; } .pc-cta:hover { border-color: #E7D9A6; }
  .pc-cta b { font-family: var(--display); font-style: italic; font-weight: 400; font-size: clamp(1.5rem, 2.2vw, 2rem); line-height: 1.05; color: #E7D9A6; } .pc-cta span { font-size: .88rem; line-height: 1.4; color: #C9C5BE; margin: 8px 0 16px; } .pc-cta em { font-style: normal; font-weight: 600; font-size: .9rem; }
  .pc small { display: block; font-size: .8rem; color: #8E8A84; line-height: 1.35; }
  .ways { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }
  .way { position: relative; margin: 0; overflow: hidden; border-radius: var(--radius); } .way img { width: 100%; aspect-ratio: 3 / 4; object-fit: cover; display: block; }
  .way::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 50%, rgba(0,0,0,.8) 100%); pointer-events: none; }
  .way figcaption { position: absolute; left: 22px; right: 18px; bottom: 22px; z-index: 2; color: #fff; }
  .way b { display: block; font-family: var(--display); font-style: italic; font-weight: 400; font-size: clamp(1.6rem, 2.4vw, 2.2rem); line-height: 1; color: #F3EBD0; }
  .way span { display: block; font-family: var(--display); font-size: 1rem; margin-top: 8px; color: rgba(255,255,255,.9); }
  .ways-dark { padding-top: clamp(56px, 7vw, 96px); }
  @media (max-width: 960px) { .pcs { grid-template-columns: repeat(2, minmax(0, 1fr)); } .ways { grid-template-columns: 1fr 1fr; } .sd-hd { grid-template-columns: 1fr; } }
  @media (max-width: 640px) { .pcs { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 10px; margin: 0 -16px; padding: 0 16px 6px; scrollbar-width: none; } .pcs::-webkit-scrollbar { display: none; } .pc { flex: 0 0 62vw; scroll-snap-align: start; } .ways { grid-template-columns: 1fr 1fr; gap: 8px; } .way img { aspect-ratio: 3 / 4; } .way figcaption { left: 12px; bottom: 12px; } .way b { font-size: 1.3rem; } .way span { font-size: .8rem; } .qrbox { display: none; } .quote-band img { height: 60vh; } }
  .sd-prints { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 14px; margin-top: clamp(32px, 4vw, 56px); padding-top: 24px; border-top: 1px solid rgba(255,255,255,.16); }
  .sd-p img { width: 100%; aspect-ratio: 1 / 1; object-fit: contain; }
  .sd-p b { display: block; font-family: var(--display); font-weight: 400; font-size: 1.1rem; margin-top: 10px; line-height: 1.1; }
  .sd-p span { display: block; color: #8E8A84; font-size: .78rem; margin-top: 3px; }
  @media (max-width: 960px) { .sd-top { grid-template-columns: 1fr; } .sd-prints { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
  @media (max-width: 640px) { .sd-prints { grid-template-columns: repeat(2, minmax(0, 1fr)); } .sd-ph img:first-child { aspect-ratio: 4 / 3; } }
  .assort { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 16px 14px; }
  .as { text-align: left; } .as-im { aspect-ratio: 1 / 1; display: flex; align-items: flex-end; justify-content: center; padding: 6% 6% 8%; border-bottom: 1px solid var(--line); } .as img { max-height: 100%; height: auto; object-fit: contain; filter: drop-shadow(0 10px 14px rgba(0,0,0,.16)); }
  .as span.num { display: block; } .as em { display: inline-block; font-style: normal; font-size: .64rem; letter-spacing: .16em; text-transform: uppercase; color: var(--ink); border: 1px solid var(--ink); border-radius: 99px; padding: 1px 7px 0 9px; margin-left: 8px; vertical-align: 1px; }
  .as b { display: block; font-family: var(--display); font-weight: 400; font-size: 1.05rem; line-height: 1.15; margin-top: 10px; }
  .as span { color: var(--ink2); font-size: .9rem; }
  @media (max-width: 960px) { .perks, .solo { grid-template-columns: 1fr; } .assort { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
  @media (max-width: 640px) { .assort { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px 8px; } .as b { font-size: .92rem; } .as span { font-size: .8rem; } .perks-ph img { aspect-ratio: 4 / 3; } }
  .ta { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: clamp(24px, 4vw, 56px); align-items: stretch; }
  .ta figure { margin: 0; } .ta figure img { width: 100%; height: 100%; min-height: 420px; object-fit: cover; border-radius: var(--radius); }
  .ta-l { display: grid; align-content: center; }
  .tr { display: grid; grid-template-columns: 96px 1fr auto; gap: 18px; align-items: center; padding: 16px 0; border-top: 1px solid var(--ink); text-decoration: none; color: inherit; }
  .tr:last-child { border-bottom: 1px solid var(--ink); }
  .tr img { width: 96px; height: 96px; object-fit: contain; filter: drop-shadow(0 10px 14px rgba(0,0,0,.16)); }
  .tr .eyebrow { margin-bottom: 2px; } .tr b { font-family: var(--display); font-weight: 400; font-size: 1.35rem; display: block; line-height: 1.15; }
  .tr span { color: var(--ink2); font-size: .9rem; display: block; margin-top: 2px; }
  .tr em { font-style: normal; font-family: var(--display); font-size: 1.5rem; white-space: nowrap; }
  .tbs { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }
  .tb { position: relative; display: block; border-radius: var(--radius); overflow: hidden; text-decoration: none; color: #fff; aspect-ratio: 3 / 4; background: #222; }
  .tb > img:first-child { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform .5s; } .tb:hover > img:first-child { transform: scale(1.03); }
  .tb::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 45%, rgba(0,0,0,.72) 100%); }
  .tb-t { position: absolute; left: 18px; right: 18px; bottom: 18px; z-index: 1; } .tb-t .eyebrow { color: rgba(255,255,255,.75); margin-bottom: 4px; }
  .tb-t b { font-family: var(--display); font-weight: 400; font-size: 1.4rem; display: block; line-height: 1.1; } .tb-t em { font-style: normal; font-family: var(--display); font-size: 1.3rem; display: block; margin-top: 6px; }
  .tb-p { position: absolute; top: 14px; right: 14px; width: 76px; height: 76px; object-fit: contain; z-index: 1; filter: drop-shadow(0 6px 10px rgba(0,0,0,.45)); }
  .tcs { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
  .tcs { gap: clamp(28px, 3.4vw, 44px) clamp(24px, 3.4vw, 48px); }
  .tc { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: clamp(16px, 2vw, 26px); border-top: 1px solid var(--ink); padding-top: 18px; text-decoration: none; color: inherit; }
  .tc-ph { margin: 0; } .tc-im { aspect-ratio: 4 / 5; position: relative; overflow: hidden; } .tc-im img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; transition: transform .5s; } .tc:hover .tc-im img { transform: scale(1.03); }
  .tc-ph figcaption { font-size: .75rem; line-height: 1.4; color: var(--ink3); margin-top: 8px; min-height: 2.8em; }
  .tc-h { display: grid; grid-template-columns: 1fr 96px; gap: 12px; align-items: center; min-height: 96px; margin: 2px 0 8px; } .tc-p { width: 96px; height: 96px; object-fit: contain; filter: drop-shadow(0 6px 10px rgba(0,0,0,.12)); } .tc-t small { display: block; min-height: 2.9em; } .tc-t .eyebrow { min-height: 2.9em; } .tc-t .tc-capm { display: none; }
  .tc-t { display: flex; flex-direction: column; } .tc-t > p:not(.eyebrow) { min-height: 5.2em; } .tc-b dd { min-height: 2.9em; } .tc-t h3 { font-size: 1.6rem; line-height: 1.12; margin: 0; } .tc-t p { color: var(--ink2); font-size: .92rem; margin: 0; }
  .tc-b { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 14px 0 0; padding: 10px 0; border-block: 1px solid var(--line); } .tc-b div { display: grid; } .tc-b dt { font-size: .72rem; color: var(--ink3); } .tc-b dd { margin: 0; font-size: .92rem; white-space: nowrap; } .tc-b dd span { display: block; }
  .tc-t .more { margin-top: 12px; font-weight: 600; font-size: .9rem; } .tc:hover .more { text-decoration: underline; }
  .sd-cta { border-color: rgba(255,255,255,.5); color: #F3F1EC; margin-top: 6px; }
  .hero.main .lead-m { display: none; }
  @media (max-width: 640px) { .hero.main .lead-m { display: block; color: var(--ink2); margin-top: 10px; } .hero.main figure img { aspect-ratio: 4 / 5 !important; object-position: 50% 15% !important; } }
  .tc-t em { font-style: normal; font-family: var(--display); font-size: 1.6rem; margin-top: auto; padding-top: 14px; } .tc-t small { color: var(--ink3); font-size: .78rem; }
  @media (max-width: 960px) { .ta { grid-template-columns: 1fr; } .ta figure img { min-height: 0; aspect-ratio: 4 / 3; } .tbs { grid-template-columns: 1fr 1fr; } .tcs { grid-template-columns: 1fr; } }
  @media (max-width: 640px) { .tbs { grid-template-columns: 1fr; } .tb { aspect-ratio: 4 / 5; } .tc { grid-template-columns: 1fr; } .tr { grid-template-columns: 72px 1fr; } .tr em { grid-column: 2; } .tr img { width: 72px; height: 72px; } }
  .cond { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; border-top: 1px solid var(--ink); padding-top: 18px; }
  .cond b { display: block; font-family: var(--display); font-weight: 400; font-size: 1.2rem; margin-bottom: 4px; } .cond span { color: var(--ink2); font-size: .92rem; }
  @media (max-width: 640px) { .cond { grid-template-columns: 1fr; } }
  .per-ph { margin: clamp(24px, 3vw, 40px) 0 0; } .per-ph img { width: 100%; height: clamp(260px, 46vw, 520px); object-fit: cover; border-radius: var(--radius); }
  .per-ph figcaption { font-size: .85rem; color: var(--ink3); margin-top: 10px; }
  .photo-band { position: relative; } .photo-band img { width: 100%; height: clamp(420px, 72vh, 720px); object-fit: cover; display: block; }
  .photo-band::after { content: ""; position: absolute; inset: 0; background: linear-gradient(0deg, rgba(0,0,0,.6) 0%, rgba(0,0,0,0) 55%); pointer-events: none; }
  .pb-t { position: absolute; left: 0; right: 0; bottom: clamp(28px, 5vw, 56px); z-index: 1; color: #fff; }
  .pb-t .eyebrow { color: rgba(255,255,255,.75); } .pb-t h2 { font-size: clamp(1.8rem, 3.6vw, 3rem); max-width: 11em; margin-top: 8px; }
  .tiers4, .pers4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; }
  .tier4, .per4 { display: flex; flex-direction: column; border-top: 1px solid var(--ink); padding-top: 12px; }
  .tier4 .n, .per4 .n { font-family: var(--display); font-weight: 400; font-size: 1.4rem; line-height: 1; margin-bottom: 10px; }
  .tier4 img, .per4 img { width: 100%; aspect-ratio: 1 / 1; object-fit: contain; filter: drop-shadow(0 10px 14px rgba(0,0,0,.16)); }
  .tier4 .eyebrow { margin: 12px 0 2px; }
  .tier4 h3, .per4 h3 { font-size: 1.25rem; margin: 0 0 6px; }
  .tier4 p, .per4 p { color: var(--ink2); font-size: .92rem; margin: 0; }
  .tier4 .pz { margin-top: auto; padding-top: 12px; display: grid; gap: 2px; }
  .tier4 .rrp { font-family: var(--display); font-weight: 400; font-size: 1.6rem; line-height: 1.1; }
  .tier4 small { color: var(--ink3); font-size: .78rem; }
  .tier4 .more { margin-top: 8px; font-weight: 600; text-decoration: none; border-bottom: 1px solid var(--ink); align-self: start; }
  .per4 .tm { color: var(--ink3); font-size: .82rem; margin: 6px 0 14px; }
  .per4.free .tm { color: var(--ink); font-weight: 600; }
  @media (max-width: 960px) { .tiers4, .pers4 { grid-template-columns: 1fr 1fr; } }
  @media (max-width: 640px) { .tiers4 { grid-template-columns: 1fr; gap: 22px; } .pers4 { grid-template-columns: 1fr 1fr; gap: 14px 10px; } .tier4 img { aspect-ratio: 16 / 10; } .per4 img { aspect-ratio: 1 / 1; } .per4 p { font-size: .84rem; } }
  .block h2 i, .hero.cover h1 i { font-style: italic; color: #8E8A84; } .hero.cover h1 i, .solo-dark h2 i { color: #E7D9A6; }
  .perks-ph { position: relative; } .perks-ph figcaption { position: absolute; left: 22px; right: 22px; bottom: 20px; color: #fff; font-family: var(--display); font-size: clamp(1.05rem, 1.5vw, 1.3rem); line-height: 1.3; z-index: 1; }
  .perks-ph::after { content: ""; position: absolute; inset: 40% 0 0; background: linear-gradient(0deg, rgba(0,0,0,.78), rgba(0,0,0,.4) 45%, rgba(0,0,0,0)); border-radius: 0 0 var(--radius) var(--radius); pointer-events: none; }
  .logo-s { padding-top: 0; overflow: hidden; } .logo2 { display: grid; grid-template-columns: minmax(0, 6fr) minmax(0, 6fr); gap: clamp(24px, 5vw, 72px); align-items: start; --edge: max(clamp(16px, 4vw, 48px), calc((100vw - 1280px) / 2 + clamp(16px, 4vw, 48px))); }
  .logo-t { padding-top: clamp(48px, 7vw, 100px); }
  .free { border-block: 1px solid var(--ink); padding: 18px 0; margin-bottom: 22px; } .free-b { font-family: var(--display); font-size: clamp(1.9rem, 3vw, 2.5rem); line-height: 1.1; margin: 6px 0 8px; } .free p:last-child { color: var(--ink2); max-width: 36em; margin: 0; }
  .ask { display: grid; } .ask .perk { border-top-color: var(--line); padding: 14px 0 12px; } .ask .perk h3 { font-size: 1.2rem; } .ask .perk p { font-size: .92rem; }
  .boxcut { margin: 0 0 0 calc(-1 * var(--edge)); } .boxcut img { width: 100%; height: auto; filter: drop-shadow(0 18px 24px rgba(0,0,0,.2)); }
  .terms2 { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: clamp(28px, 6vw, 96px); align-items: start; }
  .terms2 .perk h3 { font-size: 1.25rem; } .got { border-top: 1px solid var(--ink); padding-top: 14px; margin-top: 8px; } .got p:last-child { color: var(--ink3); font-size: .85rem; margin: 8px 0 0; }
  .qt { width: 100%; border-collapse: collapse; margin-top: 8px; font-size: .92rem; } .qt th { text-align: left; font-weight: 400; } .qt td { text-align: right; white-space: nowrap; padding-left: 14px; }
  .qt th, .qt td { padding-block: 8px; border-bottom: 1px solid var(--line); } .qt thead th { white-space: nowrap; font-size: .7rem; letter-spacing: .14em; text-transform: uppercase; color: var(--ink3); } .qt thead th:not(:first-child) { text-align: right; padding-left: 14px; }
  .qt tfoot th, .qt tfoot td { border-bottom: 1px solid var(--ink); font-family: var(--display); font-size: 1.25rem; }
  .tkv { margin: 0; } .tkv > div { display: grid; grid-template-columns: minmax(0, 150px) 1fr; gap: 18px; padding: 14px 0; border-top: 1px solid var(--line); } .tkv > div:last-child { border-bottom: 1px solid var(--line); }
  .tkv dt { font-family: var(--display); font-size: 1.2rem; line-height: 1.2; } .tkv dd { margin: 0; color: var(--ink2); font-size: .95rem; }
  .season { font-family: var(--display); font-size: clamp(1.5rem, 2.2vw, 2rem); line-height: 1.2; margin-top: 32px; max-width: 16em; } .season i { font-style: italic; color: #8E8A84; }
  @media (max-width: 960px) { .logo2, .terms2 { grid-template-columns: 1fr; } .boxcut { max-width: 520px; } .logo-t { padding-top: 0; } }
  @media (max-width: 640px) { .ask { grid-template-columns: 1fr; } .tkv > div { grid-template-columns: 1fr; gap: 4px; } }
  .photo-band h2 i { font-style: italic; color: #E7D9A6; }
  .w6g { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; } .w6 { position: relative; margin: 0; overflow: hidden; } .w6 img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; display: block; }
  .w6::after { content: ""; position: absolute; inset: 55% 0 0; background: linear-gradient(0deg, rgba(0,0,0,.62), rgba(0,0,0,0)); pointer-events: none; }
  .w6 figcaption { position: absolute; left: 22px; bottom: 18px; z-index: 1; color: #E7D9A6; font-family: var(--display); font-style: italic; font-size: clamp(1.5rem, 2.2vw, 2rem); line-height: 1; }
  .w6g.w4g { grid-template-columns: repeat(4, minmax(0, 1fr)); } .w4g .w6 img { aspect-ratio: 3 / 4; }
  @media (max-width: 960px) { .w6g.w4g { grid-template-columns: 1fr 1fr; } }
  @media (max-width: 640px) { .w6g { grid-template-columns: 1fr 1fr; gap: 8px; } .w6 figcaption { left: 12px; bottom: 12px; font-size: 1.2rem; } }
  @media (max-width: 640px) {
    .quote-band { display: none; }
    .as em { display: table; margin: 4px 0 0; }
    .tcs { gap: 0; } .tc { grid-template-columns: 104px 1fr; gap: 14px; padding: 16px 0; }
    .tc-ph { align-self: start; } .tc-im { min-height: 0; aspect-ratio: 4 / 5; } .tc-ph figcaption { display: none; }
    .tc-h { grid-template-columns: 1fr; min-height: 0; margin-bottom: 4px; } .tc-p { display: none; } .tc-t .eyebrow { font-size: .62rem; letter-spacing: .14em; white-space: normal; }
    .tc-t h3 { font-size: 1.25rem; } .tc-t > p:not(.eyebrow) { font-size: .84rem; min-height: 0; } .tc-b dd { min-height: 0; } .tc-t em { font-size: 1.35rem; padding-top: 8px; } .tc-t small { font-size: .74rem; min-height: 0; } .tc-t .tc-capm { display: block; margin-top: 2px; } .tc-t .eyebrow { min-height: 0; }
    .tc-b { margin-top: 8px; padding: 8px 0; gap: 6px; } .tc-b dt { font-size: .66rem; } .tc-b dd { font-size: .82rem; } .tc-t .more { margin-top: 8px; font-size: .84rem; }
  }
  .presets { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-bottom: 26px; }
  .preset { position: relative; display: grid; gap: 6px; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 18px 20px; cursor: pointer; text-align: left; font: inherit; color: inherit; }
  .preset:hover { border-color: var(--ink); }
  .preset.on { border-color: var(--ink); box-shadow: inset 0 0 0 1px var(--ink); }
  .preset h3 { font-size: 1.3rem; }
  .preset .pp { font-family: var(--display); font-size: 1.3rem; font-variant-numeric: lining-nums tabular-nums; }
  .preset .pp small { display: block; font-family: var(--body); font-size: .78rem; color: var(--ink2); }
  .preset p { color: var(--ink2); font-size: .88rem; }
  .preset .tag { position: absolute; top: 12px; right: 14px; font-size: .7rem; letter-spacing: .12em; text-transform: uppercase; color: var(--ink3); font-weight: 600; }
  .preset.on .tag { color: var(--ink); }
  .occs { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-bottom: 26px; }
  .occ { display: grid; grid-template-columns: 56px minmax(0, 1fr); gap: 12px; align-items: center; padding: 12px 14px; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); }
  .occ img { width: 56px; height: 56px; object-fit: cover; border-radius: calc(var(--radius) - 2px); background: #F1EEE8; }
  .occ b { font-family: var(--display); font-weight: 400; font-size: 1.05rem; line-height: 1.15; display: block; }
  .occ span { color: var(--ink2); font-size: .82rem; }
  .greet { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px 28px; max-width: 900px; }
  .greet .paper { position: static; width: auto; max-height: none; transform: rotate(-1.5deg); padding: 22px 22px 18px; }
  .greet .paper:nth-child(2n) { transform: rotate(1deg); }
  .greet .paper .t { font-size: 1.3rem; }
  .greet .paper small { display: block; font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: #8A8480; margin-bottom: 8px; }
  .whyhow { display: grid; grid-template-columns: minmax(0, 6fr) minmax(0, 5fr); gap: clamp(24px, 4vw, 64px); align-items: start; }
  .whyhow .why { grid-template-columns: 1fr 1fr; }
  .whyhow .steps { grid-template-columns: 1fr; gap: 16px; }
  .hero.main { padding-block: clamp(20px, 4vw, 52px) clamp(20px, 4vw, 44px); }
  .hero.main h1 { font-size: clamp(2rem, 3.4vw, 3.1rem); }
  .hero.main .lead { margin-top: 14px; font-size: 1.05rem; }
  .hero.main .cta { margin-top: 22px; }
  .hero.main figure img { aspect-ratio: 3 / 2; object-position: 50% 24%; }
  @media (max-width: 640px) { .hero.main .lead, .hero.main .fine { display: none; } .hero.main figure img { aspect-ratio: 2 / 1; object-position: 50% 58%; } }
  .cathead { display: flex; flex-wrap: wrap; align-items: center; gap: 12px 28px; margin-bottom: 18px; }
  .cathead h2 { font-size: clamp(1.5rem, 2.4vw, 2rem); margin-right: auto; }
  .cathead .filters { margin: 0; }
  @media (max-width: 960px) { .presets, .occs, .greet { grid-template-columns: 1fr 1fr; } .whyhow { grid-template-columns: 1fr; } }
  .hero p.m-only, p.m-only { display: none; }
  @media (max-width: 640px) { p.m-only { display: block; } .items.collapsed .item:nth-child(n+9) { display: none; } }
  figure.wide { margin: 0; } figure.wide img { width: 100%; aspect-ratio: 21 / 9; object-fit: cover; object-position: 50% 22%; border-radius: var(--radius); }
  @media (max-width: 640px) { figure.wide img { aspect-ratio: 4 / 3; } .filters .chips { padding-right: 12px; } }
  @media (max-width: 640px) { .presets, .greet, .occs { grid-template-columns: 1fr; } .occs { gap: 8px; } .occ { grid-template-columns: 48px 1fr; padding: 8px 12px; } .occ img { width: 48px; height: 48px; } .occ b { display: inline; } .occ span { display: inline; } .occ span::before { content: " — "; } .whyhow .why { grid-template-columns: 1fr; } }
"""

def plan_section():
    """Eight occasions with a recommended thing, three programmes as presets, the calculator with a silk / for-everyone split."""
    opts = "".join(team.opt(c) for c in CATALOG)
    occs = "".join(f'<div class="occ">{img(CAT[silk]["ph"], CAT[silk]["n"], sizes="56px")}<div><b>{short}</b><span>{shop.SHORT[silk]} · {price(CAT[silk]["p"])}</span></div></div>' for sid, short, _t, _d, p, a, silk, _n, _sh in STAGES)
    presets = "".join(f'<button type="button" class="preset" data-preset="{pid}" aria-pressed="false" aria-label="Програма {name}, {preset_range(rows)} на людину на рік"><span class="tag" aria-hidden="true">Обрати</span><h3>{name}</h3><span class="pp">{preset_range(rows)}<small>на людину на рік · роздрібні ціни</small></span><p>{who}</p></button>' for pid, name, who, rows in PRESETS)
    rows = "".join(f'''<div class="row" data-id="{sid}" data-share="{share}" data-silk="{silk}" data-neutral="{neu}">
        <input type="checkbox" id="c-{sid}" {"checked" if sid in ("first", "bday", "years") else ""} aria-label="{short}: враховувати в плані">
        <label class="n" for="c-{sid}">{short}</label>
        <span class="qty"><input type="number" min="0" inputmode="numeric" aria-label="{short}: скільки подарунків на рік" data-k="n"><small>шт. на рік</small></span>
        <span class="sel"><small>Шовкова річ</small><select aria-label="{short}: шовкова річ" data-k="silk">{opts}</select></span>
        <span class="sel"><small>Тим, хто не носить аксесуари</small><select aria-label="{short}: річ для тих, хто не носить аксесуари" data-k="neu">{opts}</select></span>
        <span class="sum"><b class="num" data-k="sum"></b><small data-k="split"></small></span></div>''' for sid, short, _t, _d, _p, _a, silk, neu, share in STAGES)
    js = """
    var P = __P__, N = __N__, SN = __SN__, PRE = __PRE__;
    var rows = [].slice.call(document.querySelectorAll('#rows .row[data-id]')), tpeople = document.getElementById('t-people'), tneu = document.getElementById('t-neu');
    function defaults() {
      var n = int(tpeople, 1);
      rows.forEach(function (r) { var q = r.querySelector('[data-k=n]'); if (!q.dataset.touched) q.value = Math.max(1, Math.round(n * parseFloat(r.dataset.share))); });
    }
    rows.forEach(function (r) { r.querySelector('[data-k=silk]').value = r.dataset.silk; r.querySelector('[data-k=neu]').value = r.dataset.neutral; });
    var state = { total: 0, gifts: 0, lines: [], n: 0, m: 0 };
    function calc() {
      var total = 0, g = 0, lines = [], n = int(tpeople, 1), m = Math.min(n, int(tneu, 0));
      document.getElementById('t-warn').textContent = int(tneu, 0) > n ? 'Людей у команді менше, ніж тих, хто не носить аксесуари, — рахуємо для ' + n + '.' : '';
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
      [].forEach.call(document.querySelectorAll('.preset'), function (b) { var on = b.dataset.preset === curPreset; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.querySelector('.tag').textContent = on ? 'Обрано ✓' : 'Обрати'; });
    }
    var curPreset = '';
    function applyPreset(id, quiet) {
      var n = int(tpeople, 1), cfg = PRE[id]; curPreset = id;
      rows.forEach(function (r) {
        var c = cfg[r.dataset.id]; r.querySelector('input[type=checkbox]').checked = !!c;
        if (c) { r.querySelector('[data-k=silk]').value = c[0]; r.querySelector('[data-k=neu]').value = c[1]; var q = r.querySelector('[data-k=n]'); q.value = Math.max(1, Math.round(n * c[2])); q.dataset.touched = '1'; }
      });
      calc();
      if (!quiet) document.getElementById('rows').scrollIntoView({ block: 'start', behavior: 'smooth' });
    }
    [].forEach.call(document.querySelectorAll('.preset'), function (b) { b.addEventListener('click', function () { applyPreset(b.dataset.preset); }); });
    function ptext() { return ['План на рік' + (curPreset ? ' · програма ' + document.querySelector('.preset.on h3').textContent : '') + ' · людей у команді: ' + state.n + (state.m ? ', із них не носять аксесуари: ' + state.m : '') + ' (роздрібні ціни obiimy.world, без доставки):'].concat(state.lines, ['Разом: ' + plain(fmt(state.total)) + ' · ' + gifts(state.gifts)]); }
    rows.forEach(function (r) {
      r.querySelector('[data-k=n]').addEventListener('input', function () { this.dataset.touched = '1'; curPreset = ''; calc(); });
      [].forEach.call(r.querySelectorAll('select'), function (s) { s.addEventListener('change', function () { curPreset = ''; calc(); }); });
      r.querySelector('input[type=checkbox]').addEventListener('change', function () { curPreset = ''; calc(); });
    });
    tpeople.addEventListener('input', function () { if (curPreset) applyPreset(curPreset, true); else { defaults(); calc(); } });
    tneu.addEventListener('input', calc);
    function mirror(a, b) { a.addEventListener('input', function () { if (b.value !== a.value) { b.value = a.value; b.dispatchEvent(new Event('input')); } }); }
    mirror(people, tpeople); mirror(tpeople, people); mirror(neu, tneu); mirror(tneu, neu);
    defaults(); calc();
    document.getElementById('send').addEventListener('click', function (e) { if (!state.gifts) { e.preventDefault(); return; } put(ptext(), state.gifts, fmt(state.total) + ' · ' + gifts(state.gifts) + ' на рік', 'План на рік'); });
    document.getElementById('copy').addEventListener('click', function () { if (state.gifts) copyText(ptext().join('\\n'), this); });
    """.replace("__P__", J({c["k"]: c["p"] for c in CATALOG})).replace("__N__", J({c["k"]: c["n"] for c in CATALOG})).replace("__SN__", J({c["k"]: team.SHORT_N.get(c["k"], c["n"]).lower() for c in CATALOG})).replace("__PRE__", J({pid: {k: list(v) for k, v in rows.items()} for pid, _n, _w, rows in PRESETS}))
    html = f'''
  <section class="block alt" id="plan"><div class="wrap">
    <div class="head"><p class="eyebrow">План на рік</p><h2>Вісім нагод — і скільки це коштує вашій команді</h2><p class="sub">Від першого дня до прощання. Оберіть програму або позначте нагоди самі — сума рахується за роздрібними цінами й додається до запиту одним натиском.</p></div>
    <div class="occs">{occs}</div>
    <div class="presets" role="group" aria-label="Програми на рік">{presets}</div>
    <div class="team"><label class="p" for="t-people">Людей у команді<input id="t-people" type="number" min="1" inputmode="numeric" value="40"></label>{team.split_field("t-neu", 16)}</div>
    <p class="warn" id="t-warn" aria-live="polite" style="margin:-10px 0 14px"></p>
    <div class="plan" id="rows">
      <div class="row hd" aria-hidden="true"><span></span><span>Нагода</span><span>На рік</span><span>Шовкова річ</span><span>Тим, хто не носить аксесуари</span><span style="text-align:right">Сума</span></div>
      {rows}
    </div>
    <div class="total"><div class="fig" aria-live="polite"><b id="tot" class="num">0 грн</b><span id="tot-s"></span></div>
      <div class="acts"><button class="btn btn-line" type="button" id="copy">Скопіювати план</button><a class="btn btn-gold" href="#request" id="send" role="button">Надіслати план на розрахунок</a></div></div>
    <p class="note">Програми — приклади: нагоди й речі можна замінити. Підписи «кому» — наші поради; фото — приклад принта. Точний розрахунок для вашої компанії надішлемо у відповідь на запит.</p>
  </div></section>'''
    return html, js

TIERS = [  # label, name, what is inside, price text, note, cut-out (same four gifts as in the deck, p. 3)
    ("Знак уваги", "Твіллі", "Шовкова стрічка 84 × 5: на шию, у волосся, на сумку. 38 принтів.", "1 600 грн", "довга 140 × 5 «Літній віночок» — 1 850 грн", "img/cut/zolote-tw-1.webp"),
    ("Тим, хто носить аксесуари", "Хустка й кільце", "Хустка 44 × 44 і кільце для хустки Gold — фіксує її на шиї чи сумці. Збираємо під замовлення.", "від 2 050 грн", "2 050 = хустка 1 600 + кільце 450; з двостороннім друком — 2 850 (2 400 + 450)", "img/cut/zolote-44-1.webp"),
    ("Для відпочинку", "Маска для сну й резинка", "Один принт, фірмове пакування Obiimy. Підходить і тим, хто не носить хустки.", "3 100 грн", "набором — на 300 грн менше, ніж окремо (2 700 + 700)", "img/cut/maskscr-litnie-pole.webp"),
    ("Ключовим людям", "Хустка й твіллі в коробці", "Один принт, святкова коробка. Майстер-клас від засновниці — за бажанням, узгоджуємо окремо.", "від 3 200 грн", "односторонній друк — 3 200, двосторонній — 3 600 грн", "img/cut/set-natkhnennia-box.webp"),
]
TPRICE = [(1600, None), (2050, 2850), (3100, None), (3200, 3600)]   # per person: price, ceiling (double-sided print) or None
INTRO = "Obiimy — «обійми»: український бренд шовкових хусток, твіллі й аксесуарів для сну. Засновниця й художниця — Світлана Сніжко. Нас продають INTERTOP, Hram, Be Brave (Канада) та UFD London; про нас пишуть LIGA.net та INSIDER UA."   # for a buyer who has never heard of the brand
ARGS = [  # why Obiimy — buyer arguments (deck p. 2, landing)
    ("Без розмірів і примірок", "Хустка, твіллі чи маска для сну підходять кожному — не треба збирати розміри, як для одягу."),
    ("Кожному — свій принт", "38 принтів твіллі, п’ять авторських колекцій. Один подарунок на всю команду — і кожному свій."),
    ("Шовк, який відчувають", "100% натуральний італійський шовк. Кутики кожної хустки кравчині обробляють вручну."),
    ("Український бренд з історією", "Заснований під час війни, виробництво повністю українське. Частина коштів від колекції «Співоча душа» — на гнізда для сиворакші з Червоної книги."),
    ("Ваш логотип — безкоштовно", "Подарункове пакування кожної речі й наліпка з логотипом вашої компанії всередині коробки — у кожному корпоративному замовленні."),
]
RANGE = [  # name, retail price, cut-out, «for everyone»
    ("Твіллі 84 × 5", "1 600 грн", "zolote-tw-1", 0), ("Хустка 44 × 44", "від 1 600 грн", "krok-44-1", 0), ("Хустка 65 × 65", "від 3 200 грн", "kolo-sontsia", 0),
    ("Хустка 88 × 88", "від 4 400 грн", "prob88", 0), ("Кільце для хустки", "450 грн", "ring-n", 0), ("Шовкова резинка", "700 грн", "scrunchie-pole", 0),
    ("Маска для сну", "2 700 грн", "mask-synii", 1), ("Закладка для книги", "800 грн", "bookmark-melodiia", 1), ("Наволочка 50 × 70", "від 4 200 грн", "pillow-tuman", 1),
    ("Твіллі й резинка", "набір — 2 200 грн", "twscr-makiv", 0)]
SIZE = {"zolote-tw-1": 34, "krok-44-1": 27, "kolo-sontsia": 32, "prob88": 37.5, "ring-n": 15, "scrunchie-pole": 29, "mask-synii": 34, "bookmark-melodiia": 33, "pillow-tuman": 37, "twscr-makiv": 34, "turban-bilyi": 31, "obruch": 27}   # mm on the long side in the deck; the landing keeps the proportions
RANGE_MORE = [("Тюрбан", "3 500 грн", "turban-bilyi", 0), ("Обруч для вмивання", "700 грн", "obruch", 0)]
ASK = [("Нашивна бирка", "Із логотипом компанії — на самій хустці чи твіллі."),
       ("Листівка й друковані матеріали", "Привітання вашими словами, з вашим логотипом."),
       ("Індивідуальний принт", "Для вашої компанії: кольори бренду, символи, історія.")]
STEPS = [("Нагода, кількість, дата", "Цього досить для першого листа. Якщо є — додайте бюджет на людину."),
         ("Добірка й розрахунок", "У відповідь — принти на вибір із фото й ціни окремими рядками."),
         ("Виготовлення й доставка", "Новою поштою — в офіс однією посилкою або кожному окремо.")]
TERMS = [("Строки", "Назвіть дату вручення — у відповіді напишемо, що встигаємо до неї. Терміново? Речі з наявності без наліпки відправляємо в день замовлення (до 16:00). Із наліпкою, наборами під замовлення й іншою персоналізацією — строк у робочих днях пишемо в розрахунку."),
         ("Доставка", "Новою поштою: в офіс однією посилкою або кожному окремо. Безкоштовно від 5 000 грн; як це діє для адресної розсилки кожному — напишемо в розрахунку. За кордон — за тарифами перевізника."),
         ("Оплата й документи", "Вкажіть у запиті юридичну особу та ЄДРПОУ, чи потрібен рахунок із ПДВ і які документи — форму оплати й документи підтвердимо в розрахунку."),
         ("Кількість", "Мінімальну кількість і наявність потрібного принта підтвердимо в розрахунку — напишіть, скільки людей у команді."),
         ("Вибір принтів", "Ви обираєте з добірки з фото: один принт на всіх або кожному свій. Від вас знадобиться логотип для наліпки."),
         ("Зразки", "Подивитися й потримати речі до замовлення — у шоурумі: {SHOWROOM}; пн–пт 10:00–18:00, сб 11:00–18:00.")]
TERMS = [(k, v.replace("{SHOWROOM}", team.SHOWROOM)) for k, v in TERMS]
EXAMPLE = [("Твіллі 84 × 5", 30, 1600), ("Сертифікат Obiimy", 20, 1500), ("Пакування й наліпка з логотипом", 30, 0), ("Доставка в офіс", 1, 0)]   # sample quote: mixed team of 50, retail prices
def money(n): return f"{n:,}".replace(",", " ")
def bud(i, n):   # the range has a ceiling: «від» alone is not a budget
    lo, hi = TPRICE[i]; return f"<span>від {money(lo * n)}</span><span>до {money(hi * n)}</span>" if hi else money(lo * n)
PERS = [  # name, text, terms, photo
    ("Пакування й наліпка", "Подарункове пакування кожної речі та наліпка з вашим логотипом усередині коробки.", "Безкоштовно · у кожному корпоративному замовленні", "photo/box-gold.jpg"),
    ("Бирка з логотипом", "Нашивна бирка з логотипом компанії на самій хустці чи твіллі.", "Строки й вартість — у розрахунку", "photo/dotyk-3.webp"),
    ("Друковані матеріали", "Листівка з привітанням — з вашим логотипом і текстом.", "Формат і вартість — у розрахунку", "img/sets/cert-2000.webp"),
    ("Індивідуальний принт", "Принт, створений для вашої компанії: кольори бренду, символи, історія.", "Тираж, строки й вартість — у розрахунку", "photo/vyr-flat.webp"),
]
PERKS = [
    ("Унікальні принти", "Авторські малюнки засновниці Світлани Сніжко та українських художниць. Кожному в команді — свій принт із добірки."),
    ("Якість, яку відчувають", "100% натуральний італійський шовк, кутики кожної хустки — вручну. Повністю українське виробництво."),
    ("Бренд, який упізнають", "INTERTOP і Hram в Україні, Be Brave у Канаді, UFD London. Писали LIGA.net та INSIDER UA."),
    ("Є речі для всіх", "Маска для сну, закладка, наволочка, сертифікат — і тим, хто аксесуари не носить."),
]
SOLO = [  # print, state (press release), formats seen on the shoot, price from (SITE-FACTS: 2D 44 — 2 400, 65 — 4 800, 88 — 6 600; twilly 1 600), lifestyle photo, flat photo
    ("Іскра", "Внутрішня енергія, сміливість бути помітною.", "Твіллі — 1 600 · хустка 65 × 65 — 4 800 грн", 1600, "photo/solo/iskra-65-2.webp", "img/cut/iskra-65-5.webp"),
    ("Флірт", "Віра в перемогу, оптимізм, невимушена жіночність.", "Твіллі — 1 600 · хустка 65 × 65 — 4 800 · резинка — 700 грн", 700, "photo/solo/flirt-tw-4.webp", "img/cut/flirt-65-1.webp"),
    ("Пульс", "Природна сила й внутрішня опора.", "Твіллі — 1 600 · хустка 44 × 44 — 2 400 грн", 1600, "photo/solo/puls-44-4.webp", "img/cut/puls-44-1.webp"),
    ("Золоте світло", "Моменти ясності, коли все стає на свої місця.", "Твіллі — 1 600 · хустка 44 × 44 — 2 400 грн", 1600, "photo/solo/zolote-44-3.webp", "img/cut/zolote-44-1.webp"),
    ("Авантюра", "Готовність виходити за межі звичного.", "Твіллі — 1 600 · хустка 88 × 88 — 6 600 грн", 1600, "photo/solo/avantiura-88-2.webp", "img/cut/avantiura-88-1.webp"),
    ("Тиша всередині", "Баланс і здатність чути себе серед шуму.", "Твіллі — 1 600 · хустка 88 × 88 — 6 600 грн", 1600, "photo/solo/tysha-88-2.webp", "img/cut/tysha-88-1.webp"),
    ("Сміливий крок", "Рішення рухатися вперед, довіра до себе.", "Твіллі — 1 600 · хустка 44 × 44 — 2 400 грн", 1600, "photo/solo/krok-44-2.webp", "img/cut/krok-44-1.webp"),
]
ASSORT = [  # the whole range: name, price from (retail, SITE-FACTS), photo
    ("Твіллі 84 × 5", 1600, "img/cut/zolote-tw-1.webp"),
    ("Хустка 44 × 44", 1600, "img/cut/zolote-44-1.webp"),
    ("Хустка 65 × 65", 3200, "img/cut/kolo-sontsia.webp"),
    ("Хустка 88 × 88", 4400, "img/cut/prob88.webp"),
    ("Шовкова резинка", 500, "img/cut/scrunchie-pole.webp"),
    ("Маска для сну", 2700, "img/cut/mask-svoboda.webp"),
    ("Закладка для книги", 800, "img/cut/bookmark-melodiia.webp"),
    ("Наволочка 50 × 70", 4200, "img/cut/pillow-tuman.webp"),
    ("Тюрбан", 3500, "img/cut/turban-bilyi.webp"),
    ("Обруч для вмивання", 700, "img/cut/obruch.webp"),
    ("Подарункові набори", 1250, "img/cut/twscr-makiv.webp"),
    ("Сертифікат", 1000, "img/sets/cert-2000.webp"),
]
SETS4 = [  # one page each, in the deck and on the site. Facts: SITE-FACTS (sizes, prices, prints) and the client's letter (packaging). Photos: product + the SOLO shoot
    dict(slug="b2b-set-twilly", b50="80 000 грн", short="Твіллі", name="Твіллі — подарунок на всю команду", lb="Знак уваги · 01", pr="1 600 грн", prnote="роздрібна ціна; довга 140 × 5 «Літній віночок» — 1 850 грн",
         lead="Шовкова стрічка 84 × 5 см. Універсальний подарунок із каталогу: на шию, у волосся, на сумку, на зап’ястя чи поясом. 38 авторських принтів — для кожного в команді можна обрати свій.",
         hero=("photo/solo/zolote-tw-2.webp", "Твіллі «Золоте світло» на ручці сумки, набережна", "50% 35%"),
         gal=[("photo/solo/avantiura-tw-3.webp", "У волоссі — твіллі «Авантюра»", "60% 15%"), ("photo/solo/krok-tw-3.webp", "З келихом — твіллі «Сміливий крок»", "50% 25%"), ("photo/solo/flirt-tw-4.webp", "Поясом на тренчі — «Флірт»", "50% 40%"), ("img/twilly-zolote.webp", "Твіллі «Золоте світло», 84 × 5", "")],
         inside=[("Що всередині", "Шовкова твіллі 84 × 5 см, авторський принт"), ("Шовк", "100% натуральний італійський шовк"), ("Принти", "38 принтів, зокрема з нової колекції SOLO"), ("Пакування", "Подарункове пакування Obiimy — безкоштовно; наліпка з вашим логотипом усередині"), ("Привітання", "Листівка з вашим текстом і логотипом — формат у розрахунку"), ("Кому", "Усій команді, новим співробітникам, гостям події")],
         ways=[("На шиї", "Вузол або бант під комір — класичний спосіб."), ("У волоссі", "Вплітається в косу, зав’язується на хвості чи пучку."), ("На сумці", "Обмотується навколо ручки — помітна деталь образу."), ("Поясом", "На тренчі чи сукні — як на зйомці SOLO.")],
         who="Коли треба один подарунок для всіх — і щоб кожен отримав свій принт."),
    dict(slug="b2b-set-scarf-ring", b50="від 102 500 грн", short="Хустка й кільце", name="Хустка й кільце — готовий образ", lb="Тим, хто носить аксесуари · 02", pr="від 2 050 грн", prnote="2 050 = хустка 1 600 + кільце Gold 450; з двостороннім друком — 2 850 (2 400 + 450)",
         lead="Невелика шовкова хустка 44 × 44 і кільце для хустки Gold: воно фіксує хустку на шиї, сумці чи поясі. Збираємо під замовлення; строк — у розрахунку.",
         hero=("photo/solo/zolote-44-3.webp", "Хустка «Золоте світло» 44 × 44 на шиї, чорний жакет", "50% 20%"),
         gal=[("photo/solo/krok-44-4.webp", "«Сміливий крок» на шиї, із сумкою", "50% 20%"), ("photo/solo/krok-44-2.webp", "«Сміливий крок» на шиї", "50% 20%"), ("photo/solo/zolote-44-1.webp", "Хустка «Золоте світло» 44 × 44", ""), ("photo/hratsiia-flat.webp", "Хустка «Грація» 44 × 44", "")],
         inside=[("Що всередині", "Хустка 44 × 44 см і кільце для хустки Gold, 450 грн — п’ять моделей на вибір"), ("Шовк", "100% натуральний італійський шовк, кутики оброблені вручну"), ("Друк", "Хустка з одностороннім друком — 1 600 грн, із двостороннім — 2 400 грн"), ("Принти", "Із чотирьох колекцій і SOLO — наявність у 44 × 44 підтвердимо в добірці"), ("Пакування", "Подарункове пакування Obiimy — безкоштовно; наліпка з логотипом усередині"), ("Кому", "Тим, хто носить аксесуари; ключовим людям")],
         ways=[("На шиї", "Трикутником або скрученою стрічкою — кінці протягнуті в кільце замість вузла."), ("На сумці", "Складена в стрічку — на ручці."), ("На зап’ясті", "Як браслет — для теплого сезону."), ("У волоссі", "Пов’язка чи стрічка на хвості.")],
         who="Кільце підказує, як носити."),
    dict(slug="b2b-set-mask", b50="155 000 грн", name="Маска й резинка — набір про відпочинок", short="Маска для сну й резинка", lb="Для відпочинку · 03", pr="3 100 грн", prnote="роздрібна ціна набору — на 300 грн менше, ніж окремо (маска 2 700 + резинка 700)",
         lead="Шовкова маска для сну й резинка в одному принті, у фірмовому пакуванні Obiimy. Маску носять щоночі, резинку — щодня. Підходить і тим, хто не носить хустки.",
         hero=("photo/solo/flirt-scr-3.webp", "Шовкова резинка — приклад; принти набору нижче", "50% 20%"),
         gal=[("img/mask-svoboda.webp", "Маска для сну «Свобода»", ""), ("img/sets/maskscr-litnie-pole.webp", "Набір «Літнє поле»: маска й резинка в коробці", ""), ("img/mask-vpevnenist.webp", "Маска для сну «Впевненість»", ""), ("img/sets/maskscr-enerhiia.webp", "Набір «Енергія»: маска й резинка", "")],
         inside=[("Що всередині", "Маска для сну та шовкова резинка в одному принті"), ("Шовк", "100% натуральний італійський шовк"), ("Принти", "Літнє поле, Енергія, Свобода, Впевненість, Піднесення, Мелодія двох, Сміливість, Серцебиття"), ("Пакування", "Фірмове пакування Obiimy — безкоштовно; наліпка з логотипом усередині"), ("Підходить", "І тим, хто не носить аксесуари: маска — для дому"), ("Кому", "Колегам, які не носять хустки; віддаленим командам; до подяки за проєкт. Чоловікам — маска окремо")],
         ways=[("Маска", "100% шовк — м’який до шкіри; для сну й подорожей."), ("Резинка", "Шовк — м’який до волосся; тримає хвіст і пучок."), ("Один принт", "Маска й резинка — у парі, як набір."), ("Коробка", "Приїздить готовим подарунком.")],
         who="Подарунок, що каже «відпочинь»."),
    dict(slug="b2b-set-scarf-twilly", b50="від 160 000 грн", short="Хустка й твіллі", name="Хустка й твіллі — пара в одній коробці", lb="Ключовим людям · 04", pr="від 3 200 грн", prnote="односторонній друк — 3 200, двосторонній — 3 600",
         lead="Хустка 44 × 44 і твіллі в одному принті: носять разом або окремо. Для керівників, ключових людей, до річниці в компанії.",
         hero=("photo/solo/zolote-44-2.webp", "Набір «Впевненість»: твіллі у хвості та хустка 44 × 44", "50% 20%"),
         gal=[("photo/solo/zolote-44-4.webp", "Хустка «Золоте світло» поясом на чорному", "50% 40%"), ("photo/solo/zolote-tw-3.webp", "Твіллі «Золоте світло»", ""), ("img/sets/tw44-natkhnennia.webp", "Набір «Натхнення»: хустка й твіллі в коробці", ""), ("photo/solo/zolote-44-2.webp", "«Золоте світло» на шиї, чорний жакет", "50% 20%")],
         inside=[("Що всередині", "Хустка 44 × 44 і твіллі 84 × 5 в одному принті"), ("Майстер-клас", "Від засновниці Світлани Сніжко — за бажанням; формат, дату й вартість узгодимо окремо"), ("Кому", "Керівникам, ключовим людям, до річниці в компанії"), ("Шовк і друк", "100% натуральний італійський шовк, кутики вручну; односторонній — 3 200 грн, двосторонній — 3 600 грн"), ("Принти", "18 принтів: 11 — по 3 200 грн, 7 із двостороннім друком — по 3 600 грн, зокрема «Золоте світло»"), ("Пакування", "Святкова коробка Obiimy; наліпка з логотипом усередині — безкоштовно")],
         ways=[("Пара", "Хустка на шиї, твіллі на сумці — один принт у двох деталях."), ("Окремо", "Два подарунки з однієї коробки — на будні й на вихід."), ("Майстер-клас", "За бажанням — від засновниці; формат, дату й вартість узгодимо окремо."), ("Коробка", "Святкова коробка Obiimy.")],
         who="Коли подарунок має сказати більше, ніж річ."),
]
PROD = [3, 2, 1, 2]
ALT = {"photo/site/solo-zolote-svitlo-84x5-02.jpg": "На фото — твіллі «Золоте світло»", "photo/site/solo-flirt-84x5-01.jpg": "Твіллі «Флірт» у зачісці", "photo/site/solo-smilyvyi-krok-84x5-03.jpg": "Твіллі «Сміливий крок» на моделі",
       "photo/solo/krok-44-2.webp": "На фото — «Сміливий крок» 44 × 44, двосторонній друк, зав’язана вузлом; у подарунку з кільцем — 2 850 грн", "img/cut/ring-in-use.webp": "Кільце «Н стиль» Gold тримає хустку замість вузла", "img/cut/men-mask.webp": "Чоловікам — маска окремо, 2 700 грн; на фото — «Синій»", "img/cut/duo-hratsiia-ring.webp": "Хустка «Грація» 44 × 44 і кільце «Н стиль» Gold", "photo/solo/flirt-scr-3.webp": "Шовкова резинка на волоссі; на фото — «Флірт», приклад", "photo/site/solo-zolote-svitlo-44kh44-02.jpg": "Хустка «Золоте світло» 44 × 44, двосторонній друк — 2 400 грн", "photo/site/solo-smilyvyi-krok-44kh44-02.jpg": "Хустка «Сміливий крок» 44 × 44 на моделі",
       "photo/site/mask-vpevnenist-04.jpg": "На фото — маска для сну «Впевненість»", "photo/site/set-ta-rezynka-litnie-pole-04.jpg": "Набір «Літнє поле»: маска для сну в коробці Obiimy", "photo/site/set-ta-rezynka-litnie-pole-03.jpg": "Набори «Літнє поле»: маски й резинки",
       "photo/site/set-tvilli-845-ta-khustky-4444-natkhne-04.jpg": "На фото — набір «Натхнення»: твіллі в зачісці", "photo/site/set-tvilli-845-ta-khustky-4444-smilyvy-02.jpg": "Твіллі з набору «Сміливий дотик» у косі", "photo/site/set-tvilli-845-ta-khustky-4444-vpevnen-02.jpg": "Набір «Впевненість» на моделі",
       "img/cut/zolote-tw-1.webp": "Твіллі «Золоте світло», 84 × 5", "img/cut/zolote-44-1.webp": "Хустка «Золоте світло» 44 × 44", "img/cut/hratsiia-flat.webp": "Хустка «Грація» 44 × 44 — 1 600 грн", "img/cut/maskscr-litnie-pole.webp": "Набір «Літнє поле»: маска й резинка в коробці", "img/cut/set-natkhnennia-box.webp": "Набір «Натхнення»: хустка й твіллі в коробці"}
for _i, _S in enumerate(SETS4):
    _f, _p = cast(f"H{_i + 1}", _S["hero"][0], _S["hero"][2]); _S["hero"] = (_f, ALT.get(_f, _S["hero"][1]), _p)
    _f, _p = cast(f"M{_i + 1}", _S["gal"][0][0], _S["gal"][0][2]); _S["gal"][0] = (_f, ALT.get(_f, _S["gal"][0][1]), _p)
    _f, _p = cast(f"P{_i + 1}", _S["gal"][PROD[_i]][0], _S["gal"][PROD[_i]][2]); _S["gal"][PROD[_i]] = (_f, ALT.get(_f, _S["gal"][PROD[_i]][1]), _p)
    _S["tier"] = cast(f"T{_i + 1}", _S["gal"][0][0], _S["gal"][0][2])

WAYS = [  # «Як носити» — one print across all shots, like the brand banner (t05-avantiura-ways): hustka «Авантюра» 88 × 88 and twilly
    ("У волоссі", "«Авантюра»", "photo/solo/avantiura-tw-3.webp", "50% 50%"),
    ("На шиї", "«Флірт»", "photo/solo/flirt-tw-3.webp", "50% 50%"),
    ("На сумці", "«Золоте світло»", "photo/solo/zolote-tw-2.webp", "40% 50%"),
    ("Поясом", "«Сміливий крок»", "photo/solo/krok-tw-4.webp", "45% 50%"),
]
SZ = "(max-width: 640px) 100vw, (max-width: 960px) 50vw, 25vw"
SZ6 = "(max-width: 640px) 50vw, (max-width: 960px) 33vw, 16vw"

def perks_section():
    cards = "".join(f'<div class="perk"><b class="n">0{i + 1}</b><h3>{b}</h3><p>{t}</p></div>' for i, (b, t) in enumerate(ARGS))
    return f'''
  <section class="block" id="why"><div class="wrap perks">
    <figure class="perks-ph">{img(PERKS_PH[0], "Модель у шовковій хустці Obiimy", sizes="(max-width: 960px) 100vw, 45vw", style=pos(PERKS_PH[1]))}<figcaption>«Кожна коробочка — це обійми, що нагадують: ти варта краси»</figcaption></figure>
    <div><div class="head"><p class="eyebrow">Чому Obiimy</p><h2>Подарунок, що носять, <i>а не кладуть у шухляду</i></h2><p class="sub">{INTRO}</p></div><div class="perks-l">{cards}</div>
      <p class="note">Зразки можна побачити й потримати в шоурумі: {team.SHOWROOM}.</p></div>
  </div></section>'''

_CARDS = [cast(f"S{i + 1}", f, p) for i, (f, p) in enumerate(zip(["photo/solo/iskra-65-2.webp", "photo/solo/flirt-tw-4.webp", "photo/solo/puls-44-2.webp", "photo/solo/zolote-44-5.webp", "photo/solo/avantiura-tw-4.webp", "photo/solo/tysha-88-3.webp", "photo/solo/krok-44-2.webp"], ["50% 20%", "50% 35%", "50% 15%", "50% 12%", "50% 15%", "50% 20%", "50% 20%"]))]
CARD_PH = [f for f, p in _CARDS]; CARD_POS = [p for f, p in _CARDS]
HERO = cast("D01", "photo/solo/zolote-44-5.webp", "50% 28%"); PERKS_PH = cast("D04", "photo/solo/avantiura-tw-1.webp", "50% 20%")
SOLO_BIG = cast("D05a", "photo/solo/tysha-88-2.webp", "50% 30%"); SOLO_S1 = cast("D05b", "photo/solo/puls-44-4.webp", "50% 20%"); SOLO_S2 = cast("D05c", "photo/solo/iskra-65-3.webp", "50% 50%")
QUOTE_PH = cast("D07", "photo/solo/zolote-44-4.webp", "50% 35%"); PERS_PH = cast("D16", "photo/box-gold.jpg", "50% 45%"); BAND_PH = cast("L-band", "photo/solo/krok-tw-3.webp", "50% 30%")

def solo_section():
    """Black presentational block: manifesto of the collection (press release), cinematic shots, the seven prints as tall cards."""
    cards = "".join(f'<div class="pc"><div class="pc-ph">{img(CARD_PH[i], f"Принт «{n}» на моделі", sizes="(max-width: 640px) 62vw, (max-width: 960px) 50vw, 22vw", style=pos(CARD_POS[i]), cls="m")}<div class="pc-t"><b>{n}</b><span>{st}</span></div></div><div class="pc-b">{img(fl, "", sizes="64px", cls="fl")}<small>{fm}</small></div></div>' for i, (n, st, fm, pr, ph, fl) in enumerate(SOLO))
    return f'''
  <section class="block solo-dark" id="solo"><div class="wrap">
    <div class="sd-top">
      <div class="sd-t"><p class="eyebrow">Нова колекція · 2026</p><h2>SOLO.<br>Шлях до себе</h2><p class="sd-slogan">Шовкова свобода: жіноча сила крізь десятиліття</p>
        <p>Натхнення — обкладинки модних журналів 40–50-х: змінювалися епохи й силуети, а хустка залишалася поруч. Сім авторських принтів — сім етапів шляху жінки до себе. Натуральний шовк, двосторонній друк.</p>
        <p class="sd-note">Для команди: кожному — свій принт, під стан, який хочете побажати, або один принт на всіх.</p>
        <p><a class="btn btn-line sd-cta" href="#request">Добірка SOLO для команди →</a></p></div>
      <figure class="sd-ph">{img(SOLO_BIG[0], "Колекція SOLO на моделі", sizes="(max-width: 960px) 100vw, 50vw", style=pos(SOLO_BIG[1]))}{img(SOLO_S1[0], "Колекція SOLO", sizes="(max-width: 960px) 50vw, 25vw", style=pos(SOLO_S1[1]))}{img(SOLO_S2[0], "Колекція SOLO", sizes="(max-width: 960px) 50vw, 25vw", style=pos(SOLO_S2[1]))}</figure>
    </div>
    <div class="sd-hd"><h3>Сім принтів — сім станів</h3><p>Для HR стан принта — готовий текст привітання: «Сміливий крок» — на підвищення, «Тиша всередині» — після складного кварталу. Ціни роздрібні, двосторонній друк.</p></div>
    <div class="pcs">{cards}<a class="pc pc-cta" href="#request"><b>Кожному — свій принт</b><span>Або один на всіх. Надішлемо добірку SOLO з фото й цінами на вашу кількість.</span><em>Отримати добірку →</em></a></div>
  </div></section>'''

def quote_section():
    return f'''
  <section class="quote-band" aria-label="SOLO">{img(QUOTE_PH[0], "Колекція SOLO", sizes="100vw", style=pos(QUOTE_PH[1]))}
    <div class="qb-t"><div class="wrap"><div class="qb-in"><p class="bigq">«Я є.<br>Я продовжую жити.<br>Я обираю себе»</p><p>Для жінки краса — це спосіб зберегти себе. Улюблена сукня, шовкова хустка, червона помада — маленькі акти свободи.</p><p class="eyebrow">SOLO. Шлях до себе</p></div></div></div>
  </section>'''

def ways_section():
    """«Одна твіллі — чотири образи» — right after the packaging, on paper, next to the six looks of a scarf (deck p. 9–10)."""
    ways = "".join(f'<figure class="w6">{img(ph, f"{n} — шовкова твіллі Obiimy, принт {t}", sizes="(max-width: 640px) 50vw, 25vw", style=pos(ps))}<figcaption>{n}</figcaption></figure>' for n, t, ph, ps in WAYS)
    return f'''
  <section class="block alt" id="ways"><div class="wrap">
    <div class="head"><p class="eyebrow">Як носити</p><h2>Одна твіллі — <i>чотири образи</i></h2><p class="sub">Твіллі — шовкова стрічка 84 × 5 см, найдоступніший із чотирьох подарунків: 1 600 грн. Її носять у волоссі, на шиї, на сумці й поясом. На фото — принти SOLO: «Авантюра», «Флірт», «Золоте світло», «Сміливий крок».</p></div>
    <div class="w6g w4g">{ways}</div>
  </div></section>'''

W6 = [("На сумці", "62% 50%"), ("На голові", "66% 50%"), ("На шиї", "56% 50%"), ("Поясом", "50% 50%"), ("Банданою", "50% 50%"), ("Топом", "56% 50%")]   # the client's collage, photo/ways
def scarf_ways_section():
    """«Одна хустка — шість образів» — the same six frames as on page 10 of the deck."""
    tiles = "".join(f'<figure class="w6">{img(f"photo/ways/ways-{i + 1}.jpg", f"{n} — шовкова хустка Obiimy", sizes="(max-width: 640px) 50vw, 33vw", style=pos(ps))}<figcaption>{n}</figcaption></figure>' for i, (n, ps) in enumerate(W6))
    return f'''
  <section class="block" id="scarf-ways"><div class="wrap">
    <div class="head"><p class="eyebrow">Як носити</p><h2>Одна хустка — <i>шість образів</i></h2><p class="sub">Шовкову хустку носять на сумці, на голові й на шиї, поясом, банданою чи топом. Хустки 44 × 44 — від 1 600 грн, 65 × 65 — від 3 200 грн, 88 × 88 — від 4 400 грн; який формат під який спосіб — підкажемо в добірці.</p></div>
    <div class="w6g">{tiles}</div>
  </div></section>'''

def assort_section():
    tiles = "".join(f'<div class="as"><div class="as-im">{img(f"img/cut/{c}.webp", n, sizes=SZ6, style=f"width:{round(SIZE[c] / 37.5 * 100)}%")}</div><b>{n}</b><span class="num">{pr}{" <em>усім</em>" if a else ""}</span></div>' for n, pr, c, a in RANGE + RANGE_MORE)
    return f'''
  <section class="block" id="range"><div class="wrap">
    <div class="head"><p class="eyebrow">Асортимент</p><h2>Усе, з чого можна <i>зібрати подарунок</i></h2><p class="sub">Роздрібні ціни obiimy.world. Будь-яку річ можна додати в коробку або зробити окремим подарунком. «Усім» — речі для тих, хто не носить аксесуари.</p></div>
    <div class="assort">{tiles}</div>
    <p class="note" style="margin-top:18px">Також: сертифікат Obiimy на 1 000–4 000 грн — електронний або фізичний, на будь-який товар, діє 3 місяці · набори резинок — від 1 250 грн.</p>
  </div></section>'''

def tiers_section():
    cards = "".join(f'<div class="tier4"><b class="n">0{i + 1}</b>{img(ph, n, sizes=SZ)}<p class="eyebrow">{lb}</p><h3>{n}</h3><p>{t}</p><div class="pz"><b class="rrp num">{pr}</b>{f"<small>{note}</small>" if note else ""}<a class="more" href="{SETS4[i]["slug"]}">Детальніше →</a></div></div>' for i, (lb, n, t, pr, note, ph) in enumerate(TIERS))
    return f'''
  <section class="block alt" id="tiers"><div class="wrap">
    <div class="head"><p class="eyebrow">Ціновий діапазон</p><h2>Чотири рівні подарунка — від 1 600 до 3 200 грн на людину</h2><p class="sub">Якщо для бюджету потрібна одна цифра — ось чотири точки: від однієї стрічки до набору з хусткою й твіллі. Ціни роздрібні, obiimy.world.</p></div>
    <div class="tiers4">{cards}</div>
    <p class="note" style="margin-top:16px">Команді з 50 людей — від 80 000 до 160 000 грн за речі за роздрібними цінами; доставку й майстер-клас рахуємо окремо. Склад можна змінити — перерахуємо в розрахунку.</p>
  </div></section>'''

def pos(v): return f"object-position:{v}" if v else ""

def tiers_a():
    """A — editorial: one big model photo, four rows with product thumbs."""
    rows = "".join(f'<a class="tr" href="{S["slug"]}">{img(ph, n, sizes="96px")}<div><p class="eyebrow">{lb}</p><b>{n}</b><span>{t}</span></div><em class="num">{pr}</em></a>' for (lb, n, t, pr, note, ph), S in zip(TIERS, SETS4))
    return f'''
  <section class="block alt" id="tiers"><div class="wrap">
    <div class="head"><p class="eyebrow">Ціновий діапазон · варіант A</p><h2>Чотири рівні подарунка — від 1 600 до 3 200 грн</h2><p class="sub">Від однієї стрічки до набору з хусткою, твіллі й майстер-класом. Ціни роздрібні, obiimy.world.</p></div>
    <div class="ta"><figure>{img("photo/solo/zolote-44-3.webp", "Хустка «Золоте світло» на шиї", sizes="(max-width: 960px) 100vw, 45vw", style="object-position:50% 20%")}</figure><div class="ta-l">{rows}</div></div>
  </div></section>'''

def tiers_b():
    """B — four tall model photos with the price on the photo."""
    cards = "".join(f'<a class="tb" href="{S["slug"]}">{img(S["hero"][0], n, sizes=SZ, style=pos(S["hero"][2]))}<div class="tb-t"><p class="eyebrow">0{i + 1} · {lb}</p><b>{n}</b><em class="num">{pr}</em></div>{img(ph, "", sizes="80px", cls="tb-p")}</a>' for i, ((lb, n, t, pr, note, ph), S) in enumerate(zip(TIERS, SETS4)))
    return f'''
  <section class="block" id="tiers-b"><div class="wrap">
    <div class="head"><p class="eyebrow">Ціновий діапазон · варіант B</p><h2>Чотири рівні подарунка — від 1 600 до 3 200 грн</h2><p class="sub">Від однієї стрічки до набору з хусткою, твіллі й майстер-класом. Ціни роздрібні, obiimy.world.</p></div>
    <div class="tbs">{cards}</div>
  </div></section>'''

OFFER_CUT = ["krok-tw-1", "duo-hratsiia-ring", "maskscr-litnie-pole", "set-natkhnennia-box"]
OFFER_CAP = ["На фото — твіллі «Сміливий крок»", "На фото — «Сміливий крок» 44 × 44, двосторонній друк, зав’язана вузлом; із кільцем — 2 850 грн", "На фото — маска «Впевненість»", "На фото — набір «Натхнення»"]   # the cut-out rhymes with the photo next to it
def offer_card(i, T, S):
    lb, n, t, pr, note, ph = T
    b3 = "".join(f'<div><dt>{k} людей</dt><dd class="num">{bud(i, k)}</dd></div>' for k in (20, 50, 100))
    return (f'<a class="tc" href="{S["slug"]}"><figure class="tc-ph"><div class="tc-im">{img(S["tier"][0], ALT.get(S["tier"][0], n), sizes="(max-width: 640px) 100vw, 25vw", style=pos(S["tier"][1]))}</div><figcaption>{OFFER_CAP[i]}</figcaption></figure>'
            f'<div class="tc-t"><p class="eyebrow">0{i + 1} · {lb}</p><div class="tc-h"><h3>{n}</h3>{img(f"img/cut/{OFFER_CUT[i]}.webp", "", sizes="96px", cls="tc-p")}</div><p>{t}</p>'
            f'<em class="num">{pr}</em><small>{note}</small><small class="tc-capm">{OFFER_CAP[i]}.</small><dl class="tc-b" aria-label="Бюджет команди, грн">{b3}</dl><span class="more">{"Що всередині й як носити →" if i < 2 else "Що всередині →"}</span></div></a>')

def tiers_c():
    """The offer right after the cover: four gifts, price per person, budgets for 20 / 50 / 100 people (deck p. 3)."""
    cards = "".join(offer_card(i, T, S) for i, (T, S) in enumerate(zip(TIERS, SETS4)))
    return f'''
  <section class="block alt" id="tiers"><div class="wrap">
    <div class="head"><p class="eyebrow">Чотири подарунки</p><h2>Що в коробці — <i>і скільки це коштує</i></h2><p class="sub">Базові роздрібні ціни obiimy.world на людину, без акцій сайту (жовтень 2026); бюджет команди — у гривнях, ціну для вашої кількості підтвердимо в розрахунку. У кожному подарунку — подарункове пакування й наліпка з вашим логотипом, безкоштовно.</p></div>
    <div class="tcs">{cards}</div>
    <div class="cond" style="margin-top:clamp(28px,4vw,44px)"><div><b>Змішана команда</b><span>Тим, хто не носить аксесуари, — маска для сну (2 700 грн), закладка для книги (800 грн), наволочка (від 4 200 грн) або сертифікат на 1 000–4 000 грн. Усе — в одному розрахунку.</span></div>
      <div><b>До 1 000 грн на людину</b><span>Шовкова резинка — 700 грн, закладка для книги — 800 грн, сертифікат Obiimy — 1 000 грн.</span></div>
      <div><b>Приклад: 50 людей</b><span>30 твіллі (48 000 грн) + 20 сертифікатів по 1 500 грн (30 000 грн) = 78 000 грн за роздрібними цінами. Точну суму з персоналізацією й доставкою пишемо в розрахунку окремими рядками.</span></div></div>
    <p style="margin-top:26px"><a class="btn btn-gold" href="#request">Отримати розрахунок</a></p>
  </div></section>'''

def personal_section():
    cards = "".join(f'<div class="perk"><b class="n">0{i + 1}</b><h3>{n}</h3><p>{t}</p></div>' for i, (n, t) in enumerate(ASK))
    return f'''
  <section class="block alt logo-s" id="logo"><div class="wrap logo2">
    <figure class="boxcut">{img("img/cut/box-gold.webp", "Подарункове пакування Obiimy: коробка, папір тішью, хустка й твіллі в одному принті", sizes="(max-width: 960px) 100vw, 45vw")}</figure>
    <div class="logo-t"><div class="head"><p class="eyebrow">Персоналізація</p><h2>Ваш логотип — <i>від наліпки до власного принта</i></h2></div>
      <div class="free"><p class="eyebrow">У кожному корпоративному замовленні</p><p class="free-b">Безкоштовно</p><p>Подарункове пакування кожної речі й наліпка з логотипом вашої компанії всередині коробки. Від вас — логотип; як виглядатиме наліпка, покажемо на фото в добірці.</p></div>
      <p class="eyebrow" style="margin-bottom:6px">За запитом</p><div class="ask">{cards}</div>
      <p class="note">Що встигаємо до вашої дати й скільки це коштує — пишемо в розрахунку. На фото — подарункове пакування Obiimy: коробка, папір тішью, хустка й твіллі в одному принті.</p></div>
  </div></section>'''

def terms_section():
    steps = "".join(f'<div class="perk"><b class="n">0{i + 1}</b><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(STEPS))
    rows = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in TERMS)
    calc = "".join(f'<tr><th>{n}</th><td class="num">{q}</td><td class="num">{money(pz)}</td><td class="num">{money(q * pz)}</td></tr>' for n, q, pz in EXAMPLE)
    return f'''
  <section class="block alt" id="terms"><div class="wrap terms2">
    <div><div class="head"><p class="eyebrow">Умови й замовлення</p><h2>Як замовити — <i>і що в розрахунку</i></h2></div><div class="perks-l">{steps}</div>
      <div class="got"><p class="eyebrow">Приклад розрахунку · 50 людей · ціни в грн</p>
        <table class="qt"><thead><tr><th>Виріб</th><th>Шт.</th><th>Ціна</th><th>Сума</th></tr></thead><tbody>{calc}</tbody>
        <tfoot><tr><th>Разом</th><td></td><td></td><td class="num">{money(sum(q * pz for _n, q, pz in EXAMPLE))}</td></tr></tfoot></table>
        <p>Строк у робочих днях — окремим рядком.</p></div>
      <p class="note"><a href="obiimy-podarunky-dlia-komandy.pdf" download="Obiimy-podarunky-dlia-komandy.pdf" type="application/pdf">Презентація для погодження (PDF, {team.PDF_MB} МБ) ↓</a></p></div>
    <div><dl class="tkv">{rows}</dl><p class="season">Потрібно до конкретної дати? <i>Напишіть її — скажемо, що встигаємо.</i></p><p style="margin-top:18px"><a class="btn btn-gold" href="#request">Отримати розрахунок</a></p></div>
  </div></section>'''

def photo_band():
    return f'''
  <section class="photo-band" aria-hidden="true">{img(BAND_PH[0], "", sizes="100vw", style=pos(BAND_PH[1]))}<div class="pb-t"><div class="wrap"><p class="eyebrow">Сезон</p><h2>Подарунки до Дня святого Миколая чи Нового року? <i>Напишіть дату зараз</i></h2></div></div></section>'''

def greetings():
    cards = "".join(f'<div class="paper"><small>{lab}</small><p class="t">{t.replace(chr(10), "<br>")}</p><p class="s">— ваша команда</p></div>' for k, lab, t in CARDS if k in ("first", "bday", "years", "team"))
    return f'''
  <section class="block" id="words"><div class="wrap">
    <div class="head"><p class="eyebrow">Привітання</p><h2>Слова від компанії — разом із подарунком</h2><p class="sub">Текст — ваш: до кожної нагоди свій або один на всіх. Оформлення привітання узгодимо у розрахунку. Нижче — наші приклади.</p></div>
    <div class="greet">{cards}</div>
  </div></section>'''

def whyhow():
    return f'''
  <section class="block alt" id="why"><div class="wrap whyhow">
    <div><div class="head"><p class="eyebrow">Чому Obiimy</p><h2>Чотири причини</h2></div>{shop.why_html(items=PERKS)}</div>
    <div><div class="head"><p class="eyebrow">Як це працює</p><h2>Три кроки</h2></div>
      <div class="steps">
        <div><h3>Список</h3><p>Оберіть речі й кількість на цій сторінці або просто напишіть, скільки подарунків потрібно і до якої дати.</p></div>
        <div><h3>Добірка й розрахунок</h3><p>У відповідь — принти на вибір і розрахунок окремими рядками: речі, привітання, доставка. Чи встигаємо до дати — пишемо одразу.</p></div>
        <div><h3>Відправка</h3><p>Ви надсилаєте список отримувачів і текст привітання. Відправляємо Новою поштою — кожному окремо чи в офіс, по Україні; за кордон — як домовимось.</p></div>
      </div>
      <p class="note" style="margin-top:18px"><a href="obiimy-podarunky-dlia-komandy.pdf" download="Obiimy-podarunky-dlia-komandy.pdf" type="application/pdf">Презентація для HR (PDF, 6,6 МБ) ↓</a> · <a href="b2b-team-details">Усе про шовк, пакування й доставку →</a></p>
    </div>
  </div></section>
  <section class="block alt" style="padding-top:0" aria-hidden="true"><div class="wrap"><figure class="wide">{img("photo/kolo-3.webp", "Шовкова хустка на плечах поверх бежевого пальта", sizes="100vw")}</figure></div></section>'''

def main():
    js = ""
    body = f'''
  <section class="hero cover" id="top">{img(HERO[0], "Шовкова хустка на моделі — колекція SOLO", sizes="100vw", lazy=False, eager_priority=True, cls="cover-img", style=pos(HERO[1]))}
    <div class="cover-t"><div class="wrap">
      <p class="eyebrow">Obiimy · український бренд шовкових хусток і аксесуарів</p>
      <h1>Подарунки<br>для команди —<br><i>шовк, який носять</i></h1>
      <p class="lead">Чотири варіанти подарунка — від 1 600 до 3 600 грн на людину. Пакування й наліпка з вашим логотипом — у ціні. Український бренд, виробництво в Україні.</p>
      <div class="cta"><a class="btn btn-gold" href="#request">Отримати розрахунок</a><a class="btn btn-line" href="#tiers">Чотири подарунки й ціни</a></div>
    </div></div>
  </section>
  {tiers_c()}
  {perks_section()}
  {personal_section()}
  {ways_section()}
  {scarf_ways_section()}
  {assort_section()}
  {solo_section()}
  {quote_section()}
  {terms_section()}
  {photo_band()}
  {with_qr(team.request_section("f-main", "Подарунки для команди", "Напишіть — <i>надішлемо добірку й розрахунок</i>", "Нагода, кількість і дата — цього досить для першого листа.", "tiers", corp=True))}
  ''' + team.script("f-main", js)
    return dict(slug="b2b-team-main", skin="deck", bar=BAR, title="Подарунки для команди — шовк, який носять · від 1 600 грн на людину — Obiimy",
                desc="Корпоративні подарунки Obiimy: чотири варіанти подарунка від 1 600 до 3 600 грн на людину, авторські принти на натуральному шовку, колекція SOLO, пакування й наліпка з логотипом компанії — безкоштовно.",
                og="photo/solo/zolote-44-5.webp", nav=[("Подарунки", "tiers"), ("Ваш логотип", "logo"), ("Як носити", "ways"), ("Асортимент", "range"), ("SOLO", "solo"), ("Умови", "terms")],
                cta="Запит", sticky="Подарунки для команди · від 1 600 грн", others=False, body=body)

def build():
    b2b.CSS += team.CSS + shop.CSS + CSS
    p = main()
    html = snap_type(typo(team.bind(b2b.shell(p, p["body"]))))
    (b2b.OUT / f"{p['slug']}.html").write_text(html)
    print(p["slug"], len(html) // 1024, "KB")

if __name__ == "__main__":
    build()
