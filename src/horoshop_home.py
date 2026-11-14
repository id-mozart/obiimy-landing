#!/usr/bin/env python3
"""Horoshop → Shopify, part 2 (14.11.2026, «перенести коллекции и баннеры с главной, только английские версии»).

What the main site has that the Shopify store lacked: the five print collections («Поклик душі», «Пробудження», «Соло», «Дика стихія»,
«Співоча душа»), the categories Jewelry / Obiimy HOME (Shirts, T-shirts, Sleep Accessories) / Double- and Single-Sided Pocket Squares / New,
and the eight-slide hero slider. Shopify collections are smart collections by tag (the store's own convention: tag «Scarf» → collection
scarf), so the work is: tag every product with the English names of its Horoshop categories, create the missing collections with the site's
English titles, images and texts, rebuild the home slideshow from the English slides, and add the new collections to the menus.

  python3 src/horoshop_home.py tags [--apply]          tags from Horoshop categories (parent + alt_parent) on every product
  python3 src/horoshop_home.py collections [--apply]   create the missing smart collections (title, image, description from the EN site)
  python3 src/horoshop_home.py home [--apply]          upload the EN slides to Files, replace the image banner with a slideshow, add a
                                                        «Collections» list to templates/index.json (backup in shopify/backup/)
  python3 src/horoshop_home.py menus [--apply]         main menu and footer catalog: collections + new categories
Needs the data of src/horoshop.py export (data/horoshop/products.json, pages.json) and src/horoshop-collection-descriptions-en.json.
"""
import json, pathlib, re, sys, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "horoshop"
sys.path.insert(0, str(ROOT / "src")); import horoshop as H
sys.path.insert(0, str(ROOT / "shopify")); import shop

THEME = "gid://shopify/OnlineStoreTheme/159253233885"
APPLY = "--apply" in sys.argv

# Horoshop category id → Shopify tag (= the store's existing tags where a collection already exists) and collection handle
CATS = {  # id: (tag, handle, title for a new collection | None if it exists)
    1058: ("Scarf", "scarf", None), 1145: ("Scarf 2D", "scarf-2d", None), 1060: ("Gift sets", "gift-sets", None), 1057: ("Twilly", "twilly", None),
    1055: ("Scrunchie", "scrunchie", None), 1059: ("Sleeping masks", "sleeping-masks", None), 1129: ("Pocket square", "pocket-square", None),
    1133: ("Clothing > Pajamas", "pajamas", None),
    1152: ("Double-Sided Pocket Squares", "double-sided-pocket-squares", "Double-Sided Pocket Squares"),
    1153: ("Single-Sided Pocket Squares", "single-sided-pocket-squares", "Single-Sided Pocket Squares"),
    1137: ("Jewelry", "jewelry", "Jewelry"), 1139: ("Obiimy HOME", "obiimy-home", "Obiimy HOME"), 1056: ("Shirts", "shirts", "Silk Shirts"),
    1144: ("T-shirts", "t-shirts", "T-shirts"), 1149: ("Sleep Accessories", "sleep-accessories", "Silk Sleep Accessories"), 1132: ("New", "new", "New"),
    1146: ("The Call of the Soul", "the-call-of-the-soul", "The Call of the Soul"), 1147: ("Awakening", "awakening", "Awakening"),
    1154: ("Solo: A Journey Within", "solo-a-journey-within", "Solo: A Journey Within"), 1148: ("Wild Elements", "wild-elements", "Wild Elements"),
    1140: ("The Singing Soul", "the-singing-soul", "The Singing Soul"),
}
PARENT_OF = {1152: 1129, 1153: 1129, 1056: 1139, 1133: 1139, 1144: 1139, 1149: 1139}   # a child category also tags the parent
PRINTS = [1146, 1147, 1154, 1148, 1140]                                                # the site's «Collections»
DESC_SLUG = {1146: "poklyk-dushi", 1147: "probudzhennia", 1154: "solo-shliakh-do-sebe", 1148: "dyka-stykhiia", 1140: "spivocha-dusha", 1152: "pashe-dvostoronni"}

