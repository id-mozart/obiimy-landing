#!/usr/bin/env python3
"""Horoshop (obiimy.world) → Shopify (shop.obiimy.world) catalogue sync, step by step and read-only until told otherwise.

Horoshop API (docs: https://horoshop.notion.site/cartum-api): JSON POST to https://<domain>/api/<function>/, a 32-char token from
`auth` (login + password of an API user created in the admin panel, Налаштування → Користувачі; the token lives 600 s),
`catalog/export` pages of ≤ 500 products, `currency/export` with the rates the storefront uses.
Credentials — ~/.config/obiimy/horoshop.env (HOROSHOP_DOMAIN, HOROSHOP_LOGIN, HOROSHOP_PASSWORD; never print, never commit).

  python3 src/horoshop.py export     → data/horoshop/products.json (every product, every field) + currency.json
  python3 src/horoshop.py report     → compare with Shopify by SKU (= Horoshop article): prices, new, missing → data/horoshop/report.json
Shopify prices are USD = Horoshop UAH price ÷ the site's UAH→USD rate, rounded to whole dollars — that is what the English storefront shows
(14.11.2026: rate 35.5, mask 2700 грн → $76, the same $76 in Shopify).
"""
import json, os, pathlib, re, sys, time, urllib.request, uuid

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "horoshop"
ENV = pathlib.Path.home() / ".config/obiimy/horoshop.env"

def _env():
    e = dict(os.environ)
    if ENV.exists():
        for l in ENV.read_text().splitlines():
            if "=" in l and not l.startswith("#"):
                k, v = l.strip().split("=", 1); e.setdefault(k, v.strip().strip('"').strip("'"))
    return e

class Horoshop:
    def __init__(self):
        e = _env()
        self.domain, self.login, self.password = e.get("HOROSHOP_DOMAIN", "obiimy.world"), e.get("HOROSHOP_LOGIN"), e.get("HOROSHOP_PASSWORD")
        if not (self.login and self.password): sys.exit("немає HOROSHOP_LOGIN / HOROSHOP_PASSWORD у ~/.config/obiimy/horoshop.env")
        self.token, self.token_at = None, 0

    def call(self, fn, body=None, auth=True):
        body = dict(body or {})
        if auth:
            if not self.token or time.time() - self.token_at > 500: self.auth()
            body["token"] = self.token
        req = urllib.request.Request(f"https://{self.domain}/api/{fn}/", data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
                                     headers={"Content-Type": "application/json", "User-Agent": "obiimy-sync/1.0"})
        r = json.load(urllib.request.urlopen(req, timeout=120))
        if r.get("status") not in ("OK",): raise RuntimeError(f"{fn}: {json.dumps(r, ensure_ascii=False)[:400]}")
        return r.get("response") or {}

    def auth(self):
        self.token = self.call("auth", {"login": self.login, "password": self.password}, auth=False)["token"]; self.token_at = time.time()

    def products(self, **sel):
        """Every product (variants are separate rows: `article` with `parent_article`), 500 a page."""
        out, off = [], 0
        while True:
            page = self.call("catalog/export", {"offset": off, "limit": 500, **sel}).get("products") or []
            out += page; off += 500
            sys.stderr.write(f"  export {len(out)}\n")
            if len(page) < 500: return out

    def rates(self):
        """{iso: UAH per one unit}, from the storefront's currency table."""
        cur = self.call("currency/export", {"enabledOnly": 0}).get("currency") or []
        uah = next((c for c in cur if c["iso"] == "UAH"), None)
        return {r["relatedIso"]: r["exchangeCourse"] for r in (uah or {}).get("exchangeRates", [])} | {"UAH": 1}

# ─── normalisation ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
def L(v, lang="en"):
    """A multi-language value → one language (en, then ua, then ru), plain string."""
    if isinstance(v, dict):
        if "value" in v and "id" in v: return L(v["value"], lang)
        return (v.get(lang) or v.get("ua") or v.get("ru") or "") if v else ""
    return v or ""

