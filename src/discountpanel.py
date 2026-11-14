#!/usr/bin/env python3
"""«Знижки» — a page of the editor service (14.11.2026, «список по коллекциям всех товаров, к каждому процентная или цифровая скидка,
сворачивать по коллекциям, по кнопке применить, текущие скидки показывать»). The list comes live from the Horoshop catalogue
(catalog/export, the fields that matter), grouped by the site's categories; a change is sent with catalog/import, which updates only
the fields it is given. Two kinds of discount, as Horoshop keeps them: a percentage (`discount`) or a fixed amount in гривні
(`price` lowered, the full price kept in `price_old`). Mounted by src/deck-editor.py: GET /discounts, GET|POST /api/discounts.
After applying, the Shopify store follows on the next run of /sync.
"""
import json, pathlib, re, sys, time, uuid
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src")); import horoshop as H
LOG = ROOT / "data" / "horoshop" / "discounts-log.jsonl"     # one line per apply or rollback: who (ip, browser), when, each article before → after

def _log_write(entry):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f: f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def log_entries(limit=300):
    """Newest first; an entry rolled back later carries `rolled_back_by` so the page can grey it out."""
    if not LOG.exists(): return []
    rows = [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]
    undone = {e.get("rollback_of"): e["id"] for e in rows if e.get("rollback_of")}
    for e in rows: e["rolled_back_by"] = undone.get(e["id"])
    return list(reversed(rows))[:limit]

def _state(p):
    return {"price": float(p.get("price") or 0), "price_old": float(p.get("price_old") or 0), "discount": float(p.get("discount") or 0)}

FIELDS = ["article", "parent_article", "title", "mod_title", "price", "price_old", "discount", "parent", "alt_parent", "display_in_showcase", "presence", "currency", "link", "images", "gallery_common"]

def thumb(p):
    """The site's own 120 px thumbnail of the first picture: …/images/<n>/<name>_+<hash>.jpg → …/images/<n>/120x120l80nn0/<name>.webp (falls back to the original in the page)."""
    pics = (p.get("images") or []) + (p.get("gallery_common") or [])
    if not pics: return "", ""
    import re
    m = re.match(r"(https://[^/]+/content/images/\d+/)(.+?)(?:_\+[0-9a-f]+)?\.(jpe?g|png|webp)$", pics[0])
    return (f"{m.group(1)}120x120l80nn0/{m.group(2)}.webp" if m else pics[0]), pics[0]

def full_uah(p):
    return max(float(p.get("price") or 0), float(p.get("price_old") or 0))

STOCK_WAREHOUSE = int(__import__("os").environ.get("STOCK_WAREHOUSE_ID") or 1)   # KeyCRM warehouse «1 Склад Світлана» — the only one that counts (the client, 14.11.2026)
_stock_cache = {"at": 0, "map": {}}

def _crm_key(article, keys):
    """The site's article → the code the warehouse uses: 44-xx and 44-xx-D became P-44-xx there, a few spellings differ."""
    if article in keys: return article
    m = re.match(r"^44-(\d+)(-D)?$", article)
    if m and f"P-44-{m.group(1)}{m.group(2) or ''}" in keys: return f"P-44-{m.group(1)}{m.group(2) or ''}"
    alt = {"140-15-6": "140/15-6"}.get(article)
    return alt if alt in keys else None

def stock_map(force=False):
    """{article in KeyCRM: (quantity, reserve)} on the chosen warehouse, from GET /offers/stocks?filter[details]=true (Bimp → KeyCRM every 15 min).
    Cached 10 minutes; an empty map when KeyCRM is not configured or fails — the page then shows no stock column values."""
    import keycrm as K
    if not force and time.time() - _stock_cache["at"] < 600: return _stock_cache["map"]
    out = {}
    try:
        if K.KEY:
            page = 1
            while page <= 40:
                r = K.api("GET", "/offers/stocks", params={"limit": 50, "page": page, "filter[details]": "true"}); data = r.get("data") or []
                for x in data:
                    if not x.get("sku"): continue
                    w = next((w for w in x.get("warehouse") or [] if int(w.get("id") or 0) == STOCK_WAREHOUSE), None)
                    out[x["sku"]] = ((float(w.get("quantity") or 0), float(w.get("reserve") or 0)) if w else (None, None)) + (float(x.get("quantity") or 0), float(x.get("reserve") or 0))   # + the total over all warehouses
                if len(data) < 50: break
                page += 1
        _stock_cache.update(at=time.time(), map=out)
    except Exception as e:
        sys.stderr.write(f"keycrm stocks: {e}\n")
    return _stock_cache["map"] or out

