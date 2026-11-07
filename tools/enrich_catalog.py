"""Build enriched JSON catalogs + fallback illustration images."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "catalog_src"))
sys.path.insert(0, str(ROOT / "src"))

import suppliers_data  # noqa: E402
import equipment_data  # noqa: E402
import platforms_data  # noqa: E402
import payloads_data  # noqa: E402
import launchers_data  # noqa: E402
from ssb.catalog.database import CatalogDatabase  # noqa: E402

CAT = ROOT / "data" / "catalogs"
IMG = ROOT / "data" / "images"


def make_missing_images() -> None:
    """Generate clean technical illustration JPGs with matplotlib for the 6 missing files."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon

    specs = [
        ("equip_propulsion_micro.jpg", "Propulsion micro CubeSat (1U / gaz froid / PPT)", "#0d2238", "micro"),
        ("equip_electronics.jpg", "Équipement avionique & télécommunications RF/mémoire", "#0f2430", "elec"),
        ("equip_adcs.jpg", "Système de contrôle d'attitude (viseurs d'étoiles & roues / CMG)", "#141e30", "adcs"),
        ("launcher_rideshare.jpg", "Lancement partagé (Rideshare ESPA / Déployeur CubeSat)", "#101828", "ride"),
        ("launcher_rocket.jpg", "Lanceur orbital dédié (classe micro à médium)", "#0b1526", "rock"),
        ("launcher_heavy.jpg", "Lanceur lourd institutionnel sous coiffe 4,5 m", "#111827", "heavy"),
    ]
    for fname, title, bg, kind in specs:
        out = IMG / fname
        fig, ax = plt.subplots(figsize=(8, 6), dpi=130)
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 75)
        ax.axis("off")
        for x in range(0, 101, 5):
            ax.axvline(x, color="#1e3a5f", lw=0.4, alpha=0.5)
        for y in range(0, 76, 5):
            ax.axhline(y, color="#1e3a5f", lw=0.4, alpha=0.5)

        if kind == "micro":
            ax.add_patch(FancyBboxPatch((22, 18), 56, 38, boxstyle="round,pad=1", ec="#38bdf8", fc="#1e293b", lw=2))
            ax.add_patch(Circle((42, 37), 11, ec="#fbbf24", fc="#334155", lw=2))
            for dy in (-10, -3, 4, 11):
                ax.add_patch(Polygon([(78, 37 + dy), (86, 40 + dy), (86, 34 + dy)], closed=True, ec="#38bdf8", fc="#0ea5e9"))
            ax.text(42, 37, "TANK\nR236fa / PTFE", color="#f8fafc", ha="center", va="center", fontsize=9, fontweight="bold")
        elif kind == "elec":
            ax.add_patch(FancyBboxPatch((18, 16), 64, 42, boxstyle="round,pad=1", ec="#34d399", fc="#1e293b", lw=2))
            for i in range(4):
                ax.add_patch(Rectangle((24 + i * 14, 22), 10, 28, ec="#6ee7b7", fc="#0f172a", lw=1.2))
            for i in range(3):
                ax.add_patch(Circle((30 + i * 20, 58), 3, ec="#fbbf24", fc="#f59e0b"))
            ax.text(50, 12, "SpaceFibre / SpaceWire  •  EDAC  •  RF Stage", color="#a7f3d0", ha="center", fontsize=9)
        elif kind == "adcs":
            for cx, cy in ((32, 32), (52, 32), (42, 48)):
                ax.add_patch(Circle((cx, cy), 9, ec="#60a5fa", fc="#1e293b", lw=2))
                ax.add_patch(Circle((cx, cy), 3, ec="#93c5fd", fc="#3b82f6"))
            ax.add_patch(Polygon([(68, 24), (84, 18), (84, 46), (68, 40)], closed=True, ec="#fbbf24", fc="#334155", lw=2))
            ax.text(76, 52, "Viseur d'étoiles", color="#fde68a", ha="center", fontsize=8.5)
            ax.text(42, 16, "Roues à réaction / CMG 3 axes", color="#bfdbfe", ha="center", fontsize=8.5)
        elif kind == "ride":
            ax.add_patch(Circle((50, 38), 16, ec="#38bdf8", fc="#1e293b", lw=3))
            ax.add_patch(Circle((50, 38), 10, ec="#64748b", fc=bg, lw=1.5))
            import math
            for k in range(6):
                ang = k * math.pi / 3
                px, py = 50 + 25 * math.cos(ang), 38 + 22 * math.sin(ang)
                ax.add_patch(FancyBboxPatch((px - 5, py - 4), 10, 8, boxstyle="round,pad=0.4", ec="#fbbf24", fc="#334155", lw=1.5))
            ax.text(50, 38, "ESPA\nRING", color="#e2e8f0", ha="center", va="center", fontsize=9, fontweight="bold")
        elif kind in ("rock", "heavy"):
            w = 12 if kind == "rock" else 18
            ax.add_patch(Rectangle((50 - w / 2, 12), w, 38, ec="#e2e8f0", fc="#334155", lw=2))
            ax.add_patch(Polygon([(50 - w / 2, 50), (50, 66), (50 + w / 2, 50)], closed=True, ec="#38bdf8", fc="#1e293b", lw=2))
            if kind == "heavy":
                for sx in (50 - w / 2 - 7, 50 + w / 2 + 1):
                    ax.add_patch(Rectangle((sx, 12), 6, 30, ec="#f59e0b", fc="#475569", lw=1.5))
            ax.add_patch(Circle((50, 55), w * 0.28, ec="#fbbf24", fc="#0ea5e9", alpha=0.8))

        ax.text(50, 70, title, color="#f8fafc", ha="center", va="center", fontsize=11, fontweight="bold")
        ax.text(50, 4, "Illustration technique indicative — Space Segment Builder", color="#94a3b8", ha="center", fontsize=8)
        fig.savefig(out, dpi=130, bbox_inches="tight", facecolor=bg)
        plt.close(fig)


