#!/usr/bin/env python3
"""WYSIWYG editor for the print deck: the same HTML and CSS that headless Chrome prints to PDF, opened in a browser for editing.

    python3 src/deck-editor.py        →  http://127.0.0.1:8770/

Reads   review/deck-editor-pages.json and review/deck-editor.css (written by every build of the deck).
Writes  src/deck-edits.json (applied by the build, see apply_edits in src/build-team-pdf.py), img/edit/ (pictures re-framed in the editor),
        photo/user/ (uploaded pictures), review/lb/thumbs/ (thumbnail cache). On «save» it runs the builder and reports the layout check.
Env     DECK_EDITS — the edits file; DECK_EDITOR_BUILDER — the command to run on save; DECK_EDITOR_PAGES — the pages file (tests);
        DECK_EDITOR_PUBLISH — the command «Опубликовать» runs instead of site build + git + railway (tests); DECK_EDITOR_PUBLISH_URL — the
        live PDF to check after publishing; DECK_EDITOR_PORT — the port (8770).
The page itself (HTML, CSS, JS) is src/deck-editor.html."""
import hashlib, io, json, os, pathlib, re, shlex, shutil, subprocess, sys, tempfile, threading, time, urllib.parse, urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from PIL import Image, ImageChops, ImageOps, ImageStat

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("DECK_EDITOR_PORT") or 8770)
EDITS = pathlib.Path(os.environ.get("DECK_EDITS") or ROOT / "src" / "deck-edits.json")
PAGES = pathlib.Path(os.environ.get("DECK_EDITOR_PAGES") or ROOT / "review" / "deck-editor-pages.json")
CSS = ROOT / "review" / "deck-editor.css"
UI = pathlib.Path(__file__).resolve().with_name("deck-editor.html")
PDF = "obiimy-podarunky-dlia-komandy.pdf"
EDIT_DIR, USER_DIR, THUMBS = ROOT / "img" / "edit", ROOT / "photo" / "user", ROOT / "review" / "lb" / "thumbs"
CROPS = EDIT_DIR / "crops.json"          # which original and which part of it every re-framed picture shows — to continue framing later
LIBRARY = [("photo/user", "Мои"), ("photo/solo", "SOLO"), ("photo/site", "Сайт"), ("photo/ways", "Как носить"),
           ("img/cut", "Вырезанные"), ("img/p3", "Готовые кадры"), ("img/edit", "Кадры редактора")]
PICS = {".jpg", ".jpeg", ".png", ".webp"}
PPI = 200
BUILD_TIMEOUT = 15 * 60
BUILD = {"lock": threading.Lock(), "running": False, "started": 0.0, "lines": []}      # the lock covers a build and a publication alike
LIVE_PDF = os.environ.get("DECK_EDITOR_PUBLISH_URL") or "https://obiimy-landing-production.up.railway.app/" + PDF
PUBLISH = {"running": False, "started": 0.0, "steps": [], "result": None}
PID_OK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,60}$")
NAMES = {"who": "Кто мы", "p3-now": "Стр. 3 · таблица (сейчас)", "gift-twilly": "Подарок 01 · Твилли", "gift-ring": "Подарок 02 · Платок и кольцо",
         "gift-mask": "Подарок 03 · Маска и резинка", "gift-set": "Подарок 04 · Платок и твилли", "logo": "Ваш логотип", "ways-twilly": "Как носить твилли",
         "ways-scarf": "Как носить платок", "range": "Ассортимент", "solo": "SOLO", "prints": "Семь принтов", "terms": "Условия", "contacts": "Контакты"}

def page_name(pid):
    """A readable name for the rail and the dialogs; a copy made in the editor is «… (копия)», an unknown pid stays as it is."""
    m = re.match(r"^(.*?)-copy(\d*)$", pid)
    if m: return page_name(m.group(1)) + " (копия" + (" " + m.group(2) if m.group(2) else "") + ")"
    if pid in NAMES: return NAMES[pid]
    m = re.match(r"^cover-([A-Z])$", pid)
    if m: return "Обложка " + m.group(1)
    m = re.match(r"^p3-([A-Z])$", pid)
    if m: return "Стр. 3 · вариант " + m.group(1)
    return pid
FILES = threading.Lock()                 # the edits file and the crops index are rewritten under it


class Problem(Exception):
    """An error to show to the person in the editor (the text is Russian, like the rest of its interface)."""
    def __init__(self, text, status=400):
        super().__init__(text); self.status = status


# ---------- files ----------