def rows():
    """The catalogue as the page needs it: one row per article, the category path, the full price, the current discount and the price the storefront charges."""
    h = H.Horoshop(); prods = h.products(includedParams=FIELDS); rate = h.rates().get("USD") or 35.5
    st = stock_map(); out = []
    for p in prods:
        if not p.get("article"): continue
        price = float(p.get("price") or 0); old = float(p.get("price_old") or 0); pct = float(p.get("discount") or 0)
        full = max(price, old); now = price * (1 - pct / 100)
        kind = "pct" if pct else ("amt" if old > price else "")
        k = _crm_key(p["article"], st); q = st.get(k) if k else None      # None → not in the warehouse system; (None, None) → in the system, not on this warehouse
        out.append(dict(stock=(q[0] if q and q[0] is not None else (0.0 if q else None)), reserve=(q[1] if q and q[1] is not None else 0.0), stock_all=(q[2] if q else None), reserve_all=(q[3] if q else 0.0), crm_sku=k,article=p["article"], parent=p.get("parent_article") or p["article"], name=(H.L(p.get("mod_title"), "ua") or H.L(p.get("title"), "ua")).strip(),
                        category=H.L(p.get("parent"), "ua") or "—", collections=[H.L(a, "ua") for a in p.get("alt_parent") or [] if H.L(a, "ua").startswith("Колекції/")],
                        full=full, now=round(now, 2), pct=pct, amt=round(full - now, 2), kind=kind, shown=int(p.get("display_in_showcase") or 0),
                        presence=H.presence(p), link=p.get("link") or "", thumb=thumb(p)[0], pic=thumb(p)[1]))
    out.sort(key=lambda r: (r["category"], r["parent"], r["article"]))
    return dict(ok=True, at=time.strftime("%Y-%m-%d %H:%M"), rate=rate, rows=out, stock_at=time.strftime("%H:%M", time.localtime(_stock_cache["at"])) if _stock_cache["at"] else None, warehouse=STOCK_WAREHOUSE)

def _import(h, prods, plan):
    res = h.call("catalog/import", {"products": prods}) if prods else {}
    log = {l.get("article"): l for l in (res.get("log") or [])}
    for pl in plan:
        l = log.get(pl["article"]); pl["result"] = "; ".join(m.get("message", "") for m in (l or {}).get("info", [])) if l else pl.get("error", "немає відповіді")

def apply(body, who=None):
    """body = {items: [{article, kind: 'pct'|'amt'|'none', value}]} → catalog/import. A percentage clears any amount discount and vice versa.
    Every call is logged with the previous and the new values, so it can be rolled back from the page."""
    items = body.get("items") or []
    if not items: return dict(ok=False, error="Немає змін.")
    h = H.Horoshop(); cur = {p["article"]: p for p in h.products(includedParams=["article", "price", "price_old", "discount", "mod_title", "title"]) if p.get("article")}
    prods, plan = [], []
    for it in items:
        a = str(it.get("article") or "").strip(); p = cur.get(a)
        if not p: plan.append(dict(article=a, error="не знайдено")); continue
        full = full_uah(p); kind = it.get("kind") or "none"
        try: v = float(it.get("value") or 0)
        except ValueError: v = 0
        if kind == "pct" and 0 < v < 100: upd = {"article": a, "price": full, "price_old": 0, "discount": round(v, 2)}
        elif kind == "amt" and 0 < v < full: upd = {"article": a, "price": round(full - v, 2), "price_old": full, "discount": 0}
        else: upd = {"article": a, "price": full, "price_old": 0, "discount": 0}
        prods.append(upd); plan.append(dict(article=a, name=(H.L(p.get("mod_title"), "ua") or H.L(p.get("title"), "ua")).strip(), before=_state(p), after={k: v for k, v in upd.items() if k != "article"}))
    _import(h, prods, plan)
    entry = dict(id=uuid.uuid4().hex[:10], at=time.strftime("%Y-%m-%d %H:%M:%S"), kind="apply", who=who or {}, items=plan, applied=len(prods))
    _log_write(entry)
    return dict(ok=True, applied=len(prods), plan=plan, entry_id=entry["id"])