def pages():
    j = json.loads((DATA / "pages.json").read_text()); return {p["id"]: p for p in (j.get("pages") if isinstance(j, dict) else j)}

def product_cats(p):
    ids = [(p.get("parent") or {}).get("id")] + [a.get("id") for a in p.get("alt_parent") or []]
    out = set()
    for i in ids:
        while i:
            if i in CATS: out.add(i)
            i = PARENT_OF.get(i)
    return out

# ─── tags ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def cmd_tags():
    prods = json.loads((DATA / "products.json").read_text()); hs = {p["article"]: p for p in prods}
    rows, cursor = [], None
    while True:
        d = shop.gql("""query($c: String) { products(first: 100, after: $c) { pageInfo { hasNextPage endCursor } nodes { id title tags variants(first: 20) { nodes { sku } } } } }""", {"c": cursor})
        rows += d["products"]["nodes"]
        if not d["products"]["pageInfo"]["hasNextPage"]: break
        cursor = d["products"]["pageInfo"]["endCursor"]
    plan = []
    for pr in rows:
        cats = set()
        for v in pr["variants"]["nodes"]:
            p = hs.get(v["sku"] or "") or hs.get(H.alias(v["sku"] or ""))
            if p: cats |= product_cats(p)
        want = {CATS[c][0] for c in cats}; add = sorted(want - set(pr["tags"]))
        if add: plan.append((pr["id"], pr["title"], add))
    print(f"{'Застосовую' if APPLY else 'План'} тегів: {len(plan)} товарів отримають теги")
    from collections import Counter
    print("  за тегами:", Counter(t for _, _, a in plan for t in a).most_common())
    for pid, t, add in plan[:12]: print(f"   {t[:50]:<50} + {add}")
    if not APPLY: return
    ok = 0
    for pid, t, add in plan:
        r = shop.gql("mutation($id: ID!, $tags: [String!]!) { tagsAdd(id: $id, tags: $tags) { userErrors { field message } } }", {"id": pid, "tags": add})["tagsAdd"]
        if r["userErrors"]: print("  ПОМИЛКА", t, r["userErrors"])
        else: ok += 1
        time.sleep(0.2)
    print("готово:", ok)

# ─── collections ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
def cmd_collections():
    pg = pages(); df = ROOT / "src" / "horoshop-collection-descriptions-en.json"   # the EN texts of the site's collection pages (kept in src/ so the editor image has them)
    desc = json.loads(df.read_text()) if df.exists() else {}
    have = {c["handle"]: c for c in shop.gql("{ collections(first: 100) { nodes { id handle title } } }")["collections"]["nodes"]}
    plan = []
    for cid, (tag, handle, title) in CATS.items():
        if handle in have or not title: continue
        inp = {"title": title, "handle": handle, "ruleSet": {"appliedDisjunctively": False, "rules": [{"column": "TAG", "relation": "EQUALS", "condition": tag}]},
               "sortOrder": "BEST_SELLING"}
        if pg.get(cid, {}).get("image"): inp["image"] = {"src": pg[cid]["image"], "altText": title}
        if DESC_SLUG.get(cid) in desc: inp["descriptionHtml"] = desc[DESC_SLUG[cid]]
        plan.append(inp)
    if "collections" not in have:   # the site's parent page «Collections» = any of the five print collections
        plan.append({"title": "Collections", "handle": "collections", "sortOrder": "BEST_SELLING",
                     "ruleSet": {"appliedDisjunctively": True, "rules": [{"column": "TAG", "relation": "EQUALS", "condition": CATS[c][0]} for c in PRINTS]}})
    print(f"{'Створюю' if APPLY else 'План'} колекцій: {len(plan)}")
    for i in plan: print(f"   {i['handle']:<30} {i['title']:<30} img={'image' in i} desc={len(i.get('descriptionHtml', ''))} rules={[r['condition'] for r in i['ruleSet']['rules']]}")
    if not APPLY: return
    for i in plan:
        r = shop.gql("mutation($i: CollectionInput!) { collectionCreate(input: $i) { collection { id handle productsCount { count } } userErrors { field message } } }", {"i": i})["collectionCreate"]
        print("  ", i["handle"], r["userErrors"] or f"ok, товарів {r['collection']['productsCount']['count']}")
        time.sleep(0.3)

