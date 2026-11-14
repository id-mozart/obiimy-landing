"""Minimal Shopify Admin API client: client-credentials token (cached 23h) + GraphQL."""
import json, os, time, urllib.parse, urllib.request, pathlib

ENV = pathlib.Path.home() / ".config/obiimy/shopify.env"
CACHE = pathlib.Path.home() / ".config/obiimy/.token.json"
API = "2026-07"

def _env():
    """SHOPIFY_SHOP / SHOPIFY_CLIENT_ID / SHOPIFY_CLIENT_SECRET — from ~/.config/obiimy/shopify.env locally, from the environment on Railway."""
    e = {k: v for k, v in os.environ.items() if k.startswith("SHOPIFY_")}
    if ENV.exists(): e.update(dict(l.split("=", 1) for l in ENV.read_text().split() if "=" in l))
    return e

def _cache_path():
    for c in (CACHE, pathlib.Path(__file__).resolve().parent.parent / "data" / ".shopify-token.json"):
        try: c.parent.mkdir(parents=True, exist_ok=True); return c
        except OSError: continue
    return CACHE

def token():
    cache = _cache_path()
    if cache.exists():
        c = json.loads(cache.read_text())
        if c["exp"] > time.time() + 300: return c["token"], c.get("scope", "")
    e = _env()
    body = urllib.parse.urlencode({"grant_type": "client_credentials", "client_id": e["SHOPIFY_CLIENT_ID"], "client_secret": e["SHOPIFY_CLIENT_SECRET"]}).encode()
    r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://{e['SHOPIFY_SHOP']}/admin/oauth/access_token", data=body, headers={"Content-Type": "application/x-www-form-urlencoded"}), timeout=30))
    old = os.umask(0o077)
    cache.write_text(json.dumps({"token": r["access_token"], "scope": r.get("scope", ""), "exp": time.time() + int(r.get("expires_in", 86399))}))
    os.umask(old)
    return r["access_token"], r.get("scope", "")

def gql(query, variables=None):
    t, _ = token(); shop = _env()["SHOPIFY_SHOP"]
    req = urllib.request.Request(f"https://{shop}/admin/api/{API}/graphql.json", data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 headers={"Content-Type": "application/json", "X-Shopify-Access-Token": t})
    r = json.load(urllib.request.urlopen(req, timeout=60))
    if r.get("errors"): raise RuntimeError(json.dumps(r["errors"], ensure_ascii=False)[:2000])
    return r["data"]
