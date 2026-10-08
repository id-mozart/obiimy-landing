#!/usr/bin/env python3
"""«Опубликовать» on the Railway editor (DECK_EDITOR_PUBLISH): the built PDF is copied to data/published/deck.pdf, which the editor
serves without a password at /pub/deck.pdf and the site proxies as /obiimy-podarunky-dlia-komandy.pdf (server.js, EDITOR_PUB_URL)."""
import json, pathlib, shutil, sys, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / "obiimy-podarunky-dlia-komandy.pdf"
OUT = ROOT / "data" / "published"
if not PDF.exists(): sys.exit("Нет собранного PDF — сначала «Сохранить и собрать PDF».")
OUT.mkdir(parents=True, exist_ok=True)
tmp = OUT / "deck.pdf.tmp"; shutil.copy2(PDF, tmp); tmp.replace(OUT / "deck.pdf")
(OUT / "meta.json").write_text(json.dumps(dict(published=int(time.time()), size=PDF.stat().st_size, message=" ".join(sys.argv[1:])), ensure_ascii=False))
print(f"deck.pdf → data/published ({round(PDF.stat().st_size / 1048576, 1)} MB); сайт віддає його як /obiimy-podarunky-dlia-komandy.pdf")
