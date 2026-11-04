#!/usr/bin/env python3
"""edem-motion «Рух» — the motion variant of the KRAЇNA EDEM × OBIIMY landing (client, 04.11.2026: «с параллаксами, летающими
элементами, 3D и прочим»). Same copy, facts, pictures and registration API as src/build-edem.py. What moves:
  hero    — a perspective scene: the scarf as a 3D card that tilts after the pointer with a sheen sweep; the figure, the pendants and
            the medallion float at different depths (pointer parallax + idle drift), gold dust drifts up, the whole scene parallaxes on scroll;
  manifest— the words light up one by one as the quote scrolls in, the medallion turns slowly behind;
  scarf   — the print with a magnifier lens that follows the pointer (a 2.6× view from the 2400 px render);
  story   — the figure spins in 3D with the scroll progress of the section, pendants swing on cords and kick when hovered;
  symbols — four 3D cards that tilt on hover with the element popping out towards the viewer.
Reduced motion: everything is static. Touch: no pointer parallax, idle drift only. Output: edem-motion.html (HIDDEN; in the variants bar)."""
import importlib.util, pathlib, random, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from imgs import img
_spec = importlib.util.spec_from_file_location("edemv", ROOT / "src" / "build-edem-variants.py"); V = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(V)
MANIFESTO, STORY, SYMBOLS, SPEC, EDEM_P, EDEM_L, OB_P, OB_L, STEPS = V.MANIFESTO, V.STORY, V.SYMBOLS, V.SPEC, V.EDEM_P, V.EDEM_L, V.OB_P, V.OB_L, V.STEPS
PHONE, PHONE_HREF, MAIL, TG = V.PHONE, V.PHONE_HREF, V.MAIL, V.TG
form_html, FORM_CSS, write, spec_rows = V.form_html, V.FORM_CSS, V.write, V.spec_rows

LEAD = "Мистецтво бути ближче. Шовкова хустка за трипільськими мотивами — спільна робота KRAЇNA EDEM та OBIIMY."
SCARF_LEAD = "Хустка тут — більше, ніж аксесуар: мистецьке полотно, що поєднує сучасний дизайн із пам’яттю про давні культури."

