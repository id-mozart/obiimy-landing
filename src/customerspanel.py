#!/usr/bin/env python3
"""«Клієнти» — a page of the editor service (15.11.2026, «вытащить из KeyCRM все емейлы клиентов с датой последнего заказа, количеством
заказов и суммой, имена и телефоны, табличку на отдельную страничку с возможностью скачать файлом — для рассылки рекламистов»).
Every order of KeyCRM (GET /order?include=buyer, 50 a page, limit 120 requests a minute) is pulled once into data/horoshop/keycrm-customers.json
and then refreshed by `filter[updated_between]`; the page groups the orders by the buyer's e-mail (or phone, or buyer id when there is
neither) and shows name, e-mail, phone, number of orders, sum in гривня, first and last order, channel. The CSV is built in the browser
from the filtered rows. Mounted by src/deck-editor.py behind the manager's key: GET /customers, GET /api/customers, POST /api/customers/refresh.
Personal data: the page and the API need the key, nothing is written anywhere but the volume cache.
"""
import json, pathlib, re, sys, threading, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
CACHE = ROOT / "data" / "horoshop" / "keycrm-customers.json"
USD_SOURCES = {10, 17, 18}                 # ETSY_NEW, SHOPIFY, Shopify_new keep their sums in dollars
PARTNER_SOURCES = {5, 9}                   # «ПАРТНЕРИ», «ПАРТНЕРИ продажі» — resellers, hidden by default (the client, 15.11.2026)
SKIP_STATUSES = {19, 20}                   # canceled, «Задвоєні дані» — not orders
RATE = float(__import__("os").environ.get("KEYCRM_USD_RATE") or 35.5)
_state = {"loading": None, "error": None}
_lock = threading.Lock()

def _load():
    try: return json.loads(CACHE.read_text(encoding="utf-8"))
    except Exception: return {"at": None, "orders": {}, "sources": {}}

def _save(c):
    CACHE.parent.mkdir(parents=True, exist_ok=True); tmp = CACHE.with_suffix(".tmp"); tmp.write_text(json.dumps(c, ensure_ascii=False), encoding="utf-8"); tmp.replace(CACHE)

def _slim(o):
    b = o.get("buyer") or {}
    return dict(id=o["id"], at=(o.get("ordered_at") or o.get("created_at") or "")[:19].replace("T", " "), src=int(o.get("source_id") or 0), st=int(o.get("status_id") or 0),
                total=float(o.get("grand_total") or 0), bid=b.get("id"), name=(b.get("full_name") or "").strip(), email=(b.get("email") or "").strip().lower(), phone=(b.get("phone") or "").strip())

def _refresh(full):
    import keycrm as K
    try:
        c = _load()
        if full or not c.get("orders"): c = {"at": None, "orders": {}, "sources": {}}
        try: c["sources"] = {str(s["id"]): s["name"] for s in (K.api("GET", "/order/source", params={"limit": 50}).get("data") or [])}
        except Exception as e: sys.stderr.write(f"keycrm sources: {e}\n")
        params = {"limit": 50, "include": "buyer", "sort": "-id"}
        if c.get("at"):   # anything touched since the last run (status changes included), with a day of overlap
            since = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.mktime(time.strptime(c["at"], "%Y-%m-%d %H:%M:%S")) - 86400))
            params["filter[updated_between]"] = f"{since},{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 86400))}"
        started = time.strftime("%Y-%m-%d %H:%M:%S"); page = 1
        while True:
            _state["loading"] = dict(page=page, last=_state["loading"]["last"] if _state["loading"] else None)
            r = K.api("GET", "/order", params={**params, "page": page}); data = r.get("data") or []
            for o in data: c["orders"][str(o["id"])] = _slim(o)
            _state["loading"]["last"] = r.get("last_page")
            if page >= int(r.get("last_page") or 1) or not data: break
            page += 1; time.sleep(0.55)   # ≈ 100 requests a minute, under KeyCRM's 120
        c["at"] = started; _save(c); _state["error"] = None
    except Exception as e:
        _state["error"] = str(e)[:300]; sys.stderr.write(f"keycrm customers: {e}\n")
    finally:
        _state["loading"] = None