def merge_list(existing: list[dict], overlays: dict[str, dict], new_items: list[dict], is_platform: bool = False) -> list[dict]:
    by_id = {x["id"]: x for x in existing}
    for item_id, ov in overlays.items():
        target = by_id[item_id]
        if is_platform:
            ov = dict(ov)
            slot_add = ov.pop("slot_additions", {})
            extra_slots = ov.pop("extra_slots", [])
            target.update(ov)
            slots_by_fn = {s["function"]: s for s in target["slots"]}
            for fn, eq_ids in slot_add.items():
                for eid in eq_ids:
                    if eid not in slots_by_fn[fn]["allowed_equipment_ids"]:
                        slots_by_fn[fn]["allowed_equipment_ids"].append(eid)
            for es in extra_slots:
                if es["function"] not in slots_by_fn:
                    target["slots"].append(es)
        else:
            target.update(ov)
    out = list(existing)
    existing_ids = set(by_id)
    for ni in new_items:
        if ni["id"] in existing_ids:
            # replace in place if re-running
            idx = next(i for i, x in enumerate(out) if x["id"] == ni["id"])
            out[idx] = ni
        else:
            out.append(ni)
    return out


def main() -> None:
    make_missing_images()

    with open(CAT / "suppliers.json", "w", encoding="utf-8") as f:
        json.dump(suppliers_data.SUPPLIERS, f, ensure_ascii=False, indent=2)

    for fname, mod, is_plat in [
        ("equipment.json", equipment_data, False),
        ("platforms.json", platforms_data, True),
        ("payloads.json", payloads_data, False),
        ("launchers.json", launchers_data, False),
    ]:
        p = CAT / fname
        cur = json.loads(p.read_text(encoding="utf-8"))
        # keep only original items before merging so script is idempotent
        orig_ids = set(mod.OVERLAY.keys())
        base_items = [x for x in cur if x["id"] in orig_ids]
        merged = merge_list(base_items, mod.OVERLAY, mod.NEW, is_platform=is_plat)
        p.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")

    db = CatalogDatabase()
    db.load_from_directory(CAT)
    print(
        f"Loaded: {len(db.suppliers)} suppliers, {len(db.platforms)} platforms, "
        f"{len(db.payloads)} payloads, {len(db.equipments)} equipments, {len(db.launchers)} launchers"
    )
    missing_imgs = []
    for coll in (db.platforms, db.payloads, db.equipments, db.launchers):
        for item in coll.values():
            if not item.image or not (IMG / item.image).exists():
                missing_imgs.append((item.id, item.image))
            assert item.description and item.long_description, f"Missing text on {item.id}"
    assert not missing_imgs, f"Missing images: {missing_imgs}"


if __name__ == "__main__":
    main()
