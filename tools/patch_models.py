"""One-off patch of model files (exact string replacement with assertions)."""
from pathlib import Path

root = Path("src/ssb")


def patch(rel: str, pairs: list[tuple[str, str]]) -> None:
    p = root / rel
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        assert old in s, (rel, old)
        s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8")


patch("core/platform.py", [
    ("from pydantic import BaseModel, Field\n", "from pydantic import BaseModel, Field\nfrom ssb.core.catalog_meta import CatalogMeta\n"),
    ("class Equipment(BaseModel):", "class Equipment(CatalogMeta):"),
    ("class PlatformBase(BaseModel):", "class PlatformBase(CatalogMeta):"),
    ("    description: str = \"\"\n    dry_mass_kg", "    description: str = \"\"\n    dimensions_mm: tuple[float, float, float] = (0.0, 0.0, 0.0)\n    deployed_span_m: float = Field(0.0, ge=0.0, description=\"Span with solar arrays deployed\")\n    dry_mass_kg"),
])
patch("core/payload.py", [
    ("from pydantic import BaseModel, Field\n", "from pydantic import Field\nfrom ssb.core.catalog_meta import CatalogMeta\n"),
    ("class BasePayload(BaseModel):", "class BasePayload(CatalogMeta):"),
])
patch("core/project.py", [
    ("from ssb.core.mission import", "from ssb.core.catalog_meta import CatalogMeta\nfrom ssb.core.mission import"),
    ("class Launcher(BaseModel):", "class Launcher(CatalogMeta):"),
    ("    launcher_type: str = Field(..., description=\"dedicated or rideshare\")\n", "    launcher_type: str = Field(..., description=\"dedicated or rideshare\")\n    description: str = \"\"\n    fairing_volume_m3: float = Field(0.0, ge=0.0)\n"),
])
print("ok")
