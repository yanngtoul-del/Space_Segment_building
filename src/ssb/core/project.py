"""Launcher and project models."""

import hashlib
import json
from typing import Any
from pydantic import BaseModel, Field
from ssb.core.mission import MissionSpecification
from ssb.core.orbit import OrbitDefinition
from ssb.core.platform import PlatformBase, Equipment
from ssb.core.payload import (
    OpticalImagerPayload,
    SpectrometerPayload,
    SarPayload,
    OpticalCommPayload,
    QkdPayload,
    RadioCommPayload,
)


PayloadUnion = (
    OpticalImagerPayload
    | SpectrometerPayload
    | SarPayload
    | OpticalCommPayload
    | QkdPayload
    | RadioCommPayload
)


class LauncherOrbitCapacity(BaseModel):
    """Capacity of a launcher for a given orbit type/altitude."""

    orbit_type: str = Field(..., description="e.g. sso_500km, sso_700km, leo_inclined, gto, geo")
    max_payload_mass_kg: float = Field(..., ge=0.0)
    fairing_diameter_m: float = Field(..., ge=0.5)
    fairing_height_m: float = Field(..., ge=0.5)


class Launcher(BaseModel):
    """Launcher catalog entry."""

    id: str
    supplier_id: str
    supplier_name: str
    name: str
    launcher_type: str = Field(..., description="dedicated or rideshare")
    price_base_meur: float = Field(..., ge=0.0)
    price_per_kg_meur: float = Field(0.0, ge=0.0, description="Used mainly for rideshares")
    max_total_mass_kg: float = Field(..., ge=0.0)
    capacities: list[LauncherOrbitCapacity] = Field(default_factory=list)
    lead_time_months: int = Field(18, ge=1)
    trl: int = 9
    flight_heritage: str = ""


class SelectedOption(BaseModel):
    """Equipment chosen for a given slot on the platform."""

    slot_function: str
    equipment_id: str
    quantity: int = 1


class SystemConfiguration(BaseModel):
    """Complete system configuration built by the student."""

    orbit: OrbitDefinition = Field(default_factory=OrbitDefinition)
    platform_id: str | None = None
    selected_options: list[SelectedOption] = Field(default_factory=list)
    selected_payload_ids: list[str] = Field(default_factory=list)
    launcher_id: str | None = None


class StudentProject(BaseModel):
    """Persistent student project file."""

    schema_version: str = "1.0.0"
    project_id: str
    student_name: str
    student_id: str
    mission: MissionSpecification
    configuration: SystemConfiguration = Field(default_factory=SystemConfiguration)

    # Student written sections (for Word report)
    conops_text: str = ""
    justification_text: str = ""
    risk_analysis_text: str = ""
    tradeoffs_text: str = ""

    # Computed results cache (if any)
    last_computed_results: dict[str, Any] = Field(default_factory=dict)

    # Integrity hash (computed over mission + configuration + student info)
    integrity_hash: str = ""

    def compute_hash(self) -> str:
        """Compute deterministic SHA-256 hash of project critical contents."""
        data = {
            "schema_version": self.schema_version,
            "project_id": self.project_id,
            "student_id": self.student_id,
            "mission_id": self.mission.id,
            "config": self.configuration.model_dump(mode="json"),
        }
        canonical_json = json.dumps(data, sort_keys=True)
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    def update_integrity(self) -> None:
        self.integrity_hash = self.compute_hash()

    def verify_integrity(self) -> bool:
        return self.compute_hash() == self.integrity_hash
