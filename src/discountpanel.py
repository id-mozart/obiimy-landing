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

DRAFTS = ROOT / "data" / "horoshop" / "discount-drafts.json"   # named sets of changes (article, kind, value) to apply later (the client, 14.11.2026)

def drafts_list():
    try: return json.loads(DRAFTS.read_text(encoding="utf-8"))
    except Exception: return []

def _drafts_write(rows):
    DRAFTS.parent.mkdir(parents=True, exist_ok=True); DRAFTS.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

def draft_save(body):
    """{name, items, pages?: {page, page_title, add, remove}, id?} → a new draft, or the draft with that id (or the same name) overwritten.
    `pages` is the storefront section (добірка) the draft is for and which articles it puts on or takes off that page (the client, 15.11.2026:
    «важно, чтобы можно было сохранить черновик для конкретной добірки»)."""
    name = str(body.get("name") or "").strip()[:80]; items = [i for i in (body.get("items") or []) if i.get("article")]
    pg = body.get("pages") or {}
    try: page = int(pg.get("page") or 0)
    except (TypeError, ValueError): page = 0
    pages = dict(page=page, page_title=str(pg.get("page_title") or "")[:120], add=[str(a) for a in (pg.get("add") or [])], remove=[str(a) for a in (pg.get("remove") or [])]) if page else None
    if pages and not (pages["add"] or pages["remove"]): pages = None
    if not name: return dict(ok=False, error="Назвіть чернетку.")
    if not items and not pages: return dict(ok=False, error="Немає змін для збереження.")
    rows = drafts_list(); now = time.strftime("%Y-%m-%d %H:%M")
    clean = [dict(article=str(i["article"]), kind=(i.get("kind") or "none"), value=float(i.get("value") or 0)) for i in items]
    hit = next((d for d in rows if d["id"] == body.get("id")), None) or next((d for d in rows if d["name"].lower() == name.lower()), None)
    if hit: hit.update(name=name, items=clean, pages=pages, updated=now)
    else: rows.insert(0, dict(id=uuid.uuid4().hex[:8], name=name, items=clean, pages=pages, created=now, updated=now))
    _drafts_write(rows); return dict(ok=True, drafts=rows)

def draft_delete(body):
    rows = [d for d in drafts_list() if d["id"] != body.get("id")]; _drafts_write(rows); return dict(ok=True, drafts=rows)

def _state(p):
    st = {"price": float(p.get("price") or 0), "price_old": float(p.get("price_old") or 0), "discount": float(p.get("discount") or 0)}
    if "alt_parent" in p: st["alt_parent"] = _alt_ids(p)
    return st

def _alt_ids(p): return [int(a["id"]) for a in (p.get("alt_parent") or []) if isinstance(a, dict) and a.get("id")]
def _parent_id(p):
    a = p.get("parent"); return int(a["id"]) if isinstance(a, dict) and a.get("id") else None

CATALOG_ROOT = 97   # the «Каталог» section of obiimy.world; every storefront page («SALE», «Новинки», collections…) sits under it
def pages_list(h):
    """The catalogue sections from pages/export (id, path under «Каталог»): the pages a product can be added to. Horoshop has no API to
    create a section (pages/import → UNDEFINED_FUNCTION, 14.11.2026), so a new page such as «Чорна п’ятниця» is made once in the admin."""
    raw = h.call("pages/export", {}); pg = raw.get("pages", raw) if isinstance(raw, dict) else raw
    by = {int(x["id"]): x for x in pg}
    def path(i):
        out = []; cur = by.get(i)
        while cur and int(cur["id"]) != CATALOG_ROOT and cur.get("parent") is not None:
            out.append(H.L(cur.get("title"), "ua") or str(cur["id"])); cur = by.get(int(cur["parent"]))
        return " / ".join(reversed(out)) if cur and int(cur["id"]) == CATALOG_ROOT else None
    res = []
    for i, x in by.items():
        t = path(i)
        if t and i != CATALOG_ROOT: res.append(dict(id=i, title=t, image=x.get("image")))
    return sorted(res, key=lambda r: r["title"])

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

STOCK_WAREHOUSE = int(__import__("os").environ.get("STOCK_WAREHOUSE_ID") or 1)   # the warehouse the page opens with: KeyCRM «1 Склад Світлана» (the client, 14.11.2026); any other warehouse, or several, can be picked on the page (15.11.2026)
_stock_cache = {"at": 0, "map": {}, "warehouses": []}

def _crm_key(article, keys):
    """The site's article → the code the warehouse uses: 44-xx and 44-xx-D became P-44-xx there, a few spellings differ."""
    if article in keys: return article
    m = re.match(r"^44-(\d+)(-D)?$", article)
    if m and f"P-44-{m.group(1)}{m.group(2) or ''}" in keys: return f"P-44-{m.group(1)}{m.group(2) or ''}"
    alt = {"140-15-6": "140/15-6"}.get(article)
    return alt if alt in keys else None

def stock_map(force=False):
    """{sku in KeyCRM: {"w": {warehouse id: [quantity, reserve]}, "all": [quantity, reserve]}} from GET /offers/stocks?filter[details]=true
    (Bimp → KeyCRM every 15 min); the warehouses seen, with their names, land in _stock_cache["warehouses"]. Cached 10 minutes; an empty
    map when KeyCRM is not configured or fails — the page then shows no stock values."""
    import keycrm as K
    if not force and time.time() - _stock_cache["at"] < 600: return _stock_cache["map"]
    out, whs = {}, {}
    try:
        if K.KEY:
            page = 1
            while page <= 40:
                r = K.api("GET", "/offers/stocks", params={"limit": 50, "page": page, "filter[details]": "true"}); data = r.get("data") or []
                for x in data:
                    if not x.get("sku"): continue
                    w = {}
                    for it in x.get("warehouse") or []:
                        try: wid = int(it.get("id") or 0)
                        except (TypeError, ValueError): continue
                        if not wid: continue
                        whs.setdefault(wid, str(it.get("name") or wid).strip())
                        w[str(wid)] = [float(it.get("quantity") or 0), float(it.get("reserve") or 0)]
                    out[x["sku"]] = {"w": w, "all": [float(x.get("quantity") or 0), float(x.get("reserve") or 0)]}
                if len(data) < 50: break
                page += 1
        _stock_cache.update(at=time.time(), map=out, warehouses=[{"id": i, "name": n} for i, n in sorted(whs.items(), key=lambda kv: (kv[0] != STOCK_WAREHOUSE, kv[1].lower()))])
    except Exception as e:
        sys.stderr.write(f"keycrm stocks: {e}\n")
    return _stock_cache["map"] or out

def rows():
    """The catalogue as the page needs it: one row per article, the category path (the product type), the full price, the current discount,
    the price the storefront charges, the stock on every KeyCRM warehouse and the storefront sections the product sits in."""
    h = H.Horoshop(); prods = h.products(includedParams=FIELDS); rate = h.rates().get("USD") or 35.5
    st = stock_map(); out = []; pages = pages_list(h); cnt = {}; wcnt = {}
    for p in prods:
        if not p.get("article"): continue
        price = float(p.get("price") or 0); old = float(p.get("price_old") or 0); pct = float(p.get("discount") or 0)
        full = max(price, old); now = price * (1 - pct / 100)
        kind = "pct" if pct else ("amt" if old > price else "")
        k = _crm_key(p["article"], st); q = st.get(k) if k else None      # None → not in the warehouse system
        if q:
            for wid, qr in q["w"].items():
                if qr[0] > 0: wcnt[wid] = wcnt.get(wid, 0) + 1
        pid = _parent_id(p); pg_ids = sorted({*( [pid] if pid else [] ), *_alt_ids(p)})
        for i in pg_ids: cnt[i] = cnt.get(i, 0) + 1
        out.append(dict(pages=pg_ids, main_page=pid, stock=(q["w"] if q else None), stock_all=(q["all"] if q else None), crm_sku=k,
                        article=p["article"], parent=p.get("parent_article") or p["article"], name=(H.L(p.get("mod_title"), "ua") or H.L(p.get("title"), "ua")).strip(),
                        category=H.L(p.get("parent"), "ua") or "—", collections=[H.L(a, "ua") for a in p.get("alt_parent") or [] if H.L(a, "ua").startswith("Колекції/")],
                        full=full, now=round(now, 2), pct=pct, amt=round(full - now, 2), kind=kind, shown=int(p.get("display_in_showcase") or 0),
                        presence=H.presence(p), link=p.get("link") or "", thumb=thumb(p)[0], pic=thumb(p)[1]))
    out.sort(key=lambda r: (r["category"], r["parent"], r["article"]))
    bysku = {}
    for r in out:
        if r["crm_sku"]: bysku.setdefault(r["crm_sku"], []).append(r["article"])
    for r in out: r["same_sku"] = [a for a in bysku.get(r["crm_sku"] or "", []) if a != r["article"]]   # site articles that share one warehouse code (44-xx and P-44-xx): one physical stock, counted once in sums
    for pg in pages: pg["count"] = cnt.get(pg["id"], 0)
    whs = [dict(w, skus=wcnt.get(str(w["id"]), 0)) for w in _stock_cache["warehouses"]]
    return dict(ok=True, at=time.strftime("%Y-%m-%d %H:%M"), rate=rate, rows=out, pages=pages, warehouses=whs,
                stock_at=time.strftime("%H:%M", time.localtime(_stock_cache["at"])) if _stock_cache["at"] else None, warehouse=STOCK_WAREHOUSE)

def _import(h, prods, plan):
    res = h.call("catalog/import", {"products": prods}) if prods else {}
    log = {l.get("article"): l for l in (res.get("log") or [])}
    for pl in plan:
        l = log.get(pl["article"]); pl["result"] = "; ".join(m.get("message", "") for m in (l or {}).get("info", [])) if l else pl.get("error", "немає відповіді")

