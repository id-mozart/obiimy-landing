#!/bin/sh
# Start of the deck editor on Railway: everything the editor writes goes to the volume at /app/data, reached through links
# at the paths the editor and the builders know (photo/user, img/edit, review/deck-versions, review/lb/thumbs).
set -e
cd /app
for d in user edit versions thumbs published; do mkdir -p "data/$d"; done
[ -e photo/user ] && [ ! -L photo/user ] && rm -rf photo/user; ln -sfn /app/data/user photo/user
[ -e img/edit ] && [ ! -L img/edit ] && rm -rf img/edit; ln -sfn /app/data/edit img/edit
mkdir -p review/lb; ln -sfn /app/data/versions review/deck-versions; ln -sfn /app/data/thumbs review/lb/thumbs
[ -f data/deck-edits.json ] || printf '{"pages": {}, "hidden": [], "order": []}\n' > data/deck-edits.json
# the deck is rebuilt with the volume's edits before the editor opens, so the pages and the PDF match what was saved last
python3 src/build-deck-variants.py || echo "initial build failed — the editor opens with the image's build"
export DECK_EDITOR_PORT="${PORT:-8770}"
exec python3 src/deck-editor.py
