#!/usr/bin/env python3
"""«Синхронізація з Shopify» — a page of the editor service (14.11.2026, «сделать отдельную страницу — пока просто кнопку и дату
последней синхронизации»). One button runs the Horoshop → Shopify chain of src/horoshop.py and src/horoshop_home.py as subprocesses,
one after another, writing a log to data/horoshop/sync/<stamp>.log; the page shows the date of the last successful run, the state
of the current one and the tail of the log. Mounted by src/deck-editor.py: GET /sync (page), GET /api/sync (state), POST /api/sync (start).
Needs HOROSHOP_* and SHOPIFY_* in the environment (Railway: variables of the deck-editor service) — the page says when they are missing.
"""
import json, os, pathlib, subprocess, sys, threading, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "data" / "horoshop" / "sync"
STATE = DIR / "state.json"
LOCK = threading.Lock()

STEPS = [  # (label, command) — each one prints its own plan and result; the chain stops at the first failure
    ("Резервна копія товарів Shopify", [sys.executable, "src/horoshop.py", "backup"]),
    ("Вивантаження каталогу Хорошопу", [sys.executable, "src/horoshop.py", "export"]),
    ("Порівняння з Shopify", [sys.executable, "src/horoshop.py", "report"]),
    ("Ціни, compare-at, SKU", [sys.executable, "src/horoshop.py", "prices", "--apply"]),
    ("Статуси (приховані на сайті → чернетки)", [sys.executable, "src/horoshop.py", "status", "--apply"]),
    ("Нові товари", [sys.executable, "src/horoshop.py", "new", "--apply"]),
    ("Публікація в каналах, залишки", [sys.executable, "src/horoshop.py", "publish", "--apply"]),
    ("Теги за категоріями сайту", [sys.executable, "src/horoshop_home.py", "tags", "--apply"]),
    ("Колекції, яких бракує", [sys.executable, "src/horoshop_home.py", "collections", "--apply"]),
]

def configured():
    return all(os.environ.get(k) for k in ("HOROSHOP_LOGIN", "HOROSHOP_PASSWORD")) or (pathlib.Path.home() / ".config/obiimy/horoshop.env").exists(), \
           all(os.environ.get(k) for k in ("SHOPIFY_SHOP", "SHOPIFY_CLIENT_ID", "SHOPIFY_CLIENT_SECRET")) or (pathlib.Path.home() / ".config/obiimy/shopify.env").exists()

def load():
    try: return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception: return {}

def save(st):
    DIR.mkdir(parents=True, exist_ok=True); STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")

def _summary(text):
    """The lines of the log that tell the story: the comparison totals and each step's result line."""
    keep = []
    for l in text.splitlines():
        if any(k in l for k in ("Shopify:", "ціна без змін", "готово:", "бекап:", "опубліковано:", "Створюю", "Застосовую", "План колекцій", "ПОМИЛКА", "Traceback", "Error", "KeyCRM:", "немає")):
            keep.append(l.strip()[:160])
    return keep[-14:]

