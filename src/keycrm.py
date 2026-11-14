#!/usr/bin/env python3
"""KeyCRM Open API for the Edem landing (edem.obiimy.world): the landing's order becomes an order in KeyCRM, the WayForPay
result becomes its payment. Used by src/deck-editor.py (server side, so the API key never reaches the browser) and as a CLI.

Spec: https://docs.keycrm.app/ (api.yaml, OAS 3.0, server https://openapi.keycrm.app/v1, Bearer key, 20 requests/minute).
Settings — environment only (locally ~/.config/obiimy/keycrm.env, on Railway the variables of the deck-editor service):
  KEYCRM_API_KEY              the key from KeyCRM → Налаштування → Основні → API (never print, never commit)
  KEYCRM_SOURCE_ID            id of the source «лендинг» created in Налаштування → Джерела (list: python3 src/keycrm.py refs)
  KEYCRM_SKU                  артикул of the scarf in the KeyCRM catalogue — with it the order line is matched to the product
  KEYCRM_PAYMENT_METHOD_ID    id of the payment method for card payments (or KEYCRM_PAYMENT_METHOD — its exact name; default «WayForPay»)
  KEYCRM_DELIVERY_SERVICE_ID  id of Нова Пошта among the delivery services (optional; the city and branch go as text anyway)

CLI:  python3 src/keycrm.py refs                 sources, payment methods, delivery services, statuses — with ids
      python3 src/keycrm.py product <sku>        the catalogue offer (variant) behind an артикул
      python3 src/keycrm.py order <EDEM-ref>     the KeyCRM order created for a landing order (by source_uuid)
      python3 src/keycrm.py push <EDEM-ref>      (re)send a landing order from data/edem/orders.jsonl — skipped if it is already there
      python3 src/keycrm.py payload <EDEM-ref>   print the JSON that would be sent, nothing is sent
"""
import json, os, pathlib, sys, time, urllib.error, urllib.parse, urllib.request

API = os.environ.get("KEYCRM_API_URL") or "https://openapi.keycrm.app/v1"   # the override is for local tests against a mock
KEY = os.environ.get("KEYCRM_API_KEY") or ""
SOURCE_ID = int(os.environ.get("KEYCRM_SOURCE_ID") or 0)
SKU = os.environ.get("KEYCRM_SKU") or ""
PAYMENT_METHOD = os.environ.get("KEYCRM_PAYMENT_METHOD") or "WayForPay"
PAYMENT_METHOD_ID = int(os.environ.get("KEYCRM_PAYMENT_METHOD_ID") or 0)   # preferred over the name when set (ids: python3 src/keycrm.py refs)
DELIVERY_SERVICE_ID = int(os.environ.get("KEYCRM_DELIVERY_SERVICE_ID") or 0)
ROOT = pathlib.Path(__file__).resolve().parent.parent
EDEM_DIR = ROOT / "data" / "edem"
LOG = EDEM_DIR / "keycrm.jsonl"          # one line per attempt: {at, ref, step, ok, id|error}

def configured(): return bool(KEY and SOURCE_ID)

class KeyCRMError(Exception): pass

def api(method, path, body=None, params=None):
    """One call: JSON in, JSON out; HTTP errors carry KeyCRM's message (validation errors list the fields)."""
    if not KEY: raise KeyCRMError("KEYCRM_API_KEY не задано.")
    url = API + path + (("?" + urllib.parse.urlencode(params, doseq=True)) if params else "")
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Authorization": f"Bearer {KEY}", "Accept": "application/json",
                                 "Content-Type": "application/json", "User-Agent": "obiimy-edem/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r: raw = r.read()
    except urllib.error.HTTPError as e:
        raw = e.read()[:2000].decode("utf-8", "replace")
        raise KeyCRMError(f"HTTP {e.code} {method} {path}: {raw}")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise KeyCRMError(f"{method} {path}: {e}")
    return json.loads(raw) if raw.strip() else {}

def _log(ref, step, **kw):
    EDEM_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f: f.write(json.dumps(dict(at=time.strftime("%Y-%m-%dT%H:%M:%S"), ref=ref, step=step, **kw), ensure_ascii=False) + "\n")
    sys.stderr.write(f"{time.strftime('%H:%M:%S')}  keycrm {step} {ref} {json.dumps(kw, ensure_ascii=False)[:200]}\n")

def _utm(page):
    """utm_* from the landing URL the form reported (location.href) → KeyCRM's `marketing`."""
    try: q = urllib.parse.parse_qs(urllib.parse.urlsplit(page or "").query)
    except ValueError: return {}
    return {k: q[k][0][:200] for k in ("utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content") if q.get(k)}

def _phone(p):
    """+380… when the visitor typed a Ukrainian number without the plus or the country code."""
    d = "".join(ch for ch in str(p) if ch.isdigit())
    if len(d) == 10 and d.startswith("0"): d = "38" + d
    return ("+" + d) if len(d) >= 11 else str(p).strip()