def name(p, lang="en"):
    return (L(p.get("mod_title"), lang) or L(p.get("title"), lang)).strip()

def effective_uah(p):
    """What the storefront charges: `price` less the relative `discount` (percent) — the site shows t-shirt 1700 грн · −40 % as 1020 грн / $29."""
    return float(p.get("price") or 0) * (1 - float(p.get("discount") or 0) / 100)

def usd(price_uah, rate):
    return int(round(float(price_uah) / rate)) if price_uah else 0

def presence(p):
    return L(p.get("presence"), "en").strip() or "?"

# ─── Shopify side ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
def shopify_products():
    sys.path.insert(0, str(ROOT / "shopify")); import shop
    rows, cursor = [], None
    while True:
        d = shop.gql("""query($c: String) { products(first: 100, after: $c) { pageInfo { hasNextPage endCursor }
          nodes { id title handle status productType vendor totalInventory
            variants(first: 20) { nodes { id sku price compareAtPrice title inventoryQuantity inventoryItem { id tracked } } } } } }""", {"c": cursor})
        rows += d["products"]["nodes"]
        if not d["products"]["pageInfo"]["hasNextPage"]: return rows
        cursor = d["products"]["pageInfo"]["endCursor"]

# ─── commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def cmd_export():
    OUT.mkdir(parents=True, exist_ok=True)
    h = Horoshop(); rates = h.rates(); prods = h.products()
    (OUT / "currency.json").write_text(json.dumps({"at": time.strftime("%Y-%m-%d %H:%M"), "rates_uah_per_unit": rates}, ensure_ascii=False, indent=1))
    (OUT / "products.json").write_text(json.dumps(prods, ensure_ascii=False, indent=0))
    shown = [p for p in prods if int(p.get("display_in_showcase") or 0)]
    parents = {p.get("parent_article") or p["article"] for p in prods}
    print(f"Хорошоп: {len(prods)} позицій (артикулів), {len(parents)} товарів-батьків, {len(shown)} показуються на вітрині; курс USD {rates.get('USD')}")
    by_pres = {}
    for p in prods: by_pres[presence(p)] = by_pres.get(presence(p), 0) + 1
    print("наявність:", by_pres)
    cats = {}
    for p in prods: c = L(p.get("parent"), "ua"); cats[c] = cats.get(c, 0) + 1
    for c, n in sorted(cats.items(), key=lambda x: -x[1]): print(f"  {n:>4}  {c}")

# Shopify SKUs whose article was renamed on the site (14.11.2026): old pocket-square and set codes → the current Horoshop articles
def alias(sku):
    m = re.fullmatch(r"P-(44-\d+-D)", sku)
    if m: return m.group(1)                                   # P-44-21-D → 44-21-D (double-sided pocket square)
    m = re.fullmatch(r"NT(84|140)-44-(\d+)", sku)
    if m: return f"NTD{m.group(1)}-44-{m.group(2)}"           # NT84-44-1 → NTD84-44-1 (double-sided set)
    return sku

