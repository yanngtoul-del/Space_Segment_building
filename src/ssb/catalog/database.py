"""Catalog database and loader with schema validation."""

import json
from pathlib import Path
from typing import Any
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
    """In-memory catalog containing platforms, equipments, payloads, launchers."""

    def __init__(self) -> None:
        self.platforms: dict[str, PlatformBase] = {}
        self.equipments: dict[str, Equipment] = {}
        self.payloads: dict[str, PayloadUnion] = {}
        self.launchers: dict[str, Launcher] = {}

    def load_from_directory(self, catalog_dir: Path | str) -> None:
        """Load and cross-validate all JSON catalog files from directory."""
        cdir = Path(catalog_dir)

        # 1. Equipments first (referenced by platforms)
        eq_file = cdir / "equipment.json"
        if eq_file.exists():
            with open(eq_file, "r", encoding="utf-8") as f:
                items = json.load(f)
                for item in items:
                    eq = Equipment.model_validate(item)
                    self.equipments[eq.id] = eq

        # 2. Platforms
        pl_file = cdir / "platforms.json"
        if pl_file.exists():
            with open(pl_file, "r", encoding="utf-8") as f:
                items = json.load(f)
                for item in items:
                    p = PlatformBase.model_validate(item)
                    self.platforms[p.id] = p

        # 3. Payloads
        py_file = cdir / "payloads.json"
        if py_file.exists():
            with open(py_file, "r", encoding="utf-8") as f:
                items = json.load(f)
                for item in items:
                    pl = parse_payload(item)
                    self.payloads[pl.id] = pl

        # 4. Launchers
        ln_file = cdir / "launchers.json"
        if ln_file.exists():
            with open(ln_file, "r", encoding="utf-8") as f:
                items = json.load(f)
                for item in items:
                    ln = Launcher.model_validate(item)
                    self.launchers[ln.id] = ln

        self.validate_cross_references()

    def validate_cross_references(self) -> list[str]:
        """Verify that platform slots reference existing equipment IDs."""
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
        if errors:
            raise ValueError(f"Catalog cross-reference validation failed:\n" + "\n".join(errors))
        return errors