# ─── home page ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# the English slides of obiimy.world/en (14.11.2026, in the site's order) → Shopify collection links
SLIDES_ALL = [
    ("solo", "https://obiimy.world/content/images/83/3840x1152e90nn0/16051776076908.webp", "Banner for the New “Solo” Collection", "/collections/solo-a-journey-within"),
    ("scarf-2d", "https://obiimy.world/content/images/72/3840x1152e90nn0/34319627016884.webp", "OBIIMY silk scarves styled in vibrant summer looks", "/collections/scarf-2d"),
    ("pocket-squares", "https://obiimy.world/content/images/82/3840x1152e90nn0/65885772544119.webp", "OBIIMY silk scarf gift sets in premium gift boxes for women and men", "/collections/double-sided-pocket-squares"),
    ("sale", "https://obiimy.world/content/images/61/3840x1152e90nn0/44778058390637.webp", "OBIIMY silk scarves with signature prints — up to 40% off", "/collections/sale"),
    ("scarf", "https://obiimy.world/content/images/4/3840x1152e90nn0/58535784169352.webp", "Main banner “Discounts for Spring Holidays”", "/collections/scarf"),
    ("looks", "https://obiimy.world/content/images/24/3840x1152e90nn0/14304544663502.webp", "OBIIMY silk scarves styled in elegant women’s looks", "/collections/scarf-2d"),
    ("gifts", "https://obiimy.world/content/images/34/3840x1152e90nn0/60699970300428.webp", "OBIIMY gift sets", "/collections/gift-sets"),
    ("singing-soul", "https://obiimy.world/content/images/16/3840x1152e90nn0/56957966179191.webp", "Collection “The Singing Soul”", "/collections/the-singing-soul"),
]
SLIDES = [s for s in SLIDES_ALL if s[0] in ("solo", "scarf-2d", "sale", "gifts", "singing-soul")]   # Dawn: 5 slides max

def theme_file(name):
    f = shop.gql('query($id: ID!, $n: [String!]!) { theme(id: $id) { files(filenames: $n) { nodes { body { ... on OnlineStoreThemeFileBodyText { content } } } } } }', {"id": THEME, "n": [name]})
    return f["theme"]["files"]["nodes"][0]["body"]["content"]

