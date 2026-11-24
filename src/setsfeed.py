#!/usr/bin/env python3
"""«Набори» — a page of the editor service with an XML feed of the gift sets (24.11.2026, the client: «отдельная страничка в том же
маркетинге, где можно будет скачать xml с текущими наборами — наявність, ціни, фото, артикули, описание, всё что у нас есть, и оно
должно самостоятельно обновляться раз в час»). The sets come live from the Horoshop catalogue (catalog/export, every field): the
products shown on the storefront whose own category or any extra section is «Подарунки» (SETS_SECTIONS overrides the list of
sections), gift certificates aside. Nothing is typed by hand — names, prices, discounts, availability, pictures, descriptions and
characteristics are what the site has at the moment of the refresh.

The feed is YML (`yml_catalog` → `shop` → `offers`), the format Ukrainian marketplaces and price aggregators read: one <offer> per
article, `available`, <price> (what the storefront charges) and <oldprice> (the full price when discounted), <picture> × N,
<vendorCode>, names and descriptions in three languages, <param> for every characteristic.

A daemon thread rebuilds the feed once an hour (SETS_REFRESH_SECONDS); a failed refresh keeps the last good feed and the page says
so. Mounted by src/deck-editor.py: GET /sets (the page), GET /api/sets (the rows for the preview, ?refresh=1 rebuilds now),
GET /sets.xml (the feed; ?download=1 saves it as a file) — all behind the manager's key or the advertisers' guest password."""
import html, json, os, pathlib, re, sys, threading, time
import xml.etree.ElementTree as ET
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src")); import horoshop as H

EVERY = int(os.environ.get("SETS_REFRESH_SECONDS") or 3600)
SECTIONS = [s.strip().lower() for s in (os.environ.get("SETS_SECTIONS") or "Подарунки").split("|") if s.strip()]   # category paths under «Каталог», as catalog/export names them
SITE = "https://obiimy.world/"
PARAM = {"sklad": "Склад і догляд", "druk": "Друк", "pakuvannja": "Пакування", "kranaVirobnik": "Країна-виробник", "Rozmir": "Розмір"}
_cache = {"at": 0, "tried": 0, "xml": b"", "rows": [], "error": "", "total": 0}
_lock = threading.Lock()

def configured():
    return all(os.environ.get(k) for k in ("HOROSHOP_LOGIN", "HOROSHOP_PASSWORD")) or H.ENV.exists()

def _paths(p):
    """The category paths of a product in Ukrainian: its own category first, then the extra sections."""
    out = [H.L(p.get("parent"), "ua")] + [H.L(a, "ua") for a in (p.get("alt_parent") or [])]
    return [s.strip() for s in out if isinstance(s, str) and s.strip()]

def is_set(p):
    if not p.get("article") or not int(p.get("display_in_showcase") or 0): return False              # hidden on the site → not a current set
    if str(p["article"]).lower().startswith("gift") or H.effective_uah(p) <= 0: return False           # gift certificates, service lines
    return any(s.lower() == sec or s.lower().startswith(sec + "/") for s in _paths(p) for sec in SECTIONS)

def _lang(v, lang):
    """One language of a multi-language value, no fallback to another language."""
    if isinstance(v, dict):
        if "value" in v and "id" in v: return _lang(v["value"], lang)
        v = v.get(lang)
    return v.strip() if isinstance(v, str) else ("" if v is None or isinstance(v, (dict, list)) else str(v))

def _text(s):
    """HTML → plain text for a <param>."""
    s = re.sub(r"(?i)<\s*(br|/p|/li|/div|/h\d)\s*/?>", "\n", s or ""); s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return re.sub(r"[ \t ]+", " ", re.sub(r"\s*\n\s*", "\n", s)).strip()

def _clean(s):
    """Characters XML 1.0 does not allow are dropped."""
    return re.sub(r"[^\x09\x0A\x0D\x20-퟿-�\U00010000-\U0010FFFF]", "", s or "")

def _params(p):
    out = []
    src = dict(p.get("characteristics") or {}) if isinstance(p.get("characteristics"), dict) else {}
    if p.get("Rozmir"): src.setdefault("Rozmir", p["Rozmir"])
    for k, v in src.items():
        vals = v if isinstance(v, list) else [v]
        t = "; ".join(x for x in (_text(_lang(i, "ua") or _lang(i, "ru") or _lang(i, "en")) for i in vals) if x)
        if t: out.append((PARAM.get(k, k), t))
    return out