def refresh(full=False):
    with _lock:
        if _state["loading"]: return dict(ok=True, loading=_state["loading"])
        _state["loading"] = dict(page=0, last=None)
        threading.Thread(target=_refresh, args=(bool(full),), daemon=True).start()
    return dict(ok=True, loading=_state["loading"])

DAILY = 86400
def _age():
    at = _load().get("at")
    try: return time.time() - time.mktime(time.strptime(at, "%Y-%m-%d %H:%M:%S")) if at else float("inf")
    except ValueError: return float("inf")

def _scheduler():
    """Once a day (the client, 15.11.2026: «автосинхронизацию раз в день»): whenever the cache is older than 24 h, pull what changed in KeyCRM."""
    while True:
        try:
            if _age() > DAILY and not _state["loading"]: refresh()
        except Exception as e: sys.stderr.write(f"customers scheduler: {e}\n")
        time.sleep(600)

def start_scheduler():
    threading.Thread(target=_scheduler, daemon=True).start()

def _digits(p): return re.sub(r"\D", "", p or "")

def customers():
    """{ok, at, loading, error, sources, rows:[{key, name, email, phone, orders, sum, first, last, src, srcs, usd}]} — one row per customer."""
    c = _load()
    if not c.get("orders") and not _state["loading"]: refresh()
    by = {}
    for o in c.get("orders", {}).values():
        if o["st"] in SKIP_STATUSES: continue
        key = ("e:" + o["email"]) if o["email"] else (("p:" + _digits(o["phone"])) if _digits(o["phone"]) else ("b:" + str(o["bid"] or o["id"])))
        r = by.setdefault(key, dict(key=key, name="", email=o["email"], phone="", orders=0, sum=0.0, first=o["at"], last="", src=0, srcs=set(), usd=False, _lastat=""))
        r["orders"] += 1; usd = o["src"] in USD_SOURCES; r["sum"] += o["total"] * (RATE if usd else 1); r["usd"] = r["usd"] or usd
        r["srcs"].add(o["src"]); r["first"] = min(r["first"], o["at"]) if r["first"] else o["at"]
        if o["at"] >= r["_lastat"]:   # name, phone and channel from the most recent order
            r["_lastat"] = o["at"]; r["last"] = o["at"][:10]; r["src"] = o["src"]
            if o["name"]: r["name"] = o["name"]
            if o["phone"]: r["phone"] = o["phone"]
            if o["email"]: r["email"] = o["email"]
    rows = []
    for r in by.values():
        r.pop("_lastat"); r["first"] = r["first"][:10]; r["sum"] = round(r["sum"]); r["srcs"] = sorted(r["srcs"]); rows.append(r)
    rows.sort(key=lambda r: r["last"], reverse=True)
    return dict(ok=True, at=c.get("at"), loading=_state["loading"], error=_state["error"], daily=True, sources=c.get("sources", {}), partner_sources=sorted(PARTNER_SOURCES), usd_sources=sorted(USD_SOURCES), rate=RATE, rows=rows)

import re as _re
_PATR = _re.compile(r"(ович|евич|йович|ійович|івна|ївна|овна|евна|іївна|ovich|ovna)$", _re.I)
_STRONG = _re.compile(r"(енко|єнко|чук|щук|юк|ук|ський|ська|ский|ская|цький|цька|цкий|цкая|зький|зька|ич|ець|ун|ян|ай|ей|ів|ов|ев|єв|ова|ева|єва|ко)$", _re.I)   # endings first names never have
def first_name(full, common=frozenset()):
    """«Прізвище Ім’я По батькові» or «Ім’я Прізвище» → the first name alone. Rules, in order: the word right before a patronymic;
    a word from `common` (first names seen many times across all buyers); a word without a surname ending; else the first word."""
    toks = [x for x in _re.split(r"[\s,()]+", (full or "").strip()) if x and _re.match(r"^[A-Za-zА-ЯІЇЄҐа-яіїєґ'’\-]{2,}$", x)]
    if not toks: return ""
    cap = lambda s: s[:1].upper() + s[1:]
    for i, x in enumerate(toks):
        if _PATR.search(x) and i > 0: return cap(toks[i - 1])
    for x in toks:
        if x.lower() in common: return cap(x)
    cand = [x for x in toks if not _PATR.search(x) and not _STRONG.search(x)]
    return cap((cand or toks)[0])

