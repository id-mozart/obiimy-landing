#!/usr/bin/env python3
"""«Партнери» — a page of the editor service (24.11.2026, the client: «провести исследование и составить таблицу львовских и киевских
компаний — косметологических, ювелирных, юридических, стоматологических, пластическая хирургия, магазины подарков — с названием,
телефоном, адресом, емейлом, отдельный столбец город; для потенциального партнёрства; выложить на marketing.obiimy.world/partners»).
The rows live in src/partners.json (gathered 24.11.2026 from the companies' own sites; every row keeps the URL where the phone and
address were seen — nothing is invented, a missing e-mail stays empty). Mounted by src/deck-editor.py: GET /partners (behind the
advertisers' guest password, like /portrait) and GET /api/partners (the JSON). The page filters by city and category, searches,
copies the e-mails and downloads a CSV."""
import json, pathlib
HERE = pathlib.Path(__file__).parent
CATEGORIES = ["Косметологія", "Ювелірні", "Юридичні", "Стоматологія", "Пластична хірургія", "Магазини подарунків"]
CITIES = ["Київ", "Львів"]

def rows():
    """The directory as the page and the CSV see it: a clean, de-duplicated list in the order category → city → name."""
    data = json.loads((HERE / "partners.json").read_text(encoding="utf-8"))
    out, seen = [], set()
    for r in data:
        key = (r.get("city", ""), (r.get("name") or "").strip().lower())
        if key in seen or not r.get("name"): continue
        seen.add(key)
        out.append({k: (r.get(k) or "").strip() for k in ("category", "city", "name", "phone", "address", "email", "website", "source", "note")})
    order = {c: i for i, c in enumerate(CATEGORIES)}; corder = {c: i for i, c in enumerate(CITIES)}
    out.sort(key=lambda r: (order.get(r["category"], 99), corder.get(r["city"], 99), r["name"].lower()))
    return dict(ok=True, rows=out, categories=CATEGORIES, cities=CITIES, at="24.11.2026")