def cmd_home():
    raw = theme_file("templates/index.json"); head = re.match(r"^\s*/\*.*?\*/\s*", raw, re.S); head = head.group(0) if head else ""
    j = json.loads(raw[len(head):])
    have = {c["handle"] for c in shop.gql("{ collections(first: 100) { nodes { handle } } }")["collections"]["nodes"]}
    missing = [l.split("/")[-1] for _, _, _, l in SLIDES if l.split("/")[-1] not in have] + [CATS[c][1] for c in PRINTS if CATS[c][1] not in have]
    if missing: sys.exit(f"спершу створіть колекції: {sorted(set(missing))}")
    print(f"{'Збираю' if APPLY else 'План'} головної: {len(SLIDES)} слайдів у slideshow замість image_banner, список «Collections» з {len(PRINTS)} колекцій; порядок зараз: {j['order']}")
    if not APPLY: return
    # 1. the slides → Files (fileCreate from the site's URLs, once; on re-runs the files are found by name); the names are what the theme setting references
    want = {f"home-slide-{i + 1}-{key}.webp": (url, alt) for i, (key, url, alt, _) in enumerate(SLIDES_ALL)}
    have = {}
    for f in shop.gql('{ files(first: 50, query: "filename:home-slide") { nodes { id fileStatus ... on MediaImage { image { url } } } } }')["files"]["nodes"]:
        if f.get("image"): have[f["image"]["url"].split("?")[0].split("/")[-1]] = f
    todo = [{"originalSource": url, "contentType": "IMAGE", "alt": alt, "filename": n} for n, (url, alt) in want.items() if n not in have]
    if todo:
        r = shop.gql("mutation($f: [FileCreateInput!]!) { fileCreate(files: $f) { files { id } userErrors { field message } } }", {"f": todo})["fileCreate"]
        if r["userErrors"]: sys.exit(f"fileCreate: {r['userErrors']}")
        ids = [f["id"] for f in r["files"]]
        for _ in range(30):
            st = shop.gql("query($ids: [ID!]!) { nodes(ids: $ids) { ... on MediaImage { id fileStatus image { url } } } }", {"ids": ids})["nodes"]
            if all(x and x["fileStatus"] == "READY" and x.get("image") for x in st): break
            time.sleep(2)
        for x in st: have[x["image"]["url"].split("?")[0].split("/")[-1]] = x
    names = []
    for i, (key, url, alt, _) in enumerate(SLIDES_ALL):
        if key in [k for k, *_ in SLIDES]:
            n = f"home-slide-{i + 1}-{key}.webp"
            if n not in have: sys.exit(f"файл {n} не знайдено у Files: {sorted(have)}")
            names.append(n)
    print("  файли:", names)
    # 2. templates/index.json: slideshow instead of image_banner, a «Collections» list after Sale
    blocks = {}; order = []
    for i, ((key, url, alt, link), name) in enumerate(zip(SLIDES, names)):
        bid = f"slide_{i + 1}"; order.append(bid)
        blocks[bid] = {"type": "slide", "settings": {"image": f"shopify://shop_images/{name}", "image_overlay_opacity": 0, "heading": "", "heading_size": "h1", "subheading": "", "button_label": "",
                                                     "link": link, "button_style_secondary": False, "show_text_box": False, "box_align": "middle-center", "text_alignment": "center", "text_alignment_mobile": "center", "color_scheme": "scheme-1"}}
    j["sections"]["slideshow_home"] = {"type": "slideshow", "blocks": blocks, "block_order": order,
                                      "settings": {"layout": "full_bleed", "slide_height": "adapt_image", "slider_visual": "dots", "auto_rotate": True, "change_slides_speed": 5, "image_behavior": "none", "show_text_below": False, "accessibility_info": "Slideshow about our brand"}}
    cb = {f"col_{i + 1}": {"type": "featured_collection", "settings": {"collection": CATS[c][1]}} for i, c in enumerate(PRINTS)}
    j["sections"]["collection_list_prints"] = {"type": "collection-list", "blocks": cb, "block_order": list(cb), "settings": {"title": "Collections", "heading_size": "h2", "image_ratio": "square", "columns_desktop": 5, "color_scheme": "scheme-1", "show_view_all": True, "columns_mobile": "2", "swipe_on_mobile": True, "padding_top": 36, "padding_bottom": 36}}
    # categories list: add the new categories after the existing eight
    for sid, s in j["sections"].items():
        if s["type"] == "collection-list" and sid != "collection_list_prints":
            for h in ("jewelry", "obiimy-home"):
                if not any(b["settings"].get("collection") == h for b in s["blocks"].values()):
                    s["blocks"][f"featured_collection_{h.replace('-', '_')}"] = {"type": "featured_collection", "settings": {"collection": h}}; s["block_order"].append(f"featured_collection_{h.replace('-', '_')}")
    new_order = [x for x in j["order"] if x != "image_banner"]
    new_order.insert(0, "slideshow_home"); new_order.insert(new_order.index("featured_collection_QNLK4h") + 1 if "featured_collection_QNLK4h" in new_order else 1, "collection_list_prints")
    j["order"] = new_order; j["sections"].pop("image_banner", None)
    body = head + json.dumps(j, ensure_ascii=False, indent=2)
    r = shop.gql("mutation($id: ID!, $f: [OnlineStoreThemeFilesUpsertFileInput!]!) { themeFilesUpsert(themeId: $id, files: $f) { upsertedThemeFiles { filename } userErrors { field message } } }",
                 {"id": THEME, "f": [{"filename": "templates/index.json", "body": {"type": "TEXT", "value": body}}]})["themeFilesUpsert"]
    print("  index.json:", r["userErrors"] or "ok", "| порядок:", j["order"])

