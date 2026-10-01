#!/usr/bin/env python3
"""Cover variants for the HR deck — covers.html with five A4-landscape pages; screenshots go to review/pp/team/covers/.
Pick one, then set COVER in build-team-pdf.py (or the D01 slot in review/cast.json)."""
import pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
from PIL import Image

def pic(src, cls="", pos=""):
    p = pathlib.Path(src); lb = OUT / "review" / "lb"; lb.mkdir(parents=True, exist_ok=True)
    j = lb / (p.stem + ".jpg")
    if not j.exists():
        im = Image.open(OUT / src).convert("RGB"); im.thumbnail((1200, 1200)); im.save(j, quality=72, optimize=True)
    st = f' style="object-position:{pos}"' if pos else ""
    return f'<img src="review/lb/{j.name}" class="{cls}" alt=""{st}>'

T = '<p class="eb">Для HR і офіс-менеджерів · 2026</p><h1>Подарунки<br>для команди</h1><p class="it">Авторські принти на натуральному італійському шовку</p>'
L = '<p class="line">Чотири рівні від 1 600 грн на людину · пакування й наліпка з вашим логотипом — безкоштовно · нова колекція SOLO</p>'
COVERS = [
    ("A · кабріолет, текст ліворуч (поточна)", f'<div class="full">{pic("photo/solo/tysha-88-2.webp", "ph", "50% 22%")}<div class="t tl"><img src="brand/logo-white.png" class="logo">{T}{L}</div></div>'),
    ("B · фото ліворуч, кремова панель", f'<div class="split">{pic("photo/dotyk-1.webp", "ph", "50% 20%")}<div class="panel"><img src="brand/logo-ink.png" class="logo ink"><div class="mid">{T}</div><div class="facts"><div><b>Чотири рівні</b><span>від 1 600 грн на людину</span></div><div><b>Ваш логотип</b><span>пакування й наліпка — безкоштовно</span></div><div><b>Колекція SOLO</b><span>сім нових авторських принтів</span></div></div></div></div>'),
    ("C · як SOLO-креатив: темно, курсив, чип", f'<div class="full dark">{pic("photo/solo/zolote-tw-2.webp", "ph", "35% 45%")}<div class="t tl crea"><img src="brand/logo-white.png" class="logo"><p class="eb">Для HR і офіс-менеджерів · 2026</p><h1 class="i">Подарунки,<br>які носять</h1><p class="sub">Шовкові подарунки для команди — чотири рівні від 1 600 грн</p><div class="chip">{pic("img/twilly-zolote.webp", "cp")}<div><span>Твіллі «Золоте світло» · на людину</span><em>1 600 грн</em></div></div></div></div>'),
    ("D · портрет з лукбуку, білий фон", f'<div class="split r"><div class="panel white"><img src="brand/logo-ink.png" class="logo ink"><div class="mid">{T}<p class="line ink">Чотири рівні від 1 600 грн · логотип — безкоштовно · колекція SOLO</p></div><p class="toc">Рівні й ціни — 7 · Набори — 8–12 · Запит — 15</p></div>{pic("photo/lookbook/lb05-06-L.webp", "ph", "50% 20%")}</div>'),
    ("E · тренч на полі, текст по центру знизу", f'<div class="full">{pic("photo/kolo-3.webp", "ph", "50% 30%")}<div class="t bc"><img src="brand/logo-white.png" class="logo"><h1>Подарунки для команди</h1><p class="it">Шовк Obiimy · авторські принти · чотири рівні від 1 600 грн</p></div></div>'),
]
pages = "".join(f'<section class="pg"><div class="lab">{n}</div>{h}</section>' for n, h in COVERS)
html = f'''<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>Обкладинки</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=Tenor+Sans&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }} body {{ margin: 0; background: #444; font-family: 'Tenor Sans', sans-serif; color: #141414; }}
  .pg {{ width: 297mm; height: 210mm; position: relative; overflow: hidden; margin: 8mm auto; background: #F1EFEA; }}
  .lab {{ position: absolute; top: 4mm; right: 5mm; z-index: 5; background: #fff; color: #111; font-size: 8pt; padding: 1.5mm 3mm; border-radius: 2mm; }}
  h1 {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: 50pt; line-height: 1.02; margin: 2mm 0 5mm; letter-spacing: -.012em; }} h1.i {{ font-style: italic; color: #F3EBD0; }}
  .eb {{ font-size: 7.3pt; letter-spacing: .26em; text-transform: uppercase; margin: 0 0 2mm; opacity: .8; }}
  .it {{ font-family: 'Playfair Display', serif; font-style: italic; font-size: 13pt; margin: 0; }}
  .line {{ font-size: 9.5pt; border-top: 1px solid rgba(255,255,255,.35); padding-top: 3mm; margin: 5mm 0 0; opacity: .92; }} .line.ink {{ border-color: #C9C6C0; color: #4A4A47; }}
  .full {{ position: relative; width: 100%; height: 100%; }} .full .ph {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .full::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,0,0,.6) 0%, rgba(0,0,0,.25) 50%, rgba(0,0,0,0) 75%), linear-gradient(0deg, rgba(0,0,0,.62) 0%, rgba(0,0,0,0) 55%); }}
  .full.dark::after {{ background: linear-gradient(90deg, rgba(0,0,0,.75) 0%, rgba(0,0,0,.35) 55%, rgba(0,0,0,.1) 100%), linear-gradient(0deg, rgba(0,0,0,.7) 0%, rgba(0,0,0,0) 60%); }}
  .t {{ position: absolute; z-index: 1; color: #fff; }} .tl {{ left: 18mm; bottom: 16mm; max-width: 150mm; }} .bc {{ left: 18mm; right: 18mm; bottom: 18mm; text-align: center; }}
  .bc h1 {{ font-size: 44pt; }} .bc .logo {{ margin: 0 auto 8mm; }}
  .logo {{ height: 10mm; width: auto; display: block; margin-bottom: 10mm; object-fit: contain; }} .logo.ink {{ height: 9mm; align-self: flex-start; }}
  .crea .sub {{ font-size: 11pt; color: rgba(255,255,255,.9); margin: 0 0 6mm; }}
  .chip {{ display: inline-grid; grid-template-columns: 14mm 1fr; gap: 3mm; align-items: center; background: rgba(20,20,20,.72); border: 1px solid rgba(255,255,255,.18); border-radius: 3mm; padding: 2mm 4mm 2mm 2mm; backdrop-filter: blur(6px); }}
  .chip .cp {{ width: 14mm; height: 14mm; border-radius: 2mm; background: #fff; object-fit: cover; }} .chip span {{ display: block; font-size: 7.5pt; opacity: .85; }} .chip em {{ font-style: normal; font-family: 'Playfair Display', serif; font-size: 15pt; color: #E7D9A6; }}
  .split {{ display: grid; grid-template-columns: 168mm 1fr; height: 100%; }} .split.r {{ grid-template-columns: 1fr 150mm; }} .split .ph {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .panel {{ padding: 16mm 16mm 14mm 14mm; display: flex; flex-direction: column; }} .panel.white {{ background: #fff; padding: 16mm 14mm 14mm 18mm; }}
  .mid {{ margin: auto 0; }} .panel h1 {{ font-size: 42pt; }} .panel .it {{ color: #4A4A47; font-size: 12.5pt; }}
  .facts {{ display: grid; gap: 2.5mm; }} .facts div {{ border-top: 1px solid #C9C6C0; padding-top: 2mm; font-size: 8.5pt; color: #6B6772; }} .facts b {{ display: block; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 11.5pt; color: #141414; }}
  .toc {{ font-size: 7pt; letter-spacing: .08em; color: #8E8A84; margin: 0; }}
</style></head><body>{pages}</body></html>'''
(OUT / "covers.html").write_text(html)
d = OUT / "review" / "pp" / "team" / "covers"; d.mkdir(parents=True, exist_ok=True)
script = OUT / "review" / "pp" / "covers.mjs"
script.write_text('''import puppeteer from 'puppeteer-core';
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', args: ['--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: 1123, height: 794 });
await p.goto('file:///Users/ivan/obiimy/covers.html', { waitUntil: 'networkidle0' }); await p.evaluate(() => document.fonts.ready);
const els = await p.$$('.pg'); for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: `/Users/ivan/obiimy/review/pp/team/covers/cover-${'ABCDE'[i]}.png` });
await b.close(); console.log(els.length);
''')
subprocess.run(["node", str(script)], cwd=OUT / "review" / "pp", check=True)
ims = [Image.open(d / f"cover-{c}.png") for c in "ABCDE"]
w, h = ims[0].size; W, H = int(w * .55), int(h * .55)
sh = Image.new("RGB", (W * 2 + 12, H * 3 + 24), "#555")
for i, im in enumerate(ims): sh.paste(im.resize((W, H)), ((i % 2) * (W + 12), (i // 2) * (H + 12)))
sh.save(d / "covers-sheet.jpg", quality=86); print("covers", len(ims))