def safe_path(rel):
    """A project file for a URL path or a request parameter, or None: inside the root, no dot-files, no links leading out of it."""
    parts = [p for p in urllib.parse.unquote(str(rel)).replace("\\", "/").split("/") if p not in ("", ".")]
    if not parts or any(p == ".." or p.startswith(".") or "\x00" in p for p in parts): return None
    p = ROOT.joinpath(*parts).resolve()
    try: p.relative_to(ROOT)
    except ValueError: return None
    return p

def rel(p): return p.relative_to(ROOT).as_posix()

def picture(name):
    p = safe_path(name or "")
    if not p or not p.is_file() or p.suffix.lower() not in PICS: raise Problem(f"Картинка не найдена: {name}", 404)
    return p

def write_atomic(path, data):
    """The file appears whole or not at all: a build running at the same moment must never read half of it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data if isinstance(data, bytes) else data.encode("utf-8")); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp): os.unlink(tmp)
        raise

def read_json(path, default):
    if not path.exists(): return default
    return json.loads(path.read_text(encoding="utf-8"))


# ---------- the deck ----------

def load_pages():
    if not PAGES.exists(): raise Problem("Нет файла со страницами (review/deck-editor-pages.json). Сначала соберите PDF: python3 src/build-deck-variants.py", 500)
    for attempt in range(8):                 # a build may be rewriting the file at this very moment
        try: return read_json(PAGES, {})
        except ValueError: time.sleep(0.4)
    raise Problem("Файл со страницами сейчас переписывается сборкой — попробуйте через несколько секунд.", 503)

def load_edits():
    try: ed = read_json(EDITS, {})
    except ValueError: raise Problem(f"Файл правок {EDITS.name} повреждён (это не JSON). Ничего не записано — посмотрите файл.", 500)
    if not isinstance(ed, dict): raise Problem(f"Файл правок {EDITS.name} имеет неожиданный вид. Ничего не записано.", 500)
    return ed

def pdf_info():
    p = ROOT / PDF
    return dict(pdf="/" + PDF, pdf_mb=round(p.stat().st_size / 1048576, 1), pdf_time=int(p.stat().st_mtime)) if p.exists() else dict(pdf=None, pdf_mb=None, pdf_time=None)

def api_pages():
    d = load_pages(); ed = load_edits() if EDITS.exists() else {}
    with FILES: crops = read_json(CROPS, {}) if CROPS.exists() else {}
    return dict(d, css=CSS.read_text(encoding="utf-8") if CSS.exists() else "", has_order=bool(ed.get("order")), crops=crops,
                names={p["pid"]: page_name(p["pid"]) for p in d.get("pages", [])}, building=BUILD["running"], publishing=PUBLISH["running"],
                live_pdf=LIVE_PDF, **pdf_info())

def layout_report(lines):
    """What the builder said about the layout: ("clean" | "issues" | "unknown", [issue, …]).
    It prints either «layout: clean» or «LAYOUT ISSUES:» followed by one issue per line («p3 over folio: …»)."""
    state, issues = "unknown", []
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s == "layout: clean": state, issues = "clean", []
        elif s.startswith("LAYOUT ISSUES:"):
            state, issues = "issues", ([s[14:].strip()] if s[14:].strip() else [])
            rest = [x.strip() for x in lines[i + 1:]]
            numbered = bool(rest) and re.match(r"p\d+\b", rest[0]) is not None
            for t in rest:
                if not t or (numbered and not re.match(r"p\d+\b", t)) or re.match(r"(size|QR|pages|edits|layout)\b[^:]*:", t): break
                issues.append(t)
    return state, issues

def builder_command(pages):
    if os.environ.get("DECK_EDITOR_BUILDER"): return shlex.split(os.environ["DECK_EDITOR_BUILDER"])
    b = safe_path(pages.get("builder") or "")
    if not b or not b.is_file() or b.suffix != ".py": raise Problem("В файле страниц не указан сборщик (builder).", 500)
    return [sys.executable, str(b)]

def run_builder(cmd):
    """Runs the build in the project root; the output is collected line by line so the editor can show progress."""
    BUILD.update(running=True, started=time.time(), lines=[])
    try:
        p = subprocess.Popen(cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace",
                             env=dict(os.environ, PYTHONUNBUFFERED="1"))
        killed = []
        guard = threading.Timer(BUILD_TIMEOUT, lambda: (killed.append(1), p.kill())); guard.start()
        try:
            for line in p.stdout: BUILD["lines"].append(line.rstrip("\n"))
            code = p.wait()
        finally: guard.cancel()
        return (-9 if killed else code), list(BUILD["lines"])
    finally: BUILD["running"] = False

def api_save(body):
    pages, reset, hidden, order = body.get("pages") or {}, body.get("reset") or [], body.get("hidden"), body.get("order")
    seen = body.get("base") if isinstance(body.get("base"), dict) else {}     # the hashes the editor loaded the pages with
    copies = body.get("copies") if isinstance(body.get("copies"), dict) else {}   # pages made in the editor: new pid → the page it copies
    if not isinstance(pages, dict) or not isinstance(reset, list) or not all(isinstance(v, list) or v is None for v in (hidden, order)):
        raise Problem("Неверный запрос на сохранение.")
    if not BUILD["lock"].acquire(blocking=False): raise Problem("Сборка или публикация уже идёт — дождитесь её окончания.", 409)
    try:
        deck = load_pages(); base = {p["pid"]: p["base"] for p in deck.get("pages", [])}
        with FILES: ed = load_edits(); saved = ed.get("pages") if isinstance(ed.get("pages"), dict) else {}
        known = set(base) | {pid for pid, v in saved.items() if isinstance(v, dict) and v.get("copy_of")}
        for pid, html in pages.items():
            if pid not in known and not (pid in copies and PID_OK.match(pid)): raise Problem(f"Страницы «{pid}» нет в сборке — обновите редактор.")
            if not isinstance(html, str) or not re.match(r"<section\b[^>]*\bdata-pid=\"" + re.escape(pid) + r"\"", html) or not html.rstrip().endswith("</section>"):
                raise Problem(f"Страница «{pid}» пришла в неожиданном виде — не сохраняю.")
        with FILES:
            ed = load_edits(); saved = ed.get("pages") if isinstance(ed.get("pages"), dict) else {}
            for pid, html in pages.items():
                was = saved[pid] if isinstance(saved.get(pid), dict) else {}
                if pid not in base:                    # a duplicate made in the editor has no generated twin: no base, but the page it came from
                    saved[pid] = dict(html=html, base=None, copy_of=was.get("copy_of") or str(copies.get(pid))); continue
                # base = the generated page this edit was made from: the one the editor had open (if the deck was rebuilt meanwhile, the page
                # comes back marked stale); a page saved earlier and not told otherwise keeps its base; else the page as built now
                saved[pid] = dict(html=html, base=seen[pid] if re.fullmatch(r"[0-9a-f]{40}", str(seen.get(pid))) else was.get("base") or base[pid])
            for pid in reset: saved.pop(pid, None)
            ed["pages"] = saved
            known = set(base) | {pid for pid, v in saved.items() if isinstance(v, dict) and v.get("copy_of")}
            if hidden is not None: ed["hidden"] = [pid for pid in dict.fromkeys(hidden) if pid in known]
            if order is not None: ed["order"] = [pid for pid in dict.fromkeys(order) if pid in known]
            ed.setdefault("hidden", []); ed.setdefault("order", [])
            write_atomic(EDITS, json.dumps(ed, ensure_ascii=False, indent=1) + "\n")
        t0 = time.time()
        try: code, lines = run_builder(builder_command(deck))
        except OSError as e: code, lines = -1, [f"{type(e).__name__}: {e}"]
        tail = "\n".join(lines[-40:]); took = round(time.time() - t0)
        if code != 0:
            why = "Сборка не уложилась в 15 минут и остановлена." if code == -9 else f"Сборка PDF завершилась с ошибкой (код {code})."
            return dict(ok=False, saved=True, error=why + " Правки сохранены; PDF остался прежним.", log_tail=tail, seconds=took)
        state, issues = layout_report(lines)
        return dict(ok=True, saved=True, layout=state, issues=issues, log_tail=tail, seconds=took, **pdf_info())
    finally: BUILD["lock"].release()


# ---------- publication: site build, git, railway, a look at the live PDF ----------

def tool(name):
    """A command-line tool by name; railway lives in nvm's bin, which an app launched from the Dock may not have in PATH."""
    found = shutil.which(name)
    if found: return found
    hits = sorted(pathlib.Path.home().glob(".nvm/versions/node/*/bin/" + name)) + [p for p in (pathlib.Path("/opt/homebrew/bin") / name, pathlib.Path("/usr/local/bin") / name) if p.exists()]
    return str(hits[-1]) if hits else name