CSS = """
:root { --bg: #16100C; --bg2: #1F1610; --cream: #F3E9D8; --cream2: rgba(243,233,216,.72); --gold: #D9B86A; --gold2: #B48A3A; --line: rgba(217,184,106,.22); --acc: #D9B86A; --fb: rgba(42,32,23,.3); --fbg: #FBF4E7; --fink: #2A2017; }
* { box-sizing: border-box; } html { scroll-behavior: smooth; }
body { margin: 0; background: var(--bg); color: var(--cream); font-family: Montserrat, Arial, sans-serif; font-size: 17px; line-height: 1.6; -webkit-font-smoothing: antialiased; overflow-x: hidden; }
img { max-width: 100%; height: auto; display: block; } p { margin: 0; } a { color: inherit; } figure { margin: 0; }
h1, h2, h3 { margin: 0; font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 400; line-height: 1.02; text-wrap: balance; }
.wrap { max-width: 1240px; margin: 0 auto; padding: 0 24px; }
section[id] { scroll-margin-top: 20px; }
.eyebrow { font-size: 11px; font-weight: 600; letter-spacing: .28em; text-transform: uppercase; color: var(--gold); }
.lead { font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(21px, 2vw, 28px); font-weight: 300; line-height: 1.38; color: var(--cream2); }
.btn-main { background: var(--gold); color: #1C1410; } .btn-main:hover { background: #E8CB84; }
.btn-line { border-color: rgba(243,233,216,.6); color: var(--cream); } .btn-line:hover { border-color: var(--cream); }
.cta { display: flex; flex-wrap: wrap; gap: 14px; }
/* ── hero: the scene ───────────────────────────────────────────────────────────────────────────── */
.hero { position: relative; min-height: 100vh; overflow: hidden; display: grid; align-items: center; padding: 100px 0 80px; background: radial-gradient(70% 60% at 68% 45%, rgba(180,138,58,.18), transparent 65%), var(--bg); }
.hero .top { position: absolute; left: 24px; right: 24px; top: 30px; display: flex; justify-content: space-between; font-size: 11px; letter-spacing: .26em; text-transform: uppercase; color: var(--cream2); z-index: 5; }
.dust { position: absolute; inset: 0; pointer-events: none; z-index: 1; } .dust i { position: absolute; bottom: -10px; width: 3px; height: 3px; border-radius: 50%; background: var(--gold); opacity: 0; animation: rise linear infinite; box-shadow: 0 0 6px rgba(217,184,106,.8); }
@keyframes rise { 0% { transform: translateY(0) translateX(0); opacity: 0; } 10% { opacity: .9; } 90% { opacity: .5; } 100% { transform: translateY(-110vh) translateX(40px); opacity: 0; } }
.scene { position: absolute; inset: 0; perspective: 1400px; transform-style: preserve-3d; z-index: 2; pointer-events: none; }
.layer { position: absolute; will-change: transform; transform-style: preserve-3d; }
.l-mandala { left: 50%; top: 50%; width: min(130vh, 1300px); margin-left: calc(min(130vh, 1300px) / -2 + 20vw); margin-top: calc(min(130vh, 1300px) / -2); opacity: .16; filter: sepia(.5) saturate(.6); }
.l-mandala img { animation: turn 160s linear infinite; }
@keyframes turn { to { transform: rotate(360deg); } }
.l-card { left: 71%; top: 50%; width: min(38vw, 560px); margin-left: calc(min(38vw, 560px) / -2); margin-top: calc(min(40vw, 580px) / -2 - 2vh); pointer-events: auto; }
.card { position: relative; transform-style: preserve-3d; transition: transform .12s linear; will-change: transform; animation: hover 7s ease-in-out infinite; }
.card img { width: 100%; height: auto; filter: drop-shadow(0 60px 80px rgba(0,0,0,.65)); transform: translateZ(1px); }
.card .sheen { position: absolute; inset: 4% 8%; background: linear-gradient(115deg, transparent 35%, rgba(255,255,255,.28) 48%, transparent 60%); mix-blend-mode: screen; pointer-events: none; transform: translateX(var(--sx, -60%)); transition: transform .12s linear; }
@keyframes hover { 0%, 100% { translate: 0 0; } 50% { translate: 0 -14px; } }
.l-fig { left: 48%; top: 58%; width: clamp(110px, 12vw, 200px); } .l-fig img { filter: drop-shadow(0 30px 30px rgba(0,0,0,.7)); animation: drift 9s ease-in-out infinite; }
.l-pr { left: 89%; top: 14%; width: clamp(80px, 8vw, 130px); } .l-pr img { filter: drop-shadow(0 24px 24px rgba(0,0,0,.7)); animation: drift 7s ease-in-out -2s infinite; }
.l-pd { left: 50%; top: 12%; width: clamp(70px, 7vw, 120px); } .l-pd img { filter: drop-shadow(0 24px 24px rgba(0,0,0,.7)); animation: drift 8s ease-in-out -4s infinite; }
.l-pr2 { left: 93%; top: 68%; width: clamp(54px, 5vw, 86px); opacity: .85; } .l-pr2 img { filter: drop-shadow(0 18px 20px rgba(0,0,0,.7)) blur(.6px); animation: drift 11s ease-in-out -6s infinite; }
@keyframes drift { 0%, 100% { transform: translateY(0) rotate(-3deg); } 50% { transform: translateY(-22px) rotate(3deg); } }
.hero .copy { position: relative; z-index: 4; max-width: 1240px; width: 100%; margin: 0 auto; padding: 0 24px; }
.hero .copy > * { max-width: 40%; }
.hero h1 { font-size: clamp(50px, 7.2vw, 112px); line-height: .98; margin-top: 18px; } .hero h1 i { font-style: italic; color: var(--gold); }
.hero .lead { margin-top: 24px; max-width: 24em; } .hero .cta { margin-top: 34px; }
.hero .facts { margin-top: 36px; display: flex; flex-wrap: wrap; gap: 8px 24px; font-size: 12px; letter-spacing: .12em; text-transform: uppercase; color: var(--cream2); } .hero .facts b { color: var(--gold); }
.scrollhint { position: absolute; left: 50%; bottom: 22px; transform: translateX(-50%); font-size: 10px; letter-spacing: .3em; text-transform: uppercase; color: var(--cream2); z-index: 5; display: flex; flex-direction: column; align-items: center; gap: 8px; } .scrollhint i { width: 1px; height: 36px; background: linear-gradient(180deg, var(--gold), transparent); animation: pulse 2s ease-in-out infinite; }
@keyframes pulse { 0%, 100% { opacity: .3; } 50% { opacity: 1; } }
/* ── sections ──────────────────────────────────────────────────────────────────────────────────── */
section.s { padding: clamp(80px, 10vw, 150px) 0; position: relative; overflow: hidden; }
.head { max-width: 760px; margin-bottom: clamp(34px, 4vw, 60px); } .head h2 { font-size: clamp(38px, 5vw, 72px); margin-top: 14px; } .head .lead { margin-top: 16px; }
.px { position: absolute; pointer-events: none; will-change: transform; }
.mani { text-align: center; } .mani .bg { left: 50%; top: 50%; width: 900px; margin: -450px 0 0 -450px; opacity: .12; filter: sepia(.5) saturate(.6); } .mani .bg img { animation: turn 120s linear infinite reverse; }
.mani blockquote { position: relative; margin: 0 auto; max-width: 20em; font-family: 'Cormorant Garamond', serif; font-size: clamp(30px, 4.6vw, 68px); line-height: 1.15; font-weight: 300; }
.mani .w { display: inline-block; opacity: .12; transform: translateY(.2em); transition: opacity .5s, transform .5s; } .mani .in .w { opacity: 1; transform: none; } .mani b .w, .mani .w b { color: var(--gold); font-weight: 400; }
.scarf { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, .85fr); gap: clamp(28px, 5vw, 80px); align-items: center; }
.lenswrap { position: relative; cursor: none; } .lenswrap > img { width: 100%; height: auto; border: 1px solid var(--line); padding: 12px; background: #15100C; }
.lens { position: absolute; width: 260px; height: 260px; border-radius: 50%; overflow: hidden; border: 2px solid var(--gold); box-shadow: 0 30px 60px rgba(0,0,0,.6), inset 0 0 0 1px rgba(0,0,0,.4); pointer-events: none; opacity: 0; transform: translate(-50%, -50%) scale(.6); transition: opacity .25s, transform .25s; left: 0; top: 0; z-index: 3; background: #15100C; }
.lens.on { opacity: 1; transform: translate(-50%, -50%) scale(1); } .lens img { position: absolute; left: 0; top: 0; max-width: none; will-change: transform; }
.lens::after { content: ""; position: absolute; inset: 0; border-radius: 50%; background: radial-gradient(circle at 35% 30%, rgba(255,255,255,.18), transparent 45%); }
.hintlens { margin-top: 12px; font-size: 11px; letter-spacing: .16em; text-transform: uppercase; color: var(--cream2); }
.spec div { display: flex; justify-content: space-between; gap: 20px; padding: 14px 0; border-bottom: 1px solid var(--line); font-size: 15px; } .spec span { color: var(--cream2); } .spec b { font-weight: 600; text-align: right; }
.note { margin-top: 18px; font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 20px; color: var(--cream2); }
.story { display: grid; grid-template-columns: minmax(0, 1fr) 320px; gap: clamp(28px, 5vw, 80px); align-items: center; } .text { color: var(--cream2); } .text p + p { margin-top: 1.1em; }
.spin { perspective: 1200px; display: grid; place-items: center; height: 460px; } .spin img { width: 240px; height: auto; filter: drop-shadow(0 40px 40px rgba(0,0,0,.7)); transform-style: preserve-3d; will-change: transform; }
.hangs { position: absolute; top: 0; right: 4%; display: flex; gap: 60px; z-index: 1; } .hang { width: 90px; display: flex; flex-direction: column; align-items: center; transform-origin: 50% 0; animation: sway 7s ease-in-out infinite; cursor: pointer; } .hang i { display: block; width: 1px; height: 140px; background: linear-gradient(180deg, var(--gold), rgba(217,184,106,.3)); } .hang img { width: 100%; height: auto; filter: drop-shadow(0 18px 24px rgba(0,0,0,.7)); }
.hang:nth-child(2) { animation-delay: -3s; width: 70px; } .hang:nth-child(2) i { height: 200px; } .hang.kick { animation: kick 2.6s cubic-bezier(.2,.7,.2,1); }
@keyframes sway { 0%, 100% { transform: rotate(-2deg); } 50% { transform: rotate(2deg); } }
@keyframes kick { 0% { transform: rotate(0); } 15% { transform: rotate(14deg); } 40% { transform: rotate(-10deg); } 65% { transform: rotate(6deg); } 85% { transform: rotate(-3deg); } 100% { transform: rotate(0); } }
.cards { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 24px; perspective: 1200px; }
.card3d { position: relative; background: linear-gradient(160deg, #2A1D13, #1A120D); border: 1px solid var(--line); padding: 30px 24px 28px; transform-style: preserve-3d; transform: rotateX(var(--rx, 0)) rotateY(var(--ry, 0)); transition: transform .15s linear, box-shadow .3s; }
.card3d:hover { box-shadow: 0 40px 70px -30px rgba(0,0,0,.8); } .card3d::after { content: ""; position: absolute; inset: 0; background: radial-gradient(400px circle at var(--mx, 50%) var(--my, 50%), rgba(217,184,106,.16), transparent 55%); pointer-events: none; }
.card3d .pic { height: 220px; display: flex; align-items: center; justify-content: center; transform: translateZ(50px); transform-style: preserve-3d; } .card3d .pic img { max-height: 100%; width: auto; filter: drop-shadow(0 30px 30px rgba(0,0,0,.75)); transition: transform .3s; } .card3d:hover .pic img { transform: scale(1.08); } .card3d .pic.lg img { transform: scale(1.3); } .card3d:hover .pic.lg img { transform: scale(1.4); }
.card3d h3 { font-size: 28px; margin-top: 18px; transform: translateZ(30px); } .card3d p { margin-top: 10px; font-size: 14px; color: var(--cream2); transform: translateZ(20px); } .card3d .n { display: block; font-size: 11px; letter-spacing: .3em; color: var(--gold); margin-bottom: 10px; }
.brands { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; } .brands article { border-top: 1px solid var(--line); padding-top: 24px; } .brands h3 { font-size: 32px; letter-spacing: .04em; margin-top: 10px; } .brands p { margin-top: 12px; color: var(--cream2); font-size: 15px; }
.brands ul { margin: 14px 0 0; padding: 0; list-style: none; } .brands li { padding: 9px 0; border-top: 1px solid var(--line); font-size: 14px; color: var(--cream2); }
.reg { background: var(--cream); color: #2A2017; padding: clamp(70px, 9vw, 140px) 0; position: relative; overflow: hidden; }
.reg .wrap { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: clamp(32px, 5vw, 80px); align-items: start; position: relative; }
.reg .eyebrow { color: var(--gold2); } .reg h2 { font-size: clamp(36px, 4.2vw, 60px); margin-top: 14px; } .reg .lead { margin-top: 18px; color: #6B5A48; }
.reg .btn-main { background: #2A2017; color: var(--cream); } .reg .btn-main:hover { background: #3B2A1C; } .reg .btn-line { border-color: #2A2017; color: #2A2017; }
.steps { margin-top: 30px; } .steps > div { display: grid; grid-template-columns: 44px minmax(0, 1fr); gap: 14px; padding: 16px 0; border-top: 1px solid rgba(42,32,23,.14); } .steps h3 { font-size: 24px; } .steps p { font-size: 14px; color: #6B5A48; margin-top: 4px; } .steps i { font-family: 'Cormorant Garamond', serif; font-style: normal; font-size: 24px; color: var(--gold2); }
.contacts { margin-top: 26px; font-size: 14px; color: #6B5A48; } .contacts a { text-decoration: none; border-bottom: 1px solid rgba(42,32,23,.2); }
.reg .panel { background: #fff; border: 1px solid rgba(42,32,23,.12); padding: clamp(24px, 3vw, 40px); } .reg .bg { right: -120px; bottom: -160px; width: 520px; opacity: .14; } .reg .bg img { animation: turn 140s linear infinite; }
footer { padding: 34px 24px; font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--cream2); display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; border-top: 1px solid var(--line); } footer a { text-decoration: none; }
@media (max-width: 980px) { .hero { padding: 90px 0 60px; } .hero .copy > * { max-width: none; } .l-card { position: relative; left: auto; top: auto; margin: 0 auto 30px; width: min(78vw, 420px); } .scene { position: relative; inset: auto; height: auto; pointer-events: none; } .l-mandala { display: none; } .l-fig, .l-pr, .l-pd, .l-pr2 { position: absolute; } .l-fig { left: 2%; top: 10%; } .l-pr { left: 84%; top: 4%; } .l-pd { left: 6%; top: 70%; } .l-pr2 { left: 88%; top: 60%; }
  .scarf, .story, .brands, .reg .wrap { grid-template-columns: 1fr; } .cards { grid-template-columns: repeat(2, 1fr); } .hangs { display: none; } .spin { height: 320px; } .lenswrap { cursor: default; } .hintlens { display: none; } }
@media (max-width: 600px) { body { font-size: 16px; } .cards { grid-template-columns: 1fr; } .cta .btn { flex: 1 1 100%; justify-content: center; } .hero .top { font-size: 9px; letter-spacing: .16em; } }
@media (hover: none) { .lens, .hintlens { display: none; } .lenswrap { cursor: default; } }
@media (prefers-reduced-motion: reduce) { .card, .layer img, .dust i, .hang, .l-mandala img, .mani .bg img, .reg .bg img, .scrollhint i { animation: none !important; } .mani .w { opacity: 1; transform: none; } }
"""

