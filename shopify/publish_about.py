"""Publish the new «About us» to shop.obiimy.world: back up the current page body, upload the photographs to the store's
Files (staged uploads → fileCreate), rebuild the body with the CDN URLs (build_about.py --cdn) and update the page.
Usage: python3 shopify/publish_about.py"""
import json, pathlib, subprocess, sys, time, urllib.request, mimetypes
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(HERE)); import shop
sys.path.insert(0, str(HERE))
PAGE_ID = "gid://shopify/Page/131028844765"

# 1 · backup
cur = shop.gql("query($id:ID!){ page(id:$id){ id title handle body } }", {"id": PAGE_ID})["page"]
(HERE / "backup" / f"about-us-{time.strftime('%Y%m%d-%H%M')}.json").write_text(json.dumps(cur, ensure_ascii=False, indent=1))
print("backup:", len(cur["body"]), "chars")

# 2 · photographs → Files (resized to ≤ 2000 px, JPEG)
from PIL import Image
import importlib.util
spec = importlib.util.spec_from_file_location("ba", HERE / "build_about.py");
src_pics = {}
for line in (HERE / "build_about.py").read_text().splitlines():
    pass
exec_ns = {"__file__": str(HERE / "build_about.py")}
code = (HERE / "build_about.py").read_text().split("cdn = {}")[0]
exec(code, exec_ns); PICS = exec_ns["PICS"]
tmp = HERE / "tmp"; tmp.mkdir(exist_ok=True)
cdn_file = HERE / "about-cdn.json"
cdn = json.loads(cdn_file.read_text()) if cdn_file.exists() else {}
for key, (rel, alt) in PICS.items():
    if key in cdn: continue
    f = ROOT / rel; out = tmp / f"about-{key}.jpg"
    im = Image.open(f).convert("RGB"); im.thumbnail((2000, 2000)); im.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    data = out.read_bytes()
    st = shop.gql("""mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ field message } } }""",
                  {"input": [{"resource": "IMAGE", "filename": out.name, "mimeType": "image/jpeg", "fileSize": str(len(data)), "httpMethod": "POST"}]})["stagedUploadsCreate"]
    if st["userErrors"]: sys.exit(st["userErrors"])
    t = st["stagedTargets"][0]
    boundary = "----obiimy" + str(int(time.time()))
    body = b""
    for p in t["parameters"]:
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n{p['value']}\r\n".encode()
    body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{out.name}\"\r\nContent-Type: image/jpeg\r\n\r\n".encode() + data + f"\r\n--{boundary}--\r\n".encode()
    r = urllib.request.urlopen(urllib.request.Request(t["url"], data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}), timeout=120)
    assert r.status in (200, 201, 204), r.status
    fc = shop.gql("""mutation($files:[FileCreateInput!]!){ fileCreate(files:$files){ files{ id alt ... on MediaImage { image { url } } } userErrors{ field message } } }""",
                  {"files": [{"alt": alt, "contentType": "IMAGE", "originalSource": t["resourceUrl"]}]})["fileCreate"]
    if fc["userErrors"]: sys.exit(fc["userErrors"])
    fid = fc["files"][0]["id"]; url = None
    for _ in range(20):      # the image is processed asynchronously: poll until the URL is ready
        q = shop.gql("query($id:ID!){ node(id:$id){ ... on MediaImage { fileStatus image { url } } } }", {"id": fid})["node"]
        if q and q.get("image") and q["image"].get("url"): url = q["image"]["url"]; break
        time.sleep(2)
    if not url: sys.exit(f"no url for {key}")
    cdn[key] = url; cdn_file.write_text(json.dumps(cdn, indent=1)); print("uploaded", key, url.split("/")[-1].split("?")[0])

# 3 · the body with CDN urls, then the page
subprocess.run([sys.executable, str(HERE / "build_about.py"), "--cdn", str(cdn_file)], check=True)
body = (HERE / "about-us.html").read_text()
r = shop.gql("""mutation($id:ID!,$page:PageUpdateInput!){ pageUpdate(id:$id, page:$page){ page{ id handle updatedAt } userErrors{ field message } } }""",
             {"id": PAGE_ID, "page": {"body": body, "title": "About Us"}})["pageUpdate"]
if r["userErrors"]: sys.exit(r["userErrors"])
print("published:", r["page"])