def publish_steps(message):
    """The deploy as the owner's instructions define it (CLAUDE.md): commit, push, railway up, check the live page. DECK_EDITOR_PUBLISH
    (tests) stands in for everything but the final check."""
    site = ROOT / "site"
    def copy_pdf():
        if not (ROOT / PDF).exists(): raise Problem("Нет собранного PDF — сначала «Сохранить и собрать PDF».")
        site.mkdir(exist_ok=True); shutil.copy2(ROOT / PDF, site / PDF); return [f"{PDF} → site/ ({round((ROOT / PDF).stat().st_size / 1048576, 1)} MB)"]
    if os.environ.get("DECK_EDITOR_PUBLISH"):
        return [("Публикую (тестовая команда)", shlex.split(os.environ["DECK_EDITOR_PUBLISH"]), {})]
    return [("Собираю сайт", [sys.executable, str(ROOT / "build-site.py")], {"env": {"SKIP_THUMBS": "1"}}),
            ("Кладу PDF в site/", copy_pdf, {}),
            ("Сохраняю в git", ["git", "add", "-A"], {}),
            ("Коммит", ["git", "commit", "-m", message], {"nothing_to_commit_ok": True}),
            ("Отправляю на GitHub", ["git", "push"], {}),
            ("Деплой на Railway (5–12 минут)", [tool("railway"), "up", "-y", "-c", "--service", "obiimy-landing"], {"timeout": 25 * 60})]