JS = """
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches, fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var hero = document.getElementById('hero'), card = document.getElementById('card'), layers = [].slice.call(document.querySelectorAll('.scene .layer'));
  var tx = 0, ty = 0, cx = 0, cy = 0, sy = 0, raf = null;
  function frame() {
    raf = null; cx += (tx - cx) * .08; cy += (ty - cy) * .08;
    var wide = window.innerWidth > 980;
    layers.forEach(function (l) { var d = +l.getAttribute('data-depth') || 0; var x = fine ? cx * d * 42 : 0, y = (fine ? cy * d * 42 : 0) - (wide ? sy * d * .35 : 0); l.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0)'; });
    if (card) { var ry = fine ? cx * 14 : 0, rx = fine ? -cy * 12 : 0; card.style.transform = 'rotateY(' + ry.toFixed(2) + 'deg) rotateX(' + rx.toFixed(2) + 'deg)'; card.style.setProperty('--sx', (fine ? cx * 70 : -60) + '%'); }
    if (Math.abs(tx - cx) > .002 || Math.abs(ty - cy) > .002) raf = requestAnimationFrame(frame);
  }
  function kick() { if (!raf) raf = requestAnimationFrame(frame); }
  if (!reduce) {
    if (fine) hero.addEventListener('pointermove', function (e) { var r = hero.getBoundingClientRect(); tx = ((e.clientX - r.left) / r.width - .5) * 2; ty = ((e.clientY - r.top) / r.height - .5) * 2; kick(); });
    hero.addEventListener('pointerleave', function () { tx = 0; ty = 0; kick(); });
    window.addEventListener('scroll', function () { sy = Math.min(window.scrollY, window.innerHeight); kick(); px(); spin(); }, { passive: true });
    kick();
  }
  // parallax ornaments in sections
  var pxs = [].slice.call(document.querySelectorAll('.px'));
  function px() { if (reduce) return; var h = window.innerHeight; pxs.forEach(function (el) { var r = el.parentElement.getBoundingClientRect(); var p = (r.top + r.height / 2 - h / 2) / h; el.style.transform = 'translate3d(0,' + (p * (+el.getAttribute('data-speed') || 60)).toFixed(1) + 'px,0)'; }); }
  // the figure spins with the scroll progress of the story
  var spinImg = document.getElementById('spin');
  function spin() { if (reduce || !spinImg) return; var r = spinImg.parentElement.getBoundingClientRect(), h = window.innerHeight; var p = Math.max(0, Math.min(1, (h - r.top) / (h + r.height))); spinImg.style.transform = 'rotateY(' + (p * 360 - 180).toFixed(1) + 'deg)'; }
  px(); spin(); window.addEventListener('resize', function () { px(); spin(); });
  // the manifesto lights up word by word
  var q = document.getElementById('quote');
  if (q) { q.innerHTML = q.innerHTML.replace(/(<b>|<\\/b>)/g, '\\u0001$1\\u0001').split('\\u0001').map(function (part) { return /^<\\/?b>$/.test(part) ? part : part.split(/(\\s+)/).map(function (w) { return /^\\s+$/.test(w) || !w ? w : '<span class="w">' + w + '</span>'; }).join(''); }).join('');
    [].slice.call(q.querySelectorAll('.w')).forEach(function (w, i) { w.style.transitionDelay = (i * 45) + 'ms'; });
    if ('IntersectionObserver' in window) { var qio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { q.classList.add('in'); qio.disconnect(); } }); }, { threshold: .4 }); qio.observe(q); } else q.classList.add('in'); }
  // the magnifier lens on the print
  var lw = document.getElementById('lenswrap'), lens = document.getElementById('lens'), li = lens && lens.querySelector('img'), Z = 2.6;
  if (lw && fine && !reduce) {
    var base = lw.querySelector('img');
    lw.addEventListener('pointerenter', function () { lens.classList.add('on'); });
    lw.addEventListener('pointerleave', function () { lens.classList.remove('on'); });
    lw.addEventListener('pointermove', function (e) { lens.classList.add('on'); var r = base.getBoundingClientRect(); var pad = 13, cw = r.width - 2 * pad, x = e.clientX - r.left, y = e.clientY - r.top; lens.style.left = x + 'px'; lens.style.top = y + 'px'; li.style.width = (cw * Z) + 'px'; li.style.transform = 'translate(' + (-(x - pad) * Z + 130) + 'px,' + (-(y - pad) * Z + 130) + 'px)'; });
  }
  // pendants kick when hovered
  [].slice.call(document.querySelectorAll('.hang')).forEach(function (h) { h.addEventListener('pointerenter', function () { h.classList.remove('kick'); void h.offsetWidth; h.classList.add('kick'); }); h.addEventListener('animationend', function (e) { if (e.animationName === 'kick') h.classList.remove('kick'); }); });
  // 3D cards
  if (fine && !reduce) [].slice.call(document.querySelectorAll('.card3d')).forEach(function (c) {
    c.addEventListener('pointermove', function (e) { var r = c.getBoundingClientRect(); var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height; c.style.setProperty('--ry', ((x - .5) * 16) + 'deg'); c.style.setProperty('--rx', ((.5 - y) * 14) + 'deg'); c.style.setProperty('--mx', (x * 100) + '%'); c.style.setProperty('--my', (y * 100) + '%'); });
    c.addEventListener('pointerleave', function () { c.style.setProperty('--ry', '0deg'); c.style.setProperty('--rx', '0deg'); });
  });
"""

