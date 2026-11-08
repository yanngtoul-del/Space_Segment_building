"""Equipment, Platform, Slots and Configuration models."""

from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
from ssb.core.catalog_meta import CatalogMeta


class SubsystemFunction(str, Enum):
    PROPULSION = "propulsion"
    TTC = "ttc"
    PAYLOAD_DOWNLINK = "payload_downlink"
    MASS_MEMORY = "mass_memory"
    ADCS = "adcs"
    EPS_SOLAR = "eps_solar"
    EPS_BATTERY = "eps_battery"
    OBC = "obc"
    THERMAL = "thermal"
    DEORBIT_DEVICE = "deorbit_device"
    OPTICAL_INTERFACE = "optical_interface"


class Equipment(CatalogMeta):
    """Generic catalog equipment belonging to a subsystem."""

    id: str
    supplier_id: str
    supplier_name: str
    name: str
    function: SubsystemFunction
    description: str = ""
    mass_kg: float = Field(..., ge=0.0)
    power_w: float = Field(0.0, ge=0.0, description="Average operational power consumption")
    peak_power_w: float = Field(0.0, ge=0.0)
    standby_power_w: float = Field(0.0, ge=0.0)
    volume_liters: float = Field(0.0, ge=0.0)
    dimensions_mm: tuple[float, float, float] = (0.0, 0.0, 0.0)
    price_meur: float = Field(..., ge=0.0, description="Base catalog price in M€")
    trl: int = Field(9, ge=1, le=9)
    flight_heritage: str = ""

    # Function-specific parameters (stored as key-value pairs or structured specs)
    specs: dict[str, Any] = Field(default_factory=dict)


class SlotRule(BaseModel):
    """Platform slot defining which equipment can be installed, quantity, and cost overrides."""

    function: SubsystemFunction
    allowed_equipment_ids: list[str] = Field(
        default_factory=list,
        description="Whitelist of equipment IDs allowed in this slot. Empty = none.",
    )
    included_equipment_ids: list[str] = Field(
        default_factory=list,
        description="Equipment included by default in the base platform price.",
    )
    min_qty: int = Field(0, ge=0)
    max_qty: int = Field(1, ge=0)
    exclusive_with: list[str] = Field(
        default_factory=list,
        description="List of equipment IDs or slot functions that cannot co-exist with this choice.",
    )
    requires: list[str] = Field(
        default_factory=list,
        description="List of equipment IDs or slot functions required if an option is picked.",
    )
    integration_cost_fixed_meur: float = Field(0.0, ge=0.0)
    integration_cost_pct: float = Field(0.0, ge=0.0, description="Percentage of equipment price")
    interface_mass_kg: float = Field(0.0, ge=0.0)
    lead_time_months_delta: int = Field(0, ge=0)

    # Local price/mass override per equipment ID on this platform
    equipment_overrides: dict[str, dict[str, float]] = Field(
        default_factory=dict,
        description="e.g. {'prop_chem_01': {'price_meur': 0.35, 'mass_kg': 8.5}}",
    )


class PlatformBase(CatalogMeta):
    """Platform base specifications (before options and payloads)."""

    id: str
    supplier_id: str
    supplier_name: str
    name: str
    category: str = Field(
        ..., description="e.g. cubesat_12u, smallsat_150kg, smallsat_500kg, medium_1500kg"
    )
    description: str = ""
    dimensions_mm: tuple[float, float, float] = (0.0, 0.0, 0.0)
    deployed_span_m: float = Field(0.0, ge=0.0, description="Span with solar arrays deployed")
    dry_mass_kg: float = Field(..., ge=0.0, description="Platform dry mass excluding options & payloads")
    max_payload_mass_kg: float = Field(..., ge=0.0)
    max_launch_mass_kg: float = Field(..., ge=0.0)
    payload_volume_liters: float = Field(..., ge=0.0)

    # Electrical power capability (available for payload + options)
    orbit_avg_power_w: float = Field(..., ge=0.0, description="Avg power generated on reference LEO orbit")
    payload_avg_power_w: float = Field(..., ge=0.0, description="Avg power reserved/available for payloads")
    payload_peak_power_w: float = Field(..., ge=0.0)
    bus_voltage_v: float = Field(28.0, ge=0.0)
    battery_capacity_wh: float = Field(..., ge=0.0)
    battery_max_dod: float = Field(0.3, ge=0.0, le=1.0)

    # Base ADCS capability
    pointing_accuracy_deg: float = Field(..., ge=0.0)
    pointing_stability_arcsec_s: float = Field(..., ge=0.0)
    slew_rate_deg_s: float = Field(..., ge=0.0)
    jitter_arcsec: float = Field(..., ge=0.0)

    # Thermal & mechanical
    payload_thermal_dissipation_w: float = Field(..., ge=0.0)
    launch_environment_compatible: list[str] = Field(default_factory=list)

    # Reliability & life
    design_lifetime_years: float = Field(5.0, ge=0.5)
    rad_tolerance_krad: float = Field(20.0, ge=0.0)

    # Commercial
    base_price_meur: float = Field(..., ge=0.0)
    base_lead_time_months: int = Field(12, ge=1)
    trl: int = Field(9, ge=1, le=9)

    # Slot definitions
    slots: list[SlotRule] = Field(default_factory=list)