# ─── menus ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def cmd_menus():
    cols = {c["handle"]: c["id"] for c in shop.gql("{ collections(first: 100) { nodes { id handle } } }")["collections"]["nodes"]}
    menus = shop.gql("{ menus(first: 10) { nodes { id handle title items { id title url type resourceId items { id title url type resourceId items { id title url type resourceId } } } } } }")["menus"]["nodes"]
    def item(title, handle): return {"title": title, "type": "COLLECTION", "resourceId": cols[handle], "url": f"/collections/{handle}"}
    def strip(i): return {k: v for k, v in {"id": i.get("id"), "title": i["title"], "type": i["type"], "url": i["url"], "resourceId": i.get("resourceId"), "items": [strip(x) for x in i.get("items") or []]}.items() if v is not None}
    plan = []
    for m in menus:
        items = [strip(i) for i in m["items"]]
        if m["handle"] == "main-menu":
            if not any(i["title"] == "Collections" for i in items):
                items.insert(1, {"title": "Collections", "type": "COLLECTION", "resourceId": cols["collections"], "url": "/collections/collections", "items": [item(CATS[c][2], CATS[c][1]) for c in PRINTS]})
            cat = next(i for i in items if i["title"] == "Catalog")
            for h, t in (("pocket-square", "Pocket square"), ("jewelry", "Jewelry"), ("obiimy-home", "Obiimy HOME")):
                if not any(x["url"].endswith("/" + h) for x in cat["items"]): cat["items"].append(item(t, h))
            for x in cat["items"]:
                if x["url"].endswith("/pocket-square") and not x.get("items"): x["items"] = [item("Double-Sided Pocket Squares", "double-sided-pocket-squares"), item("Single-Sided Pocket Squares", "single-sided-pocket-squares")]
                if x["url"].endswith("/obiimy-home") and not x.get("items"): x["items"] = [item("Shirts", "shirts"), item("Pajamas", "pajamas"), item("T-shirts", "t-shirts"), item("Sleep Accessories", "sleep-accessories")]
        elif m["handle"] == "footercatalog":
            for h, t in (("jewelry", "Jewelry"), ("obiimy-home", "Obiimy HOME"), ("collections", "Collections")):
                if not any(x["url"].endswith("/" + h) for x in items): items.append(item(t, h))
        else: continue
        plan.append((m, items))
    print(f"{'Оновлюю' if APPLY else 'План'} меню: {[m['handle'] for m, _ in plan]}")
    for m, items in plan:
        for i in items: print(f"   {m['handle']}: {i['title']} → {[x['title'] for x in i.get('items', [])]}")
    if not APPLY: return
    for m, items in plan:
        r = shop.gql("mutation($id: ID!, $t: String!, $h: String!, $items: [MenuItemUpdateInput!]!) { menuUpdate(id: $id, title: $t, handle: $h, items: $items) { userErrors { field message } } }",
                     {"id": m["id"], "t": m["title"], "h": m["handle"], "items": items})["menuUpdate"]
        print("  ", m["handle"], r["userErrors"] or "ok")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    {"tags": cmd_tags, "collections": cmd_collections, "home": cmd_home, "menus": cmd_menus}.get(cmd, lambda: print(__doc__))()