def run_step(step):
    """Runs one step of the publication, filling its log; raises Problem when it fails."""
    name, what, opt = step; step_log = step_rec(name)
    if callable(what):
        step_log["lines"] += what(); return
    env = dict(os.environ, PYTHONUNBUFFERED="1", **opt.get("env", {}))
    try: p = subprocess.Popen(what, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", env=env)
    except OSError as e: raise Problem(f"Не запускается «{what[0]}»: {e}")
    killed = []; guard = threading.Timer(opt.get("timeout", BUILD_TIMEOUT), lambda: (killed.append(1), p.kill())); guard.start()
    try:
        for line in p.stdout: step_log["lines"].append(line.rstrip("\n")[:300])
        code = p.wait()
    finally: guard.cancel()
    if killed: raise Problem(f"Шаг «{name}» не уложился во время и остановлен.")
    if code != 0:
        if opt.get("nothing_to_commit_ok") and any("nothing to commit" in ln for ln in step_log["lines"]): step_log["note"] = "нечего коммитить — пропускаю"; return
        raise Problem(f"Шаг «{name}» завершился с ошибкой (код {code}).")

def step_rec(name):
    rec = dict(name=name, state="running", started=time.time(), lines=[], seconds=0)
    for r in PUBLISH["steps"]:
        if r["state"] == "running": r["state"] = "done"; r["seconds"] = round(time.time() - r["started"])
    PUBLISH["steps"].append(rec); return rec

def live_size(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "deck-editor", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=30) as r: return int(r.headers.get("Content-Length") or 0)

def check_live(url, want, minutes=12):
    """The live PDF must be the one just built: same size as the local file. Polls for up to 12 minutes."""
    rec = step_rec("Проверяю PDF на сайте"); t0 = time.time(); last = None
    while time.time() - t0 < minutes * 60:
        try: last = live_size(url); rec["lines"] = [f"на сайте {round(last / 1048576, 2)} MB, нужно {round(want / 1048576, 2)} MB"]
        except Exception as e: rec["lines"] = [f"{type(e).__name__}: {str(e)[:120]}"]
        if last == want: rec["lines"].append("совпадает"); return
        time.sleep(15)
    raise Problem(f"За {minutes} минут PDF на сайте так и не обновился (на сайте {round((last or 0) / 1048576, 2)} MB, локально {round(want / 1048576, 2)} MB).")

def publish_job(message):
    PUBLISH.update(running=True, started=time.time(), steps=[], result=None)
    try:
        for step in publish_steps(message): run_step(step)
        check_live(LIVE_PDF, (ROOT / PDF).stat().st_size)
        for r in PUBLISH["steps"]:
            if r["state"] == "running": r["state"] = "done"; r["seconds"] = round(time.time() - r["started"])
        PUBLISH["result"] = dict(ok=True, seconds=round(time.time() - PUBLISH["started"]), url=LIVE_PDF, **pdf_info())
    except Exception as e:
        for r in PUBLISH["steps"]:
            if r["state"] == "running": r["state"] = "failed"; r["seconds"] = round(time.time() - r["started"])
        PUBLISH["result"] = dict(ok=False, error=str(e) if isinstance(e, Problem) else f"{type(e).__name__}: {e}", seconds=round(time.time() - PUBLISH["started"]))
    finally:
        PUBLISH["running"] = False; BUILD["lock"].release()

def api_publish(body):
    message = str(body.get("message") or "").strip().replace("\r", "")[:300] or "Правки из редактора"
    if not BUILD["lock"].acquire(blocking=False): raise Problem("Сборка или публикация уже идёт — дождитесь её окончания.", 409)
    if not (ROOT / PDF).exists(): BUILD["lock"].release(); raise Problem("Нет собранного PDF — сначала «Сохранить и собрать PDF».")
    threading.Thread(target=publish_job, args=(message,), daemon=True).start()
    return dict(ok=True, started=True)

def publish_status():
    steps = [dict(name=r["name"], state=r["state"], seconds=r["seconds"] if r["state"] != "running" else round(time.time() - r["started"]),
                  tail=r["lines"][-6:], note=r.get("note")) for r in PUBLISH["steps"]]
    return dict(running=PUBLISH["running"], seconds=round(time.time() - PUBLISH["started"]) if PUBLISH["started"] else 0, steps=steps, result=PUBLISH["result"])


# ---------- pictures ----------

def open_image(p):
    """The picture as a browser shows it: turned according to the EXIF orientation."""
    return ImageOps.exif_transpose(Image.open(p))

def has_alpha(im):
    if im.mode not in ("RGBA", "LA", "PA") and "transparency" not in im.info: return False
    return im.convert("RGBA").getchannel("A").getextrema()[0] < 255

def master(p):
    """The 2400 px master of a SOLO frame (ads/solo/src/…-2k.webp) when it is the same picture, else the file itself — full-bleed pages need the pixels."""
    k2 = ROOT / "ads" / "solo" / "src" / (p.stem + "-2k.webp")
    if rel(p).startswith("photo/solo/") and k2.is_file():
        try:
            (w, h), (W, H) = open_image(p).size, Image.open(k2).size
            if abs(w / h - W / H) < 0.005 and W > w: return k2
        except OSError: pass
    return p

def _gray(im, box=None, n=40):
    im = im.convert("RGBA"); im = Image.alpha_composite(Image.new("RGBA", im.size, (128, 128, 128, 255)), im).convert("L")
    return im.resize((n, n), Image.BILINEAR, box=box)

def guess_box(orig, cur, crops):
    """Where the pre-cropped copy `cur` sits in its original, as fractions of the original, or None. The editor's own crops are on record;
    the generator's copies in review/lb/ carry the framing in their names (see pic() in src/build-team-pdf.py) — every reading of a name
    is checked against the pixels, so a changed naming scheme costs nothing but the starting position of «Кадр»."""
    if orig == cur: return [0, 0, 1, 1]
    rec = crops.get(rel(cur))
    if rec and rec.get("src") == rel(orig): return rec["box"]
    try: o = open_image(orig); c = open_image(cur)
    except OSError: return None
    (W, H), (w, h) = o.size, c.size
    sizes = [(W, H)]; k2 = master(orig)
    if k2 != orig: sizes.append(Image.open(k2).size)
    cands = []
    m = re.search(r"-\d+x\d+-box(\d+)-(\d+)-(\d+)-(\d+)$", cur.stem)
    if m:
        x0, y0, x1, y1 = map(int, m.groups())
        cands += [(x0 / sw, y0 / sh, x1 / sw, y1 / sh) for sw, sh in sizes if x1 <= sw and y1 <= sh]
    m = re.search(r"-(\d+)x(\d+)-(\d+)-(\d+)-z(\d+)(-2k)?$", cur.stem)
    if m:
        fw, fh, px, py, z = [int(v) for v in m.groups()[:5]]
        cw, ch = (W, W * fh / fw) if W * fh / fw <= H else (H * fw / fh, H)
        cw, ch = cw * 100 / z, ch * 100 / z; x0, y0 = (W - cw) * px / 100, (H - ch) * py / 100
        cands.append((x0 / W, y0 / H, (x0 + cw) / W, (y0 + ch) / H))
    cands.append((0, 0, 1, 1))
    best, target = None, _gray(c)
    for b in cands:
        if not (-0.001 <= b[0] < b[2] <= 1.001 and -0.001 <= b[1] < b[3] <= 1.001): continue
        if abs((b[2] - b[0]) * W / ((b[3] - b[1]) * H) / (w / h) - 1) > 0.03: continue
        d = ImageStat.Stat(ImageChops.difference(_gray(o, (b[0] * W, b[1] * H, b[2] * W, b[3] * H)), target)).mean[0]
        if d < 9 and (best is None or d < best[0]): best = (d, b)
    return [round(min(1, max(0, v)), 5) for v in best[1]] if best else None

def api_picinfo(q):
    """Size and transparency of an original, and where the picture shown now (cur) sits in it — the starting point of «Кадр»."""
    orig = picture(q.get("orig")); cur = safe_path(q.get("cur") or "")
    im = open_image(orig); W, H = im.size
    with FILES: crops = read_json(CROPS, {}) if CROPS.exists() else {}
    box = guess_box(orig, cur, crops) if cur and cur.is_file() and cur.suffix.lower() in PICS else None
    mw = Image.open(master(orig)).size[0]
    return dict(ok=True, w=W, h=H, alpha=has_alpha(im), box=box, px=mw)

def api_crop(body):
    """A part of a picture (box = x0, y0, x1, y1 as fractions of the source) → img/edit/<name>-<hash>.jpg at 200 ppi for a slot w_mm wide.
    Transparent sources stay PNG; for them the box may reach beyond the picture (the margin is transparent)."""
    src = picture(body.get("src"))
    try:
        box = [float(v) for v in body.get("box")]; w_mm = float(body.get("w_mm")); assert len(box) == 4
    except (TypeError, ValueError, AssertionError): raise Problem("Неверные параметры кадра.")
    if not (0 < w_mm <= 600) or any(v != v or abs(v) > 6 for v in box): raise Problem("Неверные параметры кадра.")
    hi = master(src); im = open_image(hi); alpha = has_alpha(im); W, H = im.size
    if not alpha: box = [min(1.0, max(0.0, v)) for v in box]
    if box[2] - box[0] < 0.005 or box[3] - box[1] < 0.005: raise Problem("Кадр слишком мал.")
    px = (round(box[0] * W), round(box[1] * H), round(box[2] * W), round(box[3] * H))
    im = im.convert("RGBA" if alpha else "RGB").crop(px)             # outside the picture an RGBA crop is transparent
    src_px = im.width; tw = max(1, round(w_mm / 25.4 * PPI))
    if im.width > tw: im = im.resize((tw, max(1, round(tw * im.height / im.width))), Image.LANCZOS)
    key = hashlib.sha1("|".join([rel(src), str(hi.stat().st_mtime_ns), ",".join(f"{v:.5f}" for v in box), f"{w_mm:.2f}"]).encode()).hexdigest()[:10]
    stem = re.sub(r"[^A-Za-z0-9_-]+", "-", src.stem).strip("-")[:60] or "pic"
    out = EDIT_DIR / f"{stem}-{key}{'.png' if alpha else '.jpg'}"
    buf = io.BytesIO()
    if alpha: im.save(buf, "PNG", optimize=True)
    else: im.save(buf, "JPEG", quality=84, optimize=True, progressive=True)
    write_atomic(out, buf.getvalue())
    with FILES:
        crops = read_json(CROPS, {}) if CROPS.exists() else {}
        crops[rel(out)] = dict(src=rel(src), box=[round(v, 5) for v in box], w_mm=round(w_mm, 2))
        write_atomic(CROPS, json.dumps(crops, ensure_ascii=False, indent=1) + "\n")
    return dict(ok=True, path=rel(out), w=im.width, h=im.height, ppi=round(src_px / (w_mm / 25.4)), kb=round(len(buf.getvalue()) / 1024))

def api_uncrop(body):
    """Deletes re-framed pictures the editor no longer needs — only files under img/edit/ that are on record in crops.json."""
    paths = body.get("paths") if isinstance(body.get("paths"), list) else []
    gone = []
    with FILES:
        crops = read_json(CROPS, {}) if CROPS.exists() else {}
        for rp in paths:
            p = safe_path(str(rp)) if isinstance(rp, str) else None
            if not p or rel(p) not in crops or not rel(p).startswith("img/edit/") or p.parent != EDIT_DIR: continue
            crops.pop(rel(p), None)
            try: p.unlink(); gone.append(rel(p))
            except OSError: pass
        if CROPS.exists(): write_atomic(CROPS, json.dumps(crops, ensure_ascii=False, indent=1) + "\n")
    return dict(ok=True, deleted=gone)

TRANSLIT = dict(zip("абвгґдеєёжзиіїйклмнопрстуфхцчшщъыьэюя", "a b v g g d e ie e zh z i i i i k l m n o p r s t u f kh ts ch sh shch  y  e iu ia".split(" ")))

def api_upload(name, data):
    """A person's own picture → photo/user/<latin-name>.<ext>. Turned upright if the camera recorded a rotation: PIL crops raw pixels."""
    if not data: raise Problem("Файл пустой.")
    try: im = Image.open(io.BytesIO(data)); im.load()
    except Exception: raise Problem("Этот файл не открывается как картинка. Подходят JPEG, PNG и WebP (HEIC с телефона сначала сохраните как JPEG).")
    ext = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}.get(im.format)
    if not ext or im.getexif().get(0x0112, 1) != 1 or getattr(im, "n_frames", 1) > 1:
        im = ImageOps.exif_transpose(im); alpha = has_alpha(im); buf = io.BytesIO()
        if alpha: im.convert("RGBA").save(buf, "PNG", optimize=True); ext = ".png"
        else: im.convert("RGB").save(buf, "JPEG", quality=92, optimize=True); ext = ".jpg"
        data = buf.getvalue()
    stem = "".join(TRANSLIT.get(ch, ch) for ch in pathlib.PurePath(str(name).replace("\\", "/")).stem.lower())
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")[:60] or "foto"
    n = 1
    while True:
        out = USER_DIR / f"{stem}{'' if n == 1 else '-' + str(n)}{ext}"
        if not out.exists() or out.read_bytes() == data: break
        n += 1
    if not out.exists(): write_atomic(out, data)
    return dict(ok=True, path=rel(out), w=im.width, h=im.height)