def row(p):
    """A catalogue product → the flat record the feed and the preview are made of."""
    price, full = round(H.effective_uah(p), 2), round(H.full_uah(p), 2)
    pres_en = H.presence(p)
    return dict(article=str(p["article"]), group=str(p.get("parent_article") or ""), link=p.get("link") or "",
                name={l: (_lang(p.get("mod_title"), l) or _lang(p.get("title"), l)) for l in ("ua", "ru", "en")},
                description={l: _lang(p.get("description"), l) for l in ("ua", "ru", "en")},
                price=price, oldprice=full if full > price else 0, discount=float(p.get("discount") or 0), currency=str(p.get("currency") or "UAH"),
                available=pres_en == "In stock", presence=_lang(p.get("presence"), "ua") or pres_en,
                category=(_paths(p) or [""])[0], sections=_paths(p), pictures=H._images(p), params=_params(p))

def _when(t, f):
    """A moment in Kyiv time (the server on Railway runs in UTC); the server's own time when the zone database is missing."""
    try:
        import datetime, zoneinfo; return datetime.datetime.fromtimestamp(t, zoneinfo.ZoneInfo("Europe/Kyiv")).strftime(f)
    except Exception: return time.strftime(f, time.localtime(t))

def _num(x): return ("%.2f" % x).rstrip("0").rstrip(".")

def build_xml(rows, at):
    root = ET.Element("yml_catalog", date=_when(at, "%Y-%m-%d %H:%M"))
    shop = ET.SubElement(root, "shop")
    for tag, val in (("name", "OBIIMY"), ("company", "OBIIMY"), ("url", SITE)): ET.SubElement(shop, tag).text = val
    cur = ET.SubElement(shop, "currencies")
    for c in sorted({r["currency"] for r in rows} | {"UAH"}): ET.SubElement(cur, "currency", id=c, rate="1" if c == "UAH" else "CB")
    cats = {}; ce = ET.SubElement(shop, "categories")
    for r in rows:
        if r["category"] not in cats:
            cats[r["category"]] = str(len(cats) + 1); ET.SubElement(ce, "category", id=cats[r["category"]]).text = _clean(r["category"])
    offers = ET.SubElement(shop, "offers")
    for r in rows:
        attrs = dict(id=r["article"], available="true" if r["available"] else "false")
        if r["group"] and r["group"] != r["article"]: attrs["group_id"] = r["group"]
        o = ET.SubElement(offers, "offer", attrs)
        def add(tag, val, **kw):
            if val not in ("", None): ET.SubElement(o, tag, kw).text = _clean(str(val))
        add("url", r["link"]); add("price", _num(r["price"]))
        if r["oldprice"]: add("oldprice", _num(r["oldprice"]))
        add("currencyId", r["currency"]); add("categoryId", cats[r["category"]])
        for u in r["pictures"]: add("picture", u)
        add("vendor", "OBIIMY"); add("vendorCode", r["article"])
        add("name", r["name"]["ua"] or r["name"]["ru"] or r["name"]["en"]); add("name_ua", r["name"]["ua"]); add("name_ru", r["name"]["ru"]); add("name_en", r["name"]["en"])
        add("description", r["description"]["ua"] or r["description"]["ru"] or r["description"]["en"])
        add("description_ua", r["description"]["ua"]); add("description_ru", r["description"]["ru"]); add("description_en", r["description"]["en"])
        add("presence", r["presence"])
        if r["discount"]: add("discount", _num(r["discount"]), unit="%")
        for s in r["sections"][1:]: add("section", s)
        for k, v in r["params"]: add("param", v, name=_clean(k))
    ET.indent(root, space=" ")
    return b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="utf-8") + b"\n"

def refresh(products=None):
    """Rebuild the feed from the live catalogue (or from `products`, for tests). On failure the previous feed stays."""
    with _lock:
        _cache["tried"] = time.time()
        try:
            if products is None:
                if not configured(): raise RuntimeError("не задано HOROSHOP_LOGIN / HOROSHOP_PASSWORD")
                products = H.Horoshop().products()
            rows = sorted((row(p) for p in products if is_set(p)), key=lambda r: (r["group"] or r["article"], r["article"]))
            now = time.time()
            _cache.update(at=now, rows=rows, xml=build_xml(rows, now), error="", total=len(products))
        except BaseException as e:                                   # H.Horoshop() leaves with SystemExit when the credentials are missing
            if isinstance(e, KeyboardInterrupt): raise
            _cache["error"] = f"{type(e).__name__}: {e}"[:300]; sys.stderr.write(f"sets feed: {_cache['error']}\n")
    return _cache

def _fresh():
    if not _cache["at"] and time.time() - _cache["tried"] > 60: refresh()   # the first request after a start, or after a failed start
    return _cache

