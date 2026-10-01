"""Image casting for the team deck and landing: review/cast.json maps slot ids (D01, S1…, H1…) to {file, pos}.
Produced by the image-casting workflow (catalogue → three casts → judge → per-slot verify); the generators fall back
to their built-in defaults for any slot that is missing."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
_P = ROOT / "review" / "cast.json"
CAST = json.loads(_P.read_text()) if _P.exists() else {}

def cast(slot, default_file, default_pos=""):
    """(file, object-position) for a slot; the default pair when the slot was not cast or the file is missing."""
    c = CAST.get(slot)
    if c and c.get("file") and (ROOT / c["file"]).exists():
        return c["file"], c.get("pos") or default_pos
    return default_file, default_pos