def api_library():
    """Pictures a page can take. The resized copies for the site (…-480.webp, …-800.webp, …-1200.webp) are left out when the full one is here."""
    out = []
    for d, title in LIBRARY:
        folder = ROOT / d
        if not folder.is_dir(): continue
        files = sorted((f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in PICS and not f.name.startswith(".")), key=lambda f: f.name.lower())
        stems = {f.stem for f in files}
        for f in files:
            m = re.match(r"(.+)-(480|800|1200)$", f.stem)
            if m and m.group(1) in stems: continue
            st = f.stat(); out.append(dict(f=rel(f), dir=d, group=title, name=f.name, kb=round(st.st_size / 1024), v=int(st.st_mtime)))
    return dict(ok=True, groups=[t for _, t in LIBRARY], files=out)

def thumb(p):
    st = p.stat(); key = hashlib.sha1(f"{rel(p)}|{st.st_mtime_ns}|{st.st_size}".encode()).hexdigest()[:16]
    for ext in (".jpg", ".png"):
        if (THUMBS / (key + ext)).exists(): return THUMBS / (key + ext)
    im = Image.open(p)
    if im.format == "JPEG": im.draft("RGB", (480, 480))
    im = ImageOps.exif_transpose(im); alpha = has_alpha(im); im = im.convert("RGBA" if alpha else "RGB"); im.thumbnail((240, 240), Image.LANCZOS)
    buf = io.BytesIO()
    if alpha: im.save(buf, "PNG", optimize=True)
    else: im.save(buf, "JPEG", quality=80, optimize=True)
    out = THUMBS / (key + (".png" if alpha else ".jpg")); write_atomic(out, buf.getvalue())
    return out