def state(force=False):
    """The rows for the preview on the page; `force` rebuilds the feed now (not more often than once a minute)."""
    if force and time.time() - _cache["tried"] > 60: refresh()
    c = _fresh(); fmt = lambda t: _when(t, "%d.%m.%Y %H:%M") if t else ""
    return dict(ok=bool(c["at"]), error=c["error"], at=fmt(c["at"]), next=fmt(max(c["at"], c["tried"]) + EVERY) if c["tried"] else "", every=EVERY,
                count=len(c["rows"]), available=sum(1 for r in c["rows"] if r["available"]), total=c["total"], bytes=len(c["xml"]),
                rows=[dict(article=r["article"], name=r["name"]["ua"] or r["name"]["ru"] or r["name"]["en"], price=r["price"], oldprice=r["oldprice"], currency=r["currency"],
                           available=r["available"], presence=r["presence"], link=r["link"], category=r["category"], pictures=len(r["pictures"]),
                           pic=(r["pictures"] or [""])[0], described=bool(r["description"]["ua"] or r["description"]["ru"] or r["description"]["en"])) for r in c["rows"]])

def xml():
    """The feed as bytes, or None while there is none (no credentials, or the first export failed)."""
    return _fresh()["xml"] or None

def start_scheduler():
    """One export now and then one every EVERY seconds, in a daemon thread; quiet when Horoshop is not configured (a local run)."""
    if not configured(): return
    def loop():
        while True:
            refresh(); time.sleep(EVERY)
    threading.Thread(target=loop, daemon=True).start()