def apply(body, who=None):
    """body = {items: [{article, kind: 'pct'|'amt'|'none', value}], pages: {page, add: [articles], remove: [articles]}} → one catalog/import.
    A percentage clears any amount discount and vice versa; page membership is written as the whole `alt_parent` list of the product
    (the section ids it already has, plus or minus the chosen page). Every call is logged with the previous and the new values, so it
    can be rolled back from the page."""
    items = body.get("items") or []; pg = body.get("pages") or {}
    try: page = int(pg.get("page") or 0)
    except (TypeError, ValueError): page = 0
    add = [str(a) for a in (pg.get("add") or [])] if page else []; remove = [str(a) for a in (pg.get("remove") or [])] if page else []
    if not items and not add and not remove: return dict(ok=False, error="Немає змін.")
    h = H.Horoshop(); cur = {p["article"]: p for p in h.products(includedParams=["article", "price", "price_old", "discount", "mod_title", "title", "parent", "alt_parent"]) if p.get("article")}
    page_title = next((x["title"] for x in pages_list(h) if x["id"] == page), str(page)) if page else ""
    prods, plan = [], []
    for a in sorted(set(add) | set(remove)):
        p = cur.get(a)
        if not p: plan.append(dict(article=a, error="не знайдено")); continue
        ids = _alt_ids(p); op = "add" if a in add else "remove"
        if op == "remove" and _parent_id(p) == page: plan.append(dict(article=a, error=f"«{page_title}» — основна категорія товару, прибрати можна лише в адмінці")); continue
        new = sorted(set(ids) | {page}) if op == "add" else [i for i in ids if i != page]
        if new == ids: continue
        prods.append({"article": a, "alt_parent": [{"id": i} for i in new]})
        plan.append(dict(article=a, name=(H.L(p.get("mod_title"), "ua") or H.L(p.get("title"), "ua")).strip(), before={"alt_parent": ids}, after={"alt_parent": new, "page": page, "page_title": page_title, "op": op}))
    for it in items:
        a = str(it.get("article") or "").strip(); p = cur.get(a)
        if not p: plan.append(dict(article=a, error="не знайдено")); continue
        full = full_uah(p); kind = it.get("kind") or "none"
        try: v = float(it.get("value") or 0)
        except ValueError: v = 0
        nm = (H.L(p.get("mod_title"), "ua") or H.L(p.get("title"), "ua")).strip()
        if kind == "pct":
            if not 0 < v < 100: plan.append(dict(article=a, name=nm, error=f"знижка у відсотках має бути від 1 до 99, а не {it.get('value')}")); continue
            upd = {"article": a, "price": full, "price_old": 0, "discount": round(v, 2)}
        elif kind == "amt":
            if not 0 < v < full: plan.append(dict(article=a, name=nm, error=f"знижка в гривнях має бути меншою за повну ціну {full:.0f}, а не {it.get('value')}")); continue
            upd = {"article": a, "price": round(full - v, 2), "price_old": full, "discount": 0}
        else: upd = {"article": a, "price": full, "price_old": 0, "discount": 0}
        st = _state(p); st.pop("alt_parent", None)
        prods.append(upd); plan.append(dict(article=a, name=(H.L(p.get("mod_title"), "ua") or H.L(p.get("title"), "ua")).strip(), before=st, after={k: v for k, v in upd.items() if k != "article"}))
    merged = {}
    for u in prods: merged.setdefault(u["article"], {"article": u["article"]}).update(u)   # price and page changes of one article in one import row
    prods = list(merged.values())
    _import(h, prods, plan)
    entry = dict(id=uuid.uuid4().hex[:10], at=time.strftime("%Y-%m-%d %H:%M:%S"), kind="apply", who=who or {}, items=plan, applied=len(prods), page=page_title or None)
    _log_write(entry)
    return dict(ok=True, applied=len(prods), plan=plan, entry_id=entry["id"])

def rollback(body, who=None):
    """body = {id} → every article of that log entry gets its `before` values back (price, price_old, discount); logged as its own entry."""
    eid = str(body.get("id") or ""); entries = {e["id"]: e for e in log_entries(100000)}
    e = entries.get(eid)
    if not e: return dict(ok=False, error="Запис журналу не знайдено.")
    if e.get("rolled_back_by"): return dict(ok=False, error="Цей запис уже відкочено.")
    h = H.Horoshop(); cur = {p["article"]: p for p in h.products(includedParams=["article", "price", "price_old", "discount", "mod_title", "title", "parent", "alt_parent"]) if p.get("article")}
    prods, plan = [], []
    for it in e["items"]:
        a = it["article"]; b = it.get("before"); p = cur.get(a)
        if not b or not p: plan.append(dict(article=a, error="не знайдено")); continue
        upd = {"article": a}; before = {}
        if "price" in b: upd.update({"price": b["price"], "price_old": b["price_old"], "discount": b["discount"]}); before.update({k: v for k, v in _state(p).items() if k != "alt_parent"})
        if "alt_parent" in b: upd["alt_parent"] = [{"id": i} for i in b["alt_parent"]]; before["alt_parent"] = _alt_ids(p)
        after = {k: v for k, v in upd.items() if k != "article"}
        if "alt_parent" in after: after["alt_parent"] = b["alt_parent"]; after["page_title"] = (it.get("after") or {}).get("page_title", ""); after["op"] = "undo"
        prods.append(upd); plan.append(dict(article=a, name=it.get("name", ""), before=before, after=after))
    merged = {}
    for u in prods: merged.setdefault(u["article"], {"article": u["article"]}).update(u)
    prods = list(merged.values())
    _import(h, prods, plan)
    entry = dict(id=uuid.uuid4().hex[:10], at=time.strftime("%Y-%m-%d %H:%M:%S"), kind="rollback", rollback_of=eid, who=who or {}, items=plan, applied=len(prods))
    _log_write(entry)
    return dict(ok=True, applied=len(prods), plan=plan, entry_id=entry["id"])