def common_names(rows, min_count=3):
    """Words that repeat across many buyers' names are first names (Олена, Наталія, Андрій…) — minus surname-shaped words and
    the words seen in the surname position of three-word names («Прізвище Ім’я По батькові»)."""
    cnt, surn = {}, set()
    for r in rows:
        toks = [x for x in _re.split(r"[\s,()]+", (r.get("name") or "").lower()) if len(x) >= 2]
        if len(toks) >= 3 and _PATR.search(toks[2]): surn.add(toks[0])
        for x in set(toks):
            if not _PATR.search(x): cnt[x] = cnt.get(x, 0) + 1
    return frozenset(x for x, n in cnt.items() if n >= min_count and x not in surn and not _STRONG.search(x))

def contacts():
    """The advertisers' view: first name, phone, e-mail — nothing else (the client, 16.11.2026)."""
    c = customers(); common = common_names(c["rows"])
    return dict(ok=True, at=c["at"], loading=c["loading"], error=c["error"], rows=[dict(name=first_name(r["name"], common), phone=r["phone"], email=r["email"]) for r in c["rows"] if r["src"] not in PARTNER_SOURCES])

CONTACTS_PAGE = r"""<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Контакти</title>
<style>
:root{--ink:#141110;--muted:#6b645c;--line:#e6e0d6;--paper:#f7f3ec;--yel:#f4c430;--ok:#1f7a3a;--bad:#b3261e;--mark:#fff3c4}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.45 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:960px;margin:0 auto;padding:28px 20px 60px}h1{font-weight:500;font-size:26px;margin:0}.hd{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:14px}.hd .sp{flex:1}.hid{color:var(--muted);font-size:12.5px}
button.ghost{appearance:none;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink);font:inherit;padding:7px 14px;cursor:pointer;font-size:13.5px}
.panel{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin:0 0 12px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.search{flex:1;min-width:240px;position:relative}.search input{width:100%;border:1px solid var(--line);border-radius:999px;padding:10px 38px;font:inherit;font-size:15px;background:#fbf9f5}.search input:focus{outline:2px solid var(--yel);border-color:transparent;background:#fff}.search .ico{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--muted)}
.tog{border:1px solid var(--line);border-radius:999px;padding:6px 11px;font-size:13.5px;background:#fff;cursor:pointer;color:var(--muted);font:inherit}.tog.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.sum{color:var(--muted);font-size:13.5px;width:100%}.sum b{color:var(--ink);font-weight:500}.how{font-size:13.5px;color:var(--muted);margin:0 0 12px}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:auto}table{width:100%;border-collapse:collapse}th,td{padding:8px 12px;border-top:1px solid var(--line);text-align:left;font-size:14px;white-space:nowrap}th{color:var(--muted);font-weight:500;font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;position:sticky;top:0;background:#fff}td.e a{color:inherit}mark{background:var(--mark);padding:0 1px;border-radius:2px}.empty{padding:28px;text-align:center;color:var(--muted)}.msg{font-size:13.5px}.msg.ok{color:var(--ok)}.msg.bad{color:var(--bad)}
@media(max-width:700px){main{padding:16px 12px 40px}}
</style></head><body><main>
<div class="hd"><h1>Контакти</h1><span class="hid" id="at"></span><span class="sp"></span><button class="ghost" id="copy">Скопіювати email</button><button class="ghost" id="csv">Завантажити CSV</button></div>
<p class="how">Покупці OBIIMY для розсилок: ім’я, телефон, email. Один рядок на людину. Дані персональні — використовувати лише для комунікації від імені OBIIMY і нікому не передавати.</p>
<section class="panel"><div class="search"><span class="ico">⌕</span><input type="search" id="q" placeholder="Пошук: ім’я, email, телефон" autocomplete="off"></div><button class="tog on" id="em">лише з email</button><button class="tog" id="ph">лише з телефоном</button><span class="sum" id="sum"></span><span class="msg" id="msg"></span></section>
<div class="card"><table id="t"></table></div>
<script>
const KEY=new URLSearchParams(location.search).get('key')||'';const api=(u,o={})=>fetch(u+(u.includes('?')?'&':'?')+'key='+encodeURIComponent(KEY),o);const $=id=>document.getElementById(id);
let ROWS=[],timer=null;const F={q:'',email:true,phone:false};
const esc=s=>String(s??'').replace(/[<>&"]/g,m=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[m]));const plural=(n,a,b,c)=>{const m=n%10,h=n%100;return n+' '+(m===1&&h!==11?a:(m>=2&&m<=4&&(h<12||h>14)?b:c))};
const hl=(s,tk)=>{let h=esc(s);if(!tk.length)return h;const re=new RegExp('('+tk.map(t=>esc(t).replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')','gi');return h.replace(re,'<mark>$1</mark>')};
function filtered(){const tk=F.q.trim().toLowerCase().split(/\s+/).filter(Boolean);return ROWS.filter(r=>(!F.email||r.email)&&(!F.phone||r.phone)&&(!tk.length||tk.every(t=>(r.name+' '+r.email+' '+r.phone).toLowerCase().includes(t))));}
function render(){const rows=filtered(),tk=F.q.trim().toLowerCase().split(/\s+/).filter(Boolean);rows.sort((a,b)=>a.name.localeCompare(b.name,'uk'));
 $('sum').innerHTML=ROWS.length?'Контактів: <b>'+rows.length+'</b> із '+ROWS.length+' · з email: '+rows.filter(r=>r.email).length+' · з телефоном: '+rows.filter(r=>r.phone).length:'';
 $('t').innerHTML='<tr><th>Ім’я</th><th>Телефон</th><th>Email</th></tr>'+rows.slice(0,4000).map(r=>'<tr><td>'+hl(r.name||'—',tk)+'</td><td>'+hl(r.phone,tk)+'</td><td class="e">'+(r.email?'<a href="mailto:'+esc(r.email)+'">'+hl(r.email,tk)+'</a>':'<span class="hid">—</span>')+'</td></tr>').join('')+(rows.length?'':'<tr><td colspan="3" class="empty">'+(ROWS.length?'Нікого не знайдено.':'Дані ще завантажуються…')+'</td></tr>');window.__rows=rows;}
async function load(){const r=await api('/api/contacts',{cache:'no-store'});const d=await r.json();if(!d.ok){$('msg').textContent=d.error||'Помилка';$('msg').className='msg bad';return}ROWS=d.rows;$('at').textContent=d.at?'дані на '+d.at.slice(0,16):'';render();if(d.loading){$('msg').textContent='Завантажую…';clearTimeout(timer);timer=setTimeout(load,4000);}else $('msg').textContent='';}
$('q').oninput=()=>{F.q=$('q').value;render();};$('em').onclick=()=>{F.email=!F.email;$('em').classList.toggle('on',F.email);render();};$('ph').onclick=()=>{F.phone=!F.phone;$('ph').classList.toggle('on',F.phone);render();};
const csvCell=v=>{v=String(v??'');return /[;"\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v};
$('csv').onclick=()=>{const rows=window.__rows||[];const blob=new Blob(['\ufeff'+['Ім’я;Телефон;Email',...rows.map(r=>[r.name,r.phone,r.email].map(csvCell).join(';'))].join('\r\n')],{type:'text/csv;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='obiimy-kontakty-'+new Date().toISOString().slice(0,10)+'.csv';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),5000);$('msg').textContent='CSV: '+rows.length+' рядків.';$('msg').className='msg ok';};
$('copy').onclick=async()=>{const em=[...new Set((window.__rows||[]).map(r=>r.email).filter(Boolean))];try{await navigator.clipboard.writeText(em.join(', '));$('msg').textContent='Скопійовано '+plural(em.length,'адресу','адреси','адрес')+'.';$('msg').className='msg ok';}catch(e){prompt('Скопіюйте вручну',em.join(', '));}};
load();
</script></body></html>"""

