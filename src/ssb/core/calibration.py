"""Ground calibration and thermal-vacuum (TVAC) test campaign models."""

from enum import Enum
from pydantic import BaseModel, Field
from ssb.core.catalog_meta import CatalogMeta


class CalibrationFacilityType(str, Enum):
    AMBIENT_CLEANROOM = "ambient_cleanroom"
    TVAC_OPTICAL = "tvac_optical"
    TVAC_CRYO_SPECTRAL = "tvac_cryo_spectral"
    TVAC_RF_MULTIPACTOR = "tvac_rf_multipactor"
    TVAC_LASER_PAT = "tvac_laser_pat"
    TVAC_TELECOM_NPR = "tvac_telecom_npr"


class PayloadCalibration(CatalogMeta):
    """Ground test & calibration campaign catalog entry for satellite payloads."""

    id: str
    name: str
    facility_type: CalibrationFacilityType
    test_center: str
    supplier_id: str
    supplier_name: str
    category: str = Field("optical", description="optical, spectrometer, sar, rf_comm, laser_comm, multipurpose")
    description: str = ""
    long_description: str = ""
    is_thermal_vacuum: bool = Field(False, description="True if performed in thermal vacuum chamber (TVAC)")
    vacuum_level_mbar: float = Field(1013.25, description="Chamber pressure in mbar (e.g. 1e-6 for TVAC)")
    temp_min_c: float = Field(20.0, description="Minimum thermal cycling temperature in °C")
    temp_max_c: float = Field(20.0, description="Maximum thermal cycling temperature in °C")
    duration_weeks: float = Field(..., ge=0.5, description="Duration of testing campaign in weeks")
    price_meur: float = Field(..., ge=0.0, description="Turnkey cost of facility and engineering team in M€")
    compatible_payload_types: list[str] = Field(default_factory=list)
    key_features: list[str] = Field(default_factory=list)
    measurements_performed: list[str] = Field(default_factory=list)
    radiometric_accuracy_pct: float = Field(5.0, description="Expected post-calibration radiometric/RF uncertainty in %")
    thermal_defocus_mitigated: bool = Field(False, description="Whether defocus vs thermal gradient is mapped")
    multipactor_qualification: bool = Field(False, description="Whether high-power RF arcing margin is qualified")
    image: str = "payload_optical_large.jpg"
    trl_level: int = 9

    @property
    def is_tvac(self) -> bool:
        return self.is_thermal_vacuum

    @property
    def cost_meur(self) -> float:
        return self.price_meur

    @property
    def facility_name(self) -> str:
        return self.test_center
