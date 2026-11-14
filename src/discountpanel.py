#!/usr/bin/env python3
"""«Знижки» — a page of the editor service (14.11.2026, «список по коллекциям всех товаров, к каждому процентная или цифровая скидка,
сворачивать по коллекциям, по кнопке применить, текущие скидки показывать»). The list comes live from the Horoshop catalogue
(catalog/export, the fields that matter), grouped by the site's categories; a change is sent with catalog/import, which updates only
the fields it is given. Two kinds of discount, as Horoshop keeps them: a percentage (`discount`) or a fixed amount in гривні
(`price` lowered, the full price kept in `price_old`). Mounted by src/deck-editor.py: GET /discounts, GET|POST /api/discounts.
After applying, the Shopify store follows on the next run of /sync.
"""
import json, pathlib, sys, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src")); import horoshop as H

FIELDS = ["article", "parent_article", "title", "mod_title", "price", "price_old", "discount", "parent", "alt_parent", "display_in_showcase", "presence", "currency", "link"]

def full_uah(p):
    return max(float(p.get("price") or 0), float(p.get("price_old") or 0))

def rows():
    """The catalogue as the page needs it: one row per article, the category path, the full price, the current discount and the price the storefront charges."""
    h = H.Horoshop(); prods = h.products(includedParams=FIELDS); rate = h.rates().get("USD") or 35.5
    out = []
    for p in prods:
        if not p.get("article"): continue
        price = float(p.get("price") or 0); old = float(p.get("price_old") or 0); pct = float(p.get("discount") or 0)
        full = max(price, old); now = price * (1 - pct / 100)
        kind = "pct" if pct else ("amt" if old > price else "")
        out.append(dict(article=p["article"], parent=p.get("parent_article") or p["article"], name=(H.L(p.get("mod_title"), "ua") or H.L(p.get("title"), "ua")).strip(),
                        category=H.L(p.get("parent"), "ua") or "—", collections=[H.L(a, "ua") for a in p.get("alt_parent") or [] if H.L(a, "ua").startswith("Колекції/")],
                        full=full, now=round(now, 2), pct=pct, amt=round(full - now, 2), kind=kind, shown=int(p.get("display_in_showcase") or 0),
                        presence=H.presence(p), link=p.get("link") or ""))
    out.sort(key=lambda r: (r["category"], r["parent"], r["article"]))
    return dict(ok=True, at=time.strftime("%Y-%m-%d %H:%M"), rate=rate, rows=out)