PAGE = r"""<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Клієнти</title>
<style>
:root{--ink:#141110;--muted:#6b645c;--line:#e6e0d6;--paper:#f7f3ec;--yel:#f4c430;--ok:#1f7a3a;--bad:#b3261e;--mark:#fff3c4}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.45 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:1200px;margin:0 auto;padding:28px 20px 60px}h1{font-weight:500;font-size:26px;margin:0}
.hd{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:14px}.hd .sp{flex:1}.hid{color:var(--muted);font-size:12.5px}
button.ghost{appearance:none;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink);font:inherit;padding:7px 14px;cursor:pointer;font-size:13.5px}button.ghost:disabled{opacity:.5;cursor:default}button.go{appearance:none;border:0;border-radius:999px;background:var(--yel);color:var(--ink);font:inherit;font-weight:500;padding:8px 16px;cursor:pointer;font-size:13.5px}
.panel{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin:0 0 12px;display:flex;flex-direction:column;gap:10px}
.row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.row .sp{flex:1}
.search{flex:1;min-width:240px;position:relative}.search input{width:100%;border:1px solid var(--line);border-radius:999px;padding:10px 38px;font:inherit;font-size:15px;background:#fbf9f5}.search input:focus{outline:2px solid var(--yel);border-color:transparent;background:#fff}.search .ico{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--muted)}
details.pop{position:relative;margin:0}details.pop summary{list-style:none;cursor:pointer;padding:6px 11px;border:1px solid var(--line);border-radius:999px;background:#fff;font-size:13.5px;color:var(--muted);display:flex;gap:5px;align-items:center;white-space:nowrap}summary::-webkit-details-marker{display:none}details.pop summary b{color:var(--ink);font-weight:500}details.pop summary::after{content:"▾";font-size:11px;opacity:.7}details.pop[open] summary{border-color:var(--ink)}details.pop.on summary{background:var(--ink);border-color:var(--ink);color:#e9e3d9}details.pop.on summary b{color:#fff}
.menu{position:absolute;top:calc(100% + 6px);left:0;z-index:20;background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 12px 32px rgba(0,0,0,.12);padding:8px;min-width:300px;max-height:400px;overflow:auto}.mi{display:flex;gap:8px;align-items:center;padding:6px 8px;border-radius:8px;cursor:pointer;font-size:14px}.mi:hover{background:var(--paper)}.mi input{width:16px;height:16px;accent-color:#141110;margin:0}.mi span:first-of-type{flex:1}.mi .n{color:var(--muted);font-size:12px}.menu hr{border:0;border-top:1px solid var(--line);margin:6px 0}.menu .mb{padding:4px 8px;font-size:13px;color:var(--muted)}.clear{border:0;background:none;color:var(--muted);cursor:pointer;font-size:13px;padding:4px 6px}.clear:hover{color:var(--bad)}
.tog{border:1px solid var(--line);border-radius:999px;padding:6px 11px;font-size:13.5px;background:#fff;cursor:pointer;color:var(--muted);font:inherit}.tog.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.sum{color:var(--muted);font-size:13.5px}.sum b{color:var(--ink);font-weight:500}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:auto}table{width:100%;border-collapse:collapse}th,td{padding:7px 10px;border-top:1px solid var(--line);text-align:left;vertical-align:top;font-size:13.5px;white-space:nowrap}th{color:var(--muted);font-weight:500;font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;cursor:pointer;user-select:none;position:sticky;top:0;background:#fff}th.s{color:var(--ink)}td.num,th.num{text-align:right}td.name{white-space:normal;min-width:160px}td.e a{color:inherit}mark{background:var(--mark);padding:0 1px;border-radius:2px}
.empty{padding:28px;text-align:center;color:var(--muted)}.msg{font-size:13.5px}.msg.ok{color:var(--ok)}.msg.bad{color:var(--bad)}.prog{height:6px;background:#efe9df;border-radius:999px;overflow:hidden;width:220px}.prog i{display:block;height:100%;background:var(--yel);width:0;transition:width .4s}
.how{font-size:13.5px;color:var(--muted);margin:0 0 12px}
@media(max-width:700px){main{padding:16px 12px 40px}.menu{position:fixed;left:12px;right:12px;min-width:0}}
</style></head><body><main>
<div class="hd"><h1>Клієнти</h1><span class="hid" id="at"></span><span class="sp"></span><button class="ghost" id="copy">Скопіювати email</button><button class="ghost" id="csv">Завантажити CSV</button><button class="ghost" id="reload">Оновити з KeyCRM</button></div>
<p class="how">Усі покупці з KeyCRM, один рядок на клієнта (за email; без email — за телефоном). Сума в гривнях; замовлення Etsy і Shopify у доларах переведено за курсом <span id="rate"></span> і позначені «≈». Скасовані й задвоєні замовлення не рахуються. CSV і «Скопіювати email» беруть те, що відфільтровано на екрані. Дані персональні: сторінка за ключем, нікуди не пересилати без потреби.</p>
<section class="panel">
 <div class="row"><div class="search"><span class="ico">⌕</span><input type="search" id="q" placeholder="Пошук: ім’я, email, телефон" autocomplete="off"></div></div>
 <div class="row" id="pops"></div>
 <div class="row"><span class="sum" id="sum"></span><span class="sp"></span><span class="msg" id="msg"></span><span class="prog" id="prog" hidden><i></i></span></div>
</section>
<div class="card"><table id="t"></table></div>
<script>
const KEY=new URLSearchParams(location.search).get('key')||'';const api=(u,o={})=>fetch(u+(u.includes('?')?'&':'?')+'key='+encodeURIComponent(KEY),o);const $=id=>document.getElementById(id);
let ROWS=[],SRC={},PART=[],USD=[],SORT={k:'last',d:-1},timer=null;
const F={q:'',email:true,src:null,orders:'any',last:'any',sum:'any'};
const esc=s=>String(s??'').replace(/[<>&"]/g,m=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[m]));const num=v=>Number(v).toLocaleString('uk-UA',{maximumFractionDigits:0});
const srcName=id=>SRC[id]||('канал '+id);const plural=(n,a,b,c)=>{const m=n%10,h=n%100;return n+' '+(m===1&&h!==11?a:(m>=2&&m<=4&&(h<12||h>14)?b:c))};
const defSrc=()=>Object.keys(SRC).filter(id=>!PART.includes(+id));
const daysAgo=d=>{const t=new Date(d+'T00:00:00');return (Date.now()-t)/86400000};
const POPS=[
 {id:'src',l:'Канал',text:()=>{const s=F.src||defSrc();const all=Object.keys(SRC);return s.length===all.length?'усі':(s.length===defSrc().length&&s.every(x=>defSrc().includes(x))?'без партнерів':plural(s.length,'канал','канали','каналів'))},on:()=>!!F.src&&!(F.src.length===defSrc().length&&F.src.every(x=>defSrc().includes(x))),
  menu:()=>{const s=new Set(F.src||defSrc());const cnt={};for(const r of ROWS)cnt[r.src]=(cnt[r.src]||0)+1;return '<div class="mb"><button class="clear" data-act="srcall">усі канали</button><button class="clear" data-act="srcdef">без партнерів</button></div><hr>'+Object.keys(SRC).sort((a,b)=>(cnt[b]||0)-(cnt[a]||0)).map(id=>'<label class="mi"><input type="checkbox" data-src="'+id+'"'+(s.has(id)?' checked':'')+'> <span>'+esc(SRC[id])+(PART.includes(+id)?' <span class="n">партнери</span>':'')+'</span><span class="n">'+(cnt[id]||0)+'</span></label>').join('')}},
 {id:'orders',l:'Замовлень',opts:[['any','будь-скільки'],['1','одне'],['2','2 і більше'],['3','3 і більше'],['5','5 і більше']],def:'any'},
 {id:'last',l:'Останнє замовлення',opts:[['any','будь-коли'],['30','за 30 днів'],['90','за 90 днів'],['365','за рік'],['old','давніше року']],def:'any'},
 {id:'sum',l:'Сума',opts:[['any','будь-яка'],['2000','від 2 000 грн'],['5000','від 5 000 грн'],['10000','від 10 000 грн']],def:'any'}];
for(const p of POPS)if(p.opts){p.text=()=>(p.opts.find(o=>o[0]===F[p.id])||p.opts[0])[1];p.on=()=>F[p.id]!==p.def;p.menu=()=>p.opts.map(([v,l])=>'<label class="mi"><input type="radio" name="r'+p.id+'" data-opt="'+p.id+'" value="'+v+'"'+(F[p.id]===v?' checked':'')+'> <span>'+l+'</span></label>').join('');}
$('pops').innerHTML='<button class="tog on" id="em">лише з email</button>'+POPS.map(p=>'<details class="pop" data-pop="'+p.id+'"><summary>'+p.l+': <b></b></summary><div class="menu"></div></details>').join('');
function menus(){for(const p of POPS){const d=document.querySelector('[data-pop="'+p.id+'"]');d.querySelector('b').textContent=p.text();d.classList.toggle('on',!!p.on());d.querySelector('.menu').innerHTML=p.menu();}$('em').classList.toggle('on',F.email);}
const hl=(s,tk)=>{let h=esc(s);if(!tk.length)return h;const re=new RegExp('('+tk.map(t=>esc(t).replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')','gi');return h.replace(re,'<mark>$1</mark>')};
function filtered(){const tk=F.q.trim().toLowerCase().split(/\s+/).filter(Boolean);const src=new Set((F.src||defSrc()).map(Number));
 return ROWS.filter(r=>{if(F.email&&!r.email)return false;if(!r.srcs.some(s=>src.has(s)))return false;if(F.orders!=='any'&&!(F.orders==='1'?r.orders===1:r.orders>=+F.orders))return false;
  if(F.last!=='any'){const d=daysAgo(r.last);if(F.last==='old'?d<=365:d>+F.last)return false;}if(F.sum!=='any'&&r.sum<+F.sum)return false;
  if(tk.length){const hay=(r.name+' '+r.email+' '+r.phone).toLowerCase();if(!tk.every(t=>hay.includes(t)))return false;}return true;});}
const COLS=[['name','Ім’я'],['email','Email'],['phone','Телефон'],['orders','Замовлень','num'],['sum','Сума, грн','num'],['first','Перше','num'],['last','Останнє','num'],['src','Канал']];
function render(){const rows=filtered();const tk=F.q.trim().toLowerCase().split(/\s+/).filter(Boolean);
 rows.sort((a,b)=>{let x=a[SORT.k],y=b[SORT.k];if(SORT.k==='src'){x=srcName(x);y=srcName(y)}if(typeof x==='string')return SORT.d*x.localeCompare(y,'uk');return SORT.d*((x||0)-(y||0))});
 const ne=rows.filter(r=>r.email).length,no=rows.reduce((a,r)=>a+r.orders,0),ns=rows.reduce((a,r)=>a+r.sum,0);
 $('sum').innerHTML=ROWS.length?'Клієнтів: <b>'+rows.length+'</b> із '+ROWS.length+' · з email: <b>'+ne+'</b> · замовлень: '+num(no)+' · сума: '+num(ns)+' грн':'';
 $('t').innerHTML='<tr>'+COLS.map(([k,l,c])=>'<th class="'+(c||'')+(SORT.k===k?' s':'')+'" data-s="'+k+'">'+l+(SORT.k===k?(SORT.d>0?' ↑':' ↓'):'')+'</th>').join('')+'</tr>'
  +rows.slice(0,3000).map(r=>'<tr><td class="name">'+hl(r.name||'—',tk)+'</td><td class="e">'+(r.email?'<a href="mailto:'+esc(r.email)+'">'+hl(r.email,tk)+'</a>':'<span class="hid">немає</span>')+'</td><td>'+hl(r.phone,tk)+'</td><td class="num">'+r.orders+'</td><td class="num">'+(r.usd?'≈ ':'')+num(r.sum)+'</td><td class="num hid">'+esc(r.first)+'</td><td class="num">'+esc(r.last)+'</td><td class="hid">'+esc(srcName(r.src))+(r.srcs.length>1?' +'+(r.srcs.length-1):'')+'</td></tr>').join('')
  +(rows.length>3000?'<tr><td colspan="8" class="hid">показано перші 3 000, решта — у CSV</td></tr>':'')+(rows.length?'':'<tr><td colspan="8" class="empty">'+(ROWS.length?'Нікого не знайдено.':'Дані ще завантажуються з KeyCRM…')+'</td></tr>');
 window.__rows=rows;}
async function load(){const r=await api('/api/customers',{cache:'no-store'});const d=await r.json();if(!d.ok){$('msg').textContent=d.error||'Помилка';$('msg').className='msg bad';return}
 ROWS=d.rows;SRC=d.sources||{};PART=d.partner_sources||[];USD=d.usd_sources||[];$('rate').textContent=d.rate;if(F.src)F.src=F.src.filter(id=>SRC[id]);
 $('at').textContent=d.at?'дані KeyCRM на '+d.at+' · оновлюються автоматично раз на добу':'';menus();render();
 if(d.loading){const l=d.loading;$('prog').hidden=false;$('prog').firstElementChild.style.width=(l.last?Math.round(l.page/l.last*100):3)+'%';$('msg').textContent='Завантажую з KeyCRM: сторінка '+l.page+(l.last?' із '+l.last:'')+'…';$('msg').className='msg';$('reload').disabled=true;clearTimeout(timer);timer=setTimeout(load,3000);}
 else{$('prog').hidden=true;$('reload').disabled=false;if(d.error){$('msg').textContent='KeyCRM: '+d.error;$('msg').className='msg bad';}else if($('msg').textContent.startsWith('Завантажую')){$('msg').textContent='Оновлено.';$('msg').className='msg ok';}}}
$('reload').onclick=async()=>{await api('/api/customers/refresh',{method:'POST'});load();};
$('q').oninput=()=>{F.q=$('q').value;render();};$('em').onclick=()=>{F.email=!F.email;menus();render();};
document.addEventListener('change',e=>{const t=e.target;if(t.dataset.opt!==undefined){const pop=t.closest('.pop');F[t.dataset.opt]=t.value;menus();render();pop.open=false;}
 if(t.dataset.src!==undefined){const s=new Set(F.src||defSrc());t.checked?s.add(t.dataset.src):s.delete(t.dataset.src);F.src=Object.keys(SRC).filter(id=>s.has(id));menus();render();}});
document.addEventListener('click',e=>{const t=e.target;if(t.dataset.act==='srcall'){F.src=Object.keys(SRC);menus();render();}if(t.dataset.act==='srcdef'){F.src=null;menus();render();}
 if(t.dataset.s){SORT=SORT.k===t.dataset.s?{k:SORT.k,d:-SORT.d}:{k:t.dataset.s,d:t.dataset.s==='name'||t.dataset.s==='email'?1:-1};render();}
 if(!t.closest('.pop'))document.querySelectorAll('.pop[open]').forEach(d=>d.open=false);else{const p=t.closest('.pop');document.querySelectorAll('.pop[open]').forEach(d=>{if(d!==p)d.open=false});}});
document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.pop[open]').forEach(d=>d.open=false);});
const csvCell=v=>{v=String(v??'');return /[;"\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v};
$('csv').onclick=()=>{const rows=window.__rows||[];const head=['Ім’я','Email','Телефон','Замовлень','Сума, грн','Перше замовлення','Останнє замовлення','Канал','Усі канали'];
 const body=rows.map(r=>[r.name,r.email,r.phone,r.orders,r.sum,r.first,r.last,srcName(r.src),r.srcs.map(srcName).join(', ')].map(csvCell).join(';'));
 const blob=new Blob(['﻿'+[head.join(';'),...body].join('\r\n')],{type:'text/csv;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='obiimy-klienty-'+new Date().toISOString().slice(0,10)+'.csv';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),5000);
 $('msg').textContent='CSV: '+rows.length+' рядків. Відкривається в Excel, Numbers і Google Таблицях (розділювач «;»).';$('msg').className='msg ok';};
$('copy').onclick=async()=>{const em=[...new Set((window.__rows||[]).map(r=>r.email).filter(Boolean))];try{await navigator.clipboard.writeText(em.join(', '));$('msg').textContent='Скопійовано '+plural(em.length,'адресу','адреси','адрес')+'.';$('msg').className='msg ok';}catch(e){prompt('Скопіюйте вручну',em.join(', '));}};
load();
</script></body></html>"""