def main():
    rnd = random.Random(7)
    dust = "".join(f'<i style="left:{rnd.uniform(0, 100):.1f}%;animation-duration:{rnd.uniform(9, 22):.1f}s;animation-delay:-{rnd.uniform(0, 22):.1f}s;width:{rnd.choice([2, 2, 3, 4])}px;height:{rnd.choice([2, 2, 3, 4])}px"></i>' for _ in range(42))
    body = f'''
<main id="top">
<section class="hero" id="hero">
  <div class="top"><span>Kraїna Edem × Obiimy</span><span>Лімітований випуск · 2026</span></div>
  <div class="dust" aria-hidden="true">{dust}</div>
  <div class="scene" aria-hidden="true">
    <div class="layer l-mandala" data-depth=".12">{img("photo/edem/mandala.webp", "", sizes="1300px")}</div>
    <div class="layer l-fig" data-depth=".55">{img("photo/edem/figure.webp", "", sizes="200px", lazy=False)}</div>
    <div class="layer l-pr2" data-depth=".4">{img("photo/edem/pendant-round.webp", "", sizes="90px", lazy=False)}</div>
    <div class="layer l-card" data-depth=".25"><div class="card" id="card">{img("photo/edem/scarf.webp", "Хустка KRAЇNA EDEM × OBIIMY «Trypillia — The Art of Origins», 88 × 88", sizes="(max-width: 980px) 78vw, 44vw", lazy=False, eager_priority=True)}<i class="sheen"></i></div></div>
    <div class="layer l-pr" data-depth=".8">{img("photo/edem/pendant-round.webp", "", sizes="130px", lazy=False)}</div>
    <div class="layer l-pd" data-depth="1">{img("photo/edem/pendant-diamond.webp", "", sizes="120px", lazy=False)}</div>
  </div>
  <div class="copy">
    <p class="eyebrow">Спільний мистецький проєкт</p>
    <h1>Trypillia —<br><i>The Art of Origins</i></h1>
    <p class="lead">{LEAD}</p>
    <div class="cta"><a class="btn btn-main" href="#register">Отримати ранній доступ</a><a class="btn btn-line" href="#scarf">Роздивитися хустку</a></div>
    <div class="facts"><span><b>88 × 88</b> см</span><span><b>100%</b> шовк</span><span>Обмежений наклад</span><span>Підпис OBIIMY × Edem</span></div>
  </div>
  <p class="scrollhint">Гортайте<i></i></p>
</section>

<section class="s mani" id="manifest"><div class="px bg" data-speed="-80" aria-hidden="true">{img("photo/edem/mandala.webp", "", sizes="900px")}</div><div class="wrap"><blockquote id="quote">{MANIFESTO}</blockquote></div></section>

<section class="s" id="scarf" style="background:var(--bg2)"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Хустка · 88 × 88 см</p><h2>Мистецьке полотно, яке можна носити</h2><p class="lead">{SCARF_LEAD}</p></div>
  <div class="scarf">
    <div class="rv"><div class="lenswrap" id="lenswrap">{img("photo/edem/art-1600.webp", "Принт хустки «Trypillia — The Art of Origins» повністю", sizes="(max-width: 980px) 92vw, 58vw")}<div class="lens" id="lens" aria-hidden="true">{img("photo/edem/art-2400.webp", "", sizes="2000px")}</div></div><p class="hintlens">Наведіть курсор — лупа покаже деталі принту</p></div>
    <div class="rv"><div class="spec">{spec_rows()}</div><p class="note">Ціну й дату старту повідомимо зареєстрованим першими.</p><p style="margin-top:26px"><a class="btn btn-main" href="#register">Отримати ранній доступ</a></p></div>
  </div>
</div></section>

<section class="s" id="story">
  <div class="hangs" aria-hidden="true"><div class="hang"><i></i>{img("photo/edem/pendant-round.webp", "", sizes="90px")}</div><div class="hang"><i></i>{img("photo/edem/pendant-diamond.webp", "", sizes="70px")}</div></div>
  <div class="wrap"><div class="story">
    <div class="rv"><p class="eyebrow">Історія, що живе в нас</p><h2 style="font-size:clamp(38px,5vw,72px);margin-top:14px">Наше коріння сягає глибини тисячоліть</h2><div class="text" style="margin-top:24px">{"".join(f"<p>{t}</p>" for t in STORY)}</div></div>
    <div class="spin rv">{img("photo/edem/figure.webp", "Трипільська фігурка — елемент принту", sizes="240px", extra='id="spin"')}</div>
  </div></div>
</section>

<section class="s" id="symbols" style="background:var(--bg2)"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Символи хустки</p><h2>Кожна деталь має значення</h2><p class="lead">Давні орнаментальні мотиви й символічні образи — переосмислені мовою сучасного дизайну, у золоті й глибокому синьому.</p></div>
  <div class="cards">{"".join(f'<article class="card3d rv"><div class="pic{" lg" if k == "pendant-round" else ""}">{img(f"photo/edem/{k}.webp", a, sizes="260px")}</div><h3><span class="n">0{i + 1}</span>{t}</h3><p>{d}</p></article>' for i, (k, t, d, a) in enumerate(SYMBOLS))}</div>
</div></section>

<section class="s" id="brands"><div class="wrap">
  <div class="head rv"><p class="eyebrow">Партнери</p><h2>Два бренди. Одна філософія. Спільне мистецтво.</h2></div>
  <div class="brands">
    <article class="rv"><p class="eyebrow">Партнер</p><h3>KRAЇNA EDEM</h3><p>{EDEM_P}</p><ul>{"".join(f"<li>{x}</li>" for x in EDEM_L)}</ul></article>
    <article class="rv"><p class="eyebrow">Бренд</p><h3>OBIIMY</h3><p>{OB_P}</p><ul>{"".join(f"<li>{x}</li>" for x in OB_L)}</ul></article>
  </div>
</div></section>

<section class="reg" id="register"><div class="px bg" data-speed="-50" aria-hidden="true">{img("photo/edem/mandala.webp", "", sizes="520px")}</div><div class="wrap">
  <div class="rv"><p class="eyebrow">Як придбати</p><h2>Ранній доступ до випуску</h2><p class="lead">Ціну й дату старту підтверджуємо з партнером. Щойно вони відомі — зареєстровані дізнаються першими й отримують персональне посилання на оплату.</p>
    <div class="steps">{"".join(f"<div><i>0{i + 1}</i><div><h3>{t}</h3><p>{d}</p></div></div>" for i, (t, d) in enumerate(STEPS))}</div>
    <div class="contacts">Питання: <a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="{TG}" target="_blank" rel="noopener">Telegram</a></div></div>
  <div class="rv panel">{form_html()}</div>
</div></section>
<footer><span>Kraїna Edem × Obiimy · Trypillia — The Art of Origins · 2026</span><span><a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a></span></footer>
</main>'''
    write("edem-motion", CSS + FORM_CSS, body, JS)

if __name__ == "__main__":
    main()