PAGE = r"""<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Набори — XML</title>
<style>
:root{--ink:#141110;--muted:#6b645c;--line:#e6e0d6;--paper:#f7f3ec;--yel:#f4c430;--ok:#1f7a3a;--bad:#b3261e;--gold:#9a7430}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.45 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:1240px;margin:0 auto;padding:28px 20px 60px}h1{font-weight:500;font-size:26px;margin:0}.hd{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:10px}.hd .sp{flex:1}.hid{color:var(--muted);font-size:12.5px}
button.ghost,a.ghost{appearance:none;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink);font:inherit;padding:7px 14px;cursor:pointer;font-size:13.5px;text-decoration:none;display:inline-block}button.ghost:hover,a.ghost:hover{border-color:var(--ink)}
a.main{background:var(--ink);color:#fff;border-color:var(--ink)}a.main:hover{background:#000}button:disabled{opacity:.5;cursor:default}
.how{font-size:13.5px;color:var(--muted);margin:0 0 12px;max-width:70em}
.panel{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:0 0 12px}
.stats{display:flex;gap:26px;flex-wrap:wrap;margin-bottom:12px}.stats div{font-size:12.5px;color:var(--muted);letter-spacing:.04em;text-transform:uppercase}.stats b{display:block;font-size:22px;font-weight:500;color:var(--ink);letter-spacing:0;text-transform:none}
.url{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.url input{flex:1;min-width:240px;border:1px solid var(--line);border-radius:999px;padding:9px 14px;font:13.5px ui-monospace,Menlo,monospace;background:#fbf9f5;color:var(--ink)}
.search{position:relative;margin:0 0 12px}.search input{width:100%;border:1px solid var(--line);border-radius:999px;padding:10px 16px;font:inherit;background:#fff}.search input:focus,.url input:focus{outline:2px solid var(--yel);border-color:transparent}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:auto}table{width:100%;border-collapse:collapse}th,td{padding:8px 12px;border-top:1px solid var(--line);text-align:left;font-size:14px;vertical-align:middle}th{color:var(--muted);font-weight:500;font-size:12.5px;letter-spacing:.04em;text-transform:uppercase;border-top:0;background:#fbf9f5;white-space:nowrap}
td.i{width:64px}td.i img{width:52px;height:52px;object-fit:cover;border-radius:8px;display:block;background:#f1ece3}td.a{white-space:nowrap;font:13px ui-monospace,Menlo,monospace}td.n a{color:inherit;text-decoration:none}td.n a:hover{text-decoration:underline}td.p{white-space:nowrap}td.p s{color:var(--muted);margin-left:6px;font-size:13px}td.c{white-space:nowrap;color:var(--muted)}
.st{display:inline-block;border-radius:999px;padding:1px 9px;font-size:12.5px;white-space:nowrap}.st.y{background:#e6f3ea;color:var(--ok)}.st.n{background:#f6e7e5;color:var(--bad)}
.msg{font-size:13.5px;margin:8px 0 0;min-height:18px}.msg.ok{color:var(--ok)}.msg.bad{color:var(--bad)}
@media(max-width:700px){main{padding:16px 12px 40px}}
</style></head><body><main>
<div class="hd"><h1>Набори — XML</h1><span class="hid" id="at"></span><span class="sp"></span><button class="ghost" id="re">Оновити зараз</button><a class="ghost main" id="dl" href="/sets.xml?download=1">Завантажити XML</a></div>
<p class="how">Подарункові набори, які зараз показані на obiimy.world: артикул, назва, ціна і стара ціна, наявність, усі фото, опис і характеристики — просто з каталогу сайту. Файл оновлюється сам щогодини; формат — YML (yml_catalog), його читають маркетплейси й прайс-агрегатори.</p>
<section class="panel">
 <div class="stats"><div><b id="s1">—</b>наборів у файлі</div><div><b id="s2">—</b>в наявності</div><div><b id="s3">—</b>оновлено (за Києвом)</div><div><b id="s4">—</b>наступне оновлення</div></div>
 <div class="url"><input id="u" readonly aria-label="Постійне посилання на XML"><button class="ghost" id="cp">Скопіювати посилання</button><a class="ghost" id="op" href="/sets.xml" target="_blank" rel="noopener">Відкрити</a></div>
 <p class="msg" id="msg"></p>
</section>
<div class="search"><input type="search" id="q" placeholder="Пошук: назва або артикул" autocomplete="off"></div>
<div class="card"><table id="t"></table></div>
<script>
const KEY=new URLSearchParams(location.search).get('key')||'';const wk=u=>u+(KEY?(u.includes('?')?'&':'?')+'key='+encodeURIComponent(KEY):'');const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[<>&"]/g,m=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[m]));
const money=(v,c)=>Number(v).toLocaleString('uk-UA',{maximumFractionDigits:2})+' '+(c==='UAH'?'грн':esc(c));
const http=u=>/^https?:\/\//.test(u||'')?u:'';
let ROWS=[];
$('dl').href=wk('/sets.xml?download=1');$('op').href=wk('/sets.xml');$('u').value=location.origin+wk('/sets.xml');
function say(t,cls){$('msg').textContent=t||'';$('msg').className='msg '+(cls||'');}
function render(){const q=$('q').value.trim().toLowerCase();const rows=ROWS.filter(r=>!q||(r.name+' '+r.article).toLowerCase().includes(q));
 $('t').innerHTML='<tr><th></th><th>Артикул</th><th>Назва</th><th>Ціна</th><th>Наявність</th><th>Фото</th><th>Опис</th></tr>'+rows.map(r=>'<tr><td class="i">'+(http(r.pic)?'<img loading="lazy" alt="" src="'+esc(r.pic)+'">':'')+'</td><td class="a">'+esc(r.article)+'</td><td class="n">'+(http(r.link)?'<a href="'+esc(r.link)+'" target="_blank" rel="noopener">'+esc(r.name)+'</a>':esc(r.name))+'</td><td class="p">'+money(r.price,r.currency)+(r.oldprice?'<s>'+money(r.oldprice,r.currency)+'</s>':'')+'</td><td><span class="st '+(r.available?'y':'n')+'">'+esc(r.presence||(r.available?'В наявності':'Немає'))+'</span></td><td class="c">'+r.pictures+'</td><td class="c">'+(r.described?'є':'—')+'</td></tr>').join('');}
function show(d){ROWS=d.rows||[];$('s1').textContent=d.ok?d.count:'—';$('s2').textContent=d.ok?d.available:'—';$('s3').textContent=d.at||'—';$('s4').textContent=d.next||'—';
 $('at').textContent=d.ok?'із '+d.total+' товарів каталогу':'';
 if(!d.ok)say('Файл ще не зібрано: '+(d.error||'каталог не відповів')+'.','bad');else if(d.error)say('Останнє оновлення не вдалося ('+d.error+') — у файлі дані на '+d.at+'.','bad');else say('');render();}
async function load(force){$('re').disabled=true;try{const r=await fetch(wk('/api/sets'+(force?'?refresh=1':'')),{cache:'no-store'});show(await r.json());if(force&&!$('msg').textContent)say('Оновлено.','ok');}catch(e){say('Не вдалося завантажити дані.','bad');}$('re').disabled=false;}
$('q').oninput=render;$('re').onclick=()=>load(true);
$('cp').onclick=async()=>{try{await navigator.clipboard.writeText($('u').value);say('Посилання скопійовано.','ok');}catch(e){$('u').select();say('Скопіюйте посилання з поля.','bad');}};
load(false);
</script></body></html>"""
