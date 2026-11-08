"""Pydantic models for mission requirements, constraints, and rich mission specification sheets."""

from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class RequirementType(str, Enum):
    PAYLOAD_PERF = "payload_perf"
    ORBIT = "orbit"
    DATA_VOLUME = "data_volume"
    LATENCY = "latency"
    LIFETIME = "lifetime"
    REVISIT = "revisit"
    BUDGET = "budget"
    LAUNCHER = "launcher"
    REGULATORY = "regulatory"
    GEORETURN = "georeturn"


class RequirementOperator(str, Enum):
    LE = "<="
    GE = ">="
    EQ = "=="
    LT = "<"
    GT = ">"
    CONTAINS = "contains"


class MissionRequirement(BaseModel):
    """A quantified mission requirement with an ID and verification rule."""

    id: str = Field(..., description="Unique requirement ID, e.g. REQ-PL-01")
    title: str = Field(..., description="Short human-readable requirement title")
    description: str = Field(..., description="Full requirement text")
    req_type: RequirementType = Field(..., description="Category of requirement")
    parameter: str = Field(..., description="Internal system metric key to check")
    operator: RequirementOperator = Field(..., description="Comparison operator")
    threshold: float | str | list[str] = Field(
        ..., description="Acceptable threshold value (pass/fail)"
    )
    goal: float | str | None = Field(
        None, description="Optional target/goal value beyond threshold"
    )
    unit: str = Field("", description="Display unit, e.g. m, km, W, kg, M€, h")
    weight: float = Field(1.0, ge=0.0, description="Relative weight for score")


class GroundStationTarget(BaseModel):
    """Ground station available for the mission."""

    id: str
    name: str
    latitude_deg: float
    longitude_deg: float
    altitude_m: float = 0.0
    min_elevation_deg: float = 5.0
    bands_supported: list[str] = Field(default_factory=lambda: ["S", "X"])
    cost_per_pass_eur: float = 0.0
    cost_per_minute_eur: float = 0.0


class TargetZone(BaseModel):
    """Geographic zone of interest for coverage/revisit."""

    id: str
    name: str
    points_lat_lon: list[tuple[float, float]] = Field(
        default_factory=list,
        description="Polygon vertices [(lat, lon), ...] or single point",
    )
    priority: int = 1


class GeoReturnConstraint(BaseModel):
    """Geographical return (juste retour géographique) constraint as enforced in ESA programmes.

    Sets industrial spending percentage targets per member state without imposing specific equipment types.
    """

    country: str = Field(..., description="Target member state, e.g. France, Allemagne, Italie, Espagne")
    min_pct: float = Field(..., ge=0.0, le=100.0, description="Minimum industrial spend percentage (e.g. 25.0 %)")
    max_pct: float = Field(..., ge=0.0, le=100.0, description="Maximum industrial spend percentage (e.g. 45.0 %)")
    rationale: str = Field("", description="Justification based on national subscription / programmatic share")


class MissionSpecification(BaseModel):
    """Complete mission specification sheet (fiche de spécification mission) provided to the student."""

    schema_version: str = "1.0.0"
    id: str
    title: str
    context: str
    mission_type: str = Field(
        ..., description="e.g. optical_eo, sar_eo, telecom_opt, telecom_radio, qkd, science, atmosphere, cosmology"
    )
    max_budget_meur: float = Field(..., description="Total budget ceiling in M€ (platform + options + payloads + launch)")
    target_lifetime_years: float = Field(5.0, ge=0.5)

    # Visual illustration & rich specification sheet fields
    image: str = Field("", description="Illustration image filename in data/images")
    client_agency: str = Field(
        "Agence Spatiale / Institution",
        description="Sponsoring agency or client organization",
    )
    domain_label: str = Field(
        "",
        description="Human-readable mission domain (Observation de la Terre, Cosmologie, Atmosphère, Télécom haut débit...)",
    )
    primary_objective: str = Field(
        "",
        description="Detailed narrative of the primary scientific, operational, or data-throughput objective",
    )
    secondary_objectives: list[str] = Field(
        default_factory=list,
        description="Secondary or bonus mission objectives",
    )
    scientific_or_operational_need: str = Field(
        "",
        description="Why this mission is needed, end-users, and expected products/data volume",
    )
    orbit_constraints_description: str = Field(
        "",
        description="Orbital regime guidance or constraints (altitude range, SSO LTAN, inclination, revisit)",
    )
    conops_guidance: str = Field(
        "",
        description="Expected operational concept (duty cycle, target passes, downlink strategy, eclipse operation)",
    )
    deliverables_expected: list[str] = Field(
        default_factory=list,
        description="Questions and trade-offs the student must justify in the final report",
    )

    allowed_suppliers: list[str] = Field(
        default_factory=list,
        description="If non-empty, whitelist of allowed supplier IDs",
    )
    min_trl: int = Field(6, ge=1, le=9, description="Minimum TRL accepted")
    requirements: list[MissionRequirement] = Field(default_factory=list)
    ground_stations: list[GroundStationTarget] = Field(default_factory=list)
    target_zones: list[TargetZone] = Field(default_factory=list)
    geo_return_constraints: list[GeoReturnConstraint] = Field(
        default_factory=list,
        description="ESA-style geographic return constraints (ranges of industrial spending per country)",
    )
    max_non_esa_spend_pct: float = Field(
        15.0,
        ge=0.0,
        le=100.0,
        description="Plafond autorisé pour les achats industriels hors États membres ESA (pays tiers COTS mondiaux, max 15 %)",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)