def apply(body):
    """body = {items: [{article, kind: 'pct'|'amt'|'none', value}]} → catalog/import. A percentage clears any amount discount and vice versa."""
    items = body.get("items") or []
    if not items: return dict(ok=False, error="Немає змін.")
    h = H.Horoshop(); cur = {p["article"]: p for p in h.products(includedParams=["article", "price", "price_old", "discount"]) if p.get("article")}
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
        prods.append(upd); plan.append(dict(article=a, **{k: v for k, v in upd.items() if k != "article"}))
    res = h.call("catalog/import", {"products": prods}) if prods else {}
    log = {l.get("article"): l for l in (res.get("log") or [])}
    for pl in plan:
        l = log.get(pl["article"]); pl["result"] = "; ".join(m.get("message", "") for m in (l or {}).get("info", [])) if l else pl.get("error", "немає відповіді")
    return dict(ok=True, applied=len(prods), plan=plan)

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
td.num,th.num{text-align:right;white-space:nowrap}td.art{color:var(--muted);font-size:12.5px;white-space:nowrap}td.name a{color:inherit;text-decoration:none}td.name a:hover{text-decoration:underline}
.cur{white-space:nowrap}.cur b{font-weight:500;color:var(--ok)}.cur s{color:var(--muted)}.hid{color:var(--muted);font-size:12px}
input.v{width:64px;border:1px solid var(--line);border-radius:8px;padding:6px 8px;font:inherit;text-align:right;background:#fff}input.v:focus{outline:2px solid var(--yel);border-color:transparent}
tr.changed td{background:var(--mark)}select.k{border:1px solid var(--line);border-radius:8px;padding:6px;font:inherit;background:#fff}
.clear{border:0;background:none;color:var(--muted);cursor:pointer;font-size:13px;padding:4px 6px}.clear:hover{color:var(--bad)}
.bar{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:1px solid var(--line);padding:12px 20px;display:flex;gap:16px;align-items:center;justify-content:center;box-shadow:0 -6px 24px rgba(0,0,0,.06)}
.bar .cnt{color:var(--muted);font-size:14px}button.go{appearance:none;border:0;border-radius:999px;background:var(--yel);color:var(--ink);font:inherit;font-weight:500;padding:12px 26px;cursor:pointer}button.go:disabled{background:#d9d3c8;color:#8a8378;cursor:default}
button.ghost{appearance:none;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink);font:inherit;padding:11px 18px;cursor:pointer}
.msg{font-size:14px}.msg.ok{color:var(--ok)}.msg.bad{color:var(--bad)}#load{color:var(--muted);padding:40px 0;text-align:center}
</style></head><body><main>
<h1>Знижки</h1>
<p class="sub">Товари obiimy.world за категоріями сайту. Знижка задається у відсотках або в гривнях від повної ціни і записується в Хорошоп кнопкою «Застосувати»; у Shopify підтягується наступною <a href="/sync" id="lnk">синхронізацією</a>.</p>
<div class="top">
 <input type="search" id="q" placeholder="Пошук за назвою або артикулом">
 <label><input type="checkbox" id="onlyd"> лише зі знижкою</label>
 <button class="ghost" id="reload">Оновити з Хорошопу</button>
 <span class="hid" id="at"></span>
</div>
<div id="load">Завантажую каталог…</div>
<div id="groups"></div>
</main>
<div class="bar"><span class="cnt" id="cnt">Змін немає</span><button class="go" id="apply" disabled>Застосувати</button><span class="msg" id="msg"></span></div>
<script>
const KEY=new URLSearchParams(location.search).get('key')||'';const api=(u,o={})=>fetch(u+(u.includes('?')?'&':'?')+'key='+encodeURIComponent(KEY),o);
const $=id=>document.getElementById(id);let ROWS=[],CH={};
const money=v=>Number(v).toLocaleString('uk-UA',{maximumFractionDigits:0})+' грн';
const esc=s=>String(s).replace(/[<>&"]/g,m=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[m]));
async function load(keepMsg){ $('load').hidden=false;$('groups').innerHTML='';CH={};upd(keepMsg);
 const r=await api('/api/discounts',{cache:'no-store'});const d=await r.json();$('load').hidden=true;
 if(!d.ok){$('groups').innerHTML='<p class="msg bad">'+esc(d.error||'Помилка')+'</p>';return}
 ROWS=d.rows;$('at').textContent='дані з сайту на '+d.at+', курс '+d.rate;render();}
function render(){
 const q=$('q').value.trim().toLowerCase(),od=$('onlyd').checked;const groups={};
 for(const r of ROWS){ if(q&&!(r.name.toLowerCase().includes(q)||r.article.toLowerCase().includes(q)))continue; if(od&&!r.kind&&!CH[r.article])continue; (groups[r.category]=groups[r.category]||[]).push(r);}
 const open=new Set([...document.querySelectorAll('details[open]')].map(d=>d.dataset.g));
 $('groups').innerHTML=Object.keys(groups).sort().map(g=>{const rs=groups[g];const nd=rs.filter(r=>r.kind).length;
  return '<details data-g="'+esc(g)+'"'+(open.has(g)||q?' open':'')+'><summary>'+esc(g)+' <span class="n">'+rs.length+' арт.</span>'+(nd?'<span class="d">зі знижкою: '+nd+'</span>':'')+'</summary>'
  +'<div class="gfill">усій групі: <select class="k" data-gk="'+esc(g)+'"><option value="pct">%</option><option value="amt">грн</option></select><input class="v" data-gv="'+esc(g)+'" placeholder="0"><button class="ghost" style="padding:5px 12px;font-size:13px" data-gset="'+esc(g)+'">заповнити</button><button class="clear" data-gclr="'+esc(g)+'">зняти всі знижки групи</button></div>'
  +'<table><tr><th>Артикул</th><th>Товар</th><th class="num">Повна ціна</th><th class="num">Зараз</th><th>Нова знижка</th><th></th></tr>'
  +rs.map(r=>{const c=CH[r.article];const kind=c?c.kind:(r.kind||'pct');const val=c?c.value:(r.kind==='pct'?r.pct:(r.kind==='amt'?r.amt:''));
   return '<tr data-a="'+esc(r.article)+'"'+(c?' class="changed"':'')+'><td class="art">'+esc(r.article)+(r.shown?'':' <span class="hid">прихований</span>')+'</td><td class="name">'+(r.link?'<a href="'+esc(r.link)+'" target="_blank" rel="noopener">'+esc(r.name)+'</a>':esc(r.name))+(r.presence!=='In stock'?' <span class="hid">немає в наявності</span>':'')+'</td>'
   +'<td class="num">'+money(r.full)+'</td><td class="num cur">'+(r.kind?'<b>'+money(r.now)+'</b> <s>'+money(r.full)+'</s> <span class="hid">'+(r.kind==='pct'?'−'+r.pct+'%':'−'+money(r.amt))+'</span>':'—')+'</td>'
   +'<td><input class="v" data-v="'+esc(r.article)+'" value="'+esc(val)+'" placeholder="0"> <select class="k" data-k="'+esc(r.article)+'"><option value="pct"'+(kind==='pct'?' selected':'')+'>%</option><option value="amt"'+(kind==='amt'?' selected':'')+'>грн</option></select></td>'
   +'<td>'+(r.kind||c?'<button class="clear" data-clr="'+esc(r.article)+'" title="зняти знижку">зняти</button>':'')+'</td></tr>'}).join('')+'</table></details>'}).join('')||'<p class="hid">Нічого не знайдено.</p>';
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
$('q').oninput=render;$('onlyd').onchange=render;$('reload').onclick=load;
$('apply').onclick=async()=>{const items=Object.entries(CH).map(([article,c])=>({article,kind:c.kind,value:c.value}));
 if(!confirm('Записати '+items.length+' змін у Хорошоп? Ціни на сайті зміняться одразу.'))return;
 $('apply').disabled=true;$('msg').textContent='Записую…';$('msg').className='msg';
 const r=await api('/api/discounts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items})});const d=await r.json();
 if(!d.ok){$('msg').textContent=d.error||'Помилка';$('msg').className='msg bad';$('apply').disabled=false;return}
 const bad=d.plan.filter(p=>!/оновлен/i.test(p.result||''));$('msg').textContent=bad.length?('Записано '+(d.applied-bad.length)+', з помилками '+bad.length+': '+bad.map(p=>p.article+' — '+p.result).join('; ')):('Записано: '+d.applied+'. Щоб оновити Shopify, запустіть синхронізацію.');$('msg').className='msg '+(bad.length?'bad':'ok');
 await load(true);};
if(KEY){const l=document.getElementById('lnk');if(l)l.href+='?key='+encodeURIComponent(KEY);}
load();
</script></body></html>"""
