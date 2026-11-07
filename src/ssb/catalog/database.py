"""Catalog database and loader with schema validation and supplier index."""

import json
from pathlib import Path
from typing import Any
from ssb.core.catalog_meta import Supplier
from ssb.core.paths import catalogs_dir
from ssb.core.platform import PlatformBase, Equipment, SubsystemFunction
from ssb.core.payload import (
    BasePayload,
    OpticalImagerPayload,
    SpectrometerPayload,
    SarPayload,
    OpticalCommPayload,
    QkdPayload,
    RadioCommPayload,
    PayloadType,
)
from ssb.core.project import Launcher, PayloadUnion


def parse_payload(data: dict[str, Any]) -> PayloadUnion:
    """Parse raw dictionary into appropriate Payload subclass."""
    ptype = data.get("payload_type")
    match ptype:
        case PayloadType.OPTICAL_IMAGER | "optical_imager":
            return OpticalImagerPayload.model_validate(data)
        case PayloadType.SPECTROMETER | "spectrometer":
            return SpectrometerPayload.model_validate(data)
        case PayloadType.SAR | "sar":
            return SarPayload.model_validate(data)
        case PayloadType.OPTICAL_COMM | "optical_comm":
            return OpticalCommPayload.model_validate(data)
        case PayloadType.QKD | "qkd":
            return QkdPayload.model_validate(data)
        case PayloadType.RADIO_COMM | "radio_comm":
            return RadioCommPayload.model_validate(data)
        case _:
            raise ValueError(f"Unknown payload type: {ptype}")


class CatalogDatabase:
    """In-memory catalog containing suppliers, platforms, equipments, payloads, launchers."""

    def __init__(self) -> None:
        self.suppliers: dict[str, Supplier] = {}
        self.platforms: dict[str, PlatformBase] = {}
        self.equipments: dict[str, Equipment] = {}
        self.payloads: dict[str, PayloadUnion] = {}
        self.launchers: dict[str, Launcher] = {}

    def load_from_directory(self, catalog_dir: Path | str | None = None) -> None:
        """Load and cross-validate all JSON catalog files from directory."""
        cdir = Path(catalog_dir) if catalog_dir is not None else catalogs_dir()

        sup_file = cdir / "suppliers.json"
        if sup_file.exists():
            with open(sup_file, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    s = Supplier.model_validate(item)
                    self.suppliers[s.id] = s

        eq_file = cdir / "equipment.json"
        if eq_file.exists():
            with open(eq_file, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    eq = Equipment.model_validate(item)
                    self.equipments[eq.id] = eq

        pl_file = cdir / "platforms.json"
        if pl_file.exists():
            with open(pl_file, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    p = PlatformBase.model_validate(item)
                    self.platforms[p.id] = p

        py_file = cdir / "payloads.json"
        if py_file.exists():
            with open(py_file, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    pl = parse_payload(item)
                    self.payloads[pl.id] = pl

        ln_file = cdir / "launchers.json"
        if ln_file.exists():
            with open(ln_file, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    ln = Launcher.model_validate(item)
                    self.launchers[ln.id] = ln

        self.validate_cross_references()

    def suppliers_for(self, category: str) -> list[Supplier]:
        """Return suppliers active in a category ('platform', 'payload', 'equipment', 'launcher')."""
        return [s for s in self.suppliers.values() if category in s.categories]

    def items_by_supplier(self, supplier_id: str, category: str) -> list[Any]:
        pool: dict[str, Any] = {
            "platform": self.platforms,
            "payload": self.payloads,
            "equipment": self.equipments,
            "launcher": self.launchers,
        }[category]
        return [x for x in pool.values() if x.supplier_id == supplier_id]

    def validate_cross_references(self) -> list[str]:
        """Verify that platform slots reference existing equipment IDs and suppliers exist."""
        errors: list[str] = []
        for plat_id, plat in self.platforms.items():
            for slot in plat.slots:
                for eq_id in slot.allowed_equipment_ids:
                    if eq_id not in self.equipments:
                        errors.append(
                            f"Platform '{plat_id}' slot '{slot.function}' allows non-existent equipment '{eq_id}'"
                        )
                for inc_id in slot.included_equipment_ids:
                    if inc_id not in self.equipments:
                        errors.append(
                            f"Platform '{plat_id}' slot '{slot.function}' includes non-existent equipment '{inc_id}'"
                        )
        if self.suppliers:
            for kind, coll in [
                ("platform", self.platforms),
                ("payload", self.payloads),
                ("equipment", self.equipments),
                ("launcher", self.launchers),
            ]:
                for item_id, item in coll.items():
                    if item.supplier_id not in self.suppliers:
                        errors.append(f"{kind} '{item_id}' references unknown supplier '{item.supplier_id}'")
        if errors:
            raise ValueError("Catalog cross-reference validation failed:\n" + "\n".join(errors))
        return errors