def cmd_report():
    prods = json.loads((OUT / "products.json").read_text()); rate = json.loads((OUT / "currency.json").read_text())["rates_uah_per_unit"]["USD"]
    hs = {p["article"].strip(): p for p in prods if p.get("article")}
    sp = shopify_products()
    sv = {}                                                       # sku → (product, variant)
    for pr in sp:
        for v in pr["variants"]["nodes"]:
            if v.get("sku"): sv.setdefault(v["sku"].strip(), (pr, v))
    matched, changes, same, only_shop, only_hs = [], [], [], [], []
    for sku, (pr, v) in sv.items():
        p = hs.get(sku) or (hs.get(alias(sku)) if alias(sku) not in sv else None)
        if not p: only_shop.append((sku, pr["title"], pr["status"], v["price"])); continue
        new = usd(effective_uah(p), rate); old = float(v["price"])
        matched.append(sku)
        row = dict(sku=sku, hs_article=p["article"], title=pr["title"], status=pr["status"], old_usd=old, new_usd=new, uah=p["price"], discount=p.get("discount") or 0, full_usd=usd(p["price"], rate), presence=presence(p), shown=int(p.get("display_in_showcase") or 0), variant_id=v["id"], product_id=pr["id"])
        (changes if abs(old - new) >= 0.5 else same).append(row)
    used = {hs[sku]["article"] if sku in hs else alias(sku) for sku in sv}
    for sku, p in hs.items():
        if sku not in used: only_hs.append(dict(sku=sku, parent=p.get("parent_article"), name=name(p), uah=p["price"], discount=p.get("discount") or 0, usd=usd(effective_uah(p), rate), presence=presence(p), shown=int(p.get("display_in_showcase") or 0), category=L(p.get("parent"), "ua")))
    rep = dict(at=time.strftime("%Y-%m-%d %H:%M"), rate=rate, shopify_products=len(sp), shopify_skus=len(sv), horoshop_skus=len(hs), matched=len(matched),
               price_changes=changes, price_same=len(same), only_shopify=only_shop, only_horoshop=only_hs)
    (OUT / "report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1))
    print(f"Shopify: {len(sp)} товарів / {len(sv)} SKU · Хорошоп: {len(hs)} артикулів · збіглося за SKU: {len(matched)} · курс {rate}")
    print(f"ціна без змін: {len(same)} · ціна змінюється: {len(changes)} · лише в Shopify: {len(only_shop)} · лише в Хорошопі: {len(only_hs)}")
    if changes:
        print("\nЗміни ціни (USD старa → нова, грн):")
        for r in sorted(changes, key=lambda r: r["sku"]): print(f"  {r['sku']:<12} {r['title'][:46]:<46} {r['old_usd']:>7.2f} → {r['new_usd']:>4}   ({r['uah']} грн" + (f" −{r['discount']} %" if r['discount'] else "") + f", {r['presence']})")
    if only_shop:
        print("\nЛише в Shopify (немає такого артикулу в Хорошопі):")
        for sku, t, st, pz in sorted(only_shop): print(f"  {sku:<12} {t[:50]:<50} {st[:6]} ${pz}")
    if only_hs:
        shown = [r for r in only_hs if r["shown"]]; hidden = len(only_hs) - len(shown)
        print(f"\nЛише в Хорошопі ({len(shown)} на вітрині, {hidden} прихованих):")
        for r in sorted(shown, key=lambda r: (r["category"], r["sku"])): print(f"  {r['sku']:<12} {r['name'][:50]:<50} {r['uah']:>6} грн → ${r['usd']:<4} {r['presence']:<12} {r['category']}")


# ═══ writing to Shopify (14.11.2026, «нужно все товары заменить») ══════════════════════════════════════════════════════════════
#   python3 src/horoshop.py prices            dry run: what would change on the matched SKUs (price, compare-at, renamed SKU)
#   python3 src/horoshop.py prices --apply    productVariantsBulkUpdate, logged to data/horoshop/applied-prices.jsonl
#   python3 src/horoshop.py new               dry run: the products that would be created from the Horoshop-only articles → new-plan.json
#   python3 src/horoshop.py new --apply       productSet (draft, EN texts, photos from the site), logged to data/horoshop/applied-new.jsonl
# Existing products keep their Shopify titles and descriptions (they were localised for the international store: inches, Western Bid
# delivery and return lines, 28.09.2026) — only price, compare-at price, SKU change. New ones are created as DRAFT for the client to review.
import html as _html

INCH = {"44х44": '17"x17"', "44x44": '17"x17"', "65x65": '26"x26"', "65х65": '26"x26"', "88x88": '35"x35"', "88х88": '35"x35"', "88*88": '35"x35"',
        "84x5": '33"x2"', "84х5": '33"x2"', "140x5": '55"x2"', "140х5": '55"x2"', "50x70": '20"x28"', "50х70": '20"x28"'}
TYPE = {"Хустки": "Scarf", "Хустки 2D": "Scarf 2D", "Подарунки": "Gift sets", "Твіллі": "Twilly", "Резинки": "Scrunchie", "Маски для сну": "Sleeping masks",
        "Хустки паше/Паше односторонні": "Pocket square", "Хустки паше/Паше двосторонні": "Pocket square", "Прикраси": "Scarf rings",
        "Obiimy HOME/Футболки": "T-shirts", "Obiimy HOME/Сорочки": "Shirts", "Obiimy HOME/Піжами": "Clothing > Pajamas",
        "Obiimy HOME/Аксесуари для сну ": "Bedding", "Obiimy HOME/Аксесуари для сну": "Bedding", "Пакування та подарунки": "Packaging"}
SIZE_OPTION = {"L", "M", "S", "XL", "XS", "42 / L / 50", "40 / M / 48", "38 / S / 46", "44 / XL / 52"}   # these become variants of one product
COLOR_OPTION = {"Gold", "Silver", "Pink", "Purple", "Black", "White", "Grey", "Gray"}

def _shop():
    sys.path.insert(0, str(ROOT / "shopify")); import shop; return shop

def _title_en(p):
    t = name(p, "en")
    for k, v in INCH.items(): t = re.sub(r"(?<![\d\"])" + re.escape(k) + r"(?![\d\"])", v, t)
    return re.sub(r"\s+", " ", t).strip()

def _en(v):
    """English only — no fallback to Ukrainian or Russian (the international store must not get Cyrillic texts)."""
    return (v.get("en") or "").strip() if isinstance(v, dict) else (v or "").strip()

def _desc_html(p):
    d = _en(p.get("description"))
    if re.search(r"[\u0400-\u04FF]", d): d = ""                     # an "English" field filled with Ukrainian — treat as missing
    ch = p.get("characteristics") or {}
    extra = []
    for key, label in (("sklad", "Composition and care"), ("druk", "Print"), ("pakuvannja", "Packaging"), ("kranaVirobnik", "Country of origin")):
        v = _en(ch.get(key)) if isinstance(ch.get(key), (dict, str)) else ""
        if re.search(r"[\u0400-\u04FF]", v): v = ""
        if v: extra.append(f"<p><strong>{label}:</strong> {v}</p>" if not v.startswith("<") else f"<p><strong>{label}</strong></p>{v}")
    return d + ("".join(extra) if extra else "")

def _images(p):
    seen, out = set(), []
    for u in (p.get("images") or []) + (p.get("gallery_common") or []):
        if u and u not in seen: seen.add(u); out.append(u)
    return out

def _groups(articles, hs):
    """Horoshop-only articles → Shopify products. One product per article, except clothing sizes and colours of the same parent, which
    become variants of one product (the store's existing convention: scarves and twillies are separate products per size)."""
    by_parent = {}
    for a in articles: by_parent.setdefault(hs[a].get("parent_article") or a, []).append(a)
    products = []
    for parent, arts in by_parent.items():
        vals = {a: L(hs[a].get("Rozmir"), "en").strip() for a in arts}
        if len(arts) > 1 and all(v in SIZE_OPTION for v in vals.values()):
            products.append(("Size", sorted(arts, key=lambda a: ["XS", "S", "38 / S / 46", "M", "40 / M / 48", "L", "42 / L / 50", "XL", "44 / XL / 52"].index(vals[a]) if vals[a] in ["XS", "S", "38 / S / 46", "M", "40 / M / 48", "L", "42 / L / 50", "XL", "44 / XL / 52"] else 99)))
        elif len(arts) > 1 and all(v in COLOR_OPTION for v in vals.values()):
            products.append(("Color", sorted(arts)))
        else:
            for a in sorted(arts): products.append((None, [a]))
    return products

def cmd_prices(apply=False):
    rep = json.loads((OUT / "report.json").read_text()); rows = rep["price_changes"]
    prods = json.loads((OUT / "products.json").read_text()); hs = {p["article"]: p for p in prods}
    sp = json.loads((OUT / "shopify-before.json").read_text())
    sv = {v["sku"]: (pr, v) for pr in sp for v in pr["variants"]["nodes"] if v.get("sku")}
    plan = {}                                                      # product id → [variant inputs]
    for sku, (pr, v) in sv.items():
        p = hs.get(sku) or (hs.get(alias(sku)) if alias(sku) not in sv else None)
        if not p: continue
        new = usd(effective_uah(p), rep["rate"]); full = usd(p["price"], rep["rate"])
        inp = {"id": v["id"]}
        if abs(float(v["price"]) - new) >= 0.5: inp["price"] = f"{new:.2f}"
        want_cmp = f"{full:.2f}" if full > new else None
        if (v.get("compareAtPrice") or None) != want_cmp: inp["compareAtPrice"] = want_cmp
        if p["article"] != sku: inp["inventoryItem"] = {"sku": p["article"]}
        if len(inp) > 1: plan.setdefault(pr["id"], []).append((sku, pr["title"], inp))
    n = sum(len(v) for v in plan.values())
    print(f"{'Застосовую' if apply else 'План'}: {n} варіантів у {len(plan)} товарах (ціна / compare-at / SKU)")
    for pid, items in list(plan.items())[:400]:
        for sku, t, inp in items: print(f"  {sku:<13} {t[:44]:<44} " + " ".join(f"{k}={json.dumps(v, ensure_ascii=False)}" for k, v in inp.items() if k != "id"))
    if not apply: return
    shop = _shop(); log = open(OUT / "applied-prices.jsonl", "a", encoding="utf-8"); ok = bad = 0
    for pid, items in plan.items():
        r = shop.gql("""mutation($pid: ID!, $v: [ProductVariantsBulkInput!]!) { productVariantsBulkUpdate(productId: $pid, variants: $v) {
              productVariants { id sku price compareAtPrice } userErrors { field message } } }""", {"pid": pid, "v": [i for _, _, i in items]})["productVariantsBulkUpdate"]
        err = r["userErrors"]
        log.write(json.dumps({"at": time.strftime("%Y-%m-%d %H:%M:%S"), "product": pid, "variants": [i for _, _, i in items], "errors": err}, ensure_ascii=False) + "\n")
        if err: bad += 1; print("  ПОМИЛКА", pid, err)
        else: ok += len(items)
        time.sleep(0.3)
    print(f"готово: {ok} варіантів оновлено, помилок у {bad} товарах")

def cmd_new(apply=False):
    rep = json.loads((OUT / "report.json").read_text()); rate = rep["rate"]
    prods = json.loads((OUT / "products.json").read_text()); hs = {p["article"]: p for p in prods}
    def skip(a):   # gift certificates are denominated in гривня, «Packaging» is a 1-dollar service line — not for the USD store
        return effective_uah(hs[a]) <= 0 or a.lower().startswith("gift") or a == "pckg"
    arts = [r["sku"] for r in rep["only_horoshop"] if not skip(r["sku"])]
    skipped0 = [r["sku"] for r in rep["only_horoshop"] if skip(r["sku"])]
    plan = []
    for opt, group in _groups(arts, hs):
        first = hs[group[0]]
        cat = L(first.get("parent"), "ua")
        variants = []
        for a in group:
            p = hs[a]; price = usd(effective_uah(p), rate); full = usd(p["price"], rate)
            v = {"sku": a, "price": f"{price:.2f}", "inventoryPolicy": "DENY", "inventoryItem": {"tracked": presence(p) != "In stock"},   # in stock → not tracked (purchasable); out of stock → tracked with 0 → «Sold out»
                 "optionValues": [{"optionName": opt or "Title", "name": (L(p.get("Rozmir"), "en").strip() if opt else "Default Title")}]}
            if full > price: v["compareAtPrice"] = f"{full:.2f}"
            variants.append(v)
        title = _title_en(first)
        if opt == "Size": title = re.sub(r"\s+(XS|S|M|L|XL|\d\d / [SMLX]+ / \d\d)$", "", title)
        if opt == "Color": title = re.sub(r"\s*\b(golden|gold|silver|pink|purple)\b\s*", " ", title, flags=re.I).replace("  ", " ").strip()
        imgs = []
        for a in group:
            for u in _images(hs[a]):
                if u not in imgs: imgs.append(u)
        plan.append({"articles": group, "category": cat, "presence": [presence(hs[a]) for a in group], "shown": [int(hs[a].get("display_in_showcase") or 0) for a in group],
                     "input": {"title": title, "descriptionHtml": _desc_html(first), "vendor": "Obiimy", "productType": TYPE.get(cat, "Scarf"), "status": "ACTIVE" if all(int(hs[a].get("display_in_showcase") or 0) for a in group) else "DRAFT",
                               "tags": ["horoshop-sync", cat.split("/")[-1].strip()] + (["out-of-stock"] if any(presence(hs[a]) != "In stock" for a in group) else [])
                                       + (["needs-translation"] if not _en(first.get("description")) or re.search(r"[\u0400-\u04FF]", _en(first.get("description"))) else []),
                               "productOptions": [{"name": opt or "Title", "position": 1, "values": [{"name": v["optionValues"][0]["name"]} for v in variants]}],
                               "variants": variants, "files": [{"originalSource": u, "contentType": "IMAGE", "alt": title} for u in imgs[:12]]}})
    (OUT / "new-plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    print(f"{'Створюю' if apply else 'План'}: {len(plan)} товарів із {sum(len(x['articles']) for x in plan)} артикулів ({sum(1 for x in plan if x['input']['status'] == 'ACTIVE')} активних, {sum(1 for x in plan if x['input']['status'] != 'ACTIVE')} чернеток — приховані на сайті); пропущено: {skipped0}")
    for x in plan: print(f"  {x['input']['productType']:<16} {x['input']['title'][:52]:<52} {'/'.join(x['articles'])[:40]:<40} ${'/'.join(v['price'][:-3] for v in x['input']['variants'])}  фото {len(x['input']['files'])}  {','.join(sorted(set(x['presence'])))}")
    if not apply: return
    shop = _shop(); log = open(OUT / "applied-new.jsonl", "a", encoding="utf-8"); ok = bad = 0
    done = {json.loads(l)["articles"][0] for l in (OUT / "applied-new.jsonl").read_text(encoding="utf-8").splitlines() if l.strip() and not json.loads(l).get("errors")} if (OUT / "applied-new.jsonl").exists() else set()
    for x in plan:
        if x["articles"][0] in done: continue                     # re-runs skip what already landed
        r = shop.gql("""mutation($i: ProductSetInput!) { productSet(synchronous: true, input: $i) { product { id handle status variants(first: 10) { nodes { id sku price } } }
              userErrors { field message } } }""", {"i": x["input"]})["productSet"]
        err = r["userErrors"]; pr = r.get("product") or {}
        log.write(json.dumps({"at": time.strftime("%Y-%m-%d %H:%M:%S"), "articles": x["articles"], "product": pr.get("id"), "handle": pr.get("handle"), "errors": err}, ensure_ascii=False) + "\n"); log.flush()
        if err: bad += 1; print("  ПОМИЛКА", x["articles"], err)
        else: ok += 1; print(f"  + {pr.get('handle')}  {'/'.join(x['articles'])}")
        time.sleep(0.6)
    print(f"готово: створено {ok}, помилок {bad}")

def cmd_status(apply=False):
    """Existing products follow the site's visibility: hidden there → DRAFT here, shown → ACTIVE. Products without a SKU are not touched."""
    prods = json.loads((OUT / "products.json").read_text()); hs = {p["article"]: p for p in prods}
    sp = json.loads((OUT / "shopify-before.json").read_text()); plan = []
    for pr in sp:
        ps = [hs.get(v["sku"]) or hs.get(alias(v["sku"])) for v in pr["variants"]["nodes"] if v.get("sku")]
        ps = [p for p in ps if p]
        if not ps: continue
        want = "ACTIVE" if any(int(p.get("display_in_showcase") or 0) for p in ps) else "DRAFT"
        if pr["status"] != want: plan.append((pr["id"], pr["title"], pr["status"], want))
    print(f"{'Застосовую' if apply else 'План'} статусів: {len(plan)}")
    for pid, t, a, b in plan: print(f"  {t[:55]:<55} {a} → {b}")
    if not apply: return
    shop = _shop()
    for pid, t, a, b in plan:
        r = shop.gql("mutation($p: ProductUpdateInput!){ productUpdate(product: $p){ product { id status } userErrors { field message } } }", {"p": {"id": pid, "status": b}})["productUpdate"]
        print("  ", t[:50], r["userErrors"] or b)

def cmd_publish(apply=False):
    """After the app got write_publications / write_inventory (14.11.2026): publish the products created by `new` to every sales channel
    the existing products use, and make stock follow the site — out-of-stock variants get 0 at the store's location."""
    shop = _shop()
    pubs = [n["id"] for n in shop.gql("{ publications(first: 20) { nodes { id name } } }")["publications"]["nodes"]]
    loc = shop.gql("{ locations(first: 5) { nodes { id name isActive } } }")["locations"]["nodes"][0]["id"]
    created = [json.loads(l) for l in (OUT / "applied-new.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    pids = [c["product"] for c in created if c.get("product") and not c.get("errors")]
    prods = json.loads((OUT / "products.json").read_text()); hs = {p["article"]: p for p in prods}
    sp = shopify_products()
    oos = [(v["sku"], v["inventoryItem"]["id"], v["inventoryItem"]["tracked"], v["inventoryQuantity"]) for pr in sp for v in pr["variants"]["nodes"]
           if v.get("sku") and (hs.get(v["sku"]) or {}).get("article") and presence(hs[v["sku"]]) != "In stock"]
    print(f"{'Застосовую' if apply else 'План'}: опублікувати {len(pids)} нових товарів у {len(pubs)} каналах; обнулити залишок у {len(oos)} варіантах без наявності: {[o[0] for o in oos]}")
    if not apply: return
    ok = 0
    for pid in ([] if "--skip-publish" in sys.argv else pids):
        r = shop.gql("mutation($id: ID!, $in: [PublicationInput!]!) { publishablePublish(id: $id, input: $in) { userErrors { field message } } }",
                     {"id": pid, "in": [{"publicationId": x} for x in pubs]})["publishablePublish"]
        if r["userErrors"]: print("  ПОМИЛКА publish", pid, r["userErrors"])
        else: ok += 1
        time.sleep(0.25)
    print("опубліковано:", ok)
    for sku, item, tracked, qty in oos:
        if qty == 0 and tracked: continue
        if not tracked:
            r = shop.gql("mutation($id: ID!) { inventoryItemUpdate(id: $id, input: {tracked: true}) { userErrors { field message } } }", {"id": item})["inventoryItemUpdate"]
            if r["userErrors"]: print("  ПОМИЛКА tracked", sku, r["userErrors"])
        r = shop.gql("mutation($in: InventorySetQuantitiesInput!) { inventorySetQuantities(input: $in) @idempotent(key: \"" + uuid.uuid4().hex + "\") { userErrors { field message } } }",
                     {"in": {"name": "available", "reason": "correction", "quantities": [{"inventoryItemId": item, "locationId": loc, "quantity": 0, "changeFromQuantity": qty}]}})["inventorySetQuantities"]
        print("  ", sku, "→ 0", r["userErrors"] or "ok")
        time.sleep(0.25)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""; apply = "--apply" in sys.argv
    if cmd == "export": cmd_export()
    elif cmd == "report": cmd_report()
    elif cmd == "prices": cmd_prices(apply)
    elif cmd == "new": cmd_new(apply)
    elif cmd == "status": cmd_status(apply)
    elif cmd == "publish": cmd_publish(apply)
    else: print(__doc__)
