import json, re, sys
from pathlib import Path

ROOT = Path(r"C:\Users\Lapto\PycharmProjects\Space_Segment_building")
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8")

names = set()
for f in ("payloads", "platforms", "equipment", "launchers", "calibrations"):
    for it in json.loads((ROOT / "data/catalogs" / f"{f}.json").read_text(encoding="utf-8")):
        names.add(it["name"].split(" ")[0])
names = {n for n in names if len(n) > 5 and re.search(r"[-0-9A-Z]", n[1:])}

for mf in sorted((ROOT / "data/missions").glob("*.mission.json")):
    txt = mf.read_text(encoding="utf-8")
    hits = sorted(n for n in names if n in txt)
    print(mf.name, "->", hits or "OK")

from ssb.catalog.database import CatalogDatabase
from ssb.catalog.datasheet import build_datasheet
from ssb.core.orbit import OrbitDefinition
db = CatalogDatabase(); db.load_from_directory(ROOT / "data/catalogs")
for pid in ("pl_opt_cubesat_6cm", "pl_opt_pan_compact", "pl_opt_helios_70cm"):
    ds = build_datasheet(db.payloads[pid], OrbitDefinition(altitude_km=500, inclination_deg=97.4))
    for sec in ds.sections:
        for k, v in sec.rows:
            if "Push-Broom" in k or "TDI" in k or "plan focal" in k or "Fréquence ligne" in k:
                print(pid, "|", k, "=", v)