def run_job(stamp):
    log = DIR / f"{stamp}.log"; st = load()
    ok = True
    with open(log, "a", encoding="utf-8") as f:
        for i, (label, cmd) in enumerate(STEPS, 1):
            st.update(step=i, steps=len(STEPS), step_label=label); save(st)
            f.write(f"\n=== {i}/{len(STEPS)} {label} · {time.strftime('%H:%M:%S')}\n"); f.flush()
            r = subprocess.run(cmd, cwd=str(ROOT), stdout=f, stderr=subprocess.STDOUT, env={**os.environ, "PYTHONUNBUFFERED": "1"}, timeout=3600)
            if r.returncode != 0:
                f.write(f"!!! крок завершився з кодом {r.returncode}\n"); ok = False; break
        f.write(f"\n=== {'готово' if ok else 'зупинено через помилку'} · {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    text = log.read_text(encoding="utf-8", errors="replace")
    st.update(running=False, finished=time.strftime("%Y-%m-%d %H:%M:%S"), ok=ok, summary=_summary(text), log=log.name)
    if ok: st["last_ok"] = st["finished"]
    save(st)

def start():
    with LOCK:
        st = load()
        if st.get("running") and time.time() - st.get("started_ts", 0) < 3600 * 2: return dict(ok=False, error="Синхронізація вже йде.")
        hs, sp = configured()
        if not (hs and sp): return dict(ok=False, error="Немає доступів: " + ", ".join(n for n, v in (("Хорошоп", hs), ("Shopify", sp)) if not v) + ".")
        stamp = time.strftime("%Y%m%d-%H%M%S")
        st.update(running=True, started=time.strftime("%Y-%m-%d %H:%M:%S"), started_ts=time.time(), finished=None, ok=None, step=0, steps=len(STEPS), step_label="", summary=[], log=f"{stamp}.log")
        save(st)
        threading.Thread(target=run_job, args=(stamp,), daemon=True).start()
        return dict(ok=True, started=st["started"])

def state():
    st = load(); hs, sp = configured()
    tail = ""
    if st.get("log") and (DIR / st["log"]).exists():
        t = (DIR / st["log"]).read_text(encoding="utf-8", errors="replace"); tail = t[-6000:]
    return dict(ok=True, configured=dict(horoshop=hs, shopify=sp), running=bool(st.get("running")), started=st.get("started"), finished=st.get("finished"),
                result_ok=st.get("ok"), last_ok=st.get("last_ok"), step=st.get("step", 0), steps=st.get("steps", len(STEPS)), step_label=st.get("step_label", ""),
                summary=st.get("summary", []), tail=tail)

PAGE = """<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Синхронізація з Shopify</title>
<style>
:root{--ink:#141110;--muted:#6b645c;--line:#e6e0d6;--paper:#f7f3ec;--yel:#f4c430;--ok:#1f7a3a;--bad:#b3261e}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:720px;margin:0 auto;padding:48px 20px 80px}h1{font-weight:500;font-size:28px;margin:0 0 6px}.sub{color:var(--muted);margin:0 0 32px}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:24px}
.row{display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap}
.last{font-size:15px;color:var(--muted)}.last b{display:block;color:var(--ink);font-size:22px;font-weight:500}
button{appearance:none;border:0;border-radius:999px;background:var(--ink);color:#fff;font:inherit;font-weight:500;padding:14px 26px;cursor:pointer}
button.run{background:var(--yel);color:var(--ink)}button:disabled,button.run:disabled{background:#b9b2a8;color:#fff;cursor:default}
.status{margin-top:18px;font-size:15px;color:var(--muted)}.status .ok{color:var(--ok)}.status .bad{color:var(--bad)}
.bar{height:4px;background:var(--line);border-radius:2px;margin-top:14px;overflow:hidden}.bar i{display:block;height:100%;background:var(--yel);width:0;transition:width .4s}
details{margin-top:24px}summary{cursor:pointer;color:var(--muted);font-size:15px}pre{background:#1d1a17;color:#e9e3d8;border-radius:12px;padding:16px;font:12.5px/1.45 ui-monospace,Menlo,monospace;white-space:pre-wrap;max-height:420px;overflow:auto;margin:12px 0 0}
ul.sum{margin:12px 0 0;padding-left:18px;font-size:14px;color:var(--ink)}.warn{color:var(--bad);font-size:14px;margin-top:10px}
</style></head><body><main>
<h1>Синхронізація з Shopify</h1>
<p class="sub">Каталог obiimy.world (Хорошоп) → shop.obiimy.world: ціни, нові товари, наявність, колекції. Назви й описи наявних товарів не змінюються.</p>
<div class="card">
 <div class="row">
  <div class="last">Остання синхронізація<b id="last">—</b></div>
  <button id="go" class="run" disabled>Синхронізувати</button>
 </div>
 <div class="bar"><i id="bar"></i></div>
 <div class="status" id="status">…</div>
 <div class="warn" id="warn" hidden></div>
 <ul class="sum" id="sum"></ul>
 <details><summary>Журнал останнього запуску</summary><pre id="log"></pre></details>
</div>
</main>
<script>
const $=id=>document.getElementById(id);let timer=null;
async function load(){
 const r=await fetch('/api/sync',{cache:'no-store'});const s=await r.json();
 $('last').textContent=s.last_ok||'ще не було';
 const c=s.configured;$('warn').hidden=c.horoshop&&c.shopify;$('warn').textContent='Немає доступів: '+[!c.horoshop&&'Хорошоп',!c.shopify&&'Shopify'].filter(Boolean).join(', ')+'. Додайте змінні HOROSHOP_* / SHOPIFY_* сервісу.';
 $('go').disabled=s.running||!(c.horoshop&&c.shopify);
 $('bar').style.width=s.running?Math.max(4,Math.round(100*s.step/s.steps))+'%':(s.finished?'100%':'0');
 if(s.running){$('status').innerHTML='Іде синхронізація, крок '+s.step+' з '+s.steps+': '+s.step_label+' · почато '+s.started;}
 else if(s.finished){$('status').innerHTML=(s.result_ok?'<span class="ok">Завершено успішно</span>':'<span class="bad">Зупинено через помилку</span>')+' · '+s.finished;}
 else $('status').textContent='Ще не запускалась.';
 $('sum').innerHTML=(s.summary||[]).map(l=>'<li>'+l.replace(/[<>&]/g,m=>({'<':'&lt;','>':'&gt;','&':'&amp;'}[m]))+'</li>').join('');
 $('log').textContent=s.tail||'';
 clearTimeout(timer);timer=setTimeout(load,s.running?3000:30000);
}
$('go').onclick=async()=>{ if(!confirm('Запустити синхронізацію з Хорошопом? Ціни й наявність у Shopify буде оновлено, нові товари створено.'))return;
 $('go').disabled=true;const r=await fetch('/api/sync',{method:'POST'});const s=await r.json();if(!s.ok)alert(s.error||'Не вдалося запустити');load();};
load();
</script></body></html>"""