PAGE = r"""<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Партнери</title>
<style>
:root{--ink:#141110;--muted:#6b645c;--line:#e6e0d6;--paper:#f7f3ec;--yel:#f4c430;--ok:#1f7a3a;--bad:#b3261e;--mark:#fff3c4;--gold:#9a7430}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.45 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:1240px;margin:0 auto;padding:28px 20px 60px}h1{font-weight:500;font-size:26px;margin:0}.hd{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:10px}.hd .sp{flex:1}.hid{color:var(--muted);font-size:12.5px}
button.ghost{appearance:none;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink);font:inherit;padding:7px 14px;cursor:pointer;font-size:13.5px}button.ghost:hover{border-color:var(--ink)}
.how{font-size:13.5px;color:var(--muted);margin:0 0 12px;max-width:70em}
.panel{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin:0 0 12px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.search{flex:1;min-width:220px;position:relative}.search input{width:100%;border:1px solid var(--line);border-radius:999px;padding:10px 38px;font:inherit;font-size:15px;background:#fbf9f5}.search input:focus{outline:2px solid var(--yel);border-color:transparent}.search .ico{position:absolute;left:14px;top:9px;color:var(--muted)}
.tog{border:1px solid var(--line);border-radius:999px;padding:6px 11px;font-size:13.5px;background:#fff;cursor:pointer;color:var(--muted);font:inherit}.tog.on{background:var(--ink);color:#fff;border-color:var(--ink)}.tog.city.on{background:var(--yel);color:var(--ink);border-color:var(--yel)}
.grp{display:flex;gap:6px;flex-wrap:wrap;align-items:center}.grp .l{font-size:12px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;margin-right:2px}
.sum{color:var(--muted);font-size:13.5px;width:100%}.sum b{color:var(--ink);font-weight:500}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:auto}table{width:100%;border-collapse:collapse}th,td{padding:8px 12px;border-top:1px solid var(--line);text-align:left;font-size:14px;vertical-align:top}th{color:var(--muted);font-weight:500;font-size:12.5px;letter-spacing:.04em;text-transform:uppercase;border-top:0;background:#fbf9f5;white-space:nowrap;position:sticky;top:52px}
td.n{font-weight:500;min-width:180px}td.c{white-space:nowrap}td.p{white-space:nowrap}td.a{min-width:220px;color:#3a3530}td.e a,td.w a{color:var(--gold);text-decoration:none}td.e a:hover,td.w a:hover{text-decoration:underline}td .note{display:block;color:var(--muted);font-size:12.5px}td .src{color:var(--muted);text-decoration:none;font-size:12px}td .src:hover{text-decoration:underline}
mark{background:var(--mark);padding:0 1px;border-radius:2px}.cat{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 8px;font-size:12px;color:var(--muted);white-space:nowrap}
.msg{font-size:13.5px;margin:8px 0 0;min-height:18px}.msg.ok{color:var(--ok)}.msg.bad{color:var(--bad)}
@media(max-width:700px){main{padding:16px 12px 40px}th{position:static}}
</style></head><body><main>
<div class="hd"><h1>Партнери</h1><span class="hid" id="at"></span><span class="sp"></span><button class="ghost" id="copy">Скопіювати email</button><button class="ghost" id="csv">Завантажити CSV</button></div>
<p class="how">Компанії Києва і Львова для потенційного партнерства OBIIMY: косметологія, ювелірні, юридичні, стоматологія, пластична хірургія, магазини подарунків. Назва, телефон, адреса й email — із сайтів самих компаній (посилання «джерело» в кожному рядку); де email не опубліковано, клітинка порожня.</p>
<section class="panel">
 <div class="search"><span class="ico">⌕</span><input type="search" id="q" placeholder="Пошук: назва, адреса, телефон, email" autocomplete="off"></div>
 <div class="grp" id="cities"><span class="l">Місто</span></div>
 <div class="grp" id="cats"><span class="l">Категорія</span></div>
 <button class="tog" id="em">лише з email</button>
 <div class="sum" id="sum"></div>
</section>
<div class="card"><table id="t"></table></div>
<p class="msg" id="msg"></p>
<script>
const KEY=new URLSearchParams(location.search).get('key')||'';const api=(u,o={})=>fetch(u+(KEY?(u.includes('?')?'&':'?')+'key='+encodeURIComponent(KEY):''),o);const $=id=>document.getElementById(id);
let ROWS=[],CATS=[],CITIES=[];const F={q:'',email:false,city:new Set(),cat:new Set()};
const esc=s=>String(s??'').replace(/[<>&"]/g,m=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[m]));
const hl=(s,tk)=>{let h=esc(s);if(!tk.length)return h;const re=new RegExp('('+tk.map(t=>esc(t).replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')','gi');return h.replace(re,'<mark>$1</mark>')};
const tokens=()=>F.q.trim().toLowerCase().split(/\s+/).filter(Boolean);
function filtered(){const tk=tokens();return ROWS.filter(r=>(!F.email||r.email)&&(!F.city.size||F.city.has(r.city))&&(!F.cat.size||F.cat.has(r.category))&&(!tk.length||tk.every(t=>(r.name+' '+r.address+' '+r.phone+' '+r.email+' '+r.website+' '+r.category+' '+r.city).toLowerCase().includes(t))));}
function chips(){
 $('cities').innerHTML='<span class="l">Місто</span>'+CITIES.map(c=>'<button class="tog city'+(F.city.has(c)?' on':'')+'" data-c="'+esc(c)+'">'+esc(c)+' <small>'+ROWS.filter(r=>r.city===c).length+'</small></button>').join('');
 $('cats').innerHTML='<span class="l">Категорія</span>'+CATS.map(c=>'<button class="tog cat'+(F.cat.has(c)?' on':'')+'" data-c="'+esc(c)+'">'+esc(c)+' <small>'+ROWS.filter(r=>r.category===c).length+'</small></button>').join('');
 document.querySelectorAll('#cities .tog').forEach(b=>b.onclick=()=>{const c=b.dataset.c;F.city.has(c)?F.city.delete(c):F.city.add(c);chips();render();});
 document.querySelectorAll('#cats .tog').forEach(b=>b.onclick=()=>{const c=b.dataset.c;F.cat.has(c)?F.cat.delete(c):F.cat.add(c);chips();render();});
}
function render(){const rows=filtered(),tk=tokens();window.__rows=rows;
 $('sum').innerHTML=ROWS.length?'Компаній: <b>'+rows.length+'</b> із '+ROWS.length+' · Київ: '+rows.filter(r=>r.city==='Київ').length+' · Львів: '+rows.filter(r=>r.city==='Львів').length+' · з email: '+rows.filter(r=>r.email).length:'';
 $('t').innerHTML='<tr><th>Назва</th><th>Місто</th><th>Категорія</th><th>Телефон</th><th>Адреса</th><th>Email</th><th>Сайт</th></tr>'+rows.map(r=>'<tr><td class="n">'+hl(r.name,tk)+(r.note?'<span class="note">'+esc(r.note)+'</span>':'')+(r.source?'<a class="src" href="'+esc(r.source)+'" target="_blank" rel="noopener">джерело ↗</a>':'')+'</td><td class="c">'+esc(r.city)+'</td><td class="c"><span class="cat">'+esc(r.category)+'</span></td><td class="p">'+(r.phone?'<a href="tel:'+esc(r.phone.replace(/[^+\d]/g,''))+'" style="color:inherit;text-decoration:none">'+hl(r.phone,tk)+'</a>':'—')+'</td><td class="a">'+hl(r.address||'—',tk)+'</td><td class="e">'+(r.email?'<a href="mailto:'+esc(r.email)+'">'+hl(r.email,tk)+'</a>':'—')+'</td><td class="w">'+(r.website?'<a href="'+esc(r.website)+'" target="_blank" rel="noopener">'+esc(r.website.replace(/^https?:\/\/(www\.)?/,'').replace(/\/$/,''))+'</a>':'—')+'</td></tr>').join('');
}
async function load(){const r=await api('/api/partners',{cache:'no-store'});const d=await r.json();if(!d.ok){$('msg').textContent=d.error||'Помилка';$('msg').className='msg bad';return}ROWS=d.rows;CATS=d.categories;CITIES=d.cities;$('at').textContent=d.at?'дані на '+d.at:'';chips();render();}
$('q').oninput=()=>{F.q=$('q').value;render();};$('em').onclick=()=>{F.email=!F.email;$('em').classList.toggle('on',F.email);render();};
const csvCell=v=>{v=String(v??'');return /[;"\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v};
$('csv').onclick=()=>{const rows=window.__rows||[];const blob=new Blob(['﻿'+['Назва;Місто;Категорія;Телефон;Адреса;Email;Сайт;Джерело;Примітка',...rows.map(r=>[r.name,r.city,r.category,r.phone,r.address,r.email,r.website,r.source,r.note].map(csvCell).join(';'))].join('\r\n')],{type:'text/csv;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='obiimy-partners.csv';a.click();};
$('copy').onclick=async()=>{const em=[...new Set((window.__rows||[]).map(r=>r.email).filter(Boolean))];try{await navigator.clipboard.writeText(em.join(', '));$('msg').textContent='Скопійовано адрес: '+em.length;$('msg').className='msg ok';}catch(e){$('msg').textContent='Не вдалося скопіювати';$('msg').className='msg bad';}};
load();
</script></body></html>"""