def rollback(body, who=None):
    """body = {id} → every article of that log entry gets its `before` values back (price, price_old, discount); logged as its own entry."""
    eid = str(body.get("id") or ""); entries = {e["id"]: e for e in log_entries(100000)}
    e = entries.get(eid)
    if not e: return dict(ok=False, error="Запис журналу не знайдено.")
    if e.get("rolled_back_by"): return dict(ok=False, error="Цей запис уже відкочено.")
    h = H.Horoshop(); cur = {p["article"]: p for p in h.products(includedParams=["article", "price", "price_old", "discount", "mod_title", "title"]) if p.get("article")}
    prods, plan = [], []
    for it in e["items"]:
        a = it["article"]; b = it.get("before"); p = cur.get(a)
        if not b or not p: plan.append(dict(article=a, error="не знайдено")); continue
        upd = {"article": a, "price": b["price"], "price_old": b["price_old"], "discount": b["discount"]}
        prods.append(upd); plan.append(dict(article=a, name=it.get("name", ""), before=_state(p), after={k: v for k, v in upd.items() if k != "article"}))
    _import(h, prods, plan)
    entry = dict(id=uuid.uuid4().hex[:10], at=time.strftime("%Y-%m-%d %H:%M:%S"), kind="rollback", rollback_of=eid, who=who or {}, items=plan, applied=len(prods))
    _log_write(entry)
    return dict(ok=True, applied=len(prods), plan=plan, entry_id=entry["id"])