PAGE = r"""<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Знижки</title>
<style>
:root{--ink:#141110;--muted:#6b645c;--line:#e6e0d6;--paper:#f7f3ec;--yel:#f4c430;--ok:#1f7a3a;--bad:#b3261e;--mark:#fff3c4}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.45 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:1160px;margin:0 auto;padding:28px 20px 120px}h1{font-weight:500;font-size:26px;margin:0}.sub{color:var(--muted);margin:0 0 14px;font-size:14px}
.hd{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:14px}.hd .sp{flex:1}.hd .hid{font-size:13px}
details{background:#fff;border:1px solid var(--line);border-radius:12px;margin:0 0 10px;overflow:hidden}summary{cursor:pointer;list-style:none;padding:12px 16px;display:flex;gap:12px;align-items:center;font-weight:500}summary::-webkit-details-marker{display:none}
summary::before{content:"▸";color:var(--muted);transition:transform .15s}details[open] summary::before{transform:rotate(90deg)}summary .n{color:var(--muted);font-weight:400;font-size:13px}summary .d{margin-left:auto;font-weight:400;font-size:13px;color:var(--ok)}
.how{font-size:14px;color:var(--muted)}.how summary{font-size:14px;font-weight:400;padding:10px 16px}.how p{margin:0 16px 12px 36px}
.panel{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin:0 0 12px;display:flex;flex-direction:column;gap:10px;z-index:5}@media(min-width:900px){.panel{position:sticky;top:58px;box-shadow:0 6px 18px rgba(0,0,0,.05)}}
.row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.row .sp{flex:1}
.search{flex:1;min-width:240px;position:relative}.search input{width:100%;border:1px solid var(--line);border-radius:999px;padding:10px 38px 10px 38px;font:inherit;font-size:15px;background:#fbf9f5}.search input:focus{outline:2px solid var(--yel);border-color:transparent;background:#fff}
.search .ico{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--muted);pointer-events:none}.search .x{position:absolute;right:8px;top:50%;transform:translateY(-50%);border:0;background:#eee8dd;border-radius:999px;width:24px;height:24px;cursor:pointer;color:var(--muted);line-height:1;font-size:15px}.search .x:hover{color:var(--bad)}
.search kbd{position:absolute;right:10px;top:50%;transform:translateY(-50%);font:12px/1 inherit;color:var(--muted);border:1px solid var(--line);border-radius:5px;padding:2px 6px;background:#fff;pointer-events:none}
.pop{position:relative;margin:0;border:0;background:none;border-radius:0;overflow:visible}.pop summary{padding:6px 11px;border:1px solid var(--line);border-radius:999px;background:#fff;font-weight:400;font-size:13.5px;color:var(--muted);gap:5px;white-space:nowrap}.pop summary::before{content:none}.pop summary b{color:var(--ink);font-weight:500;max-width:220px;overflow:hidden;text-overflow:ellipsis}.pop summary::after{content:"▾";font-size:11px;opacity:.7}
.pop[open] summary{border-color:var(--ink)}.pop.on summary{background:var(--ink);border-color:var(--ink);color:#e9e3d9}.pop.on summary b{color:#fff}
.pop.g summary{border-color:transparent;background:none;padding:4px 6px;font-size:13px}#gpops{gap:2px;margin-left:auto;flex:none}.pop.g[open] summary{border-color:var(--line)}
.menu{position:absolute;top:calc(100% + 6px);left:0;z-index:20;background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 12px 32px rgba(0,0,0,.12);padding:8px;min-width:300px;max-width:min(92vw,520px);max-height:420px;overflow:auto}.pop.w .menu{min-width:420px}.pop.r .menu{left:auto;right:0}
.mi{display:flex;gap:8px;align-items:center;padding:6px 8px;border-radius:8px;cursor:pointer;font-size:14px;color:var(--ink);white-space:normal}.mi:hover{background:var(--paper)}.mi input{width:16px;height:16px;accent-color:#141110;flex:none;margin:0}.mi span:first-of-type{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.ms{width:100%;border:1px solid var(--line);border-radius:8px;padding:7px 10px;font:inherit;font-size:14px;margin:0 0 6px;background:#fbf9f5}.ms:focus{outline:2px solid var(--yel);border-color:transparent}.mh{font-size:12px;color:var(--muted);padding:2px 8px 6px}.mi .n{flex:none;color:var(--muted);font-size:12px;white-space:nowrap;padding-left:10px}.menu hr{border:0;border-top:1px solid var(--line);margin:6px 0}.menu .mb{display:flex;gap:8px;align-items:center;padding:4px 8px 2px;font-size:13.5px;color:var(--muted);flex-wrap:wrap}.menu .mb input.v{width:64px}
.sum{color:var(--muted);font-size:13.5px}.sum b{color:var(--ink);font-weight:500}
@media(max-width:700px){.panel{padding:10px 12px;gap:8px;border-radius:12px}.hd{margin-bottom:10px}.pop summary{padding:5px 10px;font-size:13px}.pop summary b{max-width:120px}.menu{position:fixed;left:12px;right:12px;top:auto;min-width:0;max-width:none}
.bar{flex-wrap:wrap;gap:8px;padding:10px 12px}.bar .cnt{width:100%;text-align:center;font-size:13px}.bar button.go,.bar button.ghost{padding:9px 16px;font-size:14px}.bar .msg{width:100%;text-align:center}main{padding:18px 12px 150px}td.pic{display:none}}
mark{background:var(--mark);color:inherit;padding:0 1px;border-radius:2px}
input.v.err{outline:2px solid var(--bad);border-color:transparent}.np{color:var(--muted);font-size:12.5px;white-space:nowrap}.np b{color:var(--ok);font-weight:500}
td.stock{cursor:default;position:relative}td.stock .brk{display:none;position:absolute;right:6px;top:calc(100% - 4px);z-index:8;min-width:220px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:8px 12px;box-shadow:0 10px 28px rgba(0,0,0,.12);font-weight:400;font-size:12.5px;color:var(--ink);text-align:left;white-space:pre-line}td.stock.open .brk{display:block}details[data-g]:not(:hover) .gfill{opacity:.5}.gfill{transition:opacity .15s}.dup{color:var(--muted);font-size:11.5px}
dialog{border:0;border-radius:16px;padding:0;max-width:720px;width:calc(100vw - 32px);box-shadow:0 24px 64px rgba(0,0,0,.25)}dialog::backdrop{background:rgba(20,17,16,.45)}.dh{padding:18px 22px 6px;font-size:18px;font-weight:500}.db{padding:0 22px;max-height:60vh;overflow:auto;font-size:14px}.db table{margin:8px 0}.db td{padding:5px 8px;font-size:13.5px}.db .sec{font-weight:500;margin:12px 0 2px}.db td:nth-child(2){width:55%}.db td:not(:nth-child(2)){white-space:nowrap}dialog button:focus-visible{outline:2px solid var(--yel);outline-offset:2px}.da{display:flex;gap:10px;justify-content:flex-end;padding:14px 22px 18px;border-top:1px solid var(--line);margin-top:10px}
.pill{display:inline-flex;gap:6px;align-items:center;border-radius:999px;padding:5px 11px;font-size:13px;background:var(--yel);cursor:pointer;border:0;font:inherit}
.pop.mode.on summary{background:var(--yel);border-color:var(--yel);color:var(--ink)}.pop.mode.on summary b{color:var(--ink)}
@media(hover:none){#qk{display:none}}@media(max-width:700px){.pop.w .menu{min-width:0}.menu{max-height:60vh}details[data-g]{overflow:visible}details[data-g] table{display:block;overflow-x:auto;white-space:nowrap}.gfill{padding-left:16px}.gfill .clear{display:none}details[data-g] th:first-child,col.c-pic{display:none}td.name{white-space:normal;min-width:180px}td.stock .brk{right:auto;left:0}}
.empty{margin-bottom:10px}
.gfill{display:flex;gap:8px;align-items:center;padding:0 16px 10px 36px;font-size:13px;color:var(--muted);flex-wrap:wrap}.gfill input{width:70px}
table{width:100%;border-collapse:collapse}th,td{padding:7px 10px;border-top:1px solid var(--line);text-align:left;vertical-align:middle;font-size:14px}th{color:var(--muted);font-weight:500;font-size:12px;text-transform:uppercase;letter-spacing:.04em}
td.num,th.num{text-align:right;white-space:nowrap}td.art{color:var(--muted);font-size:12.5px;white-space:nowrap}td.pic{width:56px;padding:4px 6px}td.pic img{width:48px;height:48px;object-fit:cover;border-radius:8px;background:#f1ece3;display:block}td.pic span{display:block;width:48px;height:48px;border-radius:8px;background:#f1ece3}td.pgc{width:40px;text-align:center}td.pgc input{width:18px;height:18px;accent-color:#141110}td.name a{color:inherit;text-decoration:none}td.name a:hover{text-decoration:underline}td.name .cat{display:block;color:var(--muted);font-size:12px}
.cur{white-space:nowrap}td.stock{white-space:nowrap;font-weight:500}td.stock.zero{color:var(--bad)}.cur b{font-weight:500;color:var(--ok)}.cur s{color:var(--muted)}.hid{color:var(--muted);font-size:12px}
input.v{width:64px;border:1px solid var(--line);border-radius:8px;padding:6px 8px;font:inherit;text-align:right;background:#fff}input.v:focus{outline:2px solid var(--yel);border-color:transparent}
td.nd{white-space:nowrap}table{table-layout:fixed}col.c-pic{width:56px}col.c-pg{width:84px}col.c-art{width:96px}col.c-pr{width:100px}col.c-st{width:96px}col.c-cur{width:125px}col.c-nd{width:215px}col.c-x{width:56px}th{overflow:hidden;text-overflow:ellipsis}@media(max-width:700px){table{table-layout:auto}}tr.changed td{background:var(--mark)}select.k{border:1px solid var(--line);border-radius:999px;padding:6px 10px;font:inherit;font-size:13.5px;background:#fff;color:var(--ink);max-width:240px}td select.k{border-radius:8px;padding:6px}
.clear{border:0;background:none;color:var(--muted);cursor:pointer;font-size:13px;padding:4px 6px}.clear:hover{color:var(--bad)}
.bar{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:1px solid var(--line);padding:12px 20px;display:flex;gap:16px;align-items:center;justify-content:center;box-shadow:0 -6px 24px rgba(0,0,0,.06);z-index:6}
.bar .cnt{color:var(--muted);font-size:14px}button.go{appearance:none;border:0;border-radius:999px;background:var(--yel);color:var(--ink);font:inherit;font-weight:500;padding:12px 26px;cursor:pointer}button.go:disabled{background:#d9d3c8;color:#8a8378;cursor:default}
button.ghost{appearance:none;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink);font:inherit;padding:11px 18px;cursor:pointer}button.ghost.sm{padding:6px 12px;font-size:13px}
.msg{font-size:14px}.msg.ok{color:var(--ok)}.msg.bad{color:var(--bad)}#load{color:var(--muted);padding:6px 0 0}.sk{height:46px;background:#efe9df;border-radius:12px;margin:0 0 10px;animation:sk 1.2s ease-in-out infinite}@keyframes sk{50%{opacity:.55}}
#logbox,#draftbox{margin-top:28px}#logbox summary,#draftbox summary{font-weight:500}.bar .ghost:disabled{opacity:.5;cursor:default}.le{padding:10px 16px;border-top:1px solid var(--line);font-size:14px}.le.undone{opacity:.55}.le .h{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.le .h b{font-weight:500}.le .h .k{font-size:12px;border-radius:999px;padding:2px 8px;background:#f1ece3;color:var(--muted)}.le .h .k.rb{background:#fde7e4;color:var(--bad)}.le .h button{margin-left:auto}
.le ul{margin:6px 0 0;padding-left:18px;color:var(--muted);font-size:13px}.le li b{color:var(--ink);font-weight:500}
.empty{padding:28px;text-align:center;color:var(--muted);background:#fff;border:1px solid var(--line);border-radius:12px}
</style></head><body><main>
<div class="hd"><h1>Знижки</h1><span class="hid" id="at"></span><span class="sp"></span><button class="ghost sm" id="reload">Оновити з Хорошопу</button></div>
<section class="panel">
 <div class="row"><div class="search"><span class="ico">⌕</span><input type="search" id="q" placeholder="Пошук: назва, артикул, категорія, колекція…" autocomplete="off"><kbd id="qk">/</kbd><button class="x" id="qx" hidden title="очистити (Esc)">×</button></div></div>
 <div class="row" id="pops"></div>
 <div class="row"><span class="sum" id="sum"></span><button class="clear" id="reset" hidden>скинути фільтри</button><span class="sp"></span><span class="row" id="gpops"></span></div>
</section>
<div id="load"><div class="hid" style="margin:0 0 8px">Завантажую каталог із Хорошопу й залишки з KeyCRM…</div><div class="sk"></div><div class="sk"></div><div class="sk"></div><div class="sk"></div><div class="sk"></div></div>
<div id="groups"></div>
<details class="how"><summary>Як це працює</summary><p>Тут усі товари obiimy.world. Пошук шукає за назвою, артикулом, категорією й колекцією (кілька слів — усі мають збігтися). Фільтри: тип товару (категорія сайту), склад KeyCRM (один, кілька або всі разом; Bimp оновлює залишки кожні 15 хв), діапазон залишку, знижка, наявність на сайті, добірка. Знижка задається у відсотках (1–99) або в гривнях від повної ціни; поруч одразу видно нову ціну, перед записом — список змін. Записується в Хорошоп кнопкою «Застосувати»; у Shopify підтягується наступною <a href="/sync" id="lnk">синхронізацією</a>. Добірка — це сторінка-розділ Хорошопу (SALE, Новинки, Чорна п’ятниця…): галочка в рядку додає товар на сторінку, зняття — прибирає, записується тією ж кнопкою. Чернетка зберігає і знижки, і зміни добірки — можна підготувати Чорну п’ятницю заздалегідь і викласти одним «Застосувати». Нову сторінку створюють в адмінці Хорошопу (Каталог → Розділи → новий розділ під «Каталог»), API їх не створює; тут вона з’явиться після «Оновити з Хорошопу». Є також <a href="/portrait" id="lnk2">портрет клієнта</a> і <a href="/customers" id="lnk3">список клієнтів</a> для розсилок.</p></details>
<details id="draftbox"><summary>Чернетки знижок <span class="hid" id="draftn"></span></summary><div id="drafts"></div></details>
<details id="logbox"><summary>Журнал змін <span class="hid" id="logn"></span></summary><div id="log"></div></details>
</main>
<dialog id="dlg"><div class="dh" id="dlgh">Записати в Хорошоп</div><div class="db" id="dlgb"></div><div class="da"><button class="ghost" id="dlgx">Скасувати</button><button class="ghost" id="dlgalt" hidden></button><button class="go" id="dlgok">Записати</button></div></dialog>
<div class="bar"><button class="clear cnt" id="cnt" title="показати лише змінені рядки">Змін немає</button><button class="ghost" id="savedraft" disabled>Зберегти як чернетку</button><button class="go" id="apply" disabled>Застосувати</button><span class="msg" id="msg"></span></div>
<script>
const KEY=new URLSearchParams(location.search).get('key')||'';const api=(u,o={})=>fetch(u+(u.includes('?')?'&':'?')+'key='+encodeURIComponent(KEY),o);
const $=id=>document.getElementById(id);let ROWS=[],CH={},PG={},PAGES=[],WH=[],TYPES=[],DEFWH='1';
const LS='obiimy.discounts.filters';const F={q:'',grp:'cat',sort:'cat',wh:null,types:[],disc:'any',avail:'any',qmin:'',qmax:'',pmin:'',pmax:'',pg:'',onlyp:false};let ONLYC=false;
try{Object.assign(F,JSON.parse(localStorage.getItem(LS)||'{}'))}catch(e){}
function saveF(){try{localStorage.setItem(LS,JSON.stringify(F))}catch(e){}}
const PAGE=()=>parseInt(F.pg||'0')||0;const inPage=r=>{const p=PAGE();if(!p)return false;const cur=r.pages.includes(p);return PG[r.article]===undefined?cur:PG[r.article];};
function setPage(a,on){const r=ROWS.find(x=>x.article===a);if(!r)return;const p=PAGE();if(!p)return;if(r.pages.includes(p)===!!on)delete PG[a];else PG[a]=!!on;upd();}
const money=v=>Number(v).toLocaleString('uk-UA',{maximumFractionDigits:0})+' грн';const num=v=>Number(v).toLocaleString('uk-UA',{maximumFractionDigits:0});
const esc=s=>String(s).replace(/[<>&"]/g,m=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[m]));
const whName=id=>{const w=WH.find(w=>String(w.id)===String(id));return w?w.name:('склад '+id)};
const whIds=()=>F.wh==='all'?WH.map(w=>String(w.id)):(F.wh||[DEFWH]);
const ST=r=>{if(!r.stock)return null;if(F.wh==='all')return r.stock_all[0];let s=0;for(const id of whIds()){const x=r.stock[id];if(x)s+=x[0];}return s};
const RS=r=>{if(!r.stock)return 0;if(F.wh==='all')return r.stock_all[1];let s=0;for(const id of whIds()){const x=r.stock[id];if(x)s+=x[1];}return s};
const plural=(n,a,b,c)=>{const m=n%10,h=n%100;return n+' '+(m===1&&h!==11?a:(m>=2&&m<=4&&(h<12||h>14)?b:c))};
const saleIds=()=>WH.filter(w=>!/швея|реклама/i.test(w.name)).map(w=>String(w.id));
const whLabel=()=>F.wh==='all'?'усі склади':(F.wh!=='all'&&whIds().length>1&&whIds().join()===saleIds().join()?'склади продажу':(whIds().length===1?whName(whIds()[0]):(whIds().length<=2?whIds().map(whName).join(' + '):plural(whIds().length,'склад','склади','складів'))));
const GROUPS={
 none:r=>'Усі товари',
 cat:r=>r.category,
 col:r=>(r.collections&&r.collections.length)?r.collections[0].replace(/^Колекції\//,''):'Без колекції',
 stock:r=>{const q=ST(r);return q===null?'Немає в обліку':q<=0?'0 на складі':q<=5?'1–5 на складі':q<=20?'6–20 на складі':'понад 20 на складі'},
 disc:r=>!r.kind?'Без знижки':r.kind==='amt'?'Знижка в гривнях':r.pct>=40?'Знижка 40 % і більше':r.pct>=20?'Знижка 20–39 %':'Знижка до 20 %',
 price:r=>r.full<1000?'до 1 000 грн':r.full<2500?'1 000–2 499 грн':r.full<5000?'2 500–4 999 грн':'від 5 000 грн',
 avail:r=>!r.shown?'Приховані на сайті':r.presence==='In stock'?'В наявності':'Немає в наявності'};
const ORDER={stock:['понад 20 на складі','6–20 на складі','1–5 на складі','0 на складі','Немає в обліку'],disc:['Знижка 40 % і більше','Знижка 20–39 %','Знижка до 20 %','Знижка в гривнях','Без знижки'],price:['до 1 000 грн','1 000–2 499 грн','2 500–4 999 грн','від 5 000 грн'],avail:['В наявності','Немає в наявності','Приховані на сайті']};
const toks=q=>q.trim().toLowerCase().replace(/[<>&"]/g,' ').split(/\s+/).filter(Boolean);
const hl=(s,tk)=>{let h=esc(s);if(!tk.length)return h;const re=new RegExp('('+tk.map(t=>esc(t).replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')','gi');return h.replace(re,'<mark>$1</mark>')};
const sub=(r,tk)=>[F.grp!=='cat'?hl(r.category,tk):'',...(r.collections||[]).map(c=>hl(c.replace(/^Колекції\//,''),tk))].filter(Boolean).join(' · ');
const dv=r=>r.kind==='pct'?r.pct:(r.kind==='amt'&&r.full?r.amt/r.full*100:0);
const SORTS={cat:(a,b)=>a.i-b.i,name:(a,b)=>a.name.localeCompare(b.name,'uk')||a.i-b.i,pricedn:(a,b)=>b.full-a.full||a.i-b.i,priceup:(a,b)=>a.full-b.full||a.i-b.i,
 stockdn:(a,b)=>((ST(b)===null?-1:ST(b))-(ST(a)===null?-1:ST(a)))||a.i-b.i,stockup:(a,b)=>((ST(a)===null?1e9:ST(a))-(ST(b)===null?1e9:ST(b)))||a.i-b.i,discdn:(a,b)=>dv(b)-dv(a)||a.i-b.i};
const filtersOn=()=>!!(toks(F.q).length||F.types.length||F.disc!=='any'||F.avail!=='any'||F.qmin!==''||F.qmax!==''||F.pmin!==''||F.pmax!==''||(F.onlyp&&PAGE())||ONLYC||F.wh==='all'||whIds().join()!==DEFWH);
const once=r=>!r.same_sku||!r.same_sku.length||r.same_sku.every(a=>a>r.article);   // one physical stock behind 44-xx and P-44-xx: count it on the first article only
const newPrice=(r,kind,v)=>kind==='pct'?r.full*(1-v/100):kind==='amt'?r.full-v:r.full;
const invalid=(r,kind,v)=>kind==='pct'?!(v>0&&v<100):kind==='amt'?!(v>0&&v<r.full):false;
const POPS=[
 {id:'typ',l:'Тип',text:()=>!F.types.length?'усі':F.types.length<=2?F.types.join(', '):plural(F.types.length,'тип','типи','типів'),on:()=>!!F.types.length,
  menu:()=>'<input class="ms" placeholder="знайти тип…"><div class="mb"><button class="clear" data-act="tall">усі типи</button></div><hr>'+TYPES.map(x=>'<label class="mi"><input type="checkbox" data-ty="'+esc(x.name)+'"'+(F.types.includes(x.name)?' checked':'')+'> <span>'+esc(x.name)+'</span><span class="n">'+x.count+' арт.</span></label>').join('')},
 {id:'wh',l:'Склад',text:whLabel,on:()=>F.wh==='all'||whIds().join()!==DEFWH,
  menu:()=>{const all=F.wh==='all',ids=new Set(all?[]:whIds());return '<input class="ms" placeholder="знайти склад…"><label class="mi"><input type="checkbox" data-whall="1"'+(all?' checked':'')+'> <span>усі склади разом</span><span class="n">сума по всіх</span></label><div class="mb"><button class="clear" data-act="whsale">лише склади продажу</button><button class="clear" data-act="whdef">лише '+esc(whName(DEFWH))+'</button></div><hr><div class="mh">склад KeyCRM · артикулів у наявності</div>'+WH.map(w=>'<label class="mi"><input type="checkbox" data-wh="'+w.id+'"'+(ids.has(String(w.id))?' checked':'')+(all?' disabled':'')+'> <span>'+esc(w.name)+'</span><span class="n">'+w.skus+'</span></label>').join('')+(WH.length?'':'<div class="mb">Склади KeyCRM недоступні</div>')}},
 {id:'stock',l:'Залишок',text:()=>F.qmin===''&&F.qmax===''?'будь-який':(F.qmin!==''&&F.qmax!==''?F.qmin+'–'+F.qmax:F.qmin!==''?'від '+F.qmin:'до '+F.qmax)+' шт.',on:()=>F.qmin!==''||F.qmax!=='',
  menu:()=>{const P=[['','','будь-який'],['0','0','0 — немає'],['1','5','1–5'],['6','20','6–20'],['21','','понад 20']];return P.map(([a,b,l])=>'<label class="mi"><input type="radio" name="rst" data-rng="'+a+'|'+b+'"'+(F.qmin===a&&F.qmax===b?' checked':'')+'> <span>'+l+'</span></label>').join('')+'<hr><div class="mb">від <input class="v" data-r="qmin" value="'+esc(F.qmin)+'" placeholder="0" inputmode="numeric"> до <input class="v" data-r="qmax" value="'+esc(F.qmax)+'" placeholder="∞" inputmode="numeric"> шт. на вибраних складах</div>'}},
 {id:'price',l:'Ціна',text:()=>F.pmin===''&&F.pmax===''?'будь-яка':(F.pmin!==''&&F.pmax!==''?F.pmin+'–'+F.pmax:F.pmin!==''?'від '+F.pmin:'до '+F.pmax)+' грн',on:()=>F.pmin!==''||F.pmax!=='',
  menu:()=>{const P=[['','','будь-яка'],['','999','до 1 000 грн'],['1000','2499','1 000–2 499'],['2500','4999','2 500–4 999'],['5000','','від 5 000']];return P.map(([a,b,l])=>'<label class="mi"><input type="radio" name="rpr" data-prng="'+a+'|'+b+'"'+(F.pmin===a&&F.pmax===b?' checked':'')+'> <span>'+l+'</span></label>').join('')+'<hr><div class="mb">від <input class="v" data-r="pmin" value="'+esc(F.pmin)+'" placeholder="0" inputmode="numeric"> до <input class="v" data-r="pmax" value="'+esc(F.pmax)+'" placeholder="∞" inputmode="numeric"> грн повної ціни</div>'}},
 {id:'disc',l:'Знижка',opts:[['any','усі'],['yes','зі знижкою'],['no','без знижки'],['pct','у відсотках'],['amt','у гривнях']],def:'any'},
 {id:'avail',l:'На сайті',opts:[['any','усі'],['in','в наявності'],['out','немає в наявності'],['hidden','приховані'],['ghost','в наявності на сайті, але 0 на вибраних складах']],def:'any'},
 {id:'pg',l:'Добірка',text:()=>PAGE()?((PAGES.find(p=>p.id===PAGE())||{}).title||'')+(F.onlyp?' · лише з неї':''):'немає',on:()=>!!PAGE(),mode:1,
  menu:()=>'<label class="mi"><input type="radio" name="rpg" data-pg=""'+(!PAGE()?' checked':'')+'> <span>— без добірки</span></label>'+(PAGE()?'<label class="mi"><input type="checkbox" data-onlyp="1"'+(F.onlyp?' checked':'')+'> <span>показувати лише товари добірки</span></label>':'')+'<hr>'+PAGES.map(p=>'<label class="mi"><input type="radio" name="rpg" data-pg="'+p.id+'"'+(p.id===PAGE()?' checked':'')+'> <span>'+esc(p.title)+'</span><span class="n">'+p.count+' арт.</span></label>').join('')+'<div class="mb">Добірка — сторінка-розділ сайту (SALE, Чорна п’ятниця…). Галочка в рядку додає товар на неї.</div>'},
 {id:'grp',l:'Групувати',g:1,opts:[['cat','за типом товару'],['col','за колекцією'],['stock','за залишком'],['disc','за знижкою'],['price','за ціною'],['avail','за наявністю на сайті'],['none','без груп']],def:'cat'},
 {id:'sort',l:'Сортувати',g:1,opts:[['cat','як у каталозі'],['name','за назвою'],['pricedn','ціна ↓'],['priceup','ціна ↑'],['stockdn','залишок ↓'],['stockup','залишок ↑'],['discdn','знижка ↓']],def:'cat'}];
for(const p of POPS)if(p.opts){p.text=()=>(p.opts.find(o=>o[0]===F[p.id])||p.opts[0])[1];p.on=()=>!p.g&&F[p.id]!==p.def;p.menu=()=>p.opts.map(([v,l])=>'<label class="mi"><input type="radio" name="r'+p.id+'" data-opt="'+p.id+'" value="'+v+'"'+(F[p.id]===v?' checked':'')+'> <span>'+esc(l)+'</span></label>').join('');}
const pill=p=>'<details class="pop'+(p.g?' g r':'')+(p.mode?' mode':'')+(p.id==='typ'||p.id==='wh'||p.id==='pg'?' w':'')+'" data-pop="'+p.id+'"><summary>'+(p.g?'':p.l+': ')+'<b></b></summary><div class="menu"></div></details>';
$('pops').innerHTML=POPS.filter(p=>!p.g).map(pill).join('');$('gpops').innerHTML=POPS.filter(p=>p.g).map(pill).join('');
function bind(){$('q').value=F.q;$('qx').hidden=!F.q;$('qk').hidden=!!F.q;menus();}
function menus(){for(const p of POPS){const d=document.querySelector('[data-pop="'+p.id+'"]');d.querySelector('b').textContent=(p.g?p.l+': ':'')+p.text();d.classList.toggle('on',!!p.on());d.querySelector('.menu').innerHTML=p.menu();}}
function set(k,v){F[k]=v;saveF();menus();render();}
async function load(keepMsg){ $('load').hidden=false;$('groups').innerHTML='';CH={};upd(keepMsg);
 const r=await api('/api/discounts',{cache:'no-store'});const d=await r.json();$('load').hidden=true;
 if(!d.ok){$('groups').innerHTML='<div class="empty"><span class="msg bad">'+esc(d.error||'Помилка')+'</span> <button class="ghost sm" onclick="load()">Спробувати ще раз</button></div>';return}
 ROWS=d.rows;ROWS.forEach((r,i)=>{r.i=i;r.hay=[r.name,r.article,r.parent,r.category,...(r.collections||[]),r.crm_sku||''].join(' ').toLowerCase();});
 PAGES=d.pages||[];WH=d.warehouses||[];DEFWH=String(d.warehouse||1);
 if(F.wh!=='all'){const ok=new Set(WH.map(w=>String(w.id)));F.wh=(F.wh||[DEFWH]).map(String).filter(x=>ok.has(x));if(!F.wh.length)F.wh=[DEFWH];}
 const tc={};for(const r of ROWS)tc[r.category]=(tc[r.category]||0)+1;TYPES=Object.keys(tc).sort((a,b)=>a.localeCompare(b,'uk')).map(n=>({name:n,count:tc[n]}));F.types=F.types.filter(t=>tc[t]);
 if(!PAGES.find(p=>String(p.id)===String(F.pg)))F.pg='';PG={};
 $('at').textContent='каталог на '+d.at+(d.stock_at?' · залишки KeyCRM на '+d.stock_at:' · залишки недоступні');$('at').title='курс USD '+d.rate;bind();menus();saveF();render();}
function render(){
 const tk=toks(F.q),qmin=F.qmin===''?null:parseFloat(F.qmin),qmax=F.qmax===''?null:parseFloat(F.qmax),pmin=F.pmin===''?null:parseFloat(F.pmin),pmax=F.pmax===''?null:parseFloat(F.pmax),op=F.onlyp&&PAGE(),types=new Set(F.types);const groups={};let shown=0,nd=0,stq=0,anyst=false;
 for(const r of ROWS){ if(ONLYC){if(!CH[r.article]&&PG[r.article]===undefined)continue;}else{ if(tk.length&&!tk.every(t=>r.hay.includes(t)))continue; if(types.size&&!types.has(r.category))continue;
  if(F.disc==='yes'&&!r.kind&&!CH[r.article])continue; if(F.disc==='no'&&(r.kind||CH[r.article]))continue; if(F.disc==='pct'&&r.kind!=='pct')continue; if(F.disc==='amt'&&r.kind!=='amt')continue;
  if(F.avail==='in'&&!(r.shown&&r.presence==='In stock'))continue; if(F.avail==='out'&&!(r.shown&&r.presence!=='In stock'))continue; if(F.avail==='hidden'&&r.shown)continue; if(F.avail==='ghost'&&!(r.shown&&r.presence==='In stock'&&r.stock&&ST(r)<=0))continue;
  if(pmin!==null&&r.full<pmin)continue; if(pmax!==null&&r.full>pmax)continue;
  if(qmin!==null||qmax!==null){const st=ST(r)===null?0:ST(r); if(qmin!==null&&st<qmin)continue; if(qmax!==null&&st>qmax)continue;}
  if(op&&!inPage(r)&&PG[r.article]===undefined)continue;}
  const gk=GROUPS[F.grp](r);(groups[gk]=groups[gk]||[]).push(r);shown++;if(r.kind)nd++;if(ST(r)!==null){anyst=true;if(once(r))stq+=ST(r);}}
 const open=new Set([...document.querySelectorAll('details[data-g][open]')].map(d=>d.dataset.g));const act=filtersOn();
 const ord=ORDER[F.grp];const keys=Object.keys(groups).sort((a,b)=>ord?(ord.indexOf(a)-ord.indexOf(b)):a.localeCompare(b,'uk'));const cmp=SORTS[F.sort]||SORTS.cat;
  $('sum').innerHTML=ROWS.length?('Показано <b>'+shown+'</b> із '+ROWS.length+' арт.'+(F.grp!=='none'?' · груп: '+keys.length:'')+' · зі знижкою: <b>'+nd+'</b>'+(anyst?' · на складі ('+esc(whLabel())+'): <b>'+num(stq)+'</b> шт.':'')+(ONLYC?' <button class="pill" id="onlyc">лише змінені ×</button>':'')+(nd?' <button class="clear" id="clrall">зняти всі показані знижки</button>':'')):'';$('reset').hidden=!act;
 const wtitle=esc(whLabel());
 $('groups').innerHTML=keys.map(g=>{const rs=groups[g].slice().sort(cmp);const gd=rs.filter(r=>r.kind).length;const gst=rs.some(r=>ST(r)!==null);
  const stg=rs.reduce((a,r)=>a+(once(r)?(ST(r)||0):0),0);const ndup=rs.filter(r=>!once(r)).length;return '<details data-g="'+esc(g)+'"'+(open.has(g)||act||keys.length===1?' open':'')+'><summary>'+esc(g)+' <span class="n">'+rs.length+' арт.'+(gst?' · на складі '+num(stg)+' шт.'+(ndup?' <span title="парні артикули (44-xx і P-44-xx) мають один склад і пораховані в іншій групі">без '+plural(ndup,'дубля','дублів','дублів')+'</span>':''):'')+'</span>'+(gd?'<span class="d">зі знижкою: '+gd+'</span>':'')+'</summary>'
  +'<div class="gfill">усій групі: <select class="k" data-gk="'+esc(g)+'"><option value="pct">%</option><option value="amt">грн</option></select><input class="v" data-gv="'+esc(g)+'" placeholder="0"><button class="ghost sm" data-gset="'+esc(g)+'">застосувати до групи</button><button class="clear" data-gclr="'+esc(g)+'">зняти всі знижки групи</button>'+(PAGE()?' · <button class="ghost sm" data-gpa="'+esc(g)+'">усі в добірку</button><button class="clear" data-gpr="'+esc(g)+'">прибрати всі з добірки</button>':'')+'</div>'
  +'<table><colgroup><col class="c-pic">'+(PAGE()?'<col class="c-pg">':'')+'<col class="c-art"><col><col class="c-pr"><col class="c-st"><col class="c-cur"><col class="c-nd"><col class="c-x"></colgroup><tr><th></th>'+(PAGE()?'<th title="'+esc((PAGES.find(p=>p.id===PAGE())||{}).title||'')+'">Добірка</th>':'')+'<th>Артикул</th><th>Товар</th><th class="num">Повна ціна</th><th class="num" title="За даними KeyCRM: '+wtitle+'">Залишок</th><th class="num">Ціна зараз</th><th>Знижка</th><th></th></tr>'
  +rs.map(r=>{const c=CH[r.article];const kind=c?c.kind:(r.kind||'pct');const val=c?c.value:(r.kind==='pct'?r.pct:(r.kind==='amt'?r.amt:''));const st=ST(r),rsv=RS(r);
   const pgc=PAGE()?('<td class="pgc">'+(r.main_page===PAGE()?'<input type="checkbox" checked disabled title="основна категорія товару">':'<input type="checkbox" data-p="'+esc(r.article)+'"'+(inPage(r)?' checked':'')+'>')+'</td>'):'';
   const br=r.stock?Object.entries(r.stock).filter(([id,x])=>x[0]||x[1]).map(([id,x])=>whName(id)+': '+num(x[0])+(x[1]?' (рез. '+num(x[1])+')':'')).join('\n'):'';const dup=r.same_sku&&r.same_sku.length?'<div class="dup">той самий склад, що '+esc(r.same_sku.join(', '))+'</div>':'';const bad=c&&c.kind!=='none'&&invalid(r,c.kind,c.value);const np=c?(c.kind==='none'?'→ без знижки, '+money(r.full):(bad?'<span style="color:var(--bad)">'+(c.kind==='pct'?'від 1 до 99 %':'менше за '+money(r.full))+'</span>':'→ <b>'+money(newPrice(r,c.kind,c.value))+'</b>')):'';
   return '<tr data-a="'+esc(r.article)+'"'+(c||PG[r.article]!==undefined?' class="changed"':'')+'><td class="pic">'+(r.thumb?'<img data-src="'+esc(r.thumb)+'" data-f="'+esc(r.pic)+'" alt="" onerror="if(!this.dataset.o){this.dataset.o=1;this.src=this.dataset.f}">':'<span></span>')+'</td>'+pgc+'<td class="art">'+hl(r.article,tk)+(r.shown?'':' <span class="hid">прихований</span>')+'</td><td class="name">'+(r.link?'<a href="'+esc(r.link)+'" target="_blank" rel="noopener">'+hl(r.name,tk)+'</a>':hl(r.name,tk))+(r.presence!=='In stock'?' <span class="hid">немає в наявності</span>':'')+(sub(r,tk)?'<span class="cat">'+sub(r,tk)+'</span>':'')+'</td>'
   +'<td class="num">'+money(r.full)+'</td><td class="num stock'+(st===null?' hid':(st<=0?' zero':''))+'" title="'+esc(br||(st===null?'немає в обліку KeyCRM':'0 на всіх складах'))+'">'+(st===null?'—':(num(st)+(rsv?' <span class="hid">(рез. '+num(rsv)+')</span>':'')))+(br?'<div class="brk">'+esc(br)+'</div>':'')+dup+'</td><td class="num cur">'+(r.kind?'<b>'+money(r.now)+'</b> <s>'+money(r.full)+'</s> <span class="hid">'+(r.kind==='pct'?'−'+r.pct+'%':'−'+money(r.amt))+'</span>':'—')+'</td>'
   +'<td class="nd"><input class="v'+(bad?' err':'')+'" data-v="'+esc(r.article)+'" value="'+esc(val)+'" placeholder="0"> <select class="k" data-k="'+esc(r.article)+'"><option value="pct"'+(kind==='pct'?' selected':'')+'>%</option><option value="amt"'+(kind==='amt'?' selected':'')+'>грн</option></select> <span class="np" data-np="'+esc(r.article)+'">'+np+'</span></td>'
   +'<td>'+(r.kind||c?'<button class="clear" data-clr="'+esc(r.article)+'" title="зняти знижку">зняти</button>':'')+'</td></tr>'}).join('')+'</table></details>'}).join('')||(ROWS.length?'<div class="empty">Нічого не знайдено'+(tk.length?' за «'+esc(F.q)+'»':'')+'. <button class="clear" id="reset2">Скинути фільтри</button></div>':'');
 document.querySelectorAll('details[data-g][open]').forEach(showPics);
}
function setChange(a,kind,value){const r=ROWS.find(x=>x.article===a);if(!r)return;const v=parseFloat(String(value).replace(',','.'))||0;
 const same=(v===0&&!r.kind)||(kind==='pct'&&r.kind==='pct'&&v===r.pct)||(kind==='amt'&&r.kind==='amt'&&v===r.amt);
 if(same)delete CH[a];else CH[a]={kind:v?kind:'none',value:v};upd();}
let DRAFT=null;
const nbad=()=>Object.entries(CH).filter(([a,c])=>{const r=ROWS.find(x=>x.article===a);return r&&c.kind!=='none'&&invalid(r,c.kind,c.value)}).length;
function upd(keep){const n=Object.keys(CH).length,pa=Object.values(PG).filter(v=>v).length,pr=Object.values(PG).filter(v=>!v).length,nb=nbad();$('cnt').textContent=(n?'Змін знижок: '+n:'Змін немає')+(pa||pr?' · добірка: +'+pa+' / −'+pr:'')+(nb?' · помилкових значень: '+nb:'')+(DRAFT?' · чернетка «'+DRAFT.name+'»':'');$('cnt').style.color=nb?'var(--bad)':'';$('apply').disabled=!(n||pa||pr)||nb>0;$('savedraft').disabled=!(n||pa||pr)||nb>0;if(!keep)$('msg').textContent='';}
const fmtItem=i=>i.kind==='pct'?('−'+i.value+'%'):i.kind==='amt'?('−'+money(i.value)):'зняти';
async function loadDrafts(list){const d=list||(await (await api('/api/discounts/drafts',{cache:'no-store'})).json()).drafts||[];$('draftn').textContent=d.length?('· '+d.length):'';
 $('drafts').innerHTML=d.map(x=>'<div class="le"><div class="h"><b>'+esc(x.name)+'</b><span class="hid">'+(x.items.length?x.items.length+' арт. зі знижкою':'без змін знижок')+(x.pages?' · добірка «'+esc(x.pages.page_title||x.pages.page)+'»: +'+x.pages.add.length+' / −'+x.pages.remove.length:'')+' · '+esc(x.updated)+'</span><span style="margin-left:auto;display:flex;gap:6px"><button class="ghost sm" data-dl="'+esc(x.id)+'">Завантажити</button><button class="go" style="padding:6px 14px;font-size:13px" data-da="'+esc(x.id)+'">Застосувати…</button><button class="clear" data-dd="'+esc(x.id)+'">видалити</button></span></div><ul>'+x.items.slice(0,30).map(i=>{const r=ROWS.find(r=>r.article===i.article);return '<li><b>'+esc(i.article)+'</b> '+esc(r?r.name:'(немає в каталозі)')+': '+esc(fmtItem(i))+'</li>'}).join('')+(x.items.length>30?'<li>… ще '+(x.items.length-30)+'</li>':'')+(x.pages&&x.pages.add.length?'<li>на сторінку «'+esc(x.pages.page_title)+'»: '+esc(x.pages.add.slice(0,25).join(', '))+(x.pages.add.length>25?' … ще '+(x.pages.add.length-25):'')+'</li>':'')+(x.pages&&x.pages.remove.length?'<li>зі сторінки «'+esc(x.pages.page_title)+'»: '+esc(x.pages.remove.slice(0,25).join(', '))+(x.pages.remove.length>25?' … ще '+(x.pages.remove.length-25):'')+'</li>':'')+'</ul></div>').join('')||'<div class="le hid">Чернеток ще немає. Внесіть зміни й натисніть «Зберегти як чернетку».</div>';
 window.__drafts=d;}
function loadDraft(x){CH={};PG={};let miss=0,done=0,nopage=false;for(const i of x.items){if(!ROWS.find(r=>r.article===i.article)){miss++;continue;}CH[i.article]={kind:i.kind,value:i.value};}
 if(x.pages&&x.pages.page){const pg=PAGES.find(p=>p.id===x.pages.page);if(!pg)nopage=true;else{F.pg=String(pg.id);for(const a of x.pages.add){const r=ROWS.find(r=>r.article===a);if(!r){miss++;continue;}if(r.pages.includes(pg.id))done++;else PG[a]=true;}for(const a of x.pages.remove){const r=ROWS.find(r=>r.article===a);if(!r){miss++;continue;}if(!r.pages.includes(pg.id))done++;else if(r.main_page!==pg.id)PG[a]=false;}}}
 DRAFT={id:x.id,name:x.name};saveF();menus();upd();render();const np=Object.keys(PG).length;$('msg').textContent='Завантажено чернетку «'+x.name+'»: '+Object.keys(CH).length+' змін знижок'+(x.pages?', добірка «'+esc(x.pages.page_title)+'»: '+np+' змін'+(done?' ('+done+' уже на місці)':''):'')+(miss?', '+miss+' артикулів немає в каталозі':'')+(nopage?'. Сторінки «'+esc(x.pages.page_title)+'» більше немає на сайті — зміни добірки пропущено':'')+'. Перевірте й натисніть «Застосувати».';$('msg').className='msg'+(nopage?' bad':'');}
$('savedraft').onclick=async()=>{const pt=(PAGES.find(p=>p.id===PAGE())||{}).title||'';const name=prompt('Назва чернетки',DRAFT?DRAFT.name:(pt&&Object.keys(PG).length?pt:''));if(!name)return;const items=Object.entries(CH).map(([article,c])=>({article,kind:c.kind,value:c.value}));
 const pages=PAGE()&&Object.keys(PG).length?{page:PAGE(),page_title:pt,add:Object.entries(PG).filter(([a,v])=>v).map(([a])=>a),remove:Object.entries(PG).filter(([a,v])=>!v).map(([a])=>a)}:null;
 const r=await api('/api/discounts/drafts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:DRAFT&&DRAFT.name===name?DRAFT.id:null,name,items,pages})});const d=await r.json();
 if(!d.ok){$('msg').textContent=d.error||'Помилка';$('msg').className='msg bad';return}DRAFT={id:(d.drafts.find(x=>x.name===name)||{}).id,name};upd(true);$('msg').textContent='Чернетку «'+name+'» збережено: '+items.length+' змін знижок'+(pages?', добірка «'+pt+'»: +'+pages.add.length+' / −'+pages.remove.length:'')+'.';$('msg').className='msg ok';$('draftbox').open=true;loadDrafts(d.drafts);};
document.addEventListener('click',async e=>{const t=e.target;const list=window.__drafts||[];
 if(t.dataset.dl!==undefined){const x=list.find(d=>d.id===t.dataset.dl);if(x)loadDraft(x);window.scrollTo({top:0,behavior:'smooth'});}
 if(t.dataset.da!==undefined){const x=list.find(d=>d.id===t.dataset.da);if(!x)return;loadDraft(x);if(Object.keys(CH).length||Object.keys(PG).length)$('apply').click();}
 if(t.dataset.dd!==undefined){const x=list.find(d=>d.id===t.dataset.dd);if(!x||!confirm('Видалити чернетку «'+x.name+'»?'))return;const r=await api('/api/discounts/drafts/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:x.id})});const d=await r.json();if(DRAFT&&DRAFT.id===x.id)DRAFT=null;upd(true);loadDrafts(d.drafts);}
});
function paintRow(a){const tr=document.querySelector('tr[data-a="'+CSS.escape(a)+'"]');if(!tr)return;const r=ROWS.find(x=>x.article===a),c=CH[a];tr.classList.toggle('changed',!!c||PG[a]!==undefined);const inp=tr.querySelector('[data-v]'),np=tr.querySelector('[data-np]');const bad=c&&c.kind!=='none'&&invalid(r,c.kind,c.value);inp.classList.toggle('err',!!bad);np.innerHTML=c?(c.kind==='none'?'→ без знижки, '+money(r.full):(bad?'<span style="color:var(--bad)">'+(c.kind==='pct'?'від 1 до 99 %':'менше за '+money(r.full))+'</span>':'→ <b>'+money(newPrice(r,c.kind,c.value))+'</b>')):'';}
document.addEventListener('input',e=>{const t=e.target;if(t.dataset.v!==undefined){const a=t.dataset.v;setChange(a,document.querySelector('[data-k="'+CSS.escape(a)+'"]').value,t.value);paintRow(a);}});
document.addEventListener('change',e=>{const t=e.target;if(t.dataset.p!==undefined){setPage(t.dataset.p,t.checked);t.closest('tr').classList.toggle('changed',PG[t.dataset.p]!==undefined||!!CH[t.dataset.p]);return;}if(t.dataset.k!==undefined){const a=t.dataset.k;const v=document.querySelector('[data-v="'+CSS.escape(a)+'"]').value;if(v)setChange(a,t.value,v);paintRow(a);}
 if(t.dataset.ty!==undefined){const s=new Set(F.types);t.checked?s.add(t.dataset.ty):s.delete(t.dataset.ty);set('types',TYPES.map(x=>x.name).filter(n=>s.has(n)));}
 if(t.dataset.whall!==undefined)set('wh',t.checked?'all':[DEFWH]);
 if(t.dataset.wh!==undefined){const s=new Set(whIds());t.checked?s.add(t.dataset.wh):s.delete(t.dataset.wh);const v=WH.map(w=>String(w.id)).filter(id=>s.has(id));set('wh',v.length?v:'all');}
 if(t.dataset.opt!==undefined){const pop=t.closest('.pop');if(t.dataset.opt==='grp')document.querySelectorAll('details[data-g]').forEach(d=>d.open=false);set(t.dataset.opt,t.value);pop.open=false;}
 if(t.dataset.rng!==undefined){const [a,b]=t.dataset.rng.split('|');F.qmin=a;set('qmax',b);}
 if(t.dataset.prng!==undefined){const [a,b]=t.dataset.prng.split('|');F.pmin=a;set('pmax',b);}
 if(t.dataset.pg!==undefined){const pop=t.closest('.pop');F.pg=t.dataset.pg;PG={};if(!PAGE())F.onlyp=false;set('pg',F.pg);upd();pop.open=false;}
 if(t.dataset.onlyp!==undefined)set('onlyp',t.checked);});
document.addEventListener('input',e=>{const t=e.target;if(t.classList.contains('ms')){const q=t.value.trim().toLowerCase();t.parentElement.querySelectorAll('.mi').forEach(m=>{m.hidden=!!q&&!m.textContent.toLowerCase().includes(q);});return;}if(t.dataset.r!==undefined){F[t.dataset.r]=t.value;saveF();render();const d=t.closest('[data-pop]');const pp=POPS.find(p=>p.id===d.dataset.pop);d.querySelector('b').textContent=pp.text();d.classList.toggle('on',!!pp.on());}});
document.addEventListener('click',e=>{const t=e.target;
 if(t.dataset.clr!==undefined){const a=t.dataset.clr;const r=ROWS.find(x=>x.article===a);if(r.kind)CH[a]={kind:'none',value:0};else delete CH[a];upd();render();}
 if(t.dataset.gset!==undefined){const g=t.dataset.gset;const kind=document.querySelector('[data-gk="'+CSS.escape(g)+'"]').value;const v=document.querySelector('[data-gv="'+CSS.escape(g)+'"]').value;if(!v)return;const gf=GROUPS[F.grp];const rows=ROWS.filter(r=>gf(r)===g&&visible(r));const has=rows.filter(r=>r.kind);const fill=skip=>{for(const r of rows)if(!(skip&&r.kind))setChange(r.article,kind,v);render();};
  if(!has.length)return fill(false);const mx=Math.max(...has.map(r=>r.kind==='pct'?r.pct:Math.round(r.amt/r.full*100)));
  ask('У '+plural(has.length,'товару','товарів','товарів')+' групи вже є знижка (до '+mx+' %)','<p>Нова знижка: '+esc(v)+(kind==='pct'?' %':' грн')+' для '+rows.length+' показаних товарів групи «'+esc(g)+'».</p>',[['Перезаписати на нову',()=>fill(false)],['Лишити їхні знижки, заповнити решту',()=>fill(true)]]);}
 if(t.dataset.gclr!==undefined){const g=t.dataset.gclr;const gf=GROUPS[F.grp];for(const r of ROWS)if(gf(r)===g&&visible(r)){if(r.kind)CH[r.article]={kind:'none',value:0};else delete CH[r.article];}upd();render();}
 if(t.dataset.gpa!==undefined||t.dataset.gpr!==undefined){const on=t.dataset.gpa!==undefined;const g=on?t.dataset.gpa:t.dataset.gpr;const gf=GROUPS[F.grp];for(const r of ROWS)if(gf(r)===g&&visible(r)&&r.main_page!==PAGE())setPage(r.article,on);render();}
 if(t.dataset.act==='tall')set('types',[]);
 if(t.dataset.act==='whsale')set('wh',WH.filter(w=>!/швея|реклама/i.test(w.name)).map(w=>String(w.id)));
 if(t.dataset.act==='whdef')set('wh',[DEFWH]);
 if(t.id==='clrall'){const rows=ROWS.filter(r=>r.kind&&visible(r));if(!confirm('Зняти знижку з '+rows.length+' показаних товарів? Запишеться лише після «Застосувати».'))return;for(const r of rows)CH[r.article]={kind:'none',value:0};upd();render();}
 if(t.id==='cnt'||t.id==='onlyc'){if(t.id==='cnt'&&!Object.keys(CH).length&&!Object.keys(PG).length)return;ONLYC=t.id==='cnt'?!ONLYC:false;render();}
 const sc=t.closest&&t.closest('td.stock');if(sc&&sc.querySelector('.brk'))sc.classList.toggle('open');
 if(t.id==='reset'||t.id==='reset2'){F.q='';F.types=[];F.disc='any';F.avail='any';F.qmin='';F.qmax='';F.pmin='';F.pmax='';F.onlyp=false;F.wh=[DEFWH];ONLYC=false;bind();saveF();render();}
 if(!e.target.closest('.pop'))document.querySelectorAll('.pop[open]').forEach(d=>d.open=false);else{const p=e.target.closest('.pop');document.querySelectorAll('.pop[open]').forEach(d=>{if(d!==p)d.open=false});}
});
const visible=r=>!!document.querySelector('tr[data-a="'+CSS.escape(typeof r==='string'?r:r.article)+'"]');   // group actions touch only the rows the current filters show
function showPics(d){d.querySelectorAll('td.pic img[data-src]').forEach(i=>{i.src=i.dataset.src;i.removeAttribute('data-src');});}
document.addEventListener('toggle',e=>{if(e.target.tagName==='DETAILS'&&e.target.open){showPics(e.target);const ms=e.target.classList.contains('pop')&&e.target.querySelector('.ms');if(ms&&matchMedia('(min-width:700px)').matches)setTimeout(()=>ms.focus(),0);}},true);
let qt;$('q').oninput=()=>{F.q=$('q').value;$('qx').hidden=!F.q;$('qk').hidden=!!F.q;clearTimeout(qt);qt=setTimeout(()=>{saveF();render();},120);};
$('qx').onclick=()=>{F.q='';bind();saveF();render();$('q').focus();};
$('q').onkeydown=e=>{if(e.key==='Escape'){F.q='';bind();saveF();render();}};
document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.pop[open]').forEach(d=>d.open=false);if(e.key==='/'&&!/^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement.tagName)){e.preventDefault();$('q').focus();$('q').select();}});
const nchg=()=>new Set([...Object.keys(CH),...Object.keys(PG)]).size;
$('reload').onclick=()=>{const n=nchg();if(n&&!confirm('Є '+n+' незбережених змін. Оновити каталог і скинути їх?'))return;load();};
window.addEventListener('beforeunload',e=>{if(Object.keys(CH).length||Object.keys(PG).length){e.preventDefault();e.returnValue='';}});
const fmt=s=>s.alt_parent&&s.price===undefined?('розділи: '+(s.alt_parent.length?s.alt_parent.join(', '):'—')):(s.discount?('−'+s.discount+'% від '+money(s.price)):(s.price_old>s.price?(money(s.price)+' (повна '+money(s.price_old)+')'):money(s.price)));
const fmtPg=i=>i.after&&i.after.op?(i.after.op==='add'?'додано на сторінку «'+esc(i.after.page_title)+'»':i.after.op==='remove'?'прибрано зі сторінки «'+esc(i.after.page_title)+'»':'повернуто розділи'+(i.after.page_title?' («'+esc(i.after.page_title)+'»)':'')):null;
async function loadLog(){const r=await api('/api/discounts/log',{cache:'no-store'});const d=await r.json();if(!d.ok)return;$('logn').textContent=d.entries.length?('· '+d.entries.length):'';
 $('log').innerHTML=d.entries.map(e=>{const who=(e.who&&e.who.ip)?' · '+e.who.ip:'';const items=e.items.slice(0,40).map(i=>'<li><b>'+esc(i.article)+'</b> '+esc(i.name||'')+(fmtPg(i)?': '+fmtPg(i):(i.before&&i.after?': '+esc(fmt(i.before))+' → '+esc(fmt(i.after)):''))+(i.result&&!/оновлен|обновлен/i.test(i.result)?' <span style="color:var(--bad)">'+esc(i.result)+'</span>':'')+'</li>').join('')+(e.items.length>40?'<li>… ще '+(e.items.length-40)+'</li>':'');
 return '<div class="le'+(e.rolled_back_by?' undone':'')+'"><div class="h"><b>'+esc(e.at)+'</b><span class="k'+(e.kind==='rollback'?' rb':'')+'">'+(e.kind==='rollback'?'відкат запису '+esc(e.rollback_of):'зміна')+'</span><span class="hid">'+e.applied+' арт.'+(e.page?' · добірка «'+esc(e.page)+'»':'')+esc(who)+'</span>'+(e.rolled_back_by?'<span class="hid">відкочено</span>':(e.kind==='apply'?'<button class="ghost sm" data-rb="'+esc(e.id)+'">Відкотити</button>':'<button class="ghost sm" data-rb="'+esc(e.id)+'">Відкотити відкат</button>'))+'</div><ul>'+items+'</ul></div>'}).join('')||'<div class="le hid">Змін ще не було.</div>';}
document.addEventListener('click',async e=>{const t=e.target;if(t.dataset.rb===undefined)return;if(!confirm('Повернути значення, які були до цієї зміни? Ціни на сайті зміняться одразу.'))return;t.disabled=true;
 const r=await api('/api/discounts/rollback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:t.dataset.rb})});const d=await r.json();
 $('msg').textContent=d.ok?('Відкочено: '+d.applied+' арт.'):(d.error||'Помилка');$('msg').className='msg '+(d.ok?'ok':'bad');await loadLog();await load(true);});
loadLog();
const rowOf=a=>ROWS.find(x=>x.article===a)||{name:'',full:0};
const curTxt=r=>r.kind?money(r.now)+' ('+(r.kind==='pct'?'−'+r.pct+' %':'−'+money(r.amt))+')':money(r.full);
const newTxt=(r,c)=>c.kind==='none'?money(r.full)+' (без знижки)':money(newPrice(r,c.kind,c.value))+' ('+(c.kind==='pct'?'−'+c.value+' %':'−'+money(c.value))+')';
$('apply').onclick=()=>{const items=Object.entries(CH).map(([article,c])=>({article,kind:c.kind,value:c.value}));
 const pages={page:PAGE(),add:Object.entries(PG).filter(([a,v])=>v).map(([a])=>a),remove:Object.entries(PG).filter(([a,v])=>!v).map(([a])=>a)};const np=pages.add.length+pages.remove.length;const pt=(PAGES.find(p=>p.id===PAGE())||{}).title||'';
 const hid=[...new Set([...Object.keys(CH),...Object.keys(PG)])].filter(a=>!visible(a)).length;
 let h='';if(items.length){h+='<div class="sec">Знижки: '+items.length+'</div><table>'+items.slice(0,40).map(i=>{const r=rowOf(i.article);return '<tr><td class="art">'+esc(i.article)+'</td><td>'+esc(r.name)+'</td><td class="num"><s class="hid">'+curTxt(r)+'</s></td><td class="num"><b>'+newTxt(r,CH[i.article])+'</b></td></tr>'}).join('')+(items.length>40?'<tr><td colspan="4" class="hid">… ще '+(items.length-40)+'</td></tr>':'')+'</table>';}
 if(pages.add.length)h+='<div class="sec">Додати на сторінку «'+esc(pt)+'»: '+pages.add.length+'</div><div class="hid">'+pages.add.slice(0,60).map(a=>esc(a)+' '+esc(rowOf(a).name)).join(' · ')+(pages.add.length>60?' · …':'')+'</div>';
 if(pages.remove.length)h+='<div class="sec">Прибрати зі сторінки «'+esc(pt)+'»: '+pages.remove.length+'</div><div class="hid">'+pages.remove.slice(0,60).map(a=>esc(a)+' '+esc(rowOf(a).name)).join(' · ')+(pages.remove.length>60?' · …':'')+'</div>';
 if(hid)h+='<p class="hid">'+hid+' із цих рядків зараз приховано фільтрами — вони теж запишуться.</p>';
 h+='<p class="hid">Сайт obiimy.world зміниться одразу; Shopify — після синхронізації. Запис можна відкотити з журналу.</p>';
 $('dlgh').textContent='Записати в Хорошоп: '+items.length+' змін знижок'+(np?', '+np+' змін добірки':'');$('dlgb').innerHTML=h;$('dlg').showModal();
 $('dlgalt').hidden=true;$('dlgok').textContent='Записати';$('dlgok').onclick=()=>{$('dlg').close();doApply(items,pages);};$('dlgx').onclick=()=>$('dlg').close();};
function ask(title,html,btns){$('dlgh').textContent=title;$('dlgb').innerHTML=html;$('dlgok').textContent=btns[0][0];$('dlgok').onclick=()=>{$('dlg').close();btns[0][1]();};const alt=$('dlgalt');alt.hidden=!btns[1];if(btns[1]){alt.textContent=btns[1][0];alt.onclick=()=>{$('dlg').close();btns[1][1]();};}$('dlgx').onclick=()=>$('dlg').close();$('dlg').showModal();}
const visibleA=a=>!!document.querySelector('tr[data-a="'+CSS.escape(a)+'"]');
async function doApply(items,pages){
 $('apply').disabled=true;$('msg').textContent='Записую…';$('msg').className='msg';
 const r=await api('/api/discounts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items,pages})});const d=await r.json();
 if(!d.ok){$('msg').textContent=d.error||'Помилка';$('msg').className='msg bad';$('apply').disabled=false;return}
 PG={};
 const bad=d.plan.filter(p=>p.error||!/оновлен|обновлен/i.test(p.result||''));$('msg').textContent=bad.length?('Записано '+(d.applied-bad.length)+', з помилками '+bad.length+': '+bad.map(p=>p.article+' — '+(p.error||p.result)).join('; ')):('Записано: '+d.applied+'. Щоб оновити Shopify, запустіть синхронізацію.');$('msg').className='msg '+(bad.length?'bad':'ok');
 DRAFT=null;await load(true);await loadLog();await loadDrafts();}
if(KEY){for(const id of ['lnk','lnk2','lnk3']){const l=document.getElementById(id);if(l)l.href+='?key='+encodeURIComponent(KEY);}}
bind();load().then(()=>loadDrafts());
</script></body></html>"""