def order_payload(rec, price):
    """A landing order record (data/edem/orders.jsonl) → POST /order body. `price` is the server's unit price (EDEM_PRICE)."""
    qty = max(1, int(rec.get("qty") or 1))
    product = {"price": price, "quantity": qty, "name": rec.get("product") or PRODUCT_NAME}
    if SKU: product["sku"] = SKU              # matched to the catalogue by артикул — name, picture, stock come from there
    shipping = {"shipping_service": "Нова Пошта", "shipping_address_country": "Україна", "shipping_address_city": rec.get("city") or "",
                "shipping_receive_point": rec.get("branch") or "", "recipient_full_name": rec.get("name") or "", "recipient_phone": _phone(rec.get("phone") or "")}
    if DELIVERY_SERVICE_ID: shipping["delivery_service_id"] = DELIVERY_SERVICE_ID
    body = {"source_id": SOURCE_ID, "source_uuid": rec.get("ref") or "",
            "ordered_at": rec.get("at", "").replace("T", " ")[:19] or None,
            "buyer": {"full_name": rec.get("name") or "", "phone": _phone(rec.get("phone") or ""), "email": rec.get("email") or ""},
            "buyer_comment": rec.get("comment") or "",
            "manager_comment": f"Лендинг {('edem.obiimy.world/en' if rec.get('lang') == 'en' else 'edem.obiimy.world')} · № {rec.get('ref', '')}" + (" · оплата карткою WayForPay" if rec.get("pay") == "wayforpay" else ""),
            "shipping": {k: v for k, v in shipping.items() if v},
            "products": [product]}
    utm = _utm(rec.get("page"))
    if utm: body["marketing"] = utm
    if not body["buyer"]["email"]: del body["buyer"]["email"]      # KeyCRM validates the e-mail; an empty one would fail
    return {k: v for k, v in body.items() if v not in ("", None)}

PRODUCT_NAME = "Хустка KRAЇNA EDEM × OBIIMY «Trypillia — The Art of Origins», 88 × 88 см"

def find_order(ref):
    """The KeyCRM order whose source_uuid is our reference, or None."""
    res = api("GET", "/order", params={"filter[source_uuid]": ref, "limit": 5})
    rows = [r for r in (res.get("data") or []) if r.get("source_uuid") == ref]
    return rows[0] if rows else None

def local_order_id(ref):
    """The KeyCRM id recorded for a reference in data/edem/keycrm.jsonl, or 0."""
    if not LOG.exists(): return 0
    ids = [json.loads(l).get("id") for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip() and f'"ref": "{ref}"' in l and '"step": "order"' in l]
    ids = [i for i in ids if i]
    return int(ids[-1]) if ids else 0

def push_order(rec, price):
    """Create the order in KeyCRM once: an existing order with the same source_uuid is reused. Returns the KeyCRM id or 0."""
    ref = rec.get("ref") or ""
    try:
        found = find_order(ref) if ref else None
        if found: _log(ref, "order", ok=True, id=found["id"], existed=True); return int(found["id"])
        res = api("POST", "/order", order_payload(rec, price))
        _log(ref, "order", ok=True, id=res.get("id")); return int(res.get("id") or 0)
    except KeyCRMError as e:
        _log(ref, "order", ok=False, error=str(e)[:600]); return 0

def add_payment(ref, amount, status="paid", description="", method=None):
    """A payment line on the KeyCRM order of a reference (POST /order/{id}/payment). Returns True when it landed."""
    try:
        oid = local_order_id(ref) or (lambda o: int(o["id"]) if o else 0)(find_order(ref))
        if not oid: _log(ref, "payment", ok=False, error="замовлення в KeyCRM не знайдено"); return False
        body = {"amount": amount, "status": status, "description": description[:250],
                **({"payment_method_id": PAYMENT_METHOD_ID} if PAYMENT_METHOD_ID and not method else {"payment_method": method or PAYMENT_METHOD}),
                "payment_date": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}
        res = api("POST", f"/order/{oid}/payment", body)
        _log(ref, "payment", ok=True, id=oid, payment_id=res.get("id"), status=status, amount=amount); return True
    except KeyCRMError as e:
        _log(ref, "payment", ok=False, error=str(e)[:600]); return False

# ─── CLI ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def _rows(name):
    f = EDEM_DIR / name
    return [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()] if f.exists() else []

def _landing_order(ref):
    rows = [r for r in _rows("orders.jsonl") + _rows("registrations.jsonl") if r.get("ref") == ref]
    if not rows: sys.exit(f"немає замовлення {ref} у data/edem")
    return rows[-1]

def main(argv):
    cmd = argv[1] if len(argv) > 1 else "help"
    price = int(os.environ.get("EDEM_PRICE") or 8500)
    if cmd == "refs":
        for title, path in (("Джерела", "/order/source"), ("Методи оплати", "/order/payment-method"), ("Служби доставки", "/order/delivery-service"), ("Статуси", "/order/status")):
            res = api("GET", path, params={"limit": 50}); rows = res.get("data") if isinstance(res, dict) else res
            print(f"\n{title}:")
            for r in rows or []: print(f"  {r.get('id'):>4}  {r.get('name')}" + (f"  ({r.get('alias')})" if r.get("alias") else "") + ("" if r.get("is_active", True) else "  [неактивний]"))
    elif cmd == "product":
        res = api("GET", "/offers", params={"filter[sku]": argv[2], "limit": 5, "include": "product"})   # /products has no sku filter; offers (variants) do
        print(json.dumps(res.get("data"), ensure_ascii=False, indent=1)[:4000])
    elif cmd == "order":
        print(json.dumps(find_order(argv[2]), ensure_ascii=False, indent=1))
    elif cmd == "payload":
        print(json.dumps(order_payload(_landing_order(argv[2]), price), ensure_ascii=False, indent=1))
    elif cmd == "push":
        print("KeyCRM id:", push_order(_landing_order(argv[2]), price))
    else:
        print(__doc__)
    return 0

if __name__ == "__main__":
    try: sys.exit(main(sys.argv))
    except KeyCRMError as e: sys.exit(f"KeyCRM: {e}")