PAGE = """<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Знижки</title>
<style>
:root{--ink:#141110;--muted:#6b645c;--line:#e6e0d6;--paper:#f7f3ec;--yel:#f4c430;--ok:#1f7a3a;--bad:#b3261e;--mark:#fff3c4}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.45 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:1100px;margin:0 auto;padding:36px 20px 120px}h1{font-weight:500;font-size:26px;margin:0 0 4px}.sub{color:var(--muted);margin:0 0 20px;font-size:14px}
.top{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:18px}.top input[type=search]{flex:1;min-width:220px;border:1px solid var(--line);border-radius:999px;padding:9px 14px;font:inherit;background:#fff}
.top label{color:var(--muted);font-size:14px}.top a{color:var(--muted)}
details{background:#fff;border:1px solid var(--line);border-radius:12px;margin:0 0 10px;overflow:hidden}summary{cursor:pointer;list-style:none;padding:12px 16px;display:flex;gap:12px;align-items:center;font-weight:500}
summary::before{content:"▸";color:var(--muted);transition:transform .15s}details[open] summary::before{transform:rotate(90deg)}summary .n{color:var(--muted);font-weight:400;font-size:13px}summary .d{margin-left:auto;font-weight:400;font-size:13px;color:var(--ok)}
.gfill{display:flex;gap:8px;align-items:center;padding:0 16px 10px 36px;font-size:13px;color:var(--muted)}.gfill input{width:70px}
table{width:100%;border-collapse:collapse}th,td{padding:7px 10px;border-top:1px solid var(--line);text-align:left;vertical-align:middle;font-size:14px}th{color:var(--muted);font-weight:500;font-size:12px;text-transform:uppercase;letter-spacing:.04em}
td.num,th.num{text-align:right;white-space:nowrap}td.art{color:var(--muted);font-size:12.5px;white-space:nowrap}td.pic{width:56px;padding:4px 6px}td.pic img{width:48px;height:48px;object-fit:cover;border-radius:8px;background:#f1ece3;display:block}td.pic span{display:block;width:48px;height:48px;border-radius:8px;background:#f1ece3}td.name a{color:inherit;text-decoration:none}td.name a:hover{text-decoration:underline}
.cur{white-space:nowrap}td.stock{white-space:nowrap;font-weight:500}td.stock.zero{color:var(--bad)}.cur b{font-weight:500;color:var(--ok)}.cur s{color:var(--muted)}.hid{color:var(--muted);font-size:12px}
input.v{width:64px;border:1px solid var(--line);border-radius:8px;padding:6px 8px;font:inherit;text-align:right;background:#fff}input.v:focus{outline:2px solid var(--yel);border-color:transparent}
tr.changed td{background:var(--mark)}select.k{border:1px solid var(--line);border-radius:8px;padding:6px;font:inherit;background:#fff}
.clear{border:0;background:none;color:var(--muted);cursor:pointer;font-size:13px;padding:4px 6px}.clear:hover{color:var(--bad)}
.bar{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:1px solid var(--line);padding:12px 20px;display:flex;gap:16px;align-items:center;justify-content:center;box-shadow:0 -6px 24px rgba(0,0,0,.06)}
.bar .cnt{color:var(--muted);font-size:14px}button.go{appearance:none;border:0;border-radius:999px;background:var(--yel);color:var(--ink);font:inherit;font-weight:500;padding:12px 26px;cursor:pointer}button.go:disabled{background:#d9d3c8;color:#8a8378;cursor:default}
button.ghost{appearance:none;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink);font:inherit;padding:11px 18px;cursor:pointer}
.msg{font-size:14px}.msg.ok{color:var(--ok)}.msg.bad{color:var(--bad)}#load{color:var(--muted);padding:40px 0;text-align:center}
#logbox{margin-top:28px}#logbox summary{font-weight:500}.le{padding:10px 16px;border-top:1px solid var(--line);font-size:14px}.le.undone{opacity:.55}.le .h{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.le .h b{font-weight:500}.le .h .k{font-size:12px;border-radius:999px;padding:2px 8px;background:#f1ece3;color:var(--muted)}.le .h .k.rb{background:#fde7e4;color:var(--bad)}.le .h button{margin-left:auto}
.le ul{margin:6px 0 0;padding-left:18px;color:var(--muted);font-size:13px}.le li b{color:var(--ink);font-weight:500}
</style></head><body><main>
<h1>Знижки</h1>
<p class="sub">Товари obiimy.world за категоріями сайту; колонка «Залишок» — за даними KeyCRM (Bimp оновлює їх кожні 15 хв): склад «1 Склад Світлана» або всі склади разом, перемикач у фільтрі. Знижка задається у відсотках або в гривнях від повної ціни і записується в Хорошоп кнопкою «Застосувати»; у Shopify підтягується наступною <a href="/sync" id="lnk">синхронізацією</a>. Є також <a href="/portrait" id="lnk2">портрет клієнта</a>.</p>
<div class="top">
 <input type="search" id="q" placeholder="Пошук за назвою або артикулом">
 <label><input type="checkbox" id="onlyd"> лише зі знижкою</label>
 <label>склад <select class="k" id="wh"><option value="1">1 Склад Світлана</option><option value="all">усі склади</option></select></label>
 <label title="Залишок за даними KeyCRM">залишок від <input class="v" id="qmin" placeholder="0" style="width:56px"> до <input class="v" id="qmax" placeholder="∞" style="width:56px"></label>
 <button class="ghost" id="reload">Оновити з Хорошопу</button>
 <span class="hid" id="at"></span>
</div>
<div id="load">Завантажую каталог…</div>
<div id="groups"></div>
<details id="logbox"><summary>Журнал змін <span class="hid" id="logn"></span></summary><div id="log"></div></details>
</main>
<div class="bar"><span class="cnt" id="cnt">Змін немає</span><button class="go" id="apply" disabled>Застосувати</button><span class="msg" id="msg"></span></div>
<script>
const KEY=new URLSearchParams(location.search).get('key')||'';const api=(u,o={})=>fetch(u+(u.includes('?')?'&':'?')+'key='+encodeURIComponent(KEY),o);
const $=id=>document.getElementById(id);let ROWS=[],CH={};
const money=v=>Number(v).toLocaleString('uk-UA',{maximumFractionDigits:0})+' грн';
const ST=r=>$('wh').value==='all'?r.stock_all:r.stock, RS=r=>$('wh').value==='all'?r.reserve_all:r.reserve;
const esc=s=>String(s).replace(/[<>&"]/g,m=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[m]));
async function load(keepMsg){ $('load').hidden=false;$('groups').innerHTML='';CH={};upd(keepMsg);
 const r=await api('/api/discounts',{cache:'no-store'});const d=await r.json();$('load').hidden=true;
 if(!d.ok){$('groups').innerHTML='<p class="msg bad">'+esc(d.error||'Помилка')+'</p>';return}
 ROWS=d.rows;$('at').textContent='дані з сайту на '+d.at+', курс '+d.rate+(d.stock_at?', залишки складу 1 з KeyCRM на '+d.stock_at:', залишки недоступні');render();}
function render(){
 const q=$('q').value.trim().toLowerCase(),od=$('onlyd').checked;const qmin=$('qmin').value===''?null:parseFloat($('qmin').value),qmax=$('qmax').value===''?null:parseFloat($('qmax').value);const groups={};
 for(const r of ROWS){ if(q&&!(r.name.toLowerCase().includes(q)||r.article.toLowerCase().includes(q)))continue; if(od&&!r.kind&&!CH[r.article])continue;
  if(qmin!==null||qmax!==null){const st=ST(r)===null?0:ST(r); if(qmin!==null&&st<qmin)continue; if(qmax!==null&&st>qmax)continue;}
  (groups[r.category]=groups[r.category]||[]).push(r);}
 const open=new Set([...document.querySelectorAll('details[open]')].map(d=>d.dataset.g));
 $('groups').innerHTML=Object.keys(groups).sort().map(g=>{const rs=groups[g];const nd=rs.filter(r=>r.kind).length;
  const stq=rs.reduce((a,r)=>a+(ST(r)||0),0);return '<details data-g="'+esc(g)+'"'+(open.has(g)||q||$('qmin').value||$('qmax').value?' open':'')+'><summary>'+esc(g)+' <span class="n">'+rs.length+' арт. · на складі '+Math.round(stq)+' шт.</span>'+(nd?'<span class="d">зі знижкою: '+nd+'</span>':'')+'</summary>'
  +'<div class="gfill">усій групі: <select class="k" data-gk="'+esc(g)+'"><option value="pct">%</option><option value="amt">грн</option></select><input class="v" data-gv="'+esc(g)+'" placeholder="0"><button class="ghost" style="padding:5px 12px;font-size:13px" data-gset="'+esc(g)+'">заповнити</button><button class="clear" data-gclr="'+esc(g)+'">зняти всі знижки групи</button></div>'
  +'<table><tr><th></th><th>Артикул</th><th>Товар</th><th class="num">Повна ціна</th><th class="num">Зараз</th><th class="num" title="За даними KeyCRM">Залишок</th><th>Нова знижка</th><th></th></tr>'
  +rs.map(r=>{const c=CH[r.article];const kind=c?c.kind:(r.kind||'pct');const val=c?c.value:(r.kind==='pct'?r.pct:(r.kind==='amt'?r.amt:''));
   return '<tr data-a="'+esc(r.article)+'"'+(c?' class="changed"':'')+'><td class="pic">'+(r.thumb?'<img data-src="'+esc(r.thumb)+'" data-f="'+esc(r.pic)+'" alt="" onerror="if(!this.dataset.o){this.dataset.o=1;this.src=this.dataset.f}">':'<span></span>')+'</td><td class="art">'+esc(r.article)+(r.shown?'':' <span class="hid">прихований</span>')+'</td><td class="name">'+(r.link?'<a href="'+esc(r.link)+'" target="_blank" rel="noopener">'+esc(r.name)+'</a>':esc(r.name))+(r.presence!=='In stock'?' <span class="hid">немає в наявності</span>':'')+'</td>'
   +'<td class="num">'+money(r.full)+'</td><td class="num stock'+(r.stock===null?' hid':(r.stock<=0?' zero':''))+'">'+(r.stock===null?'—':(Math.round(r.stock)+(r.reserve?' <span class="hid">(рез. '+Math.round(r.reserve)+')</span>':'')))+'</td><td class="num cur">'+(r.kind?'<b>'+money(r.now)+'</b> <s>'+money(r.full)+'</s> <span class="hid">'+(r.kind==='pct'?'−'+r.pct+'%':'−'+money(r.amt))+'</span>':'—')+'</td>'
   +'<td><input class="v" data-v="'+esc(r.article)+'" value="'+esc(val)+'" placeholder="0"> <select class="k" data-k="'+esc(r.article)+'"><option value="pct"'+(kind==='pct'?' selected':'')+'>%</option><option value="amt"'+(kind==='amt'?' selected':'')+'>грн</option></select></td>'
   +'<td>'+(r.kind||c?'<button class="clear" data-clr="'+esc(r.article)+'" title="зняти знижку">зняти</button>':'')+'</td></tr>'}).join('')+'</table></details>'}).join('')||'<p class="hid">Нічого не знайдено.</p>';
 document.querySelectorAll('details[open]').forEach(showPics);
}
function setChange(a,kind,value){const r=ROWS.find(x=>x.article===a);if(!r)return;const v=parseFloat(String(value).replace(',','.'))||0;
 const same=(v===0&&!r.kind)||(kind==='pct'&&r.kind==='pct'&&v===r.pct)||(kind==='amt'&&r.kind==='amt'&&v===r.amt);
 if(same)delete CH[a];else CH[a]={kind:v?kind:'none',value:v};upd();}
function upd(keep){const n=Object.keys(CH).length;$('cnt').textContent=n?'Змін: '+n:'Змін немає';$('apply').disabled=!n;if(!keep)$('msg').textContent='';}
document.addEventListener('input',e=>{const t=e.target;if(t.dataset.v!==undefined){const a=t.dataset.v;setChange(a,document.querySelector('[data-k="'+CSS.escape(a)+'"]').value,t.value);t.closest('tr').classList.toggle('changed',!!CH[a]);}});
document.addEventListener('change',e=>{const t=e.target;if(t.dataset.k!==undefined){const a=t.dataset.k;const v=document.querySelector('[data-v="'+CSS.escape(a)+'"]').value;if(v)setChange(a,t.value,v);t.closest('tr').classList.toggle('changed',!!CH[a]);}});
document.addEventListener('click',e=>{const t=e.target;
 if(t.dataset.clr!==undefined){const a=t.dataset.clr;const r=ROWS.find(x=>x.article===a);if(r.kind)CH[a]={kind:'none',value:0};else delete CH[a];upd();render();}
 if(t.dataset.gset!==undefined){const g=t.dataset.gset;const kind=document.querySelector('[data-gk="'+CSS.escape(g)+'"]').value;const v=document.querySelector('[data-gv="'+CSS.escape(g)+'"]').value;if(!v)return;for(const r of ROWS)if(r.category===g)setChange(r.article,kind,v);render();}
 if(t.dataset.gclr!==undefined){const g=t.dataset.gclr;for(const r of ROWS)if(r.category===g){if(r.kind)CH[r.article]={kind:'none',value:0};else delete CH[r.article];}upd();render();}
});
function showPics(d){d.querySelectorAll('td.pic img[data-src]').forEach(i=>{i.src=i.dataset.src;i.removeAttribute('data-src');});}
document.addEventListener('toggle',e=>{if(e.target.tagName==='DETAILS'&&e.target.open)showPics(e.target);},true);
$('q').oninput=render;$('onlyd').onchange=render;$('qmin').oninput=render;$('qmax').oninput=render;$('wh').onchange=render;$('reload').onclick=load;
const fmt=s=>s.discount?('−'+s.discount+'% від '+money(s.price)):(s.price_old>s.price?(money(s.price)+' (повна '+money(s.price_old)+')'):money(s.price));
async function loadLog(){const r=await api('/api/discounts/log',{cache:'no-store'});const d=await r.json();if(!d.ok)return;$('logn').textContent=d.entries.length?('· '+d.entries.length):'';
 $('log').innerHTML=d.entries.map(e=>{const who=(e.who&&e.who.ip)?' · '+e.who.ip:'';const items=e.items.slice(0,40).map(i=>'<li><b>'+esc(i.article)+'</b> '+esc(i.name||'')+(i.before&&i.after?': '+esc(fmt(i.before))+' → '+esc(fmt(i.after)):'')+(i.result&&!/оновлен|обновлен/i.test(i.result)?' <span style="color:var(--bad)">'+esc(i.result)+'</span>':'')+'</li>').join('')+(e.items.length>40?'<li>… ще '+(e.items.length-40)+'</li>':'');
 return '<div class="le'+(e.rolled_back_by?' undone':'')+'"><div class="h"><b>'+esc(e.at)+'</b><span class="k'+(e.kind==='rollback'?' rb':'')+'">'+(e.kind==='rollback'?'відкат запису '+esc(e.rollback_of):'зміна')+'</span><span class="hid">'+e.applied+' арт.'+esc(who)+'</span>'+(e.rolled_back_by?'<span class="hid">відкочено</span>':(e.kind==='apply'?'<button class="ghost" style="padding:5px 12px;font-size:13px" data-rb="'+esc(e.id)+'">Відкотити</button>':'<button class="ghost" style="padding:5px 12px;font-size:13px" data-rb="'+esc(e.id)+'">Відкотити відкат</button>'))+'</div><ul>'+items+'</ul></div>'}).join('')||'<div class="le hid">Змін ще не було.</div>';}
document.addEventListener('click',async e=>{const t=e.target;if(t.dataset.rb===undefined)return;if(!confirm('Повернути значення, які були до цієї зміни? Ціни на сайті зміняться одразу.'))return;t.disabled=true;
 const r=await api('/api/discounts/rollback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:t.dataset.rb})});const d=await r.json();
 $('msg').textContent=d.ok?('Відкочено: '+d.applied+' арт.'):(d.error||'Помилка');$('msg').className='msg '+(d.ok?'ok':'bad');await loadLog();await load(true);});
loadLog();
$('apply').onclick=async()=>{const items=Object.entries(CH).map(([article,c])=>({article,kind:c.kind,value:c.value}));
 if(!confirm('Записати '+items.length+' змін у Хорошоп? Ціни на сайті зміняться одразу.'))return;
 $('apply').disabled=true;$('msg').textContent='Записую…';$('msg').className='msg';
 const r=await api('/api/discounts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items})});const d=await r.json();
 if(!d.ok){$('msg').textContent=d.error||'Помилка';$('msg').className='msg bad';$('apply').disabled=false;return}
 const bad=d.plan.filter(p=>!/оновлен|обновлен/i.test(p.result||''));$('msg').textContent=bad.length?('Записано '+(d.applied-bad.length)+', з помилками '+bad.length+': '+bad.map(p=>p.article+' — '+p.result).join('; ')):('Записано: '+d.applied+'. Щоб оновити Shopify, запустіть синхронізацію.');$('msg').className='msg '+(bad.length?'bad':'ok');
 await load(true);await loadLog();};
if(KEY){for(const id of ['lnk','lnk2']){const l=document.getElementById(id);if(l)l.href+='?key='+encodeURIComponent(KEY);}}
load();
</script></body></html>"""