# ---------- http ----------

class Handler(SimpleHTTPRequestHandler):
    server_version = "DeckEditor/1"
    extensions_map = dict(SimpleHTTPRequestHandler.extensions_map, **{".webp": "image/webp", ".woff2": "font/woff2", ".woff": "font/woff", ".svg": "image/svg+xml",
                                                                    ".mjs": "text/javascript", ".js": "text/javascript", ".json": "application/json", ".pdf": "application/pdf"})

    def log_message(self, fmt, *args):
        if os.environ.get("DECK_EDITOR_LOG") or (args and str(args[0]).startswith("POST")) or (len(args) > 1 and str(args[1])[:1] in "45"):
            sys.stderr.write("%s  %s\n" % (time.strftime("%H:%M:%S"), fmt % args))

    def local(self, post=False):
        """Only this machine's browser, and only the editor's own page for anything that writes: another site open in the browser
        must not be able to save edits or start a build through a request to 127.0.0.1."""
        names = ("127.0.0.1", "localhost", "[::1]")
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0] if ":" in (self.headers.get("Host") or "") else (self.headers.get("Host") or "")
        if host not in names: return False
        origin = self.headers.get("Origin")
        if post and origin and urllib.parse.urlsplit(origin).hostname not in ("127.0.0.1", "localhost", "::1"): return False
        return True

    def send_bytes(self, data, ctype, status=200, cache="no-store"):
        self.send_response(status); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", cache); self.end_headers()
        if self.command != "HEAD": self.wfile.write(data)

    def send_json(self, obj, status=200): self.send_bytes(json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8", status)

    def end_headers(self):
        if not any(h.lower().startswith(b"cache-control") for h in getattr(self, "_headers_buffer", [])): self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def translate_path(self, path):
        p = safe_path(urllib.parse.urlsplit(path).path)
        return str(p) if p and p.is_file() else str(ROOT / ".nothing")

    def list_directory(self, path):
        self.send_error(404, "Not found"); return None

    def api(self, fn):
        try: self.send_json(fn())
        except Problem as e: self.send_json(dict(ok=False, error=str(e)), e.status)
        except Exception as e:
            sys.stderr.write(f"{type(e).__name__}: {e}\n")
            self.send_json(dict(ok=False, error=f"Внутренняя ошибка редактора: {type(e).__name__}: {e}"), 500)

    def do_GET(self):
        if not self.local(): return self.send_error(403, "Local use only")
        u = urllib.parse.urlsplit(self.path); q = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
        if u.path in ("/", "/index.html"): return self.send_bytes(UI.read_bytes(), "text/html; charset=utf-8")
        if u.path == "/api/pages": return self.api(api_pages)
        if u.path == "/api/library": return self.api(api_library)
        if u.path == "/api/picinfo": return self.api(lambda: api_picinfo(q))
        if u.path == "/api/status":
            return self.send_json(dict(ok=True, running=BUILD["running"], seconds=round(time.time() - BUILD["started"]) if BUILD["running"] else 0,
                                       last=(BUILD["lines"] or [""])[-1][:200], publish=publish_status()))
        if u.path == "/api/thumb":
            try:
                t = thumb(picture(q.get("f")))
                return self.send_bytes(t.read_bytes(), "image/png" if t.suffix == ".png" else "image/jpeg", cache="max-age=604800" if q.get("v") else "no-cache")
            except Problem as e: return self.send_error(e.status, "No such picture")
            except Exception as e: return self.send_error(500, type(e).__name__)
        if u.path.startswith("/api/"): return self.send_error(404, "Not found")
        return super().do_GET()

    def do_HEAD(self):
        if not self.local(): return self.send_error(403, "Local use only")
        return super().do_HEAD()

    def do_POST(self):
        if not self.local(post=True): return self.send_error(403, "Local use only")
        u = urllib.parse.urlsplit(self.path); q = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
        try: n = int(self.headers.get("Content-Length") or 0)
        except ValueError: n = -1
        if n < 0 or n > 80 * 1048576: return self.send_json(dict(ok=False, error="Файл слишком большой (больше 80 МБ)."), 413)
        data = self.rfile.read(n)
        if u.path == "/api/upload": return self.api(lambda: api_upload(q.get("name") or "foto", data))
        routes = {"/api/save": api_save, "/api/crop": api_crop, "/api/publish": api_publish}
        if u.path not in routes: return self.send_error(404, "Not found")
        if "application/json" not in (self.headers.get("Content-Type") or ""): return self.send_json(dict(ok=False, error="Ожидается JSON."), 415)
        try: body = json.loads(data.decode("utf-8")); assert isinstance(body, dict)
        except (ValueError, AssertionError): return self.send_json(dict(ok=False, error="Запрос не разобрать."), 400)
        return self.api(lambda: routes[u.path](body))

    def do_DELETE(self):
        if not self.local(post=True): return self.send_error(403, "Local use only")
        u = urllib.parse.urlsplit(self.path)
        if u.path != "/api/crop": return self.send_error(404, "Not found")
        try: n = int(self.headers.get("Content-Length") or 0); body = json.loads(self.rfile.read(n).decode("utf-8")); assert isinstance(body, dict)
        except (ValueError, AssertionError): return self.send_json(dict(ok=False, error="Запрос не разобрать."), 400)
        return self.api(lambda: api_uncrop(body))


class Server(ThreadingHTTPServer):
    daemon_threads = True; allow_reuse_address = True
    def handle_error(self, request, client_address):
        if not isinstance(sys.exc_info()[1], ConnectionError): super().handle_error(request, client_address)      # a browser dropping a request is not news

def main():
    try: srv = Server(("127.0.0.1", PORT), lambda *a, **k: Handler(*a, directory=str(ROOT), **k))
    except OSError as e: sys.exit(f"Порт {PORT} занят — редактор, похоже, уже запущен: http://127.0.0.1:{PORT}/  ({e})")
    print(f"Редактор колоды: http://127.0.0.1:{PORT}/   (правки → {EDITS}; остановить — Ctrl+C)", flush=True)
    try: srv.serve_forever()
    except KeyboardInterrupt: print("\nОстановлен.")

if __name__ == "__main__":
    main()
