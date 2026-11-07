"""Orbit definition and state representation."""

from enum import Enum
import math
from pydantic import BaseModel, Field
from ssb.core.constants import (
    EARTH_RADIUS_KM,
    EARTH_MU_KM,
    EARTH_J2,
    SUN_MEAN_MOTION_RAD_S,
)


class OrbitType(str, Enum):
    SSO = "sso"
    CIRCULAR = "circular"
    ELLIPTIC = "elliptic"
    REPEAT_GROUND_TRACK = "repeat_ground_track"
    GEO = "geo"
    HEO_MOLNIYA = "heo_molniya"
    HEO_TUNDRA = "heo_tundra"


class OrbitDefinition(BaseModel):
    """User-specified orbit parameters."""

    orbit_type: OrbitType = OrbitType.SSO
    altitude_km: float = Field(500.0, ge=150.0, le=40_000.0)
    eccentricity: float = Field(0.0, ge=0.0, lt=1.0)
    inclination_deg: float = Field(97.4, ge=0.0, le=180.0)
    raan_deg: float = Field(0.0, ge=0.0, lt=360.0)
    arg_perigee_deg: float = Field(0.0, ge=0.0, lt=360.0)
    true_anomaly_deg: float = Field(0.0, ge=0.0, lt=360.0)

    # Specific for SSO:
    ltan_hours: float | None = Field(
        10.5, ge=0.0, lt=24.0, description="Local Time of Descending Node (hours)"
    )

    # Specific for repeat-ground-track:
    repeat_days: int | None = Field(None, ge=1, le=100)
    repeat_revolutions: int | None = Field(None, ge=1, le=2000)

    @property
    def semi_major_axis_km(self) -> float:
        return EARTH_RADIUS_KM + self.altitude_km

    @property
    def period_seconds(self) -> float:
        a = self.semi_major_axis_km
        return 2.0 * math.pi * math.sqrt(a**3 / EARTH_MU_KM)

    @property
    def period_minutes(self) -> float:
        return self.period_seconds / 60.0

    @property
    def mean_motion_rad_s(self) -> float:
        return 2.0 * math.pi / self.period_seconds

    @property
    def revolutions_per_day(self) -> float:
        return 86400.0 / self.period_seconds

    @classmethod
    def compute_sso_inclination(cls, altitude_km: float, eccentricity: float = 0.0) -> float:
        """Compute the inclination (in deg) required for Sun-Synchronous precession under J2.

        dOmega/dt = -3/2 * J2 * R_E^2 / (a * (1-e^2))^2 * n * cos(i) = n_sun
        => cos(i) = - 2/3 * n_sun / (J2 * R_E^2) * a^2 * (1-e^2)^2 / n
        """
        a = EARTH_RADIUS_KM + altitude_km
        n = math.sqrt(EARTH_MU_KM / (a**3))  # rad/s
        p = a * (1.0 - eccentricity**2)

        cos_i = - (2.0 / 3.0) * (SUN_MEAN_MOTION_RAD_S / (EARTH_J2 * (EARTH_RADIUS_KM**2))) * (p**2) / n
        if abs(cos_i) > 1.0:
            raise ValueError(f"SSO impossible at altitude {altitude_km} km (cos(i)={cos_i})")
        return math.degrees(math.acos(cos_i))
